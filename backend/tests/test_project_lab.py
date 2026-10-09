"""Project Lab: attempts, workspace files, execution, deterministic checks and
progress — against the real API, the real validators and (through the local
development adapter) real Python/SQL execution.

Capstone-specific validator behaviour, concurrency, artifacts and final
submission are covered in test_project_lab_capstone.py.

Every project and track created here uses a unique slug and is deleted at the
end of the test (see the `lab` fixture), per the suite's rule for committed
fixtures.
"""
import copy
import pathlib
import uuid

import pytest

from app.models.learning import CareerTrack
from app.models.project_lab import LabAttempt, LabProject, LabRun, LabSubmission, LabTaskProgress, LabWorkspaceFile
from app.models.wallet import WalletTransaction
from app.services.project_lab.definitions import MASAR_COMMERCE
from app.services.project_lab.execution import (
    DisabledBackend, LocalSubprocessBackend, ProjectExecutionService, get_execution_service,
)
from app.services.project_lab.service import sync_definitions
from app.services.project_lab.templates import load_template
from app.services.project_lab.validators import masar_commerce_facts as facts_module

PASSWORD = "correct-horse-battery-staple-7"
API = "/api/v1/project-lab"
SOLUTION = pathlib.Path(__file__).parent / "project_lab_solutions" / "masar_commerce"

OBJECTIVE = (
    "# Analysis Plan\n\n## Objective\n\n"
    "Show Masar Commerce leadership how revenue, orders and customers developed in 2025 "
    "so they can decide where to invest next year.\n\n"
    "## Stakeholders\n\n"
    "- CEO: needs the overall picture to set next year's priorities.\n"
    "- Head of Sales: needs to know which categories and regions bring revenue.\n"
    "- Head of Marketing: needs to understand repeat buying and customer value.\n"
)


def solution(path: str) -> str:
    """A file of the reference solution (tests only — never in the template)."""
    return (SOLUTION / path).read_text(encoding="utf-8")


def reference_facts():
    """What the private validators expect — computed here only to prove it
    never reaches a response."""
    template = load_template(MASAR_COMMERCE["template_key"])
    return facts_module.analyze({t: template.read_csv(f"data/{t}.csv") for t in facts_module.TABLES})


def _register(client):
    response = client.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True,
        "email": f"lab-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Lab Tester", "password": PASSWORD,
    })
    assert response.status_code == 201, response.text
    body = response.json()
    return body["user"]["id"], {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def lab(db):
    """The real Masar Commerce definition, synced under unique slugs."""
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"lab-track-{suffix}", title="Data Analyst (test)", title_ar="محلل بيانات",
                        estimated_weeks=1)
    db.add(track)
    db.commit()
    definition = copy.deepcopy(MASAR_COMMERCE)
    definition["slug"] = f"masar-commerce-{suffix}"
    definition["track_slug"] = track.slug
    sync_definitions(db, [definition])
    yield definition["slug"]
    db.rollback()
    project = db.query(LabProject).filter_by(slug=definition["slug"]).first()
    if project is not None:
        db.delete(project)
    db.flush()
    db.query(CareerTrack).filter_by(id=track.id).delete()
    db.commit()


@pytest.fixture()
def use_backend(client):
    """Swap the execution backend for one test."""
    def install(backend):
        client.app.dependency_overrides[get_execution_service] = lambda: ProjectExecutionService(backend)
    yield install
    client.app.dependency_overrides.pop(get_execution_service, None)


def _start(client, headers, slug):
    response = client.post(f"{API}/projects/{slug}/start", headers=headers)
    assert response.status_code in (200, 201), response.text
    return response.json()["attempt_id"]


