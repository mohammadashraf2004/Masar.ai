import asyncio

from app.services.code_execution import LocalPythonRunner
from app.services.code_grading import PythonGrader, SQLGrader, TextGrader
from app.services.code_grading.sql_grader import sql_blank_values
from app.services.code_grading.authoring import (
    build_fill_in_blank_exercise,
    build_static_python_tests,
    count_python_blanks,
)
from app.services.code_grading.sql_grader import sql_blanks_remaining
from app.services.code_grading.text_grader import text_blanks_remaining, text_fingerprint


def run(coro):
    return asyncio.run(coro)


def test_value_checks_accept_semantically_equivalent_answers():
    tests = [{"id": "x", "type": "value_equals", "variable": "x", "expected": 10, "feedback": "wrong"}]
    grader = PythonGrader()
    assert run(grader.grade("x = 10", tests)).passed
    assert run(grader.grade("x = 5 + 5", tests)).passed


def test_variable_type_and_first_failure_feedback():
    tests = [
        {"id": "exists", "type": "variable_exists", "variable": "answer", "feedback": {"en": "Create answer", "ar": "أنشئ answer"}},
        {"id": "type", "type": "type_equals", "variable": "answer", "expected": "int", "feedback": "Use an integer"},
        {"id": "value", "type": "value_equals", "variable": "answer", "expected": 42, "feedback": "Check answer"},
    ]
    missing = run(PythonGrader().grade("pass", tests))
    assert (missing.failed_test_id, missing.tests_passed) == ("exists", 0)
    wrong_type = run(PythonGrader().grade("answer = '42'", tests))
    assert (wrong_type.failed_test_id, wrong_type.tests_passed) == ("type", 1)


def test_required_technique_even_when_value_is_correct():
    tests = [
        {"id": "exists", "type": "variable_exists", "variable": "result", "feedback": "missing"},
        {"id": "round", "type": "function_called", "function": "round", "feedback": "Use round"},
        {"id": "digits", "type": "function_argument", "function": "round", "argument_index": 1, "expected": 2, "feedback": "Use two places"},
        {"id": "value", "type": "value_equals", "variable": "result", "expected": 3.14, "feedback": "wrong value"},
    ]
    direct = run(PythonGrader().grade("result = 3.14", tests))
    assert direct.failed_test_id == "round"
    wrong_argument = run(PythonGrader().grade("result = round(3.14159)", tests))
    assert wrong_argument.failed_test_id == "digits"
    assert run(PythonGrader().grade("result = round(3.14159, 2)", tests)).passed


def test_zero_required_tests_can_never_award_a_vacuous_full_mark():
    result = run(PythonGrader().grade("answer = 'wrong'", [
        {
            "id": "optional", "type": "value_equals", "variable": "answer",
            "expected": "right", "required": False, "feedback": "wrong",
        },
    ]))
    assert result.status == "grading_error"
    assert result.passed is False
    assert result.feedback_code == "INVALID_TEST_CONFIGURATION"
    assert (result.tests_passed, result.tests_total) == (0, 0)


def test_qdrant_custom_checks_reject_a_non_numeric_vector():
    result = run(PythonGrader().grade(
        "point = {'vector': 'not a vector'}",
        [{
            "id": "vector", "type": "custom", "checker": "check_qdrant_vector",
            "feedback": "Use a numeric vector.",
        }],
    ))
    assert result.passed is False
    assert result.failed_test_id == "vector"


def test_function_count_not_called_definition_and_return_value():
    tests = [
        {"id": "defined", "type": "function_exists", "function": "double", "feedback": "define it"},
        {"id": "return", "type": "return_value_equals", "function": "double", "args": [4], "expected": 8, "feedback": "wrong return"},
        {"id": "called", "type": "function_call_count", "function": "double", "expected": 1, "feedback": "call once"},
        {"id": "no_print", "type": "function_not_called", "function": "print", "feedback": "do not print"},
    ]
    result = run(PythonGrader().grade("def double(x):\n    return x * 2\nanswer = double(3)\n", tests))
    assert result.passed


