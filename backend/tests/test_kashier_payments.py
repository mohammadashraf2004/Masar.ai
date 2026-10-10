"""
Kashier: every new payment's checkout, webhook and settlement (2026-10-08).

What must hold:
* every checkout (Pro, course, wallet top-up, exam fee) opens a Kashier hosted
  session and never a Paymob one;
* only a webhook with a valid x-kashier-signature, whose order/amount/currency/
  status are covered by that signature, and whose payment Kashier's own record
  confirms, settles anything - never the browser redirect;
* duplicates, refunds, partial refunds and declines behave exactly as before.
"""
import uuid
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from app.core.config import Settings, settings
from app.models.billing import BillingOrder, SubscriptionOrder, SubscriptionPaymentEvent, UserSubscription
from app.models.challenge import ExamPayment
from app.models.exam import Exam
from app.models.wallet import CreditPackage, TransactionStatus, UserWallet, WalletTransaction
from app.services.payments import kashier_service, paymob_service
from tests.kashier_fixtures import API_KEY, FakeKashier, kashier, sign  # noqa: F401


def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "email": f"kashier-{uuid.uuid4().hex[:12]}@example.com", "full_name": "Kashier Test",
        "password": "correct-horse-battery-staple-7", "accept_terms": True, "accept_privacy": True,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


