"""Trusted custom-check registry. Course JSON may name these; it cannot add code."""
import math
from collections.abc import Callable
from typing import Any

CustomChecker = Callable[[dict[str, Any], dict[str, Any]], bool]
CUSTOM_TESTS: dict[str, CustomChecker] = {}


def register_custom_test(name: str, checker: CustomChecker) -> None:
    if not name or name in CUSTOM_TESTS:
        raise ValueError(f"Custom test already registered: {name}")
    CUSTOM_TESTS[name] = checker


def _check_qdrant_payload(execution: dict[str, Any], _test: dict[str, Any]) -> bool:
    point = execution.get("variables", {}).get("point", {})
    value = point.get("value") if isinstance(point, dict) else None
    payload = value.get("payload") if isinstance(value, dict) else None
    required = {"text", "course", "doc_type", "source"}
    return isinstance(payload, dict) and required.issubset(payload) and all(payload[key] for key in required)


def _check_qdrant_vector(execution: dict[str, Any], _test: dict[str, Any]) -> bool:
    point = execution.get("variables", {}).get("point", {})
    value = point.get("value") if isinstance(point, dict) else None
    vector = value.get("vector") if isinstance(value, dict) else None
    return (
        isinstance(vector, list)
        and bool(vector)
        and all(
            not isinstance(item, bool)
            and isinstance(item, (int, float))
            and math.isfinite(item)
            for item in vector
        )
    )


CUSTOM_TESTS["check_qdrant_payload"] = _check_qdrant_payload
CUSTOM_TESTS["check_qdrant_vector"] = _check_qdrant_vector
