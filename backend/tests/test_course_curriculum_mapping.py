from pathlib import Path

import pytest

from app.models.learning import DifficultyLevel, Topic, TrackLevel
from app.models.learning_path import (
    COURSE_KIND_TOOL,
    COURSE_KIND_TRACK_LEVEL,
    COURSE_ROLE_RELATIONS,
    Course,
    CoursePrerequisite,
    CourseRole,
    CourseSkill,
    LearningPath,
    PathStage,
    PathStageCourse,
    PathTemplate,
    PathTemplateStage,
)
from app.models.progress import Enrollment, UserProgress
from app.services.learning.learning_service import LearningValidationError
from app.services.learning.prerequisites import find_cycle, topological_order
from app.services.curriculum.loaders import read_manifest_prerequisites
from seeds import curriculum as cfg
from seeds.seed_learning_paths import PREREQUISITES, SKILLS, seed_learning_catalog
from tests.learning_fixtures import (
    complete_level,
    create_content_sources,
    learn_catalog,
    learn_client,
    learn_db,
    logs_enabled,
    register,
)

API = "/api/v1/learning"


def _catalogue_counts(db):
    """The tables the curriculum seed/sync is allowed to manage."""
    return {
        "courses": db.query(Course).count(),
        "course_roles": db.query(CourseRole).count(),
        "course_skills": db.query(CourseSkill).count(),
        "course_prerequisites": db.query(CoursePrerequisite).count(),
        "path_stages": db.query(PathStage).count(),
        "path_stage_courses": db.query(PathStageCourse).count(),
        "path_templates": db.query(PathTemplate).count(),
        "path_template_stages": db.query(PathTemplateStage).count(),
        "learning_paths": db.query(LearningPath).count(),
    }


def test_course_directory_registry_covers_stable_ids_and_supported_metadata():
    courses = cfg.COURSE_DIRECTORY_COURSES
    assert [course["course_id"] for course in courses] == [f"COURSE-{n:03d}" for n in range(1, 15)]
    assert len({course["slug"] for course in courses}) == 14
    assert {course["slug"] for course in courses} <= set(cfg.COURSE_ROLES)
    assert {course["track"] for course in courses} <= set(cfg.GOALS)

    known_fields = {"data", "machine-learning", "nlp", "computer-vision", "speech", "multimodal"}
    known_skills = {slug for slug, _ in SKILLS}
    known_levels = {"beginner", "intermediate", "advanced"}
    for course in courses:
        assert course["title"]
        assert course["track"] in course["roles"]
        assert set(course["roles"]) <= set(cfg.GOALS)
        assert set(course["roles"].values()) <= set(COURSE_ROLE_RELATIONS)
        assert course["level"] in known_levels
        assert set(course["fields"]) <= known_fields
        assert set(course["skills"]) <= known_skills
        assert course["path_field"] is None or course["path_field"] in known_fields


def test_course_directory_ids_match_the_14_curriculum_sources():
    courses_root = Path(__file__).resolve().parents[1] / "courses"
    source_ids = {directory.name[:10] for directory in courses_root.iterdir() if directory.is_dir()}
    registry_ids = {course["course_id"] for course in cfg.COURSE_DIRECTORY_COURSES}
    assert registry_ids == source_ids == {f"COURSE-{n:03d}" for n in range(1, 15)}


def test_course_directory_prerequisites_are_known_and_acyclic():
    courses = cfg.COURSE_DIRECTORY_COURSES
    slugs = {course["slug"] for course in courses}
    edges = {course["slug"]: course["prerequisites"] for course in courses}
    assert all(set(prerequisites) <= slugs for prerequisites in edges.values())
    assert not find_cycle(edges)


def test_course_directory_topological_order_places_every_prerequisite_first():
    courses = cfg.COURSE_DIRECTORY_COURSES
    edges = {course["slug"]: course["prerequisites"] for course in courses}
    order = topological_order([course["slug"] for course in courses], edges)
    position = {slug: index for index, slug in enumerate(order)}

    assert set(order) == set(edges)
    assert all(position[prerequisite] < position[slug]
               for slug, prerequisites in edges.items() for prerequisite in prerequisites)


