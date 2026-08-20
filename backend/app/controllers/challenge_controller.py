"""
backend/app/controllers/challenge_controller.py

Register in main.py:
    from app.controllers.challenge_controller import router as challenge_router
    app.include_router(challenge_router, prefix="/api/v1/challenges", tags=["Challenges"])
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import json

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.challenge import ChallengeProject, ChallengeAttempt, ChallengeStatus
from app.services.wallet.wallet_service import deduct_credits, get_or_create_wallet
from app.services import get_llm
from app.services.mentor.mentor_service import get_challenge_hint

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
    solution_code: str
    solution_notes: Optional[str] = None
    github_url: Optional[str] = None


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
    stuck_on: str
    previous_hints: list = []


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

    # Deduct credits
    wallet = get_or_create_wallet(current_user.id, db)
    if wallet.credit_balance < ch.credit_cost:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "message": f"This challenge costs {ch.credit_cost} credits. You have {wallet.credit_balance}.",
                "credits_needed": ch.credit_cost,
                "credits_available": wallet.credit_balance,
            }
        )

    wallet.credit_balance -= ch.credit_cost
    wallet.lifetime_spent += ch.credit_cost

    from app.models.wallet import WalletTransaction, TransactionType, TransactionStatus
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.deduction,
        status=TransactionStatus.confirmed,
        credits=-ch.credit_cost,
        description=f"Enrolled in challenge: {ch.title}",
        action_type="challenge_enroll",
        balance_after=wallet.credit_balance,
    )
    db.add(tx)

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

    return {
        "message": f"Enrolled successfully! {ch.credit_cost} credits deducted.",
        "attempt_id": attempt.id,
        "credits_remaining": wallet.credit_balance,
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

    return JSONResponse(
        content=ch.dirty_dataset,
        headers={"Content-Disposition": f'attachment; filename="{ch.dataset_filename}"'},
    )


@router.post("/{slug}/submit", response_model=SubmissionResult)
def submit_solution(
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
def get_hint(
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

    # Deduct 1 credit per hint
    from app.services.wallet.wallet_service import get_or_create_wallet
    from app.models.wallet import WalletTransaction, TransactionType, TransactionStatus
    wallet = get_or_create_wallet(current_user.id, db)
    if wallet.credit_balance < 1:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "message": "You need 1 credit for a hint.",
                "credits_needed": 1,
                "credits_available": 0,
            }
        )
    wallet.credit_balance -= 1
    wallet.lifetime_spent += 1
    tx = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.deduction,
        status=TransactionStatus.confirmed,
        credits=-1,
        description=f"AI hint: {ch.title}",
        action_type="challenge_hint",
        balance_after=wallet.credit_balance,
    )
    db.add(tx)
    db.commit()

    result = get_challenge_hint(
        llm=get_llm(),
        challenge_title=ch.title,
        challenge_difficulty=ch.difficulty.value,
        rubric=ch.grading_rubric,
        dirty_dataset_sample=ch.dirty_dataset[:3],
        stuck_on=payload.stuck_on,
        hints_already_given=payload.previous_hints,
    )
    return HintResponse(**result)