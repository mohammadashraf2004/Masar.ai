"""
Personalised roadmaps: what a learner says they already know.

Two layers, mirroring the rest of the learning tests:

* the generator's rules, on hand-built catalogues (pure, no database), and
* the API against the shipped configuration (`legacy_catalog` runs the real seed).

The rules under test, in one place:

  - a course is WAIVED when the learner declared *every* skill it teaches;
  - a waived course stays in the path, visible - it is never deleted;
  - completing courses never waives a third course (only a declaration does);
  - declaring a skill never claims its prerequisites;
  - changing the declaration changes only the future of the path: what the
    learner finished stays finished.
"""
import logging

import pytest

from app.models.learning_path import Course, LearnerSkill, LearningPath, Skill
from app.services.learning.domain import (
    ADVISORY_PREREQUISITE_ROUTE_ADDED, ADVISORY_PREREQUISITES_RECOMMENDED,
    REASON_KNOWN_SKILLS, STATE_COMPLETED, STATE_REQUIRED, STATE_WAIVED, UserState,
)
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import complete_level, complete_tool, register
from tests.test_learning_generator import catalog, course, plan, stage, states

API = "/api/v1/learning"


def known(*slugs):
    return UserState(known_skill_slugs=frozenset(slugs))


# ─── The generator's rules ──────────────────────────────────────────────────

def test_a_course_is_waived_when_every_skill_it_teaches_is_declared():
    cat = catalog([course(1, 2, teaches=["rag", "retrieval"]), course(2, 2, teaches=["agents"])],
                  [stage("s", 1, 2)])
    p = plan(cat, state=known("rag", "retrieval"))
    assert states(p) == {1: STATE_WAIVED, 2: STATE_REQUIRED}
    assert p.stages[0].courses[0].reason == REASON_KNOWN_SKILLS


def test_declaring_only_some_of_a_courses_skills_does_not_waive_it():
    cat = catalog([course(1, 2, teaches=["rag", "retrieval", "embeddings"])], [stage("s", 1)])
    assert states(plan(cat, state=known("rag"))) == {1: STATE_REQUIRED}


def test_a_course_that_teaches_nothing_catalogued_cannot_be_waived_by_a_declaration():
    cat = catalog([course(1, 2, teaches=[])], [stage("s", 1)])
    assert states(plan(cat, state=known("rag", "anything"))) == {1: STATE_REQUIRED}


def test_an_unknown_required_course_stays_required():
    cat = catalog([course(1, 2, teaches=["rag"]), course(2, 2, teaches=["agents"])], [stage("s", 1, 2)])
    assert states(plan(cat, state=known("rag")))[2] == STATE_REQUIRED


def test_a_completed_course_stays_completed_even_if_its_skills_are_declared():
    cat = catalog([course(1, 2, teaches=["rag"])], [stage("s", 1)])
    p = plan(cat, state=UserState(known_skill_slugs=frozenset({"rag"}), completed_course_ids=frozenset({1})))
    assert states(p) == {1: STATE_COMPLETED}


def test_an_explicit_waiver_is_not_relabelled_as_a_declaration():
    cat = catalog([course(1, 2, teaches=["rag"])], [stage("s", 1)])
    p = plan(cat, state=UserState(known_skill_slugs=frozenset({"rag"}), waived_course_ids=frozenset({1})))
    assert states(p) == {1: STATE_WAIVED}
    assert p.stages[0].courses[0].reason is None


def test_finishing_courses_does_not_waive_a_third_that_teaches_their_union():
    """Two finished courses teach `a` and `b`; the third teaches `a` + `b`. Only a
    *declaration* may waive, so the third is still to do."""
    cat = catalog([course(1, 2, teaches=["a"]), course(2, 2, teaches=["b"]), course(3, 2, teaches=["a", "b"])],
                  [stage("s", 1, 2, 3)])
    p = plan(cat, state=UserState(completed_course_ids=frozenset({1, 2})))
    assert states(p) == {1: STATE_COMPLETED, 2: STATE_COMPLETED, 3: STATE_REQUIRED}


