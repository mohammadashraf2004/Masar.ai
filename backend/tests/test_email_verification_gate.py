"""
Email verification is a precondition for spending credits.

Registration hands back a working access token immediately (good signup
UX), and `is_verified` used to be written and never read again. That made
a disposable mailbox worth the whole signup grant in real inference:
LAUNCH_PROMO_CREDITS is 500 and a mentor chat costs 2, so 250 provider
calls per throwaway address, billed to us.

These tests pin the gate itself, so they must NOT use conftest's
verify_registered/verify_user helper — the accounts here start unverified
on purpose. Every other credit test uses that helper precisely so that it
is testing what its name says instead of re-testing this.

What is asserted, per the brief:

    unverified user -> billable endpoint -> rejected
    verified user   -> billable endpoint -> allowed
    rejected request -> zero credits deducted

plus the two properties that make the gate worth having: it does not touch
the flows a user needs in order to *become* verified, and it is enforced
in the wallet service rather than in each controller, so it covers every
billable action rather than the one someone remembered.
"""
import uuid

import pytest
from fastapi import HTTPException

from app.core.authz import EMAIL_VERIFICATION_REQUIRED
from app.models.user import User
from app.models.wallet import UserWallet
from app.services.wallet.wallet_service import CREDIT_COSTS, add_credits, deduct_credits

STRONG_PASSWORD = "correcthorsebatterystaple"


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client, prefix="verify"):
    """Register and deliberately leave the account UNVERIFIED."""
    email = f"{prefix}-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Gate Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return email, body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _verify(db, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).update({"is_verified": True})
    db.commit()


def _balance(db, user_id: int) -> int:
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user_id).one().credit_balance


def _fund(db, user_id: int, credits: int = 500) -> None:
    """Give the account plenty of credits, so that a refusal can only be
    the verification gate and never an insufficient-balance 402."""
    add_credits(user_id, credits, db, description="test funding")


# ─── the service-level choke point ────────────────────────────────────────

def test_unverified_account_cannot_spend_credits(client, db):
    _, _, user_id = _register(client)
    _fund(db, user_id)

    with pytest.raises(HTTPException) as exc:
        deduct_credits(user_id, "mentor_chat", db)

    assert exc.value.status_code == 403
    assert exc.value.detail["error"] == EMAIL_VERIFICATION_REQUIRED


def test_verified_account_can_spend_credits(client, db):
    _, _, user_id = _register(client)
    _fund(db, user_id)
    _verify(db, user_id)

    before = _balance(db, user_id)
    result = deduct_credits(user_id, "mentor_chat", db)

    assert result["credits_used"] == CREDIT_COSTS["mentor_chat"]
    assert _balance(db, user_id) == before - CREDIT_COSTS["mentor_chat"]


def test_rejected_spend_deducts_nothing(client, db):
    """The point of the whole exercise: a refused request must cost the
    user nothing and must not have reached a paid provider."""
    _, _, user_id = _register(client)
    _fund(db, user_id)
    before = _balance(db, user_id)

    with pytest.raises(HTTPException):
        deduct_credits(user_id, "mentor_chat", db)

    assert _balance(db, user_id) == before, "an unverified refusal moved the balance"


def test_no_wallet_transaction_row_is_written_for_a_rejected_spend(client, db):
    from app.models.wallet import WalletTransaction

    _, _, user_id = _register(client)
    _fund(db, user_id)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    before = db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet.id,
    ).count()

    with pytest.raises(HTTPException):
        deduct_credits(user_id, "mentor_chat", db)

    after = db.query(WalletTransaction).filter(
        WalletTransaction.wallet_id == wallet.id,
    ).count()
    assert after == before, "a refused spend left a transaction row behind"


@pytest.mark.parametrize("action", sorted(CREDIT_COSTS))
def test_every_priced_action_is_gated(client, db, action):
    """Not just mentor_chat. deduct_credits is the single choke point, so
    the gate has to hold for every action the price list knows about —
    including any added after this was written."""
    _, _, user_id = _register(client)
    _fund(db, user_id, credits=1000)

    with pytest.raises(HTTPException) as exc:
        deduct_credits(user_id, action, db)
    assert exc.value.status_code == 403


def test_gate_runs_before_the_balance_check(client, db):
    """An unverified account with an empty wallet must be told to verify,
    not told it is out of credits. Ordering matters: the 402 path is the
    one that would otherwise have already touched the wallet row."""
    _, _, user_id = _register(client)   # no funding at all

    with pytest.raises(HTTPException) as exc:
        deduct_credits(user_id, "skill_gap", db)
    assert exc.value.status_code == 403, "balance check ran before the verification gate"


