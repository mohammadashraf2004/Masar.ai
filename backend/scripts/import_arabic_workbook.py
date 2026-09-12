#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Single-purpose, hardened importer for one Arabic content workbook into the
`lessons` table's `title_ar` / `content_ar` columns.

Written from scratch against the current schema (backend/app/models/learning.py,
migration 006_arabic_first_content) and the validated workbook format
("masar-arabic-workbook/1") — not copied from backend/seeds/arabic_content.py.
That importer is general-purpose (many tables); this one is intentionally
narrow and defensive, built for one specific, high-stakes import.

Connection: uses the application's own SessionLocal (app.db.session), so it
connects to whatever DATABASE_URL is set in its runtime environment. This
script never hardcodes a connection string — run it with the right
environment (dev, staging, production) already exported, exactly like any
other management command in this codebase.

Safety properties (all enforced, not just documented):
  1. Default mode is DRY RUN. No --apply => no writes, ever.
  2. Writing requires --apply.
  3. --apply without --confirm-production is refused.
  4. Wrong workbook SHA-256 => refused before the file is even parsed.
  5. Every workbook id must resolve to an existing lesson, and that lesson's
     English title AND content must match the workbook's recorded English
     verbatim, BEFORE any write is considered. Any mismatch anywhere aborts
     the entire run (see 12).
  6. Every one of the workbook's declared ids (1..216 by default) must be
     present exactly once; the workbook itself is schema-checked before any
     database call is made.
  7. See 5.
  8. The only attribute this script ever assigns is Lesson.title_ar or
     Lesson.content_ar. Grep this file for "setattr" / "= record" — there is
     no code path that touches .title, .content, or any other column.
  9. See 8.
  10. All DB work for one run happens in one SQLAlchemy session/transaction;
      --apply either commits once at the very end or not at all.
  11. Any validation failure -> db.rollback(), non-zero exit, no partial
      writes. There is no per-row commit.
  12. Validation runs for ALL 216 records before any row is touched; a
      failure on record #200 still aborts records #1-199 too, because
      nothing is written until every record has passed.
  13. Prints exact per-field counts: would-write / unchanged / conflict.
  14. Rows whose stored Arabic already matches the workbook byte-for-byte
      are printed and counted separately as "unchanged", not "would write".
  15. A field whose current DB value is non-empty AND differs from the
      workbook's value is a "conflict" and blocks the run unless
      --allow-overwrite is explicitly passed.
  16. Immediately before writing (inside the transaction, right before the
      setattr pass), every targeted row is re-fetched fresh and reclassified
      exactly as in the dry-run pass -- if anything about the database
      changed between validation and write, the run aborts rather than
      writing against stale assumptions.
  17. After staging all writes, the session is flushed (so UPDATEs are sent
      to the database inside the open transaction, not yet committed) and
      every touched row is re-read back and checked: Arabic now equals the
      workbook, title/content are unchanged. Only then is it committed.
  18. This script never creates, restores, or deletes a backup. That is a
      separate, already-completed operation.

Usage:
    # Dry run (default, safe, no writes):
    python backend/scripts/import_arabic_workbook.py --in /path/to/workbook.json

    # Real write, only after an explicit, separate approval:
    python backend/scripts/import_arabic_workbook.py --in /path/to/workbook.json \\
        --apply --confirm-production
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field as dc_field
from pathlib import Path

# The exact hash this script was built against. Any other workbook must be
# passed explicitly with --expected-sha256; the default is deliberately
# narrow so running this against the "wrong" file requires a conscious
# override, not a copy-paste of a similarly-named path.
DEFAULT_EXPECTED_SHA256 = (
    "38448be5fe8e0561401659e22b64b6a17488f4ed342cfb19482757f3e4bdae04"
)
EXPECTED_FORMAT = "masar-arabic-workbook/1"
EXPECTED_RECORD_COUNT = 216
EXPECTED_ID_RANGE = range(1, 217)


@dataclass
class FieldPlan:
    lesson_id: int
    field: str          # "title_ar" or "content_ar"
    current: str
    target: str
    status: str          # "unchanged" | "would_write" | "conflict"


@dataclass
class RowError:
    lesson_id: int
    reason: str