def test_waived_courses_stay_in_the_path_and_appear_once():
    cat = catalog([course(1, 2, teaches=["a"]), course(2, 2, teaches=["b"], prereqs=[1])],
                  [stage("s1", 1), stage("s2", 1, 2)])
    p = plan(cat, state=known("a"))
    ids = [c.course_id for s in p.stages for c in s.courses]
    assert 1 in ids and len(ids) == len(set(ids))  # visible, and never twice


def test_waived_courses_are_not_remaining_work():
    cat = catalog([course(1, 2, teaches=["a"], hours=5), course(2, 2, teaches=["b"], hours=7)], [stage("s", 1, 2)])
    assert plan(cat, state=known("a")).estimated_hours == 7


# ─── Prerequisites are never claimed on the learner's behalf ────────────────

def test_declaring_a_course_does_not_claim_its_prerequisites():
    """Course 2 (declared) needs course 1, which the route does not list. Course 1
    is pulled in as required: the learner said they know 2, not 1."""
    cat = catalog([course(1, 2, teaches=["basics"]), course(2, 2, teaches=["advanced"], prereqs=[1])],
                  [stage("s", 2)])
    p = plan(cat, state=known("advanced"))
    assert states(p) == {1: STATE_REQUIRED, 2: STATE_WAIVED}
    assert [c.course_id for c in p.stages[0].courses] == [1, 2]      # prerequisite first
    assert p.stages[0].courses[0].reason == "prerequisite"


def test_a_prerequisite_the_learner_also_declared_is_not_added():
    cat = catalog([course(1, 2, teaches=["basics"]), course(2, 2, teaches=["advanced"], prereqs=[1])],
                  [stage("s", 2)])
    p = plan(cat, state=known("advanced", "basics"))
    assert states(p) == {2: STATE_WAIVED}   # 1 is known and not on the route: nothing to add


def test_a_required_course_still_pulls_in_its_unknown_prerequisite():
    cat = catalog([course(1, 2, teaches=["basics"]), course(2, 2, teaches=["advanced"], prereqs=[1])],
                  [stage("s", 2)])
    assert states(plan(cat, state=known("something-else"))) == {1: STATE_REQUIRED, 2: STATE_REQUIRED}


def test_a_known_prerequisite_is_not_added_for_a_required_course():
    cat = catalog([course(1, 2, teaches=["basics"]), course(2, 2, teaches=["advanced"], prereqs=[1])],
                  [stage("s", 2)])
    assert states(plan(cat, state=known("basics"))) == {2: STATE_REQUIRED}


# ─── Multimodal ─────────────────────────────────────────────────────────────

def _multimodal_catalog():
    return catalog(
        [course(1, 1, fields=["nlp"], teaches=["llms"]), course(2, 1, fields=["nlp"], teaches=["prompting"]),
         course(3, 3, fields=["multimodal"], teaches=["multimodal"], prereqs=[1])],
        [(stage("nlp-stage", 1, 2), "nlp"), (stage("mm-stage", 3), "multimodal")],
    )


def test_a_beginner_can_choose_multimodal_and_is_routed_through_a_prerequisite_field():
    p = plan(_multimodal_catalog(), level="beginner", fields=["multimodal"])
    assert "nlp" in p.effective_field_slugs                      # not blocked: routed
    codes = [a.code for a in p.advisories]
    assert ADVISORY_PREREQUISITE_ROUTE_ADDED in codes
    assert ADVISORY_PREREQUISITES_RECOMMENDED in codes           # "ideally two" is still recommended
    assert states(p)[3] == STATE_REQUIRED


