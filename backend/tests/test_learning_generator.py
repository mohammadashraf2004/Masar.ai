"""
The path generator's rules, one at a time, on hand-built catalogues.

Pure: no database. Each test builds only the catalogue it needs, so a failure
names the rule that broke. The shipped configuration is exercised end to end in
test_learning_api.py; this file pins the rules themselves.
"""
import pytest

from app.services.learning.domain import (
    ADVISORY_FIELD_ABOVE_LEVEL, ADVISORY_NO_AVAILABLE_COURSES, ADVISORY_NO_TEMPLATE,
    ADVISORY_PREREQUISITE_CYCLE, ADVISORY_PREREQUISITE_ORDER, ADVISORY_PREREQUISITE_ROUTE_ADDED,
    ADVISORY_PREREQUISITES_RECOMMENDED, STATE_COMPLETED, STATE_OPTIONAL, STATE_REQUIRED,
    STATE_WAIVED, Catalog, CourseInfo, FieldInfo, LevelInfo, RoleInfo, StageInfo, TemplateInfo,
    TemplateStageInfo, UserState,
)
from app.services.learning.path_generator import PathGenerationError, generate_plan

LEVELS = {
    "beginner": LevelInfo(1, "beginner", 1),
    "intermediate": LevelInfo(2, "intermediate", 2),
    "advanced": LevelInfo(3, "advanced", 3),
}


def field(slug, position, **kw):
    return FieldInfo(id=position, slug=slug, position=position, min_level_rank=kw.pop("min_level_rank", None), **kw)


FIELDS = {
    "nlp": field("nlp", 1),
    "computer-vision": field("computer-vision", 2),
    "speech": field("speech", 3),
    "multimodal": field(
        "multimodal", 4, min_level_rank=3,
        prerequisite_slugs=("nlp", "computer-vision", "speech"),
        prerequisite_min_required=1, prerequisite_recommended=2,
    ),
}


def course(cid, level, *, fields=(), roles=("eng",), teaches=(), prereqs=(), hours=10.0, available=True):
    return CourseInfo(
        id=cid, slug=f"c{cid}", level_rank=level, field_slugs=frozenset(fields),
        role_slugs=frozenset(roles), teaches=frozenset(teaches),
        prerequisite_ids=frozenset(prereqs), estimated_hours=hours, is_available=available,
    )


def stage(slug, *course_ids, kind="learning"):
    return StageInfo(slug=slug, phase="specialization", kind=kind, course_ids=tuple(course_ids))


def template(*entries, role="eng"):
    return TemplateInfo("t", role, tuple(TemplateStageInfo(s, f) for s, f in entries))


def catalog(courses=(), stages=(), *, fields=None, role_skills=(), tmpl=True):
    entries = [(s, None) if isinstance(s, StageInfo) else s for s in stages]
    return Catalog(
        levels=LEVELS,
        fields=FIELDS if fields is None else fields,
        roles={"eng": RoleInfo(1, "eng", 2, required_skill_slugs=frozenset(role_skills))},
        courses={c.id: c for c in courses},
        templates={"eng": template(*entries)} if tmpl else {},
    )


def plan(cat, level="intermediate", fields=("nlp",), state=UserState()):
    return generate_plan(cat, level_slug=level, role_slug="eng", field_slugs=list(fields), state=state)


def states(p):
    return {c.course_id: c.state for s in p.stages for c in s.courses}


# ─── Validation ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("kwargs,code", [
    (dict(level_slug="expert", role_slug="eng", field_slugs=[]), "unknown_level"),
    (dict(level_slug="beginner", role_slug="chef", field_slugs=[]), "unknown_career_goal"),
    (dict(level_slug="beginner", role_slug="eng", field_slugs=["alchemy"]), "unknown_field"),
])
def test_unknown_input_is_rejected_with_a_code(kwargs, code):
    with pytest.raises(PathGenerationError) as info:
        generate_plan(catalog(), **kwargs)
    assert info.value.code == code


def test_same_input_gives_the_same_plan():
    cat = catalog([course(1, 1, fields=["nlp"]), course(2, 2, fields=["nlp"])],
                  [(stage("s", 1, 2), "nlp")])
    assert plan(cat) == plan(cat)


def test_duplicate_requested_fields_are_collapsed():
    p = plan(catalog(), fields=["nlp", "nlp", "speech"])
    assert p.field_slugs == ["nlp", "speech"]


# ─── Stages ─────────────────────────────────────────────────────────────────

