"""
Independent course enrollment: any published course can be found, opened and
enrolled in without a track, a career goal or a saved path; how ready a learner is
advises but never blocks; a track is a recommended ordering of the same canonical
courses.

The courses here are real registry courses (`course-001`..`course-014`, with their real
prerequisites, roles and roadmap places) given small generated lessons; see
`tests/curriculum_fixtures.py`. The real course folders are covered by
`test_curriculum_import.py`.
"""
import pytest

from app.models.billing import CourseEnrollment, CourseOffer
from app.models.learning import Lesson
from app.models.learning_path import Course, LearningProfile, ReadinessAssessment
from app.models.progress import Enrollment
from app.models.tool_course import ToolTopic
from app.services.payments import kashier_service
from tests.curriculum_fixtures import correct_answers, finish_topics, import_small_courses, topic_ids
from tests.learning_fixtures import accept_written_answers, learn_catalog, learn_client, learn_db, logs_enabled, register  # noqa: F401

API = "/api/v1/learning"


@pytest.fixture()
def content(learn_db, learn_catalog):
    """`course-001`..`course-004`, `course-013`, `course-014` with small lessons; the rest stay shells."""
    return {c.slug: c for c in import_small_courses(learn_db)}


def _get(client, path, who=None, **params):
    return client.get(f"{API}{path}", headers=who["headers"] if who else None, params=params)


def _post(client, path, who, **body):
    return client.post(f"{API}{path}", headers=who["headers"], json=body or None)


def _cards(client, who=None, **params):
    response = _get(client, "/courses", who, **params)
    assert response.status_code == 200, response.text
    return {c["slug"]: c for c in response.json()}


# ─── The catalogue ──────────────────────────────────────────────────────────

def test_the_catalogue_lists_every_published_course_without_a_career_goal(learn_client, content):
    cards = _cards(learn_client)                                    # no filters at all
    for slug in content:
        card = cards[slug]
        assert card["is_available"] is True
        assert (card["module_count"], card["lesson_count"]) == (2, 4)
        assert card["estimated_hours"] > 0 and card["level"]["slug"] in {"beginner", "intermediate", "advanced"}
    assert cards["course-005"]["is_available"] is False              # catalogued, content not published
    assert "course-005" not in _cards(learn_client, available_only=True)
    assert {"langchain", "course-001"} <= set(cards)                 # tools and curriculum, side by side


def test_the_catalogue_filters_by_difficulty_category_skill_and_goal_and_they_combine(learn_client, content):
    beginner = _cards(learn_client, difficulty="beginner")
    assert {"course-001", "course-013"} <= set(beginner) and "course-002" not in beginner
    assert {c["level"]["slug"] for c in beginner.values()} == {"beginner"}
    assert _cards(learn_client, level="beginner").keys() == beginner.keys()      # `level` and `difficulty` are one filter

    assert "course-014" in _cards(learn_client, category="computer-vision")
    assert "course-001" not in _cards(learn_client, category="computer-vision")
    assert {"course-001", "course-004"} <= set(_cards(learn_client, skill="machine-learning"))
    assert "course-013" not in _cards(learn_client, skill="machine-learning")

    goal = _cards(learn_client, career_goal="ml-engineer")
    assert goal["course-001"]["track_role"] == "core" and goal["course-013"]["track_role"] == "supporting"
    assert "course-013" not in _cards(learn_client, career_goal="ml-engineer", difficulty="intermediate")
    both = _cards(learn_client, difficulty="beginner", category="data")
    assert "course-013" in both and "course-001" not in both


