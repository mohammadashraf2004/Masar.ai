"""
Content management: the admin API and the seed script.

The claim being proven is the one the redesign rests on — that a new
specialisation is *data*. The centrepiece test adds a field, a course, a stage
and a template stage entirely through the admin API and then watches a learner's
path change with no code involved.
"""
import logging

import pytest

from app.models.learning_path import (
    CareerRole, Course, CoursePrerequisite, LearningField, LearningLevel, PathStage, PathTemplate,
)
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import make_admin, register

ADMIN = "/api/v1/admin/learning"
API = "/api/v1/learning"


@pytest.fixture()
def admin_user(learn_client, learn_db):
    who = register(learn_client)
    make_admin(learn_db, who["id"])
    return who


def _put(client, who, kind, slug, body):
    return client.put(f"{ADMIN}/{kind}/{slug}", headers=who["headers"], json=body)


def _course_body(source_slug, level="intermediate", **kw):
    body = {"source": {"kind": "tool_course", "slug": source_slug}, "level": level}
    body.update(kw)
    return body


# ─── Authorization ──────────────────────────────────────────────────────────

WRITES = [
    ("levels", "x-level", {"name": "X", "rank": 9}),
    ("skills", "x-skill", {"name": "X"}),
    ("fields", "x-field", {"name": "X"}),
    ("career-goals", "x-goal", {"title": "X"}),
    ("courses", "x-course", {"source": {"kind": "tool_course", "slug": "langchain"}, "level": "beginner"}),
    ("stages", "x-stage", {"title": "X"}),
    ("templates", "x-template", {"title": "X", "stages": []}),
]


@pytest.mark.parametrize("kind,slug,body", WRITES)
def test_admin_writes_reject_anonymous_callers(learn_client, legacy_catalog, kind, slug, body):
    assert learn_client.put(f"{ADMIN}/{kind}/{slug}", json=body).status_code == 401


@pytest.mark.parametrize("kind,slug,body", WRITES)
def test_admin_writes_reject_students_and_change_nothing(learn_client, legacy_catalog, learn_db, kind, slug, body):
    student = register(learn_client)
    assert _put(learn_client, student, kind, slug, body).status_code == 403
    assert learn_db.query(Course).filter(Course.slug == slug).count() == 0


@pytest.mark.parametrize("path", ["catalog", "health"])
def test_admin_reads_reject_anonymous_and_students(learn_client, legacy_catalog, path):
    assert learn_client.get(f"{ADMIN}/{path}").status_code == 401
    student = register(learn_client)
    assert learn_client.get(f"{ADMIN}/{path}", headers=student["headers"]).status_code == 403


def test_a_role_change_is_read_from_the_database_not_a_token(learn_client, legacy_catalog, learn_db):
    """Demoting an admin takes effect immediately, not when their token expires."""
    who = register(learn_client)
    make_admin(learn_db, who["id"])
    assert learn_client.get(f"{ADMIN}/health", headers=who["headers"]).status_code == 200
    from app.models.user import User, UserRole

    learn_db.query(User).filter(User.id == who["id"]).update({"role": UserRole.student})
    learn_db.commit()
    assert learn_client.get(f"{ADMIN}/health", headers=who["headers"]).status_code == 403


# ─── A new specialisation is data ───────────────────────────────────────────

def _uncatalogued_tool_course(db, slug="ros-basics"):
    """A tool course with one published lesson that the catalogue does not know."""
    from app.models.learning import DifficultyLevel, Lesson
    from app.models.tool_course import ToolCourse, ToolTopic

    course = ToolCourse(slug=slug, title="ROS Basics", difficulty=DifficultyLevel.intermediate,
                        estimated_hours=8.0, related_track_ids=[], is_active=True)
    db.add(course)
    db.flush()
    topic = ToolTopic(tool_course_id=course.id, title="t", slug="t", order=1,
                      difficulty=DifficultyLevel.intermediate, estimated_hours=8.0,
                      skill_tags=[], prerequisite_ids=[])
    db.add(topic)
    db.flush()
    db.add(Lesson(tool_topic_id=topic.id, title="L", content="c", order=1))
    db.commit()


