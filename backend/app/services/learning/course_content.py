"""
app/services/learning/course_content.py

A course's *structure* - modules, lesson counts, projects - and, for a signed-in
learner, how far through each module they are.

This is what a course card, the course page and the "where do I start" answer
read. It never returns a lesson body: lessons are fetched (and paywalled) by the
course viewer's own endpoints, so a catalogue listing stays cheap and cannot leak
paid content.

A module is a `ToolTopic` for a tool/curriculum course and a `Topic` for a
track level; the two are read through the same shape. Progress is derived from
`user_progress` exactly as `progress_service.course_completion` derives it -
a lesson or exercise id in the learner's completed lists - so a module's
fraction and the course's fraction can never disagree.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.learning import Exercise, Lesson, Project, Quiz, Topic
from app.models.learning_path import COURSE_KIND_TOOL, Course
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic

MODULE_NOT_STARTED = "not_started"
MODULE_IN_PROGRESS = "in_progress"
MODULE_COMPLETED = "completed"

# A fraction at or above this is finished; see progress_service._DONE.
_DONE = 1.0 - 1e-9


@dataclass
class ProjectInfo:
    id: int
    title: str
    title_ar: Optional[str]
    estimated_hours: Optional[float]
    module_order: int
    # 'module' | 'lab' | 'capstone' | 'lesson' - read off the import's source key.
    kind: str


@dataclass
class LessonTitle:
    """A lesson as the public outline shows it: its name and place, never its body."""
    id: int
    order: int
    title: str
    title_ar: Optional[str]


@dataclass
class ModuleInfo:
    id: int                          # the topic id the viewer opens
    order: int
    title: str
    title_ar: Optional[str]
    description: Optional[str]
    description_ar: Optional[str]
    estimated_hours: Optional[float]
    lesson_count: int
    exercise_count: int
    quiz_count: int
    project_count: int
    # False means visible specialization material that does not enter course
    # completion or become the learner's required "next module".
    completion_required: bool = True
    is_optional: bool = False
    # Only for a signed-in learner.
    completion: Optional[float] = None
    status: Optional[str] = None
    # The outline: lesson names only. Bodies stay behind the course viewer.
    lessons: List[LessonTitle] = field(default_factory=list)

    @property
    def item_count(self) -> int:
        return self.lesson_count + self.exercise_count


def _project_kind(source_key: Optional[str], topic_key: Optional[str]) -> str:
    """'capstone', 'lab', 'lesson' or 'module', read off the import's source keys:
    a project keyed under its module's own key belongs to the module, one keyed under
    a lesson id to that lesson."""
    if not source_key:
        return "module"
    tail = source_key.rsplit("/", 1)[-1]
    if tail in ("capstone", "lab"):
        return tail
    if topic_key and source_key.rsplit("/", 1)[0] != topic_key:
        return "lesson"
    return "module"


def course_modules(db: Session, course: Course, user_id: Optional[int] = None) -> List[ModuleInfo]:
    """Modules in order with content counts (and the learner's progress when
    `user_id` is given) - a fixed number of queries whatever the course size."""
    tool = course.kind == COURSE_KIND_TOOL
    topic_model, owner = (ToolTopic, course.tool_course_id) if tool else (Topic, course.track_level_id)
    owner_col = ToolTopic.tool_course_id if tool else Topic.level_id
    fk = (lambda m: m.tool_topic_id) if tool else (lambda m: m.topic_id)

    topics = db.query(topic_model).filter(owner_col == owner).order_by(topic_model.order, topic_model.id).all()
    if not topics:
        return []
    ids = [t.id for t in topics]

    def counts(model) -> Dict[int, int]:
        return dict(db.query(fk(model), func.count(model.id)).filter(fk(model).in_(ids)).group_by(fk(model)).all())

    lessons, exercises, quizzes, projects = counts(Lesson), counts(Exercise), counts(Quiz), counts(Project)

    # Titles only - the columns are named so a body can never ride along.
    titles: Dict[int, List[LessonTitle]] = {}
    for lid, tid, order, title, title_ar in (
        db.query(Lesson.id, fk(Lesson), Lesson.order, Lesson.title, Lesson.title_ar)
        .filter(fk(Lesson).in_(ids))
        .order_by(Lesson.order, Lesson.id)
        .all()
    ):
        titles.setdefault(tid, []).append(LessonTitle(id=lid, order=order, title=title, title_ar=title_ar))

    done_by_topic: Dict[int, int] = {}
    if user_id is not None:
        lesson_ids: Dict[int, List[int]] = {}
        for lid, tid in db.query(Lesson.id, fk(Lesson)).filter(fk(Lesson).in_(ids)).all():
            lesson_ids.setdefault(tid, []).append(lid)
        exercise_ids: Dict[int, List[int]] = {}
        for eid, tid in db.query(Exercise.id, fk(Exercise)).filter(fk(Exercise).in_(ids)).all():
            exercise_ids.setdefault(tid, []).append(eid)
        progress_col = UserProgress.tool_topic_id if tool else UserProgress.topic_id
        rows = {
            getattr(p, "tool_topic_id" if tool else "topic_id"): p for p in db.query(UserProgress).filter(
                UserProgress.user_id == user_id, progress_col.in_(ids)).all()
        }
        for tid in ids:
            row = rows.get(tid)
            if row is None:
                continue
            done_lessons = set(row.lessons_completed or []) & set(lesson_ids.get(tid, []))
            done_exercises = set(row.exercises_completed or []) & set(exercise_ids.get(tid, []))
            done_by_topic[tid] = len(done_lessons) + len(done_exercises)

    result: List[ModuleInfo] = []
    for t in topics:
        info = ModuleInfo(
            id=t.id, order=t.order, title=t.title, title_ar=t.title_ar,
            description=t.description, description_ar=t.description_ar,
            estimated_hours=t.estimated_hours,
            lesson_count=lessons.get(t.id, 0), exercise_count=exercises.get(t.id, 0),
            quiz_count=quizzes.get(t.id, 0), project_count=projects.get(t.id, 0),
            completion_required=t.completion_required if tool else True,
            is_optional=t.is_optional if tool else False,
            lessons=titles.get(t.id, []),
        )
        if user_id is not None:
            total = info.item_count
            fraction = (done_by_topic.get(t.id, 0) / total) if total else 0.0
            info.completion = round(fraction, 4)
            info.status = (MODULE_COMPLETED if total and fraction >= _DONE
                           else MODULE_IN_PROGRESS if fraction > 0 else MODULE_NOT_STARTED)
        result.append(info)
    return result


def course_projects(db: Session, course: Course) -> List[ProjectInfo]:
    """Project titles (never briefs or rubrics) with the module they belong to."""
    tool = course.kind == COURSE_KIND_TOOL
    topic_model, owner = (ToolTopic, course.tool_course_id) if tool else (Topic, course.track_level_id)
    owner_col = ToolTopic.tool_course_id if tool else Topic.level_id
    fk = Project.tool_topic_id if tool else Project.topic_id
    topic_key = ToolTopic.source_key if tool else None
    rows = (
        db.query(Project.id, Project.title, Project.title_ar, Project.estimated_hours, Project.source_key,
                 topic_model.order, topic_key if tool else Project.source_key)
        .join(topic_model, topic_model.id == fk)
        .filter(owner_col == owner)
        .order_by(topic_model.order, Project.id)
        .all()
    )
    return [
        ProjectInfo(id=r[0], title=r[1], title_ar=r[2], estimated_hours=r[3], module_order=r[5],
                    kind=_project_kind(r[4], r[6] if tool else None))
        for r in rows
    ]


def first_incomplete(modules: List[ModuleInfo]) -> Optional[ModuleInfo]:
    """The module to continue from: the first not finished, in order."""
    return next(
        (m for m in modules if m.completion_required and m.status != MODULE_COMPLETED and m.item_count),
        None,
    )
