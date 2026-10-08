"""
app/services/curriculum/arabic.py

The Arabic text of a course, read from the ``ar/`` folder beside its English.

    COURSE-001_Machine_Learning/
        lessons/lesson_01_....py          the English, unchanged
        ar/_course.json                   course title, module titles and descriptions
        ar/M01.L01.md                     the lesson body, as a normal readable Markdown document
        ar/M01.L01.json                   that lesson's title, exercises and quiz, named by lesson id

Why files, not a database workbook: the importer rewrites every row it owns on each run, so Arabic
written straight into the catalogue is wiped by the next import. Arabic that lives in the course
folder is imported with the English every time, is reviewed in git like any other change, and is
checked here against the English it was made from.

The body is its own ``.md`` file so a reviewer opens a document, not a one-line JSON string full of
``\\n``. A lesson's ``.json`` holds everything else, and has no ``content`` key (two places for the
body would be two sources of truth)::

    {
      "schema_version": 1,
      "lesson_id": "M01.L01",
      "source_hash": "<hash of the English this was made from; `seeds/arabic_course_files.py skeleton` prints it>",
      "title": "...",
      "exercises": [{"id": "EX-...", "title": "...", "description": "..."}],
      "questions": [{"question": "...", "options": ["...", "..."], "explanation": "..."}]
    }

Code is never in the Arabic files. In the ``.md`` each fenced block is a numbered placeholder
(``⟦CODE_0⟧``, ``⟦CODE_1⟧`` ... on its own line), and the English's own block is put back at that spot
when the lesson is loaded, so a translation cannot alter code (and a reviewer reads prose, not code).
``questions`` is positional - the Nth entry is the Nth question the
English lesson ships - and its options are in the order the English authored them: the importer
reorders them if it rebalances the answer key. Neither the key nor ``correct`` is ever written here.

Nothing is imported from a file that has a fault. A fault is a structural mismatch with the English
(a missing or extra question, a different number of options, a dropped or invented code
placeholder, a taught term no longer in English); an Arabic file made from an older English text is
only a warning, so fixing a typo in the English does not stop an import.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.services.curriculum.spec import CourseSpec, LessonSpec, QuestionSpec
from app.services.language import arabic_review as R

AR_DIR = "ar"
COURSE_FILE = "_course.json"
SCHEMA_VERSION = 1
_ARABIC_LETTER = re.compile(r"[؀-ۿ]")
# Lines of prose that the lesson page turns into something: {{image:key}}, {{exercise:id}}, and the
# [[IMAGE_NEEDED: ...]] authoring placeholders. Code placeholders do not protect them.
# An image request may contain bracketed text (`[CLS]`, `[1, 4, 384]`), so one level of [...] is allowed inside it.
_MARKER = re.compile(r"\{\{[^{}\n]+\}\}|\[\[IMAGE_NEEDED(?:[^\[\]]|\[[^\[\]\n]*\])*\]\]")
# `{{image:key|caption}}`: the caption is text and gets translated, so only the key has to match.
_IMAGE_CAPTION = re.compile(r"^(\{\{(?:image|figure):[^|{}\n]+)\|[^{}\n]*\}\}$")


def markers(text: str) -> List[str]:
    """The lesson's markers in order, with the (translatable) caption of an image marker removed."""
    return [_IMAGE_CAPTION.sub(r"\1}}", m) for m in _MARKER.findall(text or "")]


# ─── The English a file is made from ────────────────────────────────────────

def questions_by_lesson(course: CourseSpec) -> Dict[str, List[QuestionSpec]]:
    """Each lesson's questions in authored order. After loading they live on the module quiz,
    tagged with the lesson they were written for."""
    out: Dict[str, List[QuestionSpec]] = {}
    for module in course.modules:
        if module.quiz is None:
            continue
        for question in module.quiz.questions:
            owner = question.lesson_ids[0] if question.lesson_ids else question.lesson_id
            out.setdefault(owner, []).append(question)
    return out


def source_payload(lesson: LessonSpec, questions: List[QuestionSpec]) -> Dict[str, Any]:
    """Everything a lesson's Arabic is a translation of, with code masked (code is not translated)."""
    return {
        "title": lesson.title,
        "content": R.protect_code(lesson.content or "")[0],
        "exercises": [
            {"id": e.exercise_id, "title": e.title, "description": e.description} for e in lesson.exercises
        ],
        "questions": [
            {"question": q.question, "options": list(q.options or []), "explanation": q.explanation}
            for q in questions
        ],
    }


def source_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


# ─── Reading and checking one lesson's file ─────────────────────────────────

