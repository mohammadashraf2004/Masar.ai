"""Deterministic baseline tests for legacy scaffolded Python exercises.

These tests deliberately compare requirements, not source text.  They are a
safe migration floor for the older tool-course exercises whose authored
solution predates the test schema: learners may use different whitespace,
variable values, and implementations as long as the required public names,
API calls, and control-flow concepts are present and the starter placeholders
are actually completed.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
from collections import Counter
from dataclasses import dataclass
from typing import Any


_STRUCTURAL_NODES = {
    "If": ast.If,
    "For": ast.For,
    "While": ast.While,
    "Try": ast.Try,
    "With": ast.With,
    "Match": ast.Match,
    "Return": ast.Return,
    "ListComp": ast.ListComp,
    "DictComp": ast.DictComp,
}

# Incidental Python operations are implementation choices, not learning
# requirements.  Framework/API calls remain in the fingerprint, while these
# common built-ins and container/string helpers may be replaced by an
# equivalent implementation.
_INTERCHANGEABLE_CALLS = {
    "all", "any", "append", "clear", "copy", "count", "dict", "enumerate",
    "extend", "filter", "float", "format", "get", "index", "insert", "int",
    "items", "join", "keys", "len", "list", "lower", "map", "max", "min",
    "pop", "range", "remove", "replace", "reversed", "set", "sorted", "split",
    "startswith", "str", "strip", "sum", "title", "tuple", "upper", "values", "zip",
}


# Tests that observe what the learner's program computes once it has run.
BEHAVIOURAL_TEST_TYPES = frozenset({
    "value_equals", "value_approx", "type_equals", "list_length", "dict_contains_key",
    "dataframe_exists", "dataframe_columns", "dataframe_shape", "dataframe_column_values",
    "stdout_equals", "stdout_contains", "return_value_equals", "expression_equals", "custom",
})


@dataclass(frozen=True)
class _BlankCandidate:
    start: int
    end: int
    lineno: int
    end_lineno: int
    score: int
    label: str
    label_ar: str
    expected_ast: str
    expected_count: int
    path: tuple[str | int, ...]


def _absolute_offset(source: str, lines: list[str], lineno: int, byte_column: int) -> int:
    """Translate CPython's UTF-8 AST column offset into a string offset."""
    line = lines[lineno - 1]
    character_column = len(line.encode("utf-8")[:byte_column].decode("utf-8"))
    return sum(len(item) for item in lines[:lineno - 1]) + character_column


def _call_label(node: ast.Call) -> str:
    target: ast.AST = node.func
    parts: list[str] = []
    while isinstance(target, ast.Attribute):
        parts.append(target.attr)
        target = target.value
    if isinstance(target, ast.Name):
        parts.append(target.id)
    return ".".join(reversed(parts)) or "function"


def _changed_solution_lines(starter_code: str, solution_code: str) -> set[int]:
    changed: set[int] = set()
    matcher = difflib.SequenceMatcher(
        a=starter_code.splitlines(), b=solution_code.splitlines(), autojunk=False,
    )
    for tag, _a1, _a2, b1, b2 in matcher.get_opcodes():
        if tag != "equal":
            changed.update(range(b1 + 1, b2 + 1))
    return changed


