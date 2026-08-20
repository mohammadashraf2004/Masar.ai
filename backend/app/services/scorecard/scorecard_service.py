"""
backend/app/services/scorecard/scorecard_service.py

Computes the Engineer Scorecard by aggregating real activity data:
  - Exam attempts & certificates  → certification metrics
  - Mentor sessions               → latency & token metrics
  - Project submissions           → code quality & avg score
  - Quiz attempts                 → quiz pass rate
  - UserProgress                  → study time

Call compute_scorecard(user_id, db) to rebuild and persist the scorecard.
"""
import statistics
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.progress import (
    EngineerScorecard, UserSkillScore,
    MentorSession, ProjectSubmission, QuizAttempt, UserProgress,
)
from app.models.exam import ExamAttempt, Certificate


# ── Grade thresholds ──────────────────────────────────────────────────────────
def _compute_grade(overall: float, hire_ready: bool) -> str:
    if overall >= 92:
        return "A+"
    if overall >= 85:
        return "A"
    if overall >= 78:
        return "B+"
    if overall >= 70:
        return "B"
    if overall >= 60:
        return "C"
    return "D"


def _safe_mean(values: list) -> Optional[float]:
    vals = [v for v in values if v is not None]
    return statistics.mean(vals) if vals else None


def _safe_percentile(values: list, pct: float) -> Optional[float]:
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    idx = int(len(vals) * pct / 100)
    return vals[min(idx, len(vals) - 1)]


# ── Cost estimation (based on approximate token pricing) ─────────────────────
# Using gpt-4o pricing as baseline: ~$0.005 / 1K tokens (blended in/out)
COST_PER_TOKEN = 0.000005


