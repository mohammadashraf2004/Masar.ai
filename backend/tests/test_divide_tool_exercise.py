"""Regression suite for the divide-tool exercise (COURSE-015.M01.L01.EX01).

The exercise is graded exactly as in production: the guided definition is
built by the importer's own ``build`` and every submission runs through the
production driver and runner harness (LocalPythonRunner).
"""
import asyncio

import pytest

from app.services.code_execution import ExecutionResult, LocalPythonRunner
from app.services.code_grading import PythonGrader
from app.services.curriculum.guided import build, fill, registry

EXERCISE_ID = "COURSE-015.M01.L01.EX01"
GUIDED = registry()[EXERCISE_ID]
BUILT = build(EXERCISE_ID, GUIDED)
TESTS = BUILT["tests"]
GRADER = PythonGrader(LocalPythonRunner(timeout_seconds=10))


def submit(code, grader=GRADER):
    return asyncio.run(grader.grade(code, TESTS))


def with_blanks(**replacements):
    """The official solution with some blanks (1-4) answered differently."""
    answers = list(GUIDED.answers)
    for name, value in replacements.items():
        answers[int(name[1:]) - 1] = value
    return fill(GUIDED.starter, tuple(answers))


SOLUTION = BUILT["solution_code"]


def test_the_official_solution_passes_every_check():
    result = submit(SOLUTION)
    assert (result.status, result.passed) == ("correct", True)
    # The hardcoding guards gate a pass but are not counted as checks.
    counted = [test for test in TESTS if test["type"] != "blank_computed"]
    assert result.tests_passed == result.tests_total == len(counted) == 6
    assert result.execution.stdout == "{'result': 2.5} {'error': 'b must not be zero'}\n"


def test_correct_division_ten_by_four_is_two_and_a_half():
    assert submit(SOLUTION).passed
    check = next(test for test in TESTS if "divide(10, 4)" in test.get("expression", ""))
    assert check["expected"][0] == {"result": 2.5}


def test_a_wrong_zero_divisor_condition_explains_the_zero_divisor_not_a_bare_crash():
    result = submit(with_blanks(b2="a == 0"))
    assert (result.status, result.passed, result.failed_test_id) == ("runtime_error", False, "check_2")
    assert "does not handle a zero divisor safely" in result.feedback["en"]
    assert "لا تتعامل `divide` بأمان مع مقسوم عليه يساوي صفرًا" in result.feedback["ar"]
    # The crash in the demo line is still reported, after the explanation.
    assert "ZeroDivisionError" in result.notice["en"] and "ZeroDivisionError" in result.notice["ar"]


@pytest.mark.parametrize("implementation", [
    '{"result": abs(a) / abs(b)}',        # negative inputs lose their sign
    '{"result": int(a) / int(b)}',        # fractional inputs truncated
    '{"result": a // b}',                 # floor division
    '{"result": b / a}',                  # operands swapped
])
def test_negative_fractional_and_wrong_implementations_fail_blank_three(implementation):
    result = submit(with_blanks(b3=implementation))
    assert not result.passed
    assert result.failed_test_id == "check_3"
    assert result.feedback["en"].startswith("Blank 3:")


def test_a_zero_dividend_is_valid_and_rejecting_it_names_blank_two():
    result = submit(with_blanks(b2="a == 0 or b == 0"))
    assert (result.passed, result.failed_test_id, result.status) == (False, "check_4", "partial")
    assert "zero dividend is valid" in result.feedback["en"]


def test_an_unknown_tool_name_must_still_be_refused():
    no_name_check = SOLUTION.replace('if call["name"] != divide_declaration["name"]:', "if False:")
    result = submit(no_name_check)
    assert not result.passed and result.failed_test_id == "check_6"
    assert "refuse a tool" in result.feedback["en"]


def test_the_declaration_must_require_both_arguments():
    result = submit(with_blanks(b1='["a"]'))
    assert (result.passed, result.failed_test_id) == (False, "check_1")
    assert "both of them" in result.feedback["en"]


@pytest.mark.parametrize("execute", [
    'divide(**call["args"])',                                  # missing args raise TypeError
    'divide(call["args"].get("a"), call["args"].get("b"))',    # ... or a TypeError on None
])
def test_missing_arguments_are_not_part_of_the_specification(execute):
    # The brief makes the MODEL supply both arguments (blank 1); the host is
    # not asked to validate a call without them, so either behaviour passes.
    assert submit(with_blanks(b4=execute)).passed


