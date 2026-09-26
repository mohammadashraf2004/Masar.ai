from __future__ import annotations
import ast
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
course=json.loads((ROOT/"course_manifest.json").read_text(encoding="utf-8"))
modules=json.loads((ROOT/"modules_manifest.json").read_text(encoding="utf-8"))

lesson_files=[]
lesson_ids=[]
minutes=0

for path in sorted(ROOT.glob("M013-*/*.py")):
    if path.name in {"module_project.py","guided_lab.py"}:
        continue
    ast.parse(path.read_text(encoding="utf-8"))
    spec=importlib.util.spec_from_file_location(path.stem,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    if not hasattr(mod,"LESSON_META"):
        continue
    meta=mod.LESSON_META
    assert hasattr(mod,"TOPIC")
    assert meta["lesson_id"]==mod.TOPIC["lesson_id"]
    lesson_files.append(path)
    lesson_ids.append(meta["lesson_id"])
    minutes += meta["estimated_minutes"]
    assert len(mod.TOPIC["exercises"])==2
    assert len(mod.TOPIC["quiz"])==3

expected=[f"L013-{i:03d}" for i in range(1,89)]
assert sorted(lesson_ids)==expected, (len(lesson_ids), sorted(set(expected)-set(lesson_ids)))
assert len(set(lesson_ids))==88
assert len(modules)==10
assert len(lesson_files)==88
assert minutes==4255, minutes
assert course["lessons"]==88
assert course["modules"]==10
assert course["guided_minutes"]==4255

module_minutes=sum(m["estimated_minutes"] for m in modules)
assert module_minutes==4255

print("COURSE-013 validation passed: 10 modules, 88 lessons, 4255 guided minutes.")
