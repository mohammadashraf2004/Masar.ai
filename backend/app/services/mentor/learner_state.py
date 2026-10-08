"""What the mentor may know about a learner, read from Masar's own records.

Least privilege: only educationally relevant facts - which courses they are enrolled in, which
lessons of those courses they finished, what they may open, and how their quiz answers went.
Never the account record, contact details or billing. Every value here comes from the
database; nothing is estimated or supplied by the client, and nothing is invented when a
record is missing (the caller says "no enrolments yet" instead).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.billing import CourseEnrollment
from app.models.learning import Lesson, Topic
from app.models.learning_path import CareerRole, Course, LearningProfile
from app.models.mentor_evidence import MentorEvidence
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic
from app.services.billing.access_service import course_access, free_lesson_ids
from app.services.mentor.v2 import skills as skill_model


@dataclass
class CourseState:
    course: Course
    title: str
    lessons: List[Lesson]                  # canonical order
    completed: set = field(default_factory=set)
    accessible: Optional[set] = None       # None: every lesson; else the preview ids
    last_activity: Optional[datetime] = None

    @property
    def done(self) -> int:
        return sum(1 for lesson in self.lessons if lesson.id in self.completed)

    def remaining(self) -> List[Lesson]:
        return [lesson for lesson in self.lessons if lesson.id not in self.completed]

    def can_open(self, lesson: Lesson) -> bool:
        return self.accessible is None or lesson.id in self.accessible


def _title(course: Course, language: str) -> str:
    # A catalogue title is an optional override of the source course's own title.
    source = course.tool_course or course.track_level
    english = course.title or getattr(source, "title", None) or course.slug
    arabic = course.title_ar or getattr(source, "title_ar", None)
    return arabic if language == "ar" and arabic else english


def lesson_title(lesson: Lesson, language: str) -> str:
    return (lesson.title_ar if language == "ar" and lesson.title_ar else lesson.title) or ""


def enrolled_courses(db: Session, user_id: int, language: str = "en", limit: int = 4) -> List[CourseState]:
    """The learner's active enrolments with their real lesson order and completion, the most
    recently active course first. Three queries for any number of courses."""
    now = datetime.now(timezone.utc)
    enrollments = (
        db.query(CourseEnrollment)
        .join(Course, CourseEnrollment.course_id == Course.id)
        .filter(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.status == "active",
            or_(CourseEnrollment.expires_at.is_(None), CourseEnrollment.expires_at > now),
            Course.is_active.is_(True),
        )
        .order_by(CourseEnrollment.enrolled_at.desc())
        .limit(limit)
        .all()
    )
    courses = [enrollment.course for enrollment in enrollments]
    tool_ids = [course.tool_course_id for course in courses if course.tool_course_id]
    level_ids = [course.track_level_id for course in courses if course.track_level_id]

    lessons_by_course: Dict[int, List[Lesson]] = {course.id: [] for course in courses}
    topic_course: Dict[tuple, int] = {}
    if tool_ids:
        rows = (
            db.query(Lesson, ToolTopic.tool_course_id)
            .join(ToolTopic, Lesson.tool_topic_id == ToolTopic.id)
            .filter(ToolTopic.tool_course_id.in_(tool_ids))
            .order_by(ToolTopic.order, Lesson.order, Lesson.id)
            .all()
        )
        by_tool = {course.tool_course_id: course.id for course in courses if course.tool_course_id}
        for lesson, tool_course_id in rows:
            lessons_by_course[by_tool[tool_course_id]].append(lesson)
            topic_course[("tool", lesson.tool_topic_id)] = by_tool[tool_course_id]
    if level_ids:
        rows = (
            db.query(Lesson, Topic.level_id)
            .join(Topic, Lesson.topic_id == Topic.id)
            .filter(Topic.level_id.in_(level_ids))
            .order_by(Topic.order, Lesson.order, Lesson.id)
            .all()
        )
        by_level = {course.track_level_id: course.id for course in courses if course.track_level_id}
        for lesson, level_id in rows:
            lessons_by_course[by_level[level_id]].append(lesson)
            topic_course[("topic", lesson.topic_id)] = by_level[level_id]

    states = {
        course.id: CourseState(course=course, title=_title(course, language), lessons=lessons_by_course[course.id])
        for course in courses
    }
    tool_topics = [key[1] for key in topic_course if key[0] == "tool"]
    topics = [key[1] for key in topic_course if key[0] == "topic"]
    if tool_topics or topics:
        filters = []
        if tool_topics:
            filters.append(UserProgress.tool_topic_id.in_(tool_topics))
        if topics:
            filters.append(UserProgress.topic_id.in_(topics))
        for row in db.query(UserProgress).filter(UserProgress.user_id == user_id, or_(*filters)).all():
            key = ("tool", row.tool_topic_id) if row.tool_topic_id else ("topic", row.topic_id)
            state = states.get(topic_course.get(key))
            if state is None:
                continue
            state.completed |= {int(value) for value in (row.lessons_completed or []) if str(value).isdigit()}
            stamp = row.completed_at or row.started_at
            if stamp is not None and (state.last_activity is None or stamp > state.last_activity):
                state.last_activity = stamp

    for state in states.values():
        if not course_access(db, user_id, state.course).has_access:
            state.accessible = free_lesson_ids(db, state.course)
    ordered = [states[course.id] for course in courses]
    # Most recent activity first; never-started courses keep their enrolment order after them.
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    ordered.sort(key=lambda state: state.last_activity or epoch, reverse=True)
    return ordered


def studied_lessons(states: List[CourseState], language: str, limit: int = 12) -> List[str]:
    """Titles of lessons the learner has completed, most active course first."""
    titles: List[str] = []
    for state in states:
        for lesson in reversed(state.lessons):
            if lesson.id in state.completed:
                titles.append(lesson_title(lesson, language))
            if len(titles) >= limit:
                return titles
    return titles


def career_role(db: Session, user_id: int, language: str) -> Optional[str]:
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if not profile or not profile.career_role_id:
        return None
    role = db.query(CareerRole).filter(CareerRole.id == profile.career_role_id).first()
    if role is None:
        return None
    return role.title_ar if language == "ar" and getattr(role, "title_ar", None) else role.title


def skill_summaries(db: Session, user_id: int, limit: int = 8) -> List[dict]:
    """Every skill the learner has quiz evidence for, folded by the mentor's skill model
    (one query). Weakest first, so what needs review is what they see."""
    rows = (
        db.query(MentorEvidence)
        .filter(MentorEvidence.user_id == user_id)
        .order_by(MentorEvidence.created_at, MentorEvidence.id)
        .all()
    )
    grouped: Dict[str, List[MentorEvidence]] = {}
    for row in rows:
        grouped.setdefault(row.skill, []).append(row)
    out = []
    for name, evidence in grouped.items():
        state = skill_model._fold(evidence)
        out.append({
            "name": name,
            "status": state.status,
            "confidence": state.confidence,
            "questions": state.questions,
            "correct": sum(1 for row in evidence if row.correct),
            "answers": len(evidence),
        })
    order = {skill_model.NEEDS_REVIEW: 0, skill_model.LEARNING: 1, skill_model.MASTERED: 2}
    out.sort(key=lambda item: (order.get(item["status"], 1), item["confidence"]))
    return out[:limit]
