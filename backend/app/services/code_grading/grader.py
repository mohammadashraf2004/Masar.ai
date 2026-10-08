"""Ordered deterministic Python grading."""
from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Any

from app.services.code_execution import CodeRunner, ExecutionResult, LocalPythonRunner
from .authoring import ast_fingerprint, ast_requirements, ast_satisfies, placeholders_are_removed
from .custom import CUSTOM_TESTS


SUPPORTED_TEST_TYPES = frozenset({
    "variable_exists", "variable_not_exists", "value_equals", "value_approx", "type_equals",
    "function_called", "function_not_called", "function_argument", "function_call_count",
    "expression_uses", "operator_used", "stdout_equals", "stdout_contains",
    "list_length", "dict_contains_key", "dataframe_exists", "dataframe_columns",
    "dataframe_shape", "dataframe_column_values", "return_value_equals", "function_exists", "custom",
    "code_changed", "placeholders_removed", "ast_requirements", "ast_contains",
})

STATIC_TEST_TYPES = frozenset({
    "function_called", "function_not_called", "function_argument", "function_call_count",
    "expression_uses", "operator_used", "function_exists",
    "code_changed", "placeholders_removed", "ast_requirements", "ast_contains",
})


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
    if not observation or observation.get("missing"):
        return _MISSING
    return observation.get("value", observation.get("repr", _MISSING))


_MISSING = object()
_OPERATORS = {
    "add": ast.Add, "+": ast.Add, "sub": ast.Sub, "-": ast.Sub, "mult": ast.Mult, "*": ast.Mult,
    "div": ast.Div, "/": ast.Div, "floordiv": ast.FloorDiv, "//": ast.FloorDiv, "mod": ast.Mod, "%": ast.Mod,
    "pow": ast.Pow, "**": ast.Pow, "eq": ast.Eq, "==": ast.Eq, "lt": ast.Lt, "<": ast.Lt,
    "gt": ast.Gt, ">": ast.Gt, "in": ast.In, "and": ast.And, "or": ast.Or,
}


