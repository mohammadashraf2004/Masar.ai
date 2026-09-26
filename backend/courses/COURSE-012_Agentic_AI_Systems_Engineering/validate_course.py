from __future__ import annotations
from pathlib import Path
import importlib.util
import json
import py_compile
import sys

ROOT = Path(__file__).resolve().parent

def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def main():
    errors = []
    warnings = []
    manifest = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
    assets = json.loads((ROOT / "assets_manifest.json").read_text(encoding="utf-8"))
    module_dirs = sorted(ROOT.glob("module_*"))
    lesson_files = sorted(ROOT.glob("module_*/lesson_*.py"), key=lambda p: int(p.stem.split("_")[-1]))

    if len(module_dirs) != 11:
        errors.append(f"Expected 11 modules, found {len(module_dirs)}")
    if len(lesson_files) != 91:
        errors.append(f"Expected 91 lesson files, found {len(lesson_files)}")

    ids, slugs = [], []
    minutes = 0
    project_count = 0

    for path in lesson_files:
        try:
            py_compile.compile(str(path), doraise=True)
            mod = load_module(path)
        except Exception as exc:
            errors.append(f"{path}: {exc}")
            continue

        ids.append(mod.LESSON_ID)
        slugs.append(mod.LESSON_META["slug"])
        minutes += mod.LESSON_META["estimated_minutes"]

        if len(mod.EXERCISES) != 2:
            errors.append(f"{mod.LESSON_ID}: expected 2 exercises")
        if len(mod.QUIZ) != 3:
            errors.append(f"{mod.LESSON_ID}: expected 3 quiz questions")
        if mod.PROJECT is not None:
            project_count += 1

    expected_ids = [f"L012-{i:03d}" for i in range(1, 92)]
    if ids != expected_ids:
        errors.append("Lesson IDs are not exactly contiguous L012-001..L012-091")
    if len(set(ids)) != len(ids):
        errors.append("Duplicate lesson IDs")
    if len(set(slugs)) != len(slugs):
        errors.append("Duplicate lesson slugs")
    if project_count != 11:
        errors.append(f"Expected 11 final-lesson module projects, found {project_count}")

    required = sum(1 for x in assets["assets"] if x["priority"] == "required")
    optional = sum(1 for x in assets["assets"] if x["priority"] == "optional")
    if required != 39:
        errors.append(f"Expected 39 required figure refs, found {required}")
    if optional != 13:
        errors.append(f"Expected 13 optional figure refs, found {optional}")

    for required_path in [
        ROOT / "README.md",
        ROOT / "course_data.py",
        ROOT / "seed_course_012.py",
        ROOT / "00-course-setup" / "local-mcp-node-setup.md",
        ROOT / "capstone" / "COURSE_012_CAPSTONE.md",
    ]:
        if not required_path.exists():
            errors.append(f"Missing {required_path.relative_to(ROOT)}")

    if minutes != manifest["duration_audit"]["sum_of_individual_lesson_estimates"]:
        errors.append("Lesson-minute audit mismatch")
    if minutes != manifest["declared_guided_minutes"]:
        warnings.append(
            f"Duration warning: individual lesson estimates total {minutes} min, "
            f"while the frozen course-level estimate is {manifest['declared_guided_minutes']} min. "
            "See course_manifest.json duration_audit."
        )

    # Loader smoke test
    try:
        sys.path.insert(0, str(ROOT))
        import course_data
        course = course_data.load_course()
        if len(course["lessons"]) != 91:
            errors.append("course_data loader did not return 91 lessons")
    except Exception as exc:
        errors.append(f"course_data loader failed: {exc}")

    print("COURSE-012 validation")
    print(f"modules={len(module_dirs)}")
    print(f"lessons={len(lesson_files)}")
    print(f"module_projects={project_count}")
    print(f"required_figures={required}")
    print(f"optional_figures={optional}")
    print(f"lesson_minutes={minutes}")

    for w in warnings:
        print("WARN:", w)

    if errors:
        for e in errors:
            print("ERROR:", e)
        raise SystemExit(1)

    print("PASS")

if __name__ == "__main__":
    main()