def test_declared_skills_that_cover_a_prerequisite_field_are_respected():
    """The learner knows what NLP's courses teach, so NLP is not added to the route
    and its courses are not asked of them again - but the second modality is still
    recommended, exactly as the configuration says."""
    p = plan(_multimodal_catalog(), level="beginner", fields=["multimodal"], state=known("llms", "prompting"))
    assert p.effective_field_slugs == ["multimodal"]             # NLP counted as known, not re-added
    assert ADVISORY_PREREQUISITE_ROUTE_ADDED not in [a.code for a in p.advisories]
    recommended = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITES_RECOMMENDED)
    assert set(recommended.params["suggested"]) == {"computer-vision", "speech"}
    assert states(p) == {3: STATE_REQUIRED}                       # the multimodal course itself remains


def test_partly_covering_a_prerequisite_field_is_not_enough():
    p = plan(_multimodal_catalog(), level="beginner", fields=["multimodal"], state=known("llms"))
    assert "nlp" in p.effective_field_slugs                      # one of two NLP courses: 50% < 60%
    assert states(p)[1] == STATE_WAIVED and states(p)[2] == STATE_REQUIRED


# ─── The API, against the shipped configuration ─────────────────────────────

def _profile(client, who, level="beginner", fields=("nlp",), goal="ai-engineer", **extra):
    resp = client.put(f"{API}/my-profile", headers=who["headers"],
                      json={"level": level, "fields": list(fields), "career_goal": goal, **extra})
    assert resp.status_code == 200, resp.text
    return resp.json()


def _build(client, who, **kw):
    _profile(client, who, **{k: v for k, v in kw.items() if k != "known_skills"},
             **({"known_skills": kw["known_skills"]} if "known_skills" in kw else {}))
    resp = client.put(f"{API}/my-path", headers=who["headers"], json={})
    assert resp.status_code == 200, resp.text
    return resp.json()


def _by_slug(path):
    return {c["course"]["slug"]: c for s in path["stages"] for c in s["courses"]}


def _states(path):
    return {slug: c["state"] for slug, c in _by_slug(path).items()}


# Known skills ---------------------------------------------------------------

def test_a_learner_can_save_known_skills_and_they_persist(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    body = _profile(learn_client, who, known_skills=["llms", "rag"])
    assert {s["slug"] for s in body["known_skills"]} == {"llms", "rag"}

    again = learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()
    assert {s["slug"] for s in again["known_skills"]} == {"llms", "rag"}

    rows = learn_db.query(LearnerSkill).filter(LearnerSkill.user_id == who["id"]).all()
    assert {(r.status, r.source) for r in rows} == {("known", "self_declared")}   # a claim, not mastery
    assert len(rows) == 2


def test_unknown_skill_ids_are_rejected_and_nothing_is_saved(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    resp = learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"known_skills": ["rag", "telepathy"]})
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "unknown_skill"
    assert learn_db.query(LearnerSkill).filter(LearnerSkill.user_id == who["id"]).count() == 0

    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["telepathy"]})
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "unknown_skill"


def test_a_malformed_skill_identifier_is_refused(learn_client, legacy_catalog):
    who = register(learn_client)
    for bad in ("../etc/passwd", "RAG", "a b", "x" * 80):
        resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": [bad]})
        assert resp.status_code == 422, bad


def test_skill_selections_are_scoped_to_the_learner(learn_client, legacy_catalog):
    alice, bob = register(learn_client), register(learn_client)
    _profile(learn_client, alice, known_skills=["llms", "rag"])
    _profile(learn_client, bob, known_skills=["prompt-engineering"])

    mine = learn_client.get(f"{API}/my-skills", headers=alice["headers"]).json()
    theirs = learn_client.get(f"{API}/my-skills", headers=bob["headers"]).json()
    assert {k["skill"]["slug"] for k in mine["known"]} == {"llms", "rag"}
    assert {k["skill"]["slug"] for k in theirs["known"]} == {"prompt-engineering"}


def test_skill_endpoints_require_a_signed_in_learner(learn_client, legacy_catalog):
    assert learn_client.get(f"{API}/my-skills").status_code == 401
    assert learn_client.put(f"{API}/my-skills", json={"skills": []}).status_code == 401


