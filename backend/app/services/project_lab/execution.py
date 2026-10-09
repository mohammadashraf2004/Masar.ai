"""ProjectExecutionService: the one way Project Lab code gets executed.

Learner code is untrusted and NEVER runs in the API process. The service
builds a job (the learner's saved editable files + which template's datasets
to mount) and hands it to an ExecutionBackend:

* RunnerServiceBackend — POSTs the job over a Unix socket to the isolated
  project-runner service (backend/project_runner, `project-runner` in
  docker-compose.yml). This is the only backend that is a security boundary:
  separate container with no network at all, no secrets, read-only
  filesystem, restrictive seccomp profile, only SETUID/SETGID capabilities,
  unprivileged per-job uid, CPU/memory/process/file-size limits, one job at a
  time, and (where the host supports it) gVisor. See docs/project-lab.md.
* LocalSubprocessBackend — the same harness and rlimits in a child process
  of the API, as the API's own user. Development and tests only; config.py
  refuses it in production. It is NOT a sandbox: the child can read what the
  API user can read and reach whatever the API can reach.
* DisabledBackend — every run reports infrastructure_error.

Nothing that calls this service knows which backend is in use, and nothing
here charges credits: project execution is free.

Everything a backend returns is treated as untrusted data: it is shape-checked
here, and validators compare it with expected values that are computed in the
API and never sent to the sandbox.
"""
from __future__ import annotations

import asyncio
import base64
import binascii
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import httpx

from app.core.config import settings
from app.core.metrics import record_project_lab_execution
from project_runner.executor import JobOutcome, Limits, execute_job

from .templates import TEMPLATES_ROOT

if TYPE_CHECKING:
    from .validation import ValidationResult

logger = logging.getLogger(__name__)

RUN_STATUSES = ("success", "error", "timeout", "infrastructure_error")
_ARTIFACT_TYPES = {"image/png", "image/jpeg", "text/plain"}
_ARTIFACT_PATH = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-/]{0,200}$")
MAX_ARTIFACT_BYTES = 2 * 1024 * 1024


@dataclass
class WorkspaceSnapshot:
    """What a run sees: the learner's saved editable files plus the template
    whose read-only datasets are mounted alongside them."""
    template_key: str
    files: dict[str, str]
    dirs: list[str] = field(default_factory=list)


@dataclass
class RunResult:
    status: str
    stdout: str = ""
    stderr: str = ""
    execution_ms: int = 0
    generated_files: list[dict] = field(default_factory=list)
    table: dict | None = None
    error: dict | None = None
    # Values captured for validators. Never returned to the learner.
    captured: dict[str, Any] = field(default_factory=dict)
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    artifacts_truncated: bool = False

    @property
    def succeeded(self) -> bool:
        return self.status == "success"


class ExecutionBackend(ABC):
    name = "abstract"

    @abstractmethod
    async def execute(self, job: dict) -> JobOutcome:
        raise NotImplementedError


class DisabledBackend(ExecutionBackend):
    name = "disabled"

    async def execute(self, job: dict) -> JobOutcome:
        return JobOutcome("infrastructure_error", stderr="Project execution is not available right now.")


class LocalSubprocessBackend(ExecutionBackend):
    """Development/test adapter. NOT a sandbox — see the module docstring."""
    name = "local"

    def __init__(self, *, timeout_seconds: float, memory_mb: int, templates_root: str = str(TEMPLATES_ROOT)):
        self.templates_root = templates_root
        self.limits = Limits(timeout_seconds=timeout_seconds, cpu_seconds=max(1, int(timeout_seconds)),
                             memory_mb=memory_mb)

    async def execute(self, job: dict) -> JobOutcome:
        return await asyncio.to_thread(execute_job, job, templates_root=self.templates_root, limits=self.limits)


