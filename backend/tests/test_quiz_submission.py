"""
Regression test for a real bug found while adding quiz-taking UI: a quiz
mixing MCQ and open-ended ("type": "open") questions used to score the
open questions as if they were MCQ — since an open question has no
"correct" index and the client doesn't submit a numeric answer for it
either, `None == None` silently counted it as correct.
"""
import uuid

from app.db.session import SessionLocal
from app.models.learning import Topic, TrackLevel, CareerTrack, Quiz, DifficultyLevel


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
