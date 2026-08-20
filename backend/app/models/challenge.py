"""
backend/app/models/challenge.py
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class ChallengeDifficulty(str, enum.Enum):
    beginner     = "beginner"
    intermediate = "intermediate"
    advanced     = "advanced"


class ChallengeStatus(str, enum.Enum):
    locked     = "locked"      # not enrolled
    enrolled   = "enrolled"    # paid credits, can access dataset
    submitted  = "submitted"   # solution submitted, awaiting grade
    graded     = "graded"      # AI grade complete
    passed     = "passed"      # score >= passing_score
    failed     = "failed"      # score < passing_score


class ChallengeProject(Base):
    """A paid challenge project with dirty data that must be cleaned & processed."""
    __tablename__ = "challenge_projects"

    id               = Column(Integer, primary_key=True, index=True)
    title            = Column(String, nullable=False)
    slug             = Column(String, unique=True, nullable=False)
    description      = Column(Text, nullable=False)
    difficulty       = Column(Enum(ChallengeDifficulty), nullable=False)
    credit_cost      = Column(Integer, nullable=False)       # credits to unlock
    passing_score    = Column(Float, default=70.0)           # 0-100
    max_attempts     = Column(Integer, default=3)
    is_active        = Column(Boolean, default=True)

    # The dirty dataset — stored as JSON, shown inline + downloadable
    dirty_dataset    = Column(JSON, nullable=False)          # list of messy records
    dataset_description = Column(Text, nullable=True)       # what's wrong with the data
    dataset_filename = Column(String, default="dirty_data.json")

    # What we're grading — list of rubric criteria
    # [{"criterion": "...", "weight": 30, "description": "..."}]
    grading_rubric   = Column(JSON, nullable=False)

    # Expected outcomes (for AI grader context)
    expected_output  = Column(JSON, nullable=True)
    hints            = Column(JSON, default=list)            # list of hint strings

    tags             = Column(JSON, default=list)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    attempts = relationship("ChallengeAttempt", back_populates="challenge")


class ChallengeAttempt(Base):
    """A user's enrollment and submission for a challenge project."""
    __tablename__ = "challenge_attempts"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id     = Column(Integer, ForeignKey("challenge_projects.id"), nullable=False)
    status           = Column(Enum(ChallengeStatus), default=ChallengeStatus.enrolled)
    attempt_number   = Column(Integer, default=1)
    credits_spent    = Column(Integer, nullable=False)

    # Submission
    solution_code    = Column(Text, nullable=True)           # the pipeline code
    solution_notes   = Column(Text, nullable=True)           # explanation
    github_url       = Column(String, nullable=True)

    # AI grading results
    score            = Column(Float, nullable=True)          # 0-100
    passed           = Column(Boolean, nullable=True)
    ai_feedback      = Column(JSON, nullable=True)           # per-criterion feedback
    # ai_feedback format:
    # [{"criterion": "...", "score": 85, "weight": 30, "feedback": "...", "passed": true}]

    enrolled_at      = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at     = Column(DateTime(timezone=True), nullable=True)
    graded_at        = Column(DateTime(timezone=True), nullable=True)

    user      = relationship("User", back_populates="challenge_attempts")
    challenge = relationship("ChallengeProject", back_populates="attempts")


class ExamPayment(Base):
    """EGP-only payment record for certification exam access."""
    __tablename__ = "exam_payments"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id          = Column(Integer, ForeignKey("exams.id"), nullable=False)
    egp_amount       = Column(Float, nullable=False)
    payment_method   = Column(String, nullable=False)        # fawry|instapay|vodafone_cash
    payment_ref      = Column(String, nullable=False)
    status           = Column(String, default="pending")     # pending|confirmed|failed
    confirmed_by     = Column(String, nullable=True)         # "admin" or "webhook"
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at     = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="exam_payments")