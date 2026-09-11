"""
backend/seeds/arabic_content.py

Export a translation workbook of every record that needs Arabic, and import
the filled-in workbook back.

    # 1. produce the workbook (read-only)
    docker compose exec api python seeds/arabic_content.py export --out /app/arabic.json

    # 2. an author fills in every "ar" block

    # 3. check it without touching a single row
    docker compose exec api python seeds/arabic_content.py import --in /app/arabic.json

    # 4. write it, in one transaction
    docker compose exec api python seeds/arabic_content.py import --in /app/arabic.json --apply

Design constraints, each of which came out of reading the existing code
rather than from a checklist:

  * **Identity is the primary key**, carried in the workbook by export.
    Titles repeat across tracks, so matching on them would silently write a
    RAG lesson's Arabic onto a different track's RAG lesson.

  * **English is never written.** Only `*_ar` columns are assigned. A reader
    who chooses English sees exactly what they saw before, and a botched
    import can be undone by nulling the Arabic columns.

  * **Idempotent.** A record whose Arabic already matches the workbook is
    counted as unchanged and not written. Re-running is a no-op.

  * **Transactional.** Every row is staged in one session and committed once
    at the end; any failure rolls the whole run back. There is no
    half-imported state to reason about.

  * **Quiz-safe.** `questions_ar` must mirror `questions` position for
    position, because grading reads the *English* blob
    (tracks_controller.submit_quiz) while the client submits positional
    indices. An Arabic option list in a different order would mark correct
    answers wrong. The importer therefore copies `correct` from English
    rather than trusting the file, and rejects any question whose option
    count differs.

  * **Dry run by default.** Writing requires `--apply`.
"""
import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
import app.models.user, app.models.progress            # noqa: F401  (mapper graph)
import app.models.community, app.models.wallet         # noqa: F401
import app.models.auth_token, app.models.challenge     # noqa: F401
import app.models.exam                                 # noqa: F401
from app.models.learning import (
    CareerTrack, Exercise, Lesson, Project, Quiz, Topic, TrackLevel,
)
from app.models.tool_course import ToolCourse, ToolTopic

# Fields the API strips out of a quiz before it reaches the browser. An
# Arabic value for any of these has no read path today, so the importer
# does not accept one — see `_normalise_questions_ar`.
ANSWER_KEY_FIELDS = ("correct", "correct_answer", "answer", "explanation", "solution")


# ─── Table registry ───────────────────────────────────────────────────────

@dataclass(frozen=True)
class TableSpec:
    """One content table and the English → Arabic column pairs on it."""
    name: str
    model: Any
    #: english column -> arabic column
    pairs: dict
    #: builds the human-readable location shown to the translator
    path: Callable[[Any], str] = field(default=lambda row: "")


def _track_path(row) -> str:
    return row.slug


def _level_path(row) -> str:
    return f"{row.track.slug} / L{row.order} {row.title}" if row.track else row.title


def _topic_path(row) -> str:
    level = row.level
    track = level.track if level else None
    parts = [track.slug if track else "?", level.title if level else "?", row.title]
    return " / ".join(parts)


def _under_topic(row) -> str:
    """Lessons, exercises, quizzes and projects hang off *either* a track
    topic or a tool-course topic — both foreign keys are nullable and only
    one is set. Naming only the track case would leave every tool-course
    record showing a bare title with no indication of where it lives."""
    if getattr(row, "topic", None):
        return f"{_topic_path(row.topic)} / {row.title}"
    tool_topic = getattr(row, "tool_topic", None)
    if tool_topic:
        return f"{_tool_topic_path(tool_topic)} / {row.title}"
    return row.title


def _tool_course_path(row) -> str:
    return row.slug


def _tool_topic_path(row) -> str:
    course = getattr(row, "tool_course", None)
    return f"{course.slug} / {row.title}" if course else row.title


TABLES: tuple = (
    TableSpec("career_tracks", CareerTrack,
              {"title": "title_ar", "description": "description_ar"}, _track_path),
    TableSpec("track_levels", TrackLevel,
              {"title": "title_ar", "description": "description_ar"}, _level_path),
    TableSpec("topics", Topic,
              {"title": "title_ar", "description": "description_ar"}, _topic_path),
    TableSpec("lessons", Lesson,
              {"title": "title_ar", "content": "content_ar"}, _under_topic),
    TableSpec("exercises", Exercise,
              {"title": "title_ar", "description": "description_ar"}, _under_topic),
    TableSpec("quizzes", Quiz,
              {"title": "title_ar", "questions": "questions_ar"}, _under_topic),
    TableSpec("projects", Project,
              {"title": "title_ar", "description": "description_ar"}, _under_topic),
    TableSpec("tool_courses", ToolCourse,
              {"title": "title_ar", "description": "description_ar"}, _tool_course_path),
    TableSpec("tool_topics", ToolTopic,
              {"title": "title_ar", "description": "description_ar"}, _tool_topic_path),
)

