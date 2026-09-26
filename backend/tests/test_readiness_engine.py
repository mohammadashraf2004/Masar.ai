"""
The readiness rules on their own: no database, no HTTP, a hand-built catalogue.

Readiness is deterministic and explainable, so each rule is pinned here:
how a skill's strength is decided from evidence, how a course's readiness follows
from its prerequisites, and what a learner is told to review. The API behaviour built
on it (enrolling never blocked, server-side grading) is in `test_independent_enrollment.py`.
"""
import pytest

from app.services.learning import readiness as R
from app.services.learning.domain import Catalog, CourseInfo


def course(cid, *, rank=1, teaches=(), required=(), recommended=(), assumes=(), available=True):
    return CourseInfo(
        id=cid, slug=f"c{cid}", level_rank=rank, teaches=frozenset(teaches), assumes=frozenset(assumes),
        prerequisite_ids=frozenset(required), recommended_prerequisite_ids=frozenset(recommended),
        is_available=available,
    )


def catalog(*courses):
    return Catalog(courses={c.id: c for c in courses})


# python(1, beginner) -> ml(2, intermediate) -> dl(3, advanced, teaches deep-learning)
PY = course(1, rank=1, teaches=["python"])
ML = course(2, rank=2, teaches=["machine-learning", "numpy"], required=[1])
DL = course(3, rank=3, teaches=["deep-learning"], required=[2], recommended=[1])
CAT = catalog(PY, ML, DL)


def ev(**kwargs):
    return R.LearnerEvidence(**kwargs)


# ─── Proficiency ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("strength, level", [
    (None, "not_assessed"), (0.0, "not_assessed"), (0.1, "beginner"), (0.59, "beginner"),
    (0.6, "intermediate"), (0.79, "intermediate"), (0.8, "advanced"), (1.0, "advanced"),
])
def test_a_strength_maps_to_one_of_four_proficiency_levels(strength, level):
    assert R.level_for(strength) == level


def test_finishing_a_course_is_capped_by_that_courses_own_level():
    done = lambda cid: ev(completion={cid: 1.0})            # noqa: E731
    assert R.skill_strength(CAT, done(1), "python") == pytest.approx(0.7)             # beginner course -> intermediate
    assert R.skill_strength(CAT, done(2), "machine-learning") == pytest.approx(0.8)   # intermediate course -> advanced
    assert R.skill_strength(CAT, done(3), "deep-learning") == pytest.approx(0.9)
    assert R.level_for(R.skill_strength(CAT, done(1), "python")) == "intermediate"
    assert R.level_for(R.skill_strength(CAT, done(2), "machine-learning")) == "advanced"


def test_part_of_a_course_is_part_of_the_strength_and_no_evidence_is_none_not_zero():
    assert R.skill_strength(CAT, ev(completion={1: 0.5}), "python") == pytest.approx(0.35)
    assert R.skill_strength(CAT, ev(), "python") is None
    assert R.skill_strength(CAT, ev(completion={1: 1.0}), "no-such-skill") is None


def test_quiz_results_count_only_once_enough_quizzes_were_taken():
    few = ev(quiz={1: (1.0, 1)})
    enough = ev(quiz={1: (1.0, 3)})
    assert R.skill_strength(CAT, few, "python") == pytest.approx(0.7 / 3)
    assert R.skill_strength(CAT, enough, "python") == pytest.approx(0.7)
    assert R.skill_strength(CAT, ev(quiz={1: (0.5, 6)}), "python") == pytest.approx(0.35)


def test_evidence_is_the_best_single_source_never_a_sum():
    both = ev(completion={1: 0.3}, assessed={"python": 0.8})
    assert R.skill_strength(CAT, both, "python") == pytest.approx(0.6)                # the check (0.75 x 0.8), not 0.21 + 0.6
    assert R.skill_strength(CAT, ev(assessed={"python": 1.0}), "python") == pytest.approx(R.ASSESSMENT_WEIGHT)


def test_a_claim_is_weaker_than_evidence_and_never_reads_as_strong_on_its_own():
    declared = ev(declared={"python": ("known", "self_declared")})
    assert R.skill_strength(CAT, declared, "python") == R.DECLARED_STRENGTH < R.INTERMEDIATE_AT
    assert R.skill_strength(CAT, ev(declared={"python": ("known", "assessment")}), "python") == R.STORED_STRENGTH
    assert R.skill_strength(CAT, ev(declared={"python": ("mastered", "self_declared")}), "python") == R.MASTERED_STRENGTH
    assert R.skill_strength(CAT, ev(priors={"python": 0.45}), "python") == 0.45
    assert R.skill_strength(CAT, ev(priors={"python": 0.0}), "python") is None


def test_an_unpublished_course_teaches_nothing_yet():
    shell = catalog(course(1, teaches=["python"], available=False))
    assert R.skill_strength(shell, ev(completion={1: 1.0}), "python") is None


def test_skill_levels_are_per_skill_never_one_global_level():
    levels = R.skill_levels(type("B", (), {"catalog": CAT}), ev(completion={1: 1.0, 2: 1.0}))
    assert levels == {"python": "intermediate", "machine-learning": "advanced", "numpy": "advanced",
                      "deep-learning": "not_assessed"}


# ─── Requirements ───────────────────────────────────────────────────────────