def test_stdout_syntax_runtime_timeout_and_forbidden_operations():
    # Give normal Windows process startup enough headroom; use the short
    # runner only for the intentional infinite loop below.
    grader = PythonGrader(LocalPythonRunner(timeout_seconds=2.0))
    stdout = run(grader.grade("print('hello world')", [
        {"id": "out", "type": "stdout_contains", "expected": "hello", "feedback": "print hello"},
    ]))
    assert stdout.passed and stdout.execution.stdout == "hello world\n"
    assert run(grader.grade("if:", [])).status == "syntax_error"
    assert run(grader.grade("raise RuntimeError('boom')", [])).status == "runtime_error"
    timeout_grader = PythonGrader(LocalPythonRunner(timeout_seconds=0.25))
    assert run(timeout_grader.grade("while True: pass", [])).status == "timeout"
    assert run(grader.grade("open('secret.txt')", [])).status == "forbidden_operation"
    assert run(grader.grade("import socket", [])).status == "forbidden_operation"


def test_collection_pre_exercise_and_output_limit_checks():
    tests = [
        {"id": "list", "type": "list_length", "variable": "items", "expected": 3, "feedback": "three"},
        {"id": "key", "type": "dict_contains_key", "variable": "record", "key": "ready", "feedback": "key"},
        {"id": "hidden", "type": "value_equals", "variable": "result", "expected": 7, "feedback": "value"},
    ]
    result = run(PythonGrader().grade(
        "items = [1, 2, 3]\nrecord = {'ready': True}\nresult = hidden_value",
        tests, pre_exercise_code="hidden_value = 7",
    ))
    assert result.passed


def test_legacy_static_tests_reject_starter_and_accept_solution_without_execution():
    starter = "from unavailable_framework import Client\nclient = None\n\ndef build():\n    pass\n"
    solution = (
        "from unavailable_framework import Client\n"
        "client = Client(url='local')\n\n"
        "def build():\n    return client.create_collection(name='docs')\n"
    )
    tests = build_static_python_tests(starter, solution)

    class RunnerThatMustNotRun:
        async def run(self, *args, **kwargs):
            raise AssertionError("static grading must not execute framework code")

    grader = PythonGrader(RunnerThatMustNotRun())
    unchanged = run(grader.grade(starter, tests))
    assert not unchanged.passed
    assert unchanged.failed_test_id == "starter_changed"
    assert run(grader.grade(solution, tests)).passed


def test_legacy_static_tests_accept_an_alternative_implementation_but_reject_placeholders():
    starter = "result = None\n\ndef transform(value):\n    pass\n"
    solution = "result = transform('x')\n\ndef transform(value):\n    return value.upper()\n"
    tests = build_static_python_tests(starter, solution)
    grader = PythonGrader()

    incomplete = run(grader.grade("result = 'changed'\n\ndef transform(value):\n    pass\n", tests))
    assert not incomplete.passed
    assert incomplete.failed_test_id == "placeholders_removed"

    alternative = "def transform(item):\n    return item.title()\n\nresult = transform('different')\n"
    assert run(grader.grade(alternative, tests)).passed


