"""
app/services/learning/learning_service.py

The learner-facing operations: save a learning profile, generate a path, save
it, read it back.

This module is the seam between the pure domain (`path_generator`,
`prerequisites`, `progress_service`) and the API. It owns the parts that touch
the database and the outside world — validation against the live catalogue,
persistence, logging and metrics — so the domain stays free of all three.

What it logs, and what it does not
----------------------------------
Log lines carry the user's id and catalogue slugs (level, career goal, fields)
— enough to reproduce a generation, none of it personal. Never an email, a
name, or free text. A generation that fails or a catalogue that is
mis-configured is logged at a level someone will see (warning / exception),
and counted in Prometheus with a fixed-vocabulary label.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.metrics import (
    record_learning_catalog_issue,
    record_learning_event,
    record_learning_path_generation,
    record_learning_profile,
    record_learning_roadmap_shape,
)
from app.models.learning_path import (
    LEARNER_SKILL_COURSE_COMPLETION, LEARNER_SKILL_KNOWN, LEARNER_SKILL_MASTERED,
    LEARNER_SKILL_SELF_DECLARED, PATH_ACTIVE, PATH_ARCHIVED, PATH_PAUSED, PROFILE_SOURCE_ONBOARDING,
    LearnerSkill, LearningPath, LearningProfile,
)
from app.models.user import ExperienceLevel, User
from app.services.learning.catalog_service import CatalogBundle, load_catalog_bundle
from app.services.learning.domain import (
    ADVISORY_NO_TEMPLATE, ADVISORY_PREREQUISITE_CYCLE, ADVISORY_PREREQUISITE_ORDER,
    ADVISORY_PREREQUISITE_ROUTE_ADDED, EMPTY_STATE, REASON_KNOWN_SKILLS, STATE_REQUIRED, STATE_WAIVED,
    PathPlan, PlannedCourse, PlannedStage, UserState, Advisory,
)
from app.services.learning.path_generator import PathGenerationError, generate_plan
from app.services.learning.progress_service import completed_course_ids, course_completion
from app.views.learning_path import ProfileUpdate

logger = logging.getLogger(__name__)

_ISSUE_BY_ADVISORY = {
    ADVISORY_PREREQUISITE_CYCLE: "prerequisite_cycle",
    ADVISORY_PREREQUISITE_ORDER: "prerequisite_out_of_order",
    ADVISORY_NO_TEMPLATE: "no_template",
}


class LearningValidationError(ValueError):
    """The request names something the catalogue does not offer."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(detail)


class ProfileIncompleteError(ValueError):
    """A path needs a level, a career goal and at least one field."""


def _event(name: str, user_id: Optional[int], **counts) -> None:
    """A product event: one counter tick plus one structured log line.

    Only the event name is a metric label, and only counts and catalogue slugs
    ever travel in the log fields - never a free-text answer, and never the
    list of skills a learner ticked (how *many* is what analysis needs).
    """
    record_learning_event(name)
    logger.info("learning event", extra={"event": name, "user_id": user_id, **counts})


# ─── Profile ────────────────────────────────────────────────────────────────

def get_profile(db: Session, user_id: int) -> Optional[LearningProfile]:
    return db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()


def profile_is_complete(profile: Optional[LearningProfile]) -> bool:
    return bool(profile and profile.level_id and profile.career_role_id and profile.field_slugs)


def _validated(kind: str, slugs: Iterable[str], known: Dict[str, object]) -> List[str]:
    unique = list(dict.fromkeys(slugs))
    unknown = [s for s in unique if s not in known]
    if unknown:
        raise LearningValidationError(f"unknown_{kind}", f"Unknown {kind.replace('_', ' ')}: {', '.join(unknown)}")
    return unique


