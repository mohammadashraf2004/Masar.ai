"""
backend/app/controllers/wallet_controller.py

Register in main.py:
    from app.controllers.wallet_controller import router as wallet_router
    app.include_router(wallet_router, prefix="/api/v1/wallet", tags=["Wallet"])
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.db.session import get_db
from app.core import security_log
from app.core.authz import require_admin
from app.core.security import get_current_user
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage, PaymentMethod, TransactionStatus, TransactionType
from app.services.wallet import credit_purchases
from app.services.wallet.wallet_service import (
    get_or_create_wallet, add_credits, confirm_pending_topup,
    expire_promo_credits_if_due, CREDIT_COSTS,
)

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────
class WalletResponse(BaseModel):
    credit_balance: int
    lifetime_purchased: int
    lifetime_spent: int
    # Read-only, server-computed. Lets the UI say "480 free credits, 22
    # days left" without the client ever being able to set either value.
    promo_credits_remaining: int = 0
    promo_expires_at: Optional[str] = None
    # The balance, split by where it came from. `purchased_credits` were bought: they never
    # expire and are untouched by plan changes. `included_credits` is the rest (signup and
    # promo credits). The two always add up to `credit_balance`.
    purchased_credits: int = 0
    included_credits: int = 0

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    transaction_type: str
    status: str
    credits: int
    egp_amount: Optional[float]
    payment_method: Optional[str]
    payment_ref: Optional[str]
    description: str
    action_type: Optional[str]
    balance_after: int
    created_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            transaction_type=obj.transaction_type.value,
            status=obj.status.value,
            credits=obj.credits,
            egp_amount=obj.egp_amount,
            payment_method=obj.payment_method.value if obj.payment_method else None,
            payment_ref=obj.payment_ref,
            description=obj.description,
            action_type=obj.action_type,
            balance_after=obj.balance_after,
            created_at=obj.created_at.isoformat(),
        )


class PackageResponse(BaseModel):
    id: int
    code: Optional[str] = None
    name: str
    credits: int
    egp_price: float
    bonus_credits: int
    is_popular: bool
    description: Optional[str]

    class Config:
        from_attributes = True


class TopUpRequest(BaseModel):
    package_id: int = Field(..., gt=0)
    payment_method: str = Field(..., max_length=32)   # "fawry" | "instapay" | "vodafone_cash"
    payment_ref: str = Field(..., min_length=3, max_length=100)  # reference from the payment provider


class AdminGrantRequest(BaseModel):
    """Identify the recipient by email or by id — exactly one.

    Email is what an operator actually has in front of them: a support
    thread, a receipt, a message. Requiring the internal id meant looking it
    up in the database first, which is how a one-step action became three.
    The id path stays for callers that already resolved it.
    """
    user_id: Optional[int] = Field(None, gt=0)
    email: Optional[EmailStr] = None
    # Bounded on both ends: a grant is a credit *issue*, not an arbitrary
    # balance write, so a negative value (a silent debit) and an absurd
    # positive one are both rejected rather than trusted.
    credits: int = Field(..., gt=0, le=100_000)
    description: str = Field("Admin grant", max_length=200)

    @model_validator(mode="after")
    def exactly_one_identifier(self) -> "AdminGrantRequest":
        if (self.user_id is None) == (self.email is None):
            raise ValueError("Provide exactly one of user_id or email")
        return self


class AdminUserLookupResponse(BaseModel):
    """The minimum needed to confirm you are crediting the right person."""
    user_id: int
    email: str
    full_name: str
    credit_balance: int


def _resolve_grant_target(payload: AdminGrantRequest, db: Session) -> User:
    """Find the recipient, by whichever identifier was supplied.

    Email is matched case-insensitively: addresses are stored as the user
    typed them at registration, and an operator copying one out of a support
    thread should not have to reproduce its capitalisation.
    """
    if payload.user_id is not None:
        user = db.query(User).filter(User.id == payload.user_id).first()
    else:
        user = db.query(User).filter(
            func.lower(User.email) == payload.email.lower()
        ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=WalletResponse)
def get_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wallet = get_or_create_wallet(current_user.id, db)
    # Sweep here too, so a user who only ever opens the wallet screen sees
    # a truthful balance rather than one that shrinks on their next action.
    expire_promo_credits_if_due(wallet, db)
    purchased = min(wallet.purchased_credits or 0, wallet.credit_balance or 0)
    return WalletResponse(
        credit_balance=wallet.credit_balance,
        lifetime_purchased=wallet.lifetime_purchased,
        lifetime_spent=wallet.lifetime_spent,
        promo_credits_remaining=wallet.promo_credits_remaining or 0,
        promo_expires_at=wallet.promo_expires_at.isoformat() if wallet.promo_expires_at else None,
        purchased_credits=purchased,
        included_credits=(wallet.credit_balance or 0) - purchased,
    )


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wallet = get_or_create_wallet(current_user.id, db)
    txs = (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet.id)
        .order_by(WalletTransaction.created_at.desc())
        .limit(limit)
        .all()
    )
    return [TransactionResponse.from_orm(tx) for tx in txs]


@router.get("/packages", response_model=List[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    return credit_purchases.active_packs(db)


@router.get("/purchases")
def my_purchases(
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """The learner's credit purchases and where each stands: pending, paid, expired,
    failed, refunded or charged back. Only what a verified provider notice (or staff)
    recorded - a redirect back from the checkout never moves an order."""
    wallet = get_or_create_wallet(current_user.id, db)
    return {"orders": credit_purchases.orders_for_wallet(db, wallet.id, limit)}


@router.get("/costs")
def get_credit_costs():
    """Returns the credit cost for each AI action."""
    return {
        "costs": CREDIT_COSTS,
        "description": {
            "mentor_chat":    "Send a message to the AI mentor",
            "code_review":    "Submit code for AI review",
            "skill_gap":      "Run a skill gap analysis",
            "mock_interview": "Get a mock interview question",
            "exam_grading":   "AI grading of a short-answer exam question",
            "roadmap":        "Generate a learning roadmap",
        }
    }


@router.post("/topup")
def request_topup(
    payload: TopUpRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit a top-up request. Creates a PENDING transaction.
    Admin confirms it via /admin/confirm or a webhook confirms automatically.
    """
    package = db.query(CreditPackage).filter(
        CreditPackage.id == payload.package_id,
        CreditPackage.is_active == True,
    ).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    if payload.payment_method not in [m.value for m in PaymentMethod]:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    total_credits = package.credits + package.bonus_credits

    wallet = add_credits(
        user_id=current_user.id,
        credits=total_credits,
        db=db,
        egp_amount=package.egp_price,
        payment_method=payload.payment_method,
        payment_ref=payload.payment_ref,
        description=f"{package.name} package — {payload.payment_method.replace('_', ' ').title()}",
        status="pending",       # pending until admin/webhook confirms
        transaction_type="topup",
    )

    return {
        "message": "Top-up request submitted. Credits will be added after payment confirmation.",
        "package": package.name,
        "credits_pending": total_credits,
        "egp_paid": package.egp_price,
        "payment_ref": payload.payment_ref,
        "current_balance": wallet.credit_balance,
    }


