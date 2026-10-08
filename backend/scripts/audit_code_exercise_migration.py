"""Report every code exercise that still needs deterministic grading."""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.curriculum.loaders import load_all_courses


def find_unmigrated_seeds() -> list[dict[str, object]]:
    """Inspect the effective seed definitions after authoring completion.

    The legacy source dictionaries are completed at import time, so a literal
    AST scan would incorrectly report every generated deterministic test as
    missing.  Importing these five data-only modules reflects what is actually
    synchronized to the database.
    """
    items: list[dict[str, object]] = []
    modules = (
        "seed_tool_fastapi", "seed_tool_langchain", "seed_tool_langgraph",
        "seed_tool_llamaindex", "seed_tool_qdrant",
    )
    for module_name in modules:
        topics: list[dict[str, Any]] = importlib.import_module(f"seeds.{module_name}").TOPICS
        for topic in topics:
            for exercise in topic.get("exercises", []):
                if not exercise.get("starter_code"):
                    continue
                missing = [
                    field for field in ("solution_code", "language", "grading_tests")
                    if not exercise.get(field)
                ]
                if not missing:
                    continue
                items.append({
                    "module": module_name,
                    "topic": topic.get("slug"),
                    "title": exercise.get("title"),
                    "missing": missing,
                })
    return items


def find_pending_canonical() -> list[dict[str, object]]:
    """Return reviewed canonical exercises whose grading is not authored yet."""
    items: list[dict[str, object]] = []
    for course in load_all_courses():
        for lesson in course.lessons:
            for exercise in lesson.exercises:
                if exercise.exercise_type != "code_pending":
                    continue
                items.append({
                    "course_id": course.course_id,
                    "module_id": lesson.module_id,
                    "lesson_id": lesson.lesson_id,
                    "exercise_id": exercise.exercise_id,
                    "title": exercise.title,
                    "language": exercise.language,
                })
    return items


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit deterministic grading coverage for code exercises.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="omit the full per-exercise backlog from the JSON output",
    )
    parser.add_argument(
        "--allow-pending",
        action="store_true",
        help="report the backlog without returning a failing exit status",
    )
    args = parser.parse_args()

    pending = find_pending_canonical()
    seed_items = find_unmigrated_seeds()
    pending_by_course = dict(sorted(Counter(
        str(item["course_id"]) for item in pending
    ).items()))
    result: dict[str, object] = {
        "pending_canonical_count": len(pending),
        "pending_by_course": pending_by_course,
        "unmigrated_seed_count": len(seed_items),
    }
    if not args.summary:
        result["pending_canonical"] = pending
        result["unmigrated_seed_exercises"] = seed_items
    print(json.dumps(result, ensure_ascii=False, indent=2))
    has_backlog = bool(pending or seed_items)
    raise SystemExit(1 if has_backlog and not args.allow_pending else 0)


if __name__ == "__main__":
    main()
