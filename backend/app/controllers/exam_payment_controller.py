"""
backend/app/controllers/exam_payment_controller.py

Handles EGP-only exam payments (no credits).
Register in main.py:
    from app.controllers.exam_payment_controller import router as exam_payment_router
    app.include_router(exam_payment_router, prefix="/api/v1/exam-payments", tags=["Exam Payments"])
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from app.db.session import get_db
from app.core import security_log
from app.core.authz import require_admin
from app.core.limiter import limiter
from app.core.security import get_current_user
from app.models.user import User
from app.models.challenge import ExamPayment
from app.models.exam import Exam

router = APIRouter()

# EGP price per exam (can be moved to DB later).
#
# THE authoritative value. payments_controller imports this rather than
# keeping its own copy — the two were previously separate literals held in
# sync by a comment, which is one edit away from charging a different
# amount through Paymob than the manual-reference flow quotes.
EXAM_PRICE_EGP = 150.0

PAYMENT_LABELS = {
    "fawry":         "Fawry",
    "instapay":      "InstaPay",
    "vodafone_cash": "Vodafone Cash",
}


class ExamPaymentRequest(BaseModel):
    exam_id: int = Field(..., gt=0)
    payment_method: str = Field(..., max_length=32)   # fawry | instapay | vodafone_cash
    payment_ref: str = Field(..., min_length=3, max_length=100)


class ConfirmPaymentRequest(BaseModel):
    payment_ref: str = Field(..., min_length=3, max_length=100)


@router.get("/price")
def get_exam_price():
    return {
        "egp_price": EXAM_PRICE_EGP,
        "methods": list(PAYMENT_LABELS.keys()),
        "note": "Certification exams require EGP payment — credits cannot be used.",
    }


@router.get("/status/{exam_id}")
def get_payment_status(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if the current user has a confirmed payment for this exam."""
    payment = db.query(ExamPayment).filter(
        ExamPayment.user_id == current_user.id,
        ExamPayment.exam_id == exam_id,
        ExamPayment.status == "confirmed",
    ).first()

    return {
        "paid": payment is not None,
        "payment_ref": payment.payment_ref if payment else None,
        "confirmed_at": payment.confirmed_at.isoformat() if payment and payment.confirmed_at else None,
    }


