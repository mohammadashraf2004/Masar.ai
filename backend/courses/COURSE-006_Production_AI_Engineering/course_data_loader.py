from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def _load_symbol(path: Path, symbol: str) -> dict[str, Any]:
    spec = spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, symbol)


def load_course() -> dict[str, Any]:
    course = _load_symbol(ROOT / "course_manifest.py", "COURSE")
    lessons: list[dict[str, Any]] = []
    modules: list[dict[str, Any]] = []
    for module_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("m006_")):
        modules.append(_load_symbol(module_dir / "module_manifest.py", "MODULE"))
        for lesson_file in sorted(module_dir.glob("l006_*.py")):
            lessons.append(_load_symbol(lesson_file, "LESSON"))
    return {"course": course, "modules": modules, "lessons": lessons}


if __name__ == "__main__":
    payload = load_course()
    print(payload["course"]["course_id"], len(payload["modules"]), len(payload["lessons"]))
