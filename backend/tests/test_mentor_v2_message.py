"""POST /mentor/message — Mentor v2 chat.

Pins down: hints and quiz answers are not leaked, an explicit intent wins,
detached context gives "general" answers, one learner never sees another's
context, a failed reply is refunded, and proactive/rule-based replies cost 0.
"""
import json

import pytest

from app.models.wallet import TransactionType
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.mentor_v2_fixtures import (
    CORRECT_OPTION, MESSAGE, QUIZ_ANSWER, SOLUTION, blocks_json, install_llm,
    make_course, register, txs, wallet,
)

COST = CREDIT_COSTS["mentor_chat"]


@pytest.fixture()
def course():
    return make_course()


def _solution_lines():
    return [l.strip() for l in SOLUTION.splitlines() if len(l.strip()) >= 12]


# ─── Hints ────────────────────────────────────────────────────────────────

def test_hint_that_leaks_the_solution_is_retried_then_replaced(client, db, monkeypatch, course):
    headers, user_id = register(client)
    leaky = blocks_json({"kind": "hint", "grounding": "lesson", "text": "Here you go:", "code": SOLUTION})
    fake = install_llm(monkeypatch, [leaky, leaky])
    before = wallet(db, user_id).credit_balance

    resp = client.post(MESSAGE, headers=headers, json={
        "content": "give me a hint, the second test fails",
        "lessonId": course["lesson"], "exerciseId": course["exercise"], "intent": "hint",
    })
    assert resp.status_code == 200, resp.text
    body = resp.json()

    assert len(fake.calls) == 2  # one try, one retry, no third
    assert "hint_leak" in fake.calls[1]["messages"][-1]["content"]
    assert body["fallback"] is True
    served = json.dumps(body["blocks"], ensure_ascii=False)
    assert not any(line in served for line in _solution_lines())
    # The fallback is rule-based, so the charge is reversed.
    assert body["creditsCharged"] == 0
    assert wallet(db, user_id).credit_balance == before
    assert len(txs(db, user_id, TransactionType.refund)) == 1


def test_clean_hint_is_served_and_charged(client, db, monkeypatch, course):
    headers, user_id = register(client)
    leaky = blocks_json({"kind": "hint", "grounding": "lesson", "text": "x", "code": SOLUTION})
    clean = blocks_json({"kind": "hint", "grounding": "lesson",
                         "text": "The checkpointer stores state under a thread_id. What does invoke receive as its second argument?"})
    install_llm(monkeypatch, [leaky, clean])
    before = wallet(db, user_id).credit_balance

    resp = client.post(MESSAGE, headers=headers, json={
        "content": "hint please", "lessonId": course["lesson"], "exerciseId": course["exercise"], "intent": "hint",
    })
    body = resp.json()
    assert body["fallback"] is False
    assert body["blocks"][0]["kind"] == "hint" and body["blocks"][0]["level"] == 1
    assert body["blocks"][0]["source"]["lessonId"] == course["lesson"]
    assert body["creditsCharged"] == COST
    assert wallet(db, user_id).credit_balance == before - COST


# ─── Quiz answers ─────────────────────────────────────────────────────────

def test_reply_giving_away_a_quiz_answer_is_rejected(client, db, monkeypatch, course):
    headers, _ = register(client)
    leaky = blocks_json({"kind": "text", "grounding": "general",
                         "text": f"The correct answer is: {CORRECT_OPTION}."})
    fake = install_llm(monkeypatch, [leaky, leaky])

    resp = client.post(MESSAGE, headers=headers, json={
        "content": "explain when the checkpointer runs", "lessonId": course["lesson"], "intent": "explain",
    })
    body = resp.json()
    assert "quiz_leak" in fake.calls[1]["messages"][-1]["content"]
    assert body["fallback"] is True
    assert CORRECT_OPTION.lower() not in json.dumps(body).lower()


