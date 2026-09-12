"""
backend/seeds/run_two_tier_arabic.py

Two-tier Arabic lesson generation, run to completion over every lesson that
has no Arabic body yet.

    docker compose exec api python seeds/run_two_tier_arabic.py \
        --out /app/ar-216-two-tier.json

WHAT THIS IS NOT: a new generation strategy. Section-based chunking, the
per-section retry cap (2 attempts), the terminology gate, and the code
placeholder mechanism all come unmodified from seeds/generate_arabic_lessons.py
(draft_lesson, draft_title, review). This script does not touch any of that.
It adds exactly one thing generate_arabic_lessons.py did not have: an
orchestration layer that runs Tier 1 (gpt-4o-mini) over every lesson, then
Tier 2 (gpt-4o) over only what Tier 1 rejected, through the IDENTICAL
validation path both times, and reports the result.

The one code change made to generate_arabic_lessons.py to support this was
adding an optional `model_id` parameter to build_provider() — called with no
argument it behaves exactly as before (falls back to
settings.GENERATION_MODEL_ID), so Tier 1 and every other caller of that
function are unaffected. This is what lets Tier 2 ask for gpt-4o without
writing to settings, which would have leaked into mentor chat and grading.

TWO PASSES, so a lesson's Tier 1 result survives a resume even if Tier 2
never got to run for it:

    Pass 1 (Tier 1)  — every lesson without a saved result gets one gpt-4o-mini
                        attempt. Passes are written as PASSED_MINI, terminal.
                        Failures are written as PENDING_TIER2, not terminal —
                        that status is what lets a resumed run skip straight
                        to Tier 2 for that lesson instead of re-spending on
                        Tier 1.
    Pass 2 (Tier 2)  — every PENDING_TIER2 lesson gets one gpt-4o attempt,
                        through the same attempt()/review() path. Recovered
                        lessons become PASSED_GPT4O; the rest become
                        NEEDS_HUMAN_REVIEW. Both are terminal.

A resumed run skips any lesson already in a terminal state (PASSED_MINI,
PASSED_GPT4O, NEEDS_HUMAN_REVIEW) and picks PENDING_TIER2 ones up in Pass 2
without repeating Pass 1 for them. Pass --redo-human-review to reprocess
lessons already marked NEEDS_HUMAN_REVIEW from an earlier complete run.

IMPORT SAFETY: a NEEDS_HUMAN_REVIEW record's ar.content_ar and ar.title_ar
are left as empty strings. seeds/arabic_content.py's importer already treats
an empty Arabic value as "nothing to write for this column" — see
apply_workbook() and
tests/test_arabic_content_import.py::test_blank_arabic_does_not_overwrite_existing_content.
So a human-review record cannot publish a rejected draft even under an
accidental --apply; only PASSED_MINI and PASSED_GPT4O rows carry anything in
the columns the importer reads. The draft that WAS produced, and exactly why
it was rejected at each tier, is kept under generation.failed_draft /
generation.tier1 / generation.tier2 for a human to work from.

This script never writes to the database. It reads lessons and writes one
workbook file (plus a small machine-readable *.summary.json beside it).
"""
import argparse
import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.session import SessionLocal
import app.models.user, app.models.progress            # noqa: F401  (mapper graph)
import app.models.community, app.models.wallet         # noqa: F401
import app.models.auth_token, app.models.challenge     # noqa: F401
import app.models.exam                                 # noqa: F401
import app.models.tool_course                          # noqa: F401  (Lesson.tool_topic target)
from app.models.learning import Lesson

from seeds.generate_arabic_lessons import (
    build_provider, draft_lesson, draft_title, review, lesson_path,
    load_workbook,
)

# Tier 2 is fixed to gpt-4o by task spec, independent of whatever Tier 1's
# model is configured to. It is passed as an explicit override to
# build_provider() and never written to settings — see module docstring.
TIER2_MODEL_ID = "gpt-4o"

# Bounded resilience for TRANSIENT failures only — a dropped connection, a
# rate limit, a provider 5xx. This is NOT a content-quality retry: those are
# already capped at 2 attempts per section/title inside draft_lesson() and
# draft_title(), and that cap is untouched. A content rejection surfaces as
# ValueError from those functions and is never retried here — only anything
# that is NOT a ValueError (i.e. not a validated gate speaking) gets a
# bounded, backed-off second chance, because a 216-lesson unattended run
# should not lose an hour of paid work to one network blip.
TRANSIENT_MAX_ATTEMPTS = 3
TRANSIENT_BACKOFF_SECONDS = 5

