"""
app/services/learning/skill_gaps.py

Skill-gap analysis and "why is this course here?" — pure, like the generator.

    declared skills + level + fields + career goal  ->  a roadmap   (path_generator)
    that roadmap + declared skills + progress       ->  skill gaps  (this module)
                                                    ->  why each course is on it

No database, no clock, no randomness, and no second catalogue: everything here is
read from the `Catalog` snapshot and the `PathPlan` the generator already
produced, so the same inputs always give the same answer and a gap can never
disagree with the roadmap it is shown beside.

Which skills are *relevant*
---------------------------
A skill is relevant to a learner when either

  * a course on their roadmap teaches it — a course that is `required`,
    `completed` or `waived`; or
  * their career goal lists it as required (even when no published course
    teaches it yet: that is reported, not hidden, and never invented).

Courses that are `optional` — below the learner's level and not needed to close
a gap — contribute nothing. That is the whole of level-awareness: an advanced
learner's roadmap has fewer required courses, so they have fewer gaps, and no
second progression system exists to drift from the first. The one exception is a
field the generator added to the route *as a prerequisite* (Multimodal's modality
route): what that field teaches is what the learner is missing to get where they
asked to go, so it counts even when the courses are below their level. Tools are ordinary
skills here exactly as they are in the "Already know" rule: a course that teaches
LangChain counts LangChain among the skills it teaches.

What a status means
-------------------
`known`             the learner *declared* it. Nothing else makes a skill known:
                    not finishing a course, not knowing a related skill, not
                    knowing a prerequisite.
`partially_covered` not declared, but a course on the roadmap that teaches it is
                    under way and unfinished. Skills are atomic in the
                    catalogue, so this is the honest meaning of "partly":
                    started, not known.
`missing`           everything else. A skill taught only by a course the learner
                    *finished* is still `missing` — completion and declaration are
                    separate facts — and says so (`covered_by_completed`).

"Immediate" means a required course in the roadmap's current stage teaches it.
Everything else that is missing is later on the same roadmap.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import AbstractSet, Dict, List, Mapping, Optional, Tuple

from app.services.learning.domain import (
    STATE_COMPLETED, STATE_OPTIONAL, STATE_REQUIRED, STATE_WAIVED, Catalog, PathPlan, PlannedCourse, PlannedStage,
)
from app.services.learning.progress_service import resolve_state

# ── Skill status ─────────────────────────────────────────────────────────────
STATUS_KNOWN = "known"
STATUS_PARTIAL = "partially_covered"
STATUS_MISSING = "missing"

# ── Why a course is on the roadmap ───────────────────────────────────────────
# A course can have several. Codes, not sentences: the wording is interface copy.
REASON_CAREER_REQUIREMENT = "career_requirement"    # teaches a skill the career goal requires
REASON_FIELD_REQUIREMENT = "field_requirement"      # belongs to a field on the learner's route
REASON_STAGE_REQUIREMENT = "stage_requirement"      # it is part of a stage of the goal's path
REASON_SKILL_GAP = "skill_gap"                      # teaches something the learner has not declared
REASON_PREREQUISITE = "prerequisite"                # another course still to do needs it first

# ── How gaps are grouped ─────────────────────────────────────────────────────
GROUP_FIELD = "field"
GROUP_GENERAL = "general"     # taught by no field-specific course (or by none at all)
GROUP_TOOLS = "tools"

_LAST = 10 ** 6   # sorts "unknown" after every real position


@dataclass(frozen=True)
class SkillGap:
    slug: str
    status: str
    is_tool: bool
    # The field most of the roadmap courses teaching it belong to.
    group_field: Optional[str]
    # The earliest roadmap stage that teaches it (None: no course on the roadmap does).
    stage_slug: Optional[str]
    is_goal_required: bool
    # A required course in the current stage teaches it and the learner lacks it.
    is_immediate: bool
    # Roadmap courses that teach it. 0 with a goal-required skill means the
    # catalogue has no published course for it yet.
    course_count: int
    covered_by_completed: bool


@dataclass(frozen=True)
class GapGroup:
    key: str
    kind: str
    field_slug: Optional[str]
    skills: Tuple[SkillGap, ...]


@dataclass(frozen=True)
class SkillGapReport:
    skills: Tuple[SkillGap, ...] = ()
    groups: Tuple[GapGroup, ...] = ()
    current_stage_slug: Optional[str] = None
    required: int = 0
    known: int = 0
    partial: int = 0
    missing: int = 0
    immediate: int = 0

    @property
    def coverage_pct(self) -> Optional[float]:
        """Share of the relevant skills the learner declared. None when nothing
        is relevant (an empty roadmap), which is not the same as 0%."""
        return round(100.0 * self.known / self.required, 1) if self.required else None


@dataclass(frozen=True)
class CourseWhy:
    course_id: int
    stage_slug: str
    reasons: Tuple[str, ...]
    taught: Tuple[str, ...]
    known: Tuple[str, ...]
    to_gain: Tuple[str, ...]
    # Taught skills the career goal lists as required.
    goal_skills: Tuple[str, ...]
    # The fields on the learner's route this course belongs to, in route order.
    route_fields: Tuple[str, ...]
    # Courses still to do on this roadmap that need this one first.
    prerequisite_for: Tuple[int, ...]


# ─── Shared: the roadmap with progress applied ───────────────────────────────

def _resolved(
    plan: PathPlan, completion: Optional[Mapping[int, float]],
) -> List[Tuple[PlannedStage, List[Tuple[PlannedCourse, str, float]]]]:
    """Every planned course with its effective state (progress applied, exactly
    as the roadmap presenter applies it) and its completion fraction."""
    live = completion is not None
    out = []
    for stage in plan.stages:
        rows = []
        for planned in stage.courses:
            fraction = (completion or {}).get(planned.course_id, 0.0)
            state = resolve_state(planned.state, fraction) if live else planned.state
            rows.append((planned, state, fraction))
        out.append((stage, rows))
    return out


def _current_stage(resolved) -> Optional[str]:
    """The first stage with a course still to do — the presenter's rule."""
    for stage, rows in resolved:
        if any(state == STATE_REQUIRED for _, state, _ in rows):
            return stage.slug
    return None