def _subscribe(client, headers, period="monthly"):
    response = client.post("/api/v1/billing/subscriptions/checkout",
                           json={"plan": "pro", "billing_period": period}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def _order(db, body) -> SubscriptionOrder:
    db.expire_all()
    return db.get(SubscriptionOrder, body["order_id"])


def _sub(db, user_id):
    db.expire_all()
    return (db.query(UserSubscription).filter_by(user_id=user_id)
            .order_by(UserSubscription.current_period_end.desc()).first())


def _pay(kashier, client, order, *, amount="299.00", transaction_id=None, status="SUCCESS", record_status="PAID"):
    session_id = kashier.session_of(order.merchant_order_id)
    kashier.record(session_id, order.merchant_order_id, amount, status=record_status)
    data = kashier.data(order.merchant_order_id, amount, status=status, transaction_id=transaction_id)
    return kashier.post(client, data), data


# ── The signature ───────────────────────────────────────────────────────────────

def test_the_signature_follows_kashiers_documented_recipe():
    data = {"amount": 1, "channel": "online | e-commerce", "currency": "EGP", "ignored": "x",
            "signatureKeys": ["currency", "channel", "amount"]}
    # The documented example string: sorted keys, values URL-encoded.
    assert kashier_service.signature_payload(data) == "amount=1&channel=online%20%7C%20e-commerce&currency=EGP"


def test_signature_verification(monkeypatch):
    monkeypatch.setattr(settings, "KASHIER_API_KEY", API_KEY)
    data = FakeKashier.data("ref-1", "299.00")
    good = sign(data)
    assert kashier_service.verify_signature(data, good)
    assert kashier_service.verify_signature(data, good.upper())          # hex case does not matter
    assert not kashier_service.verify_signature({**data, "amount": "1.00"}, good)
    assert not kashier_service.verify_signature(data, sign(data, key="another-merchants-key"))
    assert not kashier_service.verify_signature(data, "")
    assert not kashier_service.verify_signature("not a dict", good)
    monkeypatch.setattr(settings, "KASHIER_API_KEY", None)
    assert not kashier_service.verify_signature(data, good)               # no key: nothing verifies


def test_amounts_are_converted_exactly():
    assert kashier_service.minor_to_major(29900) == "299.00"
    assert kashier_service.minor_to_major(1) == "0.01"
    assert kashier_service.major_to_minor("2199.00") == 219900
    assert kashier_service.major_to_minor(299) == 29900
    assert kashier_service.major_to_minor("1.005") == -1                  # below a piaster: unreadable
    assert kashier_service.major_to_minor("abc") == -1
    with pytest.raises(ValueError):
        kashier_service.minor_to_major(0)


# ── Opening a checkout ────────────────────────────────────────────────────────

def test_create_session_calls_the_documented_endpoint_with_the_right_keys(monkeypatch):
    for name, value in (("KASHIER_MODE", "test"), ("KASHIER_MERCHANT_ID", "MID-1"), ("KASHIER_API_KEY", "api-k"),
                        ("KASHIER_SECRET_KEY", "secret-k"), ("KASHIER_PUBLIC_API_URL", "https://api.masar.test/")):
        monkeypatch.setattr(settings, name, value)
    sent = {}

    def fake_post(url, json, headers, timeout):
        sent.update(url=url, body=json, headers=headers)
        return httpx.Response(200, json={"_id": "sess-1", "sessionUrl": "https://pay.kashier.io/s/1"},
                              request=httpx.Request("POST", url))

    monkeypatch.setattr(kashier_service.httpx, "post", fake_post)
    session = kashier_service.create_session(
        amount_minor=29900, currency="EGP", merchant_order_id="subscription-1-abc", description="Masar Pro",
        customer_email="a@example.com", customer_reference="1", language="ar", kind="subscription",
    )
    assert session == {"session_id": "sess-1", "checkout_url": "https://pay.kashier.io/s/1"}
    assert sent["url"] == "https://test-api.kashier.io/v3/payment/sessions"
    assert sent["headers"]["Authorization"] == "secret-k" and sent["headers"]["api-key"] == "api-k"
    body = sent["body"]
    assert (body["amount"], body["currency"], body["order"], body["merchantId"]) == ("299.00", "EGP", "subscription-1-abc", "MID-1")
    assert body["serverWebhook"] == "https://api.masar.test/api/v1/payments/kashier/webhook"
    assert body["merchantRedirect"] == "https://api.masar.test/api/v1/payments/kashier/return?ref=subscription-1-abc"
    assert body["display"] == "ar" and body["type"] == "one-time" and body["enable3DS"] is True
    assert body["paymentType"] == "credit" and "redirectMethod" not in body   # documented example sends null

    monkeypatch.setattr(settings, "KASHIER_MODE", "live")
    kashier_service.create_session(amount_minor=100, currency="EGP", merchant_order_id="x", description="d",
                                   customer_email="a@example.com", customer_reference="1", kind="k")
    assert sent["url"] == "https://api.kashier.io/v3/payment/sessions"


def test_every_checkout_opens_kashier_and_never_paymob(client, db, kashier, monkeypatch):
    def paymob_must_not_run(**kwargs):
        raise AssertionError("a new Paymob payment was started")

    monkeypatch.setattr(paymob_service, "init_payment_minor", paymob_must_not_run)
    monkeypatch.setattr(paymob_service, "init_payment", paymob_must_not_run)
    user_id, headers = _register(client)

    body = _subscribe(client, headers, period="yearly")
    order = _order(db, body)
    assert (order.provider, order.amount) == ("kashier", 219900)
    assert order.provider_order_id == kashier.session_of(order.merchant_order_id)
    assert body["payment_url"] == f"https://checkout.kashier.test/{order.provider_order_id}"
    assert kashier.sessions[order.provider_order_id]["amount_minor"] == 219900

    package = CreditPackage(name="Starter", credits=100, bonus_credits=0, egp_price=50.0, is_active=True)
    db.add(package)
    db.commit()
    topup = client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers)
    assert topup.status_code == 200, topup.text
    tx = db.query(WalletTransaction).filter_by(payment_ref=topup.json()["merchant_order_id"]).one()
    assert tx.provider_order_id == kashier.session_of(tx.payment_ref)
    assert kashier.sessions[tx.provider_order_id]["amount_minor"] == 5000


def test_payments_switched_off_is_a_clean_503_that_leaves_no_order_behind(client, db, monkeypatch):
    for name in ("KASHIER_MERCHANT_ID", "KASHIER_API_KEY", "KASHIER_SECRET_KEY", "KASHIER_PUBLIC_API_URL"):
        monkeypatch.setattr(settings, name, None)
    user_id, headers = _register(client)
    response = client.post("/api/v1/billing/subscriptions/checkout",
                           json={"plan": "pro", "billing_period": "monthly"}, headers=headers)
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "PAYMENTS_UNAVAILABLE"
    db.expire_all()
    assert db.query(SubscriptionOrder).filter_by(user_id=user_id).count() == 0


