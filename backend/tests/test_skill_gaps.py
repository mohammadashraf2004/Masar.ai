"""
Skill-gap analysis and "why is this course here?" - the pure rules, one at a time,
on hand-built catalogues (no database). The shipped configuration is exercised
end to end in test_skill_gaps_api.py.

What these pin, in one place:

  - a skill is KNOWN only when the learner *declared* it;
  - a skill the learner has not declared is MISSING, or PARTIALLY_COVERED when a
    roadmap course teaching it is under way;
  - finishing a course never declares a skill, and declaring one never claims
    a prerequisite;
  - relevance comes from the roadmap (and the goal's required skills), so level,
    field and career goal change the gaps without a second progression system;
  - tools are ordinary skills - the existing "Already know" semantics, unchanged.
"""
from dataclasses import replace

from app.services.learning.domain import STATE_COMPLETED, STATE_REQUIRED, STATE_WAIVED, UserState
from app.services.learning.skill_gaps import (
    GROUP_FIELD, GROUP_GENERAL, GROUP_TOOLS, REASON_CAREER_REQUIREMENT, REASON_FIELD_REQUIREMENT,
    REASON_PREREQUISITE, REASON_SKILL_GAP, REASON_STAGE_REQUIREMENT, STATUS_KNOWN, STATUS_MISSING,
    STATUS_PARTIAL, calculate_skill_gaps, explain_courses,
)
from tests.test_learning_generator import catalog, course, plan, stage


def run(cat, declared=(), *, level="intermediate", fields=("nlp",), completion=None):
    """The roadmap for this learner, then the gap report and the per-course
    reasons over it - the same path the API takes."""
    completion = completion or {}
    state = UserState(
        completed_course_ids=frozenset(c for c, f in completion.items() if f >= 1.0),
        known_skill_slugs=frozenset(declared),
    )
    p = plan(cat, level=level, fields=fields, state=state)
    kw = dict(declared=frozenset(declared), completion=completion or None)
    return p, calculate_skill_gaps(cat, p, **kw), explain_courses(cat, p, **kw)


def by_slug(report):
    return {g.slug: g for g in report.skills}


def statuses(report):
    return {g.slug: g.status for g in report.skills}


FIVE = ("rag", "retrieval", "embeddings", "vector-databases", "evaluation")


def five_skill_course():
    return catalog([course(1, 2, fields=["nlp"], teaches=FIVE)], [(stage("rag", 1), "nlp")])


# ─── Basic ──────────────────────────────────────────────────────────────────

def test_with_nothing_declared_every_relevant_skill_is_a_gap():
    _, report, _ = run(five_skill_course())
    assert set(statuses(report).values()) == {STATUS_MISSING}
    assert set(statuses(report)) == set(FIVE)
    assert (report.required, report.known, report.partial, report.missing) == (5, 0, 0, 5)
    assert report.coverage_pct == 0.0


def test_a_declared_skill_is_known_and_no_longer_missing():
    _, report, _ = run(five_skill_course(), declared=["embeddings"])
    assert statuses(report)["embeddings"] == STATUS_KNOWN
    assert [s for s, st in statuses(report).items() if st == STATUS_MISSING] == sorted(set(FIVE) - {"embeddings"}, key=lambda s: s)
    assert (report.known, report.missing) == (1, 4) and report.coverage_pct == 20.0


def test_a_declared_skill_nothing_on_the_roadmap_teaches_is_not_a_gap_or_a_known_requirement():
    _, report, _ = run(five_skill_course(), declared=["knitting"])
    assert "knitting" not in statuses(report)                      # irrelevant: neither required nor counted
    assert report.required == 5 and report.known == 0


def test_the_report_is_deterministic():
    cat = five_skill_course()
    a = run(cat, declared=["rag", "evaluation"])[1]
    b = run(cat, declared=["evaluation", "rag"])[1]
    assert a == b


def test_an_empty_roadmap_has_no_coverage_rather_than_zero_percent():
    cat = catalog([], [])
    _, report, whys = run(cat)
    assert report.required == 0 and report.coverage_pct is None and whys == {}


# ─── Course coverage ────────────────────────────────────────────────────────

def test_a_course_teaching_five_skills_of_which_two_are_known():
    cat = five_skill_course()
    _, report, whys = run(cat, declared=["embeddings", "rag"])
    why = whys[1]
    assert (len(why.taught), len(why.known), len(why.to_gain)) == (5, 2, 3)
    assert set(why.known) == {"embeddings", "rag"} and set(why.to_gain) == {"retrieval", "vector-databases", "evaluation"}
    assert (report.known, report.missing) == (2, 3)


