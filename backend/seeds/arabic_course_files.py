r"""
backend/seeds/arabic_course_files.py

Work on the Arabic of the course folders (the ``ar/`` folder beside each course's English; the format
and the reasons for it are in app/services/curriculum/arabic.py).

    # what is translated, what is stale, what is broken - per course
    python seeds/arabic_course_files.py status
    python seeds/arabic_course_files.py status --course COURSE-001

    # the English a lesson's Arabic is made from, with code masked, and empty files to fill in
    python seeds/arabic_course_files.py skeleton --course COURSE-001 --lesson M01.L01
    python seeds/arabic_course_files.py skeleton --course COURSE-001 --lesson M01.L01 --write

    # write ar/<lesson>.md (the Arabic body, placeholders and markers as in the skeleton) and
    # ar/<lesson>.json (title, exercises, questions - from a small JSON file); the source hash is
    # computed here, so the file is never hand-hashed
    python seeds/arabic_course_files.py assemble --course COURSE-001 --lesson M01.L01 \
        --content body.md --rest rest.json [--force]

    # review aid: the Arabic phrases the lesson page swaps for an English glossary term
    python seeds/arabic_course_files.py glossary --course COURSE-001

    # fences to review before translating: untagged ones, and `text` ones that look like code
    python seeds/arabic_course_files.py audit --course COURSE-001

    # the whole course checked exactly as an import would check it (no database)
    python seeds/import_courses.py --validate-only

Nothing here touches the database. ``skeleton --write`` creates ``ar/<lesson>.json`` and an empty
``ar/<lesson>.md`` only if neither exists, so it can never overwrite work.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.curriculum import arabic
from app.services.language import arabic_review as R
from app.services.curriculum.loaders import COURSES_ROOT, course_dirs, course_id_of, load_course_dir
from app.services.curriculum.spec import CourseSpec


def _load(only: List[str]) -> List[CourseSpec]:
    out = []
    for directory in course_dirs(COURSES_ROOT):
        if only and course_id_of(directory) not in only:
            continue
        out.append(load_course_dir(directory))
    return out


def _folder(spec: CourseSpec) -> Path:
    return COURSES_ROOT / spec.source_dir / arabic.AR_DIR


def status(only: List[str]) -> int:
    broken = 0
    print(f"{'course':<12} {'lessons':>7} {'Arabic':>7} {'questions':>10} {'with twin':>10}  notes")
    for spec in _load(only):
        by_lesson = arabic.questions_by_lesson(spec)
        lessons = spec.lessons
        translated = [l for l in lessons if l.content_ar]
        questions = [q for l in lessons for q in by_lesson.get(l.lesson_id, [])]
        twinned = [q for q in questions if q.ar is not None]
        notes = []
        if spec.arabic_problems:
            notes.append(f"{len(spec.arabic_problems)} PROBLEMS")
            broken += 1
        stale = [w for w in spec.arabic_warnings if "older English" in w]
        if stale:
            notes.append(f"{len(stale)} stale")
        print(f"{spec.course_id:<12} {len(lessons):>7} {len(translated):>7} {len(questions):>10} {len(twinned):>10}  {', '.join(notes)}")
        for problem in spec.arabic_problems:
            print(f"    problem: {problem}")
        for warning in spec.arabic_warnings:
            print(f"    warning: {warning}")
    return 1 if broken else 0


def skeleton(course_id: str, lesson_id: str, write: bool) -> int:
    specs = _load([course_id])
    if not specs:
        print(f"no course {course_id}", file=sys.stderr)
        return 2
    spec = specs[0]
    lesson = next((l for l in spec.lessons if l.lesson_id == lesson_id), None)
    if lesson is None:
        print(f"no lesson {lesson_id} in {course_id}: {[l.lesson_id for l in spec.lessons]}", file=sys.stderr)
        return 2
    questions = arabic.questions_by_lesson(spec).get(lesson_id, [])
    english = arabic.source_payload(lesson, questions)
    template = {
        "schema_version": arabic.SCHEMA_VERSION,
        "lesson_id": lesson_id,
        "source_hash": arabic.source_hash(english),
        "title": "",
        "exercises": [{"id": e["id"], "title": "", "description": ""} for e in english["exercises"]],
        "questions": [
            {"question": "", "options": ["" for _ in q["options"]], "explanation": ""} for q in english["questions"]
        ],
    }
    if write:
        path, body = _folder(spec) / f"{lesson_id}.json", _folder(spec) / f"{lesson_id}.md"
        existing = [p for p in (path, body) if p.exists()]
        if existing:
            print(f"{existing[0]} already exists; not overwritten", file=sys.stderr)
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        body.write_text("", encoding="utf-8")
        print(f"wrote {path} and {body}")
        return 0
    print(json.dumps({"english": english, "template": template}, ensure_ascii=False, indent=2))
    return 0


def assemble(course_id: str, lesson_id: str, content: str, rest: str, force: bool) -> int:
    specs = _load([course_id])
    lesson = next((l for s in specs for l in s.lessons if l.lesson_id == lesson_id), None)
    if lesson is None:
        print(f"no lesson {lesson_id} in {course_id}", file=sys.stderr)
        return 2
    spec = specs[0]
    english = arabic.source_payload(lesson, arabic.questions_by_lesson(spec).get(lesson_id, []))
    extra = json.loads(Path(rest).read_text(encoding="utf-8"))
    data = {
        "schema_version": arabic.SCHEMA_VERSION,
        "lesson_id": lesson_id,
        "source_hash": arabic.source_hash(english),
        "title": extra["title"],
        "exercises": extra.get("exercises", []),
        "questions": extra.get("questions", []),
    }
    body, problem = arabic.read_body(Path(content))
    if body is None:
        print(problem, file=sys.stderr)
        return 2
    path, target = _folder(spec) / f"{lesson_id}.json", _folder(spec) / f"{lesson_id}.md"
    existing = [p for p in (path, target) if p.exists()]
    if existing and not force:
        print(f"{existing[0]} already exists; pass --force to replace it", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    target.write_text(body + "\n", encoding="utf-8")
    print(f"wrote {path} and {target}")
    return 0


_CODE_LIKE = re.compile(
    r"^\s*(import |from \S+ import |def |class |print\(|\$ |>>> |pip |git |curl |docker |return |[A-Za-z_][\w.]*\([^)]*\)\s*$)",
    re.MULTILINE,
)


def audit(only: List[str]) -> int:
    """Fences to look at BEFORE translating: an untagged one (is it code?) and a `text` one that
    looks like code (it will be translated, so confirm it is not executable). Exit 1 when any
    untagged fence exists - that needs a human decision."""
    untagged_total = 0
    for spec in _load(only):
        print(f"{spec.course_id}")
        for lesson in spec.lessons:
            kinds: dict = {}
            untagged, codeish = [], []
            for block in R.fences(lesson.content):
                info = R.fence_info(block)
                kinds[info or "(untagged)"] = kinds.get(info or "(untagged)", 0) + 1
                body = R._FENCE_PARTS.match(block).group(2)
                if info == "":
                    untagged.append(body)
                elif R.is_text_fence(block) and _CODE_LIKE.search(body):
                    codeish.append(body)
            untagged_total += len(untagged)
            print(f"  {lesson.lesson_id}: {kinds}")
            for body in untagged:
                print("    UNTAGGED (translated unless you tag it as code):")
                print("\n".join("      | " + line for line in body.strip("\n").split("\n")[:8]))
            for body in codeish:
                print("    text block that looks like code (translated; identifiers and numbers are kept):")
                print("\n".join("      | " + line for line in body.strip("\n").split("\n")[:4]))
    return 1 if untagged_total else 0


def glossary(only: List[str]) -> int:
    """For review: the Arabic phrases the lesson page replaces with an English glossary term (it does
    this by itself, from the glossary). Look for a phrase that is only PART of what you wrote."""
    for spec in _load(only):
        print(spec.course_id)
        for lesson in spec.lessons:
            texts = [lesson.content_ar or ""] + [f"{e.title_ar or ''}. {e.description_ar or ''}" for e in lesson.exercises]
            found = [r for text in texts for r in R.arabic_replacements(text)]
            print(f"  {lesson.lesson_id}: {len(found)} replacement(s)")
            for surface, preferred, context in found:
                print(f"    {surface} -> {preferred}   ...{context.replace(chr(10), ' ')}...")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_status = sub.add_parser("status")
    p_status.add_argument("--course", action="append", default=[])
    p_glossary = sub.add_parser("glossary")
    p_glossary.add_argument("--course", action="append", default=[])
    p_audit = sub.add_parser("audit")
    p_audit.add_argument("--course", action="append", default=[])
    p_skeleton = sub.add_parser("skeleton")
    p_skeleton.add_argument("--course", required=True)
    p_skeleton.add_argument("--lesson", required=True)
    p_skeleton.add_argument("--write", action="store_true")
    p_assemble = sub.add_parser("assemble")
    p_assemble.add_argument("--course", required=True)
    p_assemble.add_argument("--lesson", required=True)
    p_assemble.add_argument("--content", required=True)
    p_assemble.add_argument("--rest", required=True)
    p_assemble.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "status":
        return status(args.course)
    if args.command == "glossary":
        return glossary(args.course)
    if args.command == "audit":
        return audit(args.course)
    if args.command == "assemble":
        return assemble(args.course, args.lesson, args.content, args.rest, args.force)
    return skeleton(args.course, args.lesson, args.write)


if __name__ == "__main__":
    sys.exit(main())
