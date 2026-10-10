"""End-to-end grading flow through the HTTP API (2026-10-10 grading audit).

Real submissions run through the production driver and runner harness on the
development execution backend. Covers: Run never completes an exercise, one
pass completes it exactly once, a crash still gets the explaining feedback,
answer-revealing feedback waits for a second different attempt, grader
faults never count against the learner, concurrent completions keep each
other, written exercises complete only on an accepted answer, and a code pass
refreshes the tool course's progress.
"""
import threading
import time
import uuid

import pytest

from app.controllers import answer_evaluation_controller
from app.db.session import SessionLocal
from app.models.code_exercise import CodeExerciseAttempt
from app.models.learning import CareerTrack, DifficultyLevel, Exercise, Topic, TrackLevel
from app.models.progress import UserProgress
from app.models.tool_course import ToolCourse, ToolCourseCompletion, ToolEnrollment, ToolTopic
from app.services.curriculum.guided import Guided, build, eq, registry
from app.services.exercise_progress import mark_complete
from tests.conftest import verify_registered

PASSWORD = "correct-horse-battery-staple-7"
DIVIDE = build("COURSE-015.M01.L01.EX01", registry()["COURSE-015.M01.L01.EX01"])


def _register(client, *, verified=False):
    response = client.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True,
        "email": f"grading-flow-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Grading Flow", "password": PASSWORD,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    if verified:
        verify_registered(client, body["user"]["id"])
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def topic(db):
    track = CareerTrack(slug=f"grading-{uuid.uuid4().hex[:8]}", title="Grading", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Level", order=1)
    db.add(level)
    db.flush()
    topic = Topic(
        level_id=level.id, title="Grading", slug=f"grading-{uuid.uuid4().hex[:8]}", order=1,
        difficulty=DifficultyLevel.beginner, estimated_hours=1, prerequisite_ids=[], skill_tags=[],
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def _exercise(db, topic, fields, **overrides):
    values = {
        "topic_id": topic.id, "title": "Exercise", "description": fields.get("description", "Do it."),
        "exercise_type": "code", "language": fields["language"], "starter_code": fields["starter_code"],
        "solution_code": fields["solution_code"], "grading_tests": fields["tests"],
        "hint": fields.get("hint"), "success_message": fields.get("success_message"),
        "success_message_ar": fields.get("success_message_ar"), "skill_tested": ["python"],
    }
    values.update(overrides)
    exercise = Exercise(**values)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@pytest.fixture()
def divide(db, topic):
    return _exercise(db, topic, DIVIDE)


SCORES = build("TEST.SCORES", Guided(
    goal=("Add up the scores.", "اجمع الدرجات."),
    steps=(("Fill the blank with the total.", "املأ الفراغ بالمجموع."),),
    starter="scores = [3, 4, 5]\ntotal = ___\n",
    answers=("sum(scores)",),
    hints=(("Python has a built-in for this.", "في Python دالة جاهزة لذلك."),),
    success=("Correct.", "صحيح."),
    # This message quotes the answer, as 425 messages in the curriculum do.
    checks=(eq("total", 12, "Blank 1: `sum(scores)` adds them up.", "الفراغ 1: يجمعها `sum(scores)`."),),
))


@pytest.fixture()
def scores(db, topic):
    return _exercise(db, topic, SCORES)


def _submit(client, headers, exercise, code, language="en"):
    response = client.post(f"/api/v1/practice/exercises/{exercise.id}/submit", headers=headers,
                           json={"code": code, "language": language})
    assert response.status_code == 200, response.text
    return response.json()


def _completed(db, user_id):
    db.expire_all()
    rows = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return rows, [item for row in rows for item in (row.exercises_completed or [])]


def test_run_never_completes_and_one_pass_completes_exactly_once(client, db, divide):
    user_id, headers = _register(client)
    run = client.post(f"/api/v1/practice/exercises/{divide.id}/run", headers=headers,
                      json={"code": DIVIDE["solution_code"]})
    assert run.status_code == 200 and run.json()["status"] == "success"
    assert _completed(db, user_id) == ([], [])

    wrong = DIVIDE["solution_code"].replace('{"result": a / b}', '{"result": 2.5}')
    assert _submit(client, headers, divide, wrong)["passed"] is False
    assert _completed(db, user_id) == ([], [])

    for _ in range(2):
        result = _submit(client, headers, divide, DIVIDE["solution_code"])
        assert result["passed"] and result["status"] == "correct"
        assert result["tests_passed"] == result["tests_total"] == 6
    rows, completed = _completed(db, user_id)
    assert len(rows) == 1 and completed == [divide.id]
    actions = [a for (a,) in db.query(CodeExerciseAttempt.action).filter(CodeExerciseAttempt.user_id == user_id)]
    assert actions.count("run") == 1 and actions.count("submit") == 3


@pytest.mark.parametrize("language, explanation, crash", [
    ("en", "does not handle a zero divisor safely", "ZeroDivisionError"),
    ("ar", "لا تتعامل `divide` بأمان مع مقسوم عليه يساوي صفرًا", "ZeroDivisionError"),
])
def test_a_crash_gets_the_explaining_feedback_then_the_crash(client, divide, language, explanation, crash):
    _, headers = _register(client)
    code = DIVIDE["solution_code"].replace("if b == 0:", "if a == 0:")
    result = _submit(client, headers, divide, code, language)
    assert (result["status"], result["passed"], result["failed_test"]) == ("runtime_error", False, "check_2")
    message = result["feedback"]["message"]
    assert explanation in message and crash in message
    assert message.index(explanation) < message.index(crash)
    assert "Traceback" in result["stderr"]  # the technical detail stays in the console


def test_answer_revealing_feedback_waits_for_a_second_different_attempt(client, scores):
    _, headers = _register(client)
    first = _submit(client, headers, scores, "scores = [3, 4, 5]\ntotal = max(scores)\n")
    assert first["feedback"]["withheld"] is True
    assert first["feedback"]["message"].startswith("Blank 1 ") and "sum(scores)" not in first["feedback"]["message"]
    assert "sum(scores)" not in first["feedback"]["messages"]["ar"]

    again = _submit(client, headers, scores, "scores = [3, 4, 5]\ntotal = max(scores)\n")
    assert again["feedback"]["withheld"] is True  # the same answer again is not a new attempt

    second = _submit(client, headers, scores, "scores = [3, 4, 5]\ntotal = min(scores)\n", "ar")
    assert second["feedback"]["withheld"] is False
    assert second["feedback"]["message"] == "الفراغ 1: يجمعها `sum(scores)`."


def test_grader_faults_are_never_counted_against_the_learner(client, db, topic):
    _, headers = _register(client)
    broken = _exercise(db, topic, dict(SCORES, tests=[{"id": "x", "type": "value_equal", "variable": "total", "expected": 12}]))
    for answer in ("sum(scores)", "max(scores)", "min(scores)", "len(scores)"):
        result = _submit(client, headers, broken, f"scores = [3, 4, 5]\ntotal = {answer}\n")
        assert (result["status"], result["passed"]) == ("grading_error", False)
        assert "not counted" in result["feedback"]["message"]
    state = client.get(f"/api/v1/practice/exercises/{broken.id}/progress", headers=headers).json()
    assert (state["failed_checks"], state["solution_available"]) == (0, False)


def test_concurrent_completions_in_one_topic_keep_each_other(client, db, topic, divide, scores):
    """Two completions for the same learner and topic, each in its own
    transaction: the second waits for the first, then adds to its row."""
    user_id, _ = _register(client)
    first, second = SessionLocal(), SessionLocal()
    try:
        mark_complete(first, user_id, first.get(Exercise, divide.id))
        finished = threading.Event()

        def complete_second():
            mark_complete(second, user_id, second.get(Exercise, scores.id))
            second.commit()
            finished.set()

        worker = threading.Thread(target=complete_second)
        worker.start()
        time.sleep(0.5)
        assert not finished.is_set(), "the second completion must wait for the first transaction"
        first.commit()
        worker.join(timeout=10)
        assert finished.is_set()
    finally:
        first.close()
        second.close()
    rows, completed = _completed(db, user_id)
    assert len(rows) == 1 and sorted(completed) == sorted([divide.id, scores.id])


@pytest.fixture()
def written(db, topic):
    exercise = Exercise(
        topic_id=topic.id, title="Explain recursion", description="Explain recursion in two sentences.",
        skill_tested=["python"],
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def test_a_written_exercise_completes_only_on_an_accepted_answer(client, db, topic, written, monkeypatch):
    user_id, headers = _register(client, verified=True)
    progress = f"/api/v1/tracks/topics/{topic.id}/progress"
    forged = client.post(progress, headers=headers, json={"exercise_id": written.id})
    assert forged.status_code == 409 and forged.json()["detail"]["code"] == "ANSWER_NOT_ACCEPTED_YET"
    assert _completed(db, user_id) == ([], [])

    verdicts = iter([False, True])
    monkeypatch.setattr(answer_evaluation_controller, "get_llm", lambda: object())
    monkeypatch.setattr(answer_evaluation_controller.answer_evaluator_service, "evaluate_answer",
                        lambda **_: (lambda ok: {"reply": "Verdict.", "is_correct": ok, "score": 100.0 if ok else 40.0})(next(verdicts)))
    answer = f"/api/v1/practice/exercises/{written.id}/answer"
    rejected = client.post(answer, headers=headers, json={"content": "It loops.", "language": "en"})
    assert rejected.status_code == 200 and rejected.json()["is_correct"] is False
    assert _completed(db, user_id) == ([], [])
    accepted = client.post(answer, headers=headers, json={"content": "A function that calls itself on a smaller case.", "language": "en"})
    assert accepted.status_code == 200 and accepted.json()["is_correct"] is True
    # Recorded by the server at the verdict, not by a later browser request.
    assert _completed(db, user_id)[1] == [written.id]
    assert client.post(progress, headers=headers, json={"exercise_id": written.id}).status_code == 200
    assert _completed(db, user_id)[1] == [written.id]


def test_a_code_pass_refreshes_the_tool_course_progress(client, db):
    user_id, headers = _register(client)
    course = ToolCourse(slug=f"grading-tool-{uuid.uuid4().hex[:8]}", title="Tool")
    db.add(course)
    db.flush()
    tool_topic = ToolTopic(tool_course_id=course.id, title="Only topic", slug="only", order=1)
    db.add(tool_topic)
    db.flush()
    exercise = Exercise(
        tool_topic_id=tool_topic.id, title="Scores", description="Add them up.", exercise_type="code",
        language="python", starter_code=SCORES["starter_code"], solution_code=SCORES["solution_code"],
        grading_tests=SCORES["tests"], skill_tested=["python"],
    )
    db.add_all([exercise, ToolEnrollment(user_id=user_id, tool_course_id=course.id)])
    db.commit()
    try:
        assert _submit(client, headers, exercise, SCORES["solution_code"])["passed"]
        db.expire_all()
        enrollment = db.query(ToolEnrollment).filter(ToolEnrollment.user_id == user_id).one()
        assert enrollment.progress_pct == 100.0 and enrollment.completed_at is not None
    finally:
        # Other suites count tool enrollments across the whole database.
        db.rollback()
        for model, column, value in (
            (ToolCourseCompletion, ToolCourseCompletion.tool_course_id, course.id),
            (ToolEnrollment, ToolEnrollment.tool_course_id, course.id),
            (CodeExerciseAttempt, CodeExerciseAttempt.exercise_id, exercise.id),
            (UserProgress, UserProgress.tool_topic_id, tool_topic.id),
            (Exercise, Exercise.id, exercise.id),
            (ToolTopic, ToolTopic.id, tool_topic.id),
            (ToolCourse, ToolCourse.id, course.id),
        ):
            db.query(model).filter(column == value).delete(synchronize_session=False)
        db.commit()
