"""Project Lab: guided, multi-file projects in the Challenges section.

Two halves, deliberately separate:

* Content definitions — LabProject > LabMilestone > LabTask. Authored in
  app/services/project_lab/definitions/ and synced by seeds/seed_project_lab.py.
  A new project is new rows (plus a template folder and, if it needs new check
  logic, a validator module); never a schema change.
* Learner state — LabAttempt (one workspace per learner per project) with its
  LabWorkspaceFile rows (the learner's editable files only; read-only datasets
  stay in the canonical template on disk and are never copied per learner),
  LabTaskProgress (one row per task), and the LabRun / LabSubmission logs.

Named Lab* because ChallengeProject / ChallengeAttempt already belong to the
credit-paid, AI-graded challenges in app/models/challenge.py, which this does
not replace.

`LabTask.validator_config` is private: no view schema may expose it.
"""
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class LabProject(Base):
    __tablename__ = "lab_projects"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, nullable=False)
    track_id = Column(Integer, ForeignKey("career_tracks.id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    title_ar = Column(String(200), nullable=True)
    summary = Column(Text, nullable=False)
    summary_ar = Column(Text, nullable=True)
    difficulty = Column(String(24), nullable=False, default="beginner")
    estimated_hours = Column(Integer, nullable=True)
    # Folder under backend/project_templates/ holding workspace/.
    template_key = Column(String(80), nullable=False)
    template_version = Column(String(40), nullable=False)
    # Workspace paths learners may never write: exact files ("README.md") or
    # folder prefixes ending in "/" ("data/").
    read_only_paths = Column(JSON, nullable=False, default=list)
    position = Column(Integer, nullable=False, default=0)
    # Project Overview content shown before starting: role, scenario,
    # duration range, skills and deliverables (all bilingual).
    overview = Column(JSON, nullable=False, default=dict)
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    track = relationship("CareerTrack")
    milestones = relationship(
        "LabMilestone", back_populates="project", order_by="LabMilestone.position",
        cascade="all, delete-orphan",
    )


class LabMilestone(Base):
    __tablename__ = "lab_milestones"
    __table_args__ = (UniqueConstraint("project_id", "slug", name="uq_lab_milestones_project_slug"),)

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    slug = Column(String(120), nullable=False)
    position = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    title_ar = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    # Skill areas this milestone validates, shown in the final submission
    # summary: [{"en": "SQL joins", "ar": "..."}].
    skills = Column(JSON, nullable=False, default=list)

    project = relationship("LabProject", back_populates="milestones")
    tasks = relationship(
        "LabTask", back_populates="milestone", order_by="LabTask.position", cascade="all, delete-orphan",
    )


class LabTask(Base):
    __tablename__ = "lab_tasks"
    __table_args__ = (UniqueConstraint("project_id", "slug", name="uq_lab_tasks_project_slug"),)

    id = Column(Integer, primary_key=True, index=True)
    # Denormalised from the milestone so task slugs are unique per project.
    project_id = Column(Integer, ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    milestone_id = Column(Integer, ForeignKey("lab_milestones.id", ondelete="CASCADE"), nullable=False, index=True)
    slug = Column(String(120), nullable=False)
    position = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    title_ar = Column(String(200), nullable=True)
    instructions = Column(Text, nullable=False)  # Markdown
    instructions_ar = Column(Text, nullable=True)
    # [{"en": "...", "ar": "..."}] — static, authored hints; never generated.
    hints = Column(JSON, nullable=False, default=list)
    # The workspace file the lab opens when the task is selected.
    primary_file = Column(String(255), nullable=True)
    # Server-side only. Key into app/services/project_lab/validators.
    validator_key = Column(String(120), nullable=False)
    validator_config = Column(JSON, nullable=False, default=dict)

    milestone = relationship("LabMilestone", back_populates="tasks")


class LabAttempt(Base):
    """A learner's workspace for one project. One per learner per project in
    V1: starting again returns the same attempt (idempotent start)."""
    __tablename__ = "lab_attempts"
    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_lab_attempts_user_project"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("lab_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(16), nullable=False, default="active")  # active | completed
    template_version = Column(String(40), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    # Final submission: allowed once every task has passed. Extension point
    # for later portfolio/certificate work, which is out of scope today.
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    # Portfolio-ready completion summary, frozen at final submission
    # (service.completion_summary, schema_version 1). Read by nothing public
    # yet; a later portfolio/certificate feature consumes it.
    completion = Column(JSON, nullable=True)

    project = relationship("LabProject")
    files = relationship("LabWorkspaceFile", back_populates="attempt", cascade="all, delete-orphan")
    task_progress = relationship("LabTaskProgress", back_populates="attempt", cascade="all, delete-orphan")


class LabWorkspaceFile(Base):
    """A learner-editable file. Created from the template when the attempt
    starts; reset rewrites it from the template."""
    __tablename__ = "lab_workspace_files"
    __table_args__ = (UniqueConstraint("attempt_id", "path", name="uq_lab_workspace_files_attempt_path"),)

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    path = Column(String(255), nullable=False)
    content = Column(Text, nullable=False, default="")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    attempt = relationship("LabAttempt", back_populates="files")


class LabTaskProgress(Base):
    """Per-task state inside an attempt. A task is completed only by a passing
    Check Step; the row's uniqueness is what makes repeat passes idempotent."""
    __tablename__ = "lab_task_progress"
    __table_args__ = (UniqueConstraint("attempt_id", "task_id", name="uq_lab_task_progress_attempt_task"),)

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("lab_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(16), nullable=False, default="not_started")  # not_started | in_progress | completed
    check_count = Column(Integer, nullable=False, default=0)
    last_outcome = Column(String(8), nullable=True)  # pass | fail | error
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    attempt = relationship("LabAttempt", back_populates="task_progress")
    task = relationship("LabTask")


class LabRun(Base):
    """One Run of a workspace file. No source is stored: the file is in
    lab_workspace_files, and a log of every keystroke-run is not needed."""
    __tablename__ = "lab_runs"
    __table_args__ = (Index("ix_lab_runs_attempt_created", "attempt_id", "created_at"),)

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False)
    path = Column(String(255), nullable=False)
    kind = Column(String(16), nullable=False)  # python | sql
    status = Column(String(32), nullable=False)  # success | error | timeout | infrastructure_error
    execution_ms = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class LabSubmission(Base):
    """One Check Step. `checks` holds only what the learner was shown."""
    __tablename__ = "lab_submissions"
    __table_args__ = (Index("ix_lab_submissions_attempt_task", "attempt_id", "task_id"),)

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("lab_tasks.id", ondelete="CASCADE"), nullable=False)
    outcome = Column(String(8), nullable=False)  # pass | fail | error
    checks = Column(JSON, nullable=False, default=list)
    error_kind = Column(String(24), nullable=True)  # execution | infrastructure
    execution_ms = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class LabArtifact(Base):
    """A file a learner's code generated (charts/*.png and the like), kept so
    the report check, the report preview and the final summary can see it.
    The latest version per path wins; size is bounded by the runner."""
    __tablename__ = "lab_artifacts"
    __table_args__ = (UniqueConstraint("attempt_id", "path", name="uq_lab_artifacts_attempt_path"),)

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    path = Column(String(255), nullable=False)
    media_type = Column(String(64), nullable=False)
    encoding = Column(String(16), nullable=False)  # base64 | text
    content = Column(Text, nullable=False)
    size = Column(Integer, nullable=False, default=0)
    sha256 = Column(String(64), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class LabExecutionLease(Base):
    """At most one running execution (Run or Check Step) per learner, across
    every API worker. Taken with an atomic upsert that only succeeds when no
    unexpired lease exists; released when the execution ends. An expired
    lease (a worker that died mid-run) is simply overwritten, so a learner is
    never locked out. A Redis lock can replace this table later without any
    change to the API (see service.ExecutionGate)."""
    __tablename__ = "lab_execution_leases"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    attempt_id = Column(Integer, ForeignKey("lab_attempts.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), nullable=False)
    action = Column(String(16), nullable=False)  # run | check
    started_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
