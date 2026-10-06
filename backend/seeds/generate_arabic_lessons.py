"""
backend/seeds/generate_arabic_lessons.py

Draft the Arabic-first body for lessons that don't have one, and write the
drafts into a workbook that seeds/arabic_content.py can then import.

    # one lesson, to judge the output before spending on the rest
    docker compose exec api python seeds/generate_arabic_lessons.py \
        --lesson-id 134 --out /app/arabic-lessons.json

    # everything still missing Arabic, resumable
    docker compose exec api python seeds/generate_arabic_lessons.py \
        --all --out /app/arabic-lessons.json

    # then, with the existing safety rails
    docker compose exec api python seeds/arabic_content.py import --in /app/arabic-lessons.json
    docker compose exec api python seeds/arabic_content.py import --in /app/arabic-lessons.json --apply

This never writes to the database. It produces a file for review, and the
importer — dry-run by default, transactional, English-preserving — is what
applies it. A generator with direct write access to production content is
not a thing worth building.

Three settings would have quietly ruined a bulk run, so this module sets its
own rather than inheriting the defaults (and does not modify them globally,
because mentor chat and grading depend on them):

  * `GENERATION_DEFAULT_MAX_TOKENS` is 1000. The average lesson is ~7,400
    English characters and Arabic runs about 1.5x longer, so nearly every
    lesson would have been cut off mid-sentence.
  * `INPUT_DEFAULT_MAX_CHARACTERS` is 10000, and 43 lessons are longer than
    that. `clip_input` would have silently dropped the tail of the English
    source, producing an Arabic lesson missing its ending with nothing in
    the output to indicate it.
  * Temperature 0.7 is right for a mentor conversation and too loose for
    faithful technical authoring.

Every draft is checked before it is written to the workbook — see `review`.
The check that matters most is that fenced code blocks come back
byte-identical: translated code is the one failure that silently teaches
something wrong.
"""
import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session

from app.content import terminology as T
from app.core.config import settings
from app.db.session import SessionLocal
import app.models.user, app.models.progress            # noqa: F401  (mapper graph)
import app.models.community, app.models.wallet         # noqa: F401
import app.models.auth_token, app.models.challenge     # noqa: F401
import app.models.exam                                 # noqa: F401
from app.models.learning import Lesson
from app.services.language.language_policy import build_policy
from app.services.llm.enums.LLMEnum import LLMEnum
from app.services.llm.providers.AnthropicProvider import AnthropicProvider
from app.services.llm.providers.OpenAIProvider import OpenAIProvider

# Headroom over the longest lesson (16,397 chars) so no English source is
# ever clipped, and enough output tokens for an Arabic body ~1.5x its length.
INPUT_MAX_CHARACTERS = 40_000
OUTPUT_MAX_TOKENS = 8_000
TEMPERATURE = 0.2
# Above this, a lesson is drafted section by section — see draft_lesson.
CHUNK_THRESHOLD = 3_500

from app.services.language.arabic_review import (  # noqa: F401  (re-exported for callers)
    FENCE,
    FENCE_BODY,
    INLINE_CODE,
    PLACEHOLDER,
    PLACEHOLDER_RE,
    protect_code,
    restore_code,
    placeholder_problems,
    Review,
    protected_vocabulary,
    terminology_problems,
    review,
)


SYSTEM_PROMPT = """You are authoring lesson content for Masar, an Arabic-first AI
engineering platform for students in Egypt and the MENA region.

You are NOT translating. You are re-authoring this lesson in Arabic for a reader
who thinks in Arabic and will work in English. The result should read as though
it was written in Arabic first, not as an English lesson run through a translator.

Rules for the body you produce:
- Keep the same Markdown structure as the source: the same headings in the same
  order, the same lists, the same tables.
- The source contains placeholders of the form ⟦CODE_0⟧, ⟦CODE_1⟧ and so on,
  each standing for a code block that has been removed. Copy every placeholder
  through UNCHANGED, on its own line, in the same position relative to the
  surrounding prose. Do not translate them, do not renumber them, do not add
  or remove any, and do not write code in their place.
- Fenced blocks tagged `text` (diagrams, workflows, formulas, worked examples, lists
  of labels) are part of the explanation and ARE translated. Keep each block's
  fence, its number of lines, its arrows and operators (→ ↓ + = × /), its numbers
  (as Latin digits) and every identifier, variable (X, y) and code-like name exactly
  as written; translate the words around them into natural Arabic, keeping the
  important technical term in English where it helps, e.g. `خوارزمية التعلّم
  (Learning algorithm)`. Never translate a table's or a sentence's words and leave
  half of them in English.
- Introduce a technical term the first time as `English (المعنى بالعربية)`, then
  use the English term alone from then on.
- Keep the teaching voice: direct, concrete, addressed to the student.
- Do not add, remove, or reorder sections. Do not add commentary about the
  translation.

Return ONLY the Markdown body. No preamble, no fences around the whole thing,
no explanation."""


