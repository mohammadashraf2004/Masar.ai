"""
The learning-path API, end to end, against the shipped configuration.

`learn_catalog` builds the same content sources production has (the AI
Developer track, the tool courses — a handful with lessons, most as shells) and
runs the real seed over them, so these tests assert on what learners would
actually get: which stages an AI Engineer — Computer Vision route has, what a
beginner who asks for Multimodal is told, and so on.
"""
import pytest

from app.models.learning_path import (
    CareerRole, LearningField, LearningPath, LearningProfile,
)
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import complete_level, complete_tool, register

API = "/api/v1/learning"


def _profile(client, who, level="intermediate", fields=("nlp",), goal="ai-engineer"):
    resp = client.put(f"{API}/my-profile", headers=who["headers"],
                      json={"level": level, "fields": list(fields), "career_goal": goal})
    assert resp.status_code == 200, resp.text
    return resp.json()


def _build(client, who, **kw):
    _profile(client, who, **kw)
    resp = client.put(f"{API}/my-path", headers=who["headers"], json={})
    assert resp.status_code == 200, resp.text
    return resp.json()


def _slugs(path):
    return [s["slug"] for s in path["stages"]]


def _stage(path, slug):
    return next(s for s in path["stages"] if s["slug"] == slug)


def _states(path):
    return {c["course"]["slug"]: c["state"] for s in path["stages"] for c in s["courses"]}


# ─── Levels, fields, career goals ───────────────────────────────────────────

def test_levels_are_the_three_stable_slugs_in_rank_order(learn_client):
    levels = learn_client.get(f"{API}/levels").json()
    assert [l["slug"] for l in levels] == ["beginner", "intermediate", "advanced"]
    assert [l["rank"] for l in levels] == [1, 2, 3]
    assert all(l["name"] and l["name_ar"] and l["description"] and l["description_ar"] for l in levels)


def test_fields_are_served_from_the_backend_with_both_languages(learn_client, learn_catalog):
    fields = {f["slug"]: f for f in learn_client.get(f"{API}/fields").json()}
    assert list(fields) == ["data", "machine-learning", "nlp", "computer-vision", "speech", "multimodal"]
    assert fields["computer-vision"]["name"] == "Computer Vision"
    assert fields["computer-vision"]["name_ar"] == "الرؤية الحاسوبية"
    assert fields["nlp"]["name_ar"]  # technical names keep an Arabic gloss for the terminology modes


def test_multimodal_is_an_advanced_field_with_a_prerequisite_rule(learn_client, learn_catalog):
    fields = {f["slug"]: f for f in learn_client.get(f"{API}/fields").json()}
    mm = fields["multimodal"]
    assert mm["is_advanced"] is True
    assert mm["min_level"]["slug"] == "advanced"
    assert {p["slug"] for p in mm["prerequisites"]} == {"nlp", "computer-vision", "speech"}
    assert (mm["prerequisite_min_required"], mm["prerequisite_recommended"]) == (1, 2)
    assert not any(f["is_advanced"] for slug, f in fields.items() if slug != "multimodal")


def test_fields_report_how_much_published_content_each_has(learn_client, learn_catalog):
    fields = {f["slug"]: f for f in learn_client.get(f"{API}/fields").json()}
    assert fields["nlp"]["available_course_count"] > 0
    assert fields["computer-vision"]["available_course_count"] == 0  # nothing published yet: said honestly
    assert fields["multimodal"]["available_course_count"] == 1


def test_career_goals_are_the_five_roles_with_their_relationships(learn_client, learn_catalog):
    goals = {g["slug"]: g for g in learn_client.get(f"{API}/career-goals").json()}
    assert list(goals) == ["data-analyst", "ml-engineer", "ai-developer", "mlops-engineer", "ai-engineer"]
    ai = goals["ai-engineer"]
    assert ai["title"] == "AI Engineer" and ai["title_ar"]
    assert {f["slug"] for f in ai["recommended_fields"]} == {"nlp", "computer-vision", "speech", "multimodal"}
    assert [f["slug"] for f in ai["required_fields"]] == ["machine-learning"]
    assert {s["slug"] for s in ai["required_skills"]} == {"evaluation", "production-deployment"}
    assert ai["recommended_level"]["slug"] == "intermediate"


