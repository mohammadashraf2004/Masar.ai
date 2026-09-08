"""
backend/app/controllers/admin_analytics_controller.py

Admin product analytics — deliberately two read-only endpoints, no more.

    GET /admin/analytics/overview        aggregates only, no user identities
    GET /admin/analytics/users/{id}      one learner's summary, audited

Design rules this module sticks to, because an analytics dashboard is the
easiest place in an app to accidentally build a second, weaker API:

  * Authorization is `require_admin` (app/core/authz.py) — the same
    dependency every other admin route uses. No inline role comparison,
    no `?user_id=` ever consulted for *who is asking*, only for *who is
    being looked at*, and only after the admin check has passed.
  * Every number is computed by the database (COUNT/SUM/GROUP BY). No
    endpoint here loads a result set into Python to count it, and every
    list response has a hard LIMIT.
  * Operational metrics (latency, request rate, token counts) are
    Prometheus' job and stay there. This is product analytics only.
  * A metric that cannot be computed honestly from the current schema is
    reported as unavailable with a reason, never approximated.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import case, distinct, func
from sqlalchemy.orm import Session

from app.core import security_log
from app.core.authz import require_admin
from app.core.config import settings
from app.db.session import get_db
from app.models.exam import Certificate, ExamAttempt
from app.models.learning import Topic
from app.models.progress import (
    MentorSession, ProgressStatus, ProjectSubmission, QuizAttempt, UserProgress,
)
from app.models.tool_course import ToolTopic
from app.models.user import User
from app.models.wallet import TransactionType, UserWallet, WalletTransaction

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])

# Top-N caps. The dashboard shows a leaderboard, not a catalogue dump —
# and `action_type` is a free-form string column, so its cardinality is
# bounded by this LIMIT rather than by anything the schema guarantees.
TOP_TOPICS = 10
MAX_FEATURES = 20

# Why retention is not computed here. Retention needs to know when a user
# came *back*, and nothing in this schema records that: `users` has no
# last_login/last_seen column, there is no session or refresh-token table,
# and the login path writes nothing to the database (see auth_controller —
# it emits a security log line and returns a JWT). The only timestamps
# available belong to write-actions (a quiz submitted, credits spent), so
# a "D7 retention" built from them would silently report a floor, not a
# rate: every user who logged in, read three lessons and left would count
# as churned. A wrong 42% is worse than an honest gap, so this stays
# unavailable until a real activity signal exists.
RETENTION_UNAVAILABLE_REASON = (
    "No login or last-seen timestamps exist in the schema; only write-actions "
    "are timestamped, which would undercount returning users."
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _json_len(col):
    """Element count of a JSON array column; 0 for NULL or any non-array.

    `user_progress.lessons_completed` / `.exercises_completed` are JSON
    lists appended to by the progress endpoints. Postgres' json_array_length
    raises on a non-array value, which would turn one malformed legacy row
    into a 500 for the whole dashboard — so the type is checked first.
    """
    return case(
        (func.json_typeof(col) == "array", func.json_array_length(col)),
        else_=0,
    )


def _iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    # Most columns here are timezone-aware, but a couple of write paths use
    # datetime.utcnow(); normalising keeps sorting and output consistent.
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def _sort_key(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _verification_is_reliable() -> bool:
    """`is_verified` only means something if verification emails are
    actually delivered. Without RESEND_API_KEY the sender logs and returns
    (services/email/resend_service.py), so the flag reflects the mail
    configuration, not user intent. Reported, but flagged."""
    return bool(settings.RESEND_API_KEY)


# ─── Response schemas ─────────────────────────────────────────────────────────

class TopicCount(BaseModel):
    topic: str
    count: int


class UsersBlock(BaseModel):
    total: int
    # Calendar day, 00:00 UTC onward. The 7/30-day figures are rolling
    # windows ending now — stated here because "new users today" and
    # "new users in 7 days" are otherwise easy to read as the same shape.
    new_today: int
    new_last_7_days: int
    new_last_30_days: int
    verified: int
    verification_reliable: bool
    verification_note: Optional[str] = None


class ActivationBlock(BaseModel):
    """Funnel stages, each defined against data that already exists:

    signed_up              — rows in `users`.
    verified               — users.is_verified (see verification_reliable).
    started_learning       — distinct users with >=1 `user_progress` row. A
                             progress row is only ever created by a POST to
                             a topic progress endpoint (tracks_controller /
                             tool_courses_controller), so it means the user
                             actually worked through content, not merely
                             enrolled in a track.
    completed_first_lesson — distinct users with >=1 progress row whose
                             `lessons_completed` array is non-empty.
    """
    signed_up: int
    verified: int
    verification_reliable: bool
    started_learning: int
    completed_first_lesson: int


class LearningBlock(BaseModel):
    lessons_completed: int
    exercises_completed: int
    most_started_topics: List[TopicCount]
    most_completed_topics: List[TopicCount]


class AiUsageBlock(BaseModel):
    """Sourced from `wallet_transactions`, which is the authoritative
    record: every AI action deducts credits through wallet_service and
    writes one deduction row carrying its `action_type`."""
    total_credits_burned: int
    credits_by_feature: Dict[str, int]


class RetentionBlock(BaseModel):
    available: bool
    reason: Optional[str] = None
    d1: Optional[float] = None
    d7: Optional[float] = None
    d30: Optional[float] = None


class AnalyticsOverview(BaseModel):
    generated_at: str
    users: UsersBlock
    activation: ActivationBlock
    learning: LearningBlock
    ai_usage: AiUsageBlock
    retention: RetentionBlock


class ActivityItem(BaseModel):
    type: str
    at: str
    detail: str


class UserAnalytics(BaseModel):
    user_id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    verification_reliable: bool
    signed_up_at: Optional[str] = None
    overall_readiness_score: Optional[float] = None

    topics_started: int
    topics_completed: int
    lessons_completed: int
    exercises_completed: int
    study_minutes: int

    quiz_attempts: int
    quizzes_passed: int
    projects_submitted: int
    projects_reviewed: int
    exam_attempts: int
    exams_passed: int
    certificates: int

    credits_spent: int
    credits_by_feature: Dict[str, int]

    recent_activity: List[ActivityItem]


# ─── Overview ─────────────────────────────────────────────────────────────────

@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Aggregate product metrics for the admin dashboard.

    Read-only and identity-free: nothing in this response names, counts
    down to, or otherwise singles out an individual user. Six aggregate
    queries, each a single pass with the work done in the database.
    """
    now = datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 1. Users — one pass, four windows, via aggregate FILTER.
    total, new_today, new_7d, new_30d, verified = db.query(
        func.count(User.id),
        func.count(User.id).filter(User.created_at >= midnight),
        func.count(User.id).filter(User.created_at >= now - timedelta(days=7)),
        func.count(User.id).filter(User.created_at >= now - timedelta(days=30)),
        func.count(User.id).filter(User.is_verified.is_(True)),
    ).one()

    # 2. Progress — one pass over user_progress gives both funnel stages
    #    below signup and both learning totals.
    lessons_len = _json_len(UserProgress.lessons_completed)
    exercises_len = _json_len(UserProgress.exercises_completed)
    started_learning, completed_first_lesson, lessons_done, exercises_done = db.query(
        func.count(distinct(UserProgress.user_id)),
        func.count(distinct(case((lessons_len > 0, UserProgress.user_id)))),
        func.coalesce(func.sum(lessons_len), 0),
        func.coalesce(func.sum(exercises_len), 0),
    ).one()

    # 3+4. Topic leaderboards. A progress row points at either a career-track
    #      topic or a tool-course topic (never both), so the title comes from
    #      whichever join matched.
    title = func.coalesce(Topic.title, ToolTopic.title)

    def _topic_leaderboard(completed_only: bool) -> List[TopicCount]:
        q = (
            db.query(title.label("topic"), func.count(UserProgress.id).label("count"))
            .select_from(UserProgress)
            .outerjoin(Topic, Topic.id == UserProgress.topic_id)
            .outerjoin(ToolTopic, ToolTopic.id == UserProgress.tool_topic_id)
            .filter(title.isnot(None))
        )
        if completed_only:
            q = q.filter(UserProgress.status == ProgressStatus.completed)
        rows = (
            q.group_by(title)
            .order_by(func.count(UserProgress.id).desc(), title.asc())
            .limit(TOP_TOPICS)
            .all()
        )
        return [TopicCount(topic=r.topic, count=r.count) for r in rows]

    # 5+6. AI credit burn. Deductions store `credits` negative, so the
    #      burn is the negated sum. The total is computed over every
    #      deduction, not summed from the truncated breakdown below.
    is_deduction = WalletTransaction.transaction_type == TransactionType.deduction
    burned = db.query(
        func.coalesce(func.sum(-WalletTransaction.credits), 0)
    ).filter(is_deduction).scalar()

    feature_rows = (
        db.query(
            WalletTransaction.action_type,
            func.coalesce(func.sum(-WalletTransaction.credits), 0).label("credits"),
        )
        .filter(is_deduction, WalletTransaction.action_type.isnot(None))
        .group_by(WalletTransaction.action_type)
        .order_by(func.sum(-WalletTransaction.credits).desc())
        .limit(MAX_FEATURES)
        .all()
    )

    reliable = _verification_is_reliable()
    return AnalyticsOverview(
        generated_at=now.isoformat(),
        users=UsersBlock(
            total=total,
            new_today=new_today,
            new_last_7_days=new_7d,
            new_last_30_days=new_30d,
            verified=verified,
            verification_reliable=reliable,
            verification_note=None if reliable else (
                "Verification email delivery is not configured (RESEND_API_KEY "
                "is unset), so is_verified does not reflect user behaviour."
            ),
        ),
        activation=ActivationBlock(
            signed_up=total,
            verified=verified,
            verification_reliable=reliable,
            started_learning=started_learning,
            completed_first_lesson=completed_first_lesson,
        ),
        learning=LearningBlock(
            lessons_completed=lessons_done,
            exercises_completed=exercises_done,
            most_started_topics=_topic_leaderboard(completed_only=False),
            most_completed_topics=_topic_leaderboard(completed_only=True),
        ),
        ai_usage=AiUsageBlock(
            total_credits_burned=burned,
            credits_by_feature={r.action_type: int(r.credits) for r in feature_rows},
        ),
        retention=RetentionBlock(available=False, reason=RETENTION_UNAVAILABLE_REASON),
    )


