"""Run one Project Lab job in a child process and return a structured result.

Shared by two callers:

* project_runner/server.py — the isolated runner service (separate container,
  no application secrets, no network at all, read-only root filesystem,
  seccomp allowlist). There the service runs as root with only the
  SETUID/SETGID capabilities and every job runs as the unprivileged `sandbox`
  user, one job at a time, so a job can neither signal the service nor see
  another job.

* app.services.project_lab.execution.LocalSubprocessBackend — the development
  adapter. Same harness and limits, but it runs as whatever user the API runs
  as, with that user's filesystem and network access. It is NOT a sandbox and
  the API refuses to start with it in production (see app/core/config.py).

This module must not import anything from `app`: the runner image does not
contain the application.
"""
from __future__ import annotations

import json
import os
import posixpath
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.py")
SAFE_ENV = {
    "PATH": "/usr/local/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONHASHSEED": "0",
    "MPLBACKEND": "Agg",
    "OPENBLAS_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_MAX_THREADS": "1",
}
MAX_RESULT_BYTES = 24 * 1024 * 1024
MAX_FILE_CHARS = 200_000
MAX_FILES = 64
_SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-]{0,99}$")
_TEMPLATE_KEY = re.compile(r"^[a-z0-9][a-z0-9\-]{0,79}$")


@dataclass
class Limits:
    timeout_seconds: float = 15.0
    cpu_seconds: int = 12
    memory_mb: int = 1024
    max_processes: int | None = None  # only meaningful for a dedicated sandbox uid
    max_file_mb: int = 8
    max_open_files: int = 128
    output_chars: int = 65_536
    sql_row_limit: int = 500

    @classmethod
    def from_dict(cls, data: dict | None) -> "Limits":
        known = {k: v for k, v in (data or {}).items() if k in cls.__dataclass_fields__}
        return cls(**known)


@dataclass
class JobOutcome:
    status: str  # success | error | timeout | infrastructure_error
    stdout: str = ""
    stderr: str = ""
    execution_ms: int = 0
    error: dict | None = None
    captured: dict = field(default_factory=dict)
    table: dict | None = None
    generated_files: list = field(default_factory=list)
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    artifacts_truncated: bool = False

    def to_dict(self) -> dict:
        return {
            "status": self.status, "stdout": self.stdout, "stderr": self.stderr,
            "execution_ms": self.execution_ms, "error": self.error, "captured": self.captured,
            "table": self.table, "generated_files": self.generated_files,
            "stdout_truncated": self.stdout_truncated, "stderr_truncated": self.stderr_truncated,
            "artifacts_truncated": self.artifacts_truncated,
        }


class InvalidJob(ValueError):
    pass


def safe_relative_path(path: str) -> str:
    """Canonical workspace-relative path, or InvalidJob. Rejects absolute paths,
    backslashes, `..`, empty or hidden segments, and anything unusual."""
    if not isinstance(path, str) or not path or len(path) > 255 or "\x00" in path or "\\" in path:
        raise InvalidJob("invalid path")
    if path.startswith("/"):
        raise InvalidJob("absolute path")
    normalized = posixpath.normpath(path)
    if normalized != path.rstrip("/") or normalized in {".", ".."}:
        raise InvalidJob("non-canonical path")
    for segment in normalized.split("/"):
        if not _SAFE_SEGMENT.match(segment) or segment in {".", ".."}:
            raise InvalidJob("invalid path segment")
    return normalized


