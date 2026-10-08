"""Project Lab application service: content sync, attempts, workspace files,
runs, checks and progress. Controllers stay thin; everything that touches
learner state goes through here.

Workspace model: an attempt stores ONLY the learner's editable files
(LabWorkspaceFile). Read-only files — the datasets and the README — are read
from the canonical template on every request and mounted by the runner, never
copied per learner.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import logging
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings

from app.models.learning import CareerTrack
from app.models.project_lab import (
    LabArtifact, LabAttempt, LabExecutionLease, LabMilestone, LabProject, LabRun, LabSubmission, LabTask,
    LabTaskProgress, LabWorkspaceFile,
)

from .execution import RunResult, WorkspaceSnapshot
from .templates import (
    ProjectTemplate, WorkspacePathError, canonical_path, is_read_only, language_for, load_template,
)
from .validation import ValidationResult, registered_validators

logger = logging.getLogger(__name__)

MAX_FILE_CHARS = 200_000


def lab_error(status: int, code: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code})


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─── Content ─────────────────────────────────────────────────────────────────

def sync_definitions(db: Session, definitions: list[dict]) -> dict[str, int]:
    """Upsert project definitions (idempotent). Tasks and milestones are
    matched by slug, so learner progress survives content edits. Removing a
    task from a definition does not delete it (that would delete learner
    progress). A task or milestone is deleted only when the definition
    retires its slug explicitly (retired_task_slugs / retired_milestone_slugs),
    which also deletes learner progress on it."""
    validators = registered_validators()
    report = {"projects": 0, "milestones": 0, "tasks": 0}
    for definition in definitions:
        track = db.query(CareerTrack).filter(CareerTrack.slug == definition["track_slug"]).first()
        if track is None:
            raise RuntimeError(
                f"career track {definition['track_slug']!r} does not exist; seed the career tracks first (seed.py)"
            )
        template = load_template(definition["template_key"])
        project = db.query(LabProject).filter(LabProject.slug == definition["slug"]).first()
        if project is None:
            project = LabProject(slug=definition["slug"])
            db.add(project)
            report["projects"] += 1
        for key in ("title", "title_ar", "summary", "summary_ar", "difficulty", "estimated_hours",
                    "template_key", "template_version", "read_only_paths", "position"):
            setattr(project, key, definition.get(key))
        project.track_id = track.id
        project.overview = definition.get("overview", {})
        project.is_published = definition.get("is_published", True)
        db.flush()

        task_slugs: set[str] = set()
        for m_index, m_def in enumerate(definition["milestones"], start=1):
            milestone = db.query(LabMilestone).filter_by(project_id=project.id, slug=m_def["slug"]).first()
            if milestone is None:
                milestone = LabMilestone(project_id=project.id, slug=m_def["slug"])
                db.add(milestone)
                report["milestones"] += 1
            milestone.position = m_index
            for key in ("title", "title_ar", "summary", "summary_ar"):
                setattr(milestone, key, m_def.get(key))
            milestone.skills = m_def.get("skills", [])
            db.flush()
            for t_index, t_def in enumerate(m_def["tasks"], start=1):
                if t_def["slug"] in task_slugs:
                    raise RuntimeError(f"duplicate task slug {t_def['slug']!r} in {definition['slug']}")
                task_slugs.add(t_def["slug"])
                if t_def["validator_key"] not in validators:
                    raise RuntimeError(f"task {t_def['slug']!r} names unknown validator {t_def['validator_key']!r}")
                primary = t_def.get("primary_file")
                if primary and primary not in template.files:
                    raise RuntimeError(f"task {t_def['slug']!r} opens {primary!r}, which is not in the template")
                task = db.query(LabTask).filter_by(project_id=project.id, slug=t_def["slug"]).first()
                if task is None:
                    task = LabTask(project_id=project.id, slug=t_def["slug"])
                    db.add(task)
                    report["tasks"] += 1
                task.milestone_id = milestone.id
                task.position = t_index
                for key in ("title", "title_ar", "instructions", "instructions_ar", "primary_file",
                            "validator_key"):
                    setattr(task, key, t_def.get(key))
                task.hints = t_def.get("hints", [])
                task.validator_config = t_def.get("validator_config", {})
        db.flush()
        retired_tasks = set(definition.get("retired_task_slugs", [])) - task_slugs
        if retired_tasks:
            for task in db.query(LabTask).filter(LabTask.project_id == project.id, LabTask.slug.in_(retired_tasks)):
                db.delete(task)
        live_milestones = {m["slug"] for m in definition["milestones"]}
        retired_milestones = set(definition.get("retired_milestone_slugs", [])) - live_milestones
        if retired_milestones:
            for milestone in db.query(LabMilestone).filter(LabMilestone.project_id == project.id,
                                                           LabMilestone.slug.in_(retired_milestones)):
                db.delete(milestone)  # its tasks were moved or retired above
        db.flush()
    db.commit()
    return report


def published_projects(db: Session) -> list[LabProject]:
    return (
        db.query(LabProject)
        .options(selectinload(LabProject.track), selectinload(LabProject.milestones).selectinload(LabMilestone.tasks))
        .filter(LabProject.is_published.is_(True))
        .order_by(LabProject.position, LabProject.id)
        .all()
    )


def get_project(db: Session, slug: str) -> LabProject:
    project = (
        db.query(LabProject)
        .options(selectinload(LabProject.track), selectinload(LabProject.milestones).selectinload(LabMilestone.tasks))
        .filter(LabProject.slug == slug, LabProject.is_published.is_(True))
        .first()
    )
    if project is None:
        raise lab_error(404, "PROJECT_NOT_FOUND")
    return project


def ordered_tasks(project: LabProject) -> list[LabTask]:
    return [task for milestone in project.milestones for task in milestone.tasks]


def template_for(project: LabProject) -> ProjectTemplate:
    return load_template(project.template_key)


# ─── Attempts ────────────────────────────────────────────────────────────────

def _ensure_task_rows(db: Session, attempt: LabAttempt, project: LabProject) -> None:
    """One progress row per task — also for tasks authored after the attempt
    started. Rows are what Check Step locks, so they must exist first."""
    existing = {row.task_id for row in db.query(LabTaskProgress.task_id).filter_by(attempt_id=attempt.id)}
    for task in ordered_tasks(project):
        if task.id not in existing:
            db.add(LabTaskProgress(attempt_id=attempt.id, task_id=task.id, status="not_started", check_count=0))


def _ensure_files(db: Session, attempt: LabAttempt, project: LabProject) -> None:
    """Create the learner copy of every editable template file that the
    attempt does not have yet (a file added to the template later)."""
    template = template_for(project)
    present = {row.path for row in db.query(LabWorkspaceFile.path).filter_by(attempt_id=attempt.id)}
    for path in template.files:
        if path not in present and not is_read_only(path, project.read_only_paths):
            db.add(LabWorkspaceFile(attempt_id=attempt.id, path=path, content=template.read_text(path)))


def find_attempt(db: Session, user_id: int, project: LabProject) -> LabAttempt | None:
    return db.query(LabAttempt).filter_by(user_id=user_id, project_id=project.id).first()


def start_attempt(db: Session, user_id: int, project: LabProject) -> tuple[LabAttempt, bool]:
    """Idempotent: a learner has one workspace per project. Starting again
    returns the existing attempt untouched (created=False). Concurrent starts
    are settled by the unique (user_id, project_id) constraint."""
    existing = find_attempt(db, user_id, project)
    if existing is not None:
        return existing, False
    attempt = LabAttempt(user_id=user_id, project_id=project.id, status="active",
                         template_version=project.template_version)
    db.add(attempt)
    try:
        db.flush()
        _ensure_files(db, attempt, project)
        _ensure_task_rows(db, attempt, project)
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = find_attempt(db, user_id, project)
        if existing is None:
            raise
        return existing, False
    db.refresh(attempt)
    return attempt, True


def owned_attempt(db: Session, attempt_id: int, user_id: int) -> LabAttempt:
    """The attempt, only if it belongs to this user. Someone else's attempt is
    reported exactly like a missing one, so ids cannot be probed."""
    attempt = db.query(LabAttempt).filter(LabAttempt.id == attempt_id, LabAttempt.user_id == user_id).first()
    if attempt is None:
        raise lab_error(404, "ATTEMPT_NOT_FOUND")
    project = get_project(db, attempt.project.slug)
    # Content added since the attempt started appears without a restart.
    _ensure_files(db, attempt, project)
    _ensure_task_rows(db, attempt, project)
    if attempt.status == "completed" and db.new:
        # New tasks were authored after this attempt finished: it is active
        # again until they pass too (a final submission, if any, stays dated).
        attempt.status = "active"
        attempt.completed_at = None
    if db.new or db.dirty:
        db.commit()
    return attempt


# ─── Workspace files ─────────────────────────────────────────────────────────

@dataclass
class ResolvedFile:
    path: str
    editable: bool
    language: str


def resolve_path(attempt: LabAttempt, raw: str) -> ResolvedFile:
    """Canonicalise a requested path and require it to be a file this
    workspace has. Unknown files are 404; malformed paths are 400."""
    try:
        path = canonical_path(raw)
    except WorkspacePathError:
        raise lab_error(400, "INVALID_PATH")
    project = attempt.project
    template = template_for(project)
    if path not in template.files:
        raise lab_error(404, "FILE_NOT_FOUND")
    return ResolvedFile(path, not is_read_only(path, project.read_only_paths), language_for(path))


def _learner_file(db: Session, attempt: LabAttempt, path: str) -> LabWorkspaceFile:
    row = db.query(LabWorkspaceFile).filter_by(attempt_id=attempt.id, path=path).first()
    if row is None:  # created lazily by owned_attempt; absent only on a race
        row = LabWorkspaceFile(attempt_id=attempt.id, path=path,
                               content=template_for(attempt.project).read_text(path))
        db.add(row)
        db.flush()
    return row


def workspace_entries(db: Session, attempt: LabAttempt) -> list[dict]:
    project = attempt.project
    template = template_for(project)
    learner = {row.path: row for row in db.query(LabWorkspaceFile).filter_by(attempt_id=attempt.id)}
    entries = [{"path": d, "kind": "dir", "language": None, "editable": False, "size": None, "modified": False}
               for d in template.dirs]
    for path, meta in template.files.items():
        editable = not is_read_only(path, project.read_only_paths)
        row = learner.get(path) if editable else None
        content = row.content if row is not None else None
        entries.append({
            "path": path, "kind": "file", "language": meta.language, "editable": editable,
            "size": len(content.encode("utf-8")) if content is not None else meta.size,
            "modified": bool(row is not None and content != template.read_text(path)),
        })
    return sorted(entries, key=lambda e: e["path"])


def read_file(db: Session, attempt: LabAttempt, raw_path: str) -> dict:
    resolved = resolve_path(attempt, raw_path)
    template = template_for(attempt.project)
    view = {"path": resolved.path, "language": resolved.language, "editable": resolved.editable,
            "content": None, "table": None}
    if resolved.editable:
        view["content"] = _learner_file(db, attempt, resolved.path).content
    elif resolved.language == "csv":
        view["table"] = template.csv_preview(resolved.path)
    else:
        view["content"] = template.read_text(resolved.path)
    return view


def write_file(db: Session, attempt: LabAttempt, raw_path: str, content: str) -> dict:
    resolved = resolve_path(attempt, raw_path)
    if not resolved.editable:
        raise lab_error(403, "READ_ONLY_FILE")
    if len(content) > MAX_FILE_CHARS:
        raise lab_error(413, "FILE_TOO_LARGE")
    row = _learner_file(db, attempt, resolved.path)
    others = sum(
        len((other or "").encode("utf-8"))
        for (other,) in db.query(LabWorkspaceFile.content)
        .filter(LabWorkspaceFile.attempt_id == attempt.id, LabWorkspaceFile.path != resolved.path)
    )
    if others + len(content.encode("utf-8")) > settings.PROJECT_LAB_MAX_WORKSPACE_BYTES:
        raise lab_error(413, "WORKSPACE_TOO_LARGE")
    row.content = content
    attempt.updated_at = _now()
    db.commit()
    return read_file(db, attempt, resolved.path)


def reset_file(db: Session, attempt: LabAttempt, raw_path: str) -> dict:
    """Restore ONE editable file to the template version. Nothing else in the
    workspace or in task progress changes."""
    resolved = resolve_path(attempt, raw_path)
    if not resolved.editable:
        raise lab_error(403, "READ_ONLY_FILE")
    row = _learner_file(db, attempt, resolved.path)
    row.content = template_for(attempt.project).read_text(resolved.path)
    db.commit()
    return read_file(db, attempt, resolved.path)


def snapshot(db: Session, attempt: LabAttempt) -> WorkspaceSnapshot:
    """The saved state a run or check executes. Unsaved editor changes are
    not included; the lab saves before it runs."""
    template = template_for(attempt.project)
    files = {row.path: row.content for row in db.query(LabWorkspaceFile).filter_by(attempt_id=attempt.id)}
    return WorkspaceSnapshot(template_key=template.key, files=files, dirs=list(template.dirs))


# ─── Runs, checks, progress ──────────────────────────────────────────────────

def record_run(db: Session, attempt: LabAttempt, path: str, kind: str, result: RunResult) -> None:
    db.add(LabRun(attempt_id=attempt.id, path=path, kind=kind, status=result.status,
                  execution_ms=result.execution_ms))
    db.commit()


def find_task(attempt: LabAttempt, task_slug: str) -> LabTask:
    for task in ordered_tasks(attempt.project):
        if task.slug == task_slug:
            return task
    raise lab_error(404, "TASK_NOT_FOUND")


def apply_check(db: Session, attempt: LabAttempt, task: LabTask, result: ValidationResult) -> bool:
    """Record a Check Step and update progress. Returns True only the first
    time the task becomes completed: a repeated pass changes nothing but the
    check counter, so progress (and anything ever attached to completion)
    cannot be earned twice. The progress row is locked so two concurrent
    passing checks cannot both count as first."""
    progress = (
        db.query(LabTaskProgress)
        .filter_by(attempt_id=attempt.id, task_id=task.id)
        .with_for_update()
        .first()
    )
    if progress is None:
        progress = LabTaskProgress(attempt_id=attempt.id, task_id=task.id, status="not_started", check_count=0)
        db.add(progress)
        db.flush()
    progress.check_count = (progress.check_count or 0) + 1
    progress.last_outcome = result.outcome
    progress.last_checked_at = _now()
    newly_completed = False
    if result.passed and progress.status != "completed":
        progress.status = "completed"
        progress.completed_at = _now()
        newly_completed = True
    elif progress.status == "not_started":
        progress.status = "in_progress"
    db.add(LabSubmission(
        attempt_id=attempt.id, task_id=task.id, outcome=result.outcome,
        checks=[c.public() for c in result.checks], error_kind=result.error_kind,
        execution_ms=result.execution_ms,
    ))
    db.flush()
    if newly_completed:
        total = len(ordered_tasks(attempt.project))
        done = db.query(LabTaskProgress).filter_by(attempt_id=attempt.id, status="completed").count()
        if done >= total and attempt.status != "completed":
            attempt.status = "completed"
            attempt.completed_at = _now()
    db.commit()
    return newly_completed


def progress_summary(db: Session, attempt: LabAttempt) -> dict:
    rows = {row.task_id: row for row in db.query(LabTaskProgress).filter_by(attempt_id=attempt.id)}
    tasks_out, milestones_out = [], []
    current = None
    completed_total = 0
    for milestone in attempt.project.milestones:
        done = 0
        for task in milestone.tasks:
            row = rows.get(task.id)
            status = row.status if row else "not_started"
            if status == "completed":
                done += 1
            elif current is None:
                current = task.slug
            tasks_out.append({
                "slug": task.slug, "milestone": milestone.slug, "status": status,
                "check_count": row.check_count if row else 0,
                "last_outcome": row.last_outcome if row else None,
                "completed_at": row.completed_at if row else None,
            })
        total = len(milestone.tasks)
        completed_total += done
        milestones_out.append({"slug": milestone.slug, "completed_tasks": done, "total_tasks": total,
                               "percent": round(100 * done / total) if total else 0})
    total_tasks = len(tasks_out)
    return {
        "status": attempt.status,
        "completed_tasks": completed_total,
        "total_tasks": total_tasks,
        "percent": round(100 * completed_total / total_tasks) if total_tasks else 0,
        "current_task": current,
        "milestones": milestones_out,
        "tasks": tasks_out,
    }


# ─── Concurrency ─────────────────────────────────────────────────────────────

class ExecutionGate:
    """One running execution (Run or Check Step) per learner, enforced across
    every API worker by a row in lab_execution_leases.

    acquire() is a single atomic upsert: it inserts the learner's lease, or
    takes over an EXPIRED one, and otherwise changes nothing. It returns a
    token only if this call now owns the lease. release() deletes the lease
    only if the token still matches. A worker that dies mid-run leaves a lease
    that simply expires (PROJECT_LAB_EXECUTION_LEASE_SECONDS), so state
    recovers on its own. The API around it does not depend on how the lease
    is stored: a Redis SET NX PX lock can replace this class unchanged."""

    def acquire(self, db: Session, user_id: int, attempt_id: int, action: str) -> str | None:
        token = secrets.token_hex(16)
        ttl = timedelta(seconds=settings.PROJECT_LAB_EXECUTION_LEASE_SECONDS)
        statement = pg_insert(LabExecutionLease).values(
            user_id=user_id, attempt_id=attempt_id, token=token, action=action,
            started_at=func.now(), expires_at=func.now() + ttl,
        )
        statement = statement.on_conflict_do_update(
            index_elements=[LabExecutionLease.user_id],
            set_={"attempt_id": statement.excluded.attempt_id, "token": statement.excluded.token,
                  "action": statement.excluded.action, "started_at": statement.excluded.started_at,
                  "expires_at": statement.excluded.expires_at},
            where=LabExecutionLease.expires_at < func.now(),
        ).returning(LabExecutionLease.token)
        row = db.execute(statement).first()
        db.commit()
        return token if row is not None and row[0] == token else None

    def release(self, db: Session, user_id: int, token: str) -> None:
        try:
            db.rollback()  # whatever the request left half-done must not block the release
            db.query(LabExecutionLease).filter_by(user_id=user_id, token=token).delete()
            db.commit()
        except Exception:  # noqa: BLE001 - an unreleased lease still expires
            logger.exception("could not release a Project Lab execution lease")
            db.rollback()


EXECUTION_GATE = ExecutionGate()


# ─── Artifacts ───────────────────────────────────────────────────────────────

MAX_ARTIFACTS_PER_ATTEMPT = 30


def save_artifacts(db: Session, attempt: LabAttempt, generated: list[dict]) -> None:
    """Keep the latest version of each generated chart/text file. Content was
    already bounded and type-checked by the execution service."""
    existing = {row.path: row for row in db.query(LabArtifact).filter_by(attempt_id=attempt.id)}
    for item in generated:
        if item.get("content") is None or item.get("encoding") not in {"base64", "text"}:
            continue
        try:
            raw = (base64.b64decode(item["content"], validate=True) if item["encoding"] == "base64"
                   else item["content"].encode("utf-8"))
        except (binascii.Error, ValueError):
            continue
        row = existing.get(item["path"])
        if row is None:
            if len(existing) >= MAX_ARTIFACTS_PER_ATTEMPT:
                continue
            row = LabArtifact(attempt_id=attempt.id, path=item["path"])
            db.add(row)
            existing[item["path"]] = row
        row.media_type = item["media_type"]
        row.encoding = item["encoding"]
        row.content = item["content"]
        row.size = len(raw)
        row.sha256 = hashlib.sha256(raw).hexdigest()
        row.updated_at = _now()
    db.commit()


def artifacts(db: Session, attempt: LabAttempt, *, with_content: bool = True) -> list[dict]:
    rows = db.query(LabArtifact).filter_by(attempt_id=attempt.id).order_by(LabArtifact.path)
    return [{
        "path": row.path, "media_type": row.media_type, "encoding": row.encoding, "size": row.size,
        "sha256": row.sha256, "updated_at": row.updated_at,
        "content": row.content if with_content else None,
    } for row in rows]


# ─── Final submission ────────────────────────────────────────────────────────

def submission_summary(db: Session, attempt: LabAttempt) -> dict:
    progress = progress_summary(db, attempt)
    done = {m["slug"]: m for m in progress["milestones"]}
    milestones, skills, seen = [], [], set()
    for milestone in attempt.project.milestones:
        complete = done[milestone.slug]["completed_tasks"] == done[milestone.slug]["total_tasks"]
        milestones.append({"slug": milestone.slug, "title": milestone.title, "title_ar": milestone.title_ar,
                           "completed": complete})
        if complete:
            for skill in milestone.skills or []:
                if skill.get("en") not in seen:
                    seen.add(skill.get("en"))
                    skills.append(skill)
    return {
        "submitted_at": attempt.submitted_at,
        "ready": progress["completed_tasks"] == progress["total_tasks"] and progress["total_tasks"] > 0,
        "percent": progress["percent"],
        "completed_tasks": progress["completed_tasks"],
        "total_tasks": progress["total_tasks"],
        "milestones": milestones,
        "skills": skills,
        "artifacts": [{k: a[k] for k in ("path", "media_type", "size")} for a in artifacts(db, attempt, with_content=False)],
    }


COMPLETION_SCHEMA_VERSION = 1


def _artifact_kind(path: str) -> str:
    if path.startswith("charts/"):
        return "chart"
    if path == "report.md":
        return "report"
    if path.endswith(".sql"):
        return "sql"
    if path.endswith(".py"):
        return "analysis"
    return "notes"


def completion_summary(db: Session, attempt: LabAttempt) -> dict:
    """Portfolio-ready summary of an attempt (schema_version 1).

    What a later portfolio or certificate feature needs — project, role,
    demonstrated skills, deliverables, dates, milestone completion and the
    learner's artifacts — and nothing it must not show: artifacts are listed
    by path, kind and size only (no file contents, no validator data), and
    only files the learner actually changed from the template are included.
    """
    project = attempt.project
    overview = project.overview or {}
    progress = progress_summary(db, attempt)
    counts = {m["slug"]: m for m in progress["milestones"]}
    milestones, skills, seen = [], [], set()
    for milestone in project.milestones:
        count = counts[milestone.slug]
        complete = count["total_tasks"] > 0 and count["completed_tasks"] == count["total_tasks"]
        milestones.append({"slug": milestone.slug, "title": milestone.title, "title_ar": milestone.title_ar,
                           "completed": complete, "completed_tasks": count["completed_tasks"],
                           "total_tasks": count["total_tasks"]})
        if complete:
            for item in milestone.skills or []:
                if item.get("en") not in seen:
                    seen.add(item.get("en"))
                    skills.append(item)
    template = template_for(project)
    files = []
    for row in db.query(LabWorkspaceFile).filter_by(attempt_id=attempt.id).order_by(LabWorkspaceFile.path):
        if row.path in template.files and row.content != template.read_text(row.path):
            files.append({"path": row.path, "kind": _artifact_kind(row.path), "media_type": "text/plain",
                          "size": len(row.content.encode("utf-8")), "updated_at": row.updated_at})
    charts = [{"path": a["path"], "kind": "chart", "media_type": a["media_type"], "size": a["size"],
               "updated_at": a["updated_at"]} for a in artifacts(db, attempt, with_content=False)]
    all_done = progress["total_tasks"] > 0 and progress["completed_tasks"] == progress["total_tasks"]
    return {
        "schema_version": COMPLETION_SCHEMA_VERSION,
        "project": {
            "slug": project.slug, "title": project.title, "title_ar": project.title_ar,
            "description": project.summary, "description_ar": project.summary_ar,
            "role": overview.get("role"), "role_ar": overview.get("role_ar"),
            "difficulty": project.difficulty, "duration_hours": overview.get("duration_hours"),
            "track": {"slug": project.track.slug, "title": project.track.title, "title_ar": project.track.title_ar},
        },
        "status": "completed" if attempt.submitted_at else ("ready" if all_done else "in_progress"),
        "completed_tasks": progress["completed_tasks"],
        "total_tasks": progress["total_tasks"],
        "percent": progress["percent"],
        "completed_at": attempt.completed_at,
        "submitted_at": attempt.submitted_at,
        "milestones": milestones,
        "skills": skills,
        "deliverables": overview.get("deliverables", []),
        "artifacts": ([item for item in files if item["kind"] == "report"] + charts
                      + [item for item in files if item["kind"] != "report"]),
    }


def _jsonable(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def completion(db: Session, attempt: LabAttempt) -> dict:
    """The frozen snapshot once submitted, otherwise the live summary."""
    if attempt.submitted_at is not None and attempt.completion:
        return attempt.completion
    return _jsonable(completion_summary(db, attempt))


def submit_attempt(db: Session, attempt: LabAttempt) -> dict:
    """Final submission. Allowed only when every task has passed its check;
    repeating it keeps the first submission time. Portfolio publishing and
    certificates are deliberately not part of this phase: they would hang off
    lab_attempts.submitted_at."""
    progress = progress_summary(db, attempt)
    if progress["total_tasks"] == 0 or progress["completed_tasks"] < progress["total_tasks"]:
        raise lab_error(409, "PROJECT_NOT_COMPLETE")
    if attempt.submitted_at is None:
        attempt.submitted_at = _now()
        db.flush()
        attempt.completion = _jsonable(completion_summary(db, attempt))
        db.commit()
    return submission_summary(db, attempt)