# ─── Provider ─────────────────────────────────────────────────────────────

def build_provider(model_id: Optional[str] = None):
    """A provider configured for long-form authoring.

    Constructed directly rather than through LLMProviderFactory, because the
    factory injects the global generation defaults and those are sized for
    chat replies.

    `model_id` overrides `settings.GENERATION_MODEL_ID` for this call only —
    it never writes to settings, so it cannot leak into mentor chat or
    grading. This is how Tier 2 runs gpt-4o against only the Tier 1 rejects
    while Tier 1 (and the rest of the platform) stays on the configured
    model.
    """
    backend = (settings.GENERATION_BACKEND or "").strip().lower()
    common = dict(
        model_id=model_id or settings.GENERATION_MODEL_ID,
        default_max_tokens=OUTPUT_MAX_TOKENS,
        default_temperature=TEMPERATURE,
        default_input_max_characters=INPUT_MAX_CHARACTERS,
    )
    if backend == LLMEnum.ANTHROPIC.value:
        provider = AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY, **common)
    elif backend == LLMEnum.OPENAI.value:
        provider = OpenAIProvider(
            api_key=settings.OPENAI_API_KEY, api_url=settings.OPENAI_API_URL, **common
        )
    else:
        raise SystemExit(f"GENERATION_BACKEND is {backend!r} — expected 'openai' or 'anthropic'")

    if not provider.validate():
        raise SystemExit(f"No API key configured for GENERATION_BACKEND={backend}")
    return provider


# ─── Generation ───────────────────────────────────────────────────────────

def keep_list(text: str) -> List[str]:
    """Protected terms actually present in this text."""
    return [
        term for term in protected_vocabulary()
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", text, re.I)
    ]


def split_sections(masked: str) -> List[str]:
    """Split at top-level `## ` headings, keeping any preamble as its own part.

    Placeholders sit alone on their line, so a heading boundary never lands
    inside one.
    """
    parts, current = [], []
    for line in masked.split("\n"):
        if line.startswith("## ") and current:
            parts.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append("\n".join(current).strip())
    return [p for p in parts if p]


def group_sections(pieces: List[str], target: int = 1_200) -> List[str]:
    """Merge adjacent sections up to a target size.

    One call per heading is both wasteful and worse: a 15,000-character
    lesson split at every `##` became 43 separate requests, each one seeing
    a paragraph with no idea what came before it. Grouping keeps each request
    comfortably inside the size that drafts cleanly while giving the model
    enough surrounding context to stay consistent.
    """
    groups, current = [], ""
    for piece in pieces:
        if current and len(current) + len(piece) > target:
            groups.append(current)
            current = piece
        else:
            current = f"{current}\n\n{piece}" if current else piece
    if current:
        groups.append(current)
    return groups


def placeholders_in(text: str) -> List[int]:
    return sorted({int(n) for n in PLACEHOLDER_RE.findall(text)})


def prose_length(text: str) -> int:
    """Characters left once placeholders and heading marks are removed.

    A section that is a heading over a code block has nothing to translate,
    and demanding Arabic in it produces a failure that no retry can fix.
    """
    stripped = PLACEHOLDER_RE.sub("", text)
    stripped = re.sub(r"^#{1,6} ", "", stripped, flags=re.MULTILINE)
    return len(stripped.strip())


