"""In-sandbox program that executes ONE Project Lab job.

Started by project_runner/executor.py as `python -I harness.py`, already running
as the unprivileged sandbox user when the runner service is used. It must stay
self-contained (stdlib only at import time; pandas/duckdb/matplotlib are
imported lazily) because -I keeps the package directory off sys.path.

Protocol: one JSON job on stdin, one JSON result on the ORIGINAL stdout.

Everything this process reports is UNTRUSTED. Learner code runs in this same
interpreter and can reach the harness's frames, so it can forge any field of
the result. That is acceptable by design: the API treats results as
observations and compares them, server-side, with expected values that never
enter the sandbox. Do not move any comparison or expected value in here.
"""
from __future__ import annotations

import base64
import io
import json
import math
import os
import shutil
import sys
import traceback

TEXT_ARTIFACTS = {".csv", ".txt", ".json", ".md"}
IMAGE_ARTIFACTS = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
MAX_ARTIFACTS = 10
MAX_ARTIFACT_BYTES = 2 * 1024 * 1024
# Validators compare whole DataFrames the learner built (e.g. a cleaned order
# table), so captured frames are serialised in full up to this many rows.
MAX_CAPTURED_ROWS = 20_000


class BoundedBuffer(io.StringIO):
    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self.used = 0
        self.truncated = False

    def write(self, value):  # type: ignore[override]
        value = str(value)
        remaining = self.limit - self.used
        if remaining <= 0:
            self.truncated = True
            return len(value)
        piece = value[:remaining]
        self.used += len(piece)
        if len(piece) < len(value):
            self.truncated = True
        return super().write(piece)

    def result(self) -> str:
        return self.getvalue() + ("\n[output truncated]" if self.truncated else "")


def apply_limits(limits: dict) -> None:
    """Lower (never raise) this process's limits before any learner code runs.
    Soft == hard, so learner code cannot raise them back."""
    try:
        import resource
    except ImportError:  # not POSIX: the executor refuses this mode outside development
        return

    def cap(name: str, value) -> None:
        if value is None:
            return
        value = int(value)
        try:
            resource.setrlimit(getattr(resource, name), (value, value))
        except (ValueError, OSError, AttributeError):
            pass

    cap("RLIMIT_CORE", 0)
    cap("RLIMIT_CPU", limits.get("cpu_seconds"))
    if limits.get("memory_mb"):
        cap("RLIMIT_AS", int(limits["memory_mb"]) * 1024 * 1024)
    if limits.get("max_file_mb"):
        cap("RLIMIT_FSIZE", int(limits["max_file_mb"]) * 1024 * 1024)
    cap("RLIMIT_NOFILE", limits.get("max_open_files"))
    cap("RLIMIT_NPROC", limits.get("max_processes"))


