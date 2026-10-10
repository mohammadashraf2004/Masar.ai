"""Security regressions for the learner source rules (python_runner.py).

These rules are defense in depth - the isolated runner is the boundary - but
in development they are the only barrier, and every bypass below executed
before the 2026-10-10 audit.
"""
import pytest

from app.services.code_execution.python_runner import ForbiddenCode, validate_check_expressions, validate_python_source


@pytest.mark.parametrize("source", [
    "__builtins__.open('/etc/hostname').read()",
    "print(__builtins__)",
    "__builtins__ = {}",
    "global __builtins__",
    "__loader__.load_module('posix')",
    "spec = __spec__",
    "imp = __import__",
    "g = getattr\ng(1, 'real')",
    "run = eval",
    "funcs = [open]",
    "reader = compile",
    "names = globals",
    # A module-level binding may never run, so the builtin stays reachable.
    "if False:\n    getattr = None\ng = getattr",
    "vars = 1\ndel vars\nv = vars",
    "class A:\n    g = getattr",
    # Annotations, defaults and decorators are evaluated outside the function.
    "def f(x: getattr):\n    pass",
    "def f(x=getattr):\n    pass",
    "def outer():\n    def inner():\n        return eval\n    return inner",
    "x = [getattr for _ in range(1)]",
    "gen = (x for x in [1])\nframe = gen.gi_frame.f_globals",
    "def f():\n    pass\nf.__code__",
    "import numpy as np\nnp.ctypeslib.load_library('libc', '.')",
    "import os",
    "from importlib import import_module",
    "open('x')",
])
def test_known_bypasses_are_refused(source):
    with pytest.raises(ForbiddenCode):
        validate_python_source(source)


@pytest.mark.parametrize("source", [
    "if __name__ == '__main__':\n    print(__file__, __doc__)",
    "class Model:\n    __tablename__ = 'models'\n",
    "dir = 'up'\nprint(dir)",
    "def f(vars):\n    return vars\nprint(f(1))",
    "def g():\n    open = 'door'\n    return open",
    "def outer():\n    compile = 1\n    def inner():\n        return compile\n    return inner",
    "x = [vars for vars in range(3)]",
    "f = lambda open: open + 1",
    "import numpy as np\nnp.array([1, 2]).sum()",
    "import pandas as pd\ndf = pd.DataFrame({'a': [1]})\nprint(df.to_dict())",
    "items = sorted([3, 1])\nprint(len(items))",
])
def test_ordinary_exercise_code_is_still_allowed(source):
    validate_python_source(source)


@pytest.mark.parametrize("terms", [5_000, 200_000])
def test_absurdly_deep_code_is_a_syntax_error_not_an_api_failure(terms):
    # Python 3.11's own parser overflows its stack on this; the API must
    # answer "Python could not read your code", never a 500.
    with pytest.raises(SyntaxError, match="nested too deeply"):
        validate_python_source("x = " + " + ".join(["1"] * terms))


def test_the_grader_reports_deep_code_as_a_syntax_error():
    import asyncio

    from app.services.code_grading import PythonGrader

    tests = [{"type": "value_equals", "variable": "x", "expected": 1, "feedback": "x"}]
    result = asyncio.run(PythonGrader().grade("x = " + " + ".join(["1"] * 5_000), tests))
    assert (result.status, result.feedback_code) == ("syntax_error", "SYNTAX_ERROR")
    assert "nested too deeply" in result.feedback["en"]


def test_hidden_check_expressions_obey_the_same_rules():
    validate_check_expressions([{"expression": "sorted(names) == ['a']"}])
    with pytest.raises(ForbiddenCode):
        validate_check_expressions([{"expression": "__builtins__"}])
