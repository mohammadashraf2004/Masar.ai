"""
Paymob callbacks can only settle the record they were signed for, once.

The HMAC covers the transaction (id, amount, currency, success/pending,
refund/void flags, Paymob's order id) but NOT `order.merchant_order_id`. A
learner sees the signed fields of their own payment in the browser redirect,
so these tests replay real-looking signed payloads under other merchant order
ids, as refunds, twice, and after an order is already paid.
"""
import hashlib
import hmac as hmac_lib
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash
from app.models.billing import BillingPlan, SubscriptionOrder, SubscriptionPaymentEvent, UserSubscription
from app.models.challenge import ExamPayment
from app.models.exam import Exam
from app.models.learning import CareerTrack
from app.models.user import User
from app.models.wallet import PaymentMethod, TransactionStatus, TransactionType, UserWallet, WalletTransaction
from app.services.payments import paymob_service
from app.services.wallet.wallet_service import get_or_create_wallet
from tests.kashier_fixtures import kashier  # noqa: F401

SECRET = "binding-webhook-secret"


@pytest.fixture(autouse=True)
def _secret(monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)


def _id() -> int:
    return uuid.uuid4().int % 10**12


def _sign(obj: dict) -> str:
    concatenated = "".join(
        paymob_service._stringify(paymob_service._extract(obj, f)) for f in paymob_service._HMAC_FIELDS
    )
    return hmac_lib.new(SECRET.encode(), concatenated.encode(), hashlib.sha512).hexdigest()


def _obj(*, provider_order: str, merchant_order_id: str, amount: int, txn: int | None = None,
         success: bool = True, pending: bool = False, **flags) -> dict:
    obj = {
        "amount_cents": amount, "created_at": "2026-10-07T10:00:00.000000", "currency": "EGP",
        "error_occured": False, "has_parent_transaction": False, "id": txn or _id(),
        "integration_id": 1, "is_3d_secure": True, "is_auth": False, "is_capture": False,
        "is_refunded": False, "is_standalone_payment": True, "is_voided": False,
        "order": {"id": int(provider_order), "merchant_order_id": merchant_order_id},
        "owner": 1, "pending": pending,
        "source_data": {"pan": "1234", "sub_type": "MasterCard", "type": "card"}, "success": success,
    }
    obj.update(flags)
    return obj


def _post(client, obj: dict):
    return client.post(f"/api/v1/payments/paymob/webhook?hmac={_sign(obj)}", json={"obj": obj})


