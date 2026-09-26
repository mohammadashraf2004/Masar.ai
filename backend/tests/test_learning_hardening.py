"""
Hardening pass over the personalised roadmap: the rules restated as end-to-end
scenarios against the shipped configuration (`learn_catalog` runs the real seed).

Where an expectation depends on what a course teaches, it is computed from the
catalogue rows by the plain rule below - not read back from the generator - so
these tests would catch the generator drifting from the rule:

    a course is "Already know" (waived) iff it teaches at least one skill and
    the learner declared EVERY skill it teaches.

Nothing here changes behaviour; it pins it.
"""
import pytest

from app.models.learning_path import Course, LearningPath, Skill
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import complete_level, register
from tests.test_learning_personalized import API, _build, _by_slug, _profile, _states


# ─── Oracles ────────────────────────────────────────────────────────────────

def _teaches(db):
    """course slug -> the skill slugs it teaches, straight from the rows."""
    return {c.slug: {link.skill.slug for link in c.skill_links if link.relation == "teaches"}
            for c in db.query(Course).all()}


def _expected_waived(db, declared, in_path):
    return {slug for slug, taught in _teaches(db).items()
            if slug in in_path and taught and taught <= set(declared)}


def _waived(path):
    return {slug for slug, state in _states(path).items() if state == "waived"}


def _put_skills(client, who, skills):
    resp = client.put(f"{API}/my-skills", headers=who["headers"], json={"skills": list(skills)})
    assert resp.status_code == 200, resp.text
    assert resp.json()["roadmap_updated"] is True
    return resp.json()["path"]


def _reload(client, who):
    resp = client.get(f"{API}/my-path", headers=who["headers"])
    assert resp.status_code == 200, resp.text
    return resp.json()


def _shape(path):
    """Everything a reload must reproduce: what is on the roadmap, in which
    order and state, the route, the advisories, and every server-decided number."""
    step = lambda s: s and (s["course"]["slug"], s["stage_slug"])  # noqa: E731
    return {
        "id": path["id"],
        "stages": [(s["slug"], s["status"], [(c["course"]["slug"], c["state"], c["reason"],
                                              [k["slug"] for k in c["known_skills"]]) for c in s["courses"]])
                   for s in path["stages"]],
        "fields": [f["slug"] for f in path["fields"]],
        "effective_fields": [f["slug"] for f in path["effective_fields"]],
        "advisories": [(a["code"], a["params"]) for a in path["advisories"]],
        "progress": path["progress"],
        "current": step(path["current_course"]),
        "next": step(path["next_course"]),
        "is_complete": path["is_complete"],
        "current_stage": path["current_stage_slug"],
    }


def _assert_counts_are_honest(path):
    """The server's counts agree with the states it reports - so a client that
    only displays them shows the truth."""
    states = list(_states(path).values())
    progress = path["progress"]
    assert progress["path_completed"] == states.count("completed")
    assert progress["path_total"] == states.count("completed") + states.count("required")
    assert progress["path_known"] == states.count("waived")
    assert path["is_complete"] is (states.count("required") == 0 and progress["path_total"] > 0)


def _live_paths(db, user_id):
    db.expire_all()
    rows = db.query(LearningPath).filter(LearningPath.user_id == user_id).all()
    return [p for p in rows if p.status == "active"], [p for p in rows if p.status == "archived"]


# ─── Scenarios A-F ──────────────────────────────────────────────────────────

