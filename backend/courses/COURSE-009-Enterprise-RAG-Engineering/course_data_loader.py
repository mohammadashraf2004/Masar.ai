from __future__ import annotations
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent

def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def load_all_lessons():
    rows = []
    for module_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("M009-")):
        for path in sorted(module_dir.glob("l009-*.py")):
            m = _load(path)
            rows.append({
                "lesson_id": m.LESSON_ID,
                "module_id": m.MODULE_ID,
                "lesson_meta": m.LESSON_META,
                "topic": m.TOPIC,
                "path": str(path),
            })
    return rows

def load_module_projects():
    projects = {}
    for module_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("M009-")):
        path = module_dir / "module_project.py"
        m = _load(path)
        projects[m.MODULE_ID] = m.MODULE_PROJECT
    return projects

if __name__ == "__main__":
    lessons = load_all_lessons()
    print(f"Loaded {len(lessons)} COURSE-009 lessons.")
