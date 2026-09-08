"""
Roadmap parsing, and the credit consequences of a bad parse.

The bug these pin down: the roadmap prompt asks for a top-level JSON
*array*, but the shared parse_json_response only ever returns a dict — an
array fell through its type check and its brace scanner then returned the
first week OBJECT from inside the array. That dict failed the list guard in
generate_roadmap, so every roadmap became `[]`, and the endpoint answered
200 while keeping the student's 5 credits.

So there are two things to hold down: the array parses into a real list of
weeks, and anything that still fails to produce one gives the credits back
instead of returning an empty success.

Every LLM response here is a fixture string. No provider is contacted.
"""
import uuid

import pytest

from app.controllers import mentor_controller
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services import roadmap_service
from app.services.roadmap.roadmap_service import _extract_weeks, generate_roadmap
from app.services.wallet.wallet_service import CREDIT_COSTS

ROADMAP = "/api/v1/mentor/roadmap"
STRONG_PASSWORD = "correct-horse-battery-staple-7"
ROADMAP_COST = CREDIT_COSTS["roadmap"]

# Exactly the shape SYSTEM_PROMPT asks for: a bare four-week array.
VALID_ARRAY = """[
  {"week": 1, "theme": "SQL foundations", "topics": ["SELECT", "JOIN"],
   "project": "Query a sales database", "goal": "Read any schema"},
  {"week": 2, "theme": "Python for data", "topics": ["pandas"],
   "project": "Clean a CSV", "goal": "Reshape a dataframe"},
  {"week": 3, "theme": "Visualisation", "topics": ["matplotlib"],
   "project": "Build a dashboard", "goal": "Explain a trend"},
  {"week": 4, "theme": "Statistics", "topics": ["distributions"],
   "project": "A/B test writeup", "goal": "Judge significance"}
]"""


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client):
    email = f"rmp-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Roadmap Parser", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
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


class _FakeLLM:
    def __init__(self, raw): self.raw = raw
    def chat(self, **kwargs): return self.raw


@pytest.fixture()
def responds(monkeypatch):
    """Make the endpoint's provider return a canned string."""
    def _install(raw: str):
        monkeypatch.setattr(mentor_controller, "get_llm", lambda: _FakeLLM(raw))
    return _install


# ─────────────────────────────────────────────────────────────────────────
# 1. Parsing — the array survives
# ─────────────────────────────────────────────────────────────────────────

def test_top_level_array_parses_to_a_non_empty_list():
    weeks = _extract_weeks(VALID_ARRAY)
    assert isinstance(weeks, list)
    assert weeks, "a valid roadmap array must not parse to an empty list"


def test_all_weeks_are_preserved_not_just_the_first():
    """The exact regression: the old path returned the first week object."""
    weeks = _extract_weeks(VALID_ARRAY)
    assert len(weeks) == 4
    assert [w["week"] for w in weeks] == [1, 2, 3, 4]
    assert weeks[0]["theme"] == "SQL foundations"
    assert weeks[3]["theme"] == "Statistics"


def test_generate_roadmap_returns_the_full_list():
    weeks = generate_roadmap(
        llm=_FakeLLM(VALID_ARRAY), track="Data Analyst", experience_level="beginner",
    )
    assert len(weeks) == 4
    assert weeks[1]["topics"] == ["pandas"]


@pytest.mark.parametrize("raw", [
    "```json\n" + VALID_ARRAY + "\n```",
    "Here is your plan:\n" + VALID_ARRAY + "\nGood luck!",
    '{"weeks": ' + VALID_ARRAY + "}",
])
def test_common_model_deviations_still_parse(raw):
    """Fences, prose either side, and an object wrapper — none of these
    should cost a student credits."""
    assert len(_extract_weeks(raw)) == 4


@pytest.mark.parametrize("raw", [
    "",
    "I cannot help with that.",
    "[]",
    "{}",
    "[1, 2, 3]",
    '[{"week": 1}]',                                  # no theme, no topics
    '[{"theme": "x", "topics": "not a list"}]',       # topics must be a list
    '[{"theme": "   ", "topics": []}]',               # blank theme
    "[{broken json",
])
def test_unusable_responses_yield_an_empty_list(raw):
    assert _extract_weeks(raw) == []


