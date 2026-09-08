"""
backend/app/controllers/challenge_controller.py

Register in main.py:
    from app.controllers.challenge_controller import router as challenge_router
    app.include_router(challenge_router, prefix="/api/v1/challenges", tags=["Challenges"])
"""
import logging
import re

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
import json

from app.db.session import get_db
from app.core.limiter import limiter
from app.core.security import get_current_user
from app.models.user import User
from app.models.challenge import ChallengeProject, ChallengeAttempt, ChallengeStatus
from app.services.wallet.wallet_service import deduct_credits, refund_credits
from app.services import get_llm
from app.services.mentor.mentor_service import get_challenge_hint
from app.views.auth import MAX_URL_LENGTH, validate_public_url

logger = logging.getLogger(__name__)

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────
class ChallengeListItem(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    credit_cost: int
    passing_score: float
    description: str
    tags: list
    is_enrolled: bool = False
    best_score: Optional[float] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


class ChallengeDetail(ChallengeListItem):
    dataset_description: str
    dataset_filename: str
    dirty_dataset: list
    grading_rubric: list
    hints: list
    max_attempts: int
    attempts_used: int = 0


class SubmitSolutionRequest(BaseModel):
    # solution_code is pasted into the grading prompt; cap it the same way
    # every other LLM-facing field is capped.
    solution_code: str = Field(..., min_length=1, max_length=50_000)
    solution_notes: Optional[str] = Field(None, max_length=10_000)
    github_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)

    @field_validator("github_url", mode="after")
    @classmethod
    def _safe_url(cls, v: Optional[str]) -> Optional[str]:
        return validate_public_url(v)


class GradeFeedbackItem(BaseModel):
    criterion: str
    weight: int
    score: float
    feedback: str
    passed: bool


class SubmissionResult(BaseModel):
    attempt_id: int
    score: float
    passed: bool
    feedback: List[GradeFeedbackItem]
    overall_feedback: str




class HintRequest(BaseModel):
    stuck_on: str = Field(..., min_length=1, max_length=2_000)
    previous_hints: list = Field(default_factory=list, max_length=20)
    # Same language settings the mentor chat takes — a hint follows the same
    # rules as every other AI response: Arabic explanation, English terms,
    # untouched code. Pattern-bounded; anything else falls back to the
    # Arabic-first default in language_policy.py.
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    terminology_mode: Optional[str] = Field(
        None, pattern="^(arabic_first|industry|english_technical)$"
    )


class HintResponse(BaseModel):
    hint: str
    concept: str
    next_step: str

# ── AI Grader ─────────────────────────────────────────────────────────────────
def grade_submission(challenge: ChallengeProject, solution_code: str, solution_notes: str, llm) -> dict:
    """Use LLM to grade a challenge submission against the rubric."""
    rubric_text = "\n".join([
        f"- {r['criterion']} ({r['weight']}% weight): {r['description']}"
        for r in challenge.grading_rubric
    ])

    prompt = f"""You are a senior AI engineer grading a student's data pipeline solution.

CHALLENGE: {challenge.title}
DIFFICULTY: {challenge.difficulty}

GRADING RUBRIC:
{rubric_text}

STUDENT'S SOLUTION CODE:
```python
{solution_code[:3000]}
```

STUDENT'S NOTES:
{solution_notes or 'No notes provided'}

DIRTY DATASET SAMPLE (first 3 records):
{json.dumps(challenge.dirty_dataset[:3], ensure_ascii=False, indent=2)}

Grade each criterion on a scale of 0-100. Be strict but fair.
Return ONLY a JSON object with this exact structure:
{{
  "criteria_scores": [
    {{
      "criterion": "criterion name exactly as in rubric",
      "score": 0-100,
      "feedback": "specific feedback on what they did well or poorly",
      "passed": true/false
    }}
  ],
  "overall_feedback": "2-3 sentences of overall feedback",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"]
}}"""

    try:
        response = llm.generate(prompt)
        # Strip markdown code fences if present
        text = response.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text.strip())
        return result
    except Exception as e:
        # Fallback grade if LLM fails
        return {
            "criteria_scores": [
                {"criterion": r["criterion"], "score": 50, "feedback": "Auto-graded (LLM unavailable)", "passed": False}
                for r in challenge.grading_rubric
            ],
            "overall_feedback": "Automatic grading applied due to system error. Please contact support.",
            "strengths": [],
            "improvements": ["Resubmit for proper grading"],
        }


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ChallengeListItem])
def list_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    challenges = db.query(ChallengeProject).filter(ChallengeProject.is_active == True).all()

    # Get user's attempts for status enrichment
    user_attempts = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id
    ).all()
    attempt_map = {a.challenge_id: a for a in user_attempts}

    result = []
    for ch in challenges:
        attempt = attempt_map.get(ch.id)
        result.append(ChallengeListItem(
            id=ch.id, title=ch.title, slug=ch.slug,
            difficulty=ch.difficulty.value, credit_cost=ch.credit_cost,
            passing_score=ch.passing_score, description=ch.description,
            tags=ch.tags or [],
            is_enrolled=attempt is not None,
            best_score=attempt.score if attempt else None,
            status=attempt.status.value if attempt else None,
        ))
    return result