def test_a_new_field_needs_no_code_change(learn_client, legacy_catalog, admin_user, learn_db):
    """Add "Robotics" - a field, a course for it, a stage and a template entry -
    through the admin API alone, and a learner's path grows a Robotics stage."""
    _uncatalogued_tool_course(learn_db)

    assert _put(learn_client, admin_user, "fields", "robotics", {
        "name": "Robotics", "name_ar": "الروبوتات", "icon": "cpu", "position": 7,
    }).status_code == 200
    assert _put(learn_client, admin_user, "courses", "ros-basics", _course_body(
        "ros-basics", fields=["robotics"], roles=["ai-engineer"],
    )).status_code == 200
    assert _put(learn_client, admin_user, "stages", "robotics-core", {
        "title": "Robotics Foundations", "title_ar": "أسس الروبوتات", "courses": ["ros-basics"],
    }).status_code == 200

    template = next(t for t in learn_client.get(f"{ADMIN}/catalog", headers=admin_user["headers"]).json()["templates"]
                    if t["slug"] == "ai-engineer-path")
    stages = template["stages"]
    at = next(i for i, s in enumerate(stages) if s["stage"] == "production")
    stages.insert(at, {"stage": "robotics-core", "field": "robotics"})
    assert _put(learn_client, admin_user, "templates", "ai-engineer-path", {
        "title": template["title"], "career_goal": "ai-engineer", "stages": stages,
    }).status_code == 200

    # It is in the public catalogue...
    assert "robotics" in {f["slug"] for f in learn_client.get(f"{API}/fields").json()}
    # ...has its own predefined route...
    assert "ai-engineer-robotics" in {p["slug"] for p in learn_client.get(f"{API}/paths").json()}
    # ...and a learner who picks it gets the stage, with the course in it.
    learner = register(learn_client)
    path = learn_client.post(f"{API}/paths/generate", headers=learner["headers"],
                             json={"level": "intermediate", "fields": ["robotics"], "career_goal": "ai-engineer"}).json()
    stage = next(s for s in path["stages"] if s["slug"] == "robotics-core")
    assert [c["course"]["slug"] for c in stage["courses"]] == ["ros-basics"]
    # Everyone who did not pick it is unaffected.
    other = learn_client.post(f"{API}/paths/generate", headers=learner["headers"],
                              json={"level": "intermediate", "fields": ["nlp"], "career_goal": "ai-engineer"}).json()
    assert "robotics-core" not in [s["slug"] for s in other["stages"]]


# ─── Upserts ────────────────────────────────────────────────────────────────

def test_an_upsert_is_idempotent(learn_client, legacy_catalog, admin_user, learn_db):
    body = {"name": "Quantum ML", "name_ar": "تعلّم الآلة الكمّي", "min_level": "advanced",
            "prerequisites": ["machine-learning"], "position": 9}
    first = _put(learn_client, admin_user, "fields", "quantum-ml", body).json()
    second = _put(learn_client, admin_user, "fields", "quantum-ml", body).json()
    assert first == second
    assert learn_db.query(LearningField).filter(LearningField.slug == "quantum-ml").count() == 1
    assert first["min_level"] == "advanced" and first["prerequisites"] == ["machine-learning"]


def test_an_upsert_replaces_the_relationship_lists(learn_client, legacy_catalog, admin_user):
    _put(learn_client, admin_user, "career-goals", "ai-developer", {
        "title": "AI Developer", "required_fields": ["nlp"], "recommended_fields": ["multimodal"],
        "required_skills": ["llms", "rag"],
    })
    out = _put(learn_client, admin_user, "career-goals", "ai-developer", {
        "title": "AI Developer", "recommended_fields": ["speech"], "required_skills": ["llms"],
    }).json()
    assert out["required_fields"] == [] and out["recommended_fields"] == ["speech"]
    assert out["required_skills"] == ["llms"]


def test_levels_can_be_configured_and_ranks_cannot_collide(learn_client, legacy_catalog, admin_user):
    ok = _put(learn_client, admin_user, "levels", "expert", {"name": "Expert", "name_ar": "خبير", "rank": 4})
    assert ok.status_code == 200 and ok.json()["rank"] == 4
    assert [l["slug"] for l in learn_client.get(f"{API}/levels").json()][-1] == "expert"
    clash = _put(learn_client, admin_user, "levels", "other", {"name": "Other", "rank": 4})
    assert clash.status_code == 422 and clash.json()["detail"]["error"] == "rank_taken"


