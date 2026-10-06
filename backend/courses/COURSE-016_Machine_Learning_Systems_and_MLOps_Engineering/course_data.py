from __future__ import annotations
from pathlib import Path
import importlib.util, json

ROOT = Path(__file__).resolve().parent

def load_manifest():
    return json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))

def iter_lesson_files(include_optional: bool = False):
    for path in sorted(ROOT.glob("M016-*/*.py")):
        if path.parent.name == "M016-11" and not include_optional:
            continue
        yield path

def load_lesson(path):
    path = Path(path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return {
        "LESSON_ID": module.LESSON_ID,
        "MODULE_ID": module.MODULE_ID,
        "LESSON_META": module.LESSON_META,
        "TOPIC": module.TOPIC,
        "EXERCISES": module.EXERCISES,
        "QUIZ": module.QUIZ,
        "MODULE_PROJECT": module.MODULE_PROJECT,
    }

def load_course(include_optional: bool = False):
    return {"manifest": load_manifest(), "lessons": [load_lesson(p) for p in iter_lesson_files(include_optional=include_optional)]}

def load_capstone():
    return json.loads((ROOT / "projects" / "final_capstone.json").read_text(encoding="utf-8"))
