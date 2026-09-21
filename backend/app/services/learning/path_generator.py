"""
app/services/learning/path_generator.py

Deterministic learning-path generation.

    (level, fields, career goal) + what the learner has done  ->  an ordered plan

This is a pure function over a `Catalog` snapshot: no database, no clock, no
randomness. The same inputs always give the same plan, which is what makes it
testable and what lets a smarter recommender be dropped in later behind the
same signature. The rules are ordinary code on purpose — every one of them
consults *data* (levels' ranks, fields' prerequisite thresholds, the career
goal's required skills, the template's stage list) and none names a specific
field, goal or course.

The rules, in the order they apply
----------------------------------
1. **Fields.** Each requested field is checked against its own configuration.
   Below its `min_level` it draws an advisory; short of its prerequisite
   threshold, the missing prerequisite fields are *added to the route* —
   never refused. A learner asking for Multimodal as a beginner is shown the
   modality route that leads there, not an error.
2. **Stages.** The career goal's template lists stages in order; a stage tied
   to a field appears only when that field is in the route. This is how one
   goal ("AI Engineer") yields an NLP route, a Vision route or a Speech route
   without any of them being hard-coded.
3. **Courses.** A stage lists the courses configured for it. Only *available*
   ones (active, with published content) are offered; the rest are counted as
   upcoming rather than shown as startable.
4. **States.** Finished courses are `completed`. A course is `waived` when the
   learner waived it outright, or when they *declared every skill it teaches*
   (a course that teaches nothing can never be waived by a declaration). A
   course *below* the learner's level is `optional` — an advanced learner is
   not forced through beginner material — unless it teaches a skill the goal
   requires and the learner does not have. Everything else is `required`.
   Waived courses stay in the path, visible, and are never in a denominator.
5. **Prerequisites.** A required course's missing prerequisites are pulled in
   just before it, and each stage is ordered so prerequisites come first. So are
   the missing prerequisites of a course waived by declaration: claiming to
   know "RAG" does not claim its prerequisites, and each is judged on its own
   (waived only if the learner declared it too). A cycle in the graph never
   fails a generation: it is reported as an advisory and the curated order is
   kept.
"""
from __future__ import annotations

from typing import AbstractSet, Dict, List, Optional, Sequence, Set, Tuple

from app.services.learning.domain import (
    ADVISORY_FIELD_ABOVE_LEVEL,
    ADVISORY_NO_AVAILABLE_COURSES,
    ADVISORY_NO_TEMPLATE,
    ADVISORY_PREREQUISITE_CYCLE,
    ADVISORY_PREREQUISITE_ORDER,
    ADVISORY_PREREQUISITE_ROUTE_ADDED,
    ADVISORY_PREREQUISITES_RECOMMENDED,
    EMPTY_STATE,
    REASON_KNOWN_SKILLS,
    STATE_COMPLETED,
    STATE_OPTIONAL,
    STATE_REQUIRED,
    STATE_WAIVED,
    Advisory,
    Catalog,
    CourseInfo,
    LevelInfo,
    PathPlan,
    PlannedCourse,
    PlannedStage,
    RoleInfo,
    UserState,
)
from app.services.learning.prerequisites import (
    PrerequisiteCycleError,
    evaluate_threshold,
    find_cycle,
    topological_order,
    transitive_prerequisites,
)

# A field counts as "known" once the learner has finished this share of the
# available courses in it. High enough that one intro course does not unlock a
# prerequisite, low enough that skipping an optional extra does not block it.
FIELD_KNOWN_RATIO = 0.6

FALLBACK_STAGE_SLUG = "recommended"


