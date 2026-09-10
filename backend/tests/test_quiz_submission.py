"""
Regression test for a real bug found while adding quiz-taking UI: a quiz
mixing MCQ and open-ended ("type": "open") questions used to score the
open questions as if they were MCQ — since an open question has no
"correct" index and the client doesn't submit a numeric answer for it
either, `None == None` silently counted it as correct.
"""
import uuid

import pytest

from app.db.session import SessionLocal
from app.models.learning import Topic, TrackLevel, CareerTrack, Quiz, DifficultyLevel
from app.models.progress import QuizAttempt


def _register(client) -> str:
    email = f"quiz-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Quiz Test", "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201
    return resp.json()["access_token"]


def _make_mixed_quiz(db) -> int:
    track = CareerTrack(slug=f"test-track-{uuid.uuid4().hex[:8]}", title="Test Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title="T1", slug=f"t1-{uuid.uuid4().hex[:8]}", order=1,
                   difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
                   prerequisite_ids=[], skill_tags=[])
    db.add(topic)
    db.flush()
    quiz = Quiz(
        topic_id=topic.id,
        title="Mixed Quiz",
        passing_score=100,  # must get every MCQ right to pass
        questions=[
            {"question": "2+2?", "options": ["3", "4"], "correct": 1, "explanation": "..."},
            {"type": "open", "question": "Explain closures.", "explanation": "reference answer"},
            {"question": "Capital of Egypt?", "options": ["Cairo", "Alexandria"], "correct": 0, "explanation": "..."},
        ],
    )
    db.add(quiz)
    db.commit()
    return quiz.id


def test_open_questions_excluded_from_mcq_scoring(client, db):
    token = _register(client)
    headers = {"Authorization": f"Bearer {token}"}

    setup = SessionLocal()
    quiz_id = _make_mixed_quiz(setup)
    setup.close()

    # Answer both MCQ questions correctly (index 0 and 2), say nothing
    # about the open question at index 1 — matches what a real frontend
    # would send, since open questions are graded separately.
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                        json={"answers": {"0": 1, "2": 0}}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()

    # Before the fix: score was computed against len(questions) == 3,
    # and the open question's None-vs-None comparison could inflate the
    # correct count — either way, this asserts the only mathematically
    # correct outcome: 2/2 MCQ questions correct = 100%, not 2/3 ≈ 66.7%.
    assert body["score"] == 100.0
    assert body["passed"] is True
    assert body["feedback"]["1"]["skipped"] is True
    assert body["feedback"]["0"]["correct"] is True
    assert body["feedback"]["2"]["correct"] is True


def test_wrong_mcq_answer_fails_even_with_open_question_present(client, db):
    token = _register(client)
    headers = {"Authorization": f"Bearer {token}"}

    setup = SessionLocal()
    quiz_id = _make_mixed_quiz(setup)
    setup.close()

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                        json={"answers": {"0": 0, "2": 0}}, headers=headers)  # first answer wrong
    body = resp.json()
    assert body["score"] == 50.0  # 1/2 MCQ correct
    assert body["passed"] is False


# ─────────────────────────────────────────────────────────────────────────
# Helpers for the hardening tests below
# ─────────────────────────────────────────────────────────────────────────

def _register_with_id(client):
    """Same registration as _register, but hands back the user id too —
    needed to assert which account an attempt row actually belongs to."""
    email = f"quiz-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Quiz Test", "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["access_token"], body["user"]["id"]


def _make_quiz(db, questions, passing_score=70) -> int:
    """_make_mixed_quiz with the questions blob left to the caller, so the
    malformed-content tests can author something the seeder never would."""
    track = CareerTrack(slug=f"test-track-{uuid.uuid4().hex[:8]}", title="Test Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title="T1", slug=f"t1-{uuid.uuid4().hex[:8]}", order=1,
                  difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
                  prerequisite_ids=[], skill_tags=[])
    db.add(topic)
    db.flush()
    quiz = Quiz(topic_id=topic.id, title="Quiz", passing_score=passing_score, questions=questions)
    db.add(quiz)
    db.commit()
    return quiz.id


def _seed(factory, *args, **kwargs):
    """Commit fixture rows on their own session, matching how the two
    original tests in this file set up their quiz."""
    setup = SessionLocal()
    try:
        return factory(setup, *args, **kwargs)
    finally:
        setup.close()


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────────────────────────────────
# A. Authentication
# ─────────────────────────────────────────────────────────────────────────

