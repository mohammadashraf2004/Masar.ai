"""Project Lab API (Challenges › Projects).

Deterministic and free: no LLM, no wallet. Learner code runs only through
ProjectExecutionService (never in this process). Every attempt route resolves
the attempt through service.owned_attempt, so a learner can only ever reach
their own workspace, and every file route canonicalises the requested path
and requires it to be a file the workspace actually has.

Run and Check Step hold the learner's execution lease (service.EXECUTION_GATE)
for their whole duration: a second Run/Check from the same learner while one
is in flight is refused with 409 EXECUTION_IN_PROGRESS rather than queued, so
one account can occupy at most one runner slot.
"""
from contextlib import asynccontextmanager
from types import SimpleNamespace

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.services.execution_fairness import runner_turn
from app.core.metrics import record_project_lab_check, record_project_lab_rejected
from app.core.security import get_current_user, get_optional_user
from app.db.session import get_db
from app.models.project_lab import LabAttempt, LabProject
from app.models.user import User
from app.services.project_lab import service
from app.services.project_lab.execution import ProjectExecutionService, get_execution_service
from app.views.project_lab import (
    ArtifactContent, ArtifactSummary, AttemptRef, AttemptView, CheckError, CheckItem, CheckRequest,
    CheckResponse, CheckRunOutput, CompletionView, FileView, FileWrite, MilestoneDetail, MilestoneSummary,
    PathRequest, ProgressView, ProjectCard, ProjectDetail, ProjectOverview, RunResponse, StartResponse,
    SubmissionView, TaskDetail, TaskSummary, TrackRef, WorkspaceView,
)

router = APIRouter(prefix="/project-lab", tags=["Project Lab"])


# ─── Presenters ──────────────────────────────────────────────────────────────

def _attempt_ref(db: Session, attempt: LabAttempt | None) -> AttemptRef | None:
    if attempt is None:
        return None
    progress = service.progress_summary(db, attempt)
    return AttemptRef(id=attempt.id, status=attempt.status, percent=progress["percent"],
                      completed_tasks=progress["completed_tasks"], total_tasks=progress["total_tasks"],
                      submitted_at=attempt.submitted_at)


def _card(db: Session, project: LabProject, attempt: LabAttempt | None) -> dict:
    return dict(
        slug=project.slug, title=project.title, title_ar=project.title_ar,
        summary=project.summary, summary_ar=project.summary_ar, difficulty=project.difficulty,
        estimated_hours=project.estimated_hours,
        track=TrackRef(slug=project.track.slug, title=project.track.title, title_ar=project.track.title_ar),
        milestone_count=len(project.milestones),
        task_count=len(service.ordered_tasks(project)),
        attempt=_attempt_ref(db, attempt),
    )


def _attempt_view(db: Session, attempt: LabAttempt) -> AttemptView:
    project = attempt.project
    return AttemptView(
        id=attempt.id, status=attempt.status, started_at=attempt.started_at, submitted_at=attempt.submitted_at,
        project=ProjectCard(**_card(db, project, attempt)),
        milestones=[
            MilestoneDetail(
                slug=m.slug, title=m.title, title_ar=m.title_ar, summary=m.summary, summary_ar=m.summary_ar,
                tasks=[TaskDetail(
                    slug=t.slug, title=t.title, title_ar=t.title_ar, instructions=t.instructions,
                    instructions_ar=t.instructions_ar, hints=t.hints or [], primary_file=t.primary_file,
                ) for t in m.tasks],
            )
            for m in project.milestones
        ],
        workspace_root=project.template_key,
        progress=ProgressView(**service.progress_summary(db, attempt)),
    )


# ─── Projects ────────────────────────────────────────────────────────────────

# The catalogue and the overview are public: they carry titles, summaries, the
# milestone/task outline and the overview card, never a task's instructions,
# hints, files or checks (those are AttemptView, reachable only through an
# attempt the caller owns). A signed-in learner also gets their own attempt.

@router.get("/projects", response_model=list[ProjectCard])
def list_projects(current_user: User | None = Depends(get_optional_user), db: Session = Depends(get_db)):
    projects = service.published_projects(db)
    attempts = (
        {a.project_id: a for a in db.query(LabAttempt).filter(LabAttempt.user_id == current_user.id)}
        if current_user else {}
    )
    return [ProjectCard(**_card(db, p, attempts.get(p.id))) for p in projects]


