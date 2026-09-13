from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    Text, ForeignKey, Enum, Float, JSON, UniqueConstraint, Index, text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class ExamStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    submitted   = "submitted"
    passed      = "passed"
    failed      = "failed"
    flagged     = "flagged"   # passed score but too many violations


class ViolationType(str, enum.Enum):
    tab_switch      = "tab_switch"       # left the exam tab
    face_not_visible = "face_not_visible" # face left camera frame
    multiple_faces  = "multiple_faces"   # someone else visible
    no_camera       = "no_camera"        # camera disconnected
    fullscreen_exit = "fullscreen_exit"  # exited fullscreen


class Exam(Base):
    """One exam per track — the certification gate."""
    __tablename__ = "exams"

    id           = Column(Integer, primary_key=True, index=True)
    track_id     = Column(Integer, ForeignKey("career_tracks.id"), nullable=False)
    title        = Column(String, nullable=False)
    description  = Column(Text)
    duration_minutes = Column(Integer, default=60)
    passing_score    = Column(Integer, default=70)   # percentage
    max_attempts     = Column(Integer, default=3)
    questions        = Column(JSON, nullable=False, default=list)
    # questions format:
    # [{"id": 1, "question": "...", "options": [...], "correct": 0,
    #   "explanation": "...", "points": 1, "type": "mcq|code|scenario"}]
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    track    = relationship("CareerTrack")
    attempts = relationship("ExamAttempt", back_populates="exam")


class ExamAttempt(Base):
    """One attempt = one sitting of an exam by a student."""
    __tablename__ = "exam_attempts"
    __table_args__ = (
        # At most one IN_PROGRESS attempt per user per exam. Closes the
        # start_exam TOCTOU where concurrent /start requests could each
        # pass the "no existing in-progress attempt" check and each
        # insert one — see migration 010_exam_attempt_start_race, and the
        # concurrency test that reproduced it. Partial, not table-wide: a
        # new attempt after a previous one is submitted/passed/failed/
        # flagged must stay legal (the ordinary multi-attempt flow).
        Index(
            "uq_exam_attempts_one_in_progress",
            "user_id", "exam_id",
            unique=True,
            postgresql_where=text("status = 'in_progress'::examstatus"),
        ),
    )

    id          = Column(Integer, primary_key=True, index=True)
    exam_id     = Column(Integer, ForeignKey("exams.id"), nullable=False)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    status      = Column(Enum(ExamStatus), default=ExamStatus.not_started)
    answers     = Column(JSON, default=dict)   # {question_id: selected_option}
    score       = Column(Float, nullable=True)
    passed      = Column(Boolean, nullable=True)
    # proctoring summary
    violations_count  = Column(Integer, default=0)
    tab_switches      = Column(Integer, default=0)
    face_warnings     = Column(Integer, default=0)
    # timing
    started_at    = Column(DateTime(timezone=True), nullable=True)
    submitted_at  = Column(DateTime(timezone=True), nullable=True)
    time_spent_seconds = Column(Integer, nullable=True)

    exam = relationship("Exam",        back_populates="attempts")
    user = relationship("User",        back_populates="exam_attempts")
    violations = relationship("ProctoringEvent", back_populates="attempt",
                              cascade="all, delete-orphan")
    certificate = relationship("Certificate", back_populates="attempt",
                               uselist=False)


class ProctoringEvent(Base):
    """Each proctoring violation logged during an attempt."""
    __tablename__ = "proctoring_events"

    id           = Column(Integer, primary_key=True, index=True)
    attempt_id   = Column(Integer, ForeignKey("exam_attempts.id"), nullable=False)
    violation    = Column(Enum(ViolationType), nullable=False)
    description  = Column(String, nullable=True)
    occurred_at  = Column(DateTime(timezone=True), server_default=func.now())

    attempt = relationship("ExamAttempt", back_populates="violations")


class Certificate(Base):
    """Issued when a student passes an exam."""
    __tablename__ = "certificates"

    id            = Column(Integer, primary_key=True, index=True)
    attempt_id    = Column(Integer, ForeignKey("exam_attempts.id"),
                          nullable=False, unique=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    track_id      = Column(Integer, ForeignKey("career_tracks.id"), nullable=False)
    certificate_id = Column(String, unique=True, nullable=False)  # UUID
    score         = Column(Float, nullable=False)
    issued_at     = Column(DateTime(timezone=True), server_default=func.now())
    is_valid      = Column(Boolean, default=True)   # can be revoked

    attempt = relationship("ExamAttempt", back_populates="certificate")
    user    = relationship("User",        back_populates="certificates")
    track   = relationship("CareerTrack")