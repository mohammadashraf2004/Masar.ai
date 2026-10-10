"""
Pro's included AI usage: 50 credits per rolling 4 hours (2026-10-08).

A Pro subscriber's AI actions are paid from the allowance, never from the wallet;
when it is used up the request is refused before the provider is called. These
tests pin the window arithmetic, the HTTP contract, refunds, idempotency,
concurrency and every subscription state, against the real database.
"""
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.billing import BillingPlan, ProAiUsage, UserSubscription
from app.models.learning_path import Course
from app.models.user import User
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services.billing import pro_ai_allowance as pro_ai
from app.services.billing.access_service import course_access
from app.services.wallet.wallet_service import CREDIT_COSTS, deduct_credits, refund_credits

T0 = datetime(2026, 10, 8, 10, 0, tzinfo=timezone.utc)
WINDOW = timedelta(seconds=14400)


def _user(db, balance=100):
    user = User(email=f"pro-ai-{uuid.uuid4().hex[:10]}@example.com", full_name="Pro", hashed_password="x",
                is_verified=True)
    db.add(user)
    db.flush()
    db.add(UserWallet(user_id=user.id, credit_balance=balance, lifetime_purchased=balance))
    db.commit()
    return user


def _subscribe(db, user, status="active", ends_in=timedelta(days=30), plan_code="pro", period="monthly"):
    plan = db.query(BillingPlan).filter(BillingPlan.code == plan_code).one()
    now = datetime.now(timezone.utc)
    sub = UserSubscription(user_id=user.id, plan_id=plan.id, status=status, billing_period=period,
                           payment_provider="kashier", provider_subscription_id=f"t-{uuid.uuid4().hex}",
                           current_period_start=now - timedelta(days=1), current_period_end=now + ends_in)
    db.add(sub)
    db.commit()
    return sub


@pytest.fixture()
def pro(db):
    user = _user(db)
    return user, _subscribe(db, user)


@pytest.fixture(autouse=True)
def _fresh_request_scope():
    """Each test is one 'request': its own charge list and no idempotency key."""
    pro_ai.begin_request(None)
    yield


def _wallet(db, user):
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user.id).one()


def _usages(db, user):
    db.expire_all()
    return db.query(ProAiUsage).filter(ProAiUsage.user_id == user.id).order_by(ProAiUsage.id).all()


def _use(db, user, sub, credits, at, action="mentor_chat"):
    """One successful AI action at `at`: reserved, then consumed when its request answered."""
    usage = pro_ai.reserve(db, user.id, sub, action, credits, now=at)
    pro_ai.finalize(db, [usage.id], now=at)
    return usage


# ── The rolling window ─────────────────────────────────────────────────────────

def test_the_documented_example_20_then_30_then_rolling_back(db, pro):
    user, sub = pro
    _use(db, user, sub, 20, T0)
    _use(db, user, sub, 30, T0 + timedelta(hours=1))

    status = pro_ai.allowance_status(db, user.id, now=T0 + timedelta(hours=1, minutes=1))
    assert (status.used, status.remaining) == (50, 0)
    assert status.next_credit_available_at == T0 + WINDOW            # when the first 20 leave the window
    with pytest.raises(pro_ai.AllowanceExceeded) as refused:
        _use(db, user, sub, 2, T0 + timedelta(hours=2))
    assert refused.value.available_at == T0 + WINDOW

    later = T0 + WINDOW + timedelta(seconds=1)                       # the 20 are back, the 30 are not
    status = pro_ai.allowance_status(db, user.id, now=later)
    assert (status.used, status.remaining, status.next_credit_available_at) == (30, 20, None)
    _use(db, user, sub, 20, later)
    with pytest.raises(pro_ai.AllowanceExceeded) as refused:
        _use(db, user, sub, 1, later)
    assert refused.value.available_at == T0 + timedelta(hours=1) + WINDOW