def test_each_course_has_a_primary_track_path_or_documented_deferral():
    placed = {
        goal: set(cfg.template_courses(goal))
        for goal in cfg.GOALS
    }
    for course in cfg.COURSE_DIRECTORY_COURSES:
        slug, goal = course["slug"], course["track"]
        deferred = cfg.DEFERRED_PLACEMENTS.get(goal, {})
        assert slug in placed[goal] or slug in deferred, (course["course_id"], goal)


def test_primary_track_sequences_put_hard_prerequisites_first():
    for course in cfg.COURSE_DIRECTORY_COURSES:
        sequence = cfg.template_courses(course["track"])
        position = {slug: index for index, slug in enumerate(sequence)}
        assert course["slug"] in position
        for prerequisite in course["prerequisites"]:
            assert position[prerequisite] < position[course["slug"]]


def test_no_course_directory_stage_points_to_a_missing_curriculum_source():
    directory_slugs = {course["slug"] for course in cfg.COURSE_DIRECTORY_COURSES}
    configured_directory_slugs = {
        course_slug
        for _stage, _title, _title_ar, _phase, _kind, course_slugs in cfg.STAGES
        for course_slug in course_slugs
        if course_slug.startswith("course-")
    }
    assert configured_directory_slugs <= directory_slugs


def test_existing_database_sync_is_idempotent_for_directory_courses(learn_db, learn_catalog):
    from seeds.sync_curriculum import sync_curriculum

    assert sync_curriculum(learn_db, dry_run=True) == []


def test_empty_database_normal_seed_bootstrap_has_exact_curriculum_shape_and_sync_is_idempotent(learn_db):
    """Exercise the supported fresh-install order: content sources, then seed.

    The reference vocabulary is provided by migrations in the test database;
    no catalogue row, association row, or constraint is hand-created here.
    """
    create_content_sources(learn_db)
    created = seed_learning_catalog(learn_db)
    first_counts = _catalogue_counts(learn_db)

    assert created["courses"] == 50
    assert first_counts["courses"] == 50
    assert first_counts["course_roles"] == sum(len(roles) for roles in cfg.COURSE_ROLES.values())
    # Required prerequisites come from the registry; each directory course also gets the
    # other courses its own manifest names, as *recommended* ones (advice, never read by
    # the path generator).
    recommended = 0
    for course in cfg.COURSE_DIRECTORY_COURSES:
        named = {c.lower() for c, _ in read_manifest_prerequisites(course["course_id"])}
        recommended += len(named - set(course["prerequisites"]) - {course["slug"]})
    assert first_counts["course_prerequisites"] == (
        sum(len(course["prerequisites"]) for course in cfg.COURSE_DIRECTORY_COURSES)
        + sum(len(prerequisites) for prerequisites in PREREQUISITES.values())
        + recommended
    )
    assert first_counts["path_stages"] == len(cfg.STAGES)
    assert first_counts["path_stage_courses"] == sum(len(courses) for *_stage, courses in cfg.STAGES)
    assert first_counts["path_templates"] == len(cfg.TEMPLATES)
    assert first_counts["path_template_stages"] == sum(len(stages) for *_template, stages in cfg.TEMPLATES)
    assert first_counts["learning_paths"] == 0

    from seeds.sync_curriculum import sync_curriculum

    first_sync = sync_curriculum(learn_db)
    second_counts = _catalogue_counts(learn_db)
    second_sync = sync_curriculum(learn_db)
    third_counts = _catalogue_counts(learn_db)

    assert first_sync == []
    assert second_sync == []
    assert second_counts == first_counts == third_counts