def section_issues(source_piece: str, draft_piece: str) -> List[str]:
    """Validate one section against its own source.

    Checking here rather than only at the end is what makes a failure
    recoverable: a lost placeholder or a translated term is a property of one
    section, and regenerating that section costs a fraction of regenerating —
    and re-reviewing — a 16,000-character lesson.
    """
    issues = []

    missing = [i for i in placeholders_in(source_piece) if i not in placeholders_in(draft_piece)]
    if missing:
        issues.append(
            "you dropped the code placeholder(s) "
            + ", ".join(PLACEHOLDER.format(i) for i in missing)
            + " — every one must appear exactly once, on its own line"
        )

    taught, _mentioned = terminology_problems(source_piece, draft_piece)
    if taught:
        # Quoting the English line each term came from turns a rule the model
        # has already ignored once into a concrete, locatable edit. Naming the
        # terms alone was not enough for stubborn cases like Deployment.
        examples = []
        for term in taught[:4]:
            pattern = re.compile(
                r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", re.I
            )
            line = next(
                (l.strip() for l in source_piece.split("\n") if pattern.search(l)), ""
            )
            if line:
                examples.append(f'    "{line[:110]}"')
        issues.append(
            "these terms must stay in Latin script and were translated or "
            "transliterated: " + ", ".join(taught)
            + ("\n  they appear here in the source:\n" + "\n".join(examples) if examples else "")
        )

    # Only demand Arabic where there is prose to write.
    if prose_length(source_piece) > 80 and not re.search(r"[؀-ۿ]", draft_piece):
        issues.append("the text came back with no Arabic in it")

    return issues


def draft_section(provider, system: str, lesson_title: str, piece: str,
                  part: tuple, attempts: int = 2):
    """Draft one section, retrying once with the specific faults named.

    Returns (text, retries_used, unresolved_issues).
    """
    index, total = part
    present = keep_list(piece)
    keep_note = ""
    if present:
        keep_note = (
            "\n\nThese exact tokens appear in this text and MUST appear in your "
            "Arabic version, in Latin script exactly as written, never translated "
            "and never in Arabic letters:\n" + ", ".join(sorted(present))
        )

    if total == 1:
        opening = f'Re-author this lesson in Arabic.\n\nLesson title: {lesson_title}'
        label = "--- LESSON BODY ---"
    else:
        opening = (
            f'Re-author section {index} of {total} of the lesson "{lesson_title}" in Arabic.\n'
            f"Return only this section. Do not add a document title, an introduction, "
            f"or a closing summary — the surrounding sections are handled separately."
        )
        label = "--- SECTION ---"

    text, issues = "", []
    for attempt in range(1, attempts + 1):
        correction = ""
        if issues:
            correction = (
                "\n\nYour previous attempt was rejected for the following. Fix these "
                "exactly and return the whole text again:\n- " + "\n- ".join(issues)
            )
        user = f"{opening}{keep_note}{correction}\n\n{label}\n{piece}"
        text = (provider.chat(system, [{"role": "user", "content": user}],
                              max_tokens=OUTPUT_MAX_TOKENS) or "").strip()
        issues = section_issues(piece, text)
        if not issues:
            return text, attempt - 1, []

    return text, attempts - 1, issues


def draft_lesson(provider, lesson: Lesson, exemplar: Optional[Lesson]):
    """Returns (arabic_body, metadata).

    Long lessons are drafted a section at a time. In a nine-lesson sample
    every lesson over 12,000 characters lost terms it was actively teaching,
    while the short ones passed cleanly: compliance decays across a long
    generation, and the fix is to stop asking for long generations.

    Raises ValueError when the assembled result still mishandles the code
    placeholders, so the caller rejects it rather than writing a lesson with
    code missing.
    """
    system = SYSTEM_PROMPT + "\n" + build_policy(language="ar", mode="arabic_first")

    if exemplar is not None and exemplar.content_ar:
        ex_en, _ = protect_code(exemplar.content)
        ex_ar, _ = protect_code(exemplar.content_ar)
        system += (
            "\n\nHere is a lesson already authored to this standard on this platform, "
            "with its code blocks removed the same way. Match its register, its "
            "handling of terminology, and its formatting.\n\n"
            "--- ENGLISH SOURCE ---\n" + ex_en[:2000] +
            "\n\n--- ARABIC AS PUBLISHED ---\n" + ex_ar[:3000]
        )

    masked_source, blocks = protect_code(lesson.content)
    # Measured on prose, not raw length: lesson 95 is 9,583 characters but
    # 32 code blocks, so masking left it under the threshold and it was never
    # split — while still carrying more prose than drafts cleanly in one go.
    if prose_length(masked_source) > CHUNK_THRESHOLD:
        pieces = group_sections(split_sections(masked_source))
    else:
        pieces = [masked_source]

    drafted, retries, notes = [], 0, []
    for i, piece in enumerate(pieces, start=1):
        text, used, unresolved = draft_section(
            provider, system, lesson.title, piece, (i, len(pieces))
        )
        drafted.append(text)
        retries += used
        notes.extend(f"section {i}/{len(pieces)}: {issue}" for issue in unresolved)

    masked_draft = "\n\n".join(p for p in drafted if p)

    problems = placeholder_problems(masked_draft, blocks)
    if problems:
        raise ValueError("; ".join(problems))

    meta = {
        "sections": len(pieces),
        "retries": retries,
        "unresolved": notes,
        "terms_taught": keep_list(masked_source),
        "exemplar_lesson_id": exemplar.id if exemplar is not None else None,
    }
    return restore_code(masked_draft, blocks), meta

