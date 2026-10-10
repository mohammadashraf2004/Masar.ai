"""Grading rules added by the 2026-10-10 grading audit, tested without a
database: tolerant comparison, expected errors, configuration errors,
partial credit, the hardcoded-blank guard, keyword-order freedom for static
blanks, SQL classification and comparison, and withheld feedback.

Execution goes through LocalPythonRunner, which is the production driver and
runner harness in a child process (see isolated_python_runner.py).
"""
import ast
import asyncio

import pytest

from app.services.code_execution import ExecutionResult, LocalPythonRunner
from app.services.code_exercises import reveals_answer, withhold_answers
from app.services.code_grading import PythonGrader, SQLGrader
from app.services.code_grading.blanks import blank_is_computed, canonical_dump, computed_blank_tests
from app.services.code_grading.grader import grading_test_problems, values_match
from app.services.code_grading.sql_grader import rows_match

GRADER = PythonGrader(LocalPythonRunner(timeout_seconds=10))


def grade(code, tests, grader=GRADER, **kwargs):
    return asyncio.run(grader.grade(code, tests, **kwargs))


def check(expression, expected=None, raises=None, **extra):
    test = {"type": "expression_equals", "expression": expression, "feedback": {"en": expression, "ar": expression}}
    if raises is not None:
        test["raises"] = raises
    else:
        test["expected"] = expected
    test.update(extra)
    return test


# ─── Comparison ─────────────────────────────────────────────────────────────

def test_floats_compare_within_tolerance_everywhere_in_a_value():
    assert values_match(sum([0.1] * 10), 1.0)
    assert values_match({"result": 7.5 * (1 / 2.5)}, {"result": 3.0})
    assert values_match([[0.30000000000000004, "x"]], [[0.3, "x"]])
    assert not values_match(0.1349, 0.135)
    assert not values_match(18022401.0, 18022400)
    # Integers, strings and booleans keep plain equality.
    assert not values_match(2, 3) and not values_match("a", "A")
    assert values_match(True, 1) == (True == 1)  # noqa: E712 - Python semantics are kept
    assert not values_match({"a": 1}, {"a": 1, "b": 2})


def test_an_equivalent_float_computation_passes_a_value_check():
    tests = [{"id": "mean", "type": "value_equals", "variable": "mean", "expected": 1.0,
              "feedback": "Check the mean."}]
    looped = "values = [0.1] * 10\nmean = 0.0\nfor v in values:\n    mean += v\n"
    assert grade(looped, tests).passed


# ─── Expected errors ────────────────────────────────────────────────────────

def test_a_check_can_require_a_specific_exception():
    tests = [check("safe_sqrt(-1)", raises="ValueError"), check("safe_sqrt(9)", 3.0)]
    raising = "def safe_sqrt(x):\n    if x < 0:\n        raise ValueError('negative')\n    return x ** 0.5\n"
    assert grade(raising, tests).passed
    silent = "def safe_sqrt(x):\n    return abs(x) ** 0.5\n"
    result = grade(silent, tests)
    assert (result.passed, result.failed_test_id, result.tests_passed) == (False, "test_1", 1)
    wrong_type = "def safe_sqrt(x):\n    if x < 0:\n        raise TypeError('negative')\n    return x ** 0.5\n"
    assert not grade(wrong_type, tests).passed


def test_returning_a_lookalike_error_value_does_not_count_as_raising():
    tests = [check("divide(1, 0)", raises="ZeroDivisionError")]
    forged = "def divide(a, b):\n    return {'__masar_call_error__': 'ZeroDivisionError'}\n"
    assert not grade(forged, tests).passed
    honest = "def divide(a, b):\n    return a / b\n"
    assert grade(honest, tests).passed


def test_an_unexpected_exception_in_a_value_check_fails_it():
    result = grade("def f(x):\n    return 1 / x\n", [check("f(0)", 0)])
    assert not result.passed and result.failed_test_id == "test_1"


# ─── Configuration errors are never a learner's wrong answer ───────────────

