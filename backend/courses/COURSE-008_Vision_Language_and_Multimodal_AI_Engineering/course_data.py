"""COURSE-008 registry for Masar."""
from pathlib import Path
import json
ROOT=Path(__file__).parent
MANIFEST=json.loads((ROOT/"course_manifest.json").read_text(encoding="utf-8"))
COURSE_ID=MANIFEST["course_id"]
COURSE_TITLE=MANIFEST["course_title"]
MODULES=MANIFEST["module_inventory"]
ASSETS=json.loads((ROOT/"assets_manifest.json").read_text(encoding="utf-8"))
def lesson_files():
    return sorted((ROOT/"modules").glob("M008_*/*L008_*.py"))
