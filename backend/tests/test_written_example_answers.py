"""Example answers for written exercises (curriculum/examples, migration 040).

The example opens only after the learner's first evaluated answer, follows
the interface language, is the evaluator's reference, and never exists for a
code exercise (those have their worked solution).
"""
import uuid

import pytest

from app.controllers import answer_evaluation_controller
from app.models.learning import CareerTrack, DifficultyLevel, Exercise, Topic, TrackLevel
from app.services.curriculum.examples import example_problems, registry
from app.services.curriculum.loaders import load_all_courses
from tests.conftest import verify_registered

PASSWORD = "correct-horse-battery-staple-7"
EXAMPLE_EN = "Recursion solves a problem by calling the same function on a smaller case until a base case stops it."
EXAMPLE_AR = "العودية تحل المشكلة باستدعاء الدالة نفسها على حالة أصغر حتى توقفها حالة أساسية."


def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True,
        "email": f"example-{uuid.uuid4().hex[:12]}@example.com", "full_name": "Example", "password": PASSWORD,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    verify_registered(client, body["user"]["id"])
    return {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def written(db):
    track = CareerTrack(slug=f"example-{uuid.uuid4().hex[:8]}", title="Examples", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Level", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title="T", slug=f"t-{uuid.uuid4().hex[:8]}", order=1,
                  difficulty=DifficultyLevel.beginner, estimated_hours=1, prerequisite_ids=[], skill_tags=[])
    db.add(topic)
    db.flush()
    exercise = Exercise(topic_id=topic.id, title="Explain recursion", description="Explain recursion.",
                        skill_tested=["python"], example_answer=EXAMPLE_EN, example_answer_ar=EXAMPLE_AR)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@pytest.fixture()
def evaluator(monkeypatch):
    seen = []

    def evaluate(**kwargs):
        seen.append(kwargs)
        return {"reply": "Not yet: what stops it?", "is_correct": False, "score": 40.0}

    monkeypatch.setattr(answer_evaluation_controller, "get_llm", lambda: object())
    monkeypatch.setattr(answer_evaluation_controller.answer_evaluator_service, "evaluate_answer", evaluate)
    return seen


def test_the_example_opens_only_after_a_first_evaluated_answer(client, written, evaluator):
    headers = _register(client)
    example = f"/api/v1/practice/exercises/{written.id}/example"
    locked = client.get(example, headers=headers)
    assert locked.status_code == 403 and locked.json()["detail"]["code"] == "EXAMPLE_LOCKED"

    answered = client.post(f"/api/v1/practice/exercises/{written.id}/answer", headers=headers,
                           json={"content": "It calls itself.", "language": "ar"})
    assert answered.status_code == 200 and answered.json()["example_available"] is True
    assert client.get(f"/api/v1/practice/exercises/{written.id}/answer", headers=headers).json()["example_available"] is True

    opened = client.get(example, headers=headers)
    assert opened.status_code == 200
    assert opened.json() == {"example_answer": EXAMPLE_EN, "example_answer_ar": EXAMPLE_AR}
    # The evaluator graded against the example, in the learner's language.
    assert evaluator[0]["context"]["reference"] == EXAMPLE_AR


def test_no_example_and_code_exercises_are_refused(client, db, written):
    headers = _register(client)
    written.example_answer = None
    code = Exercise(topic_id=written.topic_id, title="Code", description="Code.", exercise_type="code",
                    language="python", starter_code="x = ___\n", solution_code="x = 1\n",
                    grading_tests=[{"type": "value_equals", "variable": "x", "expected": 1, "feedback": "x"}],
                    skill_tested=[])
    db.add(code)
    db.commit()
    assert client.get(f"/api/v1/practice/exercises/{written.id}/example", headers=headers).status_code == 404
    assert client.get(f"/api/v1/practice/exercises/{code.id}/example", headers=headers).status_code == 409


def test_example_definitions_are_validated():
    assert example_problems("X", ("short", "قصير")) != []
    assert any("no Arabic" in problem for problem in example_problems("X", (EXAMPLE_EN, EXAMPLE_EN)))
    assert example_problems("X", (EXAMPLE_EN, EXAMPLE_AR)) == []


def test_every_example_lands_on_a_written_exercise_and_is_valid():
    examples = registry()
    written = {
        exercise.exercise_id: exercise
        for course in load_all_courses() for lesson in course.lessons for exercise in lesson.exercises
        if exercise.exercise_type != "code"
    }
    assert set(examples) <= set(written), sorted(set(examples) - set(written))[:10]
    for exercise_id, example in examples.items():
        assert example_problems(exercise_id, example) == []
        assert written[exercise_id].example_answer == example[0].strip()
        assert written[exercise_id].example_answer_ar == example[1].strip()


def test_every_written_exercise_of_a_completed_course_has_an_example_answer():
    from app.services.curriculum.examples import COMPLETE_COURSES

    courses = {course.course_id: course for course in load_all_courses()}
    assert COMPLETE_COURSES <= set(courses)
    missing = sorted(
        exercise.exercise_id
        for course_id in COMPLETE_COURSES for lesson in courses[course_id].lessons for exercise in lesson.exercises
        if exercise.exercise_type != "code" and not exercise.example_answer
    )
    assert missing == [], f"{len(missing)} written exercises have no example answer, e.g. {missing[:5]}"