def test_hardcoding_the_sample_output_fails_on_unseen_inputs():
    result = submit(with_blanks(b3='{"result": 2.5}'))
    assert (result.passed, result.failed_test_id) == (False, "check_3")
    assert "a fixed value only matches one example" in result.feedback["en"]
    # The guard for typed-in results agrees independently.
    import ast

    from app.services.code_grading.blanks import blank_is_computed

    guard = next(test for test in TESTS if test["id"] == "blank_3_computed")
    assert not blank_is_computed(ast.parse(with_blanks(b3='{"result": 2.5}')), guard)
    assert blank_is_computed(ast.parse(SOLUTION), guard)


def test_a_lookup_table_of_the_examples_is_still_rejected():
    table = '{"result": {(10, 4): 2.5, (9, 3): 3.0}.get((a, b), 0)}'
    result = submit(with_blanks(b3=table))
    assert not result.passed and result.failed_test_id == "check_3"


def test_a_syntax_error_is_reported_as_such():
    result = submit(SOLUTION.replace("def divide(a, b):", "def divide(a, b)"))
    assert (result.status, result.feedback_code) == ("syntax_error", "SYNTAX_ERROR")
    assert "syntax error" in result.feedback["en"]


def test_a_runtime_error_in_blank_four_points_at_blank_four():
    result = submit(with_blanks(b4='divide(call["args"])'))
    assert result.status == "runtime_error" and result.failed_test_id == "check_5"
    assert result.feedback["en"].startswith("Blank 4:")
    assert "TypeError" in result.notice["en"]


@pytest.mark.parametrize("b1, b2, b3, b4", [
    ('["b", "a"]', "not b", 'dict(result=a / b)', 'divide(call["args"]["a"], call["args"]["b"])'),
    ('list("ab")', "b == 0.0", '{"result": a * (1 / b)}', 'divide(**call.get("args", {}))'),
    ('["a", "b"]', "0 == b", '{"result": float(a) / b}', 'divide(*call["args"].values())'),
])
def test_equivalent_correct_solutions_pass(b1, b2, b3, b4):
    result = submit(with_blanks(b1=b1, b2=b2, b3=b3, b4=b4))
    assert result.passed, (result.failed_test_id, result.feedback)


def test_hidden_inputs_never_reach_the_learner():
    chatty = SOLUTION.replace("def divide(a, b):\n", "def divide(a, b):\n    print('divide', a, b)\n")
    result = submit(chatty)
    assert result.passed
    for hidden in ("-9 2", "7.5 2.5", "-6 -4", "0 5", "9 3"):
        assert f"divide {hidden}" not in result.execution.stdout


def test_repeated_submissions_are_graded_identically():
    variants = [SOLUTION, with_blanks(b2="a == 0"), with_blanks(b3='{"result": 2.5}')]
    first = [submit(code) for code in variants]
    again = [submit(code) for code in variants]
    summary = lambda r: (r.status, r.passed, r.failed_test_id, r.tests_passed, r.tests_total, r.feedback)  # noqa: E731
    assert [summary(r) for r in first] == [summary(r) for r in again]


def test_concurrent_submissions_do_not_affect_each_other():
    variants = [SOLUTION, with_blanks(b2="a == 0"), with_blanks(b3='{"result": 2.5}'), with_blanks(b1='["a"]')]

    async def together():
        return await asyncio.gather(*(GRADER.grade(code, TESTS) for code in variants))

    concurrent = asyncio.run(together())
    sequential = [submit(code) for code in variants]
    assert [(r.status, r.failed_test_id, r.tests_passed) for r in concurrent] == \
        [(r.status, r.failed_test_id, r.tests_passed) for r in sequential]


def test_a_failed_grader_is_not_a_wrong_answer():
    class Broken:
        async def run(self, *args, **kwargs):
            return ExecutionResult("execution_error", stderr="The project runner failed.")

    result = submit(SOLUTION, grader=PythonGrader(Broken()))
    assert (result.status, result.passed, result.feedback_code) == ("execution_error", False, "EXECUTION_ERROR")
    assert "not graded" in result.feedback["en"]


def test_no_check_feedback_quotes_the_answer():
    from app.services.code_exercises import reveals_answer

    for test in TESTS:
        for language in ("en", "ar"):
            assert not reveals_answer(test["feedback"][language], SOLUTION, BUILT["starter_code"]), test["id"]
