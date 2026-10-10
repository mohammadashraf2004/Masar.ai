"""Integration coverage for the deterministic code-exercise path."""
import uuid

import pytest

from app.models.code_exercise import CodeExerciseAttempt
from app.models.learning import CareerTrack, DifficultyLevel, Exercise, Topic, TrackLevel
from app.models.progress import UserProgress
from app.models.wallet import UserWallet, WalletTransaction


PASSWORD = "correct-horse-battery-staple-7"


def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "accept_terms": True,
        "accept_privacy": True,
        "email": f"code-exercise-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Code Exercise Tester",
        "password": PASSWORD,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def code_exercise(db):
    track = CareerTrack(slug=f"code-{uuid.uuid4().hex[:8]}", title="Code", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Level", order=1)
    db.add(level)
    db.flush()
    topic = Topic(
        level_id=level.id, title="Python", slug=f"python-{uuid.uuid4().hex[:8]}", order=1,
        difficulty=DifficultyLevel.beginner, estimated_hours=1, prerequisite_ids=[], skill_tags=[],
    )
    db.add(topic)
    db.flush()
    exercise = Exercise(
        topic_id=topic.id, title="Round a value", description="Create result with round().",
        exercise_type="code", language="python", starter_code="value = 3.14159\nresult = ____",
        pre_exercise_code="hidden_value = 99", solution_code="result = round(3.14159, 2)",
        hint="Use round(value, digits).", success_message="Correct rounding.", skill_tested=["python"],
        grading_tests=[
            {"id": "result_exists", "type": "variable_exists", "variable": "result", "feedback": {"en": "Create result.", "ar": "أنشئ result."}},
            {"id": "round_called", "type": "function_called", "function": "round", "feedback": {"en": "Use round().", "ar": "استخدم round()."}},
            {"id": "round_digits", "type": "function_argument", "function": "round", "argument_index": 1, "expected": 2, "feedback": {"en": "Use two decimal places.", "ar": "استخدم منزلتين عشريتين."}},
            {"id": "result_value", "type": "value_equals", "variable": "result", "expected": 3.14, "feedback": {"en": "Check result.", "ar": "راجع result."}},
        ],
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@pytest.fixture()
def sql_exercise(db, code_exercise):
    starter = (
        "SELECT /* blank:1 */ ___ /* endblank */ AS customer_id, "
        "/* blank:2 */ ___ /* endblank */ AS orders "
        "FROM purchases GROUP BY customer_id ORDER BY customer_id;"
    )
    solution = starter.replace("___", "customer_id", 1).replace("___", "COUNT(*)", 1)
    exercise = Exercise(
        topic_id=code_exercise.topic_id, title="Count customer orders",
        description="Complete the two important SQL fields.", exercise_type="code",
        language="sql", starter_code=starter, solution_code=solution,
        hint="Select the customer and count rows.", success_message="Correct SQL.",
        skill_tested=["sql", "group-by"], grading_tests=[
            {
                "id": "blank_1", "type": "sql_blank", "blank": 1,
                "accepted": ["customer_id"],
                "feedback": {"en": "Blank 1: select customer_id.", "ar": "الفراغ 1: اختر customer_id."},
            },
            {
                "id": "blank_2", "type": "sql_blank", "blank": 2,
                "accepted": ["COUNT(*)"],
                "feedback": {"en": "Blank 2: count rows.", "ar": "الفراغ 2: عد الصفوف."},
            },
            {
                "id": "result", "type": "sql_result",
                "setup_sql": (
                    "CREATE TABLE purchases(customer_id INTEGER);"
                    "INSERT INTO purchases VALUES (1),(1),(2);"
                ),
                "expected_columns": ["customer_id", "orders"],
                "expected_rows": [[1, 2], [2, 1]], "ordered": True,
                "feedback": {"en": "Check the grouped result.", "ar": "راجع نتيجة التجميع."},
            },
        ],
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def test_safe_read_run_submit_progress_attempts_and_no_credits(client, db, code_exercise):
    user_id, headers = _register(client)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    starting_balance = wallet.credit_balance
    starting_transactions = db.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet.id).count()

    public = client.get(f"/api/v1/practice/exercises/{code_exercise.id}", headers=headers)
    assert public.status_code == 200, public.text
    assert public.json()["starter_code"]
    for secret in ("solution_code", "pre_exercise_code", "grading_tests", "tests"):
        assert secret not in public.json()

    run = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/run",
        headers=headers, json={"code": "print('hello')"},
    )
    assert run.status_code == 200, run.text
    assert run.json()["status"] == "success"
    assert run.json()["stdout"] == "hello\n"
    assert db.query(UserProgress).filter(UserProgress.user_id == user_id).first() is None

    missing = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/submit",
        headers=headers, json={"code": "value = 3.14159", "language": "en"},
    )
    assert missing.status_code == 200, missing.text
    assert missing.json()["failed_test"] == "result_exists"

    partial = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/submit",
        headers=headers, json={"code": "result = 3.14", "language": "ar"},
    )
    assert partial.status_code == 200, partial.text
    assert partial.json()["failed_test"] == "round_called"
    assert partial.json()["feedback"]["message"] == "استخدم round()."

    correct = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/submit",
        headers=headers, json={"code": "result = round(3.14159, 2)"},
    )
    assert correct.status_code == 200, correct.text
    assert correct.json()["passed"] is True
    assert correct.json()["tests_passed"] == correct.json()["tests_total"] == 4

    db.expire_all()
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).one()
    assert code_exercise.id in progress.exercises_completed
    attempts = db.query(CodeExerciseAttempt).filter(CodeExerciseAttempt.user_id == user_id).all()
    assert [attempt.action for attempt in attempts] == ["run", "submit", "submit", "submit"]
    assert attempts[0].submission is None
    assert attempts[-1].submission == "result = round(3.14159, 2)"
    assert db.query(UserWallet).filter(UserWallet.user_id == user_id).one().credit_balance == starting_balance
    assert db.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet.id).count() == starting_transactions


