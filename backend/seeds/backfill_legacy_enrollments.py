"""
backend/seeds/backfill_legacy_enrollments.py

Pre-launch learners keep the courses they were already taking: each course a
learner worked in before the release window (tool-course enrollment or recorded
progress) gets an active `legacy_free` enrollment. See
app/services/billing/legacy_enrollments.py for the rules.

Run once the catalogue exists, after `alembic upgrade head`, the seeds and
`seeds/import_courses.py`. Pass the moment the release window began (before the
migrations ran); only accounts and activity from before it count:

    python seeds/backfill_legacy_enrollments.py --legacy-before 2026-10-09T18:00:00+00:00 --dry-run
    python seeds/backfill_legacy_enrollments.py --legacy-before 2026-10-09T18:00:00+00:00

Idempotent and additive: a second run reports nothing created or grandfathered.
"""
import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.schema_guard import require_migrated_schema  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.services.billing.legacy_enrollments import backfill_legacy_enrollments  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Grandfather pre-launch learners into the courses they were taking.")
    parser.add_argument("--legacy-before", required=True, type=datetime.fromisoformat, metavar="ISO-TIMESTAMP",
                        help="when the release window began, with its UTC offset, e.g. 2026-10-09T18:00:00+00:00")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, then roll back")
    args = parser.parse_args()

    require_migrated_schema()
    session = SessionLocal()
    try:
        report = backfill_legacy_enrollments(session, args.legacy_before)
        session.rollback() if args.dry_run else session.commit()
    except ValueError as exc:
        session.rollback()
        print(f"Refusing to run: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    print("DRY RUN - nothing written." if args.dry_run else "Done.")
    for key in ("pairs", "created", "grandfathered", "already_entitled", "left_inactive"):
        print(f"  {key}: {report[key]}")


if __name__ == "__main__":
    main()
