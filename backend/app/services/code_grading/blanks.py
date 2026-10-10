"""Where a fill-in-the-blank answer sits in a learner's program, and whether
the learner computed it or typed its result in.

A behavioural check observes what a program computes. When a blank's value
is computed once, at module level, from fixed data (``round(partial / full,
4)``), the checks see the same number whether the learner wrote the
computation or typed ``0.1349`` - the learner can copy the sample output and
pass. An audit of the curriculum found 183 such blanks in 98 exercises.

``blank_computed`` closes that gap. It is generated for every blank whose
official answer is computed from the program's own values, and it fails only
when that exact slot - located by its path in the starter, and confirmed by
the statement around it being otherwise unchanged - holds a constant. A
learner who restructured the program is never failed by it: when the slot
cannot be confirmed, the check passes and the behavioural checks decide.
"""
from __future__ import annotations

import ast
import builtins
import copy
from typing import Any, Iterable

BLANK = "___"
_BUILTIN_NAMES = frozenset(dir(builtins))
# Nodes that make an expression depend on something other than literals.
_DYNAMIC_NODES = (
    ast.Name, ast.Attribute, ast.Call, ast.Subscript, ast.Lambda, ast.NamedExpr,
    ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom,
)


def node_at(tree: ast.AST, path: Iterable[Any]) -> Any:
    node: Any = tree
    try:
        for part in path:
            node = node[int(part)] if isinstance(node, list) else getattr(node, str(part))
    except (AttributeError, IndexError, TypeError, ValueError):
        return None
    return node


def _replace_at(root: ast.AST, path: list[Any], replacement: ast.AST) -> bool:
    if not path:
        return False
    parent = node_at(root, path[:-1])
    last = path[-1]
    try:
        if isinstance(parent, list):
            parent[int(last)] = replacement
        elif isinstance(parent, ast.AST) and hasattr(parent, str(last)):
            setattr(parent, str(last), replacement)
        else:
            return False
    except (IndexError, TypeError, ValueError):
        return False
    return True


def is_constant_expression(node: ast.AST) -> bool:
    """True when the expression is built only from literals (``0.1349``,
    ``3 / 6``, ``[0, 1, 2]``, ``"done"``): nothing in it reads the program."""
    return isinstance(node, ast.expr) and not any(isinstance(item, _DYNAMIC_NODES) for item in ast.walk(node))


def masked_statement_dump(statement: ast.AST, slots: Iterable[Iterable[Any]]) -> str:
    """The statement with each blank slot replaced by ``___``."""
    masked = copy.deepcopy(statement)
    for slot in slots:
        _replace_at(masked, list(slot), ast.Name(id=BLANK, ctx=ast.Load()))
    return ast.dump(masked, include_attributes=False)


def blank_paths(tree: ast.AST) -> list[list[Any]]:
    """AST paths of every ``___`` name, in source order."""
    found: list[tuple[int, int, list[Any]]] = []

    def walk(node: ast.AST, path: list[Any]) -> None:
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


def statement_path(tree: ast.AST, path: list[Any]) -> list[Any]:
    """The path of the innermost statement that contains ``path``."""
    best: list[Any] = []
    for length in range(1, len(path) + 1):
        if isinstance(node_at(tree, path[:length]), ast.stmt):
            best = path[:length]
    return best


def computed_blank_tests(
    starter: str, answers: tuple[str, ...], feedback: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """One ``blank_computed`` test per blank whose official answer reads the
    program's own values. ``feedback[i]`` is the message for blank ``i + 1``."""
    tree = ast.parse(starter, mode="exec")
    paths = blank_paths(tree)
    solution_bound = _program_names(starter, answers)
    tests: list[dict[str, Any]] = []
    for number, (path, answer) in enumerate(zip(paths, answers), start=1):
        try:
            expression = ast.parse(answer.strip(), mode="eval").body
        except SyntaxError:
            continue  # not a standalone expression (``*args``): nothing to compare
        if is_constant_expression(expression):
            continue
        reads = {
            node.id for node in ast.walk(expression)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }
        if not (reads & solution_bound):
            # Only modules, builtins and literals (``math.sqrt(2)``): a learner
            # may legitimately write the same value another way (``2 ** 0.5``).
            continue
        statement = statement_path(tree, path)
        slots = [p[len(statement):] for p in paths if p[:len(statement)] == statement]
        tests.append({
            "id": f"blank_{number}_computed", "type": "blank_computed", "static": True,
            "path": path, "statement": statement,
            "context": masked_statement_dump(node_at(tree, statement), slots),
            "slots": slots,
            "feedback": feedback[number - 1],
        })
    return tests


def _program_names(starter: str, answers: tuple[str, ...]) -> set[str]:
    """Names the official program binds itself (variables, functions,
    parameters, loop targets) - not imports and not builtins."""
    from app.services.code_execution.python_runner import bound_names

    pieces = starter.split(BLANK)
    solution = pieces[0] + "".join(answer + rest for answer, rest in zip(answers, pieces[1:]))
    tree = ast.parse(solution, mode="exec")
    imported = {
        alias.asname or alias.name.split(".", 1)[0]
        for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    return bound_names(tree) - imported - _BUILTIN_NAMES


def blank_is_computed(tree: ast.AST, test: dict[str, Any]) -> bool:
    """False only when the confirmed blank slot holds a constant."""
    statement = node_at(tree, test.get("statement") or [])
    if not isinstance(statement, ast.stmt):
        return True
    if masked_statement_dump(statement, test.get("slots") or []) != test.get("context"):
        return True  # the learner reshaped this statement: behaviour decides
    node = node_at(tree, test.get("path") or [])
    return not (isinstance(node, ast.AST) and is_constant_expression(node))


def canonical_dump(node: ast.AST) -> str:
    """``ast.dump`` with keyword arguments in name order, so
    ``f(b=2, a=1)`` and ``f(a=1, b=2)`` compare equal."""
    canonical = copy.deepcopy(node)
    for item in ast.walk(canonical):
        if isinstance(item, ast.Call) and all(keyword.arg is not None for keyword in item.keywords):
            item.keywords.sort(key=lambda keyword: keyword.arg or "")
    return ast.dump(canonical, include_attributes=False)
