"""Ordered deterministic Python grading.

Every required test is evaluated, so ``tests_passed`` says how much of the
exercise works; the feedback names the first failing test in authored order.
A submission is ``correct`` when every required test passes, ``partial`` when
some do, ``incorrect`` when none do. Failures that are not the learner's
answer at all - the runner unavailable (``execution_error``) or a broken
exercise definition (``grading_error``) - are reported as such and never as a
wrong answer.
"""
from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass
from typing import Any

from app.services.code_execution import CodeRunner, ExecutionResult, IsolatedPythonRunner
from app.services.code_execution.messages import platform_message
from app.services.code_execution.python_runner import parse_learner_python
from .authoring import (
    ast_fingerprint, ast_requirements, ast_satisfies, count_python_blanks, placeholders_are_removed,
)
from .blanks import blank_is_computed, canonical_dump
from .custom import CUSTOM_TESTS


SUPPORTED_TEST_TYPES = frozenset({
    "variable_exists", "variable_not_exists", "value_equals", "value_approx", "type_equals",
    "function_called", "function_not_called", "function_argument", "function_call_count",
    "expression_uses", "operator_used", "stdout_equals", "stdout_contains",
    "list_length", "dict_contains_key", "dataframe_exists", "dataframe_columns",
    "dataframe_shape", "dataframe_column_values", "return_value_equals", "expression_equals",
    "function_exists", "custom",
    "code_changed", "placeholders_removed", "ast_requirements", "ast_contains", "blank_computed",
})

STATIC_TEST_TYPES = frozenset({
    "function_called", "function_not_called", "function_argument", "function_call_count",
    "expression_uses", "operator_used", "function_exists",
    "code_changed", "placeholders_removed", "ast_requirements", "ast_contains", "blank_computed",
})

_VARIABLE_TESTS = frozenset({
    "variable_exists", "variable_not_exists", "value_equals", "value_approx", "type_equals",
    "list_length", "dict_contains_key", "dataframe_exists", "dataframe_columns",
    "dataframe_shape", "dataframe_column_values",
})
# Results that say nothing about the learner's answer.
UNGRADED_STATUSES = frozenset({"execution_error", "grading_error"})
# Default tolerance for comparing floats: equivalent computations that differ
# only in the last bits of a float (``a * (1 / b)`` vs ``a / b``) are equal.
DEFAULT_REL_TOL = 1e-9
DEFAULT_ABS_TOL = 1e-12


def is_static_only(tests: list[dict[str, Any]]) -> bool:
    """True when every required test reads the program's structure, so the
    exercise is graded without executing it (its libraries are not installed
    in the restricted runner)."""
    required = [test for test in tests if test.get("required", True)]
    return bool(required) and all(
        bool(test.get("static")) and test.get("type") in STATIC_TEST_TYPES
        for test in required
    )


def first_blank_line(code: str) -> int | None:
    try:
        tree = parse_learner_python(code or "")
    except SyntaxError:
        return None
    lines = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Name) and node.id == "___"]
    return min(lines) if lines else None


def blanks_remaining_feedback(count: int, line: int | None = None) -> dict[str, str]:
    where_en = f" The first one is on line {line}." if line else ""
    where_ar = f" أولها في السطر {line}." if line else ""
    if count == 1:
        return {
            "en": f"One blank (`___`) is still empty.{where_en} Fill it in, then check your answer again.",
            "ar": f"ما زال هناك فراغ واحد (`___`) لم يُملأ.{where_ar} أكمله ثم تحقّق من إجابتك مرة أخرى.",
        }
    en = f"{count} blanks (`___`) are still empty.{where_en} Fill them in, then check your answer again."
    # Arabic counts agree with the number: a dual for two, a plural for 3-10,
    # a singular (accusative) noun from 11 on.
    if count == 2:
        where_dual = f" أولهما في السطر {line}." if line else ""
        return {"en": en, "ar": f"ما زال هناك فراغان (`___`) لم يُملآ.{where_dual} أكملهما ثم تحقّق من إجابتك مرة أخرى."}
    noun = "فراغات" if count <= 10 else "فراغًا"
    return {"en": en, "ar": f"ما زالت هناك {count} {noun} (`___`) لم تُملأ.{where_ar} أكملها ثم تحقّق من إجابتك مرة أخرى."}


# ─── Configuration ─────────────────────────────────────────────────────────