def _candidate_label(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> str:
    parent = parents.get(node)
    if isinstance(parent, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
        targets = sorted(_targets(parent))
        return f"the expression assigned to `{', '.join(targets)}`" if targets else "the assigned expression"
    if isinstance(parent, ast.Return):
        cursor: ast.AST | None = parent
        while cursor is not None and not isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cursor = parents.get(cursor)
        return f"the return expression in `{cursor.name}()`" if cursor else "the return expression"
    if isinstance(node, ast.Call):
        return f"the `{_call_label(node)}()` call"
    if isinstance(parent, (ast.If, ast.While)):
        return "the control-flow condition"
    if isinstance(parent, ast.Dict):
        try:
            index = parent.values.index(node)  # type: ignore[arg-type]
            key = ast.literal_eval(parent.keys[index])
            return f"the value for `{key}`"
        except (ValueError, TypeError):
            return "the dictionary value"
    if isinstance(parent, ast.keyword):
        call = parents.get(parent)
        name = _call_label(call) if isinstance(call, ast.Call) else "function"
        return f"the `{parent.arg}` argument passed to `{name}()`"
    if isinstance(parent, ast.Call):
        return f"an argument passed to `{_call_label(parent)}()`"
    return "the missing expression"


def _candidate_label_ar(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> str:
    parent = parents.get(node)
    if isinstance(parent, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
        targets = sorted(_targets(parent))
        return f"التعبير المسند إلى `{', '.join(targets)}`" if targets else "التعبير المسند"
    if isinstance(parent, ast.Return):
        cursor: ast.AST | None = parent
        while cursor is not None and not isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cursor = parents.get(cursor)
        return f"تعبير الإرجاع في `{cursor.name}()`" if cursor else "تعبير الإرجاع"
    if isinstance(node, ast.Call):
        return f"استدعاء `{_call_label(node)}()`"
    if isinstance(parent, (ast.If, ast.While)):
        return "شرط تدفق التحكم"
    if isinstance(parent, ast.Dict):
        try:
            index = parent.values.index(node)  # type: ignore[arg-type]
            key = ast.literal_eval(parent.keys[index])
            return f"قيمة `{key}`"
        except (ValueError, TypeError):
            return "قيمة القاموس"
    if isinstance(parent, ast.keyword):
        call = parents.get(parent)
        name = _call_label(call) if isinstance(call, ast.Call) else "الدالة"
        return f"المعامل `{parent.arg}` الممرر إلى `{name}()`"
    if isinstance(parent, ast.Call):
        return f"أحد المعاملات الممررة إلى `{_call_label(parent)}()`"
    return "التعبير الناقص"


def _blank_candidates(starter_code: str, solution_code: str) -> list[_BlankCandidate]:
    tree = ast.parse(solution_code or "", mode="exec")
    lines = solution_code.splitlines(keepends=True)
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    paths: dict[ast.AST, tuple[str | int, ...]] = {}

    def record_paths(node: ast.AST, path: tuple[str | int, ...] = ()) -> None:
        paths[node] = path
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                record_paths(value, (*path, field))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, ast.AST):
                        record_paths(item, (*path, field, index))

    record_paths(tree)
    changed_lines = _changed_solution_lines(starter_code, solution_code)
    dumps = Counter(ast.dump(node, include_attributes=False) for node in ast.walk(tree) if isinstance(node, ast.expr))
    ranked: list[_BlankCandidate] = []
    seen_spans: set[tuple[int, int]] = set()

    def add(node: ast.expr | None, base_score: int) -> None:
        if node is None or not hasattr(node, "end_lineno") or node.end_lineno is None:
            return
        segment = ast.get_source_segment(solution_code, node)
        if not segment or segment.strip() == "___" or len(segment) > 500 or segment.count("\n") > 7:
            return
        start = _absolute_offset(solution_code, lines, node.lineno, node.col_offset)
        end = _absolute_offset(solution_code, lines, node.end_lineno, node.end_col_offset)
        if (start, end) in seen_spans:
            return
        seen_spans.add((start, end))
        overlap = any(line in changed_lines for line in range(node.lineno, node.end_lineno + 1))
        expected = ast.dump(node, include_attributes=False)
        ranked.append(_BlankCandidate(
            start=start,
            end=end,
            lineno=node.lineno,
            end_lineno=node.end_lineno,
            score=base_score + (250 if overlap else 0),
            label=_candidate_label(node, parents),
            label_ar=_candidate_label_ar(node, parents),
            expected_ast=expected,
            expected_count=dumps[expected],
            path=paths[node],
        ))

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            add(node.value, 120)
        elif isinstance(node, ast.Return):
            add(node.value, 110)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            add(node.value, 100)
        elif isinstance(node, (ast.If, ast.While)):
            add(node.test, 80)

    # Dictionary payload/schema exercises often keep the outer assignment
    # intact and teach only a handful of meaningful metadata values.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for value in node.values:
            add(value, 95 if isinstance(value, (ast.Constant, ast.Call, ast.BinOp)) else 65)

    # Arguments are a useful fallback for short examples with only one outer
    # expression. They score below assignments/returns so the learner sees the
    # program structure before being asked for a narrow API detail.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for argument in node.args:
            if not isinstance(argument, (ast.Name, ast.Constant)):
                add(argument, 55)
        for keyword in node.keywords:
            if not isinstance(keyword.value, ast.Name):
                add(keyword.value, 60)

    return sorted(ranked, key=lambda item: (-item.score, item.start, item.end))


def count_python_blanks(source: str) -> int:
    """Count editable ``___`` expression slots without counting comments/strings."""
    try:
        tree = ast.parse(source or "", mode="exec")
    except SyntaxError:
        return 0
    return sum(isinstance(node, ast.Name) and node.id == "___" for node in ast.walk(tree))


def build_fill_in_blank_exercise(
    starter_code: str,
    solution_code: str,
    tests: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]], list[str]]:
    """Turn an authored Python solution into a small, deterministic fill-in task.

    The official solution remains the source of truth. The resulting starter
    exposes the complete surrounding program and replaces only 1–5 expression
    nodes. Each selected expression gets its own hidden AST check, followed by
    the exercise's existing behavioral/structural tests.
    """
    if any(test.get("type") == "ast_contains" for test in tests):
        labels = [str(test.get("label") or "the missing expression") for test in tests if test.get("type") == "ast_contains"]
        return starter_code, tests, labels

    candidates = _blank_candidates(starter_code, solution_code)
    if not candidates:
        raise ValueError("official solution has no safe expression that can become a blank")
    required_tests = sum(bool(test.get("required", True)) for test in tests)
    requested = min(5, max(
        1,
        starter_code.count("TODO"),
        count_python_blanks(starter_code),
        min(required_tests, 5),
    ))
    selected: list[_BlankCandidate] = []
    for candidate in candidates:
        if any(not (candidate.end <= item.start or candidate.start >= item.end) for item in selected):
            continue
        selected.append(candidate)
        if len(selected) == requested:
            break
    if not selected:
        raise ValueError("official solution has no non-overlapping expression blanks")
    selected.sort(key=lambda item: item.start)

    blanked = solution_code
    for candidate in reversed(selected):
        blanked = blanked[:candidate.start] + "___" + blanked[candidate.end:]

    # With behavioural checks in place, an equivalent expression in a blank is
    # accepted (see PythonGrader); static-only exercises keep the exact check
    # because nothing else would observe what the blank computes.
    advisory = any(
        test.get("required", True) and test.get("type") in BEHAVIOURAL_TEST_TYPES for test in tests
    )
    blank_tests: list[dict[str, Any]] = []
    labels: list[str] = []
    for index, candidate in enumerate(selected, start=1):
        labels.append(candidate.label)
        blank_tests.append({
            "id": f"blank_{index}",
            "type": "ast_contains",
            "static": True,
            "advisory": advisory,
            "expected_ast": candidate.expected_ast,
            "expected_count": candidate.expected_count,
            "path": list(candidate.path),
            "label": candidate.label,
            "feedback": {
                "en": f"Blank {index}: complete {candidate.label}. Check the lesson concept and try again.",
                "ar": f"الفراغ {index}: أكمل {candidate.label_ar}. راجع مفهوم الدرس ثم حاول مرة أخرى.",
            },
        })

    updated_tests = [*blank_tests, *tests]
    starter_hash = ast_fingerprint(blanked)
    for test in updated_tests:
        if test.get("type") == "code_changed":
            test["starter_fingerprint"] = starter_hash
    return blanked, updated_tests, labels


def ast_fingerprint(source: str) -> str:
    tree = ast.parse(source or "", mode="exec")
    normalized = ast.dump(tree, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _call_leaf(node: ast.Call) -> str | None:
    target: ast.AST = node.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def _targets(node: ast.AST) -> set[str]:
    targets: set[str] = set()
    candidates: list[ast.AST] = []
    if isinstance(node, ast.Assign):
        candidates.extend(node.targets)
    elif isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
        candidates.append(node.target)
    for candidate in candidates:
        for child in ast.walk(candidate):
            if isinstance(child, ast.Name):
                targets.add(child.id)
    return targets


def ast_requirements(source: str) -> dict[str, Any]:
    tree = ast.parse(source or "", mode="exec")
    imported_symbols: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_symbols.update(alias.asname or alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported_symbols.update(alias.asname or alias.name for alias in node.names)
    calls = Counter(
        leaf for node in ast.walk(tree)
        if isinstance(node, ast.Call) and (leaf := _call_leaf(node)) and leaf != "print"
        and (
            leaf in imported_symbols
            or (isinstance(node.func, ast.Attribute) and leaf not in _INTERCHANGEABLE_CALLS)
        )
    )
    assigned: set[str] = set()
    # Only module-level names are part of an exercise's public result. Local
    # temporary variable names must remain free to differ from the reference.
    for node in tree.body:
        assigned.update(_targets(node))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
    dict_keys = {
        key.value for node in ast.walk(tree) if isinstance(node, ast.Dict)
        for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }
    return {
        "assigned": sorted(name for name in assigned if not name.startswith("_")),
        "functions": sorted(
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
        ),
        "classes": sorted(
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        ),
        "imports": sorted(imports),
        "calls": dict(sorted(calls.items())),
        "structure": {
            label: sum(isinstance(node, kind) for node in ast.walk(tree))
            for label, kind in _STRUCTURAL_NODES.items()
            if any(isinstance(node, kind) for node in ast.walk(tree))
        },
        "dict_keys": sorted(dict_keys),
    }


def _placeholder(value: ast.AST | None) -> bool:
    if value is None:
        return False
    if isinstance(value, ast.Constant):
        return value.value is None or value.value is Ellipsis or value.value == ""
    return isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict)) and not (
        getattr(value, "elts", None) or getattr(value, "keys", None)
    )


def _assigned_values(tree: ast.AST) -> dict[str, ast.AST]:
    values: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        value = node.value if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)) else None
        if value is None:
            continue
        for name in _targets(node):
            values[name] = value
    return values