def test_known_and_to_gain_partition_what_the_course_teaches():
    _, _, whys = run(five_skill_course(), declared=["rag", "unrelated"])
    why = whys[1]
    assert set(why.known) | set(why.to_gain) == set(why.taught) and not set(why.known) & set(why.to_gain)
    assert "unrelated" not in why.known                            # only what the course teaches is compared


def test_knowing_every_skill_of_a_course_leaves_it_with_no_gap():
    p, report, whys = run(five_skill_course(), declared=FIVE)
    assert p.stages[0].courses[0].state == STATE_WAIVED           # the existing strict rule, unchanged
    assert whys[1].to_gain == () and report.missing == 0 and report.known == 5
    assert REASON_SKILL_GAP not in whys[1].reasons                 # nothing left to gain


def test_a_partly_known_course_is_not_waived_and_says_what_it_would_add():
    p, _, whys = run(five_skill_course(), declared=["rag"])
    assert p.stages[0].courses[0].state == STATE_REQUIRED
    assert REASON_SKILL_GAP in whys[1].reasons


# ─── Prerequisites ──────────────────────────────────────────────────────────

def test_declaring_a_skill_does_not_claim_its_prerequisites_skills():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["llms"]),
         course(2, 2, fields=["nlp"], teaches=["rag"], prereqs=[1])],
        [(stage("s", 1, 2), "nlp")],
    )
    _, report, _ = run(cat, declared=["rag"])
    assert statuses(report) == {"llms": STATUS_MISSING, "rag": STATUS_KNOWN}   # RAG does not imply LLMs


def test_a_prerequisite_course_is_explained_as_one():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["llms"]),
         course(2, 2, fields=["nlp"], teaches=["rag"], prereqs=[1])],
        [(stage("s", 2), "nlp")],                                  # the template lists only the one that needs it
    )
    p, _, whys = run(cat)
    assert [c.course_id for c in p.stages[0].courses] == [1, 2]    # the generator pulled the prerequisite in
    assert whys[1].reasons.count(REASON_PREREQUISITE) == 1 and REASON_STAGE_REQUIREMENT not in whys[1].reasons
    assert whys[1].prerequisite_for == (2,)
    assert REASON_STAGE_REQUIREMENT in whys[2].reasons and REASON_PREREQUISITE not in whys[2].reasons


# ─── Tools: the existing semantics, unchanged ───────────────────────────────

def tool_catalog():
    cat = catalog([course(1, 2, fields=["nlp"], teaches=["rag", "langchain"])], [(stage("s", 1), "nlp")])
    return replace(cat, tools=frozenset({"langchain"}))


def test_a_tool_a_course_teaches_is_one_of_the_skills_it_teaches():
    p, report, whys = run(tool_catalog(), declared=["rag"])
    assert "langchain" in whys[1].taught and "langchain" in whys[1].to_gain
    assert p.stages[0].courses[0].state == STATE_REQUIRED          # the capability alone does not waive it
    assert by_slug(report)["langchain"].is_tool is True and by_slug(report)["rag"].is_tool is False


def test_knowing_the_tool_does_not_make_the_capability_known_or_the_reverse():
    _, report, _ = run(tool_catalog(), declared=["langchain"])
    assert statuses(report) == {"rag": STATUS_MISSING, "langchain": STATUS_KNOWN}
    _, report, _ = run(tool_catalog(), declared=["rag"])
    assert statuses(report) == {"rag": STATUS_KNOWN, "langchain": STATUS_MISSING}


def test_declaring_both_waives_the_course_exactly_as_before():
    p, report, _ = run(tool_catalog(), declared=["rag", "langchain"])
    assert p.stages[0].courses[0].state == STATE_WAIVED and report.missing == 0


def test_tools_are_grouped_apart_from_field_skills():
    _, report, _ = run(tool_catalog())
    kinds = [(g.kind, [s.slug for s in g.skills]) for g in report.groups]
    assert kinds == [(GROUP_FIELD, ["rag"]), (GROUP_TOOLS, ["langchain"])]


# ─── Field and career goal ──────────────────────────────────────────────────

def test_the_routes_field_decides_which_skills_are_relevant():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["rag"]), course(2, 2, fields=["computer-vision"], teaches=["detection"])],
        [(stage("nlp-s", 1), "nlp"), (stage("cv-s", 2), "computer-vision")],
    )
    assert set(statuses(run(cat, fields=("nlp",))[1])) == {"rag"}
    assert set(statuses(run(cat, fields=("computer-vision",))[1])) == {"detection"}


