"""Reviewed classification of canonical implementation exercises.

These prompts genuinely ask the learner to write or modify executable code,
but do not yet have an authored reference solution and deterministic tests.
They are deliberately distinct from fully migrated ``code`` exercises:

* ``code``         — Run and Submit are available; every solution is validated.
* ``code_pending`` — Run is available; Submit is unavailable until tests exist.
* ``legacy``       — a written/design answer, kept on the conversational path.

This prevents the two unsafe shortcuts: sending code to the AI evaluator or
inventing weak tests that award full marks for an incomplete answer.
"""
from __future__ import annotations

from collections import Counter

from .spec import CourseSpec


def _course(course: str, local_ids: str) -> set[str]:
    return {f"{course}.{local_id}" for local_id in local_ids.split()}


PYTHON_PENDING = frozenset(
    _course("COURSE-001", """
        M03.L01.EX01 M04.L01.EX02 M05.L01.EX01 M06.L01.EX01 M06.L01.EX02 M07.L01.EX01
    """)
    | _course("COURSE-003", """
        M04.L01.EX02 M06.L01.EX02
        M03.L01.EX01 M03.L01.EX02 M03.L01.EX03
        M04.L01.EX01 M04.L01.EX03
        M05.L01.EX01 M05.L01.EX02 M05.L01.EX04
        M06.L01.EX01 M06.L01.EX03 M06.L01.EX04
        M07.L01.EX01 M07.L01.EX02 M07.L01.EX03 M07.L01.EX04
        M08.L01.EX01 M08.L01.EX02 M08.L01.EX03 M08.L01.EX04 M08.L01.EX05
        M09.L01.EX01 M09.L01.EX02 M09.L01.EX03 M09.L01.EX04
        M10.L01.EX01 M10.L01.EX02 M10.L01.EX03
        M11.L01.EX01 M11.L01.EX02 M11.L01.EX03
        M12.L01.EX01 M12.L01.EX02 M12.L01.EX03 M12.L01.EX04
        M13.L01.EX01 M13.L01.EX02 M13.L01.EX03 M13.L01.EX04
        M14.L01.EX03 M14.L01.EX04
    """)
    | _course("COURSE-004", """
        M01.L05.EX01 M01.L07.EX01 M02.L01.EX01 M02.L01.EX02
    """)
    | _course("COURSE-005", """
        M01.L01.EX02 M02.L01.EX01 M03.L01.EX01 M04.L01.EX01
        M05.L01.EX01 M05.L01.EX02 M06.L01.EX01 M06.L01.EX02
        M07.L01.EX01 M08.L01.EX01 M09.L01.EX01 M10.L01.EX01
        M11.L01.EX01 M12.L01.EX01
    """)
    | _course("COURSE-006", """
        M02.L01.EX02 M08.L01.EX02 M08.L01.EX03
    """)
    | _course("COURSE-007", """
        M03.L02.EX01 M03.L02.EX02 M03.L02.EX03 M03.L02.EX04 M04.L01.EX03
    """)
    | _course("COURSE-008", """
        M01.L01.EX04 M01.L03.EX02 M01.L05.EX01 M01.L09.EX04
    """)
    | _course("COURSE-009", """
        M01.L02.EX09
    """)
    | _course("COURSE-010", """
        M01.L02.EX01 M01.L02.EX03
        M01.L04.EX01 M01.L04.EX02 M01.L04.EX03 M01.L04.EX04 M01.L04.EX05 M01.L04.EX06
        M01.L05.EX02 M01.L05.EX03 M01.L05.EX04 M01.L05.EX06
        M01.L06.EX02 M01.L06.EX03 M01.L06.EX05 M01.L06.EX06
        M01.L07.EX03 M01.L07.EX04 M01.L07.EX05 M01.L07.EX06 M01.L07.EX08
        M01.L08.EX06 M01.L09.EX02 M01.L09.EX03 M01.L09.EX07
        M01.L10.EX02 M01.L10.EX03 M01.L10.EX04 M01.L10.EX06
        M01.L11.EX03 M01.L11.EX04 M01.L11.EX05 M01.L11.EX07 M01.L11.EX08 M01.L11.EX09
    """)
    | _course("COURSE-012", """
        M01.L02.EX02 M01.L03.EX01 M01.L03.EX02
        M01.L04.EX01 M01.L04.EX02 M01.L05.EX01 M01.L05.EX02 M01.L06.EX01
        M01.L07.EX01 M01.L07.EX02 M01.L08.EX01 M01.L08.EX02
        M01.L09.EX01 M01.L09.EX02 M01.L10.EX01 M01.L10.EX02
    """)
    | _course("COURSE-013", """
        M03.L01.EX01
        M04.L01.EX01 M04.L01.EX02 M04.L01.EX04
        M05.L01.EX01 M05.L01.EX02 M05.L01.EX03 M05.L01.EX04
        M06.L01.EX01 M06.L01.EX02 M06.L01.EX04 M06.L01.EX05
        M07.L01.EX01 M07.L01.EX02 M07.L01.EX03
        M08.L01.EX01 M08.L01.EX02 M08.L01.EX04
        M09.L01.EX01 M09.L01.EX02 M09.L01.EX03
        M10.L01.EX01 M10.L01.EX02 M10.L01.EX03
        M11.L01.EX01 M11.L01.EX02 M11.L01.EX03 M11.L01.EX04
        M12.L01.EX02 M12.L01.EX03 M12.L01.EX04
        M13.L01.EX01 M13.L01.EX02 M13.L01.EX03 M13.L01.EX04
        M14.L01.EX01 M14.L01.EX02
        M15.L01.EX01 M15.L01.EX02
    """)
    | _course("COURSE-014", """
        M01.L01.EX01 M01.L01.EX02 M02.L01.EX01 M02.L01.EX02
        M03.L01.EX01 M03.L01.EX02 M04.L01.EX01 M04.L01.EX02
        M05.L01.EX01 M05.L01.EX02 M06.L01.EX01 M06.L01.EX02
        M07.L01.EX01 M07.L01.EX02 M08.L01.EX01 M08.L01.EX02
        M09.L01.EX01 M09.L01.EX02 M10.L01.EX01 M10.L01.EX02
        M11.L01.EX01 M11.L01.EX02 M12.L01.EX01 M12.L01.EX02 M13.L01.EX01
    """)
    | _course("COURSE-015", """
        M01.L01.EX01 M01.L03.EX03 M01.L04.EX03 M01.L05.EX03
        M01.L06.EX08 M01.L07.EX04 M01.L07.EX06
    """)
    | _course("COURSE-016", """
        M11.L01.EX01 M14.L01.EX03 M14.L01.EX04 M15.L01.EX04 M16.L01.EX04 M16.L01.EX06
    """)
    | _course("COURSE-002", "M03.L01.EX02")
)