class RunnerServiceBackend(ExecutionBackend):
    """The project-runner service, over its Unix socket. The runner container
    has no network interface besides loopback, so a socket on a shared volume
    is the only way in, and learner code inside it cannot reach that socket
    (see backend/project_runner/server.py)."""
    name = "runner"
    _BASE = "http://project-runner"  # the host part is ignored on a Unix socket

    def __init__(self, *, socket_path: str, token: str, timeout_seconds: float, require_gvisor: bool = False):
        self.socket_path = socket_path
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.require_gvisor = require_gvisor
        self._runtime_checked_at: float | None = None

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(uds=self.socket_path), timeout=self.timeout_seconds,
            headers={"Authorization": f"Bearer {self.token}"},
        )

    async def _runtime_ok(self, client: httpx.AsyncClient) -> bool:
        """With PROJECT_LAB_REQUIRE_GVISOR, confirm (re-checked every minute)
        that the runner reports gVisor before giving it learner code."""
        checked = self._runtime_checked_at
        if not self.require_gvisor or (checked is not None and time.monotonic() - checked < 60):
            return True
        response = await client.get(f"{self._BASE}/healthz")
        raw = response.json() if response.status_code == 200 else {}
        data = raw if isinstance(raw, dict) else {}
        runtime = data.get("runtime")
        if data.get("ok") is not True or runtime != "gvisor":
            logger.error(
                "project runner health/runtime attestation failed (HTTP %s, runtime %r)",
                response.status_code,
                runtime,
            )
            return False
        self._runtime_checked_at = time.monotonic()
        return True

    async def assert_ready(self, *, wait_seconds: float = 0) -> None:
        """Prove that the configured runner is reachable and is really gVisor.

        Production calls this during application startup.  A short retry
        window tolerates the runner and API containers starting together;
        an explicit non-gVisor response fails immediately.  No Docker socket
        is mounted into the API: Docker runtime registration is checked by
        the host verification script, while this attests the effective
        runtime from inside the running sandbox.
        """
        deadline = time.monotonic() + max(0.0, wait_seconds)
        last_error: Exception | None = None
        while True:
            try:
                async with self._client() as client:
                    response = await client.get(f"{self._BASE}/healthz")
                raw = response.json() if response.status_code == 200 else {}
                data = raw if isinstance(raw, dict) else {}
                runtime = data.get("runtime")
                if response.status_code == 200 and data.get("ok") is True and runtime == "gvisor":
                    self._runtime_checked_at = time.monotonic()
                    return
                if runtime is not None and runtime != "gvisor":
                    raise RuntimeError(
                        f"project runner attested runtime {runtime!r}, not required runtime 'gvisor'"
                    )
                last_error = RuntimeError(
                    f"project runner readiness returned HTTP {response.status_code} without a gVisor attestation"
                )
            except RuntimeError:
                raise
            except (httpx.HTTPError, OSError, ValueError) as exc:
                last_error = exc
            if time.monotonic() >= deadline:
                raise RuntimeError(
                    "project runner is unavailable; production learner execution requires a live gVisor attestation"
                ) from last_error
            await asyncio.sleep(min(1.0, max(0.0, deadline - time.monotonic())))

    async def execute(self, job: dict) -> JobOutcome:
        try:
            async with self._client() as client:
                if not await self._runtime_ok(client):
                    return JobOutcome("infrastructure_error", stderr="Project execution is not available right now.")
                response = await client.post(f"{self._BASE}/v1/jobs", json={"job": job})
        except (httpx.HTTPError, OSError, ValueError) as exc:
            logger.warning("project runner unreachable: %s", type(exc).__name__)
            return JobOutcome("infrastructure_error", stderr="The project runner is unavailable. Try again shortly.")
        if response.status_code == 503:
            return JobOutcome("infrastructure_error", stderr="The project runner is busy. Try again in a moment.")
        if response.status_code != 200:
            logger.error("project runner returned HTTP %s", response.status_code)
            return JobOutcome("infrastructure_error", stderr="The project runner failed.")
        try:
            data = response.json()
        except ValueError:
            return JobOutcome("infrastructure_error", stderr="The project runner returned an invalid result.")
        if not isinstance(data, dict):
            return JobOutcome("infrastructure_error", stderr="The project runner returned an invalid result.")
        return JobOutcome(
            status=data.get("status", "infrastructure_error"),
            stdout=data.get("stdout") or "", stderr=data.get("stderr") or "",
            execution_ms=data.get("execution_ms") or 0, error=data.get("error"),
            captured=data.get("captured") or {}, table=data.get("table"),
            generated_files=data.get("generated_files") or [],
            stdout_truncated=bool(data.get("stdout_truncated")), stderr_truncated=bool(data.get("stderr_truncated")),
            artifacts_truncated=bool(data.get("artifacts_truncated")),
        )


