"""Masar payment references, reviewed refunds, and credit/access handling."""
from datetime import datetime, timedelta, timezone
import uuid

import pytest
from sqlalchemy.exc import DBAPIError

from app.core.security import get_password_hash
from app.models.billing import BillingPlan, SubscriptionOrder, SubscriptionRefundEvent, UserSubscription
from app.models.user import User, UserRole
from app.models.wallet import UserWallet
from app.services.billing.refunds import RefundError, reconcile_provider_refund, request_refund, transition_refund
from app.services.billing.subscriptions import cancel_at_period_end, start_free_trial, subscription_is_entitled
from app.services.wallet.wallet_service import get_or_create_wallet


def _user(db, role=UserRole.student):
    user = User(
        email=f"refund-{uuid.uuid4().hex[:12]}@example.com", full_name="Refund Test",
        hashed_password=get_password_hash("correct-horse-battery-staple"), role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _token(client, user):
    response = client.post("/api/v1/auth/login", json={
        "email": user.email, "password": "correct-horse-battery-staple",
    })
    assert response.status_code == 200
    return response.json()["access_token"]


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def _paid_order(db, user, *, age=timedelta(), amount=29900):
    plan = db.query(BillingPlan).filter_by(code="pro").one()
    now = datetime.now(timezone.utc)
    subscription = UserSubscription(
        user_id=user.id, plan_id=plan.id, status="active", billing_period="monthly",
        payment_provider="paymob", provider_subscription_id=f"txn-{uuid.uuid4().hex}",
        current_period_start=now - age, current_period_end=now + timedelta(days=30),
    )
    db.add(subscription)
    db.flush()
    order = SubscriptionOrder(
        user_id=user.id, plan_id=plan.id, billing_period="monthly", amount=amount,
        currency="EGP", provider="paymob", merchant_order_id=f"subscription-{uuid.uuid4().hex}",
        provider_order_id=str(uuid.uuid4().int % 10**10),
        provider_transaction_id=subscription.provider_subscription_id,
        subscription_id=subscription.id, status="paid", paid_at=now - age,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order, subscription


def _request(db, order, user, *, amount=None, key=None):
    return request_refund(
        db, order_id=order.id, user_id=user.id, amount=amount or order.amount,
        reason="Duplicate charge that needs review", confirmed=True,
        idempotency_key=key or f"request-{uuid.uuid4().hex}",
    )


def _transition(db, order, user, status, **kw):
    return transition_refund(
        db, order_id=order.id, to_status=status, actor_user_id=user.id,
        idempotency_key=f"transition-{status}-{uuid.uuid4().hex}", **kw,
    )


def test_every_order_gets_a_unique_immutable_nonsequential_reference(db):
    user = _user(db)
    plan = db.query(BillingPlan).filter_by(code="pro").one()
    orders = [
        SubscriptionOrder(
            user_id=user.id, plan_id=plan.id, billing_period="monthly", amount=29900,
            currency="EGP", provider="paymob", merchant_order_id=f"subscription-{uuid.uuid4().hex}",
            status="pending",
        )
        for _ in range(2)
    ]
    # The partial unique pending-order index allows only one open checkout per
    # account, so make the second a failed historical checkout.
    orders[1].status = "failed"
    db.add_all(orders)
    db.commit()
    assert all(order.reference_number.startswith("MSR-") for order in orders)
    assert len({order.reference_number for order in orders}) == 2
    assert all(len(order.reference_number.split("-")[-1]) == 8 for order in orders)

    orders[0].reference_number = "MSR-20261007-REPLACED"
    with pytest.raises(DBAPIError):
        db.commit()
    db.rollback()


def test_user_sees_own_reference_but_not_another_users_order(client, db):
    owner, stranger = _user(db), _user(db)
    order, _ = _paid_order(db, owner)
    own = client.get(
        f"/api/v1/billing/subscription-orders/by-reference/{order.reference_number}",
        headers=_headers(_token(client, owner)),
    )
    foreign = client.get(
        f"/api/v1/billing/subscription-orders/by-reference/{order.reference_number}",
        headers=_headers(_token(client, stranger)),
    )
    assert own.status_code == 200
    assert own.json()["reference_number"] == order.reference_number
    assert foreign.status_code == 404


def test_refund_request_is_reviewed_and_duplicate_requests_are_prevented(db):
    user = _user(db)
    order, _ = _paid_order(db, user)
    key = f"request-{uuid.uuid4().hex}"
    requested = _request(db, order, user, key=key)
    assert requested.refund_status == "requested"
    assert requested.status == "paid"
    # Retrying the same request is idempotent.
    assert _request(db, order, user, key=key).refund_status == "requested"
    assert db.query(SubscriptionRefundEvent).filter_by(order_id=order.id).count() == 1
    with pytest.raises(RefundError, match="not eligible") as duplicate:
        _request(db, order, user)
    assert duplicate.value.code == "DUPLICATE_REFUND_REQUEST"


def test_refund_amount_and_state_transitions_are_validated(db):
    user = _user(db)
    order, _ = _paid_order(db, user)
    with pytest.raises(RefundError) as too_much:
        _request(db, order, user, amount=order.amount + 1)
    assert too_much.value.code == "INVALID_REFUND_AMOUNT"

    _request(db, order, user)
    with pytest.raises(RefundError) as invalid:
        _transition(db, order, user, "refunded", provider_reference="refund-x")
    assert invalid.value.code == "INVALID_REFUND_TRANSITION"
    assert _transition(db, order, user, "under_review").refund_status == "under_review"
    assert _transition(db, order, user, "approved").refund_status == "approved"


def test_successful_refund_revokes_access_but_not_unrelated_wallet_credits(db):
    user = _user(db)
    order, subscription = _paid_order(db, user)
    wallet = get_or_create_wallet(user.id, db)
    wallet.credit_balance = 37
    db.commit()
    _request(db, order, user)
    _transition(db, order, user, "under_review")
    _transition(db, order, user, "approved")
    _transition(db, order, user, "processing")
    result = _transition(db, order, user, "refunded", provider_reference="paymob-refund-1")
    db.refresh(subscription)
    db.refresh(wallet)
    assert result.status == "refunded" and result.refund_status == "refunded"
    assert subscription.status == "expired"
    assert subscription_is_entitled(subscription) is False
    assert wallet.credit_balance == 37


def test_failed_provider_refund_is_audited_and_can_be_retried(db):
    user = _user(db)
    order, _ = _paid_order(db, user)
    _request(db, order, user)
    _transition(db, order, user, "under_review")
    _transition(db, order, user, "approved")
    _transition(db, order, user, "processing")
    failed = _transition(db, order, user, "failed", note="Provider timeout")
    assert failed.refund_status == "failed"
    assert failed.status == "paid"
    assert _transition(db, order, user, "processing").refund_status == "processing"


def test_duplicate_provider_refund_reconciliation_is_idempotent(db):
    user = _user(db)
    order, _ = _paid_order(db, user)
    reconcile_provider_refund(
        db, order=order, provider_event_id="provider-refund-duplicate",
        amount=order.amount, success=True,
    )
    db.commit()
    reconcile_provider_refund(
        db, order=order, provider_event_id="provider-refund-duplicate",
        amount=order.amount, success=True,
    )
    db.commit()
    assert db.query(SubscriptionRefundEvent).filter_by(order_id=order.id).count() == 1


def test_cancellation_never_becomes_a_refund(db):
    user = _user(db)
    order, _ = _paid_order(db, user)
    cancelled = cancel_at_period_end(db, user.id)
    db.refresh(order)
    assert cancelled.status == "cancelled"
    assert order.status == "paid"
    assert order.refund_status == "not_requested"


def test_trial_is_once_per_account_and_lasts_seven_days(db):
    user = _user(db)
    plan = db.query(BillingPlan).filter_by(code="pro").one()
    trial = start_free_trial(db, user.id, plan, "monthly")
    assert trial.status == "trialing"
    assert timedelta(days=6, hours=23) < trial.current_period_end - trial.current_period_start <= timedelta(days=7)
    assert subscription_is_entitled(trial)
    with pytest.raises(ValueError):
        start_free_trial(db, user.id, plan, "monthly")


def test_refund_policy_has_english_and_arabic_labels(client):
    english = client.get("/api/v1/legal/refund?lang=en")
    arabic = client.get("/api/v1/legal/refund?lang=ar")
    assert english.status_code == arabic.status_code == 200
    assert english.json()["title"] == "Refund Policy"
    assert arabic.json()["title"] == "سياسة الاسترداد"
    assert any("Cancellation is different" in section["heading"] for section in english.json()["sections"])
    assert any("الإلغاء مختلف عن الاسترداد" in section["heading"] for section in arabic.json()["sections"])
