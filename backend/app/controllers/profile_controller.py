"""
backend/app/controllers/profile_controller.py

Adds scorecard endpoint on top of existing auth routes.
Register in main.py:
    from app.controllers.profile_controller import router as profile_router
    app.include_router(profile_router, prefix="/api/v1/profile", tags=["profile"])
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.progress import EngineerScorecard
from app.services.scorecard.scorecard_service import compute_scorecard
from pydantic import BaseModel

router = APIRouter()


# ── Response schema ───────────────────────────────────────────────────────────
class ScorecardResponse(BaseModel):
    # Certification
    certs_earned: int
    exams_attempted: int
    exam_pass_rate: Optional[float]

    # Performance
    avg_latency_ms: Optional[float]
    p95_latency_ms: Optional[float]
    cost_per_1k_requests: Optional[float]
    total_tokens_used: int

    # Quality
    hallucination_rate: Optional[float]
    retrieval_precision: Optional[float]
    code_quality_score: Optional[float]
    avg_project_score: Optional[float]

    # Activity
    projects_submitted: int
    quizzes_passed: int
    mentor_sessions_count: int
    total_study_minutes: int

    # Summary
    overall_grade: Optional[str]
    hire_ready: bool
    last_computed_at: Optional[str]

    class Config:
        from_attributes = True


@router.get("/scorecard", response_model=ScorecardResponse)
async def get_scorecard(
    refresh: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns the engineer scorecard for the current user.
    Pass ?refresh=true to recompute from latest activity.
    Otherwise returns cached version if available.
    """
    scorecard = db.query(EngineerScorecard).filter(
        EngineerScorecard.user_id == current_user.id
    ).first()

    if not scorecard or refresh:
        scorecard = compute_scorecard(current_user.id, db)

    return ScorecardResponse(
        certs_earned=scorecard.certs_earned or 0,
        exams_attempted=scorecard.exams_attempted or 0,
        exam_pass_rate=scorecard.exam_pass_rate,
        avg_latency_ms=scorecard.avg_latency_ms,
        p95_latency_ms=scorecard.p95_latency_ms,
        cost_per_1k_requests=scorecard.cost_per_1k_requests,
        total_tokens_used=scorecard.total_tokens_used or 0,
        hallucination_rate=scorecard.hallucination_rate,
        retrieval_precision=scorecard.retrieval_precision,
        code_quality_score=scorecard.code_quality_score,
        avg_project_score=scorecard.avg_project_score,
        projects_submitted=scorecard.projects_submitted or 0,
        quizzes_passed=scorecard.quizzes_passed or 0,
        mentor_sessions_count=scorecard.mentor_sessions_count or 0,
        total_study_minutes=scorecard.total_study_minutes or 0,
        overall_grade=scorecard.overall_grade,
        hire_ready=scorecard.hire_ready or False,
        last_computed_at=scorecard.last_computed_at.isoformat() if scorecard.last_computed_at else None,
    )