def build_backend() -> ExecutionBackend:
    backend = settings.project_lab_backend
    if backend == "runner":
        return RunnerServiceBackend(
            socket_path=settings.PROJECT_LAB_RUNNER_SOCKET, token=settings.PROJECT_LAB_RUNNER_TOKEN,
            timeout_seconds=settings.PROJECT_LAB_RUNNER_TIMEOUT_SECONDS,
            require_gvisor=settings.PROJECT_LAB_REQUIRE_GVISOR,
        )
    if backend == "local" and not settings.is_production:
        return LocalSubprocessBackend(
            timeout_seconds=settings.PROJECT_LAB_LOCAL_TIMEOUT_SECONDS,
            memory_mb=settings.PROJECT_LAB_LOCAL_MEMORY_MB,
        )
    return DisabledBackend()


async def verify_production_runner(*, wait_seconds: float = 30.0) -> None:
    """Fail application startup unless an enabled production runner is gVisor.

    Disabled production execution deliberately returns without contacting a
    runner, so the rest of Masar can start safely during installation,
    incidents, and rollback.
    """
    if not settings.is_production or settings.project_lab_backend == "disabled":
        return
    backend = build_backend()
    if not isinstance(backend, RunnerServiceBackend) or not backend.require_gvisor:
        raise RuntimeError("production learner execution has no enforced gVisor runner")
    await backend.assert_ready(wait_seconds=wait_seconds)


def _clean_artifacts(raw: Any) -> list[dict]:
    """Keep only well-formed, bounded artifacts of allowed types."""
    cleaned: list[dict] = []
    for item in raw if isinstance(raw, list) else []:
        if not isinstance(item, dict) or len(cleaned) >= 10:
            continue
        path = item.get("path")
        if not isinstance(path, str) or not _ARTIFACT_PATH.match(path) or ".." in path.split("/"):
            continue
        media_type, encoding, content = item.get("media_type"), item.get("encoding"), item.get("content")
        entry = {"path": path, "size": int(item.get("size") or 0), "media_type": None, "encoding": None, "content": None}
        if media_type in _ARTIFACT_TYPES and isinstance(content, str):
            if encoding == "base64" and media_type.startswith("image/"):
                try:
                    if len(base64.b64decode(content, validate=True)) <= MAX_ARTIFACT_BYTES:
                        entry.update(media_type=media_type, encoding="base64", content=content)
                except (binascii.Error, ValueError):
                    pass
            elif encoding == "text" and media_type == "text/plain" and len(content) <= 256 * 1024:
                entry.update(media_type=media_type, encoding="text", content=content)
        cleaned.append(entry)
    return cleaned


def _clean_table(raw: Any) -> dict | None:
    if not isinstance(raw, dict):
        return None
    columns = raw.get("columns")
    rows = raw.get("rows")
    if not isinstance(columns, list) or not isinstance(rows, list):
        return None
    return {
        "columns": [str(c)[:200] for c in columns[:200]],
        "rows": [list(r)[:200] for r in rows[:500] if isinstance(r, list)],
        "row_count": int(raw.get("row_count") or 0),
        "truncated": bool(raw.get("truncated")),
    }


