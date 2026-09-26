"""
app/services/learning/presenters.py

Turns catalogue rows and generated plans into the API's response models.

Everything a screen needs is decided here on the server — a stage's status
(completed / current / upcoming / coming soon / skippable), the current
stage, per-stage and overall percentages, the estimated weeks — so the
client renders a state rather than re-deriving one. That is the point of
keeping path rules in the domain layer: a second client would get the same
answers.
"""
from __future__ import annotations

import math
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from app.core.config import settings
from app.models.learning_path import (
    COURSE_KIND_TOOL, CareerRole, Course, LearningField, LearningLevel, LearningPath, Skill,
)
from app.services.learning.catalog_service import CatalogBundle, course_href
from app.services.learning.domain import (
    COUNTED_STATES, EMPTY_STATE, STATE_COMPLETED, STATE_REQUIRED, STATE_WAIVED, PathPlan, PlannedStage,
)
from app.services.learning.path_generator import generate_plan
from app.services.learning.progress_service import overview, pct, resolve_state, stage_progress
from app.services.learning.skill_gaps import (
    GROUP_FIELD, STATUS_KNOWN, STATUS_MISSING, STATUS_PARTIAL, SkillGap, calculate_skill_gaps, explain_courses,
)
from app.views.learning_path import (
    AdvisoryOut, CareerGoalOut, CourseDetail, CourseRef, CourseSummary, CourseWhyOut, FieldOut, FieldRef,
    LearnerSkillOut, LevelOut, LevelRef, MySkillsOut, PathCourseOut, PathOut, PathStageOut,
    PathSummaryOut, ProfileOut, ProgressOut, RoadmapStep, RoleRef, SkillGapGroupOut, SkillGapItemOut,
    SkillGapsOut, SkillGapSummaryOut, SkillOptionOut, SkillOut, StageRef,
)


# ─── Vocabulary ─────────────────────────────────────────────────────────────

def level_ref(level: LearningLevel) -> LevelRef:
    return LevelRef(slug=level.slug, name=level.name, name_ar=level.name_ar, rank=level.rank)


def level_out(level: LearningLevel) -> LevelOut:
    return LevelOut(
        slug=level.slug, name=level.name, name_ar=level.name_ar, rank=level.rank,
        description=level.description, description_ar=level.description_ar,
    )


def field_ref(field: LearningField) -> FieldRef:
    return FieldRef(slug=field.slug, name=field.name, name_ar=field.name_ar, icon=field.icon)


def role_ref(role: CareerRole) -> RoleRef:
    return RoleRef(slug=role.slug, title=role.title, title_ar=role.title_ar, icon=role.icon)


def skill_out(skill: Skill) -> SkillOut:
    return SkillOut(slug=skill.slug, name=skill.name, name_ar=skill.name_ar, kind=skill.kind or "skill")


def _counts(bundle: CatalogBundle, tag_of) -> Dict[str, List[int]]:
    """slug -> [course_count, available_course_count]."""
    out: Dict[str, List[int]] = {}
    for course in bundle.catalog.courses.values():
        for slug in tag_of(course):
            row = out.setdefault(slug, [0, 0])
            row[0] += 1
            row[1] += 1 if course.is_available else 0
    return out


def fields_out(bundle: CatalogBundle) -> List[FieldOut]:
    counts = _counts(bundle, lambda c: c.field_slugs)
    top_rank = max((lv.rank for lv in bundle.levels.values()), default=0)
    by_id = {f.id: f for f in bundle.fields.values()}
    result = []
    for field in bundle.fields.values():
        info = bundle.catalog.fields[field.slug]
        c = counts.get(field.slug, [0, 0])
        result.append(FieldOut(
            slug=field.slug, name=field.name, name_ar=field.name_ar, icon=field.icon,
            description=field.description, description_ar=field.description_ar,
            position=field.position,
            min_level=level_ref(field.min_level) if field.min_level and field.min_level.slug in bundle.levels else None,
            is_advanced=bool(info.min_level_rank is not None and info.min_level_rank >= top_rank > 0),
            prerequisites=[field_ref(bundle.fields[s]) for s in info.prerequisite_slugs if s in bundle.fields],
            prerequisite_min_required=field.prerequisite_min_required,
            prerequisite_recommended=field.prerequisite_recommended,
            course_count=c[0], available_course_count=c[1],
        ))
    return result


