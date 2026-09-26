from __future__ import annotations
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parent
EXPECTED_MODULES = 9
EXPECTED_LESSONS = 84
EXPECTED_MINUTES = 4260
EXPECTED_VISUALS = 29
EXPECTED_COUNTS = {
    "M010-01": 10, "M010-02": 14, "M010-03": 8, "M010-04": 7,
    "M010-05": 8, "M010-06": 14, "M010-07": 7, "M010-08": 8, "M010-09": 8,
}
EXPECTED_MODULE_MINUTES = {
    "M010-01": 435, "M010-02": 630, "M010-03": 435, "M010-04": 370,
    "M010-05": 410, "M010-06": 740, "M010-07": 350, "M010-08": 425, "M010-09": 465,
}

def load_literal(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(f"{name} not found in {path}")

def validate_embedded_python(markdown: str, path: Path):
    for idx, code in enumerate(re.findall(r"```python\n(.*?)```", markdown, flags=re.S), 1):
        ast.parse(code, filename=f"{path}::python_block_{idx}")

def main():
    module_dirs = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("M010-"))
    assert len(module_dirs) == EXPECTED_MODULES, len(module_dirs)

    files=[]
    for d in module_dirs:
        assert (d / "module_project.py").exists()
        compile((d / "module_project.py").read_text(encoding="utf-8"), str(d / "module_project.py"), "exec")
        files.extend(sorted(d.glob("l010-*.py")))
    assert len(files)==EXPECTED_LESSONS, len(files)

    ids=[]; slugs=[]; total=0; module_counts={}; module_minutes={}
    for path in files:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        meta=load_literal(path,"LESSON_META"); topic=load_literal(path,"TOPIC")
        ids.append(meta["lesson_id"]); slugs.append(topic["slug"])
        mins=topic["lesson"]["estimated_minutes"]; total += mins
        module_counts[meta["module_id"]]=module_counts.get(meta["module_id"],0)+1
        module_minutes[meta["module_id"]]=module_minutes.get(meta["module_id"],0)+mins
        assert len(topic["exercises"])==2
        assert len(topic["quiz"]["questions"])==3
        assert "TODO" not in topic["lesson"]["content"]
        validate_embedded_python(topic["lesson"]["content"], path)

    assert sorted(ids)==[f"L010-{i:03d}" for i in range(1,85)]
    assert len(ids)==len(set(ids))
    assert len(slugs)==len(set(slugs))
    assert total==EXPECTED_MINUTES, total
    assert module_counts==EXPECTED_COUNTS, module_counts
    assert module_minutes==EXPECTED_MODULE_MINUTES, module_minutes

    visuals=json.loads((ROOT/"assets"/"visual_assets_manifest.json").read_text(encoding="utf-8"))
    assert len(visuals)==EXPECTED_VISUALS
    lesson_id_set=set(ids)
    assert all(v["lesson_id"] in lesson_id_set for v in visuals)

    for extra in ["course_data_loader.py","seed_course_010.py","course_manifest.py"]:
        compile((ROOT/extra).read_text(encoding="utf-8"), extra, "exec")

    print("PASS: module_count")
    print("PASS: lesson_file_count")
    print("PASS: python_syntax")
    print("PASS: embedded_python_syntax")
    print("PASS: unique_lesson_ids")
    print("PASS: unique_slugs")
    print("PASS: frozen_id_range")
    print("PASS: exercise_count")
    print("PASS: quiz_count")
    print("PASS: module_project_count")
    print("PASS: total_guided_minutes")
    print("PASS: module_guided_minutes")
    print("PASS: visual_reference_count")
    print("COURSE-010 validation complete.")

if __name__ == "__main__":
    main()
