from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class UserRole(str, enum.Enum):
    student = "student"
    mentor = "mentor"
    admin = "admin"


class ExperienceLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student)
    experience_level = Column(Enum(ExperienceLevel), default=ExperienceLevel.beginner)
    is_active = Column(Boolean, default=True)
    bio = Column(Text, nullable=True)
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    overall_readiness_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    progress_records = relationship("UserProgress", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    project_submissions = relationship("ProjectSubmission", back_populates="user")
    mentor_sessions = relationship("MentorSession", back_populates="user")
    skill_scores = relationship("UserSkillScore", back_populates="user")