def test_unused_allowance_never_accumulates_beyond_50(db, pro):
    user, sub = pro
    much_later = T0 + timedelta(days=30)
    assert pro_ai.allowance_status(db, user.id, now=much_later).remaining == 50
    with pytest.raises(pro_ai.AllowanceExceeded):
        pro_ai.reserve(db, user.id, sub, "mentor_chat", 51, now=much_later)


def test_a_partial_fit_reports_when_enough_comes_back(db, pro):
    user, sub = pro
    _use(db, user, sub, 30, T0)
    _use(db, user, sub, 17, T0 + timedelta(minutes=30))
    with pytest.raises(pro_ai.AllowanceExceeded) as refused:          # 3 left, 5 needed
        _use(db, user, sub, 5, T0 + timedelta(hours=1), action="code_review")
    assert refused.value.status.remaining == 3
    assert refused.value.status.next_credit_available_at is None      # credits remain, just not enough
    assert refused.value.available_at == T0 + WINDOW                  # the 30 free up the 2 missing


def test_a_long_call_counts_once_from_the_moment_it_was_let_through(db, pro):
    user, sub = pro
    usage = pro_ai.reserve(db, user.id, sub, "mock_interview", 3, now=T0 + WINDOW - timedelta(seconds=5))
    pro_ai.finalize(db, [usage.id], now=T0 + WINDOW + timedelta(minutes=2))   # finished after a boundary
    assert pro_ai.allowance_status(db, user.id, now=T0 + WINDOW).used == 3
    assert pro_ai.allowance_status(db, user.id, now=T0 + 2 * WINDOW).used == 0
    assert _usages(db, user)[0].status == "consumed"


def test_a_reservation_nobody_settled_is_given_back(db, pro):
    """A worker killed mid-request delivered nothing: once the reservation lifetime
    has passed, those credits stop counting and are released with the reason."""
    user, sub = pro
    ttl = timedelta(seconds=settings.PRO_AI_RESERVATION_TTL_SECONDS)
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 2, now=T0)
    assert pro_ai.allowance_status(db, user.id, now=T0 + ttl - timedelta(seconds=1)).used == 2
    assert pro_ai.allowance_status(db, user.id, now=T0 + ttl + timedelta(seconds=1)).used == 0
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 2, now=T0 + ttl + timedelta(seconds=1))
    first, second = _usages(db, user)
    assert (first.status, first.release_reason) == ("released", pro_ai.UNSETTLED)
    assert second.status == "reserved"
    assert pro_ai.allowance_status(db, user.id, now=T0 + ttl + timedelta(seconds=2)).used == 2


# ── Through deduct_credits / refund_credits ────────────────────────────────────

def test_pro_ai_actions_draw_on_the_allowance_and_never_on_the_wallet(db, pro):
    user, _ = pro
    result = deduct_credits(user.id, "code_review", db)
    assert result["source"] == "pro_allowance"
    assert result["allowance_remaining"] == 50 - CREDIT_COSTS["code_review"]
    assert _wallet(db, user).credit_balance == 100
    assert db.query(WalletTransaction).filter(WalletTransaction.action_type == "code_review",
                                              WalletTransaction.wallet_id == _wallet(db, user).id).count() == 0
    [usage] = _usages(db, user)
    assert (usage.action_type, usage.credits, usage.status) == ("code_review", 5, "reserved")


def test_an_exhausted_allowance_is_429_before_the_provider_and_keeps_purchased_credits(db, pro):
    user, sub = pro
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 49)
    with pytest.raises(HTTPException) as refused:
        deduct_credits(user.id, "code_review", db)
    assert refused.value.status_code == 429
    detail = refused.value.detail
    assert detail["error"] == "pro_ai_limit_reached"
    assert (detail["limit"], detail["window_seconds"], detail["used"], detail["remaining"],
            detail["credits_needed"]) == (50, 14400, 49, 1, 5)
    assert detail["retry_at"] and "Retry-After" in refused.value.headers
    assert "course access remains available" in detail["message"]
    assert _wallet(db, user).credit_balance == 100                    # never silently spent
    assert len(_usages(db, user)) == 1


