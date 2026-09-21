"""
The other three AI mentor tools — code review, skill gap, mock interview.

They share POST /mentor/chat's failure mode, and had the same defect: the
credits are charged before the provider is called, and nothing handled the
provider failing, so a timeout, a bad key or an empty answer was a 500 that
kept the student's credits. /mentor/roadmap already refunds; these now do
too, and answer with the same fixed sentence and nothing internal.

The provider is always a stub. See test_mentor_chat.py for the chat endpoint;
the shared helpers live in mentor_fixtures.py.
"""
import json

import pytest

from app.controllers import mentor_controller
from app.core.config import settings
from app.models.wallet import TransactionType
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.mentor_fixtures import (
    UNAVAILABLE_MARKER, FakeLLM, _auth, _balance, _register, _txs,
)

REVIEW = {
    "overall_quality": "good", "score": 82,
    "issues": [{"type": "style", "severity": "low", "line": 3, "message": "Name it", "suggestion": "Rename"}],
    "strengths": ["Readable"], "improvements": ["Add tests"], "summary": "Solid.",
}
GAP = {
    "target_role": "AI Engineer", "current_skills": ["python"],
    "missing_skills": [{"skill": "RAG", "priority": "high", "reason": "Core to the role"}],
    "recommended_roadmap": ["Step 1: build a RAG app"], "readiness_score": 55, "summary": "Getting there.",
}
QUESTION = {
    "question": "Explain overfitting.", "question_type": "theoretical",
    "hints": ["Think bias vs variance"], "follow_up": None,
}

# action charged -> (path, HTTP method, request body, a good provider answer,
#                    a key of the response that must carry that answer through)
TOOLS = {
    "code_review": ("/api/v1/mentor/code-review", "post", {"code": "print(1)"}, REVIEW, "summary"),
    "skill_gap": ("/api/v1/mentor/skill-gap", "post", {"target_role": "AI Engineer"}, GAP, "summary"),
    "mock_interview": ("/api/v1/mentor/mock-interview", "post", {"topic": "Machine Learning"}, QUESTION, "question"),
}
ACTIONS = list(TOOLS)


def _call(client, token, action):
    path, method, body, _, _ = TOOLS[action]
    return getattr(client, method)(path, headers=_auth(token), json=body)


def _use(monkeypatch, llm):
    monkeypatch.setattr(mentor_controller, "get_llm", lambda: llm)
    return llm


def _failed_cleanly(resp, db, user_id, before, action):
    cost = CREDIT_COSTS[action]
    assert resp.status_code == 503, resp.text
    assert UNAVAILABLE_MARKER in resp.json()["detail"].lower()
    assert _balance(db, user_id) == before, "a failed call kept the student's credits"
    deductions = _txs(db, user_id, TransactionType.deduction)
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(deductions) == 1 and deductions[0].credits == -cost and deductions[0].action_type == action
    assert len(refunds) == 1 and refunds[0].credits == cost and refunds[0].action_type == action


@pytest.mark.parametrize("action", ACTIONS)
def test_success_charges_once_and_returns_the_result(api, db, monkeypatch, action):
    _, _, _, good, key = TOOLS[action]
    _use(monkeypatch, FakeLLM(json.dumps(good)))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    resp = _call(api, token, action)
    assert resp.status_code == 200, resp.text
    assert resp.json()[key] == good[key]
    assert _balance(db, user_id) == before - CREDIT_COSTS[action]
    assert _txs(db, user_id, TransactionType.refund) == []


@pytest.mark.parametrize("action", ACTIONS)
def test_provider_error_refunds_and_returns_503(api, db, monkeypatch, action):
    _use(monkeypatch, FakeLLM(RuntimeError("provider down")))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _failed_cleanly(_call(api, token, action), db, user_id, before, action)


@pytest.mark.parametrize("action", ACTIONS)
def test_provider_error_text_never_reaches_the_client(api, monkeypatch, action):
    secret = "sk-LEAK-ME-0123456789"
    _use(monkeypatch, FakeLLM(RuntimeError(f"401 Incorrect API key provided: {secret} at api.openai.com")))
    token, _ = _register(api)

    resp = _call(api, token, action)
    assert resp.status_code == 503
    for fragment in (secret, "Incorrect API key", "api.openai.com", "RuntimeError", "Traceback"):
        assert fragment not in resp.text


@pytest.mark.parametrize("bad", [None, "", "  \n "])
@pytest.mark.parametrize("action", ACTIONS)
def test_empty_provider_answer_is_a_failure_not_a_paid_blank(api, db, monkeypatch, action, bad):
    """Used to be a 200 with an empty review, a 0% readiness score or a blank
    interview question."""
    _use(monkeypatch, FakeLLM(bad))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _failed_cleanly(_call(api, token, action), db, user_id, before, action)


@pytest.mark.parametrize("action, wrong", [
    # Well-formed JSON, wrong types: response validation used to turn these
    # into a 500 after the charge.
    ("code_review", {**REVIEW, "score": "excellent"}),
    ("skill_gap", {**GAP, "readiness_score": "high"}),
    ("skill_gap", {**GAP, "missing_skills": "none"}),
    ("mock_interview", {**QUESTION, "hints": "just think"}),
])
def test_wrongly_typed_provider_json_is_a_refunded_failure(api, db, monkeypatch, action, wrong):
    _use(monkeypatch, FakeLLM(json.dumps(wrong)))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _failed_cleanly(_call(api, token, action), db, user_id, before, action)


@pytest.mark.parametrize("action", ACTIONS)
def test_missing_provider_key_is_a_clean_refunded_503(api, db, monkeypatch, action):
    monkeypatch.setattr(settings, "GENERATION_BACKEND", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    token, user_id = _register(api)
    before = _balance(db, user_id)

    resp = _call(api, token, action)
    _failed_cleanly(resp, db, user_id, before, action)
    assert "API_KEY" not in resp.text


def test_a_failed_skill_gap_does_not_touch_the_readiness_score(api, db, monkeypatch):
    from app.models.user import User

    _use(monkeypatch, FakeLLM(json.dumps({**GAP, "readiness_score": "high"})))
    token, user_id = _register(api)
    db.expire_all()
    before = db.query(User).filter(User.id == user_id).one().overall_readiness_score

    assert _call(api, token, "skill_gap").status_code == 503
    db.expire_all()
    assert db.query(User).filter(User.id == user_id).one().overall_readiness_score == before


def test_a_good_skill_gap_updates_the_readiness_score(api, db, monkeypatch):
    from app.models.user import User

    _use(monkeypatch, FakeLLM(json.dumps(GAP)))
    token, user_id = _register(api)

    assert _call(api, token, "skill_gap").status_code == 200
    db.expire_all()
    assert db.query(User).filter(User.id == user_id).one().overall_readiness_score == 55.0


def test_unparseable_prose_still_degrades_gracefully_for_code_review(api, monkeypatch):
    """Existing, deliberate behaviour: prose instead of JSON is not a failure,
    it is shown as the summary. Pinned so the new checks do not remove it."""
    _use(monkeypatch, FakeLLM("This looks fine, but add type hints."))
    token, _ = _register(api)

    resp = _call(api, token, "code_review")
    assert resp.status_code == 200, resp.text
    assert "add type hints" in resp.json()["summary"]