def test_a_single_course_is_available_on_its_own_with_structure_but_no_lesson_text(learn_client, content):
    response = _get(learn_client, "/courses/COURSE-004")             # the frozen id, in any case
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["slug"] == "course-004" and body["href"] == "/courses/course-004/learn"
    assert [m["order"] for m in body["modules"]] == [1, 2]
    assert all(m["lesson_count"] == 2 and m["exercise_count"] == 4 and m["quiz_count"] == 1 for m in body["modules"])
    assert [p["kind"] for p in body["projects"]] == ["module", "module", "capstone"]
    assert [p["slug"] for p in body["prerequisites"]] == ["course-003"]
    assert {"course-001", "course-002"} <= {p["slug"] for p in body["recommended_prerequisites"]}
    assert "Body of" not in response.text and "Explained for" not in response.text        # no lesson or quiz content
    assert _get(learn_client, "/courses/course-999").status_code == 404


def test_a_course_lists_the_roadmaps_it_appears_in_as_information_only(learn_client, content):
    body = _get(learn_client, "/courses/course-004").json()
    roles = {r["career_goal"]["slug"]: r["track_role"] for r in body["roadmaps"]}
    # See seeds/curriculum.py:TRACK_WORKFLOWS - the canonical career-track mapping.
    assert roles == {"ml-engineer": "optional", "ai-developer": "core", "ai-engineer": "core"}
    assert all(r["position"] and r["total"] >= r["position"] for r in body["roadmaps"])


def test_a_signed_in_learner_sees_their_own_enrollment_and_readiness_on_cards_an_anonymous_visitor_does_not(
    learn_client, content,
):
    who = register(learn_client)
    assert _post(learn_client, "/courses/course-001/enroll", who).status_code == 200
    anon = _cards(learn_client)
    mine = _cards(learn_client, who)
    assert anon["course-001"]["enrollment"] is None and anon["course-001"]["readiness"] is None
    assert mine["course-001"]["enrollment"]["status"] == "enrolled"
    assert mine["course-004"]["enrollment"] is None and mine["course-004"]["readiness"]["state"] != "ready"
    assert set(_cards(learn_client, who, enrolled=True)) == {"course-001"}
    assert "course-001" not in _cards(learn_client, who, enrolled=False)
    assert _get(learn_client, "/courses/course-001", who).json()["enrollment"]["status"] == "enrolled"


# ─── Enrolling ──────────────────────────────────────────────────────────────

def test_a_learner_enrolls_in_any_course_with_no_track_no_goal_and_no_profile(learn_client, learn_db, content):
    who = register(learn_client)
    response = _post(learn_client, "/courses/COURSE-013/enroll", who)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["created"] is True
    assert (body["enrollment"]["status"], body["enrollment"]["source"], body["enrollment"]["progress_percentage"]) \
        == ("enrolled", "free", 0.0)
    assert body["readiness"]["state"] == "ready" and body["readiness"]["has_prerequisites"] is False
    assert body["start"]["mode"] == "start" and body["start"]["recommended_module"]["order"] == 1
    # ... and nothing about a track or goal was needed or created.
    assert learn_db.query(Enrollment).filter(Enrollment.user_id == who["id"]).count() == 0
    assert learn_db.query(LearningProfile).filter(LearningProfile.user_id == who["id"]).count() == 0


def test_enrolling_twice_is_idempotent(learn_client, learn_db, content):
    who = register(learn_client)
    first = _post(learn_client, "/courses/course-001/enroll", who).json()
    second = _post(learn_client, "/courses/course-001/enroll", who).json()
    assert (first["created"], second["created"]) == (True, False)
    assert first["enrollment"]["enrolled_at"] == second["enrollment"]["enrolled_at"]
    assert learn_db.query(CourseEnrollment).filter(CourseEnrollment.user_id == who["id"]).count() == 1


def test_enrolling_needs_a_signed_in_learner_a_real_and_a_published_course(learn_client, content):
    who = register(learn_client)
    assert learn_client.post(f"{API}/courses/course-001/enroll").status_code == 401
    assert _post(learn_client, "/courses/course-999/enroll", who).status_code == 404
    unavailable = _post(learn_client, "/courses/course-005/enroll", who)           # a shell: no lessons yet
    assert unavailable.status_code == 409 and unavailable.json()["detail"]["code"] == "COURSE_UNAVAILABLE"
    assert learn_client.get(f"{API}/courses/course-001/readiness").status_code == 401
    assert learn_client.get(f"{API}/recommendations").status_code == 401