def test_fill_in_blank_authoring_checks_each_field_before_execution():
    starter = (
        "numbers = [1, 2, 3, 4]\n"
        "# TODO: calculate the requested summary values\n"
        "total = None\n"
        "average = None\n"
    )
    solution = (
        "numbers = [1, 2, 3, 4]\n"
        "total = sum(numbers)\n"
        "average = total / len(numbers)\n"
    )
    behavioral_tests = [
        {"id": "total", "type": "value_equals", "variable": "total", "expected": 10, "feedback": "Check the total."},
        {"id": "average", "type": "value_equals", "variable": "average", "expected": 2.5, "feedback": "Check the average."},
    ]
    blanked, tests, labels = build_fill_in_blank_exercise(starter, solution, behavioral_tests)

    assert count_python_blanks(blanked) == 2
    assert "numbers = [1, 2, 3, 4]" in blanked
    assert labels == ["the expression assigned to `total`", "the expression assigned to `average`"]

    class RunnerThatMustNotRun:
        async def run(self, *args, **kwargs):
            raise AssertionError("an unresolved blank must fail before execution")

    # Unfilled blanks are reported as such, in both languages, before anything runs.
    grader = PythonGrader(RunnerThatMustNotRun())
    first = run(grader.grade(blanked, tests))
    assert (first.failed_test_id, first.tests_passed, first.feedback_code) == ("blanks_remaining", 0, "BLANKS_REMAINING")
    first_line = blanked.splitlines().index("total = ___") + 1
    assert "2 blanks" in first.feedback["en"] and f"line {first_line}" in first.feedback["en"]
    assert f"السطر {first_line}" in first.feedback["ar"]

    first_completed = blanked.replace("___", "sum(numbers)", 1)
    second = run(grader.grade(first_completed, tests))
    assert second.feedback_code == "BLANKS_REMAINING"
    assert "One blank" in second.feedback["en"] and f"line {first_line + 1}" in second.feedback["en"]

    # With behavioural checks the blanks are advisory: an equivalent expression
    # passes, and a wrong value is pointed at the blank that computed it.
    equivalent = blanked.replace("___", "numbers[0] + numbers[1] + numbers[2] + numbers[3]", 1).replace(
        "___", "sum(numbers) / 4", 1,
    )
    accepted = run(PythonGrader().grade(equivalent, tests))
    assert accepted.passed and accepted.tests_passed == accepted.tests_total

    wrong = blanked.replace("___", "max(numbers)", 1).replace("___", "total / len(numbers)", 1)
    rejected = run(PythonGrader().grade(wrong, tests))
    assert (rejected.passed, rejected.failed_test_id) == (False, "blank_1")
    assert "Blank 1" in rejected.feedback["en"]

    assert run(PythonGrader().grade(solution, tests)).passed


def test_static_configuration_grader_accepts_valid_variants_and_rejects_starter():
    starter = "# TODO: write a Dockerfile\n"
    tests = [
        {
            "id": "changed", "type": "text_changed",
            "starter_fingerprint": text_fingerprint(starter), "feedback": "complete it",
        },
        {
            "id": "required", "type": "regex_all",
            "patterns": [r"^FROM\s+python:3\.12-slim$", r"^WORKDIR\s+/app$"],
            "feedback": "missing instruction",
        },
        {
            "id": "safe", "type": "regex_none", "patterns": [r"^ENV\s+API_KEY"],
            "feedback": "do not bake secrets",
        },
    ]
    grader = TextGrader()
    assert not run(grader.grade(starter, tests)).passed
    assert run(grader.grade("FROM python:3.12-slim\nWORKDIR /app\n", tests)).passed
    unsafe = run(grader.grade("FROM python:3.12-slim\nWORKDIR /app\nENV API_KEY=secret\n", tests))
    assert not unsafe.passed
    assert unsafe.failed_test_id == "safe"

    blank_tests = [{
        "id": "blank_1", "type": "regex_all", "patterns": [r"^FROM python:3\.12-slim$"],
        "feedback": {"en": "Blank 1: choose the base image.", "ar": "الفراغ 1: اختر الصورة الأساسية."},
    }]
    blank = run(grader.grade("FROM python:3.11\n", blank_tests))
    assert blank.feedback_code == "BLANK_INCORRECT"
    assert blank.feedback["en"].startswith("Blank 1")

    # A blank left empty is unfinished, not a wrong answer.
    empty = run(grader.grade("FROM ___\n", blank_tests))
    assert (empty.passed, empty.feedback_code, empty.failed_test_id) == (False, "BLANKS_REMAINING", "blanks_remaining")
    assert empty.feedback["en"].startswith("One blank (`___`) is still empty. The first one is on line 1.")
    assert "أولها في السطر 1" in empty.feedback["ar"]


def test_blanks_remaining_feedback_uses_correct_arabic_number_forms():
    from app.services.code_grading.grader import blanks_remaining_feedback

    assert blanks_remaining_feedback(1, 4)["ar"].startswith("ما زال هناك فراغ واحد (`___`) لم يُملأ. أولها في السطر 4.")
    two = blanks_remaining_feedback(2, 3)["ar"]
    assert two.startswith("ما زال هناك فراغان (`___`) لم يُملآ. أولهما في السطر 3. أكملهما")
    assert blanks_remaining_feedback(5)["ar"].startswith("ما زالت هناك 5 فراغات (`___`) لم تُملأ. أكملها")
    assert blanks_remaining_feedback(12)["ar"].startswith("ما زالت هناك 12 فراغًا (`___`)")
    assert blanks_remaining_feedback(2, 3)["en"] == (
        "2 blanks (`___`) are still empty. The first one is on line 3. Fill them in, then check your answer again."
    )


