"""Source rules for learner Python, applied before anything executes.

This is defense-in-depth, not the sandbox. The security boundary for learner
code is the isolated project runner (see isolated_python_runner.py and
docs/project-lab.md): its own container, no network, read-only filesystem,
seccomp and gVisor in production. These rules stop the obvious misuse early,
with a clear message, and keep a development machine's runner honest.

``LocalPythonRunner`` (development and tests) lives in isolated_python_runner
and is re-exported here for the callers that import it from this module.
"""
from __future__ import annotations

import ast
from typing import Any


_ALLOWED_IMPORT_ROOTS = {
    "math", "statistics", "decimal", "fractions", "random", "re", "json",
    "collections", "itertools", "functools", "datetime", "string", "typing",
    "dataclasses", "enum",
    "numpy", "pandas", "sklearn", "scipy",
}
# Read-only view for callers that explain what the sandbox can run.
ALLOWED_IMPORT_ROOTS = frozenset(_ALLOWED_IMPORT_ROOTS)
_BLOCKED_CALLS = {
    "open", "exec", "eval", "compile", "__import__", "input", "breakpoint",
    "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr",
}
_BLOCKED_ROOTS = {
    "os", "sys", "subprocess", "socket", "pathlib", "shutil", "tempfile",
    "multiprocessing", "ctypes", "resource", "signal", "importlib", "builtins",
}
# Dunder names a program may legitimately read. Every other one
# (``__builtins__``, ``__loader__``, ``__spec__``, ``__import__`` ...) hands
# out the interpreter's internals, which the rules below exist to withhold.
_ALLOWED_DUNDER_NAMES = {"__name__", "__file__", "__doc__"}
# Attributes without a leading underscore that still reach an interpreter
# frame (and through it the globals and builtins of any module) or load
# native code.
_ESCAPE_ATTRIBUTES = {
    "gi_frame", "gi_code", "cr_frame", "cr_code", "ag_frame", "ag_code",
    "f_globals", "f_locals", "f_builtins", "f_back", "f_code", "tb_frame", "tb_next",
    "ctypeslib", "load_library",
}
_BLOCKED_ATTRIBUTES = _BLOCKED_ROOTS | _ESCAPE_ATTRIBUTES | {
    "system", "popen", "spawn", "fork", "kill", "unlink", "remove", "rmdir",
    "read_csv", "read_pickle", "read_excel", "read_parquet", "read_json",
    "to_csv", "to_pickle", "to_excel", "to_parquet", "to_json", "load", "save", "savez",
}


# Builtins that hand out the interpreter itself (code execution, attribute
# access by name, namespaces, files). Merely naming one - ``g = getattr`` and
# later ``g(obj, name)`` - is the same as calling it.
_REFERENCE_BLOCKED = _BLOCKED_CALLS - {"input", "dir"}
_COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
_FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


class ForbiddenCode(ValueError):
    pass


# Deeper than any real exercise program. Grading steps that recurse over the
# syntax tree (ast.unparse, ast.dump, copy.deepcopy) would otherwise exceed
# Python's recursion limit inside the API on a crafted 1 + 1 + ... chain.
MAX_SYNTAX_DEPTH = 120
_TOO_DEEP = "your code is nested too deeply for Python to read"


def parse_learner_python(source: str) -> ast.Module:
    """``ast.parse`` for submitted code that never raises anything but
    SyntaxError: a parser stack overflow or an absurdly deep tree becomes a
    syntax error instead of an API failure."""
    try:
        tree: ast.Module | None = ast.parse(source or "", mode="exec")
    except (RecursionError, MemoryError):
        tree = None
    if tree is not None:
        pending: list[tuple[ast.AST, int]] = [(tree, 0)]
        while pending:
            node, depth = pending.pop()
            if depth > MAX_SYNTAX_DEPTH:
                tree = None
                break
            pending.extend((child, depth + 1) for child in ast.iter_child_nodes(node))
    if tree is None:
        error = SyntaxError(_TOO_DEEP)
        error.lineno = 1
        raise error
    return tree


