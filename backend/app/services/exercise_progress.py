"""Recording that a learner completed an exercise.

One place for the three rules every completion path must follow:

* only the server decides that an exercise was passed: a code exercise by
  the deterministic grader, a written one by a correct evaluated answer.
  The generic progress routes accept an exercise id only when that verdict
  is on record (``written_answer_accepted``);
* the read-modify-write of a ``user_progress`` row is serialized per learner
  and topic (``lock_progress``), so two completions arriving together can
  neither lose one another nor create a second row for the same topic;
* completing an item refreshes the course figures derived from it
  (``refresh_course_progress``), whichever route recorded it.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.answer_submission import AnswerSubmission
from app.models.learning import Exercise, Lesson
from app.models.progress import ProgressStatus, UserProgress
from app.models.tool_course import ToolCourseCompletion, ToolEnrollment, ToolTopic


def lock_progress(db: Session, user_id: int, *, tool_topic_id: int | None = None, topic_id: int | None = None) -> None:
    """Hold a transaction-scoped lock on this learner's progress for one
    topic until the surrounding transaction ends. ``user_progress`` has no
    unique key on (user, topic), and its completion lists are JSON arrays
    rewritten whole, so without this two concurrent completions could each
    insert a row, or each overwrite the other's list."""
    if db.get_bind().dialect.name != "postgresql":
        return
    scope = f"tool:{tool_topic_id}" if tool_topic_id is not None else f"track:{topic_id}"
    db.execute(text("SELECT pg_advisory_xact_lock(hashtext(:key))"), {"key": f"user_progress:{user_id}:{scope}"})


def written_answer_accepted(db: Session, user_id: int, exercise_id: int) -> bool:
    """The evaluator has accepted this learner's written answer."""
    return db.query(AnswerSubmission.id).filter(
        AnswerSubmission.user_id == user_id,
        AnswerSubmission.exercise_id == exercise_id,
        AnswerSubmission.is_correct.is_(True),
    ).first() is not None


def mark_complete(db: Session, user_id: int, exercise: Exercise) -> bool:
    """Record completion in Masar's UserProgress aggregate. Idempotent;
    returns True when this call added the exercise."""
    filters = [UserProgress.user_id == user_id]
    values: dict[str, Any] = {"user_id": user_id, "status": ProgressStatus.in_progress, "started_at": datetime.utcnow()}
    if exercise.tool_topic_id is not None:
        lock_progress(db, user_id, tool_topic_id=exercise.tool_topic_id)
        filters.append(UserProgress.tool_topic_id == exercise.tool_topic_id)
        values["tool_topic_id"] = exercise.tool_topic_id
    elif exercise.topic_id is not None:
        lock_progress(db, user_id, topic_id=exercise.topic_id)
        filters.append(UserProgress.topic_id == exercise.topic_id)
        values["topic_id"] = exercise.topic_id
    else:
        return False
    progress = db.query(UserProgress).filter(*filters).order_by(UserProgress.id.asc()).first()
    if progress is None:
        progress = UserProgress(**values)
        db.add(progress)
        db.flush()
    completed = progress.exercises_completed or []
    added = exercise.id not in completed
    if added:
        progress.exercises_completed = [*completed, exercise.id]

    if exercise.tool_topic_id is not None:
        total_lessons = db.query(Lesson).filter(Lesson.tool_topic_id == exercise.tool_topic_id).count()
        total_exercises = db.query(Exercise).filter(Exercise.tool_topic_id == exercise.tool_topic_id).count()
        if (len(progress.lessons_completed or []) >= total_lessons
                and len(progress.exercises_completed or []) >= total_exercises
                and (total_lessons or total_exercises)):
            progress.status = ProgressStatus.completed
            progress.completed_at = progress.completed_at or datetime.utcnow()
    return added


def recompute_tool_course_progress(db: Session, user_id: int, tool_course_id: int) -> None:
    """Keep ToolEnrollment.progress_pct (and the completion record) in step:
    the fraction of the course's required topics this learner completed."""
    topic_ids = [
        t.id for t in db.query(ToolTopic.id).filter(
            ToolTopic.tool_course_id == tool_course_id,
            ToolTopic.completion_required.is_(True),
        ).all()
    ]
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


def refresh_course_progress(db: Session, user_id: int, exercise: Exercise) -> None:
    """After a completion has been committed: the tool course's percentage
    and the course enrollment's lifecycle (both derived from the items)."""
    from app.services.billing.access_service import course_for_content
    from app.services.learning import enrollment as course_enrollment

    if exercise.tool_topic_id is not None:
        tool_course_id = db.query(ToolTopic.tool_course_id).filter(ToolTopic.id == exercise.tool_topic_id).scalar()
        if tool_course_id is not None:
            recompute_tool_course_progress(db, user_id, tool_course_id)
    course = course_for_content(db, exercise)
    if course is not None:
        course_enrollment.sync_lifecycle(db, user_id, course)