def test_field_tied_stage_appears_only_with_its_field():
    cat = catalog(
        [course(1, 2), course(2, 2), course(3, 2)],
        [(stage("core", 1), None), (stage("nlp-stage", 2), "nlp"), (stage("cv-stage", 3), "computer-vision")],
    )
    assert [s.slug for s in plan(cat, fields=["nlp"]).stages] == ["core", "nlp-stage"]
    assert [s.slug for s in plan(cat, fields=["computer-vision"]).stages] == ["core", "cv-stage"]
    assert [s.slug for s in plan(cat, fields=["nlp", "computer-vision"]).stages] == ["core", "nlp-stage", "cv-stage"]
    assert [s.slug for s in plan(cat, fields=[]).stages] == ["core"]


def test_stage_positions_are_consecutive_from_one():
    cat = catalog([course(1, 2)], [(stage("a", 1), None), (stage("b"), "speech"), (stage("c"), None)])
    assert [s.position for s in plan(cat, fields=["nlp"]).stages] == [1, 2]


def test_unpublished_courses_are_counted_as_upcoming_not_offered():
    cat = catalog([course(1, 2), course(2, 2, available=False), course(3, 2, available=False)],
                  [stage("s", 1, 2, 3)])
    s = plan(cat).stages[0]
    assert [c.course_id for c in s.courses] == [1]
    assert s.upcoming_count == 2


def test_a_course_in_two_stages_appears_once_per_path():
    cat = catalog([course(1, 2), course(2, 2)], [stage("a", 1, 2), stage("b", 2)])
    p = plan(cat)
    assert [c.course_id for c in p.stages[0].courses] == [1, 2]
    assert p.stages[1].courses == []


def test_a_path_with_nothing_available_says_so():
    cat = catalog([course(1, 2, available=False)], [stage("s", 1)])
    p = plan(cat)
    assert ADVISORY_NO_AVAILABLE_COURSES in [a.code for a in p.advisories]
    assert p.estimated_hours == 0


# ─── Course states ──────────────────────────────────────────────────────────

def test_courses_at_or_above_the_level_are_required():
    cat = catalog([course(1, 2), course(2, 3)], [stage("s", 1, 2)])
    assert states(plan(cat, level="intermediate")) == {1: STATE_REQUIRED, 2: STATE_REQUIRED}


def test_courses_below_the_level_are_optional_not_removed():
    cat = catalog([course(1, 1), course(2, 2)], [stage("s", 1, 2)])
    p = plan(cat, level="advanced")
    assert states(p) == {1: STATE_OPTIONAL, 2: STATE_OPTIONAL}
    assert p.stages[0].courses[0].reason == "below_level"


def test_beginners_are_not_treated_as_advanced():
    cat = catalog([course(1, 1)], [stage("s", 1)])
    assert states(plan(cat, level="beginner")) == {1: STATE_REQUIRED}


def test_below_level_course_stays_required_when_it_closes_a_required_skill_gap():
    cat = catalog([course(1, 1, teaches=["evaluation"]), course(2, 1, teaches=["trivia"])],
                  [stage("s", 1, 2)], role_skills=["evaluation"])
    assert states(plan(cat, level="advanced")) == {1: STATE_REQUIRED, 2: STATE_OPTIONAL}


def test_a_skill_the_learner_declares_turns_the_gap_into_optional():
    # The course also teaches something the learner did not declare, so it is not
    # waived (see test_learning_personalized.py) - it just stops being *needed*.
    cat = catalog([course(1, 1, teaches=["evaluation", "metrics"])], [stage("s", 1)], role_skills=["evaluation"])
    p = plan(cat, level="advanced", state=UserState(known_skill_slugs=frozenset({"evaluation"})))
    assert states(p) == {1: STATE_OPTIONAL}


def test_a_skill_learned_by_finishing_a_course_closes_the_gap_too():
    cat = catalog([course(1, 2, teaches=["evaluation"]), course(2, 1, teaches=["evaluation"])],
                  [stage("s", 1, 2)], role_skills=["evaluation"])
    p = plan(cat, level="advanced", state=UserState(completed_course_ids=frozenset({1})))
    assert states(p) == {1: STATE_COMPLETED, 2: STATE_OPTIONAL}


def test_completed_and_waived_courses_are_marked_and_not_counted_as_remaining_work():
    cat = catalog([course(1, 2, hours=5), course(2, 2, hours=7), course(3, 2, hours=11)],
                  [stage("s", 1, 2, 3)])
    p = plan(cat, state=UserState(completed_course_ids=frozenset({1}), waived_course_ids=frozenset({2})))
    assert states(p) == {1: STATE_COMPLETED, 2: STATE_WAIVED, 3: STATE_REQUIRED}
    assert p.estimated_hours == 11


