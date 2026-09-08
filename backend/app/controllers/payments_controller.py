"""
backend/app/controllers/payments_controller.py

Paymob-backed payment initiation + webhook handling for both wallet
top-ups and exam-fee payments. This is the ONLY path that should ever
mark a Paymob-routed payment as confirmed — the GET /callback route the
customer's browser lands on after paying is purely cosmetic routing and
must never itself grant credits/access (a browser redirect can be
skipped, replayed, or forged; the server-to-server webhook, verified by
HMAC, cannot).

Register in main.py:
    from app.controllers.payments_controller import router as payments_router
    app.include_router(payments_router, prefix="/api/v1/payments", tags=["Payments"])
"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Literal

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
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
from app.models.exam import Exam
from app.core.security import get_current_user
from app.services.wallet.wallet_service import get_or_create_wallet
from app.services.payments import paymob_service

router = APIRouter()

EXAM_PRICE_EGP = 150.0  # kept in sync with exam_payment_controller.EXAM_PRICE_EGP


class InitPaymentRequest(BaseModel):
    method: Literal["card", "wallet"]
    # Digits (with optional leading +) only — this value is forwarded to
    # the payment provider, so it should not be a free-text passthrough.
    phone_number: str | None = Field(None, min_length=6, max_length=20, pattern=r"^\+?[0-9]{6,19}$")


class WalletTopUpInitRequest(InitPaymentRequest):
    package_id: int = Field(..., gt=0)


class ExamPaymentInitRequest(InitPaymentRequest):
    exam_id: int = Field(..., gt=0)


def _new_merchant_order_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def _require_phone_for_wallet(payload: InitPaymentRequest):
    if payload.method == "wallet" and not payload.phone_number:
        raise HTTPException(status_code=422, detail="phone_number is required for method=wallet")


def _init_checkout(amount_egp: float, merchant_order_id: str, payload: InitPaymentRequest, user: User) -> str:
    try:
        result = paymob_service.init_payment(
            amount_egp=amount_egp,
            merchant_order_id=merchant_order_id,
            method=payload.method,
            full_name=user.full_name,
            email=user.email,
            phone_number=payload.phone_number or "01000000000",
        )
    except paymob_service.PaymobConfigError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except httpx.HTTPStatusError as e:
        # The upstream body can echo request details and provider-side
        # diagnostics; it belongs in our logs, not in a client response.
        logging.getLogger("app.payments").warning(
            "Paymob rejected a payment init (status=%s)", e.response.status_code,
        )
        raise HTTPException(status_code=502, detail="The payment provider rejected this request.")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach Paymob. Please try again.")
    return result["checkout_url"]


# ─── Wallet top-up ──────────────────────────────────────────────────────────

@router.post("/wallet/topup/init")
@limiter.limit("10/minute")
def init_wallet_topup(
    request: Request,
    payload: WalletTopUpInitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_phone_for_wallet(payload)
    package = db.query(CreditPackage).filter(
        CreditPackage.id == payload.package_id,
        CreditPackage.is_active == True,
    ).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    merchant_order_id = _new_merchant_order_id("wallet")
    total_credits = package.credits + package.bonus_credits

    wallet = get_or_create_wallet(current_user.id, db)
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.topup,
        status=TransactionStatus.pending,
        credits=total_credits,
        egp_amount=package.egp_price,
        payment_method=PaymentMethod(payload.method if payload.method == "card" else "vodafone_cash"),
        payment_ref=merchant_order_id,
        description=f"{package.name} package — Paymob {payload.method}",
        balance_after=wallet.credit_balance,
    )
    db.add(tx)
    db.commit()

    checkout_url = _init_checkout(package.egp_price, merchant_order_id, payload, current_user)
    return {"checkout_url": checkout_url, "merchant_order_id": merchant_order_id}


# ─── Exam fee ────────────────────────────────────────────────────────────────

@router.post("/exam/init")
@limiter.limit("10/minute")
def init_exam_payment(
    request: Request,
    payload: ExamPaymentInitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_phone_for_wallet(payload)
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
        payment_method=payload.method,
        payment_ref=merchant_order_id,
        status="pending",
    )
    db.add(payment)
    db.commit()

    checkout_url = _init_checkout(EXAM_PRICE_EGP, merchant_order_id, payload, current_user)
    return {"checkout_url": checkout_url, "merchant_order_id": merchant_order_id}


# ─── Status polling (for the frontend post-checkout page) ───────────────────

@router.get("/status/{merchant_order_id}")
def get_payment_status(
    merchant_order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Read-only status check by merchant_order_id, scoped to the
    requesting user — only ever reflects what the webhook has actually
    confirmed, never what a browser redirect claims."""
    tx = db.query(WalletTransaction).join(UserWallet).filter(
        WalletTransaction.payment_ref == merchant_order_id,
        UserWallet.user_id == current_user.id,
    ).first()
    if tx:
        return {"kind": "wallet_topup", "status": tx.status.value}

    payment = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == merchant_order_id,
        ExamPayment.user_id == current_user.id,
    ).first()
    if payment:
        return {"kind": "exam_payment", "status": payment.status}

    raise HTTPException(status_code=404, detail="No payment found for this reference")


# ─── Webhook (authoritative) ─────────────────────────────────────────────────

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

    success = bool(obj.get("success"))
    merchant_order_id = (obj.get("order") or {}).get("merchant_order_id")
    if not merchant_order_id:
        raise HTTPException(status_code=400, detail="Missing merchant_order_id")

    # Wallet top-up?
    tx = (
        db.query(WalletTransaction)
        .filter(
            WalletTransaction.payment_ref == merchant_order_id,
            WalletTransaction.status == TransactionStatus.pending,
        )
        .with_for_update()
        .first()
    )
    if tx:
        wallet = db.query(UserWallet).filter(UserWallet.id == tx.wallet_id).with_for_update().one()
        if success:
            wallet.credit_balance += tx.credits
            wallet.lifetime_purchased += tx.credits
            tx.status = TransactionStatus.confirmed
            tx.balance_after = wallet.credit_balance
        else:
            tx.status = TransactionStatus.failed
        db.commit()
        security_log.payment_event(
            kind="wallet_topup", ref=merchant_order_id, success=success, user_id=wallet.user_id,
        )
        return {"status": "processed", "kind": "wallet_topup", "success": success}

    # Exam fee?
    payment = (
        db.query(ExamPayment)
        .filter(
            ExamPayment.payment_ref == merchant_order_id,
            ExamPayment.status == "pending",
        )
        .with_for_update()
        .first()
    )
    if payment:
        payment.status = "confirmed" if success else "failed"
        if success:
            payment.confirmed_by = "webhook"
            payment.confirmed_at = datetime.now(timezone.utc)
        db.commit()
        security_log.payment_event(
            kind="exam_payment", ref=merchant_order_id, success=success, user_id=payment.user_id,
        )
        return {"status": "processed", "kind": "exam_payment", "success": success}

    # Nothing pending matches — ack 200 anyway (so Paymob doesn't retry
    # forever on an already-processed or unrelated notification) but don't
    # pretend anything happened.
    return {"status": "no matching pending transaction"}


# ─── Browser return (cosmetic only — grants nothing) ────────────────────────

@router.get("/paymob/callback")
def paymob_callback(request: Request):
    """Where the customer's browser lands after completing checkout.
    Deliberately does not trust anything in these query params — redirects
    to a frontend page that polls our own authenticated status endpoints,
    which only ever reflect what the webhook above actually confirmed."""
    merchant_order_id = request.query_params.get("merchant_order_id", "")
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/dashboard?payment_ref={merchant_order_id}"
    )