def test_quiz_intent_serves_a_stored_question_without_its_key_for_free(client, db, monkeypatch, course):
    headers, user_id = register(client)
    fake = install_llm(monkeypatch, [])
    before = wallet(db, user_id).credit_balance

    resp = client.post(MESSAGE, headers=headers, json={"content": "اختبرني", "lessonId": course["lesson"]})
    body = resp.json()
    assert body["intent"] == "quiz" and body["intentSource"] == "rules"
    quiz = next(b for b in body["blocks"] if b["kind"] == "quiz")["quiz"]
    assert set(quiz) == {"quizId", "questionIndex", "question", "options"}
    assert "Saving a snapshot per node" not in json.dumps(body)  # the explanation stays server-side
    assert fake.calls == []
    assert body["creditsCharged"] == 0
    assert wallet(db, user_id).credit_balance == before
    assert txs(db, user_id, TransactionType.deduction) == []


# ─── Intent ───────────────────────────────────────────────────────────────

def test_explicit_intent_wins_over_detection(client, monkeypatch, course):
    headers, _ = register(client)
    reply = blocks_json({"kind": "text", "grounding": "lesson",
                         "text": "The checkpointer captures a snapshot of the graph state after each node."})
    fake = install_llm(monkeypatch, [reply])

    # "اختبرني" (quiz me) would be detected as quiz; the chip says explain.
    resp = client.post(MESSAGE, headers=headers, json={
        "content": "اختبرني", "lessonId": course["lesson"], "intent": "explain",
    })
    body = resp.json()
    assert body["intent"] == "explain" and body["intentSource"] == "explicit"
    assert len(fake.calls) == 1  # no classification call, straight to the reply
    assert "Intent: explain." in fake.calls[0]["system"]


def test_model_classifies_only_when_rules_cannot_decide(client, monkeypatch, course):
    headers, _ = register(client)
    reply = blocks_json({"kind": "text", "grounding": "general", "text": "Sure — tell me more about it."})
    fake = install_llm(monkeypatch, ["socratic", reply])

    resp = client.post(MESSAGE, headers=headers, json={"content": "thread_id?", "lessonId": course["lesson"]})
    body = resp.json()
    assert body["intent"] == "socratic" and body["intentSource"] == "model"
    assert fake.calls[0]["max_tokens"] <= 10


# ─── Context ──────────────────────────────────────────────────────────────

def test_detached_context_gives_general_answers(client, monkeypatch, course):
    headers, _ = register(client)
    # The model claims lesson grounding anyway; with nothing attached that
    # cannot be true, so it is reported as general.
    reply = blocks_json({"kind": "text", "grounding": "lesson",
                         "text": "thread_id names the conversation a checkpointer resumes."})
    fake = install_llm(monkeypatch, [reply])

    resp = client.post(MESSAGE, headers=headers, json={"content": "why do we need thread_id?", "intent": "why"})
    body = resp.json()
    assert resp.status_code == 200, resp.text
    assert {b["grounding"] for b in body["blocks"]} == {"general"}
    assert body["context"]["lessonId"] is None
    assert "No course context is attached" in fake.prompts()
    assert "Persistent memory" not in fake.prompts()


def test_client_supplied_progress_and_grades_are_ignored(client, monkeypatch, course):
    headers, _ = register(client)
    reply = blocks_json({"kind": "text", "grounding": "general", "text": "ok"})
    fake = install_llm(monkeypatch, [reply])

    resp = client.post(MESSAGE, headers=headers, json={
        "content": "explain the checkpointer", "lessonId": course["lesson"], "intent": "explain",
        "progress": {"lessonsCompleted": 99}, "mastery": {"Checkpointers": 1.0}, "grades": [100],
    })
    assert resp.status_code == 200, resp.text
    prompt = fake.prompts()
    assert "Lessons completed in this module: 0" in prompt
    assert "99" not in prompt and "Checkpointers 1.00" not in prompt