def compute_scorecard(user_id: int, db: Session) -> EngineerScorecard:
    """Recompute the full scorecard for a user and persist it."""

    # ── Fetch raw data (graceful fallback if table doesn't exist yet) ─────────
    def safe_query(model, uid):
        try:
            return db.query(model).filter(model.user_id == uid).all()
        except Exception:
            db.rollback()
            return []

    exam_attempts = safe_query(ExamAttempt, user_id)
    certificates  = safe_query(Certificate, user_id)
    sessions      = safe_query(MentorSession, user_id)
    submissions   = safe_query(ProjectSubmission, user_id)
    quiz_attempts = safe_query(QuizAttempt, user_id)
    progress_recs = safe_query(UserProgress, user_id)

    # ── Certification ─────────────────────────────────────────────────────────
    certs_earned   = len(certificates)
    exams_attempted = len(exam_attempts)
    passed_count   = sum(1 for a in exam_attempts if a.passed)
    exam_pass_rate = (passed_count / exams_attempted * 100) if exams_attempted else None

    # ── Mentor session metrics ────────────────────────────────────────────────
    # Pull latency from messages if stored per-message, else fall back to session avg
    all_latencies: list[float] = []
    all_tokens: list[int] = []

    for s in sessions:
        if s.avg_latency_ms:
            all_latencies.append(s.avg_latency_ms)
        else:
            # Try to extract from messages list
            for msg in (s.messages or []):
                if isinstance(msg, dict) and msg.get("latency_ms"):
                    all_latencies.append(float(msg["latency_ms"]))
        if s.total_tokens:
            all_tokens.append(s.total_tokens)

    # ── Project submission metrics ────────────────────────────────────────────
    project_scores = [s.score for s in submissions if s.score is not None]
    avg_project_score = _safe_mean(project_scores)

    proj_latencies = [s.review_latency_ms for s in submissions if s.review_latency_ms]
    all_latencies.extend(proj_latencies)

    proj_tokens = [s.review_tokens_used for s in submissions if s.review_tokens_used]
    all_tokens.extend(proj_tokens)

    # Code quality: parse from ai_review JSON if present
    code_quality_scores: list[float] = []
    for sub in submissions:
        if sub.ai_review and isinstance(sub.ai_review, dict):
            cq = sub.ai_review.get("quality_score") or sub.ai_review.get("score")
            if cq is not None:
                try:
                    code_quality_scores.append(float(cq))
                except (ValueError, TypeError):
                    pass
    code_quality_score = _safe_mean(code_quality_scores)

    # ── Quiz metrics ──────────────────────────────────────────────────────────
    quizzes_passed = sum(1 for q in quiz_attempts if q.passed)

    # ── Study time ────────────────────────────────────────────────────────────
    total_study_minutes = sum(p.time_spent_minutes or 0 for p in progress_recs)

    # ── Latency & cost aggregations ───────────────────────────────────────────
    avg_latency_ms = _safe_mean(all_latencies)
    p95_latency_ms = _safe_percentile(all_latencies, 95)

    total_tokens_used = sum(all_tokens)
    # Cost per 1K requests: estimate assuming avg ~500 tokens per request
    total_requests = len(sessions) + len(submissions)
    cost_per_1k_requests = (
        (total_tokens_used * COST_PER_TOKEN / total_requests * 1000)
        if total_requests and total_tokens_used
        else None
    )

    # ── Quality metrics: pull from skill scores if available ──────────────────
    skill_scores = db.query(UserSkillScore).filter(UserSkillScore.user_id == user_id).all()

    hallucination_vals = [s.hallucination_rate for s in skill_scores if s.hallucination_rate is not None]
    hallucination_rate = _safe_mean(hallucination_vals)

    retrieval_vals = [s.retrieval_precision for s in skill_scores if s.retrieval_precision is not None]
    retrieval_precision = _safe_mean(retrieval_vals)

    # ── Overall score for grading ─────────────────────────────────────────────
    # Weighted average of what we have
    grade_components: list[float] = []
    if exam_pass_rate is not None:
        grade_components.append(exam_pass_rate * 0.30)
    if avg_project_score is not None:
        grade_components.append(avg_project_score * 0.30)
    if code_quality_score is not None:
        grade_components.append(code_quality_score * 0.20)
    # Quiz performance
    total_quizzes = len(quiz_attempts)
    if total_quizzes:
        quiz_rate = quizzes_passed / total_quizzes * 100
        grade_components.append(quiz_rate * 0.20)

    overall = sum(grade_components) / (sum([
        0.30 if exam_pass_rate is not None else 0,
        0.30 if avg_project_score is not None else 0,
        0.20 if code_quality_score is not None else 0,
        0.20 if total_quizzes else 0,
    ]) or 1)

    # Hire-ready: at least 1 cert + avg project score ≥ 70 + overall ≥ 75
    hire_ready = (
        certs_earned >= 1
        and (avg_project_score or 0) >= 70
        and overall >= 75
    )

    overall_grade = _compute_grade(overall, hire_ready)

    # ── Upsert scorecard ──────────────────────────────────────────────────────
    scorecard = db.query(EngineerScorecard).filter(
        EngineerScorecard.user_id == user_id
    ).first()

    if not scorecard:
        scorecard = EngineerScorecard(user_id=user_id)
        db.add(scorecard)

    scorecard.certs_earned          = certs_earned
    scorecard.exams_attempted       = exams_attempted
    scorecard.exam_pass_rate        = exam_pass_rate
    scorecard.avg_latency_ms        = avg_latency_ms
    scorecard.p95_latency_ms        = p95_latency_ms
    scorecard.cost_per_1k_requests  = cost_per_1k_requests
    scorecard.total_tokens_used     = total_tokens_used
    scorecard.hallucination_rate    = hallucination_rate
    scorecard.retrieval_precision   = retrieval_precision
    scorecard.code_quality_score    = code_quality_score
    scorecard.avg_project_score     = avg_project_score
    scorecard.projects_submitted    = len(submissions)
    scorecard.quizzes_passed        = quizzes_passed
    scorecard.mentor_sessions_count = len(sessions)
    scorecard.total_study_minutes   = total_study_minutes
    scorecard.overall_grade         = overall_grade
    scorecard.hire_ready            = hire_ready
    scorecard.last_computed_at      = datetime.now(timezone.utc)

    db.commit()
    db.refresh(scorecard)
    return scorecard
