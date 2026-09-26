"""COURSE-014 repository-neutral seed adapter.

This file intentionally does not import Masar ORM models because the exact
production repository contract was not supplied in this export request.

Integrate `load_course_data()` with the canonical Masar curriculum registry /
reconciliation layer in the application repository. Do not insert duplicate
course copies per career track; map the reusable course to track roles.
"""
from course_data import load_course_data

COURSE_ID = "COURSE-014"

def build_seed_payload():
    return load_course_data()

def seed_course_014():
    raise RuntimeError(
        "Repository-specific database insertion is intentionally disabled. "
        "Map build_seed_payload() to the production Masar ORM/repository contract first."
    )

if __name__ == "__main__":
    payload = build_seed_payload()
    print(f"{COURSE_ID}: loaded {len(payload)} lesson records.")
