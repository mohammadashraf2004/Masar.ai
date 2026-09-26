# -*- coding: utf-8 -*-
"""Read the entire Applied Deep Learning course as portable Python seed data.

Usage: python course_data.py
DATA ONLY: this script performs no database writes.
"""
from pathlib import Path
import importlib.util, json

ROOT = Path(__file__).resolve().parent
COURSE = json.loads((ROOT / "course_manifest.json").read_text(encoding="utf-8"))

def load_lesson(path):
    source = ROOT / path
    spec = importlib.util.spec_from_file_location(source.stem, source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TOPIC, module.SOURCE, module.MODERNIZATION

def get_modules(include_optional=True):
    result=[]
    for entry in COURSE["modules"]:
        if entry.get("optional") and not include_optional:
            continue
        topics=[load_lesson(x["file"])[0] for x in entry["lessons"]]
        result.append({"title":entry["arabic_title"],"description":entry["learning_objective"],
                       "order":int(entry["module_id"][1:]),"optional":entry.get("optional",False),"topics":topics})
    return result

LEVELS = get_modules(include_optional=True)

if __name__ == "__main__":
    topics=[t for m in LEVELS for t in m["topics"]]
    print("modules:",len(LEVELS),"lessons:",len(topics),
          "guided_minutes:",sum(t["lesson"]["estimated_minutes"] for t in topics),
          "code_exercises:",sum(len(t["exercises"]) for t in topics))
