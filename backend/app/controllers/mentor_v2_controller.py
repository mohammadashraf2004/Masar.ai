from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.mentor import learner_state
from app.services.mentor.observability import mentor_event
from app.services.mentor.v2.context import context_reference
from app.services.mentor.v2.plan import weekly_plan
from app.services.mentor.v2.message import is_live, scoped_session
from app.models.learning import Lesson
from app.services.billing.access_service import require_lesson_access
from app.services.mentor.v2.message import send_message
from app.services.mentor.v2.quiz import answer_quiz, block_for_reference
from app.views.mentor_v2 import MentorContextOut, MentorMessageIn, MentorMessageOut, QuizAnswerIn, QuizAnswerOut

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])


@router.get("/context", response_model=MentorContextOut)
def mentor_context(
    lesson_id: str | None = Query(None, alias="lessonId", pattern=r"^\d{1,9}$"),
    exercise_id: str | None = Query(None, alias="exerciseId", pattern=r"^\d{1,9}$"),
    language: str = Query("ar", pattern="^(ar|en)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return context_reference(
        db, current_user.id, lesson_id=lesson_id, exercise_id=exercise_id, language=language,
    )


@router.post("/message", response_model=MentorMessageOut)
@limiter.limit("20/minute")
def message(
    request: Request,
    payload: MentorMessageIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return send_message(db, current_user, payload)


@router.get("/quiz/{quiz_id}")
@limiter.limit("60/minute")
def quiz_question(
    request: Request,
    quiz_id: str = Path(..., pattern=r"^\d{1,9}:\d{1,4}$"),
    language: str = Query("ar", pattern="^(ar|en)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """The question a quiz block shows, in `language` - for a learner who switched language while
    it was on screen. Free, and it records nothing: it is the same question, not a new one."""
    return block_for_reference(db, current_user, quiz_id, language)


@router.post("/quiz/answer", response_model=QuizAnswerOut)
@limiter.limit("60/minute")
def quiz_answer(
    request: Request,
    payload: QuizAnswerIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return answer_quiz(db, current_user, payload)


@router.get("/plan")
@limiter.limit("30/minute")
def mentor_plan(
    request: Request,
    week_start: str = Query(..., alias="weekStart", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    variant: int = Query(0, ge=0, le=50),
    language: str = Query("ar", pattern="^(ar|en)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """The learner's weekly plan, from their enrolments and progress. Free: no model is called."""
    try:
        start = date.fromisoformat(week_start)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid weekStart")
    with mentor_event("weekly_plan", current_user.id) as event:
        plan = weekly_plan(db, current_user.id, start, variant, language)
        event.set(credits_charged=0, status=plan["status"],
                  blocks=sum(len(day["blocks"]) for day in plan["days"]))
        return plan


@router.get("/learner")
@limiter.limit("60/minute")
def mentor_learner(
    request: Request,
    language: str = Query("ar", pattern="^(ar|en)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """What the mentor knows about this learner: where they are, and their quiz-evidenced
    skills. Read from their own records only; empty when there is nothing yet."""
    try:
        reference = context_reference(db, current_user.id, language=language)
    except HTTPException:
        # The next lesson is one they cannot open: no position rather than a locked title.
        reference = {}
    skills = learner_state.skill_summaries(db, current_user.id)
    arabic = language == "ar"
    return {
        "position": {
            "track": learner_state.career_role(db, current_user.id, language) or "",
            "course": reference.get("courseTitle") or "",
            "lesson": reference.get("lessonTitle") or "",
            "courseId": reference.get("courseId"),
            "lessonId": reference.get("lessonId"),
        },
        "skills": [
            {
                "name": skill["name"],
                "status": skill["status"],
                "confidence": round(skill["confidence"] / 100, 2),
                "evidence": [
                    f"{skill['correct']} صحيحة من {skill['answers']} إجابة" if arabic
                    else f"{skill['correct']} of {skill['answers']} answers right"
                ],
            }
            for skill in skills
        ],
    }


@router.get("/thread")
@limiter.limit("60/minute")
def mentor_thread(
    request: Request,
    lesson_id: str | None = Query(None, alias="lessonId", pattern=r"^\d{1,9}$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """The conversation the mentor is continuing in this scope (the lesson, or general) - the
    same turns it sends the model as history - so another device shows what the mentor
    remembers. Only this learner's own sessions, only lessons they may open. Free."""
    if lesson_id:
        lesson = db.query(Lesson).filter(Lesson.id == int(lesson_id)).first()
        if lesson is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        require_lesson_access(db, current_user.id, lesson)
    key = f"lesson:{int(lesson_id)}" if lesson_id else "general"
    session = scoped_session(db, current_user.id, key)
    if session is None or not is_live(session, datetime.now(timezone.utc)):
        return {"messages": []}
    out = []
    for index, item in enumerate((session.messages or [])[-20:]):
        if not isinstance(item, dict):
            continue
        if item.get("role") == "user" and isinstance(item.get("content"), str):
            out.append({
                "id": f"s{session.id}-{index}", "role": "learner", "intent": item.get("intent"), "creditCost": 0,
                "blocks": [{"kind": "text", "text": item["content"], "grounding": "general"}],
            })
        elif item.get("role") == "assistant" and isinstance(item.get("blocks"), list):
            out.append({
                "id": f"s{session.id}-{index}", "role": "mentor", "creditCost": item.get("creditCost") or 0,
                "blocks": item["blocks"],
            })
    return {"messages": out}