def test_text_blanks_remaining_counts_every_placeholder_including_comments():
    assert text_blanks_remaining("FROM python:3.12-slim\nWORKDIR /app\n") == (0, None)
    assert text_blanks_remaining("FROM ___\nWORKDIR ___\n") == (2, 1)
    # Blanks inside YAML templating, after a sigil, and in a comment the brief asks to complete.
    assert text_blanks_remaining("replicas: 3\nimage: \"{{ ___ }}\"\n") == (1, 2)
    assert text_blanks_remaining("subjectAltName = @___\n") == (1, 1)
    assert text_blanks_remaining("# ex:nolan ex:directed ___ .\nSELECT ?m WHERE {}\n") == (1, 1)
    # Identifiers that merely contain underscores are the learner's own text.
    assert text_blanks_remaining("my___var: 1\n____: 2\n") == (0, None)


def _sql_blank_tests(template: str) -> list[dict]:
    return [
        {
            "id": "blank_1", "type": "sql_blank", "blank": 1,
            "accepted": ["customer_id"],
            "feedback": {"en": "Blank 1: select the customer.", "ar": "الفراغ 1: اختر العميل."},
        },
        {
            "id": "blank_2", "type": "sql_blank", "blank": 2,
            "accepted": ["COUNT(*)", "count(1)"],
            "feedback": {"en": "Blank 2: count the rows.", "ar": "الفراغ 2: عد الصفوف."},
        },
        {
            "id": "result", "type": "sql_result", "template": template,
            "setup_sql": (
                "CREATE TABLE purchases(customer_id INTEGER);"
                "INSERT INTO purchases VALUES (1),(1),(2);"
            ),
            "expected_columns": ["customer_id", "orders"],
            "expected_rows": [[1, 2], [2, 1]], "ordered": True,
            "feedback": {"en": "Check the result.", "ar": "راجع النتيجة."},
        },
    ]


PLAIN_SQL_STARTER = (
    "SELECT ___ AS customer_id,\n"
    "       ___ AS orders\n"
    "FROM purchases GROUP BY customer_id ORDER BY customer_id;"
)


def test_sql_starter_shows_bare_blanks_and_fields_are_still_checked_one_by_one():
    tests = _sql_blank_tests(PLAIN_SQL_STARTER)
    grader = SQLGrader()

    # Untouched or half-filled is unfinished, not wrong: never run, never an attempt.
    first = run(grader.grade(PLAIN_SQL_STARTER, tests))
    assert (first.feedback_code, first.failed_test_id, first.tests_passed) == ("BLANKS_REMAINING", "blanks_remaining", 0)

    one_field = PLAIN_SQL_STARTER.replace("___", "customer_id", 1)
    second = run(grader.grade(one_field, tests))
    assert (second.feedback_code, second.failed_test_id) == ("BLANKS_REMAINING", "blanks_remaining")

    # Every blank filled but one wrong: the field is named once the result disagrees.
    wrong = one_field.replace("___", "SUM(customer_id)", 1)
    third = run(grader.grade(wrong, tests))
    assert (third.feedback_code, third.failed_test_id) == ("BLANK_INCORRECT", "blank_2")

    solution = one_field.replace("___", "count(*)", 1)
    result = run(grader.grade(solution, tests))
    assert result.passed
    assert result.execution.stdout == "customer_id\torders\n1\t2\n2\t1\n"