# ─── Skill gaps ──────────────────────────────────────────────────────────────

def calculate_skill_gaps(
    catalog: Catalog,
    plan: PathPlan,
    *,
    declared: AbstractSet[str],
    completion: Optional[Mapping[int, float]] = None,
) -> SkillGapReport:
    role = catalog.roles.get(plan.role_slug)
    goal_required = role.required_skill_slugs if role else frozenset()
    resolved = _resolved(plan, completion)
    current = _current_stage(resolved)
    # Fields on the route that the learner did not ask for: prerequisite routes.
    routed = frozenset(plan.effective_field_slugs) - frozenset(plan.field_slugs)

    # skill -> [(stage position, stage slug, course id, state, fraction)]
    teachers: Dict[str, List[Tuple[int, str, int, str, float]]] = {}
    for stage, rows in resolved:
        for planned, state, fraction in rows:
            course = catalog.courses.get(planned.course_id)
            if course is None:
                continue
            counted = state in (STATE_REQUIRED, STATE_COMPLETED, STATE_WAIVED) or (
                state == STATE_OPTIONAL and bool(course.field_slugs & routed)
            )
            if not counted:
                continue  # an optional course is not this learner's business yet
            for slug in course.teaches:
                teachers.setdefault(slug, []).append((stage.position, stage.slug, course.id, state, fraction))

    scope = set(teachers) | set(goal_required)
    field_position = {slug: info.position for slug, info in catalog.fields.items()}

    gaps: List[SkillGap] = []
    for slug in scope:
        rows = teachers.get(slug, [])
        is_known = slug in declared
        started = any(state == STATE_REQUIRED and 0.0 < fraction < 1.0 for *_, state, fraction in rows)
        status = STATUS_KNOWN if is_known else STATUS_PARTIAL if started else STATUS_MISSING

        # Earliest stage that still asks the learner to do something about it;
        # failing that, the earliest that teaches it at all.
        pending = [r for r in rows if r[3] == STATE_REQUIRED]
        chosen = min(pending or rows, default=None)
        stage_slug = chosen[1] if chosen else None

        tally: Dict[str, int] = {}
        for _, _, cid, _, _ in rows:
            for f in catalog.courses[cid].field_slugs:
                if f in catalog.fields:
                    tally[f] = tally.get(f, 0) + 1
        group_field = min(tally, key=lambda f: (-tally[f], field_position.get(f, _LAST), f)) if tally else None

        gaps.append(SkillGap(
            slug=slug, status=status, is_tool=slug in catalog.tools, group_field=group_field,
            stage_slug=stage_slug, is_goal_required=slug in goal_required,
            is_immediate=(not is_known) and current is not None
            and any(r[1] == current and r[3] == STATE_REQUIRED for r in rows),
            course_count=len({r[2] for r in rows}),
            covered_by_completed=(not is_known) and any(r[3] == STATE_COMPLETED for r in rows),
        ))

    stage_position = {stage.slug: stage.position for stage, _ in resolved}
    gaps.sort(key=lambda g: (stage_position.get(g.stage_slug, _LAST), g.slug))

    buckets: Dict[Tuple[str, Optional[str]], List[SkillGap]] = {}
    for g in gaps:
        if g.is_tool:
            key = (GROUP_TOOLS, None)
        elif g.group_field:
            key = (GROUP_FIELD, g.group_field)
        else:
            key = (GROUP_GENERAL, None)
        buckets.setdefault(key, []).append(g)

    def order(key: Tuple[str, Optional[str]]):
        kind, f = key
        return ({GROUP_FIELD: 0, GROUP_GENERAL: 1, GROUP_TOOLS: 2}[kind], field_position.get(f, _LAST), f or "")

    groups = tuple(
        GapGroup(key=f"{kind}:{f}" if f else kind, kind=kind, field_slug=f, skills=tuple(buckets[(kind, f)]))
        for kind, f in sorted(buckets, key=order)
    )

    count = lambda status: sum(1 for g in gaps if g.status == status)  # noqa: E731
    return SkillGapReport(
        skills=tuple(gaps), groups=groups, current_stage_slug=current,
        required=len(gaps), known=count(STATUS_KNOWN), partial=count(STATUS_PARTIAL),
        missing=count(STATUS_MISSING), immediate=sum(1 for g in gaps if g.is_immediate),
    )