def _to_run_result(outcome: JobOutcome) -> RunResult:
    status = outcome.status if outcome.status in RUN_STATUSES else "infrastructure_error"
    error = outcome.error if isinstance(outcome.error, dict) else None
    if error is not None:
        error = {
            "type": str(error.get("type") or "")[:80],
            "message": str(error.get("message") or "")[:500],
            "line": error.get("line") if isinstance(error.get("line"), int) else None,
        }
    return RunResult(
        status=status,
        stdout=str(outcome.stdout or "")[:70_000],
        stderr=str(outcome.stderr or "")[:70_000],
        execution_ms=max(0, int(outcome.execution_ms or 0)),
        generated_files=_clean_artifacts(outcome.generated_files) if status == "success" else [],
        table=_clean_table(outcome.table),
        error=error,
        captured=outcome.captured if isinstance(outcome.captured, dict) else {},
        stdout_truncated=bool(outcome.stdout_truncated) or len(str(outcome.stdout or "")) > 70_000,
        stderr_truncated=bool(outcome.stderr_truncated) or len(str(outcome.stderr or "")) > 70_000,
        artifacts_truncated=bool(outcome.artifacts_truncated) or len(outcome.generated_files or []) > 10,
    )


class ProjectExecutionService:
    def __init__(self, backend: ExecutionBackend):
        self.backend = backend

    async def _execute(self, job: dict, purpose: str) -> RunResult:
        started = time.perf_counter()
        try:
            outcome = await self.backend.execute(job)
        except Exception:  # noqa: BLE001 - a backend bug is an infrastructure error, not a 500
            logger.exception("project execution backend %s raised", self.backend.name)
            outcome = JobOutcome("infrastructure_error", stderr="The execution environment failed.")
        result = _to_run_result(outcome)
        seconds = time.perf_counter() - started
        record_project_lab_execution(purpose, job["mode"], result.status, seconds)
        # Structured and content-free: never file contents, output or captured values.
        log = logger.warning if result.status == "infrastructure_error" else logger.info
        log("project_lab.execution", extra={
            "event": "project_lab.execution", "purpose": purpose, "kind": job["mode"],
            "backend": self.backend.name, "status": result.status, "seconds": round(seconds, 3),
            "stdout_truncated": result.stdout_truncated, "stderr_truncated": result.stderr_truncated,
        })
        return result

    async def run_python(
        self, snapshot: WorkspaceSnapshot, file_path: str, *,
        capture: list[str] | tuple[str, ...] = (), data_inline: dict[str, str] | None = None,
        purpose: str = "run",
    ) -> RunResult:
        return await self._execute({
            "mode": "python", "entry": file_path, "template_key": snapshot.template_key,
            "files": snapshot.files, "dirs": snapshot.dirs, "capture": list(capture),
            "data_inline": data_inline or {},
        }, purpose)

    async def run_sql(
        self, snapshot: WorkspaceSnapshot, file_path: str, *,
        data_inline: dict[str, str] | None = None, purpose: str = "run",
    ) -> RunResult:
        return await self._execute({
            "mode": "sql", "entry": file_path, "template_key": snapshot.template_key,
            "files": snapshot.files, "dirs": snapshot.dirs, "data_inline": data_inline or {},
        }, purpose)

    async def validate_task(
        self, snapshot: WorkspaceSnapshot, task, *, template, artifacts: dict[str, dict] | None = None,
    ) -> "ValidationResult":
        from .validation import ValidationContext, run_validator

        context = ValidationContext(execution=self, snapshot=snapshot, template=template,
                                    config=dict(task.validator_config or {}), artifacts=artifacts or {})
        return await run_validator(task.validator_key, context)


_service: ProjectExecutionService | None = None


def get_execution_service() -> ProjectExecutionService:
    """FastAPI dependency. Tests override it to inject a fake backend."""
    global _service
    if _service is None:
        _service = ProjectExecutionService(build_backend())
    return _service