def test_roadmap_scenarios_a_to_f_in_one_learners_life(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    everything = set(_teaches(learn_db)["rag-knowledge-systems"]) | {"llms"}

    # A - nothing declared: nothing is waived, and nothing is claimed for them.
    path = _build(learn_client, who, level="beginner")
    in_path = set(_states(path))
    assert _waived(path) == set() and path["progress"]["path_known"] == 0
    assert path["is_complete"] is False and path["current_course"] is not None
    assert _shape(_reload(learn_client, who)) == _shape(path)
    _assert_counts_are_honest(path)

    # B - one skill: only a course whose *every* skill that is waives; the rest
    # that touch it are partly known and still to do.
    path = _put_skills(learn_client, who, ["llms"])
    assert _waived(path) == _expected_waived(learn_db, ["llms"], in_path) != set()
    partly = _by_slug(path)["ai-engineering-foundations"]                 # teaches llms AND system-design
    assert partly["state"] == "required"
    assert [k["slug"] for k in partly["known_skills"]] == ["llms"]
    assert len(partly["course"]["skills"]) == 2                            # "1 of 2 skills here"
    _assert_counts_are_honest(path)

    # C - every skill of a course: it is waived; its prerequisite is judged on its own.
    path = _put_skills(learn_client, who, ["rag", "retrieval"])
    assert _states(path)["rag-knowledge-systems"] == "waived"
    assert _states(path)["llm-integration"] == "required"                  # its prerequisite was NOT claimed
    assert _states(path)["ai-engineering-foundations"] == "required"
    path = _put_skills(learn_client, who, sorted(everything))
    assert _states(path)["rag-knowledge-systems"] == "waived" and _states(path)["llm-integration"] == "waived"

    # D - finish courses, then declare more: what was finished stays finished.
    complete_level(learn_db, who["id"], learn_catalog, 1)
    complete_level(learn_db, who["id"], learn_catalog, 3)                  # rag-knowledge-systems, for real
    path = _put_skills(learn_client, who, sorted(everything | {"embeddings", "semantic-search"}))
    states = _states(path)
    assert states["ai-engineering-foundations"] == "completed"
    assert states["rag-knowledge-systems"] == "completed"                  # completed wins over "already know"
    assert _by_slug(path)["ai-engineering-foundations"]["completion_pct"] == 100.0
    assert states["embeddings-semantic-search"] == "waived"                # the new declaration applied
    _assert_counts_are_honest(path)
    before_e = _shape(path)

    # E - remove declared skills: waived courses are required again; completion is untouched.
    path = _put_skills(learn_client, who, [])
    states = _states(path)
    assert "waived" not in states.values()
    assert states["ai-engineering-foundations"] == "completed" and states["rag-knowledge-systems"] == "completed"
    assert states["embeddings-semantic-search"] == "required" and states["llm-integration"] == "required"
    assert path["progress"]["path_known"] == 0 and path["progress"]["path_completed"] == 2
    assert _shape(path) != before_e
    _assert_counts_are_honest(path)

    # F - "reload the app": the saved roadmap reads back identically, and there
    # is exactly one live roadmap however many times it was rebuilt.
    assert _shape(_reload(learn_client, who)) == _shape(path)
    active, archived = _live_paths(learn_db, who["id"])
    assert len(active) == 1 and active[0].id == path["id"]
    assert len(archived) == 5                                              # six builds in all: five kept as history
    assert learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()["has_active_path"] is True


def test_the_current_and_next_course_are_recalculated_when_skills_change(learn_client, learn_catalog):
    who = register(learn_client)
    first = _build(learn_client, who, level="beginner")
    order = [c["course"]["slug"] for s in first["stages"] for c in s["courses"] if c["state"] == "required"]
    assert first["current_course"]["course"]["slug"] == order[0]

    # Declare exactly what the current course teaches: it is waived, so the
    # roadmap moves on to the next thing that is genuinely still to do.
    declared = {s["slug"] for s in first["current_course"]["course"]["skills"]}
    after = _put_skills(learn_client, who, sorted(declared))
    assert _states(after)[order[0]] == "waived"
    assert after["current_course"]["course"]["slug"] != order[0]
    still_required = [c["course"]["slug"] for s in after["stages"] for c in s["courses"] if c["state"] == "required"]
    assert after["current_course"]["course"]["slug"] == still_required[0]
    assert after["next_course"]["course"]["slug"] == still_required[1]


def test_every_rebuild_keeps_exactly_one_active_roadmap(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    for skills in (["llms"], ["llms", "rag"], ["llms"], [], ["rag"]):
        _put_skills(learn_client, who, skills)
        active, _ = _live_paths(learn_db, who["id"])
        assert len(active) == 1


# ─── Multimodal ─────────────────────────────────────────────────────────────

def test_multimodal_keeps_its_route_and_prerequisite_metadata_through_regeneration_and_reload(
        learn_client, learn_catalog):
    who = register(learn_client)
    built = _build(learn_client, who, level="beginner", fields=("multimodal",))
    codes = {a["code"] for a in built["advisories"]}
    assert {"field_above_level", "prerequisite_route_added"} <= codes        # advised and routed, not blocked
    assert [f["slug"] for f in built["effective_fields"]] == ["nlp", "multimodal"]
    assert _states(built)["multimodal-ai"] == "required"                     # never blocked
    assert _shape(_reload(learn_client, who)) == _shape(built)               # header/path metadata survive a reload

    # Regenerating with unrelated skills keeps the same route and the same advice.
    again = _put_skills(learn_client, who, ["observability"])
    assert [f["slug"] for f in again["effective_fields"]] == ["nlp", "multimodal"]
    assert {"field_above_level", "prerequisite_route_added"} <= {a["code"] for a in again["advisories"]}
    route = next(a for a in again["advisories"] if a["code"] == "prerequisite_route_added")
    assert route["params"] == {"field": "multimodal", "added": ["nlp"]}      # which field needed which
    assert _shape(_reload(learn_client, who)) == _shape(again)


def test_the_client_never_supplies_completion_it_only_reads_it(learn_client, learn_catalog):
    """The roadmap has no writable field for completion, current/next course or
    progress counts - the server derives every one from lessons."""
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    forged = learn_client.put(f"{API}/my-path", headers=who["headers"], json={
        "is_complete": True, "current_course": None, "next_course": None,
        "progress": {"path_pct": 100.0, "path_completed": 99, "path_total": 99},
    })
    assert forged.status_code == 200
    body = forged.json()
    assert body["is_complete"] is False and body["current_course"] is not None
    assert body["progress"]["path_completed"] == 0 and body["progress"]["path_total"] != 99


# ─── Skill vs tool ──────────────────────────────────────────────────────────

def test_course_technologies_are_tools_and_capabilities_are_skills(learn_catalog, learn_db):
    kinds = {s.slug: s.kind for s in learn_db.query(Skill).all()}
    assert {slug for slug, kind in kinds.items() if kind == "tool"} == {
        "langchain", "langgraph", "llamaindex", "qdrant", "fastapi", "python", "numpy",
        "pandas", "scikit-learn", "pytorch", "transformers", "docker",
    }
    assert {"rag", "embeddings", "vector-databases", "llms"} <= {s for s, k in kinds.items() if k == "skill"}
    assert kinds["cloud-deployment"] == "skill" and kinds["ci-cd"] == "skill"


def test_a_tool_is_never_taken_for_the_capability_and_the_capability_never_for_the_tool(
        learn_client, learn_catalog, learn_db):
    """LangChain must not satisfy RAG, and RAG must not satisfy LangChain. A
    course that teaches both a capability and a tool needs both declared."""
    teaches = _teaches(learn_db)
    langchain_course = teaches["langchain"]
    assert "langchain" in langchain_course and len(langchain_course) > 1
    capabilities = langchain_course - {"langchain"}

    who = register(learn_client)
    path = _build(learn_client, who, level="beginner", known_skills=["langchain", "langgraph", "llamaindex"])
    assert _states(path)["rag-knowledge-systems"] == "required"              # the tools said nothing about RAG
    assert _states(path)["langchain"] == "required"                          # ...nor did they cover their own course

    path = _put_skills(learn_client, who, sorted(capabilities))              # every capability, but not the tool
    assert _states(path)["langchain"] == "required"
    assert [k["slug"] for k in _by_slug(path)["langchain"]["known_skills"]] == sorted(capabilities)

    path = _put_skills(learn_client, who, sorted(capabilities | {"langchain"}))
    assert _states(path)["langchain"] == "waived"


def test_the_kind_travels_with_a_skill_through_every_learner_facing_response(learn_client, learn_catalog):
    who = register(learn_client)
    profile = _profile(learn_client, who, known_skills=["rag", "langchain"])
    assert {s["slug"]: s["kind"] for s in profile["known_skills"]} == {"rag": "skill", "langchain": "tool"}
    mine = learn_client.get(f"{API}/my-skills", headers=who["headers"]).json()
    assert {k["skill"]["slug"]: k["skill"]["kind"] for k in mine["known"]} == {"rag": "skill", "langchain": "tool"}
    options = learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer", "field": "nlp"}).json()
    assert {o["slug"]: o["kind"] for o in options if o["slug"] in ("rag", "langchain")} == {
        "rag": "skill", "langchain": "tool"}


def test_the_declared_list_has_no_field_through_which_a_kind_could_be_chosen(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    resp = learn_client.put(f"{API}/my-skills", headers=who["headers"],
                            json={"skills": ["rag"], "kind": "tool", "kinds": {"rag": "tool"}})
    assert resp.status_code == 200
    assert learn_db.query(Skill).filter(Skill.slug == "rag").one().kind == "skill"


# ─── API contract ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("body", [
    {},                                    # forgot the key: not "knows nothing"
    {"skills": "rag"},                     # a string, not a list
    {"skills": None},
    {"skills": [1, 2]},
    {"skills": ["rag", {"slug": "rag"}]},
    {"skills": ["x"] * 101},               # over the bound
])
def test_a_malformed_skill_list_is_a_422_and_changes_nothing(learn_client, learn_catalog, learn_db, body):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    _put_skills(learn_client, who, ["rag", "llms"])
    assert learn_client.put(f"{API}/my-skills", headers=who["headers"], json=body).status_code == 422
    mine = learn_client.get(f"{API}/my-skills", headers=who["headers"]).json()
    assert {k["skill"]["slug"] for k in mine["known"]} == {"rag", "llms"}


def test_saving_the_same_skills_twice_gives_the_same_roadmap(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who, level="beginner")
    first = _put_skills(learn_client, who, ["llms", "rag"])
    second = _put_skills(learn_client, who, ["rag", "llms", "rag"])           # same set, other order, a duplicate
    shape = lambda p: {k: v for k, v in _shape(p).items() if k != "id"}       # noqa: E731
    assert shape(first) == shape(second)


def test_one_learners_skills_never_change_anothers_roadmap(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a, level="beginner")
    before = _shape(_reload(learn_client, a))
    _build(learn_client, b, level="beginner")
    _put_skills(learn_client, b, ["llms", "rag", "retrieval"])
    assert _shape(_reload(learn_client, a)) == before


def test_the_catalogue_skill_list_is_public_and_the_learner_lists_are_not(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/skills", params={"career_goal": "ai-engineer"}).status_code == 200
    for method, url in (("get", "my-skills"), ("put", "my-skills"), ("get", "my-path"), ("put", "my-path"),
                        ("get", "my-progress"), ("get", "my-profile")):
        resp = getattr(learn_client, method)(f"{API}/{url}", **({"json": {"skills": []}} if method == "put" else {}))
        assert resp.status_code == 401, (method, url)