def test_gaps_are_grouped_under_the_field_most_of_their_courses_belong_to():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["embeddings"]), course(2, 2, fields=["nlp", "computer-vision"], teaches=["embeddings"]),
         course(3, 2, fields=["computer-vision"], teaches=["embeddings"])],
        [(stage("a", 1, 2, 3), None)],
    )
    _, report, _ = run(cat, fields=("nlp", "computer-vision"))
    # nlp has 2 courses, computer-vision 2: a tie, broken by the configured field order (nlp first).
    assert by_slug(report)["embeddings"].group_field == "nlp"


def test_skills_no_field_course_teaches_are_general():
    cat = catalog([course(1, 2, fields=[], teaches=["system-design"])], [stage("core", 1)])
    _, report, _ = run(cat, fields=())
    assert [g.kind for g in report.groups] == [GROUP_GENERAL]


def test_a_skill_the_career_goal_requires_is_relevant_even_when_no_course_teaches_it():
    cat = catalog([course(1, 2, fields=["nlp"], teaches=["rag"])], [(stage("s", 1), "nlp")], role_skills=["statistics"])
    _, report, _ = run(cat)
    stats = by_slug(report)["statistics"]
    assert (stats.status, stats.is_goal_required, stats.course_count, stats.stage_slug) == (STATUS_MISSING, True, 0, None)
    assert by_slug(report)["rag"].is_goal_required is False        # nothing was invented, and nothing over-flagged


def test_the_career_goal_is_a_reason_only_for_courses_that_teach_its_required_skills():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["rag"]), course(2, 2, fields=["nlp"], teaches=["prompting"])],
        [(stage("s", 1, 2), "nlp")], role_skills=["rag"],
    )
    _, _, whys = run(cat)
    assert REASON_CAREER_REQUIREMENT in whys[1].reasons and whys[1].goal_skills == ("rag",)
    assert REASON_CAREER_REQUIREMENT not in whys[2].reasons and whys[2].goal_skills == ()


# ─── Level ──────────────────────────────────────────────────────────────────

def level_catalog():
    return catalog(
        [course(1, 1, fields=["nlp"], teaches=["llms"]), course(2, 3, fields=["nlp"], teaches=["agents"])],
        [(stage("basics", 1), "nlp"), (stage("advanced", 2), "nlp")],
    )


def test_a_beginner_and_an_advanced_learner_do_not_get_the_same_gaps():
    _, beginner, _ = run(level_catalog(), level="beginner")
    _, advanced, _ = run(level_catalog(), level="advanced")
    assert set(statuses(beginner)) == {"llms", "agents"}
    assert set(statuses(advanced)) == {"agents"}                   # the basics are optional at their level


def test_a_beginners_immediate_gaps_are_the_current_stage_and_the_rest_come_later():
    _, report, _ = run(level_catalog(), level="beginner")
    assert report.current_stage_slug == "basics"
    assert by_slug(report)["llms"].is_immediate is True
    assert by_slug(report)["agents"].is_immediate is False and by_slug(report)["agents"].stage_slug == "advanced"
    assert report.immediate == 1


def test_an_optional_courses_skills_are_not_gaps_unless_the_goal_requires_them():
    _, report, _ = run(level_catalog(), level="advanced")
    assert "llms" not in statuses(report)
    cat = replace(level_catalog(), roles={"eng": replace(level_catalog().roles["eng"], required_skill_slugs=frozenset({"llms"}))})
    _, report, _ = run(cat, level="advanced")
    assert statuses(report)["llms"] == STATUS_MISSING              # required by the goal: still a gap


# ─── Multimodal ─────────────────────────────────────────────────────────────

def multimodal_catalog():
    return catalog(
        [course(1, 2, fields=["nlp"], teaches=["transformers"]),
         course(2, 2, fields=["computer-vision"], teaches=["cnn"]),
         course(3, 3, fields=["multimodal"], teaches=["vlm"])],
        [(stage("nlp-s", 1), "nlp"), (stage("cv-s", 2), "computer-vision"), (stage("mm-s", 3), "multimodal")],
    )


def test_multimodal_gaps_follow_the_prerequisite_route_the_generator_built():
    p, report, _ = run(multimodal_catalog(), level="advanced", fields=("multimodal",))
    assert "multimodal" in p.effective_field_slugs and len(p.effective_field_slugs) == 2   # one modality routed in
    added = next(f for f in p.effective_field_slugs if f != "multimodal")
    assert "vlm" in statuses(report)                               # never blocked
    routed_skill = {"nlp": "transformers", "computer-vision": "cnn"}[added]
    assert statuses(report)[routed_skill] == STATUS_MISSING


