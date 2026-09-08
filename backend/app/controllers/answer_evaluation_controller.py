"""
backend/app/controllers/answer_evaluation_controller.py

Conversational, LLM-graded answers for exercises and open-ended quiz
questions — shared between career-track and tool-course content, since
Exercise/Quiz rows are the same tables either way (only topic_id vs
tool_topic_id differs, which this controller never needs to look at).
"""
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.learning import Exercise, Quiz, Topic
from app.models.tool_course import ToolTopic
from app.models.answer_submission import AnswerSubmission
from app.views.answer_submission import AnswerMessage, AnswerSubmissionResponse
from app.core.security import get_current_user
from app.core.limiter import limiter
from app.services import get_llm, answer_evaluator_service
from app.services.content.vocabulary_service import promote_from_correct_answer
from app.services.wallet.wallet_service import deduct_credits, refund_credits

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/practice", tags=["Answer Evaluation"])

# Both handlers charge this before calling the provider.
CHARGE_ACTION = "exercise_feedback"

# Deliberately identical for every failure: the student is told grading is
# unavailable and that the credits came back, never why the provider
# misbehaved. Same contract as GET /mentor/roadmap.
UNAVAILABLE = "Answer grading is unavailable right now. Your credits were refunded."


def _declared_terms(db: Session, content) -> list:
    """The terminology the content's parent topic says it teaches.

    A content row hangs off either a track Topic or a ToolTopic (never both
    — same convention as everywhere else in this codebase), and either kind
    can carry `technical_terms`. Detection from the text still runs on top of
    this, so a topic whose author left the field empty is not penalised.
    """
    if getattr(content, "topic_id", None):
        topic = db.query(Topic).filter(Topic.id == content.topic_id).first()
        return list(topic.technical_terms or []) if topic else []
    if getattr(content, "tool_topic_id", None):
        topic = db.query(ToolTopic).filter(ToolTopic.id == content.tool_topic_id).first()
        return list(topic.technical_terms or []) if topic else []
    return []


def _run_turn(
    db: Session,
    submission: AnswerSubmission,
    context: dict,
    payload: AnswerMessage,
) -> AnswerSubmission:
    user_message = payload.content
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in (submission.messages or [])[-10:]
    ]
    result = answer_evaluator_service.evaluate_answer(
        llm=get_llm(),
        context=context,
        conversation_history=history,
        user_message=user_message,
        language=payload.language,
        terminology_mode=payload.terminology_mode,
    )

    # answer_evaluator_service already degrades a malformed JSON response
    # into a plain-text reply, so an unparseable answer is still an answer
    # and still worth what the student paid. What is NOT worth paying for
    # is an empty one — the student would be charged for a blank turn. This
    # is the same line GET /mentor/roadmap draws at `if not weeks`, and
    # raising here routes it through the caller's single refund path.
    if not (result.get("reply") or "").strip():
        raise ValueError("evaluator returned an empty reply")

    new_messages = list(submission.messages or [])
    new_messages.append({"role": "user", "content": user_message, "timestamp": datetime.utcnow().isoformat()})
    new_messages.append({"role": "assistant", "content": result["reply"], "timestamp": datetime.utcnow().isoformat()})
    submission.messages = new_messages

    if result["is_correct"] is not None:
        submission.is_correct = result["is_correct"]
    if result["score"] is not None:
        submission.score = result["score"]

    if submission.is_correct:
        # The earned half of vocabulary progress: reading a lesson marks a
        # term "encountered", answering correctly about it marks it
        # "learned". Best-effort — a bookkeeping failure must not lose the
        # student's graded answer, which they paid credits for.
        try:
            promote_from_correct_answer(
                db,
                submission.user_id,
                context.get("title", ""),
                context.get("prompt", ""),
                declared=context.get("technical_terms"),
                commit=False,
            )
        except Exception:  # noqa: BLE001 — never fail the grading on this
            pass

    return submission