def career_goals_out(bundle: CatalogBundle) -> List[CareerGoalOut]:
    counts = _counts(bundle, lambda c: c.role_slugs)
    result = []
    for role in bundle.roles.values():
        info = bundle.catalog.roles[role.slug]
        c = counts.get(role.slug, [0, 0])
        result.append(CareerGoalOut(
            slug=role.slug, title=role.title, title_ar=role.title_ar, icon=role.icon,
            description=role.description, description_ar=role.description_ar,
            position=role.position,
            recommended_level=(level_ref(role.recommended_level)
                               if role.recommended_level and role.recommended_level.slug in bundle.levels else None),
            required_fields=[field_ref(bundle.fields[s]) for s in info.required_field_slugs],
            recommended_fields=[field_ref(bundle.fields[s]) for s in info.recommended_field_slugs],
            required_skills=[skill_out(bundle.skills[s]) for s in sorted(info.required_skill_slugs) if s in bundle.skills],
            course_count=c[0], available_course_count=c[1],
        ))
    return result


# ─── Courses ────────────────────────────────────────────────────────────────

def _source_text(course: Course):
    src = course.tool_course if course.kind == COURSE_KIND_TOOL else course.track_level
    if src is None:
        return None, None, None, None
    return src.title, src.title_ar, src.description, src.description_ar


def course_summary(bundle: CatalogBundle, course: Course, *, role_slug: Optional[str] = None) -> CourseSummary:
    """`role_slug` puts the course in the context of one career goal, which is
    what fills `track_role`; without it the field stays null."""
    info = bundle.catalog.courses[course.id]
    s_title, s_title_ar, s_desc, s_desc_ar = _source_text(course)
    return CourseSummary(
        id=course.id, slug=course.slug,
        title=course.title or s_title or course.slug,
        title_ar=course.title_ar or s_title_ar,
        description=course.description or s_desc,
        description_ar=course.description_ar or s_desc_ar,
        kind=course.kind, href=course_href(course),
        level=level_ref(course.level),
        fields=[field_ref(bundle.fields[s]) for s in sorted(info.field_slugs, key=lambda s: bundle.fields[s].position)],
        roles=[role_ref(bundle.roles[s]) for s in sorted(info.role_slugs, key=lambda s: bundle.roles[s].position)],
        skills=[skill_out(bundle.skills[s]) for s in sorted(info.teaches) if s in bundle.skills],
        estimated_hours=info.estimated_hours,
        module_count=info.module_count, lesson_count=info.lesson_count,
        is_available=info.is_available,
        is_free=course.is_free,
        track_role=info.relation_for(role_slug) if role_slug else None,
    )


def course_detail(bundle: CatalogBundle, course: Course) -> CourseDetail:
    info = bundle.catalog.courses[course.id]
    base = course_summary(bundle, course).model_dump()
    prereqs = [bundle.courses[p] for p in sorted(info.prerequisite_ids) if p in bundle.courses]
    ref = lambda c: CourseRef(  # noqa: E731
        id=c.id, slug=c.slug,
        title=c.title or _source_text(c)[0] or c.slug, title_ar=c.title_ar or _source_text(c)[1],
    )
    return CourseDetail(
        **base,
        assumes=[skill_out(bundle.skills[s]) for s in sorted(info.assumes) if s in bundle.skills],
        prerequisites=[ref(c) for c in prereqs],
        learning_objectives=list(course.learning_objectives or []),
        learning_objectives_ar=list(course.learning_objectives_ar or []),
    )


# ─── Paths ──────────────────────────────────────────────────────────────────

def _stage_status(stage: PlannedStage, states: Sequence[str], is_first_open: bool) -> str:
    if not stage.courses:
        return "coming_soon"
    counted = [s for s in states if s in COUNTED_STATES]
    if not counted:
        return "skippable"
    if all(s == STATE_COMPLETED for s in counted):
        return "completed"
    return "current" if is_first_open else "upcoming"