@pytest.mark.parametrize("tests, fragment", [
    ([{"type": "value_equal", "variable": "x", "expected": 1}], "unsupported type"),
    ([{"type": "value_equals", "expected": 1}], "variable name"),
    ([{"type": "expression_equals", "expression": "x +", "expected": 1}], "does not parse"),
    ([{"type": "expression_equals", "expression": "x"}], "expected value or raises"),
    ([{"type": "custom", "checker": "nope"}], "custom checker"),
    ([{"type": "value_approx", "variable": "x", "expected": "abc"}], "number"),
])
def test_malformed_tests_are_a_grading_error_not_incorrect(tests, fragment):
    assert any(fragment in problem for problem in grading_test_problems(tests))
    result = grade("x = 1\n", tests)
    assert (result.status, result.passed, result.feedback_code) == ("grading_error", False, "INVALID_TEST_CONFIGURATION")
    assert "not counted" in result.feedback["en"] and "لم تُحتسب" in result.feedback["ar"]


def test_a_check_that_the_runner_refuses_is_a_grading_error():
    result = grade("x = 1\n", [check("open('x')", 1)])
    assert result.status == "grading_error"


# ─── Partial credit and ordering ────────────────────────────────────────────

def test_every_required_check_is_counted_and_partial_is_its_own_status():
    tests = [check("a", 1), check("b", 2), check("c", 3)]
    result = grade("a, b, c = 1, 0, 3\n", tests)
    assert (result.status, result.tests_passed, result.tests_total, result.failed_test_id) == ("partial", 2, 3, "test_2")
    assert grade("a, b, c = 0, 0, 0\n", tests).status == "incorrect"
    assert grade("a, b, c = 1, 2, 3\n", tests).status == "correct"


def test_a_crash_still_reports_the_check_that_explains_it():
    tests = [
        check("ratio(1, 0)", {"error": "zero"}, feedback={"en": "ratio must refuse a zero divisor.", "ar": "يجب أن ترفض ratio المقسوم عليه الصفري."}),
        check("ratio(6, 3)", {"result": 2.0}),
    ]
    code = "def ratio(a, b):\n    if a == 0:\n        return {'error': 'zero'}\n    return {'result': a / b}\n\nprint(ratio(1, 0))\n"
    result = grade(code, tests)
    assert result.status == "runtime_error" and not result.passed
    assert result.failed_test_id == "test_1"
    assert result.feedback["en"] == "ratio must refuse a zero divisor."
    # The innermost learner frame: where the division failed.
    assert "ZeroDivisionError" in result.notice["en"] and "line 4" in result.notice["en"]
    assert "السطر 4" in result.notice["ar"]
    assert 'File "exercise.py", line 6' in result.execution.stderr  # the learner's own line numbers


def test_a_crash_with_every_check_passing_is_still_a_runtime_error():
    code = "def double(x):\n    return 2 * x\n\nraise RuntimeError('demo line')\n"
    result = grade(code, [check("double(4)", 8)])
    assert (result.status, result.passed, result.tests_passed) == ("runtime_error", False, 1)


def test_setup_code_does_not_shift_learner_line_numbers():
    result = grade("x = 1\ny = missing\n", [check("x", 1)], pre_exercise_code="a = 1\nb = 2\nc = 3\n")
    assert result.status == "runtime_error"
    assert 'File "exercise.py", line 2' in result.execution.stderr


# ─── The learner cannot see or disturb the hidden checks ───────────────────

def test_output_printed_while_hidden_checks_run_is_not_shown():
    code = "def area(w, h):\n    print('called with', w, h)\n    return w * h\n\nprint(area(2, 3))\n"
    result = grade(code, [check("area(17, 23)", 391)])
    assert result.passed
    assert "17" not in result.execution.stdout and "23" not in result.execution.stdout
    assert result.execution.stdout == "called with 2 3\n6\n"


def test_a_variable_named_like_a_builtin_does_not_break_a_check():
    tests = [check("sorted(names)", ["a", "b"]), check("round(score, 1)", 0.3)]
    code = "names = ['b', 'a']\nscore = 0.25 + 0.05\nsorted = 'alphabetical'\nround = 2\n"
    assert grade(code, tests).passed


def test_a_type_check_sees_an_objects_real_type():
    tests = [{"type": "type_equals", "variable": "item", "expected": "Point", "feedback": "Make a Point."}]
    code = "class Point:\n    pass\n\nitem = Point()\n"
    assert grade(code, tests).passed