def materialize(job: dict) -> set[str]:
    """Build the workspace in the job directory (already the cwd).

    Datasets are COPIED, never symlinked: in the development adapter the
    template lives on a writable disk, and a symlink would let learner code
    write through to the canonical dataset."""
    created: set[str] = set()
    for directory in job.get("dirs", []):
        os.makedirs(directory, exist_ok=True)
    for rel, source in job.get("data_links", {}).items():
        os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
        shutil.copyfile(source, rel)
        os.chmod(rel, 0o444)
        created.add(rel)
    for rel, content in job.get("data_inline", {}).items():
        os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
        if os.path.exists(rel):
            os.chmod(rel, 0o644)
        with open(rel, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.chmod(rel, 0o444)
        created.add(rel)
    for rel, content in job.get("files", {}).items():
        os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
        with open(rel, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        created.add(rel)
    return created


def _number(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def jsonable(value, depth: int = 0):
    """A JSON-safe observation of a learner value (bounded in size)."""
    if depth > 6:
        return {"__repr__": "<depth limit>"}
    if value is None or isinstance(value, (bool, str)):
        return value[:10_000] if isinstance(value, str) else value
    if type(value).__name__ in {"Timestamp", "datetime", "date", "Period", "datetime64", "NaTType"}:
        return None if type(value).__name__ == "NaTType" else str(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return _number(value)
    item = getattr(value, "item", None)  # numpy scalars
    if callable(item) and getattr(value, "shape", None) == ():
        try:
            return jsonable(item(), depth + 1)
        except Exception:
            pass
    if isinstance(value, dict):
        return {str(k): jsonable(v, depth + 1) for k, v in list(value.items())[:MAX_CAPTURED_ROWS]}
    if isinstance(value, (list, tuple)):
        return [jsonable(v, depth + 1) for v in list(value)[:MAX_CAPTURED_ROWS]]
    if isinstance(value, (set, frozenset)):
        return [jsonable(v, depth + 1) for v in sorted(value, key=repr)[:MAX_CAPTURED_ROWS]]
    if hasattr(value, "columns") and hasattr(value, "to_dict"):  # DataFrame
        try:
            head = value.head(MAX_CAPTURED_ROWS)
            return {
                "__dataframe__": True,
                "columns": [str(c) for c in value.columns],
                "shape": list(value.shape),
                "records": jsonable(head.to_dict(orient="records"), depth + 1),
            }
        except Exception:
            pass
    if hasattr(value, "to_dict") and hasattr(value, "index"):  # Series
        try:
            return jsonable(value.to_dict(), depth + 1)
        except Exception:
            pass
    if hasattr(value, "tolist"):  # numpy arrays, pandas Index
        try:
            return jsonable(value.tolist(), depth + 1)
        except Exception:
            pass
    return {"__repr__": repr(value)[:2000], "__type__": type(value).__name__}


def learner_traceback(exc: BaseException, learner_files: set[str]) -> tuple[str, int | None]:
    """The traceback restricted to the learner's own frames: harness internals
    are noise to a learner and describe the sandbox to an attacker."""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename in learner_files]
    lines = ["Traceback (most recent call last):\n"] if frames else []
    lines += traceback.format_list(frames)
    lines += traceback.format_exception_only(type(exc), exc)
    return "".join(lines), (frames[-1].lineno if frames else None)


def run_python(job: dict, out: BoundedBuffer, err: BoundedBuffer) -> dict:
    entry = job["entry"]
    with open(entry, encoding="utf-8") as handle:
        source = handle.read()
    result: dict = {"status": "success", "error": None, "captured": {}}
    try:
        code = compile(source, entry, "exec")
    except SyntaxError as exc:
        err.write("".join(traceback.format_exception_only(type(exc), exc)))
        result.update(status="error", error={"type": "SyntaxError", "message": str(exc.msg), "line": exc.lineno})
        return result
    namespace = {"__name__": "__main__", "__file__": entry, "__builtins__": __builtins__}
    learner_files = set(job.get("files", {}))
    previous_out, previous_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        exec(code, namespace)  # noqa: S102 - this IS the sandboxed learner execution
    except SystemExit as exc:
        if exc.code not in (None, 0):
            result.update(status="error", error={"type": "SystemExit", "message": f"exit code {exc.code}", "line": None})
    except MemoryError:
        result.update(status="error", error={"type": "MemoryError", "message": "memory limit exceeded", "line": None})
        err.write("MemoryError: your program used more memory than the project allows.\n")
    except BaseException as exc:  # noqa: BLE001 - every learner failure is reported, not raised
        text, line = learner_traceback(exc, learner_files)
        err.write(text)
        result.update(status="error", error={"type": type(exc).__name__, "message": str(exc)[:500], "line": line})
    finally:
        sys.stdout, sys.stderr = previous_out, previous_err
    for name in job.get("capture", []):
        result["captured"][name] = jsonable(namespace[name]) if name in namespace else {"__missing__": True}
    return result


def run_sql(job: dict, out: BoundedBuffer, err: BoundedBuffer) -> dict:
    import duckdb

    entry = job["entry"]
    with open(entry, encoding="utf-8") as handle:
        sql = handle.read()
    result: dict = {"status": "success", "error": None, "table": None}
    if not sql.strip() or all(not line.strip() or line.strip().startswith("--") for line in sql.splitlines()):
        err.write("The SQL file is empty.\n")
        result.update(status="error", error={"type": "EmptyQuery", "message": "The SQL file is empty.", "line": None})
        return result
    con = duckdb.connect(":memory:", config={"threads": 1})
    data_dir = "data"
    for name in sorted(os.listdir(data_dir)) if os.path.isdir(data_dir) else []:
        if name.endswith(".csv"):
            table = name[:-4]
            path = os.path.join(data_dir, name).replace("'", "''")
            con.execute(f'CREATE TABLE "{table}" AS SELECT * FROM read_csv_auto(\'{path}\', header=true)')
    # After the tables exist: learner SQL may not read or write files, load
    # extensions or change these settings back.
    for statement in (
        "SET enable_external_access = false",
        "SET autoinstall_known_extensions = false",
        "SET autoload_known_extensions = false",
        "SET lock_configuration = true",
    ):
        try:
            con.execute(statement)
        except duckdb.Error:
            pass
    limit = int(job.get("limits", {}).get("sql_row_limit", 500))
    try:
        cursor = con.execute(sql)
        if cursor.description is None:
            result["table"] = {"columns": [], "rows": [], "row_count": 0, "truncated": False}
            out.write("Statement executed. It returned no rows.\n")
            return result
        columns = [str(d[0]) for d in cursor.description]
        rows = cursor.fetchmany(limit + 1)
        truncated = len(rows) > limit
        rows = rows[:limit]
        result["table"] = {
            "columns": columns,
            "rows": [[jsonable(v if isinstance(v, (int, float, str, bool)) or v is None else str(v)) for v in row] for row in rows],
            "row_count": len(rows),
            "truncated": truncated,
        }
        out.write(f"{len(rows)} row(s){' (truncated)' if truncated else ''}.\n")
    except duckdb.Error as exc:
        message = str(exc)
        err.write(message[:4000] + "\n")
        result.update(status="error", error={"type": type(exc).__name__, "message": message[:500], "line": None})
    finally:
        con.close()
    return result


def collect_artifacts(created: set[str]) -> tuple[list[dict], bool]:
    """New files the run produced (charts, exports), bounded in count and size.
    Returns (artifacts, truncated) — truncated when more files existed."""
    artifacts: list[dict] = []
    for root, dirs, names in os.walk("."):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "data" and d != "__pycache__")
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(root, name), ".").replace(os.sep, "/")
            if rel in created or name.startswith(".") or os.path.islink(rel):
                continue
            ext = os.path.splitext(name)[1].lower()
            size = os.path.getsize(rel)
            entry: dict = {"path": rel, "size": size, "media_type": None, "content": None, "encoding": None}
            if size <= MAX_ARTIFACT_BYTES and ext in IMAGE_ARTIFACTS:
                with open(rel, "rb") as handle:
                    entry.update(media_type=IMAGE_ARTIFACTS[ext], encoding="base64",
                                 content=base64.b64encode(handle.read()).decode("ascii"))
            elif size <= 256 * 1024 and ext in TEXT_ARTIFACTS:
                with open(rel, encoding="utf-8", errors="replace") as handle:
                    entry.update(media_type="text/plain", encoding="text", content=handle.read())
            if len(artifacts) >= MAX_ARTIFACTS:
                return artifacts, True
            artifacts.append(entry)
    return artifacts, False


def main() -> None:
    reporter = os.getpid()
    raw = sys.stdin.buffer.read(16 * 1024 * 1024)
    job = json.loads(raw.decode("utf-8"))
    limits = job.get("limits", {})
    output_chars = int(limits.get("output_chars", 65_536))

    # The result goes to a private duplicate of the original stdout; fds 1 and
    # 2 then point at /dev/null, so learner (or C-extension) writes straight to
    # the file descriptors cannot corrupt the result stream.
    result_fd = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)

    if not os.path.isdir(job["workdir"]):
        # Under the runner service the harness creates its own job directory
        # (it already runs as the sandbox user); see executor.execute_job.
        os.mkdir(job["workdir"], 0o700)
    os.chdir(job["workdir"])
    # Workspace modules are importable (`from analysis.clean_data import ...`)
    # — they are the learner's own files, nothing else is added.
    sys.path.insert(0, job["workdir"])
    os.environ["MPLCONFIGDIR"] = os.path.join(job["workdir"], ".mpl")
    os.environ["HOME"] = job["workdir"]
    seed = os.environ.get("MASAR_MPL_SEED")
    if seed and os.path.isdir(seed):
        # A prebuilt font cache, so importing matplotlib does not rebuild it
        # on every run.
        shutil.copytree(seed, os.environ["MPLCONFIGDIR"], dirs_exist_ok=True)
    created = materialize(job)
    apply_limits(limits)

    out, err = BoundedBuffer(output_chars), BoundedBuffer(output_chars)
    try:
        if job["mode"] == "python":
            result = run_python(job, out, err)
        elif job["mode"] == "sql":
            result = run_sql(job, out, err)
        else:
            result = {"status": "infrastructure_error", "error": {"type": "BadJob", "message": "unknown mode", "line": None}}
        if result.get("status") != "infrastructure_error":
            result["generated_files"], result["artifacts_truncated"] = collect_artifacts(created)
        else:
            result["generated_files"], result["artifacts_truncated"] = [], False
    except MemoryError:
        result = {"status": "error", "error": {"type": "MemoryError", "message": "memory limit exceeded", "line": None},
                  "generated_files": []}
        err.write("MemoryError: your program used more memory than the project allows.\n")
    if os.getpid() != reporter:
        # A process the learner forked has fallen through to here. Only the
        # original harness reports; a second writer would corrupt the result.
        os._exit(0)
    result["stdout"], result["stderr"] = out.result(), err.result()
    result["stdout_truncated"], result["stderr_truncated"] = out.truncated, err.truncated
    payload = json.dumps(result, ensure_ascii=False, allow_nan=False, default=str).encode("utf-8")
    with os.fdopen(result_fd, "wb") as channel:
        channel.write(payload)


if __name__ == "__main__":
    main()