class PythonGrader:
    def __init__(self, runner: CodeRunner | None = None):
        self.runner = runner or LocalPythonRunner()

    async def grade(self, code: str, tests: list[dict[str, Any]], *, pre_exercise_code: str = "") -> GradingResult:
        required = [test for test in tests if test.get("required", True)]
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as exc:
            execution = ExecutionResult(
                "syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})",
            )
            return GradingResult(
                "syntax_error", False, "SYNTAX_ERROR",
                {"en": execution.stderr, "ar": execution.stderr},
                None, 0, len(required), execution,
            )
        # Fill-in-the-blank checks run before learner code. This lets the
        # grader identify the first incorrect field instead of executing an
        # unresolved ``___`` name and returning an unhelpful NameError. Each
        # check points to the exact AST slot authored for that blank.
        preflight_indexes: set[int] = set()
        passed = 0
        preflight_execution = ExecutionResult("success")
        for index, test in enumerate(tests):
            if not test.get("required", True) or test.get("type") != "ast_contains":
                continue
            preflight_indexes.add(index)
            if self._check(test, index, tree, preflight_execution):
                passed += 1
                continue
            return GradingResult(
                "incorrect", False, self._feedback_code("ast_contains"),
                test.get("feedback") or self._default_feedback("ast_contains"),
                str(test.get("id") or f"test_{index + 1}"), passed, len(required),
                preflight_execution,
            )
        variable_names = sorted({
            str(test.get("variable")) for test in tests
            if test.get("variable") and test.get("type") in {
                "variable_exists", "variable_not_exists", "value_equals", "value_approx", "type_equals",
                "list_length", "dict_contains_key", "dataframe_exists", "dataframe_columns",
                "dataframe_shape", "dataframe_column_values",
            }
        })
        calls = []
        for index, test in enumerate(tests):
            if test.get("type") == "return_value_equals":
                calls.append({
                    "key": str(index), "function": test.get("function"),
                    "args": test.get("args", []), "kwargs": test.get("kwargs", {}),
                })
        # Legacy framework exercises often demonstrate APIs that are not
        # installed in the restricted runner. Their migrated tests inspect
        # Python structure only, so submitting them must not import or invoke
        # those libraries. Mixed/runtime exercises retain normal execution
        # and its security/runtime precedence.
        static_only = bool(required) and all(
            bool(test.get("static")) and test.get("type") in STATIC_TEST_TYPES
            for test in required
        )
        execution = ExecutionResult("success") if static_only else await self.runner.run(
            code, pre_exercise_code=pre_exercise_code, variables=variable_names, calls=calls,
        )
        if not execution.succeeded:
            return GradingResult(
                execution.status, False, execution.status.upper(),
                {"en": execution.stderr or "Code execution failed.", "ar": execution.stderr or "فشل تنفيذ الكود."},
                None, 0, len(required), execution,
            )
        # An executable program is not, by itself, a correct answer. Without
        # this guard an authoring mistake such as an empty test list (or a
        # list containing only optional diagnostics) would vacuously pass.
        if not required:
            execution.status = "grading_error"
            execution.stderr = "This exercise has no required grading tests."
            return GradingResult(
                "grading_error", False, "INVALID_TEST_CONFIGURATION",
                {
                    "en": "This exercise cannot be graded because it has no required tests.",
                    "ar": "لا يمكن تقييم هذا التمرين لعدم وجود اختبارات مطلوبة.",
                },
                None, 0, 0, execution,
            )
        for index, test in enumerate(tests):
            if index in preflight_indexes:
                continue
            ok = self._check(test, index, tree, execution)
            if ok:
                if test.get("required", True):
                    passed += 1
                continue
            if not test.get("required", True):
                continue
            return GradingResult(
                "incorrect", False, self._feedback_code(str(test.get("type"))),
                test.get("feedback") or self._default_feedback(str(test.get("type"))),
                str(test.get("id") or f"test_{index + 1}"), passed, len(required), execution,
            )
        return GradingResult(
            "correct", True, "CORRECT", {"en": "Correct!", "ar": "إجابة صحيحة!"},
            None, passed, len(required), execution,
        )

    def _check(self, test: dict[str, Any], index: int, tree: ast.AST, result: ExecutionResult) -> bool:
        kind = test.get("type")
        name = str(test.get("variable", ""))
        observation = result.variables.get(name)
        value = _value(observation)
        if kind == "variable_exists": return value is not _MISSING
        if kind == "variable_not_exists": return value is _MISSING
        if kind == "value_equals": return value is not _MISSING and value == test.get("expected")
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
            return columns.get(str(test.get("column"))) == test.get("expected")
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
            expected = str(test.get("expected_ast", ""))
            path = test.get("path")
            if isinstance(path, list):
                node: Any = tree
                try:
                    for part in path:
                        node = node[int(part)] if isinstance(node, list) else getattr(node, str(part))
                except (AttributeError, IndexError, TypeError, ValueError):
                    return False
                return isinstance(node, ast.AST) and ast.dump(node, include_attributes=False) == expected
            expected_count = int(test.get("expected_count", 1))
            return sum(
                ast.dump(node, include_attributes=False) == expected
                for node in ast.walk(tree)
            ) >= expected_count
        if kind == "return_value_equals": return _value(result.return_values.get(str(index))) == test.get("expected")
        if kind == "custom":
            checker = CUSTOM_TESTS.get(str(test.get("checker", "")))
            return bool(checker and checker({"variables": result.variables, "stdout": result.stdout}, test))
        return False

    @staticmethod
    def _feedback_code(kind: str) -> str:
        return {
            "variable_exists": "VARIABLE_MISSING", "variable_not_exists": "UNEXPECTED_VARIABLE",
            "value_equals": "WRONG_VALUE", "value_approx": "WRONG_VALUE", "type_equals": "WRONG_TYPE",
            "function_called": "REQUIRED_FUNCTION_MISSING", "function_not_called": "FORBIDDEN_FUNCTION_USED",
            "function_argument": "WRONG_FUNCTION_ARGUMENT", "function_call_count": "WRONG_CALL_COUNT",
            "ast_contains": "BLANK_INCORRECT",
        }.get(kind, "TEST_FAILED")

    @staticmethod
    def _default_feedback(kind: str) -> dict[str, str]:
        return {
            "en": "Your solution did not satisfy this requirement.",
            "ar": "لم يحقق حلك هذا الشرط.",
        }