def test_more_observations_than_the_runner_captures_is_a_configuration_error():
    tests = [check(str(index), index) for index in range(18)]
    result = grade("x = 1\n", tests)
    assert result.status == "grading_error"


# ─── Hardcoded blanks ───────────────────────────────────────────────────────

STARTER = "tp, fp = 3, 1\nprecision = ___\nlabel = 'ok'\n"


def test_computed_blank_guard_rejects_a_typed_result_only():
    [guard] = computed_blank_tests(STARTER, ("tp / (tp + fp)",), [{"en": "Blank 1", "ar": "الفراغ 1"}])
    filled = lambda value: ast.parse(STARTER.replace("___", value))  # noqa: E731
    assert blank_is_computed(filled("tp / (tp + fp)"), guard)
    assert blank_is_computed(filled("tp / (fp + tp)"), guard)  # an equivalent expression
    assert not blank_is_computed(filled("0.75"), guard)
    assert not blank_is_computed(filled("3 / 4"), guard)  # computed by hand
    # A restructured program is never failed by the guard: behaviour decides.
    reshaped = ast.parse("tp, fp = 3, 1\nprint('x')\nprecision = 0.75\nlabel = 'ok'\n")
    assert blank_is_computed(reshaped, guard)


def test_no_guard_for_literal_answers_or_module_only_expressions():
    starter = "import math\nrequired = ___\nroot = ___\n"
    tests = computed_blank_tests(starter, ('["a", "b"]', "math.sqrt(2)"), [{"en": "1", "ar": "1"}, {"en": "2", "ar": "2"}])
    assert tests == []


def test_typing_the_sample_result_into_a_blank_is_rejected_end_to_end():
    from app.services.curriculum.guided import Guided, build, eq

    guided = Guided(
        goal=("g", "g"), steps=(("s", "s"),), hints=(("h", "h"),), success=("ok", "ok"),
        starter="partial, full = 1349, 10000\nshare = ___\n",
        answers=("round(partial / full, 4)",),
        checks=(eq("share", 0.1349, "Blank 1: divide partial by full.", "الفراغ 1: اقسم partial على full."),),
    )
    tests = build("TEST.HARDCODE", guided)["tests"]
    typed = grade("partial, full = 1349, 10000\nshare = 0.1349\n", tests)
    assert (typed.passed, typed.failed_test_id, typed.feedback_code) == (False, "blank_1_computed", "BLANK_HARDCODED")
    assert "instead of typing" in typed.feedback["en"]
    assert grade("partial, full = 1349, 10000\nshare = round(partial / full, 4)\n", tests).passed
    assert grade("partial, full = 1349, 10000\nshare = round(partial * 1.0 / full, 4)\n", tests).passed


def test_static_blanks_accept_keyword_arguments_in_any_order():
    from app.services.curriculum.guided import Guided, build

    guided = Guided(
        goal=("g", "g"), steps=(("s", "s"),), hints=(("h", "h"),), success=("ok", "ok"),
        starter="import plotly.express as px\nfig = ___\n",
        answers=('px.bar(df, x="product", y="sales")',),
        blanks=(("draw the bars", "ارسم الأعمدة"),),
    )
    tests = build("TEST.KEYWORDS", guided)["tests"]
    swapped = grade('import plotly.express as px\nfig = px.bar(df, y="sales", x="product")\n', tests)
    assert swapped.passed
    assert not grade('import plotly.express as px\nfig = px.bar(df, x="sales", y="product")\n', tests).passed
    assert canonical_dump(ast.parse("f(b=2, a=1)", mode="eval").body) == canonical_dump(ast.parse("f(a=1, b=2)", mode="eval").body)


# ─── Infrastructure failures ────────────────────────────────────────────────

class Unavailable:
    async def run(self, *args, **kwargs):
        return ExecutionResult("execution_error", stderr="The project runner is unavailable. Try again shortly.")


def test_an_unavailable_runner_is_never_a_wrong_answer():
    result = grade("x = 1\n", [check("x", 1)], grader=PythonGrader(Unavailable()))
    assert (result.status, result.passed, result.feedback_code) == ("execution_error", False, "EXECUTION_ERROR")
    assert "not graded" in result.feedback["en"]
    assert "بيئة التشغيل غير متاحة" in result.feedback["ar"] and "لن تُحتسب" in result.feedback["ar"]