def test_quiz_submit_requires_authentication(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit", json={"answers": {"0": 1}})
    assert resp.status_code == 401


def test_quiz_attempts_require_authentication(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    assert client.get(f"/api/v1/tracks/quizzes/{quiz_id}/attempts").status_code == 401


# ─────────────────────────────────────────────────────────────────────────
# B. User isolation
# ─────────────────────────────────────────────────────────────────────────

def test_quiz_attempts_are_scoped_to_the_caller(client, db):
    """There is no user id in the request to tamper with, and the attempts
    query is scoped to the token's subject — so B must not see A's work."""
    quiz_id = _seed(_make_mixed_quiz)
    token_a = _register(client)
    token_b = _register(client)

    submit = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                         json={"answers": {"0": 1, "2": 0}}, headers=_auth(token_a))
    assert submit.status_code == 200

    assert len(client.get(f"/api/v1/tracks/quizzes/{quiz_id}/attempts",
                          headers=_auth(token_a)).json()) == 1
    assert client.get(f"/api/v1/tracks/quizzes/{quiz_id}/attempts",
                      headers=_auth(token_b)).json() == []


def test_submission_creates_an_attempt_owned_by_the_submitter(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    token, user_id = _register_with_id(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1}}, headers=_auth(token))
    assert resp.status_code == 200
    attempt_id = resp.json()["id"]

    check = SessionLocal()
    try:
        row = check.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).one()
        assert row.user_id == user_id
        assert row.quiz_id == quiz_id
    finally:
        check.close()


# ─────────────────────────────────────────────────────────────────────────
# C. Answer-key policy after submission
# ─────────────────────────────────────────────────────────────────────────

def test_submit_does_not_return_the_correct_answer(client, db):
    """The taker learns whether they were right, not what the right answer
    was. Returning the key made one throwaway POST a complete answer-key
    dump — precisely what QuizResponse strips from every read path."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 0, "2": 1}}, headers=_auth(token))  # both wrong
    assert resp.status_code == 200
    assert "correct_answer" not in resp.text
    for entry in resp.json()["feedback"].values():
        assert "correct_answer" not in entry


def test_a_blank_submission_reveals_nothing(client, db):
    """The actual attack: submit nothing, read the key out of feedback,
    resubmit with a perfect score."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {}}, headers=_auth(token))
    assert resp.status_code == 200
    assert resp.json()["score"] == 0.0
    assert "correct_answer" not in resp.text


def test_attempts_do_not_replay_the_correct_answer(client, db):
    """The attempts endpoint serves the STORED feedback blob, so the key
    must not have been written to the row in the first place."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)

    client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                json={"answers": {"0": 1}}, headers=_auth(token))
    resp = client.get(f"/api/v1/tracks/quizzes/{quiz_id}/attempts", headers=_auth(token))
    assert resp.status_code == 200
    assert "correct_answer" not in resp.text
    for attempt in resp.json():
        for entry in attempt["feedback"].values():
            assert "correct_answer" not in entry


def test_stored_feedback_on_the_row_carries_no_answer_key(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    attempt_id = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                             json={"answers": {"0": 1}}, headers=_auth(token)).json()["id"]

    check = SessionLocal()
    try:
        row = check.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).one()
        for entry in row.feedback.values():
            assert "correct_answer" not in entry
    finally:
        check.close()


def test_an_attempt_written_before_the_policy_is_stripped_on_read(client, db):
    """Rows already in production carry `correct_answer` in their stored
    feedback. Nothing rewrites them, so the response model has to be what
    stops the attempts endpoint replaying the key."""
    quiz_id = _seed(_make_mixed_quiz)
    token, user_id = _register_with_id(client)

    setup = SessionLocal()
    try:
        setup.add(QuizAttempt(
            user_id=user_id, quiz_id=quiz_id, answers={"0": 1}, score=100.0, passed=True,
            feedback={"0": {
                "correct": True, "your_answer": 1,
                "correct_answer": 1, "explanation": "because four",
            }},
        ))
        setup.commit()
    finally:
        setup.close()

    resp = client.get(f"/api/v1/tracks/quizzes/{quiz_id}/attempts", headers=_auth(token))
    assert resp.status_code == 200
    assert "correct_answer" not in resp.text
    # The teaching half survives the stripping.
    assert "because four" in resp.text


def test_explanations_and_correctness_remain_available(client, db):
    """The policy withholds the key, not the feedback: a student still
    learns which questions they got wrong and why."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)

    body = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1, "2": 1}},  # first right, second wrong
                       headers=_auth(token)).json()
    assert body["feedback"]["0"]["correct"] is True
    assert body["feedback"]["2"]["correct"] is False
    assert body["feedback"]["0"]["your_answer"] == 1
    assert body["feedback"]["0"]["explanation"] == "..."
    assert body["score"] == 50.0


