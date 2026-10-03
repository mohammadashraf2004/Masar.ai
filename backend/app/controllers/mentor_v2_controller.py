"""Mentor v2: POST /mentor/message and POST /mentor/quiz/answer.

/mentor/message
  * context is built on the server from lessonId/exerciseId and the
    learner's own records (see mentor_context); the body cannot supply
    progress, mastery or grades
  * intent: explicit > keyword rules > model (only when rules can't decide)
  * credits: the existing wallet. Charged before any provider call,
    refunded when the reply fails (provider error, or validation failed
    twice and a fallback was served). Proactive and rule-based replies
    cost 0.
  * history is stored in the existing mentor_sessions rows, the same ones
    /mentor/chat writes; v2 turns add `blocks` and `intent` to a message.

/mentor/quiz/answer
  * graded on the server against the authored key; the response never
    contains the correct option
  * each answer is evidence for a skill (skill_state); a wrong one is also
    the "recent mistake" later replies can bring up
  * free: no provider call
"""
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.learning import Lesson
from app.models.progress import MentorQuizAnswer, MentorSession
from app.models.user import User
from app.services import get_llm
from app.services.language.language_policy import normalize_language
from app.services.mentor import mentor_intent, mentor_quiz, mentor_v2_service, skill_state
from app.services.mentor.mentor_context import build_context, is_gradable, load_available_quiz, quiz_questions
from app.services.mentor.mentor_quiz import L
from app.services.wallet.wallet_service import CREDIT_COSTS, deduct_credits, refund_credits
from app.views.mentor_v2 import (
    MentorContextOut, MentorV2Message, MentorV2Response,
    QuizAnswerRequest, QuizAnswerResponse, SkillDelta,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])

ACTION = "mentor_chat"
UNAVAILABLE = "The mentor is unavailable right now. Your credits were refunded."