def _put(client, headers, attempt_id, path, content):
    response = client.put(f"{API}/attempts/{attempt_id}/files", params={"path": path},
                          json={"content": content}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def _check(client, headers, attempt_id, task, language="en"):
    response = client.post(f"{API}/attempts/{attempt_id}/tasks/{task}/check",
                           json={"language": language}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


# ─── Projects & starting ─────────────────────────────────────────────────────

MILESTONES = [
    "business-brief", "understand-the-data", "prepare-and-clean", "sql-business-analysis", "core-kpis",
    "customer-analysis", "product-analysis", "time-and-regional-analysis", "data-visualization", "executive-report",
]
EDITABLE = [
    "analysis/clean_data.py", "analysis/customers.py", "analysis/inspect_data.py", "analysis/kpis.py",
    "analysis/products.py", "analysis/trends.py", "analysis/visualize.py", "analysis_plan.md", "findings.md",
    "report.md",
    "sql/monthly_revenue.sql", "sql/price_bands.sql", "sql/product_performance.sql", "sql/regional_performance.sql",
    "sql/revenue_by_category.sql", "sql/top_customers.sql",
]


def test_project_card_and_detail_never_expose_validators(client, lab):
    _, headers = _register(client)
    cards = client.get(f"{API}/projects", headers=headers)
    assert cards.status_code == 200
    card = next(c for c in cards.json() if c["slug"] == lab)
    assert card["title_ar"] == "مسار كوميرس — تحليل أداء الأعمال"
    assert card["milestone_count"] == 10 and card["task_count"] == 29 and card["attempt"] is None
    assert 12 <= card["estimated_hours"] <= 18
    detail = client.get(f"{API}/projects/{lab}", headers=headers)
    assert [m["slug"] for m in detail.json()["milestones"]] == MILESTONES
    overview = detail.json()["overview"]
    assert overview["role"] == "Junior Data Analyst" and overview["role_ar"]
    assert overview["duration_hours"] == [12, 18] and len(overview["skills"]) == 9 and overview["deliverables"]
    for body in (cards.text, detail.text):
        assert "validator" not in body and "masar_commerce." not in body


def test_unknown_project_is_404(client):
    _, headers = _register(client)
    assert client.get(f"{API}/projects/no-such-project", headers=headers).status_code == 404
    assert client.post(f"{API}/projects/no-such-project/start", headers=headers).status_code == 404


def test_requires_authentication(client, lab):
    assert client.get(f"{API}/projects").status_code == 401
    assert client.post(f"{API}/projects/{lab}/start").status_code == 401


def test_start_is_idempotent_and_creates_the_workspace(client, db, lab):
    _, headers = _register(client)
    first = client.post(f"{API}/projects/{lab}/start", headers=headers)
    second = client.post(f"{API}/projects/{lab}/start", headers=headers)
    assert first.status_code == 201 and first.json()["created"] is True
    assert second.status_code == 200 and second.json() == {"attempt_id": first.json()["attempt_id"], "created": False}
    attempt_id = first.json()["attempt_id"]
    assert db.query(LabAttempt).filter_by(id=attempt_id).count() == 1

    stored = sorted(row.path for row in db.query(LabWorkspaceFile).filter_by(attempt_id=attempt_id))
    # Only editable files are stored per learner: no datasets, no README.
    assert stored == EDITABLE
    assert db.query(LabTaskProgress).filter_by(attempt_id=attempt_id, status="not_started").count() == 29

    card = next(c for c in client.get(f"{API}/projects", headers=headers).json() if c["slug"] == lab)
    assert card["attempt"] == {"id": attempt_id, "status": "active", "percent": 0, "completed_tasks": 0,
                               "total_tasks": 29, "submitted_at": None}


def test_attempt_view_has_instructions_but_no_validator(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    response = client.get(f"{API}/attempts/{attempt_id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    task = body["milestones"][4]["tasks"][0]
    assert task["slug"] == "headline-kpis" and task["primary_file"] == "analysis/kpis.py"
    assert body["progress"]["current_task"] == "frame-the-brief"
    assert body["submitted_at"] is None
    for milestone in body["milestones"]:
        for item in milestone["tasks"]:
            # Complete Arabic content and three authored hints on every task.
            assert item["title_ar"] and item["instructions_ar"], item["slug"]
            assert len(item["hints"]) == 3 and all(h["en"] and h["ar"] for h in item["hints"]), item["slug"]
    assert "validator" not in response.text and "masar_commerce." not in response.text


# ─── Workspace files ─────────────────────────────────────────────────────────

def test_workspace_tree_marks_datasets_and_readme_read_only(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    entries = {e["path"]: e for e in client.get(f"{API}/attempts/{attempt_id}/workspace", headers=headers).json()["entries"]}
    for path in ("data/customers.csv", "data/orders.csv", "data/order_items.csv", "data/products.csv", "README.md",
                 "README.ar.md"):
        assert entries[path]["editable"] is False, path
    for path in EDITABLE:
        assert entries[path]["editable"] is True, path
    assert entries["charts"]["kind"] == "dir"
    assert entries["analysis/kpis.py"]["language"] == "python"
    assert entries["sql/revenue_by_category.sql"]["language"] == "sql"
    assert entries["report.md"]["language"] == "markdown"
    assert entries["data/orders.csv"]["language"] == "csv"


def test_reading_files(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    kpis = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"}, headers=headers).json()
    assert kpis["editable"] is True and "kpis = {" in kpis["content"]
    orders = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "data/orders.csv"}, headers=headers).json()
    assert orders["editable"] is False and orders["content"] is None
    assert orders["table"]["columns"][:2] == ["order_id", "customer_id"]
    assert orders["table"]["row_count"] == len(load_template(MASAR_COMMERCE["template_key"]).read_csv("data/orders.csv"))
    assert orders["table"]["truncated"] is True and len(orders["table"]["rows"]) == 100


def test_editing_an_allowed_file(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    saved = _put(client, headers, attempt_id, "analysis/kpis.py", "print('hello')\n")
    assert saved["content"] == "print('hello')\n"
    again = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"}, headers=headers)
    assert again.json()["content"] == "print('hello')\n"
    entries = {e["path"]: e for e in client.get(f"{API}/attempts/{attempt_id}/workspace", headers=headers).json()["entries"]}
    assert entries["analysis/kpis.py"]["modified"] is True
    assert entries["analysis/inspect_data.py"]["modified"] is False


@pytest.mark.parametrize("path", ["data/orders.csv", "README.md", "README.ar.md"])
def test_read_only_files_cannot_be_changed(client, lab, path):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    before = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": path}, headers=headers).json()
    response = client.put(f"{API}/attempts/{attempt_id}/files", params={"path": path},
                          json={"content": "tampered"}, headers=headers)
    assert response.status_code == 403 and response.json()["detail"]["code"] == "READ_ONLY_FILE"
    reset = client.post(f"{API}/attempts/{attempt_id}/files/reset", json={"path": path}, headers=headers)
    assert reset.status_code == 403
    after = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": path}, headers=headers).json()
    assert after == before


@pytest.mark.parametrize("path", [
    "../../etc/passwd", "/etc/passwd", "data/../../secrets.txt", "analysis/../../app/core/config.py",
    "analysis\\..\\..\\x.py", "analysis/./kpis.py", "./report.md", "analysis//kpis.py", ".env",
    "data/.hidden.csv", "report.md\x00.py",
])
def test_path_traversal_and_non_canonical_paths_are_rejected(client, lab, path):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    responses = [
        client.get(f"{API}/attempts/{attempt_id}/files", params={"path": path}, headers=headers),
        client.put(f"{API}/attempts/{attempt_id}/files", params={"path": path}, json={"content": "x"}, headers=headers),
        client.post(f"{API}/attempts/{attempt_id}/files/reset", json={"path": path}, headers=headers),
        client.post(f"{API}/attempts/{attempt_id}/run", json={"path": path}, headers=headers),
    ]
    for response in responses:
        assert response.status_code in (400, 404, 422), (path, response.status_code, response.text)


def test_unknown_but_canonical_file_is_404(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    response = client.put(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/new.py"},
                          json={"content": "x"}, headers=headers)
    assert response.status_code == 404 and response.json()["detail"]["code"] == "FILE_NOT_FOUND"


def test_file_size_is_bounded(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    response = client.put(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"},
                          json={"content": "x" * 200_001}, headers=headers)
    assert response.status_code == 422


def test_reset_restores_one_file_only(client, db, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    template = load_template(MASAR_COMMERCE["template_key"])
    _put(client, headers, attempt_id, "analysis/kpis.py", "kpis = {}\n")
    _put(client, headers, attempt_id, "analysis_plan.md", OBJECTIVE)
    assert _check(client, headers, attempt_id, "frame-the-brief")["outcome"] == "pass"

    reset = client.post(f"{API}/attempts/{attempt_id}/files/reset", json={"path": "analysis/kpis.py"}, headers=headers)
    assert reset.status_code == 200
    assert reset.json()["content"] == template.read_text("analysis/kpis.py")
    plan = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis_plan.md"}, headers=headers).json()
    assert plan["content"] == OBJECTIVE  # untouched
    progress = client.get(f"{API}/attempts/{attempt_id}", headers=headers).json()["progress"]
    assert progress["completed_tasks"] == 1  # reset never touches progress


# ─── Ownership ───────────────────────────────────────────────────────────────

def test_attempts_are_private_to_their_owner(client, lab):
    _, owner = _register(client)
    _, intruder = _register(client)
    attempt_id = _start(client, owner, lab)
    _put(client, owner, attempt_id, "analysis/kpis.py", "secret = 1\n")
    attempts = [
        client.get(f"{API}/attempts/{attempt_id}", headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/workspace", headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"}, headers=intruder),
        client.put(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"},
                   json={"content": "overwritten"}, headers=intruder),
        client.post(f"{API}/attempts/{attempt_id}/files/reset", json={"path": "analysis/kpis.py"}, headers=intruder),
        client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=intruder),
        client.post(f"{API}/attempts/{attempt_id}/tasks/headline-kpis/check", json={}, headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/artifacts", headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/artifacts/content", params={"path": "charts/x.png"}, headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/submission", headers=intruder),
        client.post(f"{API}/attempts/{attempt_id}/submit", headers=intruder),
        client.get(f"{API}/attempts/{attempt_id}/completion", headers=intruder),
    ]
    for response in attempts:
        assert response.status_code == 404, response.text
        assert response.json()["detail"]["code"] == "ATTEMPT_NOT_FOUND"
    assert client.get(f"{API}/attempts/{attempt_id}").status_code == 401
    still = client.get(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/kpis.py"}, headers=owner)
    assert still.json()["content"] == "secret = 1\n"


# ─── Run ─────────────────────────────────────────────────────────────────────

def test_run_python_success_is_free_and_logged(client, db, lab):
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/inspect_data.py", solution("analysis/inspect_data.py"))
    transactions_before = db.query(WalletTransaction).count()
    response = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/inspect_data.py"}, headers=headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "success" and body["kind"] == "python"
    raw_orders = len(load_template(MASAR_COMMERCE["template_key"]).read_csv("data/orders.csv"))
    assert f"'orders': {raw_orders}" in body["stdout"] and body["stderr"] == ""
    assert body["execution_ms"] > 0 and body["generated_files"] == []
    assert body["stdout_truncated"] is False and body["stderr_truncated"] is False
    assert "captured" not in body
    assert db.query(LabRun).filter_by(attempt_id=attempt_id, status="success").count() == 1
    assert db.query(WalletTransaction).count() == transactions_before  # execution never charges credits
    progress = client.get(f"{API}/attempts/{attempt_id}", headers=headers).json()["progress"]
    assert progress["completed_tasks"] == 0  # Run never grants progress


def test_run_runs_the_saved_file_with_a_learner_only_traceback(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "x = 1\ny = {}['missing']\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "error"
    assert 'File "analysis/kpis.py", line 2' in body["stderr"] and "KeyError" in body["stderr"]
    assert "harness" not in body["stderr"] and "project_runner" not in body["stderr"]
    assert body["error"] == {"type": "KeyError", "message": "'missing'", "line": 2}


def test_run_python_syntax_error(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "def broken(:\n    pass\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "error" and body["error"]["type"] == "SyntaxError" and body["error"]["line"] == 1


def test_run_timeout(client, lab, use_backend):
    use_backend(LocalSubprocessBackend(timeout_seconds=2, memory_mb=1024))
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "while True:\n    pass\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "timeout"


def test_run_output_flood_is_truncated_and_flagged(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py",
         "import sys\nfor i in range(200000):\n    print('x' * 100)\n    sys.stderr.write('e' * 100)\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "success"
    assert body["stdout_truncated"] is True and body["stderr_truncated"] is True
    assert len(body["stdout"]) < 70_000 and body["stdout"].endswith("[output truncated]")


def test_run_infrastructure_failure_is_distinguished(client, lab, use_backend):
    use_backend(DisabledBackend())
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "infrastructure_error"



def test_run_sql_queries_the_project_datasets(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "sql/revenue_by_category.sql"},
                       headers=headers).json()
    assert body["status"] == "success" and body["kind"] == "sql"
    assert body["table"]["columns"] == ["category", "order_lines"]
    categories = {row[0] for row in body["table"]["rows"]}
    assert {"Electronics", "Books", "Sports"} <= categories

    _put(client, headers, attempt_id, "sql/revenue_by_category.sql",
         "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status;")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "sql/revenue_by_category.sql"},
                       headers=headers).json()
    assert body["status"] == "success"
    assert [r[0] for r in body["table"]["rows"]] == ["cancelled", "completed", "pending", "returned"]


def test_run_sql_errors_and_file_access_is_blocked(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    for sql in ("SELECT nope FROM orders", "SELECT * FROM read_csv('/etc/passwd')", "COPY orders TO 'x.csv'"):
        _put(client, headers, attempt_id, "sql/revenue_by_category.sql", sql)
        body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "sql/revenue_by_category.sql"},
                           headers=headers).json()
        assert body["status"] == "error", sql
        assert body["stderr"]


def test_run_sql_result_rows_are_limited(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "sql/revenue_by_category.sql", "SELECT * FROM order_items")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "sql/revenue_by_category.sql"},
                       headers=headers).json()
    assert body["status"] == "success"
    assert body["table"]["truncated"] is True and len(body["table"]["rows"]) == 500


def test_markdown_and_datasets_are_not_runnable(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    for path in ("report.md", "data/orders.csv", "README.md"):
        response = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": path}, headers=headers)
        assert response.status_code == 400 and response.json()["detail"]["code"] == "NOT_RUNNABLE"


def test_chart_artifacts_are_returned(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py",
         "import matplotlib.pyplot as plt\nplt.bar(['a', 'b'], [1, 2])\nplt.savefig('charts/kpis.png')\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "success"
    chart = next(f for f in body["generated_files"] if f["path"] == "charts/kpis.png")
    assert chart["media_type"] == "image/png" and chart["encoding"] == "base64" and chart["content"]


def test_learner_code_cannot_modify_the_canonical_dataset(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    template = load_template(MASAR_COMMERCE["template_key"])
    original = template.read_text("data/orders.csv")
    _put(client, headers, attempt_id, "analysis/kpis.py", "open('data/orders.csv', 'a').write('tampered')\n")
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    # Each run gets its own copy of the datasets (mode 0444; the runner's
    # unprivileged user cannot write it — root, as in this test container,
    # can). Either way the canonical template is never the file written.
    assert body["status"] in {"success", "error"}
    assert template.read_text("data/orders.csv") == original


# ─── Check Step ──────────────────────────────────────────────────────────────

def test_plan_check_fails_on_the_template_then_passes(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    first = _check(client, headers, attempt_id, "frame-the-brief")
    assert first["outcome"] == "fail" and first["passed"] is False
    assert {c["id"]: c["passed"] for c in first["checks"]} == {
        "objective_present": True, "objective_written": False,
        "stakeholders_present": True, "stakeholders_written": False, "stakeholders_items": False}
    assert first["task_status"] == "in_progress" and first["newly_completed"] is False

    _put(client, headers, attempt_id, "analysis_plan.md", OBJECTIVE)
    second = _check(client, headers, attempt_id, "frame-the-brief")
    assert second["outcome"] == "pass" and second["newly_completed"] is True
    assert second["task_status"] == "completed"
    assert second["progress"]["completed_tasks"] == 1
    assert second["progress"]["current_task"] == "plan-questions-and-kpis"


def test_inspect_check_passes_with_a_real_solution(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/inspect_data.py", solution("analysis/inspect_data.py"))
    result = _check(client, headers, attempt_id, "profile-the-tables")
    assert result["outcome"] == "pass", result
    assert [c["id"] for c in result["checks"]] == [
        "row_counts_keys", "row_counts_values", "order_date_range", "computed_from_data",
    ]


def _kpi_workspace(client, headers, attempt_id, clean_data=None):
    _put(client, headers, attempt_id, "analysis/clean_data.py", clean_data or solution("analysis/clean_data.py"))
    _put(client, headers, attempt_id, "analysis/kpis.py", solution("analysis/kpis.py"))


CLEAN_ALL_STATUSES = solution("analysis/clean_data.py").replace(
    'completed = orders[orders["status"] == "completed"]', "completed = orders")


def test_kpi_check_pass_updates_progress_once(client, db, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _kpi_workspace(client, headers, attempt_id)
    first = _check(client, headers, attempt_id, "headline-kpis")
    assert first["outcome"] == "pass" and first["newly_completed"] is True, first
    assert all(c["passed"] and c["message"] is None for c in first["checks"])
    milestone = next(m for m in first["progress"]["milestones"] if m["slug"] == "core-kpis")
    assert milestone == {"slug": "core-kpis", "completed_tasks": 1, "total_tasks": 2, "percent": 50}
    assert first["progress"]["percent"] == round(100 / 29)

    row = db.query(LabTaskProgress).filter_by(attempt_id=attempt_id, status="completed").one()
    completed_at = row.completed_at

    second = _check(client, headers, attempt_id, "headline-kpis")
    assert second["outcome"] == "pass" and second["newly_completed"] is False
    assert second["progress"] == first["progress"] | {"tasks": second["progress"]["tasks"]}
    db.refresh(row)
    assert row.check_count == 2 and row.completed_at == completed_at
    assert db.query(LabTaskProgress).filter_by(attempt_id=attempt_id, status="completed").count() == 1
    assert db.query(LabSubmission).filter_by(attempt_id=attempt_id).count() == 2


def test_kpi_check_fail_explains_without_revealing_answers(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _kpi_workspace(client, headers, attempt_id, CLEAN_ALL_STATUSES)
    result = _check(client, headers, attempt_id, "headline-kpis")
    assert result["outcome"] == "fail" and result["passed"] is False and result["error"] is None
    checks = {c["id"]: c for c in result["checks"]}
    assert checks["kpis_defined"]["passed"] is True
    for key in ("revenue", "aov", "completed_orders"):
        assert checks[key]["passed"] is False
        assert checks[key]["message"].startswith("Cancelled, returned or pending orders appear to be included")
    assert checks["computed_from_data"]["passed"] is False
    assert result["task_status"] == "in_progress" and result["progress"]["completed_tasks"] == 0

    expected = reference_facts()
    serialized = str(result)
    for value in (expected.revenue, expected.aov):
        assert f"{value:.2f}" not in serialized and f"{value:,.0f}" not in serialized and str(round(value)) not in serialized
    assert str(expected.completed_orders) not in serialized


def test_kpi_check_arabic_messages(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _kpi_workspace(client, headers, attempt_id, CLEAN_ALL_STATUSES)
    result = _check(client, headers, attempt_id, "headline-kpis", language="ar")
    revenue = next(c for c in result["checks"] if c["id"] == "revenue")
    assert "الطلبات المكتملة" in revenue["message"] and revenue["messages"]["en"].startswith("Cancelled")
    assert revenue["label"] == "الإيرادات المعترف بها"


def test_hard_coded_answers_fail_the_behaviour_check(client, lab):
    """Correct numbers typed in by hand pass the value checks but not the
    re-run on changed data."""
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    expected = reference_facts()
    typed = {"revenue": expected.revenue, "completed_orders": expected.completed_orders, "aov": expected.aov,
             "unique_customers": expected.unique_customers, "items_sold": expected.items_sold}
    _put(client, headers, attempt_id, "analysis/kpis.py", f"kpis = {typed!r}\n")
    result = _check(client, headers, attempt_id, "headline-kpis")
    checks = {c["id"]: c["passed"] for c in result["checks"]}
    assert checks == {"kpis_defined": True, "revenue": True, "completed_orders": True, "aov": True,
                      "unique_customers": True, "items_sold": True, "computed_from_data": False}
    assert result["outcome"] == "fail" and result["task_status"] == "in_progress"


def test_check_execution_error_is_error_not_fail(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "import pandas as pd\nkpis = 1 / 0\n")
    result = _check(client, headers, attempt_id, "headline-kpis")
    assert result["outcome"] == "error" and result["passed"] is False and result["checks"] == []
    assert result["error"]["kind"] == "execution" and "analysis/kpis.py" in result["error"]["message"]
    assert result["run"]["status"] == "error" and "ZeroDivisionError" in result["run"]["stderr"]
    assert "captured" not in str(result["run"])
    assert result["task_status"] == "in_progress" and result["newly_completed"] is False


def test_check_infrastructure_error(client, db, lab, use_backend):
    use_backend(DisabledBackend())
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _kpi_workspace(client, headers, attempt_id)
    result = _check(client, headers, attempt_id, "headline-kpis")
    assert result["outcome"] == "error" and result["error"]["kind"] == "infrastructure"
    assert result["run"] is None and result["newly_completed"] is False
    assert db.query(LabSubmission).filter_by(attempt_id=attempt_id, outcome="error", error_kind="infrastructure").count() == 1


def test_unknown_task_is_404(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    response = client.post(f"{API}/attempts/{attempt_id}/tasks/not-a-task/check", json={}, headers=headers)
    assert response.status_code == 404 and response.json()["detail"]["code"] == "TASK_NOT_FOUND"


# ─── Unit-level guarantees ───────────────────────────────────────────────────

def test_sync_is_idempotent(db, lab):
    definition = copy.deepcopy(MASAR_COMMERCE)
    definition["slug"] = lab
    definition["track_slug"] = db.query(LabProject).filter_by(slug=lab).one().track.slug
    assert sync_definitions(db, [definition]) == {"projects": 0, "milestones": 0, "tasks": 0}


def test_sync_rejects_unknown_validator(db, lab):
    definition = copy.deepcopy(MASAR_COMMERCE)
    definition["slug"] = lab
    definition["track_slug"] = db.query(LabProject).filter_by(slug=lab).one().track.slug
    definition["milestones"][0]["tasks"][0]["validator_key"] = "nope.missing"
    with pytest.raises(RuntimeError, match="unknown validator"):
        sync_definitions(db, [definition])
    db.rollback()


def test_unknown_or_crashing_validator_is_an_infrastructure_error():
    import asyncio

    from app.services.project_lab.execution import WorkspaceSnapshot
    from app.services.project_lab.validation import ValidationContext, _REGISTRY, run_validator

    context = ValidationContext(execution=ProjectExecutionService(DisabledBackend()),
                                snapshot=WorkspaceSnapshot("masar-commerce-analysis", {}),
                                template=load_template("masar-commerce-analysis"), config={})

    async def crashes(ctx):
        raise KeyError("validator bug")

    _REGISTRY["tests.crashes"] = crashes
    try:
        for key in ("tests.not-registered", "tests.crashes"):
            result = asyncio.run(run_validator(key, context))
            assert result.outcome == "error" and result.error_kind == "infrastructure"
    finally:
        _REGISTRY.pop("tests.crashes", None)


def test_runner_job_validation_rejects_traversal(tmp_path):
    from project_runner.executor import InvalidJob, validate_job

    base = {"mode": "python", "entry": "analysis/a.py", "files": {"analysis/a.py": "x = 1"},
            "template_key": "masar-commerce-analysis"}
    for bad in (
        dict(base, entry="../a.py"),
        dict(base, files={"analysis/a.py": "", "../../etc/x.py": ""}),
        dict(base, files={"analysis/a.py": "", "data/orders.csv": "fake"}),
        dict(base, template_key="../masar-commerce-analysis"),
        dict(base, data_inline={"/etc/passwd": "x"}),
        dict(base, mode="shell"),
        dict(base, entry="analysis/a.sql"),
    ):
        with pytest.raises(InvalidJob):
            validate_job(bad, str(tmp_path))


def test_production_never_uses_the_local_adapter(monkeypatch):
    from app.core.config import Settings
    from app.services.project_lab import execution

    assert Settings(APP_ENV="production").project_lab_backend == "disabled"
    assert Settings(APP_ENV="development").project_lab_backend == "local"
    problems = " ".join(Settings(APP_ENV="production", PROJECT_LAB_EXECUTION_BACKEND="runner").project_lab_problems())
    assert "PROJECT_LAB_RUNNER_SOCKET must be an absolute socket path" in problems
    assert "PROJECT_LAB_RUNNER_TOKEN must be a random value" in problems
    assert "PROJECT_RUNNER_RUNTIME must be runsc" in problems
    assert "PROJECT_RUNNER_SECCOMP must be runner-seccomp-gvisor.json" in problems
    assert "PROJECT_RUNNER_REQUIRE_GVISOR must be true" in problems
    assert "PROJECT_LAB_REQUIRE_GVISOR must be true" in problems
    assert "PROJECT_RUNNER_PIDS_LIMIT must be at least 512" in problems
    ok = Settings(APP_ENV="production", PROJECT_LAB_EXECUTION_BACKEND="runner",
                  PROJECT_LAB_RUNNER_SOCKET="/run/project-runner/runner.sock",
                  PROJECT_LAB_RUNNER_TOKEN="0123456789abcdef0123456789abcdef",
                  PROJECT_RUNNER_RUNTIME="runsc",
                  PROJECT_RUNNER_SECCOMP="runner-seccomp-gvisor.json",
                  PROJECT_RUNNER_REQUIRE_GVISOR=True,
                  PROJECT_LAB_REQUIRE_GVISOR=True,
                  PROJECT_RUNNER_PIDS_LIMIT=512)
    assert ok.project_lab_problems() == []
    default_token = Settings(APP_ENV="production", PROJECT_LAB_EXECUTION_BACKEND="runner",
                             PROJECT_LAB_RUNNER_SOCKET="/run/project-runner/runner.sock",
                             PROJECT_LAB_RUNNER_TOKEN="local-dev-runner-token-change-me")
    assert default_token.project_lab_problems()

    # The kill switch remains available even when runsc is absent: none of
    # the runner settings is required while learner execution is disabled.
    disabled = Settings(APP_ENV="production", PROJECT_LAB_EXECUTION_BACKEND="disabled")
    assert disabled.project_lab_problems() == []

    monkeypatch.setattr(execution.settings, "APP_ENV", "production")
    monkeypatch.setattr(execution.settings, "PROJECT_LAB_EXECUTION_BACKEND", "local")
    assert isinstance(execution.build_backend(), DisabledBackend)
