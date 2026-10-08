"""
Authored quiz questions as mentor blocks, and grading an answer to one.

A mentor quiz question is never invented here: it is a question a course author wrote,
taken from the quiz of the lesson's module. That is what makes it safe to grade on the
server (the author's `correct` index is the key) and free to serve (no model is called).

The key never leaves the server. A quiz block carries the question and its options; the
reply to an answer says whether it was right and, for a wrong one, asks a guiding question
instead of giving the way out.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.learning import Lesson, Quiz, Topic
from app.models.mentor_evidence import MentorEvidence
from app.models.tool_course import ToolTopic
from app.models.user import User
from app.core.authz import is_email_verified
from app.services.billing.access_service import require_content_access
from app.services.mentor.v2 import skills, translate
from app.views.mentor_v2 import QuizAnswerIn, QuizAnswerOut, SkillDeltaOut

_QUIZ_ID = re.compile(r"^(\d+):(\d+)$")


def option_id(index: int) -> str:
    return chr(ord("a") + index)


def option_index(option: str) -> int:
    return ord(option) - ord("a") if len(option) == 1 else -1


def make_quiz_id(quiz_id: int, index: int) -> str:
    return f"{quiz_id}:{index}"


def parse_quiz_id(raw: str) -> Tuple[int, int]:
    match = _QUIZ_ID.match(raw or "")
    if not match:
        raise HTTPException(status_code=422, detail="Invalid quiz id")
    return int(match.group(1)), int(match.group(2))


def _is_mcq(question: Any) -> bool:
    if not isinstance(question, dict) or question.get("type", "mcq") == "open":
        return False
    options = question.get("options")
    correct = question.get("correct")
    return (
        isinstance(options, list) and 2 <= len(options) <= 8
        and all(isinstance(o, str) and o.strip() for o in options)
        and isinstance(correct, int) and not isinstance(correct, bool) and 0 <= correct < len(options)
    )


def mcq_question(quiz: Quiz, index: int) -> Optional[Dict[str, Any]]:
    """The authored question at `index`, or None when it is missing, open-ended, or has no
    usable key. An ungradable question is never served, so it can never be a free mark."""
    questions = quiz.questions if isinstance(quiz.questions, list) else []
    if not 0 <= index < len(questions):
        return None
    question = questions[index]
    return question if _is_mcq(question) else None


def shown_question(quiz: Quiz, index: int, language: Optional[str]) -> Optional[Dict[str, Any]]:
    """What the learner reads: question, options and explanation, in the language asked for
    when the quiz has a twin that lines up 1:1 with the graded one, else the graded one."""
    base = mcq_question(quiz, index)
    if base is None:
        return None
    if language == "ar" and isinstance(quiz.questions_ar, list) and index < len(quiz.questions_ar):
        twin = quiz.questions_ar[index]
        if _is_mcq(twin) and len(twin["options"]) == len(base["options"]) and twin.get("question"):
            return twin
    return base


def localized_question(db: Session, quiz: Quiz, index: int, language: Optional[str],
                       *, may_call_model: bool = True) -> Optional[Tuple[Dict[str, Any], str]]:
    """What the learner reads, and the language it is really in. The authored question, its
    hand-written twin, or - when the quiz has neither in `language` - a cached translation, so
    the question follows the UI language. If no translation can be made, the authored text."""
    base = mcq_question(quiz, index)
    if base is None:
        return None
    return translate.localized(db, quiz, index, base, shown_question(quiz, index, language) or base, language,
                               may_call_model=may_call_model)


def quiz_block(db: Session, quiz: Quiz, index: int, language: Optional[str],
               *, may_call_model: bool = True) -> Optional[Dict[str, Any]]:
    """The block the learner answers. No key, no explanation. `lang` says which language the
    text is in, so a client that switches language knows to ask for it again."""
    picked = localized_question(db, quiz, index, language, may_call_model=may_call_model)
    if picked is None:
        return None
    shown, shown_language = picked
    return {
        "kind": "quiz",
        "quizId": make_quiz_id(quiz.id, index),
        "question": str(shown["question"]),
        "options": [{"id": option_id(i), "text": text} for i, text in enumerate(shown["options"])],
        "grounding": "lesson",
        "lang": shown_language,
    }


def block_for_reference(db: Session, user: User, raw_quiz_id: str, language: Optional[str]) -> Dict[str, Any]:
    """The same question as `raw_quiz_id` names, in `language`. Used when the learner switches
    language while a question is on screen: it is the same question, not a new one, so it costs
    nothing and records nothing."""
    quiz_id, index = parse_quiz_id(raw_quiz_id)
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    require_content_access(db, user.id, quiz)
    block = quiz_block(db, quiz, index, language if language in ("ar", "en") else "ar",
                       may_call_model=is_email_verified(user))
    if block is None:
        raise HTTPException(status_code=404, detail="Question not found")
    lesson = lesson_for_question(db, quiz, mcq_question(quiz, index) or {})
    if lesson is not None:
        block["sourceLessonId"] = str(lesson.id)
    return block


def correct_option_texts(quiz: Quiz) -> List[str]:
    """For the validation layer only: the texts the mentor must not hand over."""
    out: List[str] = []
    questions = quiz.questions if isinstance(quiz.questions, list) else []
    for index in range(len(questions)):
        question = mcq_question(quiz, index)
        if question is not None:
            out.append(question["options"][question["correct"]])
    return out


# ─── Which lesson / skill a question belongs to ─────────────────────────────

def module_of_quiz(db: Session, quiz: Quiz):
    if quiz.topic_id:
        return db.query(Topic).filter(Topic.id == quiz.topic_id).first()
    if quiz.tool_topic_id:
        return db.query(ToolTopic).filter(ToolTopic.id == quiz.tool_topic_id).first()
    return None


def lesson_for_question(db: Session, quiz: Quiz, question: Dict[str, Any]) -> Optional[Lesson]:
    """The lesson a question was written for: its `lesson_id` ('L004-001') is the tail of the
    lesson's source key ('COURSE-004/L004-001')."""
    tail = question.get("lesson_id")
    if not isinstance(tail, str) or not tail:
        return None
    query = db.query(Lesson).filter(Lesson.source_key.like(f"%/{tail}"))
    if quiz.topic_id:
        query = query.filter(Lesson.topic_id == quiz.topic_id)
    elif quiz.tool_topic_id:
        query = query.filter(Lesson.tool_topic_id == quiz.tool_topic_id)
    return query.first()


