from pathlib import Path
import ast, importlib.util, json, re, sys

ROOT = Path(__file__).resolve().parent

def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m

def main():
    module_dirs = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("m014_"))
    assert len(module_dirs) == 10, f"Expected 10 module folders, got {len(module_dirs)}"
    lesson_files = []
    for d in module_dirs:
        lesson_files += sorted(d.glob("l014_*.py"))
    assert len(lesson_files) == 99, f"Expected 99 lesson files, got {len(lesson_files)}"

    ids, slugs, total_minutes, projects = [], [], 0, 0
    for p in lesson_files:
        ast.parse(p.read_text(encoding="utf-8"))
        m = load_module(p)
        ids.append(m.LESSON_ID)
        slugs.append(m.LESSON_META["slug"])
        total_minutes += m.LESSON_META["estimated_minutes"]
        assert len(m.EXERCISES) == 2, f"{m.LESSON_ID}: expected 2 exercises"
        assert len(m.QUIZ) == 3, f"{m.LESSON_ID}: expected 3 quiz questions"
        for q in m.QUIZ:
            assert 0 <= q["answer_index"] < len(q["choices"])
            assert q["explanation"]
        if m.PROJECT:
            projects += 1

    expected_ids = [f"L014-{i:03d}" for i in range(1,100)]
    assert sorted(ids) == expected_ids
    assert len(ids) == len(set(ids))
    assert len(slugs) == len(set(slugs))
    assert total_minutes == 5920, total_minutes
    assert projects == 10, projects

    assets = json.loads((ROOT / "assets_manifest.json").read_text(encoding="utf-8"))
    assert sum(x["priority"]=="required" for x in assets) == 11
    assert sum(x["priority"]=="optional" for x in assets) == 2

    manifest = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
    assert manifest["lessons"] == 99
    assert manifest["modules"] == 10
    assert manifest["guided_minutes"] == 5920

    print("COURSE-014 validation: PASS")
    print("module_count: PASS (10)")
    print("lesson_file_count: PASS (99)")
    print("python_syntax: PASS")
    print("unique_lesson_ids: PASS")
    print("unique_slugs: PASS")
    print("frozen_id_range: PASS (L014-001..L014-099)")
    print("exercises_per_lesson: PASS (2)")
    print("quiz_questions_per_lesson: PASS (3)")
    print("module_project_count: PASS (10)")
    print("guided_minutes: PASS (5920)")
    print("manual_figures: PASS (11 required + 2 optional)")

if __name__ == "__main__":
    main()