STATUS_PASSED_MINI = "PASSED_MINI"
STATUS_PENDING_TIER2 = "PENDING_TIER2"
STATUS_PASSED_GPT4O = "PASSED_GPT4O"
STATUS_NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
TERMINAL_STATUSES = {STATUS_PASSED_MINI, STATUS_PASSED_GPT4O, STATUS_NEEDS_HUMAN_REVIEW}


def call_with_resilience(fn, *a, **kw):
    """Run fn, retrying only exceptions that are not ValueError.

    ValueError is how draft_lesson()/draft_title() signal a genuine content
    rejection from an already-validated gate — it is raised, not retried,
    here. Anything else (connection errors, rate limits, provider outages)
    gets up to TRANSIENT_MAX_ATTEMPTS with linear backoff before it is
    allowed to fail the attempt.
    """
    last = None
    for attempt_n in range(1, TRANSIENT_MAX_ATTEMPTS + 1):
        try:
            return fn(*a, **kw)
        except ValueError:
            raise
        except Exception as exc:
            last = exc
            if attempt_n < TRANSIENT_MAX_ATTEMPTS:
                time.sleep(TRANSIENT_BACKOFF_SECONDS * attempt_n)
                continue
            raise
    raise last  # pragma: no cover — loop always returns or raises above


def parent_info(lesson: Lesson) -> dict:
    """Where this lesson lives, for a reviewer who has only the workbook
    open and not the database — a track topic or a tool-course topic,
    never both (the two foreign keys are mutually exclusive)."""
    if lesson.topic:
        t = lesson.topic
        level = t.level
        track = level.track if level else None
        return {
            "kind": "track_topic",
            "topic_id": t.id,
            "topic_title": t.title,
            "level_title": level.title if level else None,
            "track_slug": track.slug if track else None,
            "track_title": track.title if track else None,
        }
    if lesson.tool_topic:
        tt = lesson.tool_topic
        course = tt.tool_course
        return {
            "kind": "tool_topic",
            "tool_topic_id": tt.id,
            "tool_topic_title": tt.title,
            "tool_course_slug": course.slug if course else None,
            "tool_course_title": course.title if course else None,
        }
    return {"kind": "unknown"}


def attempt(provider, lesson: Lesson, exemplar) -> dict:
    """One full attempt (body, then title) against one provider/model.

    Never raises for a content rejection — that is the whole point of this
    wrapper: draft_lesson()/draft_title() speak in exceptions, and this
    layer turns that into a result the orchestration loop can act on and
    persist. A transient error that survives call_with_resilience's retries
    is caught too, and recorded as a distinct "transient failure" reason
    rather than crashing the run.

    Body failure and title failure are reported independently (section 6 of
    the spec), but either one fails the attempt as a whole: a lesson cannot
    go to the workbook with an Arabic body and an English title.
    """
    result = {"ok": False, "content_ar": "", "title_ar": "", "meta": None,
              "verdict_warnings": [], "reasons": []}

    try:
        arabic, meta = call_with_resilience(draft_lesson, provider, lesson, exemplar)
    except ValueError as exc:
        result["reasons"].append(f"body: {exc}")
        return result
    except Exception as exc:
        result["reasons"].append(f"body: transient failure — {type(exc).__name__}: {exc}")
        return result

    result["meta"] = meta
    if meta["unresolved"]:
        result["reasons"].extend(f"section {n}" for n in meta["unresolved"])

    verdict = review(lesson.content, arabic)
    result["verdict_warnings"] = verdict.warnings
    if not verdict.ok:
        result["reasons"].extend(f"body: {p}" for p in verdict.problems)
        result["content_ar"] = arabic  # kept for a human even though rejected
        return result

    try:
        title_ar = call_with_resilience(draft_title, provider, lesson)
    except ValueError as exc:
        result["reasons"].append(f"title: {exc}")
        result["content_ar"] = arabic
        return result
    except Exception as exc:
        result["reasons"].append(f"title: transient failure — {type(exc).__name__}: {exc}")
        result["content_ar"] = arabic
        return result

    result.update(ok=True, content_ar=arabic, title_ar=title_ar)
    return result


