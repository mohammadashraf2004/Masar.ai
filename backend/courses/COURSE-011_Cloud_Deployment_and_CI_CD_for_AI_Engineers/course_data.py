"""Repository-neutral loader for COURSE-011.

This deliberately does not assume Masar ORM/database field names.
Map the returned payload to the real application schema.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent

def _load_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def load_course_payload() -> dict:
    manifest = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
    modules_payload = []

    for module_dir in sorted((ROOT / "modules").iterdir()):
        if not module_dir.is_dir():
            continue
        module_manifest = json.loads((module_dir / "module_manifest.json").read_text(encoding="utf-8"))
        order = json.loads((module_dir / "lesson_order.json").read_text(encoding="utf-8"))
        lessons = []
        for filename in order:
            mod = _load_module_from_path(module_dir / filename)
            lessons.append({
                "meta": mod.LESSON_META,
                "topics": mod.TOPICS,
                "source_references": mod.SOURCE_REFERENCES,
                "figure_references": mod.FIGURE_REFERENCES,
                "markdown": mod.LESSON_MARKDOWN,
                "exercises": mod.EXERCISES,
                "quiz": mod.QUIZ,
                "project": mod.PROJECT,
            })
        modules_payload.append({
            "module": module_manifest,
            "lessons": lessons,
        })

    return {
        "course": manifest,
        "modules": modules_payload,
    }

if __name__ == "__main__":
    payload = load_course_payload()
    print(f"{payload['course']['course_id']}: {len(payload['modules'])} modules / "
          f"{sum(len(m['lessons']) for m in payload['modules'])} lessons")