def _placeholder_functions(tree: ast.AST) -> set[str]:
    result: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = [item for item in node.body if not (
            isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant)
            and isinstance(item.value.value, str)
        )]
        if not body or all(
            isinstance(item, ast.Pass)
            or (isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant) and item.value.value is Ellipsis)
            for item in body
        ):
            result.add(node.name)
    return result


def placeholder_requirements(starter_code: str, solution_code: str) -> dict[str, Any]:
    starter, solution = ast.parse(starter_code or ""), ast.parse(solution_code or "")
    starter_values, solution_values = _assigned_values(starter), _assigned_values(solution)
    targets = sorted(
        name for name, value in starter_values.items()
        if _placeholder(value) and name in solution_values and not _placeholder(solution_values[name])
    )
    functions = sorted(_placeholder_functions(starter) - _placeholder_functions(solution))
    return {
        "targets": targets,
        "functions": functions,
        "max_pass": sum(isinstance(node, ast.Pass) for node in ast.walk(solution)),
    }


def build_static_python_tests(starter_code: str, solution_code: str) -> list[dict[str, Any]]:
    """Build ordered, hidden, static checks from an authored scaffold/solution.

    This is used only for legacy exercises which have a real official Python
    solution but no authored tests.  It never embeds or compares solution
    source and it always proves that the untouched starter cannot pass.
    """
    starter_hash = ast_fingerprint(starter_code)
    solution_hash = ast_fingerprint(solution_code)
    if starter_hash == solution_hash:
        raise ValueError("starter_code and solution_code are structurally identical")
    placeholders = placeholder_requirements(starter_code, solution_code)
    tests: list[dict[str, Any]] = [
        {
            "id": "starter_changed",
            "type": "code_changed",
            "static": True,
            "starter_fingerprint": starter_hash,
            "feedback": {
                "en": "Complete the TODOs instead of submitting the unchanged starter code.",
                "ar": "أكمل مواضع TODO بدلًا من إرسال الكود المبدئي دون تغيير.",
            },
        },
    ]
    if placeholders["targets"] or placeholders["functions"] or placeholders["max_pass"] == 0:
        tests.append({
            "id": "placeholders_removed",
            "type": "placeholders_removed",
            "static": True,
            **placeholders,
            "feedback": {
                "en": "Replace the remaining `pass`, `None`, empty value, or unfinished function placeholder.",
                "ar": "استبدل موضع `pass` أو `None` أو القيمة الفارغة أو الدالة غير المكتملة المتبقية.",
            },
        })
    tests.append({
        "id": "required_structure",
        "type": "ast_requirements",
        "static": True,
        "requirements": ast_requirements(solution_code),
        "feedback": {
            "en": "Your solution is missing a required definition, API call, data key, or control-flow step.",
            "ar": "يفتقد حلك تعريفًا أو استدعاء API أو مفتاح بيانات أو خطوة تحكم مطلوبة.",
        },
    })
    return tests


