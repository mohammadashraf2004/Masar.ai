"""Plan and subscription state shared by access checks and billing routes."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.billing import (
    BillingPlan,
    SubscriptionOrder,
    SubscriptionPaymentEvent,
    UserSubscription,
)
from app.services.payments import paymob_service
from app.services.payments.notice import PaymentNotice

logger = logging.getLogger("app.billing.subscriptions")

FREE_PLAN_CODE = "free"
PRO_PLAN_CODE = "pro"
ACCESS_STATUSES = {"trialing", "active", "cancelled"}
# Orders a successful payment may still settle. "cancelled" is an abandoned
# checkout that a new one replaced; if the learner did pay it after all, the
# payment is honoured rather than lost.
OPEN_ORDER_STATUSES = {"pending", "failed", "cancelled"}
# Checkout sessions live for an hour (Kashier `expireAt`, set by
# payments.checkout; Paymob payment keys likewise); after this an unpaid
# checkout no longer blocks a new one.
PENDING_ORDER_TTL = timedelta(minutes=75)


def current_subscription(db: Session, user_id: int, *, lock: bool = False) -> Optional[UserSubscription]:
    query = (
        db.query(UserSubscription)
        .filter(UserSubscription.user_id == user_id)
        .order_by(UserSubscription.current_period_end.desc(), UserSubscription.id.desc())
    )
    if lock:
        query = query.with_for_update()
    return query.first()


def subscription_is_entitled(subscription: Optional[UserSubscription], now: Optional[datetime] = None) -> bool:
    if subscription is None or subscription.status not in ACCESS_STATUSES:
        return False
    now = now or datetime.now(timezone.utc)
    end = subscription.current_period_end
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return end > now and subscription.plan.code == PRO_PLAN_CODE


def has_pro_access(db: Session, user_id: int) -> bool:
    return subscription_is_entitled(current_subscription(db, user_id))


def current_plan_code(db: Session, user_id: Optional[int]) -> str:
    return PRO_PLAN_CODE if user_id is not None and has_pro_access(db, user_id) else FREE_PLAN_CODE


def release_stale_checkouts(db: Session, model, user_id: int, now: Optional[datetime] = None, **scope) -> int:
    """Cancel this learner's pending checkouts that can no longer be paid, so
    an abandoned or broken checkout does not block a new one forever.

    Stale means older than the payment key's lifetime, or older than two
    minutes without a provider order (the provider call never completed).
    `model` is SubscriptionOrder or BillingOrder; `scope` narrows it further
    (e.g. course_id). The caller commits."""
    now = now or datetime.now(timezone.utc)
    query = db.query(model).filter(
        model.user_id == user_id, model.status == "pending",
        or_(
            model.created_at < now - PENDING_ORDER_TTL,
            and_(model.provider_order_id.is_(None), model.created_at < now - timedelta(minutes=2)),
        ),
        *[getattr(model, key) == value for key, value in scope.items()],
    )
    return query.update({model.status: "cancelled"}, synchronize_session=False)


def _period_end(start: datetime, period: str) -> datetime:
    # Provider-independent entitlement window. The provider webhook is the
    # only caller that starts or extends it.
    return start + timedelta(days=365 if period == "yearly" else 30)


def process_paymob_subscription_webhook(db: Session, obj: dict) -> Optional[dict]:
    """A verified Paymob callback for a subscription order (see settle_subscription_notice)."""
    notice = paymob_service.to_notice(obj)
    return settle_subscription_notice(db, notice) if notice else None


def settle_subscription_notice(db: Session, notice: PaymentNotice) -> Optional[dict]:
    """Settle a subscription order, returning None for another payment kind."""
    order = (
        db.query(SubscriptionOrder)
        .filter(SubscriptionOrder.merchant_order_id == notice.merchant_order_id)
        .with_for_update()
        .first()
    )
    if order is None:
        return None

    if not notice.event_id:
        raise ValueError("Missing provider transaction id")
    event_id = notice.event_id
    incoming_pending = notice.pending
    event = db.query(SubscriptionPaymentEvent).filter(
        SubscriptionPaymentEvent.provider == notice.provider,
        SubscriptionPaymentEvent.provider_event_id == event_id,
    ).first()
    if event and event.order_id != order.id:
        return {"status": "rejected", "kind": "subscription", "success": False}
    if event and (not event.pending or incoming_pending):
        return {"status": "already_processed", "kind": "subscription", "success": order.status == "paid"}

    amount = notice.amount
    currency = notice.currency
    kind = notice.kind
    # A payment must be for exactly the order's amount; a refund may return
    # part of it (staff-issued partial refund), never more.
    amount_ok = 0 < amount <= order.amount if kind == "reversal" else amount == order.amount
    error_code = None
    # The provider that took the order is the only one whose callbacks bind to it.
    if order.provider != notice.provider or not notice.binds(order.provider_order_id):
        error_code = "provider_order_mismatch"
    elif not amount_ok:
        error_code = "amount_mismatch"
    elif currency != order.currency:
        error_code = "currency_mismatch"

    values = dict(
        amount=max(amount, 0), currency=currency[:3] or "N/A",
        success=notice.success, pending=incoming_pending,
        response_code=error_code or (kind if kind != "payment" else None), raw_payload=notice.raw,
    )
    if event:
        for key, value in values.items():
            setattr(event, key, value)
    else:
        event = SubscriptionPaymentEvent(
            order_id=order.id, provider=notice.provider, provider_event_id=event_id, **values,
        )
        db.add(event)

    # A paid order is final: a mismatched, declined or duplicate callback that
    # arrives afterwards is recorded but never moves it backwards.
    open_order = order.status in OPEN_ORDER_STATUSES
    if error_code:
        if open_order:
            order.status = "failed"
        db.commit()
        logger.warning("billing.subscription.%s", error_code, extra={"order_id": order.id})
        return {"status": "rejected", "kind": "subscription", "success": False}

    if kind == "reversal":
        # A verified refund/void never grants. Provider truth completes the
        # audited refund exactly once and ends the period that payment bought:
        # staff usually refund in the provider's dashboard (Kashier; Paymob for
        # its older orders) while the request is "processing", and this
        # callback lands before anyone clicks
        # "refunded" - after which no workflow step could revoke it any more.
        if order.status in {"paid", "refunded"} and not incoming_pending:
            from app.services.billing.refunds import reconcile_provider_refund

            reconcile_provider_refund(
                db, order=order, provider_event_id=event_id,
                amount=amount, success=notice.success,
            )
        db.commit()
        logger.warning("billing.subscription.reversal", extra={"order_id": order.id, "user_id": order.user_id})
        return {"status": "processed", "kind": "subscription", "success": False}

    provider_success = notice.settles
    if not provider_success:
        if open_order:
            order.status = "pending" if incoming_pending or kind == "authorization" else "failed"
        db.commit()
        return {"status": "processed", "kind": "subscription", "success": False}

    if not open_order:
        # Paid twice (or paid after a refund): one order buys one period.
        db.commit()
        logger.warning("billing.subscription.extra_payment", extra={"order_id": order.id, "user_id": order.user_id})
        return {"status": "already_processed", "kind": "subscription", "success": order.status == "paid"}

    event.grants_period = True
    now = datetime.now(timezone.utc)
    subscription = current_subscription(db, order.user_id, lock=True)
    if subscription and subscription_is_entitled(subscription, now) and subscription.plan_id == order.plan_id:
        start = subscription.current_period_end
        subscription.current_period_end = _period_end(start, order.billing_period)
        subscription.status = "active"
        subscription.billing_period = order.billing_period
        subscription.cancel_at_period_end = False
        subscription.cancelled_at = None
        subscription.provider_subscription_id = event_id
    else:
        if subscription and subscription.status in ACCESS_STATUSES:
            subscription.status = "expired"
        subscription = UserSubscription(
            user_id=order.user_id, plan_id=order.plan_id, status="active",
            billing_period=order.billing_period, payment_provider=notice.provider,
            provider_subscription_id=event_id,
            current_period_start=now, current_period_end=_period_end(now, order.billing_period),
        )
        db.add(subscription)

    order.status = "paid"
    order.paid_at = order.paid_at or now
    order.provider_transaction_id = order.provider_transaction_id or event_id
    db.flush()
    order.subscription_id = subscription.id
    try:
        db.commit()
    except IntegrityError:
        # uq_subscription_payment_one_grant: another worker granted this order.
        db.rollback()
        return {"status": "already_processed", "kind": "subscription", "success": True}
    logger.info("billing.subscription.activated", extra={"order_id": order.id, "user_id": order.user_id})
    return {"status": "processed", "kind": "subscription", "success": True}


def cancel_at_period_end(db: Session, user_id: int) -> UserSubscription:
    subscription = current_subscription(db, user_id, lock=True)
    if not subscription or not subscription_is_entitled(subscription):
        raise LookupError("No active subscription")
    subscription.status = "cancelled"
    subscription.cancel_at_period_end = True
    subscription.cancelled_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(subscription)
    return subscription


def start_free_trial(db: Session, user_id: int, plan: BillingPlan, billing_period: str) -> UserSubscription:
    """Start the account's one seven-day trial without creating a charge."""
    if db.query(UserSubscription.id).filter(UserSubscription.user_id == user_id).first():
        raise ValueError("Trial already used")
    now = datetime.now(timezone.utc)
    subscription = UserSubscription(
        user_id=user_id, plan_id=plan.id, status="trialing", billing_period=billing_period,
        payment_provider="internal", provider_subscription_id=None,
        current_period_start=now, current_period_end=now + timedelta(days=7),
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def plan_amount(plan: BillingPlan, period: str) -> int:
    return plan.yearly_price_minor if period == "yearly" else plan.monthly_price_minor