def test_sql_blank_values_ignore_commas_inside_answers_and_whitespace_changes():
    template = "SELECT ___, ___ AS n\nFROM t\nWHERE x IN (___)\nGROUP BY ___;"
    code = "SELECT  COALESCE(a, ',') ,  COUNT(*) AS n FROM t WHERE x IN ('a', 'b, c') GROUP BY a;"
    values = sql_blank_values(template, code)
    assert [value.strip() for value in values] == ["COALESCE(a, ',')", "COUNT(*)", "'a', 'b, c'", "a"]
    # Blanks separated only by a line break split at that break.
    window = "OVER (\n    ___\n    ___\n)"
    filled = "OVER (\n    ORDER BY m\n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n)"
    assert [value.strip() for value in sql_blank_values(window, filled)] == [
        "ORDER BY m", "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW",
    ]
    # Rewritten scaffold: the blanks can no longer be told apart.
    assert sql_blank_values(template, "SELECT a, COUNT(*) AS total FROM t GROUP BY a;") is None


def test_sql_grader_falls_back_to_the_result_when_the_scaffold_was_rewritten():
    tests = _sql_blank_tests(PLAIN_SQL_STARTER)
    grader = SQLGrader()
    rewritten = "SELECT customer_id, COUNT(*) AS orders FROM purchases GROUP BY 1 ORDER BY 1"
    assert run(grader.grade(rewritten, tests)).passed
    wrong = "SELECT customer_id, 0 AS orders FROM purchases GROUP BY 1 ORDER BY 1"
    failure = run(grader.grade(wrong, tests))
    assert (failure.feedback_code, failure.failed_test_id) == ("TEST_FAILED", "result")


def test_a_like_pattern_of_underscores_is_a_pattern_not_an_unfinished_blank():
    tests = _sql_blank_tests(PLAIN_SQL_STARTER)
    grader = SQLGrader()
    # Rewritten scaffold: the result decides, and '___' is a three-character LIKE pattern.
    rewritten = ("SELECT customer_id, COUNT(*) AS orders FROM purchases "
                 "WHERE 'abc' LIKE '___' GROUP BY 1 ORDER BY 1")
    assert sql_blanks_remaining(rewritten) == (0, None)
    assert run(grader.grade(rewritten, tests)).passed
    # The same pattern inside a blank of the real starter.
    filled = PLAIN_SQL_STARTER.replace("___", "customer_id", 1).replace(
        "___", "COUNT(CASE WHEN 'abc' LIKE '___' THEN 1 END)", 1)
    assert run(grader.grade(filled, tests)).passed


def test_sql_grader_still_reads_drafts_from_marked_starters():
    """Learners may hold drafts of the older starters that marked each blank."""
    starter = (
        "SELECT /* blank:1 */ ___ /* endblank */ AS customer_id, "
        "/* blank:2 */ ___ /* endblank */ AS orders "
        "FROM purchases GROUP BY customer_id ORDER BY customer_id;"
    )
    tests = _sql_blank_tests(PLAIN_SQL_STARTER)
    grader = SQLGrader()
    one_field = starter.replace("___", "customer_id", 1)
    assert run(grader.grade(one_field, tests)).feedback_code == "BLANKS_REMAINING"   # blank 2 is still empty
    wrong = one_field.replace("___", "SUM(customer_id)", 1)
    assert run(grader.grade(wrong, tests)).failed_test_id == "blank_2"               # the marked field is still read
    assert run(grader.grade(one_field.replace("___", "count(*)", 1), tests)).passed