def validate_job(job: dict, templates_root: str) -> dict:
    """Shape-check a job and resolve its template datasets. The caller is the
    trusted API, but the runner validates anyway: it is the last line before
    files are written."""
    if not isinstance(job, dict):
        raise InvalidJob("job must be an object")
    mode = job.get("mode")
    if mode not in {"python", "sql"}:
        raise InvalidJob("unknown mode")
    entry = safe_relative_path(job.get("entry", ""))
    suffix = ".py" if mode == "python" else ".sql"
    if not entry.endswith(suffix):
        raise InvalidJob("entry does not match mode")
    files = job.get("files") or {}
    if not isinstance(files, dict) or len(files) > MAX_FILES:
        raise InvalidJob("files")
    clean_files = {}
    for rel, content in files.items():
        rel = safe_relative_path(rel)
        if rel.startswith("data/") or not isinstance(content, str) or len(content) > MAX_FILE_CHARS:
            raise InvalidJob("file entry")
        clean_files[rel] = content
    if entry not in clean_files:
        raise InvalidJob("entry file missing")

    template_key = job.get("template_key", "")
    if not _TEMPLATE_KEY.match(template_key or ""):
        raise InvalidJob("template key")
    data_root = os.path.realpath(os.path.join(templates_root, template_key, "workspace", "data"))
    data_links = {}
    if os.path.isdir(data_root):
        for name in sorted(os.listdir(data_root)):
            source = os.path.realpath(os.path.join(data_root, name))
            if os.path.dirname(source) == data_root and os.path.isfile(source) and not name.startswith("."):
                data_links[f"data/{name}"] = source
    data_inline = {}
    for rel, content in (job.get("data_inline") or {}).items():
        rel = safe_relative_path(rel)
        if not rel.startswith("data/") or not isinstance(content, str) or len(content) > 4 * 1024 * 1024:
            raise InvalidJob("inline data")
        data_inline[rel] = content
    capture = [c for c in (job.get("capture") or []) if isinstance(c, str) and c.isidentifier()][:20]
    dirs = [safe_relative_path(d) for d in (job.get("dirs") or [])][:32]
    return {
        "mode": mode, "entry": entry, "files": clean_files, "data_links": data_links,
        "data_inline": data_inline, "capture": capture, "dirs": dirs,
    }


def _read_bounded(stream, sink: list, limit: int) -> None:
    total = 0
    while True:
        chunk = stream.read(65_536)
        if not chunk:
            return
        total += len(chunk)
        if total <= limit:
            sink.append(chunk)
        else:
            sink.append(None)  # overflow marker; keep draining so the child never blocks


def _kill_group(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, AttributeError, OSError):
        try:
            proc.kill()
        except OSError:
            pass


# Runs as the sandbox uid after every job: removes the job directory and any
# files the job left in shared writable places (/dev/shm is world-writable in
# every container), then kills every process the sandbox uid still owns —
# itself last — so nothing a job started survives into the next job.
_CLEANUP = (
    "import os, shutil, signal, sys\n"
    "shutil.rmtree(sys.argv[1], ignore_errors=True)\n"
    "for d in ('/dev/shm',):\n"
    "    try:\n"
    "        names = os.listdir(d)\n"
    "    except OSError:\n"
    "        names = []\n"
    "    for n in names:\n"
    "        p = os.path.join(d, n)\n"
    "        try:\n"
    "            if os.lstat(p).st_uid == os.getuid():\n"
    "                shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)\n"
    "        except OSError:\n"
    "            pass\n"
    "os.kill(-1, signal.SIGKILL)\n"
)


