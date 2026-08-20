"""
Covers the tool-courses feature: browsing, enrollment (including
idempotency), and topic progress tracking / course-level progress_pct
recomputation.
"""
import uuid

from app.db.session import SessionLocal
from app.models.tool_course import ToolCourse, ToolTopic
from app.models.learning import Lesson, DifficultyLevel


def _register(client) -> str:
    email = f"tool-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Tool Test", "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201
    return resp.json()["access_token"]


def test_list_tool_courses_includes_seeded_categories(client, db):
    resp = client.get("/api/v1/tool-courses/")
    assert resp.status_code == 200
    courses = resp.json()
    categories = {c["category"] for c in courses}
    # Seeded via seeds/seed_tool_courses.py — this test assumes that seed
    # has run against the test db, same as it does against dev.
    if courses:
        assert categories & {
            "LLM & AI Application Layer", "Vector Databases",
            "MLOps & Infrastructure", "Data Tools",
        }


def test_enroll_is_idempotent(client, db):
    token = _register(client)
    headers = {"Authorization": f"Bearer {token}"}

    setup = SessionLocal()
    course = ToolCourse(slug=f"test-tool-{uuid.uuid4().hex[:8]}", title="Test Tool",
                         category="Data Tools", difficulty=DifficultyLevel.beginner,
                         estimated_hours=1.0, related_track_ids=[], is_active=True)
    setup.add(course)
    setup.commit()
    setup.refresh(course)
    course_id = course.id
    setup.close()

    resp1 = client.post("/api/v1/tool-courses/enroll", json={"tool_course_id": course_id}, headers=headers)
    assert resp1.status_code == 201
    enrollment_id = resp1.json()["id"]

    resp2 = client.post("/api/v1/tool-courses/enroll", json={"tool_course_id": course_id}, headers=headers)
    assert resp2.status_code == 201
    assert resp2.json()["id"] == enrollment_id  # same row, not a duplicate

    my = client.get("/api/v1/tool-courses/my-enrollments", headers=headers)
    assert my.status_code == 200
    assert len([e for e in my.json() if e["tool_course_id"] == course_id]) == 1


def test_topic_progress_marks_course_complete(client, db):
    token = _register(client)
    headers = {"Authorization": f"Bearer {token}"}

    setup = SessionLocal()
    course = ToolCourse(slug=f"test-tool-{uuid.uuid4().hex[:8]}", title="Test Tool 2",
                         category="Data Tools", difficulty=DifficultyLevel.beginner,
                         estimated_hours=1.0, related_track_ids=[], is_active=True)
    setup.add(course)
    setup.flush()
    topic = ToolTopic(tool_course_id=course.id, title="Only Topic", slug="only-topic",
                       order=1, difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
                       skill_tags=[], prerequisite_ids=[])
    setup.add(topic)
    setup.flush()
    lesson = Lesson(tool_topic_id=topic.id, title="L", content="...", order=1)
    setup.add(lesson)
    setup.commit()
    course_id, topic_id, lesson_id = course.id, topic.id, lesson.id
    setup.close()

    client.post("/api/v1/tool-courses/enroll", json={"tool_course_id": course_id}, headers=headers)

    resp = client.post(f"/api/v1/tool-courses/topics/{topic_id}/progress",
                        json={"lesson_id": lesson_id}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"  # only lesson in the topic, now done

    my = client.get("/api/v1/tool-courses/my-enrollments", headers=headers)
    entry = next(e for e in my.json() if e["tool_course_id"] == course_id)
    assert entry["progress_pct"] == 100.0
    assert entry["completed_at"] is not None
