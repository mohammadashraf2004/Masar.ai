"""
backend/app/controllers/tool_courses_controller.py

Standalone tool courses (LangChain, Docker, Pinecone, etc.) — separate
from the CareerTrack system. A user can enroll in any tool course
independently of any track, at any time, with no prerequisites.
Progress tracking mirrors tracks_controller.py's pattern but keyed on
tool_topic_id instead of topic_id; quiz/project submission reuses the
existing /tracks/quizzes/{id}/submit and /tracks/projects/{id}/submit
endpoints as-is, since those operate on Quiz/Project rows by id
regardless of which kind of topic they belong to.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.tool_course import ToolCourse, ToolTopic, ToolEnrollment, ToolCourseCompletion
from app.models.learning import Lesson, Exercise, Project, Quiz
from app.models.progress import UserProgress, ProgressStatus
from app.views.tool_course import (
    ToolCourseSummary, ToolCourseResponse, ToolTopicResponse,
    ToolEnrollRequest, ToolEnrollmentResponse,
    ToolProgressUpdate, ToolProgressResponse,
)
from app.core.security import get_current_user

router = APIRouter(prefix="/tool-courses", tags=["Tool Courses"])

# Mirrors tracks_controller.MAX_TOPIC_MINUTES.
MAX_TOPIC_MINUTES = 100_000


def _validate_progress_targets(db: Session, payload: ToolProgressUpdate, *, topic_id: int) -> None:
    """Same rule as tracks_controller._validate_progress_targets, and for
    the same reason — here it matters more, because completion of every
    topic in a tool course writes a ToolCourseCompletion row, i.e. a
    credential. Marking topics done with lesson ids picked out of thin air
    would forge that credential outright."""
    if payload.lesson_id is not None:
        if not db.query(Lesson.id).filter(
            Lesson.id == payload.lesson_id,
            Lesson.tool_topic_id == topic_id,
        ).first():
            raise HTTPException(status_code=400, detail="That lesson does not belong to this topic")

    if payload.exercise_id is not None:
        if not db.query(Exercise.id).filter(
            Exercise.id == payload.exercise_id,
            Exercise.tool_topic_id == topic_id,
        ).first():
            raise HTTPException(status_code=400, detail="That exercise does not belong to this topic")


# ─── Browse ──────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ToolCourseSummary])
def list_tool_courses(db: Session = Depends(get_db)):
    courses = (
        db.query(ToolCourse)
        .options(joinedload(ToolCourse.topics))
        .filter(ToolCourse.is_active == True)
        .order_by(ToolCourse.category, ToolCourse.title)
        .all()
    )
    return [
        ToolCourseSummary(
            **{c.name: getattr(course, c.name) for c in course.__table__.columns},
            topic_count=len(course.topics),
        )
        for course in courses
    ]


# ─── Enrollment — MUST come before /{slug} to avoid route collision ─────

@router.post("/enroll", response_model=ToolEnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll(
    payload: ToolEnrollRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = db.query(ToolCourse).filter(
        ToolCourse.id == payload.tool_course_id,
        ToolCourse.is_active == True,
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Tool course not found")

    existing = db.query(ToolEnrollment).filter(
        ToolEnrollment.user_id == current_user.id,
        ToolEnrollment.tool_course_id == payload.tool_course_id,
    ).first()
    if existing:
        return existing

    enrollment = ToolEnrollment(user_id=current_user.id, tool_course_id=payload.tool_course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/my-enrollments", response_model=List[ToolEnrollmentResponse])
def my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Same reasoning as tracks_controller.my_enrollments: a retired course
    # must not linger on the dashboard, since GET /tool-courses/{slug}
    # filters on is_active and would 404 on the card.
    enrollments = (
        db.query(ToolEnrollment)
        .join(ToolCourse, ToolEnrollment.tool_course_id == ToolCourse.id)
        .options(joinedload(ToolEnrollment.tool_course).joinedload(ToolCourse.topics))
        .filter(
            ToolEnrollment.user_id == current_user.id,
            ToolCourse.is_active == True,
        )
        .all()
    )
    result = []
    for e in enrollments:
        course = e.tool_course
        result.append(ToolEnrollmentResponse(
            id=e.id,
            tool_course_id=e.tool_course_id,
            tool_course=ToolCourseSummary(
                **{c.name: getattr(course, c.name) for c in course.__table__.columns},
                topic_count=len(course.topics),
            ),
            progress_pct=e.progress_pct,
            enrolled_at=e.enrolled_at,
            completed_at=e.completed_at,
        ))
    return result


# ─── Course detail — AFTER all literal routes ───────────────────────────

@router.get("/{slug}", response_model=ToolCourseResponse)
def get_tool_course(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Authenticated, same reasoning as GET /tracks/{slug}: the response
    carries the course's full lesson bodies, not a catalogue entry."""
    course = (
        db.query(ToolCourse)
        .options(
            joinedload(ToolCourse.topics).joinedload(ToolTopic.lessons),
            joinedload(ToolCourse.topics).joinedload(ToolTopic.exercises),
            joinedload(ToolCourse.topics).joinedload(ToolTopic.quizzes),
            joinedload(ToolCourse.topics).joinedload(ToolTopic.projects),
        )
        .filter(ToolCourse.slug == slug, ToolCourse.is_active == True)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Tool course not found")
    return course


# ─── Topic detail ────────────────────────────────────────────────────────

@router.get("/topics/{topic_id}", response_model=ToolTopicResponse)
def get_tool_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = (
        db.query(ToolTopic)
        .options(
            joinedload(ToolTopic.lessons),
            joinedload(ToolTopic.exercises),
            joinedload(ToolTopic.quizzes),
            joinedload(ToolTopic.projects),
        )
        .filter(ToolTopic.id == topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


# ─── Progress tracking ────────────────────────────────────────────────────

def _recompute_course_progress(db: Session, user_id: int, tool_course_id: int) -> None:
    """Keeps ToolEnrollment.progress_pct in sync: fraction of the course's
    topics that have at least one recorded UserProgress row with a
    non-empty lessons_completed list. Simple and cheap; matches the
    granularity actually shown in the UI (topic-level progress cards)."""
    topic_ids = [t.id for t in db.query(ToolTopic.id).filter(ToolTopic.tool_course_id == tool_course_id).all()]
    if not topic_ids:
        return
    done = (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == user_id,
            UserProgress.tool_topic_id.in_(topic_ids),
            UserProgress.status == ProgressStatus.completed,
        )
        .count()
    )
    pct = round(100 * done / len(topic_ids), 1)

    enrollment = db.query(ToolEnrollment).filter(
        ToolEnrollment.user_id == user_id,
        ToolEnrollment.tool_course_id == tool_course_id,
    ).first()
    if enrollment:
        enrollment.progress_pct = pct
        if pct >= 100 and not enrollment.completed_at:
            enrollment.completed_at = datetime.utcnow()
            if not db.query(ToolCourseCompletion).filter(
                ToolCourseCompletion.user_id == user_id,
                ToolCourseCompletion.tool_course_id == tool_course_id,
            ).first():
                db.add(ToolCourseCompletion(user_id=user_id, tool_course_id=tool_course_id))
        db.commit()


@router.post("/topics/{topic_id}/progress", response_model=ToolProgressResponse)
def update_tool_progress(
    topic_id: int,
    payload: ToolProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = db.query(ToolTopic).filter(ToolTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    _validate_progress_targets(db, payload, topic_id=topic_id)

    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.tool_topic_id == topic_id,
    ).first()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            tool_topic_id=topic_id,
            status=ProgressStatus.in_progress,
            started_at=datetime.utcnow(),
        )
        db.add(progress)

    if payload.lesson_id and payload.lesson_id not in (progress.lessons_completed or []):
        progress.lessons_completed = (progress.lessons_completed or []) + [payload.lesson_id]

    if payload.exercise_id and payload.exercise_id not in (progress.exercises_completed or []):
        progress.exercises_completed = (progress.exercises_completed or []) + [payload.exercise_id]

    if payload.time_spent_minutes:
        progress.time_spent_minutes = min(
            MAX_TOPIC_MINUTES,
            (progress.time_spent_minutes or 0) + payload.time_spent_minutes,
        )

    # A topic counts as done once every lesson and exercise attached to it
    # has been marked complete.
    total_lessons = db.query(Lesson).filter(Lesson.tool_topic_id == topic_id).count()
    total_exercises = db.query(Exercise).filter(Exercise.tool_topic_id == topic_id).count()
    lessons_done = len(progress.lessons_completed or [])
    exercises_done = len(progress.exercises_completed or [])
    if lessons_done >= total_lessons and exercises_done >= total_exercises and (total_lessons or total_exercises):
        progress.status = ProgressStatus.completed
        progress.completed_at = progress.completed_at or datetime.utcnow()

    db.commit()
    db.refresh(progress)
    _recompute_course_progress(db, current_user.id, topic.tool_course_id)
    return progress


@router.get("/topics/{topic_id}/progress", response_model=ToolProgressResponse)
def get_tool_topic_progress(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.tool_topic_id == topic_id,
    ).first()
    if not progress:
        raise HTTPException(status_code=404, detail="No progress found for this topic")
    return progress