def _graded_turn(
    db: Session,
    user_id: int,
    submission: AnswerSubmission,
    context: dict,
    payload: AnswerMessage,
    what: str,
) -> AnswerSubmission:
    """Run one grading turn, reversing the charge if it does not land.

    The credits are taken before the provider call (never grade for free),
    and deduct_credits commits immediately — so a provider outage used to
    bill 2 credits per attempt and hand back a 500. This is the other half
    of that bargain, and follows the refund_credits pattern already used by
    GET /mentor/roadmap and POST /tracks/projects/{id}/hint rather than
    inventing a second mechanism.

    Not refunded, because no charge was made: a 402 from deduct_credits
    (raised by the caller, before this runs) and a 429 from the rate
    limiter (refused before the handler runs at all).
    """
    try:
        return _run_turn(db, submission, context, payload)
    except Exception:
        # Discard the half-written submission so the student is not left
        # with a turn recording a question that was never answered. The
        # deduction is already committed and is undone below, not here.
        db.rollback()
        logger.exception(
            "answer evaluation failed; refunding the credits",
            extra={"user_id": user_id, "what": what},
        )
        try:
            refund_credits(
                user_id, CHARGE_ACTION, db,
                reason=f"Refund: answer grading failed ({what})",
            )
        except Exception:
            # The charge stands and we could not reverse it. Loud, because
            # this is the one path that leaves a student out of pocket and
            # only the log will say so.
            logger.critical(
                "answer evaluation refund FAILED; user is owed credits",
                extra={"user_id": user_id, "action": CHARGE_ACTION},
            )
        raise HTTPException(status_code=503, detail=UNAVAILABLE)


# ─── Exercises ───────────────────────────────────────────────────────────

@router.post("/exercises/{exercise_id}/answer", response_model=AnswerSubmissionResponse)
@limiter.limit("20/minute")
def answer_exercise(
    request: Request,
    exercise_id: int,
    payload: AnswerMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    deduct_credits(current_user.id, CHARGE_ACTION, db)

    submission = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == current_user.id,
        AnswerSubmission.exercise_id == exercise_id,
    ).first()
    if not submission:
        submission = AnswerSubmission(user_id=current_user.id, exercise_id=exercise_id, messages=[])
        db.add(submission)
        db.flush()

    context = {
        "kind": "exercise",
        "title": exercise.title,
        "prompt": exercise.description,
        "starter_code": exercise.starter_code,
        "reference": exercise.solution_code,
        "skill_tags": exercise.skill_tested or [],
        "technical_terms": _declared_terms(db, exercise),
    }
    submission = _graded_turn(
        db, current_user.id, submission, context, payload,
        what=f"exercise {exercise_id}",
    )
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/exercises/{exercise_id}/answer", response_model=AnswerSubmissionResponse)
def get_exercise_answer(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    submission = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == current_user.id,
        AnswerSubmission.exercise_id == exercise_id,
    ).first()
    if not submission:
        raise HTTPException(status_code=404, detail="No conversation yet for this exercise")
    return submission


# ─── Open-ended quiz questions ────────────────────────────────────────────
# MCQ questions still grade instantly via POST /tracks/quizzes/{id}/submit —
# these two routes are only for questions marked "type": "open" in the
# quiz's `questions` JSON.

@router.post("/quizzes/{quiz_id}/questions/{question_index}/answer", response_model=AnswerSubmissionResponse)
@limiter.limit("20/minute")
def answer_quiz_question(
    request: Request,
    quiz_id: int,
    question_index: int,
    payload: AnswerMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if question_index < 0 or question_index >= len(quiz.questions or []):
        raise HTTPException(status_code=404, detail="Question not found")

    question = quiz.questions[question_index]
    if question.get("type", "mcq") != "open":
        raise HTTPException(status_code=400, detail="This question is multiple-choice — submit it via /tracks/quizzes/{id}/submit instead")

    deduct_credits(current_user.id, CHARGE_ACTION, db)

    submission = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == current_user.id,
        AnswerSubmission.quiz_id == quiz_id,
        AnswerSubmission.question_index == question_index,
    ).first()
    if not submission:
        submission = AnswerSubmission(
            user_id=current_user.id, quiz_id=quiz_id, question_index=question_index, messages=[],
        )
        db.add(submission)
        db.flush()

    context = {
        "kind": "quiz_question",
        "title": quiz.title,
        "prompt": question.get("question", ""),
        "reference": question.get("explanation"),
        "skill_tags": [],
        "technical_terms": _declared_terms(db, quiz),
    }
    submission = _graded_turn(
        db, current_user.id, submission, context, payload,
        what=f"quiz {quiz_id} question {question_index}",
    )
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/quizzes/{quiz_id}/questions/{question_index}/answer", response_model=AnswerSubmissionResponse)
def get_quiz_question_answer(
    quiz_id: int,
    question_index: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    submission = db.query(AnswerSubmission).filter(
        AnswerSubmission.user_id == current_user.id,
        AnswerSubmission.quiz_id == quiz_id,
        AnswerSubmission.question_index == question_index,
    ).first()
    if not submission:
        raise HTTPException(status_code=404, detail="No conversation yet for this question")
    return submission
