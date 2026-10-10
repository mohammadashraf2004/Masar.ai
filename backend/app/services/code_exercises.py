"""Application service connecting execution, grading, attempts, and progress."""
from __future__ import annotations

import ast
import re
from typing import Any

from sqlalchemy.orm import Session

from app.models.code_exercise import CodeExerciseAttempt
from app.models.learning import Exercise
from app.services.code_execution import ExecutionResult, IsolatedPythonRunner
from app.services.code_execution.python_runner import ALLOWED_IMPORT_ROOTS as RUNNABLE_IMPORTS, parse_learner_python
from app.services.code_grading import PythonGrader, SQLGrader, TextGrader
from app.services.code_grading.grader import UNGRADED_STATUSES
from app.services.exercise_progress import mark_complete  # noqa: F401 - re-exported for callers


RUNNER = IsolatedPythonRunner()
GRADER = PythonGrader(RUNNER)
TEXT_GRADER = TextGrader()
SQL_GRADER = SQLGrader()
TEXT_LANGUAGES = frozenset({"bash", "dockerfile", "hcl", "ini", "sparql", "yaml"})


def grader_for_language(language: str | None):
    if language == "python":
        return GRADER
    if language == "sql":
        return SQL_GRADER
    if language in TEXT_LANGUAGES:
        return TEXT_GRADER
    return None


NOT_EXECUTED_LANGUAGE = {
    "en": "This file is checked by reading it, not by running it. Click Check answer to grade it.\n",
    "ar": "يُفحص هذا الملف بقراءته لا بتشغيله. اضغط «تحقّق من الإجابة» لتقييمه.\n",
}


def check_without_running(code: str, language: str) -> ExecutionResult:
    """Run for an exercise whose libraries cannot run in the sandbox.

    Its grading reads the program's structure (see ``is_static_only``), so
    executing it would only fail on the first import. Report what Run can
    honestly confirm - that the code parses - and where the check happens.
    """
    try:
        tree = parse_learner_python(code)
    except SyntaxError as exc:
        return ExecutionResult("syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})")
    libraries = sorted({
        name.split(".", 1)[0]
        for node in ast.walk(tree)
        for name in (
            [alias.name for alias in node.names] if isinstance(node, ast.Import)
            else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
        )
        if name and name.split(".", 1)[0] not in RUNNABLE_IMPORTS
    })
    names = ", ".join(libraries)
    if language == "ar":
        lead = f"الصياغة سليمة. يستخدم هذا الكود مكتبات لا يمكن تشغيلها في بيئة التدريب ({names})" if names else "الصياغة سليمة"
        return ExecutionResult("success", stdout=(
            f"{lead}، لذلك يُفحص الكود بقراءة بنيته لا بتشغيله. اضغط «تحقّق من الإجابة» لتقييمه.\n"
        ))
    lead = f"Syntax OK. This code uses libraries that cannot run in the practice sandbox ({names})" if names else "Syntax OK"
    return ExecutionResult("success", stdout=(
        f"{lead}, so it is checked by reading its structure instead of running it. Click Check answer to grade it.\n"
    ))


# The worked solution rewards genuine attempts: it opens once the learner has
# passed, or after this many *different* incorrect programs. An untouched
# starter, a program with blanks left, or the same program checked again does
# not count, so clicking Check Answer repeatedly cannot unlock it.
SOLUTION_AFTER_FAILED_CHECKS = 3
# Feedback that would hand over part of the official answer (a check that
# says "Blank 3: `{"result": a / b}`") is held back until this many different
# wrong answers: the learner first hears which blank is wrong, then how.
FULL_FEEDBACK_AFTER_FAILED_CHECKS = 2


def _normalized(code: str | None) -> str:
    return "\n".join(line.rstrip() for line in (code or "").strip().splitlines())