# ─── User drill-down ──────────────────────────────────────────────────────────

@router.get("/users/{user_id}", response_model=UserAnalytics)
def user_analytics(
    user_id: int,
    limit: int = Query(20, ge=1, le=50, description="Recent activity rows to return"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """One learner's summary. Admin-only, read-only, bounded, and audited.

    `user_id` selects *who is looked at*; it has no bearing on *who is
    allowed to look* — that is settled by require_admin before this body
    runs. Reading an individual's learning record is privileged, so the
    access is written to the security log the same way every other admin
    action in this codebase is.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Logged here, before the reads: the audit trail should record the
    # access even if a later query fails.
    security_log.admin_action(
        admin_id=admin.id, action="analytics.view_user", target=f"user={user_id}",
    )

    lessons_len = _json_len(UserProgress.lessons_completed)
    exercises_len = _json_len(UserProgress.exercises_completed)
    topics_started, topics_completed, lessons_done, exercises_done, minutes = db.query(
        func.count(UserProgress.id),
        func.count(UserProgress.id).filter(UserProgress.status == ProgressStatus.completed),
        func.coalesce(func.sum(lessons_len), 0),
        func.coalesce(func.sum(exercises_len), 0),
        func.coalesce(func.sum(UserProgress.time_spent_minutes), 0),
    ).filter(UserProgress.user_id == user_id).one()

    quiz_total, quiz_passed = db.query(
        func.count(QuizAttempt.id),
        func.count(QuizAttempt.id).filter(QuizAttempt.passed.is_(True)),
    ).filter(QuizAttempt.user_id == user_id).one()

    projects_total, projects_reviewed = db.query(
        func.count(ProjectSubmission.id),
        func.count(ProjectSubmission.id).filter(ProjectSubmission.reviewed_at.isnot(None)),
    ).filter(ProjectSubmission.user_id == user_id).one()

    exams_total, exams_passed = db.query(
        func.count(ExamAttempt.id),
        func.count(ExamAttempt.id).filter(ExamAttempt.passed.is_(True)),
    ).filter(ExamAttempt.user_id == user_id).one()

    certs = db.query(func.count(Certificate.id)).filter(
        Certificate.user_id == user_id
    ).scalar()

    # AI spend for this user, joined through their wallet.
    def _spend_query(*entities):
        return (
            db.query(*entities)
            .select_from(WalletTransaction)
            .join(UserWallet, WalletTransaction.wallet_id == UserWallet.id)
            .filter(
                UserWallet.user_id == user_id,
                WalletTransaction.transaction_type == TransactionType.deduction,
            )
        )

    credits_spent = _spend_query(
        func.coalesce(func.sum(-WalletTransaction.credits), 0)
    ).scalar()

    feature_rows = (
        _spend_query(
            WalletTransaction.action_type,
            func.coalesce(func.sum(-WalletTransaction.credits), 0).label("credits"),
        )
        .filter(WalletTransaction.action_type.isnot(None))
        .group_by(WalletTransaction.action_type)
        .order_by(func.sum(-WalletTransaction.credits).desc())
        .limit(MAX_FEATURES)
        .all()
    )

    # Recent activity: one bounded query per source, merged in memory.
    # Each source returns at most `limit` rows, so the merge is over at
    # most 5 * limit records regardless of how much history a user has.
    events: List[tuple] = []

    for at, score in db.query(QuizAttempt.attempted_at, QuizAttempt.score).filter(
        QuizAttempt.user_id == user_id, QuizAttempt.attempted_at.isnot(None)
    ).order_by(QuizAttempt.attempted_at.desc()).limit(limit).all():
        events.append((at, "quiz_attempt", f"scored {score:.0f}%"))

    for at, score in db.query(ProjectSubmission.submitted_at, ProjectSubmission.score).filter(
        ProjectSubmission.user_id == user_id, ProjectSubmission.submitted_at.isnot(None)
    ).order_by(ProjectSubmission.submitted_at.desc()).limit(limit).all():
        events.append((at, "project_submission",
                       "submitted" if score is None else f"submitted, scored {score:.0f}"))

    for at, status in db.query(ExamAttempt.started_at, ExamAttempt.status).filter(
        ExamAttempt.user_id == user_id, ExamAttempt.started_at.isnot(None)
    ).order_by(ExamAttempt.started_at.desc()).limit(limit).all():
        events.append((at, "exam_attempt", getattr(status, "value", str(status))))

    for (at,) in db.query(MentorSession.created_at).filter(
        MentorSession.user_id == user_id, MentorSession.created_at.isnot(None)
    ).order_by(MentorSession.created_at.desc()).limit(limit).all():
        # The session title is user-written free text and adds nothing an
        # admin needs here, so it is left out of this audit-adjacent view.
        events.append((at, "mentor_session", "AI mentor session"))

    for at, action, credits in _spend_query(
        WalletTransaction.created_at, WalletTransaction.action_type, WalletTransaction.credits,
    ).filter(WalletTransaction.created_at.isnot(None)).order_by(
        WalletTransaction.created_at.desc()
    ).limit(limit).all():
        events.append((at, "ai_usage", f"{action or 'unknown'} ({-credits} credits)"))

    events.sort(key=lambda e: _sort_key(e[0]), reverse=True)

    return UserAnalytics(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=getattr(user.role, "value", str(user.role)),
        is_active=bool(user.is_active),
        is_verified=bool(user.is_verified),
        verification_reliable=_verification_is_reliable(),
        signed_up_at=_iso(user.created_at),
        overall_readiness_score=user.overall_readiness_score,
        topics_started=topics_started,
        topics_completed=topics_completed,
        lessons_completed=lessons_done,
        exercises_completed=exercises_done,
        study_minutes=minutes,
        quiz_attempts=quiz_total,
        quizzes_passed=quiz_passed,
        projects_submitted=projects_total,
        projects_reviewed=projects_reviewed,
        exam_attempts=exams_total,
        exams_passed=exams_passed,
        certificates=certs,
        credits_spent=credits_spent,
        credits_by_feature={r.action_type: int(r.credits) for r in feature_rows},
        recent_activity=[
            ActivityItem(type=kind, at=_iso(at), detail=detail)
            for at, kind, detail in events[:limit]
        ],
    )
