"""Project Lab smoke test against the CONFIGURED execution backend.

Run inside the API container of a deployed stack (production included):

    docker compose exec -T api python scripts/project_lab_smoke.py

It executes a representative slice of the Masar Commerce capstone — Python,
pandas joins with large captures, SQL, a matplotlib chart, the hidden-variant
rerun — through exactly the backend the API uses (the project-runner over
its socket, with PROJECT_LAB_REQUIRE_GVISOR honoured), then two negative
cases: a hard-coded answer must fail, and a known mistake must get its named
feedback. It reads the reference solution in tests/project_lab_solutions/
(present in the API image, never mounted into the runner) and touches no
database. Exit status 0 only when every step behaves as expected.
"""
from __future__ import annotations

import asyncio
import os
import sys
import types
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings  # noqa: E402
from app.services.project_lab.definitions import MASAR_COMMERCE  # noqa: E402
from app.services.project_lab.execution import WorkspaceSnapshot, build_backend, ProjectExecutionService  # noqa: E402
from app.services.project_lab.templates import is_read_only, load_template  # noqa: E402
from app.services.project_lab.validators import masar_commerce_facts as F  # noqa: E402

SOLUTION = Path(__file__).resolve().parents[1] / "tests" / "project_lab_solutions" / "masar_commerce"
TASKS = ["profile-the-tables", "build-sales-table", "sql-revenue-by-category", "headline-kpis",
         "chart-monthly-revenue"]


def _workspace(overrides: dict[str, str] | None = None) -> WorkspaceSnapshot:
    template = load_template(MASAR_COMMERCE["template_key"])
    files = {p: template.read_text(p) for p in template.files if not is_read_only(p, MASAR_COMMERCE["read_only_paths"])}
    for path in SOLUTION.rglob("*"):
        if path.is_file():
            files[path.relative_to(SOLUTION).as_posix()] = path.read_text(encoding="utf-8")
    files.update(overrides or {})
    return WorkspaceSnapshot(template_key=template.key, files=files, dirs=list(template.dirs))


def _task(slug: str):
    for milestone in MASAR_COMMERCE["milestones"]:
        for task in milestone["tasks"]:
            if task["slug"] == slug:
                return types.SimpleNamespace(validator_key=task["validator_key"], validator_config=task["validator_config"])
    raise KeyError(slug)


async def main() -> int:
    backend = build_backend()
    print(f"backend: {backend.name}  require_gvisor: {settings.PROJECT_LAB_REQUIRE_GVISOR}")
    if backend.name != "runner":
        print("FAIL  the API is not configured to use the project-runner (PROJECT_LAB_EXECUTION_BACKEND)")
        return 1
    service = ProjectExecutionService(backend)
    template = load_template(MASAR_COMMERCE["template_key"])
    failures = 0

    async def check(slug: str, snapshot: WorkspaceSnapshot, expect: str, contains: str | None = None) -> None:
        nonlocal failures
        result = await service.validate_task(snapshot, _task(slug), template=template)
        messages = " ".join(c.message["en"] for c in result.checks if c.message)
        ok = result.outcome == expect and (contains is None or contains in messages)
        if not ok:
            failures += 1
        detail = f"{result.outcome}" + (f" / {result.error_kind}" if result.error_kind else "")
        print(f"{'PASS' if ok else 'FAIL'}  {slug}: expected {expect}, got {detail}")

    solution = _workspace()
    for slug in TASKS:
        await check(slug, solution, "pass")
    # The correct numbers typed in by hand: only the hidden-variant rerun can catch this.
    facts = F.analyze({name: template.read_csv(f"data/{name}.csv") for name in F.TABLES})
    typed = {"revenue": facts.revenue, "completed_orders": facts.completed_orders, "aov": facts.aov,
             "unique_customers": facts.unique_customers, "items_sold": facts.items_sold}
    await check("headline-kpis", _workspace({"analysis/kpis.py": f"kpis = {typed!r}\n"}), "fail",
                contains="Your code must calculate its results")
    cancelled = solution.files["analysis/clean_data.py"].replace(
        'completed = orders[orders["status"] == "completed"]', "completed = orders")
    await check("build-sales-table", _workspace({"analysis/clean_data.py": cancelled}), "fail",
                contains="Cancelled, returned or pending orders appear to be included")
    print(f"\n{'ALL PASS' if not failures else f'{failures} FAILURE(S)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