def save_profile(db: Session, user: User, update: ProfileUpdate) -> LearningProfile:
    bundle = load_catalog_bundle(db)
    provided = update.model_fields_set
    profile = get_profile(db, user.id)
    created = profile is None
    if created:
        profile = LearningProfile(user_id=user.id, field_slugs=[], known_skill_slugs=[])
        db.add(profile)
    goal_before, fields_before = profile.career_role_id, list(profile.field_slugs or [])
    skills_changed: Optional[Tuple[int, int, int]] = None

    try:
        if "level" in provided:
            if update.level is None:
                profile.level_id = None
            else:
                level = bundle.levels.get(update.level)
                if level is None:
                    raise LearningValidationError("unknown_level", f"Unknown level: {update.level}")
                profile.level_id = level.id
        if "career_goal" in provided:
            if update.career_goal is None:
                profile.career_role_id = None
            else:
                role = bundle.roles.get(update.career_goal)
                if role is None:
                    raise LearningValidationError("unknown_career_goal", f"Unknown career goal: {update.career_goal}")
                profile.career_role_id = role.id
        if "fields" in provided:
            profile.field_slugs = _validated("field", update.fields or [], bundle.fields)
        if "known_skills" in provided:
            skills_changed = set_self_declared_skills(db, user, update.known_skills or [], bundle)
    except LearningValidationError:
        db.rollback()
        record_learning_profile("rejected")
        raise

    # Saving is the learner confirming these answers, so a migrated profile
    # stops being "migrated" the moment they touch it. `migrated_from` is kept:
    # it records what the row started as, and that stays true.
    profile.source = PROFILE_SOURCE_ONBOARDING

    if profile_is_complete(profile):
        profile.onboarding_completed_at = profile.onboarding_completed_at or datetime.now(timezone.utc)
    else:
        # Clearing an answer means onboarding is no longer finished, and the
        # flag the client branches on has to say so.
        profile.onboarding_completed_at = None

    # `users.experience_level` is the same idea as the profile's level and is
    # still read by the mentor and community screens — keep them in step
    # instead of leaving two answers to one question.
    if "level" in provided and update.level is not None:
        try:
            user.experience_level = ExperienceLevel(update.level)
        except ValueError:
            pass  # a level added later that the legacy enum does not know

    db.commit()
    db.refresh(profile)
    record_learning_profile("created" if created else "updated")
    if created:
        _event("learning_onboarding_started", user.id)
    if "career_goal" in provided and profile.career_role_id and profile.career_role_id != goal_before:
        _event("career_goal_selected", user.id)
    if "fields" in provided and profile.field_slugs and list(profile.field_slugs) != fields_before:
        _event("field_selected", user.id, field_count=len(profile.field_slugs))
    if skills_changed is not None:
        added, removed, total = skills_changed
        _event("known_skills_selected", user.id, known_skill_count=total, added=added, removed=removed)
    logger.info(
        "learning profile saved",
        # NB: never name an `extra` key after a LogRecord attribute ("created",
        # "name", "module"...) - logging raises KeyError rather than overwrite it.
        extra={
            "user_id": user.id,
            "profile_created": created,
            "complete": profile_is_complete(profile),
            "field_count": len(profile.field_slugs or []),
        },
    )
    return profile


# ─── Learner skills ─────────────────────────────────────────────────────────

def learner_skill_rows(db: Session, user_id: int) -> List[LearnerSkill]:
    return db.query(LearnerSkill).filter(LearnerSkill.user_id == user_id).order_by(LearnerSkill.id).all()


def known_skill_slugs(db: Session, user_id: int, bundle: CatalogBundle) -> List[str]:
    """Skills the learner counts as knowing when a path is built: `known` and
    `mastered` rows, whatever their source. A skill since retired from the
    catalogue is ignored rather than resurrected."""
    slug_of = {s.id: s.slug for s in bundle.skills.values()}
    return [
        slug_of[r.skill_id] for r in learner_skill_rows(db, user_id)
        if r.status in (LEARNER_SKILL_KNOWN, LEARNER_SKILL_MASTERED) and r.skill_id in slug_of
    ]


def set_self_declared_skills(
    db: Session, user: User, slugs: Iterable[str], bundle: CatalogBundle,
) -> Tuple[int, int, int]:
    """Make the learner's *self-declared* skills exactly `slugs`.

    Returns (added, removed, total_known). Rows that came from better evidence
    (an assessment, a finished course) are never removed by an edit to the
    self-declared list, and a self-declaration never downgrades them. Does not
    commit: the caller decides the unit of work.
    """
    wanted = _validated("skill", slugs, bundle.skills)
    wanted_ids = {bundle.skills[s].id for s in wanted}
    existing = {r.skill_id: r for r in learner_skill_rows(db, user.id)}

    added = removed = 0
    for skill_id in wanted_ids:
        row = existing.get(skill_id)
        if row is None:
            db.add(LearnerSkill(user_id=user.id, skill_id=skill_id,
                                status=LEARNER_SKILL_KNOWN, source=LEARNER_SKILL_SELF_DECLARED))
            added += 1
        elif row.status not in (LEARNER_SKILL_KNOWN, LEARNER_SKILL_MASTERED):
            row.status, row.source = LEARNER_SKILL_KNOWN, LEARNER_SKILL_SELF_DECLARED
            added += 1
    for skill_id, row in existing.items():
        if (skill_id not in wanted_ids and row.source == LEARNER_SKILL_SELF_DECLARED
                and row.status == LEARNER_SKILL_KNOWN):
            db.delete(row)
            removed += 1
    db.flush()
    total = db.query(LearnerSkill).filter(
        LearnerSkill.user_id == user.id,
        LearnerSkill.status.in_((LEARNER_SKILL_KNOWN, LEARNER_SKILL_MASTERED)),
    ).count()
    return added, removed, total