@router.post("/submit")
# Submitting a reference is cheap for the caller and creates a row keyed on
# an attacker-chosen string, so it is worth a tighter limit than the
# 120/minute default ceiling: it bounds how fast someone can spray
# candidate references at the adjudication queue.
@limiter.limit("10/minute")
def submit_exam_payment(
    request: Request,
    payload: ExamPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit a payment reference for exam access. Starts as pending."""
    exam = db.query(Exam).filter(Exam.id == payload.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if payload.payment_method not in PAYMENT_LABELS:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # Check already confirmed
    existing = db.query(ExamPayment).filter(
        ExamPayment.user_id == current_user.id,
        ExamPayment.exam_id == payload.exam_id,
        ExamPayment.status == "confirmed",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have confirmed payment for this exam")

    # ── Reference reuse ───────────────────────────────────────────────────
    # Deliberately NOT "has anyone ever typed this string". `payment_ref`
    # is supplied by the user after paying offline, so rejecting every
    # reference that already exists in any state let anybody permanently
    # squat a reference and lock its real payer out of the exam they had
    # already paid for. See migration 008.
    #
    # What genuinely has to be unique is a CONFIRMED payment: one real
    # payment, one exam access. A pending claim by somebody else is only
    # an unverified assertion, and must not block the actual payer from
    # making their own claim — the admin adjudicates between them against
    # the provider's records.
    confirmed_elsewhere = db.query(ExamPayment.id).filter(
        ExamPayment.payment_ref == payload.payment_ref,
        ExamPayment.status == "confirmed",
    ).first()
    if confirmed_elsewhere:
        raise HTTPException(
            status_code=400,
            detail="This payment reference has already been used to confirm an exam payment",
        )

    # Idempotency for the honest retry: a user double-submitting their own
    # reference (double-clicked the button, lost the response) should get a
    # clear answer rather than a second pending row for the same payment.
    own = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == payload.payment_ref,
        ExamPayment.user_id == current_user.id,
    ).first()
    if own:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted this payment reference; it is awaiting confirmation",
        )

    payment = ExamPayment(
        user_id=current_user.id,
        exam_id=payload.exam_id,
        egp_amount=EXAM_PRICE_EGP,
        payment_method=payload.payment_method,
        payment_ref=payload.payment_ref,
        status="pending",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment submitted. Exam access will be granted after confirmation (usually within 1 hour).",
        "payment_id": payment.id,
        "exam_id": payload.exam_id,
        "egp_paid": EXAM_PRICE_EGP,
        "method": PAYMENT_LABELS[payload.payment_method],
        "ref": payload.payment_ref,
        "status": "pending",
    }


@router.post("/admin/confirm/{payment_ref}")
def confirm_exam_payment(
    payment_ref: str,
    payment_id: Optional[int] = Query(
        None,
        gt=0,
        description=(
            "Which pending claim to confirm, when more than one user has "
            "claimed this reference. Ids come from the 409 body or from "
            "/admin/pending."
        ),
    ),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: confirm an exam payment and grant access.

    This is the only thing standing between "submitted a reference
    number" and "may sit a paid certification exam", so it is both
    admin-gated and audit-logged.

    Pending claims on a reference are no longer unique (see the submit
    handler and migration 008: enforcing that was what let a reference be
    squatted). So this can find more than one row, and picking one
    arbitrarily would be worse than the DoS it replaced — a squatter who
    claimed first would be handed the exam access the real payer bought.
    Contested references therefore stop here with a 409 listing the
    candidates, and the admin re-calls with ?payment_id= once they have
    checked the provider's records. The single-claim case — effectively
    all of them — is unchanged.
    """
    q = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == payment_ref,
        ExamPayment.status == "pending",
    )
    if payment_id is not None:
        q = q.filter(ExamPayment.id == payment_id)

    # Locked because confirming is a read-then-write, and two admins
    # working the same queue must not both pass the check below.
    candidates = q.order_by(ExamPayment.created_at.asc()).with_for_update().all()

    if not candidates:
        raise HTTPException(status_code=404, detail="Pending payment not found")

    if len(candidates) > 1:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "ambiguous_payment_reference",
                "message": (
                    "More than one user has claimed this payment reference. "
                    "Check the provider's records for who actually paid, then "
                    "re-send this request with ?payment_id=<id>."
                ),
                "candidates": [
                    {
                        "payment_id": p.id,
                        "user_id": p.user_id,
                        "exam_id": p.exam_id,
                        "submitted_at": p.created_at.isoformat() if p.created_at else None,
                    }
                    for p in candidates
                ],
            },
        )

    payment = candidates[0]

    # The reference may have been confirmed since this claim was filed —
    # by the other side of a contested pair, or by a concurrent admin. The
    # partial unique index from migration 008 is the real guarantee; this
    # check turns what would be a 409 IntegrityError into a clear message.
    already = db.query(ExamPayment.id).filter(
        ExamPayment.payment_ref == payment_ref,
        ExamPayment.status == "confirmed",
    ).first()
    if already:
        raise HTTPException(
            status_code=409,
            detail="This payment reference has already been confirmed for another claim",
        )

    payment.status       = "confirmed"
    payment.confirmed_by = "admin"
    payment.confirmed_at = datetime.now(timezone.utc)
    db.commit()

    security_log.admin_action(
        admin_id=current_user.id, action="exam_payment.confirm",
        target=f"ref={payment_ref} user={payment.user_id} exam={payment.exam_id}",
    )
    return {
        "message": "Payment confirmed. User can now access the exam.",
        "user_id": payment.user_id,
        "exam_id": payment.exam_id,
        "ref": payment_ref,
    }


@router.get("/admin/pending")
def list_pending_payments(
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: list pending exam payments, oldest first (most urgent to clear)."""
    payments = (
        db.query(ExamPayment)
        .filter(ExamPayment.status == "pending")
        .order_by(ExamPayment.created_at.asc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "exam_id": p.exam_id,
            "egp_amount": p.egp_amount,
            "method": p.payment_method,
            "ref": p.payment_ref,
            "submitted_at": p.created_at.isoformat(),
        }
        for p in payments
    ]