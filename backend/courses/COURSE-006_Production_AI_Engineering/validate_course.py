from __future__ import annotations

import py_compile
from pathlib import Path
from course_data_loader import load_course

ROOT = Path(__file__).resolve().parent
EXPECTED_MODULES = 10
EXPECTED_LESSONS = 67
EXPECTED_GUIDED_MINUTES = 3230
EXPECTED_IDS = [f"L006-{i:03d}" for i in range(1, 68)]


def validate() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            errors.append(f"syntax: {path}: {exc}")

    payload = load_course()
    modules = payload["modules"]
    lessons = payload["lessons"]
    if len(modules) != EXPECTED_MODULES:
        errors.append(f"module count {len(modules)} != {EXPECTED_MODULES}")
    if len(lessons) != EXPECTED_LESSONS:
        errors.append(f"lesson count {len(lessons)} != {EXPECTED_LESSONS}")

    ids = [x["lesson_id"] for x in lessons]
    if sorted(ids) != EXPECTED_IDS:
        errors.append("lesson ID range/gaps mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate lesson IDs")

    slugs = [x["slug"] for x in lessons]
    if len(slugs) != len(set(slugs)):
        errors.append("duplicate lesson slugs")

    minutes = sum(int(x["guided_minutes"]) for x in lessons)
    if minutes != EXPECTED_GUIDED_MINUTES:
        errors.append(f"guided minutes {minutes} != {EXPECTED_GUIDED_MINUTES}")

    course = payload["course"]
    if course["lesson_id_range"] != "L006-001..L006-067":
        errors.append("frozen lesson range mismatch")

    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        print("VALIDATION: FAIL")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("VALIDATION: PASS")
    print("modules=10 lessons=67 guided_minutes=3230 guided_time=53h50m")
