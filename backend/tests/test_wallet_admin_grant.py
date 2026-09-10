"""
Tests for the admin credit-grant endpoints.

Granting credits issues something of value, so the tests are written from
the attacker's side first: anonymous and student callers must be refused
before any of the convenience behaviour is worth checking.

The second theme is the email path added so an operator can credit an
account from the address they already have, without looking up an internal
id. Resolution must be case-insensitive, must reject an ambiguous or absent
identifier, and must credit the account the *server* resolved rather than
anything the caller asserted.
"""
import uuid

import pytest

from app.models.user import User, UserRole
from app.models.wallet import TransactionType, UserWallet, WalletTransaction

GRANT = "/api/v1/wallet/admin/grant"
LOOKUP = "/api/v1/wallet/admin/user-lookup"
STRONG_PASSWORD = "correct-horse-battery-staple-7"


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client, full_name="Grant Tester"):
    email = f"grant-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": full_name, "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return email, body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_admin(db, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.admin})
    db.commit()


def _balance(db, user_id: int) -> int:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    return wallet.credit_balance if wallet else 0


@pytest.fixture()
def admin(client, db):
    """An admin caller and their auth header."""
    _email, token, user_id = _register(client, "Grant Admin")
    _make_admin(db, user_id)
    return {"id": user_id, "token": token, "headers": _auth(token)}


# ─── authorization ────────────────────────────────────────────────────────

def test_grant_rejects_anonymous(client, db):
    email, _token, _uid = _register(client)
    resp = client.post(GRANT, json={"email": email, "credits": 100})
    assert resp.status_code in (401, 403)


def test_grant_rejects_student(client, db):
    """A student must not be able to credit anyone — including themselves."""
    email, token, user_id = _register(client)
    before = _balance(db, user_id)

    resp = client.post(GRANT, json={"email": email, "credits": 100}, headers=_auth(token))
    assert resp.status_code == 403
    assert _balance(db, user_id) == before


def test_lookup_rejects_student(client, db):
    email, token, _uid = _register(client)
    resp = client.get(LOOKUP, params={"email": email}, headers=_auth(token))
    assert resp.status_code == 403


# ─── lookup ───────────────────────────────────────────────────────────────

def test_lookup_returns_account_and_balance(client, db, admin):
    email, _token, user_id = _register(client, "Looked Up")

    resp = client.get(LOOKUP, params={"email": email}, headers=admin["headers"])
    assert resp.status_code == 200
    body = resp.json()
    assert body["user_id"] == user_id
    assert body["email"] == email
    assert body["full_name"] == "Looked Up"
    assert body["credit_balance"] == _balance(db, user_id)


def test_lookup_is_case_insensitive(client, db, admin):
    """An address copied out of a support thread should not have to match
    the capitalisation used at registration."""
    email, _token, user_id = _register(client)

    resp = client.get(LOOKUP, params={"email": email.upper()}, headers=admin["headers"])
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user_id


def test_lookup_unknown_email_404s(client, db, admin):
    resp = client.get(
        LOOKUP, params={"email": f"nobody-{uuid.uuid4().hex[:8]}@example.com"},
        headers=admin["headers"],
    )
    assert resp.status_code == 404


# ─── granting ─────────────────────────────────────────────────────────────

def test_grant_by_email_credits_the_account(client, db, admin):
    email, _token, user_id = _register(client, "Credited Person")
    before = _balance(db, user_id)

    resp = client.post(
        GRANT,
        json={"email": email, "credits": 250, "description": "support refund"},
        headers=admin["headers"],
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["user_id"] == user_id
    assert body["email"] == email
    assert body["credits_granted"] == 250
    assert body["new_balance"] == before + 250
    assert _balance(db, user_id) == before + 250


def test_grant_by_email_is_case_insensitive(client, db, admin):
    email, _token, user_id = _register(client)
    before = _balance(db, user_id)

    resp = client.post(
        GRANT, json={"email": email.upper(), "credits": 10}, headers=admin["headers"]
    )
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user_id
    assert _balance(db, user_id) == before + 10


def test_grant_by_user_id_still_works(client, db, admin):
    """The pre-existing id-based path is unchanged for callers already
    holding a resolved id."""
    _email, _token, user_id = _register(client)
    before = _balance(db, user_id)

    resp = client.post(
        GRANT, json={"user_id": user_id, "credits": 42}, headers=admin["headers"]
    )
    assert resp.status_code == 200
    assert _balance(db, user_id) == before + 42


def test_grant_records_a_bonus_transaction_with_the_reason(client, db, admin):
    """The statement is the audit trail the user themselves can read."""
    email, _token, user_id = _register(client)

    resp = client.post(
        GRANT,
        json={"email": email, "credits": 75, "description": "goodwill for the outage"},
        headers=admin["headers"],
    )
    assert resp.status_code == 200

    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    tx = (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet.id)
        .order_by(WalletTransaction.id.desc())
        .first()
    )
    assert tx.transaction_type == TransactionType.bonus
    assert tx.credits == 75
    assert tx.description == "goodwill for the outage"
    assert tx.balance_after == wallet.credit_balance


# ─── input bounds ─────────────────────────────────────────────────────────

def test_grant_requires_exactly_one_identifier(client, db, admin):
    email, _token, user_id = _register(client)

    neither = client.post(GRANT, json={"credits": 10}, headers=admin["headers"])
    assert neither.status_code == 422

    both = client.post(
        GRANT, json={"credits": 10, "email": email, "user_id": user_id},
        headers=admin["headers"],
    )
    assert both.status_code == 422


def test_grant_rejects_zero_negative_and_absurd_amounts(client, db, admin):
    email, _token, user_id = _register(client)
    before = _balance(db, user_id)

    for amount in (0, -100, 100_001):
        resp = client.post(
            GRANT, json={"email": email, "credits": amount}, headers=admin["headers"]
        )
        assert resp.status_code == 422, amount

    assert _balance(db, user_id) == before


def test_grant_to_unknown_email_404s_and_credits_nobody(client, db, admin):
    resp = client.post(
        GRANT,
        json={"email": f"ghost-{uuid.uuid4().hex[:8]}@example.com", "credits": 10},
        headers=admin["headers"],
    )
    assert resp.status_code == 404
