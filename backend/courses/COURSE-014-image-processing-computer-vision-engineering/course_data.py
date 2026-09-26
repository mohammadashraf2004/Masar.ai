"""Repository-neutral loader for COURSE-014 lesson seed files."""
from __future__ import annotations
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent

def load_lesson_files():
    files = []
    for module_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("m014_")):
        files.extend(sorted(module_dir.glob("l014_*.py")))
    return files

def load_course_data():
    lessons = []
    for path in load_lesson_files():
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        lessons.append({
            "lesson_id": module.LESSON_ID,
            "module_id": module.MODULE_ID,
            "lesson_meta": module.LESSON_META,
            "topic": module.TOPIC,
            "exercises": module.EXERCISES,
            "quiz": module.QUIZ,
            "project": module.PROJECT,
        })
    return lessons