@router.post("/admin/confirm/{payment_ref}")
def confirm_payment(
    payment_ref: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Admin endpoint: confirm a pending payment and release credits.
    In production this would be called by a Fawry/InstaPay webhook.

    Authorization is the require_admin dependency, not an inline role
    string comparison — see app/core/authz.py for why.
    """
    tx = db.query(WalletTransaction).filter(
        WalletTransaction.payment_ref == payment_ref,
        WalletTransaction.status == "pending",
    ).with_for_update().first()
    if not tx:
        raise HTTPException(status_code=404, detail="Pending transaction not found")

    # Same authoritative payout path as the payment webhooks — see
    # wallet_service.confirm_pending_topup. It takes the wallet row lock
    # and is idempotent on a row that is no longer pending.
    wallet = confirm_pending_topup(tx, db)
    security_log.admin_action(
        admin_id=current_user.id, action="wallet.confirm_payment", target=payment_ref,
    )
    return {
        "message": "Payment confirmed. Credits released.",
        "credits_added": tx.credits,
        "new_balance": wallet.credit_balance,
    }


class AdminReverseRequest(BaseModel):
    """Staff reconciliation of a credit purchase the provider refunded or charged back
    outside Masar (a dashboard refund, a bank dispute)."""
    model_config = ConfigDict(extra="forbid")
    kind: Literal["refund", "chargeback"]
    # The provider's refund / dispute id: makes the call safe to repeat.
    idempotency_key: str = Field(..., min_length=6, max_length=80)
    # Defaults to everything not yet reversed.
    amount_egp: Optional[float] = Field(None, gt=0, le=1_000_000)
    note: Optional[str] = Field(None, max_length=120)


@router.post("/admin/purchases/{reference}/reverse")
def admin_reverse_purchase(
    reference: str,
    payload: AdminReverseRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: take back the credits of a refunded or charged-back purchase. Capped at the
    purchased credits the learner still holds, so it can never create a negative balance;
    what was already spent is reported as `unrecovered`."""
    order = db.query(WalletTransaction).filter(
        WalletTransaction.payment_ref == reference,
        WalletTransaction.transaction_type == TransactionType.topup,
    ).with_for_update().first()
    if order is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    paid_minor = round(float(order.egp_amount or 0) * 100)
    already_minor = sum(
        round(float(r.egp_amount or 0) * 100) for r in db.query(WalletTransaction).filter(
            WalletTransaction.transaction_type == TransactionType.reversal,
            WalletTransaction.related_tx_id == order.id,
        )
    )
    amount_minor = round(payload.amount_egp * 100) if payload.amount_egp is not None else paid_minor - already_minor
    try:
        result = credit_purchases.reverse_purchase(
            db, order, amount_minor=amount_minor, event_id=f"admin:{payload.idempotency_key}",
            kind=payload.kind, note=payload.note,
        )
    except credit_purchases.ReversalRejected as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail=exc.code)
    security_log.admin_action(
        admin_id=current_user.id, action=f"wallet.purchase_{payload.kind}", target=f"{reference} {result['status']}",
    )
    return result


