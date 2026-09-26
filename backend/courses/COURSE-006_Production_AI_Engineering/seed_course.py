from __future__ import annotations

from typing import Protocol, Any
from course_data_loader import load_course


class MasarSeedAdapter(Protocol):
    """Implement these methods against the actual Masar repository/database models."""

    def ensure_course(self, course: dict[str, Any]) -> Any: ...
    def ensure_module(self, course_ref: Any, module: dict[str, Any]) -> Any: ...
    def ensure_lesson(self, module_ref: Any, lesson: dict[str, Any]) -> Any: ...


def seed(adapter: MasarSeedAdapter, *, dry_run: bool = True) -> dict[str, int]:
    """Idempotent-by-contract seed orchestration.

    The adapter must use stable IDs (COURSE-006, M006-xx, L006-xxx) and must not
    overwrite learner progress or unrelated existing records.
    """
    payload = load_course()
    if dry_run:
        return {
            "courses": 1,
            "modules": len(payload["modules"]),
            "lessons": len(payload["lessons"]),
        }

    course_ref = adapter.ensure_course(payload["course"])
    module_refs: dict[str, Any] = {}
    for module in payload["modules"]:
        module_refs[module["module_id"]] = adapter.ensure_module(course_ref, module)
    for lesson in payload["lessons"]:
        adapter.ensure_lesson(module_refs[lesson["module_id"]], lesson)
    return {"courses": 1, "modules": len(payload["modules"]), "lessons": len(payload["lessons"])}


if __name__ == "__main__":
    print(seed(adapter=None, dry_run=True))