def bound_names(tree: ast.AST) -> set[str]:
    """Every name a program binds anywhere: assignment, def, class, parameter,
    import, and loop/comprehension/with/except/match targets."""
    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            bound.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bound.update(alias.asname or alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            bound.add(node.name)
    return bound


def _local_names(scope: ast.AST) -> set[str]:
    """Names local to one function, lambda or comprehension scope. Inside it
    such a name can never fall back to the builtin of the same name (Python
    raises UnboundLocalError instead), unlike a module-level name whose
    binding may never run (``if False: getattr = None``)."""
    if isinstance(scope, _COMPREHENSIONS):
        return {
            node.id for generator in scope.generators for node in ast.walk(generator.target)
            if isinstance(node, ast.Name)
        }
    arguments = scope.args
    names = {argument.arg for argument in (
        *arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs,
        *(item for item in (arguments.vararg, arguments.kwarg) if item is not None),
    )}
    declared: set[str] = set()
    pending: list[ast.AST] = list(scope.body) if isinstance(scope.body, list) else [scope.body]
    while pending:
        node = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
            pending.extend(node.decorator_list)
            continue  # its body is another scope
        if isinstance(node, (ast.Lambda, *_COMPREHENSIONS)):
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(alias.asname or alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            declared.update(node.names)
        pending.extend(ast.iter_child_nodes(node))
    return names - declared


def _check_builtin_references(tree: ast.AST) -> None:
    """Refuse any reference to a dangerous builtin that is not provably the
    learner's own local name. Iterative, so deeply nested code cannot make
    the API itself run out of stack."""
    pending: list[tuple[ast.AST, tuple[frozenset[str], ...]]] = [(tree, ())]
    while pending:
        node, scopes = pending.pop()
        if isinstance(node, _FUNCTIONS):
            # Decorators, defaults and annotations are evaluated in the
            # enclosing scope (``typing.get_type_hints`` hands annotations back).
            arguments = node.args
            every = (*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs,
                     *(item for item in (arguments.vararg, arguments.kwarg) if item is not None))
            outer = [*getattr(node, "decorator_list", []), *arguments.defaults,
                     *(item for item in arguments.kw_defaults if item is not None),
                     *(item.annotation for item in every if item.annotation is not None),
                     *([node.returns] if getattr(node, "returns", None) is not None else [])]
            pending.extend((item, scopes) for item in outer)
            inner = (*scopes, frozenset(_local_names(node)))
            body = node.body if isinstance(node.body, list) else [node.body]
            pending.extend((item, inner) for item in body)
            continue
        if isinstance(node, _COMPREHENSIONS):
            inner = (*scopes, frozenset(_local_names(node)))
            pending.extend((item, inner) for item in ast.iter_child_nodes(node))
            continue
        if (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in _REFERENCE_BLOCKED
                and not any(node.id in scope for scope in scopes)):
            raise ForbiddenCode(f"Using '{node.id}' is not allowed in exercises.")
        pending.extend((item, scopes) for item in ast.iter_child_nodes(node))


def validate_python_source(source: str) -> ast.AST:
    tree = parse_learner_python(source)
    _check_builtin_references(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id.startswith("__") and node.id.endswith("__"):
            # ``__builtins__.open(...)`` and ``__loader__.load_module(...)``
            # would bypass every call rule below, and no exercise needs them.
            if node.id == "__builtins__" or (
                isinstance(node.ctx, ast.Load) and node.id not in _ALLOWED_DUNDER_NAMES
            ):
                raise ForbiddenCode(f"Using '{node.id}' is not allowed in exercises.")
        if isinstance(node, (ast.Global, ast.Nonlocal)) and "__builtins__" in node.names:
            raise ForbiddenCode("Using '__builtins__' is not allowed in exercises.")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for module in modules:
                root = module.split(".", 1)[0]
                if root not in _ALLOWED_IMPORT_ROOTS:
                    raise ForbiddenCode(f"Importing '{root}' is not allowed in exercises.")
            for alias in node.names:
                name = alias.asname or alias.name.split(".", 1)[0]
                if name.startswith("_") or name in _BLOCKED_ROOTS:
                    raise ForbiddenCode(f"Importing '{name}' is not allowed in exercises.")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _BLOCKED_CALLS:
                raise ForbiddenCode(f"Calling '{node.func.id}' is not allowed in exercises.")
            if isinstance(node.func, ast.Attribute):
                root = node.func
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in _BLOCKED_ROOTS:
                    raise ForbiddenCode(f"Calling '{root.id}.{node.func.attr}' is not allowed in exercises.")
        if isinstance(node, ast.Attribute):
            pieces = []
            current: ast.AST = node
            while isinstance(current, ast.Attribute):
                pieces.append(current.attr)
                current = current.value
            if any(piece.startswith("_") for piece in pieces):
                raise ForbiddenCode("Private attribute access is not allowed in exercises.")
            if any(piece in _BLOCKED_ATTRIBUTES for piece in pieces):
                raise ForbiddenCode(f"Attribute '{node.attr}' is not allowed in exercises.")
    return tree


def validate_check_expressions(calls: list[dict[str, Any]] | None) -> None:
    """Hidden checks come from exercise definitions, not from learners, but
    they run beside learner code and obey the same source rules."""
    for request in calls or []:
        if "expression" in request:
            expression = str(request["expression"])
            ast.parse(expression, mode="eval")
            validate_python_source(expression)


def __getattr__(name: str) -> Any:
    # Lazy: the local runner is built on the isolated runner, which imports
    # the rules above from this module.
    if name == "LocalPythonRunner":
        from .isolated_python_runner import LocalPythonRunner
        return LocalPythonRunner
    raise AttributeError(name)