def test_what_a_prerequisite_route_teaches_counts_even_when_its_courses_are_below_the_learners_level():
    p, report, _ = run(multimodal_catalog(), level="advanced", fields=("multimodal",))
    added = next(f for f in p.effective_field_slugs if f != "multimodal")
    routed_course = next(c for s in p.stages for c in s.courses if c.course_id == {"nlp": 1, "computer-vision": 2}[added])
    assert routed_course.state == "optional"                       # the generator is unchanged: below their level...
    assert statuses(report)[{"nlp": "transformers", "computer-vision": "cnn"}[added]] == STATUS_MISSING   # ...but still a gap
    assert by_slug(report)[{"nlp": "transformers", "computer-vision": "cnn"}[added]].is_immediate is False


def test_a_declared_modality_removes_that_route_and_its_gaps():
    _, report, _ = run(multimodal_catalog(), declared=["transformers"], level="advanced", fields=("multimodal",))
    assert "transformers" not in statuses(report) or statuses(report)["transformers"] == STATUS_KNOWN
    assert statuses(report)["vlm"] == STATUS_MISSING


# ─── Completed courses vs declared skills ───────────────────────────────────

def test_finishing_a_course_does_not_declare_its_skills():
    cat = five_skill_course()
    p, report, whys = run(cat, completion={1: 1.0})
    assert p.stages[0].courses[0].state == STATE_COMPLETED         # completion is untouched by any gap
    assert report.known == 0 and report.missing == 5              # ...and declares nothing
    assert all(g.covered_by_completed for g in report.skills)      # the report says why they are still open
    assert REASON_SKILL_GAP not in whys[1].reasons                 # a finished course is not "to do"


def test_declared_skills_and_completion_are_reported_independently():
    _, report, _ = run(five_skill_course(), declared=["rag"], completion={1: 1.0})
    g = by_slug(report)
    assert g["rag"].status == STATUS_KNOWN and g["rag"].covered_by_completed is False   # declared: nothing to hint at
    assert g["retrieval"].status == STATUS_MISSING and g["retrieval"].covered_by_completed is True


def test_a_course_under_way_makes_its_undeclared_skills_partially_covered():
    _, report, _ = run(five_skill_course(), declared=["rag"], completion={1: 0.5})
    assert statuses(report)["rag"] == STATUS_KNOWN                 # declaring beats being under way
    assert {s for s, st in statuses(report).items() if st == STATUS_PARTIAL} == set(FIVE) - {"rag"}
    assert (report.known, report.partial, report.missing) == (1, 4, 0)


# ─── Why this course? ───────────────────────────────────────────────────────

def test_a_course_can_have_several_reasons_and_each_comes_from_data():
    cat = catalog(
        [course(1, 2, fields=["nlp"], teaches=["rag", "retrieval"]), course(2, 2, fields=["nlp"], teaches=["agents"], prereqs=[1])],
        [(stage("s", 1, 2), "nlp")], role_skills=["rag"],
    )
    _, _, whys = run(cat, declared=["retrieval"])
    assert whys[1].reasons == (REASON_CAREER_REQUIREMENT, REASON_FIELD_REQUIREMENT, REASON_STAGE_REQUIREMENT,
                               REASON_SKILL_GAP, REASON_PREREQUISITE)
    assert whys[1].route_fields == ("nlp",) and whys[1].stage_slug == "s"
    assert whys[1].known == ("retrieval",) and whys[1].to_gain == ("rag",)
    assert whys[2].reasons == (REASON_FIELD_REQUIREMENT, REASON_STAGE_REQUIREMENT, REASON_SKILL_GAP)


def test_a_course_outside_the_learners_fields_has_no_field_reason():
    cat = catalog([course(1, 2, fields=[], teaches=["system-design"])], [stage("core", 1)])
    _, _, whys = run(cat, fields=())
    assert whys[1].route_fields == () and REASON_FIELD_REQUIREMENT not in whys[1].reasons


def test_a_prerequisite_already_finished_is_not_still_needed_by_anything():
    cat = catalog(
        [course(1, 1, fields=["nlp"], teaches=["llms"]), course(2, 2, fields=["nlp"], teaches=["rag"], prereqs=[1])],
        [(stage("s", 1, 2), "nlp")],
    )
    _, _, whys = run(cat, completion={1: 1.0})
    assert whys[1].prerequisite_for == (2,) and REASON_PREREQUISITE in whys[1].reasons   # course 2 is still to do
    _, _, whys = run(cat, completion={1: 1.0, 2: 1.0})
    assert whys[1].prerequisite_for == ()                          # nothing left that needs it
