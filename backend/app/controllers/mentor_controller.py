from fastapi import APIRouter, Depends, HTTPException
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
from app.core.security import get_current_user
from app.services import (
    get_llm,
    mentor_service,
    code_review_service,
    skill_gap_service,
    interview_service,
    roadmap_service,
)

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])


@router.post("/chat", response_model=MentorResponse)
def chat_with_mentor(
    payload: MentorMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
def review_code(payload: CodeReviewRequest, current_user: User = Depends(get_current_user)):
    result = code_review_service.review_code(
        llm=get_llm(), code=payload.code, language=payload.language, context=payload.context,
    )
    return CodeReviewResponse(**result)


@router.post("/skill-gap", response_model=SkillGapResponse)
def analyze_skill_gap(
    payload: SkillGapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
def mock_interview(payload: MockInterviewRequest, current_user: User = Depends(get_current_user)):
    result = interview_service.generate_question(
        llm=get_llm(), topic=payload.topic, difficulty=payload.difficulty, previous_qa=payload.previous_qa,
    )
    return MockInterviewResponse(**result)


@router.get("/roadmap")
def get_roadmap(track: str = "AI Engineer", current_user: User = Depends(get_current_user)):
    weak_skills = [s.skill_name for s in current_user.skill_scores if s.score < 50]
    weeks = roadmap_service.generate_roadmap(
        llm=get_llm(), track=track,
        experience_level=current_user.experience_level,
        weak_skills=weak_skills,
    )
    return {"track": track, "weeks": weeks}


@router.get("/skill-scores")
def get_skill_scores(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scores = db.query(UserSkillScore).filter(UserSkillScore.user_id == current_user.id).all()
    return {
        "readiness_score": current_user.overall_readiness_score,
        "skills": [{"skill": s.skill_name, "score": s.score} for s in scores],
    }