def test_the_client_cannot_name_a_user_or_a_status_when_enrolling(learn_client, learn_db, content):
    mine, other = register(learn_client), register(learn_client)
    response = learn_client.post(f"{API}/courses/course-001/enroll", headers=mine["headers"],
                                 json={"user_id": other["id"], "status": "completed"})
    assert response.status_code == 200
    rows = learn_db.query(CourseEnrollment).filter(CourseEnrollment.course_id == content["course-001"].id).all()
    assert [(r.user_id, r.learning_status) for r in rows] == [(mine["id"], "enrolled")]


# ─── Readiness is advice, never a gate ──────────────────────────────────────

def test_weak_readiness_does_not_block_enrollment_and_comes_with_preparation(learn_client, content):
    who = register(learn_client)
    response = _post(learn_client, "/courses/course-004/enroll", who)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["readiness"]["state"] in ("needs_foundation", "not_assessed")
    review = {r["course"]["slug"]: r for r in body["readiness"]["recommended_review"]}
    assert "course-003" in review and review["course-003"]["required"] is True
    assert [m["order"] for m in review["course-003"]["modules"]] == [1, 2]              # where to begin in it
    assert body["start"]["mode"] == "start" and body["start"]["preparation"] == body["readiness"]["recommended_review"]
    assert body["enrollment"]["status"] == "enrolled"


def test_finishing_the_prerequisites_raises_readiness_and_empties_the_review_list(learn_client, learn_db, content):
    who = register(learn_client)
    before = _get(learn_client, "/courses/course-004/readiness", who).json()
    assert before["state"] in ("needs_foundation", "not_assessed") and before["strengths"] == []

    finish_topics(learn_db, who["id"], content["course-001"])
    finish_topics(learn_db, who["id"], content["course-002"])
    partway = _get(learn_client, "/courses/course-004/readiness", who).json()
    assert partway["state"] in ("needs_foundation", "mostly_ready")          # 003 (required) still missing
    assert "course-003" in {r["course"]["slug"] for r in partway["recommended_review"]}
    assert "course-001" not in {r["course"]["slug"] for r in partway["recommended_review"]}     # done: never proposed

    finish_topics(learn_db, who["id"], content["course-003"])
    after = _get(learn_client, "/courses/course-004/readiness", who).json()
    assert after["state"] == "ready" and after["gaps"] == [] and after["recommended_review"] == []
    assert {"deep-learning", "machine-learning"} <= {s["skill"]["slug"] for s in after["strengths"]}


def test_readiness_is_separate_from_difficulty(learn_client, learn_db, content):
    who = register(learn_client)
    finish_topics(learn_db, who["id"], content["course-001"])
    beginner_ready = _get(learn_client, "/courses/course-013/readiness", who).json()
    intermediate = _get(learn_client, "/courses/course-002/readiness", who).json()
    assert beginner_ready["state"] == "ready" and intermediate["state"] == "ready"
    assert content["course-002"].level.slug == "intermediate"        # an intermediate course, a ready learner
    assert _get(learn_client, "/courses/course-004/readiness", who).json()["state"] != "ready"   # another intermediate course, not ready


def test_a_course_with_no_prerequisites_is_ready_and_has_no_readiness_check(learn_client, content):
    who = register(learn_client)
    readiness = _get(learn_client, "/courses/course-013/readiness", who).json()
    assert readiness["state"] == "ready" and readiness["assessment_available"] is False
    assert _get(learn_client, "/courses/course-013/readiness-assessment", who).status_code == 404


