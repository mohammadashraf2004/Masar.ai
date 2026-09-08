import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.user import User
from app.models.progress import MentorSession, UserSkillScore
from app.views.mentor import (
    MentorMessage, MentorResponse,
    MentorSessionResponse,
    CodeReviewRequest, CodeReviewResponse,
    SkillGapRequest, SkillGapResponse,
    MockInterviewRequest, MockInterviewResponse,
)
from app.core.limiter import limiter
from app.core.security import get_current_user
from app.services import (
    get_llm,
    mentor_service,
    code_review_service,
    skill_gap_service,
    interview_service,
    roadmap_service,
)
from app.services.wallet.wallet_service import deduct_credits, refund_credits

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])

# The credit wallet is the primary control on AI spend here (every handler
# below calls deduct_credits first). These limits are the second one: they
# bound *concurrency and burst*, which credits do not — a scripted client
# with a topped-up wallet could otherwise open hundreds of simultaneous
# provider calls and exhaust our rate budget with the upstream vendor.


@router.post("/chat", response_model=MentorResponse)
@limiter.limit("20/minute")
def chat_with_mentor(
    request: Request,
    payload: MentorMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ── Deduct credits before calling LLM ─────────────────────────────────────
    deduct_credits(current_user.id, "mentor_chat", db)

    session = (
        db.query(MentorSession)
        .filter(MentorSession.user_id == current_user.id)
        .order_by(MentorSession.updated_at.desc())
        .first()
    )
    if not session:
        session = MentorSession(
            user_id=current_user.id,
            title=payload.content[:50],
            context_topic_id=payload.topic_id,
            messages=[],
        )
        db.add(session)
        db.flush()

    history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in (session.messages or [])[-10:]
    ]
    user_context = {
        "name": current_user.full_name,
        "experience_level": current_user.experience_level,
        "readiness_score": current_user.overall_readiness_score,
    }

    llm = get_llm()
    reply, suggested_actions = mentor_service.get_mentor_reply(
        llm=llm,
        conversation_history=history,
        user_message=payload.content,
        user_context=user_context,
        language=payload.language,
        terminology_mode=payload.terminology_mode,
    )

    new_messages = list(session.messages or [])
    new_messages.append({"role": "user", "content": payload.content, "timestamp": datetime.utcnow().isoformat()})
    new_messages.append({"role": "assistant", "content": reply, "timestamp": datetime.utcnow().isoformat()})
    session.messages = new_messages
    session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(session)

    return MentorResponse(session_id=session.id, reply=reply, suggested_actions=suggested_actions)


@router.post("/new-session", response_model=MentorSessionResponse)
def new_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = MentorSession(user_id=current_user.id, title="New Session", messages=[])
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=List[MentorSessionResponse])
def list_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(MentorSession)
        .filter(MentorSession.user_id == current_user.id)
        .order_by(MentorSession.updated_at.desc())
        .limit(20)
        .all()
    )


@router.get("/sessions/{session_id}", response_model=MentorSessionResponse)
def get_session(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(MentorSession).filter(
        MentorSession.id == session_id,
        MentorSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/code-review", response_model=CodeReviewResponse)
@limiter.limit("10/minute")
def review_code(
    request: Request,
    payload: CodeReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deduct_credits(current_user.id, "code_review", db)
    result = code_review_service.review_code(
        llm=get_llm(), code=payload.code, language=payload.language, context=payload.context,
    )
    return CodeReviewResponse(**result)


@router.post("/skill-gap", response_model=SkillGapResponse)
@limiter.limit("6/minute")
def analyze_skill_gap(
    request: Request,
    payload: SkillGapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deduct_credits(current_user.id, "skill_gap", db)
    result = skill_gap_service.analyze_skill_gap(
        llm=get_llm(),
        target_role=payload.target_role,
        current_skills=payload.current_skills,
        cv_text=payload.cv_text,
        github_url=payload.github_url,
    )
    if result.get("readiness_score") is not None:
        current_user.overall_readiness_score = float(result["readiness_score"])
        db.commit()
    return SkillGapResponse(**result)


@router.post("/mock-interview", response_model=MockInterviewResponse)
@limiter.limit("15/minute")
def mock_interview(
    request: Request,
    payload: MockInterviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deduct_credits(current_user.id, "mock_interview", db)
    result = interview_service.generate_question(
        llm=get_llm(), topic=payload.topic, difficulty=payload.difficulty, previous_qa=payload.previous_qa,
    )
    return MockInterviewResponse(**result)


@router.get("/roadmap")
@limiter.limit("6/minute")
def get_roadmap(
    request: Request,
    track: str = Query("AI Engineer", max_length=120),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Charged before the call, as every handler here does. What follows is
    # the other half of that bargain: the deduction commits immediately, so
    # if generation then fails the student has paid for nothing. Without the
    # refund below, a provider outage silently bills every user who asks.
    deduct_credits(current_user.id, "roadmap", db)

    def _refund(why: str) -> None:
        """Reverse the charge above. Used by both failure paths: a provider
        that raised, and a provider that returned something unusable — the
        student is equally empty-handed either way."""
        try:
            refund_credits(
                current_user.id, "roadmap", db,
                reason=f"Refund: roadmap generation failed ({track})",
            )
        except Exception:
            # The charge stands and we could not reverse it. Loud, because
            # this is the one path that leaves a user out of pocket and only
            # the log will say so.
            logger.critical(
                "roadmap refund FAILED after %s; user is owed credits", why,
                extra={"user_id": current_user.id, "action": "roadmap"},
            )

    # Deliberately identical for every failure: the client is told the
    # roadmap is unavailable and that the credits came back, never why the
    # provider misbehaved.
    UNAVAILABLE = "Roadmap generation is unavailable right now. Your credits were refunded."

    weak_skills = [s.skill_name for s in current_user.skill_scores if s.score < 50]
    try:
        weeks = roadmap_service.generate_roadmap(
            llm=get_llm(), track=track,
            experience_level=current_user.experience_level,
            weak_skills=weak_skills,
        )
    except Exception:
        # Only reached when generation itself failed. An insufficient-credits
        # 402 is raised by deduct_credits above, outside this block, so it
        # can never be "refunded" — there was no deduction to reverse.
        logger.exception(
            "roadmap generation failed; refunding the credits",
            extra={"user_id": current_user.id, "track": track},
        )
        _refund("a provider exception")
        raise HTTPException(status_code=503, detail=UNAVAILABLE)

    if not weeks:
        # The provider answered, but with nothing we can show: no parseable
        # week array, or one whose entries were all unusable. Returning
        # `{"weeks": []}` with a 200 here is what silently billed students
        # for a blank plan — a success status for a non-result.
        logger.warning(
            "roadmap generation produced no usable weeks; refunding the credits",
            extra={"user_id": current_user.id, "track": track},
        )
        _refund("an unusable roadmap")
        raise HTTPException(status_code=503, detail=UNAVAILABLE)

    return {"track": track, "weeks": weeks}


@router.get("/skill-scores")
def get_skill_scores(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scores = db.query(UserSkillScore).filter(UserSkillScore.user_id == current_user.id).all()
    return {
        "readiness_score": current_user.overall_readiness_score,
        "skills": [{"skill": s.skill_name, "score": s.score} for s in scores],
    }
