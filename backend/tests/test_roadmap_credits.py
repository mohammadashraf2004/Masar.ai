"""
Roadmap credit accounting.

GET /mentor/roadmap charges 5 credits before it calls the provider, which
is the right order (never generate for free) but leaves a debt: if
generation then fails, the student has paid for nothing. These tests pin
down both halves — the charge sticks when it worked, and is reversed when
it didn't.

The provider is always stubbed. Nothing here makes a real LLM call.
"""
import uuid

import pytest

from app.controllers import mentor_controller
from app.models.wallet import (
    TransactionType, UserWallet, WalletTransaction,
)
from app.services import roadmap_service
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.conftest import verify_registered

ROADMAP = "/api/v1/mentor/roadmap"
STRONG_PASSWORD = "correct-horse-battery-staple-7"
ROADMAP_COST = CREDIT_COSTS["roadmap"]

FAKE_WEEKS = [
    {"week": 1, "theme": "Foundations", "topics": ["python"], "goal": "Get set up"},
]


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client):
    email = f"rm-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Roadmap Tester", "password": STRONG_PASSWORD,
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


@pytest.fixture()
def stub_llm(monkeypatch):
    """A provider that never gets called for real."""
    monkeypatch.setattr(mentor_controller, "get_llm", lambda: object())


@pytest.fixture()
def working_provider(monkeypatch, stub_llm):
    monkeypatch.setattr(roadmap_service, "generate_roadmap", lambda **kw: list(FAKE_WEEKS))


@pytest.fixture()
def broken_provider(monkeypatch, stub_llm):
    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(roadmap_service, "generate_roadmap", _boom)


# ─────────────────────────────────────────────────────────────────────────
# 1. Success — the charge stands
# ─────────────────────────────────────────────────────────────────────────

def test_successful_roadmap_keeps_the_deduction(client, db, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = client.get(ROADMAP, headers=_auth(token), params={"track": "AI Engineer"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["weeks"] == FAKE_WEEKS

    assert _wallet(db, user_id).credit_balance == before - ROADMAP_COST
    deductions = _txs(db, user_id, TransactionType.deduction)
    assert len(deductions) == 1
    assert deductions[0].credits == -ROADMAP_COST
    assert deductions[0].action_type == "roadmap"
    # A successful call must never be refunded.
    assert _txs(db, user_id, TransactionType.refund) == []


def test_lifetime_spent_tracks_a_successful_charge(client, db, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).lifetime_spent or 0
    client.get(ROADMAP, headers=_auth(token))
    assert _wallet(db, user_id).lifetime_spent == before + ROADMAP_COST


# ─────────────────────────────────────────────────────────────────────────
# 2. Provider failure — the charge is reversed
# ─────────────────────────────────────────────────────────────────────────

def test_failed_generation_refunds_the_credits(client, db, broken_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = client.get(ROADMAP, headers=_auth(token))
    assert resp.status_code == 503, resp.text
    assert "refunded" in resp.json()["detail"].lower()

    # Net zero: the deduction and the refund both exist and cancel out.
    assert _wallet(db, user_id).credit_balance == before

    deductions = _txs(db, user_id, TransactionType.deduction)
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(deductions) == 1 and deductions[0].credits == -ROADMAP_COST
    assert len(refunds) == 1
    assert refunds[0].credits == ROADMAP_COST
    assert refunds[0].action_type == "roadmap"
    assert refunds[0].balance_after == before


def test_refund_is_committed_not_just_staged(client, db, broken_provider):
    """The deduction commits before the provider call, so the refund has to
    commit too — a refund left in an uncommitted session is no refund."""
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    client.get(ROADMAP, headers=_auth(token))

    # Read through a brand-new session: only committed state is visible.
    from app.db.session import SessionLocal
    fresh = SessionLocal()
    try:
        balance = fresh.query(UserWallet).filter(
            UserWallet.user_id == user_id
        ).one().credit_balance
    finally:
        fresh.close()
    assert balance == before


def test_refund_does_not_inflate_lifetime_purchased(client, db, broken_provider):
    """A refund is not a purchase. Reversing the spend must not make the
    wallet claim the student bought credits they never bought."""
    token, user_id = _register(client)
    purchased_before = _wallet(db, user_id).lifetime_purchased or 0
    spent_before = _wallet(db, user_id).lifetime_spent or 0

    client.get(ROADMAP, headers=_auth(token))

    wallet = _wallet(db, user_id)
    assert wallet.lifetime_purchased == purchased_before
    # The spend was undone, so it should no longer count as spent.
    assert wallet.lifetime_spent == spent_before


def test_repeated_failures_do_not_drift_the_balance(client, db, broken_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    for _ in range(3):
        assert client.get(ROADMAP, headers=_auth(token)).status_code == 503
    assert _wallet(db, user_id).credit_balance == before
    assert len(_txs(db, user_id, TransactionType.deduction)) == 3
    assert len(_txs(db, user_id, TransactionType.refund)) == 3


# ─────────────────────────────────────────────────────────────────────────
# 3. Insufficient credits — unchanged, and never refunded
# ─────────────────────────────────────────────────────────────────────────

def test_insufficient_credits_still_returns_402(client, db, working_provider):
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = ROADMAP_COST - 1
    db.commit()

    resp = client.get(ROADMAP, headers=_auth(token))
    assert resp.status_code == 402
    detail = resp.json()["detail"]
    assert detail["error"] == "insufficient_credits"
    assert detail["credits_needed"] == ROADMAP_COST


def test_no_refund_when_no_deduction_happened(client, db, broken_provider):
    """The 402 is raised before the generation call, so there is nothing to
    reverse — a refund here would mint credits out of a failed request."""
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 0
    db.commit()

    assert client.get(ROADMAP, headers=_auth(token)).status_code == 402

    assert _wallet(db, user_id).credit_balance == 0
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _txs(db, user_id, TransactionType.deduction) == []


# ─────────────────────────────────────────────────────────────────────────
# 4. Everything else about the endpoint is unchanged
# ─────────────────────────────────────────────────────────────────────────

def test_roadmap_still_requires_authentication(client):
    assert client.get(ROADMAP).status_code == 401


def test_roadmap_rate_limit_still_applies(client, db, working_provider):
    """6/minute, unchanged by the refund work. Credits are topped up so the
    limiter is what stops the run, not an empty wallet."""
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 1000
    db.commit()

    statuses = [client.get(ROADMAP, headers=_auth(token)).status_code for _ in range(8)]
    assert statuses[:6] == [200] * 6
    assert 429 in statuses[6:], statuses


def test_rate_limited_request_is_never_charged(client, db, working_provider):
    """A 429 is refused before the handler runs, so it must not move the
    wallet at all — neither a deduction nor a refund."""
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 1000
    db.commit()

    for _ in range(8):
        client.get(ROADMAP, headers=_auth(token))

    # Six calls got through the limiter; only those six were charged.
    assert len(_txs(db, user_id, TransactionType.deduction)) == 6
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _wallet(db, user_id).credit_balance == 1000 - (6 * ROADMAP_COST)
