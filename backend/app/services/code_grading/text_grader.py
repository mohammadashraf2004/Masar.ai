"""Deterministic static grading for Dockerfile/YAML-style exercises."""
from __future__ import annotations

import hashlib
import re
from typing import Any

from app.services.code_execution import ExecutionResult
from .grader import GradingResult


TEXT_TEST_TYPES = frozenset({"text_changed", "regex_all", "regex_none", "regex_ordered"})


def text_fingerprint(value: str) -> str:
    normalized = "\n".join(line.rstrip() for line in value.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class TextGrader:
    """Grade configuration files without executing them or using an LLM."""

    async def grade(self, code: str, tests: list[dict[str, Any]], **_: Any) -> GradingResult:
        required = [test for test in tests if test.get("required", True)]
        execution = ExecutionResult("success")
        if not required:
            execution.status = "grading_error"
            execution.stderr = "This exercise has no required grading tests."
            return GradingResult(
                "grading_error", False, "INVALID_TEST_CONFIGURATION",
                {"en": execution.stderr, "ar": "لا يمكن تقييم هذا التمرين لعدم وجود اختبارات مطلوبة."},
                None, 0, 0, execution,
            )
        passed = 0
        for index, test in enumerate(tests):
            ok = self._check(code, test)
            if ok:
                if test.get("required", True):
                    passed += 1
                continue
            if not test.get("required", True):
                continue
            return GradingResult(
                "incorrect", False,
                "BLANK_INCORRECT" if str(test.get("id", "")).startswith("blank_") else "TEST_FAILED",
                test.get("feedback") or {
                    "en": "Your configuration is missing a required entry.",
                    "ar": "يفتقد ملف الإعداد إدخالًا مطلوبًا.",
                },
                str(test.get("id") or f"test_{index + 1}"), passed, len(required), execution,
            )
        return GradingResult(
            "correct", True, "CORRECT", {"en": "Correct!", "ar": "إجابة صحيحة!"},
            None, passed, len(required), execution,
        )

    @staticmethod
    def _check(code: str, test: dict[str, Any]) -> bool:
        kind = test.get("type")
        if kind == "text_changed":
            return text_fingerprint(code) != str(test.get("starter_fingerprint", ""))
        patterns = [str(pattern) for pattern in test.get("patterns", [])]
        flags = re.IGNORECASE | re.MULTILINE
        if kind == "regex_all":
            return bool(patterns) and all(re.search(pattern, code, flags) for pattern in patterns)
        if kind == "regex_none":
            return all(not re.search(pattern, code, flags) for pattern in patterns)
        if kind == "regex_ordered":
            position = 0
            for pattern in patterns:
                match = re.search(pattern, code[position:], flags)
                if not match:
                    return False
                position += match.end()
            return bool(patterns)
        return False