def test_a_course_can_be_tagged_and_retagged_without_being_duplicated(learn_client, legacy_catalog, admin_user, learn_db):
    body = _course_body("langchain", level="advanced", fields=["nlp", "multimodal"],
                        roles=["ai-engineer"], teaches=["llms", "langchain"], assumes=["rag"],
                        title="LangChain in Depth", title_ar="LangChain بعمق")
    out = _put(learn_client, admin_user, "courses", "langchain", body).json()
    assert out["level"] == "advanced" and out["fields"] == ["nlp", "multimodal"]
    assert out["assumes"] == ["rag"] and out["title"] == "LangChain in Depth"
    assert learn_db.query(Course).filter(Course.slug == "langchain").count() == 1
    public = learn_client.get(f"{API}/courses/langchain").json()
    assert public["title_ar"] == "LangChain بعمق" and [f["slug"] for f in public["fields"]] == ["nlp", "multimodal"]


def test_stage_and_template_order_is_the_order_sent(learn_client, legacy_catalog, admin_user):
    stage = _put(learn_client, admin_user, "stages", "custom", {
        "title": "Custom", "courses": ["prompt-engineering", "langchain", "llm-integration"],
    }).json()
    assert stage["courses"] == ["prompt-engineering", "langchain", "llm-integration"]
    tpl = _put(learn_client, admin_user, "templates", "ai-developer-path", {
        "title": "AI Developer path", "career_goal": "ai-developer",
        "stages": [{"stage": "production"}, {"stage": "foundations"}, {"stage": "custom", "field": "nlp"}],
    }).json()
    assert [s["stage"] for s in tpl["stages"]] == ["production", "foundations", "custom"]
    assert tpl["stages"][2]["field"] == "nlp"


# ─── Validation ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("kind,slug,body,error", [
    ("fields", "f1", {"name": "F", "min_level": "godlike"}, "unknown_level"),
    ("fields", "f2", {"name": "F", "prerequisites": ["nope"]}, "unknown_field"),
    ("fields", "nlp", {"name": "NLP", "prerequisites": ["nlp"]}, "field_prerequisite_self"),
    ("career-goals", "g1", {"title": "G", "required_skills": ["nope"]}, "unknown_skill"),
    ("career-goals", "g2", {"title": "G", "required_fields": ["nlp"], "recommended_fields": ["nlp"]}, "field_in_both"),
    ("courses", "langchain", _course_body("langchain", fields=["nope"]), "unknown_field"),
    ("courses", "c2", _course_body("nope-tool"), "unknown_source"),
    ("courses", "c3", {"source": {"kind": "track_level", "track_slug": "ai-developer", "level_order": 99}, "level": "beginner"}, "unknown_source"),
    ("courses", "c4", _course_body("langchain"), "source_already_catalogued"),
    ("courses", "llamaindex", _course_body("langchain"), "source_immutable"),
    ("stages", "s1", {"title": "S", "courses": ["nope"]}, "unknown_course"),
    ("templates", "t1", {"title": "T", "stages": [{"stage": "nope"}]}, "unknown_stage"),
    ("templates", "t2", {"title": "T", "stages": [{"stage": "foundations"}, {"stage": "foundations"}]}, "duplicate_stage"),
    ("templates", "t3", {"title": "T", "career_goal": "ai-engineer", "stages": []}, "template_exists"),
])
def test_invalid_configuration_is_refused_with_a_code(learn_client, legacy_catalog, admin_user, kind, slug, body, error):
    resp = _put(learn_client, admin_user, kind, slug, body)
    assert resp.status_code == 422, resp.text
    assert resp.json()["detail"]["error"] == error


def test_a_refused_write_leaves_nothing_behind(learn_client, legacy_catalog, admin_user, learn_db):
    resp = _put(learn_client, admin_user, "career-goals", "half-made", {
        "title": "Half made", "required_fields": ["nlp"], "required_skills": ["nope"],
    })
    assert resp.status_code == 422
    assert learn_db.query(CareerRole).filter(CareerRole.slug == "half-made").count() == 0


def test_malformed_slugs_and_oversized_lists_are_bounded(learn_client, legacy_catalog, admin_user):
    assert _put(learn_client, admin_user, "fields", "Bad Slug!", {"name": "X"}).status_code == 422
    assert _put(learn_client, admin_user, "stages", "big", {"title": "X", "courses": ["a"] * 201}).status_code == 422
    assert _put(learn_client, admin_user, "levels", "x", {"name": "X", "rank": 101}).status_code == 422


# ─── Prerequisite graphs ────────────────────────────────────────────────────