def test_the_local_runner_refuses_to_run_in_production(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "APP_ENV", "production")
    result = asyncio.run(LocalPythonRunner().run("print('LEARNER CODE RAN')"))
    assert result.status == "execution_error" and "LEARNER CODE RAN" not in result.stdout


# ─── SQL ────────────────────────────────────────────────────────────────────

def sql_tests(rows, ordered=False):
    return [{
        "id": "result", "type": "sql_result",
        "setup_sql": "CREATE TABLE t(g TEXT, v REAL); INSERT INTO t VALUES ('a', 0.1),('a', 0.2),('b', 3);",
        "expected_columns": ["g", "total"], "expected_rows": rows, "ordered": ordered,
        "feedback": {"en": "Check the totals.", "ar": "راجع المجاميع."},
    }]


def test_sql_rows_compare_floats_within_tolerance_and_as_a_multiset():
    assert rows_match([(1, 0.30000000000000004)], [(1, 0.3)], ordered=True)
    assert rows_match([("b", 3.0), ("a", 2)], [("a", 2), ("b", 3)], ordered=False)
    assert not rows_match([("a", 2), ("a", 2)], [("a", 2), ("b", 2)], ordered=False)
    result = asyncio.run(SQLGrader().grade("SELECT g, SUM(v) AS total FROM t GROUP BY g", sql_tests([["b", 3], ["a", 0.3]])))
    assert result.passed


@pytest.mark.parametrize("query, status", [
    ("SELEC g FROM t", "syntax_error"),
    ("SELECT g, FROM t", "syntax_error"),
    ("SELECT nope AS total, g FROM t", "runtime_error"),
    ("DELETE FROM t", "forbidden_operation"),
    ("SELECT 1; SELECT 2", "forbidden_operation"),
    ("WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM n) SELECT COUNT(*) AS g, 1 AS total FROM n",
     "timeout"),
])
def test_sql_failures_are_classified_and_explained_in_both_languages(query, status):
    result = asyncio.run(SQLGrader().grade(query, sql_tests([["a", 1]])))
    assert result.status == status and not result.passed
    assert result.feedback["en"] and result.feedback["ar"] != result.feedback["en"]


# ─── Feedback that would give the answer away ───────────────────────────────

SOLUTION = 'def divide(a, b):\n    if b == 0:\n        return {"error": "zero"}\n    return {"result": a / b}\n'
STARTER_DIVIDE = 'def divide(a, b):\n    if ___:\n        return {"error": "zero"}\n    return ___\n'


def test_feedback_quoting_the_answer_is_detected():
    assert reveals_answer("Blank 2: check the divisor `b == 0`, not the dividend.", SOLUTION, STARTER_DIVIDE)
    assert reveals_answer('Blank 3: `{"result": a / b}`.', SOLUTION, STARTER_DIVIDE)
    # Code the learner already has is not part of the answer.
    assert not reveals_answer("Blank 2: `divide` must refuse a zero divisor.", SOLUTION, STARTER_DIVIDE)
    assert not reveals_answer("One blank (`___`) is still empty.", SOLUTION, STARTER_DIVIDE)


def test_withheld_feedback_still_names_the_blank_in_both_languages():
    messages = {"en": "Blank 2: check the divisor `b == 0`.", "ar": "الفراغ 2: افحص المقسوم عليه `b == 0`."}
    withheld, changed = withhold_answers(messages, solution=SOLUTION, starter=STARTER_DIVIDE, failed_test_id="check_2")
    assert changed
    assert withheld["en"].startswith("Blank 2 ") and "b == 0" not in withheld["en"]
    assert withheld["ar"].startswith("الفراغ 2 ") and "b == 0" not in withheld["ar"]
    plain = {"en": "Blank 2: `divide` must refuse a zero divisor.", "ar": "الفراغ 2: يجب أن ترفض `divide` الصفر."}
    assert withhold_answers(plain, solution=SOLUTION, starter=STARTER_DIVIDE, failed_test_id="check_2") == (plain, False)
