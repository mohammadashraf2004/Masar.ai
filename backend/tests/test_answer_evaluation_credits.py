"""
Answer-evaluation credit accounting.

POST /practice/exercises/{id}/answer and
POST /practice/quizzes/{id}/questions/{i}/answer both charge
`exercise_feedback` before calling the provider, which is the right order
(never grade for free) but leaves a debt: if grading then fails, the
student has paid for nothing. These tests pin down both halves — the
charge sticks when it worked, and is reversed when it didn't — matching
the contract already tested for GET /mentor/roadmap.

The provider is always stubbed. Nothing here makes a real LLM call.
"""
import uuid

import pytest

from app.controllers import answer_evaluation_controller
from app.models.learning import (
    CareerTrack, DifficultyLevel, Exercise, Quiz, Topic, TrackLevel,
)
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.conftest import verify_registered

STRONG_PASSWORD = "correct-horse-battery-staple-7"
COST = CREDIT_COSTS["exercise_feedback"]

GOOD_RESULT = {
    "reply": "Close — you have the idea, but what happens on an empty list?",
    "is_correct": None,
    "score": None,
    "suggested_actions": ["Try the empty case"],
}


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client):
    email = f"ans-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Answer Tester", "password": STRONG_PASSWORD,
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
def topic(db) -> Topic:
    track = CareerTrack(slug=f"ans-track-{uuid.uuid4().hex[:8]}", title="Answer Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    t = Topic(
        level_id=level.id, title="T1", slug=f"ans-t1-{uuid.uuid4().hex[:8]}", order=1,
        difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
        prerequisite_ids=[], skill_tags=[],
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@pytest.fixture()
def exercise(db, topic) -> Exercise:
    ex = Exercise(
        topic_id=topic.id,
        title="Reverse a list",
        description="Write a function that reverses a list.",
        starter_code="def rev(xs): ...",
        solution_code="def rev(xs): return xs[::-1]",
        skill_tested=["python"],
    )
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex


@pytest.fixture()
def open_quiz(db, topic) -> Quiz:
    q = Quiz(
        topic_id=topic.id,
        title="Open Quiz",
        passing_score=50,
        questions=[{"type": "open", "question": "Explain closures.", "explanation": "reference"}],
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@pytest.fixture()
def stub_llm(monkeypatch):
    """A provider handle that never gets called for real."""
    monkeypatch.setattr(answer_evaluation_controller, "get_llm", lambda: object())


@pytest.fixture()
def working_provider(monkeypatch, stub_llm):
    monkeypatch.setattr(
        answer_evaluation_controller.answer_evaluator_service,
        "evaluate_answer", lambda **kw: dict(GOOD_RESULT),
    )


@pytest.fixture()
def broken_provider(monkeypatch, stub_llm):
    def _boom(**kwargs):
        raise RuntimeError("provider down")
    monkeypatch.setattr(
        answer_evaluation_controller.answer_evaluator_service, "evaluate_answer", _boom,
    )


@pytest.fixture()
def empty_provider(monkeypatch, stub_llm):
    """The provider answered, but with nothing to show the student."""
    monkeypatch.setattr(
        answer_evaluation_controller.answer_evaluator_service,
        "evaluate_answer",
        lambda **kw: {"reply": "   ", "is_correct": None, "score": None, "suggested_actions": []},
    )


@pytest.fixture()
def unparseable_provider(monkeypatch, stub_llm):
    """The provider ignored the JSON contract. answer_evaluator_service
    degrades that to a plain-text reply, so the student still gets an
    answer — which they should still be charged for."""
    monkeypatch.setattr(
        answer_evaluation_controller.answer_evaluator_service,
        "evaluate_answer",
        lambda **kw: {
            "reply": "Sorry, I got a bit muddled, but your loop looks right.",
            "is_correct": None, "score": None, "suggested_actions": [],
        },
    )


def _answer_exercise(client, token, exercise, content="my answer"):
    return client.post(
        f"/api/v1/practice/exercises/{exercise.id}/answer",
        headers=_auth(token), json={"content": content},
    )


def _answer_quiz(client, token, quiz, content="my answer"):
    return client.post(
        f"/api/v1/practice/quizzes/{quiz.id}/questions/0/answer",
        headers=_auth(token), json={"content": content},
    )


# ─────────────────────────────────────────────────────────────────────────
# 1. Success — the charge stands
# ─────────────────────────────────────────────────────────────────────────

def test_successful_evaluation_keeps_the_deduction(client, db, exercise, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = _answer_exercise(client, token, exercise)
    assert resp.status_code == 200, resp.text
    assert resp.json()["messages"][-1]["content"] == GOOD_RESULT["reply"]

    assert _wallet(db, user_id).credit_balance == before - COST
    deductions = _txs(db, user_id, TransactionType.deduction)
    assert len(deductions) == 1
    assert deductions[0].credits == -COST
    assert deductions[0].action_type == "exercise_feedback"
    # A successful call must never be refunded.
    assert _txs(db, user_id, TransactionType.refund) == []


def test_successful_quiz_answer_keeps_the_deduction(client, db, open_quiz, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    assert _answer_quiz(client, token, open_quiz).status_code == 200

    assert _wallet(db, user_id).credit_balance == before - COST
    assert _txs(db, user_id, TransactionType.refund) == []


def test_lifetime_spent_tracks_a_successful_charge(client, db, exercise, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).lifetime_spent or 0
    _answer_exercise(client, token, exercise)
    assert _wallet(db, user_id).lifetime_spent == before + COST


# ─────────────────────────────────────────────────────────────────────────
# 2. Provider failure — the charge is reversed
# ─────────────────────────────────────────────────────────────────────────

def test_provider_exception_refunds_the_credits(client, db, exercise, broken_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = _answer_exercise(client, token, exercise)
    assert resp.status_code == 503, resp.text
    assert "refunded" in resp.json()["detail"].lower()

    # Net zero: the deduction and the refund both exist and cancel out.
    assert _wallet(db, user_id).credit_balance == before

    deductions = _txs(db, user_id, TransactionType.deduction)
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(deductions) == 1 and deductions[0].credits == -COST
    assert len(refunds) == 1
    assert refunds[0].credits == COST
    assert refunds[0].action_type == "exercise_feedback"
    assert refunds[0].balance_after == before


def test_provider_exception_refunds_on_the_quiz_route_too(client, db, open_quiz, broken_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    assert _answer_quiz(client, token, open_quiz).status_code == 503
    assert _wallet(db, user_id).credit_balance == before


def test_provider_error_is_not_exposed(client, db, exercise, broken_provider):
    """The client is told grading is unavailable, never why."""
    token, _ = _register(client)
    detail = _answer_exercise(client, token, exercise).json()["detail"]
    assert "provider down" not in detail
    assert "RuntimeError" not in detail


def test_empty_reply_refunds_the_credits(client, db, exercise, empty_provider):
    """The provider answered, but with nothing to show. The student is
    equally empty-handed, so the charge is reversed the same way."""
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    assert _answer_exercise(client, token, exercise).status_code == 503
    assert _wallet(db, user_id).credit_balance == before
    assert len(_txs(db, user_id, TransactionType.refund)) == 1


def test_unparseable_but_usable_reply_is_still_charged(client, db, exercise, unparseable_provider):
    """A provider that ignored the JSON contract still produced feedback
    the student can read — that is delivery, so the charge stands."""
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = _answer_exercise(client, token, exercise)
    assert resp.status_code == 200, resp.text
    assert _wallet(db, user_id).credit_balance == before - COST
    assert _txs(db, user_id, TransactionType.refund) == []


def test_failed_turn_leaves_no_half_written_submission(client, db, exercise, broken_provider):
    """The student's question must not be recorded as a graded turn when
    nothing graded it."""
    from app.models.answer_submission import AnswerSubmission

    token, user_id = _register(client)
    assert _answer_exercise(client, token, exercise).status_code == 503

    db.expire_all()
    rows = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == user_id,
        AnswerSubmission.exercise_id == exercise.id,
    ).all()
    assert rows == []
    assert client.get(
        f"/api/v1/practice/exercises/{exercise.id}/answer", headers=_auth(token),
    ).status_code == 404


def test_refund_is_committed_not_just_staged(client, db, exercise, broken_provider):
    """The deduction commits before the provider call, so the refund has to
    commit too — a refund left in an uncommitted session is no refund."""
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    _answer_exercise(client, token, exercise)

    from app.db.session import SessionLocal
    fresh = SessionLocal()
    try:
        balance = fresh.query(UserWallet).filter(
            UserWallet.user_id == user_id
        ).one().credit_balance
    finally:
        fresh.close()
    assert balance == before


def test_refund_does_not_inflate_lifetime_purchased(client, db, exercise, broken_provider):
    """A refund is not a purchase. Reversing the spend must not make the
    wallet claim the student bought credits they never bought."""
    token, user_id = _register(client)
    purchased_before = _wallet(db, user_id).lifetime_purchased or 0
    spent_before = _wallet(db, user_id).lifetime_spent or 0

    _answer_exercise(client, token, exercise)

    wallet = _wallet(db, user_id)
    assert wallet.lifetime_purchased == purchased_before
    assert wallet.lifetime_spent == spent_before


def test_repeated_failures_do_not_drift_the_balance(client, db, exercise, broken_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    for _ in range(3):
        assert _answer_exercise(client, token, exercise).status_code == 503
    assert _wallet(db, user_id).credit_balance == before
    assert len(_txs(db, user_id, TransactionType.deduction)) == 3
    assert len(_txs(db, user_id, TransactionType.refund)) == 3


# ─────────────────────────────────────────────────────────────────────────
# 3. Insufficient credits — unchanged, and never refunded
# ─────────────────────────────────────────────────────────────────────────

def test_insufficient_credits_still_returns_402(client, db, exercise, working_provider):
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = COST - 1
    db.commit()

    resp = _answer_exercise(client, token, exercise)
    assert resp.status_code == 402
    detail = resp.json()["detail"]
    assert detail["error"] == "insufficient_credits"
    assert detail["credits_needed"] == COST


def test_402_is_never_refunded(client, db, exercise, broken_provider):
    """The 402 is raised before the grading call, so there is nothing to
    reverse — a refund here would mint credits out of a failed request."""
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 0
    db.commit()

    assert _answer_exercise(client, token, exercise).status_code == 402

    assert _wallet(db, user_id).credit_balance == 0
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _txs(db, user_id, TransactionType.deduction) == []


# ─────────────────────────────────────────────────────────────────────────
# 4. Rate limiting — refused before the handler, so never charged
# ─────────────────────────────────────────────────────────────────────────

def test_rate_limit_still_applies(client, db, exercise, working_provider):
    """20/minute, unchanged by the refund work. Credits are topped up so
    the limiter is what stops the run, not an empty wallet."""
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 1000
    db.commit()

    statuses = [_answer_exercise(client, token, exercise).status_code for _ in range(22)]
    assert statuses[:20] == [200] * 20
    assert 429 in statuses[20:], statuses


def test_429_is_never_charged_or_refunded(client, db, exercise, working_provider):
    token, user_id = _register(client)
    wallet = _wallet(db, user_id)
    wallet.credit_balance = 1000
    db.commit()

    for _ in range(22):
        _answer_exercise(client, token, exercise)

    # Twenty got past the limiter; only those twenty were charged, and a
    # rate-limited request moved the wallet in neither direction.
    assert len(_txs(db, user_id, TransactionType.deduction)) == 20
    assert _txs(db, user_id, TransactionType.refund) == []
    assert _wallet(db, user_id).credit_balance == 1000 - (20 * COST)


# ─────────────────────────────────────────────────────────────────────────
# 5. Everything else about the endpoints is unchanged
# ─────────────────────────────────────────────────────────────────────────

def test_answering_still_requires_authentication(client, exercise):
    assert client.post(
        f"/api/v1/practice/exercises/{exercise.id}/answer", json={"content": "x"},
    ).status_code == 401


def test_unknown_exercise_is_still_404_and_free(client, db, working_provider):
    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance
    resp = client.post(
        "/api/v1/practice/exercises/999999/answer",
        headers=_auth(token), json={"content": "x"},
    )
    assert resp.status_code == 404
    assert _wallet(db, user_id).credit_balance == before


def test_mcq_question_is_still_rejected_before_charging(client, db, topic, working_provider):
    """An MCQ question grades instantly elsewhere; this route refuses it,
    and must do so without taking credits."""
    quiz = Quiz(
        topic_id=topic.id, title="MCQ Quiz", passing_score=50,
        questions=[{"question": "2+2?", "options": ["3", "4"], "correct": 1}],
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    token, user_id = _register(client)
    before = _wallet(db, user_id).credit_balance

    resp = _answer_quiz(client, token, quiz)
    assert resp.status_code == 400
    assert _wallet(db, user_id).credit_balance == before


def test_conversation_is_retrievable_after_a_successful_turn(client, exercise, working_provider):
    token, _ = _register(client)
    _answer_exercise(client, token, exercise, content="first try")

    resp = client.get(
        f"/api/v1/practice/exercises/{exercise.id}/answer", headers=_auth(token),
    )
    assert resp.status_code == 200
    messages = resp.json()["messages"]
    assert messages[0]["content"] == "first try"
    assert messages[1]["content"] == GOOD_RESULT["reply"]
