from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Index, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.legal import acceptance_is_current
from app.core.releases import pending_updates
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
    __table_args__ = (
        # The plain unique index on `email` is case-SENSITIVE, so it would
        # happily store Alice@x.com alongside alice@x.com — two accounts
        # the user experiences as one. The API normalizes to lowercase
        # (app.core.security.normalize_email); this index is the guarantee
        # that holds even for rows a seed script or a future code path
        # writes without going through that.
        Index("ix_users_email_lower", func.lower(Column("email", String)), unique=True),
    )

    id                      = Column(Integer, primary_key=True, index=True)
    email                   = Column(String, unique=True, index=True, nullable=False)
    full_name               = Column(String, nullable=False)
    hashed_password         = Column(String, nullable=False)
    # NOT NULL: every authorization decision reads this column, and a
    # NULL role is an ambiguous state an authz check has to guess about.
    # See alembic/versions/004_security_constraints.py.
    role                    = Column(
        Enum(UserRole), default=UserRole.student, server_default="student", nullable=False,
    )
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
    # Which Terms of Service / Privacy Policy the account accepted, and when.
    # Versions are written by the server from app.core.legal, never taken from
    # a request. NULL means "never accepted" (every account that predates the
    # feature) - not "accepted the current version".
    terms_version           = Column(String, nullable=True)
    terms_accepted_at       = Column(DateTime(timezone=True), nullable=True)
    privacy_version         = Column(String, nullable=True)
    privacy_accepted_at     = Column(DateTime(timezone=True), nullable=True)
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
    update_acknowledgements = relationship(
        "UserUpdateAcknowledgement", back_populates="user", cascade="all, delete-orphan",
    )
    tours = relationship("UserTour", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("UserSubscription", back_populates="user")

    @property
    def pending_updates(self) -> list:
        """The product announcements this account has yet to see (app.core.releases)."""
        return pending_updates(a.release_id for a in self.update_acknowledgements)

    @property
    def requires_legal_acceptance(self) -> bool:
        """True until the account has accepted the versions in force now."""
        return not acceptance_is_current(
            self.terms_version, self.terms_accepted_at,
            self.privacy_version, self.privacy_accepted_at,
        )