def test_the_onboarding_answers_are_a_weak_prior_never_proof(learn_client, content):
    who = register(learn_client)
    saved = learn_client.put(f"{API}/my-profile", headers=who["headers"], json={
        "programming_experience": "professional", "ai_experience": "basics", "fields": ["machine-learning"]})
    assert saved.status_code == 200, saved.text
    levels = _get(learn_client, "/my-skill-levels", who).json()
    assert levels["levels"]["python"] == "intermediate" and levels["levels"]["machine-learning"] == "beginner"
    assert levels["programming_experience"] == "professional"
    assert levels["levels"]["deep-learning"] == "not_assessed"
    # Claiming experience does not make a learner ready for a course that builds on real coursework.
    assert _get(learn_client, "/courses/course-004/readiness", who).json()["state"] == "needs_foundation"


def test_skill_levels_follow_completed_coursework_and_are_per_skill(learn_client, learn_db, content):
    who = register(learn_client)
    assert set(_get(learn_client, "/my-skill-levels", who).json()["levels"].values()) == {"not_assessed"}
    finish_topics(learn_db, who["id"], content["course-001"])          # beginner course -> intermediate at its skills
    finish_topics(learn_db, who["id"], content["course-002"])          # intermediate course -> advanced at its skills
    levels = _get(learn_client, "/my-skill-levels", who).json()["levels"]
    assert (levels["machine-learning"], levels["deep-learning"], levels["fastapi"]) == ("intermediate", "advanced", "not_assessed")


# ─── The readiness check ────────────────────────────────────────────────────

def test_the_check_asks_real_prerequisite_questions_and_never_sends_the_answer_key(learn_client, content):
    who = register(learn_client)
    response = _get(learn_client, "/courses/course-004/readiness-assessment", who)
    assert response.status_code == 200, response.text
    body = response.json()
    assert 3 <= body["question_count"] <= 10 and body["estimated_minutes"] >= 1
    prerequisite_skills = {"deep-learning", "pytorch", "machine-learning", "python", "scikit-learn", "numpy"}
    for question in body["questions"]:
        assert set(question) == {"id", "skill", "question", "question_ar", "options", "options_ar"}
        assert question["skill"]["slug"] in prerequisite_skills and len(question["options"]) == 4
        assert question["question"].startswith("L00")                      # authored quiz questions, nothing generated
    assert "correct" not in response.text and "explanation" not in response.text and "Explained for" not in response.text
    assert _get(learn_client, "/courses/course-004/readiness-assessment", who).json() == body     # stable between calls


def test_the_check_is_graded_on_the_server_and_moves_readiness(learn_client, learn_db, content):
    who = register(learn_client)
    questions = _get(learn_client, "/courses/course-004/readiness-assessment", who).json()["questions"]
    ids = [q["id"] for q in questions]
    assert _get(learn_client, "/courses/course-004/readiness", who).json()["state"] == "not_assessed"

    wrong = {qid: (correct + 1) % 4 for qid, correct in correct_answers(learn_db, ids).items()}
    failed = _post(learn_client, "/courses/course-004/readiness-assessment", who, answers=wrong)
    assert failed.status_code == 200, failed.text
    assert failed.json()["score"] == 0.0 and set(failed.json()["skill_results"].values()) == {0.0}
    assert failed.json()["readiness"]["state"] == "needs_foundation"

    right = correct_answers(learn_db, ids)
    passed = _post(learn_client, "/courses/course-004/readiness-assessment", who, answers=right).json()
    assert passed["score"] == 100.0 and passed["correct_count"] == passed["question_count"] == len(ids)
    assert all(r["correct"] for r in passed["questions"])
    assert passed["readiness"]["state"] in ("ready", "mostly_ready")             # the latest check replaces the earlier one
    assert learn_db.query(ReadinessAssessment).filter(ReadinessAssessment.user_id == who["id"]).count() == 2
    # It is that learner's alone.
    assert _get(learn_client, "/courses/course-004/readiness", register(learn_client)).json()["state"] == "not_assessed"


