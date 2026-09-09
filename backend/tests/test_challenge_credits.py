"""
Challenge credit accounting.

Enrolling in a challenge and asking for a challenge hint both spend
credits. Both used to adjust the wallet row inline — no row lock, no
promo-expiry check, no promo-balance decrement — which left
`promo_credits_remaining` overstated after every challenge spend and let
already-expired promo credits keep buying. These tests pin the spends to
the canonical wallet service and to the promo invariants that follow.

The LLM is always stubbed. Nothing here makes a real provider call.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.controllers import challenge_controller
from app.core.config import settings
from app.models.challenge import ChallengeDifficulty, ChallengeProject
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services.wallet.wallet_service import CREDIT_COSTS, add_credits
from tests.conftest import verify_registered

STRONG_PASSWORD = "correct-horse-battery-staple-7"
ENROLL_COST = 25          # what the fixture challenge charges
HINT_COST = CREDIT_COSTS["challenge_hint"]

FAKE_HINT = {
    "hint": "Look at how the dates are formatted.",
    "concept": "Data normalisation",
    "next_step": "Normalise them before parsing.",
}


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client):
    email = f"chal-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Challenge Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    # Billable endpoints refuse unverified accounts; these tests are
    # about credits/refunds/limits, not about the verification gate.
    verify_registered(client, body["user"]["id"])
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _wallet(db, user_id: int) -> UserWallet:
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user_id).one()


def _txs(db, user_id: int, kind: TransactionType):
    return (
        db.query(WalletTransaction)
        .join(UserWallet, WalletTransaction.wallet_id == UserWallet.id)
        .filter(UserWallet.user_id == user_id,
                WalletTransaction.transaction_type == kind)
        .all()
    )


def _promo_open(monkeypatch, credits=500, days=30):
    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "2099-12-31")
    monkeypatch.setattr(settings, "LAUNCH_PROMO_CREDITS", credits)
    monkeypatch.setattr(settings, "LAUNCH_PROMO_DAYS", days)


def _lapse_promo(db, user_id: int):
    """Move the promo window into the past, as the clock would."""
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()


@pytest.fixture()
def challenge(db) -> ChallengeProject:
    ch = ChallengeProject(
        title="Messy Sales Data",
        slug=f"messy-sales-{uuid.uuid4().hex[:8]}",
        description="Clean it.",
        difficulty=ChallengeDifficulty.beginner,
        credit_cost=ENROLL_COST,
        passing_score=70.0,
        max_attempts=3,
        is_active=True,
        dirty_dataset=[{"a": 1}, {"a": 2}, {"a": 3}],
        dataset_description="Duplicated rows.",
        grading_rubric=[{"criterion": "dedup", "weight": 100}],
        hints=[],
        tags=[],
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


@pytest.fixture()
def stub_hint(monkeypatch):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())
    monkeypatch.setattr(
        challenge_controller, "get_challenge_hint", lambda **kw: dict(FAKE_HINT),
    )


def _enroll(client, token, challenge):
    return client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(token))


def _hint(client, token, challenge):
    return client.post(
        f"/api/v1/challenges/{challenge.slug}/hint",
        headers=_auth(token),
        json={"stuck_on": "the dates", "previous_hints": []},
    )


# ─────────────────────────────────────────────────────────────────────────
# 1. The spend goes through the wallet service — promo balance included
# ─────────────────────────────────────────────────────────────────────────

def test_enrolling_draws_down_promo_credits(client, db, monkeypatch, challenge):
    """The bug: enrolling moved credit_balance but left
    promo_credits_remaining untouched, so the wallet claimed the user still
    held promo credits they had already spent."""
    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)

    assert _enroll(client, token, challenge).status_code == 200

    wallet = _wallet(db, user_id)
    assert wallet.credit_balance == 500 - ENROLL_COST
    assert wallet.promo_credits_remaining == 500 - ENROLL_COST, (
        "enrolment spent promo credits without decrementing the promo counter"
    )


def test_hint_draws_down_promo_credits(client, db, monkeypatch, challenge, stub_hint):
    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)
    assert _enroll(client, token, challenge).status_code == 200

    assert _hint(client, token, challenge).status_code == 200

    wallet = _wallet(db, user_id)
    spent = ENROLL_COST + HINT_COST
    assert wallet.credit_balance == 500 - spent
    assert wallet.promo_credits_remaining == 500 - spent


def test_challenge_spends_are_recorded_in_the_ledger(client, db, monkeypatch, challenge, stub_hint):
    """Balance must never move without a matching transaction row, and the
    rows keep the action labels the wallet history renders."""
    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)
    _enroll(client, token, challenge)
    _hint(client, token, challenge)

    deductions = _txs(db, user_id, TransactionType.deduction)
    by_action = {t.action_type: t for t in deductions}
    assert set(by_action) == {"challenge_enroll", "challenge_hint"}
    assert by_action["challenge_enroll"].credits == -ENROLL_COST
    assert by_action["challenge_enroll"].description == f"Enrolled in challenge: {challenge.title}"
    assert by_action["challenge_hint"].credits == -HINT_COST


# ─────────────────────────────────────────────────────────────────────────
# 2. Expired promo credits cannot be spent
# ─────────────────────────────────────────────────────────────────────────

def test_expired_promo_credits_cannot_pay_for_enrolment(client, db, monkeypatch, challenge):
    """Before the fix this route never ran the expiry check, so a lapsed
    500-credit promo balance still bought challenges."""
    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)
    _lapse_promo(db, user_id)

    resp = _enroll(client, token, challenge)
    assert resp.status_code == 402, resp.text
    assert resp.json()["detail"]["error"] == "insufficient_credits"
    assert resp.json()["detail"]["credits_needed"] == ENROLL_COST

    wallet = _wallet(db, user_id)
    assert wallet.credit_balance == 0
    assert wallet.promo_credits_remaining == 0


def test_expired_promo_credits_cannot_pay_for_a_hint(client, db, monkeypatch, challenge, stub_hint):
    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)
    assert _enroll(client, token, challenge).status_code == 200

    _lapse_promo(db, user_id)

    resp = _hint(client, token, challenge)
    assert resp.status_code == 402, resp.text
    assert _wallet(db, user_id).credit_balance == 0


def test_a_refused_enrolment_creates_no_attempt(client, db, monkeypatch, challenge):
    """A 402 must leave no trace — no attempt row consuming one of the
    three tries, and no ledger entry."""
    from app.models.challenge import ChallengeAttempt

    _promo_open(monkeypatch, credits=500)
    token, user_id = _register(client)
    _lapse_promo(db, user_id)

    assert _enroll(client, token, challenge).status_code == 402

    attempts = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == user_id,
    ).all()
    assert attempts == []
    assert _txs(db, user_id, TransactionType.deduction) == []


# ─────────────────────────────────────────────────────────────────────────
# 3. Expiry never takes purchased credits, even after challenge spending
# ─────────────────────────────────────────────────────────────────────────

def test_expiry_after_a_challenge_spend_keeps_purchased_credits(
    client, db, monkeypatch, challenge,
):
    """The consequence of the bug that actually cost users money.

    Promo 100 + purchased 100. Enrolling spends 25, which should be 25
    promo credits. When the promo lapses, only the 75 *unspent* promo
    credits may be withdrawn, leaving the 100 purchased. With the inline
    deduction, promo_credits_remaining stayed at 100, so expiry removed
    100 and ate 25 credits the user had paid for.
    """
    from app.services.wallet.wallet_service import expire_promo_credits_if_due

    _promo_open(monkeypatch, credits=100)
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    assert _wallet(db, user_id).credit_balance == 200

    assert _enroll(client, token, challenge).status_code == 200
    assert _wallet(db, user_id).credit_balance == 200 - ENROLL_COST

    _lapse_promo(db, user_id)
    wallet = _wallet(db, user_id)
    removed = expire_promo_credits_if_due(wallet, db)

    assert removed == 100 - ENROLL_COST, "expiry withdrew more than the unspent promo"
    db.refresh(wallet)
    assert wallet.credit_balance == 100, "expiry ate credits the user paid for"


# ─────────────────────────────────────────────────────────────────────────
# 4. Ordinary (non-promo) credits still work exactly as before
# ─────────────────────────────────────────────────────────────────────────

def test_ordinary_credits_pay_for_enrolment(client, db, challenge):
    """Promo off — the plain starter/purchased balance path."""
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    before = _wallet(db, user_id).credit_balance

    resp = _enroll(client, token, challenge)
    assert resp.status_code == 200, resp.text

    wallet = _wallet(db, user_id)
    assert wallet.credit_balance == before - ENROLL_COST
    assert wallet.promo_credits_remaining == 0
    assert resp.json()["credits_remaining"] == wallet.credit_balance


def test_ordinary_credits_pay_for_a_hint(client, db, challenge, stub_hint):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    _enroll(client, token, challenge)
    before = _wallet(db, user_id).credit_balance

    resp = _hint(client, token, challenge)
    assert resp.status_code == 200, resp.text
    assert resp.json()["hint"] == FAKE_HINT["hint"]
    assert _wallet(db, user_id).credit_balance == before - HINT_COST


def test_lifetime_spent_tracks_challenge_spending(client, db, challenge, stub_hint):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    before = _wallet(db, user_id).lifetime_spent or 0

    _enroll(client, token, challenge)
    _hint(client, token, challenge)

    assert _wallet(db, user_id).lifetime_spent == before + ENROLL_COST + HINT_COST


def test_challenge_spending_does_not_inflate_lifetime_purchased(client, db, challenge):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    purchased_before = _wallet(db, user_id).lifetime_purchased

    _enroll(client, token, challenge)

    assert _wallet(db, user_id).lifetime_purchased == purchased_before


def test_insufficient_ordinary_credits_returns_402(client, db, challenge):
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = ENROLL_COST - 1
    db.commit()

    resp = _enroll(client, token, challenge)
    assert resp.status_code == 402
    detail = resp.json()["detail"]
    assert detail["error"] == "insufficient_credits"
    assert detail["credits_needed"] == ENROLL_COST
    assert detail["credits_available"] == ENROLL_COST - 1


# ─────────────────────────────────────────────────────────────────────────
# 5. Everything else about the two endpoints is unchanged
# ─────────────────────────────────────────────────────────────────────────

def test_enrolment_still_creates_the_attempt_and_unlocks_the_dataset(client, db, challenge):
    from app.models.challenge import ChallengeAttempt, ChallengeStatus

    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")

    body = _enroll(client, token, challenge).json()
    assert body["dataset_unlocked"] is True
    assert body["message"] == f"Enrolled successfully! {ENROLL_COST} credits deducted."

    attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == user_id,
        ChallengeAttempt.challenge_id == challenge.id,
    ).one()
    assert attempt.id == body["attempt_id"]
    assert attempt.status == ChallengeStatus.enrolled
    assert attempt.attempt_number == 1
    assert attempt.credits_spent == ENROLL_COST

    dl = client.get(f"/api/v1/challenges/{challenge.slug}/dataset/download", headers=_auth(token))
    assert dl.status_code == 200


def test_double_enrolment_is_still_refused_and_not_charged(client, db, challenge):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    assert _enroll(client, token, challenge).status_code == 200
    after_first = _wallet(db, user_id).credit_balance

    resp = _enroll(client, token, challenge)
    assert resp.status_code == 400
    assert "Already enrolled" in resp.json()["detail"]
    assert _wallet(db, user_id).credit_balance == after_first


def test_max_attempts_is_still_enforced_before_charging(client, db, challenge):
    from app.models.challenge import ChallengeAttempt, ChallengeStatus

    token, user_id = _register(client)
    add_credits(user_id, 500, db, description="purchased")
    for n in range(challenge.max_attempts):
        db.add(ChallengeAttempt(
            user_id=user_id, challenge_id=challenge.id,
            status=ChallengeStatus.failed, attempt_number=n + 1, credits_spent=0,
        ))
    db.commit()
    before = _wallet(db, user_id).credit_balance

    resp = _enroll(client, token, challenge)
    assert resp.status_code == 400
    assert _wallet(db, user_id).credit_balance == before, "charged for a refused enrolment"


def test_hint_still_requires_enrolment_and_does_not_charge(client, db, challenge, stub_hint):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    before = _wallet(db, user_id).credit_balance

    resp = _hint(client, token, challenge)
    assert resp.status_code == 403
    assert _wallet(db, user_id).credit_balance == before


def test_challenge_endpoints_still_require_authentication(client, challenge):
    assert client.post(f"/api/v1/challenges/{challenge.slug}/enroll").status_code == 401
    assert client.post(
        f"/api/v1/challenges/{challenge.slug}/hint",
        json={"stuck_on": "x", "previous_hints": []},
    ).status_code == 401


def test_unknown_challenge_is_still_404_and_free(client, db):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    before = _wallet(db, user_id).credit_balance

    assert client.post("/api/v1/challenges/no-such-slug/enroll", headers=_auth(token)).status_code == 404
    assert _wallet(db, user_id).credit_balance == before


def test_hint_rate_limit_still_applies(client, db, challenge, stub_hint):
    """20/hour, unchanged. Credits are topped up so the limiter is what
    stops the run, not an empty wallet."""
    token, user_id = _register(client)
    add_credits(user_id, 1000, db, description="purchased")
    _enroll(client, token, challenge)

    statuses = [_hint(client, token, challenge).status_code for _ in range(22)]
    assert statuses[:20] == [200] * 20
    assert 429 in statuses[20:], statuses


def test_rate_limited_hint_is_never_charged(client, db, challenge, stub_hint):
    token, user_id = _register(client)
    add_credits(user_id, 1000, db, description="purchased")
    _enroll(client, token, challenge)
    before = _wallet(db, user_id).credit_balance

    for _ in range(22):
        _hint(client, token, challenge)

    # Twenty got past the limiter; only those twenty were charged.
    assert _wallet(db, user_id).credit_balance == before - (20 * HINT_COST)


def test_challenge_hint_price_is_published(client):
    """The price moved from a literal in the controller into CREDIT_COSTS,
    which is what GET /wallet/costs serves."""
    costs = client.get("/api/v1/wallet/costs").json()["costs"]
    assert costs["challenge_hint"] == 1


# ─────────────────────────────────────────────────────────────────────────
# 6. A hint that never arrives is refunded
# ─────────────────────────────────────────────────────────────────────────
# deduct_credits commits before the provider is called, so every failure
# after that point leaves the student paying for nothing. The enrolment
# path already refunded; the hint path did not, and billed 1 credit for a
# 500. Both provider failures and response-validation failures count: the
# student is equally empty-handed either way.

def test_failed_hint_provider_refunds_the_credit(client, db, monkeypatch, challenge):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(challenge_controller, "get_challenge_hint", _boom)

    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    _enroll(client, token, challenge)
    before = _wallet(db, user_id).credit_balance

    resp = _hint(client, token, challenge)
    assert resp.status_code == 503, resp.text
    assert "refunded" in resp.json()["detail"].lower()

    # Net zero: charged, then given back.
    assert _wallet(db, user_id).credit_balance == before
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(refunds) == 1
    assert refunds[0].credits == HINT_COST
    assert refunds[0].action_type == "challenge_hint"


def test_malformed_hint_response_refunds_the_credit(client, db, monkeypatch, challenge):
    """The concrete failure that surfaced this: HintResponse requires three
    string fields, so a model returning a non-string raises a validation
    error AFTER the deduction — previously a charged 500."""
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())
    monkeypatch.setattr(
        challenge_controller, "get_challenge_hint",
        lambda **kw: {"hint": {"not": "a string"}, "concept": "", "next_step": ""},
    )

    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    _enroll(client, token, challenge)
    before = _wallet(db, user_id).credit_balance

    resp = _hint(client, token, challenge)
    assert resp.status_code == 503, resp.text
    assert _wallet(db, user_id).credit_balance == before
    assert len(_txs(db, user_id, TransactionType.refund)) == 1


def test_failed_hint_does_not_inflate_lifetime_purchased(client, db, monkeypatch, challenge):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(challenge_controller, "get_challenge_hint", _boom)

    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    _enroll(client, token, challenge)
    purchased_before = _wallet(db, user_id).lifetime_purchased or 0
    spent_before = _wallet(db, user_id).lifetime_spent or 0

    _hint(client, token, challenge)

    wallet = _wallet(db, user_id)
    assert wallet.lifetime_purchased == purchased_before
    assert wallet.lifetime_spent == spent_before


def test_successful_hint_is_never_refunded(client, db, challenge, stub_hint):
    token, user_id = _register(client)
    add_credits(user_id, 100, db, description="purchased")
    _enroll(client, token, challenge)
    before = _wallet(db, user_id).credit_balance

    resp = _hint(client, token, challenge)
    assert resp.status_code == 200
    assert _wallet(db, user_id).credit_balance == before - HINT_COST
    assert _txs(db, user_id, TransactionType.refund) == []


def test_hint_error_body_does_not_leak_provider_detail(client, db, monkeypatch, challenge):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("RateLimitError org-abc123 quota exceeded")
    monkeypatch.setattr(challenge_controller, "get_challenge_hint", _boom)

    token, _uid = _register(client)
    add_credits(_uid, 100, db, description="purchased")
    _enroll(client, token, challenge)
    detail = _hint(client, token, challenge).json()["detail"]
    for leak in ("RateLimitError", "org-abc123", "quota"):
        assert leak not in detail


def test_unenrolled_hint_failure_creates_no_refund(client, db, monkeypatch, challenge):
    """The 403 fires before any deduction, so there is nothing to reverse —
    a refund here would mint credits from a refused request."""
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(challenge_controller, "get_challenge_hint", _boom)

    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    assert _hint(client, token, challenge).status_code == 403
    assert _wallet(db, user_id).credit_balance == before
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _txs(db, user_id, TransactionType.deduction) == []
