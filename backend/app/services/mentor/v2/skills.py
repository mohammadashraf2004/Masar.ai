"""
What the mentor believes about a learner's skills, derived from evidence.

The rule that keeps it honest: **a status never rests on one answer.** Every answer is
stored as a `MentorEvidence` row and the state is *folded* from the rows on demand, so
there is no counter that could drift and nothing a single wrong answer can flip.

Confidence is a smoothed 0-100 estimate that starts at a neutral prior and moves a
quarter of the way toward each answer (toward 100 for a right one, 0 for a wrong one).
A retry of a question already answered moves it a quarter as far: a learner who simply
tries every option should not be able to farm confidence.

Status needs *distinct questions* behind it:

    fewer than 2 questions answered              -> learning   (not enough evidence)
    confidence < 40 and 2 of the last 3 wrong    -> needs_review
    confidence >= 80, 3+ questions, last 2 right -> mastered
    anything else                                -> learning

`confidence` can still move on the first answer (so the learner sees the effect of what
they did); only the *status* is guarded.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

from sqlalchemy.orm import Session

from app.models.mentor_evidence import MentorEvidence

PRIOR = 50.0
ALPHA = 0.25
RETRY_WEIGHT = 0.25

MIN_QUESTIONS_FOR_STATUS = 2
NEEDS_REVIEW_BELOW = 40.0
MASTERED_AT = 80.0
MASTERED_MIN_QUESTIONS = 3

LEARNING = "learning"
NEEDS_REVIEW = "needs_review"
MASTERED = "mastered"

# How far back a mistake still counts as "recent" for the mentor's context.
RECENT_MISTAKE_DAYS = 30


@dataclass(frozen=True)
class SkillState:
    confidence: int      # 0-100, rounded
    status: str
    questions: int       # distinct questions answered


def _fold(rows: Sequence[MentorEvidence]) -> SkillState:
    confidence = PRIOR
    for row in rows:
        target = 100.0 if row.correct else 0.0
        confidence += ALPHA * (row.weight if row.weight is not None else 1.0) * (target - confidence)
    questions = sum(1 for r in rows if (r.attempt_no or 1) == 1)

    status = LEARNING
    if questions >= MIN_QUESTIONS_FOR_STATUS:
        last3 = rows[-3:]
        wrong_of_last3 = sum(1 for r in last3 if not r.correct)
        if confidence < NEEDS_REVIEW_BELOW and wrong_of_last3 >= 2:
            status = NEEDS_REVIEW
        elif (confidence >= MASTERED_AT and questions >= MASTERED_MIN_QUESTIONS
              and all(r.correct for r in rows[-2:])):
            status = MASTERED
    return SkillState(confidence=int(round(confidence)), status=status, questions=questions)


def evidence_rows(db: Session, user_id: int, skill: str) -> List[MentorEvidence]:
    return (
        db.query(MentorEvidence)
        .filter(MentorEvidence.user_id == user_id, MentorEvidence.skill == skill)
        .order_by(MentorEvidence.created_at, MentorEvidence.id)
        .all()
    )


def skill_state(db: Session, user_id: int, skill: str) -> SkillState:
    return _fold(evidence_rows(db, user_id, skill))


@dataclass(frozen=True)
class SkillChange:
    skill: str
    before: int
    after: int
    status: str


def record_answer(
    db: Session, *, user_id: int, skill: str, correct: bool,
    quiz_id: Optional[int], question_index: Optional[int], lesson_id: Optional[int], selected: Optional[int],
) -> Optional[SkillChange]:
    """Store one answer and return how the skill's confidence moved - or None when it did
    not (a retry of an already-mastered question, for instance), so the caller reports a
    delta only when there is one."""
    rows = evidence_rows(db, user_id, skill)
    before = _fold(rows)

    same_question = [r for r in rows if r.quiz_id == quiz_id and r.question_index == question_index]
    attempt = len(same_question) + 1
    row = MentorEvidence(
        user_id=user_id, kind="quiz", skill=skill, correct=correct, quiz_id=quiz_id,
        question_index=question_index, lesson_id=lesson_id, selected=selected,
        attempt_no=attempt, weight=1.0 if attempt == 1 else RETRY_WEIGHT,
    )
    db.add(row)
    db.flush()

    after = _fold(rows + [row])
    if after.confidence == before.confidence:
        return None
    return SkillChange(skill=skill, before=before.confidence, after=after.confidence, status=after.status)
