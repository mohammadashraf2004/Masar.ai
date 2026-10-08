"""Deterministic, read-only SQL grading against isolated in-memory fixtures."""
from __future__ import annotations

import asyncio
import re
import sqlite3
import time
from typing import Any

from app.services.code_execution import ExecutionResult
from .grader import GradingResult


SQL_TEST_TYPES = frozenset({"sql_blank", "sql_result"})
_BLANK = re.compile(r"/\*\s*blank:(\d+)\s*\*/(.*?)/\*\s*endblank\s*\*/", re.I | re.S)
_LEADING_COMMENT = re.compile(r"\A(?:\s|--[^\n]*(?:\n|$)|/\*.*?\*/)*", re.S)

# Learner SQL runs inside the API process, so its cost must be bounded there.
# The VM-step deadline alone is not enough: one step such as
# printf('%.*c', 900000000, 'x') or zeroblob() allocates hundreds of MB and runs
# for seconds before the progress handler is ever consulted.
MAX_VALUE_BYTES = 1_000_000          # any one string/blob/row
MAX_SQL_BYTES = 100_000              # fixture + learner statement text
HEAP_LIMIT_BYTES = 128 * 1024 * 1024  # process-wide: this grader is the API's only SQLite user
MAX_CONCURRENT = 2                   # per worker; queries run off the event loop
_SLOTS = asyncio.Semaphore(MAX_CONCURRENT)


async def _execute_off_loop(code: str, test: dict[str, Any]) -> ExecutionResult:
    async with _SLOTS:
        return await asyncio.to_thread(SQLGrader._execute, code, test)


def normalize_sql_fragment(value: str) -> str:
    """Normalize case and insignificant spacing without changing SQL meaning."""
    value = re.sub(r"--[^\n]*", " ", value)
    value = re.sub(r"/\*.*?\*/", " ", value, flags=re.S)
    value = value.strip().rstrip(";").lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*([(),=<>+*/%-])\s*", r"\1", value)
    return value


