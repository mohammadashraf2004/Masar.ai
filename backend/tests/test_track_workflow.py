"""The five fixed, backend-owned career-track workflows."""
import json
from pathlib import Path

from app.models.learning import Lesson
from app.models.learning_path import Course
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic
from seeds.curriculum import TRACK_WORKFLOWS
from seeds.sync_curriculum import sync_track_workflow
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register


API = "/api/v1/learning"

EXPECTED = {
    "data-analyst": [
        ("course-013", "core", True),
        ("course-017", "core", True),
        ("course-001", "supporting", False),
    ],
    "ml-engineer": [
        ("course-013", "supporting", False),
        ("course-001", "core", True),
        ("course-018", "supporting", False),
        ("course-002", "core", True),
        ("course-003", "core", True),
        ("course-010", "supporting", True),
        ("course-011", "supporting", True),
        ("course-016", "core", True),
        ("course-004", "optional", False),
        ("course-014", "optional", False),
    ],
    "ai-developer": [
        ("course-001", "supporting", True),
        ("course-002", "supporting", True),
        ("course-003", "supporting", True),
        ("course-004", "core", True),
        ("course-005", "core", True),
        ("course-006", "core", True),
        ("course-010", "core", True),
        ("course-009", "core", True),
        ("course-012", "core", True),
        ("course-007", "core", True),
        ("course-008", "optional", False),
        ("course-015", "optional", False),
    ],
    "mlops-engineer": [
        ("course-013", "supporting", False),
        ("course-001", "core", True),
        ("course-002", "supporting", False),
        ("course-003", "supporting", False),
        ("course-010", "core", True),
        ("course-011", "core", True),
        ("course-016", "core", True),
        ("course-006", "optional", False),
    ],
    "ai-engineer": [
        ("course-013", "supporting", True),
        ("course-017", "supporting", False),
        ("course-001", "core", True),
        ("course-018", "supporting", False),
        ("course-002", "core", True),
        ("course-003", "core", True),
        ("course-004", "core", True),
        ("course-005", "core", True),
        ("course-006", "core", True),
        ("course-010", "supporting", True),
        ("course-011", "core", True),
        ("course-016", "core", True),
        ("course-009", "supporting", True),
        ("course-012", "supporting", True),
        ("course-007", "supporting", True),
        ("course-014", "optional", False),
        ("course-015", "optional", False),
        ("course-008", "optional", False),
    ],
}

AI_SECTIONS = {
    "course-001": "foundations",
    "course-013": "foundations",
    "course-017": "foundations",
    "course-018": "foundations",
    "course-002": "foundations",
    "course-003": "foundations",
    "course-004": "language-generative-ai",
    "course-005": "language-generative-ai",
    "course-010": "application-production",
    "course-006": "application-production",
    "course-011": "application-production",
    "course-016": "application-production",
    "course-007": "advanced-ai-systems",
    "course-009": "advanced-ai-systems",
    "course-012": "advanced-ai-systems",
    "course-008": "specializations",
    "course-014": "specializations",
    "course-015": "specializations",
}


def _workflow(client, goal, headers=None):
    response = client.get(f"{API}/tracks/{goal}/workflow", headers=headers or {})
    assert response.status_code == 200, response.text
    return response.json()


def _publish_one_lesson(db, slug, *, completion_required=True, suffix="test-module"):
    course = db.query(Course).filter(Course.slug == slug).one()
    topic = ToolTopic(
        tool_course_id=course.tool_course_id,
        title=f"{slug} {suffix}",
        slug=f"{slug}-{suffix}",
        order=1,
        estimated_hours=1.0,
        skill_tags=[],
        prerequisite_ids=[],
        completion_required=completion_required,
        is_optional=not completion_required,
    )
    db.add(topic)
    db.flush()
    lesson = Lesson(tool_topic_id=topic.id, title="Test lesson", content="Test", order=1)
    db.add(lesson)
    db.commit()
    return topic, lesson


