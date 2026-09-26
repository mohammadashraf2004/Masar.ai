"""COURSE-004 registry for Masar.

This registry is framework/repository-light. Lesson files themselves follow the supplied
Masar seed-template field names.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
MANIFEST = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))
COURSE_ID = MANIFEST["course_id"]
COURSE_TITLE = MANIFEST["course_title"]
MODULES = MANIFEST["module_inventory"]

def lesson_files():
    return sorted((ROOT / "modules").glob("M004_*/*L004_*.py"))
