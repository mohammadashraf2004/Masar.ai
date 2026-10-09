"""Deterministic code exercise API. No LLM or wallet service is imported here."""
from contextlib import nullcontext

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.learning import Exercise
from app.models.user import User
from app.services.billing.access_service import course_for_content, require_content_access
from app.services.code_exercises import (
    NOT_EXECUTED_LANGUAGE, SQL_GRADER, check_without_running, grader_for_language, RUNNER,
    attempt_state, feedback_messages, mark_complete, record_attempt,
)
from app.services.code_execution import ExecutionResult
from app.services.code_execution.messages import platform_message
from app.services.code_grading.authoring import count_python_blanks
from app.services.code_grading.grader import blanks_remaining_feedback, first_blank_line, is_static_only
from app.services.execution_fairness import runner_turn
from app.services.learning import enrollment as course_enrollment
from app.views.code_exercise import (
    AttemptStateResponse, CodeExerciseResponse, CodePayload, FeedbackResponse, RunResponse, SolutionResponse,
    SubmitResponse,
)


router = APIRouter(prefix="/practice/exercises", tags=["Code Exercises"])


def _exercise(db: Session, exercise_id: int, user_id: int) -> Exercise:
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    require_content_access(db, user_id, exercise)
    return exercise


def _code_exercise(db: Session, exercise_id: int, user_id: int, *, require_tests: bool = True) -> Exercise:
    exercise = _exercise(db, exercise_id, user_id)
    if exercise.exercise_type != "code" and not exercise.starter_code:
        raise HTTPException(status_code=409, detail={"code": "NOT_CODE_EXERCISE"})
    if grader_for_language(exercise.language) is None:
        raise HTTPException(status_code=409, detail={"code": "UNSUPPORTED_LANGUAGE", "language": exercise.language})
    if require_tests and not exercise.grading_tests:
        raise HTTPException(status_code=409, detail={"code": "EXERCISE_NOT_MIGRATED"})
    return exercise


