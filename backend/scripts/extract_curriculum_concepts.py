"""
backend/scripts/extract_curriculum_concepts.py

Regenerates the AI Vocabulary candidate-extraction artifact: every
`concepts` list in every course/module/lesson under `backend/courses/`,
plus per-course raw/distinct counts.

This is a research/dev tool, not part of the seed pipeline. The actual
canonical dictionary (`app/content/vocabulary_seed_terms.py` and
`vocabulary_seed_terms_expansion.py`) is hand-curated FROM this candidate
list — terms are picked, normalized and rejected by a person, never bulk-
imported. Nine of the fifteen courses (004/005/007/008/009/010/012/013/014)
carry a structured `concepts` field on their `LESSON_META`; the other six
(001/002/003/006/011/015) use older schemas with no such field, and are
recorded with empty concept lists here (their real signal is lesson titles/
bodies, read separately via `load_all_courses()` when curating).

Output is NOT committed to the repo (see .gitignore) — regenerate it with:

    python scripts/extract_curriculum_concepts.py [output_path]

Default output: backend/.generated/vocab_extraction_raw.json
"""
import ast
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, course_id_of

DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / ".generated" / "vocab_extraction_raw.json"


def _dict_literal(tree: ast.Module, name: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            try:
                return ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                return None
    return None


def _lesson_fields(path: Path) -> dict:
    """Extract lesson_id/module_id/title/learning_objective/concepts from a
    lesson file's LESSON_META (or LESSON/TOPIC, for schemas that carry the
    fields under a different name) via `ast.literal_eval` — the file is never
    executed."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return {"_error": f"{path}: {exc}"}

    merged: dict = {}
    for name in ("LESSON_META", "LESSON", "TOPIC"):
        data = _dict_literal(tree, name)
        if isinstance(data, dict):
            for key in ("lesson_id", "module_id", "title", "learning_objective", "concepts"):
                if key not in merged and key in data:
                    merged[key] = data[key]
                if key == "learning_objective" and key not in merged and "learning_objectives" in data:
                    merged[key] = data["learning_objectives"]
    return {
        "title": merged.get("title"),
        "learning_objective": merged.get("learning_objective"),
        "concepts": merged.get("concepts") or [],
    }


def extract(root: Path = COURSES_ROOT) -> dict:
    result: dict = {"_errors": [], "_notes": []}
    for course_dir in course_dirs(root):
        course_id = course_id_of(course_dir)
        modules: dict = {}
        for lesson_file in sorted(course_dir.rglob("*.py")):
            if "__pycache__" in lesson_file.parts or lesson_file.name in ("module.py", "module_manifest.py", "course_data.py", "course_project.py", "seed_course_015.py", "validate_course.py"):
                continue
            fields = _lesson_fields(lesson_file)
            if "_error" in fields:
                result["_errors"].append(fields["_error"])
                continue
            if not fields.get("title") and not fields.get("concepts"):
                continue  # not a lesson file (a helper/module file with no LESSON_META/TOPIC)
            module_id = lesson_file.parent.name
            modules.setdefault(module_id, {}).setdefault("lessons", {})[lesson_file.stem] = {
                "title": fields.get("title"),
                "learning_objective": fields.get("learning_objective"),
                "concepts": fields.get("concepts"),
            }
        result[course_id] = {"title": course_dir.name, "modules": modules}

    for course_id, course in result.items():
        if course_id.startswith("_"):
            continue
        raw = sum(len(l["concepts"]) for m in course["modules"].values() for l in m["lessons"].values())
        distinct = len({c.strip().lower() for m in course["modules"].values() for l in m["lessons"].values() for c in l["concepts"]})
        if raw == 0:
            result["_notes"].append(f"{course_id}: no `concepts` field in its lesson schema (0 extracted) — curate from lesson titles/bodies instead")

    return result


if __name__ == "__main__":
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = extract()
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    total_courses = len([k for k in data if not k.startswith("_")])
    print(f"Wrote {output_path} — {total_courses} courses, {len(data['_errors'])} errors, {len(data['_notes'])} notes")
