"""
backend/app/controllers/payments_controller.py

Payment initiation for wallet top-ups and exam fees, and the provider webhooks
that settle every kind of order (subscriptions, course purchases, top-ups, exam
fees). New payments are Kashier hosted checkouts (app/services/payments/checkout.py).
Paymob is no longer initiated; its webhook stays so the orders it already took
still reconcile their payments and refunds.

The webhooks are the ONLY path that marks a payment confirmed. The routes the
shopper's browser returns to are purely cosmetic: a redirect can be skipped,
replayed or forged; a signed server-to-server webhook, confirmed against the
provider's own record, cannot.

Register in main.py:
    from app.controllers.payments_controller import router as payments_router
    app.include_router(payments_router, prefix="/api/v1/payments", tags=["Payments"])
"""
import uuid
from urllib.parse import quote
from typing import Literal

import httpx
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core import security_log
from app.core.config import settings
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction, TransactionStatus, TransactionType, CreditPackage, PaymentMethod
from app.models.challenge import ExamPayment
from app.models.billing import BillingOrder, SubscriptionOrder
from app.models.exam import Exam
from app.core.security import get_current_user
from app.services.wallet import credit_purchases
from app.services.wallet.wallet_service import get_or_create_wallet
from app.services.payments import kashier_service, paymob_service
from app.services.payments.checkout import language_of, payments_gate, start_checkout
from app.services.payments.settlement import settle_notice

from app.controllers.exam_payment_controller import EXAM_PRICE_EGP

router = APIRouter()


class InitPaymentRequest(BaseModel):
    # Which method the shopper prefers. Kashier's hosted page offers every
    # enabled method (card, mobile wallet) itself, so no phone number is taken here.
    method: Literal["card", "wallet"] = "card"
    # Accepted for older clients and ignored (Kashier's page collects it).
    phone_number: str | None = Field(None, min_length=6, max_length=20, pattern=r"^\+?[0-9]{6,19}$")


class WalletTopUpInitRequest(InitPaymentRequest):
    package_id: int = Field(..., gt=0)


class ExamPaymentInitRequest(InitPaymentRequest):
    exam_id: int = Field(..., gt=0)


def _new_merchant_order_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


# ─── Wallet top-up ──────────────────────────────────────────────────────────

@router.post("/wallet/topup/init", dependencies=[Depends(payments_gate)])
@limiter.limit("10/minute")
def init_wallet_topup(
    request: Request,
    payload: WalletTopUpInitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    package = db.query(CreditPackage).filter(
        CreditPackage.id == payload.package_id,
        CreditPackage.is_active == True,
    ).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    merchant_order_id = _new_merchant_order_id("wallet")
    total_credits = package.credits + (package.bonus_credits or 0)

    wallet = get_or_create_wallet(current_user.id, db)
    # An abandoned checkout must not block a new one forever, and a learner cannot
    # stack up an unbounded number of unpaid orders.
    credit_purchases.release_stale_orders(db, wallet.id)
    db.commit()
    if credit_purchases.open_order_count(db, wallet.id) >= credit_purchases.MAX_OPEN_ORDERS:
        raise HTTPException(
            status_code=429,
            detail="You already have unpaid credit orders open. Finish or wait for them to expire before starting another.",
        )
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.topup,
        status=TransactionStatus.pending,
        credits=total_credits,
        egp_amount=package.egp_price,
        payment_method=PaymentMethod(payload.method if payload.method == "card" else "vodafone_cash"),
        payment_ref=merchant_order_id,
        description=f"{package.name} package — Kashier",
        balance_after=wallet.credit_balance,
        package_id=package.id,
    )
    db.add(tx)
    db.commit()

    try:
        result = start_checkout(
            kind="wallet_topup", amount_minor=round(float(package.egp_price) * 100), currency="EGP",
            merchant_order_id=merchant_order_id, user=current_user,
            description=f"Masar credits: {package.name}", language=language_of(request),
        )
    except HTTPException:
        tx.status = TransactionStatus.failed
        db.commit()
        raise
    tx.provider_order_id = result["provider_order_id"]
    db.commit()
    return {"checkout_url": result["checkout_url"], "merchant_order_id": merchant_order_id,
            "reference": merchant_order_id}