def test_a_course_prerequisite_cycle_is_refused_and_rolled_back(learn_client, legacy_catalog, admin_user, learn_db):
    a = _course_body("langchain", prerequisites=["llamaindex"])
    b = _course_body("llamaindex", prerequisites=["langchain"])
    assert _put(learn_client, admin_user, "courses", "langchain", a).status_code == 200
    resp = _put(learn_client, admin_user, "courses", "llamaindex", b)
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "course_prerequisite_cycle"
    assert "langchain" in resp.json()["detail"]["message"]
    llama = learn_db.query(Course).filter(Course.slug == "llamaindex").one()
    assert learn_db.query(CoursePrerequisite).filter(CoursePrerequisite.course_id == llama.id).count() == 0


def test_a_field_prerequisite_cycle_is_refused(learn_client, legacy_catalog, admin_user):
    resp = _put(learn_client, admin_user, "fields", "nlp", {"name": "NLP & LLMs", "prerequisites": ["multimodal"]})
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "field_prerequisite_cycle"


def test_the_multimodal_rule_can_be_tightened_through_the_api(learn_client, legacy_catalog, admin_user):
    fields = {f["slug"]: f for f in learn_client.get(f"{API}/fields").json()}
    mm = fields["multimodal"]
    assert _put(learn_client, admin_user, "fields", "multimodal", {
        "name": mm["name"], "name_ar": mm["name_ar"], "icon": mm["icon"], "min_level": "advanced",
        "prerequisites": ["nlp", "computer-vision", "speech"], "prerequisite_min_required": 2,
        "prerequisite_recommended": 2, "position": mm["position"],
    }).status_code == 200
    learner = register(learn_client)
    path = learn_client.post(f"{API}/paths/generate", headers=learner["headers"],
                             json={"level": "advanced", "fields": ["nlp", "multimodal"], "career_goal": "ai-engineer"}).json()
    added = next(a for a in path["advisories"] if a["code"] == "prerequisite_route_added")
    assert len(added["params"]["added"]) == 1  # one modality chosen, a second now required


# ─── Retiring things ────────────────────────────────────────────────────────

def test_deactivating_a_course_removes_it_from_new_paths_but_a_saved_path_keeps_working(learn_client, legacy_catalog, admin_user):
    learner = register(learn_client)
    learn_client.put(f"{API}/my-profile", headers=learner["headers"],
                     json={"level": "intermediate", "fields": ["nlp"], "career_goal": "ai-engineer"})
    built = learn_client.put(f"{API}/my-path", headers=learner["headers"], json={}).json()
    assert "prompt-engineering" in {c["course"]["slug"] for s in built["stages"] for c in s["courses"]}

    assert _put(learn_client, admin_user, "courses", "prompt-engineering", {
        "source": {"kind": "track_level", "track_slug": "ai-developer", "level_order": 4},
        "level": "intermediate", "title": "Prompt Engineering", "fields": ["nlp"],
        "roles": ["ai-developer", "ai-engineer"], "is_active": False,
    }).status_code == 200

    assert "prompt-engineering" not in {c["slug"] for c in learn_client.get(f"{API}/courses").json()}
    saved = learn_client.get(f"{API}/my-path", headers=learner["headers"])
    assert saved.status_code == 200  # the learner's path still resolves...
    assert "prompt-engineering" not in {c["course"]["slug"] for s in saved.json()["stages"] for c in s["courses"]}  # ...minus it


def test_deactivating_a_career_goal_asks_the_learner_to_choose_again(learn_client, legacy_catalog, admin_user):
    learner = register(learn_client)
    learn_client.put(f"{API}/my-profile", headers=learner["headers"],
                     json={"level": "beginner", "fields": ["data"], "career_goal": "data-analyst"})
    assert _put(learn_client, admin_user, "career-goals", "data-analyst",
                {"title": "Data Analyst", "is_active": False}).status_code == 200
    resp = learn_client.put(f"{API}/my-path", headers=learner["headers"], json={})
    assert resp.status_code == 409 and resp.json()["detail"]["error"] == "learning_profile_incomplete"


def test_the_admin_catalogue_includes_inactive_entries_the_public_one_hides(learn_client, legacy_catalog, admin_user):
    f = learn_client.get(f"{API}/fields").json()[-1]
    _put(learn_client, admin_user, "fields", f["slug"], {"name": f["name"], "position": f["position"], "is_active": False})
    assert f["slug"] not in {x["slug"] for x in learn_client.get(f"{API}/fields").json()}
    everything = learn_client.get(f"{ADMIN}/catalog", headers=admin_user["headers"]).json()
    assert f["slug"] in {x["slug"] for x in everything["fields"]}


# ─── Health report ──────────────────────────────────────────────────────────