class PathGenerationError(ValueError):
    """The request names something the catalogue does not offer."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(detail)


# ─── Field route ────────────────────────────────────────────────────────────

def skill_waived_course_ids(catalog: Catalog, declared: AbstractSet[str]) -> Set[int]:
    """Courses whose every taught skill the learner declared.

    All-of, not any-of: declaring "RAG" must not waive a course that also
    teaches retrieval and embeddings the learner never mentioned. A course that
    teaches no catalogued skill cannot be waived this way at all.
    """
    if not declared:
        return set()
    return {c.id for c in catalog.courses.values() if c.teaches and c.teaches <= declared}


def known_fields(catalog: Catalog, state: UserState, waived: AbstractSet[int] = frozenset()) -> Set[str]:
    """Fields the learner has effectively covered, judged by their courses:
    finished ones, and ones they have said they already know."""
    known: Set[str] = set()
    for slug in catalog.fields:
        available = catalog.available_courses_in_field(slug)
        if not available:
            continue
        done = sum(1 for c in available if c.id in state.completed_course_ids or c.id in waived)
        if done / len(available) >= FIELD_KNOWN_RATIO:
            known.add(slug)
    return known


def _slug_of_rank(catalog: Catalog, rank: Optional[int]) -> Optional[str]:
    if rank is None:
        return None
    return next((lv.slug for lv in catalog.levels.values() if lv.rank == rank), None)


def resolve_field_route(
    catalog: Catalog,
    level: LevelInfo,
    requested: Sequence[str],
    state: UserState,
    waived: AbstractSet[int] = frozenset(),
) -> Tuple[List[str], List[Advisory]]:
    """Requested fields plus whatever prerequisite fields the route needs.

    Never raises for a rule the learner falls short of; a shortfall becomes an
    advisory and, where a threshold is unmet, extra fields on the route.
    """
    advisories: List[Advisory] = []
    effective: List[str] = list(requested)
    have_known = known_fields(catalog, state, waived)

    queue: List[str] = list(requested)
    processed: Set[str] = set()
    while queue:
        slug = queue.pop(0)
        if slug in processed:
            continue
        processed.add(slug)
        field = catalog.fields[slug]

        if field.min_level_rank is not None and level.rank < field.min_level_rank:
            advisories.append(Advisory(
                ADVISORY_FIELD_ABOVE_LEVEL, "info",
                {"field": slug, "level": level.slug,
                 "min_level": _slug_of_rank(catalog, field.min_level_rank)},
            ))

        # Inactive prerequisite fields are absent from the snapshot, so they
        # neither count nor get added.
        prerequisites = [p for p in field.prerequisite_slugs if p in catalog.fields]
        if not prerequisites:
            continue

        have = (set(effective) | have_known) - {slug}
        result = evaluate_threshold(
            prerequisites, have,
            min_required=field.prerequisite_min_required,
            recommended=field.prerequisite_recommended,
        )

        if not result.met:
            # Prefer a prerequisite that has published content, then the
            # configured order — so the suggested route is one the learner
            # can actually start.
            ranked = sorted(
                result.missing,
                key=lambda p: (0 if catalog.available_courses_in_field(p) else 1,
                               catalog.fields[p].position),
            )
            added = [p for p in ranked[:result.shortfall] if p not in effective]
            at = effective.index(slug)
            effective[at:at] = added
            queue.extend(added)
            advisories.append(Advisory(
                ADVISORY_PREREQUISITE_ROUTE_ADDED, "warning", {"field": slug, "added": added},
            ))
            have = (set(effective) | have_known) - {slug}
            result = evaluate_threshold(
                prerequisites, have,
                min_required=field.prerequisite_min_required,
                recommended=field.prerequisite_recommended,
            )

        if not result.recommended_met:
            advisories.append(Advisory(
                ADVISORY_PREREQUISITES_RECOMMENDED, "info",
                {"field": slug, "have": len(result.satisfied),
                 "recommended": min(field.prerequisite_recommended, len(prerequisites)),
                 "suggested": result.missing},
            ))

    return effective, advisories


# ─── Course states ──────────────────────────────────────────────────────────

def _known_skills(catalog: Catalog, state: UserState) -> Set[str]:
    known = set(state.known_skill_slugs)
    for cid in state.completed_course_ids:
        course = catalog.courses.get(cid)
        if course:
            known |= course.teaches
    return known


def classify_course(
    course: CourseInfo,
    level: LevelInfo,
    role: RoleInfo,
    state: UserState,
    known_skills: Set[str],
    skill_waived: AbstractSet[int] = frozenset(),
) -> Tuple[str, Optional[str]]:
    if course.id in state.completed_course_ids:
        return STATE_COMPLETED, None
    if course.id in state.waived_course_ids:
        return STATE_WAIVED, None
    if course.id in skill_waived:
        return STATE_WAIVED, REASON_KNOWN_SKILLS
    if course.level_rank < level.rank:
        # Below the learner's level. Optional — unless it is the only way to
        # close a skill the career goal demands and they have not got.
        gap = role.required_skill_slugs - known_skills
        if not (course.teaches & gap):
            return STATE_OPTIONAL, "below_level"
    return STATE_REQUIRED, None


# ─── Generation ─────────────────────────────────────────────────────────────

def generate_plan(
    catalog: Catalog,
    *,
    level_slug: str,
    role_slug: str,
    field_slugs: Sequence[str],
    state: UserState = EMPTY_STATE,
) -> PathPlan:
    level = catalog.levels.get(level_slug)
    if level is None:
        raise PathGenerationError("unknown_level", f"Unknown level '{level_slug}'.")
    role = catalog.roles.get(role_slug)
    if role is None:
        raise PathGenerationError("unknown_career_goal", f"Unknown career goal '{role_slug}'.")

    requested = list(dict.fromkeys(field_slugs))
    for slug in requested:
        if slug not in catalog.fields:
            raise PathGenerationError("unknown_field", f"Unknown field '{slug}'.")

    # Declared knowledge counts as much as finished courses when deciding
    # which fields the learner has already covered (so a Multimodal route does
    # not send someone back through NLP they told us they know).
    skill_waived = skill_waived_course_ids(catalog, state.known_skill_slugs) - state.completed_course_ids
    effective, advisories = resolve_field_route(
        catalog, level, requested, state, waived=set(state.waived_course_ids) | skill_waived,
    )
    effective_set = set(effective)
    known_skills = _known_skills(catalog, state)

    template = catalog.templates.get(role.slug) or catalog.templates.get(None)
    stages: List[PlannedStage] = []
    seen: Set[int] = set()

    def plan_course(course: CourseInfo, reason: Optional[str] = None) -> PlannedCourse:
        course_state, why = classify_course(course, level, role, state, known_skills, skill_waived)
        return PlannedCourse(course.id, course_state, reason or why)

    if template is None:
        # A career goal with no template of its own and no default is a
        # configuration gap, not a reason to fail: offer what is tagged for it.
        advisories.append(Advisory(ADVISORY_NO_TEMPLATE, "info", {"career_goal": role.slug}))
        matching = sorted(
            (c for c in catalog.courses.values()
             if c.is_available and (role.slug in c.role_slugs or c.field_slugs & effective_set)),
            key=lambda c: (c.level_rank, c.id),
        )
        stage = PlannedStage(FALLBACK_STAGE_SLUG, 1, "specialization", "learning")
        for course in matching:
            seen.add(course.id)
            stage.courses.append(plan_course(course))
        stages.append(stage)
    else:
        position = 0
        for entry in template.stages:
            if entry.field_slug is not None and entry.field_slug not in effective_set:
                continue
            position += 1
            planned = PlannedStage(entry.stage.slug, position, entry.stage.phase, entry.stage.kind)
            for cid in entry.stage.course_ids:
                course = catalog.courses.get(cid)
                if course is None or not course.is_active:
                    continue
                if not course.is_available:
                    planned.upcoming_count += 1
                    continue
                if cid in seen:
                    continue  # one course, one place in a path — never counted twice
                seen.add(cid)
                planned.courses.append(plan_course(course))
            stages.append(planned)

    _apply_prerequisites(catalog, stages, plan_course, advisories)

    estimated = sum(
        catalog.courses[c.course_id].estimated_hours
        for stage in stages for c in stage.courses if c.state == STATE_REQUIRED
    )

    if not any(stage.courses for stage in stages):
        advisories.append(Advisory(
            ADVISORY_NO_AVAILABLE_COURSES, "info", {"fields": effective, "career_goal": role.slug},
        ))

    return PathPlan(
        level_slug=level.slug,
        role_slug=role.slug,
        field_slugs=requested,
        effective_field_slugs=effective,
        template_slug=template.slug if template else None,
        stages=stages,
        advisories=advisories,
        estimated_hours=round(estimated, 1),
    )


# ─── Prerequisites within a plan ────────────────────────────────────────────

def _apply_prerequisites(catalog: Catalog, stages: List[PlannedStage], plan_course, advisories: List[Advisory]) -> None:
    edges: Dict[int, Set[int]] = {c.id: set(c.prerequisite_ids) for c in catalog.courses.values()}
    planned_ids = {c.course_id for s in stages for c in s.courses}
    if not planned_ids:
        return

    # Only the part of the graph this plan can reach matters, and only a cycle
    # in *that* part should stop the plan reordering itself.
    reachable = set(planned_ids)
    for cid in planned_ids:
        reachable.update(transitive_prerequisites(cid, edges))
    cycle = find_cycle({cid: [d for d in edges.get(cid, ()) if d in reachable] for cid in reachable})
    if cycle:
        advisories.append(Advisory(
            ADVISORY_PREREQUISITE_CYCLE, "warning",
            {"course_ids": cycle},
        ))
        return

    # Pull in required prerequisites the route does not already contain,
    # placing each just before the course that needs it.
    for stage in stages:
        idx = 0
        while idx < len(stage.courses):
            planned = stage.courses[idx]
            # A course waived by declaration still needs its prerequisites
            # judged: the learner claimed the course, not what leads to it.
            needs_prerequisites = planned.state == STATE_REQUIRED or (
                planned.state == STATE_WAIVED and planned.reason == REASON_KNOWN_SKILLS
            )
            if not needs_prerequisites:
                idx += 1
                continue
            # Farthest prerequisite first, so a chain lands in dependency order.
            missing = [
                pid for pid in reversed(transitive_prerequisites(planned.course_id, edges))
                if pid not in planned_ids
            ]
            inserted = 0
            for pid in missing:
                course = catalog.courses.get(pid)
                if course is None or not course.is_available or not course.is_active:
                    continue
                pulled = plan_course(course, reason="prerequisite")
                if pulled.state != STATE_REQUIRED:
                    continue  # finished, waived, or optional: nothing to add
                stage.courses.insert(idx + inserted, pulled)
                planned_ids.add(pid)
                inserted += 1
            idx += inserted + 1

    for stage in stages:
        ids = [c.course_id for c in stage.courses]
        try:
            order = topological_order(ids, edges)
        except PrerequisiteCycleError:  # unreachable after the check above; kept as a guard
            continue
        by_id = {c.course_id: c for c in stage.courses}
        stage.courses = [by_id[i] for i in order]

    # Across stages the template's order is authoritative — so a prerequisite
    # that lands in a *later* stage is a curation mistake to surface, not
    # something to silently reshuffle.
    where: Dict[int, Tuple[int, int]] = {}
    for stage in stages:
        for i, c in enumerate(stage.courses):
            where[c.course_id] = (stage.position, i)
    for cid, at in where.items():
        for pid in edges.get(cid, ()):
            if pid in where and where[pid] > at:
                advisories.append(Advisory(
                    ADVISORY_PREREQUISITE_ORDER, "warning",
                    {"course_id": cid, "prerequisite_id": pid},
                ))
