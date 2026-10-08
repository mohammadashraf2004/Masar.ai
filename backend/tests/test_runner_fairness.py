"""
One account must not be able to monopolise the shared runner (audit finding #5):
parallel requests from one account (tabs, scripts) get one execution at a time,
and sustained use is capped by a rolling per-account budget of runner seconds.
Other accounts are unaffected.
"""
import asyncio

import httpx
import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.services import code_exercises, execution_fairness
from app.services.code_execution import ExecutionResult
from app.services.execution_fairness import runner_turn

from tests.test_code_exercise_api import _register, code_exercise  # noqa: F401
from tests.test_project_lab import lab  # noqa: F401


@pytest.fixture(autouse=True)
def _fresh_store():
    execution_fairness._store = execution_fairness._MemoryStore()
    yield
    execution_fairness._store = None


def test_one_account_holds_one_runner_turn_at_a_time():
    async def scenario():
        async with runner_turn(1):
            with pytest.raises(HTTPException) as busy:
                async with runner_turn(1):
                    pass
            assert busy.value.status_code == 429
            assert busy.value.detail["code"] == "RUNNER_BUSY_FOR_ACCOUNT"
            async with runner_turn(2):  # another account is not affected
                pass
        async with runner_turn(1):  # released afterwards
            pass
    asyncio.run(scenario())


def test_sustained_use_is_capped_by_the_rolling_budget(monkeypatch):
    monkeypatch.setattr(settings, "RUNNER_USER_SECONDS", 3)

    async def scenario():
        for _ in range(3):  # every turn is charged at least one second
            async with runner_turn(7):
                pass
        with pytest.raises(HTTPException) as spent:
            async with runner_turn(7):
                pass
        assert spent.value.status_code == 429
        assert spent.value.detail["code"] == "RUNNER_BUDGET_EXHAUSTED"
        assert int(spent.value.headers["Retry-After"]) > 0
        async with runner_turn(8):
            pass
    asyncio.run(scenario())


def _slow_runner(monkeypatch, seconds=0.4):
    state = {"now": 0, "peak": 0, "calls": 0}

    async def run(code, **_):
        state["now"] += 1
        state["calls"] += 1
        state["peak"] = max(state["peak"], state["now"])
        await asyncio.sleep(seconds)
        state["now"] -= 1
        return ExecutionResult("success", stdout="ok\n")

    monkeypatch.setattr(code_exercises.RUNNER, "run", run)
    return state


async def _burst(app, exercise_id, headers_list, per_account=6):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        requests = [
            client.post(f"/api/v1/practice/exercises/{exercise_id}/run", headers=headers, json={"code": "print(1)"})
            for headers in headers_list for _ in range(per_account)
        ]
        return await asyncio.gather(*requests)


def test_parallel_requests_from_one_account_run_one_at_a_time(client, code_exercise, monkeypatch):
    state = _slow_runner(monkeypatch)
    _, headers = _register(client)
    responses = asyncio.run(_burst(client.app, code_exercise.id, [headers]))
    codes = sorted(r.status_code for r in responses)
    assert state["peak"] == 1, state
    assert codes.count(200) >= 1 and set(codes) <= {200, 429}, codes
    assert any(r.status_code == 429 and r.json()["detail"]["code"] == "RUNNER_BUSY_FOR_ACCOUNT" for r in responses)


def test_other_accounts_still_get_their_turn(client, code_exercise, monkeypatch):
    state = _slow_runner(monkeypatch)
    accounts = [_register(client)[1] for _ in range(3)]
    responses = asyncio.run(_burst(client.app, code_exercise.id, accounts, per_account=1))
    assert [r.status_code for r in responses] == [200, 200, 200]
    assert state["calls"] == 3


def test_an_account_that_spent_its_budget_is_refused_with_retry_after(client, code_exercise, monkeypatch):
    _slow_runner(monkeypatch, seconds=0)
    monkeypatch.setattr(settings, "RUNNER_USER_SECONDS", 2)
    _, headers = _register(client)
    url = f"/api/v1/practice/exercises/{code_exercise.id}/run"
    assert client.post(url, headers=headers, json={"code": "print(1)"}).status_code == 200
    assert client.post(url, headers=headers, json={"code": "print(1)"}).status_code == 200
    refused = client.post(url, headers=headers, json={"code": "print(1)"})
    assert refused.status_code == 429 and refused.json()["detail"]["code"] == "RUNNER_BUDGET_EXHAUSTED"
    assert refused.headers.get("Retry-After")
    _, other = _register(client)
    assert client.post(url, headers=other, json={"code": "print(1)"}).status_code == 200


