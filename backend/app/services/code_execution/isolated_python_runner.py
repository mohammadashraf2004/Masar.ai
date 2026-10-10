"""Python exercise adapter for Masar's isolated project-runner service.

The project runner is the repository's security boundary for learner code and
already carries the data-science libraries used by curriculum exercises. This
adapter sends it two files and translates the captured values into the
smaller CodeRunner contract consumed by the deterministic exercise grader:

* ``exercise.py`` - the learner's code, byte for byte, so every traceback
  line number and source line is the learner's own;
* ``masar_check.py`` - a trusted driver (the entry point). It runs the
  author's setup and then the learner's file in a namespace of their own,
  and afterwards evaluates the exercise's hidden checks against that
  namespace.

Running the learner's file through the driver, instead of appending the
checks to it, gives four guarantees the appended form could not:

* the checks still run when the learner's program stops with an error, so a
  crash in the learner's demo line (``divide(1, 0)``) still gets the precise
  feedback of the check that explains it;
* anything printed while the hidden checks run is discarded, so a ``print``
  inside the learner's function cannot reveal the hidden inputs;
* a builtin a check relies on (``sorted``, ``round``, ``len``) is the real
  builtin even when the learner reused that name for a variable;
* the driver's results live in its own globals, which the learner's code
  cannot name, so a learner cannot fake an expected error or a check value.

Everything the runner returns is still untrusted: it is shape-checked here and
compared with expected values server-side; expected values never enter the
sandbox.
"""
from __future__ import annotations

import ast
import builtins
from typing import Any

from app.core.config import settings
from app.services.project_lab.execution import (
    LocalSubprocessBackend, ProjectExecutionService, WorkspaceSnapshot, get_execution_service,
)

from .base import CodeRunner, ExecutionResult
from .python_runner import ForbiddenCode, validate_check_expressions, validate_python_source

LEARNER_FILE = "exercise.py"
DRIVER_FILE = "masar_check.py"
# The runner captures at most this many names per job (project_runner/executor.py).
MAX_CAPTURES = 20
# Captures the driver always uses besides one per variable and one per check.
_RESERVED_CAPTURES = ("masar_failure", "masar_setup_error", "masar_errors")
MAX_OBSERVATIONS = MAX_CAPTURES - len(_RESERVED_CAPTURES)
_BUILTIN_NAMES = frozenset(dir(builtins))

_DRIVER = '''\
"""Masar grading driver (trusted). See isolated_python_runner.py."""
import builtins
import sys
import traceback

LEARNER = {learner!r}
SETUP = {setup!r}
VARIABLES = {variables!r}
CALLS = {calls!r}


def _learner_failure(exc):
    frames = [frame for frame in traceback.extract_tb(exc.__traceback__) if frame.filename == LEARNER]
    lines = ["Traceback (most recent call last):\\n"] if frames else []
    lines += traceback.format_list(frames)
    lines += traceback.format_exception_only(type(exc), exc)
    sys.stderr.write("".join(lines))
    line = frames[-1].lineno if frames else getattr(exc, "lineno", None)
    return {{"type": type(exc).__name__, "message": str(exc)[:500], "line": line if isinstance(line, int) else None}}


class _Discard:
    def write(self, text):
        return len(text)

    def flush(self):
        pass


_namespace = {{"__name__": "__main__", "__file__": LEARNER, "__builtins__": builtins}}
masar_failure = None
masar_setup_error = None
masar_errors = {{}}
if SETUP:
    try:
        exec(compile(SETUP, "<setup>", "exec"), _namespace)
    except BaseException as exc:
        masar_setup_error = {{"type": type(exc).__name__, "message": str(exc)[:300]}}
if masar_setup_error is None:
    with open(LEARNER, encoding="utf-8") as _handle:
        _source = _handle.read()
    try:
        exec(compile(_source, LEARNER, "exec"), _namespace)
    except SystemExit as exc:
        if exc.code not in (None, 0):
            masar_failure = {{"type": "SystemExit", "message": "exit code %s" % (exc.code,), "line": None}}
    except BaseException as exc:
        masar_failure = _learner_failure(exc)
    for _index, _name in enumerate(VARIABLES):
        if _name in _namespace:
            globals()["masar_v_%d" % _index] = _namespace[_name]
    _stdout, _stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = _Discard()
    try:
        for _index, (_key, _kind, _payload, _builtin_names) in enumerate(CALLS):
            try:
                if _kind == "expression":
                    # An exercise author's hidden check, validated by the API with the
                    # same source rules as learner code; this runs inside the sandbox.
                    _scope = dict(_namespace)
                    for _builtin in _builtin_names:
                        _scope[_builtin] = getattr(builtins, _builtin)
                    _value = eval(compile(_payload, "<check>", "eval"), _scope)
                else:
                    _function = _namespace.get(_payload["function"])
                    if not callable(_function):
                        masar_errors[_key] = "NameError"
                        continue
                    _value = _function(*_payload["args"], **_payload["kwargs"])
                globals()["masar_r_%d" % _index] = _value
            except BaseException as exc:
                masar_errors[_key] = type(exc).__name__
    finally:
        sys.stdout, sys.stderr = _stdout, _stderr
'''