def _user(db) -> User:
    user = User(email=f"bind-{uuid.uuid4().hex[:12]}@example.com", full_name="Bind Test",
                hashed_password=get_password_hash("x"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _topup(db, user, *, egp=50.0, credits=100, provider_order: str | None = None) -> WalletTransaction:
    wallet = get_or_create_wallet(user.id, db)
    tx = WalletTransaction(
        wallet_id=wallet.id, transaction_type=TransactionType.topup, status=TransactionStatus.pending,
        credits=credits, egp_amount=egp, payment_method=PaymentMethod.card,
        payment_ref=f"wallet-{uuid.uuid4().hex}", provider_order_id=provider_order,
        description="test package", balance_after=wallet.credit_balance,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def _balance(db, user) -> int:
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user.id).one().credit_balance


# ─── Wallet top-ups ─────────────────────────────────────────────────────────

def test_a_cheap_signed_payment_cannot_settle_a_different_top_up(client, db):
    user = _user(db)
    cheap = _topup(db, user, egp=50.0, credits=100, provider_order=str(_id()))
    big = _topup(db, user, egp=500.0, credits=5000, provider_order=str(_id()))
    paid = _obj(provider_order=cheap.provider_order_id, merchant_order_id=cheap.payment_ref, amount=5000)
    assert _post(client, paid).json()["success"] is True
    assert _balance(db, user) == 100

    # Same signed fields, merchant_order_id swapped to the expensive top-up.
    replay = dict(paid, order={"id": int(cheap.provider_order_id), "merchant_order_id": big.payment_ref})
    response = _post(client, replay)
    assert response.json() == {"status": "rejected", "kind": "wallet_topup", "success": False}
    db.expire_all()
    assert db.get(WalletTransaction, big.id).status == TransactionStatus.pending
    assert _balance(db, user) == 100


def test_amount_and_currency_must_match_the_top_up(client, db):
    user = _user(db)
    tx = _topup(db, user, egp=50.0, provider_order=str(_id()))
    for bad in (_obj(provider_order=tx.provider_order_id, merchant_order_id=tx.payment_ref, amount=100),
                _obj(provider_order=tx.provider_order_id, merchant_order_id=tx.payment_ref, amount=5000,
                     currency="USD")):
        assert _post(client, bad).json()["status"] == "rejected"
    assert _balance(db, user) == 0


def test_a_refund_or_void_callback_never_settles_a_top_up(client, db):
    user = _user(db)
    tx = _topup(db, user, provider_order=str(_id()))
    for flags in ({"is_refunded": True}, {"is_voided": True}, {"is_refund": True},
                  {"has_parent_transaction": True}, {"is_auth": True}):
        obj = _obj(provider_order=tx.provider_order_id, merchant_order_id=tx.payment_ref, amount=5000, **flags)
        assert _post(client, obj).json()["success"] is False
    db.expire_all()
    assert db.get(WalletTransaction, tx.id).status == TransactionStatus.pending
    assert _balance(db, user) == 0


def test_one_paymob_transaction_settles_at_most_one_top_up(client, db):
    user = _user(db)
    shared_order = str(_id())
    first = _topup(db, user, provider_order=shared_order)
    second = _topup(db, user, provider_order=shared_order)
    txn = _id()
    assert _post(client, _obj(provider_order=shared_order, merchant_order_id=first.payment_ref,
                              amount=5000, txn=txn)).json()["success"] is True
    again = _post(client, _obj(provider_order=shared_order, merchant_order_id=second.payment_ref,
                               amount=5000, txn=txn))
    assert again.json()["status"] == "rejected"
    assert _balance(db, user) == 100


def test_a_top_up_created_before_the_binding_is_left_for_manual_review(client, db):
    user = _user(db)
    legacy = _topup(db, user, provider_order=None)
    obj = _obj(provider_order=str(_id()), merchant_order_id=legacy.payment_ref, amount=5000)
    assert _post(client, obj).json()["status"] == "rejected"
    db.expire_all()
    assert db.get(WalletTransaction, legacy.id).status == TransactionStatus.pending
    assert _balance(db, user) == 0


def test_the_database_refuses_one_transaction_id_on_two_top_ups(db):
    user = _user(db)
    a, b = _topup(db, user), _topup(db, user)
    a.provider_transaction_id = b.provider_transaction_id = "txn-dup"
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


# ─── Exam fees ──────────────────────────────────────────────────────────────

@pytest.fixture()
def exam(db):
    track = CareerTrack(slug=f"bind-track-{uuid.uuid4().hex[:8]}", title="Bind Track", estimated_weeks=1)
    db.add(track)
    db.commit()
    row = Exam(track_id=track.id, title=f"Cert {uuid.uuid4().hex[:8]}", description="x", questions=[])
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def test_an_exam_fee_cannot_be_settled_by_another_orders_signed_payment(client, db, exam):
    user = _user(db)
    target = ExamPayment(user_id=user.id, exam_id=exam.id, egp_amount=50.0, payment_method="card",
                         payment_ref=f"exam-{uuid.uuid4().hex}", provider_order_id=str(_id()), status="pending")
    db.add(target)
    db.commit()
    foreign = _obj(provider_order=str(_id()), merchant_order_id=target.payment_ref, amount=5000)
    assert _post(client, foreign).json()["status"] == "rejected"
    db.expire_all()
    assert db.get(ExamPayment, target.id).status == "pending"

    own = _obj(provider_order=target.provider_order_id, merchant_order_id=target.payment_ref, amount=5000)
    assert _post(client, own).json()["success"] is True
    db.expire_all()
    assert db.get(ExamPayment, target.id).status == "confirmed"


# ─── Subscriptions ──────────────────────────────────────────────────────────

def _subscription_order(db, user, *, status="pending", created_at=None, provider_order="auto") -> SubscriptionOrder:
    plan = db.query(BillingPlan).filter_by(code="pro").one()
    order = SubscriptionOrder(
        user_id=user.id, plan_id=plan.id, billing_period="monthly", amount=29900, currency="EGP",
        provider="paymob", merchant_order_id=f"subscription-{uuid.uuid4().hex}",
        provider_order_id=str(_id()) if provider_order == "auto" else provider_order, status=status,
    )
    if created_at is not None:
        order.created_at = created_at
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def _period_end(db, user):
    db.expire_all()
    rows = db.query(UserSubscription).filter_by(user_id=user.id).all()
    return max((r.current_period_end for r in rows), default=None), len(rows)


def _sub_obj(order, **kw):
    return _obj(provider_order=order.provider_order_id, merchant_order_id=order.merchant_order_id,
                amount=order.amount, **kw)


def test_a_refund_callback_never_extends_pro_and_marks_the_order_refunded(client, db):
    user = _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    end, count = _period_end(db, user)

    for flags in ({"is_refunded": True}, {"is_refund": True, "has_parent_transaction": True},
                  {"is_voided": True}):
        assert _post(client, _sub_obj(order, **flags)).json()["success"] is False
    # Never extended, never duplicated - and the one period the refunded
    # payment bought is gone (removed once, not once per reversal callback).
    new_end, new_count = _period_end(db, user)
    assert new_count == count and new_end <= end
    assert new_end <= datetime.now(timezone.utc) + timedelta(seconds=5)
    db.expire_all()
    assert db.get(SubscriptionOrder, order.id).status == "refunded"
    assert db.query(UserSubscription).filter_by(user_id=user.id).one().status == "expired"


def test_a_second_successful_transaction_on_a_paid_order_buys_nothing(client, db):
    user = _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    end, count = _period_end(db, user)
    for _ in range(3):
        assert _post(client, _sub_obj(order)).json()["status"] == "already_processed"
    assert _period_end(db, user) == (end, count)
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id, grants_period=True).count() == 1


def test_a_mismatched_or_declined_callback_cannot_unpay_a_paid_order(client, db):
    user = _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    _post(client, _obj(provider_order=order.provider_order_id, merchant_order_id=order.merchant_order_id,
                       amount=1))
    _post(client, _sub_obj(order, success=False))
    db.expire_all()
    assert db.get(SubscriptionOrder, order.id).status == "paid"


def test_a_decline_then_a_retry_on_the_same_order_still_grants_once(client, db):
    user = _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order, success=False)).json()["success"] is False
    assert _post(client, _sub_obj(order)).json()["success"] is True
    assert _period_end(db, user)[1] == 1