DOCKERFILE_PENDING = frozenset(
    _course("COURSE-010", "M01.L12.EX02 M01.L12.EX06 M01.L12.EX07")
    | _course("COURSE-011", "M03.L01.EX02")
)

YAML_PENDING = frozenset(
    _course("COURSE-010", "M01.L12.EX03 M01.L12.EX05")
    | _course("COURSE-011", "M03.L01.EX03 M05.L01.EX02 M06.L01.EX02 M06.L01.EX04")
    | _course("COURSE-016", "M15.L01.EX03")
)

BASH_PENDING = frozenset(
    _course("COURSE-011", """
        M01.L01.EX03 M01.L01.EX04 M02.L01.EX01 M02.L01.EX03 M02.L01.EX04
        M03.L01.EX04 M04.L01.EX03 M06.L01.EX03
    """)
)

HCL_PENDING = frozenset(
    _course("COURSE-011", "M04.L01.EX02 M04.L01.EX04")
)

INI_PENDING = frozenset(
    _course("COURSE-011", "M08.L06.EX02")
)

SQL_PENDING = frozenset(
    _course("COURSE-009", "M01.L02.EX14")
)

SPARQL_PENDING = frozenset(
    _course("COURSE-009", "M01.L09.EX04")
)

PENDING_BY_LANGUAGE = {
    **{exercise_id: "python" for exercise_id in PYTHON_PENDING},
    **{exercise_id: "dockerfile" for exercise_id in DOCKERFILE_PENDING},
    **{exercise_id: "yaml" for exercise_id in YAML_PENDING},
    **{exercise_id: "bash" for exercise_id in BASH_PENDING},
    **{exercise_id: "hcl" for exercise_id in HCL_PENDING},
    **{exercise_id: "ini" for exercise_id in INI_PENDING},
    **{exercise_id: "sql" for exercise_id in SQL_PENDING},
    **{exercise_id: "sparql" for exercise_id in SPARQL_PENDING},
}


def _comment_prefix(language: str) -> str:
    if language in {"sql", "sparql"}:
        return "--"
    if language == "ini":
        return ";"
    return "#"


def apply_pending_code_classification(course: CourseSpec) -> None:
    """Apply reviewed classifications and report stale registry entries."""
    expected = {
        exercise_id: language
        for exercise_id, language in PENDING_BY_LANGUAGE.items()
        if exercise_id.startswith(f"{course.course_id}.")
    }
    found: set[str] = set()
    for lesson in course.lessons:
        for exercise in lesson.exercises:
            language = expected.get(exercise.exercise_id)
            if language is None:
                continue
            found.add(exercise.exercise_id)
            # An authored deterministic definition always wins over backlog
            # metadata when an exercise is migrated later.
            if exercise.exercise_type == "code" and exercise.tests:
                continue
            exercise.exercise_type = "code_pending"
            exercise.language = language
            if not exercise.starter_code:
                comment = _comment_prefix(language)
                exercise.starter_code = (
                    f"{comment} TODO: Complete {exercise.title!r} using the instructions above.\n"
                )
            if not exercise.hint:
                exercise.hint = (
                    "You can run this exercise now. Deterministic submission tests are still being authored."
                )
    missing = sorted(set(expected) - found)
    if missing:
        course.structure_problems.append(
            f"pending code classification references missing exercises: {', '.join(missing)}"
        )


def pending_counts() -> dict[str, int]:
    return dict(sorted(Counter(exercise_id.split(".", 1)[0] for exercise_id in PENDING_BY_LANGUAGE).items()))