@router.get("/admin/user-lookup", response_model=AdminUserLookupResponse)
def admin_user_lookup(
    email: EmailStr = Query(..., description="The account's sign-in address"),
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: resolve an email to a user and their current balance.

    Read-only, and its purpose is to make the grant below safe: an operator
    sees the name and current balance of the person they are about to credit
    before committing, instead of discovering the typo afterwards.
    """
    user = db.query(User).filter(func.lower(User.email) == email.lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    wallet = get_or_create_wallet(user.id, db)
    return AdminUserLookupResponse(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        credit_balance=wallet.credit_balance,
    )


@router.post("/admin/grant")
def admin_grant(
    payload: AdminGrantRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: grant free credits to any user, by email or by id."""
    user = _resolve_grant_target(payload, db)

    wallet = add_credits(
        user_id=user.id,
        credits=payload.credits,
        db=db,
        payment_method="admin",
        description=payload.description,
        transaction_type="bonus",
    )
    # The resolved id is what goes in the audit line, never the email the
    # caller happened to type — the log has to name the account that was
    # actually credited.
    security_log.admin_action(
        admin_id=current_user.id, action="wallet.grant_credits",
        target=f"user={user.id} credits={payload.credits}",
    )
    return {
        "message": "Credits granted.",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "credits_granted": payload.credits,
        "new_balance": wallet.credit_balance,
    }