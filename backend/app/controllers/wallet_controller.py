"""
backend/app/controllers/wallet_controller.py

Register in main.py:
    from app.controllers.wallet_controller import router as wallet_router
    app.include_router(wallet_router, prefix="/api/v1/wallet", tags=["Wallet"])
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.core import security_log
from app.core.authz import require_admin
from app.core.security import get_current_user
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage, PaymentMethod
from app.services.wallet.wallet_service import (
    get_or_create_wallet, add_credits, expire_promo_credits_if_due, CREDIT_COSTS,
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
    user_id: int = Field(..., gt=0)
    # Bounded on both ends: a grant is a credit *issue*, not an arbitrary
    # balance write, so a negative value (a silent debit) and an absurd
    # positive one are both rejected rather than trusted.
    credits: int = Field(..., gt=0, le=100_000)
    description: str = Field("Admin grant", max_length=200)


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
    return WalletResponse(
        credit_balance=wallet.credit_balance,
        lifetime_purchased=wallet.lifetime_purchased,
        lifetime_spent=wallet.lifetime_spent,
        promo_credits_remaining=wallet.promo_credits_remaining or 0,
        promo_expires_at=wallet.promo_expires_at.isoformat() if wallet.promo_expires_at else None,
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
    return db.query(CreditPackage).filter(CreditPackage.is_active == True).all()


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

    wallet = db.query(UserWallet).filter(UserWallet.id == tx.wallet_id).with_for_update().one()
    wallet.credit_balance     += tx.credits
    wallet.lifetime_purchased += tx.credits
    tx.status = "confirmed"
    tx.balance_after = wallet.credit_balance

    db.commit()
    security_log.admin_action(
        admin_id=current_user.id, action="wallet.confirm_payment", target=payment_ref,
    )
    return {
        "message": "Payment confirmed. Credits released.",
        "credits_added": tx.credits,
        "new_balance": wallet.credit_balance,
    }


@router.post("/admin/grant")
def admin_grant(
    payload: AdminGrantRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: grant free credits to any user."""
    if not db.query(User.id).filter(User.id == payload.user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    wallet = add_credits(
        user_id=payload.user_id,
        credits=payload.credits,
        db=db,
        payment_method="admin",
        description=payload.description,
        transaction_type="bonus",
    )
    security_log.admin_action(
        admin_id=current_user.id, action="wallet.grant_credits",
        target=f"user={payload.user_id} credits={payload.credits}",
    )
    return {"message": "Credits granted.", "new_balance": wallet.credit_balance}