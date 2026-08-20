from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class UserRole(str, enum.Enum):
    student = "student"
    mentor  = "mentor"
    admin   = "admin"


class ExperienceLevel(str, enum.Enum):
    beginner     = "beginner"
    intermediate = "intermediate"
    advanced     = "advanced"


class User(Base):
    __tablename__ = "users"

    id                      = Column(Integer, primary_key=True, index=True)
    email                   = Column(String, unique=True, index=True, nullable=False)
    full_name               = Column(String, nullable=False)
    hashed_password         = Column(String, nullable=False)
    role                    = Column(Enum(UserRole), default=UserRole.student)
    experience_level        = Column(Enum(ExperienceLevel), default=ExperienceLevel.beginner)
    is_active               = Column(Boolean, default=True)
    is_verified             = Column(Boolean, default=False, nullable=False)
    bio                     = Column(Text, nullable=True)
    github_url              = Column(String, nullable=True)
    linkedin_url            = Column(String, nullable=True)
    avatar_url              = Column(String, nullable=True)
    overall_readiness_score = Column(Float, default=0.0)
    # Bumped on password change / "log out everywhere" / account deletion.
    # Embedded in every JWT at issuance time — a mismatch means the token
    # predates one of those events and is rejected, even though JWTs are
    # otherwise stateless and can't be individually revoked.
    token_version           = Column(Integer, default=0, nullable=False)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())
    updated_at              = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    enrollments         = relationship("Enrollment",         back_populates="user")
    progress_records    = relationship("UserProgress",       back_populates="user")
    quiz_attempts       = relationship("QuizAttempt",        back_populates="user")
    project_submissions = relationship("ProjectSubmission",  back_populates="user")
    mentor_sessions     = relationship("MentorSession",      back_populates="user")
    skill_scores        = relationship("UserSkillScore",     back_populates="user")
    scorecard           = relationship("EngineerScorecard",  back_populates="user", uselist=False)
    wallet              = relationship("UserWallet",         back_populates="user", uselist=False)
    challenge_attempts  = relationship("ChallengeAttempt",   back_populates="user")
    exam_payments       = relationship("ExamPayment",        back_populates="user")

    posts         = relationship("Post",        back_populates="author")
    comments      = relationship("PostComment", back_populates="author")
    exam_attempts = relationship("ExamAttempt", back_populates="user")
    certificates  = relationship("Certificate", back_populates="user")

    tool_enrollments = relationship("ToolEnrollment",       back_populates="user")
    tool_completions = relationship("ToolCourseCompletion", back_populates="user")
    email_tokens      = relationship("EmailToken",          back_populates="user")