@dataclass
class Plan:
    field_plans: list = dc_field(default_factory=list)
    errors: list = dc_field(default_factory=list)  # RowError

    @property
    def ok(self) -> bool:
        return not self.errors

    def counts(self):
        c = {"unchanged": 0, "would_write": 0, "conflict": 0}
        for p in self.field_plans:
            c[p.status] += 1
        return c


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_and_check_workbook(path: Path, expected_sha256: str) -> dict:
    actual = sha256_of(path)
    if actual != expected_sha256:
        print(f"REFUSING TO RUN: SHA-256 mismatch for {path}")
        print(f"  expected: {expected_sha256}")
        print(f"  actual:   {actual}")
        print("Pass --expected-sha256 explicitly if this is intentionally a "
              "different, already-verified workbook. Not doing so as a "
              "default is the point of this check.")
        sys.exit(1)
    print(f"SHA-256 verified: {actual}")

    with open(path, encoding="utf-8") as fh:
        wb = json.load(fh)

    if wb.get("format") != EXPECTED_FORMAT:
        print(f"REFUSING TO RUN: unrecognised workbook format {wb.get('format')!r}, "
              f"expected {EXPECTED_FORMAT!r}")
        sys.exit(1)

    records = wb.get("records") or []
    if len(records) != EXPECTED_RECORD_COUNT:
        print(f"REFUSING TO RUN: expected exactly {EXPECTED_RECORD_COUNT} records, "
              f"found {len(records)}")
        sys.exit(1)

    ids = [r.get("id") for r in records]
    missing = sorted(set(EXPECTED_ID_RANGE) - set(ids))
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    unexpected = sorted(set(ids) - set(EXPECTED_ID_RANGE))
    if missing or dupes or unexpected:
        print(f"REFUSING TO RUN: id set is not exactly {{1..{EXPECTED_RECORD_COUNT}}}")
        print(f"  missing: {missing or 'none'}  duplicate: {dupes or 'none'}  "
              f"unexpected: {unexpected or 'none'}")
        sys.exit(1)

    for r in records:
        rid = r["id"]
        en = r.get("en") or {}
        ar = r.get("ar") or {}
        if not (en.get("title") or "").strip() or not (en.get("content") or "").strip():
            print(f"REFUSING TO RUN: record {rid} has an empty English title/content")
            sys.exit(1)
        if not (ar.get("title_ar") or "").strip() or not (ar.get("content_ar") or "").strip():
            print(f"REFUSING TO RUN: record {rid} has an empty Arabic title_ar/content_ar")
            sys.exit(1)

    print(f"workbook structurally valid: {len(records)} records, "
          f"ids {{1..{EXPECTED_RECORD_COUNT}}} exactly, all fields non-empty")
    return wb


def build_plan(db, records: list) -> Plan:
    """Read-only pass: classify every field of every record. Never writes."""
    from app.models.learning import Lesson

    plan = Plan()
    for r in sorted(records, key=lambda r: r["id"]):
        rid = r["id"]
        row = db.query(Lesson).filter(Lesson.id == rid).first()
        if row is None:
            plan.errors.append(RowError(rid, "no lesson with this id exists in the database"))
            continue

        en_title, en_content = r["en"]["title"], r["en"]["content"]
        if row.title != en_title:
            plan.errors.append(RowError(
                rid, f"English title in database does not match workbook -- "
                     f"db={row.title!r} workbook={en_title!r}"))
        if row.content != en_content:
            plan.errors.append(RowError(
                rid, "English content in database does not match workbook "
                     f"({len(row.content or '')} vs {len(en_content)} chars)"))

        for field_name in ("title_ar", "content_ar"):
            current = getattr(row, field_name) or ""
            target = r["ar"][field_name]
            if current == target:
                status = "unchanged"
            elif current == "":
                status = "would_write"
            else:
                status = "conflict"
            plan.field_plans.append(FieldPlan(rid, field_name, current, target, status))

    return plan


def print_plan_summary(plan: Plan, *, allow_overwrite: bool) -> bool:
    """Returns True iff it is safe to proceed (no errors, no unresolved conflicts)."""
    counts = plan.counts()
    conflicts = [p for p in plan.field_plans if p.status == "conflict"]

    print(f"\nfields checked: {len(plan.field_plans)} "
          f"({len(plan.field_plans) // 2} lessons x 2 fields)")
    print(f"  unchanged (already current):  {counts['unchanged']}")
    print(f"  would write (new Arabic):     {counts['would_write']}")
    print(f"  conflict (existing, differs): {counts['conflict']}")

    if plan.errors:
        print(f"\n{len(plan.errors)} ROW ERROR(S) -- aborting, nothing will be written:")
        for e in plan.errors:
            print(f"  id {e.lesson_id}: {e.reason}")
        return False

    if conflicts and not allow_overwrite:
        print(f"\n{len(conflicts)} CONFLICT(S) -- existing Arabic differs from the "
              f"workbook and would be overwritten. Aborting, nothing will be "
              f"written. Re-run with --allow-overwrite if this is intended:")
        for p in conflicts:
            print(f"  id {p.lesson_id}.{p.field}: "
                  f"{len(p.current)} existing chars -> {len(p.target)} workbook chars")
        return False

    if conflicts and allow_overwrite:
        print(f"\n{len(conflicts)} conflict(s) will be OVERWRITTEN "
              f"(--allow-overwrite was given):")
        for p in conflicts:
            print(f"  id {p.lesson_id}.{p.field}")

    return True


