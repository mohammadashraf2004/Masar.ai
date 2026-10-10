"""Replaceable code-execution boundary."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionResult:
    status: str
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: int = 0
    variables: dict[str, Any] = field(default_factory=dict)
    return_values: dict[str, Any] = field(default_factory=dict)
    detail: str | None = None
    # The learner program's own failure ({"type", "message", "line"}) when it
    # stopped with an error; None when it ran to the end.
    error: dict[str, Any] | None = None

    @property
    def succeeded(self) -> bool:
        return self.status == "success"


class CodeRunner(ABC):
    @abstractmethod
    async def run(
        self,
        code: str,
        *,
        pre_exercise_code: str = "",
        variables: list[str] | None = None,
        calls: list[dict[str, Any]] | None = None,
    ) -> ExecutionResult:
        raise NotImplementedError