BY_NAME = {spec.name: spec for spec in TABLES}


# ─── Errors ───────────────────────────────────────────────────────────────

class ImportError_(Exception):
    """A problem with the workbook. Carries the record it came from so the
    author is told which entry to fix, not merely that something is wrong."""


# ─── Export ───────────────────────────────────────────────────────────────

def _quiz_skeleton(questions) -> list:
    """An empty Arabic questions blob shaped like the English one.

    `correct` is deliberately absent: the importer copies it from English,
    so there is nothing here for a translator to get wrong.
    """
    if not isinstance(questions, list):
        return []
    skeleton = []
    for q in questions:
        options = q.get("options") if isinstance(q, dict) else None
        count = len(options) if isinstance(options, list) else 0
        skeleton.append({"question": "", "options": [""] * count})
    return skeleton


def export_workbook(db: Session, only: Optional[set] = None) -> dict:
    """Every record with an empty Arabic column, plus its English source."""
    records = []
    for spec in TABLES:
        if only and spec.name not in only:
            continue
        for row in db.query(spec.model).all():
            english, arabic = {}, {}
            for en_col, ar_col in spec.pairs.items():
                en_value = getattr(row, en_col)
                english[en_col] = en_value
                if ar_col == "questions_ar":
                    arabic[ar_col] = _quiz_skeleton(en_value)
                else:
                    arabic[ar_col] = getattr(row, ar_col) or ""
            records.append({
                "table": spec.name,
                "id": row.id,
                "path": spec.path(row),
                "en": english,
                "ar": arabic,
            })
    return {
        "format": "masar-arabic-workbook/1",
        "note": (
            "Fill in every value under 'ar'. Leave a field empty to skip it. "
            "'en' is reference only and is never written back. For quizzes, "
            "keep the option order identical to the English list — grading "
            "uses positional indices against the English blob."
        ),
        "records": records,
    }


# ─── Validation ───────────────────────────────────────────────────────────

def _normalise_questions_ar(ar_questions, en_questions, where: str) -> Optional[list]:
    """Validate an Arabic questions blob and return the value to store.

    Returns None when there is nothing worth storing, so a workbook whose
    quiz section was left blank does not write an empty list over a column
    the reader treats as "no Arabic version".
    """
    if not ar_questions:
        return None
    if not isinstance(ar_questions, list):
        raise ImportError_(f"{where}: questions_ar must be a list")
    if not isinstance(en_questions, list):
        raise ImportError_(f"{where}: the English quiz has no question list to mirror")
    if len(ar_questions) != len(en_questions):
        raise ImportError_(
            f"{where}: {len(ar_questions)} Arabic questions against "
            f"{len(en_questions)} English ones — they must correspond one to one"
        )

    out = []
    for i, (ar_q, en_q) in enumerate(zip(ar_questions, en_questions), start=1):
        if not isinstance(ar_q, dict):
            raise ImportError_(f"{where} Q{i}: each question must be an object")

        leaked = [k for k in ar_q if k in ANSWER_KEY_FIELDS]
        if leaked:
            raise ImportError_(
                f"{where} Q{i}: remove {', '.join(sorted(leaked))} — the answer key is "
                f"copied from the English quiz and is stripped before it reaches a browser"
            )

        text = (ar_q.get("question") or "").strip()
        ar_options = ar_q.get("options") or []
        en_options = en_q.get("options") if isinstance(en_q, dict) else None
        en_options = en_options if isinstance(en_options, list) else []

        if not text and not any((o or "").strip() for o in ar_options):
            # Untranslated question inside an otherwise-translated quiz.
            # Partial quizzes would render half in each language.
            raise ImportError_(
                f"{where} Q{i}: left blank while other questions are translated — "
                f"a quiz must be fully Arabic or fully English"
            )
        if len(ar_options) != len(en_options):
            raise ImportError_(
                f"{where} Q{i}: {len(ar_options)} options against {len(en_options)} "
                f"in English — option order and count carry the answer key"
            )
        if not text:
            raise ImportError_(f"{where} Q{i}: question text is empty")
        if any(not (o or "").strip() for o in ar_options):
            raise ImportError_(f"{where} Q{i}: one or more options are empty")

        built = {"question": text, "options": [o.strip() for o in ar_options]}
        # Copied, never taken from the file: this is the field that decides
        # whether an answer is marked right.
        if isinstance(en_q, dict) and "correct" in en_q:
            built["correct"] = en_q["correct"]
        out.append(built)

    return out


# ─── Import ───────────────────────────────────────────────────────────────

@dataclass
class Outcome:
    updated: int = 0
    unchanged: int = 0
    skipped: int = 0
    fields_written: int = 0
    problems: list = field(default_factory=list)
    changes: list = field(default_factory=list)


