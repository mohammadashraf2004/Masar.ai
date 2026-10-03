"""
backend/seeds/import_courses.py

Imports the course folders under backend/courses/ into the catalogue.

    python seeds/import_courses.py --validate-only     # check the folders, touch nothing
    python seeds/import_courses.py --dry-run           # run it all, roll it back, print the report
    python seeds/import_courses.py                     # import
    python seeds/import_courses.py --course COURSE-004 # one course

The lesson text is read from the files and copied into the database; nothing is
retyped or generated. What is imported per course: the modules (as course
topics), lessons, exercises, quizzes and projects, with stable `source_key`s so
running it again updates rows in place, never duplicates them, never deletes
one, and never touches a learner's enrolment or progress.

Order of operations (one transaction - a failure changes nothing):

  1. load every folder, then VALIDATE all of them (and the registry) - the run
     stops with the full list of problems before anything is written;
  2. create/update each course record and its content;
  3. bring the catalogue's relations to `seeds/curriculum.py` (course roles,
     prerequisites, stages, path templates) via `sync_curriculum`.

Run after `alembic upgrade head` and `seeds/seed_learning_paths.py`.
"""
import argparse
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.schema_guard import require_migrated_schema
from app.db.session import SessionLocal
import app.models.user             # noqa: F401
import app.models.learning         # noqa: F401
import app.models.progress         # noqa: F401
import app.models.community        # noqa: F401
import app.models.wallet           # noqa: F401
import app.models.auth_token       # noqa: F401
import app.models.answer_submission  # noqa: F401
import app.models.challenge        # noqa: F401
import app.models.exam             # noqa: F401
import app.models.tool_course      # noqa: F401
import app.models.learning_path    # noqa: F401

from app.services.curriculum import importer, validate
from app.services.curriculum.loaders import load_all_courses
from app.services.curriculum.spec import CourseSpec, CurriculumError
from seeds import curriculum as cfg
from seeds.sync_curriculum import ensure_curriculum_courses, sync_curriculum


def load_and_validate(only: List[str] | None = None) -> List[CourseSpec]:
    """Load every course folder and validate them together with the registry.
    Raises `CurriculumError` listing every problem found."""
    courses = load_all_courses()
    validate.validate_courses(courses)
    validate.validate_registry(
        courses, cfg.COURSE_DIRECTORY_COURSES, goals=cfg.GOALS,
        stage_courses={slug: members for slug, _t, _a, _p, _k, members in cfg.STAGES},
    )
    if only:
        wanted = {c.upper() for c in only}
        unknown = wanted - {c.course_id for c in courses}
        if unknown:
            raise CurriculumError([f"unknown course id(s): {', '.join(sorted(unknown))}"])
        courses = [c for c in courses if c.course_id in wanted]
    return courses


def import_courses(db, courses: List[CourseSpec]) -> List[importer.CourseReport]:
    """Import `courses` and sync the catalogue. Does not commit."""
    from seeds.seed_learning_paths import SKILLS  # noqa: F401  (skills are created by ensure_curriculum_courses)
    ensure_curriculum_courses(db)
    definitions: Dict[str, dict] = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    reports = [importer.import_course(db, spec, definitions[spec.course_id]) for spec in courses]
    sync_curriculum(db, dry_run=False, commit=False)
    return reports


def main() -> None:
    parser = argparse.ArgumentParser(description="Import the course folders under backend/courses/.")
    parser.add_argument("--validate-only", action="store_true", help="validate the folders and write nothing")
    parser.add_argument("--dry-run", action="store_true", help="import, print the report, roll everything back")
    parser.add_argument("--course", action="append", metavar="COURSE-NNN", help="import only this course (repeatable)")
    args = parser.parse_args()

    try:
        courses = load_and_validate(args.course)
    except CurriculumError as exc:
        print("The course folders are not valid - nothing was imported:\n" + str(exc), file=sys.stderr)
        raise SystemExit(1)

    lessons = sum(len(c.lessons) for c in courses)
    print(f"Validated {len(courses)} courses, {sum(len(c.modules) for c in courses)} modules, {lessons} lessons.")
    for note in validate.warnings(courses):
        print(f"  note: {note}")
    if args.validate_only:
        return

    require_migrated_schema()
    session = SessionLocal()
    try:
        reports = import_courses(session, courses)
        if args.dry_run:
            session.rollback()
        else:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    print(f"\n{'DRY RUN - nothing written.' if args.dry_run else 'Imported.'}")
    for r in reports:
        figures = f"  figures {r.assets}" if r.assets.created or r.assets.updated or r.assets.unchanged else ""
        print(f"  {r.course_id}: modules {r.modules}  lessons {r.lessons}  exercises {r.exercises}  "
              f"quizzes {r.quizzes}  projects {r.projects}{figures}")
        for note in r.notes:
            print(f"      note: {note}")
        for key in r.stale:
            print(f"      stale (kept, no longer in the folder): {key}")


if __name__ == "__main__":
    main()