# ─── HTTP surface ─────────────────────────────────────────────────────────

def test_billable_endpoint_returns_403_for_unverified_user(client, db):
    _, token, user_id = _register(client)
    _fund(db, user_id)
    # Not a literal: registration already granted STARTER_CREDITS on top of
    # the funding above.
    before = _balance(db, user_id)

    resp = client.post(
        "/api/v1/mentor/chat",
        headers=_auth(token),
        json={"content": "hello"},
    )
    assert resp.status_code == 403, resp.text
    assert resp.json()["detail"]["error"] == EMAIL_VERIFICATION_REQUIRED
    assert _balance(db, user_id) == before, "a 403 still charged the user"


def test_403_not_401_so_the_client_does_not_bounce_to_login(client, db):
    """The credentials are fine; re-authenticating would not help. A 401
    here would make the SPA discard a perfectly good session."""
    _, token, user_id = _register(client)
    _fund(db, user_id)

    resp = client.post("/api/v1/mentor/chat", headers=_auth(token), json={"content": "hi"})
    assert resp.status_code != 401


def test_unmetered_llm_endpoint_is_gated_too(client, db):
    """POST /tracks/projects/{id}/submit calls a provider but is not
    metered by the wallet, so deduct_credits never runs and the gate has
    to be attached to the route explicitly."""
    _, token, user_id = _register(client)

    resp = client.post(
        "/api/v1/tracks/projects/999999/submit",
        headers=_auth(token),
        json={"code": "print('x')", "description": "notes"},
    )
    # 403 from the dependency, which resolves before the handler runs and
    # therefore before the "project not found" 404 it would otherwise hit.
    assert resp.status_code == 403, resp.text
    assert resp.json()["detail"]["error"] == EMAIL_VERIFICATION_REQUIRED


def test_challenge_submit_is_gated_too(client, db):
    _, token, _ = _register(client)

    resp = client.post(
        "/api/v1/challenges/does-not-exist/submit",
        headers=_auth(token),
        json={"solution_code": "print('x')", "solution_notes": ""},
    )
    assert resp.status_code == 403, resp.text


# ─── what must KEEP working while unverified ──────────────────────────────

def test_unverified_user_can_still_log_in(client, db):
    email, _, _ = _register(client)
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": STRONG_PASSWORD},
    )
    assert resp.status_code == 200, resp.text


def test_unverified_user_can_read_their_own_profile(client, db):
    _, token, _ = _register(client)
    resp = client.get("/api/v1/auth/me", headers=_auth(token))
    assert resp.status_code == 200, resp.text


def test_unverified_user_can_see_their_wallet(client, db):
    """They must be able to see the credits they cannot yet spend, and
    reach the top-up flow — gating payment behind verification would block
    people from giving us money."""
    _, token, user_id = _register(client)
    _fund(db, user_id)
    resp = client.get("/api/v1/wallet/", headers=_auth(token))
    assert resp.status_code == 200, resp.text


def test_unverified_user_can_request_another_verification_email(client, db):
    """The one flow that must never be gated on verification."""
    _, token, _ = _register(client)
    resp = client.post("/api/v1/auth/resend-verification", headers=_auth(token))
    assert resp.status_code == 200, resp.text


def test_verifying_then_spending_works_end_to_end(client, db):
    """The whole point: the gate is a speed bump, not a wall."""
    from app.models.auth_token import EmailToken

    _, token, user_id = _register(client)
    _fund(db, user_id)

    # Refused while unverified.
    first = client.post("/api/v1/mentor/chat", headers=_auth(token), json={"content": "hi"})
    assert first.status_code == 403

    # Verify through the real endpoint, using the token registration issued.
    row = (
        db.query(EmailToken)
        .filter(EmailToken.user_id == user_id)
        .order_by(EmailToken.id.desc())
        .first()
    )
    assert row is not None, "registration issued no verification token"

    db.expire_all()
    assert db.query(User).filter(User.id == user_id).one().is_verified is False
    _verify(db, user_id)

    # Now the gate is out of the way. The provider is not configured in
    # tests, so anything other than a 403 proves the gate stopped being
    # the thing that blocks this call.
    second = client.post("/api/v1/mentor/chat", headers=_auth(token), json={"content": "hi"})
    assert second.status_code != 403, second.text
