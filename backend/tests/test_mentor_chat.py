"""
POST /mentor/chat — the AI Mentor's main path.

Two things are pinned here that had no direct coverage before:

1. What a student sees and pays when the provider works, and when it does
   not. The charge is taken *before* the provider is called (never answer
   for free), so every failure path has to give it back, exactly as
   GET /mentor/roadmap already does — see test_roadmap_credits.py.
2. What the endpoint refuses to leak. A provider error is an internal
   detail: the client gets one fixed sentence, never an exception message,
   an env-var name, or a key.

The provider is always a stub. Nothing here makes a real LLM call and no
API key is needed. The real mentor_service, prompt builder and language
policy DO run — only the network call underneath them is replaced.
"""
import uuid

import httpx
import openai
import pytest

from app.controllers import mentor_controller
from app.core.config import settings
from app.models.learning import CareerTrack, Topic, TrackLevel
from app.models.progress import MentorSession
from app.models.wallet import TransactionType
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.mentor_fixtures import (
    UNAVAILABLE_MARKER, FakeLLM, _auth, _balance, _register, _sessions, _txs,
)

CHAT = "/api/v1/mentor/chat"
COST = CREDIT_COSTS["mentor_chat"]

GOOD_REPLY = (
    '{"reply": "RAG retrieves documents first, then generates from them.", '
    '"suggested_actions": ["Try the exercise", "Ask me to quiz you"]}'
)


# ─── helpers ──────────────────────────────────────────────────────────────

def _use(monkeypatch, llm) -> FakeLLM:
    monkeypatch.setattr(mentor_controller, "get_llm", lambda: llm)
    return llm


def _say(client, token, content="What is RAG?", **extra):
    return client.post(CHAT, headers=_auth(token), json={"content": content, **extra})


def _assert_failed_cleanly(resp, db, user_id, before):
    """The contract for every failure: a fixed 503, the credits back, and
    nothing half-saved."""
    assert resp.status_code == 503, resp.text
    assert UNAVAILABLE_MARKER in resp.json()["detail"].lower()
    assert _balance(db, user_id) == before, "a failed mentor call kept the student's credits"
    deductions = _txs(db, user_id, TransactionType.deduction)
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(deductions) == 1 and deductions[0].credits == -COST
    assert len(refunds) == 1 and refunds[0].credits == COST
    assert refunds[0].action_type == "mentor_chat"
    assert _sessions(db, user_id) == [], "a failed call left an orphan session behind"


# ─────────────────────────────────────────────────────────────────────────
# 1. Success
# ─────────────────────────────────────────────────────────────────────────

def test_successful_chat_returns_reply_and_charges_once(api, db, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    resp = _say(api, token)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["reply"].startswith("RAG retrieves")
    assert body["suggested_actions"] == ["Try the exercise", "Ask me to quiz you"]
    assert isinstance(body["session_id"], int)

    assert _balance(db, user_id) == before - COST
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1
    assert _txs(db, user_id, TransactionType.refund) == []
    assert len(llm.calls) == 1


def test_exchange_is_persisted_on_one_session(api, db, monkeypatch):
    _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)

    _say(api, token, "What is RAG?")
    sessions = _sessions(db, user_id)
    assert len(sessions) == 1
    assert [m["role"] for m in sessions[0].messages] == ["user", "assistant"]
    assert sessions[0].messages[0]["content"] == "What is RAG?"
    assert sessions[0].title == "What is RAG?"


def test_plain_text_reply_is_passed_through(api, monkeypatch):
    """Models sometimes ignore the JSON instruction. That is not a failure —
    the student still gets the answer, with the stock follow-ups."""
    _use(monkeypatch, FakeLLM("RAG means retrieval-augmented generation."))
    token, _ = _register(api)

    resp = _say(api, token)
    assert resp.status_code == 200, resp.text
    assert resp.json()["reply"] == "RAG means retrieval-augmented generation."
    assert resp.json()["suggested_actions"]


# ─────────────────────────────────────────────────────────────────────────
# 2. Authentication — and no provider call, no charge
# ─────────────────────────────────────────────────────────────────────────