def test_putting_skills_replaces_the_declared_list(learn_client, legacy_catalog):
    who = register(learn_client)
    learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["llms", "rag"]})
    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["rag", "embeddings"]})
    assert resp.status_code == 200
    assert {k["skill"]["slug"] for k in resp.json()["known"]} == {"rag", "embeddings"}
    # No complete profile yet: the skills are saved and there is no roadmap to rebuild.
    assert resp.json()["path"] is None and resp.json()["roadmap_updated"] is False


def test_duplicate_skills_in_a_request_collapse_to_one_row(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["rag", "rag", "rag"]})
    assert learn_db.query(LearnerSkill).filter(LearnerSkill.user_id == who["id"]).count() == 1


def test_evidence_from_better_sources_is_not_erased_by_editing_the_declared_list(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    rag = learn_db.query(Skill).filter(Skill.slug == "rag").one()
    learn_db.add(LearnerSkill(user_id=who["id"], skill_id=rag.id, status="mastered", source="assessment"))
    learn_db.commit()
    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": []})
    known = {k["skill"]["slug"]: (k["status"], k["source"]) for k in resp.json()["known"]}
    assert known["rag"] == ("mastered", "assessment")


# What to ask ---------------------------------------------------------------

def test_the_skills_to_ask_about_come_from_the_catalogue(learn_client, legacy_catalog):
    resp = learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer", "field": "nlp", "level": "beginner"})
    assert resp.status_code == 200
    options = {o["slug"]: o for o in resp.json()}
    assert {"llms", "rag", "embeddings", "prompt-engineering", "ai-agents"} <= set(options)
    assert options["rag"]["group"]["slug"] == "nlp" and options["rag"]["kind"] == "skill"
    assert options["evaluation"]["is_required"] is True            # the goal names it
    assert all(o["name"] for o in options.values())


def test_tools_are_told_apart_from_skills(learn_client, legacy_catalog):
    options = {o["slug"]: o for o in learn_client.get(
        f"{API}/skills", params={"career_goal": "ai-engineer", "field": "nlp"}).json()}
    for tool in ("langchain", "langgraph", "fastapi"):
        assert options[tool]["kind"] == "tool", tool
        assert options[tool]["group"] is None                       # filed under "tools", not a field
    assert options["rag"]["kind"] == "skill"
    listed = [o["kind"] for o in learn_client.get(
        f"{API}/skills", params={"career_goal": "ai-engineer", "field": "nlp"}).json()]
    assert listed == sorted(listed, key=lambda k: k == "tool")      # capabilities first, tools after


def test_knowing_a_tool_does_not_waive_the_skill_it_is_used_for(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, known_skills=["langchain", "qdrant", "llamaindex"])
    states_ = _states(path)
    assert states_["rag-knowledge-systems"] == STATE_REQUIRED       # the skill course is still to do
    assert states_["langchain"] == STATE_REQUIRED                    # langchain also teaches `llms`, undeclared


def test_skill_options_depend_on_the_route(learn_client, legacy_catalog):
    nlp = {o["slug"] for o in learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer", "field": "nlp"}).json()}
    core = {o["slug"] for o in learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer"}).json()}
    assert "rag" in nlp and "rag" not in core                      # RAG lives in the NLP route


def test_unknown_goal_or_field_for_skill_options_is_a_clean_error(learn_client, legacy_catalog):
    assert learn_client.get(f"{API}/skills", params={"career_goal": "chef"}).status_code == 422
    assert learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer", "field": "alchemy"}).status_code == 422
    assert learn_client.get(f"{API}/skills").status_code == 422     # a goal is required


# Path generation ---------------------------------------------------------------

def test_scenario_a_known_courses_are_shown_as_already_known_and_not_required(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, known_skills=["llms"])
    c = _by_slug(path)
    assert c["llm-integration"]["state"] == "waived" and c["llm-integration"]["reason"] == "known_skills"
    assert [s["slug"] for s in c["llm-integration"]["known_skills"]] == ["llms"]      # why it is waived
    # Foundations teaches llms *and* system-design: partly known, still to do - and it says what is known.
    assert c["ai-engineering-foundations"]["state"] == "required"
    assert [s["slug"] for s in c["ai-engineering-foundations"]["known_skills"]] == ["llms"]
    assert path["progress"]["path_known"] >= 1
    assert "llm-integration" in {x["course"]["slug"] for s in path["stages"] for x in s["courses"]}   # not deleted


def test_a_learner_with_no_declared_skills_gets_every_route_course_as_required(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who)
    assert STATE_WAIVED not in set(_states(path).values())


def test_scenario_b_the_roadmap_begins_with_what_remains(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="intermediate",
                  known_skills=["llms", "prompt-engineering", "embeddings", "semantic-search"])
    c = _by_slug(path)
    assert c["llm-integration"]["state"] == "waived"
    assert c["prompt-engineering"]["state"] == "waived"
    assert c["embeddings-semantic-search"]["state"] == "waived"
    first = path["current_course"]
    assert first is not None and c[first["course"]["slug"]]["state"] == "required"


def test_prerequisites_still_apply_to_a_declared_course(learn_client, legacy_catalog):
    """RAG & Knowledge Systems is declared; its prerequisite (LLM Integration) is not.
    The prerequisite stays on the route as required."""
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner", known_skills=["rag", "retrieval"])
    c = _by_slug(path)
    assert c["rag-knowledge-systems"]["state"] == "waived"
    assert c["llm-integration"]["state"] == "required"


def test_no_course_appears_twice(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="intermediate", fields=("nlp", "multimodal"),
                  known_skills=["llms", "rag", "retrieval"])
    ids = [c["course"]["id"] for s in path["stages"] for c in s["courses"]]
    assert len(ids) == len(set(ids))


# Regeneration ---------------------------------------------------------------

def test_scenario_c_editing_skills_rebuilds_the_roadmap_without_touching_progress(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], legacy_catalog, 1)                # finished AI Engineering Foundations
    before = _build(learn_client, who, level="intermediate", known_skills=["llms"])
    assert _by_slug(before)["ai-engineering-foundations"]["state"] == "completed"

    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["llms", "rag", "retrieval"]})
    assert resp.status_code == 200
    after = resp.json()["path"]
    assert resp.json()["roadmap_updated"] is True
    assert after["id"] != before["id"]                                    # a fresh path...
    c = _by_slug(after)
    assert c["ai-engineering-foundations"]["state"] == "completed"        # ...with progress intact
    assert c["rag-knowledge-systems"]["state"] == "waived"                # the new declaration applied
    assert c["llm-integration"]["state"] == "waived"

    paths = learn_db.query(LearningPath).filter(LearningPath.user_id == who["id"]).all()
    assert sorted(p.status for p in paths) == ["active", "archived"]      # history kept, one live path
    assert learn_client.get(f"{API}/my-path", headers=who["headers"]).json()["id"] == after["id"]


