from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class Enrollment(Base):
    """User enrolled in a career track"""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("career_tracks.id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    completion_percentage = Column(Float, default=0.0)
    target_job_title = Column(String, nullable=True)

    user = relationship("User", back_populates="enrollments")
    track = relationship("CareerTrack", back_populates="enrollments")


class UserProgress(Base):
    """Tracks completion of individual topics"""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(Enum(ProgressStatus), default=ProgressStatus.not_started)
    lessons_completed = Column(JSON, default=list)  # list of lesson IDs
    exercises_completed = Column(JSON, default=list)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_spent_minutes = Column(Integer, default=0)

    user = relationship("User", back_populates="progress_records")
    topic = relationship("Topic", back_populates="progress_records")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    answers = Column(JSON, nullable=False)  # {question_index: selected_option}
    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    feedback = Column(JSON, default=dict)  # per-question feedback
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    github_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    ai_review = Column(JSON, nullable=True)  # AI feedback JSON
    score = Column(Float, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="project_submissions")
    project = relationship("Project", back_populates="submissions")


class MentorSession(Base):
    """Chat session with AI mentor"""
    __tablename__ = "mentor_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    context_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    messages = Column(JSON, default=list)
    # messages format: [{"role": "user"|"assistant", "content": "...", "timestamp": "..."}]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="mentor_sessions")


class UserSkillScore(Base):
    """Tracks individual skill competency scores"""
    __tablename__ = "user_skill_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String, nullable=False)
    score = Column(Float, default=0.0)  # 0-100
    last_assessed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="skill_scores")
