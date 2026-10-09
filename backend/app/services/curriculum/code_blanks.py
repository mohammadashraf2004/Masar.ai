"""Present authored deterministic Python exercises as focused fill-in tasks."""
from __future__ import annotations

from app.services.code_grading.authoring import build_fill_in_blank_exercise, count_python_blanks

from .spec import CourseSpec


def apply_fill_in_blank_format(course: CourseSpec) -> None:
    """Replace broad TODO scaffolds with 1–5 solution-derived expression blanks.

    Pending exercises have no trusted solution yet and are intentionally left
    alone. They cannot be submitted, so this transformation only touches fully
    authored deterministic Python exercises. A starter that already has its
    own ``___`` blanks is a hand-authored guided scaffold (step comments,
    behavioural tests, progressive hints) and is kept exactly as written.
    """
    for lesson in course.lessons:
        for exercise in lesson.exercises:
            if (
                exercise.exercise_type != "code"
                or exercise.language != "python"
                or not exercise.starter_code
                or not exercise.solution_code
                or not exercise.tests
                or count_python_blanks(exercise.starter_code)
            ):
                continue
            try:
                starter, tests, labels = build_fill_in_blank_exercise(
                    exercise.starter_code,
                    exercise.solution_code,
                    list(exercise.tests),
                )
            except (SyntaxError, ValueError) as exc:
                course.structure_problems.append(
                    f"{exercise.exercise_id}: cannot create fill-in starter ({exc})"
                )
                continue
            exercise.starter_code = starter
            exercise.tests = tests
            exercise.hint = (
                "Fill the `___` expressions using the lesson concepts, then submit your completed program."
            )
            if not exercise.success_message:
                concepts = ", ".join(label.replace("the ", "", 1) for label in labels[:3])
                exercise.success_message = (
                    f"Correct! The missing expressions complete {concepts} in the full program."
                )