class SQLGrader:
    """Grade SQL without touching Masar's application database.

    Author-provided fixture SQL is loaded into a new ``:memory:`` SQLite
    connection. Learner code must be one SELECT/WITH statement; query-only
    mode, an authorizer, a VM-step deadline, and a row cap provide defense in
    depth. Blank markers let the grader report the first incorrect field before
    running the query.
    """

    async def run(self, code: str, tests: list[dict[str, Any]]) -> ExecutionResult:
        result_test = next((test for test in tests if test.get("type") == "sql_result"), None)
        if not result_test:
            return ExecutionResult("success", stdout="SQL syntax is checked when you submit.\n")
        return await _execute_off_loop(code, result_test)

    async def grade(self, code: str, tests: list[dict[str, Any]], **_: Any) -> GradingResult:
        required = [test for test in tests if test.get("required", True)]
        empty = ExecutionResult("success")
        if not required:
            return GradingResult(
                "grading_error", False, "INVALID_TEST_CONFIGURATION",
                {"en": "This exercise has no required tests.", "ar": "لا يحتوي هذا التمرين على اختبارات مطلوبة."},
                None, 0, 0, empty,
            )

        passed = 0
        execution = empty
        for index, test in enumerate(tests):
            kind = test.get("type")
            if kind == "sql_blank":
                ok = self._blank_matches(code, test)
            elif kind == "sql_result":
                execution = await _execute_off_loop(code, test)
                if not execution.succeeded:
                    return GradingResult(
                        execution.status, False, execution.status.upper(),
                        {"en": execution.stderr, "ar": execution.stderr},
                        str(test.get("id") or f"test_{index + 1}"), passed, len(required), execution,
                    )
                ok = bool(execution.detail == "match")
            else:
                ok = False
            if ok:
                if test.get("required", True):
                    passed += 1
                continue
            if not test.get("required", True):
                continue
            return GradingResult(
                "incorrect", False,
                "BLANK_INCORRECT" if kind == "sql_blank" else "TEST_FAILED",
                test.get("feedback") or {
                    "en": "The query does not produce the expected result.",
                    "ar": "لا ينتج الاستعلام النتيجة المتوقعة.",
                },
                str(test.get("id") or f"test_{index + 1}"), passed, len(required), execution,
            )
        return GradingResult(
            "correct", True, "CORRECT", {"en": "Correct!", "ar": "إجابة صحيحة!"},
            None, passed, len(required), execution,
        )

    @staticmethod
    def _blank_matches(code: str, test: dict[str, Any]) -> bool:
        wanted = int(test.get("blank", 0))
        fields = {int(number): value for number, value in _BLANK.findall(code)}
        actual = fields.get(wanted, "")
        if not actual.strip() or "___" in actual:
            return False
        normalized = normalize_sql_fragment(actual)
        return normalized in {
            normalize_sql_fragment(str(value)) for value in test.get("accepted", [])
        }

    @staticmethod
    def _execute(code: str, test: dict[str, Any]) -> ExecutionResult:
        started = time.perf_counter()
        visible = _LEADING_COMMENT.sub("", code)
        if not re.match(r"(?is)^(select|with)\b", visible):
            return ExecutionResult(
                "forbidden_operation", stderr="Only one read-only SELECT or WITH query is allowed.",
            )
        if len(code) > MAX_SQL_BYTES:
            return ExecutionResult("output_limit", stderr="The query is too long.")
        connection = sqlite3.connect(":memory:", check_same_thread=False)
        connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, MAX_VALUE_BYTES)
        connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, MAX_SQL_BYTES)
        connection.execute(f"PRAGMA hard_heap_limit = {HEAP_LIMIT_BYTES}")
        connection.execute("PRAGMA temp_store = MEMORY")
        deadline = time.monotonic() + 0.5
        try:
            connection.executescript(str(test.get("setup_sql") or ""))
            connection.execute("PRAGMA query_only = ON")
            denied = {
                getattr(sqlite3, name) for name in (
                    "SQLITE_INSERT", "SQLITE_UPDATE", "SQLITE_DELETE", "SQLITE_ALTER_TABLE",
                    "SQLITE_DROP_TABLE", "SQLITE_DROP_INDEX", "SQLITE_DROP_VIEW", "SQLITE_DROP_TRIGGER",
                    "SQLITE_CREATE_TABLE", "SQLITE_CREATE_INDEX", "SQLITE_CREATE_VIEW", "SQLITE_CREATE_TRIGGER",
                    "SQLITE_ATTACH", "SQLITE_DETACH", "SQLITE_PRAGMA", "SQLITE_TRANSACTION",
                    "SQLITE_SAVEPOINT",
                ) if hasattr(sqlite3, name)
            }
            connection.set_authorizer(
                lambda action, *_: sqlite3.SQLITE_DENY if action in denied else sqlite3.SQLITE_OK
            )
            connection.set_progress_handler(
                lambda: 1 if time.monotonic() > deadline else 0, 1_000,
            )
            cursor = connection.execute(code)
            rows = cursor.fetchmany(501)
            if len(rows) > 500:
                return ExecutionResult("output_limit", stderr="The query returned more than 500 rows.")
            columns = [item[0] for item in cursor.description or []]
        except sqlite3.ProgrammingError as exc:
            return ExecutionResult("syntax_error", stderr=f"SQL error: {exc}")
        except sqlite3.DatabaseError as exc:
            message = str(exc)
            status = "timeout" if "interrupted" in message.lower() else "syntax_error"
            return ExecutionResult(status, stderr=f"SQL error: {message}")
        finally:
            connection.close()

        expected_rows = [tuple(row) for row in test.get("expected_rows", [])]
        actual_rows = [tuple(row) for row in rows]
        ordered = bool(test.get("ordered", False))
        rows_match = actual_rows == expected_rows if ordered else sorted(actual_rows, key=repr) == sorted(expected_rows, key=repr)
        expected_columns = test.get("expected_columns")
        columns_match = expected_columns is None or columns == [str(item) for item in expected_columns]
        rendered = "\t".join(columns) + "\n" + "\n".join("\t".join(str(value) for value in row) for row in rows)
        return ExecutionResult(
            "success", stdout=rendered.rstrip() + "\n", execution_time_ms=int((time.perf_counter() - started) * 1000),
            detail="match" if rows_match and columns_match else "mismatch",
        )