def present_plan(
    bundle: CatalogBundle,
    plan: PathPlan,
    *,
    completion: Optional[Dict[int, float]] = None,
    saved: Optional[LearningPath] = None,
    known_skill_slugs: Iterable[str] = (),
) -> PathOut:
    """`completion` is None for an anonymous preview: no states are promoted
    and no progress is reported. With it, a course the learner has finished
    reads as completed wherever the saved snapshot still says required.
    `known_skill_slugs` is what the learner declared; it only decides which
    skills a course lists as "you already know this" - never a state."""
    live = completion is not None
    completion = completion or {}
    declared = frozenset(known_skill_slugs)
    # "Why is this course here?" for every course, from the same plan, declared
    # skills and progress the states below are computed from.
    whys = explain_courses(bundle.catalog, plan, declared=declared, completion=completion if live else None)
    role_out = role_ref(bundle.roles[plan.role_slug])

    stages_out: List[PathStageOut] = []
    current: Optional[str] = None
    seen_open = False
    path_courses: Dict[int, str] = {}
    remaining_hours = 0.0
    # Every required course still to do, in path order, with the stage it is in.
    open_steps: List[Tuple[PlannedStage, PathCourseOut]] = []

    for stage in plan.stages:
        row = bundle.stages.get(stage.slug)
        resolved = []
        for planned in stage.courses:
            state = resolve_state(planned.state, completion.get(planned.course_id, 0.0)) if live else planned.state
            resolved.append((planned, state))
            path_courses.setdefault(planned.course_id, state)
            if state == STATE_REQUIRED:
                remaining_hours += bundle.catalog.courses[planned.course_id].estimated_hours

        states = [s for _, s in resolved]
        is_first_open = False
        if not seen_open and stage.courses and any(s == STATE_REQUIRED for s in states):
            is_first_open = True
            seen_open = True
        status = _stage_status(stage, states, is_first_open)
        if status == "current":
            current = stage.slug

        def course_out(p, s) -> PathCourseOut:
            info = bundle.catalog.courses[p.course_id]
            return PathCourseOut(
                course=course_summary(bundle, bundle.courses[p.course_id], role_slug=plan.role_slug),
                state=s, reason=p.reason,
                completion_pct=pct(completion.get(p.course_id, 0.0)) if live else None,
                known_skills=[skill_out(bundle.skills[k]) for k in sorted(info.teaches & declared)
                              if k in bundle.skills] if s in ("waived", "required") else [],
                why=_why_out(bundle, whys.get(p.course_id), role_out),
            )

        stage_courses = [course_out(p, s) for p, s in resolved]
        for out in stage_courses:
            if out.state == STATE_REQUIRED:
                open_steps.append((stage, out))

        stages_out.append(PathStageOut(
            slug=stage.slug, position=stage.position,
            title=row.title if row else stage.slug, title_ar=row.title_ar if row else None,
            description=row.description if row else None, description_ar=row.description_ar if row else None,
            phase=stage.phase, kind=stage.kind, status=status,
            progress_pct=stage_progress([(p.course_id, s) for p, s in resolved], completion) if live else None,
            upcoming_count=stage.upcoming_count,
            courses=stage_courses,
        ))

    progress = None
    if live:
        counted = [(cid, st) for cid, st in path_courses.items()]
        summary = overview(bundle.catalog, completion, path_course_ids=[c for c, s in counted if s in COUNTED_STATES])
        progress = ProgressOut(
            path_pct=stage_progress(counted, completion),
            path_completed=sum(1 for _, st in counted if st == STATE_COMPLETED),
            path_total=sum(1 for _, st in counted if st in COUNTED_STATES),
            path_known=sum(1 for _, st in counted if st == STATE_WAIVED),
            **summary,
        )

    current_step = next_step = None
    if live and open_steps:
        # Where to pick up: a course already under way if there is one, else the
        # first still to do; "next" is the one after it in path order.
        at = next((i for i, (_, c) in enumerate(open_steps) if (c.completion_pct or 0) > 0), 0)
        current_step = _step(bundle, *open_steps[at])
        rest = open_steps[at + 1:]
        next_step = _step(bundle, *rest[0]) if rest else None

    hours = round(remaining_hours, 1) if live else plan.estimated_hours
    level = bundle.levels[plan.level_slug]
    role = bundle.roles[plan.role_slug]
    return PathOut(
        id=saved.id if saved else None,
        is_saved=saved is not None,
        status=saved.status if saved else "preview",
        level=level_ref(level),
        career_goal=role_ref(role),
        fields=[field_ref(bundle.fields[s]) for s in plan.field_slugs if s in bundle.fields],
        effective_fields=[field_ref(bundle.fields[s]) for s in plan.effective_field_slugs if s in bundle.fields],
        template_slug=plan.template_slug,
        stages=stages_out,
        current_stage_slug=current,
        current_course=current_step,
        next_course=next_step,
        is_complete=bool(live and not open_steps and progress and (progress.path_total or 0) > 0),
        advisories=[AdvisoryOut(code=a.code, severity=a.severity, params=a.params) for a in plan.advisories],
        estimated_hours=hours,
        estimated_weeks=math.ceil(hours / settings.LEARNING_HOURS_PER_WEEK) if hours > 0 else 0,
        progress=progress,
        generated_at=saved.generated_at if saved else None,
    )