def test_code_exercise_cannot_fall_back_to_ai_or_client_completion(client, db, code_exercise):
    user_id, headers = _register(client)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    starting_balance = wallet.credit_balance

    ai = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/answer",
        headers=headers, json={"content": "looks correct"},
    )
    assert ai.status_code == 409
    assert ai.json()["detail"]["code"] == "USE_DETERMINISTIC_CODE_GRADER"

    bypass = client.post(
        f"/api/v1/tracks/topics/{code_exercise.topic_id}/progress",
        headers=headers, json={"exercise_id": code_exercise.id},
    )
    assert bypass.status_code == 409
    assert bypass.json()["detail"]["code"] == "SUBMIT_CODE_TO_COMPLETE"

    db.expire_all()
    assert db.query(UserProgress).filter(UserProgress.user_id == user_id).first() is None
    assert db.query(UserWallet).filter(UserWallet.user_id == user_id).one().credit_balance == starting_balance


def test_show_solution_is_explicit_and_never_completes(client, db, code_exercise):
    user_id, headers = _register(client)
    base = f"/api/v1/practice/exercises/{code_exercise.id}"

    def submit(code):
        response = client.post(f"{base}/submit", headers=headers, json={"code": code})
        assert response.status_code == 200 and response.json()["passed"] is False
        return response.json()["attempt"]

    locked = client.post(f"{base}/solution", headers=headers)
    assert locked.status_code == 403
    assert locked.json()["detail"] == {"code": "SOLUTION_LOCKED", "checks_until_solution": 3}

    # Neither the untouched starter nor the same program checked again is a new attempt.
    assert submit(code_exercise.starter_code)["failed_checks"] == 0
    assert submit("value = 3.14159\nresult = 3")["failed_checks"] == 1
    assert submit("value = 3.14159\nresult = 3\n")["checks_until_solution"] == 2
    assert submit("value = 3.14159\nresult = round(value)")["checks_until_solution"] == 1
    assert client.post(f"{base}/solution", headers=headers).status_code == 403
    third = submit("value = 3.14159\nresult = round(value, 3)")
    assert third["solution_available"] is True and third["failed_checks"] == 3

    # A reload asks the server, which remembers.
    state = client.get(f"{base}/progress", headers=headers).json()
    assert state == {
        "failed_checks": 3, "passed": False, "completed_independently": False,
        "solution_viewed": False, "solution_available": True, "checks_until_solution": 0,
    }

    response = client.post(f"{base}/solution", headers=headers)
    assert response.status_code == 200
    assert response.json()["solution_code"] == code_exercise.solution_code
    attempt = db.query(CodeExerciseAttempt).filter_by(
        user_id=user_id, exercise_id=code_exercise.id, action="solution",
    ).one()
    assert attempt.status == "solution_viewed"
    assert attempt.passed is False
    # Viewing the solution completes nothing.
    assert db.query(UserProgress).filter(UserProgress.user_id == user_id).first() is None

    # Passing after viewing it completes the exercise, but not independently.
    passed = client.post(f"{base}/submit", headers=headers, json={"code": "value = 3.14159\nresult = round(value, 2)"})
    assert passed.json()["passed"] is True
    assert passed.json()["attempt"]["completed_independently"] is False
    assert client.get(f"{base}/progress", headers=headers).json()["solution_viewed"] is True


