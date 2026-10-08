"""
Learner code shares an interpreter with the harness, so it can always write its
own "result" to the harness's private result pipe and exit before the harness
reports (project_runner/harness.py says so). These tests prove that ability buys
nothing: a forged result is an observation like any other, and the trusted
outcome - a passed Check Step, task progress, artifacts kept - is decided
server-side against expected values the sandbox never sees.
"""
import json

from app.models.project_lab import LabTaskProgress

from tests.test_project_lab import API, _check, _put, _register, _start, lab, reference_facts  # noqa: F401

# Finds every pipe it can write to (the private result channel is one of them)
# and writes the forged payload there, then dies before the harness can speak.
FORGER = """
import json, os, stat
payload = {payload}.replace("__BIG__", "A" * (4 * 1024 * 1024)).encode()
for fd in range(3, 256):
    try:
        if stat.S_ISFIFO(os.fstat(fd).st_mode):
            os.write(fd, payload)
    except OSError:
        pass
os._exit(0)
"""


def _forger(result: dict) -> str:
    return FORGER.replace("{payload}", repr(json.dumps(result, default=str)))


def test_a_forged_success_with_the_right_real_data_answers_does_not_pass(client, db, lab):
    facts = reference_facts()
    # The strongest forger: it knows the exact answers for the visible data
    # (anyone can compute them once and hard-code them) and asserts success.
    forged = {
        "status": "success", "error": None, "stdout": "", "stderr": "",
        "captured": {"row_counts": dict(facts.row_counts), "order_date_range": list(facts.order_date_range)},
        "generated_files": [],
    }
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/inspect_data.py", _forger(forged))

    result = _check(client, headers, attempt_id, "profile-the-tables")
    by_id = {c["id"]: c for c in result["checks"]}
    # The forgery is accepted as an observation for the real data...
    assert by_id["row_counts_values"]["passed"] is True
    # ...but the hidden variant run receives the same forged answers.
    assert by_id["computed_from_data"]["passed"] is False
    assert result["outcome"] == "fail" and not result.get("newly_completed")
    assert db.query(LabTaskProgress).filter_by(attempt_id=attempt_id, status="completed").count() == 0


def test_a_forged_artifact_list_is_bounded_and_sanitised_by_the_server(client, lab):
    forged = {
        "status": "success", "error": None, "stdout": "", "stderr": "", "captured": {},
        "generated_files": (
            [{"path": "../../etc/passwd", "media_type": "text/plain", "encoding": "text", "content": "x", "size": 1},
             {"path": "charts/x.html", "media_type": "text/html", "encoding": "text",
              "content": "<script>alert(1)</script>", "size": 25},
             {"path": "charts/big.png", "media_type": "image/png", "encoding": "base64",
              "content": "__BIG__", "size": 3 * 1024 * 1024}]
            + [{"path": f"out/f{i}.txt", "media_type": "text/plain", "encoding": "text", "content": "ok", "size": 2}
               for i in range(40)]
        ),
    }
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", _forger(forged))
    response = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers)
    assert response.status_code == 200, response.text
    files = response.json()["generated_files"]
    # Control: the forged list really arrived (otherwise the bounds prove nothing).
    assert any(f["path"].startswith("out/f") for f in files), files
    assert len(files) <= 10
    assert all(".." not in f["path"].split("/") for f in files)
    assert all(f.get("media_type") in (None, "image/png", "image/jpeg", "text/plain") for f in files)
    html = next((f for f in files if f["path"] == "charts/x.html"), None)
    assert html is None or html.get("content") is None
    big = next((f for f in files if f["path"] == "charts/big.png"), None)
    assert big is None or big.get("content") is None