def test_sync_moves_an_empty_synthetic_source_onto_its_own_course_without_touching_learner_rows(
    learn_db, learn_client, learn_catalog,
):
    """An earlier layout pointed a directory course at an empty, marked track level.
    The course is now its own tool course: the same catalogue row (same id) is moved
    over, the empty stand-in level is removed, and every learner-owned row survives."""
    who = register(learn_client)
    profile = learn_client.put(
        f"{API}/my-profile", headers=who["headers"],
        json={"level": "intermediate", "career_goal": "ai-engineer", "fields": ["nlp"]},
    )
    assert profile.status_code == 200, profile.text
    saved = learn_client.put(f"{API}/my-path", headers=who["headers"], json={})
    assert saved.status_code == 200, saved.text
    path_id = saved.json()["id"]
    snapshot_before = list(learn_db.query(LearningPath).filter(LearningPath.id == path_id).one().stages)

    complete_level(learn_db, who["id"], learn_catalog, 1)
    enrollment = Enrollment(user_id=who["id"], track_id=learn_catalog["track"].id)
    learn_db.add(enrollment)
    learn_db.flush()
    enrollment_id = enrollment.id
    progress_snapshot = [
        (row.id, list(row.lessons_completed))
        for row in learn_db.query(UserProgress).filter(UserProgress.user_id == who["id"]).order_by(UserProgress.id)
    ]

    definition = next(course for course in cfg.COURSE_DIRECTORY_COURSES if course["slug"] == "course-006")
    course = learn_db.query(Course).filter(Course.slug == definition["slug"]).one()
    course_id, tool_course_id = course.id, course.tool_course_id
    old_source = TrackLevel(
        track_id=learn_catalog["track"].id, title=definition["title"],
        description=f"curriculum-source:{definition['course_id']}", order=100,
    )
    learn_db.add(old_source)
    learn_db.flush()
    old_source_id = old_source.id
    course.kind, course.tool_course_id, course.track_level_id = COURSE_KIND_TRACK_LEVEL, None, old_source_id
    learn_db.commit()

    from seeds.sync_curriculum import sync_curriculum

    changes = sync_curriculum(learn_db)
    moved = learn_db.query(Course).filter(Course.slug == definition["slug"]).one()

    assert any(change.kind == "course" and change.subject == definition["slug"] for change in changes)
    assert moved.id == course_id
    assert (moved.kind, moved.track_level_id) == (COURSE_KIND_TOOL, None)
    assert moved.tool_course.category == "curriculum"
    assert learn_db.query(TrackLevel).filter(TrackLevel.id == old_source_id).first() is None
    assert learn_db.query(Enrollment).filter(Enrollment.id == enrollment_id).one().user_id == who["id"]
    assert [
        (row.id, list(row.lessons_completed))
        for row in learn_db.query(UserProgress).filter(UserProgress.user_id == who["id"]).order_by(UserProgress.id)
    ] == progress_snapshot
    assert learn_db.query(LearningPath).filter(LearningPath.id == path_id).one().stages == snapshot_before
    assert sync_curriculum(learn_db) == []


def test_sync_refuses_to_move_a_directory_course_from_a_populated_source(learn_db, learn_catalog):
    definition = next(course for course in cfg.COURSE_DIRECTORY_COURSES if course["slug"] == "course-006")
    course = learn_db.query(Course).filter(Course.slug == definition["slug"]).one()
    old_source = TrackLevel(
        track_id=learn_catalog["track"].id,
        title=definition["title"],
        description=f"curriculum-source:{definition['course_id']}",
        order=101,
    )
    learn_db.add(old_source)
    learn_db.flush()
    learn_db.add(Topic(
        level_id=old_source.id, title="Existing learner content", slug="sync-source-guard",
        order=1, difficulty=DifficultyLevel.intermediate, estimated_hours=1.0, skill_tags=[],
    ))
    course.kind, course.tool_course_id, course.track_level_id = COURSE_KIND_TRACK_LEVEL, None, old_source.id
    learn_db.commit()

    from seeds.sync_curriculum import sync_curriculum

    with pytest.raises(LearningValidationError) as error:
        sync_curriculum(learn_db)

    assert error.value.code == "curriculum_source_mismatch"
    assert learn_db.query(Course).filter(Course.id == course.id).one().track_level_id == old_source.id
    assert learn_db.query(Topic).filter(Topic.level_id == old_source.id).count() == 1