def _identifier(value: Any) -> bool:
    return isinstance(value, str) and value.isidentifier()


def _raises_names(test: dict[str, Any]) -> list[str] | None:
    """The exception names a check expects, or None when it expects a value."""
    raises = test.get("raises")
    if raises is None:
        return None
    names = [raises] if isinstance(raises, str) else list(raises) if isinstance(raises, (list, tuple)) else []
    return [str(name) for name in names]


def grading_test_problems(tests: Any) -> list[str]:
    """What is wrong with an exercise's Python tests, before anything runs.

    A malformed test can never pass, so without this check a typo in an
    exercise definition fails every learner as "incorrect". The importer
    refuses such definitions; the grader reports them as a grading error.
    """
    if not isinstance(tests, list):
        return ["tests must be a list"]
    problems: list[str] = []
    for index, test in enumerate(tests, start=1):
        where = f"test {index}"
        if not isinstance(test, dict):
            problems.append(f"{where}: not an object")
            continue
        kind = test.get("type")
        where = f"test {index} ({test.get('id') or kind})"
        if kind not in SUPPORTED_TEST_TYPES:
            problems.append(f"{where}: unsupported type {kind!r}")
            continue
        if kind in _VARIABLE_TESTS and not _identifier(test.get("variable")):
            problems.append(f"{where}: needs a variable name")
        if kind == "value_approx":
            try:
                float(test.get("expected"))
            except (TypeError, ValueError):
                problems.append(f"{where}: expected must be a number")
        if kind in {"function_called", "function_not_called", "function_argument",
                    "function_call_count", "function_exists"} and not str(test.get("function") or "").strip():
            problems.append(f"{where}: needs a function name")
        if kind == "return_value_equals":
            if not _identifier(test.get("function")):
                problems.append(f"{where}: needs a function name")
            if not isinstance(test.get("args", []), list) or not isinstance(test.get("kwargs", {}), dict):
                problems.append(f"{where}: args must be a list and kwargs an object")
        if kind == "expression_equals":
            try:
                ast.parse(str(test.get("expression") or ""), mode="eval")
            except SyntaxError:
                problems.append(f"{where}: expression does not parse")
            if not str(test.get("expression") or "").strip():
                problems.append(f"{where}: needs an expression")
        if kind in {"return_value_equals", "expression_equals"}:
            names = _raises_names(test)
            if names is not None and (not names or not all(name.isidentifier() for name in names)):
                problems.append(f"{where}: raises must name exception classes")
            if names is None and "expected" not in test:
                problems.append(f"{where}: needs an expected value or raises")
        if kind == "custom" and str(test.get("checker") or "") not in CUSTOM_TESTS:
            problems.append(f"{where}: unknown custom checker {test.get('checker')!r}")
        if kind == "ast_contains" and not (test.get("expected_ast") or test.get("expected_ast_any")):
            problems.append(f"{where}: needs expected_ast")
        if kind == "blank_computed" and not (
            isinstance(test.get("path"), list) and isinstance(test.get("statement"), list)
            and isinstance(test.get("slots"), list) and isinstance(test.get("context"), str)
        ):
            problems.append(f"{where}: needs path, statement, slots and context")
        for key in ("rel_tol", "abs_tol"):
            if key in test:
                try:
                    if float(test[key]) < 0:
                        raise ValueError
                except (TypeError, ValueError):
                    problems.append(f"{where}: {key} must be a non-negative number")
    return problems


# ─── Comparing observed values ─────────────────────────────────────────────

def values_match(actual: Any, expected: Any, *, rel_tol: float = DEFAULT_REL_TOL,
                 abs_tol: float = DEFAULT_ABS_TOL) -> bool:
    """Python equality, except that floats (anywhere inside lists and dicts)
    compare within a tolerance."""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual == expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if isinstance(actual, float) or isinstance(expected, float):
            if math.isnan(float(actual)) or math.isnan(float(expected)):
                return math.isnan(float(actual)) and math.isnan(float(expected))
            return math.isclose(float(actual), float(expected), rel_tol=rel_tol, abs_tol=abs_tol)
        return actual == expected
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            values_match(a, e, rel_tol=rel_tol, abs_tol=abs_tol) for a, e in zip(actual, expected)
        )
    if isinstance(actual, dict) and isinstance(expected, dict):
        if set(map(str, actual)) != set(map(str, expected)):
            return False
        plain = {str(key): value for key, value in actual.items()}
        return all(
            values_match(plain[str(key)], value, rel_tol=rel_tol, abs_tol=abs_tol)
            for key, value in expected.items()
        )
    return actual == expected