def test_sql_grading_in_the_api_process_is_bounded_in_memory_and_time():
    """SQL exercises run in-process: one learner query must not allocate
    hundreds of MB or hold a worker for seconds (both measured before the fix:
    ~900 MB and 5.6 s for a single printf padding)."""
    import time

    from app.services.code_grading.sql_grader import SQLGrader

    test = {"type": "sql_result", "setup_sql": "CREATE TABLE t(x); INSERT INTO t VALUES (1);",
            "expected_rows": [[1]]}
    grader = SQLGrader()

    async def run(query):
        started = time.monotonic()
        result = await grader.run(query, [test])
        return result, time.monotonic() - started

    blob, _ = asyncio.run(run("SELECT length(zeroblob(900000000))"))
    assert blob.status != "success" and "too big" in blob.stderr
    padded, seconds = asyncio.run(run("SELECT length(printf('%.*c', 900000000, 'x'))"))
    assert seconds < 1.0 and padded.detail != "match"
    recursive, seconds = asyncio.run(run(
        "WITH RECURSIVE r(n, s) AS (SELECT 1, zeroblob(900000) UNION ALL "
        "SELECT n + 1, zeroblob(900000) FROM r WHERE n < 4000) SELECT count(*) FROM r ORDER BY 1"))
    assert recursive.status in {"timeout", "syntax_error"} and seconds < 2.0
    ok, _ = asyncio.run(run("SELECT x FROM t"))
    assert ok.status == "success" and ok.detail == "match"


class _AllInFlight:
    """Hold every fake execution until `expected` are waiting on the runner at the same
    time, sample the pool once at that instant, then let them all finish. Sampling later
    would also count requests that already left the runner and are doing their normal,
    short post-run DB work - not what "pinned during the wait" means."""

    def __init__(self, engine, expected: int):
        self.engine, self.expected, self.waiting = engine, expected, 0
        self.sample = None
        self._event = None

    async def checkpoint(self):
        if self._event is None:
            self._event = asyncio.Event()
        self.waiting += 1
        if self.waiting == self.expected and self.sample is None:
            self.sample = self.engine.pool.checkedout()
            self._event.set()
        try:
            await asyncio.wait_for(self._event.wait(), timeout=5)
        except asyncio.TimeoutError:
            pass


def test_waiting_on_the_runner_does_not_pin_pooled_connections(client, code_exercise, monkeypatch):
    """Audit finding #10: async handlers held an open transaction (a pooled
    connection) for the whole runner wait; with enough learners in flight a
    worker's pool ran dry and the next checkout blocked its event loop."""
    from app.db.session import engine, get_db

    gate = _AllInFlight(engine, expected=5)

    async def run(code, **_):
        await gate.checkpoint()
        return ExecutionResult("success", stdout="ok\n")

    monkeypatch.setattr(code_exercises.RUNNER, "run", run)
    accounts = [_register(client)[1] for _ in range(5)]
    override = client.app.dependency_overrides.pop(get_db)  # real per-request sessions
    try:
        responses = asyncio.run(_burst(client.app, code_exercise.id, accounts, per_account=1))
    finally:
        client.app.dependency_overrides[get_db] = override
    assert [r.status_code for r in responses] == [200] * 5
    # Five runs waiting at once: pinned connections would show 6 (5 + the test's own session).
    assert gate.sample is not None and gate.sample <= 1, gate.sample


def test_project_lab_run_and_check_do_not_pin_connections_while_executing(client, lab, monkeypatch):
    from app.db.session import engine, get_db
    from app.services.project_lab.execution import ProjectExecutionService, get_execution_service
    from project_runner.executor import JobOutcome

    from tests.test_project_lab import _put, _register as _lab_register, _start, solution

    # One execution per account can be in flight (lease + runner turn): four accounts.
    gate = _AllInFlight(engine, expected=4)

    class SlowBackend:
        name = "slow"

        async def execute(self, job):
            await gate.checkpoint()
            return JobOutcome("success", captured={})

    accounts = []
    for _ in range(4):
        _, headers = _lab_register(client)
        attempt_id = _start(client, headers, lab)
        _put(client, headers, attempt_id, "analysis/inspect_data.py", solution("analysis/inspect_data.py"))
        accounts.append((headers, attempt_id))

    client.app.dependency_overrides[get_execution_service] = lambda: ProjectExecutionService(SlowBackend())
    override = client.app.dependency_overrides.pop(get_db)
    try:
        async def burst():
            transport = httpx.ASGITransport(app=client.app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
                # One request per account (two Runs, two Check Steps), so every request is a
                # real in-flight execution: a request refused for a busy lease would still be
                # inside its own short pre-lease DB work at the sampling instant.
                calls = []
                for index, (headers, attempt_id) in enumerate(accounts):
                    if index % 2 == 0:
                        calls.append(http.post(f"/api/v1/project-lab/attempts/{attempt_id}/run",
                                               json={"path": "analysis/inspect_data.py"}, headers=headers))
                    else:
                        calls.append(http.post(
                            f"/api/v1/project-lab/attempts/{attempt_id}/tasks/profile-the-tables/check",
                            json={"language": "en"}, headers=headers))
                return await asyncio.gather(*calls)
        responses = asyncio.run(burst())
    finally:
        client.app.dependency_overrides[get_db] = override
        client.app.dependency_overrides.pop(get_execution_service, None)
    assert [r.status_code for r in responses] == [200] * 4, [r.text for r in responses]
    # Four executions waiting at once: pinned connections would show 5 (4 + the test's session).
    assert gate.sample is not None and gate.sample <= 1, gate.sample