def test_the_database_allows_one_granting_event_per_order(db):
    user = _user(db)
    order = _subscription_order(db, user)
    for _ in range(2):
        db.add(SubscriptionPaymentEvent(order_id=order.id, provider="paymob", provider_event_id=str(_id()),
                                        amount=29900, currency="EGP", success=True, raw_payload={},
                                        grants_period=True))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


# ─── Abandoned checkouts ────────────────────────────────────────────────────

def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "email": f"stale-{uuid.uuid4().hex[:12]}@example.com", "full_name": "Stale Checkout",
        "password": "correct-horse-battery-staple-7", "accept_terms": True, "accept_privacy": True,
    })
    body = response.json()
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


def test_an_abandoned_checkout_stops_blocking_once_its_payment_key_expired(client, db, kashier):
    user_id, headers = _register(client)
    user = db.get(User, user_id)
    body = {"plan": "pro", "billing_period": "monthly"}

    fresh = _subscription_order(db, user)
    assert client.post("/api/v1/billing/subscriptions/checkout", json=body, headers=headers).status_code == 409

    fresh.created_at = datetime.now(timezone.utc) - timedelta(hours=2)
    db.commit()
    response = client.post("/api/v1/billing/subscriptions/checkout", json=body, headers=headers)
    assert response.status_code == 200, response.text
    db.expire_all()
    assert db.get(SubscriptionOrder, fresh.id).status == "cancelled"


def test_a_checkout_whose_provider_call_never_finished_does_not_block(client, db, kashier):
    user_id, headers = _register(client)
    user = db.get(User, user_id)
    _subscription_order(db, user, provider_order=None,
                        created_at=datetime.now(timezone.utc) - timedelta(minutes=5))
    response = client.post("/api/v1/billing/subscriptions/checkout",
                           json={"plan": "pro", "billing_period": "yearly"}, headers=headers)
    assert response.status_code == 200, response.text


def test_an_unexpected_provider_error_fails_the_order_instead_of_leaving_it_pending(client, db, kashier):
    kashier.create_fails = KeyError("token")
    user_id, headers = _register(client)
    response = client.post("/api/v1/billing/subscriptions/checkout",
                           json={"plan": "pro", "billing_period": "monthly"}, headers=headers)
    assert response.status_code == 502
    db.expire_all()
    statuses = [o.status for o in db.query(SubscriptionOrder).filter_by(user_id=user_id)]
    assert statuses == ["failed"]


def test_a_late_payment_for_a_replaced_checkout_is_still_honoured(client, db):
    user = _user(db)
    order = _subscription_order(db, user, status="cancelled")
    assert _post(client, _sub_obj(order)).json()["success"] is True
    assert _period_end(db, user)[1] == 1
