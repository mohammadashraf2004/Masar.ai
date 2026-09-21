"""
GET /learning/my-skill-gaps and the `why` block on roadmap courses, against the
shipped configuration (`learn_catalog` runs the real seed).

The pure rules are pinned in test_skill_gaps.py; this file checks that the API
serves them faithfully, respects the existing semantics (strict "Already know",
tools as skills, declared != completed), never inflates the roadmap's own
behaviour, and does not query per course.
"""
import pytest
from sqlalchemy import event

from app.db.session import engine
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import complete_level, register
from tests.test_learning_hardening import _by_slug, _put_skills, _reload
from tests.test_learning_personalized import API, _build, _profile

URL = f"{API}/my-skill-gaps"


def gaps(client, who):
    resp = client.get(URL, headers=who["headers"])
    assert resp.status_code == 200, resp.text
    return resp.json()


def slugs(items):
    return [s["slug"] for s in items]


def all_courses(path):
    return [c for s in path["stages"] for c in s["courses"]]


# ─── Contract ───────────────────────────────────────────────────────────────

def test_the_endpoint_requires_sign_in(learn_client, learn_catalog):
    assert learn_client.get(URL).status_code == 401


def test_a_learner_with_no_roadmap_gets_an_empty_state_not_an_error(learn_client, learn_catalog):
    who = register(learn_client)
    body = gaps(learn_client, who)
    assert body["available"] is False
    assert body["known"] == body["partial"] == body["missing"] == body["groups"] == []
    assert body["summary"] == {"required": 0, "known": 0, "partial": 0, "missing": 0, "immediate": 0, "coverage_pct": None}
    _profile(learn_client, who)                                    # a profile alone is still not a roadmap
    assert gaps(learn_client, who)["available"] is False