@dataclass
class SkillsOverview:
    """What the learner knows and is learning, for the profile's "My Skills".

    `known` entries carry their source: a stored self-declaration, or a skill
    inferred from a course they finished (derived here, never stored, like every
    other progress figure). `learning` is derived from courses they have started
    and not finished."""
    known: List[Tuple[str, str, str]]     # (skill slug, status, source)
    learning: List[str]


def skills_overview(db: Session, user_id: int, bundle: CatalogBundle) -> SkillsOverview:
    slug_of = {s.id: s.slug for s in bundle.skills.values()}
    known: Dict[str, Tuple[str, str]] = {}
    for row in learner_skill_rows(db, user_id):
        slug = slug_of.get(row.skill_id)
        if slug and row.status in (LEARNER_SKILL_KNOWN, LEARNER_SKILL_MASTERED):
            known[slug] = (row.status, row.source)

    _, completion = build_user_state(db, user_id, bundle)
    done = completed_course_ids(completion)
    learning: Dict[str, None] = {}
    for cid, info in bundle.catalog.courses.items():
        if not info.is_available:
            continue
        if cid in done:
            for slug in info.teaches:
                known.setdefault(slug, (LEARNER_SKILL_KNOWN, LEARNER_SKILL_COURSE_COMPLETION))
        elif completion.get(cid, 0.0) > 0:
            for slug in info.teaches:
                learning.setdefault(slug, None)

    order = {slug: i for i, slug in enumerate(bundle.skills)}
    return SkillsOverview(
        known=[(slug, *known[slug]) for slug in sorted(known, key=lambda s: order.get(s, 0))],
        learning=[s for s in sorted(learning, key=lambda s: order.get(s, 0)) if s not in known],
    )


# ─── Generation ─────────────────────────────────────────────────────────────

@dataclass
class Generated:
    plan: PathPlan
    bundle: CatalogBundle
    completion: Dict[int, float]
    has_user: bool


def build_user_state(
    db: Session, user_id: int, bundle: CatalogBundle,
    *, known_skills: Iterable[str] = (), waived: Iterable[int] = (),
) -> Tuple[UserState, Dict[int, float]]:
    available = [bundle.courses[cid] for cid, info in bundle.catalog.courses.items() if info.is_available]
    completion = course_completion(db, user_id, available)
    state = UserState(
        completed_course_ids=frozenset(completed_course_ids(completion)),
        known_skill_slugs=frozenset(known_skills),
        waived_course_ids=frozenset(waived),
    )
    return state, completion