def _tolerances(test: dict[str, Any]) -> dict[str, float]:
    return {
        "rel_tol": float(test.get("rel_tol", DEFAULT_REL_TOL)),
        "abs_tol": float(test.get("abs_tol", DEFAULT_ABS_TOL)),
    }


# ─── Feedback ──────────────────────────────────────────────────────────────

_FORBIDDEN_AR = (
    (re.compile(r"^Importing '(.+)' is not allowed in exercises\.$"), "استيراد '{0}' غير مسموح في التمارين."),
    (re.compile(r"^Calling '(.+)' is not allowed in exercises\.$"), "استدعاء '{0}' غير مسموح في التمارين."),
    (re.compile(r"^Using '(.+)' is not allowed in exercises\.$"), "استخدام '{0}' غير مسموح في التمارين."),
    (re.compile(r"^Attribute '(.+)' is not allowed in exercises\.$"), "الخاصية '{0}' غير مسموحة في التمارين."),
    (re.compile(r"^Private attribute access is not allowed in exercises\.$"), "الوصول إلى الخصائص الخاصة غير مسموح في التمارين."),
)


def forbidden_message_ar(text: str) -> str:
    for pattern, arabic in _FORBIDDEN_AR:
        match = pattern.match(text.strip())
        if match:
            return arabic.format(*match.groups())
    return text


def _where(execution: ExecutionResult, *, ar: bool) -> str:
    line = (execution.error or {}).get("line")
    if not isinstance(line, int):
        return ""
    return f" في السطر {line}" if ar else f" on line {line}"


def _error_name(execution: ExecutionResult) -> str:
    name = str((execution.error or {}).get("type") or "")
    if name:
        return name
    lines = [line for line in (execution.stderr or "").strip().splitlines() if line.strip()]
    last = lines[-1].strip() if lines else ""
    return last.split(":", 1)[0] if re.match(r"^[A-Za-z_][\w.]*(Error|Exception|Exit|Interrupt)\b", last) else ""


def execution_failure_feedback(execution: ExecutionResult) -> dict[str, str]:
    """Name the kind of failure in the learner's language. The console keeps
    the raw traceback; the feedback says what happened and where."""
    status = execution.status
    if status == "timeout":
        return {
            "en": "Your code took too long and was stopped. Look for a loop that never ends or work on a smaller sample.",
            "ar": "استغرق الكود وقتًا طويلًا فأُوقف. ابحث عن حلقة لا تنتهي أو اعمل على عينة أصغر.",
        }
    if status == "memory_limit":
        return {
            "en": "Your code used more memory than the practice sandbox allows and was stopped. "
                  "Look for data that keeps growing, or work on a smaller sample.",
            "ar": "استخدم الكود ذاكرة أكثر مما تسمح به بيئة التدريب فأُوقف. "
                  "ابحث عن بيانات تكبر باستمرار، أو اعمل على عينة أصغر.",
        }
    if status == "output_limit":
        return {
            "en": "Your code printed more output than the practice sandbox allows. Print a summary instead of every value.",
            "ar": "طبع الكود مخرجات أكثر مما تسمح به بيئة التدريب. اطبع ملخصًا بدلًا من كل قيمة.",
        }
    if status == "forbidden_operation":
        detail = (execution.stderr or "").strip()
        return {
            "en": f"This operation is not available in the practice sandbox. {detail}".strip(),
            "ar": f"هذه العملية غير متاحة في بيئة التدريب. {forbidden_message_ar(detail)}".strip(),
        }
    if status == "syntax_error":
        message = str((execution.error or {}).get("message") or "")
        if not message:
            lines = [line for line in (execution.stderr or "").strip().splitlines() if line.strip()]
            message = lines[-1].strip() if lines else ""
        return {
            "en": f"Python could not read your code (syntax error){_where(execution, ar=False)}."
                  + (f" {message}" if message else ""),
            "ar": f"تعذّر على Python قراءة الكود (خطأ في الصياغة){_where(execution, ar=True)}. "
                  "التفاصيل في نافذة المخرجات.",
        }
    if status == "runtime_error":
        name = _error_name(execution)
        message = str((execution.error or {}).get("message") or "")
        named_en = f" with {name}" if name else " with an error"
        named_ar = f" بسبب {name}" if name else " بسبب خطأ"
        return {
            "en": f"Your code started but stopped{named_en}{_where(execution, ar=False)}."
                  + (f" {name}: {message}" if name and message else ""),
            "ar": f"بدأ تشغيل الكود لكنه توقف{named_ar}{_where(execution, ar=True)}. التفاصيل في نافذة المخرجات.",
        }
    if status == "grading_error":
        return {
            "en": "This exercise cannot be checked right now because of a problem on our side. "
                  "Your attempt was not counted.",
            "ar": "لا يمكن التحقق من هذا التمرين الآن بسبب مشكلة من جهتنا. لم تُحتسب هذه المحاولة.",
        }
    # execution_error: Masar's runner was unavailable; the answer was not graded.
    stderr = (execution.stderr or "").strip()
    return {
        "en": f"{stderr or 'Code execution failed.'} Your answer was not graded and this attempt does not count.",
        "ar": f"{platform_message(stderr, 'ar') or 'فشل تنفيذ الكود.'} لم تُقيَّم إجابتك ولن تُحتسب هذه المحاولة.",
    }