# ─── Exam fee ────────────────────────────────────────────────────────────────

@router.post("/exam/init", dependencies=[Depends(payments_gate)])
@limiter.limit("10/minute")
def init_exam_payment(
    request: Request,
    payload: ExamPaymentInitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == payload.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    existing = db.query(ExamPayment).filter(
        ExamPayment.user_id == current_user.id,
        ExamPayment.exam_id == payload.exam_id,
        ExamPayment.status == "confirmed",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have confirmed payment for this exam")

    merchant_order_id = _new_merchant_order_id(f"exam{payload.exam_id}")
    payment = ExamPayment(
        user_id=current_user.id,
        exam_id=payload.exam_id,
        egp_amount=EXAM_PRICE_EGP,
        payment_method="kashier",
        payment_ref=merchant_order_id,
        status="pending",
    )
    db.add(payment)
    db.commit()

    try:
        result = start_checkout(
            kind="exam_payment", amount_minor=round(float(EXAM_PRICE_EGP) * 100), currency="EGP",
            merchant_order_id=merchant_order_id, user=current_user,
            description=f"Masar certification exam #{payload.exam_id}", language=language_of(request),
        )
    except HTTPException:
        payment.status = "failed"
        db.commit()
        raise
    payment.provider_order_id = result["provider_order_id"]
    db.commit()
    return {"checkout_url": result["checkout_url"], "merchant_order_id": merchant_order_id}


# ─── Status polling (for the frontend post-checkout page) ───────────────────

@router.get("/status/{merchant_order_id}")
def get_payment_status(
    merchant_order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Read-only status check by merchant_order_id, scoped to the
    requesting user — only ever reflects what a webhook has actually
    confirmed, never what a browser redirect claims."""
    tx = db.query(WalletTransaction).join(UserWallet).filter(
        WalletTransaction.payment_ref == merchant_order_id,
        UserWallet.user_id == current_user.id,
    ).first()
    if tx:
        # `status` is the settlement state ("pending" | "confirmed" | "failed"); `order` is the
        # learner-facing state of a credit purchase (paid, refunded, expired...).
        order = credit_purchases.order_by_reference(db, tx.wallet_id, merchant_order_id) \
            if tx.transaction_type == TransactionType.topup else None
        return {"kind": "wallet_topup", "status": tx.status.value, "order": order}

    payment = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == merchant_order_id,
        ExamPayment.user_id == current_user.id,
    ).first()
    if payment:
        return {"kind": "exam_payment", "status": payment.status}

    raise HTTPException(status_code=404, detail="No payment found for this reference")


# ─── Kashier webhook (authoritative for new payments) ───────────────────────

def _bound_checkout(db: Session, merchant_order_id: str):
    """The Kashier session bound to our order at checkout, or None when no
    Kashier order of ours has this reference."""
    for model, column in ((SubscriptionOrder, SubscriptionOrder.merchant_order_id),
                          (BillingOrder, BillingOrder.merchant_order_id)):
        row = db.query(model.provider, model.provider_order_id).filter(column == merchant_order_id).first()
        if row is not None:
            return row.provider_order_id if row.provider == "kashier" else None
    for model in (WalletTransaction, ExamPayment):
        row = db.query(model.provider_order_id).filter(model.payment_ref == merchant_order_id).first()
        if row is not None:
            return row.provider_order_id
    return None


@router.post("/kashier/webhook")
# Unauthenticated by necessity (Kashier calls it server-to-server): the
# x-kashier-signature is the authentication. The limit bounds forged-signature
# grinding and replay floods.
@limiter.limit("120/minute")
def kashier_webhook(request: Request, payload: dict = Body(...), db: Session = Depends(get_db)):
    data = payload.get("data")
    event = str(payload.get("event") or "").lower()
    if not isinstance(data, dict) or not kashier_service.verify_signature(
        data, request.headers.get("x-kashier-signature", ""),
    ):
        security_log.payment_event(kind="kashier_signature_rejected", ref="<unverified>", success=False)
        raise HTTPException(status_code=401, detail="Invalid signature")
    merchant_order_id = str(data.get("merchantOrderId") or "")
    missing = kashier_service.unsigned_required_fields(data)
    if missing or not merchant_order_id:
        # Settlement trusts these fields; a signature that does not cover them
        # proves nothing about them.
        security_log.payment_event(kind="kashier_unsigned_fields", ref=merchant_order_id or "<none>", success=False)
        raise HTTPException(status_code=400, detail="Webhook fields are not covered by the signature")

    session_id = _bound_checkout(db, merchant_order_id)
    if session_id is None:
        return {"status": "no matching order"}

    # A payment, refund or void changes access only once Kashier's own record says
    # so; until then Kashier is told to retry.
    confirmed = None
    record = kashier_service.needs_confirmation(event, data)
    if record is not None:
        lookup = kashier_service.get_session_payment if record == "payment" else kashier_service.get_session
        try:
            confirmed = lookup(session_id)
        except (httpx.HTTPError, kashier_service.KashierConfigError, ValueError):
            raise HTTPException(status_code=503, detail="Payment confirmation unavailable; retry later")
    try:
        notice = kashier_service.notice_from_webhook(event, data, session_id=session_id, confirmed=confirmed)
    except kashier_service.PaymentNotConfirmed:
        raise HTTPException(status_code=503, detail="Payment not confirmed by the provider yet; retry later")
    try:
        return settle_notice(db, notice)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ─── Paymob webhook (historical orders only) ─────────────────────────────────

@router.post("/paymob/webhook")
# Unauthenticated by necessity (Paymob calls it server-to-server) — HMAC
# is the authentication. The limit bounds how hard an attacker can grind
# forged signatures, and how much load a replay flood can create.
@limiter.limit("120/minute")
async def paymob_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed webhook payload")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Malformed webhook payload")
    obj = payload.get("obj") or {}
    received_hmac = request.query_params.get("hmac") or payload.get("hmac", "")

    if not paymob_service.verify_webhook_hmac(obj, received_hmac):
        security_log.payment_event(kind="hmac_rejected", ref="<unverified>", success=False)
        raise HTTPException(status_code=401, detail="Invalid HMAC signature")

    # `merchant_order_id` is NOT covered by Paymob's HMAC: it only *finds* a
    # candidate row; the signed provider order id, amount and currency must all
    # match that row, and one Paymob transaction id settles at most one row.
    notice = paymob_service.to_notice(obj)
    if notice is None:
        raise HTTPException(status_code=400, detail="Missing merchant_order_id")
    try:
        return settle_notice(db, notice)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ─── Browser return (cosmetic only — grants nothing) ────────────────────────

def _frontend_return(db: Session, merchant_order_id: str) -> RedirectResponse:
    """Send the shopper to the page that polls our own authenticated status
    endpoints, which only ever reflect what a webhook confirmed."""
    course_order = db.query(BillingOrder).filter(BillingOrder.merchant_order_id == merchant_order_id).first()
    if course_order:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/billing/course-success?order_id={course_order.id}")
    if merchant_order_id.startswith("wallet-"):
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/billing/credits?reference={quote(merchant_order_id, safe='')}")
    subscription_order = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.merchant_order_id == merchant_order_id,
    ).first()
    if subscription_order:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/billing/success?reference={subscription_order.reference_number}"
        )
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard?payment_ref={merchant_order_id}")


@router.get("/kashier/return")
def kashier_return(request: Request, db: Session = Depends(get_db)):
    """Where Kashier returns the shopper. `ref` is our own order reference, set in
    the session's merchantRedirect; Kashier's added parameters are ignored."""
    return _frontend_return(db, request.query_params.get("ref", ""))


@router.get("/paymob/callback")
def paymob_callback(request: Request, db: Session = Depends(get_db)):
    return _frontend_return(db, request.query_params.get("merchant_order_id", ""))