def test_the_limit_message_when_nothing_is_left(db, pro):
    user, sub = pro
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 50)
    with pytest.raises(HTTPException) as refused:
        deduct_credits(user.id, "mentor_chat", db)
    assert refused.value.detail["message"] == (
        "You've used your 50 included AI credits for the current 4-hour window. Your course access "
        "remains available. More AI credits will become available as earlier usage leaves the window.")
    assert refused.value.detail["next_credit_available_at"] is not None


def test_a_failed_provider_call_gives_the_credits_back_to_the_allowance(db, pro):
    user, _ = pro
    deduct_credits(user.id, "mentor_chat", db)
    refund_credits(user.id, "mentor_chat", db, reason="provider timeout")
    [usage] = _usages(db, user)
    assert usage.status == "released" and usage.released_at is not None
    assert usage.release_reason == "provider timeout"
    assert pro_ai.allowance_status(db, user.id).used == 0
    assert _wallet(db, user).credit_balance == 100                     # the wallet was never touched
    assert db.query(WalletTransaction).filter(WalletTransaction.wallet_id == _wallet(db, user).id,
                                              WalletTransaction.transaction_type == TransactionType.refund).count() == 0

    refund_credits(user.id, "mentor_chat", db, reason="refunded twice by mistake")   # idempotent
    assert _wallet(db, user).credit_balance == 100
    assert pro_ai.release(db, usage.id) is False


def test_a_repeated_request_key_cannot_charge_or_run_twice(db, pro):
    user, sub = pro
    pro_ai.begin_request("client-message-1")
    deduct_credits(user.id, "mentor_message", db)
    with pytest.raises(HTTPException) as again:
        deduct_credits(user.id, "mentor_message", db)
    assert again.value.status_code == 409 and again.value.detail["error"] == "duplicate_request"
    assert pro_ai.allowance_status(db, user.id).used == 2

    # After the first attempt failed and was released, the same key may retry once.
    refund_credits(user.id, "mentor_message", db, reason="failed")
    pro_ai.begin_request("client-message-1")
    deduct_credits(user.id, "mentor_message", db)
    assert [u.status for u in _usages(db, user)] == ["reserved"]
    assert pro_ai.allowance_status(db, user.id).used == 2


def test_concurrent_requests_never_pass_50(db, pro):
    user, sub = pro
    user_id, sub_id = user.id, sub.id       # read here: the fixture's session is not for threads
    workers = 8
    # A timeout, so a pool that cannot hand every worker a connection fails the
    # test instead of hanging it. Each worker's connection is taken after the
    # barrier and given back between attempts.
    start = threading.Barrier(workers, timeout=30)

    def attempt(_):
        start.wait()
        results = []
        for _ in range(4):
            session = SessionLocal()
            try:
                subscription = session.get(UserSubscription, sub_id)
                pro_ai.reserve(session, user_id, subscription, "mentor_chat", 2)
                results.append(True)
            except pro_ai.AllowanceExceeded:
                results.append(False)
            finally:
                session.close()
        return results

    with ThreadPoolExecutor(max_workers=workers) as pool:
        outcomes = [ok for batch in pool.map(attempt, range(workers)) for ok in batch]
    assert len(outcomes) == 32 and outcomes.count(True) == 25          # 25 x 2 = 50, never more
    assert pro_ai.allowance_status(db, user.id).used == 50


def test_free_accounts_keep_paying_from_the_wallet(db):
    user = _user(db, balance=40)
    result = deduct_credits(user.id, "mentor_chat", db)
    assert "source" not in result and result["balance_after"] == 38
    assert _usages(db, user) == []


def test_non_ai_spends_stay_on_the_wallet_for_pro(db, pro):
    user, _ = pro
    deduct_credits(user.id, "challenge_enroll", db, cost=25, description="Enrolled in challenge: X")
    assert _wallet(db, user).credit_balance == 75
    assert _usages(db, user) == []


