"""
app/services/curriculum/importer.py

Writes a validated `CourseSpec` into the catalogue.

Where a curriculum course lives
-------------------------------
A course folder becomes one **`ToolCourse`** (the existing standalone course
entity - "a user can enroll in any tool course independently of any track") and
one catalogue **`Course`** facade over it. It is deliberately *not* a level of a
career track: the course is its own entity, and the many-to-many relation to
career goals lives in `course_roles` / the path stages, never in the course's
storage. Inside the course:

    module  -> ToolTopic          lesson   -> Lesson
    lesson's exercises -> Exercise (on the module's topic)
    lesson's quiz      -> Quiz     (on the module's topic)
    module / lesson / capstone projects -> Project

so the course viewer, progress endpoints, quiz grading, project submission and
paywall that already exist all work on it unchanged.

Safe to run repeatedly
----------------------
Every row is keyed by a `source_key` ('COURSE-004/L004-001'). A re-import
updates the row in place - ids never change, and learners' progress refers to
lesson and exercise ids - creates what is missing, and never deletes: a row
whose source no longer exists is reported as *stale* and left alone. Nothing
about a learner is read or written.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from sqlalchemy import null
from sqlalchemy.orm import Session

from app.models.course_asset import CourseAsset
from app.models.learning import DifficultyLevel, Exercise, Lesson, Project, Quiz, Topic
from app.models.learning_path import COURSE_KIND_TOOL, Course
from app.models.tool_course import CURRICULUM_CATEGORY, ToolCourse, ToolTopic
from app.services.content.quiz_balance import rebalance_quiz
from app.services.curriculum import normalize as N
from app.services.curriculum.spec import CourseSpec, ExerciseSpec, LessonSpec, ModuleSpec, ProjectSpec
from app.services.learning import catalog_admin as admin

# Marker an earlier layout put on the empty, synthetic track level that stood in
# for a course before its lessons were imported. See `_adopt_synthetic_source`.
_SYNTHETIC_MARKER = "curriculum-source:"


def _difficulty(value: str) -> DifficultyLevel:
    return DifficultyLevel(value if value in ("beginner", "intermediate", "advanced") else "intermediate")


def _hours(minutes: Optional[int]) -> Optional[float]:
    return round(minutes / 60.0, 2) if minutes else None


@dataclass
class Tally:
    """created / updated / unchanged counts for one kind of row."""
    created: int = 0
    updated: int = 0
    unchanged: int = 0

    def add(self, outcome: str) -> None:
        setattr(self, outcome, getattr(self, outcome) + 1)

    def __str__(self) -> str:
        return f"+{self.created} ~{self.updated} ={self.unchanged}"


@dataclass
class CourseReport:
    course_id: str
    modules: Tally = field(default_factory=Tally)
    lessons: Tally = field(default_factory=Tally)
    exercises: Tally = field(default_factory=Tally)
    quizzes: Tally = field(default_factory=Tally)
    projects: Tally = field(default_factory=Tally)
    assets: Tally = field(default_factory=Tally)
    stale: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        tallies = (self.modules, self.lessons, self.exercises, self.quizzes, self.projects, self.assets)
        return any(t.created or t.updated for t in tallies)


def _assign(row: Any, values: Mapping[str, Any]) -> bool:
    """Set only the attributes that differ; True if anything changed."""
    changed = False
    for name, value in values.items():
        if getattr(row, name) != value:
            setattr(row, name, value)
            changed = True
    return changed


def _upsert(db: Session, model: Any, existing: Dict[str, Any], key: str, values: Mapping[str, Any],
            tally: Tally) -> Any:
    row = existing.get(key)
    if row is None:
        # A value the folder does not state is stored as NULL. Left as None, the ORM would
        # let a column's Python-side default (15 minutes, 8 hours) fill it in - a number
        # nobody wrote, which the next run would then "correct" back to NULL.
        row = model(source_key=key, **{k: (null() if v is None else v) for k, v in values.items()})
        db.add(row)
        existing[key] = row
        tally.add("created")
    elif _assign(row, values):
        tally.add("updated")
    else:
        tally.add("unchanged")
    return row


# ─── Text placement ─────────────────────────────────────────────────────────

def _text_fields(text: Optional[str], en: str, ar: str, *, required: bool) -> Dict[str, Any]:
    """Put `text` in the column of the language it is written in, and leave the
    other empty so the reader's language switch falls back correctly (an Arabic
    body with an empty English twin renders as Arabic, right-to-left, with the
    "not available in your language" note - see `pickText`). `required` columns
    are NOT NULL, so their empty side is '' rather than NULL."""
    empty: Any = "" if required else None
    if not text:
        return {en: empty, ar: None}
    return {en: empty, ar: text} if N.is_arabic(text) else {en: text, ar: None}


def _title_fields(title: str, given_ar: Optional[str] = None) -> Dict[str, Any]:
    """`title` is NOT NULL, so an Arabic title stays in it as well as in `title_ar`."""
    return {"title": title, "title_ar": given_ar or (title if N.is_arabic(title) else None)}


# ─── Course records ─────────────────────────────────────────────────────────

def ensure_tool_course(db: Session, definition: Mapping[str, Any], spec: Optional[CourseSpec] = None) -> ToolCourse:
    """The `ToolCourse` for one registry entry: created empty (a shell) when its
    lessons are not imported yet, updated with the real title and hours when they are."""
    slug = str(definition["slug"])
    row = db.query(ToolCourse).filter(ToolCourse.slug == slug).first()
    values: Dict[str, Any] = {
        "title": str(definition["title"]),
        "description": definition.get("capability"),
        "category": CURRICULUM_CATEGORY,
        "difficulty": _difficulty(str(definition["level"])),
        "is_active": True,
    }
    if spec is not None:
        values["title_ar"] = spec.title_ar
        values["estimated_hours"] = _hours(spec.estimated_minutes)
    if row is None:
        row = ToolCourse(slug=slug, related_track_ids=[], technical_terms=[], industry_skills=[], **values)
        db.add(row)
        db.flush()
    else:
        _assign(row, values)
        db.flush()
    return row


def _adopt_synthetic_source(db: Session, course: Course, tool_course: ToolCourse) -> bool:
    """Move a catalogue course that an earlier layout pointed at an empty,
    synthetic track level onto its tool course, then remove that placeholder level.

    Only ever a level that carries the placeholder marker and has no topics - a
    stand-in with no content and no learner activity - so nothing real is touched.
    Returns True when a course was moved."""
    if course.kind == COURSE_KIND_TOOL:
        return False
    level = course.track_level
    is_placeholder = (
        level is not None and (level.description or "").startswith(_SYNTHETIC_MARKER)
        and db.query(Topic.id).filter(Topic.level_id == level.id).first() is None
    )
    if not is_placeholder:
        raise admin.LearningValidationError(
            "curriculum_source_mismatch",
            f"'{course.slug}' points at real track content and cannot be moved automatically.",
        )
    course.kind, course.tool_course_id, course.track_level_id = COURSE_KIND_TOOL, tool_course.id, None
    db.flush()
    db.delete(level)
    db.flush()
    return True


def ensure_course_record(db: Session, definition: Mapping[str, Any], spec: Optional[CourseSpec] = None) -> Course:
    """The catalogue `Course` for one registry entry, over its `ToolCourse`.
    Metadata (level, fields, roles, skills) comes from the registry."""
    tool_course = ensure_tool_course(db, definition, spec)
    slug = str(definition["slug"])
    existing = db.query(Course).filter(Course.slug == slug).first()
    if existing is not None:
        _adopt_synthetic_source(db, existing, tool_course)
    objective = [str(definition["capability"])]
    return admin.upsert_course(
        db, slug, source={"kind": COURSE_KIND_TOOL, "slug": slug},
        level=str(definition["level"]), title=str(definition["title"]),
        description=str(definition["capability"]), fields=list(definition["fields"]),
        roles=[{"slug": g, "relation": r} for g, r in definition["roles"].items()],
        teaches=list(definition["skills"]), learning_objectives=objective,
    )


# ─── Content ────────────────────────────────────────────────────────────────

def _exercise_values(spec: ExerciseSpec, topic_id: int) -> Dict[str, Any]:
    return {
        "tool_topic_id": topic_id,
        **_title_fields(spec.title),
        **_text_fields(spec.description, "description", "description_ar", required=True),
        "starter_code": spec.starter_code, "solution_code": spec.solution_code,
        "difficulty": _difficulty(spec.difficulty), "skill_tested": spec.skill_tested,
    }


def _project_values(spec: ProjectSpec, topic_id: int) -> Dict[str, Any]:
    return {
        "tool_topic_id": topic_id,
        **_title_fields(spec.title),
        **_text_fields(spec.description, "description", "description_ar", required=True),
        "difficulty": _difficulty(spec.difficulty), "tech_stack": spec.tech_stack,
        "objectives": spec.objectives, "rubric": spec.rubric, "starter_repo_url": spec.starter_repo_url,
        "estimated_hours": spec.estimated_hours,
    }


def _quiz_values(lesson: LessonSpec, topic_id: int) -> Dict[str, Any]:
    title = f"Check: {lesson.title}"
    # Several courses author the correct option first in every question, which lets a
    # learner score without knowing anything. Reorder the options the way the rest of the
    # catalogue already is (text untouched, key remapped, deterministic).
    questions, _changed = rebalance_quiz(title, [q.as_json() for q in lesson.questions])
    arabic = any(N.is_arabic(q.question) for q in lesson.questions)
    return {
        "tool_topic_id": topic_id,
        "title": title, "title_ar": f"اختبر نفسك: {lesson.title}" if arabic else None,
        # `questions` is what grading reads; `questions_ar` is the display twin and, for an
        # Arabic-first quiz, the same list (indices must line up 1:1).
        "questions": questions, "questions_ar": questions if arabic else None,
        "passing_score": 70,
    }


def _module_tags(module: ModuleSpec) -> List[str]:
    tags: List[str] = []
    for lesson in module.lessons:
        for tag in lesson.skill_tags:
            if tag not in tags:
                tags.append(tag)
    return tags[:12]


def import_content(db: Session, spec: CourseSpec, tool_course: ToolCourse) -> CourseReport:
    """Create or update every module, lesson, exercise, quiz and project of `spec`."""
    report = CourseReport(spec.course_id)
    prefix = f"{spec.course_id}/"

    topics = {t.source_key: t for t in db.query(ToolTopic).filter(ToolTopic.source_key.like(prefix + "%")).all()}
    topic_ids = [t.id for t in topics.values()]

    def keyed(model: Any, column: Any) -> Dict[str, Any]:
        if not topic_ids:
            return {}
        return {r.source_key: r for r in db.query(model).filter(column.in_(topic_ids), model.source_key.isnot(None)).all()}

    lessons = keyed(Lesson, Lesson.tool_topic_id)
    exercises = keyed(Exercise, Exercise.tool_topic_id)
    quizzes = keyed(Quiz, Quiz.tool_topic_id)
    projects = keyed(Project, Project.tool_topic_id)
    produced: set = set()

    def mark(*keys: str) -> None:
        produced.update(keys)

    last_module = spec.modules[-1] if spec.modules else None
    for module in spec.modules:
        key = f"{spec.course_id}/{module.module_id}"
        mark(key)
        topic = topics.get(key)
        values = {
            "tool_course_id": tool_course.id,
            **_title_fields(module.title, module.title_ar),
            "slug": f"{spec.slug}-{module.module_id.lower()}",
            **_text_fields(module.description, "description", "description_ar", required=False),
            "order": module.order,
            "difficulty": _difficulty(module.lessons[0].difficulty if module.lessons else "intermediate"),
            "estimated_hours": _hours(module.estimated_minutes),
            "skill_tags": _module_tags(module), "technical_terms": [], "prerequisite_ids": [],
        }
        topic = _upsert(db, ToolTopic, topics, key, values, report.modules)
        db.flush()  # the children below need the topic's id

        for lesson in module.lessons:
            lkey = f"{spec.course_id}/{lesson.lesson_id}"
            mark(lkey)
            _upsert(db, Lesson, lessons, lkey, {
                "tool_topic_id": topic.id, **_title_fields(lesson.title),
                **_text_fields(lesson.content, "content", "content_ar", required=True),
                "order": lesson.order, "estimated_minutes": lesson.estimated_minutes,
                "has_code_examples": lesson.has_code_examples,
            }, report.lessons)
            for index, exercise in enumerate(lesson.exercises, start=1):
                ekey = f"{lkey}/x{index}"
                mark(ekey)
                _upsert(db, Exercise, exercises, ekey, _exercise_values(exercise, topic.id), report.exercises)
            if lesson.questions:
                qkey = f"{lkey}/quiz"
                mark(qkey)
                _upsert(db, Quiz, quizzes, qkey, _quiz_values(lesson, topic.id), report.quizzes)
            if lesson.project:
                pkey = f"{lkey}/project"
                mark(pkey)
                _upsert(db, Project, projects, pkey, _project_values(lesson.project, topic.id), report.projects)

        for suffix, project in (("project", module.project), ("lab", module.lab)):
            if project:
                pkey = f"{key}/{suffix}"
                mark(pkey)
                _upsert(db, Project, projects, pkey, _project_values(project, topic.id), report.projects)
        if spec.capstone and module is last_module:
            pkey = f"{spec.course_id}/capstone"
            mark(pkey)
            _upsert(db, Project, projects, pkey, _project_values(spec.capstone, topic.id), report.projects)
        db.flush()

    for store in (topics, lessons, exercises, quizzes, projects):
        report.stale += sorted(k for k in store if k not in produced)

    if not spec.has_lesson_bodies:
        report.notes.append(f"{len(spec.modules)} modules imported, {spec.outline_lesson_count} outline lessons not "
                            "imported: the folder has no lesson text, so the course stays non-startable")
    return report


def import_assets(db: Session, spec: CourseSpec, tool_course: ToolCourse, report: CourseReport) -> None:
    """Create or update the course's figures, keyed by (course, asset key). A figure
    the folder no longer lists is reported as stale and kept: a lesson written
    earlier may still place it."""
    existing = {a.key: a for a in db.query(CourseAsset).filter(CourseAsset.tool_course_id == tool_course.id).all()}
    for asset in spec.assets:
        values = {
            "tool_course_id": tool_course.id, "asset_type": "image", "storage_key": asset.storage_key,
            "mime_type": asset.mime_type, "byte_size": asset.byte_size, "width": asset.width, "height": asset.height,
            "sha256": asset.sha256, "alt": asset.alt, "caption": asset.caption,
            "figure_number": asset.figure_number, "source_reference": asset.source_reference,
        }
        row = existing.get(asset.key)
        if row is None:
            db.add(CourseAsset(key=asset.key, **values))
            report.assets.add("created")
        elif _assign(row, values):
            report.assets.add("updated")
        else:
            report.assets.add("unchanged")
    report.stale += sorted(f"{spec.course_id}/asset/{k}" for k in existing if k not in {a.key for a in spec.assets})
    db.flush()


def import_course(db: Session, spec: CourseSpec, definition: Mapping[str, Any]) -> CourseReport:
    """Course record + content for one folder. Does not commit."""
    course = ensure_course_record(db, definition, spec)
    tool_course = course.tool_course
    report = import_content(db, spec, tool_course)
    import_assets(db, spec, tool_course, report)
    return report