def crash_notice(execution: ExecutionResult) -> dict[str, str]:
    """A one-line note that the learner's program also crashed, added after
    the feedback of the check that explains the crash."""
    name = _error_name(execution) or "an error"
    return {
        "en": f"Your program also stopped with {name}{_where(execution, ar=False)}.",
        "ar": f"وتوقف برنامجك أيضًا بسبب {name if name != 'an error' else 'خطأ'}{_where(execution, ar=True)}.",
    }


@dataclass
class GradingResult:
    status: str
    passed: bool
    feedback_code: str
    feedback: Any
    failed_test_id: str | None
    tests_passed: int
    tests_total: int
    execution: ExecutionResult
    # A second, independent message (for example "your program also crashed
    # on line 31"), shown after ``feedback``.
    notice: dict[str, str] | None = None


def _configuration_error(problems: list[str], total: int, execution: ExecutionResult | None = None) -> GradingResult:
    execution = execution or ExecutionResult("grading_error")
    execution.status = "grading_error"
    execution.detail = "; ".join(problems)[:500]
    return GradingResult(
        "grading_error", False, "INVALID_TEST_CONFIGURATION",
        execution_failure_feedback(execution), None, 0, total, execution,
    )


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return None


def _calls(tree: ast.AST, name: str) -> list[ast.Call]:
    return [node for node in ast.walk(tree) if isinstance(node, ast.Call) and _call_name(node.func) == name]


def _value(observation: dict[str, Any] | None) -> Any:
    if not observation or observation.get("missing") or observation.get("kind") == "error":
        return _MISSING
    return observation.get("value", observation.get("repr", _MISSING))


_MISSING = object()
_OPERATORS = {
    "add": ast.Add, "+": ast.Add, "sub": ast.Sub, "-": ast.Sub, "mult": ast.Mult, "*": ast.Mult,
    "div": ast.Div, "/": ast.Div, "floordiv": ast.FloorDiv, "//": ast.FloorDiv, "mod": ast.Mod, "%": ast.Mod,
    "pow": ast.Pow, "**": ast.Pow, "eq": ast.Eq, "==": ast.Eq, "lt": ast.Lt, "<": ast.Lt,
    "gt": ast.Gt, ">": ast.Gt, "in": ast.In, "and": ast.And, "or": ast.Or,
}


# Tests that guard how an answer was reached (a blank typed in rather than
# computed). They must pass for a correct result, but they are not part of
# the answer, so they never count toward "3 of 4 checks".
GATE_TEST_TYPES = frozenset({"blank_computed"})


def _failure_status(passed: int) -> str:
    """A graded answer that did not pass: partly right or not at all."""
    return "partial" if passed > 0 else "incorrect"


def _counts(test: dict[str, Any]) -> bool:
    return test.get("type") not in GATE_TEST_TYPES