def test_removing_a_declared_skill_makes_its_course_required_again_but_never_undoes_completion(
        learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], legacy_catalog, 2)                # llm-integration finished for real
    _build(learn_client, who, level="intermediate", known_skills=["llms", "rag", "retrieval"])
    path = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": []}).json()["path"]
    c = _by_slug(path)
    assert c["llm-integration"]["state"] == "completed"
    assert c["rag-knowledge-systems"]["state"] == "required"


def test_the_profile_page_edit_flow_matches_the_onboarding_one(learn_client, legacy_catalog):
    """Saving skills through PUT /my-profile then rebuilding gives the same roadmap
    as PUT /my-skills - there is one rule, however it is reached."""
    a, b = register(learn_client), register(learn_client)
    via_profile = _build(learn_client, a, level="intermediate", known_skills=["llms", "rag", "retrieval"])
    _profile(learn_client, b, level="intermediate")
    via_skills = learn_client.put(f"{API}/my-skills", headers=b["headers"],
                                  json={"skills": ["llms", "rag", "retrieval"]}).json()["path"]
    assert _states(via_profile) == _states(via_skills)


def test_saving_skills_before_onboarding_is_complete_does_not_invent_a_path(learn_client, legacy_catalog):
    who = register(learn_client)
    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["llms"]})
    assert resp.status_code == 200 and resp.json()["path"] is None
    assert learn_client.get(f"{API}/my-path", headers=who["headers"]).status_code == 404


