"""Mentor quiz questions: picking one, and the feedback after an answer.

No LLM call happens here, which is why these turns are free. A question
always comes from an authored Quiz, so its key is real and grading is a
server-side comparison. The client never receives the correct option, not
in the question and not in the feedback. A wrong answer gets a guiding
question and a smaller follow-up question, never the answer.
"""
import re
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.learning import Quiz
from app.models.progress import MentorQuizAnswer
from app.services.mentor.mentor_context import MentorContext, is_gradable, quiz_questions
from app.services.mentor.mentor_text import split_chunks, squash, token_set, tokens


def L(lang: str, ar: str, en: str) -> str:
    return ar if lang == "ar" else en


def pick_question(db: Session, user_id: int, ctx: MentorContext) -> Optional[Tuple[Quiz, int, dict]]:
    """First gradable question in this module the learner has not yet
    answered correctly; the first gradable one if they have done them all."""
    candidates = []
    for quiz in ctx.quizzes:
        for i, q in enumerate(quiz_questions(quiz, ctx.language)):
            if is_gradable(q):
                candidates.append((quiz, i, q))
    if not candidates:
        return None
    done = {
        (r.quiz_id, r.question_index)
        for r in db.query(MentorQuizAnswer.quiz_id, MentorQuizAnswer.question_index).filter(
            MentorQuizAnswer.user_id == user_id,
            MentorQuizAnswer.is_correct == True,  # noqa: E712
            MentorQuizAnswer.quiz_id.in_([q.id for q in ctx.quizzes]),
        )
    }
    for c in candidates:
        if (c[0].id, c[1]) not in done:
            return c
    return candidates[0]


def quiz_block(quiz: Quiz, index: int, q: dict, grounding: str) -> dict:
    # Built field by field from the authored question: `correct` and
    # `explanation` are never copied, so they cannot leak by serialisation.
    return {
        "kind": "quiz",
        "grounding": grounding,
        "quiz": {
            "quizId": quiz.id,
            "questionIndex": index,
            "question": str(q.get("question", "")),
            "options": [str(o) for o in q["options"]],
        },
    }


def skill_for(q: dict, topic) -> str:
    if isinstance(q.get("skill"), str) and q["skill"].strip():
        return q["skill"].strip()[:120]
    tags = getattr(topic, "skill_tags", None) or []
    if tags and isinstance(tags[0], str):
        return tags[0][:120]
    return (getattr(topic, "title", None) or "general")[:120]


_TERM = re.compile(r"[A-Za-z][A-Za-z0-9_.]*[A-Za-z0-9_]")


def _key_term(question: str, fallback: str) -> str:
    """The most specific English technical term in the stem: identifiers
    (thread_id, graph.invoke) beat plain words."""
    terms = _TERM.findall(question or "")
    if not terms:
        return fallback
    return sorted(terms, key=lambda t: (("_" in t or "." in t or any(c.isupper() for c in t[1:])), len(t)))[-1]


def _guiding_sentence(lesson_texts: List[str], question: str, forbidden: List[str]) -> Optional[str]:
    """The lesson sentence closest to the question that does NOT contain
    the answer. Pointing back to the lesson is the guide; quoting the key
    would be the answer."""
    q = token_set(question)
    best, best_score = None, 0
    for body in lesson_texts:
        for chunk in split_chunks(body):
            if chunk.lstrip().startswith("```"):
                continue
            for sentence in re.split(r"(?<=[.!؟?])\s+|\n+", chunk):
                s = sentence.strip().lstrip("#").strip()
                if not (20 <= len(s) <= 220):
                    continue
                if any(f and f in squash(s) for f in forbidden):
                    continue
                score = len(set(tokens(s)) & q)
                if score > best_score:
                    best, best_score = s, score
    return best


def feedback_blocks(
    lang: str,
    q: dict,
    choice: int,
    is_correct: bool,
    lesson_texts: List[str],
    skill: str,
    grounding: str,
) -> List[dict]:
    correct_text = str(q["options"][q["correct"]])
    if is_correct:
        explanation = str(q.get("explanation") or "").strip()
        text = L(lang, "صحيح", "Correct") + (f" — {explanation}" if explanation else ".")
        return [{"kind": "text", "grounding": grounding, "text": text}]

    forbidden = [squash(correct_text)] if len(squash(correct_text)) >= 3 else []
    chosen = str(q["options"][choice])

    authored_guide = q.get("guide") or q.get("hint")
    if isinstance(authored_guide, str) and not any(f in squash(authored_guide) for f in forbidden):
        guide = authored_guide.strip()
    else:
        sentence = _guiding_sentence(lesson_texts, str(q.get("question", "")), forbidden)
        if sentence:
            guide = L(
                lang,
                f"قريب — لنفكّر معاً. لماذا قد لا يكون «{chosen}» هو الجواب؟ ارجع لهذه الفكرة من الدرس: «{sentence}»",
                f"Close — let's think it through. Why might \"{chosen}\" not be it? Go back to this idea from the lesson: \"{sentence}\"",
            )
        else:
            guide = L(
                lang,
                f"قريب — لنفكّر معاً. ما الذي يجعل «{chosen}» غير كافٍ هنا؟ أعد قراءة السؤال وحدّد الكلمة المفتاحية فيه.",
                f"Close — let's think it through. What makes \"{chosen}\" not quite enough here? Re-read the question and find its key word.",
            )

    authored_follow = q.get("followup") or q.get("follow_up")
    if isinstance(authored_follow, str) and not any(f in squash(authored_follow) for f in forbidden):
        follow = authored_follow.strip()
    else:
        term = _key_term(str(q.get("question", "")), skill)
        follow = L(lang, f"سؤال أصغر: بجملة واحدة، ما دور {term} هنا؟", f"A smaller question: in one sentence, what does {term} do here?")

    return [
        {"kind": "hint", "grounding": grounding, "text": guide},
        {"kind": "check", "grounding": grounding, "text": follow},
    ]