def _stage_ref(bundle: CatalogBundle, slug: Optional[str]) -> Optional[StageRef]:
    if slug is None:
        return None
    row = bundle.stages.get(slug)
    return StageRef(slug=slug, title=row.title if row else slug, title_ar=row.title_ar if row else None)


def _skills(bundle: CatalogBundle, slugs: Iterable[str]) -> List[SkillOut]:
    return [skill_out(bundle.skills[s]) for s in slugs if s in bundle.skills]


def _why_out(bundle: CatalogBundle, why, role: RoleRef) -> Optional[CourseWhyOut]:
    if why is None:
        return None
    return CourseWhyOut(
        career_goal=role,
        fields=[field_ref(bundle.fields[f]) for f in why.route_fields if f in bundle.fields],
        stage=_stage_ref(bundle, why.stage_slug),
        reasons=list(why.reasons),
        skills_taught=_skills(bundle, why.taught),
        known_skills=_skills(bundle, why.known),
        skills_to_gain=_skills(bundle, why.to_gain),
        goal_skills=_skills(bundle, why.goal_skills),
        prerequisite_for=[
            CourseRef(id=c.id, slug=c.slug, title=c.title or _source_text(c)[0] or c.slug,
                      title_ar=c.title_ar or _source_text(c)[1])
            for c in (bundle.courses[i] for i in why.prerequisite_for if i in bundle.courses)
        ],
        taught_count=len(why.taught), known_count=len(why.known), to_gain_count=len(why.to_gain),
    )


def _step(bundle: CatalogBundle, stage: PlannedStage, course: PathCourseOut) -> RoadmapStep:
    row = bundle.stages.get(stage.slug)
    return RoadmapStep(
        **course.model_dump(),
        stage_slug=stage.slug,
        stage_title=row.title if row else stage.slug,
        stage_title_ar=row.title_ar if row else None,
    )


# ─── Skill gaps ─────────────────────────────────────────────────────────────

def _gap_item(bundle: CatalogBundle, g: SkillGap) -> SkillGapItemOut:
    skill = bundle.skills[g.slug]
    return SkillGapItemOut(
        slug=skill.slug, name=skill.name, name_ar=skill.name_ar, kind=skill.kind or "skill",
        status=g.status,
        group=field_ref(bundle.fields[g.group_field]) if g.group_field in bundle.fields else None,
        stage=_stage_ref(bundle, g.stage_slug),
        is_goal_required=g.is_goal_required, is_immediate=g.is_immediate,
        course_count=g.course_count, covered_by_completed=g.covered_by_completed,
    )


