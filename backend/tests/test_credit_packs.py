"""
Additional AI credit packs, end to end against the real database.

The catalogue is server-owned; a purchase is a pending order that only a signed,
server-confirmed Kashier notice can pay out, exactly once; bought credits sit in their own
bucket that survives every plan change, is spent last, and is the only thing a Pro
subscriber can spend past the included allowance; refunds and chargebacks take credits
back without ever driving a balance negative.
"""
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.billing import BillingPlan, UserSubscription
from app.models.user import User
from app.models.wallet import CreditPackage, TransactionStatus, TransactionType, UserWallet, WalletTransaction
from app.services.billing import pro_ai_allowance as pro_ai
from app.services.billing.subscriptions import current_plan_code
from app.services.wallet import credit_purchases
from app.services.wallet.wallet_service import (
    deduct_credits, expire_promo_credits_if_due, get_or_create_wallet, refund_credits,
)
from tests.kashier_fixtures import API_KEY, FakeKashier, kashier, sign  # noqa: F401

PACKS = {"starter": (50, 29), "standard": (150, 69), "plus": (400, 149), "power": (1000, 299)}


@pytest.fixture(autouse=True)
def _fresh_request_scope():
    pro_ai.begin_request(None)
    yield


def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "email": f"packs-{uuid.uuid4().hex[:12]}@example.com", "full_name": "Pack Buyer",
        "password": "correct-horse-battery-staple-7", "accept_terms": True, "accept_privacy": True,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


def _verified_user(db, *, balance=0, purchased=0):
    user = User(email=f"packs-{uuid.uuid4().hex[:10]}@example.com", full_name="Pack User",
                hashed_password=get_password_hash("x"), is_verified=True)
    db.add(user)
    db.flush()
    db.add(UserWallet(user_id=user.id, credit_balance=balance, purchased_credits=purchased,
                      lifetime_purchased=purchased))
    db.commit()
    return user


def _subscribe(db, user, status="active", ends_in=timedelta(days=30)):
    plan = db.query(BillingPlan).filter(BillingPlan.code == "pro").one()
    now = datetime.now(timezone.utc)
    sub = UserSubscription(user_id=user.id, plan_id=plan.id, status=status, billing_period="monthly",
                           payment_provider="kashier", provider_subscription_id=f"t-{uuid.uuid4().hex}",
                           current_period_start=now - timedelta(days=1), current_period_end=now + ends_in)
    db.add(sub)
    db.commit()
    return sub


def _wallet(db, user_id):
    db.expire_all()
    return db.query(UserWallet).filter_by(user_id=user_id).one()


def _pack(db, code):
    return db.query(CreditPackage).filter_by(code=code).one()


def _buy(client, db, kashier, headers, code="plus"):
    """Open a checkout for a pack; returns (merchant_order_id, session_id, package)."""
    package = _pack(db, code)
    response = client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers)
    assert response.status_code == 200, response.text
    ref = response.json()["merchant_order_id"]
    return ref, kashier.session_of(ref), package


def _pay(client, kashier, ref, session_id, amount, **kw):
    kashier.record(session_id, ref, f"{amount:.2f}")
    return kashier.post(client, kashier.data(ref, f"{amount:.2f}", **kw))


# ── The catalogue ─────────────────────────────────────────────────────────────

def test_the_four_packs_have_the_agreed_credits_and_prices_and_plus_is_popular(client, db):
    packs = client.get("/api/v1/wallet/packages").json()
    assert [(p["code"], p["credits"], p["egp_price"]) for p in packs] == [
        (code, credits, float(price)) for code, (credits, price) in PACKS.items()]
    assert [p["is_popular"] for p in packs] == [False, False, True, False]
    assert all(p["bonus_credits"] == 0 for p in packs)


