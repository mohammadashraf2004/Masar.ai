"""
Adversarial billing checks written during the 2026-10 release audit.

They complement test_payment_webhook_binding.py / test_subscription_refunds.py with
the cases those do not cover: concurrent delivery of the same or competing
callbacks (real separate DB sessions, not the shared test client), the reviewed
refund workflow racing the provider's refund callback, refunding one of several
paid periods, and a declined-then-approved retry on a wallet top-up.
"""
import threading
import uuid
from datetime import datetime, timedelta, timezone

from app.db.session import SessionLocal
from app.models.billing import SubscriptionOrder, SubscriptionPaymentEvent, UserSubscription
from app.models.challenge import ExamPayment
from app.models.wallet import TransactionStatus, WalletTransaction
from app.services.billing.refunds import request_refund, transition_refund
from app.services.billing.subscriptions import has_pro_access, process_paymob_subscription_webhook

from tests.test_payment_webhook_binding import (  # noqa: F401  (autouse HMAC secret fixture)
    _balance, _id, _obj, _period_end, _post, _secret, _sub_obj, _subscription_order, _topup, _user, exam,
)
from tests.test_subscription_refunds import _token, _user as _login_user


def _race(fn, n=8):
    """Run fn(session) in n threads released together; each gets its own session."""
    barrier, results, errors = threading.Barrier(n), [], []

    def run():
        session = SessionLocal()
        try:
            barrier.wait()
            results.append(fn(session))
        except Exception as exc:  # noqa: BLE001 - the assertion is on what happened
            session.rollback()
            errors.append(exc)
        finally:
            session.close()

    threads = [threading.Thread(target=run) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    return results, errors


def _workflow_to_processing(db, order, user, admin_id):
    request_refund(db, order_id=order.id, user_id=user.id, amount=order.amount,
                   reason="Not what I expected", confirmed=True, idempotency_key=uuid.uuid4().hex)
    for status in ("under_review", "approved", "processing"):
        transition_refund(db, order_id=order.id, to_status=status, actor_user_id=admin_id,
                          idempotency_key=uuid.uuid4().hex)


# ─── Concurrency ─────────────────────────────────────────────────────────────

def test_the_same_success_callback_delivered_concurrently_grants_one_period(db):
    user = _user(db)
    order = _subscription_order(db, user)
    obj = _sub_obj(order)
    results, errors = _race(lambda s: process_paymob_subscription_webhook(s, obj))
    assert not errors, errors
    assert sum(1 for r in results if r["status"] == "processed" and r["success"]) == 1
    end, count = _period_end(db, user)
    assert count == 1
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id, grants_period=True).count() == 1


def test_competing_success_transactions_for_one_order_grant_one_period(db):
    user = _user(db)
    order = _subscription_order(db, user)
    objs = iter([_sub_obj(order) for _ in range(8)])
    lock = threading.Lock()

    def deliver(session):
        with lock:
            obj = next(objs)
        return process_paymob_subscription_webhook(session, obj)

    results, errors = _race(deliver)
    assert not errors, errors
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id, grants_period=True).count() == 1
    end, count = _period_end(db, user)
    assert count == 1
    assert end - datetime.now(timezone.utc) < timedelta(days=31)


# ─── Forged binding ──────────────────────────────────────────────────────────

def test_another_users_signed_payment_cannot_fail_or_settle_a_victims_order(client, db):
    attacker, victim = _user(db), _user(db)
    mine = _subscription_order(db, attacker)
    theirs = _subscription_order(db, victim)
    # The attacker's own signed transaction, re-sent under the victim's merchant order id.
    lifted = _obj(provider_order=mine.provider_order_id, merchant_order_id=theirs.merchant_order_id,
                  amount=theirs.amount)
    assert _post(client, lifted).json()["success"] is False
    assert not has_pro_access(db, victim.id)
    # The victim's genuine payment still settles their order.
    assert _post(client, _sub_obj(theirs)).json()["success"] is True
    db.expire_all()
    assert has_pro_access(db, victim.id)


# ─── Refund entitlement ──────────────────────────────────────────────────────

def test_a_refund_completed_by_the_provider_callback_ends_the_access_it_bought(client, db):
    """Normal operations: staff approve the request, mark it processing, refund in
    the Paymob dashboard, and Paymob's refund callback arrives before staff click
    "refunded". The money is back; the Pro period it paid for must not survive."""
    user, admin = _user(db), _user(db)
    order = _subscription_order(db, user)
    paid = _sub_obj(order)
    assert _post(client, paid).json()["success"] is True
    db.expire_all()
    order = db.get(SubscriptionOrder, order.id)
    _workflow_to_processing(db, order, user, admin.id)

    refund = _sub_obj(order, is_refund=True, has_parent_transaction=True)
    _post(client, refund)
    db.expire_all()
    order = db.get(SubscriptionOrder, order.id)
    assert order.refund_status == "refunded"
    assert not has_pro_access(db, user.id), "refunded payment still grants Pro"


def test_refunding_one_paid_period_keeps_the_other_paid_period(client, db):
    user, admin = _user(db), _user(db)
    first = _subscription_order(db, user)
    assert _post(client, _sub_obj(first)).json()["success"] is True
    second = _subscription_order(db, user)
    assert _post(client, _sub_obj(second)).json()["success"] is True
    end_two_periods, _ = _period_end(db, user)

    db.expire_all()
    second = db.get(SubscriptionOrder, second.id)
    _workflow_to_processing(db, second, user, admin.id)
    transition_refund(db, order_id=second.id, to_status="refunded", actor_user_id=admin.id,
                      idempotency_key=uuid.uuid4().hex, provider_reference="rf-1")
    db.expire_all()
    assert has_pro_access(db, user.id), "refunding period 2 also took away paid period 1"
    end, _ = _period_end(db, user)
    assert end_two_periods - end >= timedelta(days=29)