@router.get("/{slug}", response_model=ChallengeDetail)
def get_challenge(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ch = db.query(ChallengeProject).filter(
        ChallengeProject.slug == slug,
        ChallengeProject.is_active == True,
    ).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).order_by(ChallengeAttempt.enrolled_at.desc()).first()

    attempts_used = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).count()

    # Only expose dataset if enrolled
    dataset = ch.dirty_dataset if attempt else []
    hints   = ch.hints if attempt else []

    return ChallengeDetail(
        id=ch.id, title=ch.title, slug=ch.slug,
        difficulty=ch.difficulty.value, credit_cost=ch.credit_cost,
        passing_score=ch.passing_score, description=ch.description,
        tags=ch.tags or [],
        dataset_description=ch.dataset_description or "",
        dataset_filename=ch.dataset_filename,
        dirty_dataset=dataset,
        grading_rubric=ch.grading_rubric,
        hints=hints,
        max_attempts=ch.max_attempts,
        attempts_used=attempts_used,
        is_enrolled=attempt is not None,
        best_score=attempt.score if attempt else None,
        status=attempt.status.value if attempt else None,
    )


@router.post("/{slug}/enroll")
def enroll_challenge(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ch = db.query(ChallengeProject).filter(
        ChallengeProject.slug == slug,
        ChallengeProject.is_active == True,
    ).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Check max attempts
    attempts_used = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).count()
    if attempts_used >= ch.max_attempts:
        raise HTTPException(status_code=400, detail=f"Maximum {ch.max_attempts} attempts reached")

    # Check existing active enrollment
    active = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
        ChallengeAttempt.status == ChallengeStatus.enrolled,
    ).first()
    if active:
        raise HTTPException(status_code=400, detail="Already enrolled in this challenge")

    # Charge through the wallet service rather than adjusting the row here.
    # An inline deduction skipped the SELECT ... FOR UPDATE row lock, the
    # lazy promo-expiry check and the promo-balance decrement, so enrolling
    # left `promo_credits_remaining` overstated (and expiry then clawed
    # back purchased credits), and already-expired promo credits stayed
    # spendable through this route. The price is unchanged — it still comes
    # from the challenge row, passed as an explicit cost because it varies
    # per challenge and so has no entry in CREDIT_COSTS.
    #
    # Raises 402 with the standard insufficient_credits payload; the wording
    # of `message` differs from the old bespoke one, but the fields the
    # client actually renders (error, credits_needed, credits_available)
    # are the same.
    charge = deduct_credits(
        current_user.id, "challenge_enroll", db,
        cost=ch.credit_cost,
        description=f"Enrolled in challenge: {ch.title}",
    )

    # deduct_credits commits, so the enrolment row can no longer share the
    # deduction's transaction the way the inline version did. If creating it
    # fails, the student has paid for an enrolment they did not get — so put
    # the credits back, the same way the roadmap and hint paths do.
    try:
        attempt = ChallengeAttempt(
            user_id=current_user.id,
            challenge_id=ch.id,
            status=ChallengeStatus.enrolled,
            attempt_number=attempts_used + 1,
            credits_spent=ch.credit_cost,
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
    except Exception:
        db.rollback()
        logger.exception(
            "challenge enrolment failed after charging; refunding",
            extra={"user_id": current_user.id, "challenge_id": ch.id},
        )
        try:
            refund_credits(
                current_user.id, "challenge_enroll", db,
                reason=f"Refund: enrolment failed for {ch.title}",
                cost=ch.credit_cost,
            )
        except Exception:
            # The charge stands and we could not reverse it. Loud, because
            # this is the one path that leaves a user out of pocket and
            # only the log will say so. Same handling as the roadmap path.
            logger.critical(
                "challenge enrolment refund FAILED; user is owed credits",
                extra={"user_id": current_user.id, "action": "challenge_enroll"},
            )
        raise HTTPException(
            status_code=503,
            detail="Could not start this challenge right now. Your credits were refunded.",
        )

    return {
        "message": f"Enrolled successfully! {ch.credit_cost} credits deducted.",
        "attempt_id": attempt.id,
        "credits_remaining": charge["balance_after"],
        "dataset_unlocked": True,
    }


@router.get("/{slug}/dataset/download")
def download_dataset(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download the dirty dataset as a JSON file (enrolled users only)."""
    ch = db.query(ChallengeProject).filter(ChallengeProject.slug == slug).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=403, detail="Enroll in this challenge to download the dataset")

    # dataset_filename comes out of the database and is interpolated into
    # a response header. A value containing a quote or a CR/LF would break
    # out of the header (response-splitting); one containing a path would
    # steer where a naive client writes the file. Reduce it to a bare,
    # safe basename before it goes anywhere near the header.
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", (ch.dataset_filename or "dataset.json").rsplit("/", 1)[-1])[:100]
    return JSONResponse(
        content=ch.dirty_dataset,
        headers={"Content-Disposition": f'attachment; filename="{safe_name}"'},
    )


@router.post("/{slug}/submit", response_model=SubmissionResult)
@limiter.limit("10/hour")
def submit_solution(
    request: Request,
    slug: str,
    payload: SubmitSolutionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ch = db.query(ChallengeProject).filter(ChallengeProject.slug == slug).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
        ChallengeAttempt.status == ChallengeStatus.enrolled,
    ).order_by(ChallengeAttempt.enrolled_at.desc()).first()
    if not attempt:
        raise HTTPException(status_code=400, detail="Not enrolled in this challenge or already submitted")

    # Grade with AI
    llm = get_llm()
    grade_result = grade_submission(ch, payload.solution_code, payload.solution_notes or "", llm)

    # Calculate weighted score
    criteria_scores = grade_result.get("criteria_scores", [])
    rubric_map = {r["criterion"]: r["weight"] for r in ch.grading_rubric}
    total_weight = sum(rubric_map.values())
    weighted_score = 0.0
    feedback_items = []

    for cs in criteria_scores:
        weight = rubric_map.get(cs["criterion"], 10)
        weighted_score += (cs["score"] / 100) * weight
        feedback_items.append(GradeFeedbackItem(
            criterion=cs["criterion"],
            weight=weight,
            score=cs["score"],
            feedback=cs["feedback"],
            passed=cs["passed"],
        ))

    final_score = (weighted_score / total_weight) * 100
    passed = final_score >= ch.passing_score

    # Update attempt
    attempt.solution_code  = payload.solution_code
    attempt.solution_notes = payload.solution_notes
    attempt.github_url     = payload.github_url
    attempt.score          = final_score
    attempt.passed         = passed
    attempt.status         = ChallengeStatus.passed if passed else ChallengeStatus.failed
    attempt.ai_feedback    = grade_result.get("criteria_scores", [])
    attempt.submitted_at   = datetime.now(timezone.utc)
    attempt.graded_at      = datetime.now(timezone.utc)

    db.commit()

    return SubmissionResult(
        attempt_id=attempt.id,
        score=round(final_score, 1),
        passed=passed,
        feedback=feedback_items,
        overall_feedback=grade_result.get("overall_feedback", ""),
    )


@router.get("/{slug}/attempts")
def get_my_attempts(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ch = db.query(ChallengeProject).filter(ChallengeProject.slug == slug).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempts = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).order_by(ChallengeAttempt.enrolled_at.desc()).all()

    return [
        {
            "id": a.id,
            "attempt_number": a.attempt_number,
            "status": a.status.value,
            "score": a.score,
            "passed": a.passed,
            "enrolled_at": a.enrolled_at.isoformat() if a.enrolled_at else None,
            "submitted_at": a.submitted_at.isoformat() if a.submitted_at else None,
        }
        for a in attempts
    ]

@router.post("/{slug}/hint", response_model=HintResponse)
@limiter.limit("20/hour")
def get_hint(
    request: Request,
    slug: str,
    payload: HintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get an AI Socratic hint for a challenge (costs 1 credit). Must be enrolled."""
    ch = db.query(ChallengeProject).filter(
        ChallengeProject.slug == slug,
        ChallengeProject.is_active == True,
    ).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=403, detail="Enroll in this challenge to get AI hints")

    # 1 credit per hint, unchanged — the price now lives in CREDIT_COSTS
    # under "challenge_hint" instead of being written out here, so this
    # goes through the same locked, promo-aware path as every other AI
    # spend. Adjusting the wallet inline (as this did) bypassed the promo
    # accounting entirely and let expired promo credits buy hints.
    deduct_credits(current_user.id, "challenge_hint", db)

    # The charge above commits immediately, so everything that can still
    # fail has to give it back. That includes building the response, not
    # just the provider call: HintResponse requires three string fields,
    # and a model that returns a non-string for one of them raises a
    # validation error *after* the student has paid — a charged 500.
    try:
        result = get_challenge_hint(
            llm=get_llm(),
            challenge_title=ch.title,
            challenge_difficulty=ch.difficulty.value,
            rubric=ch.grading_rubric,
            dirty_dataset_sample=ch.dirty_dataset[:3],
            stuck_on=payload.stuck_on,
            hints_already_given=payload.previous_hints,
            language=payload.language,
            terminology_mode=payload.terminology_mode,
        )
        response = HintResponse(**result)
    except Exception:
        logger.exception(
            "challenge hint failed after charging; refunding",
            extra={"user_id": current_user.id, "challenge_id": ch.id},
        )
        try:
            refund_credits(
                current_user.id, "challenge_hint", db,
                reason=f"Refund: hint unavailable for {ch.title}",
            )
        except Exception:
            # The charge stands and we could not reverse it. Loud, because
            # this is the one path that leaves a user out of pocket and
            # only the log will say so. Same handling as the enrolment path.
            logger.critical(
                "challenge hint refund FAILED; user is owed credits",
                extra={"user_id": current_user.id, "action": "challenge_hint"},
            )
        raise HTTPException(
            status_code=503,
            detail="Hints are unavailable right now. Your credits were refunded.",
        )

    return response