def test_unanswered_questions_count_as_wrong(learn_client, learn_db, content):
    who = register(learn_client)
    ids = [q["id"] for q in _get(learn_client, "/courses/course-004/readiness-assessment", who).json()["questions"]]
    one = {ids[0]: correct_answers(learn_db, ids[:1])[ids[0]]}
    result = _post(learn_client, "/courses/course-004/readiness-assessment", who, answers=one).json()
    assert result["correct_count"] == 1 and result["question_count"] == len(ids)
    assert result["score"] == round(100 / len(ids), 1)


def test_the_client_cannot_supply_a_score_a_question_or_an_option_that_is_not_there(learn_client, learn_db, content):
    who = register(learn_client)
    ids = [q["id"] for q in _get(learn_client, "/courses/course-004/readiness-assessment", who).json()["questions"]]
    good = correct_answers(learn_db, ids)
    path = "/courses/course-004/readiness-assessment"
    for body in (
        {"answers": good, "score": 100},                              # a score is not accepted
        {"answers": good, "readiness": "ready"},
        {"answers": {"999999:0": 1}},                                 # a question that is not in the check
        {"answers": {ids[0]: 9}},                                     # an option that does not exist
        {"answers": {ids[0]: -1}},
        {"answers": {ids[0]: True}},
        {"answers": {"not-an-id": 1}},
    ):
        assert learn_client.post(f"{API}{path}", headers=who["headers"], json=body).status_code == 422, body
    assert learn_db.query(ReadinessAssessment).filter(ReadinessAssessment.user_id == who["id"]).count() == 0
    assert _get(learn_client, "/courses/course-004/readiness", who).json()["state"] == "not_assessed"


# ─── Recommendations ────────────────────────────────────────────────────────

def _groups(client, who):
    response = _get(client, "/recommendations", who)
    assert response.status_code == 200, response.text
    body = response.json()
    return body, {g: {i["course"]["slug"]: i for i in body[g]}
                  for g in ("continue_learning", "recommended_next", "build_foundations", "completed")}


def test_recommendations_work_with_no_career_goal_and_each_carries_a_reason(learn_client, content):
    who = register(learn_client)
    body, groups = _groups(learn_client, who)
    assert body["career_goal"] is None
    assert {"course-001", "course-013"} <= set(groups["recommended_next"])          # nothing needed first
    assert "course-004" not in groups["recommended_next"]                           # its prerequisites are not done
    for item in body["recommended_next"]:
        assert item["reason_code"] and item["reason"] and item["readiness"] in ("ready", "mostly_ready", "not_assessed")
    assert groups["recommended_next"]["course-013"]["reason_code"] == "good_place_to_start"


def test_completed_courses_are_never_recommended_as_next(learn_client, learn_db, content):
    who = register(learn_client)
    finish_topics(learn_db, who["id"], content["course-001"])
    _, groups = _groups(learn_client, who)
    assert "course-001" in groups["completed"]
    assert "course-001" not in groups["recommended_next"] and "course-001" not in groups["build_foundations"]
    assert groups["recommended_next"]["course-002"]["reason_code"] == "follows_completed"
    assert "course-001" in groups["recommended_next"]["course-002"]["reason"] or "Machine Learning" in \
        groups["recommended_next"]["course-002"]["reason"]
    # The client writes the sentence itself, so the params carry the course *names*, not only ids.
    named = groups["recommended_next"]["course-002"]["params"]["courses"]
    assert [c["slug"] for c in named] == ["course-001"] and named[0]["title"]


def test_a_course_in_progress_is_offered_to_continue_and_its_prerequisites_are_offered_as_foundations(
    learn_client, learn_db, content,
):
    who = register(learn_client)
    assert _post(learn_client, "/courses/course-004/enroll", who).status_code == 200
    finish_topics(learn_db, who["id"], content["course-004"], upto=1)
    _, groups = _groups(learn_client, who)
    assert groups["continue_learning"]["course-004"]["reason_code"] == "in_progress"
    assert groups["continue_learning"]["course-004"]["params"]["percent"] == 50
    assert "course-004" not in groups["recommended_next"]
    assert groups["build_foundations"]["course-003"]["reason_code"] == "strengthens_enrolled"


