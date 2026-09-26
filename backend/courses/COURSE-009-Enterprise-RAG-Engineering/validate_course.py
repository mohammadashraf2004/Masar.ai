from __future__ import annotations
from pathlib import Path
import ast
import json
import zipfile

ROOT = Path(__file__).resolve().parent
EXPECTED_MODULES = 10
EXPECTED_LESSONS = 80
EXPECTED_MINUTES = 4335
EXPECTED_VISUALS = 14

def load_literal(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(f"{name} not found in {path}")

def main():
    module_dirs = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("M009-"))
    assert len(module_dirs) == EXPECTED_MODULES, len(module_dirs)

    files = []
    for d in module_dirs:
        assert (d / "module_project.py").exists()
        files.extend(sorted(d.glob("l009-*.py")))
    assert len(files) == EXPECTED_LESSONS, len(files)

    ids, slugs = [], []
    total_minutes = 0
    module_counts = {}
    for path in files:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        meta = load_literal(path, "LESSON_META")
        topic = load_literal(path, "TOPIC")
        ids.append(meta["lesson_id"])
        slugs.append(topic["slug"])
        total_minutes += topic["lesson"]["estimated_minutes"]
        module_counts[meta["module_id"]] = module_counts.get(meta["module_id"], 0) + 1
        assert len(topic["exercises"]) == 2
        assert len(topic["quiz"]["questions"]) == 3
        assert "TODO" not in topic["lesson"]["content"]

    assert sorted(ids) == [f"L009-{i:03d}" for i in range(1, 81)], sorted(ids)[:5]
    assert len(ids) == len(set(ids))
    assert len(slugs) == len(set(slugs))
    assert total_minutes == EXPECTED_MINUTES, total_minutes

    expected_counts = {
        "M009-01": 4, "M009-02": 8, "M009-03": 8, "M009-04": 8,
        "M009-05": 6, "M009-06": 10, "M009-07": 9, "M009-08": 9,
        "M009-09": 9, "M009-10": 9,
    }
    assert module_counts == expected_counts, module_counts

    visuals = json.loads((ROOT / "assets" / "visual_assets_manifest.json").read_text(encoding="utf-8"))
    assert len(visuals) == EXPECTED_VISUALS

    for extra in ["course_data_loader.py", "seed_course_009.py", "course_manifest.py"]:
        compile((ROOT / extra).read_text(encoding="utf-8"), extra, "exec")

    print("PASS: module_count")
    print("PASS: lesson_file_count")
    print("PASS: python_syntax")
    print("PASS: unique_lesson_ids")
    print("PASS: unique_slugs")
    print("PASS: frozen_id_range")
    print("PASS: exercise_count")
    print("PASS: quiz_count")
    print("PASS: module_project_count")
    print("PASS: total_guided_minutes")
    print("PASS: visual_asset_count")
    print("COURSE-009 validation complete.")

if __name__ == "__main__":
    main()
