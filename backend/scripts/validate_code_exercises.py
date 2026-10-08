"""Validate deterministic exercise content, including official solutions."""
import argparse
import asyncio
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.code_execution import IsolatedPythonRunner
from app.services.code_grading import PythonGrader, SQLGrader, TextGrader
from app.services.code_grading.authoring import count_python_blanks
from app.services.curriculum.loaders import load_all_courses
from app.services.curriculum.validate import code_exercise_problems


async def validate_solutions(courses) -> list[str]:
    graders = {
        "python": PythonGrader(IsolatedPythonRunner()),
        "sql": SQLGrader(),
        "bash": TextGrader(),
        "dockerfile": TextGrader(),
        "hcl": TextGrader(),
        "ini": TextGrader(),
        "sparql": TextGrader(),
        "yaml": TextGrader(),
    }
    problems: list[str] = []
    for course in courses:
        for lesson in course.lessons:
            for exercise in lesson.exercises:
                if exercise.exercise_type != "code" or not exercise.tests or not exercise.solution_code:
                    continue
                grader = graders.get(exercise.language or "")
                if grader is None:
                    problems.append(
                        f"{course.course_id} {exercise.exercise_id}: no grader for "
                        f"language {exercise.language!r}"
                    )
                    continue
                result = await grader.grade(
                    exercise.solution_code, exercise.tests,
                    pre_exercise_code=exercise.pre_exercise_code or "",
                )
                if not result.passed:
                    problems.append(
                        f"{course.course_id} {exercise.exercise_id}: official solution failed "
                        f"({result.status}, test={result.failed_test_id})"
                    )
                starter_result = await grader.grade(
                    exercise.starter_code, exercise.tests,
                    pre_exercise_code=exercise.pre_exercise_code or "",
                )
                if starter_result.passed:
                    problems.append(
                        f"{course.course_id} {exercise.exercise_id}: untouched starter "
                        "incorrectly receives full marks"
                    )
    return problems


async def validate_seed_definitions() -> tuple[int, list[str]]:
    """Validate deterministic definitions in legacy standalone tool seeds."""
    grader = PythonGrader(IsolatedPythonRunner())
    problems: list[str] = []
    count = 0
    seen: set[str] = set()
    modules = (
        "seed_tool_fastapi", "seed_tool_langchain", "seed_tool_langgraph",
        "seed_tool_llamaindex", "seed_tool_qdrant",
    )
    for module_name in modules:
        topics = importlib.import_module(f"seeds.{module_name}").TOPICS
        tool = module_name.removeprefix("seed_tool_")
        for topic in topics:
            for exercise in topic.get("exercises", []):
                is_code = exercise.get("exercise_type") == "code" or bool(exercise.get("starter_code"))
                if not is_code:
                    continue
                count += 1
                where = f"{tool}/{topic.get('slug')}/{exercise.get('title')}"
                identity = where.lower()
                if identity in seen:
                    problems.append(f"{where}: duplicate exercise identity")
                seen.add(identity)
                for field in ("starter_code", "solution_code", "language", "grading_tests"):
                    if not exercise.get(field):
                        problems.append(f"{where}: missing {field}")
                if exercise.get("language") == "python" and exercise.get("starter_code"):
                    blank_count = count_python_blanks(str(exercise["starter_code"]))
                    if not 1 <= blank_count <= 5:
                        problems.append(f"{where}: starter must contain 1-5 ___ blanks (found {blank_count})")
                tests = exercise.get("grading_tests") or []
                ids = [str(test.get("id") or "") for test in tests]
                if len(ids) != len(set(ids)):
                    problems.append(f"{where}: duplicate test ids")
                if any(not test_id for test_id in ids):
                    problems.append(f"{where}: every test needs an id")
                if not all(test.get("feedback") for test in tests):
                    problems.append(f"{where}: every test needs feedback")
                if all(exercise.get(field) for field in ("solution_code", "grading_tests")):
                    result = await grader.grade(exercise["solution_code"], tests)
                    if not result.passed:
                        problems.append(f"{where}: official solution failed ({result.status}, test={result.failed_test_id})")
                if all(exercise.get(field) for field in ("starter_code", "grading_tests")):
                    result = await grader.grade(exercise["starter_code"], tests)
                    if result.passed:
                        problems.append(f"{where}: untouched starter incorrectly receives full marks")
    return count, problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", action="append")
    args = parser.parse_args()
    courses = load_all_courses(only=args.course)
    seed_count, seed_problems = asyncio.run(validate_seed_definitions())
    problems = code_exercise_problems(courses) + asyncio.run(validate_solutions(courses)) + seed_problems
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    count = sum(
        exercise.exercise_type == "code"
        for course in courses for lesson in course.lessons for exercise in lesson.exercises
    )
    print(f"OK: {count + seed_count} deterministic code exercises; every official solution passes")


if __name__ == "__main__":
    main()