def _type_name(value: Any) -> str:
    if value is None:
        return "NoneType"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return type(value).__name__


def _observation(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and value.get("__missing__") is True:
        return {"missing": True}
    if isinstance(value, dict) and value.get("__dataframe__") is True:
        columns = [str(column) for column in value.get("columns") or []]
        records = value.get("records") if isinstance(value.get("records"), list) else []
        column_values = {
            column: [row.get(column) for row in records if isinstance(row, dict)]
            for column in columns
        }
        return {
            "kind": "dataframe",
            "type": "DataFrame",
            "value": {
                "columns": columns,
                "shape": list(value.get("shape") or []),
                "column_values": column_values,
            },
        }
    if isinstance(value, dict) and set(value) == {"__repr__", "__type__"}:
        # An object the harness could not turn into data: keep its real type
        # name (a type check must not see it as a ``dict``) and its repr.
        return {"kind": "repr", "type": str(value["__type__"]), "repr": str(value["__repr__"])}
    return {"kind": "value", "type": _type_name(value), "value": value}


def builtins_used(expression: str) -> list[str]:
    """Builtin names a check expression reads. The driver binds them to the
    real builtins, so a learner's variable named ``sorted`` cannot break it."""
    tree = ast.parse(expression, mode="eval")
    return sorted({
        node.id for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in _BUILTIN_NAMES
    })


_STATUS_BY_ERROR = {
    "SyntaxError": "syntax_error", "IndentationError": "syntax_error", "TabError": "syntax_error",
    "MemoryError": "memory_limit",
}


class IsolatedPythonRunner(CodeRunner):
    """Execute one-file Python exercises through the configured execution
    service (the isolated runner in production; refused when disabled)."""

    def __init__(self, *, output_limit: int = 16_384):
        self.output_limit = output_limit

    def _service(self) -> ProjectExecutionService | None:
        return get_execution_service()

    async def run(
        self,
        code: str,
        *,
        pre_exercise_code: str = "",
        variables: list[str] | None = None,
        calls: list[dict[str, Any]] | None = None,
    ) -> ExecutionResult:
        try:
            validate_python_source(code)
        except SyntaxError as exc:
            return ExecutionResult(
                "syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})",
                error={"type": "SyntaxError", "message": str(exc.msg), "line": exc.lineno},
            )
        except ForbiddenCode as exc:
            return ExecutionResult("forbidden_operation", stderr=str(exc), detail=str(exc))
        try:
            validate_python_source(pre_exercise_code)
            validate_check_expressions(calls)
        except (SyntaxError, ForbiddenCode) as exc:
            return ExecutionResult("grading_error", stderr="Exercise setup is invalid.", detail=str(exc))

        requested_variables = [name for name in (variables or []) if isinstance(name, str) and name.isidentifier()]
        driver_calls: list[tuple[str, str, Any, list[str]]] = []
        for request in calls or []:
            key = str(request.get("key", ""))
            if "expression" in request:
                # An exercise author's hidden check (validated above).
                expression = str(request["expression"])
                driver_calls.append((key, "expression", expression, builtins_used(expression)))
                continue
            function = str(request.get("function", ""))
            if not function.isidentifier():
                return ExecutionResult(
                    "grading_error", stderr="Exercise setup is invalid.",
                    detail=f"check {key} names no valid function",
                )
            driver_calls.append((key, "call", {
                "function": function,
                "args": list(request.get("args") or []),
                "kwargs": dict(request.get("kwargs") or {}),
            }, []))
        if len(requested_variables) + len(driver_calls) > MAX_OBSERVATIONS:
            # The runner would silently drop the extra captures and the
            # checks reading them would fail the learner for nothing.
            return ExecutionResult(
                "grading_error", stderr="Exercise setup is invalid.",
                detail=f"{len(requested_variables) + len(driver_calls)} observations exceed {MAX_OBSERVATIONS}",
            )

        service = self._service()
        if service is None:
            return ExecutionResult("execution_error", stderr="Project execution is not available right now.")
        driver = _DRIVER.format(
            learner=LEARNER_FILE, setup=pre_exercise_code or "",
            variables=requested_variables, calls=driver_calls,
        )
        capture = [
            *(f"masar_v_{index}" for index in range(len(requested_variables))),
            *(f"masar_r_{index}" for index in range(len(driver_calls))),
            *_RESERVED_CAPTURES,
        ]
        result = await service.run_python(
            WorkspaceSnapshot(template_key="code-exercise", files={LEARNER_FILE: code, DRIVER_FILE: driver}),
            DRIVER_FILE,
            capture=capture,
            purpose="code_exercise",
        )
        captured = result.captured if isinstance(result.captured, dict) else {}
        stdout = result.stdout[: self.output_limit]
        stderr = result.stderr[: self.output_limit]
        execution_ms = result.execution_ms

        if result.status == "infrastructure_error":
            return ExecutionResult("execution_error", stdout=stdout, stderr=stderr, execution_time_ms=execution_ms,
                                   detail=str(result.error or "") or None)
        if result.status == "timeout":
            return ExecutionResult("timeout", stdout=stdout, stderr=stderr, execution_time_ms=execution_ms)

        failure = captured.get("masar_failure") if result.status == "success" else None
        setup_error = captured.get("masar_setup_error") if result.status == "success" else None
        if isinstance(setup_error, dict):
            return ExecutionResult(
                "grading_error", stderr="Exercise setup is invalid.", execution_time_ms=execution_ms,
                detail=f"setup raised {setup_error.get('type')}",
            )

        error: dict[str, Any] | None = None
        if result.status == "error":
            # The driver itself was stopped: a resource limit the learner's
            # program hit (memory, output, processes) or the CPU limit.
            error_type = str((result.error or {}).get("type") or "")
            if "more output than" in stderr or result.stdout_truncated:
                status = "output_limit"
            elif error_type == "MemoryError" or "resource limit" in stderr or "MemoryError" in stderr:
                status = "memory_limit"
            else:
                status = "runtime_error"
            error = {"type": error_type or None, "message": str((result.error or {}).get("message") or ""), "line": None}
        elif isinstance(failure, dict):
            error_type = str(failure.get("type") or "")
            status = _STATUS_BY_ERROR.get(error_type, "runtime_error")
            line = failure.get("line")
            error = {
                "type": error_type, "message": str(failure.get("message") or "")[:500],
                "line": line if isinstance(line, int) and not isinstance(line, bool) else None,
            }
        else:
            status = "success"

        observations = {
            name: _observation(captured.get(f"masar_v_{index}", {"__missing__": True}))
            for index, name in enumerate(requested_variables)
        }
        errors = captured.get("masar_errors") if isinstance(captured.get("masar_errors"), dict) else {}
        return_values: dict[str, Any] = {}
        for index, (key, _kind, _payload, _names) in enumerate(driver_calls):
            if key in errors:
                return_values[key] = {"kind": "error", "type": str(errors[key])[:80]}
            else:
                return_values[key] = _observation(captured.get(f"masar_r_{index}", {"__missing__": True}))
        return ExecutionResult(
            status=status, stdout=stdout, stderr=stderr, execution_time_ms=execution_ms,
            variables=observations, return_values=return_values, error=error,
            detail=str(result.error or "") or None,
        )


class LocalPythonRunner(IsolatedPythonRunner):
    """Development and tests: the same driver and runner harness as
    production, run as a child process of the API (LocalSubprocessBackend).

    It is NOT a sandbox - the child has the API user's filesystem and network
    - so it refuses to run at all in production, whatever constructed it.
    """

    def __init__(self, *, timeout_seconds: float = 3.0, memory_mb: int | None = None, output_limit: int = 16_384):
        super().__init__(output_limit=output_limit)
        self.timeout_seconds = timeout_seconds
        self.memory_mb = memory_mb or settings.PROJECT_LAB_LOCAL_MEMORY_MB

    def _service(self) -> ProjectExecutionService | None:
        if settings.is_production:
            return None
        return ProjectExecutionService(
            LocalSubprocessBackend(timeout_seconds=self.timeout_seconds, memory_mb=self.memory_mb),
        )