# ── Subscription states ─────────────────────────────────────────────────────────

def test_trials_pay_for_ai_from_the_wallet_by_default(db):
    """Decision 2026-10-08: a trial opens every course, but its AI actions are paid
    from the wallet until the first payment."""
    assert settings.PRO_AI_INCLUDE_TRIAL is False
    user = _user(db)
    _subscribe(db, user, status="trialing", ends_in=timedelta(days=7))
    result = deduct_credits(user.id, "mentor_chat", db)
    assert "source" not in result and _wallet(db, user).credit_balance == 98
    assert course_access(db, user.id, Course(id=-1, slug="any-course")).reason == "pro"


@pytest.mark.parametrize("status, ends_in, include_trial, gets_allowance", [
    ("active", timedelta(days=3), False, True),
    ("trialing", timedelta(days=3), True, True),            # only if the setting is switched on
    ("trialing", timedelta(days=3), False, False),
    ("cancelled", timedelta(days=3), True, True),           # until the paid period ends
    ("cancelled", timedelta(days=-1), True, False),
    ("active", timedelta(seconds=-1), True, False),         # period over
    ("expired", timedelta(days=3), True, False),
])
def test_who_gets_the_allowance(db, monkeypatch, status, ends_in, include_trial, gets_allowance):
    monkeypatch.setattr(settings, "PRO_AI_INCLUDE_TRIAL", include_trial)
    user = _user(db)
    _subscribe(db, user, status=status, ends_in=ends_in)
    result = deduct_credits(user.id, "mentor_chat", db)
    assert (result.get("source") == "pro_allowance") is gets_allowance
    assert _wallet(db, user).credit_balance == (100 if gets_allowance else 98)


@pytest.mark.parametrize("period", ["monthly", "yearly"])
def test_monthly_and_yearly_pro_get_the_same_50_credit_rolling_allowance(db, period):
    """The billing period changes the price and the length of the paid period, never the
    allowance: 50 credits per rolling 4 hours either way."""
    user = _user(db)
    sub = _subscribe(db, user, period=period, ends_in=timedelta(days=365 if period == "yearly" else 30))
    assert pro_ai.eligible_subscription(db, user.id).billing_period == period

    _use(db, user, sub, 46, T0)
    status = pro_ai.allowance_status(db, user.id, now=T0 + timedelta(minutes=1))
    assert (status.limit, status.window_seconds, status.used, status.remaining) == (50, 14400, 46, 4)
    with pytest.raises(pro_ai.AllowanceExceeded) as refused:
        _use(db, user, sub, 5, T0 + timedelta(minutes=2), action="code_review")
    assert refused.value.available_at == T0 + WINDOW
    assert pro_ai.allowance_status(db, user.id, now=T0 + WINDOW + timedelta(seconds=1)).remaining == 50


def test_resubscribing_does_not_refill_the_window(db):
    user = _user(db)
    first = _subscribe(db, user)
    pro_ai.reserve(db, user.id, first, "mentor_chat", 50)
    first.status = "expired"
    first.current_period_end = datetime.now(timezone.utc) - timedelta(seconds=1)
    db.commit()
    _subscribe(db, user)                                    # paid again minutes later
    with pytest.raises(HTTPException) as refused:
        deduct_credits(user.id, "mentor_chat", db)
    assert refused.value.status_code == 429


def test_course_access_does_not_depend_on_the_allowance(db, pro):
    user, sub = pro
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 50)
    access = course_access(db, user.id, Course(id=-1, slug="any-course"))
    assert access.has_access and access.reason == "pro"


# ── Request settlement ─────────────────────────────────────────────────────────

def _app(user_id, outcome):
    app = FastAPI()

    @app.post("/ai")
    def ai():
        session = SessionLocal()
        try:
            deduct_credits(user_id, "mentor_chat", session)
            if outcome == "crash":
                raise RuntimeError("provider exploded")
            if outcome == "refund":
                refund_credits(user_id, "mentor_chat", session, reason="provider failed")
                raise HTTPException(status_code=502, detail="provider failed")
            return {"ok": True}
        finally:
            session.close()

    return pro_ai.AllowanceRequestMiddleware(app)