def _payment_rows(db, user_id) -> dict:
    """How many rows one user has in every table a checkout writes to."""
    db.expire_all()
    wallet_ids = [wallet.id for wallet in db.query(UserWallet).filter_by(user_id=user_id)]
    return {
        "subscription_orders": db.query(SubscriptionOrder).filter_by(user_id=user_id).count(),
        "billing_orders": db.query(BillingOrder).filter_by(user_id=user_id).count(),
        "wallet_transactions": (
            db.query(WalletTransaction).filter(WalletTransaction.wallet_id.in_(wallet_ids)).count()
            if wallet_ids else 0
        ),
        "exam_payments": db.query(ExamPayment).filter_by(user_id=user_id).count(),
    }


def test_the_master_switch_keeps_checkout_closed_even_with_every_key_present(client, db, kashier, monkeypatch):
    """Keys alone never open payments: PAYMENTS_ENABLED is the deliberate act.

    Every checkout is given real inputs (a pack, an exam, a Pro plan), so a missing
    gate would write an order or open a session instead of merely failing on a 404."""
    from app.models.learning import CareerTrack

    monkeypatch.setattr(settings, "PAYMENTS_ENABLED", False)
    assert settings.kashier_configured and not settings.payments_open     # the keys really are present
    user_id, headers = _register(client)
    package = CreditPackage(name="Starter", credits=100, bonus_credits=0, egp_price=50.0, is_active=True)
    track = CareerTrack(slug=f"switch-exam-{uuid.uuid4().hex[:8]}", title="Exam Track", estimated_weeks=1)
    db.add_all([package, track])
    db.flush()
    exam = Exam(track_id=track.id, title="Certification", duration_minutes=60, passing_score=70, max_attempts=3,
                questions=[{"id": 1, "question": "2+2?", "options": ["3", "4"], "correct": 1,
                            "explanation": "arithmetic", "points": 1, "type": "mcq"}])
    db.add(exam)
    db.commit()
    package_id, exam_id, track_id = package.id, exam.id, track.id
    try:
        before = _payment_rows(db, user_id)
        calls = {
            "/api/v1/billing/subscriptions/checkout": {"plan": "pro", "billing_period": "monthly"},
            "/api/v1/billing/checkout": {"course_id": "1"},
            "/api/v1/payments/wallet/topup/init": {"package_id": package_id},
            "/api/v1/payments/exam/init": {"exam_id": exam_id},
        }
        for url, body in calls.items():
            response = client.post(url, json=body, headers=headers)
            assert response.status_code == 503, url
            detail = response.json()["detail"]
            assert detail["code"] == "PAYMENTS_UNAVAILABLE" and detail["message_ar"], url
        assert _payment_rows(db, user_id) == before
        assert kashier.sessions == {}

        # Anonymous callers are turned away by authentication, never told about the gateway.
        for url, body in calls.items():
            assert client.post(url, json=body).status_code == 401, url
    finally:
        # The test database is shared for the whole session: leave no active pack in the
        # catalogue and no track behind (test_credit_packs reads the full pack list).
        db.rollback()
        db.query(Exam).filter(Exam.id == exam_id).delete()
        db.query(CareerTrack).filter(CareerTrack.id == track_id).delete()
        db.query(CreditPackage).filter(CreditPackage.id == package_id).delete()
        db.commit()


def test_payments_are_off_unless_someone_turns_them_on():
    assert Settings.model_fields["PAYMENTS_ENABLED"].default is False
    assert Settings(_env_file=None).PAYMENTS_ENABLED is False


