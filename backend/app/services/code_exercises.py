"""Application service connecting execution, grading, attempts, and progress."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.code_exercise import CodeExerciseAttempt
from app.models.learning import Exercise, Lesson
from app.models.progress import ProgressStatus, UserProgress
from app.services.code_execution import IsolatedPythonRunner
from app.services.code_grading import PythonGrader, SQLGrader, TextGrader


RUNNER = IsolatedPythonRunner()
GRADER = PythonGrader(RUNNER)
TEXT_GRADER = TextGrader()
SQL_GRADER = SQLGrader()
TEXT_LANGUAGES = frozenset({"bash", "dockerfile", "hcl", "ini", "sparql", "yaml"})


def grader_for_language(language: str | None):
    if language == "python":
        return GRADER
    if language == "sql":
        return SQL_GRADER
    if language in TEXT_LANGUAGES:
        return TEXT_GRADER
    return None


def feedback_messages(value: Any, fallback: dict[str, str]) -> dict[str, str]:
    if isinstance(value, str) and value.strip():
        return {"en": value.strip(), "ar": value.strip()}
    if isinstance(value, dict):
        en = str(value.get("en") or value.get("ar") or fallback["en"])
        ar = str(value.get("ar") or value.get("en") or fallback["ar"])
        return {"en": en, "ar": ar}
    return fallback


def record_attempt(
    db: Session, *, user_id: int, exercise_id: int, action: str, status: str,
    submission: str | None = None, passed: bool = False, failed_test_id: str | None = None,
    tests_passed: int = 0, tests_total: int = 0, execution_time_ms: int = 0,
) -> CodeExerciseAttempt:
    attempt = CodeExerciseAttempt(
        user_id=user_id, exercise_id=exercise_id, action=action,
        # Run events intentionally omit source; submitted source is bounded by
        # the request schema and retained for useful attempt analysis.
        submission=submission if action == "submit" else None,
        status=status, passed=passed, failed_test_id=failed_test_id,
        tests_passed=tests_passed, tests_total=tests_total,
        execution_time_ms=execution_time_ms,
    )
    db.add(attempt)
    return attempt


def mark_complete(db: Session, user_id: int, exercise: Exercise) -> None:
    """Record completion in Masar's existing UserProgress aggregate."""
    filters = [UserProgress.user_id == user_id]
    values: dict[str, Any] = {"user_id": user_id, "status": ProgressStatus.in_progress, "started_at": datetime.utcnow()}
    if exercise.tool_topic_id is not None:
        filters.append(UserProgress.tool_topic_id == exercise.tool_topic_id)
        values["tool_topic_id"] = exercise.tool_topic_id
    elif exercise.topic_id is not None:
        filters.append(UserProgress.topic_id == exercise.topic_id)
        values["topic_id"] = exercise.topic_id
    else:
        return
    progress = db.query(UserProgress).filter(*filters).first()
    if progress is None:
        progress = UserProgress(**values)
        db.add(progress)
        db.flush()
    completed = progress.exercises_completed or []
    if exercise.id not in completed:
        progress.exercises_completed = [*completed, exercise.id]

    if exercise.tool_topic_id is not None:
        total_lessons = db.query(Lesson).filter(Lesson.tool_topic_id == exercise.tool_topic_id).count()
        total_exercises = db.query(Exercise).filter(Exercise.tool_topic_id == exercise.tool_topic_id).count()
        if (len(progress.lessons_completed or []) >= total_lessons
                and len(progress.exercises_completed or []) >= total_exercises
                and (total_lessons or total_exercises)):
            progress.status = ProgressStatus.completed
            progress.completed_at = progress.completed_at or datetime.utcnow()