def test_the_billing_catalogue_serves_the_same_server_owned_packs(client, db):
    catalog = client.get("/api/v1/billing/catalog").json()
    assert [(p["code"], p["credits"], p["price"], p["popular"]) for p in catalog["packs"]] == [
        ("starter", 50, 29.0, False), ("standard", 150, 69.0, False), ("plus", 400, 149.0, True),
        ("power", 1000, 299.0, False)]


# ── Checkout: server-priced, authenticated, bounded ───────────────────────────

def test_checkout_charges_the_catalogue_price_whatever_the_request_says(client, db, kashier):
    _, headers = _register(client)
    package = _pack(db, "power")
    response = client.post("/api/v1/payments/wallet/topup/init", headers=headers, json={
        "package_id": package.id, "price": 1, "egp_amount": 1, "credits": 99999, "amount": 1})
    assert response.status_code == 200, response.text
    ref = response.json()["merchant_order_id"]
    assert kashier.sessions[kashier.session_of(ref)]["amount_minor"] == 29900
    tx = db.query(WalletTransaction).filter_by(payment_ref=ref).one()
    assert (tx.credits, tx.egp_amount, tx.status, tx.package_id) == (1000, 299.0, TransactionStatus.pending, package.id)


def test_checkout_needs_a_signed_in_account_and_a_real_active_pack(client, db, kashier):
    package = _pack(db, "plus")
    assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}).status_code in (401, 403)
    _, headers = _register(client)
    assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": 999999}, headers=headers).status_code == 404
    package.is_active = False
    db.commit()
    try:
        assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers).status_code == 404
    finally:
        package.is_active = True
        db.commit()


def test_a_buyer_cannot_stack_unpaid_orders_but_an_expired_one_does_not_block(client, db, kashier):
    user_id, headers = _register(client)
    package = _pack(db, "starter")
    for _ in range(credit_purchases.MAX_OPEN_ORDERS):
        assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers).status_code == 200
    assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers).status_code == 429
    old = datetime.now(timezone.utc) - timedelta(hours=3)
    db.query(WalletTransaction).filter_by(transaction_type=TransactionType.topup).filter(
        WalletTransaction.payment_ref.like("wallet-%")).update({WalletTransaction.created_at: old}, synchronize_session=False)
    db.commit()
    assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers).status_code == 200


def test_a_provider_failure_to_open_checkout_fails_the_order_and_credits_nothing(client, db, kashier):
    import httpx
    user_id, headers = _register(client)
    kashier.create_fails = httpx.ConnectError("down")
    package = _pack(db, "plus")
    assert client.post("/api/v1/payments/wallet/topup/init", json={"package_id": package.id}, headers=headers).status_code == 502
    db.expire_all()
    assert [t.status for t in db.query(WalletTransaction).filter_by(transaction_type=TransactionType.topup)
            .join(UserWallet).filter(UserWallet.user_id == user_id)] == [TransactionStatus.failed]
    assert _wallet(db, user_id).purchased_credits == 0


# ── Payment confirmation ──────────────────────────────────────────────────────

