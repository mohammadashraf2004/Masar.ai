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
MAX_ANSWER_CHARS = 10_000            # all blank answers together, beyond the starter
_SLOTS = asyncio.Semaphore(MAX_CONCURRENT)


async def _execute_off_loop(code: str, test: dict[str, Any]) -> ExecutionResult:
    async with _SLOTS:
        return await asyncio.to_thread(SQLGrader._execute, code, test)


def _tolerant(piece: str) -> str:
    """Fixed starter text as a pattern; any whitespace run may differ."""
    return r"\s*".join(re.escape(token) for token in piece.split())


def _piece_pattern(piece: str, *, last: bool) -> re.Pattern[str]:
    """The starter text that ends a blank."""
    body = _tolerant(piece)
    if not body and not last:
        # Two blanks separated only by whitespace: split at the line break the
        # starter puts between them, or else at the first space.
        body = r"[ \t]*\n\s*" if "\n" in piece else r"\s+"
    return re.compile(body + (r"\s*\Z" if last else ""))


def _value_end(code: str, start: int, piece: re.Pattern[str]) -> re.Match[str] | None:
    """Where the fixed text after a blank begins.

    The first place outside any string, comment or parentheses the learner
    opened inside the blank, so ``COALESCE(a, b)`` or ``'a, b'`` does not end
    a blank at its comma. A blank with an unclosed quote falls back to the
    first place at all.
    """
    depth, quote, index = 0, "", start
    while index <= len(code):
        if not quote and depth == 0 and (match := piece.match(code, index)):
            return match
        if index == len(code):
            break
        char = code[index]
        if quote:
            quote = "" if char == quote else quote
        elif char in "'\"`":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif code.startswith("--", index):
            newline = code.find("\n", index)
            index = len(code) - 1 if newline < 0 else newline - 1
        elif code.startswith("/*", index):
            close = code.find("*/", index + 2)
            index = len(code) - 1 if close < 0 else close + 1
        index += 1
    return piece.search(code, start)


def sql_blank_values(template: str, code: str) -> list[str] | None:
    """What the learner wrote in each ``___`` of ``template``, in order.

    The starter shows bare ``___`` blanks, so each answer is found by lining
    the submission up against the starter text around it. ``None`` when the
    learner changed that surrounding text and the blanks can no longer be
    told apart.
    """
    pieces = template.split("___")
    # Answers are short; a submission far longer than its starter was rewritten,
    # and bounding it keeps the matching below cheap.
    if len(pieces) < 2 or len(code) > len(template) + MAX_ANSWER_CHARS:
        return None
    head = re.compile(r"\s*" + _tolerant(pieces[0])).match(code)
    if head is None:
        return None
    values, position = [], head.end()
    for number, piece in enumerate(pieces[1:], start=1):
        # Skip the layout before the answer, so a line break between two
        # blanks ends the first one only after something was written in it.
        start = position
        while start < len(code) and code[start].isspace():
            start += 1
        match = _value_end(code, start, _piece_pattern(piece, last=number == len(pieces) - 1))
        if match is None:
            return None
        values.append(code[position:match.start()])
        position = match.end()
    return values


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
    depth. Each blank's answer is read by lining the submission up against
    the starter (the ``template`` on a test), so the grader can report the
    first incorrect field before running the query. Submissions made from the
    older marked starters (``/* blank:N */ ___ /* endblank */``) are still
    read by their markers.
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

        result_test = next((test for test in tests if test.get("type") == "sql_result"), None)
        if result_test is not None and any(test.get("type") == "sql_blank" for test in tests):
            return await self._grade_by_result(code, tests, required, result_test)

        fields = self._fields(code, tests)
        passed = 0
        execution = empty
        for index, test in enumerate(tests):
            kind = test.get("type")
            if kind == "sql_blank":
                ok = self._blank_matches(fields, test)
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

    async def _grade_by_result(
        self, code: str, tests: list[dict[str, Any]], required: list[dict[str, Any]],
        result_test: dict[str, Any],
    ) -> GradingResult:
        """Blanks guide the learner; the query's result decides.

        An empty blank is reported before running anything. Once every blank
        is filled, any query that returns the expected result passes, even if
        a field is written differently from the accepted answers. When the
        result is wrong, the first field that differs from them is named.
        """
        blanks = [(index, test) for index, test in enumerate(tests) if test.get("type") == "sql_blank"]
        fields = self._fields(code, tests)
        for done, (index, test) in enumerate(blanks):
            if not self._blank_filled(fields, code, test):
                return self._blank_failure(test, index, done, len(required))
        execution = await _execute_off_loop(code, result_test)
        if not execution.succeeded:
            return GradingResult(
                execution.status, False, execution.status.upper(),
                {"en": execution.stderr, "ar": execution.stderr},
                str(result_test.get("id") or "result"), 0, len(required), execution,
            )
        if execution.detail == "match":
            return GradingResult(
                "correct", True, "CORRECT", {"en": "Correct!", "ar": "إجابة صحيحة!"},
                None, len(required), len(required), execution,
            )
        # A rewritten scaffold has no blanks to name; the result alone speaks.
        for done, (index, test) in enumerate(blanks if fields is not None else []):
            if not self._blank_matches(fields, test):
                failure = self._blank_failure(test, index, done, len(required))
                failure.execution = execution
                return failure
        return GradingResult(
            "incorrect", False, "TEST_FAILED",
            result_test.get("feedback") or {
                "en": "The query does not produce the expected result.",
                "ar": "لا ينتج الاستعلام النتيجة المتوقعة.",
            },
            str(result_test.get("id") or "result"), len(blanks), len(required), execution,
        )

    @staticmethod
    def _blank_failure(test: dict[str, Any], index: int, passed: int, total: int) -> GradingResult:
        return GradingResult(
            "incorrect", False, "BLANK_INCORRECT",
            test.get("feedback") or {
                "en": "The query does not produce the expected result.",
                "ar": "لا ينتج الاستعلام النتيجة المتوقعة.",
            },
            str(test.get("id") or f"test_{index + 1}"), passed, total, ExecutionResult("success"),
        )

    @staticmethod
    def _fields(code: str, tests: list[dict[str, Any]]) -> dict[int, str] | None:
        """Blank number -> what the learner wrote there; ``None`` if unreadable."""
        marked = _BLANK.findall(code)
        if marked:
            return {int(number): value for number, value in marked}
        template = next((test["template"] for test in tests if isinstance(test.get("template"), str)), None)
        values = sql_blank_values(template, code) if template else None
        return None if values is None else dict(enumerate(values, start=1))

    @staticmethod
    def _blank_filled(fields: dict[int, str] | None, code: str, test: dict[str, Any]) -> bool:
        actual = (fields or {}).get(int(test.get("blank", 0)))
        if actual is None:
            # Scaffold rewritten: the result test decides, unless blanks remain.
            return "___" not in code
        return bool(actual.strip()) and "___" not in actual

    @staticmethod
    def _blank_matches(fields: dict[int, str] | None, test: dict[str, Any]) -> bool:
        actual = (fields or {}).get(int(test.get("blank", 0)), "")
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