def test_all_five_tracks_return_only_the_canonical_mapping_in_deterministic_order(
    learn_client, learn_catalog,
):
    for goal, expected in EXPECTED.items():
        first = _workflow(learn_client, goal)
        second = _workflow(learn_client, goal)
        rows = first["courses"]

        assert [(row["slug"], row["role"], row["required"]) for row in rows] == expected
        assert [row["order"] for row in rows] == list(range(1, len(expected) + 1))
        assert len({row["slug"] for row in rows}) == len(rows)
        assert [row["slug"] for row in second["courses"]] == [row["slug"] for row in rows]
        assert all(row["slug"].startswith("course-") for row in rows)


def test_workflow_seed_is_idempotent_and_uses_one_canonical_course_row(
    learn_client, learn_catalog, learn_db,
):
    assert sync_track_workflow(learn_db) == []
    for goal, entries in TRACK_WORKFLOWS.items():
        slugs = [slug for slug, *_ in entries]
        assert len(slugs) == len(set(slugs)), goal
    assert learn_db.query(Course).filter(Course.slug == "course-001").count() == 1


def test_ai_engineer_returns_all_eighteen_courses_in_the_five_named_sections(
    learn_client, learn_catalog,
):
    workflow = _workflow(learn_client, "ai-engineer")
    assert workflow["has_sections"] is True
    assert len(workflow["courses"]) == 18
    assert {row["slug"]: row["section"] for row in workflow["courses"]} == AI_SECTIONS


def test_optional_courses_do_not_enter_required_completion_or_block_core_progression(
    learn_client, learn_catalog,
):
    ml = _workflow(learn_client, "ml-engineer")
    assert ml["required_total"] == 6
    assert ml["required_completed"] == 0
    assert ml["progress_percent"] == 0

    mlops = _workflow(learn_client, "mlops-engineer")
    assert mlops["required_total"] == 4  # 001, 010, 011, 016: deep learning and 006 are optional here
    course_010 = next(row for row in mlops["courses"] if row["slug"] == "course-010")
    # 010 needs only COURSE-001 (no optional course, no LLM course), so it is
    # locked until 001 is done and nothing else.
    assert [row["slug"] for row in course_010["prerequisites"]] == ["course-001"]
    assert course_010["status"] == "locked"


def test_an_optional_course_never_blocks_a_required_one_once_the_real_prerequisite_is_done(
    learn_client, learn_catalog, learn_db,
):
    topic, lesson = _publish_one_lesson(learn_db, "course-001")
    who = register(learn_client)
    learn_db.add(UserProgress(
        user_id=who["id"], tool_topic_id=topic.id, lessons_completed=[lesson.id], exercises_completed=[],
    ))
    learn_db.commit()

    mlops = _workflow(learn_client, "mlops-engineer", who["headers"])
    by_slug = {row["slug"]: row for row in mlops["courses"]}
    assert by_slug["course-001"]["status"] == "completed"
    # Optional 002/003 are untouched, yet required 010 is no longer locked.
    assert by_slug["course-002"]["status"] != "completed"
    assert by_slug["course-010"]["status"] == "available"
    assert by_slug["course-016"]["status"] == "available"  # needs COURSE-001 only


def test_partial_course_progress_does_not_count_as_a_completed_required_course(
    learn_client, learn_catalog, learn_db,
):
    topic, first_lesson = _publish_one_lesson(learn_db, "course-001")
    learn_db.add(Lesson(tool_topic_id=topic.id, title="Second lesson", content="Test", order=2))
    who = register(learn_client)
    learn_db.add(UserProgress(
        user_id=who["id"], tool_topic_id=topic.id,
        lessons_completed=[first_lesson.id], exercises_completed=[],
    ))
    learn_db.commit()

    workflow = _workflow(learn_client, "ml-engineer", who["headers"])
    course_001 = next(row for row in workflow["courses"] if row["slug"] == "course-001")
    assert course_001["status"] == "in_progress"
    assert course_001["progress_percent"] == 50
    assert workflow["required_completed"] == 0
    assert workflow["progress_percent"] == 0