# ─── Why is this course here? ────────────────────────────────────────────────

def explain_courses(
    catalog: Catalog,
    plan: PathPlan,
    *,
    declared: AbstractSet[str],
    completion: Optional[Mapping[int, float]] = None,
) -> Dict[int, CourseWhy]:
    """One `CourseWhy` per course on the roadmap — structured facts, no wording.

    Everything is a relationship the catalogue already holds: what the course
    teaches (`course_skills`), what the goal requires (`career_role_skills`),
    which fields it belongs to (`course_fields`), which stage lists it and which
    courses need it first (`course_prerequisites`). Nothing is hard-coded and
    nothing is inferred beyond `teaches - declared`.
    """
    role = catalog.roles.get(plan.role_slug)
    goal_required = role.required_skill_slugs if role else frozenset()
    resolved = _resolved(plan, completion)

    still_to_do = {planned.course_id for _, rows in resolved for planned, state, _ in rows if state == STATE_REQUIRED}
    needed_by: Dict[int, List[int]] = {}
    for cid in still_to_do:
        course = catalog.courses.get(cid)
        if course is None:
            continue
        for pid in course.prerequisite_ids:
            needed_by.setdefault(pid, []).append(cid)

    out: Dict[int, CourseWhy] = {}
    for stage, rows in resolved:
        for planned, state, _ in rows:
            course = catalog.courses.get(planned.course_id)
            if course is None or planned.course_id in out:
                continue
            taught = tuple(sorted(course.teaches))
            known = tuple(s for s in taught if s in declared)
            to_gain = tuple(s for s in taught if s not in declared)
            goal_skills = tuple(s for s in taught if s in goal_required)
            route_fields = tuple(f for f in plan.effective_field_slugs if f in course.field_slugs)
            dependents = tuple(sorted(needed_by.get(planned.course_id, ())))
            from_prerequisite_rule = planned.reason == "prerequisite"

            reasons: List[str] = []
            if goal_skills:
                reasons.append(REASON_CAREER_REQUIREMENT)
            if route_fields:
                reasons.append(REASON_FIELD_REQUIREMENT)
            if not from_prerequisite_rule:
                reasons.append(REASON_STAGE_REQUIREMENT)
            if state == STATE_REQUIRED and to_gain:
                reasons.append(REASON_SKILL_GAP)
            if from_prerequisite_rule or dependents:
                reasons.append(REASON_PREREQUISITE)

            out[planned.course_id] = CourseWhy(
                course_id=planned.course_id, stage_slug=stage.slug, reasons=tuple(reasons),
                taught=taught, known=known, to_gain=to_gain, goal_skills=goal_skills,
                route_fields=route_fields, prerequisite_for=dependents,
            )
    return out