def test_a_courses_requirements_are_the_skills_its_prerequisites_teach():
    reqs = {r.skill: r for r in R.requirements_for(CAT, DL)}
    assert set(reqs) == {"machine-learning", "numpy", "python"}
    assert reqs["machine-learning"].required and reqs["numpy"].required
    assert reqs["python"].required is False and reqs["python"].courses == (1,)           # recommended only
    assert R.requirements_for(CAT, PY) == []


def test_a_skill_taught_by_a_required_and_a_recommended_prerequisite_is_required():
    both = catalog(course(1, teaches=["python"]), course(2, teaches=["python"]),
                   course(3, required=[1], recommended=[2]))
    (req,) = R.requirements_for(both, both.courses[3])
    assert req.required and set(req.courses) == {1, 2}


def test_a_skill_a_course_explicitly_assumes_is_a_requirement_too():
    cat = catalog(course(1, teaches=["sql"]), course(2, assumes=["sql"]))
    (req,) = R.requirements_for(cat, cat.courses[2])
    assert (req.skill, req.required, req.courses) == ("sql", True, ())


def test_a_prerequisite_that_is_not_published_yet_is_not_asked_of_the_learner():
    cat = catalog(course(1, teaches=["python"], available=False), course(2, required=[1]))
    assert R.requirements_for(cat, cat.courses[2]) == []
    assert R.evaluate(cat, cat.courses[2], ev()).state == R.READY


# ─── Readiness ──────────────────────────────────────────────────────────────

def test_a_course_with_no_prerequisites_is_ready_for_everyone():
    result = R.evaluate(CAT, PY, ev())
    assert (result.state, result.score, result.has_prerequisites, result.review) == ("ready", 100, False, ())


def test_no_evidence_at_all_is_not_assessed_not_failed():
    result = R.evaluate(CAT, ML, ev())
    assert result.state == R.NOT_ASSESSED and result.score == 0
    assert all(s.standing == "unknown" and s.level == "not_assessed" for s in result.standings)


def test_readiness_states_follow_the_prerequisites_the_learner_has_shown():
    ready = R.evaluate(CAT, DL, ev(completion={1: 1.0, 2: 1.0}))
    assert ready.state == R.READY and ready.gaps == [] and ready.review == ()

    # Only the recommended prerequisite is missing: still mostly ready.
    mostly = R.evaluate(CAT, DL, ev(completion={2: 1.0}))
    assert mostly.state == R.MOSTLY_READY and {s.skill for s in mostly.gaps} == {"python"}
    assert [t.course_id for t in mostly.review] == [1]

    # A required prerequisite is untouched while the learner has other evidence.
    needs = R.evaluate(CAT, DL, ev(completion={1: 1.0}))
    assert needs.state == R.NEEDS_FOUNDATION
    assert {s.skill for s in needs.gaps} == {"machine-learning", "numpy"} and needs.review[0].course_id == 2


def test_a_declared_skill_helps_but_does_not_make_a_learner_ready():
    claimed = R.evaluate(CAT, ML, ev(declared={"python": ("known", "self_declared")}))
    assert claimed.state == R.MOSTLY_READY and claimed.standings[0].standing == R.SKILL_PARTIAL
    assert claimed.score < R.READY_SCORE and [t.course_id for t in claimed.review] == [1]    # review is still suggested


def test_the_score_is_a_summary_the_state_does_not_rest_on_it_alone():
    weak_required = catalog(course(1, teaches=["a"]), course(2, teaches=["b"]),
                            course(3, required=[1], recommended=[2]))
    evidence = ev(completion={2: 1.0})                    # the *recommended* one is fully done, the required one not at all
    result = R.evaluate(weak_required, weak_required.courses[3], evidence)
    assert result.score == 33                              # 1 of 3 weighted parts ...
    assert result.state == R.NEEDS_FOUNDATION              # ... and a required skill is untouched


def test_readiness_does_not_depend_on_how_hard_the_course_is():
    cat = catalog(course(1, teaches=["a"]),
                  course(2, rank=1, required=[1]), course(3, rank=3, required=[1]))
    learner = ev(completion={1: 1.0})
    assert R.evaluate(cat, cat.courses[2], learner).state == R.evaluate(cat, cat.courses[3], learner).state == R.READY


def test_review_names_the_prerequisite_course_required_first_and_never_a_finished_one():
    cat = catalog(
        course(1, rank=1, teaches=["a"]), course(2, rank=1, teaches=["b"]), course(3, rank=2, teaches=["c"]),
        course(4, rank=3, required=[3], recommended=[1, 2]),
    )
    result = R.evaluate(cat, cat.courses[4], ev(completion={2: 1.0}))
    assert [(t.course_id, t.required) for t in result.review] == [(3, True), (1, False)]     # required first; 2 is done
    assert result.review[0].skills == ("c",)


def test_review_falls_back_to_any_published_course_that_teaches_an_assumed_skill():
    cat = catalog(course(1, teaches=["sql"]), course(2, assumes=["sql"]))
    result = R.evaluate(cat, cat.courses[2], ev())
    assert result.review == (R.ReviewTarget(1, ("sql",), True),)


def test_evidence_about_other_skills_is_not_an_assessment_of_these_prerequisites():
    other = catalog(course(1, teaches=["x"]), course(2, teaches=["y"]), course(3, required=[2]))
    result = R.evaluate(other, other.courses[3], ev(completion={1: 1.0}))
    assert result.state == R.NOT_ASSESSED            # nothing about *this* course's prerequisites is known yet
    assert result.review[0].course_id == 2
