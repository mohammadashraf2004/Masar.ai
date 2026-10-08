"""
Every endpoint that serializes a paid course's topics hides locked content the same way
(audit finding #8: the /tracks copy of the redaction had fallen behind and leaked hints).

Real catalogue courses, a learner without access, and secret markers planted in every field a
locked exercise, project or quiz must not reveal - checked against the raw response bodies of
/tracks/{slug}, /tracks/topics/{id}, /tool-courses/{slug} and /tool-courses/topics/{id}.
"""
import pytest

from app.models.learning import Exercise, Project, Quiz
from app.services.learning.catalog_service import load_catalog_bundle
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

SECRETS = ("HINT-SECRET-EN", "HINT-SECRET-AR", "STARTER-SECRET", "DESC-SECRET", "DESC-AR-SECRET",
           "OBJECTIVE-SECRET", "RUBRIC-SECRET", "REPO-SECRET", "QUESTION-SECRET", "SUCCESS-SECRET")


def _plant(db, *, topic_id=None, tool_topic_id=None, key="LOCKED-TEST"):
    owner = {"topic_id": topic_id} if topic_id else {"tool_topic_id": tool_topic_id}
    exercise = Exercise(**owner, source_key=f"{key}/L099/x1", title="Locked exercise",
                        description="DESC-SECRET", description_ar="DESC-AR-SECRET", starter_code="STARTER-SECRET",
                        hint="HINT-SECRET-EN", hint_ar="HINT-SECRET-AR", success_message="SUCCESS-SECRET",
                        exercise_type="code", language="python", grading_tests=[{"id": "t", "type": "variable_exists"}])
    project = Project(**owner, title="Locked project", description="DESC-SECRET", objectives=["OBJECTIVE-SECRET"],
                      rubric={"RUBRIC-SECRET": 1}, starter_repo_url="https://example.com/REPO-SECRET",
                      tech_stack=["python"])
    quiz = Quiz(**owner, source_key=f"{key}/L099/quiz", title="Locked quiz",
                questions=[{"question": "QUESTION-SECRET", "options": ["a", "b"], "correct": 0}])
    db.add_all([exercise, project, quiz])
    db.commit()
    return exercise, project, quiz


def _assert_locked(body: str, payload_items: dict, planted) -> None:
    for secret in SECRETS:
        assert secret not in body, secret
    exercise, project, quiz = planted
    for item in (payload_items["exercises"][exercise.id], payload_items["projects"][project.id],
                 payload_items["quizzes"][quiz.id]):
        assert item["is_locked"] is True and item["course_slug"]
    assert payload_items["exercises"][exercise.id]["title"] == "Locked exercise"  # catalogue metadata stays


def _items(topics):
    out = {"exercises": {}, "projects": {}, "quizzes": {}}
    for topic in topics:
        for kind in out:
            out[kind].update({item["id"]: item for item in topic[kind]})
    return out


@pytest.fixture()
def bundle(learn_db, learn_catalog):
    return load_catalog_bundle(learn_db)


def test_tool_course_endpoints_hide_every_locked_field(learn_client, learn_db, bundle):
    who = register(learn_client)
    course = next(c for c in bundle.courses.values() if c.tool_course_id and bundle.catalog.courses[c.id].is_available)
    topic = course.tool_course.topics[0]
    planted = _plant(learn_db, tool_topic_id=topic.id)

    whole = learn_client.get(f"/api/v1/tool-courses/{course.tool_course.slug}", headers=who["headers"])
    assert whole.status_code == 200, whole.text
    _assert_locked(whole.text, _items(whole.json()["topics"]), planted)

    one = learn_client.get(f"/api/v1/tool-courses/topics/{topic.id}", headers=who["headers"])
    assert one.status_code == 200, one.text
    _assert_locked(one.text, _items([one.json()]), planted)


def test_track_endpoints_hide_every_locked_field(learn_client, learn_db, bundle):
    who = register(learn_client)
    course = next(c for c in bundle.courses.values() if c.track_level_id)
    level = course.track_level
    topic = level.topics[0]
    planted = _plant(learn_db, topic_id=topic.id, key="LOCKED-TRACK")

    whole = learn_client.get(f"/api/v1/tracks/{level.track.slug}", headers=who["headers"])
    assert whole.status_code == 200, whole.text
    level_body = next(l for l in whole.json()["levels"] if l["id"] == level.id)
    _assert_locked(whole.text, _items(level_body["topics"]), planted)

    one = learn_client.get(f"/api/v1/tracks/topics/{topic.id}", headers=who["headers"])
    assert one.status_code == 200, one.text
    _assert_locked(one.text, _items([one.json()]), planted)


def test_a_learner_with_access_still_sees_everything(learn_client, learn_db, bundle):
    """Control: the same planted content is fully visible to an account with access (admins
    always have it), so the checks above test redaction, not missing data."""
    from tests.learning_fixtures import make_admin

    who = register(learn_client)
    make_admin(learn_db, who["id"])
    course = next(c for c in bundle.courses.values() if c.tool_course_id and bundle.catalog.courses[c.id].is_available)
    topic = course.tool_course.topics[0]
    exercise, _, _ = _plant(learn_db, tool_topic_id=topic.id, key="OPEN-TEST")
    one = learn_client.get(f"/api/v1/tool-courses/topics/{topic.id}", headers=who["headers"])
    assert one.status_code == 200, one.text
    item = {e["id"]: e for e in one.json()["exercises"]}[exercise.id]
    assert item["is_locked"] is False and item["hint"] == "HINT-SECRET-EN"
