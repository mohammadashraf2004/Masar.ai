"""
Shared helpers for the AI mentor tests (test_mentor_chat.py, test_mentor_tools.py).

Not a test module. Import the names you need. (The `api` client fixture these
tests use lives in conftest.py, next to `client`.)
"""
import uuid

from app.models.progress import MentorSession
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from tests.conftest import verify_registered

STRONG_PASSWORD = "correct-horse-battery-staple-7"

# The one sentence a student is allowed to see when a mentor request fails.
UNAVAILABLE_MARKER = "credits were refunded"


class FakeLLM(BaseLLMProvider):
    """A provider whose replies are scripted. An entry that is an exception
    is raised instead of returned. The last entry repeats forever."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls: list[dict] = []

    def validate(self) -> bool:
        return True

    def chat(self, system, messages, max_tokens=None):
        self.calls.append({"system": system, "messages": messages, "max_tokens": max_tokens})
        reply = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        if isinstance(reply, BaseException):
            raise reply
        return reply


def _register(client):
    email = f"mc-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True,
        "email": email, "full_name": "Mentor Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    verify_registered(client, body["user"]["id"])
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _balance(db, user_id: int) -> int:
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user_id).one().credit_balance


def _txs(db, user_id: int, kind: TransactionType):
    return (
        db.query(WalletTransaction)
        .join(UserWallet, WalletTransaction.wallet_id == UserWallet.id)
        .filter(UserWallet.user_id == user_id, WalletTransaction.transaction_type == kind)
        .all()
    )


def _sessions(db, user_id: int):
    db.expire_all()
    return db.query(MentorSession).filter(MentorSession.user_id == user_id).all()