def test_a_webhook_cannot_settle_anything_when_no_key_is_configured(client, db, monkeypatch):
    """No Payment API key: nothing verifies, not even a signature made with an empty key."""
    monkeypatch.setattr(settings, "KASHIER_API_KEY", None)
    data = FakeKashier.data("wallet-forged-1", "50.00")
    before = db.query(WalletTransaction).count()
    for signature in ("deadbeef", sign(data, key=""), ""):
        response = client.post("/api/v1/payments/kashier/webhook", json={"event": "pay", "data": data},
                               headers={"x-kashier-signature": signature})
        assert response.status_code == 401, signature
    db.expire_all()
    assert db.query(WalletTransaction).count() == before


def test_the_paymob_webhook_cannot_settle_anything_when_no_secret_is_configured(client, db, monkeypatch):
    monkeypatch.setattr(settings, "PAYMOB_HMAC_SECRET", None)
    payload = {"obj": {"id": 9, "success": True, "amount_cents": 5000, "currency": "EGP",
                       "order": {"id": 9, "merchant_order_id": "wallet-forged-2"}}}
    before = db.query(WalletTransaction).count()
    for received in ("deadbeef", ""):
        response = client.post("/api/v1/payments/paymob/webhook", json=payload, params={"hmac": received})
        assert response.status_code == 401, received
    db.expire_all()
    assert db.query(WalletTransaction).count() == before


def test_a_refused_session_fails_the_order(client, db, kashier):
    kashier.create_fails = httpx.HTTPStatusError(
        "400", request=httpx.Request("POST", "https://x"), response=httpx.Response(400, text="ERR_ORD_02"))
    user_id, headers = _register(client)
    response = client.post("/api/v1/billing/subscriptions/checkout",
                           json={"plan": "pro", "billing_period": "monthly"}, headers=headers)
    assert response.status_code == 502 and "ERR_ORD_02" not in response.text
    db.expire_all()
    assert [o.status for o in db.query(SubscriptionOrder).filter_by(user_id=user_id)] == ["failed"]


# ── Settling a Pro subscription ────────────────────────────────────────────────

def test_a_confirmed_payment_activates_pro_exactly_once(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    response, data = _pay(kashier, client, order)
    assert response.status_code == 200 and response.json() == {"status": "processed", "kind": "subscription", "success": True}
    sub = _sub(db, user_id)
    assert (sub.status, sub.payment_provider, sub.provider_subscription_id) == ("active", "kashier", data["transactionId"])
    end = sub.current_period_end

    replay = kashier.post(client, data)                                   # Kashier retries the same event
    assert replay.json()["status"] == "already_processed"
    assert _sub(db, user_id).current_period_end == end
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id).count() == 1

    second_charge, _ = _pay(kashier, client, order, transaction_id="TX-another-charge")
    assert second_charge.json()["status"] == "already_processed"        # one order buys one period
    assert _sub(db, user_id).current_period_end == end
    assert _order(db, {"order_id": order.id}).status == "paid"