def test_unauthenticated_request_is_rejected_before_the_provider(api, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    resp = api.post(CHAT, json={"content": "hello"})
    assert resp.status_code in (401, 403), resp.text
    assert llm.calls == []


def test_garbage_token_is_401(api, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    resp = api.post(CHAT, headers=_auth("not-a-jwt"), json={"content": "hello"})
    assert resp.status_code == 401, resp.text
    assert llm.calls == []


# ─────────────────────────────────────────────────────────────────────────
# 3. Provider failure — the charge is reversed, nothing leaks
# ─────────────────────────────────────────────────────────────────────────

def test_provider_error_refunds_and_returns_503(api, db, monkeypatch):
    _use(monkeypatch, FakeLLM(RuntimeError("provider down")))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _assert_failed_cleanly(_say(api, token), db, user_id, before)


def test_provider_timeout_refunds_and_returns_503(api, db, monkeypatch):
    timeout = openai.APITimeoutError(
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    )
    _use(monkeypatch, FakeLLM(timeout))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _assert_failed_cleanly(_say(api, token), db, user_id, before)


def test_provider_error_text_never_reaches_the_client(api, db, monkeypatch):
    secret = "sk-LEAK-ME-0123456789"
    _use(monkeypatch, FakeLLM(RuntimeError(
        f"401 Incorrect API key provided: {secret} at https://api.openai.com/v1"
    )))
    token, _ = _register(api)

    resp = _say(api, token)
    assert resp.status_code == 503
    for fragment in (secret, "Incorrect API key", "api.openai.com", "RuntimeError", "Traceback"):
        assert fragment not in resp.text, f"{fragment!r} leaked to the client"


@pytest.mark.parametrize("bad", [None, "", "   \n  "])
def test_empty_provider_answer_is_a_failure_not_a_paid_blank(api, db, monkeypatch, bad):
    """A model can return no content at all (a refusal, a length cutoff).
    That used to crash inside the JSON parser with the charge already taken."""
    _use(monkeypatch, FakeLLM(bad))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _assert_failed_cleanly(_say(api, token), db, user_id, before)


def test_failure_does_not_leave_the_next_message_broken(api, db, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(RuntimeError("blip"), GOOD_REPLY))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    assert _say(api, token).status_code == 503
    assert _balance(db, user_id) == before

    retry = _say(api, token)
    assert retry.status_code == 200, retry.text
    assert retry.json()["reply"].startswith("RAG retrieves")
    assert _balance(db, user_id) == before - COST
    assert len(llm.calls) == 2


# ─────────────────────────────────────────────────────────────────────────
# 4. Configuration — a missing key is a 503 with a refund, not a 500
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("backend, key_field", [
    ("openai", "OPENAI_API_KEY"),
    ("anthropic", "ANTHROPIC_API_KEY"),
])
def test_missing_provider_key_is_a_clean_refunded_503(api, db, monkeypatch, backend, key_field):
    """The real get_llm() — no stub — with no key, which is exactly what a
    deployment that forgot to provision one looks like."""
    monkeypatch.setattr(settings, "GENERATION_BACKEND", backend)
    monkeypatch.setattr(settings, key_field, None)
    token, user_id = _register(api)
    before = _balance(db, user_id)

    resp = _say(api, token)
    _assert_failed_cleanly(resp, db, user_id, before)
    for internal in ("API_KEY", ".env", "console.anthropic", "platform.openai"):
        assert internal not in resp.text, f"{internal!r} leaked to the client"


def test_blank_model_id_is_a_clean_refunded_503(api, db, monkeypatch):
    """`GENERATION_MODEL_ID=` (blank) is what deploy/production.env.example
    used to ship. pydantic-settings takes the empty string over the default,
    and the provider then rejects every request for having no model."""
    monkeypatch.setattr(settings, "GENERATION_BACKEND", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-test-not-real")
    monkeypatch.setattr(settings, "GENERATION_MODEL_ID", "")
    token, user_id = _register(api)
    before = _balance(db, user_id)

    _assert_failed_cleanly(_say(api, token), db, user_id, before)


# ─────────────────────────────────────────────────────────────────────────
# 5. Malformed provider output
# ─────────────────────────────────────────────────────────────────────────

def test_null_suggested_actions_does_not_500(api, monkeypatch):
    _use(monkeypatch, FakeLLM('{"reply": "ok", "suggested_actions": null}'))
    token, _ = _register(api)

    resp = _say(api, token)
    assert resp.status_code == 200, resp.text
    assert resp.json()["reply"] == "ok"
    assert resp.json()["suggested_actions"] == []


def test_wrongly_typed_fields_do_not_500(api, monkeypatch):
    _use(monkeypatch, FakeLLM('{"reply": ["a", "b"], "suggested_actions": "x"}'))
    token, _ = _register(api)

    resp = _say(api, token)
    assert resp.status_code == 200, resp.text
    assert isinstance(resp.json()["reply"], str) and resp.json()["reply"]
    assert resp.json()["suggested_actions"] == []


def test_non_string_suggestions_are_dropped(api, monkeypatch):
    _use(monkeypatch, FakeLLM('{"reply": "ok", "suggested_actions": ["Quiz me", 3, null, "Go on"]}'))
    token, _ = _register(api)

    assert _say(api, token).json()["suggested_actions"] == ["Quiz me", "Go on"]


# ─────────────────────────────────────────────────────────────────────────
# 6. Conversation history, language, context
# ─────────────────────────────────────────────────────────────────────────

def test_second_message_carries_the_first_exchange(api, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, _ = _register(api)

    _say(api, token, "What is RAG?")
    _say(api, token, "Explain it more simply")

    second = llm.calls[1]["messages"]
    assert [m["role"] for m in second] == ["user", "assistant", "user"]
    assert second[0]["content"] == "What is RAG?"
    assert second[1]["content"].startswith("RAG retrieves")
    assert second[2]["content"].startswith("Explain it more simply")


def test_only_the_last_ten_stored_messages_are_replayed(api, db, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)
    _say(api, token, "first")  # creates the session
    session = _sessions(db, user_id)[0]
    session.messages = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"m{i}", "timestamp": "t"}
        for i in range(14)
    ]
    db.commit()

    _say(api, token, "latest")
    sent = llm.calls[-1]["messages"]
    assert len(sent) == 11  # ten of history + the new question
    assert sent[0]["content"] == "m4"


@pytest.mark.parametrize("language, marker", [
    ("en", "Answer in English"),
    ("ar", "Modern Standard Arabic"),
])
def test_language_selects_the_policy_in_the_system_prompt(api, monkeypatch, language, marker):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, _ = _register(api)

    resp = _say(api, token, "ما هو RAG؟" if language == "ar" else "What is RAG?", language=language)
    assert resp.status_code == 200, resp.text
    assert marker in llm.calls[0]["system"]


def test_arabic_message_round_trips_intact(api, db, monkeypatch):
    arabic = "اشرح لي RAG ببساطة"
    llm = _use(monkeypatch, FakeLLM('{"reply": "تمام — RAG بيجيب المستندات الأول.", "suggested_actions": []}'))
    token, user_id = _register(api)

    resp = _say(api, token, arabic, language="ar", terminology_mode="arabic_first")
    assert resp.status_code == 200, resp.text
    assert resp.json()["reply"] == "تمام — RAG بيجيب المستندات الأول."
    assert llm.calls[0]["messages"][-1]["content"].startswith(arabic)
    assert _sessions(db, user_id)[0].messages[0]["content"] == arabic


def test_invalid_language_value_is_rejected_not_sent_to_the_model(api, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, _ = _register(api)

    assert _say(api, token, language="fr").status_code == 422
    assert llm.calls == []


@pytest.fixture()
def real_topic_id(db):
    """A real topic to use as context, removed again afterwards — the
    endpoint commits, so a rolled-back fixture would not clean it up."""
    suffix = uuid.uuid4().hex[:10]
    track = CareerTrack(slug=f"mc-{suffix}", title="Mentor ctx", is_active=True)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title="RAG", slug=f"rag-{suffix}", order=1)
    db.add(topic)
    db.commit()
    topic_id = topic.id
    yield topic_id
    db.rollback()
    db.query(MentorSession).filter(MentorSession.context_topic_id == topic_id).delete()
    db.query(Topic).filter(Topic.id == topic_id).delete()
    db.query(TrackLevel).filter(TrackLevel.track_id == track.id).delete()
    db.query(CareerTrack).filter(CareerTrack.id == track.id).delete()
    db.commit()


def test_topic_context_is_recorded_on_the_session(api, db, monkeypatch, real_topic_id):
    _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)

    resp = _say(api, token, topic_id=real_topic_id)
    assert resp.status_code == 200, resp.text
    assert _sessions(db, user_id)[0].context_topic_id == real_topic_id


def test_unknown_topic_is_refused_before_anything_is_charged(api, db, monkeypatch):
    """context_topic_id is a foreign key. An id that does not exist used to
    fail at INSERT — after the charge and after the provider had already
    been paid to answer."""
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    resp = _say(api, token, topic_id=987_654_321)
    assert resp.status_code == 404, resp.text
    assert llm.calls == [], "the provider was called for a request that could not be saved"
    assert _balance(db, user_id) == before
    assert _txs(db, user_id, TransactionType.deduction) == []


# ─────────────────────────────────────────────────────────────────────────
# 7. Input bounds
# ─────────────────────────────────────────────────────────────────────────

def test_empty_message_is_rejected_without_a_charge(api, db, monkeypatch):
    llm = _use(monkeypatch, FakeLLM(GOOD_REPLY))
    token, user_id = _register(api)
    before = _balance(db, user_id)

    assert _say(api, token, "").status_code == 422
    assert llm.calls == []
    assert _balance(db, user_id) == before