def test_the_response_has_the_documented_shape(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    body = gaps(learn_client, who)
    assert {"available", "level", "career_goal", "fields", "current_stage", "summary",
            "known", "partial", "missing", "groups"} <= set(body)
    assert body["available"] is True and body["career_goal"]["slug"] == "ai-engineer"
    assert body["level"]["slug"] == "beginner" and [f["slug"] for f in body["fields"]] == ["nlp"]
    item = body["missing"][0]
    assert {"slug", "name", "name_ar", "kind", "status", "group", "stage", "is_goal_required",
            "is_immediate", "course_count", "covered_by_completed"} <= set(item)
    assert item["status"] == "missing" and item["kind"] in ("skill", "tool")
    group = body["groups"][0]
    assert {"key", "kind", "field", "total", "known_count", "skills"} <= set(group)


def test_the_summary_agrees_with_the_lists_and_the_groups(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner", known_skills=["llms", "rag"])
    body = gaps(learn_client, who)
    s = body["summary"]
    assert s["known"] == len(body["known"]) and s["partial"] == len(body["partial"]) and s["missing"] == len(body["missing"])
    assert s["required"] == s["known"] + s["partial"] + s["missing"]
    assert s["coverage_pct"] == pytest.approx(100.0 * s["known"] / s["required"], abs=0.1)
    assert sum(g["total"] for g in body["groups"]) == s["required"]
    assert sum(g["known_count"] for g in body["groups"]) == s["known"]
    listed = [x["slug"] for g in body["groups"] for x in g["skills"]]
    assert sorted(listed) == sorted(slugs(body["missing"]) + slugs(body["partial"]))   # groups hold what is still to do


def test_one_learners_gaps_never_depend_on_anothers_skills(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a, level="beginner")
    _build(learn_client, b, level="beginner", known_skills=["llms"])
    assert "llms" in slugs(gaps(learn_client, a)["missing"])
    assert "llms" in slugs(gaps(learn_client, b)["known"])


# ─── Skills ─────────────────────────────────────────────────────────────────

def test_with_nothing_declared_the_relevant_skills_are_all_missing(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    body = gaps(learn_client, who)
    assert body["known"] == [] and body["summary"]["coverage_pct"] == 0.0
    assert {"llms", "rag", "embeddings"} <= set(slugs(body["missing"]))


def test_a_declared_skill_moves_from_missing_to_known(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    assert "embeddings" in slugs(gaps(learn_client, who)["missing"])
    _put_skills(learn_client, who, ["embeddings"])
    body = gaps(learn_client, who)
    assert "embeddings" in slugs(body["known"]) and "embeddings" not in slugs(body["missing"])
    assert "rag" in slugs(body["missing"])                          # nothing else was inferred from it


def test_declaring_a_skill_does_not_claim_the_skills_of_its_prerequisite_course(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    _put_skills(learn_client, who, ["rag", "retrieval"])            # rag-knowledge-systems is now "Already know"
    path = _reload(learn_client, who)
    assert _by_slug(path)["rag-knowledge-systems"]["state"] == "waived"
    body = gaps(learn_client, who)
    assert {"rag", "retrieval"} <= set(slugs(body["known"]))
    assert "llms" in slugs(body["missing"])                         # its prerequisite's skill is still to gain


def test_a_tool_never_stands_in_for_the_skill_and_is_told_apart(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    _put_skills(learn_client, who, ["langchain"])
    body = gaps(learn_client, who)
    known = {s["slug"]: s["kind"] for s in body["known"]}
    assert known == {"langchain": "tool"}                           # LangChain known, and nothing else with it
    assert "rag" in slugs(body["missing"])
    tools = [g for g in body["groups"] if g["kind"] == "tools"]
    assert len(tools) == 1 and all(s["kind"] == "tool" for s in tools[0]["skills"])
    assert body["groups"][-1]["kind"] == "tools"                    # tools come last
    assert all(s["kind"] == "skill" for g in body["groups"] if g["kind"] != "tools" for s in g["skills"])


def test_gaps_are_grouped_under_real_fields_and_the_field_is_named(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    body = gaps(learn_client, who)
    nlp = next(g for g in body["groups"] if g["kind"] == "field")
    assert nlp["field"]["slug"] == "nlp" and nlp["field"]["name"]
    assert "rag" in slugs(nlp["skills"])
    rag = next(s for s in body["missing"] if s["slug"] == "rag")
    assert rag["group"]["slug"] == "nlp" and rag["stage"]["slug"] and rag["course_count"] >= 1


def test_a_skill_the_goal_requires_is_flagged(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    required = {s["slug"] for s in gaps(learn_client, who)["missing"] if s["is_goal_required"]}
    assert {"evaluation", "production-deployment"} <= required      # AI Engineer's own required skills


def test_no_skill_is_invented_every_gap_is_a_catalogue_skill(learn_client, learn_catalog, learn_db):
    from app.models.learning_path import Skill
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    body = gaps(learn_client, who)
    catalogue = {s.slug for s in learn_db.query(Skill).all()}
    assert set(slugs(body["missing"]) + slugs(body["known"]) + slugs(body["partial"])) <= catalogue
    assert "python" not in catalogue and "python" not in slugs(body["missing"])


# ─── Level, field, career ───────────────────────────────────────────────────

def test_a_beginner_and_an_advanced_learner_get_different_gaps(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a, level="beginner")
    _build(learn_client, b, level="advanced")
    beginner, advanced = gaps(learn_client, a), gaps(learn_client, b)
    assert set(slugs(advanced["missing"])) < set(slugs(beginner["missing"]))    # fewer, not the same
    assert advanced["summary"]["required"] < beginner["summary"]["required"]


def test_the_learners_field_decides_which_skills_are_relevant(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a, level="intermediate", fields=("nlp",))
    _build(learn_client, b, level="intermediate", fields=("multimodal",))
    assert "rag" in slugs(gaps(learn_client, a)["missing"])
    mm = gaps(learn_client, b)
    assert "multimodal" in slugs(mm["missing"]) and "vision-language-models" in slugs(mm["missing"])


def test_the_career_goal_decides_what_is_required(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a, level="beginner", goal="ai-engineer")
    _build(learn_client, b, level="beginner", goal="data-analyst", fields=("data",))
    data = gaps(learn_client, b)
    required = {s["slug"] for s in data["missing"] if s["is_goal_required"]}
    assert {"sql", "data-analysis", "statistics"} == required      # what the goal lists, whether or not a course teaches it yet
    uncovered = [s for s in data["missing"] if s["is_goal_required"] and s["course_count"] == 0]
    assert uncovered, "required skills no published course teaches are reported, not hidden"
    assert all(s["stage"] is None for s in uncovered)


def test_multimodal_is_never_blocked_and_its_prerequisite_route_shows_up_as_gaps(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="advanced", fields=("multimodal",))
    assert _by_slug(path)["multimodal-ai"]["state"] == "required"
    body = gaps(learn_client, who)
    assert [f["slug"] for f in body["fields"]] == ["nlp", "multimodal"]      # the route the generator built
    assert {"multimodal", "vision-language-models"} <= set(slugs(body["missing"]))
    assert "embeddings" in slugs(body["missing"])                   # the NLP prerequisite route's skills count
    _put_skills(learn_client, who, ["llms", "prompt-engineering", "rag", "retrieval", "embeddings", "semantic-search",
                                    "ai-agents", "langchain", "langgraph", "llamaindex", "qdrant", "vector-databases"])
    after = gaps(learn_client, who)
    assert [f["slug"] for f in after["fields"]] == ["multimodal"]  # declared NLP: not routed back through it
    assert "multimodal" in slugs(after["missing"])


# ─── Completed courses ──────────────────────────────────────────────────────

def test_finishing_a_course_declares_nothing_and_completion_is_independent(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 1)           # AI Engineering Foundations
    path = _build(learn_client, who, level="beginner")
    assert _by_slug(path)["ai-engineering-foundations"]["state"] == "completed"
    body = gaps(learn_client, who)
    assert body["known"] == []                                       # completion is not a declaration
    llms = next(s for s in body["missing"] if s["slug"] == "llms")
    assert llms["covered_by_completed"] is True                      # ...but the report knows a finished course teaches it
    assert learn_client.get(f"{API}/my-skills", headers=who["headers"]).json()["known"][0]["source"] == "course_completion"
    # Changing the declaration never un-completes anything.
    after = _put_skills(learn_client, who, ["rag"])
    assert _by_slug(after)["ai-engineering-foundations"]["state"] == "completed"
    assert "llms" not in slugs(gaps(learn_client, who)["known"])


def test_a_course_under_way_makes_its_skills_partially_covered(learn_client, learn_catalog, learn_db):
    from app.models.progress import UserProgress
    who = register(learn_client)
    topic_id, lesson_id = learn_catalog["level_lessons"][3][0]      # one of two lessons of RAG & Knowledge Systems
    learn_db.add(UserProgress(user_id=who["id"], topic_id=topic_id, lessons_completed=[lesson_id], exercises_completed=[]))
    learn_db.commit()
    _build(learn_client, who, level="beginner")
    body = gaps(learn_client, who)
    assert {"rag", "retrieval"} <= set(slugs(body["partial"]))
    assert body["summary"]["partial"] == len(body["partial"]) > 0
    _put_skills(learn_client, who, ["rag"])
    body = gaps(learn_client, who)
    assert "rag" in slugs(body["known"]) and "rag" not in slugs(body["partial"])      # declared beats under way


def test_regenerating_the_roadmap_is_unchanged_and_the_gaps_follow_it(learn_client, learn_catalog, learn_db):
    from app.models.learning_path import LearningPath
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    before = gaps(learn_client, who)
    path = _put_skills(learn_client, who, ["llms", "rag"])
    after = gaps(learn_client, who)
    assert after["summary"]["known"] > before["summary"]["known"]
    rows = learn_db.query(LearningPath).filter(LearningPath.user_id == who["id"]).all()
    assert sorted(p.status for p in rows) == ["active", "archived"]                # the existing archive-and-rebuild, once
    assert path["id"] == max(p.id for p in rows)


# ─── Why this course? ───────────────────────────────────────────────────────

def test_every_roadmap_course_carries_a_why_that_partitions_its_skills(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner", known_skills=["llms", "embeddings"])
    courses = all_courses(path)
    assert courses
    for c in courses:
        why = c["why"]
        assert why is not None, c["course"]["slug"]
        taught, known, gain = slugs(why["skills_taught"]), slugs(why["known_skills"]), slugs(why["skills_to_gain"])
        assert sorted(taught) == sorted(slugs(c["course"]["skills"]))            # the course's own skills, not a second list
        assert sorted(known + gain) == sorted(taught) and not set(known) & set(gain)
        assert (why["taught_count"], why["known_count"], why["to_gain_count"]) == (len(taught), len(known), len(gain))
        assert why["career_goal"]["slug"] == "ai-engineer" and why["stage"]["slug"]
        assert set(why["reasons"]) <= {"career_requirement", "field_requirement", "stage_requirement", "skill_gap", "prerequisite"}
        assert sorted(known) == sorted(slugs(c["known_skills"])) or c["state"] not in ("required", "waived")


def test_the_why_reports_partial_coverage_with_the_existing_strict_semantics(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner", known_skills=["llms"])
    foundations = _by_slug(path)["ai-engineering-foundations"]                # teaches llms and system-design
    assert foundations["state"] == "required"                                 # not waived: one of two
    why = foundations["why"]
    assert slugs(why["known_skills"]) == ["llms"] and slugs(why["skills_to_gain"]) == ["system-design"]
    assert why["known_count"] == 1 and why["taught_count"] == 2
    assert "skill_gap" in why["reasons"]
    llm = _by_slug(path)["llm-integration"]                                   # teaches only llms: waived
    assert llm["state"] == "waived" and llm["why"]["to_gain_count"] == 0 and "skill_gap" not in llm["why"]["reasons"]


def test_the_why_names_the_route_fields_stage_and_prerequisites(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner")
    rag = _by_slug(path)["rag-knowledge-systems"]["why"]
    assert [f["slug"] for f in rag["fields"]] == ["nlp"]
    assert rag["stage"]["slug"] == "rag" and rag["stage"]["title"]
    assert {"field_requirement", "stage_requirement", "skill_gap"} <= set(rag["reasons"])
    llm = _by_slug(path)["llm-integration"]["why"]
    assert "prerequisite" in llm["reasons"] and "rag-knowledge-systems" in [c["slug"] for c in llm["prerequisite_for"]]
    ev = _by_slug(path)["ai-evaluation-observability"]["why"]
    assert "career_requirement" in ev["reasons"] and "evaluation" in slugs(ev["goal_skills"])


def test_the_current_and_next_course_carry_the_same_why(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner")
    by_slug = _by_slug(path)
    for step in (path["current_course"], path["next_course"]):
        assert step["why"] == by_slug[step["course"]["slug"]]["why"]
        assert step["why"]["to_gain_count"] > 0
    assert _reload(learn_client, who)["current_course"]["why"] == path["current_course"]["why"]   # survives a reload


def test_a_finished_course_is_not_explained_as_something_to_gain(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 1)
    path = _build(learn_client, who, level="beginner")
    why = _by_slug(path)["ai-engineering-foundations"]["why"]
    assert "skill_gap" not in why["reasons"]


def test_the_reasons_are_codes_never_sentences(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner")
    for c in all_courses(path):
        assert all(" " not in r for r in c["why"]["reasons"])


# ─── Performance ────────────────────────────────────────────────────────────

def _count_queries(fn):
    seen = []
    def hook(conn, cursor, statement, params, context, executemany):
        seen.append(statement)
    event.listen(engine, "before_cursor_execute", hook)
    try:
        fn()
    finally:
        event.remove(engine, "before_cursor_execute", hook)
    return len(seen)


def test_gaps_cost_no_more_queries_than_the_roadmap_itself_and_do_not_grow_per_course(learn_client, learn_catalog):
    small, big = register(learn_client), register(learn_client)
    _build(learn_client, small, level="advanced")                   # fewer courses on the roadmap
    _build(learn_client, big, level="beginner", fields=("nlp", "multimodal"))
    n_path = _count_queries(lambda: learn_client.get(f"{API}/my-path", headers=big["headers"]))
    n_gaps = _count_queries(lambda: learn_client.get(URL, headers=big["headers"]))
    assert n_gaps <= n_path, (n_gaps, n_path)
    n_small = _count_queries(lambda: learn_client.get(URL, headers=small["headers"]))
    assert n_gaps - n_small <= 2, (n_gaps, n_small)                 # a bigger roadmap adds no per-course queries