@pytest.mark.parametrize("outcome, final_status, reason", [
    ("ok", "consumed", None), ("refund", "released", "provider failed"), ("crash", "released", "request failed"),
])
def test_the_request_outcome_settles_the_reservation(db, pro, outcome, final_status, reason):
    user, _ = pro
    with TestClient(_app(user.id, outcome), raise_server_exceptions=False) as client:
        client.post("/ai")
    [usage] = _usages(db, user)
    assert usage.status == final_status and usage.release_reason == reason
    assert pro_ai.allowance_status(db, user.id).used == (2 if final_status == "consumed" else 0)


def test_an_idempotency_key_header_blocks_a_replay(db, pro):
    user, _ = pro
    with TestClient(_app(user.id, "ok")) as client:
        first = client.post("/ai", headers={"Idempotency-Key": "abc"})
        replay = client.post("/ai", headers={"Idempotency-Key": "abc"})
    assert first.status_code == 200 and replay.status_code == 409
    assert pro_ai.allowance_status(db, user.id).used == 2


# ── The status endpoint ─────────────────────────────────────────────────────────

def _token(client, user):
    from app.core.security import create_access_token
    return {"Authorization": f"Bearer {create_access_token(data={'sub': str(user.id), 'tv': user.token_version or 0})}"}


def test_the_allowance_endpoint_reports_server_side_state(client, db, pro):
    user, sub = pro
    pro_ai.reserve(db, user.id, sub, "mentor_chat", 15)
    body = client.get("/api/v1/billing/ai-allowance", headers=_token(client, user)).json()
    assert body == {"plan": "pro", "all_courses_access": True, "ai_billing": "allowance", "trial": False,
                    "ai_allowance": {"limit": 50, "window_seconds": 14400, "used": 15, "remaining": 35,
                                     "next_credit_available_at": None}}

    pro_ai.reserve(db, user.id, sub, "mentor_chat", 35)
    body = client.get("/api/v1/billing/ai-allowance", headers=_token(client, user)).json()
    assert body["ai_allowance"]["remaining"] == 0 and body["ai_allowance"]["next_credit_available_at"]


def test_the_allowance_endpoint_on_free(client, db):
    user = _user(db)
    body = client.get("/api/v1/billing/ai-allowance", headers=_token(client, user)).json()
    assert body == {"plan": "free", "ai_allowance": None, "all_courses_access": False,
                    "ai_billing": "wallet", "trial": False}
    assert client.get("/api/v1/billing/ai-allowance").status_code == 401


def test_the_allowance_endpoint_during_a_trial(client, db):
    user = _user(db)
    _subscribe(db, user, status="trialing", ends_in=timedelta(days=7))
    body = client.get("/api/v1/billing/ai-allowance", headers=_token(client, user)).json()
    assert body == {"plan": "pro", "ai_allowance": None, "all_courses_access": True,
                    "ai_billing": "wallet", "trial": True}


def test_mentor_v2_validation_limit_counts_pro_releases(db, pro):
    """The limit on validation-failed mentor replies used to read only the wallet ledger,
    which a Pro send never touches - so for Pro it never applied."""
    from app.services.mentor.v2.message import VALIDATION_REFUND, validation_failures_since

    user, sub = pro
    for _ in range(2):
        usage = pro_ai.reserve(db, user.id, sub, "mentor_message", 2)
        pro_ai.release(db, usage.id, reason=VALIDATION_REFUND)
    usage = pro_ai.reserve(db, user.id, sub, "mentor_message", 2)
    pro_ai.release(db, usage.id, reason="Refund: mentor message failed")      # a provider error: not capped
    assert len(validation_failures_since(db, user.id, datetime.now(timezone.utc) - timedelta(hours=1))) == 2