def test_ai_engineer_copy_no_longer_says_it_is_the_sum_of_other_roles(learn_client, learn_catalog):
    ai = next(g for g in learn_client.get(f"{API}/career-goals").json() if g["slug"] == "ai-engineer")
    en = ai["description"].lower()
    # The retired framing listed the other roles' skills as its ingredients.
    assert not any(word in en for word in ("combines", "mlops", "data analysis", "ml engineering"))
    assert "nlp" in en and "nlp" in ai["description_ar"].lower()  # names the routes instead


def test_a_deactivated_field_disappears_from_the_catalogue(learn_client, learn_catalog, learn_db):
    learn_db.query(LearningField).filter(LearningField.slug == "speech").update({"is_active": False})
    learn_db.commit()
    assert "speech" not in {f["slug"] for f in learn_client.get(f"{API}/fields").json()}


def test_catalogue_reads_are_public(learn_client, learn_catalog):
    for path in ("levels", "fields", "career-goals", "courses", "paths", "courses/langchain", "paths/ai-engineer"):
        assert learn_client.get(f"{API}/{path}").status_code == 200, path


# ─── Courses ────────────────────────────────────────────────────────────────

def _list(client, **params):
    return client.get(f"{API}/courses", params=params)


def test_a_course_carries_levels_fields_roles_skills_and_where_to_open_it(learn_client, learn_catalog):
    course = learn_client.get(f"{API}/courses/rag-knowledge-systems").json()
    assert course["level"]["slug"] == "intermediate"
    assert [f["slug"] for f in course["fields"]] == ["nlp"]
    assert {r["slug"] for r in course["roles"]} == {"ai-developer", "ai-engineer"}
    assert {"rag", "retrieval"} <= {s["slug"] for s in course["skills"]}
    assert [p["slug"] for p in course["prerequisites"]] == ["llm-integration"]
    assert course["href"] == "/tracks/ai-developer"
    assert course["is_available"] is True