def test_partially_valid_array_keeps_only_usable_weeks():
    raw = '[{"week": 1, "theme": "Good", "topics": []}, {"week": 2}, "junk"]'
    weeks = _extract_weeks(raw)
    assert len(weeks) == 1
    assert weeks[0]["theme"] == "Good"


# ─────────────────────────────────────────────────────────────────────────
# 2. Endpoint — success keeps the charge
# ─────────────────────────────────────────────────────────────────────────

def test_valid_roadmap_returns_weeks_and_keeps_the_charge(client, db, responds):
    responds(VALID_ARRAY)
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = client.get(ROADMAP, headers=_auth(token), params={"track": "Data Analyst"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["weeks"]) == 4
    assert body["track"] == "Data Analyst"

    assert _wallet(db, user_id).credit_balance == before - ROADMAP_COST
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1
    assert _txs(db, user_id, TransactionType.refund) == []


# ─────────────────────────────────────────────────────────────────────────
# 3. Endpoint — unusable output refunds and never 200s
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("raw,label", [
    ("[]", "empty array"),
    ("I'm not able to produce that.", "prose, no JSON"),
    ("[{broken json", "malformed"),
    ('[{"week": 1}]', "weeks missing required fields"),
])
def test_unusable_generation_refunds_and_errors(client, db, responds, raw, label):
    responds(raw)
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = client.get(ROADMAP, headers=_auth(token))
    assert resp.status_code == 503, f"{label}: expected 503, got {resp.status_code}"

    # Net zero — charged, then given back.
    assert _wallet(db, user_id).credit_balance == before, label
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1, label
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(refunds) == 1 and refunds[0].credits == ROADMAP_COST, label


def test_endpoint_never_returns_200_with_an_empty_roadmap(client, db, responds):
    """The precise shape of the reported bug: HTTP 200, weeks: [], 5 credits gone."""
    responds("[]")
    token, _uid = _register(client)
    resp = client.get(ROADMAP, headers=_auth(token))
    assert resp.status_code != 200
    assert resp.json().get("weeks") is None


def test_error_body_does_not_leak_provider_detail(client, db, responds):
    responds("upstream said: RateLimitError org-abc123 quota exceeded")
    token, _uid = _register(client)
    detail = client.get(ROADMAP, headers=_auth(token)).json()["detail"]
    assert "refunded" in detail.lower()
    for leak in ("RateLimitError", "org-abc123", "upstream", "quota"):
        assert leak not in detail


def test_unusable_generation_does_not_inflate_lifetime_purchased(client, db, responds):
    responds("[]")
    token, user_id = _register(client)
    purchased_before = _wallet(db, user_id).lifetime_purchased or 0
    spent_before = _wallet(db, user_id).lifetime_spent or 0

    client.get(ROADMAP, headers=_auth(token))

    wallet = _wallet(db, user_id)
    assert wallet.lifetime_purchased == purchased_before
    assert wallet.lifetime_spent == spent_before


def test_provider_exception_still_refunds(client, db, monkeypatch):
    """The pre-existing failure path must keep working alongside the new one."""
    monkeypatch.setattr(mentor_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(roadmap_service, "generate_roadmap", _boom)

    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    assert client.get(ROADMAP, headers=_auth(token)).status_code == 503
    assert _wallet(db, user_id).credit_balance == before
    assert len(_txs(db, user_id, TransactionType.refund)) == 1


# ─────────────────────────────────────────────────────────────────────────
# 4. Unchanged behaviour
# ─────────────────────────────────────────────────────────────────────────

def test_insufficient_credits_still_402_with_no_refund(client, db, responds):
    responds(VALID_ARRAY)
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = ROADMAP_COST - 1
    db.commit()

    resp = client.get(ROADMAP, headers=_auth(token))
    assert resp.status_code == 402
    assert resp.json()["detail"]["error"] == "insufficient_credits"
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _txs(db, user_id, TransactionType.deduction) == []


def test_rate_limit_still_429_with_no_wallet_movement(client, db, responds):
    responds(VALID_ARRAY)
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 1000
    db.commit()

    statuses = [client.get(ROADMAP, headers=_auth(token)).status_code for _ in range(8)]
    assert statuses[:6] == [200] * 6
    assert 429 in statuses[6:], statuses

    # Only the six that got through were charged; none were refunded.
    assert len(_txs(db, user_id, TransactionType.deduction)) == 6
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _wallet(db, user_id).credit_balance == 1000 - (6 * ROADMAP_COST)
