"""Project Lab API schemas.

These pick public fields explicitly. In particular nothing here carries
LabTask.validator_config, validator keys, captured run values or expected
results — validators are private and stay server-side.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class LocalizedHint(BaseModel):
    en: str
    ar: Optional[str] = None


class TrackRef(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None


class TaskSummary(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None


class TaskDetail(TaskSummary):
    instructions: str
    instructions_ar: Optional[str] = None
    hints: list[LocalizedHint] = []
    primary_file: Optional[str] = None


class MilestoneSummary(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    summary: Optional[str] = None
    summary_ar: Optional[str] = None
    tasks: list[TaskSummary]


class MilestoneDetail(MilestoneSummary):
    tasks: list[TaskDetail]


class AttemptRef(BaseModel):
    id: int
    status: str
    percent: int
    completed_tasks: int
    total_tasks: int
    submitted_at: Optional[datetime] = None


class ProjectOverview(BaseModel):
    """What the Project Overview shows before the learner starts."""
    role: Optional[str] = None
    role_ar: Optional[str] = None
    scenario: Optional[str] = None
    scenario_ar: Optional[str] = None
    duration_hours: Optional[list[int]] = None
    skills: list[LocalizedHint] = []
    deliverables: list[LocalizedHint] = []


class ProjectCard(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    summary: str
    summary_ar: Optional[str] = None
    difficulty: str
    estimated_hours: Optional[int] = None
    track: TrackRef
    milestone_count: int
    task_count: int
    attempt: Optional[AttemptRef] = None


class ProjectDetail(ProjectCard):
    milestones: list[MilestoneSummary]
    overview: ProjectOverview = ProjectOverview()


class TaskProgressView(BaseModel):
    slug: str
    milestone: str
    status: Literal["not_started", "in_progress", "completed"]
    check_count: int
    last_outcome: Optional[Literal["pass", "fail", "error"]] = None
    completed_at: Optional[datetime] = None


class MilestoneProgressView(BaseModel):
    slug: str
    completed_tasks: int
    total_tasks: int
    percent: int


class ProgressView(BaseModel):
    status: str
    completed_tasks: int
    total_tasks: int
    percent: int
    current_task: Optional[str] = None
    milestones: list[MilestoneProgressView]
    tasks: list[TaskProgressView]


class AttemptView(BaseModel):
    id: int
    status: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    project: ProjectCard
    milestones: list[MilestoneDetail]
    workspace_root: str
    progress: ProgressView


class StartResponse(BaseModel):
    attempt_id: int
    created: bool


class WorkspaceEntry(BaseModel):
    path: str
    kind: Literal["file", "dir"]
    language: Optional[str] = None
    editable: bool
    size: Optional[int] = None
    modified: bool = False


class WorkspaceView(BaseModel):
    root: str
    entries: list[WorkspaceEntry]


class TablePreview(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int
    truncated: bool


class FileView(BaseModel):
    path: str
    language: str
    editable: bool
    content: Optional[str] = None
    table: Optional[TablePreview] = None


class FileWrite(BaseModel):
    content: str = Field(..., max_length=200_000)


class PathRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=255)


class RunRequest(PathRequest):
    # Interface language for Masar's own message when nothing could run (as CheckRequest).
    language: Literal["en", "ar"] = "en"


class GeneratedFile(BaseModel):
    path: str
    size: int
    media_type: Optional[str] = None
    encoding: Optional[Literal["base64", "text"]] = None
    content: Optional[str] = None


class RunError(BaseModel):
    type: str
    message: str
    line: Optional[int] = None


class RunResponse(BaseModel):
    """status: success | error (the learner's code failed) | timeout |
    infrastructure_error (the platform failed; not the learner's fault)."""
    path: str
    kind: Literal["python", "sql"]
    status: Literal["success", "error", "timeout", "infrastructure_error"]
    stdout: str
    stderr: str
    execution_ms: int
    generated_files: list[GeneratedFile] = []
    table: Optional[TablePreview] = None
    error: Optional[RunError] = None
    # Output beyond the project's limit was cut; the UI says so.
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    # The run generated more files than are returned (and kept).
    artifacts_truncated: bool = False


class CheckRequest(BaseModel):
    language: Literal["en", "ar"] = "en"


class CheckItem(BaseModel):
    id: str
    passed: bool
    # Not run yet: it depends on the checks above passing first.
    pending: bool = False
    label: Optional[str] = None
    labels: Optional[dict[str, str]] = None
    message: Optional[str] = None
    messages: Optional[dict[str, str]] = None


class CheckError(BaseModel):
    kind: Literal["execution", "infrastructure"]
    message: str
    messages: dict[str, str]


class CheckRunOutput(BaseModel):
    status: str
    stdout: str
    stderr: str


class CheckResponse(BaseModel):
    """outcome: pass | fail (the analysis is wrong) | error (the file could
    not run, or the platform failed — see error.kind)."""
    task: str
    outcome: Literal["pass", "fail", "error"]
    passed: bool
    checks: list[CheckItem]
    error: Optional[CheckError] = None
    run: Optional[CheckRunOutput] = None
    newly_completed: bool
    task_status: str
    progress: ProgressView


class ArtifactSummary(BaseModel):
    path: str
    media_type: str
    encoding: Literal["base64", "text"]
    size: int
    sha256: str
    updated_at: datetime


class ArtifactContent(ArtifactSummary):
    content: str


class SubmissionMilestone(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    completed: bool


class SubmissionArtifact(BaseModel):
    path: str
    media_type: str
    size: int


class SubmissionView(BaseModel):
    """The final-submission summary. `ready` is true once every task has
    passed; `submitted_at` is set by POST /submit. Portfolio publishing and
    certificates are out of scope and would extend this later."""
    submitted_at: Optional[datetime] = None
    ready: bool
    percent: int
    completed_tasks: int
    total_tasks: int
    milestones: list[SubmissionMilestone]
    skills: list[LocalizedHint]
    artifacts: list[SubmissionArtifact]


class CompletionTrack(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None


class CompletionProject(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    description: str
    description_ar: Optional[str] = None
    role: Optional[str] = None
    role_ar: Optional[str] = None
    difficulty: str
    duration_hours: Optional[list[int]] = None
    track: CompletionTrack


class CompletionMilestone(BaseModel):
    slug: str
    title: str
    title_ar: Optional[str] = None
    completed: bool
    completed_tasks: int
    total_tasks: int


class CompletionArtifact(BaseModel):
    path: str
    kind: Literal["report", "chart", "analysis", "sql", "notes"]
    media_type: str
    size: int
    updated_at: Optional[datetime] = None


class CompletionView(BaseModel):
    """Portfolio-ready project completion data (frozen at final submission).
    Lists the learner's artifacts by path only — never contents — and no
    validator data. Consumed by the completion page now, and by portfolio and
    certificate features later."""
    schema_version: int
    project: CompletionProject
    status: Literal["in_progress", "ready", "completed"]
    completed_tasks: int
    total_tasks: int
    percent: int
    completed_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    milestones: list[CompletionMilestone]
    skills: list[LocalizedHint]
    deliverables: list[LocalizedHint]
    artifacts: list[CompletionArtifact]
