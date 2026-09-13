"""
IDOR/BOLA regression tests for answer_evaluation_controller.

Mirrors test_security.py's mentor-session IDOR tests: a victim's
conversational exercise/quiz-question grading is per-user state
(AnswerSubmission.user_id) and must never be readable, or extendable,
by another authenticated user who happens to know the same
exercise_id / quiz_id — there is no submission id in any request here,
only content ids, so the resolution query itself is the whole boundary.
"""
import uuid

import pytest

from app.controllers import answer_evaluation_controller as aec
from app.models.answer_submission import AnswerSubmission
from app.models.learning import CareerTrack, Exercise, Quiz, Topic, TrackLevel
from app.services.wallet.wallet_service import add_credits
from tests.conftest import verify_registered

STRONG_PASSWORD = "correct-horse-battery-staple-7"

FAKE_EVAL_CORRECT = {"reply": "Correct!", "is_correct": True, "score": 100.0}
FAKE_EVAL_WRONG = {"reply": "Not quite.", "is_correct": False, "score": 20.0}


def _register(client):
    email = f"ans-idor-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Attacker Or Victim", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    verify_registered(client, body["user"]["id"])
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _fund(db, user_id, amount=1000):
    add_credits(user_id, amount, db, description="test funds")


@pytest.fixture()
def topic_with_content(db):
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"ans-idor-track-{suffix}", title="T", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, slug=f"ans-idor-topic-{suffix}", title="Topic", order=1)
    db.add(topic)
    db.flush()
    exercise = Exercise(
        topic_id=topic.id, title="Ex", description="Do the thing",
        starter_code="", solution_code="reference solution",
    )
    quiz = Quiz(topic_id=topic.id, title="Q", passing_score=70, questions=[
        {"type": "open", "question": "Explain X.", "explanation": "Because Y."},
    ])
    db.add_all([exercise, quiz])
    db.commit()
    db.refresh(exercise)
    db.refresh(quiz)
    return {"exercise_id": exercise.id, "quiz_id": quiz.id}


@pytest.fixture()
def stub_evaluator(monkeypatch):
    monkeypatch.setattr(aec, "get_llm", lambda: object())
    responses = {"value": dict(FAKE_EVAL_CORRECT)}

    def _evaluate(**kwargs):
        return dict(responses["value"])

    monkeypatch.setattr(aec.answer_evaluator_service, "evaluate_answer", _evaluate)
    return responses


# ─────────────────────────────────────────────────────────────────────────
# Exercise conversations
# ─────────────────────────────────────────────────────────────────────────

def test_attacker_cannot_read_victims_exercise_conversation(
    client, db, topic_with_content, stub_evaluator,
):
    victim_token, victim_id = _register(client)
    attacker_token, _ = _register(client)
    _fund(db, victim_id)
    exercise_id = topic_with_content["exercise_id"]

    posted = client.post(
        f"/api/v1/practice/exercises/{exercise_id}/answer",
        headers=_auth(victim_token),
        json={"content": "my private attempt at the answer"},
    )
    assert posted.status_code == 200, posted.text

    stolen = client.get(
        f"/api/v1/practice/exercises/{exercise_id}/answer", headers=_auth(attacker_token),
    )
    assert stolen.status_code == 404
    assert "my private attempt" not in stolen.text


def test_attacker_posting_to_the_same_exercise_gets_their_own_conversation_not_the_victims(
    client, db, topic_with_content, stub_evaluator,
):
    """Both users answering the same exercise must never merge into one
    conversation, and the attacker's turn must not read or extend the
    victim's message history."""
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)
    exercise_id = topic_with_content["exercise_id"]

    client.post(
        f"/api/v1/practice/exercises/{exercise_id}/answer", headers=_auth(victim_token),
        json={"content": "victim's private message"},
    )
    resp = client.post(
        f"/api/v1/practice/exercises/{exercise_id}/answer", headers=_auth(attacker_token),
        json={"content": "attacker's own message"},
    )
    assert resp.status_code == 200

    victim_sub = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == victim_id, AnswerSubmission.exercise_id == exercise_id,
    ).one()
    attacker_sub = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == attacker_id, AnswerSubmission.exercise_id == exercise_id,
    ).one()

    assert victim_sub.id != attacker_sub.id
    attacker_contents = [m["content"] for m in attacker_sub.messages]
    assert "victim's private message" not in attacker_contents
    assert len(victim_sub.messages) == 2  # only the victim's own user+assistant turn


# ─────────────────────────────────────────────────────────────────────────
# Open-ended quiz-question conversations
# ─────────────────────────────────────────────────────────────────────────

def test_attacker_cannot_read_victims_quiz_question_conversation(
    client, db, topic_with_content, stub_evaluator,
):
    victim_token, victim_id = _register(client)
    attacker_token, _ = _register(client)
    _fund(db, victim_id)
    quiz_id = topic_with_content["quiz_id"]

    posted = client.post(
        f"/api/v1/practice/quizzes/{quiz_id}/questions/0/answer",
        headers=_auth(victim_token),
        json={"content": "victim's open-ended answer"},
    )
    assert posted.status_code == 200, posted.text

    stolen = client.get(
        f"/api/v1/practice/quizzes/{quiz_id}/questions/0/answer", headers=_auth(attacker_token),
    )
    assert stolen.status_code == 404
    assert "victim's open-ended answer" not in stolen.text


def test_attacker_cannot_extend_victims_quiz_question_conversation(
    client, db, topic_with_content, stub_evaluator,
):
    """Confirms the write path is scoped the same way the read path is —
    an attacker answering the same (quiz_id, question_index) must create
    their own row, never append to the victim's."""
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)
    quiz_id = topic_with_content["quiz_id"]

    client.post(
        f"/api/v1/practice/quizzes/{quiz_id}/questions/0/answer", headers=_auth(victim_token),
        json={"content": "victim's answer"},
    )
    client.post(
        f"/api/v1/practice/quizzes/{quiz_id}/questions/0/answer", headers=_auth(attacker_token),
        json={"content": "attacker's answer"},
    )

    from app.models.answer_submission import AnswerSubmission as Sub
    victim_sub = db.query(Sub).filter(
        Sub.user_id == victim_id, Sub.quiz_id == quiz_id, Sub.question_index == 0,
    ).one()
    attacker_sub = db.query(Sub).filter(
        Sub.user_id == attacker_id, Sub.quiz_id == quiz_id, Sub.question_index == 0,
    ).one()
    assert victim_sub.id != attacker_sub.id
    assert len(victim_sub.messages) == 2
    assert len(attacker_sub.messages) == 2