def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _check_lesson(
    lesson: LessonSpec, questions: List[QuestionSpec], data: Any, masked: str, where: str, body_where: str,
) -> Tuple[List[str], List[str]]:
    """`data` is the lesson's JSON, `masked` its Markdown body (code as placeholders)."""
    problems: List[str] = []
    warnings: List[str] = []
    if not isinstance(data, dict):
        return [f"{where}: must be a JSON object"], warnings
    if "content" in data:
        problems.append(f"{where}: has a 'content' key - the body belongs in {body_where}, not here")
    if data.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"{where}: schema_version must be {SCHEMA_VERSION}")
    if data.get("lesson_id") != lesson.lesson_id:
        problems.append(f"{where}: lesson_id {data.get('lesson_id')!r} does not match {lesson.lesson_id}")

    payload = source_payload(lesson, questions)
    if data.get("source_hash") != source_hash(payload):
        warnings.append(f"{where}: made from an older English text (source_hash differs) - re-check it")

    hidden = R.invisible_characters(json.dumps(data, ensure_ascii=False))
    if hidden:
        problems.append(f"{where}: {len(hidden)} invisible character(s), e.g. {hidden[0]}")

    if not _text(data.get("title")):
        problems.append(f"{where}: title is empty")
    elif not _ARABIC_LETTER.search(data["title"]):
        warnings.append(f"{where}: title has no Arabic letters")

    if not masked:
        problems.append(f"{body_where}: the body is empty")
    else:
        english_blocks = R.protect_code(lesson.content or "")[1]
        broken = R.placeholder_problems(masked, english_blocks)
        problems += [f"{body_where}: {p}" for p in broken]
        if not broken:
            restored = R.restore_code(masked, english_blocks)
            report = R.review(lesson.content or "", restored)
            problems += [f"{body_where}: {p}" for p in report.problems]
            warnings += [f"{body_where}: {w}" for w in report.warnings]
            # A marker is a line of prose, not code, so the placeholders do not protect it: a
            # translation that drops or renames one would silently lose a figure or an exercise.
            wanted, got = markers(lesson.content or ""), markers(restored)
            if got != wanted:
                problems.append(f"{body_where}: markers {got} do not match the English {wanted}")

    exercises = data.get("exercises") or []
    by_id = {e.exercise_id: e for e in lesson.exercises}
    seen = set()
    for entry in exercises if isinstance(exercises, list) else []:
        ident = entry.get("id") if isinstance(entry, dict) else None
        if ident not in by_id:
            problems.append(f"{where}: exercise {ident!r} is not one of {sorted(by_id)}")
        elif ident in seen:
            problems.append(f"{where}: exercise {ident} appears twice")
        elif not _text(entry.get("title")) or not _text(entry.get("description")):
            problems.append(f"{where}: exercise {ident} needs a title and a description")
        elif R.left_in_english(entry["title"]) or R.left_in_english(entry["description"]):
            problems.append(f"{where}: exercise {ident} was left in English")
        seen.add(ident)
    if not isinstance(exercises, list):
        problems.append(f"{where}: exercises must be a list")
    elif set(by_id) - seen:
        warnings.append(f"{where}: no Arabic yet for exercise(s) {sorted(set(by_id) - seen)}")

    entries = data.get("questions") or []
    if not isinstance(entries, list):
        problems.append(f"{where}: questions must be a list")
    elif entries and len(entries) != len(questions):
        # The Nth Arabic question is the twin of the Nth English one, so a different count means
        # some twin is attached to the wrong question - and a learner is graded on position.
        problems.append(f"{where}: {len(entries)} questions against {len(questions)} in the English")
    elif not entries and questions:
        warnings.append(f"{where}: no Arabic yet for its {len(questions)} questions")
    else:
        for index, (english, entry) in enumerate(zip(questions, entries), start=1):
            label = f"{where} question {index}"
            if not isinstance(entry, dict) or not _text(entry.get("question")):
                problems.append(f"{label}: needs a question")
                continue
            if english.is_open:
                if entry.get("options") not in (None, []):
                    problems.append(f"{label}: the English is open-ended, so it has no options")
            else:
                options = entry.get("options")
                if not isinstance(options, list) or len(options) != len(english.options or []):
                    problems.append(
                        f"{label}: {len(options) if isinstance(options, list) else 0} options against "
                        f"{len(english.options or [])} in the English"
                    )
                elif not all(_text(o) for o in options):
                    problems.append(f"{label}: an option is empty")
                elif len({_text(o) for o in options}) < len({_text(o) for o in english.options or []}):
                    problems.append(f"{label}: two different options became the same text")
            if english.explanation and not _text(entry.get("explanation")):
                problems.append(f"{label}: the English has an explanation; the Arabic has none")
            spoken = [entry.get("question"), entry.get("explanation"), *(entry.get("options") or [])]
            if any(isinstance(t, str) and R.left_in_english(t) for t in spoken):
                problems.append(f"{label}: some of it was left in English")
    return problems, warnings