def attempt_state(db: Session, user_id: int, exercise: Exercise) -> dict[str, Any]:
    """This learner's standing on one exercise, derived from the attempt log
    (the authority for whether the solution may be shown)."""
    rows = (
        db.query(
            CodeExerciseAttempt.action, CodeExerciseAttempt.passed, CodeExerciseAttempt.status,
            CodeExerciseAttempt.failed_test_id, CodeExerciseAttempt.submission,
        )
        .filter(CodeExerciseAttempt.user_id == user_id, CodeExerciseAttempt.exercise_id == exercise.id)
        .order_by(CodeExerciseAttempt.id.asc())
        .all()
    )
    starter = _normalized(exercise.starter_code)
    different_failures: set[str] = set()
    passed = viewed = independent = False
    for action, ok, status, failed_test_id, submission in rows:
        if action == "solution":
            viewed = True
        elif action == "submit" and ok:
            passed = True
            # Passing before ever opening the solution is an independent pass.
            independent = independent or not viewed
        # The sandbox being unavailable is not the learner's wrong answer.
        elif action == "submit" and failed_test_id != "blanks_remaining" and status not in UNGRADED_STATUSES:
            code = _normalized(submission)
            if code and code != starter:
                different_failures.add(code)
    available = passed or viewed or len(different_failures) >= SOLUTION_AFTER_FAILED_CHECKS
    return {
        "failed_checks": len(different_failures),
        "passed": passed,
        "completed_independently": independent,
        "solution_viewed": viewed,
        "solution_available": available,
        "checks_until_solution": 0 if available else SOLUTION_AFTER_FAILED_CHECKS - len(different_failures),
    }


def feedback_messages(value: Any, fallback: dict[str, str]) -> dict[str, str]:
    if isinstance(value, str) and value.strip():
        return {"en": value.strip(), "ar": value.strip()}
    if isinstance(value, dict):
        en = str(value.get("en") or value.get("ar") or fallback["en"])
        ar = str(value.get("ar") or value.get("en") or fallback["ar"])
        return {"en": en, "ar": ar}
    return fallback


def record_attempt(
    db: Session, *, user_id: int, exercise_id: int, action: str, status: str,
    submission: str | None = None, passed: bool = False, failed_test_id: str | None = None,
    tests_passed: int = 0, tests_total: int = 0, execution_time_ms: int = 0,
) -> CodeExerciseAttempt:
    attempt = CodeExerciseAttempt(
        user_id=user_id, exercise_id=exercise_id, action=action,
        # Run events intentionally omit source; submitted source is bounded by
        # the request schema and retained for useful attempt analysis.
        submission=submission if action == "submit" else None,
        status=status, passed=passed, failed_test_id=failed_test_id,
        tests_passed=tests_passed, tests_total=tests_total,
        execution_time_ms=execution_time_ms,
    )
    db.add(attempt)
    return attempt


_CODE_SPAN = re.compile(r"`([^`\n]+)`")
_BLANK_NUMBER = re.compile(r"(?:\bBlank\s+|الفراغ\s+)(\d+)")


def _squash(value: str | None) -> str:
    return re.sub(r"\s+", "", value or "")


def reveals_answer(text: str, solution: str | None, starter: str | None) -> bool:
    """True when the message quotes code that is in the official solution
    but not in the starter the learner was given - part of the answer."""
    solution_text, starter_text = _squash(solution), _squash(starter)
    if not solution_text:
        return False
    for span in _CODE_SPAN.findall(text or ""):
        piece = _squash(span)
        if len(piece) >= 2 and piece in solution_text and piece not in starter_text:
            return True
    return False


def _withheld_message(language: str, number: str | None) -> str:
    if language == "ar":
        if number:
            return (f"الفراغ {number} لا يعطي النتيجة المطلوبة بعد. أعد قراءة الخطوة الخاصة به ثم حاول مرة أخرى؛ "
                    "ستظهر ملاحظة أدق بعد محاولتك المختلفة التالية.")
        return "أحد الفحوص لم ينجح بعد. أعد قراءة التعليمات ثم حاول مرة أخرى؛ ستظهر ملاحظة أدق بعد محاولتك المختلفة التالية."
    if number:
        return (f"Blank {number} does not give the required result yet. Re-read its step and try again; "
                "a more specific note appears after your next different attempt.")
    return ("One of the checks does not pass yet. Re-read the instructions and try again; "
            "a more specific note appears after your next different attempt.")


def withhold_answers(
    messages: dict[str, str], *, solution: str | None, starter: str | None, failed_test_id: str | None,
) -> tuple[dict[str, str], bool]:
    """``messages`` with any answer-revealing text replaced by a message
    that still names the blank. Returns (messages, whether anything was held back)."""
    fallback = re.match(r"blank_(\d+)", failed_test_id or "")
    result, withheld = dict(messages), False
    for language in ("en", "ar"):
        text = messages.get(language) or ""
        if reveals_answer(text, solution, starter):
            found = _BLANK_NUMBER.search(text)
            number = found.group(1) if found else (fallback.group(1) if fallback else None)
            result[language] = _withheld_message(language, number)
            withheld = True
    return result, withheld