def test_track_order_does_not_create_prerequisites(
    learn_client, learn_catalog,
):
    workflow = _workflow(learn_client, "ml-engineer")
    course_002 = next(row for row in workflow["courses"] if row["slug"] == "course-002")
    course_001 = next(row for row in workflow["courses"] if row["slug"] == "course-001")
    # 013 is placed first (001 recommends it) without becoming a prerequisite of anything.
    assert workflow["courses"][0]["slug"] == "course-013"
    assert [row["slug"] for row in course_001["prerequisites"]] == []
    assert [row["slug"] for row in course_002["prerequisites"]] == ["course-001"]
    assert "course-013" not in {row["slug"] for row in course_002["prerequisites"]}


def test_shared_progress_and_external_prerequisite_completion_are_reused_across_tracks(
    learn_client, learn_catalog, learn_db,
):
    course_001_topic, course_001_lesson = _publish_one_lesson(learn_db, "course-001")
    course_003_topic, course_003_lesson = _publish_one_lesson(learn_db, "course-003")
    who = register(learn_client)

    before = _workflow(learn_client, "ai-developer", who["headers"])
    assert next(row for row in before["courses"] if row["slug"] == "course-004")["status"] == "locked"

    learn_db.add_all([
        UserProgress(
            user_id=who["id"], tool_topic_id=course_001_topic.id,
            lessons_completed=[course_001_lesson.id], exercises_completed=[],
        ),
        UserProgress(
            user_id=who["id"], tool_topic_id=course_003_topic.id,
            lessons_completed=[course_003_lesson.id], exercises_completed=[],
        ),
    ])
    learn_db.commit()

    for goal in ("data-analyst", "ml-engineer", "ai-developer", "mlops-engineer", "ai-engineer"):
        workflow = _workflow(learn_client, goal, who["headers"])
        course_001 = next(row for row in workflow["courses"] if row["slug"] == "course-001")
        assert course_001["status"] == "completed"
        assert course_001["progress_percent"] == 100

    after = _workflow(learn_client, "ai-developer", who["headers"])
    assert next(row for row in after["courses"] if row["slug"] == "course-004")["status"] == "available"


def test_course_016_has_unique_lesson_ids_and_no_stale_optional_kubernetes_policy():
    manifest_path = (
        Path(__file__).parents[1]
        / "courses/COURSE-016_Machine_Learning_Systems_and_MLOps_Engineering/course_manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "completion_policy" not in manifest  # the Kubernetes-supplemental chapters are no longer in this course

    from app.services.curriculum.loaders import load_course_dir

    spec = load_course_dir(manifest_path.parent)
    lesson_ids = [lesson.lesson_id for lesson in spec.lessons]
    assert len(lesson_ids) == len(set(lesson_ids)) == manifest["lessons"] == 17
    assert [module.module_id for module in spec.modules if module.optional] == []
    # The infrastructure module holds two lessons: M10.L01 (chapter 10, infrastructure) and M10.L02 (chapter 11, people and responsible ML).
    assert [len(m.lessons) for m in spec.modules if m.module_id == "M016-10"] == [2]


def test_course_016_optional_kubernetes_lessons_do_not_enter_course_or_track_completion(
    learn_client, learn_catalog, learn_db,
):
    required_topic, required_lesson = _publish_one_lesson(
        learn_db, "course-016", completion_required=True, suffix="required-test-module",
    )
    _publish_one_lesson(
        learn_db, "course-016", completion_required=False, suffix="optional-kubernetes-test-module",
    )
    who = register(learn_client)
    learn_db.add(UserProgress(
        user_id=who["id"], tool_topic_id=required_topic.id,
        lessons_completed=[required_lesson.id], exercises_completed=[],
    ))
    learn_db.commit()

    workflow = _workflow(learn_client, "mlops-engineer", who["headers"])
    course_016 = next(row for row in workflow["courses"] if row["slug"] == "course-016")
    assert course_016["status"] == "completed"
    assert course_016["progress_percent"] == 100