def _apply_lesson(lesson: LessonSpec, questions: List[QuestionSpec], data: Dict[str, Any], masked: str) -> None:
    blocks = R.protect_code(lesson.content or "")[1]
    lesson.title_ar = _text(data["title"])
    lesson.content_ar = R.restore_code(masked, blocks)
    by_id = {e.exercise_id: e for e in lesson.exercises}
    for entry in data.get("exercises") or []:
        exercise = by_id[entry["id"]]
        exercise.title_ar, exercise.description_ar = _text(entry["title"]), _text(entry["description"])
    for question, entry in zip(questions, data.get("questions") or []):
        question.ar = {
            "question": _text(entry["question"]),
            **({} if question.is_open else {"options": [_text(o) for o in entry["options"]]}),
            "explanation": _text(entry.get("explanation")),
        }


# ─── The course ─────────────────────────────────────────────────────────────

def _read(path: Path) -> Tuple[Optional[Any], Optional[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, ValueError) as exc:
        return None, f"{path.name}: cannot be read as JSON ({exc})"


def read_body(path: Path) -> Tuple[Optional[str], Optional[str]]:
    """A lesson body. Tolerates a BOM and Windows line endings (git on Windows may rewrite them),
    and returns it stripped, so the same text is stored wherever the file was last saved."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return None, f"{AR_DIR}/{path.name}: cannot be read as UTF-8 text ({exc})"
    return text.replace("\r\n", "\n").replace("\r", "\n").strip(), None


def _apply_course(course: CourseSpec, data: Any, where: str) -> None:
    if not isinstance(data, dict):
        course.arabic_problems.append(f"{where}: must be a JSON object")
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        course.arabic_problems.append(f"{where}: schema_version must be {SCHEMA_VERSION}")
    if data.get("course_id") not in (None, course.course_id):
        course.arabic_problems.append(f"{where}: course_id {data.get('course_id')!r} is not {course.course_id}")
    if _text(data.get("title")):
        course.title_ar = _text(data["title"])
    if _text(data.get("description")):
        course.description_ar = _text(data["description"])
    modules = data.get("modules") or {}
    known = {m.module_id: m for m in course.modules}
    for module_id, entry in (modules.items() if isinstance(modules, dict) else []):
        module = known.get(module_id)
        if module is None:
            course.arabic_problems.append(f"{where}: module {module_id!r} is not one of {sorted(known)}")
        elif not isinstance(entry, dict) or not _text(entry.get("title")):
            course.arabic_problems.append(f"{where}: module {module_id} needs a title")
        else:
            module.title_ar = _text(entry["title"])
            module.description_ar = _text(entry.get("description")) or None
            if module.description and not module.description_ar:
                course.arabic_warnings.append(f"{where}: module {module_id} has no Arabic description yet")


def attach_arabic(course: CourseSpec, *roots: Path) -> None:
    """Read `<root>/ar/` for the first root that has one and put its Arabic on `course`.
    Absent folder = no Arabic yet = nothing happens."""
    folder = next((r / AR_DIR for r in roots if (r / AR_DIR).is_dir()), None)
    if folder is None:
        return
    lessons = {lesson.lesson_id: lesson for lesson in course.lessons}
    questions = questions_by_lesson(course)

    course_file = folder / COURSE_FILE
    if course_file.is_file():
        data, error = _read(course_file)
        if error:
            course.arabic_problems.append(error)
        else:
            _apply_course(course, data, f"{AR_DIR}/{COURSE_FILE}")

    # A lesson is its `.json` and its `.md` together; either one alone is a fault.
    stems = sorted({p.stem for p in folder.iterdir() if p.suffix in (".json", ".md") and p.name != COURSE_FILE})
    for stem in stems:
        where, body_where = f"{AR_DIR}/{stem}.json", f"{AR_DIR}/{stem}.md"
        lesson = lessons.get(stem)
        if lesson is None:
            course.arabic_problems.append(f"{AR_DIR}/{stem}: no lesson {stem!r} in {course.course_id}")
            continue
        if not (folder / f"{stem}.json").is_file():
            course.arabic_problems.append(f"{body_where}: has no {where} beside it (title, exercises and quiz live there)")
            continue
        if not (folder / f"{stem}.md").is_file():
            course.arabic_problems.append(f"{where}: has no {body_where} beside it (the lesson body lives there)")
            continue
        data, error = _read(folder / f"{stem}.json")
        masked, body_error = read_body(folder / f"{stem}.md")
        for message in (error and f"{AR_DIR}/{error}", body_error):
            if message:
                course.arabic_problems.append(message)
        if error or body_error:
            continue
        found, notes = _check_lesson(lesson, questions.get(lesson.lesson_id, []), data, masked, where, body_where)
        course.arabic_problems += found
        course.arabic_warnings += notes
        if not found:
            _apply_lesson(lesson, questions.get(lesson.lesson_id, []), data, masked)