def test_sync_leaves_tool_courses_as_distinct_tool_sources(learn_db, learn_catalog):
    before = {
        course.slug: (course.id, course.kind, course.tool_course_id, course.track_level_id)
        for course in learn_db.query(Course).filter(Course.kind == COURSE_KIND_TOOL).all()
    }
    curriculum_slugs = {definition["slug"] for definition in cfg.COURSE_DIRECTORY_COURSES}

    from seeds.sync_curriculum import sync_curriculum

    assert sync_curriculum(learn_db) == []
    after = {
        course.slug: (course.id, course.kind, course.tool_course_id, course.track_level_id)
        for course in learn_db.query(Course).filter(Course.kind == COURSE_KIND_TOOL).all()
    }
    assert after == before
    # 16 hand-seeded tool courses, plus the 14 curriculum courses (also tool courses).
    assert len(after) == 16 + len(curriculum_slugs)
    assert curriculum_slugs <= set(after)


def test_every_canonical_track_is_served_through_fastapi_with_its_exact_directory_roles(
    learn_client, learn_catalog,
):
    """Check config -> persisted rows -> catalogue service -> HTTP response."""
    directory_slugs = {course["slug"] for course in cfg.COURSE_DIRECTORY_COURSES}
    summaries = learn_client.get(f"{API}/paths")
    assert summaries.status_code == 200, summaries.text
    by_goal = {}
    for summary in summaries.json():
        by_goal.setdefault(summary["career_goal"]["slug"], []).append(summary)

    assert set(cfg.GOALS) <= set(by_goal)
    for goal in cfg.GOALS:
        listing = learn_client.get(f"{API}/courses", params={"career_goal": goal})
        assert listing.status_code == 200, listing.text
        actual_roles = {
            item["slug"]: item["track_role"]
            for item in listing.json() if item["slug"] in directory_slugs
        }
        expected_roles = {
            course["slug"]: course["roles"][goal]
            for course in cfg.COURSE_DIRECTORY_COURSES if goal in course["roles"]
        }
        assert actual_roles == expected_roles

        summary = next((item for item in by_goal[goal] if item["field"] is None), by_goal[goal][0])
        path = learn_client.get(f"{API}/paths/{summary['slug']}")
        assert path.status_code == 200, path.text
        body = path.json()
        assert body["career_goal"]["slug"] == goal
        effective_fields = {field["slug"] for field in body["effective_fields"]}
        expected_stages = [
            stage for stage, field in cfg.template_stages(goal)
            if field is None or field in effective_fields
        ]
        assert [stage["slug"] for stage in body["stages"]] == expected_stages


def test_directory_courses_are_independent_courses_with_their_own_route_and_typed_prerequisites(
    learn_client, learn_catalog, learn_db,
):
    """A curriculum course is a course in its own right: not a level of a career track,
    opened under /courses, and its prerequisites split into required and recommended."""
    for definition in cfg.COURSE_DIRECTORY_COURSES:
        course = learn_db.query(Course).filter(Course.slug == definition["slug"]).one()
        assert course.kind == COURSE_KIND_TOOL and course.track_level_id is None
        assert course.tool_course.category == "curriculum"
        assert course.tool_course.slug == definition["slug"]

        response = learn_client.get(f"{API}/courses/{definition['slug']}")
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["href"] == f"/courses/{definition['slug']}/learn"
        assert [prerequisite["slug"] for prerequisite in body["prerequisites"]] == definition["prerequisites"]
        assert not {p["slug"] for p in body["recommended_prerequisites"]} & set(definition["prerequisites"])
        # A career goal is never part of how a course is reached.
        assert learn_client.get(f"{API}/courses/{definition['slug'].upper()}").status_code == 200


def test_legacy_rag_remains_an_ml_engineer_nlp_elective():
    assert cfg.COURSE_ROLES["rag-knowledge-systems"][cfg.ML_ENGINEER] == cfg.OPTIONAL
    assert "rag-knowledge-systems" not in cfg.template_courses(cfg.ML_ENGINEER, fields=[])
    assert "rag-knowledge-systems" in cfg.template_courses(cfg.ML_ENGINEER, fields=["nlp"])
