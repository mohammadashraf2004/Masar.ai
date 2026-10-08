"""
app/services/learning/catalog_service.py

Reads the learning catalogue out of the database.

`load_catalog_bundle` is the one place ORM rows become the immutable `Catalog`
snapshot the path generator reasons over. It returns the rows as well,
because the API layer needs display text (both languages) that the domain
deliberately does not carry.

Two facts about "available" are computed here, and only here:

  * a course is **available** when it is active *and* its source has at least
    one lesson. Most tool courses and four of the five career tracks are
    seeded as shells (see seed_tool_courses.py, tracks_all.py); offering one
    as startable would land the learner on an empty page.
  * a course's **hours** are its own override, else the source's declared
    hours, else the sum of its topics — so the estimate is never zero merely
    because nobody typed a number.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.learning import Lesson, Topic, TrackLevel
from app.models.learning_path import (
    COURSE_KIND_TOOL, COURSE_KIND_TRACK_LEVEL, PREREQ_RECOMMENDED, PREREQ_REQUIRED,
    ROLE_FIELD_RECOMMENDED, ROLE_FIELD_REQUIRED,
    SKILL_ASSUMES, SKILL_KIND_TOOL, SKILL_TEACHES,
    CareerRole, Course, LearningField, LearningFieldPrerequisite, LearningLevel,
    PathStage, PathTemplate, PathTemplateStage, Skill,
)
from app.models.tool_course import CURRICULUM_CATEGORY, ToolTopic
from app.services.learning.domain import (
    Catalog, CourseInfo, CourseRoleWorkflow, FieldInfo, LevelInfo, RoleInfo, StageInfo, TemplateInfo,
    TemplateStageInfo,
)


@dataclass
class CatalogBundle:
    """The domain snapshot plus the ORM rows it was built from."""

    catalog: Catalog
    levels: Dict[str, LearningLevel] = field(default_factory=dict)
    fields: Dict[str, LearningField] = field(default_factory=dict)
    roles: Dict[str, CareerRole] = field(default_factory=dict)
    courses: Dict[int, Course] = field(default_factory=dict)
    stages: Dict[str, PathStage] = field(default_factory=dict)
    templates: Dict[str, PathTemplate] = field(default_factory=dict)
    skills: Dict[str, Skill] = field(default_factory=dict)

    def course_by_slug(self, slug: str) -> Optional[Course]:
        return next((c for c in self.courses.values() if c.slug == slug), None)


def course_href(course: Course) -> Optional[str]:
    """Where the underlying content lives in the app. The catalogue owns no
    pages of its own for lessons — it points at the ones that exist."""
    if course.kind == COURSE_KIND_TOOL and course.tool_course is not None:
        # A curriculum course is a course in its own right, not a "tool": it opens in
        # the course viewer under /courses, never on the Tools pages.
        if course.tool_course.category == CURRICULUM_CATEGORY:
            return f"/courses/{course.slug}/learn"
        return f"/tools/{course.tool_course.slug}"
    if course.kind == COURSE_KIND_TRACK_LEVEL and course.track_level is not None:
        track = course.track_level.track
        return f"/tracks/{track.slug}" if track is not None else None
    return None


def _content_and_hours(db: Session):
    """Lesson counts and summed topic hours per content source, in four
    grouped queries rather than one per course."""
    tool_lessons = dict(
        db.query(ToolTopic.tool_course_id, func.count(Lesson.id))
        .join(Lesson, Lesson.tool_topic_id == ToolTopic.id)
        .group_by(ToolTopic.tool_course_id).all()
    )
    level_lessons = dict(
        db.query(Topic.level_id, func.count(Lesson.id))
        .join(Lesson, Lesson.topic_id == Topic.id)
        .group_by(Topic.level_id).all()
    )
    tool_hours = dict(
        db.query(ToolTopic.tool_course_id, func.coalesce(func.sum(ToolTopic.estimated_hours), 0.0))
        .group_by(ToolTopic.tool_course_id).all()
    )
    level_hours = dict(
        db.query(Topic.level_id, func.coalesce(func.sum(Topic.estimated_hours), 0.0))
        .group_by(Topic.level_id).all()
    )
    tool_modules = dict(
        db.query(ToolTopic.tool_course_id, func.count(ToolTopic.id)).group_by(ToolTopic.tool_course_id).all()
    )
    level_modules = dict(db.query(Topic.level_id, func.count(Topic.id)).group_by(Topic.level_id).all())
    return tool_lessons, level_lessons, tool_hours, level_hours, tool_modules, level_modules


def load_catalog_bundle(db: Session) -> CatalogBundle:
    levels = {
        lv.slug: lv for lv in
        db.query(LearningLevel).filter(LearningLevel.is_active.is_(True)).order_by(LearningLevel.rank).all()
    }
    fields = {
        f.slug: f for f in
        db.query(LearningField).filter(LearningField.is_active.is_(True))
        .order_by(LearningField.position, LearningField.id).all()
    }
    skills = {s.slug: s for s in db.query(Skill).order_by(Skill.slug).all()}
    skill_slug = {s.id: s.slug for s in skills.values()}
    field_slug = {f.id: f.slug for f in fields.values()}

    prereq_rows = db.query(LearningFieldPrerequisite).all()
    field_prereqs: Dict[int, List[str]] = {}
    for row in prereq_rows:
        if row.prerequisite_field_id in field_slug:
            field_prereqs.setdefault(row.field_id, []).append(field_slug[row.prerequisite_field_id])

    level_rank_by_id = {lv.id: lv.rank for lv in levels.values()}

    roles = {
        r.slug: r for r in
        db.query(CareerRole)
        .options(selectinload(CareerRole.field_links), selectinload(CareerRole.skill_links))
        .filter(CareerRole.is_active.is_(True)).order_by(CareerRole.position, CareerRole.id).all()
    }

    course_rows = (
        db.query(Course)
        .options(
            joinedload(Course.level),
            joinedload(Course.tool_course),
            joinedload(Course.track_level).joinedload(TrackLevel.track),
            selectinload(Course.field_links),
            selectinload(Course.role_links),
            selectinload(Course.skill_links),
            selectinload(Course.prerequisite_links),
        )
        .filter(Course.is_active.is_(True))
        .order_by(Course.id).all()
    )
    role_slug = {r.id: r.slug for r in roles.values()}

    tool_lessons, level_lessons, tool_hours, level_hours, tool_modules, level_modules = _content_and_hours(db)

    courses: Dict[int, CourseInfo] = {}
    for c in course_rows:
        if c.kind == COURSE_KIND_TOOL:
            lessons = tool_lessons.get(c.tool_course_id, 0)
            modules = tool_modules.get(c.tool_course_id, 0)
            source_hours = (c.tool_course.estimated_hours if c.tool_course else None) or tool_hours.get(c.tool_course_id, 0.0)
        else:
            lessons = level_lessons.get(c.track_level_id, 0)
            modules = level_modules.get(c.track_level_id, 0)
            source_hours = level_hours.get(c.track_level_id, 0.0)
        hours = c.estimated_hours if c.estimated_hours is not None else source_hours
        courses[c.id] = CourseInfo(
            id=c.id,
            slug=c.slug,
            level_rank=c.level.rank if c.level else 0,
            field_slugs=frozenset(field_slug[l.field_id] for l in c.field_links if l.field_id in field_slug),
            role_slugs=frozenset(role_slug[l.role_id] for l in c.role_links if l.role_id in role_slug),
            role_relations=tuple(sorted(
                (role_slug[l.role_id], l.relation) for l in c.role_links if l.role_id in role_slug
            )),
            role_workflow=tuple(sorted(
                (
                    CourseRoleWorkflow(
                        role_slug=role_slug[l.role_id], relation=l.relation,
                        position=l.position, required=l.required, section=l.section,
                    )
                    for l in c.role_links if l.role_id in role_slug
                ),
                key=lambda w: w.role_slug,
            )),
            teaches=frozenset(skill_slug[l.skill_id] for l in c.skill_links
                              if l.relation == SKILL_TEACHES and l.skill_id in skill_slug),
            assumes=frozenset(skill_slug[l.skill_id] for l in c.skill_links
                              if l.relation == SKILL_ASSUMES and l.skill_id in skill_slug),
            prerequisite_ids=frozenset(p.prerequisite_course_id for p in c.prerequisite_links
                                       if p.kind == PREREQ_REQUIRED),
            recommended_prerequisite_ids=frozenset(p.prerequisite_course_id for p in c.prerequisite_links
                                                   if p.kind == PREREQ_RECOMMENDED),
            estimated_hours=round(float(hours or 0.0), 1),
            module_count=modules, lesson_count=lessons,
            is_available=lessons > 0,
            is_active=True,
        )
    # A prerequisite that points at a course that is no longer active would
    # dangle; drop the reference rather than chase it.
    for cid, info in list(courses.items()):
        live = frozenset(p for p in info.prerequisite_ids if p in courses)
        live_recommended = frozenset(p for p in info.recommended_prerequisite_ids if p in courses)
        if live != info.prerequisite_ids or live_recommended != info.recommended_prerequisite_ids:
            courses[cid] = replace(info, prerequisite_ids=live, recommended_prerequisite_ids=live_recommended)

    stage_rows = (
        db.query(PathStage).options(selectinload(PathStage.course_links))
        .filter(PathStage.is_active.is_(True)).order_by(PathStage.id).all()
    )
    stages = {s.slug: s for s in stage_rows}
    stage_info = {
        s.slug: StageInfo(
            slug=s.slug, phase=s.phase, kind=s.kind,
            course_ids=tuple(l.course_id for l in sorted(s.course_links, key=lambda l: (l.position, l.course_id))),
        )
        for s in stage_rows
    }

    template_rows = (
        db.query(PathTemplate)
        # Eager-load the stage row too, so the loop below never lazy-loads.
        .options(selectinload(PathTemplate.stage_links).joinedload(PathTemplateStage.stage))
        .filter(PathTemplate.is_active.is_(True)).all()
    )
    role_by_id = {r.id: r.slug for r in roles.values()}
    templates_info: Dict[Optional[str], TemplateInfo] = {}
    templates: Dict[str, PathTemplate] = {}
    for t in template_rows:
        entries = []
        for link in sorted(t.stage_links, key=lambda l: (l.position, l.id)):
            info = stage_info.get(link.stage.slug)
            if info is None:
                continue  # inactive stage
            fslug = field_slug.get(link.field_id) if link.field_id is not None else None
            if link.field_id is not None and fslug is None:
                continue  # the field it is tied to is inactive
            entries.append(TemplateStageInfo(stage=info, field_slug=fslug))
        owner = role_by_id.get(t.career_role_id) if t.career_role_id is not None else None
        if t.career_role_id is not None and owner is None:
            continue  # template for an inactive career goal
        templates_info[owner] = TemplateInfo(slug=t.slug, role_slug=owner, stages=tuple(entries))
        templates[t.slug] = t

    role_infos: Dict[str, RoleInfo] = {}
    for r in roles.values():
        role_infos[r.slug] = RoleInfo(
            id=r.id,
            slug=r.slug,
            recommended_level_rank=level_rank_by_id.get(r.recommended_level_id),
            required_field_slugs=tuple(
                field_slug[l.field_id] for l in r.field_links
                if l.relation == ROLE_FIELD_REQUIRED and l.field_id in field_slug
            ),
            recommended_field_slugs=tuple(
                field_slug[l.field_id] for l in r.field_links
                if l.relation == ROLE_FIELD_RECOMMENDED and l.field_id in field_slug
            ),
            required_skill_slugs=frozenset(
                skill_slug[l.skill_id] for l in r.skill_links if l.is_required and l.skill_id in skill_slug
            ),
        )

    catalog = Catalog(
        levels={lv.slug: LevelInfo(lv.id, lv.slug, lv.rank) for lv in levels.values()},
        fields={
            f.slug: FieldInfo(
                id=f.id, slug=f.slug, position=f.position,
                min_level_rank=level_rank_by_id.get(f.min_level_id),
                prerequisite_slugs=tuple(field_prereqs.get(f.id, ())),
                prerequisite_min_required=f.prerequisite_min_required,
                prerequisite_recommended=f.prerequisite_recommended,
            )
            for f in fields.values()
        },
        roles=role_infos,
        courses=courses,
        templates=templates_info,
        tools=frozenset(s.slug for s in skills.values() if s.kind == SKILL_KIND_TOOL),
    )
    return CatalogBundle(
        catalog=catalog, levels=levels, fields=fields, roles=roles,
        courses={c.id: c for c in course_rows}, stages=stages, templates=templates, skills=skills,
    )