def draft_title(provider, lesson: Lesson) -> str:
    """The title goes through the same terminology rules as the body.

    It did not at first, and the result was a body that correctly said
    "OpenAI API" under a heading that said "واجهة برمجة تطبيقات OpenAI" —
    the one string most visible in the sidebar and the lesson list.

    Raises ValueError when a term is lost, so the caller keeps the English
    title rather than publishing a mistranslated one.
    """
    present = [
        term for term in protected_vocabulary()
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])",
                     lesson.title, re.I)
    ]
    system = (
        "Give the Arabic form of this lesson title for an Arabic-first AI engineering "
        "platform. Keep technology names and technical terms in English, in Latin "
        "script — never translated, never written in Arabic letters. Return only the "
        "title, nothing else."
    )
    if present:
        system += (
            "\nThese tokens must appear unchanged in your answer: " + ", ".join(present)
        )

    def lost_from(title: str) -> List[str]:
        return [
            term for term in present
            if not re.search(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])",
                             title, re.I)
        ]

    # Retried like a section is. Titles were the most frequent single failure
    # in the sample — Docker and Evaluation both got translated — and they are
    # also the most visible string in the product, so one corrective attempt
    # is worth the handful of tokens it costs.
    title, lost = "", []
    for attempt in (1, 2):
        prompt = lesson.title
        if lost:
            prompt = (
                f"{lesson.title}\n\nYour previous answer translated "
                f"{', '.join(lost)}. Keep {'them' if len(lost) > 1 else 'it'} "
                f"in Latin script, exactly as spelled here."
            )
        out = (provider.chat(system, [{"role": "user", "content": prompt}],
                             max_tokens=200) or "").strip().strip('"')
        title = out.splitlines()[0] if out else ""
        lost = lost_from(title)
        if not lost:
            return title

    raise ValueError(f"title dropped {', '.join(lost)}")


# ─── Workbook ─────────────────────────────────────────────────────────────

