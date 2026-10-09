"""Python exercise adapter for Masar's isolated project-runner service.

The project runner is the repository's security boundary for learner code and
already carries the data-science libraries used by curriculum exercises.  This
adapter translates its captured-value format into the smaller CodeRunner
contract consumed by the deterministic exercise grader.
"""
from __future__ import annotations

from typing import Any

from app.services.project_lab.execution import WorkspaceSnapshot, get_execution_service

from .base import CodeRunner, ExecutionResult
from .python_runner import ForbiddenCode, validate_check_expressions, validate_python_source


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
    return {"kind": "value", "type": _type_name(value), "value": value}


class IsolatedPythonRunner(CodeRunner):
    """Execute one-file Python exercises through the no-network runner."""

    def __init__(self, *, output_limit: int = 16_384):
        self.output_limit = output_limit

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
            return ExecutionResult("syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})")
        except ForbiddenCode as exc:
            return ExecutionResult("forbidden_operation", stderr=str(exc), detail=str(exc))
        try:
            validate_python_source(pre_exercise_code)
            validate_check_expressions(calls)
        except (SyntaxError, ForbiddenCode) as exc:
            return ExecutionResult("execution_error", stderr="Exercise setup is invalid.", detail=str(exc))

        requested_variables = [name for name in (variables or []) if isinstance(name, str) and name.isidentifier()]
        return_names: list[tuple[str, str]] = []
        call_source: list[str] = []
        for request in calls or []:
            key = str(request.get("key", ""))
            capture_name = f"masar_return_{len(return_names)}"
            if "expression" in request:
                # An exercise author's hidden check (validated above), evaluated after learner code.
                call_source.extend([
                    "try:",
                    f"    {capture_name} = ({request['expression']})",
                    "except Exception as masar_call_error:",
                    f"    {capture_name} = {{'__masar_call_error__': type(masar_call_error).__name__}}",
                ])
                return_names.append((key, capture_name))
                continue
            function = str(request.get("function", ""))
            if not function.isidentifier():
                continue
            args = repr(list(request.get("args") or []))
            kwargs = repr(dict(request.get("kwargs") or {}))
            call_source.extend([
                "try:",
                f"    {capture_name} = {function}(*{args}, **{kwargs})",
                "except Exception as masar_call_error:",
                f"    {capture_name} = {{'__masar_call_error__': type(masar_call_error).__name__}}",
            ])
            return_names.append((key, capture_name))

        combined = "\n".join(part for part in (pre_exercise_code, code, "\n".join(call_source)) if part)
        capture = requested_variables + [name for _, name in return_names]
        result = await get_execution_service().run_python(
            WorkspaceSnapshot(template_key="code-exercise", files={"exercise.py": combined}),
            "exercise.py",
            capture=capture,
            purpose="code_exercise",
        )

        status = result.status
        if status == "error":
            error_type = str((result.error or {}).get("type") or "")
            status = "syntax_error" if error_type == "SyntaxError" else "runtime_error"
        elif status == "infrastructure_error":
            status = "execution_error"

        captured = result.captured if isinstance(result.captured, dict) else {}
        observations = {
            name: _observation(captured.get(name, {"__missing__": True}))
            for name in requested_variables
        }
        return_values = {
            key: _observation(captured.get(name, {"__missing__": True}))
            for key, name in return_names
        }
        return ExecutionResult(
            status=status,
            stdout=result.stdout[: self.output_limit],
            stderr=result.stderr[: self.output_limit],
            execution_time_ms=result.execution_ms,
            variables=observations,
            return_values=return_values,
            detail=str(result.error or "") or None,
        )