# Multimodal ---------------------------------------------------------------

def test_scenario_d_a_beginner_can_choose_multimodal_and_declared_nlp_is_respected(learn_client, legacy_catalog):
    who = register(learn_client)
    everything_nlp_teaches = ["llms", "prompt-engineering", "rag", "retrieval", "embeddings", "semantic-search",
                              "ai-agents", "langchain", "langgraph", "llamaindex", "qdrant", "vector-databases"]
    path = _build(learn_client, who, level="beginner", fields=("multimodal",), known_skills=everything_nlp_teaches)
    assert [f["slug"] for f in path["fields"]] == ["multimodal"]            # selectable, not blocked
    assert [f["slug"] for f in path["effective_fields"]] == ["multimodal"]  # NLP known: not routed back through
    assert "prerequisite_route_added" not in [a["code"] for a in path["advisories"]]
    assert "nlp-llm" not in [s["slug"] for s in path["stages"]]             # its stages are not asked of them again
    recommended = next(a for a in path["advisories"] if a["code"] == "prerequisites_recommended")
    assert set(recommended["params"]["suggested"]) == {"computer-vision", "speech"}   # the config still recommends two
    assert _by_slug(path)["multimodal-ai"]["state"] == "required"


def test_a_beginner_choosing_multimodal_without_declaring_anything_is_routed_not_blocked(learn_client, legacy_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner", fields=("multimodal",))
    codes = [a["code"] for a in path["advisories"]]
    assert "field_above_level" in codes and "prerequisite_route_added" in codes
    assert "nlp-llm" in [s["slug"] for s in path["stages"]]                 # the route to it is in the roadmap
    assert [f["slug"] for f in path["effective_fields"]] == ["nlp", "multimodal"]   # and survives a reload


# Dashboard / home ---------------------------------------------------------------

def test_the_dashboard_has_an_empty_state_before_a_roadmap_exists(learn_client, legacy_catalog):
    who = register(learn_client)
    assert learn_client.get(f"{API}/my-path", headers=who["headers"]).status_code == 404
    profile = learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()
    assert profile["needs_onboarding"] is True and profile["has_active_path"] is False


def test_the_roadmap_reports_progress_current_and_next_course(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], legacy_catalog, 1)
    path = _build(learn_client, who, level="beginner", known_skills=["llms"])
    progress = path["progress"]
    assert progress["path_completed"] == 1
    assert progress["path_total"] >= 2
    assert progress["path_known"] >= 1
    assert progress["path_pct"] == pytest.approx(100.0 * 1 / progress["path_total"], abs=0.2)

    current, nxt = path["current_course"], path["next_course"]
    assert current and nxt and current["course"]["id"] != nxt["course"]["id"]
    c = _by_slug(path)
    assert c[current["course"]["slug"]]["state"] == "required"
    assert c[nxt["course"]["slug"]]["state"] == "required"
    assert current["stage_slug"] and current["stage_title"]

    # Path order: the next course comes after the current one, nothing required in between.
    order = [x["course"]["slug"] for s in path["stages"] for x in s["courses"] if x["state"] == "required"]
    assert order.index(nxt["course"]["slug"]) == order.index(current["course"]["slug"]) + 1
    assert order[0] == current["course"]["slug"]                    # nothing started, so the first one


def test_a_course_already_under_way_is_the_current_one(learn_client, legacy_catalog, learn_db):
    from app.models.progress import UserProgress
    who = register(learn_client)
    topic_id, lesson_id = legacy_catalog["level_lessons"][3][0]
    learn_db.add(UserProgress(user_id=who["id"], topic_id=topic_id, lessons_completed=[lesson_id], exercises_completed=[]))
    learn_db.commit()
    path = _build(learn_client, who, level="intermediate")
    assert path["current_course"]["course"]["slug"] == "rag-knowledge-systems"


