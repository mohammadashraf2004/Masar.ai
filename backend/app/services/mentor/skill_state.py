"""Learner skill state from repeated evidence.

Each graded mentor quiz answer is one piece of evidence for one skill.
State lives on UserSkillScore (`score` 0–100 is the confidence the UI
shows as 0–1), and the decision of whether to move it reads the last
few answers from mentor_quiz_answers.

The rule the UI promises ("one mistake doesn't change your status"):
  * a correct answer raises confidence a step
  * a wrong answer lowers it only when it repeats an earlier one: at least
    REPEAT_WRONG wrong answers among the last RECENT. An isolated wrong
    answer is logged as evidence (and as a mistake) but moves nothing.

Status is derived, not stored, so it can never drift from the evidence:
  needs_review  repeated wrong answers (REPEAT_WRONG in the last RECENT)
  mastered      confidence >= MASTERED_AT with at least MIN_EVIDENCE answers
  learning      everything else
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.progress import MentorQuizAnswer, UserSkillScore

STEP = 0.2
RECENT = 3
REPEAT_WRONG = 2
MASTERED_AT = 75.0
MIN_EVIDENCE = 3
INITIAL_SCORE = 50.0

NEEDS_REVIEW = "needs_review"
LEARNING = "learning"
MASTERED = "mastered"


@dataclass
class SkillChange:
    skill: str
    before: float
    after: float
    status: str
    previous_status: str


def _recent_outcomes(db: Session, user_id: int, skill: str, limit: int) -> List[bool]:
    rows = (
        db.query(MentorQuizAnswer.is_correct)
        .filter(MentorQuizAnswer.user_id == user_id, MentorQuizAnswer.skill_name == skill)
        .order_by(MentorQuizAnswer.created_at.desc(), MentorQuizAnswer.id.desc())
        .limit(limit)
        .all()
    )
    return [r[0] for r in rows]


def status_for(score: float, outcomes: List[bool]) -> str:
    """`outcomes` newest first."""
    if sum(1 for ok in outcomes[:RECENT] if not ok) >= REPEAT_WRONG:
        return NEEDS_REVIEW
    if score >= MASTERED_AT and len(outcomes) >= MIN_EVIDENCE:
        return MASTERED
    return LEARNING


def apply_answer(db: Session, user_id: int, skill: str, is_correct: bool) -> Optional[SkillChange]:
    """Update state for an answer that has already been added (and flushed)
    to mentor_quiz_answers. Returns the change only when confidence moved."""
    outcomes = _recent_outcomes(db, user_id, skill, max(RECENT, MIN_EVIDENCE) + 1)
    previous_outcomes = outcomes[1:]

    row = (
        db.query(UserSkillScore)
        .filter(UserSkillScore.user_id == user_id, UserSkillScore.skill_name == skill)
        .first()
    )
    before = float(row.score) if row and row.score is not None else INITIAL_SCORE

    repeated_wrong = sum(1 for ok in outcomes[:RECENT] if not ok) >= REPEAT_WRONG
    if is_correct:
        after = before + STEP * (100.0 - before)
    elif repeated_wrong:
        after = before - STEP * before
    else:
        after = before

    previous_status = status_for(before, previous_outcomes)
    status = status_for(after, outcomes)

    if round(after) == round(before):
        return None

    if row is None:
        row = UserSkillScore(user_id=user_id, skill_name=skill)
        db.add(row)
    row.score = round(after, 1)
    row.evidence_source = "mentor"
    row.last_assessed_at = datetime.now(timezone.utc)
    return SkillChange(
        skill=skill,
        before=round(before / 100, 2),
        after=round(after / 100, 2),
        status=status,
        previous_status=previous_status,
    )