def test_hours_count_only_required_courses():
    cat = catalog([course(1, 1, hours=4), course(2, 2, hours=6)], [stage("s", 1, 2)])
    assert plan(cat, level="advanced").estimated_hours == 0
    assert plan(cat, level="beginner").estimated_hours == 10


# ─── Field route: level and prerequisites ───────────────────────────────────

def test_multimodal_below_its_level_is_advised_not_blocked():
    cat = catalog([course(1, 3, fields=["multimodal"])], [(stage("mm", 1), "multimodal")])
    p = plan(cat, level="beginner", fields=["multimodal"])
    codes = [a.code for a in p.advisories]
    assert ADVISORY_FIELD_ABOVE_LEVEL in codes
    above = next(a for a in p.advisories if a.code == ADVISORY_FIELD_ABOVE_LEVEL)
    assert above.params == {"field": "multimodal", "level": "beginner", "min_level": "advanced"}
    assert "multimodal" in p.effective_field_slugs
    assert [s.slug for s in p.stages] == ["mm"]  # still reachable, at the end of its route


def test_multimodal_with_no_modality_gets_one_added_preferring_published_content():
    cat = catalog(
        [course(1, 2, fields=["speech"], available=False), course(2, 2, fields=["nlp"]),
         course(3, 3, fields=["multimodal"])],
        [(stage("nlp-s", 2), "nlp"), (stage("mm", 3), "multimodal")],
    )
    p = plan(cat, level="advanced", fields=["multimodal"])
    added = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITE_ROUTE_ADDED)
    assert added.params == {"field": "multimodal", "added": ["nlp"]}  # nlp has content; speech does not
    assert p.effective_field_slugs == ["nlp", "multimodal"]  # prerequisite before dependent
    assert [s.slug for s in p.stages] == ["nlp-s", "mm"]


def test_a_selected_modality_satisfies_the_requirement_with_no_route_added():
    cat = catalog([course(1, 3, fields=["multimodal"])], [(stage("mm", 1), "multimodal")])
    p = plan(cat, level="advanced", fields=["speech", "multimodal"])
    assert ADVISORY_PREREQUISITE_ROUTE_ADDED not in [a.code for a in p.advisories]
    assert p.effective_field_slugs == ["speech", "multimodal"]


def test_one_modality_meets_the_requirement_but_two_are_recommended():
    cat = catalog([], [])
    p = plan(cat, level="advanced", fields=["nlp", "multimodal"])
    rec = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITES_RECOMMENDED)
    assert rec.params["have"] == 1 and rec.params["recommended"] == 2
    assert set(rec.params["suggested"]) == {"computer-vision", "speech"}


def test_two_modalities_silence_the_recommendation():
    p = plan(catalog(), level="advanced", fields=["nlp", "speech", "multimodal"])
    assert ADVISORY_PREREQUISITES_RECOMMENDED not in [a.code for a in p.advisories]


def test_finished_courses_count_as_knowing_a_prerequisite_field():
    cat = catalog(
        [course(1, 2, fields=["nlp"]), course(2, 2, fields=["nlp"]), course(3, 3, fields=["multimodal"])],
        [(stage("mm", 3), "multimodal")],
    )
    done = UserState(completed_course_ids=frozenset({1, 2}))
    p = plan(cat, level="advanced", fields=["multimodal"], state=done)
    assert ADVISORY_PREREQUISITE_ROUTE_ADDED not in [a.code for a in p.advisories]
    assert p.effective_field_slugs == ["multimodal"]


def test_one_finished_course_of_several_is_not_enough_to_know_a_field():
    cat = catalog(
        [course(1, 2, fields=["nlp"]), course(2, 2, fields=["nlp"]), course(3, 2, fields=["nlp"]),
         course(4, 3, fields=["multimodal"])],
        [(stage("mm", 4), "multimodal")],
    )
    p = plan(cat, level="advanced", fields=["multimodal"], state=UserState(completed_course_ids=frozenset({1})))
    assert ADVISORY_PREREQUISITE_ROUTE_ADDED in [a.code for a in p.advisories]


def test_an_inactive_prerequisite_field_is_not_counted_or_added():
    fields = {k: v for k, v in FIELDS.items() if k != "computer-vision"}
    p = plan(catalog(fields=fields), level="advanced", fields=["multimodal"])
    added = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITE_ROUTE_ADDED)
    assert "computer-vision" not in added.params["added"]


