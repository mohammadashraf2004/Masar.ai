"""A learner's practice activity per day, from records that carry a time.

Counted: code-exercise runs and checks, quiz and exam attempts, project
submissions, and Project Lab runs and submissions. Reading a lesson is not
timestamped anywhere, so it cannot be counted; the profile labels this as
practice activity for that reason.
"""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models.code_exercise import CodeExerciseAttempt
from app.models.exam import ExamAttempt
from app.models.progress import ProjectSubmission, QuizAttempt
from app.models.project_lab import LabAttempt, LabRun, LabSubmission

MAX_DAYS = 371  # a year of weeks


def _timestamps(db: Session, user_id: int, since: datetime) -> list[datetime]:
    queries = [
        db.query(CodeExerciseAttempt.created_at).filter(
            CodeExerciseAttempt.user_id == user_id, CodeExerciseAttempt.created_at >= since),
        db.query(QuizAttempt.attempted_at).filter(
            QuizAttempt.user_id == user_id, QuizAttempt.attempted_at >= since),
        db.query(ExamAttempt.submitted_at).filter(
            ExamAttempt.user_id == user_id, ExamAttempt.submitted_at >= since),
        db.query(ProjectSubmission.submitted_at).filter(
            ProjectSubmission.user_id == user_id, ProjectSubmission.submitted_at >= since),
        db.query(LabRun.created_at).join(LabAttempt, LabRun.attempt_id == LabAttempt.id).filter(
            LabAttempt.user_id == user_id, LabRun.created_at >= since),
        db.query(LabSubmission.created_at).join(LabAttempt, LabSubmission.attempt_id == LabAttempt.id).filter(
            LabAttempt.user_id == user_id, LabSubmission.created_at >= since),
    ]
    return [row[0] for query in queries for row in query.all() if row[0] is not None]


def daily_activity(
    db: Session, user_id: int, *, days: int = 84, tz_offset_minutes: int = 0, now: datetime | None = None,
) -> dict[str, Any]:
    """Counts per local day for the last `days` days (oldest first), how many
    of them were active, and the current streak of consecutive active days.

    `tz_offset_minutes` is the browser's `Date.getTimezoneOffset()` (minutes
    *behind* UTC, so Cairo in summer is -180). A streak still counts when
    today has no activity yet, as long as yesterday did.
    """
    days = max(1, min(int(days), MAX_DAYS))
    shift = timedelta(minutes=-int(tz_offset_minutes))
    now = now or datetime.now(timezone.utc)
    today = (now + shift).date()
    first = today - timedelta(days=days - 1)
    # A day of margin either side of the window covers any timezone.
    since = datetime.combine(first - timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)

    counts: Counter[date] = Counter()
    for moment in _timestamps(db, user_id, since):
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        local_day = (moment.astimezone(timezone.utc) + shift).date()
        if first <= local_day <= today:
            counts[local_day] += 1

    window = [first + timedelta(days=i) for i in range(days)]
    streak = 0
    cursor = today if counts[today] else today - timedelta(days=1)
    while cursor >= first and counts[cursor]:
        streak += 1
        cursor -= timedelta(days=1)
    return {
        "days": [{"date": day.isoformat(), "count": counts[day]} for day in window],
        "active_days": sum(1 for day in window if counts[day]),
        "current_streak": streak,
    }