def tier_summary(r: dict) -> dict:
    if r is None:
        return None
    meta = r["meta"] or {}
    return {
        "ok": r["ok"],
        "reasons": r["reasons"],
        "warnings": r["verdict_warnings"],
        "sections": meta.get("sections"),
        "retries": meta.get("retries"),
    }


def make_record(lesson: Lesson, status: str, r1: dict, r2: dict, exemplar_id) -> dict:
    final = r2 if (r2 is not None and r2["ok"]) else (r1 if (r1 is not None and r1["ok"]) else None)
    record = {
        "table": "lessons",
        "id": lesson.id,
        "path": lesson_path(lesson),
        "parent": parent_info(lesson),
        "en": {"title": lesson.title, "content": lesson.content},
        "ar": {
            "title_ar": final["title_ar"] if final else "",
            "content_ar": final["content_ar"] if final else "",
        },
        "generation": {
            "status": status,
            "tier": {STATUS_PASSED_MINI: "gpt-4o-mini",
                    STATUS_PASSED_GPT4O: "gpt-4o"}.get(status),
            "backend": settings.GENERATION_BACKEND,
            "tier1_model": settings.GENERATION_MODEL_ID,
            "tier2_model": TIER2_MODEL_ID,
            "exemplar_lesson_id": exemplar_id,
            "tier1": tier_summary(r1),
            "tier2": tier_summary(r2),
        },
    }
    if status == STATUS_NEEDS_HUMAN_REVIEW:
        reference = r2 if r2 is not None else r1
        record["generation"]["failed_draft"] = {
            "content_ar": reference["content_ar"] if reference else "",
            "title_ar": reference["title_ar"] if reference else "",
        }
    return record