def apply_writes(db, records: list, plan: Plan, *, allow_overwrite: bool) -> None:
    """Only called when --apply --confirm-production were both given, and
    print_plan_summary already returned True for a plan built moments ago.
    Re-validates from scratch against fresh rows before writing anything."""
    from app.models.learning import Lesson

    # (16) verify database state immediately before writing: rebuild the
    # plan fresh, right now, inside this same transaction, rather than
    # trusting the read taken before the operator confirmed --apply.
    fresh_plan = build_plan(db, records)
    if not fresh_plan.ok:
        raise RuntimeError(
            f"database state changed since the dry run -- {len(fresh_plan.errors)} "
            f"new row error(s); aborting write"
        )
    fresh_conflicts = [p for p in fresh_plan.field_plans if p.status == "conflict"]
    if fresh_conflicts and not allow_overwrite:
        raise RuntimeError(
            f"database state changed since the dry run -- {len(fresh_conflicts)} "
            f"new conflict(s); aborting write"
        )

    by_id = {r["id"]: r for r in records}
    touched_ids = set()
    for p in fresh_plan.field_plans:
        if p.status == "unchanged":
            continue
        if p.status == "conflict" and not allow_overwrite:
            continue  # already fatal above; unreachable, kept for clarity
        row = db.query(Lesson).filter(Lesson.id == p.lesson_id).first()
        setattr(row, p.field, p.target)  # ONLY title_ar / content_ar ever assigned
        touched_ids.add(p.lesson_id)

    db.flush()  # send UPDATEs now, still inside the open transaction

    # (17) post-write verification, inside the same transaction, before commit.
    post_errors = []
    for rid in touched_ids:
        row = db.query(Lesson).filter(Lesson.id == rid).first()
        record = by_id[rid]
        if row.title != record["en"]["title"] or row.content != record["en"]["content"]:
            post_errors.append(f"id {rid}: English drifted during write")
        if row.title_ar != record["ar"]["title_ar"] or row.content_ar != record["ar"]["content_ar"]:
            post_errors.append(f"id {rid}: Arabic does not match workbook after flush")

    if post_errors:
        db.rollback()
        raise RuntimeError("post-write verification failed, rolled back:\n  " +
                          "\n  ".join(post_errors))

    print(f"\npost-write verification passed for {len(touched_ids)} touched lesson(s)")
    db.commit()
    print(f"COMMITTED: {len(touched_ids)} lesson(s) updated.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="in_path", required=True, help="workbook JSON path")
    parser.add_argument("--expected-sha256", default=DEFAULT_EXPECTED_SHA256)
    parser.add_argument("--apply", action="store_true",
                        help="write to the database (default: dry run only)")
    parser.add_argument("--confirm-production", action="store_true",
                        help="required alongside --apply, no other effect")
    parser.add_argument("--allow-overwrite", action="store_true",
                        help="permit overwriting existing, non-matching Arabic content")
    args = parser.parse_args()

    if args.apply and not args.confirm_production:
        print("REFUSING TO RUN: --apply requires --confirm-production as well. "
              "This is intentional -- there is no single flag that writes.")
        return 1

    path = Path(args.in_path)
    if not path.is_file():
        print(f"REFUSING TO RUN: no such file: {path}")
        return 1

    wb = load_and_check_workbook(path, args.expected_sha256)
    records = wb["records"]

    # Standard model-import block: SQLAlchemy's mapper registry must see
    # every model class before any query touches a relationship, or it
    # raises InvalidRequestError for unrelated tables.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from app.db.session import SessionLocal
    import app.models.user, app.models.progress            # noqa: F401
    import app.models.community, app.models.wallet         # noqa: F401
    import app.models.auth_token, app.models.challenge     # noqa: F401
    import app.models.exam, app.models.tool_course         # noqa: F401
    import app.models.learning                              # noqa: F401

    db = SessionLocal()
    try:
        print("\n=== DRY RUN: classifying all fields against the live database ===")
        plan = build_plan(db, records)
        proceed = print_plan_summary(plan, allow_overwrite=args.allow_overwrite)

        if not args.apply:
            db.rollback()
            print("\nDRY RUN — no writes performed (pass --apply --confirm-production "
                  "to write, after this report has been reviewed).")
            return 0 if proceed else 1

        if not proceed:
            db.rollback()
            print("\n--apply given, but the dry-run plan above is not clean. "
                  "Aborting without writing.")
            return 1

        print("\n=== --apply --confirm-production given: writing ===")
        apply_writes(db, records, plan, allow_overwrite=args.allow_overwrite)
        return 0

    except Exception as e:
        db.rollback()
        print(f"\nABORTED, rolled back: {type(e).__name__}: {e}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
