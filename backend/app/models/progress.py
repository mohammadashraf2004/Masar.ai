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
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    status = Column(Enum(ProgressStatus), default=ProgressStatus.not_started)
    lessons_completed = Column(JSON, default=list)
    exercises_completed = Column(JSON, default=list)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_spent_minutes = Column(Integer, default=0)

    user = relationship("User", back_populates="progress_records")
    topic = relationship("Topic", back_populates="progress_records")

    # A progress row belongs to EITHER a track topic OR a tool topic, never
    # both — same convention as Lesson/Exercise/Quiz/Project's tool_topic_id.
    tool_topic_id = Column(Integer, ForeignKey("tool_topics.id"), nullable=True)
    tool_topic    = relationship("ToolTopic", back_populates="progress_records",
                                 foreign_keys="[UserProgress.tool_topic_id]")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    answers = Column(JSON, nullable=False)
    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    feedback = Column(JSON, default=dict)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    # Legacy. No request schema accepts it and no response returns it any
    # more — a project is submitted as code written in the reader, not as a
    # repo link. Kept because rows written before that change still hold
    # real URLs; see alembic/versions/007_project_submission_code.py.
    github_url = Column(String, nullable=True)
    # The submitted solution. This is what the AI reviewer reads.
    code = Column(Text, nullable=True)
    # Optional notes on approach and decisions — context for the reviewer,
    # never a substitute for the code.
    description = Column(Text, nullable=True)
    ai_review = Column(JSON, nullable=True)
    score = Column(Float, nullable=True)
    # New: performance metrics captured during AI code review
    review_latency_ms = Column(Float, nullable=True)
    review_tokens_used = Column(Integer, nullable=True)
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
    # messages format: [{"role": "user"|"assistant", "content": "...", "timestamp": "...", "latency_ms": int, "tokens": int}]
    total_tokens = Column(Integer, default=0)
    avg_latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="mentor_sessions")


class UserSkillScore(Base):
    """Tracks individual skill competency scores with verified metrics"""
    __tablename__ = "user_skill_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String, nullable=False)
    score = Column(Float, default=0.0)           # 0–100 competency
    last_assessed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Verified performance metrics (populated from real activity)
    avg_latency_ms = Column(Float, nullable=True)
    cost_per_1k_tokens = Column(Float, nullable=True)
    hallucination_rate = Column(Float, nullable=True)   # 0–1
    retrieval_precision = Column(Float, nullable=True)  # 0–100
    tokens_used = Column(Integer, nullable=True)
    verified = Column(Boolean, default=False)
    evidence_source = Column(String, nullable=True)     # "exam"|"project"|"mentor"|"skill_gap"

    user = relationship("User", back_populates="skill_scores")


class EngineerScorecard(Base):
    """Aggregated verified engineer scorecard — one per user"""
    __tablename__ = "engineer_scorecards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Certification
    certs_earned = Column(Integer, default=0)
    exams_attempted = Column(Integer, default=0)
    exam_pass_rate = Column(Float, nullable=True)        # 0–100

    # Performance
    avg_latency_ms = Column(Float, nullable=True)
    p95_latency_ms = Column(Float, nullable=True)
    cost_per_1k_requests = Column(Float, nullable=True)
    total_tokens_used = Column(Integer, default=0)

    # Quality
    hallucination_rate = Column(Float, nullable=True)   # 0–1 lower is better
    retrieval_precision = Column(Float, nullable=True)  # 0–100
    code_quality_score = Column(Float, nullable=True)   # 0–100
    avg_project_score = Column(Float, nullable=True)    # 0–100

    # Activity
    projects_submitted = Column(Integer, default=0)
    quizzes_passed = Column(Integer, default=0)
    mentor_sessions_count = Column(Integer, default=0)
    total_study_minutes = Column(Integer, default=0)

    # Summary
    overall_grade = Column(String(2), nullable=True)    # A+, A, B+, B, C, D
    hire_ready = Column(Boolean, default=False)
    last_computed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="scorecard")