def test_a_finished_roadmap_has_no_current_or_next_course(learn_client, legacy_catalog, learn_db):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner")
    for slug, c in _by_slug(path).items():
        if c["state"] != "required":
            continue
        source = learn_db.query(Course).filter_by(slug=slug).one()
        if source.kind == "track_level":
            complete_level(learn_db, who["id"], legacy_catalog, source.track_level.order)
        else:
            complete_tool(learn_db, who["id"], legacy_catalog, slug)
    done = learn_client.get(f"{API}/my-path", headers=who["headers"]).json()
    assert done["current_course"] is None and done["next_course"] is None
    assert done["progress"]["path_pct"] == 100.0
    assert done["is_complete"] is True
    assert path["is_complete"] is False                            # ...and not before


# Observability ---------------------------------------------------------------

def test_events_carry_counts_never_the_answers(learn_client, legacy_catalog, caplog):
    who = register(learn_client)
    with caplog.at_level(logging.INFO):
        _build(learn_client, who, level="intermediate", known_skills=["llms", "rag"])
    events = {r.event: r for r in caplog.records if getattr(r, "event", None)}
    assert {"learning_onboarding_started", "career_goal_selected", "field_selected",
            "known_skills_selected", "roadmap_generated"} <= set(events)
    assert events["known_skills_selected"].known_skill_count == 2
    text = " ".join(f"{r.getMessage()} {r.__dict__}" for r in caplog.records if getattr(r, "event", None))
    assert "llms" not in text and "'rag'" not in text                    # counts, not the ticked list

    generated = next(r for r in caplog.records if r.getMessage() == "learning path generated")
    assert generated.known_skill_count == 2
    assert generated.waived_course_count >= 0 and generated.required_course_count > 0
    assert generated.roadmap_generation_success is True


def test_a_second_build_is_reported_as_an_update(learn_client, legacy_catalog, caplog):
    who = register(learn_client)
    _build(learn_client, who, level="intermediate")
    with caplog.at_level(logging.INFO):
        learn_client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": ["llms"]})
    assert "roadmap_updated" in {getattr(r, "event", None) for r in caplog.records}


# Migration ---------------------------------------------------------------

def test_skills_have_a_kind_and_the_check_constraint_holds(learn_client, legacy_catalog, learn_db):
    from sqlalchemy.exc import IntegrityError
    kinds = {s.slug: s.kind for s in learn_db.query(Skill).all()}
    assert kinds["langchain"] == "tool" and kinds["rag"] == "skill"
    learn_db.add(Skill(slug="bogus", name="Bogus", kind="gadget"))
    with pytest.raises(IntegrityError):
        learn_db.flush()
    learn_db.rollback()


def test_a_learner_cannot_hold_the_same_skill_twice(learn_client, legacy_catalog, learn_db):
    from sqlalchemy.exc import IntegrityError
    who = register(learn_client)
    rag = learn_db.query(Skill).filter(Skill.slug == "rag").one()
    learn_db.add(LearnerSkill(user_id=who["id"], skill_id=rag.id))
    learn_db.flush()
    learn_db.add(LearnerSkill(user_id=who["id"], skill_id=rag.id))
    with pytest.raises(IntegrityError):
        learn_db.flush()
    learn_db.rollback()


def test_status_and_source_are_constrained(learn_client, legacy_catalog, learn_db):
    from sqlalchemy.exc import IntegrityError
    who = register(learn_client)
    rag = learn_db.query(Skill).filter(Skill.slug == "rag").one()
    learn_db.add(LearnerSkill(user_id=who["id"], skill_id=rag.id, status="wizard"))
    with pytest.raises(IntegrityError):
        learn_db.flush()
    learn_db.rollback()
