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
    module quiz         -> Quiz     (one on the module's topic)
    module / lesson / capstone projects -> Project

so the course viewer, progress endpoints, quiz grading, project submission and
paywall that already exist all work on it unchanged.

Safe to run repeatedly
----------------------
Every row is keyed by a `source_key` ('COURSE-004/L004-001'). A re-import
updates the row in place - ids never change, and learners' progress refers to
lesson and exercise ids - and creates what is missing.

A row of THIS course whose source no longer exists (a lesson or module the folder
dropped, or a whole earlier layout of the course) is *retired*: deleted, so the
catalogue always matches the folder. Retirement is deliberately narrow:

  * only rows keyed `<COURSE-NNN>/...` of a course being imported, found through
    that course's own topics - never another course, a tool course or a legacy row;
  * only when the folder has lesson text (an outline-only or empty folder retires
    nothing);
  * a row any learner-state table points at (progress, quiz attempts, answers,
    submissions - found from the schema's foreign keys, not a hard-coded list), or
    that a surviving row still depends on, is KEPT and reported as stale instead;
  * it runs in the caller's transaction, so a failure leaves the catalogue as it was.

Nothing about a learner is ever written.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from sqlalchemy import null
from sqlalchemy.orm import Session

from app.db.session import Base

from app.models.course_asset import CourseAsset
from app.models.learning import DifficultyLevel, Exercise, Lesson, Project, Quiz, Topic
from app.models.progress import UserProgress
from app.models.learning_path import COURSE_KIND_TOOL, Course
from app.models.tool_course import CURRICULUM_CATEGORY, ToolCourse, ToolTopic
from app.services.content.quiz_balance import rebalance_quiz
from app.services.curriculum import normalize as N
from app.services.curriculum.spec import CourseSpec, ExerciseSpec, LessonSpec, ModuleSpec, ProjectSpec, QuestionSpec
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
    # Rows no longer in the folder that are still in the catalogue because a learner
    # (or a surviving row) refers to them, as "key (why)".
    stale: List[str] = field(default_factory=list)
    # Rows no longer in the folder that this import deleted, by kind.
    retired: Dict[str, int] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        tallies = (self.modules, self.lessons, self.exercises, self.quizzes, self.projects, self.assets)
        return any(t.created or t.updated for t in tallies) or any(self.retired.values())


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

def _text_fields(text: Optional[str], en: str, ar: str, *, required: bool, given_ar: Optional[str] = None) -> Dict[str, Any]:
    """Put `text` in the column of the language it is written in, and leave the
    other empty so the reader's language switch falls back correctly (an Arabic
    body with an empty English twin renders as Arabic, right-to-left, with the
    "not available in your language" note - see `pickText`). `required` columns
    are NOT NULL, so their empty side is '' rather than NULL.

    `given_ar` is the Arabic twin of an English text, read from the course's `ar/`
    folder. It fills the Arabic column beside the English one."""
    empty: Any = "" if required else None
    if not text:
        return {en: empty, ar: given_ar or None}
    if N.is_arabic(text):
        return {en: empty, ar: text}
    return {en: text, ar: given_ar or None}


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

def _exercise_values(spec: ExerciseSpec, topic_id: int, lesson_id: int) -> Dict[str, Any]:
    return {
        "tool_topic_id": topic_id,
        "lesson_id": lesson_id,
        **_title_fields(spec.title, spec.title_ar),
        **_text_fields(spec.description, "description", "description_ar", required=True, given_ar=spec.description_ar),
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


def _quiz_values(module: ModuleSpec, topic_id: int) -> Dict[str, Any]:
    quiz = module.quiz
    if quiz is None:  # guarded by the caller; keeps this helper total for type checkers
        raise ValueError(f"{module.module_id} has no module quiz")
    title = quiz.title
    # Several courses author the correct option first in every question, which lets a
    # learner score without knowing anything. Reorder the options the way the rest of the
    # catalogue already is (text untouched, key remapped, deterministic).
    questions, _changed = rebalance_quiz(title, [q.as_json() for q in quiz.questions])
    arabic = any(N.is_arabic(q.question) for q in quiz.questions)
    twin = None if arabic else _arabic_twin(quiz.questions, questions)
    title_ar = f"اختبار الوحدة: {module.title}" if arabic else (
        f"اختبار الوحدة: {module.title_ar}" if module.title_ar else None
    )
    return {
        "tool_topic_id": topic_id,
        "title": title, "title_ar": title_ar,
        # `questions` is what grading reads; `questions_ar` is the display twin and, for an
        # Arabic-first quiz, the same list (indices must line up 1:1).
        "questions": questions, "questions_ar": questions if arabic else twin,
        "passing_score": 70,
    }


def _arabic_twin(authored: List[QuestionSpec], served: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    """`questions_ar` for an English quiz whose Arabic lives in the course's `ar/` folder.

    `served` is the English the learner is graded on, after the importer reordered each question's
    options to spread the right answer around; the Arabic options are written in the authored
    order, so each is moved to where its English option went and the key (`correct`, `lesson_id`,
    ids) is copied from the English, never read from the Arabic. A quiz is translated whole or not
    at all: a twin that skipped a question would put a different question at some position than
    the one a learner is graded on."""
    if not authored or any(q.ar is None for q in authored):
        return None
    twin: List[Dict[str, Any]] = []
    for question, english in zip(authored, served):
        arabic = question.ar or {}
        shown = {**english, "question": arabic["question"], "explanation": arabic.get("explanation", "")}
        if not question.is_open:
            options = list(question.options or [])
            used: set = set()
            moved: List[str] = []
            for text in english["options"]:
                at = next((i for i, o in enumerate(options) if o == text and i not in used), None)
                if at is None:
                    return None
                used.add(at)
                moved.append(arabic["options"][at])
            shown["options"] = moved
        twin.append(shown)
    return twin


def _module_tags(module: ModuleSpec) -> List[str]:
    tags: List[str] = []
    for lesson in module.lessons:
        for tag in lesson.skill_tags:
            if tag not in tags:
                tags.append(tag)
    return tags[:12]


# The tables the importer owns. Every other table that points at one of them is
# learner state (or something that must keep resolving) and blocks a deletion.
_OWNED_TABLES = {"tool_topics", "lessons", "exercises", "quizzes", "projects"}


def _learner_references(db: Session, model: Any, ids: List[int]) -> Dict[int, str]:
    """id -> "table.column" for each of `ids` that a table the importer does not own
    points at. Read from the schema's foreign keys, so a learner table added later is
    covered without touching this."""
    found: Dict[int, str] = {}
    if not ids:
        return found
    for table in Base.metadata.tables.values():
        if table.name in _OWNED_TABLES:
            continue
        for fk in table.foreign_keys:
            if fk.column.table is model.__table__:
                column = fk.parent
                for (value,) in db.query(column).filter(column.in_(ids)).distinct().all():
                    found.setdefault(value, f"{table.name}.{column.name}")
    return found


def _completed_ids(db: Session, topic_ids: List[int]) -> Dict[str, set]:
    """Lesson and exercise ids that any learner has recorded as done in these modules.
    They sit in JSON arrays, not foreign keys, so the schema scan cannot see them."""
    done: Dict[str, set] = {"lessons": set(), "exercises": set()}
    if topic_ids:
        for lessons, exercises in db.query(UserProgress.lessons_completed, UserProgress.exercises_completed).filter(
                UserProgress.tool_topic_id.in_(topic_ids)).all():
            done["lessons"].update(lessons or [])
            done["exercises"].update(exercises or [])
    return done


def _retire_stale(db: Session, report: CourseReport, stale: Dict[str, Dict[str, Any]],
                  course_topic_ids: List[int]) -> None:
    """Delete this course's stale rows, children before parents, keeping any that is
    still referenced. Core deletes (not ORM) so nothing cascades or is nulled behind
    our back: a missed reference is a foreign-key error and the transaction rolls back."""
    kept: Dict[str, str] = {}

    def settle(kind: str, model: Any, blocked_extra: Optional[Dict[int, str]] = None) -> None:
        rows = stale[kind]
        refs = _learner_references(db, model, [r.id for r in rows.values()])
        refs = {**(blocked_extra or {}), **refs}  # a learner reference is the reason worth reporting
        doomed = [r for r in rows.values() if r.id not in refs]
        for key, row in rows.items():
            if row.id in refs:
                kept[key] = refs[row.id]
        if doomed:
            db.query(model).filter(model.id.in_([r.id for r in doomed])).delete(synchronize_session=False)
            report.retired[kind] = report.retired.get(kind, 0) + len(doomed)
        db.flush()

    done = _completed_ids(db, course_topic_ids)

    def completed(kind: str) -> Dict[int, str]:
        return {r.id: f"user_progress.{kind}_completed" for r in stale[kind].values() if r.id in done[kind]}

    settle("projects", Project)
    settle("quizzes", Quiz)
    settle("exercises", Exercise, completed("exercises"))

    # A lesson a surviving exercise is still graded against stays.
    lesson_ids = [r.id for r in stale["lessons"].values()]
    pinned: Dict[int, str] = completed("lessons")
    if lesson_ids:
        for (lesson_id,) in db.query(Exercise.lesson_id).filter(Exercise.lesson_id.in_(lesson_ids)).distinct().all():
            pinned[lesson_id] = "exercises.lesson_id"
    settle("lessons", Lesson, pinned)

    # A module with any child left (kept above, or an unkeyed legacy row) stays.
    pinned = {}
    topic_ids = [r.id for r in stale["topics"].values()]
    if topic_ids:
        for model in (Lesson, Exercise, Quiz, Project):
            for (topic_id,) in db.query(model.tool_topic_id).filter(model.tool_topic_id.in_(topic_ids)).distinct().all():
                pinned[topic_id] = f"{model.__tablename__}.tool_topic_id"
    settle("topics", ToolTopic, pinned)

    report.stale += sorted(f"{key} (kept: referenced by {why})" for key, why in kept.items())


def import_content(db: Session, spec: CourseSpec, tool_course: ToolCourse, *, retire_stale: bool = True) -> CourseReport:
    """Create or update every module, lesson, exercise, quiz and project of `spec`, and
    retire this course's rows the folder no longer has (see the module docstring)."""
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
            **_text_fields(module.description, "description", "description_ar", required=False, given_ar=module.description_ar),
            "order": module.order,
            "difficulty": _difficulty(module.lessons[0].difficulty if module.lessons else "intermediate"),
            "estimated_hours": _hours(module.estimated_minutes),
            "skill_tags": _module_tags(module), "technical_terms": [], "prerequisite_ids": [],
            "is_optional": module.optional,
            "completion_required": module.counts_toward_completion,
        }
        topic = _upsert(db, ToolTopic, topics, key, values, report.modules)
        db.flush()  # the children below need the topic's id

        for lesson in module.lessons:
            lkey = f"{spec.course_id}/{lesson.lesson_id}"
            mark(lkey)
            lesson_row = _upsert(db, Lesson, lessons, lkey, {
                "tool_topic_id": topic.id, **_title_fields(lesson.title, lesson.title_ar),
                **_text_fields(lesson.content, "content", "content_ar", required=True, given_ar=lesson.content_ar),
                "order": lesson.order, "estimated_minutes": lesson.estimated_minutes,
                "has_code_examples": lesson.has_code_examples,
            }, report.lessons)
            db.flush()  # exercises store the canonical database lesson id
            for index, exercise in enumerate(lesson.exercises, start=1):
                ekey = f"{lkey}/x{index}"
                mark(ekey)
                _upsert(
                    db, Exercise, exercises, ekey,
                    _exercise_values(exercise, topic.id, lesson_row.id), report.exercises,
                )
            if lesson.project:
                pkey = f"{lkey}/project"
                mark(pkey)
                _upsert(db, Project, projects, pkey, _project_values(lesson.project, topic.id), report.projects)

        if module.quiz:
            qkey = f"{key}/quiz"
            mark(qkey)
            _upsert(db, Quiz, quizzes, qkey, _quiz_values(module, topic.id), report.quizzes)

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

    stale = {
        kind: {k: row for k, row in store.items() if k not in produced}
        for kind, store in (("topics", topics), ("lessons", lessons), ("exercises", exercises),
                            ("quizzes", quizzes), ("projects", projects))
    }
    if retire_stale and spec.has_lesson_bodies and spec.modules:
        _retire_stale(db, report, stale, [t.id for t in topics.values()])
    else:
        for rows in stale.values():
            report.stale += sorted(rows)

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
            "alt_ar": asset.alt_ar, "caption_ar": asset.caption_ar,
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


def import_course(db: Session, spec: CourseSpec, definition: Mapping[str, Any], *,
                  retire_stale: bool = True) -> CourseReport:
    """Course record + content for one folder. Does not commit."""
    course = ensure_course_record(db, definition, spec)
    tool_course = course.tool_course
    report = import_content(db, spec, tool_course, retire_stale=retire_stale)
    import_assets(db, spec, tool_course, report)
    return report