def test_health_flags_configuration_problems_as_data(learn_client, legacy_catalog, admin_user):
    _put(learn_client, admin_user, "career-goals", "quant", {"title": "Quant"})
    _put(learn_client, admin_user, "stages", "empty-stage", {"title": "Empty"})
    issues = learn_client.get(f"{ADMIN}/health", headers=admin_user["headers"]).json()
    codes = {(i["code"], str(i["subject"])) for i in issues}
    assert ("career_goal_without_template", "quant") in codes
    assert ("stage_without_courses", "empty-stage") in codes
    assert ("course_without_content", "pinecone") in codes
    assert not any(i["code"] == "course_prerequisite_cycle" for i in issues)


def test_health_reports_a_prerequisite_cycle_written_around_the_api(learn_client, legacy_catalog, admin_user, learn_db):
    a = learn_db.query(Course).filter(Course.slug == "langchain").one()
    b = learn_db.query(Course).filter(Course.slug == "llamaindex").one()
    learn_db.add_all([CoursePrerequisite(course_id=a.id, prerequisite_course_id=b.id),
                      CoursePrerequisite(course_id=b.id, prerequisite_course_id=a.id)])
    learn_db.commit()
    issues = learn_client.get(f"{ADMIN}/health", headers=admin_user["headers"]).json()
    cycle = next(i for i in issues if i["code"] == "course_prerequisite_cycle")
    assert {"langchain", "llamaindex"} <= set(cycle["subject"])


# ─── Audit ──────────────────────────────────────────────────────────────────

def test_every_admin_write_is_audited_without_leaking_content(learn_client, legacy_catalog, admin_user, caplog, logs_enabled):
    with caplog.at_level(logging.INFO, logger="security"):
        _put(learn_client, admin_user, "skills", "audited-skill", {"name": "Audited"})
    events = [r.getMessage() for r in caplog.records if r.name == "security"]
    line = next(e for e in events if "admin.action" in e)
    assert f"admin_id={admin_user['id']}" in line and "learning.skill.upsert" in line and "audited-skill" in line
    assert "Audited" not in line  # the target is named, the payload is not logged


def test_a_refused_write_is_not_audited_as_done(learn_client, legacy_catalog, admin_user, caplog, logs_enabled):
    with caplog.at_level(logging.INFO, logger="security"):
        _put(learn_client, admin_user, "fields", "bad", {"name": "Bad", "prerequisites": ["nope"]})
    assert not [r for r in caplog.records if "admin.action" in r.getMessage()]


# ─── Seed ───────────────────────────────────────────────────────────────────

def test_the_seed_is_idempotent(learn_db, legacy_catalog):
    from seeds.seed_learning_paths import seed_learning_catalog

    assert all(count == 0 for count in seed_learning_catalog(learn_db).values())


def test_the_seed_never_overwrites_what_an_admin_changed(learn_client, legacy_catalog, admin_user, learn_db):
    from seeds.seed_learning_paths import seed_learning_catalog

    _put(learn_client, admin_user, "stages", "rag", {"title": "Retrieval, Renamed", "courses": ["advanced-rag"]})
    seed_learning_catalog(learn_db)
    stage = learn_db.query(PathStage).filter(PathStage.slug == "rag").one()
    assert stage.title == "Retrieval, Renamed" and len(stage.course_links) == 1


def test_the_seed_fills_gaps_only(learn_db, legacy_catalog):
    from seeds.seed_learning_paths import seed_learning_catalog

    learn_db.query(PathTemplate).filter(PathTemplate.slug == "mlops-engineer-path").delete()
    learn_db.commit()
    assert seed_learning_catalog(learn_db)["templates"] == 1


def test_the_seed_tolerates_content_that_has_not_been_seeded(learn_db):
    from seeds.seed_learning_paths import seed_learning_catalog

    report = seed_learning_catalog(learn_db)  # no track, no tool courses at all
    # The only courses that can exist are the curriculum courses: each is its own tool course,
    # so - unlike a track level - it needs no legacy track to point at.
    from seeds.curriculum import COURSE_DIRECTORY_COURSES
    assert report["courses"] == len(COURSE_DIRECTORY_COURSES)
    assert report["stages"] > 0 and report["templates"] == 5


def test_the_seeded_configuration_has_no_prerequisite_cycle(learn_client, legacy_catalog, admin_user):
    issues = learn_client.get(f"{ADMIN}/health", headers=admin_user["headers"]).json()
    assert [i for i in issues if i["code"] == "course_prerequisite_cycle"] == []