def test_a_tool_course_points_at_its_own_page_and_a_shell_is_not_available(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/courses/langchain").json()["href"] == "/tools/langchain"
    shell = learn_client.get(f"{API}/courses/pinecone").json()
    assert shell["is_available"] is False


def test_the_catalogue_title_is_bilingual_on_one_row_not_two_courses(learn_client, learn_catalog):
    course = learn_client.get(f"{API}/courses/ai-agents-orchestration").json()
    assert course["title"] == "AI Agents & Orchestration"
    assert "AI Agents" in course["title_ar"]
    slugs = [c["slug"] for c in _list(learn_client).json()]
    assert len(slugs) == len(set(slugs))


def test_unknown_course_is_a_404(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/courses/nope").status_code == 404


def test_filter_by_level(learn_client, learn_catalog):
    got = {c["slug"] for c in _list(learn_client, level="advanced").json()}
    assert {"advanced-rag", "multimodal-ai", "langgraph"} <= got
    assert "ai-engineering-foundations" not in got


def test_filter_by_field_any_of(learn_client, learn_catalog):
    nlp = {c["slug"] for c in _list(learn_client, field="nlp").json()}
    mm = {c["slug"] for c in _list(learn_client, field="multimodal").json()}
    both = {c["slug"] for c in _list(learn_client, field=["nlp", "multimodal"]).json()}
    assert both == nlp | mm and "multimodal-ai" in mm - nlp


def test_filters_combine_all_of_across_dimensions(learn_client, learn_catalog):
    """The Explore example: Intermediate + NLP + AI Engineer."""
    got = {c["slug"] for c in _list(learn_client, level="intermediate", field="nlp", career_goal="ai-engineer").json()}
    assert {"rag-knowledge-systems", "prompt-engineering", "langchain", "llamaindex"} <= got
    assert "advanced-rag" not in got and "multimodal-ai" not in got and "llm-integration" not in got


def test_filter_by_career_goal(learn_client, learn_catalog):
    got = {c["slug"] for c in _list(learn_client, career_goal="mlops-engineer").json()}
    assert {"deployment-integration", "fastapi-serving", "mlflow"} <= got
    assert "advanced-rag" not in got


def test_available_only_hides_courses_whose_content_is_not_written(learn_client, learn_catalog):
    everything = {c["slug"] for c in _list(learn_client).json()}
    live = {c["slug"] for c in _list(learn_client, available_only=True).json()}
    assert "pinecone" in everything and "pinecone" not in live
    assert live < everything and "langchain" in live


def test_search_bridges_english_and_arabic_through_the_terminology_dictionary(learn_client, learn_catalog):
    en = {c["slug"] for c in _list(learn_client, q="embeddings").json()}
    ar = {c["slug"] for c in _list(learn_client, q="التضمينات").json()}
    assert "embeddings-semantic-search" in en
    assert "embeddings-semantic-search" in ar


def test_an_unknown_filter_value_matches_nothing_rather_than_erroring(learn_client, learn_catalog):
    assert _list(learn_client, field="alchemy").json() == []


def test_a_malformed_filter_is_rejected(learn_client, learn_catalog):
    assert _list(learn_client, field="NLP; DROP TABLE").status_code == 422


# ─── Predefined paths ───────────────────────────────────────────────────────

def test_paths_list_is_one_per_goal_and_field_route(learn_client, learn_catalog):
    paths = {p["slug"]: p for p in learn_client.get(f"{API}/paths").json()}
    assert {"ai-engineer", "ai-engineer-nlp", "ai-engineer-computer-vision", "ai-engineer-speech",
            "ai-engineer-multimodal", "ml-engineer-computer-vision", "data-analyst-data"} <= set(paths)
    nlp, cv = paths["ai-engineer-nlp"], paths["ai-engineer-computer-vision"]
    assert nlp["career_goal"]["slug"] == "ai-engineer" and nlp["field"]["slug"] == "nlp"
    assert paths["ai-engineer"]["field"] is None  # the shared core, listed on its own
    # The Vision route shares the core but has no field-specific content yet, so
    # it offers strictly less to start than the NLP route does.
    assert nlp["available_course_count"] > cv["available_course_count"] > 0


def test_ai_engineer_is_a_goal_with_routes_not_a_sum_of_roles(learn_client, learn_catalog):
    """AI Engineer — NLP and AI Engineer — Speech are different journeys drawn
    from one template, and neither mentions completing other roles."""
    nlp = learn_client.get(f"{API}/paths/ai-engineer-nlp").json()
    speech = learn_client.get(f"{API}/paths/ai-engineer-speech").json()
    assert "nlp-llm" in _slugs(nlp) and "voice-ai" not in _slugs(nlp)
    assert "voice-ai" in _slugs(speech) and "nlp-llm" not in _slugs(speech)
    assert nlp["template_slug"] == speech["template_slug"] == "ai-engineer-path"


def test_the_nlp_route_has_the_stages_the_spec_describes_in_order(learn_client, learn_catalog):
    path = learn_client.get(f"{API}/paths/ai-engineer-nlp").json()
    assert _slugs(path) == ["foundations", "machine-learning", "deep-learning", "nlp-llm", "rag", "agents",
                            "llm-production", "production", "capstone-ai-engineer"]


def test_the_vision_and_speech_routes_have_their_own_stage_lists(learn_client, learn_catalog):
    cv = _slugs(learn_client.get(f"{API}/paths/ai-engineer-computer-vision").json())
    assert cv == ["foundations", "machine-learning", "deep-learning", "computer-vision", "advanced-cv",
                  "vision-language", "production", "capstone-ai-engineer"]
    sp = _slugs(learn_client.get(f"{API}/paths/ai-engineer-speech").json())
    assert sp == ["foundations", "machine-learning", "deep-learning", "audio-processing", "speech-recognition",
                  "text-to-speech", "voice-ai", "realtime-voice-agents", "production", "capstone-ai-engineer"]


def test_a_route_with_no_published_content_says_so_instead_of_inventing_courses(learn_client, learn_catalog):
    cv = learn_client.get(f"{API}/paths/ai-engineer-computer-vision").json()
    for slug in ("computer-vision", "advanced-cv", "vision-language"):
        stage = _stage(cv, slug)
        assert stage["status"] == "coming_soon" and stage["courses"] == []
    assert "no_available_courses" not in [a["code"] for a in cv["advisories"]]  # foundations/production exist
    only_cv = learn_client.get(f"{API}/paths/ml-engineer-computer-vision").json()
    assert only_cv["stages"]  # still a real, ordered journey


def test_multimodal_route_at_the_default_level_explains_and_routes(learn_client, learn_catalog):
    path = learn_client.get(f"{API}/paths/ai-engineer-multimodal").json()
    codes = {a["code"]: a for a in path["advisories"]}
    assert codes["field_above_level"]["params"]["min_level"] == "advanced"
    assert codes["prerequisite_route_added"]["params"]["added"] == ["nlp"]
    assert [f["slug"] for f in path["effective_fields"]] == ["nlp", "multimodal"]
    assert _slugs(path).index("nlp-llm") < _slugs(path).index("multimodal")  # single modality first


def test_predefined_path_level_can_be_chosen(learn_client, learn_catalog):
    adv = learn_client.get(f"{API}/paths/ai-engineer-nlp", params={"level": "advanced"}).json()
    assert adv["level"]["slug"] == "advanced"
    assert _states(adv)["llm-integration"] == "optional"
    beg = learn_client.get(f"{API}/paths/ai-engineer-nlp", params={"level": "beginner"}).json()
    assert _states(beg)["llm-integration"] == "required"


def test_unknown_path_and_level_are_rejected(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/paths/ai-engineer-basket-weaving").status_code == 404
    bad = learn_client.get(f"{API}/paths/ai-engineer-nlp", params={"level": "expert"})
    assert bad.status_code == 422 and bad.json()["detail"]["error"] == "unknown_level"


# ─── Generation ─────────────────────────────────────────────────────────────

def _generate(client, who, level="intermediate", fields=("nlp",), goal="ai-engineer"):
    return client.post(f"{API}/paths/generate", headers=who["headers"],
                       json={"level": level, "fields": list(fields), "career_goal": goal})


def test_generate_requires_sign_in(learn_client, learn_catalog):
    resp = learn_client.post(f"{API}/paths/generate", json={"level": "beginner", "fields": [], "career_goal": "ai-engineer"})
    assert resp.status_code == 401


def test_generate_returns_the_documented_shape(learn_client, learn_catalog):
    who = register(learn_client)
    path = _generate(learn_client, who).json()
    assert path["level"]["slug"] == "intermediate"
    assert path["career_goal"]["slug"] == "ai-engineer"
    assert [f["slug"] for f in path["fields"]] == ["nlp"]
    assert path["is_saved"] is False and path["status"] == "preview"
    stage = _stage(path, "nlp-llm")
    assert stage["title"] == "NLP & LLM Engineering" and stage["title_ar"]
    assert {c["course"]["slug"] for c in stage["courses"]} >= {"prompt-engineering", "langchain"}


def test_generate_does_not_save_anything(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    assert _generate(learn_client, who).status_code == 200
    assert learn_client.get(f"{API}/my-path", headers=who["headers"]).status_code == 404
    assert learn_db.query(LearningPath).count() == 0


@pytest.mark.parametrize("level,fields,goal,error", [
    ("expert", ["nlp"], "ai-engineer", "unknown_level"),
    ("beginner", ["nlp"], "chef", "unknown_career_goal"),
    ("beginner", ["alchemy"], "ai-engineer", "unknown_field"),
])
def test_generate_rejects_unknown_input_with_a_machine_readable_code(learn_client, learn_catalog, level, fields, goal, error):
    who = register(learn_client)
    resp = _generate(learn_client, who, level=level, fields=fields, goal=goal)
    assert resp.status_code == 422
    assert resp.json()["detail"]["error"] == error


def test_generate_bounds_the_field_list(learn_client, learn_catalog):
    who = register(learn_client)
    assert _generate(learn_client, who, fields=["nlp"] * 13).status_code == 422


def test_generate_accepts_multiple_fields(learn_client, learn_catalog):
    """Level: Advanced, Interest: Speech + NLP, Goal: AI Engineer."""
    who = register(learn_client)
    path = _generate(learn_client, who, level="advanced", fields=["speech", "nlp"]).json()
    assert {"voice-ai", "nlp-llm"} <= set(_slugs(path))


def test_advanced_users_are_not_forced_through_introductory_courses(learn_client, learn_catalog):
    who = register(learn_client)
    states = _states(_generate(learn_client, who, level="advanced").json())
    assert states["ai-engineering-foundations"] == "optional"
    assert states["llm-integration"] == "optional"
    assert states["advanced-rag"] == "required"
    # ...but a skill the goal demands and they have not shown is still required.
    assert states["ai-evaluation-observability"] == "required"


def test_beginner_multimodal_is_advised_and_routed_never_blocked(learn_client, learn_catalog):
    who = register(learn_client)
    resp = _generate(learn_client, who, level="beginner", fields=["multimodal"])
    assert resp.status_code == 200
    path = resp.json()
    assert {a["code"] for a in path["advisories"]} >= {"field_above_level", "prerequisite_route_added"}
    assert "multimodal" in _slugs(path) and "nlp-llm" in _slugs(path)


def test_advanced_multimodal_with_one_modality_is_only_recommended_a_second(learn_client, learn_catalog):
    who = register(learn_client)
    path = _generate(learn_client, who, level="advanced", fields=["nlp", "multimodal"]).json()
    codes = [a["code"] for a in path["advisories"]]
    assert "prerequisite_route_added" not in codes and "field_above_level" not in codes
    assert "prerequisites_recommended" in codes


def test_generation_is_personalised_with_the_callers_own_progress(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 3)  # RAG & Knowledge Systems
    path = _generate(learn_client, who).json()
    assert _states(path)["rag-knowledge-systems"] == "completed"
    other = register(learn_client)
    assert _states(_generate(learn_client, other).json())["rag-knowledge-systems"] == "required"


# ─── Learning profile ───────────────────────────────────────────────────────

def test_a_new_learner_has_an_empty_profile_that_asks_for_onboarding(learn_client, learn_catalog):
    who = register(learn_client)
    profile = learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()
    assert profile["level"] is None and profile["career_goal"] is None and profile["fields"] == []
    assert profile["needs_onboarding"] is True and profile["onboarding_completed"] is False
    assert profile["has_active_path"] is False


def test_profile_requires_sign_in(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/my-profile").status_code == 401
    assert learn_client.put(f"{API}/my-profile", json={"level": "beginner"}).status_code == 401


def test_saving_a_full_profile_completes_onboarding(learn_client, learn_catalog):
    who = register(learn_client)
    profile = _profile(learn_client, who, level="beginner", fields=("computer-vision", "nlp"), goal="ml-engineer")
    assert profile["level"]["slug"] == "beginner"
    assert profile["career_goal"]["slug"] == "ml-engineer"
    assert [f["slug"] for f in profile["fields"]] == ["computer-vision", "nlp"]  # more than one, order kept
    assert profile["onboarding_completed"] is True and profile["needs_onboarding"] is False


def test_a_partial_save_keeps_the_rest_and_is_not_complete(learn_client, learn_catalog):
    who = register(learn_client)
    learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"level": "advanced"})
    profile = learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"fields": ["speech"]}).json()
    assert profile["level"]["slug"] == "advanced"  # the earlier answer was kept
    assert [f["slug"] for f in profile["fields"]] == ["speech"]
    assert profile["needs_onboarding"] is True  # no goal yet


def test_clearing_an_answer_reopens_onboarding(learn_client, learn_catalog):
    who = register(learn_client)
    _profile(learn_client, who)
    cleared = learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"level": None}).json()
    assert cleared["level"] is None and cleared["needs_onboarding"] is True
    assert learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"fields": []}).json()["fields"] == []