# ─────────────────────────────────────────────────────────────────────────
# D. Answer payload validation
# ─────────────────────────────────────────────────────────────────────────

def test_numeric_answers_are_accepted(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1, "2": 0}}, headers=_auth(token))
    assert resp.status_code == 200


@pytest.mark.parametrize("value", [
    "1",                    # numeric string — the frontend sends real numbers
    "not-a-number",
    [1, 2],
    {"nested": 1},
    None,
    1.5,
    True,
], ids=["numeric-str", "str", "list", "object", "null", "float", "bool"])
def test_non_integer_answer_values_are_rejected(client, db, value):
    """The answers map is persisted verbatim on the attempt row, so the
    value type is a storage control, not a tidiness one."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": value}}, headers=_auth(token))
    assert resp.status_code == 422, resp.text


def test_more_than_two_hundred_answers_are_rejected(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {str(i): 0 for i in range(201)}}, headers=_auth(token))
    assert resp.status_code == 422


def test_exactly_two_hundred_answers_are_still_accepted(client, db):
    """The bound is a ceiling, not an off-by-one that rejects the limit."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {str(i): 0 for i in range(200)}}, headers=_auth(token))
    assert resp.status_code == 200


def test_a_huge_answer_value_cannot_be_persisted(client, db):
    """max_length on the map only ever bounded the number of keys. A single
    multi-megabyte value used to reach the JSON column untouched."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": "A" * 1_000_000}}, headers=_auth(token))
    assert resp.status_code == 422

    check = SessionLocal()
    try:
        assert check.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).count() == 0
    finally:
        check.close()


def test_a_huge_answer_key_cannot_be_persisted(client, db):
    """The key half of the entry was unbounded for the same reason."""
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"A" * 100_000: 0}}, headers=_auth(token))
    assert resp.status_code == 422


def test_an_out_of_range_answer_index_is_rejected(client, db):
    quiz_id = _seed(_make_mixed_quiz)
    token = _register(client)
    for value in (-1, 10 ** 40):
        resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                           json={"answers": {"0": value}}, headers=_auth(token))
        assert resp.status_code == 422, value


# ─────────────────────────────────────────────────────────────────────────
# E. Malformed authored question content
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", ["just a string", None, 42, ["a", "list"]],
                         ids=["str", "null", "int", "list"])
def test_a_malformed_question_does_not_crash_the_endpoint(client, db, bad):
    """A content bug must not cost a student their submission. The scoring
    loop used to call .get() on whatever was in the blob."""
    quiz_id = _seed(_make_quiz, [
        {"question": "2+2?", "options": ["3", "4"], "correct": 1, "explanation": "..."},
        bad,
    ])
    token = _register(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1}}, headers=_auth(token))
    assert resp.status_code == 200, resp.text
    assert "error_id" not in resp.text


def test_a_malformed_question_is_ungradable_not_a_free_mark(client, db):
    """Excluded from the denominator, exactly like an open question — so
    it neither awards a mark nor costs one."""
    quiz_id = _seed(_make_quiz, [
        {"question": "2+2?", "options": ["3", "4"], "correct": 1, "explanation": "..."},
        "malformed",
    ], passing_score=100)
    token = _register(client)

    body = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1}}, headers=_auth(token)).json()
    assert body["score"] == 100.0          # 1/1 gradable question, not 1/2
    assert body["passed"] is True
    assert body["feedback"]["1"]["skipped"] is True


def test_a_wholly_malformed_questions_blob_does_not_crash(client, db):
    """`questions` is JSON, so it can be an object rather than a list."""
    quiz_id = _seed(_make_quiz, {"not": "a list"})
    token = _register(client)

    resp = client.post(f"/api/v1/tracks/quizzes/{quiz_id}/submit",
                       json={"answers": {"0": 1}}, headers=_auth(token))
    assert resp.status_code == 200, resp.text
    assert resp.json()["score"] == 0