def generate(
    db: Session,
    *,
    level: str,
    career_goal: str,
    fields: Sequence[str],
    user: Optional[User] = None,
    known_skills: Optional[Iterable[str]] = None,
    waived: Iterable[int] = (),
    bundle: Optional[CatalogBundle] = None,
) -> Generated:
    """`known_skills` left as None means "whatever this learner has declared";
    pass a list to ask a what-if instead."""
    started = time.perf_counter()
    try:
        bundle = bundle or load_catalog_bundle(db)
        if user is not None:
            if known_skills is None:
                known_skills = known_skill_slugs(db, user.id, bundle)
            state, completion = build_user_state(
                db, user.id, bundle, known_skills=known_skills, waived=waived,
            )
        else:
            state, completion = EMPTY_STATE, {}
        plan = generate_plan(
            bundle.catalog, level_slug=level, role_slug=career_goal, field_slugs=fields, state=state,
        )
    except PathGenerationError as exc:
        record_learning_path_generation("rejected", time.perf_counter() - started)
        raise LearningValidationError(exc.code, exc.detail) from exc
    except Exception:
        record_learning_path_generation("error", time.perf_counter() - started)
        logger.exception(
            "learning path generation failed",
            extra={"user_id": user.id if user else None, "level": level,
                   "career_goal": career_goal, "fields": list(fields),
                   "roadmap_generation_success": False},
        )
        raise

    empty = not any(stage.courses for stage in plan.stages)
    record_learning_path_generation("empty" if empty else "ok", time.perf_counter() - started)
    _report_catalog_issues(plan, user_id=user.id if user else None)
    known_count = len(state.known_skill_slugs)
    required_count = sum(1 for st in plan.stages for c in st.courses if c.state == STATE_REQUIRED)
    waived_count = sum(1 for st in plan.stages for c in st.courses
                       if c.state == STATE_WAIVED and c.reason == REASON_KNOWN_SKILLS)
    if user is not None:
        record_learning_roadmap_shape(known_count, waived_count)
    logger.info(
        "learning path generated",
        extra={
            "user_id": user.id if user else None,
            "level": plan.level_slug, "career_goal": plan.role_slug,
            "fields": plan.field_slugs, "effective_fields": plan.effective_field_slugs,
            "stages": len(plan.stages),
            "advisories": [a.code for a in plan.advisories],
            "known_skill_count": known_count,
            "required_course_count": required_count,
            "waived_course_count": waived_count,
            "roadmap_generation_success": True,
        },
    )
    return Generated(plan=plan, bundle=bundle, completion=completion, has_user=user is not None)


def _report_catalog_issues(plan: PathPlan, *, user_id: Optional[int]) -> None:
    """A path generated fine but the *catalogue* has a problem an admin should
    hear about: a prerequisite cycle, a prerequisite curated after the course
    that needs it, a career goal with no template."""
    for advisory in plan.advisories:
        issue = _ISSUE_BY_ADVISORY.get(advisory.code)
        if issue is None:
            continue
        record_learning_catalog_issue(issue)
        logger.warning(
            "learning catalogue issue: %s", issue,
            extra={"user_id": user_id, "career_goal": plan.role_slug, "params": advisory.params},
        )


# ─── Persistence ────────────────────────────────────────────────────────────

def get_active_path(db: Session, user_id: int) -> Optional[LearningPath]:
    return (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user_id, LearningPath.status == PATH_ACTIVE)
        .first()
    )


def get_current_path(db: Session, user_id: int) -> Optional[LearningPath]:
    """The learner's path as they would describe it: the active one, or - if
    they have paused it - the paused one. A pause is not the path vanishing, so
    reads must not treat it as "no path"; only archived paths are history."""
    return (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user_id, LearningPath.status.in_((PATH_ACTIVE, PATH_PAUSED)))
        .order_by(LearningPath.status.asc(), LearningPath.id.desc())  # 'active' sorts before 'paused'
        .first()
    )


def snapshot_stages(plan: PathPlan) -> List[dict]:
    return [
        {
            "slug": stage.slug,
            "position": stage.position,
            "upcoming_count": stage.upcoming_count,
            "courses": [
                {"course_id": c.course_id, "state": c.state, "reason": c.reason}
                for c in stage.courses
            ],
        }
        for stage in plan.stages
    ]


def plan_from_path(path: LearningPath, bundle: CatalogBundle) -> PathPlan:
    """Rebuild a displayable plan from a saved snapshot.

    Only membership and order are stored; stage titles, phases and everything
    a course looks like come from the live catalogue. A course that has since
    been deactivated simply drops out — the saved path never resurrects it.
    """
    level = bundle.levels.get(path.level.slug) if path.level else None
    role = bundle.roles.get(path.career_role.slug) if path.career_role else None
    stages: List[PlannedStage] = []
    for entry in path.stages or []:
        stage_row = bundle.stages.get(entry.get("slug"))
        courses = [
            PlannedCourse(c["course_id"], c["state"], c.get("reason"))
            for c in entry.get("courses", [])
            if c["course_id"] in bundle.catalog.courses
        ]
        stages.append(PlannedStage(
            slug=entry["slug"],
            position=entry.get("position", len(stages) + 1),
            phase=stage_row.phase if stage_row else "specialization",
            kind=stage_row.kind if stage_row else "learning",
            courses=courses,
            upcoming_count=entry.get("upcoming_count", 0),
        ))
    advisories = [Advisory(a["code"], a.get("severity", "info"), a.get("params", {}))
                  for a in (path.advisories or [])]
    return PathPlan(
        level_slug=level.slug if level else path.level.slug,
        role_slug=role.slug if role else path.career_role.slug,
        field_slugs=list(path.field_slugs or []),
        effective_field_slugs=_effective_fields(list(path.field_slugs or []), advisories),
        template_slug=path.template_slug,
        stages=stages,
        advisories=advisories,
        estimated_hours=path.estimated_hours or 0.0,
    )