def test_a_career_goal_sharpens_recommendations_but_never_controls_access(learn_client, learn_db, content):
    who = register(learn_client)
    saved = learn_client.put(f"{API}/my-profile", headers=who["headers"],
                             json={"level": "beginner", "career_goal": "ml-engineer", "fields": ["machine-learning"]})
    assert saved.status_code == 200, saved.text
    body, groups = _groups(learn_client, who)
    assert body["career_goal"]["slug"] == "ml-engineer"
    # The ML Engineer roadmap opens with 013 (Python and data; supporting), then 001.
    assert groups["recommended_next"]["course-013"]["reason_code"] == "next_in_roadmap"
    assert groups["recommended_next"]["course-001"]["reason_code"] == "roadmap_course"
    # A course outside the goal's roadmap is still open to enroll in.
    assert _post(learn_client, "/courses/course-012/enroll", who).status_code in (200, 409)   # 409 only because 012 is a shell here
    assert _post(learn_client, "/courses/course-013/enroll", who).status_code == 200


# ─── Tracks are roadmaps over the same canonical courses ────────────────────

def test_one_canonical_course_belongs_to_many_tracks_with_a_different_role_and_order_in_each(
    learn_client, learn_db, content,
):
    roadmaps = {}
    for slug in ("ml-engineer", "ai-developer", "ai-engineer"):
        response = _get(learn_client, f"/tracks/{slug}/courses")
        assert response.status_code == 200, response.text
        roadmaps[slug] = {c["course"]["slug"]: c for c in response.json()}
    ids = {slug: r["course-004"]["course"]["id"] for slug, r in roadmaps.items()}
    assert len(set(ids.values())) == 1                                       # the same course object everywhere
    assert learn_db.query(Course).filter(Course.slug == "course-004").count() == 1
    # course-004's weight per goal now comes from the canonical career-track
    # workflow mapping (seeds/curriculum.py:TRACK_WORKFLOWS): an optional ML
    # Engineer specialisation branch, core for AI Developer and AI Engineer.
    assert {s: r["course-004"]["track_role"] for s, r in roadmaps.items()} == {
        "ml-engineer": "optional", "ai-developer": "core", "ai-engineer": "core"}
    assert len({r["course-004"]["position"] for r in roadmaps.values()}) > 1     # its place differs per roadmap
    for r in roadmaps.values():
        positions = sorted(c["position"] for c in r.values())
        assert positions == list(range(1, len(positions) + 1))


def test_a_track_page_lists_the_roadmap_and_each_course_is_directly_enrollable(learn_client, content):
    tracks = _get(learn_client, "/tracks").json()
    assert {t["slug"] for t in tracks} == {"data-analyst", "ml-engineer", "ai-developer", "mlops-engineer", "ai-engineer"}
    who = register(learn_client)
    detail = _get(learn_client, "/tracks/ml-engineer", who).json()
    assert detail["slug"] == "ml-engineer" and detail["courses"]
    first = next(c for c in detail["courses"] if c["course"]["is_available"])
    assert first["course"]["enrollment"] is None
    # Enrolling from the roadmap is the same course enrollment - no track enrollment is created.
    assert _post(learn_client, f"/courses/{first['course']['slug']}/enroll", who).status_code == 200
    assert _get(learn_client, "/tracks/ml-engineer", who).json()["courses"][0]["course"]["id"] == detail["courses"][0]["course"]["id"]
    assert _get(learn_client, "/tracks/no-such-track").status_code == 404


# ─── Progress and lifecycle ─────────────────────────────────────────────────