def test_passing_first_unlocks_the_solution_and_counts_as_independent(client, db, code_exercise):
    _, headers = _register(client)
    base = f"/api/v1/practice/exercises/{code_exercise.id}"
    passed = client.post(f"{base}/submit", headers=headers, json={"code": "value = 3.14159\nresult = round(value, 2)"})
    assert passed.json()["attempt"] == {
        "failed_checks": 0, "passed": True, "completed_independently": True,
        "solution_viewed": False, "solution_available": True, "checks_until_solution": 0,
    }
    assert client.post(f"{base}/solution", headers=headers).status_code == 200


def test_attempt_state_is_private_to_each_learner(client, db, code_exercise):
    _, first = _register(client)
    _, second = _register(client)
    base = f"/api/v1/practice/exercises/{code_exercise.id}"
    client.post(f"{base}/submit", headers=first, json={"code": "value = 3.14159\nresult = round(value, 2)"})
    assert client.get(f"{base}/progress", headers=second).json()["solution_available"] is False
    assert client.post(f"{base}/solution", headers=second).status_code == 403
    assert client.get(f"{base}/progress").status_code in (401, 403)


def test_classified_pending_code_can_run_but_cannot_receive_fake_marks(client, db, code_exercise):
    code_exercise.exercise_type = "code_pending"
    code_exercise.grading_tests = None
    code_exercise.solution_code = None
    db.commit()
    user_id, headers = _register(client)

    public = client.get(f"/api/v1/practice/exercises/{code_exercise.id}", headers=headers)
    assert public.status_code == 200
    assert public.json()["exercise_type"] == "code_pending"
    assert public.json()["grading_available"] is False

    run = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/run",
        headers=headers, json={"code": "print('draft')"},
    )
    assert run.status_code == 200
    assert run.json()["stdout"] == "draft\n"

    submit = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/submit",
        headers=headers, json={"code": "print('draft')"},
    )
    assert submit.status_code == 409
    assert submit.json()["detail"]["code"] == "EXERCISE_NOT_MIGRATED"
    assert db.query(UserProgress).filter(UserProgress.user_id == user_id).first() is None


def test_pending_shell_exercise_uses_the_editor_without_claiming_execution(client, db, code_exercise):
    code_exercise.exercise_type = "code_pending"
    code_exercise.language = "bash"
    code_exercise.grading_tests = None
    code_exercise.solution_code = None
    db.commit()
    _, headers = _register(client)

    response = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/run",
        headers=headers, json={"code": "git status"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "checked by reading it, not by running it" in response.json()["stdout"]

    arabic = client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/run",
        headers=headers, json={"code": "git status", "language": "ar"},
    )
    assert "بقراءته لا بتشغيله" in arabic.json()["stdout"]