@router.get("/{exercise_id}", response_model=CodeExerciseResponse)
def get_code_exercise(
    exercise_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    # Response schema intentionally has no solution, setup, or tests.
    return _exercise(db, exercise_id, current_user.id)


@router.get("/{exercise_id}/progress", response_model=AttemptStateResponse)
def get_attempt_state(
    exercise_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Where this learner stands (attempts, pass, solution access), so a
    reloaded page offers the same options as before."""
    exercise = _code_exercise(db, exercise_id, current_user.id, require_tests=False)
    return AttemptStateResponse(**attempt_state(db, current_user.id, exercise))


@router.post("/{exercise_id}/run", response_model=RunResponse)
@limiter.limit("30/minute")
async def run_code(
    request: Request, exercise_id: int, payload: CodePayload,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    exercise = _code_exercise(db, exercise_id, current_user.id, require_tests=False)
    remaining = count_python_blanks(payload.code) if exercise.language == "python" else 0
    if remaining:
        message = blanks_remaining_feedback(remaining, first_blank_line(payload.code))[payload.language]
        result = ExecutionResult("incomplete", stderr=message + "\n")
    elif exercise.language == "python" and is_static_only(list(exercise.grading_tests or [])):
        result = check_without_running(payload.code, payload.language)
    elif exercise.language == "python":
        # Plain values only past this commit: touching an expired ORM object
        # (even current_user.id) would silently reopen a transaction and pin
        # the connection for the whole runner wait.
        setup, user_id = exercise.pre_exercise_code or "", current_user.id
        db.commit()  # no pooled connection held while the runner works
        async with runner_turn(user_id):
            result = await RUNNER.run(payload.code, pre_exercise_code=setup)
    elif exercise.language == "sql":
        result = await SQL_GRADER.run(payload.code, list(exercise.grading_tests or []))
    else:
        result = ExecutionResult("success", stdout=NOT_EXECUTED_LANGUAGE[payload.language])
    record_attempt(
        db, user_id=current_user.id, exercise_id=exercise.id, action="run",
        status=result.status, execution_time_ms=result.execution_time_ms,
    )
    db.commit()
    # When nothing ran, stderr holds Masar's own message (runner off or unavailable), not the
    # learner's output: give it in the interface language.
    stderr = result.stderr
    if result.status == "execution_error":
        stderr = platform_message(stderr, payload.language)
    return RunResponse(
        status=result.status, stdout=result.stdout, stderr=stderr,
        execution_time_ms=result.execution_time_ms,
    )


@router.post("/{exercise_id}/submit", response_model=SubmitResponse)
@limiter.limit("20/minute")
async def submit_code(
    request: Request, exercise_id: int, payload: CodePayload,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    exercise = _code_exercise(db, exercise_id, current_user.id)
    grader = grader_for_language(exercise.language)
    assert grader is not None  # validated by _code_exercise
    # Python grading runs on the shared runner (SQL is graded in-process and
    # bounded in sql_grader); hold this account's runner turn for it.
    tests, setup = list(exercise.grading_tests or []), exercise.pre_exercise_code or ""
    language, user_id = exercise.language, current_user.id
    db.commit()  # no pooled connection held while the runner works (plain values only below)
    turn = runner_turn(user_id) if language == "python" else nullcontext()
    async with turn:
        grade = await grader.grade(payload.code, tests, pre_exercise_code=setup)
    feedback = grade.feedback
    if grade.passed and exercise.success_message:
        feedback = {"en": exercise.success_message, "ar": exercise.success_message_ar or exercise.success_message}
    messages = feedback_messages(feedback, {"en": "Check your solution.", "ar": "راجع حلك."})
    record_attempt(
        db, user_id=current_user.id, exercise_id=exercise.id, action="submit",
        submission=payload.code, status=grade.status, passed=grade.passed,
        failed_test_id=grade.failed_test_id, tests_passed=grade.tests_passed,
        tests_total=grade.tests_total, execution_time_ms=grade.execution.execution_time_ms,
    )
    if grade.passed:
        mark_complete(db, current_user.id, exercise)
    course = course_for_content(db, exercise) if grade.passed else None
    db.flush()
    state = attempt_state(db, current_user.id, exercise)
    db.commit()
    if course is not None:
        course_enrollment.sync_lifecycle(db, current_user.id, course)
    stderr = grade.execution.stderr
    if grade.status == "execution_error":  # Masar's own message, as in run_code
        stderr = platform_message(stderr, payload.language)
    return SubmitResponse(
        status=grade.status, passed=grade.passed, stdout=grade.execution.stdout,
        stderr=stderr, execution_time_ms=grade.execution.execution_time_ms,
        feedback=FeedbackResponse(
            code=grade.feedback_code, message=messages[payload.language],
            messages=messages, test_id=grade.failed_test_id,
        ),
        tests_passed=grade.tests_passed, tests_total=grade.tests_total,
        failed_test=grade.failed_test_id,
        attempt=AttemptStateResponse(**state),
    )


@router.post("/{exercise_id}/solution", response_model=SolutionResponse)
def show_solution(
    exercise_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    exercise = _code_exercise(db, exercise_id, current_user.id, require_tests=False)
    if not exercise.solution_code:
        raise HTTPException(status_code=404, detail="No solution is available")
    # The worked solution is a reward for trying, not a shortcut: it opens
    # after a pass or after several genuinely different attempts.
    state = attempt_state(db, current_user.id, exercise)
    if not state["solution_available"]:
        raise HTTPException(status_code=403, detail={
            "code": "SOLUTION_LOCKED", "checks_until_solution": state["checks_until_solution"],
        })
    record_attempt(
        db, user_id=current_user.id, exercise_id=exercise.id, action="solution",
        status="solution_viewed",
    )
    db.commit()
    return SolutionResponse(solution_code=exercise.solution_code)
