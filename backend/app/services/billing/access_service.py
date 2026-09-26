"""The single course-access policy used by billing and learning routes."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.billing import CourseEnrollment
from app.models.learning import Exercise, Lesson, Project, Quiz, Topic
from app.models.learning_path import Course
from app.models.tool_course import ToolTopic


@dataclass(frozen=True)
class CourseAccess:
    has_access: bool
    reason: str
    enrollment_id: Optional[int] = None


def active_enrollment(
    db: Session, user_id: int, course_id: int, *, entitled_only: bool = False,
) -> Optional[CourseEnrollment]:
    """The learner's live enrollment in a course, if any.

    `entitled_only` keeps only enrollments that *grant* access to a paid course -
    a purchase or an admin grant. A `free` enrollment records that the learner
    joined while the course cost nothing; it is never a purchase, so it does not
    open the course (or block buying it) once it is made paid."""
    now = datetime.now(timezone.utc)
    query = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.status == "active",
        or_(CourseEnrollment.expires_at.is_(None), CourseEnrollment.expires_at > now),
    )
    if entitled_only:
        query = query.filter(CourseEnrollment.source != "free")
    return query.first()


def course_access(db: Session, user_id: int, course: Course) -> CourseAccess:
    if course.is_free:
        return CourseAccess(True, "free")
    enrollment = active_enrollment(db, user_id, course.id, entitled_only=True)
    if not enrollment:
        return CourseAccess(False, "purchase_required")
    return CourseAccess(True, enrollment.source, enrollment.id)


def has_course_access(db: Session, user_id: int, course_id: int) -> bool:
    course = db.query(Course).filter(Course.id == course_id, Course.is_active.is_(True)).first()
    return bool(course and course_access(db, user_id, course).has_access)


def purchase_required(course: Course) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"code": "COURSE_PURCHASE_REQUIRED", "course_id": course.slug},
    )


def require_course_access(db: Session, user_id: int, course: Course) -> CourseAccess:
    access = course_access(db, user_id, course)
    if not access.has_access:
        raise purchase_required(course)
    return access


def course_for_track_topic(db: Session, topic_id: int) -> Optional[Course]:
    return (
        db.query(Course)
        .join(Topic, Topic.level_id == Course.track_level_id)
        .filter(Topic.id == topic_id, Course.is_active.is_(True))
        .first()
    )


def course_for_tool_topic(db: Session, topic_id: int) -> Optional[Course]:
    return (
        db.query(Course)
        .join(ToolTopic, ToolTopic.tool_course_id == Course.tool_course_id)
        .filter(ToolTopic.id == topic_id, Course.is_active.is_(True))
        .first()
    )


def course_for_content(db: Session, content) -> Optional[Course]:
    if getattr(content, "topic_id", None):
        return course_for_track_topic(db, content.topic_id)
    if getattr(content, "tool_topic_id", None):
        return course_for_tool_topic(db, content.tool_topic_id)
    return None


def require_content_access(db: Session, user_id: int, content) -> CourseAccess | None:
    """Require ownership for an exercise, quiz or project.

    Content not represented by the new catalogue keeps its legacy behaviour;
    this prevents a partially migrated catalogue from making old routes fail.
    """
    course = course_for_content(db, content)
    return require_course_access(db, user_id, course) if course else None


def require_lesson_access(db: Session, user_id: int, lesson: Lesson) -> CourseAccess | None:
    if lesson.is_preview:
        return CourseAccess(True, "preview")
    return require_content_access(db, user_id, lesson)


def course_for_resource_id(db: Session, kind: str, resource_id: int) -> Optional[Course]:
    model = {"exercise": Exercise, "quiz": Quiz, "project": Project, "lesson": Lesson}.get(kind)
    item = db.query(model).filter(model.id == resource_id).first() if model else None
    return course_for_content(db, item) if item else None
