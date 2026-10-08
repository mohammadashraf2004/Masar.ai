"""Restricted local Python runner.

This is a development runner and defense-in-depth, not a production sandbox.
The interface deliberately permits replacing it with a container/microVM
service without changing grading or API code.
"""
from __future__ import annotations

import ast
import asyncio
import json
import os
import subprocess
import sys
import tempfile
import time
from typing import Any

from .base import CodeRunner, ExecutionResult


_ALLOWED_IMPORT_ROOTS = {
    "math", "statistics", "decimal", "fractions", "random", "re", "json",
    "collections", "itertools", "functools", "datetime", "string", "typing",
    "numpy", "pandas", "sklearn",
}
_BLOCKED_CALLS = {
    "open", "exec", "eval", "compile", "__import__", "input", "breakpoint",
    "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr",
}
_BLOCKED_ROOTS = {
    "os", "sys", "subprocess", "socket", "pathlib", "shutil", "tempfile",
    "multiprocessing", "ctypes", "resource", "signal", "importlib", "builtins",
}


class ForbiddenCode(ValueError):
    pass


def validate_python_source(source: str) -> ast.AST:
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError:
        raise
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for module in modules:
                root = module.split(".", 1)[0]
                if root not in _ALLOWED_IMPORT_ROOTS:
                    raise ForbiddenCode(f"Importing '{root}' is not allowed in exercises.")
            for alias in node.names:
                bound = alias.asname or alias.name.split(".", 1)[0]
                if bound.startswith("_") or bound in _BLOCKED_ROOTS:
                    raise ForbiddenCode(f"Importing '{bound}' is not allowed in exercises.")
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
            current = node
            while isinstance(current, ast.Attribute):
                pieces.append(current.attr)
                current = current.value
            if any(piece.startswith("_") for piece in pieces):
                raise ForbiddenCode("Private attribute access is not allowed in exercises.")
            blocked_attributes = _BLOCKED_ROOTS | {
                "system", "popen", "spawn", "fork", "kill", "unlink", "remove", "rmdir",
                "read_csv", "read_pickle", "read_excel", "read_parquet", "read_json",
                "to_csv", "to_pickle", "to_excel", "to_parquet", "to_json", "load", "save", "savez",
            }
            if any(piece in blocked_attributes for piece in pieces):
                raise ForbiddenCode(f"Attribute '{node.attr}' is not allowed in exercises.")
    return tree


_CHILD = r'''
import contextlib, io, json, traceback

class LimitedBuffer(io.StringIO):
    def __init__(self, limit):
        super().__init__(); self.limit = limit; self.used = 0; self.truncated = False
    def write(self, value):
        value = str(value); remaining = self.limit - self.used
        if remaining <= 0:
            self.truncated = True; return len(value)
        piece = value[:remaining]; self.used += len(piece)
        if len(piece) < len(value): self.truncated = True
        return super().write(piece)
    def result(self):
        return self.getvalue() + ("\n[output truncated]" if self.truncated else "")

def safe(value, depth=0):
    if depth > 5: return {"kind": "repr", "type": type(value).__name__, "repr": "<depth limit>"}
    if value is None or isinstance(value, (bool, int, float, str)):
        return {"kind": "value", "type": type(value).__name__, "value": value}
    if isinstance(value, (list, tuple)):
        return {"kind": "value", "type": type(value).__name__, "value": [safe(v, depth+1).get("value", safe(v, depth+1).get("repr")) for v in value[:100]]}
    if isinstance(value, dict):
        items = list(value.items())[:100]
        return {"kind": "value", "type": type(value).__name__, "value": {str(k): safe(v, depth+1).get("value", safe(v, depth+1).get("repr")) for k, v in items}}
    if hasattr(value, "columns") and hasattr(value, "shape"):
        data = {"columns": [str(c) for c in list(value.columns)], "shape": list(value.shape)}
        try: data["column_values"] = {str(c): value[c].tolist()[:100] for c in value.columns}
        except Exception: pass
        return {"kind": "dataframe", "type": type(value).__name__, "value": data}
    return {"kind": "repr", "type": type(value).__name__, "repr": repr(value)[:2000]}

payload = json.loads(input())
out, err, ns = LimitedBuffer(payload["output_limit"]), LimitedBuffer(payload["output_limit"]), {"__name__": "__exercise__"}
result = {"status": "success", "stdout": "", "stderr": "", "variables": {}, "return_values": {}}
try:
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        if payload.get("pre_code"): exec(compile(payload["pre_code"], "<setup>", "exec"), ns, ns)
        exec(compile(payload["code"], "<learner>", "exec"), ns, ns)
        for request in payload.get("calls", []):
            key = request["key"]
            try:
                fn = ns.get(request["function"])
                result["return_values"][key] = safe(fn(*request.get("args", []), **request.get("kwargs", {}))) if callable(fn) else {"missing": True}
            except Exception as exc:
                result["return_values"][key] = {"error": f"{type(exc).__name__}: {exc}"}
    for name in payload.get("variables", []):
        result["variables"][name] = safe(ns[name]) if name in ns else {"missing": True}
except SyntaxError as exc:
    result["status"] = "syntax_error"; err.write("".join(traceback.format_exception_only(type(exc), exc)))
except Exception as exc:
    result["status"] = "runtime_error"; err.write("".join(traceback.format_exception_only(type(exc), exc)))
result["stdout"], result["stderr"] = out.result(), err.result()
print(json.dumps(result, ensure_ascii=False, allow_nan=False))
'''


