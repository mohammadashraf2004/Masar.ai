"""
app/services/learning/catalog_admin.py

Writing the learning catalogue: levels, fields, career goals, skills, courses,
stages and path templates.

The point of this module is that adding a specialisation is *data*: an admin
(or a seed script) upserts a field, tags courses with it and adds template
stages for it, and the path generator, the API and the frontend pick it up
with no code change. Everything is keyed by slug and idempotent — running the
same upsert twice leaves the same rows — and each upsert is a full statement
of that entity's configuration, relationship lists included.

Validation happens here, once, and both callers get it: the admin API and
`seeds/seed_learning_paths.py` both go through these functions, so a seed can
never write a prerequisite cycle the API would have refused.

Nothing is ever deleted. Retiring something is `is_active = false`: it
disappears from the catalogue and from new paths, while learners' saved paths
and history keep resolving.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence

from sqlalchemy.orm import Session

from app.models.learning import CareerTrack, TrackLevel
from app.models.learning_path import (
    COURSE_KIND_TOOL, COURSE_KIND_TRACK_LEVEL, ROLE_FIELD_RECOMMENDED, ROLE_FIELD_REQUIRED,
    SKILL_ASSUMES, SKILL_KINDS, SKILL_TEACHES,
    CareerRole, CareerRoleField, CareerRoleSkill, Course, CourseField, CoursePrerequisite,
    CourseRole, CourseSkill, LearningField, LearningFieldPrerequisite, LearningLevel,
    PathStage, PathStageCourse, PathTemplate, PathTemplateStage, Skill,
)
from app.models.tool_course import ToolCourse
from app.services.learning.catalog_service import load_catalog_bundle
from app.services.learning.learning_service import LearningValidationError
from app.services.learning.prerequisites import find_cycle


def _by_slug(db: Session, model, slugs: Iterable[str], what: str) -> Dict[str, object]:
    wanted = list(dict.fromkeys(slugs))
    if not wanted:
        return {}
    rows = {r.slug: r for r in db.query(model).filter(model.slug.in_(wanted)).all()}
    missing = [s for s in wanted if s not in rows]
    if missing:
        raise LearningValidationError(f"unknown_{what}", f"Unknown {what.replace('_', ' ')}: {', '.join(missing)}")
    return rows


def _one(db: Session, model, slug: Optional[str], what: str):
    if slug is None:
        return None
    return _by_slug(db, model, [slug], what)[slug]


def _replace(db: Session, collection, items) -> None:
    """Replace an association collection with `items`.

    The old rows are deleted and flushed *before* the new ones are added.
    Assigning a new list in one step lets the unit of work INSERT the new rows
    ahead of the DELETE of the old ones, which trips any unique constraint the
    two sets share - re-saving a template with an overlapping stage list failed
    on `uq_path_template_stage` exactly that way. Two flushes cost nothing here
    and make the result independent of which constraints a table carries.
    """
    collection.clear()
    db.flush()
    collection.extend(items)
    db.flush()


def _get_or_create(db: Session, model, slug: str, **create):
    row = db.query(model).filter(model.slug == slug).first()
    if row is None:
        row = model(slug=slug, **create)
        db.add(row)
        db.flush()
    return row


# ─── Levels ─────────────────────────────────────────────────────────────────

def upsert_level(db: Session, slug: str, *, name: str, rank: int, name_ar: Optional[str] = None,
                 description: Optional[str] = None, description_ar: Optional[str] = None,
                 is_active: bool = True) -> LearningLevel:
    clash = db.query(LearningLevel).filter(LearningLevel.rank == rank, LearningLevel.slug != slug).first()
    if clash:
        raise LearningValidationError("rank_taken", f"Rank {rank} is already used by '{clash.slug}'.")
    level = _get_or_create(db, LearningLevel, slug, name=name, rank=rank)
    level.name, level.name_ar = name, name_ar
    level.description, level.description_ar = description, description_ar
    level.rank, level.is_active = rank, is_active
    db.flush()
    return level


# ─── Skills ─────────────────────────────────────────────────────────────────

def upsert_skill(db: Session, slug: str, *, name: str, name_ar: Optional[str] = None,
                 kind: Optional[str] = None) -> Skill:
    """`kind` is 'skill' or 'tool'. Left out, a new skill is a 'skill' and an
    existing one keeps whatever kind it has - an edit to a name must not quietly
    turn a tool back into a capability."""
    if kind is not None and kind not in SKILL_KINDS:
        raise LearningValidationError("invalid_skill_kind", f"Skill kind must be one of: {', '.join(SKILL_KINDS)}.")
    skill = _get_or_create(db, Skill, slug, name=name)
    skill.name, skill.name_ar = name, name_ar
    if kind is not None:
        skill.kind = kind
    db.flush()
    return skill


# ─── Fields ─────────────────────────────────────────────────────────────────

def set_field_prerequisites(db: Session, field: LearningField, prerequisites: Sequence[str]) -> None:
    if field.slug in prerequisites:
        raise LearningValidationError("field_prerequisite_self", "A field cannot be its own prerequisite.")
    targets = _by_slug(db, LearningField, prerequisites, "field")
    db.query(LearningFieldPrerequisite).filter(LearningFieldPrerequisite.field_id == field.id).delete()
    for slug in dict.fromkeys(prerequisites):
        db.add(LearningFieldPrerequisite(field_id=field.id, prerequisite_field_id=targets[slug].id))
    db.flush()
    _assert_field_graph_acyclic(db)


def _assert_field_graph_acyclic(db: Session) -> None:
    slug_of = {f.id: f.slug for f in db.query(LearningField).all()}
    edges: Dict[str, List[str]] = {}
    for row in db.query(LearningFieldPrerequisite).all():
        edges.setdefault(slug_of[row.field_id], []).append(slug_of[row.prerequisite_field_id])
    cycle = find_cycle(edges)
    if cycle:
        raise LearningValidationError("field_prerequisite_cycle", "Field prerequisites form a cycle: " + " -> ".join(cycle))


def field_has_prerequisites(db: Session, field: LearningField) -> bool:
    return db.query(LearningFieldPrerequisite).filter(LearningFieldPrerequisite.field_id == field.id).first() is not None


def upsert_field(db: Session, slug: str, *, name: str, name_ar: Optional[str] = None,
                 description: Optional[str] = None, description_ar: Optional[str] = None,
                 icon: Optional[str] = None, min_level: Optional[str] = None,
                 prerequisites: Sequence[str] = (), prerequisite_min_required: int = 1,
                 prerequisite_recommended: int = 1, position: int = 0,
                 is_active: bool = True) -> LearningField:
    level = _one(db, LearningLevel, min_level, "level")
    field = _get_or_create(db, LearningField, slug, name=name)
    field.name, field.name_ar = name, name_ar
    field.description, field.description_ar = description, description_ar
    field.icon = icon
    field.min_level_id = level.id if level else None
    field.prerequisite_min_required = prerequisite_min_required
    field.prerequisite_recommended = max(prerequisite_recommended, prerequisite_min_required)
    field.position, field.is_active = position, is_active
    db.flush()
    set_field_prerequisites(db, field, prerequisites)
    return field


# ─── Career goals ───────────────────────────────────────────────────────────

def set_role_relations(db: Session, role: CareerRole, *, required_fields: Optional[Sequence[str]] = None,
                       recommended_fields: Optional[Sequence[str]] = None,
                       required_skills: Optional[Sequence[str]] = None,
                       optional_skills: Optional[Sequence[str]] = None) -> None:
    """Replace whichever relation lists are given; `None` leaves that list as it
    is. Field relations are replaced together — required and recommended are two
    halves of one statement about the goal."""
    if required_fields is not None or recommended_fields is not None:
        required, recommended = list(required_fields or []), list(recommended_fields or [])
        overlap = set(required) & set(recommended)
        if overlap:
            raise LearningValidationError(
                "field_in_both", f"A field cannot be both required and recommended: {', '.join(sorted(overlap))}")
        fields = _by_slug(db, LearningField, [*required, *recommended], "field")
        _replace(db, role.field_links,
                 [CareerRoleField(field_id=fields[s].id, relation=ROLE_FIELD_REQUIRED) for s in dict.fromkeys(required)]
                 + [CareerRoleField(field_id=fields[s].id, relation=ROLE_FIELD_RECOMMENDED) for s in dict.fromkeys(recommended)])
    if required_skills is not None or optional_skills is not None:
        req, opt = list(required_skills or []), list(optional_skills or [])
        skills = _by_slug(db, Skill, [*req, *opt], "skill")
        _replace(db, role.skill_links,
                 [CareerRoleSkill(skill_id=skills[s].id, is_required=True) for s in dict.fromkeys(req)]
                 + [CareerRoleSkill(skill_id=skills[s].id, is_required=False) for s in dict.fromkeys(opt) if s not in req])
    db.flush()


def upsert_career_goal(db: Session, slug: str, *, title: str, title_ar: Optional[str] = None,
                       description: Optional[str] = None, description_ar: Optional[str] = None,
                       icon: Optional[str] = None, recommended_level: Optional[str] = None,
                       position: int = 0, is_active: bool = True, **relations) -> CareerRole:
    level = _one(db, LearningLevel, recommended_level, "level")
    role = _get_or_create(db, CareerRole, slug, title=title)
    role.title, role.title_ar = title, title_ar
    role.description, role.description_ar = description, description_ar
    role.icon = icon
    role.recommended_level_id = level.id if level else None
    role.position, role.is_active = position, is_active
    db.flush()
    set_role_relations(db, role, **relations)
    return role


# ─── Courses ────────────────────────────────────────────────────────────────

def resolve_source(db: Session, source: Dict[str, object]):
    """Find the existing content a catalogue course points at.

    Either `{"kind": "tool_course", "slug": "langchain"}` or
    `{"kind": "track_level", "track_slug": "ai-developer", "level_order": 3}`.
    """
    kind = source.get("kind")
    if kind == COURSE_KIND_TOOL:
        row = db.query(ToolCourse).filter(ToolCourse.slug == source.get("slug")).first()
        if row is None:
            raise LearningValidationError("unknown_source", f"No tool course '{source.get('slug')}'.")
        return kind, row.id
    if kind == COURSE_KIND_TRACK_LEVEL:
        row = (
            db.query(TrackLevel).join(CareerTrack, TrackLevel.track_id == CareerTrack.id)
            .filter(CareerTrack.slug == source.get("track_slug"), TrackLevel.order == source.get("level_order"))
            .first()
        )
        if row is None:
            raise LearningValidationError(
                "unknown_source", f"No level {source.get('level_order')} in track '{source.get('track_slug')}'.")
        return kind, row.id
    raise LearningValidationError("unknown_source", "source.kind must be 'tool_course' or 'track_level'.")


def set_course_relations(db: Session, course: Course, *, fields: Optional[Sequence[str]] = None,
                         roles: Optional[Sequence[str]] = None, teaches: Optional[Sequence[str]] = None,
                         assumes: Optional[Sequence[str]] = None,
                         prerequisites: Optional[Sequence[str]] = None) -> None:
    """Replace whichever relation lists are given; `None` leaves that list as it
    is. That is what lets a seed create every course first and add the
    prerequisites between them in a second pass."""
    if fields is not None:
        rows = _by_slug(db, LearningField, fields, "field")
        _replace(db, course.field_links, [CourseField(field_id=rows[s].id) for s in dict.fromkeys(fields)])
    if roles is not None:
        rows = _by_slug(db, CareerRole, roles, "career_goal")
        _replace(db, course.role_links, [CourseRole(role_id=rows[s].id) for s in dict.fromkeys(roles)])
    if teaches is not None or assumes is not None:
        t, a = list(teaches or []), list(assumes or [])
        rows = _by_slug(db, Skill, [*t, *a], "skill")
        _replace(db, course.skill_links,
                 [CourseSkill(skill_id=rows[s].id, relation=SKILL_TEACHES) for s in dict.fromkeys(t)]
                 + [CourseSkill(skill_id=rows[s].id, relation=SKILL_ASSUMES) for s in dict.fromkeys(a)])
    if prerequisites is not None:
        if course.slug in prerequisites:
            raise LearningValidationError("course_prerequisite_self", "A course cannot be its own prerequisite.")
        rows = _by_slug(db, Course, prerequisites, "course")
        _replace(db, course.prerequisite_links,
                 [CoursePrerequisite(prerequisite_course_id=rows[s].id) for s in dict.fromkeys(prerequisites)])
    db.flush()
    if prerequisites is not None:
        _assert_course_graph_acyclic(db)


def _assert_course_graph_acyclic(db: Session) -> None:
    slug_of = {c.id: c.slug for c in db.query(Course).all()}
    edges: Dict[str, List[str]] = {}
    for row in db.query(CoursePrerequisite).all():
        edges.setdefault(slug_of[row.course_id], []).append(slug_of[row.prerequisite_course_id])
    cycle = find_cycle(edges)
    if cycle:
        raise LearningValidationError("course_prerequisite_cycle", "Course prerequisites form a cycle: " + " -> ".join(cycle))


def upsert_course(db: Session, slug: str, *, source: Dict[str, object], level: str,
                  title: Optional[str] = None, title_ar: Optional[str] = None,
                  description: Optional[str] = None, description_ar: Optional[str] = None,
                  estimated_hours: Optional[float] = None,
                  learning_objectives: Optional[Sequence[str]] = None,
                  learning_objectives_ar: Optional[Sequence[str]] = None,
                  is_active: bool = True, **relations) -> Course:
    lvl = _one(db, LearningLevel, level, "level")
    kind, source_id = resolve_source(db, source)
    course = db.query(Course).filter(Course.slug == slug).first()
    if course is None:
        clash = db.query(Course).filter(
            (Course.tool_course_id if kind == COURSE_KIND_TOOL else Course.track_level_id) == source_id
        ).first()
        if clash:
            raise LearningValidationError(
                "source_already_catalogued", f"That content is already catalogued as '{clash.slug}'.")
        course = Course(
            slug=slug, kind=kind, level_id=lvl.id,
            tool_course_id=source_id if kind == COURSE_KIND_TOOL else None,
            track_level_id=source_id if kind == COURSE_KIND_TRACK_LEVEL else None,
        )
        db.add(course)
        db.flush()
    else:
        current = course.tool_course_id if course.kind == COURSE_KIND_TOOL else course.track_level_id
        if course.kind != kind or current != source_id:
            raise LearningValidationError(
                "source_immutable", "A catalogue course cannot be re-pointed at different content; create a new one.")
    course.level_id = lvl.id
    course.title, course.title_ar = title, title_ar
    course.description, course.description_ar = description, description_ar
    course.estimated_hours = estimated_hours
    course.learning_objectives = list(learning_objectives) if learning_objectives is not None else None
    course.learning_objectives_ar = list(learning_objectives_ar) if learning_objectives_ar is not None else None
    course.is_active = is_active
    db.flush()
    set_course_relations(db, course, **relations)
    return course


# ─── Stages and templates ───────────────────────────────────────────────────

def upsert_stage(db: Session, slug: str, *, title: str, title_ar: Optional[str] = None,
                 description: Optional[str] = None, description_ar: Optional[str] = None,
                 phase: str = "specialization", kind: str = "learning",
                 courses: Sequence[str] = (), is_active: bool = True) -> PathStage:
    if kind not in ("learning", "capstone"):
        raise LearningValidationError("invalid_stage_kind", "kind must be 'learning' or 'capstone'.")
    rows = _by_slug(db, Course, courses, "course")
    stage = _get_or_create(db, PathStage, slug, title=title)
    stage.title, stage.title_ar = title, title_ar
    stage.description, stage.description_ar = description, description_ar
    stage.phase, stage.kind, stage.is_active = phase, kind, is_active
    _replace(db, stage.course_links,
             [PathStageCourse(course_id=rows[s].id, position=i) for i, s in enumerate(dict.fromkeys(courses))])
    return stage


def upsert_template(db: Session, slug: str, *, title: str, stages: Sequence[Dict[str, Optional[str]]],
                    title_ar: Optional[str] = None, description: Optional[str] = None,
                    description_ar: Optional[str] = None, career_goal: Optional[str] = None,
                    is_active: bool = True) -> PathTemplate:
    """`stages` is ordered: each entry is `{"stage": slug, "field": slug | None}`."""
    role = _one(db, CareerRole, career_goal, "career_goal")
    stage_rows = _by_slug(db, PathStage, [s["stage"] for s in stages], "stage")
    field_rows = _by_slug(db, LearningField, [s["field"] for s in stages if s.get("field")], "field")
    if len({s["stage"] for s in stages}) != len(stages):
        raise LearningValidationError("duplicate_stage", "A stage can appear only once in a template.")
    if role is not None:
        taken = db.query(PathTemplate).filter(
            PathTemplate.career_role_id == role.id, PathTemplate.slug != slug).first()
        if taken:
            raise LearningValidationError("template_exists", f"'{taken.slug}' already defines the path for this career goal.")

    template = _get_or_create(db, PathTemplate, slug, title=title)
    template.title, template.title_ar = title, title_ar
    template.description, template.description_ar = description, description_ar
    template.career_role_id = role.id if role else None
    template.is_active = is_active
    _replace(db, template.stage_links, [
        PathTemplateStage(
            stage_id=stage_rows[s["stage"]].id, position=i,
            field_id=field_rows[s["field"]].id if s.get("field") else None,
        )
        for i, s in enumerate(stages)
    ])
    return template


# ─── Catalogue health ───────────────────────────────────────────────────────

def catalog_health(db: Session) -> List[Dict[str, object]]:
    """Configuration problems an admin should fix, as data.

    Nothing here blocks a learner — the generator degrades around every one of
    these — but each is a promise the catalogue is not keeping.
    """
    bundle = load_catalog_bundle(db)
    issues: List[Dict[str, object]] = []

    edges = {c.slug: [bundle.courses[p].slug for p in bundle.catalog.courses[c.id].prerequisite_ids]
             for c in bundle.courses.values()}
    cycle = find_cycle(edges)
    if cycle:
        issues.append({"code": "course_prerequisite_cycle", "subject": cycle})

    for slug, stage in bundle.stages.items():
        if stage.kind == "learning" and not stage.course_links:
            issues.append({"code": "stage_without_courses", "subject": slug})
        elif stage.kind == "learning" and not any(
            bundle.catalog.courses.get(l.course_id) and bundle.catalog.courses[l.course_id].is_available
            for l in stage.course_links
        ):
            issues.append({"code": "stage_without_available_courses", "subject": slug})

    for role_slug in bundle.roles:
        if role_slug not in bundle.catalog.templates:
            issues.append({"code": "career_goal_without_template", "subject": role_slug,
                           "detail": "falls back to the default template" if None in bundle.catalog.templates
                           else "no default template either — a generic list is used"})

    for course in bundle.courses.values():
        info = bundle.catalog.courses[course.id]
        # A course with no fields is fine — FastAPI serving belongs to no single
        # specialisation — but one serving no career goal is unreachable from
        # every path and from goal-based discovery.
        if not info.role_slugs:
            issues.append({"code": "course_without_career_goals", "subject": course.slug})
        if not info.is_available:
            issues.append({"code": "course_without_content", "subject": course.slug})
    return issues