class PythonGrader:
    def __init__(self, runner: CodeRunner | None = None):
        # The default runner follows the configured execution backend: the
        # isolated runner in production, nothing at all when it is disabled.
        self.runner = runner or IsolatedPythonRunner()

    async def grade(self, code: str, tests: list[dict[str, Any]], *, pre_exercise_code: str = "") -> GradingResult:
        problems = grading_test_problems(tests)
        if problems:
            return _configuration_error(problems, len([t for t in tests or [] if isinstance(t, dict)]))
        required = [test for test in tests if test.get("required", True)]
        total = sum(_counts(test) for test in required)
        try:
            tree = parse_learner_python(code)
        except SyntaxError as exc:
            execution = ExecutionResult(
                "syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})",
                error={"type": "SyntaxError", "message": str(exc.msg), "line": exc.lineno},
            )
            return GradingResult(
                "syntax_error", False, "SYNTAX_ERROR", execution_failure_feedback(execution),
                None, 0, total, execution,
            )
        # An untouched ``___`` would only surface as a NameError at runtime.
        # Say what is actually wrong instead, before anything executes.
        remaining = count_python_blanks(code)
        if remaining:
            return GradingResult(
                "incorrect", False, "BLANKS_REMAINING",
                blanks_remaining_feedback(remaining, first_blank_line(code)),
                "blanks_remaining", 0, total, ExecutionResult("success"),
            )
        # Fill-in-the-blank checks run before learner code, so the grader can
        # name the first incorrect field instead of executing a program that
        # cannot work. Each check points to the exact AST slot authored for
        # that blank.
        #
        # An ``advisory`` blank check is the exception: its exercise also has
        # behavioural tests that observe what the blank computes, so any
        # equivalent expression (``tp / (fp + tp)``, ``reshape((6, 4))``) is
        # accepted. Its AST is only consulted to point at the blank when a
        # behavioural test fails.
        preflight_indexes: set[int] = set()
        advisory_indexes: list[int] = []
        passed = 0
        first_failure: tuple[int, dict[str, Any]] | None = None
        preflight_execution = ExecutionResult("success")
        # Without another required test nothing would observe the blank, so
        # an advisory flag on its own never relaxes a check.
        observed = any(test.get("type") != "ast_contains" for test in required)
        for index, test in enumerate(tests):
            if not test.get("required", True) or test.get("type") != "ast_contains":
                continue
            preflight_indexes.add(index)
            if test.get("advisory") and observed:
                advisory_indexes.append(index)
                continue
            if self._check(test, index, tree, preflight_execution):
                passed += _counts(test)
            elif first_failure is None:
                first_failure = (index, test)
        if first_failure is not None:
            index, test = first_failure
            return GradingResult(
                _failure_status(passed), False, self._feedback_code("ast_contains"),
                test.get("feedback") or self._default_feedback("ast_contains"),
                str(test.get("id") or f"test_{index + 1}"), passed, total,
                preflight_execution,
            )
        variable_names = sorted({
            str(test.get("variable")) for test in tests
            if test.get("variable") and test.get("type") in _VARIABLE_TESTS
        })
        calls = []
        for index, test in enumerate(tests):
            if test.get("type") == "return_value_equals":
                calls.append({
                    "key": str(index), "function": test.get("function"),
                    "args": test.get("args", []), "kwargs": test.get("kwargs", {}),
                })
            elif test.get("type") == "expression_equals":
                # An author's hidden check, evaluated after the learner's code.
                calls.append({"key": str(index), "expression": str(test.get("expression", ""))})
        # Legacy framework exercises often demonstrate APIs that are not
        # installed in the restricted runner. Their migrated tests inspect
        # Python structure only, so submitting them must not import or invoke
        # those libraries. Mixed/runtime exercises retain normal execution
        # and its security/runtime precedence.
        execution = ExecutionResult("success") if is_static_only(tests) else await self.runner.run(
            code, pre_exercise_code=pre_exercise_code, variables=variable_names, calls=calls,
        )
        if execution.status == "grading_error":
            return _configuration_error([execution.detail or "runner refused the exercise setup"], total, execution)
        # A crash still lets the checks speak: they ran against whatever the
        # program defined before it stopped (see isolated_python_runner).
        crashed = execution.status == "runtime_error" and bool(required)
        if not execution.succeeded and not crashed:
            return GradingResult(
                execution.status, False, execution.status.upper(),
                execution_failure_feedback(execution),
                None, 0, total, execution,
            )
        # An executable program is not, by itself, a correct answer. Without
        # this guard an authoring mistake such as an empty test list (or a
        # list containing only optional diagnostics) would vacuously pass.
        if not required:
            return _configuration_error(["the exercise has no required tests"], 0, execution)
        failure: tuple[int, dict[str, Any]] | None = None
        for index, test in enumerate(tests):
            if index in preflight_indexes or not test.get("required", True):
                continue
            if self._check(test, index, tree, execution):
                passed += _counts(test)
            elif failure is None:
                failure = (index, test)
        if failure is None:
            if crashed:
                # Everything the checks look at works, but the program itself
                # still stops with an error: that is not a finished answer.
                return GradingResult(
                    "runtime_error", False, "RUNTIME_ERROR", execution_failure_feedback(execution),
                    None, passed, total, execution,
                )
            # Every behavioural test passed, so the advisory blanks are satisfied.
            passed += len(advisory_indexes)
            return GradingResult(
                "correct", True, "CORRECT", {"en": "Correct!", "ar": "إجابة صحيحة!"},
                None, passed, total, execution,
            )
        index, test = failure
        if crashed and not self._observed(test, index, execution):
            # The check failed only because the crash stopped the program
            # before it defined what the check reads: the crash is the news.
            return GradingResult(
                "runtime_error", False, "RUNTIME_ERROR", execution_failure_feedback(execution),
                None, passed, total, execution,
            )
        # A wrong blank is the most precise thing to point at.
        for blank_index in advisory_indexes:
            blank = tests[blank_index]
            if not self._check(blank, blank_index, tree, execution):
                index, test = blank_index, blank
                break
        kind = str(test.get("type"))
        return GradingResult(
            "runtime_error" if crashed else _failure_status(passed), False,
            "RUNTIME_ERROR" if crashed else self._feedback_code(kind),
            test.get("feedback") or self._default_feedback(kind),
            str(test.get("id") or f"test_{index + 1}"), passed, total, execution,
            notice=crash_notice(execution) if crashed else None,
        )

    def _check(self, test: dict[str, Any], index: int, tree: ast.AST, result: ExecutionResult) -> bool:
        kind = test.get("type")
        name = str(test.get("variable", ""))
        observation = result.variables.get(name)
        value = _value(observation)
        if kind == "variable_exists": return value is not _MISSING
        if kind == "variable_not_exists": return value is _MISSING
        if kind == "value_equals": return value is not _MISSING and values_match(value, test.get("expected"), **_tolerances(test))
        if kind == "value_approx":
            try: return math.isclose(float(value), float(test.get("expected")), rel_tol=float(test.get("rel_tol", 1e-9)), abs_tol=float(test.get("abs_tol", 1e-9)))
            except (TypeError, ValueError): return False
        if kind == "type_equals": return bool(observation) and observation.get("type") == test.get("expected")
        if kind in {"function_called", "function_not_called", "function_call_count", "function_argument"}:
            found = _calls(tree, str(test.get("function", "")))
            if kind == "function_called": return bool(found)
            if kind == "function_not_called": return not found
            if kind == "function_call_count": return len(found) == int(test.get("expected", test.get("count", 0)))
            if not found: return False
            call = found[int(test.get("call_index", 0))] if len(found) > int(test.get("call_index", 0)) else None
            if call is None: return False
            argument_index = int(test.get("argument_index", 0))
            if argument_index >= len(call.args): return False
            try: return ast.literal_eval(call.args[argument_index]) == test.get("expected")
            except (ValueError, TypeError): return False
        if kind == "expression_uses":
            expected = str(test.get("expression", test.get("expected", "")))
            return any(expected in ast.unparse(node) for node in ast.walk(tree) if isinstance(node, ast.expr))
        if kind == "operator_used":
            operator = _OPERATORS.get(str(test.get("operator", test.get("expected", ""))).lower())
            return operator is not None and any(isinstance(node, operator) for node in ast.walk(tree))
        if kind == "stdout_equals": return result.stdout.rstrip("\n") == str(test.get("expected", "")).rstrip("\n")
        if kind == "stdout_contains": return str(test.get("expected", "")) in result.stdout
        if kind == "list_length": return isinstance(value, list) and len(value) == int(test.get("expected", 0))
        if kind == "dict_contains_key": return isinstance(value, dict) and str(test.get("key")) in value
        if kind == "dataframe_exists": return bool(observation) and observation.get("kind") == "dataframe"
        if kind == "dataframe_columns":
            actual = (observation or {}).get("value", {}).get("columns")
            expected = [str(item) for item in test.get("expected", [])]
            return actual == expected if test.get("ordered", True) else set(actual or []) == set(expected)
        if kind == "dataframe_shape": return (observation or {}).get("value", {}).get("shape") == list(test.get("expected", []))
        if kind == "dataframe_column_values":
            columns = (observation or {}).get("value", {}).get("column_values", {})
            column = str(test.get("column"))
            return column in columns and values_match(columns[column], test.get("expected"), **_tolerances(test))
        if kind == "function_exists":
            expected = str(test.get("function", ""))
            return any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == expected for node in ast.walk(tree))
        if kind == "code_changed":
            return ast_fingerprint(ast.unparse(tree)) != str(test.get("starter_fingerprint", ""))
        if kind == "placeholders_removed":
            return placeholders_are_removed(tree, test)
        if kind == "ast_requirements":
            return ast_satisfies(ast_requirements(ast.unparse(tree)), dict(test.get("requirements") or {}))
        if kind == "ast_contains":
            # ``expected_ast_any`` lists equivalent answers a static blank accepts;
            # ``expected_ast_canonical`` the same answers with keyword arguments
            # in name order, so their order in the learner's call is free.
            accepted = {str(test.get("expected_ast", ""))} | {
                str(item) for item in test.get("expected_ast_any") or []
            }
            canonical = {str(item) for item in test.get("expected_ast_canonical") or []}

            def matches(node: ast.AST) -> bool:
                return ast.dump(node, include_attributes=False) in accepted or (
                    bool(canonical) and canonical_dump(node) in canonical
                )

            path = test.get("path")
            if isinstance(path, list):
                node: Any = tree
                try:
                    for part in path:
                        node = node[int(part)] if isinstance(node, list) else getattr(node, str(part))
                except (AttributeError, IndexError, TypeError, ValueError):
                    return False
                return isinstance(node, ast.AST) and matches(node)
            expected_count = int(test.get("expected_count", 1))
            return sum(matches(node) for node in ast.walk(tree)) >= expected_count
        if kind == "blank_computed":
            return blank_is_computed(tree, test)
        if kind in {"return_value_equals", "expression_equals"}:
            observed = result.return_values.get(str(index)) or {}
            raised = observed.get("type") if observed.get("kind") == "error" else None
            expected_errors = _raises_names(test)
            if expected_errors is not None:
                # The check expects the call to raise one of these exceptions.
                return raised in expected_errors
            if raised:
                return False
            actual = _value(observed)
            return actual is not _MISSING and values_match(actual, test.get("expected"), **_tolerances(test))
        if kind == "custom":
            checker = CUSTOM_TESTS.get(str(test.get("checker", "")))
            return bool(checker and checker({"variables": result.variables, "stdout": result.stdout}, test))
        return False

    @staticmethod
    def _observed(test: dict[str, Any], index: int, result: ExecutionResult) -> bool:
        """Whether a failing check saw the learner's program at all, rather
        than a name the program never reached because it crashed first."""
        kind = test.get("type")
        if kind in _VARIABLE_TESTS:
            return _value(result.variables.get(str(test.get("variable", "")))) is not _MISSING
        if kind in {"return_value_equals", "expression_equals"}:
            observed = result.return_values.get(str(index)) or {}
            if observed.get("missing"):
                return False
            return not (observed.get("kind") == "error" and observed.get("type") == "NameError")
        return True

    @staticmethod
    def _feedback_code(kind: str) -> str:
        return {
            "variable_exists": "VARIABLE_MISSING", "variable_not_exists": "UNEXPECTED_VARIABLE",
            "value_equals": "WRONG_VALUE", "value_approx": "WRONG_VALUE", "type_equals": "WRONG_TYPE",
            "function_called": "REQUIRED_FUNCTION_MISSING", "function_not_called": "FORBIDDEN_FUNCTION_USED",
            "function_argument": "WRONG_FUNCTION_ARGUMENT", "function_call_count": "WRONG_CALL_COUNT",
            "ast_contains": "BLANK_INCORRECT", "blank_computed": "BLANK_HARDCODED",
        }.get(kind, "TEST_FAILED")

    @staticmethod
    def _default_feedback(kind: str) -> dict[str, str]:
        return {
            "en": "Your solution did not satisfy this requirement.",
            "ar": "لم يحقق حلك هذا الشرط.",
        }
