from __future__ import annotations
from pathlib import Path
import importlib.util, json, sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
manifest = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
lesson_files = sorted(ROOT.glob("M015-*/*.py"))
assert manifest["modules"] == 8
assert manifest["lessons"] == 64
assert len([p for p in ROOT.glob("M015-*") if p.is_dir()]) == 8
assert len(lesson_files) == 64
ids=[]; slugs=[]; minutes=0; projects=0
for p in lesson_files:
    source = p.read_text(encoding="utf-8")
    compile(source, str(p), "exec")
    spec = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    ids.append(m.LESSON_ID)
    slugs.append(m.LESSON_META["slug"])
    minutes += m.LESSON_META["duration_minutes"]
    assert len(m.EXERCISES) == 2
    assert len(m.QUIZ) == 3
    assert all("explanation" in q for q in m.QUIZ)
    assert m.TOPIC["id"] == m.LESSON_ID
    if m.MODULE_PROJECT is not None:
        projects += 1
assert ids == [f"L015-{i:03d}" for i in range(1,65)]
assert len(slugs) == len(set(slugs))
assert minutes == 4050, minutes
assert projects == 7, projects
assets = json.loads((ROOT / "manual_figures_notes.json").read_text(encoding="utf-8"))
req = sum(1 for x in assets["manual_figures"] if x["priority"] == "REQUIRED")
opt = sum(1 for x in assets["manual_figures"] if x["priority"] == "OPTIONAL")
assert (req, opt) == (2, 6)
assert (ROOT / "projects" / "final_capstone.json").exists()
print("PASS: COURSE-015 structural validation")
print("Modules: 8 | Lessons: 64 | Guided minutes: 4050 | Projects: 7 + capstone | Figures: 2 required + 6 optional")