def test_multimodal_is_savable_at_any_level(learn_client, learn_catalog):
    who = register(learn_client)
    profile = _profile(learn_client, who, level="beginner", fields=("multimodal",))
    assert [f["slug"] for f in profile["fields"]] == ["multimodal"]


@pytest.mark.parametrize("body,error", [
    ({"level": "expert"}, "unknown_level"),
    ({"career_goal": "chef"}, "unknown_career_goal"),
    ({"fields": ["nlp", "alchemy"]}, "unknown_field"),
    ({"known_skills": ["telepathy"]}, "unknown_skill"),
])
def test_unknown_values_are_refused_and_change_nothing(learn_client, learn_catalog, body, error):
    who = register(learn_client)
    _profile(learn_client, who, level="beginner", fields=("nlp",), goal="ai-developer")
    resp = learn_client.put(f"{API}/my-profile", headers=who["headers"], json=body)
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == error
    after = learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()
    assert after["level"]["slug"] == "beginner" and after["career_goal"]["slug"] == "ai-developer"


def test_a_malformed_slug_is_rejected_before_it_reaches_a_lookup(learn_client, learn_catalog):
    who = register(learn_client)
    assert learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"level": "Beginner "}).status_code == 422


def test_saving_the_level_keeps_the_legacy_experience_level_in_step(learn_client, learn_catalog):
    who = register(learn_client)
    _profile(learn_client, who, level="advanced")
    me = learn_client.get("/api/v1/auth/me", headers=who["headers"]).json()
    assert me["experience_level"] == "advanced"


