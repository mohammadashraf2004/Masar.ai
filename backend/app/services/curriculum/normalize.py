"""
app/services/curriculum/normalize.py

Pure conversions from the shapes the course folders use to the shapes the
catalogue stores. No I/O, no database.

Nothing is invented here. Where a source field has no home in the catalogue it is
folded into the nearest text field (an exercise's acceptance criteria become
part of its description) rather than dropped, and where a value is missing the
caller's stated default is used.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

from app.services.curriculum.spec import (
    DIFFICULTIES, CurriculumError, ExerciseSpec, ProjectSpec, QuestionSpec,
)

_ARABIC = re.compile(r"[؀-ۿ]")
_LETTER = re.compile(r"[^\W\d_]", re.UNICODE)


def arabic_ratio(text: str) -> float:
    """Share of the letters in `text` that are Arabic."""
    letters = _LETTER.findall(text or "")
    if not letters:
        return 0.0
    return sum(1 for c in letters if _ARABIC.match(c)) / len(letters)


def is_arabic(text: Optional[str]) -> bool:
    """A body is Arabic-first when most of its letters are Arabic. Mixed
    Arabic prose with English terms and code (COURSE-002/003) is Arabic; an
    English lesson with one Arabic word is not."""
    return arabic_ratio(text or "") >= 0.3


def norm_difficulty(value: Any, default: str = "intermediate") -> str:
    """'Intermediate → Advanced', 'intermediate-to-advanced', 'Intermediate / Advanced'
    all name a range; the lesson starts at its first level."""
    text = str(value or "").strip().lower()
    for level in DIFFICULTIES:
        if text.startswith(level):
            return level
    for level in DIFFICULTIES:
        if level in text:
            return level
    return default


def as_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def bullets(items: Iterable[Any]) -> str:
    return "\n".join(f"- {as_text(i) or i}" for i in items if i)


def _section(heading: str, body: str) -> str:
    return f"**{heading}**\n\n{body}" if body else ""


def _join(parts: Iterable[str]) -> str:
    return "\n\n".join(p for p in parts if p)


def slugify_skill(tag: str) -> str:
    """Case, underscore and hyphen variants of one tag are one tag.
    `Machine_Learning`, `machine learning` and `machine-learning` collapse."""
    return re.sub(r"[^a-z0-9]+", "-", str(tag).lower()).strip("-")


def norm_tags(tags: Iterable[Any]) -> List[str]:
    seen: List[str] = []
    for tag in tags or []:
        slug = slugify_skill(tag)
        if slug and slug not in seen:
            seen.append(slug)
    return seen


# ─── Quizzes ────────────────────────────────────────────────────────────────

def norm_question(raw: Dict[str, Any], where: str) -> QuestionSpec:
    """One quiz question from any of the shapes in the course folders.

    Answers appear as an index (`correct`, `answer_index`), as the text of the
    right option (`answer`), or as a bool for true/false. A question with no
    options is open-ended: its reference answer travels in `explanation`, which
    is where the AI answer evaluator reads it (`answer_evaluation_controller`).
    """
    if not isinstance(raw, dict):
        raise CurriculumError([f"{where}: a quiz question must be an object"])
    question = as_text(raw.get("question"))
    if not question:
        raise CurriculumError([f"{where}: quiz question has no text"])
    explanation = as_text(raw.get("explanation"))
    question_id = as_text(raw.get("id") or raw.get("question_id"))
    lesson_id = as_text(raw.get("lesson_id"))
    raw_lesson_ids = raw.get("lesson_ids")
    lesson_ids = ([as_text(value) for value in raw_lesson_ids if as_text(value)]
                  if isinstance(raw_lesson_ids, list) else [])
    metadata = {
        str(key): value for key, value in raw.items()
        if key not in {
            "id", "question_id", "lesson_id", "lesson_ids", "question", "options", "choices",
            "correct", "answer_index", "answer", "explanation",
        }
    }
    kind = str(raw.get("type") or "").lower()
    options = raw.get("options") if raw.get("options") is not None else raw.get("choices")

    if options is None and kind in ("true_false", "true-false", "boolean") and isinstance(raw.get("answer"), bool):
        options = ["True", "False"]
        correct = 0 if raw["answer"] else 1
        return QuestionSpec(question, options, correct, explanation, question_id, lesson_id, lesson_ids, metadata)

    if not options:
        answer = raw.get("answer")
        reference = _join([as_text(answer) if isinstance(answer, str) else "", explanation])
        return QuestionSpec(question, None, None, reference, question_id, lesson_id, lesson_ids, metadata)

    if not isinstance(options, list) or not all(isinstance(o, str) and o.strip() for o in options):
        raise CurriculumError([f"{where}: quiz options must be a list of non-empty strings"])
    if len(set(options)) != len(options):
        raise CurriculumError([f"{where}: quiz has duplicate options"])

    if isinstance(raw.get("correct"), int) and not isinstance(raw.get("correct"), bool):
        correct = raw["correct"]
    elif isinstance(raw.get("answer_index"), int) and not isinstance(raw.get("answer_index"), bool):
        correct = raw["answer_index"]
    elif isinstance(raw.get("answer"), str) and raw["answer"] in options:
        correct = options.index(raw["answer"])
    else:
        raise CurriculumError([f"{where}: quiz question '{question[:50]}' has no resolvable correct answer"])
    if not 0 <= correct < len(options):
        raise CurriculumError([f"{where}: correct answer index {correct} is outside the {len(options)} options"])
    return QuestionSpec(question, list(options), correct, explanation, question_id, lesson_id, lesson_ids, metadata)


def norm_questions(raw: Any, where: str) -> List[QuestionSpec]:
    if isinstance(raw, dict):
        raw = raw.get("questions")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise CurriculumError([f"{where}: quiz must be a list of questions"])
    return [norm_question(q, f"{where} question {i + 1}") for i, q in enumerate(raw)]


# ─── Exercises ──────────────────────────────────────────────────────────────

def norm_exercise(raw: Dict[str, Any], where: str, default_difficulty: str) -> ExerciseSpec:
    """`description` / `instructions` / `prompt` all hold the task text. The
    extra fields some courses add (acceptance criteria, hints, expected output,
    a validation snippet) have no column of their own, so they follow the task
    in the description instead of being lost."""
    if not isinstance(raw, dict):
        raise CurriculumError([f"{where}: an exercise must be an object"])
    title = as_text(raw.get("title"))
    summary = as_text(raw.get("description"))
    instructions = as_text(raw.get("instructions"))
    prompt = as_text(raw.get("prompt"))
    task = summary or instructions or prompt
    if not title or not task:
        raise CurriculumError([f"{where}: exercise needs a title and a task description"])
    validation = as_text(raw.get("validation_code"))
    description = _join([
        task,
        _section("Instructions", instructions if instructions and instructions != task else ""),
        _section(
            "Prompt",
            prompt if prompt and prompt != task and prompt != instructions else "",
        ),
        _section("Acceptance criteria", bullets(raw.get("acceptance_criteria") or [])),
        _section("Expected output", as_text(raw.get("expected_output"))),
        _section("Hints", bullets(raw.get("hints") or [])),
        _section("Self-check", f"```python\n{validation}\n```" if validation else ""),
    ])
    return ExerciseSpec(
        title=title, description=description,
        difficulty=norm_difficulty(raw.get("difficulty"), default_difficulty),
        skill_tested=norm_tags(raw.get("skill_tested") or []),
        starter_code=as_text(raw.get("starter_code")) or None,
        solution_code=as_text(raw.get("solution_code")) or None,
        exercise_id=as_text(raw.get("id") or raw.get("exercise_id")),
        course_id=as_text(raw.get("course_id")),
        module_id=as_text(raw.get("module_id")),
        lesson_id=as_text(raw.get("lesson_id")),
    )


def norm_exercises(raw: Any, where: str, default_difficulty: str) -> List[ExerciseSpec]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise CurriculumError([f"{where}: exercises must be a list"])
    return [norm_exercise(e, f"{where} exercise {i + 1}", default_difficulty) for i, e in enumerate(raw)]


# ─── Projects ───────────────────────────────────────────────────────────────

def norm_project(raw: Any, where: str, default_difficulty: str) -> Optional[ProjectSpec]:
    """A project, or None when the source has an empty placeholder (COURSE-009
    puts `{"title": None, ...}` on every lesson that has no project)."""
    if not isinstance(raw, dict) or not as_text(raw.get("title")):
        return None
    summary = (
        as_text(raw.get("description")) or as_text(raw.get("summary")) or as_text(raw.get("brief"))
        or as_text(raw.get("purpose")) or as_text(raw.get("objective")) or as_text(raw.get("goal"))
    )
    stages = raw.get("required_stages") or raw.get("stages") or []
    choose = raw.get("choose_one") or []
    deliverables = raw.get("deliverables") or []
    criteria = raw.get("acceptance_criteria") or []
    requirements = raw.get("requirements") or []
    if not summary and not (deliverables or stages or requirements):
        return None
    description = _join([
        summary,
        _section("Choose one", bullets(choose)),
        _section("Stages", bullets(stages)),
        _section("Requirements", bullets(requirements)),
        _section("Deliverables", bullets(deliverables)),
        _section("Acceptance criteria", bullets(criteria)),
    ])
    objectives = list(raw.get("objectives") or []) or [as_text(d) for d in deliverables if as_text(d)]
    rubric = raw.get("rubric") if isinstance(raw.get("rubric"), dict) else {}
    hours = raw.get("estimated_hours")
    if hours is None and isinstance(raw.get("estimated_minutes"), (int, float)):
        hours = round(raw["estimated_minutes"] / 60, 2)
    return ProjectSpec(
        title=as_text(raw["title"]), description=description,
        difficulty=norm_difficulty(raw.get("difficulty"), default_difficulty),
        tech_stack=[as_text(t) for t in raw.get("tech_stack") or [] if as_text(t)],
        objectives=[as_text(o) for o in objectives if as_text(o)],
        rubric={str(k): v for k, v in rubric.items() if isinstance(v, (int, float))},
        starter_repo_url=as_text(raw.get("starter_repo_url")) or None,
        estimated_hours=float(hours) if isinstance(hours, (int, float)) else None,
    )


# ─── Identifiers ────────────────────────────────────────────────────────────

_MODULE_ID = re.compile(r"^M(\d{3})?[-_.]?(\d{2})$", re.IGNORECASE)


def module_id_for(course_id: str, raw: Any) -> str:
    """'M004_01' / 'm004-01' / 'M01' -> 'M004-01'. The course number is taken
    from the course id, so every course uses one spelling."""
    text = str(raw).strip()
    match = _MODULE_ID.match(text)
    if not match:
        raise CurriculumError([f"{course_id}: unrecognised module id '{raw}'"])
    return f"M{course_id.split('-')[1]}-{match.group(2)}"


_LESSON_ID = re.compile(r"^L(\d{3})[-_](\d{3})$", re.IGNORECASE)


def lesson_id_for(course_id: str, raw: Any) -> str:
    """'L004_001' / 'l004-001' -> 'L004-001'. Course-native ids that are not of
    this form (COURSE-001's 'M01.L01', COURSE-002's 'T001') are kept as written."""
    text = str(raw).strip()
    match = _LESSON_ID.match(text)
    return f"L{match.group(1)}-{match.group(2)}" if match else text