def test_sql_run_and_submit_are_isolated_deterministic_and_track_progress(client, db, sql_exercise):
    user_id, headers = _register(client)

    public = client.get(f"/api/v1/practice/exercises/{sql_exercise.id}", headers=headers)
    assert public.status_code == 200, public.text
    assert public.json()["language"] == "sql"
    assert "setup_sql" not in public.text

    run_response = client.post(
        f"/api/v1/practice/exercises/{sql_exercise.id}/run",
        headers=headers, json={"code": sql_exercise.solution_code},
    )
    assert run_response.status_code == 200, run_response.text
    assert run_response.json()["status"] == "success"
    assert "customer_id\torders" in run_response.json()["stdout"]

    wrong_code = sql_exercise.starter_code.replace("___", "customer_id", 1).replace("___", "SUM(customer_id)", 1)
    wrong = client.post(
        f"/api/v1/practice/exercises/{sql_exercise.id}/submit",
        headers=headers, json={"code": wrong_code},
    )
    assert wrong.status_code == 200, wrong.text
    assert wrong.json()["passed"] is False
    assert wrong.json()["failed_test"] == "blank_2"

    correct = client.post(
        f"/api/v1/practice/exercises/{sql_exercise.id}/submit",
        headers=headers, json={"code": sql_exercise.solution_code},
    )
    assert correct.status_code == 200, correct.text
    assert correct.json()["passed"] is True
    assert correct.json()["tests_passed"] == correct.json()["tests_total"] == 3

    db.expire_all()
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).one()
    assert sql_exercise.id in progress.exercises_completed


# ─── Sandbox: learner Python never runs outside the execution service ──────

@pytest.fixture()
def execution_disabled(monkeypatch):
    """The production fail-closed switch (PROJECT_LAB_EXECUTION_BACKEND=disabled),
    with every in-process path booby-trapped so a fallback would be caught."""
    from app.services.code_execution.python_runner import LocalPythonRunner
    from app.services.project_lab import execution

    async def must_not_run(*args, **kwargs):
        raise AssertionError("learner code must not run outside the execution service")

    monkeypatch.setattr(execution, "_service", execution.ProjectExecutionService(execution.DisabledBackend()))
    monkeypatch.setattr(LocalPythonRunner, "run", must_not_run)
    monkeypatch.setattr(execution.LocalSubprocessBackend, "execute", must_not_run)


def test_disabled_execution_fails_closed_for_run_and_check(client, db, code_exercise, execution_disabled):
    user_id, headers = _register(client)
    base = f"/api/v1/practice/exercises/{code_exercise.id}"
    solution = "value = 3.14159\nresult = round(value, 2)"

    run = client.post(f"{base}/run", headers=headers, json={"code": solution})
    assert run.status_code == 200 and run.json()["status"] == "execution_error"

    submit = client.post(f"{base}/submit", headers=headers, json={"code": solution})
    assert submit.status_code == 200
    assert submit.json()["passed"] is False and submit.json()["status"] == "execution_error"
    assert "not available" in submit.json()["feedback"]["message"]
    # An outage is not a wrong answer: it never counts toward the solution.
    for code in ("result = 1", "result = 2", "result = 3"):
        client.post(f"{base}/submit", headers=headers, json={"code": f"value = 3.14159\n{code}"})
    state = client.get(f"{base}/progress", headers=headers).json()
    assert (state["failed_checks"], state["solution_available"]) == (0, False)
    assert db.query(UserProgress).filter(UserProgress.user_id == user_id).first() is None


def test_production_never_selects_the_in_process_backend(monkeypatch):
    from app.core.config import settings
    from app.services.project_lab import execution

    monkeypatch.setattr(type(settings), "is_production", property(lambda self: True))
    monkeypatch.setattr(settings, "PROJECT_LAB_EXECUTION_BACKEND", "")
    assert settings.project_lab_backend == "disabled"
    assert isinstance(execution.build_backend(), execution.DisabledBackend)
    monkeypatch.setattr(settings, "PROJECT_LAB_EXECUTION_BACKEND", "local")
    assert isinstance(execution.build_backend(), execution.DisabledBackend)