def load_workbook(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            book = json.load(fh)
        if book.get("format") != "masar-arabic-workbook/1":
            raise SystemExit(f"{path} is not a masar-arabic-workbook/1 file")
        return book
    return {
        "format": "masar-arabic-workbook/1",
        "note": "Machine-drafted Arabic lesson bodies. Review before applying.",
        "records": [],
    }


def lesson_path(lesson: Lesson) -> str:
    topic = getattr(lesson, "topic", None) or getattr(lesson, "tool_topic", None)
    return f"{topic.title} / {lesson.title}" if topic else lesson.title


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft Arabic lesson bodies into a workbook.")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--lesson-id", type=int, help="draft exactly one lesson")
    scope.add_argument("--ids", help="comma-separated lesson ids, for a review batch")
    scope.add_argument("--all", action="store_true", help="every lesson with no Arabic body")
    parser.add_argument("--out", required=True, help="workbook to write (merged if it exists)")
    parser.add_argument("--limit", type=int, help="stop after this many lessons")
    parser.add_argument("--sleep", type=float, default=0.0, help="seconds between calls")
    parser.add_argument("--titles", action="store_true", help="also draft title_ar")
    args = parser.parse_args()

    db: Session = SessionLocal()
    try:
        if args.lesson_id:
            lessons = db.query(Lesson).filter(Lesson.id == args.lesson_id).all()
            if not lessons:
                print(f"No lesson with id {args.lesson_id}", file=sys.stderr)
                return 1
        elif args.ids:
            try:
                wanted = [int(part) for part in args.ids.split(",") if part.strip()]
            except ValueError:
                print(f"--ids must be comma-separated integers, got {args.ids!r}", file=sys.stderr)
                return 2
            found = db.query(Lesson).filter(Lesson.id.in_(wanted)).all()
            by_id = {lesson.id: lesson for lesson in found}
            missing = [i for i in wanted if i not in by_id]
            if missing:
                print(f"No lesson with id(s): {', '.join(map(str, missing))}", file=sys.stderr)
                return 1
            # Preserve the order the reviewer asked for.
            lessons = [by_id[i] for i in wanted]
        else:
            lessons = (
                db.query(Lesson)
                .filter(Lesson.content_ar.is_(None))
                .order_by(Lesson.id)
                .all()
            )
        if args.limit:
            lessons = lessons[: args.limit]

        book = load_workbook(args.out)
        already = {r["id"] for r in book["records"] if r.get("table") == "lessons"}
        todo = [l for l in lessons if l.id not in already]

        exemplar = (
            db.query(Lesson)
            .filter(Lesson.content_ar.isnot(None), Lesson.id != (args.lesson_id or -1))
            .order_by(Lesson.id)
            .first()
        )

        print(f"{settings.GENERATION_BACKEND}/{settings.GENERATION_MODEL_ID} · "
              f"max_tokens={OUTPUT_MAX_TOKENS} · temperature={TEMPERATURE}")
        print(f"{len(todo)} lesson(s) to draft"
              f"{f', {len(lessons) - len(todo)} already in the workbook' if lessons != todo else ''}")
        if exemplar:
            print(f"style exemplar: lesson {exemplar.id} '{exemplar.title}'")
        print()

        provider = build_provider()
        drafted = failed = 0

        for n, lesson in enumerate(todo, start=1):
            label = f"[{n}/{len(todo)}] lesson {lesson.id} '{lesson.title[:48]}'"
            try:
                arabic, meta = draft_lesson(provider, lesson, exemplar)
            except Exception as exc:
                print(f"{label}\n    ✗ {type(exc).__name__}: {exc}")
                failed += 1
                continue

            verdict = review(lesson.content, arabic)
            ratio = len(arabic) / max(len(lesson.content), 1)
            shape = f"{meta['sections']} section(s)"
            if meta["retries"]:
                shape += f", {meta['retries']} retry(ies)"
            print(f"{label}\n    {len(lesson.content)} → {len(arabic)} chars "
                  f"({ratio:.0%}) · {shape}")
            for note in meta["unresolved"]:
                print(f"    ! unresolved after retry — {note}")
            for w in verdict.warnings:
                print(f"    ! {w}")
            if not verdict.ok:
                for p in verdict.problems:
                    print(f"    ✗ {p}")
                print("    not written to the workbook")
                failed += 1
                continue

            title_ar, title_note = "", None
            if args.titles:
                try:
                    title_ar = draft_title(provider, lesson)
                except Exception as exc:
                    title_note = str(exc)
                    print(f"    ! title draft failed: {exc}")

            record = {
                "table": "lessons",
                "id": lesson.id,
                "path": lesson_path(lesson),
                "en": {"title": lesson.title, "content": lesson.content},
                "ar": {"title_ar": title_ar, "content_ar": arabic},
                # Everything a reviewer needs to judge a draft without
                # re-deriving it: how it was produced, what it was checked
                # against, and anything the checks could not resolve.
                "generation": {
                    "model": settings.GENERATION_MODEL_ID,
                    "backend": settings.GENERATION_BACKEND,
                    "english_chars": len(lesson.content),
                    "arabic_chars": len(arabic),
                    "length_ratio_pct": round(ratio * 100),
                    "sections": meta["sections"],
                    "retries": meta["retries"],
                    "status": "passed" if not meta["unresolved"] else "passed with notes",
                    "warnings": verdict.warnings,
                    "unresolved": meta["unresolved"],
                    "title_problem": title_note,
                    "terms_taught": meta["terms_taught"],
                    "exemplar_lesson_id": meta["exemplar_lesson_id"],
                },
            }

            book["records"].append(record)
            drafted += 1

            # Written after every lesson, so a run interrupted at lesson 180
            # keeps the first 179 and resumes rather than starting over.
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(book, fh, ensure_ascii=False, indent=2)

            if args.sleep:
                time.sleep(args.sleep)

        print(f"\n{drafted} drafted, {failed} rejected → {args.out}")
        print("Review the file, then:")
        print(f"  python seeds/arabic_content.py import --in {args.out}")
        return 0 if failed == 0 else 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
