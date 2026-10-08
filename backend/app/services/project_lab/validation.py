"""Deterministic, private Check Step validation.

A task names a validator by key (LabTask.validator_key) and gives it private
settings (LabTask.validator_config). Validators live in
app/services/project_lab/validators/ and never leave the server: they are not
in the template folder the runner mounts, they are not in any API response,
and the expected values they compute stay in this process — the sandbox only
ever returns observations (what the learner's code produced).

Outcomes:
  pass  — every check passed;
  fail  — the learner's analysis ran but at least one check is wrong;
  error — the learner's file could not run (error_kind="execution") or the
          platform failed (error_kind="infrastructure").

Validators check behaviour and results, never source text, and their
messages say what to reconsider without revealing expected values.
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from app.core.metrics import record_project_lab_validator_failure

if TYPE_CHECKING:
    from .execution import ProjectExecutionService, RunResult, WorkspaceSnapshot
    from .templates import ProjectTemplate

logger = logging.getLogger(__name__)

Message = dict[str, str]  # {"en": ..., "ar": ...}


@dataclass
class CheckResult:
    id: str
    passed: bool
    message: Message | None = None  # what to reconsider; only on failure
    label: Message | None = None    # what is being checked, shown either way
    # Not evaluated yet because it depends on the checks above (never a pass).
    pending: bool = False

    def public(self) -> dict:
        return {"id": self.id, "passed": self.passed, "message": self.message, "label": self.label,
                "pending": self.pending}


@dataclass
class ValidationResult:
    outcome: str  # pass | fail | error
    checks: list[CheckResult] = field(default_factory=list)
    error_kind: str | None = None  # execution | infrastructure
    error_message: Message | None = None
    # The learner's own run, shown on an execution error so they can see the
    # traceback. Captured values are stripped before it leaves the server.
    run: "RunResult | None" = None
    execution_ms: int = 0
    # Files the learner's code generated during the check (e.g. charts), to
    # be kept as the attempt's artifacts.
    artifacts: list[dict] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.outcome == "pass"


@dataclass
class ValidationContext:
    execution: "ProjectExecutionService"
    snapshot: "WorkspaceSnapshot"
    template: "ProjectTemplate"
    config: dict[str, Any]
    # The attempt's saved artifacts, path -> {"media_type", "encoding", "content", ...}.
    artifacts: dict[str, dict] = field(default_factory=dict)
    execution_ms: int = 0
    generated: list[dict] = field(default_factory=list)

    def file_text(self, path: str) -> str | None:
        return self.snapshot.files.get(path)

    async def run_python(self, path: str, capture: list[str], data_inline: dict[str, str] | None = None) -> "RunResult":
        result = await self.execution.run_python(
            self.snapshot, path, capture=capture, data_inline=data_inline, purpose="check",
        )
        self.execution_ms += result.execution_ms
        if data_inline is None and result.succeeded:
            self.generated.extend(result.generated_files)
        return result

    async def run_sql(self, path: str, data_inline: dict[str, str] | None = None) -> "RunResult":
        result = await self.execution.run_sql(self.snapshot, path, data_inline=data_inline, purpose="check")
        self.execution_ms += result.execution_ms
        return result


Validator = Callable[[ValidationContext], Awaitable[ValidationResult]]
_REGISTRY: dict[str, Validator] = {}


def validator(key: str) -> Callable[[Validator], Validator]:
    def register(fn: Validator) -> Validator:
        if key in _REGISTRY:
            raise RuntimeError(f"duplicate Project Lab validator: {key}")
        _REGISTRY[key] = fn
        return fn
    return register


def registered_validators() -> frozenset[str]:
    from . import validators  # noqa: F401 - importing registers them
    return frozenset(_REGISTRY)


INFRASTRUCTURE_MESSAGE: Message = {
    "en": "We could not check this step right now. Your work is saved; try Check Step again shortly.",
    "ar": "تعذّر التحقق من هذه الخطوة الآن. عملك محفوظ؛ أعد المحاولة بعد قليل.",
}


def infrastructure_error() -> ValidationResult:
    return ValidationResult("error", error_kind="infrastructure", error_message=INFRASTRUCTURE_MESSAGE)


def execution_error(path: str, run: "RunResult") -> ValidationResult:
    """The learner's file did not run to completion (error or timeout)."""
    if run.status == "infrastructure_error":
        return infrastructure_error()
    if run.status == "timeout":
        message = {
            "en": f"{path} took too long to run, so it could not be checked. Run it, make it finish, then check again.",
            "ar": f"استغرق تشغيل {path} وقتًا أطول من المسموح، لذلك تعذّر التحقق منه. شغّله وتأكد أنه ينتهي ثم أعد التحقق.",
        }
    else:
        message = {
            "en": f"{path} stopped with an error, so it could not be checked. Run it, fix the error shown, then check again.",
            "ar": f"توقف {path} بخطأ، لذلك تعذّر التحقق منه. شغّله وأصلح الخطأ الظاهر ثم أعد التحقق.",
        }
    return ValidationResult("error", error_kind="execution", error_message=message, run=run)


def from_checks(checks: list[CheckResult]) -> ValidationResult:
    return ValidationResult("pass" if checks and all(c.passed for c in checks) else "fail", checks=checks)


async def run_validator(key: str, context: ValidationContext) -> ValidationResult:
    registered_validators()
    fn = _REGISTRY.get(key)
    if fn is None:
        logger.error("Project Lab task uses unknown validator %r", key)
        record_project_lab_validator_failure("unknown_key")
        return infrastructure_error()
    try:
        result = await fn(context)
    except Exception:  # noqa: BLE001 - a validator bug must not read as the learner's failure
        logger.exception("Project Lab validator %r raised", key)
        record_project_lab_validator_failure("exception")
        return infrastructure_error()
    result.execution_ms = context.execution_ms
    result.artifacts = list(context.generated)
    return result


# ─── Comparison helpers shared by validators ─────────────────────────────────

MISSING = object()


def observed(captured: dict, name: str) -> Any:
    value = captured.get(name, MISSING)
    if isinstance(value, dict) and value.get("__missing__"):
        return MISSING
    return value


def as_number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None or value is MISSING:
        return None
    if isinstance(value, (int, float)):
        return None if (isinstance(value, float) and not math.isfinite(value)) else float(value)
    if isinstance(value, str):
        try:
            number = float(value.replace(",", "").strip())
        except ValueError:
            return None
        return number if math.isfinite(number) else None
    return None


def close(value: Any, expected: float, *, abs_tol: float = 0.01) -> bool:
    number = as_number(value)
    return number is not None and math.isclose(number, expected, rel_tol=1e-9, abs_tol=abs_tol)


def same_integer(value: Any, expected: int) -> bool:
    number = as_number(value)
    return number is not None and number == float(expected)


def as_string_list(value: Any) -> list[str] | None:
    """A list-like observation as strings: a list, set or tuple (serialised as
    a list), an array (serialised as a list) or a Series (a dict)."""
    if isinstance(value, dict) and not any(k.startswith("__") for k in value):
        value = list(value.values())
    if not isinstance(value, list):
        return None
    if any(isinstance(v, (dict, list)) for v in value):
        return None
    return [str(v) for v in value]
