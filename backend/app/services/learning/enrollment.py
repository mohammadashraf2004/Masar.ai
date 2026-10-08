"""
app/services/learning/enrollment.py

Enrolling in a course - directly, with no track, career goal or roadmap involved.

`course_enrollments` (one row per learner and course) is the single enrollment
record. It carries *access* (`status`, `source`, `expires_at` - set by a purchase
or an admin grant, see `access_service`) and the *learning lifecycle*
(`learning_status`, `started_at`, `completed_at`) that this module keeps.
Progress itself is derived from `user_progress` and is never stored on the
enrollment: `progress_percentage` in every response is recomputed.

Rules
-----
* Enrolling is idempotent: a second call returns the same row and creates nothing.
* A paid course the learner has not bought is refused with the same 403 the
  lesson endpoints use - the entitlement decision lives in `access_service`, not here.
* A free course needs no purchase, and its enrollment (`source='free'`) never
  grants access to it if it is later made paid.
* Readiness never blocks: it is computed *around* enrollment (see `readiness`)
  and only advises.
* Recording progress in an accessible course enrolls the learner if they were not
  yet, so "enrolled" is always true of anyone who is working in a course.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.billing import CourseEnrollment
from app.models.learning_path import COURSE_KIND_TOOL, Course
from app.models.tool_course import CURRICULUM_CATEGORY, ToolEnrollment
from app.models.user import User
from app.services.billing.access_service import enrollment_access, purchase_required
from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.progress_service import _DONE, course_completion

logger = logging.getLogger("app.learning.enrollment")

ENROLLED, IN_PROGRESS, COMPLETED, PAUSED = "enrolled", "in_progress", "completed", "paused"


def course_unavailable(course: Course) -> HTTPException:
    """Same code the checkout uses for a course with no published lessons."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"code": "COURSE_UNAVAILABLE", "message": "This course is not currently available.",
                "course_id": course.slug},
    )


def get_enrollment(db: Session, user_id: int, course_id: int) -> Optional[CourseEnrollment]:
    return db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id, CourseEnrollment.course_id == course_id,
    ).first()


def _mirror_tool_enrollment(db: Session, user_id: int, course: Course) -> None:
    """A hand-seeded tool course (LangChain, Docker...) also keeps its own
    enrollment row for the Tools pages; keep the two in step. Curriculum courses
    are not tools and have none."""
    tool = course.tool_course
    if course.kind != COURSE_KIND_TOOL or tool is None or tool.category == CURRICULUM_CATEGORY:
        return
    exists = db.query(ToolEnrollment.id).filter(
        ToolEnrollment.user_id == user_id, ToolEnrollment.tool_course_id == tool.id,
    ).first()
    if not exists:
        db.add(ToolEnrollment(user_id=user_id, tool_course_id=tool.id))


def enroll(db: Session, user: User, course: Course, bundle: CatalogBundle) -> Tuple[CourseEnrollment, bool]:
    """Enroll `user` in `course`. Returns `(enrollment, created)`. Commits."""
    info = bundle.catalog.courses.get(course.id)
    if not course.is_active or info is None or not info.is_available:
        raise course_unavailable(course)

    access = enrollment_access(db, user.id, course)
    if not access.has_access:
        raise purchase_required(course)

    existing = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user.id, CourseEnrollment.course_id == course.id,
    ).with_for_update().first()
    if existing is not None:
        if existing.status != "active" and existing.source == "free":
            existing.status, existing.expires_at = "active", None
            _mirror_tool_enrollment(db, user.id, course)
            db.commit()
        return existing, False

    enrollment = CourseEnrollment(
        user_id=user.id, course_id=course.id, source="free", status="active", learning_status=ENROLLED,
    )
    db.add(enrollment)
    _mirror_tool_enrollment(db, user.id, course)
    try:
        db.commit()
    except IntegrityError:
        # A concurrent request enrolled the same learner first: that row is the answer.
        db.rollback()
        existing = get_enrollment(db, user.id, course.id)
        if existing is None:
            raise
        return existing, False
    db.refresh(enrollment)
    logger.info("learning.course_enrolled", extra={"user_id": user.id, "course_id": course.id})
    return enrollment, True


def set_paused(db: Session, user: User, course: Course, paused: bool) -> CourseEnrollment:
    """The one lifecycle state that is the learner's own choice."""
    enrollment = get_enrollment(db, user.id, course.id)
    if enrollment is None or enrollment.status != "active":
        raise HTTPException(status_code=404, detail="You are not enrolled in this course")
    fraction = course_completion(db, user.id, [course])[course.id]
    if paused:
        if enrollment.learning_status != COMPLETED:
            enrollment.learning_status = PAUSED
    else:
        enrollment.learning_status = _status_for(fraction)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def _status_for(fraction: float) -> str:
    if fraction >= _DONE:
        return COMPLETED
    return IN_PROGRESS if fraction > 0 else ENROLLED


def sync_lifecycle(db: Session, user_id: int, course: Course, *, fraction: Optional[float] = None) -> None:
    """Move an enrollment's lifecycle to match the learner's real progress.

    Called after progress is recorded. Never raises into the caller: the progress
    write has already been committed, and a lifecycle cache that lags is
    repaired by the next call, so an error here is logged, not surfaced."""
    try:
        if fraction is None:
            fraction = course_completion(db, user_id, [course])[course.id]
        enrollment = get_enrollment(db, user_id, course.id)
        now = datetime.now(timezone.utc)
        if enrollment is None:
            if not enrollment_access(db, user_id, course).has_access:
                return
            enrollment = CourseEnrollment(
                user_id=user_id, course_id=course.id, source="free", status="active", learning_status=ENROLLED,
            )
            db.add(enrollment)
            _mirror_tool_enrollment(db, user_id, course)
            db.flush()
        wanted = _status_for(fraction)
        if wanted != ENROLLED and not enrollment.started_at:
            enrollment.started_at = now
        if wanted == COMPLETED:
            enrollment.completed_at = enrollment.completed_at or now
        elif enrollment.completed_at is not None:
            enrollment.completed_at = None       # new material was added after completion
        if not (wanted == ENROLLED and enrollment.learning_status == PAUSED):
            enrollment.learning_status = wanted
        enrollment.updated_at = now
        db.commit()
    except IntegrityError:
        db.rollback()          # raced another writer creating the same row; the row exists now
    except Exception:  # noqa: BLE001 - see docstring
        db.rollback()
        logger.warning("learning.lifecycle_sync_failed", exc_info=True,
                       extra={"user_id": user_id, "course_id": course.id})