def complete_seed_exercises(topics: list[dict[str, Any]]) -> int:
    """Complete and blank-format Python definitions in a tool-course list."""
    completed = 0
    for topic in topics:
        for exercise in topic.get("exercises", []):
            if exercise.get("grading_tests"):
                exercise.setdefault("exercise_type", "code")
                exercise.setdefault("language", "python")
            else:
                starter, solution = exercise.get("starter_code"), exercise.get("solution_code")
                if not starter or not solution:
                    continue
                try:
                    tests = build_static_python_tests(str(starter), str(solution))
                except ValueError:
                    # If only comments differ, this is a prediction/reflection
                    # prompt rather than an implementation exercise.  Leaving a
                    # starter on it would render a code cell that can never be
                    # graded from Python semantics.
                    exercise["exercise_type"] = "legacy"
                    exercise["starter_code"] = None
                    exercise["language"] = None
                    exercise["grading_tests"] = None
                    continue
                except SyntaxError:
                    continue
                exercise["exercise_type"] = "code"
                exercise["language"] = "python"
                exercise["grading_tests"] = tests

            starter, solution = exercise.get("starter_code"), exercise.get("solution_code")
            if exercise.get("exercise_type") != "code" or exercise.get("language") != "python" or not starter or not solution:
                continue
            try:
                blanked, tests, labels = build_fill_in_blank_exercise(
                    str(starter), str(solution), list(exercise.get("grading_tests") or []),
                )
            except (SyntaxError, ValueError):
                continue
            exercise["starter_code"] = blanked
            exercise["grading_tests"] = tests
            exercise["hint"] = "Fill the `___` expressions using the lesson concepts, then submit your completed program."
            concepts = ", ".join(label.replace("the ", "", 1) for label in labels[:3])
            exercise["success_message"] = (
                f"Correct! The completed expressions supply {concepts} while the surrounding code shows the full workflow."
            )
            completed += 1
    return completed


def ast_satisfies(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    for key in ("assigned", "functions", "classes", "imports", "dict_keys"):
        if not set(expected.get(key, [])).issubset(actual.get(key, [])):
            return False
    for key in ("calls", "structure"):
        if any(int(actual.get(key, {}).get(name, 0)) < int(count) for name, count in expected.get(key, {}).items()):
            return False
    return True


def placeholders_are_removed(tree: ast.AST, test: dict[str, Any]) -> bool:
    values = _assigned_values(tree)
    if any(name not in values or _placeholder(values[name]) for name in test.get("targets", [])):
        return False
    if any(name in _placeholder_functions(tree) for name in test.get("functions", [])):
        return False
    return sum(isinstance(node, ast.Pass) for node in ast.walk(tree)) <= int(test.get("max_pass", 0))
