"""Course checkout selection and authoritative Paymob settlement."""
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.billing import BillingOrder, CourseEnrollment, CourseOffer, PaymentTransaction
from app.services.payments import paymob_service

logger = logging.getLogger("app.billing")


def current_offer(db: Session, course_id: int, *, lock: bool = False) -> Optional[CourseOffer]:
    now = datetime.now(timezone.utc)
    query = db.query(CourseOffer).filter(
        CourseOffer.course_id == course_id,
        CourseOffer.is_active.is_(True),
        or_(CourseOffer.starts_at.is_(None), CourseOffer.starts_at <= now),
        or_(CourseOffer.ends_at.is_(None), CourseOffer.ends_at > now),
    )
    if lock:
        query = query.with_for_update()
    return query.first()


def _response_code(obj: dict) -> Optional[str]:
    data = obj.get("data")
    value = data.get("message") if isinstance(data, dict) else None
    return str(value or obj.get("txn_response_code") or "")[:100] or None


def process_paymob_course_webhook(db: Session, obj: dict) -> Optional[dict]:
    """Settle a course order, or return None when this is a legacy payment.

    The order row lock serializes callbacks for the same purchase. Provider
    transaction and enrollment uniqueness remain the database-level safety
    net if independent workers race before reaching the lock.
    """
    provider_order = obj.get("order") if isinstance(obj.get("order"), dict) else {}
    merchant_order_id = provider_order.get("merchant_order_id")
    if not merchant_order_id:
        return None

    order = (
        db.query(BillingOrder)
        .filter(BillingOrder.merchant_order_id == str(merchant_order_id))
        .with_for_update()
        .first()
    )
    if not order:
        return None

    provider_transaction_id = obj.get("id")
    if provider_transaction_id is None:
        raise ValueError("Missing provider transaction id")
    provider_transaction_id = str(provider_transaction_id)

    transaction = db.query(PaymentTransaction).filter(
        PaymentTransaction.provider == "paymob",
        PaymentTransaction.provider_transaction_id == provider_transaction_id,
    ).first()
    incoming_pending = bool(obj.get("pending"))
    if transaction and transaction.order_id != order.id:
        logger.warning(
            "billing.webhook.transaction_order_mismatch",
            extra={"order_id": order.id, "provider_transaction_id": provider_transaction_id},
        )
        return {"status": "rejected", "kind": "course_payment", "success": False}
    if transaction and (not transaction.pending or incoming_pending):
        logger.info(
            "billing.webhook.duplicate",
            extra={"order_id": order.id, "provider_transaction_id": provider_transaction_id},
        )
        return {"status": "already_processed", "kind": "course_payment", "success": order.status == "paid"}

    amount = obj.get("amount_cents")
    currency = str(obj.get("currency") or "").upper()
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        amount = -1
    provider_matches = paymob_service.provider_order_matches(obj, order.provider_order_id)
    amount_matches = amount == order.amount
    currency_matches = currency == order.currency
    kind = paymob_service.classify_transaction(obj)
    provider_success = bool(obj.get("success")) and not incoming_pending and kind == "payment"
    # A paid order is final: later mismatched, declined or reversed callbacks
    # are recorded but never move it backwards or re-grant.
    open_order = order.status != "paid" and order.status != "refunded"

    error_code = None
    if not provider_matches:
        error_code = "provider_order_mismatch"
    elif not amount_matches:
        error_code = "amount_mismatch"
    elif not currency_matches:
        error_code = "currency_mismatch"

    if transaction:
        # Paymob can first report a transaction as pending and later send its
        # terminal state under the same id. Update that one audit record; a
        # terminal event remains immutable and retries above are no-ops.
        transaction.amount = max(amount, 0)
        transaction.currency = currency[:3] or "N/A"
        transaction.success = bool(obj.get("success"))
        transaction.pending = incoming_pending
        transaction.response_code = error_code or _response_code(obj)
        transaction.raw_payload = obj
    else:
        db.add(PaymentTransaction(
            order_id=order.id,
            provider="paymob",
            provider_transaction_id=provider_transaction_id,
            amount=max(amount, 0),
            currency=currency[:3] or "N/A",
            success=bool(obj.get("success")),
            pending=incoming_pending,
            response_code=error_code or _response_code(obj),
            raw_payload=obj,
        ))

    if error_code:
        if open_order:
            order.status = "failed"
        db.commit()
        logger.warning(
            "billing.payment.%s", error_code,
            extra={
                "order_id": order.id,
                "course_id": order.course_id,
                "provider_transaction_id": provider_transaction_id,
            },
        )
        return {"status": "rejected", "kind": "course_payment", "success": False}

    if kind == "reversal":
        if order.status == "paid" and bool(obj.get("success")) and not incoming_pending:
            order.status = "refunded"
        db.commit()
        logger.warning(
            "billing.payment.reversal",
            extra={"order_id": order.id, "user_id": order.user_id, "course_id": order.course_id},
        )
        return {"status": "processed", "kind": "course_payment", "success": False}

    if not provider_success:
        if open_order:
            order.status = "pending" if incoming_pending or kind == "authorization" else "failed"
        db.commit()
        logger.info(
            "billing.payment.failed",
            extra={"order_id": order.id, "course_id": order.course_id},
        )
        return {"status": "processed", "kind": "course_payment", "success": False}

    if not open_order:
        db.commit()
        logger.warning("billing.payment.extra_payment", extra={"order_id": order.id, "user_id": order.user_id})
        return {"status": "already_processed", "kind": "course_payment", "success": order.status == "paid"}

    order.status = "paid"
    order.paid_at = order.paid_at or datetime.now(timezone.utc)
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == order.user_id,
        CourseEnrollment.course_id == order.course_id,
    ).with_for_update().first()
    if enrollment:
        enrollment.status = "active"
        enrollment.source = "purchase"
        enrollment.order_id = order.id
        enrollment.expires_at = None
    else:
        enrollment = CourseEnrollment(
            user_id=order.user_id,
            course_id=order.course_id,
            source="purchase",
            order_id=order.id,
            status="active",
            expires_at=None,
        )
        db.add(enrollment)
    db.commit()
    logger.info(
        "billing.payment.succeeded",
        extra={
            "order_id": order.id,
            "user_id": order.user_id,
            "course_id": order.course_id,
            "provider_transaction_id": provider_transaction_id,
        },
    )
    return {"status": "processed", "kind": "course_payment", "success": True}