def test_sql_grader_checks_fields_individually_then_hidden_result():
    starter = (
        "SELECT /* blank:1 */ ___ /* endblank */ AS customer_id, "
        "/* blank:2 */ ___ /* endblank */ AS orders "
        "FROM purchases GROUP BY customer_id ORDER BY customer_id;"
    )
    tests = [
        {
            "id": "blank_1", "type": "sql_blank", "blank": 1,
            "accepted": ["customer_id"],
            "feedback": {"en": "Blank 1: select the customer.", "ar": "الفراغ 1: اختر العميل."},
        },
        {
            "id": "blank_2", "type": "sql_blank", "blank": 2,
            "accepted": ["COUNT(*)", "count(1)"],
            "feedback": {"en": "Blank 2: count the rows.", "ar": "الفراغ 2: عد الصفوف."},
        },
        {
            "id": "result", "type": "sql_result",
            "setup_sql": (
                "CREATE TABLE purchases(customer_id INTEGER);"
                "INSERT INTO purchases VALUES (1),(1),(2);"
            ),
            "expected_columns": ["customer_id", "orders"],
            "expected_rows": [[1, 2], [2, 1]], "ordered": True,
            "feedback": {"en": "Check the result.", "ar": "راجع النتيجة."},
        },
    ]
    grader = SQLGrader()

    # Empty or partly filled: unfinished, reported without running the query.
    first = run(grader.grade(starter, tests))
    assert (first.passed, first.feedback_code, first.failed_test_id) == (False, "BLANKS_REMAINING", "blanks_remaining")
    assert first.feedback["en"].startswith("2 blanks (`___`) are still empty.")
    assert (first.execution.stdout, first.execution.stderr) == ("", "")

    one_field = starter.replace("___", "customer_id", 1)
    second = run(grader.grade(one_field, tests))
    assert (second.feedback_code, second.failed_test_id) == ("BLANKS_REMAINING", "blanks_remaining")
    assert second.feedback["en"].startswith("One blank (`___`) is still empty.")
    assert "near" not in second.feedback["en"] and second.execution.stderr == ""

    # A marked field emptied out is still a blank, even with no ___ left.
    emptied = one_field.replace("/* blank:2 */ ___ /* endblank */", "/* blank:2 */  /* endblank */")
    assert run(grader.grade(emptied, tests)).feedback_code == "BLANKS_REMAINING"

    # Every field filled: the query runs, and the first wrong field is named.
    wrong = one_field.replace("___", "SUM(customer_id)", 1)
    third = run(grader.grade(wrong, tests))
    assert (third.feedback_code, third.failed_test_id, third.tests_passed) == ("BLANK_INCORRECT", "blank_2", 1)
    assert third.execution.stdout.startswith("customer_id\torders\n")

    solution = one_field.replace("___", "count(*)", 1)
    result = run(grader.grade(solution, tests))
    assert result.passed
    assert result.execution.stdout == "customer_id\torders\n1\t2\n2\t1\n"


def test_sql_blanks_remaining_counts_unfilled_fields_not_literals_or_comments():
    marked = (
        "SELECT\n"
        "    /* blank:1 */ ___ /* endblank */ AS customer_id,\n"
        "    /* blank:2 */ ___ /* endblank */ AS orders\n"
        "FROM purchases;"
    )
    assert sql_blanks_remaining(marked) == (2, 2)
    assert sql_blanks_remaining(marked.replace("___", "customer_id", 1)) == (1, 3)
    # Markers deleted, placeholder kept; a placeholder inside an expression.
    assert sql_blanks_remaining("SELECT ___ FROM purchases") == (1, 1)
    assert sql_blanks_remaining("SELECT\n  COUNT(___)\nFROM purchases") == (1, 2)
    # An emptied marked field counts once, not twice.
    assert sql_blanks_remaining("SELECT /* blank:1 */ /* endblank */ FROM t") == (1, 1)
    # Underscores the learner wrote on purpose are not blanks.
    finished = (
        "SELECT name FROM t -- replace ___ later\n"
        "WHERE code LIKE '___' AND note <> 'it''s ___' AND \"___\" IS NOT NULL\n"
        "/* ___ */ AND my___col = 1"
    )
    assert sql_blanks_remaining(finished) == (0, None)
    assert sql_blanks_remaining("") == (0, None)


def test_sql_grader_rejects_writes_and_multiple_statements():
    tests = [{
        "id": "result", "type": "sql_result",
        "setup_sql": "CREATE TABLE records(value INTEGER); INSERT INTO records VALUES (1);",
        "expected_rows": [[1]], "feedback": "Use a read-only query.",
    }]
    grader = SQLGrader()

    write = run(grader.grade("DELETE FROM records", tests))
    assert write.status == "forbidden_operation"

    # Two queries are not a syntax error: the answer breaks the one-query rule.
    multiple = run(grader.grade("SELECT value FROM records; SELECT 2", tests))
    assert multiple.status == "forbidden_operation"
    assert "Only one read-only SELECT" in multiple.feedback["en"]
    assert "استعلام قراءة واحد" in multiple.feedback["ar"]