def error_record(lesson: Lesson, exc: Exception) -> dict:
    """An unexpected failure in the orchestrator itself (not a content
    rejection, not a modeled transient error) — logged and quarantined as
    human-review rather than aborting the whole run. See module docstring,
    'Do not lose successful results because a later lesson failed.'"""
    return {
        "table": "lessons",
        "id": lesson.id,
        "path": lesson_path(lesson),
        "parent": parent_info(lesson),
        "en": {"title": lesson.title, "content": lesson.content},
        "ar": {"title_ar": "", "content_ar": ""},
        "generation": {
            "status": STATUS_NEEDS_HUMAN_REVIEW,
            "tier": None,
            "tier1": None,
            "tier2": None,
            "orchestrator_error": f"{type(exc).__name__}: {exc}",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Two-tier Arabic lesson generation (workbook only).")
    ap.add_argument("--out", required=True, help="workbook path (loaded and resumed if it exists)")
    ap.add_argument("--ids", help="comma-separated lesson ids — for testing the orchestrator itself")
    ap.add_argument("--limit", type=int, help="stop Pass 1 after this many NEW lessons")
    ap.add_argument("--sleep", type=float, default=0.3, help="seconds between lessons, per pass")
    ap.add_argument("--redo-human-review", action="store_true",
                    help="reprocess lessons already terminal as NEEDS_HUMAN_REVIEW")
    args = ap.parse_args()

    db = SessionLocal()
    try:
        if args.ids:
            wanted = [int(p) for p in args.ids.split(",") if p.strip()]
            lessons = (
                db.query(Lesson).filter(Lesson.id.in_(wanted)).order_by(Lesson.id).all()
            )
            missing = sorted(set(wanted) - {l.id for l in lessons})
            if missing:
                print(f"No lesson with id(s): {', '.join(map(str, missing))}", file=sys.stderr)
                return 1
        else:
            lessons = (
                db.query(Lesson)
                .filter(Lesson.content_ar.is_(None))
                .order_by(Lesson.id)
                .all()
            )
        total_source = len(lessons)

        book = load_workbook(args.out)
        by_id = {r["id"]: r for r in book["records"]}

        def status_of(lesson_id: int):
            rec = by_id.get(lesson_id)
            return rec["generation"]["status"] if rec else None

        exemplar = (
            db.query(Lesson)
            .filter(Lesson.content_ar.isnot(None))
            .order_by(Lesson.id)
            .first()
        )
        exemplar_id = exemplar.id if exemplar else None

        def save():
            book["records"] = [by_id[k] for k in sorted(by_id)]
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(book, fh, ensure_ascii=False, indent=2)

        print("=== Two-tier Arabic lesson generation ===")
        print(f"Tier 1 model: {settings.GENERATION_BACKEND}/{settings.GENERATION_MODEL_ID}")
        print(f"Tier 2 model: {settings.GENERATION_BACKEND}/{TIER2_MODEL_ID}")
        print(f"Source lessons: {total_source}")
        if exemplar:
            print(f"Style exemplar: lesson {exemplar.id} '{exemplar.title}'")
        print(flush=True)

        # ── Pass 1 — Tier 1, gpt-4o-mini ────────────────────────────────
        pending_tier1 = [
            l for l in lessons
            if status_of(l.id) not in TERMINAL_STATUSES
            and status_of(l.id) != STATUS_PENDING_TIER2
        ]
        if args.limit:
            pending_tier1 = pending_tier1[: args.limit]
        skipped_tier1 = total_source - len(pending_tier1) - sum(
            1 for l in lessons if status_of(l.id) == STATUS_PENDING_TIER2
        )

        print(f"--- Pass 1: {len(pending_tier1)} lesson(s) to draft on gpt-4o-mini "
              f"({skipped_tier1} already finalized, "
              f"{sum(1 for l in lessons if status_of(l.id) == STATUS_PENDING_TIER2)} "
              f"already pending Tier 2, skipped) ---", flush=True)

        provider_mini = build_provider()

        for n, lesson in enumerate(pending_tier1, start=1):
            label = f"[{n}/{len(pending_tier1)}] lesson {lesson.id} '{lesson.title[:44]}'"
            try:
                r1 = attempt(provider_mini, lesson, exemplar)
                if r1["ok"]:
                    print(f"{label}  ✓ passed (mini)")
                    by_id[lesson.id] = make_record(lesson, STATUS_PASSED_MINI, r1, None, exemplar_id)
                else:
                    for reason in r1["reasons"]:
                        print(f"{label}\n    ✗ {reason}")
                    by_id[lesson.id] = make_record(lesson, STATUS_PENDING_TIER2, r1, None, exemplar_id)
            except Exception as exc:
                print(f"{label}\n    ✗ orchestrator error: {type(exc).__name__}: {exc}")
                traceback.print_exc()
                by_id[lesson.id] = error_record(lesson, exc)
            save()
            if args.sleep:
                time.sleep(args.sleep)

        tier1_all = [r for r in by_id.values()
                    if r["generation"]["status"] in (STATUS_PASSED_MINI, STATUS_PENDING_TIER2)
                    or r["generation"]["status"] in (STATUS_PASSED_GPT4O, STATUS_NEEDS_HUMAN_REVIEW)]
        n_mini = sum(1 for r in by_id.values() if r["generation"]["status"] == STATUS_PASSED_MINI)
        n_rejected_t1 = sum(
            1 for r in by_id.values()
            if r["generation"]["status"] in (STATUS_PENDING_TIER2, STATUS_PASSED_GPT4O, STATUS_NEEDS_HUMAN_REVIEW)
        )

        print("\n=== TIER 1 — gpt-4o-mini ===")
        print(f"Total lessons:       {total_source}")
        print(f"Passed:              {n_mini}")
        print(f"Rejected:            {n_rejected_t1}")
        rejected_ids_t1 = sorted(
            r["id"] for r in by_id.values()
            if r["generation"]["status"] in (STATUS_PENDING_TIER2, STATUS_PASSED_GPT4O, STATUS_NEEDS_HUMAN_REVIEW)
        )
        print(f"\nRejected lesson IDs:\n{', '.join(map(str, rejected_ids_t1)) or '(none)'}")
        print(flush=True)

        # ── Pass 2 — Tier 2, gpt-4o, ONLY the Tier 1 rejects ────────────
        pending_tier2 = [
            l for l in lessons
            if status_of(l.id) == STATUS_PENDING_TIER2
            or (args.redo_human_review and status_of(l.id) == STATUS_NEEDS_HUMAN_REVIEW)
        ]

        print(f"--- Pass 2: {len(pending_tier2)} lesson(s) to retry on gpt-4o ---", flush=True)

        provider_4o = build_provider(model_id=TIER2_MODEL_ID) if pending_tier2 else None

        for n, lesson in enumerate(pending_tier2, start=1):
            label = f"[{n}/{len(pending_tier2)}] lesson {lesson.id} '{lesson.title[:44]}'"
            existing = by_id.get(lesson.id, {})
            # r1 is carried over from Pass 1 (or a prior run) so the final
            # record keeps the ORIGINAL Tier 1 failure reason, not just the
            # Tier 2 outcome.
            r1 = None
            prior_tier1 = existing.get("generation", {}).get("tier1")
            if prior_tier1:
                r1 = {"ok": prior_tier1["ok"], "reasons": prior_tier1["reasons"],
                      "verdict_warnings": prior_tier1["warnings"],
                      "meta": {"sections": prior_tier1["sections"], "retries": prior_tier1["retries"],
                              "unresolved": []},
                      "content_ar": existing.get("generation", {}).get("failed_draft", {}).get("content_ar", ""),
                      "title_ar": ""}
            try:
                r2 = attempt(provider_4o, lesson, exemplar)
                if r2["ok"]:
                    print(f"{label}  ✓ recovered (gpt-4o)")
                    by_id[lesson.id] = make_record(lesson, STATUS_PASSED_GPT4O, r1, r2, exemplar_id)
                else:
                    for reason in r2["reasons"]:
                        print(f"{label}\n    ✗ {reason}")
                    print(f"{label}\n    → needs human review")
                    by_id[lesson.id] = make_record(lesson, STATUS_NEEDS_HUMAN_REVIEW, r1, r2, exemplar_id)
            except Exception as exc:
                print(f"{label}\n    ✗ orchestrator error: {type(exc).__name__}: {exc}")
                traceback.print_exc()
                by_id[lesson.id] = error_record(lesson, exc)
            save()
            if args.sleep:
                time.sleep(args.sleep)

        n_4o = sum(1 for r in by_id.values() if r["generation"]["status"] == STATUS_PASSED_GPT4O)
        n_hr = sum(1 for r in by_id.values() if r["generation"]["status"] == STATUS_NEEDS_HUMAN_REVIEW)
        n_still_pending = sum(1 for r in by_id.values() if r["generation"]["status"] == STATUS_PENDING_TIER2)

        print("\n=== TIER 2 — gpt-4o ===")
        print(f"Input rejects:       {n_rejected_t1}")
        print(f"Recovered:           {n_4o}")
        print(f"Still rejected:      {n_hr}")
        remaining_ids = sorted(r["id"] for r in by_id.values()
                               if r["generation"]["status"] == STATUS_NEEDS_HUMAN_REVIEW)
        print(f"\nRemaining lesson IDs:\n{', '.join(map(str, remaining_ids)) or '(none)'}")

        n_mini = sum(1 for r in by_id.values() if r["generation"]["status"] == STATUS_PASSED_MINI)
        checked_total = n_mini + n_4o + n_hr + n_still_pending

        print("\n=== FINAL SUMMARY ===")
        print(f"Total source lessons:   {total_source}")
        print(f"Tier 1 passed:          {n_mini}")
        print(f"Tier 2 passed:          {n_4o}")
        print(f"Human review:           {n_hr}")
        if n_still_pending:
            print(f"Still pending Tier 2:   {n_still_pending}  (run was limited or interrupted — rerun to finish)")
        print(f"Import-ready:            {n_mini + n_4o}")
        print(f"Sum check:               {n_mini} + {n_4o} + {n_hr}"
              f"{f' + {n_still_pending} pending' if n_still_pending else ''}"
              f" = {checked_total}  (source: {total_source})  "
              f"{'OK' if checked_total == total_source else 'MISMATCH'}")
        print("\nEnglish source modified:     NO — this script only reads Lesson.content/.title")
        print("Production Arabic written:   NO — this script performs no database writes")
        print(f"Workbook:                     {args.out}")

        summary_path = args.out + ".summary.json"
        with open(summary_path, "w", encoding="utf-8") as fh:
            json.dump({
                "total_source_lessons": total_source,
                "tier1_model": settings.GENERATION_MODEL_ID,
                "tier2_model": TIER2_MODEL_ID,
                "passed_tier1": n_mini,
                "passed_tier2": n_4o,
                "needs_human_review": n_hr,
                "still_pending_tier2": n_still_pending,
                "import_ready": n_mini + n_4o,
                "rejected_lesson_ids_tier1": rejected_ids_t1,
                "human_review_lesson_ids": remaining_ids,
                "workbook": args.out,
            }, fh, ensure_ascii=False, indent=2)
        print(f"Machine-readable summary:    {summary_path}")

        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