def apply_workbook(db: Session, workbook: dict, *, apply: bool) -> Outcome:
    """Stage every record, then commit once — or roll back and report."""
    if workbook.get("format") != "masar-arabic-workbook/1":
        raise ImportError_(
            "Unrecognised workbook format. Expected 'masar-arabic-workbook/1'; "
            f"got {workbook.get('format')!r}"
        )

    result = Outcome()
    records = workbook.get("records") or []

    try:
        for entry in records:
            table = entry.get("table")
            row_id = entry.get("id")
            where = f"{table}#{row_id} ({entry.get('path') or '?'})"

            spec = BY_NAME.get(table)
            if spec is None:
                raise ImportError_(f"{where}: unknown table {table!r}")

            row = db.query(spec.model).filter(spec.model.id == row_id).first()
            if row is None:
                # A record deleted since the workbook was exported. Reported,
                # not fatal — the rest of the import is still valid.
                result.problems.append(f"{where}: no such row, skipped")
                result.skipped += 1
                continue

            arabic = entry.get("ar") or {}
            english = entry.get("en") or {}
            wrote_any = False

            for en_col, ar_col in spec.pairs.items():
                incoming = arabic.get(ar_col)

                if ar_col == "questions_ar":
                    value = _normalise_questions_ar(incoming, getattr(row, en_col), where)
                else:
                    value = (incoming or "").strip() or None

                if value is None:
                    continue

                # The workbook carried the English it was translated against.
                # If the English has since been rewritten, the Arabic may no
                # longer say the same thing.
                if en_col in english and ar_col != "questions_ar":
                    current_en = getattr(row, en_col)
                    if english[en_col] and current_en != english[en_col]:
                        result.problems.append(
                            f"{where}: English '{en_col}' changed since export — "
                            f"Arabic applied anyway, re-check this one"
                        )

                if getattr(row, ar_col) == value:
                    continue

                setattr(row, ar_col, value)
                result.fields_written += 1
                wrote_any = True
                result.changes.append(f"{where}: {ar_col}")

            if wrote_any:
                result.updated += 1
            else:
                result.unchanged += 1

        if apply:
            db.commit()
        else:
            db.rollback()

    except Exception:
        db.rollback()
        raise

    return result


# ─── Counts ───────────────────────────────────────────────────────────────

def coverage(db: Session) -> list:
    rows = []
    for spec in TABLES:
        total = db.query(spec.model).count()
        counts = {}
        for ar_col in spec.pairs.values():
            column = getattr(spec.model, ar_col)
            counts[ar_col] = db.query(spec.model).filter(column.isnot(None)).count()
        rows.append((spec.name, total, counts))
    return rows


def print_coverage(db: Session, heading: str) -> None:
    print(f"\n{heading}")
    print(f"  {'table':<16}{'rows':>7}   arabic")
    for name, total, counts in coverage(db):
        detail = "  ".join(f"{col}={n}" for col, n in counts.items())
        print(f"  {name:<16}{total:>7}   {detail}")


# ─── CLI ──────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[2].strip())
    sub = parser.add_subparsers(dest="command", required=True)

    p_export = sub.add_parser("export", help="write a translation workbook")
    p_export.add_argument("--out", required=True, help="path to write the JSON workbook to")
    p_export.add_argument("--tables", help="comma-separated subset, e.g. lessons,quizzes")

    p_import = sub.add_parser("import", help="apply a filled-in workbook")
    p_import.add_argument("--in", dest="path", required=True, help="path to the JSON workbook")
    p_import.add_argument(
        "--apply", action="store_true",
        help="actually write. Without it nothing is committed.",
    )

    sub.add_parser("counts", help="print Arabic coverage and exit")

    args = parser.parse_args()
    db = SessionLocal()
    try:
        if args.command == "counts":
            print_coverage(db, "Arabic coverage")
            return 0

        if args.command == "export":
            only = {t.strip() for t in args.tables.split(",")} if args.tables else None
            if only:
                unknown = only - set(BY_NAME)
                if unknown:
                    print(f"Unknown table(s): {', '.join(sorted(unknown))}", file=sys.stderr)
                    return 2
            workbook = export_workbook(db, only)
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(workbook, fh, ensure_ascii=False, indent=2)
            print(f"Wrote {len(workbook['records'])} records to {args.out}")
            return 0

        # import
        with open(args.path, encoding="utf-8") as fh:
            workbook = json.load(fh)

        print_coverage(db, "Before")
        try:
            outcome = apply_workbook(db, workbook, apply=args.apply)
        except ImportError_ as exc:
            print(f"\n✗ Refused: {exc}", file=sys.stderr)
            print("  Nothing was written.", file=sys.stderr)
            return 1

        print(f"\n{'Applied' if args.apply else 'Dry run — nothing written'}")
        print(f"  records updated   {outcome.updated}")
        print(f"  already current   {outcome.unchanged}")
        print(f"  skipped           {outcome.skipped}")
        print(f"  fields written    {outcome.fields_written}")
        for problem in outcome.problems:
            print(f"  ! {problem}")

        if args.apply:
            print_coverage(db, "After")
        else:
            print("\nRe-run with --apply to write these changes.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
