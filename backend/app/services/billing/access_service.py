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
from app.models.user import User, UserRole
from app.services.billing.course_billing import current_offer
from app.services.billing.subscriptions import has_pro_access


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
    # Administrators must be able to inspect and support every course without
    # creating fake purchases or grants for their own account.
    if db.query(User.id).filter(User.id == user_id, User.role == UserRole.admin).first():
        return CourseAccess(True, "admin")
    if has_pro_access(db, user_id):
        return CourseAccess(True, "pro")
    enrollment = active_enrollment(db, user_id, course.id, entitled_only=True)
    if not enrollment:
        return CourseAccess(False, "purchase_required")
    return CourseAccess(True, enrollment.source, enrollment.id)


def enrollment_access(db: Session, user_id: int, course: Course) -> CourseAccess:
    """Whether a learner may create or keep a `course_enrollments` row.

    Enrolling is browsing and progress tracking, not content access: every
    course gives an ordered two-lesson preview regardless of enrollment, and
    `require_lesson_access` is what actually stops lesson 3+ without Pro. So
    enrollment itself is only closed off for a course an admin has put up
    for individual sale (an active `CourseOffer`) that this learner has
    neither Pro nor a purchase/admin grant for - the same gate the checkout
    flow already uses to decide whether the course is even for sale.
    """
    access = course_access(db, user_id, course)
    if access.has_access or current_offer(db, course.id) is None:
        return access if access.has_access else CourseAccess(True, "free_preview")
    return access


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
    Exercises and quizzes authored under either of the first two canonical
    lessons share those lessons' free-preview entitlement. Projects do not.
    """
    course = course_for_content(db, content)
    if course is None:
        return None
    access = course_access(db, user_id, course)
    if access.has_access:
        return access
    if isinstance(content, (Exercise, Quiz)) and is_free_preview_content(db, course, content):
        return CourseAccess(True, "free_preview")
    raise purchase_required(course)


def free_lesson_ids(db: Session, course: Course, limit: int = 2) -> set[int]:
    """The first lessons in canonical course order, independent of the UI."""
    if course.tool_course_id:
        rows = (
            db.query(Lesson.id)
            .join(ToolTopic, Lesson.tool_topic_id == ToolTopic.id)
            .filter(ToolTopic.tool_course_id == course.tool_course_id)
            .order_by(ToolTopic.order.asc(), Lesson.order.asc(), Lesson.id.asc())
            .limit(limit)
            .all()
        )
    elif course.track_level_id:
        rows = (
            db.query(Lesson.id)
            .join(Topic, Lesson.topic_id == Topic.id)
            .filter(Topic.level_id == course.track_level_id)
            .order_by(Topic.order.asc(), Lesson.order.asc(), Lesson.id.asc())
            .limit(limit)
            .all()
        )
    else:
        rows = []
    return {row.id for row in rows}


def _free_lesson_source_keys(db: Session, course: Course, limit: int = 2) -> set[str]:
    ids = free_lesson_ids(db, course, limit)
    if not ids:
        return set()
    return {
        key for (key,) in db.query(Lesson.source_key).filter(Lesson.id.in_(ids)).all()
        if key
    }


def is_free_preview_content(db: Session, course: Course, content, limit: int = 2) -> bool:
    """Whether an imported exercise/quiz belongs to a free preview lesson.

    Canonical imports key children as ``COURSE-NNN/LNNN-NNN/x1`` or
    ``.../quiz``. Legacy topic-level content has no such lesson link and stays
    locked rather than accidentally exposing a whole module.
    """
    source_key = getattr(content, "source_key", None)
    if not source_key:
        return False
    return any(source_key.startswith(f"{lesson_key}/") for lesson_key in _free_lesson_source_keys(db, course, limit))


def free_preview_content_ids(db: Session, course: Course, limit: int = 2) -> tuple[set[int], set[int]]:
    """Exercise ids and quiz ids attached to the course's preview lessons."""
    lesson_keys = _free_lesson_source_keys(db, course, limit)
    if not lesson_keys:
        return set(), set()

    def belongs(source_key: Optional[str]) -> bool:
        return bool(source_key and any(source_key.startswith(f"{key}/") for key in lesson_keys))

    topic_ids: list[int] = []
    tool_topic_ids: list[int] = []
    if course.track_level_id:
        topic_ids = [row.id for row in db.query(Topic.id).filter(Topic.level_id == course.track_level_id).all()]
    if course.tool_course_id:
        tool_topic_ids = [row.id for row in db.query(ToolTopic.id).filter(ToolTopic.tool_course_id == course.tool_course_id).all()]

    def rows(model):
        query = db.query(model.id, model.source_key)
        if topic_ids:
            query = query.filter(model.topic_id.in_(topic_ids))
        elif tool_topic_ids:
            query = query.filter(model.tool_topic_id.in_(tool_topic_ids))
        else:
            return []
        return query.all()

    return (
        {row.id for row in rows(Exercise) if belongs(row.source_key)},
        {row.id for row in rows(Quiz) if belongs(row.source_key)},
    )


def require_lesson_access(db: Session, user_id: int, lesson: Lesson) -> CourseAccess | None:
    course = course_for_content(db, lesson)
    if course is None:
        return None
    access = course_access(db, user_id, course)
    if access.has_access:
        return access
    if lesson.id in free_lesson_ids(db, course):
        return CourseAccess(True, "free_preview")
    raise purchase_required(course)


def course_for_resource_id(db: Session, kind: str, resource_id: int) -> Optional[Course]:
    model = {"exercise": Exercise, "quiz": Quiz, "project": Project, "lesson": Lesson}.get(kind)
    item = db.query(model).filter(model.id == resource_id).first() if model else None
    return course_for_content(db, item) if item else None