def skill_gaps_out(
    bundle: CatalogBundle, plan: PathPlan, *, declared: Iterable[str], completion: Dict[int, float],
) -> SkillGapsOut:
    """The gap report for a saved roadmap, shaped for the API. The domain decides
    every status and every group; this only attaches names."""
    report = calculate_skill_gaps(bundle.catalog, plan, declared=frozenset(declared), completion=completion)
    items = {g.slug: _gap_item(bundle, g) for g in report.skills if g.slug in bundle.skills}
    by_status = lambda status: [items[g.slug] for g in report.skills if g.status == status and g.slug in items]  # noqa: E731
    known, partial, missing = by_status(STATUS_KNOWN), by_status(STATUS_PARTIAL), by_status(STATUS_MISSING)
    groups = []
    for group in report.groups:
        members = [g for g in group.skills if g.slug in items]
        if not members:
            continue
        in_field = group.kind == GROUP_FIELD and group.field_slug in bundle.fields
        groups.append(SkillGapGroupOut(
            key=group.key, kind=group.kind,
            field=field_ref(bundle.fields[group.field_slug]) if in_field else None,
            total=len(members), known_count=sum(1 for g in members if g.status == STATUS_KNOWN),
            skills=[items[g.slug] for g in members if g.status == STATUS_PARTIAL]
            + [items[g.slug] for g in members if g.status == STATUS_MISSING],
        ))
    return SkillGapsOut(
        available=True,
        level=level_ref(bundle.levels[plan.level_slug]),
        career_goal=role_ref(bundle.roles[plan.role_slug]),
        fields=[field_ref(bundle.fields[s]) for s in plan.effective_field_slugs if s in bundle.fields],
        current_stage=_stage_ref(bundle, report.current_stage_slug),
        summary=SkillGapSummaryOut(
            required=len(items), known=len(known), partial=len(partial), missing=len(missing),
            immediate=sum(1 for i in items.values() if i.is_immediate),
            coverage_pct=round(100.0 * len(known) / len(items), 1) if items else None,
        ),
        known=known, partial=partial, missing=missing, groups=groups,
    )


# ─── Skills the learner can declare ─────────────────────────────────────────

def skill_options(
    bundle: CatalogBundle, *, level_slug: str, role_slug: str, field_slugs: Sequence[str],
) -> List[SkillOptionOut]:
    """The skills worth asking about for this goal, route and level.

    Derived, not listed: generate the route for an empty learner and take what
    its courses teach, plus what the goal itself requires. Nothing is named here
    - a skill appears because a course in the route teaches it, and it is filed
    under the field most of those courses belong to.
    """
    plan = generate_plan(
        bundle.catalog, level_slug=level_slug, role_slug=role_slug,
        field_slugs=field_slugs, state=EMPTY_STATE,
    )
    role = bundle.catalog.roles[role_slug]
    taught: Dict[str, int] = {}
    by_field: Dict[str, Dict[str, int]] = {}
    for stage in plan.stages:
        for planned in stage.courses:
            info = bundle.catalog.courses[planned.course_id]
            for slug in info.teaches:
                taught[slug] = taught.get(slug, 0) + 1
                for f in info.field_slugs:
                    by_field.setdefault(slug, {}).setdefault(f, 0)
                    by_field[slug][f] += 1
    slugs = {s for s in set(taught) | set(role.required_skill_slugs) if s in bundle.skills}

    def group_of(slug: str) -> Optional[str]:
        tally = by_field.get(slug)
        if not tally:
            return None
        return max(tally, key=lambda f: (tally[f], -bundle.fields[f].position, f))

    options = []
    for slug in slugs:
        skill = bundle.skills[slug]
        group = group_of(slug) if skill.kind != "tool" else None
        options.append((skill, group))
    options.sort(key=lambda o: (
        o[0].kind == "tool",
        o[1] is None, bundle.fields[o[1]].position if o[1] else 0,
        o[0].name.lower(),
    ))
    return [
        SkillOptionOut(
            slug=s.slug, name=s.name, name_ar=s.name_ar, kind=s.kind or "skill",
            group=field_ref(bundle.fields[g]) if g else None,
            is_required=s.slug in role.required_skill_slugs,
            course_count=taught.get(s.slug, 0),
        )
        for s, g in options
    ]


def my_skills_out(bundle: CatalogBundle, overview) -> MySkillsOut:
    return MySkillsOut(
        known=[LearnerSkillOut(skill=skill_out(bundle.skills[slug]), status=status, source=source)
               for slug, status, source in overview.known if slug in bundle.skills],
        learning=[skill_out(bundle.skills[s]) for s in overview.learning if s in bundle.skills],
    )