def test_the_redirect_back_grants_nothing(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    back = client.get(f"/api/v1/payments/kashier/return?ref={order.merchant_order_id}"
                      "&paymentStatus=SUCCESS&merchantOrderId=x&signature=forged", follow_redirects=False)
    assert back.status_code in (302, 307)
    assert back.headers["location"].endswith(f"/billing/success?reference={order.reference_number}")
    assert _sub(db, user_id) is None and _order(db, {"order_id": order.id}).status == "pending"


@pytest.mark.parametrize("signature", ["", "0" * 64, "forged"])
def test_an_unsigned_or_forged_webhook_changes_nothing(client, db, kashier, signature):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    kashier.record(order.provider_order_id, order.merchant_order_id, "299.00")
    data = kashier.data(order.merchant_order_id, "299.00")
    assert kashier.post(client, data, signature=signature).status_code == 401
    assert _sub(db, user_id) is None


def test_fields_outside_the_signature_are_refused(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    kashier.record(order.provider_order_id, order.merchant_order_id, "299.00")
    data = kashier.data(order.merchant_order_id, "299.00", signed=("transactionId", "status"))
    assert kashier.post(client, data).status_code == 400
    assert _sub(db, user_id) is None


def test_success_is_only_believed_once_kashier_confirms_it(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    data = kashier.data(order.merchant_order_id, "299.00")

    kashier.record(order.provider_order_id, order.merchant_order_id, "299.00", status="PENDING")
    assert kashier.post(client, data).status_code == 503                 # Kashier retries later
    kashier.lookup_fails = True
    assert kashier.post(client, data).status_code == 503
    assert _sub(db, user_id) is None and _order(db, {"order_id": order.id}).status == "pending"

    kashier.lookup_fails = False
    kashier.record(order.provider_order_id, order.merchant_order_id, "299.00", status="PAID")
    assert kashier.post(client, data).json()["success"] is True           # the retry settles it
    assert _sub(db, user_id).status == "active"


def test_kashiers_record_decides_the_amount_and_the_order(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    data = kashier.data(order.merchant_order_id, "299.00")

    kashier.record(order.provider_order_id, order.merchant_order_id, "1.00")    # paid one pound
    assert kashier.post(client, data).json()["status"] == "rejected"
    assert _sub(db, user_id) is None
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=order.id).one().response_code == "amount_mismatch"

    other_user, other_headers = _register(client)
    other = _order(db, _subscribe(client, other_headers))
    kashier.record(other.provider_order_id, "someone-elses-order", "299.00")   # session paid another order
    assert kashier.post(client, kashier.data(other.merchant_order_id, "299.00")).json()["status"] == "rejected"
    assert _sub(db, other_user) is None


def test_a_declined_payment_fails_the_order_without_access(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    response = kashier.post(client, kashier.data(order.merchant_order_id, "299.00", status="FAILURE"))
    assert response.json() == {"status": "processed", "kind": "subscription", "success": False}
    assert _order(db, {"order_id": order.id}).status == "failed" and _sub(db, user_id) is None


def test_a_paymob_callback_cannot_settle_a_kashier_order(client, db, kashier, monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", "paymob-secret")
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    notice = paymob_service.to_notice({
        "id": 555, "amount_cents": order.amount, "currency": "EGP", "success": True, "pending": False,
        "order": {"id": order.provider_order_id, "merchant_order_id": order.merchant_order_id},
    })
    from app.services.payments.settlement import settle_notice
    assert settle_notice(db, notice)["status"] == "rejected"
    assert _sub(db, user_id) is None


# ── Refunds ────────────────────────────────────────────────────────────────────
# A refund changes access only once Kashier's session document shows it, for this
# order: the webhook amount's unit is not documented, so it is never trusted alone.

def test_a_full_refund_ends_only_that_orders_period_and_is_idempotent(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "299.00")
    refund = kashier.data(order.merchant_order_id, "299.00", transaction_id="TX-refund-1")
    assert kashier.post(client, refund, event="refund").json()["status"] == "processed"
    order = _order(db, {"order_id": order.id})
    assert (order.status, order.refund_status, order.refund_amount) == ("refunded", "refunded", 29900)
    assert _sub(db, user_id).status == "expired"
    assert kashier.post(client, refund, event="refund").json()["status"] == "already_processed"


def test_a_partial_refund_keeps_pro(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    end = _sub(db, user_id).current_period_end
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "100.00")
    partial = kashier.data(order.merchant_order_id, "100.00", transaction_id="TX-partial-1")
    assert kashier.post(client, partial, event="partial_refund").status_code == 200
    assert _order(db, {"order_id": order.id}).refund_amount == 10000
    sub = _sub(db, user_id)
    assert sub.status == "active" and sub.current_period_end == end


def test_a_refund_kashier_does_not_show_yet_waits_and_changes_nothing(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    refund = kashier.data(order.merchant_order_id, "299.00", transaction_id="TX-refund-early")
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "0")
    assert kashier.post(client, refund, event="refund").status_code == 503
    kashier.lookup_fails = True
    assert kashier.post(client, refund, event="refund").status_code == 503
    assert _sub(db, user_id).status == "active" and _order(db, {"order_id": order.id}).status == "paid"

    kashier.lookup_fails = False
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "299.00")
    assert kashier.post(client, refund, event="refund").json()["status"] == "processed"   # the retry applies it


def test_a_refund_amount_in_the_wrong_unit_never_ends_pro(client, db, kashier):
    """If Kashier sent piasters (299 for 2.99 EGP) where pounds are assumed, the amount
    read (299 EGP, the whole order) is more than the session shows refunded: it waits."""
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "2.99")
    misread = kashier.data(order.merchant_order_id, "299", transaction_id="TX-unit")
    assert kashier.post(client, misread, event="refund").status_code == 503
    assert _sub(db, user_id).status == "active"


def test_a_refund_on_another_orders_session_is_refused(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    kashier.refunded(order.provider_order_id, "someone-elses-order", "299.00")
    refund = kashier.data(order.merchant_order_id, "299.00", transaction_id="TX-refund-x")
    assert kashier.post(client, refund, event="refund").json()["status"] == "rejected"
    assert _sub(db, user_id).status == "active"


def test_a_refund_larger_than_the_payment_is_refused(client, db, kashier):
    user_id, headers = _register(client)
    order = _order(db, _subscribe(client, headers))
    _pay(kashier, client, order)
    kashier.refunded(order.provider_order_id, order.merchant_order_id, "299.01")
    too_much = kashier.data(order.merchant_order_id, "299.01", transaction_id="TX-refund-x")
    assert kashier.post(client, too_much, event="refund").json()["status"] == "rejected"
    assert _sub(db, user_id).status == "active"


# ── Renewal, cancellation ──────────────────────────────────────────────────────

def test_a_failed_renewal_keeps_the_paid_period_and_grants_nothing(client, db, kashier):
    user_id, headers = _register(client)
    _pay(kashier, client, _order(db, _subscribe(client, headers)))
    paid = _sub(db, user_id)
    end, subscription_id = paid.current_period_end, paid.id

    renewal = _order(db, _subscribe(client, headers))                       # renew before it ends
    declined = kashier.post(client, kashier.data(renewal.merchant_order_id, "299.00", status="FAILURE"))
    assert declined.json() == {"status": "processed", "kind": "subscription", "success": False}
    assert _order(db, {"order_id": renewal.id}).status == "failed"
    sub = _sub(db, user_id)
    assert (sub.id, sub.status, sub.current_period_end) == (subscription_id, "active", end)

    # A success claim Kashier's own record does not back grants nothing either.
    kashier.record(kashier.session_of(renewal.merchant_order_id), renewal.merchant_order_id, "299.00",
                   status="PENDING")
    assert kashier.post(client, kashier.data(renewal.merchant_order_id, "299.00")).status_code == 503
    db.expire_all()
    assert db.query(UserSubscription).filter_by(user_id=user_id).count() == 1
    assert _sub(db, user_id).current_period_end == end
    assert db.query(SubscriptionPaymentEvent).filter_by(order_id=renewal.id, grants_period=True).count() == 0

    # The failed renewal does not block another attempt.
    assert client.post("/api/v1/billing/subscriptions/checkout",
                       json={"plan": "pro", "billing_period": "monthly"}, headers=headers).status_code == 200


def test_manual_renewal_extends_from_the_current_end_and_cancellation_keeps_the_paid_period(client, db, kashier):
    user_id, headers = _register(client)
    _pay(kashier, client, _order(db, _subscribe(client, headers)))
    first_end = _sub(db, user_id).current_period_end
    _pay(kashier, client, _order(db, _subscribe(client, headers)))                 # renew before it ends
    assert _sub(db, user_id).current_period_end == first_end + timedelta(days=30)

    cancelled = client.post("/api/v1/billing/subscription/cancel", headers=headers)
    assert cancelled.status_code == 200
    sub = _sub(db, user_id)
    assert sub.status == "cancelled" and sub.current_period_end == first_end + timedelta(days=30)


# ── Wallet top-ups and exam fees ───────────────────────────────────────────────

def test_a_wallet_top_up_is_credited_once(client, db, kashier):
    user_id, headers = _register(client)
    package = CreditPackage(name="Pack", credits=100, bonus_credits=20, egp_price=50.0, is_active=True)
    db.add(package)
    db.commit()
    ref = client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id},
                      headers=headers).json()["merchant_order_id"]
    session_id = kashier.session_of(ref)
    kashier.record(session_id, ref, "50.00")
    data = kashier.data(ref, "50.00")
    assert kashier.post(client, data).json() == {"status": "processed", "kind": "wallet_topup", "success": True}
    assert kashier.post(client, data).json()["status"] in {"no matching pending transaction", "processed"}
    db.expire_all()
    assert db.query(UserWallet).filter_by(user_id=user_id).one().credit_balance == 40 + 120
    assert db.query(WalletTransaction).filter_by(payment_ref=ref).one().status == TransactionStatus.confirmed


def test_an_exam_fee_is_confirmed_by_the_webhook_only(client, db, kashier):
    from app.models.learning import CareerTrack

    user_id, headers = _register(client)
    track = CareerTrack(slug=f"kashier-exam-{uuid.uuid4().hex[:8]}", title="Exam Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    exam = Exam(track_id=track.id, title="Certification", duration_minutes=60, passing_score=70, max_attempts=3,
                questions=[{"id": 1, "question": "2+2?", "options": ["3", "4"], "correct": 1,
                            "explanation": "arithmetic", "points": 1, "type": "mcq"}])
    db.add(exam)
    db.commit()
    ref = client.post("/api/v1/payments/exam/init", json={"exam_id": exam.id}, headers=headers).json()["merchant_order_id"]
    payment = db.query(ExamPayment).filter_by(payment_ref=ref).one()
    assert payment.provider_order_id == kashier.session_of(ref) and payment.status == "pending"
    kashier.record(payment.provider_order_id, ref, "150.00")
    assert kashier.post(client, kashier.data(ref, "150.00")).json()["success"] is True
    db.expire_all()
    assert db.query(ExamPayment).filter_by(payment_ref=ref).one().status == "confirmed"


# ── Configuration ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("values, production, expected", [
    ({}, True, []),                                                      # payments off: allowed
    ({"KASHIER_MERCHANT_ID": "MID-1"}, False, ["partly configured"]),
    ({"KASHIER_MERCHANT_ID": "M", "KASHIER_API_KEY": "a", "KASHIER_SECRET_KEY": "s",
      "KASHIER_PUBLIC_API_URL": "https://api.x"}, True, ["must be live"]),
    ({"KASHIER_MODE": "live", "KASHIER_MERCHANT_ID": "M", "KASHIER_API_KEY": "a", "KASHIER_SECRET_KEY": "s",
      "KASHIER_PUBLIC_API_URL": "http://api.x"}, True, ["https://"]),
    ({"KASHIER_MODE": "live", "KASHIER_MERCHANT_ID": "M", "KASHIER_API_KEY": "a", "KASHIER_SECRET_KEY": "s",
      "KASHIER_PUBLIC_API_URL": "https://api.x"}, True, []),
    ({"KASHIER_MODE": "sandbox"}, False, ["test or live"]),
])
def test_kashier_configuration_fails_closed(values, production, expected):
    problems = Settings(_env_file=None, **values).kashier_problems(production=production)
    assert len(problems) == len(expected)
    for fragment, problem in zip(expected, problems):
        assert fragment in problem


@pytest.mark.parametrize("enabled, keys, expected", [
    (False, False, False),
    (False, True, False),   # keys alone never open payments
    (True, False, False),   # the switch alone never opens payments
    (True, True, True),
])
def test_payments_open_needs_the_switch_and_every_key(enabled, keys, expected):
    values = {"PAYMENTS_ENABLED": enabled}
    if keys:
        values.update(KASHIER_MERCHANT_ID="M", KASHIER_API_KEY="a", KASHIER_SECRET_KEY="s",
                      KASHIER_PUBLIC_API_URL="https://api.x")
    assert Settings(_env_file=None, **values).payments_open is expected


def test_the_switch_without_a_configured_gateway_is_refused_at_boot():
    problems = Settings(_env_file=None, PAYMENTS_ENABLED=True).kashier_problems(production=True)
    assert any("PAYMENTS_ENABLED" in p for p in problems)
    assert Settings(_env_file=None).kashier_problems(production=True) == []