def _mark(client, who, topic_id, lesson_ids=(), exercise_ids=()):
    for lesson_id in lesson_ids:
        r = client.post(f"/api/v1/tool-courses/topics/{topic_id}/progress", headers=who["headers"],
                        json={"lesson_id": lesson_id})
        assert r.status_code == 200, r.text
    for exercise_id in exercise_ids:
        r = client.post(f"/api/v1/tool-courses/topics/{topic_id}/progress", headers=who["headers"],
                        json={"exercise_id": exercise_id})
        assert r.status_code == 200, r.text


def _module_items(db, topic_id):
    from app.models.learning import Exercise
    return ([l.id for l in db.query(Lesson).filter(Lesson.tool_topic_id == topic_id).all()],
            [e.id for e in db.query(Exercise).filter(Exercise.tool_topic_id == topic_id).all()])


def test_progress_moves_the_enrollment_from_enrolled_to_in_progress_to_completed(learn_client, learn_db, content):
    who = register(learn_client)
    # Exercises are topic-level, not lesson-level, so they fall outside the
    # two-lesson free preview (access_service.free_lesson_ids) and need Pro
    # or a purchase; grant one directly so this test can exercise lifecycle
    # status transitions, which are its actual subject.
    learn_db.add(CourseEnrollment(user_id=who["id"], course_id=content["course-013"].id, source="purchase"))
    learn_db.commit()
    _post(learn_client, "/courses/course-013/enroll", who)
    first, second = topic_ids(learn_db, content["course-013"])

    lessons, exercises = _module_items(learn_db, first)
    _mark(learn_client, who, first, lessons[:1])
    progress = _get(learn_client, "/courses/course-013/progress", who).json()
    assert (progress["enrolled"], progress["status"]) == (True, "in_progress")
    assert 0 < progress["progress_percentage"] < 50 and progress["next_module"]["id"] == first
    assert _get(learn_client, "/my-courses", who).json()[0]["status"] == "in_progress"

    accept_written_answers(learn_db, who["id"], exercises)
    _mark(learn_client, who, first, lessons[1:], exercises)
    progress = _get(learn_client, "/courses/course-013/progress", who).json()
    assert progress["modules_completed"] == 1 and progress["next_module"]["id"] == second
    assert progress["progress_percentage"] == 50.0 and progress["status"] == "in_progress"

    lessons, exercises = _module_items(learn_db, second)
    accept_written_answers(learn_db, who["id"], exercises)
    _mark(learn_client, who, second, lessons, exercises)
    progress = _get(learn_client, "/courses/course-013/progress", who).json()
    assert (progress["status"], progress["progress_percentage"], progress["next_module"]) == ("completed", 100.0, None)
    row = learn_db.query(CourseEnrollment).filter(CourseEnrollment.user_id == who["id"]).one()
    assert row.learning_status == "completed" and row.started_at and row.completed_at
    assert _get(learn_client, "/my-courses", who).json()[0]["progress"] == 100.0


def test_working_in_a_course_enrolls_the_learner_who_had_not_enrolled(learn_client, learn_db, content):
    who = register(learn_client)
    (topic, *_rest) = topic_ids(learn_db, content["course-013"])
    lessons, _ = _module_items(learn_db, topic)
    _mark(learn_client, who, topic, lessons[:1])
    mine = _get(learn_client, "/my-courses", who).json()
    assert [(c["slug"], c["status"]) for c in mine] == [("course-013", "in_progress")]


def test_a_learner_can_pause_and_resume_a_course(learn_client, learn_db, content):
    who = register(learn_client)
    _post(learn_client, "/courses/course-013/enroll", who)
    paused = learn_client.patch(f"{API}/courses/course-013/enrollment", headers=who["headers"], json={"status": "paused"})
    assert paused.status_code == 200 and paused.json()["status"] == "paused"
    assert "course-013" not in {i["course"]["slug"] for i in _get(learn_client, "/recommendations", who).json()["continue_learning"]}
    resumed = learn_client.patch(f"{API}/courses/course-013/enrollment", headers=who["headers"], json={"status": "active"})
    assert resumed.json()["status"] == "enrolled"
    assert learn_client.patch(f"{API}/courses/course-013/enrollment", headers=who["headers"],
                              json={"status": "completed"}).status_code == 422       # only pause / resume
    other = register(learn_client)
    assert learn_client.patch(f"{API}/courses/course-013/enrollment", headers=other["headers"],
                              json={"status": "paused"}).status_code == 404