# ─── Predefined paths ───────────────────────────────────────────────────────

def parse_path_slug(bundle: CatalogBundle, slug: str):
    """`ai-engineer-computer-vision` -> ("ai-engineer", "computer-vision").

    Role and field slugs both contain hyphens, so the split cannot be a
    separator — instead the *known* career-goal slugs are tried, longest
    first, and whatever follows must be a known field. Returns None when the
    slug names nothing the catalogue has."""
    for role_slug in sorted(bundle.roles, key=len, reverse=True):
        if slug == role_slug:
            return role_slug, None
        if slug.startswith(role_slug + "-"):
            field_slug = slug[len(role_slug) + 1:]
            if field_slug in bundle.fields:
                return role_slug, field_slug
    return None


def default_level_slug(bundle: CatalogBundle, role_slug: str) -> Optional[str]:
    role = bundle.roles[role_slug]
    if role.recommended_level and role.recommended_level.slug in bundle.levels:
        return role.recommended_level.slug
    return next(iter(bundle.levels), None)  # ordered by rank


def path_summaries(bundle: CatalogBundle) -> List[PathSummaryOut]:
    """One summary per career goal (its shared core) and per (career goal, field)
    route the configuration defines.

    Derived, not stored: each is the goal's template filtered to one field and
    generated for an empty learner at the goal's recommended level — so a new
    template stage or field shows up here with no other change."""
    summaries: List[PathSummaryOut] = []
    for role in bundle.roles.values():
        level_slug = default_level_slug(bundle, role.slug)
        if level_slug is None:
            continue
        template = bundle.catalog.templates.get(role.slug) or bundle.catalog.templates.get(None)
        fields_in_template: List[str] = []
        if template:
            for entry in template.stages:
                if entry.field_slug and entry.field_slug not in fields_in_template:
                    fields_in_template.append(entry.field_slug)
        # The shared core first, then one route per field the template knows.
        for field_slug in [None, *fields_in_template]:
            plan = generate_plan(
                bundle.catalog, level_slug=level_slug, role_slug=role.slug,
                field_slugs=[field_slug] if field_slug else [], state=EMPTY_STATE,
            )
            listed = sum(len(s.courses) for s in plan.stages)
            summaries.append(PathSummaryOut(
                slug=f"{role.slug}-{field_slug}" if field_slug else role.slug,
                career_goal=role_ref(role),
                field=field_ref(bundle.fields[field_slug]) if field_slug else None,
                recommended_level=level_ref(bundle.levels[level_slug]),
                stage_count=len(plan.stages),
                course_count=listed + sum(s.upcoming_count for s in plan.stages),
                available_course_count=listed,
                estimated_hours=plan.estimated_hours,
            ))
    return summaries


# ─── Profile ────────────────────────────────────────────────────────────────

def profile_out(
    bundle: CatalogBundle, profile, *, has_active_path: bool, known_skills: Sequence[str] = (),
) -> ProfileOut:
    """A learner with no profile row yet gets the same shape, empty — the
    client never has to special-case "404 means new"."""
    if profile is None:
        return ProfileOut(onboarding_completed=False, needs_onboarding=True,
                          source="none", has_active_path=has_active_path,
                          known_skills=[skill_out(bundle.skills[s]) for s in known_skills if s in bundle.skills])
    level = next((l for l in bundle.levels.values() if l.id == profile.level_id), None)
    role = next((r for r in bundle.roles.values() if r.id == profile.career_role_id), None)
    completed = profile.onboarding_completed_at is not None
    return ProfileOut(
        level=level_ref(level) if level else None,
        career_goal=role_ref(role) if role else None,
        fields=[field_ref(bundle.fields[s]) for s in (profile.field_slugs or []) if s in bundle.fields],
        known_skills=[skill_out(bundle.skills[s]) for s in known_skills if s in bundle.skills],
        programming_experience=profile.programming_experience, ai_experience=profile.ai_experience,
        onboarding_completed=completed,
        needs_onboarding=not completed,
        source=profile.source,
        has_active_path=has_active_path,
    )
