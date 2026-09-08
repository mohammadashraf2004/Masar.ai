"""
backend/app/models/answer_submission.py

A conversational thread where a student answers an Exercise (open-ended,
often code) or an open-ended Quiz question, and an LLM evaluates it
turn-by-turn — like chatting with ChatGPT about whether the answer is
right, rather than a single static grade.

Exactly one of (exercise_id) or (quiz_id + question_index) is set per row.
Works for both career-track and tool-course content, since Exercise/Quiz
rows are shared between the two (topic_id vs tool_topic_id) — this model
doesn't need to know which kind of topic it came from at all.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class AnswerSubmission(Base):
    __tablename__ = "answer_submissions"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id    = Column(Integer, ForeignKey("exercises.id"), nullable=True)
    quiz_id        = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    question_index = Column(Integer, nullable=True)  # only meaningful when quiz_id is set

    # messages format: [{"role": "user"|"assistant", "content": "...", "timestamp": "..."}]
    messages    = Column(JSON, default=list)
    is_correct  = Column(Boolean, nullable=True)  # null = not yet resolved by the LLM
    score       = Column(Float, nullable=True)    # 0-100, null until first evaluation

    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    user     = relationship("User")
    exercise = relationship("Exercise")
    quiz     = relationship("Quiz")
