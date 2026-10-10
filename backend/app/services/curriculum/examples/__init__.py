"""Example answers for written exercises, in English and Arabic.

A written exercise is graded by the AI evaluator. Its example answer is one
good answer, not the only one: the learner sees it after their first
evaluated answer (to compare and improve), and the evaluator receives it as
its reference - which its prompt already treats as one acceptable answer,
never a template to match.

Definitions live in one module per course (``c001.py`` ...), keyed by the
canonical exercise id, and are applied by the loader after the guided code
exercises, so the Arabic source hash of the lesson is unaffected.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple

from ..spec import CourseSpec

# (English, Arabic)
Example = Tuple[str, str]

MIN_CHARACTERS = 40
MAX_CHARACTERS = 4000

# Courses whose every written exercise has an example answer. The test suite
# enforces full coverage for these; add a course here once its file is done
# (see docs/written-example-answers-guide.md).
COMPLETE_COURSES = frozenset({
    "COURSE-001", "COURSE-002", "COURSE-003", "COURSE-004", "COURSE-005", "COURSE-006", "COURSE-007",
})
_ARABIC = re.compile(r"[؀-ۿ]")


def registry() -> Dict[str, Example]:
    """Every example answer, keyed by canonical exercise id."""
    from . import catalog
    return catalog.ALL


def example_problems(exercise_id: str, example: Example) -> List[str]:
    problems: List[str] = []
    if not isinstance(example, tuple) or len(example) != 2:
        return [f"{exercise_id}: an example answer is an (English, Arabic) pair"]
    english, arabic = example
    for language, text in (("English", english), ("Arabic", arabic)):
        if not isinstance(text, str) or not MIN_CHARACTERS <= len(text.strip()) <= MAX_CHARACTERS:
            problems.append(f"{exercise_id}: the {language} example answer must be "
                            f"{MIN_CHARACTERS}-{MAX_CHARACTERS} characters")
    if isinstance(arabic, str) and not _ARABIC.search(arabic):
        problems.append(f"{exercise_id}: the Arabic example answer has no Arabic text")
    return problems


def apply_example_answers(course: CourseSpec) -> None:
    examples = registry()
    for lesson in course.lessons:
        for exercise in lesson.exercises:
            example = examples.get(exercise.exercise_id)
            if example is None:
                continue
            if exercise.exercise_type == "code":
                course.structure_problems.append(
                    f"{exercise.exercise_id}: example answers are for written exercises; "
                    "a code exercise has its worked solution"
                )
                continue
            problems = example_problems(exercise.exercise_id, example)
            if problems:
                course.structure_problems.extend(problems)
                continue
            exercise.example_answer, exercise.example_answer_ar = (text.strip() for text in example)