def test_a_learner_cannot_pre_claim_the_providers_refund_idempotency_key(client, db):
    user = _login_user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    db.expire_all()
    order = db.get(SubscriptionOrder, order.id)
    refund_txn = _id()
    headers = {"Authorization": f"Bearer {_token(client, user)}"}
    response = client.post(
        f"/api/v1/billing/subscription-orders/{order.reference_number}/refund", headers=headers,
        json={"reason": "please refund", "confirmed": True,
              "idempotency_key": f"provider-refund:paymob:{refund_txn}"},
    )
    assert response.status_code == 201, response.text
    _post(client, _sub_obj(order, txn=refund_txn, is_refund=True, has_parent_transaction=True))
    db.expire_all()
    assert db.get(SubscriptionOrder, order.id).refund_status == "refunded"


def test_staff_completion_then_the_provider_callback_revokes_only_once(client, db):
    user, admin = _user(db), _user(db)
    first = _subscription_order(db, user)
    assert _post(client, _sub_obj(first)).json()["success"] is True
    second = _subscription_order(db, user)
    assert _post(client, _sub_obj(second)).json()["success"] is True
    end_two, _ = _period_end(db, user)
    db.expire_all()
    second = db.get(SubscriptionOrder, second.id)
    _workflow_to_processing(db, second, user, admin.id)
    transition_refund(db, order_id=second.id, to_status="refunded", actor_user_id=admin.id,
                      idempotency_key=uuid.uuid4().hex, provider_reference="rf-2")
    # Paymob's callbacks for that same refund arrive afterwards - a success and
    # a stray failure. Neither may take a second period or reopen the refund.
    _post(client, _sub_obj(second, is_refund=True, has_parent_transaction=True))
    _post(client, _sub_obj(second, is_refund=True, has_parent_transaction=True, success=False))
    db.expire_all()
    assert db.get(SubscriptionOrder, second.id).refund_status == "refunded"
    assert has_pro_access(db, user.id)
    end, _ = _period_end(db, user)
    assert timedelta(days=29) <= end_two - end <= timedelta(days=31)


def test_a_partial_provider_refund_is_recorded_and_keeps_access(client, db):
    user = _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    partial = _obj(provider_order=order.provider_order_id, merchant_order_id=order.merchant_order_id,
                   amount=order.amount // 2, is_refund=True, has_parent_transaction=True)
    _post(client, partial)
    db.expire_all()
    order = db.get(SubscriptionOrder, order.id)
    assert order.refund_status == "refunded" and order.refund_amount == order.amount // 2
    assert has_pro_access(db, user.id)
    too_much = _obj(provider_order=order.provider_order_id, merchant_order_id=order.merchant_order_id,
                    amount=order.amount + 1, is_refund=True, has_parent_transaction=True)
    assert _post(client, too_much).json()["status"] == "rejected"


# ─── Wallet top-up retry ─────────────────────────────────────────────────────

def test_a_declined_attempt_then_an_approved_retry_on_one_top_up_pays_out(client, db):
    """Paymob lets the buyer retry inside one payment key (one provider order):
    the first card is declined, the second is charged. The charge must credit."""
    user = _user(db)
    provider_order = str(_id())
    tx = _topup(db, user, egp=50.0, credits=100, provider_order=provider_order)
    before = _balance(db, user)
    declined = _obj(provider_order=provider_order, merchant_order_id=tx.payment_ref, amount=5000, success=False)
    approved = _obj(provider_order=provider_order, merchant_order_id=tx.payment_ref, amount=5000)
    _post(client, declined)
    _post(client, approved)
    assert _balance(db, user) == before + 100, "card was charged but no credits were granted"
    db.expire_all()
    assert db.get(WalletTransaction, tx.id).status == TransactionStatus.confirmed


def test_a_declined_attempt_then_an_approved_retry_on_one_exam_fee_confirms_it(client, db, exam):
    user = _user(db)
    provider_order = str(_id())
    payment = ExamPayment(user_id=user.id, exam_id=exam.id, egp_amount=150.0, payment_method="card",
                          payment_ref=f"exam-{uuid.uuid4().hex}", provider_order_id=provider_order,
                          status="pending")
    db.add(payment)
    db.commit()
    for success in (False, True):
        _post(client, _obj(provider_order=provider_order, merchant_order_id=payment.payment_ref,
                           amount=15000, success=success))
    db.expire_all()
    assert db.get(ExamPayment, payment.id).status == "confirmed"


def test_a_partial_refund_completed_by_staff_keeps_access(client, db):
    """Approved policy: a partial refund never removes Pro; only a verified FULL refund ends the
    period its order bought (and only that period)."""
    user, admin = _user(db), _user(db)
    order = _subscription_order(db, user)
    assert _post(client, _sub_obj(order)).json()["success"] is True
    end_before, _ = _period_end(db, user)
    db.expire_all()
    order = db.get(SubscriptionOrder, order.id)
    request_refund(db, order_id=order.id, user_id=user.id, amount=order.amount // 3,
                   reason="Partial goodwill refund", confirmed=True, idempotency_key=uuid.uuid4().hex)
    for status in ("under_review", "approved", "processing"):
        transition_refund(db, order_id=order.id, to_status=status, actor_user_id=admin.id,
                          idempotency_key=uuid.uuid4().hex)
    transition_refund(db, order_id=order.id, to_status="refunded", actor_user_id=admin.id,
                      idempotency_key=uuid.uuid4().hex, provider_reference="rf-partial")
    db.expire_all()
    assert db.get(SubscriptionOrder, order.id).refund_status == "refunded"
    assert has_pro_access(db, user.id)
    assert _period_end(db, user)[0] == end_before