@pytest.mark.parametrize("code", list(PACKS))
def test_a_confirmed_payment_credits_the_pack_to_the_purchased_bucket_exactly_once(client, db, kashier, code):
    user_id, headers = _register(client)
    before = _wallet(db, user_id).credit_balance           # the Free signup grant
    ref, session_id, package = _buy(client, db, kashier, headers, code)
    credits, price = PACKS[code]
    assert _pay(client, kashier, ref, session_id, price).json() == {"status": "processed", "kind": "wallet_topup", "success": True}
    wallet = _wallet(db, user_id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (before + credits, credits)
    assert wallet.lifetime_purchased == credits
    tx = db.query(WalletTransaction).filter_by(payment_ref=ref).one()
    assert (tx.status, tx.purchased_delta, tx.package_id, tx.balance_after) == (
        TransactionStatus.confirmed, credits, package.id, before + credits)
    assert tx.settled_at is not None and tx.provider_transaction_id
    # the Free signup grant is preserved and not counted as bought
    assert wallet.credit_balance - wallet.purchased_credits == before


def test_replaying_the_same_webhook_never_grants_twice(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    kashier.record(session_id, ref, "149.00")
    data = kashier.data(ref, "149.00")
    for _ in range(4):
        kashier.post(client, data)
    assert _wallet(db, user_id).purchased_credits == 400
    assert db.query(WalletTransaction).filter_by(payment_ref=ref).count() == 1


def test_a_second_provider_transaction_for_a_paid_order_is_not_credited_again(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    _pay(client, kashier, ref, session_id, 149)
    _pay(client, kashier, ref, session_id, 149, transaction_id="TX-OTHER-1")
    assert _wallet(db, user_id).purchased_credits == 400


def test_a_forged_or_unsigned_notification_grants_nothing(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    kashier.record(session_id, ref, "149.00")
    data = kashier.data(ref, "149.00")
    assert kashier.post(client, data, signature="0" * 64).status_code == 401
    assert kashier.post(client, data, signature="").status_code == 401
    tampered = {**data, "amount": "1.00"}
    assert kashier.post(client, tampered, signature=sign(data)).status_code == 401
    unsigned_amount = kashier.data(ref, "149.00", signed=("currency", "merchantOrderId", "status", "transactionId"))
    assert kashier.post(client, unsigned_amount).status_code == 400
    assert _wallet(db, user_id).purchased_credits == 0


def test_a_payment_for_the_wrong_amount_or_session_is_rejected(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    assert _pay(client, kashier, ref, session_id, 29).json()["status"] == "rejected"      # paid the Starter price
    assert _wallet(db, user_id).purchased_credits == 0
    ref2, session2, _ = _buy(client, db, kashier, headers, "starter")
    kashier.record(session2, "wallet-someone-else", "29.00")                               # session paid another order
    assert kashier.post(client, kashier.data(ref2, "29.00")).status_code in (200, 503)
    assert _wallet(db, user_id).purchased_credits == 0


def test_pending_failed_and_declined_payments_credit_nothing_and_stay_retryable(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    kashier.record(session_id, ref, "149.00", status="PENDING")
    assert kashier.post(client, kashier.data(ref, "149.00", status="PENDING")).json()["success"] is False
    assert kashier.post(client, kashier.data(ref, "149.00", status="FAILURE")).json()["success"] is False
    assert _wallet(db, user_id).purchased_credits == 0
    assert db.query(WalletTransaction).filter_by(payment_ref=ref).one().status == TransactionStatus.pending
    # the buyer retries inside the same checkout and pays
    assert _pay(client, kashier, ref, session_id, 149).json()["success"] is True
    assert _wallet(db, user_id).purchased_credits == 400


def test_a_session_the_provider_does_not_show_paid_is_not_credited(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    kashier.record(session_id, ref, "149.00", status="PENDING")           # webhook says SUCCESS, record says not paid
    assert kashier.post(client, kashier.data(ref, "149.00")).status_code == 503
    kashier.lookup_fails = True
    assert kashier.post(client, kashier.data(ref, "149.00", transaction_id="TX-2")).status_code == 503
    assert _wallet(db, user_id).purchased_credits == 0


def test_the_browser_return_grants_nothing_and_points_at_the_buy_credits_page(client, db, kashier):
    user_id, headers = _register(client)
    ref, _, _ = _buy(client, db, kashier, headers, "plus")
    response = client.get(f"/api/v1/payments/kashier/return?ref={ref}", follow_redirects=False)
    assert response.status_code in (302, 307) and f"/billing/credits?reference={ref}" in response.headers["location"]
    assert _wallet(db, user_id).purchased_credits == 0
    status = client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()
    assert status["status"] == "pending" and status["order"]["status"] == "pending"


def test_the_status_and_history_endpoints_report_the_servers_record_to_the_owner_only(client, db, kashier):
    user_id, headers = _register(client)
    _, other = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    _pay(client, kashier, ref, session_id, 149)
    status = client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()
    assert status["status"] == "confirmed"
    assert (status["order"]["status"], status["order"]["credits"], status["order"]["package"]) == ("paid", 400, "Plus")
    assert client.get(f"/api/v1/payments/status/{ref}", headers=other).status_code == 404
    orders = client.get("/api/v1/wallet/purchases", headers=headers).json()["orders"]
    assert [(o["reference"], o["status"], o["price"]) for o in orders] == [(ref, "paid", 149.0)]
    assert client.get("/api/v1/wallet/purchases", headers=other).json()["orders"] == []
    wallet = client.get("/api/v1/wallet/", headers=headers).json()
    assert wallet["purchased_credits"] == 400 and wallet["included_credits"] == wallet["credit_balance"] - 400


def test_concurrent_duplicate_webhooks_credit_once(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    kashier.record(session_id, ref, "149.00")
    tx = db.query(WalletTransaction).filter_by(payment_ref=ref).one()
    tx_id = tx.id
    start = threading.Barrier(6, timeout=30)

    def settle(_):
        from app.services.wallet.wallet_service import confirm_pending_topup
        session = SessionLocal()
        try:
            start.wait()
            row = session.query(WalletTransaction).filter_by(id=tx_id).with_for_update().one()
            confirm_pending_topup(row, session)
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(settle, range(6)))
    assert _wallet(db, user_id).purchased_credits == 400


# ── Free, Pro and subscription changes ────────────────────────────────────────

def test_free_and_pro_accounts_can_both_buy_and_buying_never_touches_the_subscription(client, db, kashier):
    free_id, free_headers = _register(client)
    pro_id, pro_headers = _register(client)
    sub = _subscribe(db, db.get(User, pro_id))
    for uid, headers in ((free_id, free_headers), (pro_id, pro_headers)):
        ref, session_id, _ = _buy(client, db, kashier, headers, "standard")
        assert _pay(client, kashier, ref, session_id, 69).json()["success"] is True
        assert _wallet(db, uid).purchased_credits == 150
    db.expire_all()
    assert current_plan_code(db, free_id) == "free" and current_plan_code(db, pro_id) == "pro"
    refreshed = db.get(UserSubscription, sub.id)
    assert (refreshed.status, refreshed.current_period_end) == (sub.status, sub.current_period_end)


def test_purchased_credits_survive_renewal_cancellation_expiry_and_upgrade(db):
    user = _verified_user(db, balance=250, purchased=250)
    sub = _subscribe(db, user)
    for mutate in (
        lambda s: setattr(s, "current_period_end", s.current_period_end + timedelta(days=30)),   # renewal
        lambda s: (setattr(s, "status", "cancelled"), setattr(s, "cancel_at_period_end", True)),  # cancellation
        lambda s: (setattr(s, "status", "expired"), setattr(s, "current_period_end", datetime.now(timezone.utc) - timedelta(days=1))),
    ):
        mutate(sub)
        db.commit()
        assert (_wallet(db, user.id).credit_balance, _wallet(db, user.id).purchased_credits) == (250, 250)
    assert current_plan_code(db, user.id) == "free"
    _subscribe(db, user)                                                                       # upgrade again
    assert _wallet(db, user.id).purchased_credits == 250


def test_promo_expiry_never_takes_purchased_credits(db):
    user = _verified_user(db, balance=500, purchased=300)
    wallet = _wallet(db, user.id)
    wallet.promo_credits_remaining = 200
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()
    expire_promo_credits_if_due(wallet, db)
    wallet = _wallet(db, user.id)
    assert wallet.purchased_credits == 300 and wallet.credit_balance >= 300


# ── Spending ──────────────────────────────────────────────────────────────────

def test_free_accounts_spend_included_credits_first_then_purchased(db):
    user = _verified_user(db, balance=41, purchased=39)             # 2 included + 39 purchased
    assert deduct_credits(user.id, "mentor_chat", db)["purchased_credits_used"] == 0           # 2 included
    result = deduct_credits(user.id, "mentor_chat", db)                                        # 0 included -> purchased
    assert result["purchased_credits_used"] == 2
    wallet = _wallet(db, user.id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (37, 37)
    rows = db.query(WalletTransaction).filter_by(wallet_id=wallet.id, transaction_type=TransactionType.deduction).order_by(WalletTransaction.id).all()
    assert [r.purchased_delta for r in rows] == [0, -2]


def test_a_charge_that_straddles_included_and_purchased_credits_splits_correctly(db):
    user = _verified_user(db, balance=103, purchased=100)           # 3 included
    deduct_credits(user.id, "code_review", db)                      # 5 credits: 3 included + 2 purchased
    wallet = _wallet(db, user.id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (98, 98)
    row = db.query(WalletTransaction).filter_by(wallet_id=wallet.id, transaction_type=TransactionType.deduction).one()
    assert row.purchased_delta == -2


def test_pro_past_the_allowance_spends_purchased_credits_only(db):
    user = _verified_user(db, balance=130, purchased=30)            # 100 included credits must stay out of reach
    sub = _subscribe(db, user)
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 50)             # allowance used up
    result = deduct_credits(user.id, "mentor_chat", db)
    assert result["source"] == "purchased_credits" and result["credits_used"] == 2
    wallet = _wallet(db, user.id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (128, 28)


def test_pro_with_an_exhausted_allowance_and_no_purchased_credits_is_refused_and_keeps_signup_credits(db):
    user = _verified_user(db, balance=100, purchased=0)
    sub = _subscribe(db, user)
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 50)
    with pytest.raises(HTTPException) as refused:
        deduct_credits(user.id, "mentor_chat", db)
    assert refused.value.status_code == 429 and refused.value.detail["error"] == "pro_ai_limit_reached"
    assert _wallet(db, user.id).credit_balance == 100


def test_pro_inside_the_allowance_never_touches_purchased_credits(db):
    user = _verified_user(db, balance=100, purchased=100)
    _subscribe(db, user)
    deduct_credits(user.id, "mentor_chat", db)
    assert _wallet(db, user.id).purchased_credits == 100


def test_purchased_credits_have_their_own_daily_safety_limit_for_pro(db, monkeypatch):
    monkeypatch.setattr(settings, "PURCHASED_CREDITS_DAILY_LIMIT", 6)
    user = _verified_user(db, balance=1000, purchased=1000)
    sub = _subscribe(db, user)
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 50)
    for _ in range(3):
        deduct_credits(user.id, "mentor_chat", db)                  # 3 x 2 = 6
    with pytest.raises(HTTPException) as limited:
        deduct_credits(user.id, "mentor_chat", db)
    assert limited.value.status_code == 429 and limited.value.detail["error"] == "purchased_credits_daily_limit"
    assert _wallet(db, user.id).credit_balance == 994


def test_an_unverified_account_cannot_spend_purchased_credits(db):
    user = _verified_user(db, balance=100, purchased=100)
    user.is_verified = False
    db.commit()
    with pytest.raises(HTTPException) as refused:
        deduct_credits(user.id, "mentor_chat", db)
    assert refused.value.status_code in (401, 403)
    assert _wallet(db, user.id).credit_balance == 100


def test_a_failed_request_refunds_purchased_credits_back_to_the_purchased_bucket(db):
    user = _verified_user(db, balance=40, purchased=40)
    deduct_credits(user.id, "mentor_chat", db)
    refund_credits(user.id, "mentor_chat", db, reason="provider failed")
    wallet = _wallet(db, user.id)
    assert (wallet.credit_balance, wallet.purchased_credits, wallet.lifetime_spent) == (40, 40, 0)
    deduction = db.query(WalletTransaction).filter_by(wallet_id=wallet.id, transaction_type=TransactionType.deduction).one()
    refund = db.query(WalletTransaction).filter_by(wallet_id=wallet.id, transaction_type=TransactionType.refund).one()
    assert refund.related_tx_id == deduction.id and refund.purchased_delta == 2


def test_refunding_twice_cannot_mint_credits_beyond_what_was_charged(db):
    user = _verified_user(db, balance=40, purchased=40)
    deduct_credits(user.id, "mentor_chat", db)
    refund_credits(user.id, "mentor_chat", db, reason="failed")
    wallet = _wallet(db, user.id)
    assert wallet.purchased_credits == 40
    refund_credits(user.id, "mentor_chat", db, reason="failed again")      # no standing deduction to answer
    wallet = _wallet(db, user.id)
    assert wallet.purchased_credits == 40                                  # the bucket is not inflated


def test_a_retried_request_with_the_same_idempotency_key_is_not_charged_twice(db):
    user = _verified_user(db, balance=40, purchased=40)
    pro_ai.begin_request("key-123")
    deduct_credits(user.id, "mentor_chat", db)
    with pytest.raises(HTTPException) as dup:
        deduct_credits(user.id, "mentor_chat", db)
    assert dup.value.status_code == 409
    assert _wallet(db, user.id).credit_balance == 38
    refund_credits(user.id, "mentor_chat", db, reason="failed")
    deduct_credits(user.id, "mentor_chat", db)                              # after a refund the retry may charge again
    assert _wallet(db, user.id).credit_balance == 38


def test_concurrent_spends_never_overspend_the_wallet(db):
    user = _verified_user(db, balance=10, purchased=10)
    user_id = user.id
    start = threading.Barrier(8, timeout=30)

    def spend(_):
        session = SessionLocal()
        start.wait()
        try:
            deduct_credits(user_id, "mentor_chat", session)
            return True
        except HTTPException:
            return False
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(spend, range(8)))
    assert results.count(True) == 5                                         # 5 x 2 = 10
    wallet = _wallet(db, user_id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (0, 0)


def test_concurrent_purchase_and_spend_lose_no_update(db):
    user = _verified_user(db, balance=20, purchased=20)
    user_id = user.id
    wallet = _wallet(db, user_id)
    tx = WalletTransaction(wallet_id=wallet.id, transaction_type=TransactionType.topup, status=TransactionStatus.pending,
                           credits=400, egp_amount=149.0, payment_ref=f"wallet-{uuid.uuid4().hex}",
                           description="Plus", balance_after=20)
    db.add(tx)
    db.commit()
    tx_id = tx.id
    start = threading.Barrier(7, timeout=30)

    def work(i):
        from app.services.wallet.wallet_service import confirm_pending_topup
        session = SessionLocal()
        start.wait()
        try:
            if i == 0:
                confirm_pending_topup(session.query(WalletTransaction).filter_by(id=tx_id).with_for_update().one(), session)
            else:
                deduct_credits(user_id, "mentor_chat", session)
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=7) as pool:
        list(pool.map(work, range(7)))
    wallet = _wallet(db, user_id)
    assert wallet.credit_balance == 20 + 400 - 12 and wallet.purchased_credits == wallet.credit_balance


# ── Refunds and chargebacks ───────────────────────────────────────────────────

def _paid_order(client, db, kashier, code="plus"):
    user_id, headers = _register(client)
    ref, session_id, package = _buy(client, db, kashier, headers, code)
    _pay(client, kashier, ref, session_id, PACKS[code][1])
    return user_id, headers, ref, session_id


def _refund_webhook(client, kashier, ref, session_id, amount_major, refunded_total, *, tx=None):
    tx = tx or f"TX-R-{uuid.uuid4().hex[:10]}"
    kashier.refunded(session_id, ref, refunded_total)
    data = kashier.data(ref, amount_major, transaction_id=tx)
    return kashier.post(client, data, event="refund")


def test_a_provider_refund_takes_back_the_purchased_credits(client, db, kashier):
    user_id, headers, ref, session_id = _paid_order(client, db, kashier)
    before = _wallet(db, user_id)
    included = before.credit_balance - before.purchased_credits
    result = _refund_webhook(client, kashier, ref, session_id, "149.00", "149.00")
    assert result.json()["kind"] == "wallet_reversal", result.text
    wallet = _wallet(db, user_id)
    assert (wallet.purchased_credits, wallet.credit_balance) == (0, included)
    order = client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()["order"]
    assert order["status"] == "refunded" and order["credits_reversed"] == 400


def test_a_refund_replay_reverses_once(client, db, kashier):
    user_id, _, ref, session_id = _paid_order(client, db, kashier)
    for _ in range(3):
        _refund_webhook(client, kashier, ref, session_id, "149.00", "149.00", tx="TX-REPLAY-" + ref[-8:])
    assert _wallet(db, user_id).purchased_credits == 0
    assert db.query(WalletTransaction).filter_by(related_tx_id=db.query(WalletTransaction).filter_by(payment_ref=ref).one().id,
                                                 transaction_type=TransactionType.reversal).count() == 1


def test_a_partial_refund_takes_back_a_proportional_share_and_the_rest_completes_it(client, db, kashier):
    user_id, headers, ref, session_id = _paid_order(client, db, kashier, "plus")      # 400 credits / 149 EGP
    _refund_webhook(client, kashier, ref, session_id, "74.50", "74.50", tx="TX-R-A")
    wallet = _wallet(db, user_id)
    assert wallet.purchased_credits == 200
    assert client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()["order"]["status"] == "partially_refunded"
    _refund_webhook(client, kashier, ref, session_id, "74.50", "149.00", tx="TX-R-B")
    assert _wallet(db, user_id).purchased_credits == 0
    assert client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()["order"]["status"] == "refunded"


def test_refunding_after_the_credits_were_spent_never_goes_negative(client, db, kashier):
    user_id, headers, ref, session_id = _paid_order(client, db, kashier, "starter")   # 50 credits
    db.query(UserWallet).filter_by(user_id=user_id).update({UserWallet.credit_balance: 10, UserWallet.purchased_credits: 10})
    db.commit()                                                                         # 40 of the 50 already spent
    _refund_webhook(client, kashier, ref, session_id, "29.00", "29.00")
    wallet = _wallet(db, user_id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (0, 0)
    reversal = db.query(WalletTransaction).filter_by(transaction_type=TransactionType.reversal).order_by(WalletTransaction.id.desc()).first()
    assert reversal.credits == -10 and "40 already spent" in reversal.description


def test_a_refund_never_reaches_included_credits(client, db, kashier):
    user_id, _, ref, session_id = _paid_order(client, db, kashier, "starter")
    included = _wallet(db, user_id).credit_balance - 50
    db.query(UserWallet).filter_by(user_id=user_id).update({UserWallet.purchased_credits: 5, UserWallet.credit_balance: included + 5})
    db.commit()
    _refund_webhook(client, kashier, ref, session_id, "29.00", "29.00")
    assert _wallet(db, user_id).credit_balance == included


def test_a_forged_refund_or_one_for_another_order_changes_nothing(client, db, kashier):
    user_id, _, ref, session_id = _paid_order(client, db, kashier)
    data = kashier.data(ref, "149.00", transaction_id="TX-F-1")
    kashier.refunded(session_id, ref, "149.00")
    assert kashier.post(client, data, event="refund", signature="1" * 64).status_code == 401
    # the provider's session document shows no refund yet: wait (503), do not reverse
    kashier.documents[session_id]["refundedAmount"] = "0.00"
    assert kashier.post(client, data, event="refund").status_code == 503
    assert _wallet(db, user_id).purchased_credits == 400


def test_a_refund_of_more_than_was_paid_is_rejected(client, db, kashier):
    user_id, _, ref, session_id = _paid_order(client, db, kashier)
    result = _refund_webhook(client, kashier, ref, session_id, "500.00", "500.00")
    assert result.json()["status"] == "rejected"
    assert _wallet(db, user_id).purchased_credits == 400


def test_a_refund_of_an_order_that_was_never_paid_does_nothing(client, db, kashier):
    user_id, headers = _register(client)
    ref, session_id, _ = _buy(client, db, kashier, headers, "plus")
    result = _refund_webhook(client, kashier, ref, session_id, "149.00", "149.00")
    assert result.json()["status"] in {"rejected", "processed", "no matching pending transaction"}
    assert _wallet(db, user_id).purchased_credits == 0


def _admin(db):
    admin = User(email=f"admin-{uuid.uuid4().hex[:8]}@example.com", full_name="Admin",
                 hashed_password=get_password_hash("x"), is_verified=True)
    from app.models.user import UserRole
    admin.role = UserRole.admin
    db.add(admin)
    db.commit()
    return admin


def _token(client, db, user):
    from app.core.security import create_access_token
    return {"Authorization": f"Bearer {create_access_token(data={'sub': str(user.id), 'tv': user.token_version or 0})}"}


def test_a_chargeback_reconciled_by_staff_is_idempotent_and_marks_the_order_disputed(client, db, kashier):
    user_id, headers, ref, _ = _paid_order(client, db, kashier)
    admin_headers = _token(client, db, _admin(db))
    url = f"/api/v1/wallet/admin/purchases/{ref}/reverse"
    body = {"kind": "chargeback", "idempotency_key": "dispute-0001"}
    first = client.post(url, json=body, headers=admin_headers)
    assert first.status_code == 200, first.text
    assert first.json()["status"] == "processed"
    assert client.post(url, json=body, headers=admin_headers).json()["status"] == "already_processed"
    assert _wallet(db, user_id).purchased_credits == 0
    assert client.get(f"/api/v1/payments/status/{ref}", headers=headers).json()["order"]["status"] == "chargeback"


def test_reconciliation_is_for_admins_only(client, db, kashier):
    _, headers, ref, _ = _paid_order(client, db, kashier)
    response = client.post(f"/api/v1/wallet/admin/purchases/{ref}/reverse", headers=headers,
                           json={"kind": "refund", "idempotency_key": "nope-0001"})
    assert response.status_code in (401, 403)


def test_a_wallet_row_can_never_be_made_negative_in_the_database(db):
    user = _verified_user(db, balance=5, purchased=5)
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        db.query(UserWallet).filter_by(user_id=user.id).update({UserWallet.purchased_credits: -1})
        db.commit()
    db.rollback()


# ── Migration and ledger ──────────────────────────────────────────────────────

def test_legacy_manual_topups_still_credit_through_the_same_path(db):
    user = _verified_user(db, balance=0)
    from app.services.wallet.wallet_service import add_credits
    add_credits(user.id, 100, db, egp_amount=50.0, payment_method="card", payment_ref="manual-1")
    wallet = _wallet(db, user.id)
    assert (wallet.credit_balance, wallet.purchased_credits) == (100, 100)


def test_every_purchase_is_traceable_from_wallet_row_to_payment_order(client, db, kashier):
    user_id, _, ref, session_id = _paid_order(client, db, kashier)
    _refund_webhook(client, kashier, ref, session_id, "149.00", "149.00")
    rows = db.query(WalletTransaction).join(UserWallet).filter(UserWallet.user_id == user_id).order_by(WalletTransaction.id).all()
    order = next(r for r in rows if r.payment_ref == ref)
    reversal = next(r for r in rows if r.transaction_type == TransactionType.reversal)
    assert order.package_id and order.provider_order_id == session_id and order.provider_transaction_id
    assert reversal.related_tx_id == order.id and reversal.provider_transaction_id
    assert sum(r.purchased_delta for r in rows) == 0                      # bought, then fully taken back