def _cleanup(job_dir: str, sandbox_user: str | None) -> None:
    if sandbox_user is None:
        shutil.rmtree(job_dir, ignore_errors=True)
        return
    try:
        subprocess.run(
            [sys.executable, "-I", "-c", _CLEANUP, job_dir], user=sandbox_user, group=sandbox_user,
            extra_groups=[], env=SAFE_ENV, timeout=10, stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
    except Exception:  # noqa: BLE001 - cleanup must never mask the job result
        pass


def execute_job(
    job: dict,
    *,
    templates_root: str,
    jobs_root: str | None = None,
    sandbox_user: str | None = None,
    limits: Limits | None = None,
    python: str = sys.executable,
) -> JobOutcome:
    """Execute one job. Never raises for learner behaviour; returns
    `infrastructure_error` for anything that is the platform's fault."""
    limits = limits or Limits()
    started = time.perf_counter()
    try:
        clean = validate_job(job, templates_root)
    except InvalidJob as exc:
        return JobOutcome("infrastructure_error", stderr="The execution request was rejected.",
                          error={"type": "InvalidJob", "message": str(exc), "line": None})

    if sandbox_user is not None:
        # The harness creates this directory itself, already running as the
        # sandbox user, inside the sticky jobs root (mode 1733): the service
        # needs no CAP_CHOWN to hand it over, cannot list the jobs root, and
        # the sandbox user can remove only its own entries there.
        job_dir = os.path.join(jobs_root or "/jobs", f"masar-job-{secrets.token_hex(12)}")
    else:
        job_dir = tempfile.mkdtemp(prefix="masar-job-", dir=jobs_root)  # created 0700

    payload = dict(clean, workdir=job_dir, limits={
        "cpu_seconds": limits.cpu_seconds, "memory_mb": limits.memory_mb,
        "max_processes": limits.max_processes, "max_file_mb": limits.max_file_mb,
        "max_open_files": limits.max_open_files, "output_chars": limits.output_chars,
        "sql_row_limit": limits.sql_row_limit,
    })
    env = dict(SAFE_ENV, HOME=job_dir, TMPDIR=job_dir, MPLCONFIGDIR=os.path.join(job_dir, ".mpl"))
    if os.environ.get("MASAR_MPL_SEED"):
        env["MASAR_MPL_SEED"] = os.environ["MASAR_MPL_SEED"]
    popen_kwargs: dict = {
        "stdin": subprocess.PIPE, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE,
        # Not the job dir: the service has no DAC override, and Popen changes
        # directory before switching user. The harness chdirs there itself.
        "cwd": os.path.dirname(job_dir), "env": env, "close_fds": True,
    }
    if os.name == "posix":
        popen_kwargs["start_new_session"] = True
    if sandbox_user is not None:
        popen_kwargs.update(user=sandbox_user, group=sandbox_user, extra_groups=[], umask=0o077)

    try:
        try:
            proc = subprocess.Popen([python, "-I", HARNESS], **popen_kwargs)
        except OSError as exc:
            return JobOutcome("infrastructure_error", stderr="The execution environment could not start.",
                              error={"type": "SpawnError", "message": str(exc)[:300], "line": None})
        out_chunks: list = []
        err_chunks: list = []
        readers = [
            threading.Thread(target=_read_bounded, args=(proc.stdout, out_chunks, MAX_RESULT_BYTES), daemon=True),
            threading.Thread(target=_read_bounded, args=(proc.stderr, err_chunks, 64 * 1024), daemon=True),
        ]
        for reader in readers:
            reader.start()
        timed_out = False
        try:
            proc.stdin.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
            proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass
        try:
            proc.wait(timeout=limits.timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            if sandbox_user is not None:
                # The service holds no CAP_KILL, so it cannot signal another
                # uid. The cleanup step runs AS the sandbox user and kills
                # every process that user owns — the job included.
                _cleanup(job_dir, sandbox_user)
            else:
                _kill_group(proc)
            proc.wait()
        for reader in readers:
            reader.join(timeout=5)
        elapsed = int((time.perf_counter() - started) * 1000)

        if timed_out:
            return JobOutcome("timeout", stderr=f"Execution stopped after {limits.timeout_seconds:g} seconds.",
                              execution_ms=elapsed)
        killed_by = -proc.returncode if proc.returncode and proc.returncode < 0 else None
        if killed_by in (getattr(signal, "SIGXCPU", 24), signal.SIGKILL) and not out_chunks:
            return JobOutcome("timeout", stderr="Execution exceeded the CPU time limit.", execution_ms=elapsed)
        if None in out_chunks:
            return JobOutcome("error", stderr="Your program produced more output than the project allows.",
                              execution_ms=elapsed, stdout_truncated=True)
        raw = b"".join(c for c in out_chunks if c is not None)
        if not raw:
            # The harness died before reporting: almost always a resource
            # limit hit by learner code (e.g. memory exhaustion killing the
            # interpreter outright).
            detail = b"".join(c for c in err_chunks if c is not None).decode("utf-8", "replace")
            if killed_by is not None or "MemoryError" in detail:
                return JobOutcome("error", stderr="Your program was stopped because it exceeded a resource limit "
                                  "(memory, processes or file size).", execution_ms=elapsed)
            return JobOutcome("infrastructure_error", stderr="The execution environment failed.",
                              execution_ms=elapsed, error={"type": "HarnessFailure", "message": detail[-500:], "line": None})
        try:
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("result is not an object")
        except (UnicodeDecodeError, ValueError):
            return JobOutcome("infrastructure_error", stderr="The execution environment returned an invalid result.",
                              execution_ms=elapsed)
        status = data.get("status")
        if status not in {"success", "error", "infrastructure_error"}:
            status = "infrastructure_error"
        return JobOutcome(
            status=status,
            stdout=str(data.get("stdout", ""))[: limits.output_chars + 64],
            stderr=str(data.get("stderr", ""))[: limits.output_chars + 64],
            execution_ms=elapsed,
            error=data.get("error") if isinstance(data.get("error"), dict) else None,
            captured=data.get("captured") if isinstance(data.get("captured"), dict) else {},
            table=data.get("table") if isinstance(data.get("table"), dict) else None,
            generated_files=data.get("generated_files") if isinstance(data.get("generated_files"), list) else [],
            stdout_truncated=bool(data.get("stdout_truncated")),
            stderr_truncated=bool(data.get("stderr_truncated")),
            artifacts_truncated=bool(data.get("artifacts_truncated")),
        )
    finally:
        _cleanup(job_dir, sandbox_user)
