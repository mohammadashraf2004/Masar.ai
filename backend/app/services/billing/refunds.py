"""Reviewed, idempotent refunds for subscription payments.

Submitting a request never moves money. Staff review eligibility and resource
consumption first; provider confirmation (or an audited manual reconciliation)
is what completes a refund.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.billing import SubscriptionOrder, SubscriptionRefundEvent, UserSubscription
from app.models.wallet import UserWallet


REFUND_WINDOW = timedelta(days=7)
REFUND_STATES = {
    "not_requested", "requested", "under_review", "approved", "rejected",
    "processing", "refunded", "failed",
}
ACTIVE_REFUND_STATES = {"requested", "under_review", "approved", "processing"}
REFUND_TRANSITIONS = {
    "not_requested": {"requested"},
    "requested": {"under_review", "rejected"},
    "under_review": {"approved", "rejected"},
    "approved": {"processing", "rejected"},
    "processing": {"refunded", "failed"},
    "failed": {"processing", "rejected"},
    "rejected": set(),
    "refunded": set(),
}


class RefundError(ValueError):
    def __init__(self, code: str, message: str, status_code: int = 422):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def refund_eligibility(order: SubscriptionOrder, now: Optional[datetime] = None) -> tuple[bool, Optional[str]]:
    now = now or datetime.now(timezone.utc)
    if order.status != "paid" or order.paid_at is None:
        return False, "payment_not_captured"
    if _aware(order.paid_at) + REFUND_WINDOW < now:
        return False, "refund_window_expired"
    if order.refund_status != "not_requested":
        return False, "refund_already_requested"
    return True, None


def _wallet_snapshot(db: Session, user_id: int) -> dict:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    return {
        "subscription_credits_granted": 0,
        "credit_rule": "subscription_payment_grants_no_wallet_credits",
        "wallet_balance_at_request": wallet.credit_balance if wallet else None,
    }


def _append_event(
    db: Session,
    order: SubscriptionOrder,
    *,
    from_status: str,
    to_status: str,
    actor_user_id: Optional[int],
    idempotency_key: str,
    provider_reference: Optional[str] = None,
    note: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> SubscriptionRefundEvent:
    event = SubscriptionRefundEvent(
        order_id=order.id, from_status=from_status, to_status=to_status,
        actor_user_id=actor_user_id, idempotency_key=idempotency_key,
        provider_reference=provider_reference, note=note,
        metadata_json=metadata or {},
    )
    db.add(event)
    return event


def _idempotent_event(db: Session, idempotency_key: str, order_id: int) -> Optional[SubscriptionRefundEvent]:
    event = db.query(SubscriptionRefundEvent).filter_by(idempotency_key=idempotency_key).first()
    if event is not None and event.order_id != order_id:
        raise RefundError("IDEMPOTENCY_KEY_REUSED", "Idempotency key belongs to another order.", 409)
    return event


def request_refund(
    db: Session,
    *,
    order_id: int,
    user_id: int,
    amount: int,
    reason: str,
    confirmed: bool,
    idempotency_key: str,
    now: Optional[datetime] = None,
) -> SubscriptionOrder:
    order = db.query(SubscriptionOrder).filter(
        SubscriptionOrder.id == order_id, SubscriptionOrder.user_id == user_id,
    ).with_for_update().first()
    if order is None:
        raise RefundError("ORDER_NOT_FOUND", "Order not found.", 404)
    previous = _idempotent_event(db, idempotency_key, order.id)
    if previous is not None:
        return order
    if not confirmed:
        raise RefundError("REFUND_CONFIRMATION_REQUIRED", "Explicit confirmation is required.")
    reason = reason.strip()
    if len(reason) < 5:
        raise RefundError("REFUND_REASON_REQUIRED", "Please provide a refund reason of at least 5 characters.")
    if amount <= 0 or amount > order.amount:
        raise RefundError("INVALID_REFUND_AMOUNT", "Refund amount must be positive and cannot exceed the captured payment.")
    eligible, eligibility_reason = refund_eligibility(order, now)
    if not eligible:
        code = "DUPLICATE_REFUND_REQUEST" if eligibility_reason == "refund_already_requested" else "REFUND_NOT_ELIGIBLE"
        raise RefundError(code, "This payment is not eligible for a new refund request.", 409)

    now = now or datetime.now(timezone.utc)
    order.refund_status = "requested"
    order.refund_requested_at = now
    order.refund_amount = amount
    order.refund_reason = reason
    _append_event(
        db, order, from_status="not_requested", to_status="requested",
        actor_user_id=user_id, idempotency_key=idempotency_key,
        metadata={"requested_amount": amount, **_wallet_snapshot(db, user_id)},
    )
    db.commit()
    db.refresh(order)
    return order


def _period_bought(order: SubscriptionOrder) -> timedelta:
    # Mirrors subscriptions._period_end: the window one paid order grants.
    return timedelta(days=365 if order.billing_period == "yearly" else 30)


def _revoke_refunded_entitlement(db: Session, order: SubscriptionOrder, now: datetime) -> None:
    # Pro subscription payments grant access, not wallet credits. A completed
    # refund therefore removes exactly the period this payment bought - not
    # periods other, unrefunded orders extended the subscription by - and
    # creates no credit-ledger mutation. A partial refund (a goodwill or
    # pro-rata adjustment staff chose) keeps the access; it is recorded only.
    if order.refund_amount is not None and order.refund_amount < order.amount:
        return
    subscription = None
    if order.subscription_id:
        subscription = db.query(UserSubscription).filter_by(id=order.subscription_id).with_for_update().first()
    if subscription is None:
        subscription = (
            db.query(UserSubscription)
            .filter(UserSubscription.user_id == order.user_id)
            .order_by(UserSubscription.current_period_end.desc())
            .with_for_update()
            .first()
        )
    if subscription is None or subscription.status not in {"trialing", "active", "cancelled"}:
        return
    remaining_end = _aware(subscription.current_period_end) - _period_bought(order)
    if remaining_end > now:
        subscription.current_period_end = remaining_end
        return
    subscription.status = "expired"
    subscription.cancel_at_period_end = False
    if _aware(subscription.current_period_end) > now:
        subscription.current_period_end = now


def transition_refund(
    db: Session,
    *,
    order_id: int,
    to_status: str,
    actor_user_id: Optional[int],
    idempotency_key: str,
    note: Optional[str] = None,
    provider_reference: Optional[str] = None,
    refund_amount: Optional[int] = None,
    now: Optional[datetime] = None,
) -> SubscriptionOrder:
    if to_status not in REFUND_STATES or to_status == "not_requested":
        raise RefundError("INVALID_REFUND_STATUS", "Unknown refund status.")
    order = db.query(SubscriptionOrder).filter_by(id=order_id).with_for_update().first()
    if order is None:
        raise RefundError("ORDER_NOT_FOUND", "Order not found.", 404)
    previous = _idempotent_event(db, idempotency_key, order.id)
    if previous is not None:
        return order
    current = order.refund_status
    if to_status not in REFUND_TRANSITIONS[current]:
        raise RefundError(
            "INVALID_REFUND_TRANSITION", f"Refund cannot move from {current} to {to_status}.", 409,
        )
    amount = refund_amount if refund_amount is not None else order.refund_amount
    if amount is None or amount <= 0 or amount > order.amount:
        raise RefundError("INVALID_REFUND_AMOUNT", "Refund amount must be positive and cannot exceed the captured payment.")
    if to_status in {"processing", "refunded"} and not order.provider_transaction_id:
        raise RefundError("MISSING_PROVIDER_TRANSACTION", "The captured provider transaction is missing.", 409)
    if to_status == "refunded" and not provider_reference:
        raise RefundError("PROVIDER_REFERENCE_REQUIRED", "A provider refund reference is required.")

    now = now or datetime.now(timezone.utc)
    order.refund_status = to_status
    order.refund_amount = amount
    if note is not None:
        order.refund_admin_note = note.strip() or None
    if provider_reference:
        order.refund_provider_reference = provider_reference
    if to_status in {"refunded", "failed"}:
        order.refund_processed_at = now
    if to_status == "refunded":
        order.status = "refunded"
        _revoke_refunded_entitlement(db, order, now)
    _append_event(
        db, order, from_status=current, to_status=to_status,
        actor_user_id=actor_user_id, idempotency_key=idempotency_key,
        provider_reference=provider_reference, note=note,
        metadata={"refund_amount": amount},
    )
    db.commit()
    db.refresh(order)
    return order


def reconcile_provider_refund(
    db: Session,
    *,
    order: SubscriptionOrder,
    provider_event_id: str,
    amount: int,
    success: bool,
    revoke_entitlement: bool = True,
    now: Optional[datetime] = None,
) -> SubscriptionOrder:
    """Apply verified provider truth once, including dashboard-issued refunds."""
    key = f"provider-refund:{order.provider}:{provider_event_id}"
    if _idempotent_event(db, key, order.id) is not None:
        return order
    if amount <= 0 or amount > order.amount:
        raise RefundError("INVALID_REFUND_AMOUNT", "Provider refund exceeds captured amount.")
    now = now or datetime.now(timezone.utc)
    current = order.refund_status
    # Staff may already have completed this refund (processing -> refunded),
    # which revoked the access it bought. The provider's own callback for the
    # same refund then only adds the audit row: it must neither revoke a second
    # period nor flip a completed refund back to "failed".
    already_refunded = current == "refunded"
    target = "refunded" if success or already_refunded else "failed"
    revoked = bool(success and revoke_entitlement and not already_refunded)
    if not already_refunded:
        order.refund_status = target
        order.refund_amount = amount
        order.refund_provider_reference = provider_event_id
        order.refund_processed_at = now
        if success:
            order.status = "refunded"
            if revoke_entitlement:
                _revoke_refunded_entitlement(db, order, now)
    _append_event(
        db, order, from_status=current, to_status=target, actor_user_id=None,
        idempotency_key=key, provider_reference=provider_event_id,
        note="Verified payment-provider callback",
        metadata={
            "refund_amount": amount, "provider_reconciliation": True,
            "success": success, "entitlement_revoked": revoked,
            "already_refunded": already_refunded,
        },
    )
    return order