def _effective_fields(requested: List[str], advisories: List[Advisory]) -> List[str]:
    """The route a saved path was built for: what was asked for plus the
    prerequisite fields the generator added, recovered from the advisories it
    saved (only the requested fields are stored on the row). Applied the same
    way the generator applied them - each added field goes just before the one
    that needed it - so a reload shows the route the learner was given."""
    effective = list(requested)
    for advisory in advisories:
        if advisory.code != ADVISORY_PREREQUISITE_ROUTE_ADDED:
            continue
        needed_by = advisory.params.get("field")
        at = effective.index(needed_by) if needed_by in effective else len(effective)
        for added in advisory.params.get("added", []):
            if added not in effective:
                effective.insert(at, added)
                at += 1
    return effective


def save_path(
    db: Session, user: User, generated: Generated, *, waived: Iterable[int] = (),
) -> LearningPath:
    """Persist a generated plan as the learner's one active path, archiving
    whatever was active before. History is kept, never overwritten."""
    plan, bundle = generated.plan, generated.bundle
    level = bundle.levels[plan.level_slug]
    role = bundle.roles[plan.role_slug]
    replacing = get_current_path(db, user.id) is not None

    # A rebuild replaces whatever the learner had - active or paused - so a
    # paused path cannot linger beside its successor.
    db.query(LearningPath).filter(
        LearningPath.user_id == user.id, LearningPath.status != PATH_ARCHIVED,
    ).update({"status": PATH_ARCHIVED}, synchronize_session=False)

    path = LearningPath(
        user_id=user.id,
        level_id=level.id,
        career_role_id=role.id,
        field_slugs=plan.field_slugs,
        status=PATH_ACTIVE,
        template_slug=plan.template_slug,
        stages=snapshot_stages(plan),
        advisories=[{"code": a.code, "severity": a.severity, "params": a.params} for a in plan.advisories],
        waived_course_ids=sorted(set(waived)),
        estimated_hours=plan.estimated_hours,
    )
    db.add(path)
    try:
        db.commit()
    except IntegrityError:
        # A concurrent request saved an active path between our archive and
        # our insert; the partial unique index refused the second. The outcome
        # the learner wanted — one live path — already holds, so return it.
        db.rollback()
        existing = get_active_path(db, user.id)
        if existing is None:
            raise
        return existing
    db.refresh(path)
    _event("roadmap_updated" if replacing else "roadmap_generated", user.id,
           stages=len(plan.stages), waived_course_count=len(path.waived_course_ids or []))
    return path


def rebuild_path(
    db: Session, user: User, *, waived: Optional[Sequence[int]] = None,
    bundle: Optional[CatalogBundle] = None,
) -> Tuple[LearningPath, Generated]:
    """Build the learner's path afresh from their saved profile and declared
    skills, archiving the previous one.

    Progress is never touched: completion is derived from lessons the learner
    finished, so a rebuilt path reads a finished course as finished wherever it
    now sits. Only membership and state of *future* courses can change.
    `waived=None` keeps the explicit per-course waivers of the current path.
    """
    bundle = bundle or load_catalog_bundle(db)
    profile = get_profile(db, user.id)
    if not profile_is_complete(profile):
        raise ProfileIncompleteError("Choose a level, at least one field and a career goal before building your path.")
    active = get_current_path(db, user.id)
    waived_ids = list(waived) if waived is not None else list(active.waived_course_ids if active else [])
    level = next((l for l in bundle.levels.values() if l.id == profile.level_id), None)
    role = next((r for r in bundle.roles.values() if r.id == profile.career_role_id), None)
    if level is None or role is None:
        # The learner's chosen level or goal has since been deactivated.
        raise ProfileIncompleteError("Your level or career goal is no longer offered. Please choose again.")
    generated = generate(
        db, level=level.slug, career_goal=role.slug, fields=profile.field_slugs or [],
        user=user, waived=waived_ids, bundle=bundle,
    )
    return save_path(db, user, generated, waived=waived_ids), generated