def skill_for_quiz(db: Session, quiz: Quiz) -> str:
    module = module_of_quiz(db, quiz)
    tags = [t for t in (getattr(module, "skill_tags", None) or []) if isinstance(t, str) and t.strip()]
    name = tags[0] if tags else (module.title if module else quiz.title)
    return str(name).strip()[:120]


def quizzes_of_module(db: Session, lesson: Lesson) -> List[Quiz]:
    if lesson.topic_id:
        query = db.query(Quiz).filter(Quiz.topic_id == lesson.topic_id)
    elif lesson.tool_topic_id:
        query = db.query(Quiz).filter(Quiz.tool_topic_id == lesson.tool_topic_id)
    else:
        return []
    return query.order_by(Quiz.id).all()


def pick_question(db: Session, user_id: int, lesson: Lesson) -> Optional[Tuple[Quiz, int]]:
    """A question for this learner on this lesson.

    The lesson's own questions come first, then the rest of its module's. Within a group a
    question the learner last got wrong comes before one they have never seen, which comes
    before one they have answered right - so the mentor asks about what is shaky."""
    quizzes = quizzes_of_module(db, lesson)
    if not quizzes:
        return None
    last = {}
    for row in (
        db.query(MentorEvidence)
        .filter(MentorEvidence.user_id == user_id, MentorEvidence.quiz_id.in_([q.id for q in quizzes]))
        .order_by(MentorEvidence.created_at, MentorEvidence.id)
        .all()
    ):
        last[(row.quiz_id, row.question_index)] = row.correct

    tail = (lesson.source_key or "").rsplit("/", 1)[-1]
    candidates: List[Tuple[int, int, Quiz, int]] = []
    for quiz in quizzes:
        questions = quiz.questions if isinstance(quiz.questions, list) else []
        for index, question in enumerate(questions):
            if not _is_mcq(question):
                continue
            own = 0 if (tail and question.get("lesson_id") == tail) else 1
            state = last.get((quiz.id, index))
            rank = 0 if state is False else 1 if state is None else 2
            candidates.append((own, rank, quiz, index))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1], c[2].id, c[3]))
    _, _, quiz, index = candidates[0]
    return quiz, index


