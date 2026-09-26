"""Repository-neutral loader for COURSE-012 seed files."""
from __future__ import annotations
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent

def load_manifest() -> dict:
    return json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))

def iter_lesson_files():
    return sorted(ROOT.glob("module_*/lesson_*.py"))

def load_lesson(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return {
        "lesson_meta": module.LESSON_META,
        "topic": module.TOPIC,
        "exercises": module.EXERCISES,
        "quiz": module.QUIZ,
        "project": module.PROJECT,
    }

def load_course() -> dict:
    lessons = [load_lesson(path) for path in iter_lesson_files()]
    return {
        "manifest": load_manifest(),
        "lessons": lessons,
    }

if __name__ == "__main__":
    course = load_course()
    print(course["manifest"]["course_id"])
    print(f'lessons={len(course["lessons"])}')