def test_a_learner_cannot_read_another_learners_context(client, monkeypatch, course):
    a_headers, _ = register(client)
    b_headers, _ = register(client)

    # A gets a quiz question wrong: that mistake is A's context.
    r = client.post(QUIZ_ANSWER, headers=a_headers, json={"quizId": course["quiz"], "questionIndex": 0, "choice": 2})
    assert r.status_code == 200, r.text

    reply = blocks_json({"kind": "text", "grounding": "general", "text": "ok"})
    fake_a = install_llm(monkeypatch, [reply])
    a_resp = client.post(MESSAGE, headers=a_headers, json={
        "content": "explain the checkpointer", "lessonId": course["lesson"], "intent": "explain"})
    assert "When does LangGraph call the checkpointer?" in fake_a.prompts()

    fake_b = install_llm(monkeypatch, [reply])
    b_resp = client.post(MESSAGE, headers=b_headers, json={
        "content": "explain the checkpointer", "lessonId": course["lesson"], "intent": "explain"})
    assert "When does LangGraph call the checkpointer?" not in fake_b.prompts()
    assert "## RECENT MISTAKES" not in fake_b.prompts()
    assert b_resp.json()["sessionId"] != a_resp.json()["sessionId"]

    # Nor can B write into, or read through, A's session.
    install_llm(monkeypatch, [reply])
    stolen = client.post(MESSAGE, headers=b_headers, json={
        "content": "hi", "intent": "explain", "sessionId": a_resp.json()["sessionId"]})
    assert stolen.status_code == 404
    assert client.get(f"/api/v1/mentor/sessions/{a_resp.json()['sessionId']}", headers=b_headers).status_code == 404


def test_unknown_lesson_is_404_and_free(client, db, monkeypatch, course):
    headers, user_id = register(client)
    install_llm(monkeypatch, [])
    before = wallet(db, user_id).credit_balance
    resp = client.post(MESSAGE, headers=headers, json={"content": "explain", "lessonId": 987654321})
    assert resp.status_code == 404
    assert wallet(db, user_id).credit_balance == before


# ─── Credits ──────────────────────────────────────────────────────────────

def test_failed_reply_is_refunded(client, db, monkeypatch, course):
    headers, user_id = register(client)
    install_llm(monkeypatch, [RuntimeError("provider down")])
    before = wallet(db, user_id).credit_balance

    resp = client.post(MESSAGE, headers=headers, json={
        "content": "explain the checkpointer", "lessonId": course["lesson"], "intent": "explain"})
    assert resp.status_code == 503
    assert "refunded" in resp.json()["detail"]
    assert wallet(db, user_id).credit_balance == before
    assert len(txs(db, user_id, TransactionType.deduction)) == 1
    refunds = txs(db, user_id, TransactionType.refund)
    assert len(refunds) == 1 and refunds[0].credits == COST


def test_proactive_reply_costs_nothing_and_never_calls_the_model(client, db, monkeypatch, course):
    headers, user_id = register(client)
    client.post(f"/api/v1/tracks/topics/{course['topic']}/progress", headers=headers,
                json={"lesson_id": course["lesson"]})
    fake = install_llm(monkeypatch, [])
    before = wallet(db, user_id).credit_balance

    resp = client.post(MESSAGE, headers=headers, json={"trigger": "lesson_completed", "lessonId": course["lesson"]})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["proactive"] is True and body["creditsCharged"] == 0
    assert any(b["kind"] == "quiz" for b in body["blocks"])
    assert fake.calls == []
    assert wallet(db, user_id).credit_balance == before
    assert txs(db, user_id, TransactionType.deduction) == []


def test_replies_are_stored_in_the_existing_mentor_session(client, monkeypatch, course):
    headers, _ = register(client)
    reply = blocks_json({"kind": "text", "grounding": "lesson",
                         "text": "The checkpointer captures a snapshot of the graph state."})
    install_llm(monkeypatch, [reply])
    body = client.post(MESSAGE, headers=headers, json={
        "content": "explain", "lessonId": course["lesson"], "intent": "explain"}).json()

    session = client.get(f"/api/v1/mentor/sessions/{body['sessionId']}", headers=headers).json()
    assert [m["role"] for m in session["messages"]] == ["user", "assistant"]
    assert session["messages"][1]["blocks"][0]["grounding"] == "lesson"
    assert session["messages"][1]["content"]  # v1 readers still get plain text
