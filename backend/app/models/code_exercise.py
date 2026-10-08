"""Persistence for deterministic code runs, submissions, and solution views."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class CodeExerciseAttempt(Base):
    __tablename__ = "code_exercise_attempts"
    __table_args__ = (
        Index("ix_code_exercise_attempt_user_exercise", "user_id", "exercise_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(16), nullable=False)  # run | submit | solution
    submission = Column(Text, nullable=True)
    status = Column(String(32), nullable=False)
    passed = Column(Boolean, nullable=False, default=False)
    failed_test_id = Column(String(160), nullable=True)
    tests_passed = Column(Integer, nullable=False, default=0)
    tests_total = Column(Integer, nullable=False, default=0)
    execution_time_ms = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")
    exercise = relationship("Exercise")
