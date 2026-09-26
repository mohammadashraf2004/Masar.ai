"""Framework-neutral seed adapter for COURSE-013.

The project intentionally does not assume concrete ORM/database fields.
Use iter_topics() to obtain canonical payloads and map them inside the
Masar application layer.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module

def iter_topics():
    for path in sorted(ROOT.glob("M013-*/*.py")):
        if path.name in {"module_project.py", "guided_lab.py"}:
            continue
        mod = _load_module(path)
        if hasattr(mod, "LESSON_META") and hasattr(mod, "TOPIC"):
            yield {
                "meta": mod.LESSON_META,
                "topic": mod.TOPIC,
            }

def iter_module_projects():
    for path in sorted(ROOT.glob("M013-*/module_project.py")):
        mod = _load_module(path)
        if hasattr(mod, "PROJECT"):
            yield mod.PROJECT

def export_payload():
    return {
        "course": json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8")),
        "modules": json.loads((ROOT / "modules_manifest.json").read_text(encoding="utf-8")),
        "topics": list(iter_topics()),
        "projects": list(iter_module_projects()),
    }

if __name__ == "__main__":
    payload = export_payload()
    print(f"Loaded {len(payload['modules'])} modules and {len(payload['topics'])} lessons.")