def _session_for(db: Session, user: User, session_id: Optional[int], title: str, topic_id) -> MentorSession:
    if session_id is not None:
        # Scoped to the caller: another learner's session id is a 404,
        # indistinguishable from one that doesn't exist.
        session = db.query(MentorSession).filter(
            MentorSession.id == session_id, MentorSession.user_id == user.id,
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    session = (
        db.query(MentorSession)
        .filter(MentorSession.user_id == user.id)
        .order_by(MentorSession.updated_at.desc().nullslast(), MentorSession.id.desc())
        .first()
    )
    if not session:
        session = MentorSession(user_id=user.id, title=title[:50] or "Mentor", context_topic_id=topic_id, messages=[])
        db.add(session)
        db.flush()
    return session


def _hint_level(session: MentorSession, exercise_id: Optional[int]) -> int:
    given = sum(
        1 for m in (session.messages or [])
        if m.get("role") == "assistant" and m.get("intent") == "hint" and m.get("exercise_id") == exercise_id
        and not m.get("fallback")
    )
    return min(given + 1, mentor_v2_service.MAX_HINT_LEVEL)


@router.post("/message", response_model=MentorV2Response)
@limiter.limit("20/minute")
def mentor_message(
    request: Request,
    payload: MentorV2Message,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    language = normalize_language(payload.language)
    query = "\n".join(p for p in (payload.content, payload.selection or "") if p and p.strip())

    ctx = build_context(
        db, current_user.id,
        lesson_id=payload.lesson_id, exercise_id=payload.exercise_id,
        query=query, language=language,
    )
    session = _session_for(
        db, current_user, payload.session_id, payload.content or (ctx.lesson_title or ""),
        ctx.lesson.topic_id if ctx.lesson is not None else None,
    )

    charged = False

    def charge():
        nonlocal charged
        if not charged:
            deduct_credits(current_user.id, ACTION, db)
            charged = True

    def refund(why: str):
        nonlocal charged
        if not charged:
            return
        try:
            refund_credits(current_user.id, ACTION, db, reason=f"Refund: mentor reply failed ({why})")
            charged = False
        except Exception:
            logger.critical("mentor v2 refund FAILED after %s; user is owed credits", why,
                            extra={"user_id": current_user.id, "action": ACTION})

    proactive = payload.trigger is not None
    blocks = None
    fallback = False

    if proactive:
        intent, source = "quiz", "trigger"
        blocks = _proactive_blocks(db, current_user.id, ctx)
    else:
        if mentor_intent.needs_model(payload.intent, query):
            # Classification is a provider call, so it is paid for like one.
            # If the result turns out to be a free, rule-based reply the
            # charge is reversed below.
            charge()
        intent, source = mentor_intent.resolve_intent(payload.intent, query, llm_factory=get_llm)

        if intent == "quiz" and ctx.has_course_context:
            picked = mentor_quiz.pick_question(db, current_user.id, ctx)
            if picked is not None:
                quiz, idx, q = picked
                blocks = [
                    {"kind": "text", "grounding": "lesson" if ctx.lesson is not None else "module",
                     "text": L(language, "سؤال سريع من هذه الوحدة:", "A quick question from this module:")},
                    mentor_quiz.quiz_block(quiz, idx, q, "lesson" if ctx.lesson is not None else "module"),
                ]
                refund("rule-based reply")

        if blocks is None:
            charge()
            hint_level = _hint_level(session, payload.exercise_id) if intent == "hint" else None
            try:
                blocks, fallback, violations = mentor_v2_service.generate_reply(
                    get_llm(), ctx,
                    intent=intent, text=payload.content, selection=payload.selection,
                    history=mentor_v2_service.history_for_model(session.messages),
                    hint_level=hint_level,
                    language=payload.language, terminology_mode=payload.terminology_mode,
                )
            except Exception:
                logger.exception("mentor v2 generation failed; refunding", extra={"user_id": current_user.id})
                refund("provider error")
                db.rollback()
                raise HTTPException(status_code=503, detail=UNAVAILABLE)
            if fallback:
                logger.warning("mentor v2 served a fallback after two failed validations: %s", violations,
                               extra={"user_id": current_user.id})
                refund("validation")

    now = datetime.utcnow().isoformat()
    messages = list(session.messages or [])
    if not proactive:
        messages.append({
            "role": "user", "content": query, "timestamp": now, "intent": intent,
            "lesson_id": payload.lesson_id, "exercise_id": payload.exercise_id,
        })
    messages.append({
        "role": "assistant", "content": mentor_v2_service.blocks_as_text(blocks), "timestamp": now,
        "v": 2, "intent": intent, "blocks": blocks, "proactive": proactive, "fallback": fallback,
        "lesson_id": payload.lesson_id, "exercise_id": payload.exercise_id,
    })
    session.messages = messages
    session.updated_at = datetime.utcnow()
    db.commit()

    return MentorV2Response(
        session_id=session.id,
        intent=intent,
        intent_source=source,
        proactive=proactive,
        blocks=blocks,
        credits_charged=CREDIT_COSTS[ACTION] if charged else 0,
        fallback=fallback,
        context=MentorContextOut(
            lesson_id=ctx.lesson.id if ctx.lesson is not None else None,
            lesson_title=ctx.lesson_title,
            module_title=ctx.module_title,
            exercise_id=ctx.exercise.id if ctx.exercise is not None else None,
            exercise_title=ctx.exercise_title,
        ),
    )


def _proactive_blocks(db: Session, user_id: int, ctx) -> list:
    lang = ctx.language
    title = ctx.lesson_title or ""
    intro = (
        L(lang, f"أحسنت — أنهيت «{title}». قبل الانتقال، سؤال سريع:", f"Nice work — you finished \"{title}\". A quick question before you move on:")
        if ctx.lesson_completed else
        L(lang, f"سؤال سريع على «{title}»:", f"A quick question on \"{title}\":")
    )
    blocks = [{"kind": "text", "grounding": "lesson", "text": intro}]
    picked = mentor_quiz.pick_question(db, user_id, ctx)
    if picked is not None:
        quiz, idx, q = picked
        blocks.append(mentor_quiz.quiz_block(quiz, idx, q, "lesson"))
    else:
        blocks.append({"kind": "check", "grounding": "lesson",
                       "text": L(lang, f"بجملة واحدة: ما أهم فكرة في «{title}»؟", f"In one sentence: what is the key idea of \"{title}\"?")})
    order = ctx.lesson.order if ctx.lesson is not None else None
    if order is not None and (order + 1) in ctx.module_lessons:
        blocks.append({"kind": "text", "grounding": "module",
                       "text": L(lang, f"التالي: الدرس {order + 1} — {ctx.module_lessons[order + 1]}",
                                 f"Next: lesson {order + 1} — {ctx.module_lessons[order + 1]}")})
    return blocks


@router.post("/quiz/answer", response_model=QuizAnswerResponse)
@limiter.limit("30/minute")
def mentor_quiz_answer(
    request: Request,
    payload: QuizAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    language = normalize_language(payload.language)
    quiz, topic = load_available_quiz(db, payload.quiz_id)
    questions = quiz_questions(quiz, language)
    if payload.question_index >= len(questions) or not is_gradable(questions[payload.question_index]):
        raise HTTPException(status_code=404, detail="Question not found")
    q = questions[payload.question_index]
    if payload.choice >= len(q["options"]):
        raise HTTPException(status_code=422, detail="choice is out of range")

    # Grade against the English key when the Arabic blob disagrees on it:
    # indices line up 1:1 by contract, and the original is authoritative.
    key_source = quiz.questions[payload.question_index] if isinstance(quiz.questions, list) else q
    correct_index = key_source.get("correct") if is_gradable(key_source) else q["correct"]
    is_correct = payload.choice == correct_index

    lesson = None
    if payload.lesson_id is not None:
        lesson = db.query(Lesson).filter(Lesson.id == payload.lesson_id).first()
        same_topic = lesson is not None and (
            (quiz.topic_id and lesson.topic_id == quiz.topic_id)
            or (quiz.tool_topic_id and lesson.tool_topic_id == quiz.tool_topic_id)
        )
        if not same_topic:
            lesson = None  # an unrelated lesson id is ignored, not trusted

    skill = mentor_quiz.skill_for(q, topic)
    db.add(MentorQuizAnswer(
        user_id=current_user.id,
        quiz_id=quiz.id,
        question_index=payload.question_index,
        lesson_id=lesson.id if lesson is not None else None,
        skill_name=skill,
        chosen_index=payload.choice,
        is_correct=is_correct,
        question_text=str(q.get("question", ""))[:500],
    ))
    db.flush()
    change = skill_state.apply_answer(db, current_user.id, skill, is_correct)

    if lesson is not None:
        lesson_texts = [(lesson.content_ar or lesson.content) if language == "ar" else (lesson.content or lesson.content_ar)]
        grounding = "lesson"
    else:
        lesson_texts = [
            ((l.content_ar or l.content) if language == "ar" else (l.content or l.content_ar)) or ""
            for l in (topic.lessons or [])
        ]
        grounding = "module"
    feedback = mentor_quiz.feedback_blocks(
        language, {**q, "correct": correct_index}, payload.choice, is_correct, lesson_texts, skill, grounding,
    )
    db.commit()

    return QuizAnswerResponse(
        correct=is_correct,
        feedback=feedback,
        skill_delta=SkillDelta(**change.__dict__) if change else None,
    )