@router.get("/projects/{slug}", response_model=ProjectDetail)
def get_project(slug: str, current_user: User | None = Depends(get_optional_user), db: Session = Depends(get_db)):
    project = service.get_project(db, slug)
    attempt = service.find_attempt(db, current_user.id, project) if current_user else None
    return ProjectDetail(
        **_card(db, project, attempt),
        milestones=[
            MilestoneSummary(
                slug=m.slug, title=m.title, title_ar=m.title_ar, summary=m.summary, summary_ar=m.summary_ar,
                tasks=[TaskSummary(slug=t.slug, title=t.title, title_ar=t.title_ar) for t in m.tasks],
            )
            for m in project.milestones
        ],
        overview=ProjectOverview(**(project.overview or {})),
    )


@router.post("/projects/{slug}/start", response_model=StartResponse)
@limiter.limit("20/minute")
def start_project(
    request: Request, response: Response, slug: str,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Idempotent: 201 the first time, 200 with the same attempt afterwards.
    Free — starting a project does not touch the wallet."""
    project = service.get_project(db, slug)
    attempt, created = service.start_attempt(db, current_user.id, project)
    response.status_code = 201 if created else 200
    return StartResponse(attempt_id=attempt.id, created=created)


# ─── Attempt & workspace ─────────────────────────────────────────────────────

@router.get("/attempts/{attempt_id}", response_model=AttemptView)
def get_attempt(attempt_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _attempt_view(db, service.owned_attempt(db, attempt_id, current_user.id))


@router.get("/attempts/{attempt_id}/workspace", response_model=WorkspaceView)
def get_workspace(attempt_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return WorkspaceView(root=attempt.project.template_key, entries=service.workspace_entries(db, attempt))


@router.get("/attempts/{attempt_id}/files", response_model=FileView)
def get_file(
    attempt_id: int, path: str = Query(..., min_length=1, max_length=255),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.read_file(db, attempt, path)


@router.put("/attempts/{attempt_id}/files", response_model=FileView)
@limiter.limit("120/minute")
def put_file(
    request: Request, attempt_id: int, payload: FileWrite,
    path: str = Query(..., min_length=1, max_length=255),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.write_file(db, attempt, path, payload.content)


@router.post("/attempts/{attempt_id}/files/reset", response_model=FileView)
@limiter.limit("30/minute")
def reset_file(
    request: Request, attempt_id: int, payload: PathRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.reset_file(db, attempt, payload.path)


# ─── Execution ───────────────────────────────────────────────────────────────

@asynccontextmanager
async def _execution_lease(db: Session, user_id: int, attempt_id: int, action: str):
    """Hold the learner's single execution lease for the body, or refuse."""
    token = service.EXECUTION_GATE.acquire(db, user_id, attempt_id, action)
    if token is None:
        record_project_lab_rejected("concurrent")
        raise service.lab_error(409, "EXECUTION_IN_PROGRESS")
    try:
        # The runner is shared with code exercises: one job per account at a
        # time and a rolling share of runner time (execution_fairness).
        async with runner_turn(user_id):
            yield
    finally:
        service.EXECUTION_GATE.release(db, user_id, token)


@router.post("/attempts/{attempt_id}/run", response_model=RunResponse)
@limiter.limit("30/minute")
async def run_file(
    request: Request, attempt_id: int, payload: PathRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
    execution: ProjectExecutionService = Depends(get_execution_service),
):
    """Runs the SAVED file. Free: no credits are charged for execution, and
    a Run never changes task progress (only a passing Check Step does).
    Charts the run generates are kept as the attempt's artifacts."""
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    resolved = service.resolve_path(attempt, payload.path)
    if resolved.language not in {"python", "sql"} or not resolved.editable:
        raise service.lab_error(400, "NOT_RUNNABLE")
    async with _execution_lease(db, current_user.id, attempt.id, "run"):
        snap = service.snapshot(db, attempt)
        # End the read transaction before waiting on the runner (up to its
        # timeout, queue included): otherwise every execution in flight pins a
        # pooled connection, and once a worker's pool is exhausted the next
        # request blocks that worker's event loop inside pool checkout.
        db.commit()
        if resolved.language == "python":
            result = await execution.run_python(snap, resolved.path)
        else:
            result = await execution.run_sql(snap, resolved.path)
        service.record_run(db, attempt, resolved.path, resolved.language, result)
        if result.succeeded and result.generated_files:
            service.save_artifacts(db, attempt, result.generated_files)
    return RunResponse(
        path=resolved.path, kind=resolved.language, status=result.status, stdout=result.stdout,
        stderr=result.stderr, execution_ms=result.execution_ms, generated_files=result.generated_files,
        table=result.table, error=result.error, stdout_truncated=result.stdout_truncated,
        stderr_truncated=result.stderr_truncated, artifacts_truncated=result.artifacts_truncated,
    )


@router.post("/attempts/{attempt_id}/tasks/{task_slug}/check", response_model=CheckResponse)
@limiter.limit("20/minute")
async def check_task(
    request: Request, attempt_id: int, task_slug: str, payload: CheckRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
    execution: ProjectExecutionService = Depends(get_execution_service),
):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    task = service.find_task(attempt, task_slug)
    async with _execution_lease(db, current_user.id, attempt.id, "check"):
        saved = {a["path"]: a for a in service.artifacts(db, attempt)}
        snap, template = service.snapshot(db, attempt), service.template_for(attempt.project)
        # Validation reads only these two task fields; plain copies keep the
        # expired ORM row from reopening a transaction during the runner wait.
        spec = SimpleNamespace(validator_key=task.validator_key, validator_config=dict(task.validator_config or {}))
        db.commit()  # release the pooled connection while the runner works (see run_file)
        result = await execution.validate_task(snap, spec, template=template, artifacts=saved)
        newly_completed = service.apply_check(db, attempt, task, result)
        if result.artifacts:
            service.save_artifacts(db, attempt, result.artifacts)
    record_project_lab_check(result.outcome, result.error_kind)
    progress = service.progress_summary(db, attempt)
    lang = payload.language
    error = None
    if result.outcome == "error" and result.error_message:
        error = CheckError(kind=result.error_kind or "infrastructure", message=result.error_message[lang],
                           messages=result.error_message)
    run = None
    if result.run is not None and result.error_kind == "execution":
        # Only the learner's own output; captured values never leave the server.
        run = CheckRunOutput(status=result.run.status, stdout=result.run.stdout, stderr=result.run.stderr)
    return CheckResponse(
        task=task.slug, outcome=result.outcome, passed=result.passed,
        checks=[CheckItem(id=c.id, passed=c.passed, pending=c.pending,
                          label=c.label[lang] if c.label else None, labels=c.label,
                          message=c.message[lang] if c.message else None, messages=c.message)
                for c in result.checks],
        error=error, run=run, newly_completed=newly_completed,
        task_status=next(t["status"] for t in progress["tasks"] if t["slug"] == task.slug),
        progress=ProgressView(**progress),
    )


# ─── Artifacts ───────────────────────────────────────────────────────────────

@router.get("/attempts/{attempt_id}/artifacts", response_model=list[ArtifactSummary])
def list_artifacts(attempt_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Files the learner's code generated (charts), latest version per path."""
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.artifacts(db, attempt, with_content=False)


@router.get("/attempts/{attempt_id}/artifacts/content", response_model=ArtifactContent)
def get_artifact(
    attempt_id: int, path: str = Query(..., min_length=1, max_length=255),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    for artifact in service.artifacts(db, attempt):
        if artifact["path"] == path:
            return artifact
    raise service.lab_error(404, "ARTIFACT_NOT_FOUND")


# ─── Final submission ────────────────────────────────────────────────────────

@router.get("/attempts/{attempt_id}/submission", response_model=SubmissionView)
def get_submission(attempt_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.submission_summary(db, attempt)


@router.post("/attempts/{attempt_id}/submit", response_model=SubmissionView)
@limiter.limit("10/minute")
def submit_project(
    request: Request, attempt_id: int,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Final submission: 409 PROJECT_NOT_COMPLETE until every task has passed.
    Idempotent — repeating it keeps the first submission time."""
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.submit_attempt(db, attempt)


@router.get("/attempts/{attempt_id}/completion", response_model=CompletionView)
def get_completion(attempt_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """The completion summary: frozen at final submission, live before it."""
    attempt = service.owned_attempt(db, attempt_id, current_user.id)
    return service.completion(db, attempt)
