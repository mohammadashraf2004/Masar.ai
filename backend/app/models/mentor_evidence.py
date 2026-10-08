from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.sql import func

from app.db.session import Base


class MentorEvidence(Base):
    """One thing a learner did that says something about a skill: today, an answer to
    a mentor quiz question.

    It is the only new table behind the Mentor v2 endpoints, and it serves two readers:

    * the skill state (`services/mentor/v2/skills.py`) folds a learner's rows for a skill
      into a confidence and a status, so a status rests on repeated evidence and never on
      a single answer;
    * the mentor's context (`services/mentor/v2/context.py`) reads the recent *wrong*
      rows, so a reply can build on what the learner just got wrong.

    `selected` is the index the learner picked. The correct index is never copied here:
    it stays on the authored `Quiz` row, so this table cannot become an answer key.
    """
    __tablename__ = "mentor_evidence"
    __table_args__ = (
        Index("ix_mentor_evidence_user_skill_created", "user_id", "skill", "created_at"),
        Index("ix_mentor_evidence_user_lesson", "user_id", "lesson_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    kind = Column(String(20), nullable=False, default="quiz", server_default="quiz")
    skill = Column(String(120), nullable=False)
    correct = Column(Boolean, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="SET NULL"), nullable=True)
    question_index = Column(Integer, nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    selected = Column(Integer, nullable=True)
    # 1 for the first answer to a question, 2 for the retry, ... A retry says much less than a
    # first answer (a learner can simply try each option), so it counts for a fraction.
    attempt_no = Column(Integer, nullable=False, default=1, server_default="1")
    weight = Column(Float, nullable=False, default=1.0, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