def test_one_learners_profile_never_touches_anothers(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _profile(learn_client, a, level="advanced", fields=("speech",), goal="ai-engineer")
    other = learn_client.get(f"{API}/my-profile", headers=b["headers"]).json()
    assert other["level"] is None and other["fields"] == []


# ─── Saved path ─────────────────────────────────────────────────────────────

def test_no_path_yet_is_a_404_and_building_needs_a_complete_profile(learn_client, learn_catalog):
    who = register(learn_client)
    assert learn_client.get(f"{API}/my-path", headers=who["headers"]).status_code == 404
    resp = learn_client.put(f"{API}/my-path", headers=who["headers"], json={})
    assert resp.status_code == 409 and resp.json()["detail"]["error"] == "learning_profile_incomplete"


def test_path_endpoints_require_sign_in(learn_client, learn_catalog):
    assert learn_client.get(f"{API}/my-path").status_code == 401
    assert learn_client.put(f"{API}/my-path", json={}).status_code == 401
    assert learn_client.get(f"{API}/my-progress").status_code == 401


def test_building_saves_the_path_and_it_reads_back_the_same(learn_client, learn_catalog):
    who = register(learn_client)
    built = _build(learn_client, who)
    assert built["is_saved"] is True and built["status"] == "active" and built["id"]
    assert _slugs(built) == ["foundations", "machine-learning", "deep-learning", "nlp-llm", "rag", "agents",
                            "llm-production", "production", "capstone-ai-engineer"]
    read = learn_client.get(f"{API}/my-path", headers=who["headers"]).json()
    assert read["id"] == built["id"] and _slugs(read) == _slugs(built)
    assert learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()["has_active_path"] is True


def test_the_current_stage_is_the_first_one_with_work_left(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who)
    assert path["current_stage_slug"] == "nlp-llm"  # foundations is optional at intermediate
    assert _stage(path, "foundations")["status"] == "skippable"
    assert _stage(path, "nlp-llm")["status"] == "current"
    assert _stage(path, "rag")["status"] == "upcoming"
    assert _stage(path, "machine-learning")["status"] == "coming_soon"
    assert _stage(path, "capstone-ai-engineer")["status"] == "coming_soon"


def test_rebuilding_archives_the_old_path_and_keeps_history(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    first = _build(learn_client, who)
    learn_client.put(f"{API}/my-profile", headers=who["headers"], json={"fields": ["nlp", "speech"]})
    second = learn_client.put(f"{API}/my-path", headers=who["headers"], json={}).json()
    assert second["id"] != first["id"] and "voice-ai" in _slugs(second)
    rows = learn_db.query(LearningPath).filter(LearningPath.user_id == who["id"]).all()
    assert sorted(r.status for r in rows) == ["active", "archived"]


def test_a_saved_path_stores_membership_not_copies_of_the_catalogue(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    _build(learn_client, who)
    row = learn_db.query(LearningPath).filter(LearningPath.user_id == who["id"]).one()
    stage = next(s for s in row.stages if s["slug"] == "nlp-llm")
    assert set(stage) == {"slug", "position", "upcoming_count", "courses"}  # no titles, no translations
    assert all(set(c) == {"course_id", "state", "reason"} for c in stage["courses"])


def test_pausing_changes_only_the_status_and_the_path_stays_readable(learn_client, learn_catalog):
    who = register(learn_client)
    built = _build(learn_client, who)
    paused = learn_client.put(f"{API}/my-path", headers=who["headers"], json={"status": "paused"}).json()
    assert paused["status"] == "paused" and paused["id"] == built["id"]  # not rebuilt
    read = learn_client.get(f"{API}/my-path", headers=who["headers"])
    assert read.status_code == 200 and read.json()["status"] == "paused"  # a pause is not "no path"
    assert learn_client.get(f"{API}/my-profile", headers=who["headers"]).json()["has_active_path"] is True
    resumed = learn_client.put(f"{API}/my-path", headers=who["headers"], json={"status": "active"}).json()
    assert resumed["status"] == "active" and resumed["id"] == built["id"]


def test_rebuilding_replaces_a_paused_path_too(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    _build(learn_client, who)
    learn_client.put(f"{API}/my-path", headers=who["headers"], json={"status": "paused"})
    rebuilt = learn_client.put(f"{API}/my-path", headers=who["headers"], json={}).json()
    assert rebuilt["status"] == "active"
    rows = learn_db.query(LearningPath).filter(LearningPath.user_id == who["id"]).all()
    assert sorted(r.status for r in rows) == ["active", "archived"]


def test_asking_for_a_rebuild_and_a_status_change_together_is_refused(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who)
    resp = learn_client.put(f"{API}/my-path", headers=who["headers"], json={"regenerate": True, "status": "paused"})
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "conflicting_update"


def test_waiving_a_course_removes_it_from_the_work_left(learn_client, learn_catalog):
    who = register(learn_client)
    built = _build(learn_client, who)
    prompt = next(c["course"] for s in built["stages"] for c in s["courses"] if c["course"]["slug"] == "prompt-engineering")
    waived = learn_client.put(f"{API}/my-path", headers=who["headers"], json={"waived_course_ids": [prompt["id"]]}).json()
    assert _states(waived)["prompt-engineering"] == "waived"
    assert waived["estimated_hours"] < built["estimated_hours"]
    # A rebuild that does not mention waivers keeps them.
    again = learn_client.put(f"{API}/my-path", headers=who["headers"], json={}).json()
    assert _states(again)["prompt-engineering"] == "waived"


def test_waiving_an_unknown_course_is_refused(learn_client, learn_catalog):
    who = register(learn_client)
    _build(learn_client, who)
    resp = learn_client.put(f"{API}/my-path", headers=who["headers"], json={"waived_course_ids": [999_999]})
    assert resp.status_code == 422 and resp.json()["detail"]["error"] == "unknown_course"


def test_one_learners_path_is_invisible_to_another(learn_client, learn_catalog):
    a, b = register(learn_client), register(learn_client)
    _build(learn_client, a)
    assert learn_client.get(f"{API}/my-path", headers=b["headers"]).status_code == 404


def test_estimated_duration_is_hours_and_weeks(learn_client, learn_catalog):
    who = register(learn_client)
    path = _build(learn_client, who, level="beginner")
    assert path["estimated_hours"] > 0
    assert path["estimated_weeks"] * 6 >= path["estimated_hours"] > (path["estimated_weeks"] - 1) * 6


# ─── Progress ───────────────────────────────────────────────────────────────

def test_progress_is_derived_from_lessons_even_though_track_topics_never_set_a_status(learn_client, learn_catalog, learn_db):
    """Track progress rows stay `in_progress` forever in the existing API; the
    fixture leaves the status at its default, so this fails if progress were
    read from `status` rather than from the lessons."""
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 3)
    path = _build(learn_client, who)
    course = next(c for s in path["stages"] for c in s["courses"] if c["course"]["slug"] == "rag-knowledge-systems")
    assert course["state"] == "completed" and course["completion_pct"] == 100.0


def test_partial_completion_is_a_partial_percentage(learn_client, learn_catalog, learn_db):
    from app.models.progress import UserProgress

    who = register(learn_client)
    topic_id, lesson_id = learn_catalog["level_lessons"][4][0]  # one of two topics
    learn_db.add(UserProgress(user_id=who["id"], topic_id=topic_id, lessons_completed=[lesson_id]))
    learn_db.commit()
    path = _build(learn_client, who)
    course = next(c for s in path["stages"] for c in s["courses"] if c["course"]["slug"] == "prompt-engineering")
    assert course["state"] == "required" and course["completion_pct"] == 50.0


def test_a_tool_course_credential_counts_as_complete(learn_client, learn_catalog, learn_db):
    from app.models.tool_course import ToolCourse, ToolCourseCompletion

    who = register(learn_client)
    tool = learn_db.query(ToolCourse).filter(ToolCourse.slug == "langchain").one()
    learn_db.add(ToolCourseCompletion(user_id=who["id"], tool_course_id=tool.id))
    learn_db.commit()
    assert _states(_build(learn_client, who))["langchain"] == "completed"


def test_stage_and_path_progress_ignore_optional_courses(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    path = _build(learn_client, who)  # intermediate: foundations + llm-integration are optional
    assert _stage(path, "foundations")["progress_pct"] is None  # nothing to measure, never "0%"
    complete_level(learn_db, who["id"], learn_catalog, 4)  # prompt-engineering
    complete_tool(learn_db, who["id"], learn_catalog, "langchain")
    done = learn_client.get(f"{API}/my-path", headers=who["headers"]).json()
    assert _stage(done, "nlp-llm")["progress_pct"] == 100.0
    assert _stage(done, "nlp-llm")["status"] == "completed"
    assert done["current_stage_slug"] == "rag"


def test_a_finished_course_counts_in_every_path_it_belongs_to_without_double_counting(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 9)  # Multimodal AI: field multimodal, roles ai-developer + ai-engineer
    progress = learn_client.get(f"{API}/my-progress", headers=who["headers"]).json()
    assert progress["by_field"]["multimodal"] == 100.0
    assert progress["by_role"]["ai-engineer"] > 0 and progress["by_role"]["ai-developer"] > 0
    assert progress["by_skill"]["multimodal"] == 100.0
    # One engaged course, finished: overall is 100, not 200 for "two roles".
    assert progress["overall_pct"] == 100.0


def test_overall_progress_is_the_mean_over_engaged_courses_counted_once(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 9)
    _build(learn_client, who, level="intermediate", fields=("nlp",), goal="ai-engineer")
    progress = learn_client.get(f"{API}/my-progress", headers=who["headers"]).json()
    path = learn_client.get(f"{API}/my-path", headers=who["headers"]).json()
    engaged = {c["course"]["slug"]: c["completion_pct"] for s in path["stages"] for c in s["courses"]
               if c["state"] in ("required", "completed")}
    assert progress["path_pct"] == path["progress"]["path_pct"] == 0.0  # nothing on this path is done
    # Multimodal AI is finished but sits outside this NLP path: it is still
    # engaged, so it joins the path's courses in the mean - once.
    expected = 100.0 / (len(engaged) + 1)
    assert progress["overall_pct"] == pytest.approx(expected, abs=0.1)
    assert path["progress"]["overall_pct"] == progress["overall_pct"]


def test_progress_reports_per_goal_field_and_skill(learn_client, learn_catalog, learn_db):
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 7)  # AI Agents: nlp
    progress = learn_client.get(f"{API}/my-progress", headers=who["headers"]).json()
    assert 0 < progress["by_field"]["nlp"] < 100
    assert progress["by_field"].get("computer-vision") is None  # no available courses: not reported as 0%
    assert progress["by_skill"]["ai-agents"] == 100.0


def test_a_learner_with_no_activity_has_zero_not_an_error(learn_client, learn_catalog):
    who = register(learn_client)
    progress = learn_client.get(f"{API}/my-progress", headers=who["headers"]).json()
    assert progress["overall_pct"] == 0 and progress["path_pct"] is None