def test_the_rule_is_data_a_stricter_threshold_needs_two():
    strict = dict(FIELDS)
    strict["multimodal"] = field(
        "multimodal", 4, min_level_rank=3,
        prerequisite_slugs=("nlp", "computer-vision", "speech"),
        prerequisite_min_required=2, prerequisite_recommended=2,
    )
    p = plan(catalog(fields=strict), level="advanced", fields=["nlp", "multimodal"])
    added = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITE_ROUTE_ADDED)
    assert len(added.params["added"]) == 1  # nlp chosen; one more is needed


def test_a_field_prerequisite_cycle_in_bad_data_cannot_hang_generation():
    looped = {
        "nlp": field("nlp", 1, prerequisite_slugs=("speech",)),
        "speech": field("speech", 2, prerequisite_slugs=("nlp",)),
    }
    p = plan(catalog(fields=looped), fields=["nlp"])
    assert set(p.effective_field_slugs) <= {"nlp", "speech"}


# ─── Course prerequisites ───────────────────────────────────────────────────

def test_a_missing_prerequisite_is_pulled_in_just_before_the_course():
    # Course 1 is in no stage at all — that is what "missing" means here.
    cat = catalog([course(1, 2), course(2, 2, prereqs=[1])], [stage("s", 2)])
    p = plan(cat)
    assert [c.course_id for c in p.stages[0].courses] == [1, 2]
    assert p.stages[0].courses[0].reason == "prerequisite"
    assert p.stages[0].courses[1].reason is None


def test_a_transitive_chain_lands_in_dependency_order():
    cat = catalog([course(1, 2), course(2, 2, prereqs=[1]), course(3, 2, prereqs=[2])], [stage("s", 3)])
    assert [c.course_id for c in plan(cat).stages[0].courses] == [1, 2, 3]


def test_a_stage_is_reordered_so_prerequisites_come_first():
    cat = catalog([course(1, 2), course(2, 2, prereqs=[1])], [stage("s", 2, 1)])
    assert [c.course_id for c in plan(cat).stages[0].courses] == [1, 2]


def test_a_finished_or_optional_prerequisite_is_not_pulled_in():
    cat = catalog([course(1, 1), course(2, 3, prereqs=[1])], [stage("s", 2)])
    p = plan(cat, level="advanced")  # 1 is below the level and closes no gap
    assert [c.course_id for c in p.stages[0].courses] == [2]
    p = plan(cat, level="beginner", state=UserState(completed_course_ids=frozenset({1})))
    assert [c.course_id for c in p.stages[0].courses] == [2]


def test_an_unpublished_prerequisite_is_not_offered():
    cat = catalog([course(1, 2, available=False), course(2, 2, prereqs=[1])], [stage("s", 2)])
    assert [c.course_id for c in plan(cat).stages[0].courses] == [2]


def test_a_prerequisite_cycle_never_fails_a_generation():
    cat = catalog([course(1, 2, prereqs=[2]), course(2, 2, prereqs=[1])], [stage("s", 1, 2)])
    p = plan(cat)
    assert ADVISORY_PREREQUISITE_CYCLE in [a.code for a in p.advisories]
    assert [c.course_id for c in p.stages[0].courses] == [1, 2]  # curated order kept


def test_a_prerequisite_curated_into_a_later_stage_is_flagged_not_reshuffled():
    cat = catalog([course(1, 2), course(2, 2, prereqs=[1])], [stage("first", 2), stage("second", 1)])
    p = plan(cat)
    # 1 is already on the path (in the later stage), so it is not pulled again...
    assert [c.course_id for c in p.stages[0].courses] == [2]
    assert [c.course_id for c in p.stages[1].courses] == [1]
    # ...and the mis-ordering is reported for an admin to fix.
    order = next(a for a in p.advisories if a.code == ADVISORY_PREREQUISITE_ORDER)
    assert order.params == {"course_id": 2, "prerequisite_id": 1}


# ─── Templates ──────────────────────────────────────────────────────────────

def test_a_career_goal_without_a_template_gets_a_tagged_fallback():
    cat = catalog(
        [course(1, 2, fields=["nlp"]), course(2, 1, roles=("eng",)), course(3, 2, roles=("other",))],
        tmpl=False,
    )
    p = plan(cat, level="beginner")
    assert ADVISORY_NO_TEMPLATE in [a.code for a in p.advisories]
    assert [c.course_id for c in p.stages[0].courses] == [2, 1]  # by level, then id; course 3 is not theirs
    assert p.template_slug is None


def test_the_default_template_serves_a_goal_with_none_of_its_own():
    cat = catalog([course(1, 2)])
    cat = Catalog(levels=cat.levels, fields=cat.fields, roles=cat.roles, courses=cat.courses,
                  templates={None: template((stage("s", 1), None), role=None)})
    assert [s.slug for s in plan(cat).stages] == ["s"]
