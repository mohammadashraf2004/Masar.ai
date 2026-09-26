from __future__ import annotations
from pathlib import Path
import ast, importlib.util, json, sys

ROOT = Path(__file__).resolve().parent
EXPECTED_MODULES = 6
EXPECTED_LESSONS = 85
EXPECTED_IDS = [f"L011-{i:03d}" for i in range(1, 86)]

def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

errors = []
manifest = json.loads((ROOT/"course_manifest.json").read_text(encoding="utf-8"))
module_dirs = sorted(p for p in (ROOT/"modules").iterdir() if p.is_dir())

if len(module_dirs) != EXPECTED_MODULES:
    errors.append(f"Expected {EXPECTED_MODULES} modules, found {len(module_dirs)}")

ids, slugs = [], []
project_count = 0
lesson_files = []

for md in module_dirs:
    mm = json.loads((md/"module_manifest.json").read_text(encoding="utf-8"))
    order = json.loads((md/"lesson_order.json").read_text(encoding="utf-8"))
    if len(order) != mm["lesson_count"]:
        errors.append(f"{mm['module_id']}: lesson_order count mismatch")
    for fn in order:
        p = md/fn
        lesson_files.append(p)
        try:
            ast.parse(p.read_text(encoding="utf-8"))
            mod = load(p)
        except Exception as e:
            errors.append(f"{p.name}: Python/load error: {e}")
            continue
        meta = mod.LESSON_META
        ids.append(meta["lesson_id"])
        slugs.append(meta["slug"])
        if meta["course_id"] != manifest["course_id"]:
            errors.append(f"{meta['lesson_id']}: wrong course_id")
        if not mod.TOPICS:
            errors.append(f"{meta['lesson_id']}: missing topics")
        if not mod.SOURCE_REFERENCES:
            errors.append(f"{meta['lesson_id']}: missing source references")
        if len(mod.EXERCISES) != 2:
            errors.append(f"{meta['lesson_id']}: expected 2 exercises")
        if len(mod.QUIZ) != 3:
            errors.append(f"{meta['lesson_id']}: expected 3 quiz questions")
        if mod.PROJECT is not None:
            project_count += 1

if len(lesson_files) != EXPECTED_LESSONS:
    errors.append(f"Expected {EXPECTED_LESSONS} lesson files, found {len(lesson_files)}")
if ids != EXPECTED_IDS:
    errors.append("Lesson IDs do not exactly match frozen range L011-001..L011-085")
if len(ids) != len(set(ids)):
    errors.append("Duplicate lesson IDs")
if len(slugs) != len(set(slugs)):
    errors.append("Duplicate lesson slugs")
if project_count != EXPECTED_MODULES:
    errors.append(f"Expected {EXPECTED_MODULES} module projects, found {project_count}")

assets = json.loads((ROOT/"assets_manifest.json").read_text(encoding="utf-8"))
required = [a for a in assets if a["priority"] == "required"]
optional = [a for a in assets if a["priority"] == "optional"]
if manifest["totals"]["required_manual_figures"] != len(required):
    errors.append("Required figure count mismatch")
if manifest["totals"]["optional_manual_figures"] != len(optional):
    errors.append("Optional figure count mismatch")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALIDATION PASSED")
print(f"Modules: {len(module_dirs)}")
print(f"Lessons: {len(lesson_files)}")
print(f"Projects: {project_count}")
print(f"Required figures: {len(required)}")
print(f"Optional figures: {len(optional)}")
