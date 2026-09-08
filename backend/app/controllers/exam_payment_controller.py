"""
backend/app/controllers/exam_payment_controller.py

Handles EGP-only exam payments (no credits).
Register in main.py:
    from app.controllers.exam_payment_controller import router as exam_payment_router
    app.include_router(exam_payment_router, prefix="/api/v1/exam-payments", tags=["Exam Payments"])
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from app.db.session import get_db
from app.core import security_log
from app.core.authz import require_admin
from app.core.security import get_current_user
from app.models.user import User
from app.models.challenge import ExamPayment
from app.models.exam import Exam

router = APIRouter()

# EGP price per exam (can be moved to DB later)
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
def submit_exam_payment(
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

    # Check duplicate ref
    dup = db.query(ExamPayment).filter(ExamPayment.payment_ref == payload.payment_ref).first()
    if dup:
        raise HTTPException(status_code=400, detail="This payment reference has already been submitted")

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
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin: confirm an exam payment and grant access.

    This is the only thing standing between "submitted a reference
    number" and "may sit a paid certification exam", so it is both
    admin-gated and audit-logged.
    """
    payment = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == payment_ref,
        ExamPayment.status == "pending",
    ).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pending payment not found")

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