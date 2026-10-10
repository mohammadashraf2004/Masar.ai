"""Guided, deterministic versions of the curriculum's implementation exercises.

The lesson files stay the source of each exercise's id, title, placement and
skills. This registry replaces the parts a learner works with: a short goal,
numbered steps, a starter with 1-5 ``___`` blanks, progressive hints, hidden
checks with feedback, and a success message - each in English and Arabic.

One definition is the single source of truth for its exercise:

* the official solution is the starter with each blank replaced by its
  answer, so the two can never drift apart;
* a runnable Python exercise is graded by *behavioural* checks on the values
  the program computes, so any correct implementation of a blank passes;
* an exercise whose libraries the sandbox does not install (PyTorch,
  Transformers, FastAPI, ...) is graded statically: each blank must be one of
  its accepted expressions, compared as syntax trees, and nothing executes;
* a configuration file (YAML, Dockerfile, shell, HCL, ...) is graded by one
  whitespace-tolerant pattern per blank.

Applied by the loader after the Arabic files are attached, so the Arabic
source hash (which covers the English exercise text) is unaffected.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from app.services.code_grading.authoring import count_python_blanks
from app.services.code_grading.sql_grader import sql_blank_values
from app.services.code_grading.blanks import canonical_dump, computed_blank_tests

from ..spec import CourseSpec

# (English, Arabic)
Text = Tuple[str, str]

BLANK = "___"
TEXT_LANGUAGES = frozenset({"bash", "dockerfile", "hcl", "ini", "sparql", "yaml"})


@dataclass(frozen=True)
class Guided:
    goal: Text
    steps: Tuple[Text, ...]
    starter: str
    answers: Tuple[str, ...]
    hints: Tuple[Text, ...]
    success: Text
    # Behavioural checks (see the helpers below). Empty = graded statically.
    checks: Tuple[Dict[str, Any], ...] = ()
    # Feedback per blank, used by static and text grading ("Blank 2: ...").
    blanks: Tuple[Text, ...] = ()
    # 1-based blank number -> further accepted answers (static/text grading).
    alternatives: Dict[int, Tuple[str, ...]] = field(default_factory=dict)
    expected: Optional[Text] = None
    reflect: Optional[Text] = None
    language: str = "python"
    pre: Optional[str] = None
    # SQL only: the hidden fixture and the rows the completed query must return.
    sql_setup: Optional[str] = None
    sql_columns: Tuple[str, ...] = ()
    sql_rows: Tuple[Tuple[Any, ...], ...] = ()
    sql_ordered: bool = True


# ─── Check helpers ─────────────────────────────────────────────────────────

def _fb(en: str, ar: str) -> Dict[str, str]:
    return {"en": en, "ar": ar}


def eq(variable: str, expected: Any, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "value_equals", "variable": variable, "expected": expected, "feedback": _fb(en, ar)}


def near(variable: str, expected: float, en: str, ar: str, tol: float = 1e-6) -> Dict[str, Any]:
    return {
        "type": "value_approx", "variable": variable, "expected": expected,
        "abs_tol": tol, "rel_tol": tol, "feedback": _fb(en, ar),
    }


def kind(variable: str, type_name: str, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "type_equals", "variable": variable, "expected": type_name, "feedback": _fb(en, ar)}


def length(variable: str, expected: int, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "list_length", "variable": variable, "expected": expected, "feedback": _fb(en, ar)}


def has_key(variable: str, key: str, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "dict_contains_key", "variable": variable, "key": key, "feedback": _fb(en, ar)}


def frame_shape(variable: str, shape: List[int], en: str, ar: str) -> Dict[str, Any]:
    return {"type": "dataframe_shape", "variable": variable, "expected": shape, "feedback": _fb(en, ar)}


def frame_columns(variable: str, columns: List[str], en: str, ar: str, ordered: bool = True) -> Dict[str, Any]:
    return {
        "type": "dataframe_columns", "variable": variable, "expected": columns,
        "ordered": ordered, "feedback": _fb(en, ar),
    }


def column_values(variable: str, column: str, values: List[Any], en: str, ar: str) -> Dict[str, Any]:
    return {
        "type": "dataframe_column_values", "variable": variable, "column": column,
        "expected": values, "feedback": _fb(en, ar),
    }


def prints(text: str, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "stdout_contains", "expected": text, "feedback": _fb(en, ar)}


def returns(function: str, args: List[Any], expected: Any, en: str, ar: str,
            kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "type": "return_value_equals", "function": function, "args": args,
        "kwargs": kwargs or {}, "expected": expected, "feedback": _fb(en, ar),
    }


def check(expression: str, expected: Any, en: str, ar: str) -> Dict[str, Any]:
    """A hidden one-line expression evaluated after the learner's program, so
    a check can observe behaviour (``bool(np.allclose(...))``) without its
    code appearing in the starter."""
    if "\n" in expression:
        raise ValueError("a check expression must fit on one line")
    return {"type": "expression_equals", "expression": expression, "expected": expected, "feedback": _fb(en, ar)}


def calls(function: str, en: str, ar: str) -> Dict[str, Any]:
    """The program calls ``function`` (dotted names allowed). Read statically."""
    return {"type": "function_called", "function": function, "static": True, "feedback": _fb(en, ar)}


def never_calls(function: str, en: str, ar: str) -> Dict[str, Any]:
    return {"type": "function_not_called", "function": function, "static": True, "feedback": _fb(en, ar)}


# ─── Building one exercise ─────────────────────────────────────────────────

def _blank_paths(tree: ast.AST) -> List[List[Any]]:
    """AST paths of every ``___`` name, in source order."""
    found: List[Tuple[int, int, List[Any]]] = []

    def walk(node: ast.AST, path: List[Any]) -> None:
        if isinstance(node, ast.Name) and node.id == BLANK:
            found.append((node.lineno, node.col_offset, path))
            return
        for name, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                walk(value, [*path, name])
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, ast.AST):
                        walk(item, [*path, name, index])

    walk(tree, [])
    return [path for _line, _column, path in sorted(found, key=lambda item: (item[0], item[1]))]


def _expression_dump(source: str) -> str:
    return ast.dump(ast.parse(source.strip(), mode="eval").body, include_attributes=False)


def _canonical_expression_dump(source: str) -> str:
    return canonical_dump(ast.parse(source.strip(), mode="eval").body)


def fill(starter: str, answers: Tuple[str, ...]) -> str:
    """The starter with each blank, in order, replaced by its answer."""
    pieces = starter.split(BLANK)
    if len(pieces) - 1 != len(answers):
        raise ValueError(f"starter has {len(pieces) - 1} blanks but {len(answers)} answers")
    out = pieces[0]
    for answer, rest in zip(answers, pieces[1:]):
        out += answer + rest
    return out


def _text_blank_tests(guided: Guided) -> List[Dict[str, Any]]:
    """One whitespace-tolerant, whole-line pattern per blank."""
    tests: List[Dict[str, Any]] = []
    lines = [line for line in guided.starter.splitlines() if BLANK in line]
    if sum(line.count(BLANK) for line in lines) != len(lines):
        raise ValueError("a configuration exercise may have at most one blank per line")
    for number, (line, answer) in enumerate(zip(lines, guided.answers), start=1):
        before, after = line.split(BLANK)
        options = [answer, *guided.alternatives.get(number, ())]
        tolerant = lambda text: r"\s+".join(re.escape(part) for part in text.strip().split())  # noqa: E731
        # "re:<pattern>" accepts any value the pattern matches (a commit
        # message, your own registry namespace); anything else is literal.
        option_pattern = lambda option: option[3:] if option.startswith("re:") else tolerant(option)  # noqa: E731
        lead = tolerant(before)
        tail = tolerant(after)
        pattern = (
            r"^\s*" + lead + (r"\s*" if before.strip() else "")
            + "(?:" + "|".join(option_pattern(option) for option in options) + ")"
            + (r"\s*" + tail if after.strip() else "") + r"\s*$"
        )
        re.compile(pattern)
        en, ar = guided.blanks[number - 1]
        tests.append({
            "id": f"blank_{number}", "type": "regex_all", "patterns": [pattern],
            "feedback": _fb(f"Blank {number}: {en}", f"الفراغ {number}: {ar}"),
        })
    return tests


def _python_blank_tests(guided: Guided) -> List[Dict[str, Any]]:
    paths = _blank_paths(ast.parse(guided.starter, mode="exec"))
    tests: List[Dict[str, Any]] = []
    for number, (path, answer) in enumerate(zip(paths, guided.answers), start=1):
        en, ar = guided.blanks[number - 1]
        tests.append({
            "id": f"blank_{number}", "type": "ast_contains", "static": True,
            "path": path, "expected_ast": _expression_dump(answer),
            "expected_ast_any": [_expression_dump(option) for option in guided.alternatives.get(number, ())],
            # The same answers with keyword arguments in name order: ``f(b=2, a=1)``
            # is the same call as ``f(a=1, b=2)``.
            "expected_ast_canonical": [
                _canonical_expression_dump(option)
                for option in (answer, *guided.alternatives.get(number, ()))
            ],
            "label": f"blank {number}",
            "feedback": _fb(f"Blank {number}: {en}", f"الفراغ {number}: {ar}"),
        })
    return tests


def _sql_tests(guided: Guided) -> List[Dict[str, Any]]:
    tests: List[Dict[str, Any]] = []
    for number, answer in enumerate(guided.answers, start=1):
        en, ar = guided.blanks[number - 1]
        tests.append({
            "id": f"blank_{number}", "type": "sql_blank", "blank": number,
            "accepted": [answer, *guided.alternatives.get(number, ())],
            "feedback": _fb(f"Blank {number}: {en}", f"الفراغ {number}: {ar}"),
        })
    tests.append({
        "id": "query_result", "type": "sql_result", "setup_sql": guided.sql_setup,
        # The learner sees bare ___ blanks; the grader finds each answer by
        # lining the submission up against this starter.
        "template": guided.starter,
        "expected_columns": list(guided.sql_columns),
        "expected_rows": [list(row) for row in guided.sql_rows],
        "ordered": guided.sql_ordered,
        "feedback": _fb(
            "The query runs, but its columns or rows do not match the required result.",
            "يعمل الاستعلام، لكن أعمدته أو صفوفه لا تطابق النتيجة المطلوبة.",
        ),
    })
    return tests


COMPUTED_FEEDBACK = (
    "Blank {n}: compute this value from the program's own variables instead of typing its result in.",
    "الفراغ {n}: احسب هذه القيمة من متغيرات البرنامج نفسها بدلًا من كتابة نتيجتها مباشرةً.",
)


def _check_problems(exercise_id: str, solution: str, tests: List[Dict[str, Any]]) -> List[str]:
    """Problems with an executed exercise's checks that would otherwise only
    show up as learners failing for nothing."""
    from app.services.code_execution.isolated_python_runner import MAX_OBSERVATIONS, builtins_used
    from app.services.code_execution.python_runner import ForbiddenCode, bound_names, validate_python_source
    from app.services.code_grading.grader import grading_test_problems

    problems = list(grading_test_problems(tests))
    bound = bound_names(ast.parse(solution, mode="exec"))
    observations = 0
    variables = set()
    for test in tests:
        if test.get("type") in {"expression_equals", "return_value_equals"}:
            observations += 1
        if test.get("variable"):
            variables.add(str(test["variable"]))
        if test.get("type") == "expression_equals":
            expression = str(test.get("expression") or "")
            try:
                validate_python_source(expression)
            except (SyntaxError, ForbiddenCode) as exc:
                problems.append(f"check {test.get('id')}: {exc}")
                continue
            # The driver evaluates a check's builtins as the real builtins; a
            # check must therefore never mean a program name that is also a
            # builtin's name.
            clashes = sorted(set(builtins_used(expression)) & bound)
            if clashes:
                problems.append(f"check {test.get('id')} reads {clashes}, which the solution redefines")
    if observations + len(variables) > MAX_OBSERVATIONS:
        problems.append(f"{observations + len(variables)} observed values exceed the runner's {MAX_OBSERVATIONS}")
    return problems


def _section(title: str, body: str) -> str:
    return f"**{title}**\n\n{body}" if body else ""


def _brief(guided: Guided, ar: bool) -> str:
    pick = 1 if ar else 0
    steps = "\n".join(f"{index}. {step[pick]}" for index, step in enumerate(guided.steps, start=1))
    parts = [
        guided.goal[pick],
        _section("التعليمات" if ar else "Instructions", steps),
        _section("المخرَج المتوقع" if ar else "Expected output", guided.expected[pick] if guided.expected else ""),
        _section("فكّر في الأمر" if ar else "Think about it", guided.reflect[pick] if guided.reflect else ""),
    ]
    return "\n\n".join(part for part in parts if part)


def build(exercise_id: str, guided: Guided) -> Dict[str, Any]:
    """The canonical exercise fields for one definition. Raises ValueError on
    an inconsistent definition, so a broken entry stops the import."""
    blank_count = guided.starter.count(BLANK)
    if not 1 <= blank_count <= 5:
        raise ValueError(f"{exercise_id}: a guided starter needs 1-5 blanks, found {blank_count}")
    if len(guided.answers) != blank_count:
        raise ValueError(f"{exercise_id}: {blank_count} blanks but {len(guided.answers)} answers")
    if not guided.hints or not guided.steps:
        raise ValueError(f"{exercise_id}: needs steps and at least one hint")
    starter = guided.starter
    solution = fill(starter, guided.answers)
    language = guided.language
    if language == "python":
        if count_python_blanks(guided.starter) != blank_count:
            raise ValueError(f"{exercise_id}: every ___ must be an expression (none in comments or strings)")
        ast.parse(solution, mode="exec")
        if guided.checks:
            tests = [dict(check) for check in guided.checks]
            for number, test in enumerate(tests, start=1):
                test.setdefault("id", f"check_{number}")
            problems = _check_problems(exercise_id, solution, tests)
            if problems:
                raise ValueError(f"{exercise_id}: " + "; ".join(problems))
            # A blank whose value the checks only ever see once can be passed
            # by typing that value in. These guards, after the behavioural
            # checks, ask for the computation itself.
            tests += computed_blank_tests(guided.starter, guided.answers, [
                _fb(COMPUTED_FEEDBACK[0].format(n=number), COMPUTED_FEEDBACK[1].format(n=number))
                for number in range(1, blank_count + 1)
            ])
        else:
            if len(guided.blanks) != blank_count:
                raise ValueError(f"{exercise_id}: a statically graded exercise needs feedback for every blank")
            tests = _python_blank_tests(guided)
    elif language in TEXT_LANGUAGES:
        if len(guided.blanks) != blank_count:
            raise ValueError(f"{exercise_id}: a configuration exercise needs feedback for every blank")
        tests = _text_blank_tests(guided) + [dict(check) for check in guided.checks]
    elif language == "sql":
        if len(guided.blanks) != blank_count or not guided.sql_setup or not guided.sql_columns:
            raise ValueError(f"{exercise_id}: a SQL exercise needs blank feedback, a fixture and expected columns")
        tests = _sql_tests(guided)
        read_back = sql_blank_values(starter, solution) or []
        if [value.strip() for value in read_back] != [answer.strip() for answer in guided.answers]:
            raise ValueError(f"{exercise_id}: the answers cannot be read back from the completed query")
    else:
        raise ValueError(f"{exercise_id}: unsupported guided language {language!r}")
    for number, test in enumerate(tests, start=1):
        test.setdefault("id", f"check_{number}")
    return {
        "exercise_type": "code",
        "language": language,
        "starter_code": starter,
        "solution_code": solution,
        "tests": tests,
        "pre_exercise_code": guided.pre,
        "hint": "\n\n".join(hint[0] for hint in guided.hints),
        "hint_ar": "\n\n".join(hint[1] for hint in guided.hints),
        "success_message": guided.success[0],
        "success_message_ar": guided.success[1],
        "description": _brief(guided, ar=False),
        "description_ar": _brief(guided, ar=True),
    }


def registry() -> Dict[str, Guided]:
    """Every guided definition, keyed by canonical exercise id."""
    from . import catalog
    return catalog.ALL


def apply_guided_exercises(course: CourseSpec) -> None:
    definitions = registry()
    for lesson in course.lessons:
        for exercise in lesson.exercises:
            guided = definitions.get(exercise.exercise_id)
            if guided is None:
                continue
            try:
                fields = build(exercise.exercise_id, guided)
            except (SyntaxError, ValueError) as exc:
                course.structure_problems.append(f"{exercise.exercise_id}: invalid guided exercise ({exc})")
                continue
            for name, value in fields.items():
                setattr(exercise, name, value)