# ─── Answering ──────────────────────────────────────────────────────────────

_COPY = {
    "ar": {
        "right": "صحيح — أحسنت.",
        "right_why": "صحيح. {explanation}",
        "guide": "قريب — لنفكّر معاً. أعد قراءة السؤال: «{question}». ما الذي يسأل عنه بالضبط، وأي خيار يتّسق مع ما شرحه الدرس عن {skill}؟",
        "guide_lesson": "ليس بعد — راجع قسم «{lesson}» من الدرس ثم عُد للسؤال: «{question}». ما الذي تغيّر في فهمك لـ {skill}؟",
        "small": "سؤال أصغر: لو شرحت {skill} لزميلك في جملة واحدة، ماذا ستقول؟ ثم اختر الخيار الأقرب لجملتك.",
    },
    "en": {
        "right": "Correct - well done.",
        "right_why": "Correct. {explanation}",
        "guide": "Close - let's think it through. Re-read the question: \"{question}\". What exactly is it asking, and which option fits what the lesson said about {skill}?",
        "guide_lesson": "Not yet - revisit the \"{lesson}\" section of the lesson, then come back to: \"{question}\". What changed in your understanding of {skill}?",
        "small": "A smaller question: if you explained {skill} to a teammate in one sentence, what would you say? Then pick the option closest to your sentence.",
    },
}


def answer_quiz(db: Session, user: User, payload: QuizAnswerIn) -> QuizAnswerOut:
    quiz_id, index = parse_quiz_id(payload.quizId)
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    require_content_access(db, user.id, quiz)

    graded = mcq_question(quiz, index)
    if graded is None:
        raise HTTPException(status_code=404, detail="Question not found")
    selected = option_index(payload.optionId)
    if not 0 <= selected < len(graded["options"]):
        raise HTTPException(status_code=422, detail="Unknown option")

    language = payload.language if payload.language in ("ar", "en") else "ar"
    copy = _COPY[language]
    shown, _ = localized_question(db, quiz, index, language) or (graded, language)
    correct = selected == graded["correct"]

    lesson = lesson_for_question(db, quiz, graded)
    skill = skill_for_quiz(db, quiz)
    previous = skills.evidence_rows(db, user.id, skill)
    recent_wrong = sum(1 for r in previous[-3:] if not r.correct)

    change = skills.record_answer(
        db, user_id=user.id, skill=skill, correct=correct, quiz_id=quiz.id, question_index=index,
        lesson_id=lesson.id if lesson else None, selected=selected,
    )
    db.commit()

    source = {"sourceLessonId": str(lesson.id)} if lesson else {}
    if correct:
        explanation = str(shown.get("explanation") or "").strip()
        text = copy["right_why"].format(explanation=explanation) if explanation else copy["right"]
        feedback: List[Dict[str, Any]] = [{"kind": "text", "text": text, "grounding": "lesson" if lesson else "general", **source}]
    else:
        # Never the way out: a guiding question about the question itself, then a smaller one.
        # A second miss in a row on the same skill points back at the lesson's own section.
        lesson_title = (lesson.title_ar if language == "ar" and lesson and lesson.title_ar else lesson.title) if lesson else None
        guide = copy["guide_lesson"] if (recent_wrong >= 1 and lesson_title) else copy["guide"]
        feedback = [
            {"kind": "text", "grounding": "lesson" if lesson else "general", **source,
             "text": guide.format(question=str(shown["question"]), skill=skill, lesson=lesson_title or "")},
            {"kind": "check", "grounding": "lesson" if lesson else "general", **source,
             "question": copy["small"].format(skill=skill)},
        ]

    delta = (
        SkillDeltaOut(skill=change.skill, **{"from": change.before}, to=change.after, status=change.status)
        if change else None
    )
    return QuizAnswerOut(correct=correct, feedback=feedback, skillDelta=delta)