def _limits(memory_bytes: int, cpu_seconds: int):
    def apply() -> None:
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
            resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
            resource.setrlimit(resource.RLIMIT_NOFILE, (16, 16))
        except (ImportError, OSError, ValueError):
            pass
    return apply


class LocalPythonRunner(CodeRunner):
    def __init__(self, *, timeout_seconds: float = 3.0, memory_mb: int = 512, output_limit: int = 16_384):
        self.timeout_seconds = timeout_seconds
        self.memory_bytes = memory_mb * 1024 * 1024
        self.output_limit = output_limit

    async def run(self, code: str, *, pre_exercise_code: str = "", variables=None, calls=None) -> ExecutionResult:
        started = time.perf_counter()
        try:
            validate_python_source(code)
        except SyntaxError as exc:
            return ExecutionResult("syntax_error", stderr=f"SyntaxError: {exc.msg} (line {exc.lineno})")
        except ForbiddenCode as exc:
            return ExecutionResult("forbidden_operation", stderr=str(exc), detail=str(exc))
        try:
            validate_python_source(pre_exercise_code)
        except (SyntaxError, ForbiddenCode) as exc:
            return ExecutionResult("execution_error", stderr="Exercise setup is invalid.", detail=str(exc))

        payload = json.dumps({
            "code": code, "pre_code": pre_exercise_code, "variables": variables or [],
            "calls": calls or [], "output_limit": self.output_limit,
        }, ensure_ascii=False).encode()
        kwargs: dict[str, Any] = {
            "stdin": asyncio.subprocess.PIPE, "stdout": asyncio.subprocess.PIPE,
            "stderr": asyncio.subprocess.PIPE,
        }
        if os.name == "posix":
            kwargs["preexec_fn"] = _limits(self.memory_bytes, max(1, int(self.timeout_seconds)))
        elif os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        with tempfile.TemporaryDirectory(prefix="masar-exercise-") as workdir:
            try:
                process = await asyncio.create_subprocess_exec(
                    sys.executable, "-I", "-c", _CHILD, cwd=workdir,
                    env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}, **kwargs,
                )
                stdout, stderr = await asyncio.wait_for(process.communicate(payload + b"\n"), self.timeout_seconds)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ExecutionResult("timeout", stderr="Execution exceeded the time limit.", execution_time_ms=int((time.perf_counter()-started)*1000))
            except Exception as exc:
                return ExecutionResult("execution_error", stderr="The execution service failed.", detail=str(exc))
        elapsed = int((time.perf_counter() - started) * 1000)
        if process.returncode and not stdout:
            status = "memory_limit" if process.returncode < 0 else "execution_error"
            return ExecutionResult(status, stderr=stderr.decode("utf-8", "replace")[:self.output_limit], execution_time_ms=elapsed)
        try:
            data = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return ExecutionResult("execution_error", stderr="The execution service returned an invalid result.", execution_time_ms=elapsed)
        return ExecutionResult(
            data.get("status", "execution_error"), data.get("stdout", "")[:self.output_limit],
            data.get("stderr", "")[:self.output_limit], elapsed, data.get("variables", {}),
            data.get("return_values", {}),
        )