def test_existing_legacy_progress_stays_accessible_and_counts(learn_client, learn_db, learn_catalog):
    """Progress recorded on a track level before this change is still read, unchanged."""
    from tests.learning_fixtures import complete_level
    who = register(learn_client)
    complete_level(learn_db, who["id"], learn_catalog, 1)
    cards = _cards(learn_client, who)
    assert cards["ai-engineering-foundations"]["is_available"] is True
    progress = _get(learn_client, "/courses/ai-engineering-foundations/progress", who).json()
    assert progress["progress_percentage"] == 100.0 and progress["modules_completed"] == 2


# ─── Paid courses and the paywall ───────────────────────────────────────────

def _make_paid(db, course):
    course.is_free = False
    db.add(CourseOffer(course_id=course.id, price_amount=149900, currency="EGP", is_active=True))
    db.commit()


def test_a_paid_course_is_enrolled_only_with_a_purchase_and_still_needs_no_track(learn_client, learn_db, content):
    _make_paid(learn_db, content["course-013"])
    who = register(learn_client)
    assert _cards(learn_client)["course-013"]["is_free"] is False
    denied = _post(learn_client, "/courses/course-013/enroll", who)
    assert denied.status_code == 403 and denied.json()["detail"]["code"] == "COURSE_PURCHASE_REQUIRED"
    assert learn_db.query(CourseEnrollment).filter(CourseEnrollment.user_id == who["id"]).count() == 0

    learn_db.add(CourseEnrollment(user_id=who["id"], course_id=content["course-013"].id, source="purchase"))
    learn_db.commit()
    granted = _post(learn_client, "/courses/course-013/enroll", who)
    assert granted.status_code == 200 and granted.json()["created"] is False
    assert granted.json()["enrollment"]["source"] == "purchase"


def test_a_free_enrollment_never_opens_a_course_that_is_later_made_paid(learn_client, learn_db, content, monkeypatch):
    who = register(learn_client)
    assert _post(learn_client, "/courses/course-013/enroll", who).status_code == 200
    _make_paid(learn_db, content["course-013"])

    access = _get(learn_client, "/courses/course-013/access", who).json()
    assert access["has_access"] is False and access["reason"] == "purchase_required"
    # The course's first two lessons (by order) stay open as the Free plan's
    # preview regardless of the individual paid offer; the second module's
    # lessons are past that preview and are the ones actually locked.
    topic = topic_ids(learn_db, content["course-013"])[1]
    locked = learn_client.get(f"/api/v1/tool-courses/topics/{topic}", headers=who["headers"]).json()
    assert all(l["is_locked"] for l in locked["lessons"]) and all(not l["content"] for l in locked["lessons"])

    monkeypatch.setattr(kashier_service, "create_session",
                        lambda **kw: {"session_id": "sess-91", "checkout_url": "https://checkout.kashier.test/sess-91"})
    checkout = learn_client.post("/api/v1/billing/checkout", headers=who["headers"], json={"course_id": "course-013"})
    assert checkout.status_code == 200, checkout.text                       # not "already owned"


def test_a_paid_course_purchased_by_one_learner_is_not_open_to_another(learn_client, learn_db, content):
    _make_paid(learn_db, content["course-013"])
    buyer, other = register(learn_client), register(learn_client)
    learn_db.add(CourseEnrollment(user_id=buyer["id"], course_id=content["course-013"].id, source="purchase"))
    learn_db.commit()
    assert _post(learn_client, "/courses/course-013/enroll", buyer).status_code == 200
    assert _post(learn_client, "/courses/course-013/enroll", other).status_code == 403
