"""Masar Commerce capstone: every milestone's validators against correct,
plausible-but-wrong, hard-coded and broken work; the complete milestone flow
and final submission; per-learner execution leases; artifacts; observability.

Learner code runs for real through the local development adapter (the same
harness the project-runner uses). The reference solution lives in
tests/project_lab_solutions/ — never in project_templates/, which the runner
mounts for learners.
"""
import asyncio
import base64
import logging
import math
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from app.core.limiter import limiter
from app.models.project_lab import LabArtifact, LabAttempt, LabExecutionLease, LabMilestone, LabProject, LabTask, LabTaskProgress
from app.services.project_lab import service
from app.services.project_lab.definitions import MASAR_COMMERCE
from app.services.project_lab.execution import (
    ExecutionBackend, JobOutcome, LocalSubprocessBackend, RunnerServiceBackend,
)
from app.services.project_lab.service import sync_definitions
from app.services.project_lab.templates import load_template
from app.services.project_lab.validators import masar_commerce as mc
from app.services.project_lab.validators import masar_commerce_facts as F
from tests.learning_fixtures import logs_enabled  # noqa: F401
from tests.test_project_lab import (  # noqa: F401 - fixtures
    API, _check, _put, _register, _start, lab, reference_facts, solution, use_backend,
)

SOLUTION = pathlib.Path(__file__).parent / "project_lab_solutions" / "masar_commerce"
TASK_ORDER = [t["slug"] for m in MASAR_COMMERCE["milestones"] for t in m["tasks"]]


def _solution_files() -> dict[str, str]:
    return {p.relative_to(SOLUTION).as_posix(): p.read_text(encoding="utf-8")
            for p in SOLUTION.rglob("*") if p.is_file()}


def _write_solution(client, headers, attempt_id, **overrides):
    files = _solution_files()
    files.update(overrides)
    for path, content in files.items():
        _put(client, headers, attempt_id, path, content)


@pytest.fixture()
def no_rate_limit():
    """The flow tests make dozens of Check Steps in a minute."""
    limiter.enabled = False
    yield
    limiter.enabled = True


# ─── The complete capstone, start to final submission ────────────────────────

def test_complete_capstone_flow_and_final_submission(client, db, lab, no_rate_limit):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    early = client.post(f"{API}/attempts/{attempt_id}/submit", headers=headers)
    assert early.status_code == 409 and early.json()["detail"]["code"] == "PROJECT_NOT_COMPLETE"
    _write_solution(client, headers, attempt_id)

    for index, slug in enumerate(TASK_ORDER, start=1):
        result = _check(client, headers, attempt_id, slug)
        assert result["outcome"] == "pass", (slug, [c for c in result["checks"] if not c["passed"]], result["error"])
        assert result["newly_completed"] is True and result["progress"]["completed_tasks"] == index
    assert index == 29
    progress = result["progress"]
    assert progress["percent"] == 100 and progress["status"] == "completed" and progress["current_task"] is None
    assert all(m["percent"] == 100 for m in progress["milestones"]) and len(progress["milestones"]) == 10

    # Re-checking a completed task stays a pass and changes nothing.
    again = _check(client, headers, attempt_id, "headline-kpis")
    assert again["outcome"] == "pass" and again["newly_completed"] is False
    assert again["progress"]["completed_tasks"] == 29

    summary = client.get(f"{API}/attempts/{attempt_id}/submission", headers=headers).json()
    assert summary["ready"] is True and summary["submitted_at"] is None

    submitted = client.post(f"{API}/attempts/{attempt_id}/submit", headers=headers)
    assert submitted.status_code == 200, submitted.text
    body = submitted.json()
    assert body["submitted_at"] and body["percent"] == 100 and body["completed_tasks"] == body["total_tasks"] == 29
    assert [m["slug"] for m in body["milestones"]] == [m["slug"] for m in MASAR_COMMERCE["milestones"]]
    assert all(m["completed"] for m in body["milestones"])
    assert {"en": "SQL Business Analysis", "ar": "تحليل الأعمال باستخدام SQL"} in body["skills"]
    charts = {a["path"] for a in body["artifacts"]}
    assert {"charts/monthly_revenue.png", "charts/revenue_by_category.png", "charts/revenue_by_region.png"} <= charts
    assert "validator" not in submitted.text

    repeat = client.post(f"{API}/attempts/{attempt_id}/submit", headers=headers).json()
    assert repeat["submitted_at"] == body["submitted_at"]  # idempotent: the first submission time is kept
    attempt = client.get(f"{API}/attempts/{attempt_id}", headers=headers).json()
    assert attempt["status"] == "completed" and attempt["submitted_at"] == body["submitted_at"]

    # Portfolio-ready completion data, frozen at submission.
    completion = client.get(f"{API}/attempts/{attempt_id}/completion", headers=headers)
    assert completion.status_code == 200, completion.text
    data = completion.json()
    assert data["schema_version"] == 1 and data["status"] == "completed"
    assert data["completed_tasks"] == data["total_tasks"] == 29 and data["submitted_at"] == body["submitted_at"]
    assert data["project"]["role"] == "Junior Data Analyst" and data["project"]["duration_hours"] == [12, 18]
    assert {s["en"] for s in data["skills"]} == {
        "SQL Business Analysis", "Data Cleaning", "Pandas", "KPI Analysis", "Customer Analysis", "Product Analysis",
        "Time-Series Analysis", "Data Visualization", "Business Reporting"}
    assert len(data["deliverables"]) == 7 and all(m["completed"] for m in data["milestones"])
    paths = [a["path"] for a in data["artifacts"]]
    assert paths[0] == "report.md" and "charts/monthly_revenue.png" in paths and "analysis/kpis.py" in paths
    assert "findings.md" in paths and "sql/top_customers.sql" in paths and "README.md" not in paths
    serialized = completion.text
    assert "content" not in serialized and "validator" not in serialized and "line_revenue" not in serialized
    # Later edits never change the frozen snapshot.
    _put(client, headers, attempt_id, "report.md", "# changed after submission\n")
    assert client.get(f"{API}/attempts/{attempt_id}/completion", headers=headers).json() == data


# ─── Representative validators, every milestone ──────────────────────────────

SOL = _solution_files()
CLEAN = SOL["analysis/clean_data.py"]
CLEAN_ALL_STATUSES = CLEAN.replace('completed = orders[orders["status"] == "completed"]', "completed = orders")
CLEAN_KEEPS_DUPLICATES = CLEAN.replace("orders = orders.drop_duplicates().reset_index(drop=True)", "orders = orders.copy()") \
    .replace("return order_items.drop_duplicates().reset_index(drop=True)", "return order_items.copy()")
CLEAN_DROPS_CUSTOMERS = CLEAN.replace('customers["city"] = customers["city"].fillna("Unknown")',
                                      'customers = customers.dropna(subset=["city"])')
CLEAN_FORGETS_COUNTRIES = CLEAN.replace('customers["country"] = customers["country"].str.strip().str.title()', "pass")
CANCELLED = "Cancelled, returned or pending orders appear to be included"
DUPLICATES = "Duplicate export rows appear to be counted twice"
LIST_PRICE = "The catalogue list_price appears to be used"
COMPUTED = "Your code must calculate its results from the files in data/"

CASES = [
    # (task, overrides, {check id: expected message start or None for "failed"}, outcome)
    pytest.param("frame-the-brief", {"analysis_plan.md": "# Analysis Plan\n\n## Objective\n\nTo analyse.\n\n## Stakeholders\n\n"
                 "- CEO: the overall picture.\n"},
                 {"objective_written": "Under “Objective”, replace the placeholder",
                  "stakeholders_items": "List at least 3 separate points"}, "fail", id="m1-too-short"),
    pytest.param("plan-questions-and-kpis", {"analysis_plan.md": SOL["analysis_plan.md"].replace("completed orders only", "all orders")
                 .replace("completed orders.", "orders.").replace("at least one completed order", "an order")},
                 {"kpi_definitions_term_0": "Say which orders count as recognised revenue"}, "fail", id="m1-kpi-rule-missing"),
    pytest.param("find-quality-issues", {"analysis/inspect_data.py": SOL["analysis/inspect_data.py"].replace(
                 "orders.duplicated().sum()", "orders.duplicated(keep=False).sum()").replace(
                 "order_items.duplicated().sum()", "order_items.duplicated(keep=False).sum()")},
                 {"duplicate_rows": "Count only the extra copies"}, "fail", id="m2-duplicates-counted-twice"),
    pytest.param("understand-orders-and-customers", {"analysis/inspect_data.py": SOL["analysis/inspect_data.py"].replace(
                 'orders.drop_duplicates()["status"]', 'orders["status"]')},
                 {"orders_by_status": "Count each order once"}, "fail", id="m2-raw-status-counts"),
    pytest.param("remove-duplicates", {"analysis/clean_data.py": CLEAN_KEEPS_DUPLICATES},
                 {"orders_clean_unique": "orders_clean still has the duplicate rows"}, "fail", id="m3-duplicates-kept"),
    pytest.param("standardise-customers", {"analysis/clean_data.py": CLEAN_DROPS_CUSTOMERS},
                 {"customers_kept": "Customers with a missing city were dropped"}, "fail", id="m3-customers-dropped"),
    pytest.param("standardise-customers", {"analysis/clean_data.py": CLEAN_FORGETS_COUNTRIES},
                 {"countries_standardised": "Some country values still differ"}, "fail", id="m3-countries-not-fixed"),
    pytest.param("build-sales-table", {"analysis/clean_data.py": CLEAN_ALL_STATUSES},
                 {"sales_rows": CANCELLED, "sales_revenue": CANCELLED}, "fail", id="m3-cancelled-included"),
    pytest.param("build-sales-table", {"analysis/clean_data.py": CLEAN_KEEPS_DUPLICATES},
                 {"sales_rows": DUPLICATES}, "fail", id="m3-join-to-duplicates"),
    pytest.param("sql-revenue-by-category", {"sql/revenue_by_category.sql": SOL["sql/revenue_by_category.sql"]
                 .replace("i.quantity * i.unit_price", "i.quantity * p.list_price")},
                 {"revenue": LIST_PRICE}, "fail", id="m4-list-price"),
    pytest.param("sql-revenue-by-category", {"sql/revenue_by_category.sql": SOL["sql/revenue_by_category.sql"]
                 .replace("SELECT DISTINCT * FROM orders", "SELECT * FROM orders")
                 .replace("SELECT DISTINCT * FROM order_items", "SELECT * FROM order_items")},
                 {"revenue": DUPLICATES}, "fail", id="m4-duplicates"),
    pytest.param("sql-revenue-by-category", {"sql/revenue_by_category.sql": SOL["sql/revenue_by_category.sql"]
                 .replace("WHERE o.status = 'completed'\n", "")},
                 {"revenue": CANCELLED}, "fail", id="m4-cancelled"),
    pytest.param("sql-monthly-revenue", {"sql/monthly_revenue.sql": SOL["sql/monthly_revenue.sql"].replace("ORDER BY 1", "ORDER BY 2 DESC")},
                 {"calendar_order": "Sort the result by month"}, "fail", id="m4-month-order"),
    pytest.param("sql-monthly-revenue", {"sql/monthly_revenue.sql": SOL["sql/monthly_revenue.sql"]
                 .replace("COUNT(DISTINCT o.order_id)", "COUNT(*)")},
                 {"orders": "orders should count DISTINCT completed orders"}, "fail", id="m4-wrong-aggregation"),
    pytest.param("sql-top-customers", {"sql/top_customers.sql": "SELECT * FROM (\n"
                 + SOL["sql/top_customers.sql"].rstrip().rstrip(";") + "\n) t ORDER BY customer_id"},
                 {"ranking": "These are the right customers, but sort them"}, "fail", id="m4-ranking-order"),
    pytest.param("sql-product-performance", {"sql/product_performance.sql": SOL["sql/product_performance.sql"]
                 .replace("LEFT JOIN sales_by_product", "JOIN sales_by_product")},
                 {"every_product": "Products that never sold are missing"}, "fail", id="m4-inner-join"),
    pytest.param("sql-product-performance", {"sql/product_performance.sql": SOL["sql/product_performance.sql"]
                 .replace("COALESCE(s.units_sold, 0)", "s.units_sold").replace("COALESCE(s.revenue, 0)", "s.revenue")},
                 {"values": "Unsold products show NULL"}, "fail", id="m4-null-not-zero"),
    pytest.param("sql-regional-performance", {"sql/regional_performance.sql": "SELECT region, 1 AS customers, 1 AS orders, "
                 "1.0 AS revenue, 1.0 AS aov FROM customers GROUP BY region"},
                 {"revenue": None, "counts": None, "aov": None}, "fail", id="m4-placeholder-values"),
    pytest.param("headline-kpis", {"analysis/clean_data.py": CLEAN_ALL_STATUSES},
                 {"revenue": CANCELLED, "aov": CANCELLED}, "fail", id="m5-cancelled-included"),
    pytest.param("revenue-at-risk", {"analysis/kpis.py": SOL["analysis/kpis.py"].replace(
                 '(orders["status"] == "cancelled").mean()', '(orders["status"] == "cancelled").sum()')},
                 {"cancellation_rate": "cancellation_rate is cancelled orders divided by ALL"}, "fail", id="m5-count-not-rate"),
    pytest.param("customer-concentration", {"analysis/customers.py": SOL["analysis/customers.py"].replace(
                 "top_decile_share = ranked.head(len(ranked) // 10).sum() / ranked.sum()",
                 "top_decile_share = 100 * ranked.head(len(ranked) // 10).sum() / ranked.sum()")},
                 {"top_decile_share": "Give the share as a fraction"}, "fail", id="m6-percentage-share"),
    pytest.param("customer-concentration", {"analysis/customers.py": SOL["analysis/customers.py"].replace(
                 "ranked = customer_revenue.sort_values(ascending=False)", "ranked = customer_revenue.sort_values(ascending=True)")},
                 {"top_decile_share": "Take the top 10% of purchasing customers"}, "fail", id="m6-bottom-decile"),
    pytest.param("headline-kpis", {"analysis/kpis.py": SOL["analysis/kpis.py"].replace(
                 '"unique_customers": sales["customer_id"].nunique()', '"unique_customers": sales["order_id"].nunique()')},
                 {"unique_customers": "Purchasing customers appear to count orders instead"}, "fail", id="m5-customers-are-orders"),
    pytest.param("sql-top-customers", {"sql/top_customers.sql": SOL["sql/top_customers.sql"].replace(
                 "ORDER BY revenue DESC", "ORDER BY orders DESC, revenue DESC")},
                 {"ranking": "The ranking appears to be based on the number of orders"}, "fail", id="m4-ranked-by-orders"),
    pytest.param("sql-regional-performance", {"sql/regional_performance.sql": SOL["sql/regional_performance.sql"].replace(
                 "COUNT(DISTINCT o.customer_id) AS customers", "COUNT(DISTINCT o.order_id) AS customers")},
                 {"counts": "The customer count appears to count orders instead"}, "fail", id="m4-customers-are-orders"),
    pytest.param("sql-regional-performance", {"findings.md": "# Analysis Findings\n\n## SQL findings\n\nGood.\n"},
                 {"sql_findings_written": "Under “SQL findings”, replace the placeholder"}, "fail", id="m4-insight-missing"),
    pytest.param("repeat-purchase-behaviour", {"analysis/customers.py": SOL["analysis/customers.py"].replace(
                 '["order_id"].nunique()\nrepeat', '["order_id"].count()\nrepeat')},
                 {"avg_orders_per_customer": "Average the number of DISTINCT"}, "fail", id="m6-lines-not-orders"),
    pytest.param("repeat-purchase-behaviour", {"analysis/customers.py": SOL["analysis/customers.py"].replace(
                 "repeat_customer_rate = (per_customer >= 2).mean()", "repeat_customer_rate = 100 * (per_customer >= 2).mean()")},
                 {"repeat_customer_rate": "Give the rate as a fraction"}, "fail", id="m6-percentage"),
    pytest.param("category-mix", {"analysis/products.py": SOL["analysis/products.py"].replace(
                 'category_revenue = sales.groupby("category")["line_revenue"].sum()',
                 'category_revenue = sales.groupby("category")["line_revenue"].mean()')},
                 {"category_share": "A category's share is its recognised revenue"}, "fail", id="m7-mean-not-sum"),
    pytest.param("product-concentration", {"analysis/products.py": SOL["analysis/products.py"].replace(
                 '.sum().sort_values(ascending=False)\ntop5_share', '.sum()\ntop5_share')},
                 {"top5_share": "Rank products by recognised revenue"}, "fail", id="m7-unranked-products"),
    # A different but equivalent query passes: no product is priced exactly 1,500.
    pytest.param("sql-price-bands", {"sql/price_bands.sql": SOL["sql/price_bands.sql"].replace("list_price < 1500", "list_price <= 1500")},
                 {}, "pass", id="m7-boundary-without-products-at-1500"),
    pytest.param("sql-price-bands", {"sql/price_bands.sql": SOL["sql/price_bands.sql"].replace("LEFT JOIN sales_by_product", "JOIN sales_by_product")},
                 {"products": "products counts every catalogue product"}, "fail", id="m7-unsold-dropped"),
    pytest.param("growth", {"analysis/trends.py": SOL["analysis/trends.py"].replace(
                 "mom_growth = s.pct_change().dropna().to_dict()", "mom_growth = (100 * s.pct_change()).dropna().to_dict()")},
                 {"mom_growth": "Give growth as fractions"}, "fail", id="m8-percent-growth"),
    pytest.param("regional-value", {"analysis/trends.py": SOL["analysis/trends.py"].replace(
                 'revenue_per_customer = region_revenue / g["customer_id"].nunique()',
                 'revenue_per_customer = region_revenue / g["order_id"].nunique()')},
                 {"revenue_per_customer": "Divide each region's recognised revenue by its number of DISTINCT"}, "fail",
                 id="m8-per-order-not-per-customer"),
    pytest.param("chart-monthly-revenue", {"analysis/visualize.py": SOL["analysis/visualize.py"].replace(
                 'plt.savefig("charts/monthly_revenue.png")', 'plt.savefig("monthly.png")')},
                 {"chart_saved": 'Save the chart with plt.savefig("charts/monthly_revenue.png")'}, "fail", id="m9-wrong-path"),
    pytest.param("chart-revenue-by-category", {"analysis/visualize.py": SOL["analysis/visualize.py"].replace(
                 'plt.figure(figsize=(8, 4.5))\nplt.bar(', 'plt.figure(figsize=(2, 1))\nplt.bar(')},
                 {"chart_valid": "charts/revenue_by_category.png must be a PNG of at least"}, "fail", id="m9-tiny-image"),
    pytest.param("write-the-report", {"report.md": SOL["report.md"].split("# Key Risks")[0]},
                 {"key_risks_present": "Keep the “Key Risks” heading", "recommendations_present": None}, "fail",
                 id="m10-sections-missing"),
    pytest.param("support-with-numbers", {"report.md": SOL["report.md"].replace("11.47 million", "14.28 million")},
                 {"revenue": "State the recognised revenue you calculated"}, "fail", id="m10-wrong-revenue"),
    pytest.param("embed-the-charts", {"report.md": SOL["report.md"].replace("charts/revenue_by_region.png", "charts/regions.png")},
                 {"required": "Also embed: charts/revenue_by_region.png", "generated": "Not generated yet: charts/regions.png"},
                 "fail", id="m10-unknown-chart"),
]


@pytest.mark.parametrize("task, overrides, expected, outcome", CASES)
def test_validator_feedback(client, lab, no_rate_limit, task, overrides, expected, outcome):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id, **overrides)
    if task == "embed-the-charts":
        client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/visualize.py"}, headers=headers)
    result = _check(client, headers, attempt_id, task)
    checks = {c["id"]: c for c in result["checks"]}
    assert result["outcome"] == outcome, (result["outcome"], [c for c in result["checks"] if not c["passed"]], result["error"])
    for check_id, message in expected.items():
        assert checks[check_id]["passed"] is False, check_id
        if message is not None:
            assert checks[check_id]["message"].startswith(message), (check_id, checks[check_id]["message"])
        assert checks[check_id]["messages"]["ar"], check_id  # every message has its Arabic twin
    if outcome == "fail":
        assert result["task_status"] == "in_progress" and result["newly_completed"] is False
        _assert_no_answer_leaks(result)


def _assert_no_answer_leaks(result) -> None:
    facts = reference_facts()
    text = str(result)
    for value in (facts.revenue, facts.aov, facts.region_revenue["Egypt"], facts.category_revenue["Electronics"]):
        for form in (f"{value:.2f}", f"{value:,.2f}", f"{value:,.0f}", str(round(value))):
            assert form not in text, form
    for value in (facts.completed_orders, facts.unique_customers, facts.items_sold, facts.one_time_customers):
        assert f" {value}" not in text and f"{value:,}" not in text, value
    assert facts.top_customers[0] not in text and facts.best_month not in text


HARD_CODED = [
    pytest.param("profile-the-tables", "analysis/inspect_data.py",
                 lambda f: f"row_counts = {f.row_counts!r}\norder_date_range = {list(f.order_date_range)!r}\n", id="m2"),
    pytest.param("sql-regional-performance", "sql/regional_performance.sql",
                 lambda f: "SELECT * FROM (VALUES " + ", ".join(
                     f"('{r}', {f.region_customers[r]}, {f.region_orders[r]}, {f.region_revenue[r]!r}, {f.region_aov[r]!r})"
                     for r in f.region_revenue) + ") AS t(region, customers, orders, revenue, aov)", id="m4-sql-values"),
    pytest.param("product-concentration", "analysis/products.py",
                 lambda f: f"top5_share = {f.top5_product_share!r}\ntop10_share = {f.top10_product_share!r}\n", id="m7"),
    pytest.param("customer-concentration", "analysis/customers.py",
                 lambda f: f"customer_revenue = {f.customer_revenue!r}\ntop_decile_share = {f.top_decile_share!r}\n",
                 id="m6"),
    pytest.param("growth", "analysis/trends.py",
                 lambda f: f"mom_growth = {f.mom_growth!r}\nbest_month = {f.best_month!r}\n"
                           f"h2_vs_h1_growth = {f.h2_vs_h1_growth!r}\n", id="m8"),
]


@pytest.mark.parametrize("task, path, source", HARD_CODED)
def test_hard_coded_answers_fail_on_the_hidden_variant(client, lab, task, path, source):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, path, source(reference_facts()))
    _put(client, headers, attempt_id, "findings.md", SOL["findings.md"])  # isolate the variant check
    result = _check(client, headers, attempt_id, task)
    checks = {c["id"]: c for c in result["checks"]}
    assert all(c["passed"] for k, c in checks.items() if k != "computed_from_data"), checks
    assert checks["computed_from_data"]["passed"] is False
    assert checks["computed_from_data"]["message"].startswith(COMPUTED)
    assert result["outcome"] == "fail"


def test_runtime_error_then_retry_passes(client, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id, **{
        "analysis/customers.py": SOL["analysis/customers.py"].replace('groupby("segment")', 'groupby("segmnt")')})
    broken = _check(client, headers, attempt_id, "customer-segments")
    assert broken["outcome"] == "error" and broken["error"]["kind"] == "execution"
    assert "KeyError" in broken["run"]["stderr"] and broken["checks"] == []
    _put(client, headers, attempt_id, "analysis/customers.py", SOL["analysis/customers.py"])
    fixed = _check(client, headers, attempt_id, "customer-segments")
    assert fixed["outcome"] == "pass" and fixed["newly_completed"] is True


def test_arabic_report_with_arabic_headings_and_digits_passes(client, lab, no_rate_limit):
    facts = reference_facts()
    to_arabic = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")
    revenue = f"{facts.revenue / 1e6:.2f}".translate(to_arabic)
    orders = f"{facts.completed_orders}".translate(to_arabic)
    aov = f"{facts.aov:.0f}".translate(to_arabic)
    repeat = f"{100 * facts.repeat_customer_rate:.1f}".translate(to_arabic)
    filler = "وهذا يوضح للإدارة ما يجب التركيز عليه خلال العام القادم بناءً على البيانات المتاحة لدينا الآن. " * 3
    report = (
        f"# الملخص التنفيذي\n\n{filler}\n\n"
        f"# أداء الأعمال\n\nحققت الشركة إيرادات معترفًا بها قدرها {revenue} مليون جنيه من {orders} طلبًا مكتملًا، "
        f"بمتوسط قيمة طلب {aov} جنيه. {filler}\n\n"
        f"# رؤى العملاء\n\nبلغ معدل العملاء المتكررين {repeat}٪ من العملاء المشترين. {filler}\n\n"
        f"# رؤى المنتجات\n\nتتصدر الإلكترونيات الفئات من حيث الإيرادات. {filler}\n\n"
        "![الإيرادات حسب الفئة](charts/revenue_by_category.png)\n\n"
        f"# الاتجاهات الإقليمية والزمنية\n\nتتصدر مصر المناطق، وكان شهر نوفمبر الأفضل. {filler}\n\n"
        "![الإيرادات الشهرية](charts/monthly_revenue.png)\n\n![المناطق](charts/revenue_by_region.png)\n\n"
        "# المخاطر الرئيسية\n\n- التركز في فئة واحدة ومنطقتين يعرض جزءًا كبيرًا من الإيرادات للخطر إذا تراجع الطلب.\n"
        "- يشتري عدد كبير من العملاء مرة واحدة فقط ثم لا يعودون، وهذا يرفع تكلفة النمو.\n\n"
        "# التوصيات\n\n- التسويق: إطلاق عرض للشراء الثاني للعملاء الجدد خلال ثلاثين يومًا من أول طلب.\n"
        "- المبيعات: تنمية فئة المنزل والمطبخ وفئة التجميل لتقليل الاعتماد على الإلكترونيات.\n"
        "- العمليات: دراسة أسباب الإلغاء والإرجاع في الفئات الكبرى ووضع خطة لخفضها.\n"
    )
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id, **{"report.md": report})
    client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/visualize.py"}, headers=headers)
    for task in ("write-the-report", "support-with-numbers", "embed-the-charts"):
        result = _check(client, headers, attempt_id, task, language="ar")
        assert result["outcome"] == "pass", (task, [c for c in result["checks"] if not c["passed"]])


# ─── Facts and the hidden variant (pure) ─────────────────────────────────────

def _template_data():
    template = load_template(MASAR_COMMERCE["template_key"])
    return {t: template.read_csv(f"data/{t}.csv") for t in F.TABLES}


def test_variant_moves_every_answer_a_learner_could_type_in():
    data = _template_data()
    original, variant = F.analyze(data), F.analyze(F.variant(data))
    for name in ("row_counts", "order_date_range", "duplicate_rows", "missing_city", "inconsistent_countries",
                 "orders_by_status", "customers_without_orders", "revenue", "completed_orders", "aov",
                 "unique_customers", "items_sold", "status_value", "cancellation_rate", "customer_revenue",
                 "top_customers", "repeat_customer_rate", "one_time_customers", "segment_revenue", "category_revenue",
                 "category_share", "top_products", "unsold_products", "discount_by_category", "price_bands",
                 "monthly_revenue", "mom_growth", "best_month", "h2_vs_h1_growth", "region_revenue", "top_region",
                 "top_decile_share", "top5_product_share", "top10_product_share", "region_share",
                 "region_revenue_per_customer"):
        assert getattr(original, name) != getattr(variant, name), name
    # Every intentional data issue is still present in the variant.
    assert all(variant.duplicate_rows.values()) and variant.missing_city and variant.inconsistent_countries
    assert set(variant.orders_by_status) == set(F.STATUSES)


def test_dataset_supports_the_story_and_known_mistakes_differ():
    data = _template_data()
    facts = F.analyze(data)
    assert set(facts.region_revenue) == set(F.REGIONS) and len(facts.category_revenue) == 6
    assert facts.monthly_revenue.keys() == {f"2025-{m:02d}" for m in range(1, 13)}
    assert 0.3 < facts.repeat_customer_rate < 0.7 and facts.one_time_customers > 100 and facts.customers_without_orders > 0
    assert len(facts.unsold_products) == 2 and facts.h2_vs_h1_growth > 0
    for mistake in ({"statuses": F.STATUSES}, {"dedupe": False}, {"price": "list_price"}):
        assert F.analyze(data, **mistake).revenue != facts.revenue, mistake


LEARNER_TEXT_KEYS = {"title", "title_ar", "summary", "summary_ar", "instructions", "instructions_ar",
                     "scenario", "scenario_ar", "role", "role_ar", "en", "ar"}


def _learner_texts() -> dict[str, str]:
    """Everything a learner can read: definition text (instructions, hints, overview), every string
    literal of the validator modules (check labels and failure messages) and the starter files."""
    import ast

    texts: dict[str, str] = {}

    def walk(node, where):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "validator_config":
                    continue  # server-side only
                if isinstance(value, str) and key in LEARNER_TEXT_KEYS:
                    texts[f"{where}.{key}"] = value
                else:
                    walk(value, f"{where}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{where}[{index}]")

    walk(MASAR_COMMERCE, "definition")
    for module in (mc, __import__("app.services.project_lab.validators.common", fromlist=["x"])):
        tree = ast.parse(pathlib.Path(module.__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                texts[f"{pathlib.Path(module.__file__).name}:{node.lineno}"] = node.value
    template = load_template(MASAR_COMMERCE["template_key"])
    for path in template.files:
        if not path.startswith("data/"):
            texts[path] = template.read_text(path)
    return texts


def test_learner_facing_text_reveals_no_expected_value():
    """Examples in instructions and messages must never be the real answers (a rounding example
    once read "11.5 million EGP" — the actual recognised revenue)."""
    facts = F.analyze(_template_data())
    amounts = {
        "revenue": facts.revenue, "completed_orders": facts.completed_orders, "aov": facts.aov,
        "unique_customers": facts.unique_customers, "items_sold": facts.items_sold,
        "customers_without_orders": facts.customers_without_orders, "one_time_customers": facts.one_time_customers,
        # row_counts["customers"] (1,500) is left out: it coincides with the documented price-band threshold.
        "orders_rows": facts.row_counts["orders"], "order_items_rows": facts.row_counts["order_items"],
        **{f"status_value.{k}": v for k, v in facts.status_value.items()},
        **{f"category_revenue.{k}": v for k, v in facts.category_revenue.items()},
        **{f"region_revenue.{k}": v for k, v in facts.region_revenue.items()},
        **{f"monthly_revenue.{k}": v for k, v in facts.monthly_revenue.items()},
    }
    rates = {
        "repeat_customer_rate": facts.repeat_customer_rate, "cancellation_rate": facts.cancellation_rate,
        "top_decile_share": facts.top_decile_share, "h2_vs_h1_growth": facts.h2_vs_h1_growth,
        "top5_product_share": facts.top5_product_share, "top10_product_share": facts.top10_product_share,
        "top_category_share": facts.category_share[facts.top_category],
        "top_region_share": facts.region_share[facts.top_region],
    }
    leaks = []
    for where, text in _learner_texts().items():
        for number in mc.report_numbers(text):
            leaks += [(where, name, number) for name, value in amounts.items()
                      if math.isclose(number, value, rel_tol=0.005)]
        for percent in mc.report_percents(text):
            leaks += [(where, name, percent) for name, value in rates.items()
                      if abs(percent - 100 * value) < 0.5]
    assert not leaks, leaks


def test_report_number_parsing():
    assert mc.report_numbers("11.47 million and 3,357 orders and 3.4K") == pytest.approx([11.47e6, 3357.0, 3400.0])
    assert mc.report_numbers("١١٫٥ مليون جنيه") == pytest.approx([11.5e6])
    assert mc.report_percents("53.8% / ٥٤٪ / 12 percent") == [53.8, 54.0, 12.0]
    assert mc.mentions_month("Revenue peaked in November.", "2025-11")
    assert mc.mentions_month("كان نوفمبر الأفضل", "2025-11") and not mc.mentions_month("in May", "2025-03")
    assert mc.mentions_name("تتصدر مصر", "Egypt") and not mc.mentions_name("Gulf leads", "Egypt")


def test_png_size_rejects_non_images():
    png = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + (800).to_bytes(4, "big")
                           + (450).to_bytes(4, "big") + b"\x08\x02\x00\x00\x00").decode()
    assert mc.png_size(png) == (800, 450)
    assert mc.png_size(base64.b64encode(b"GIF89a....").decode()) is None
    assert mc.png_size("not base64!") is None


# ─── Concurrency: one execution per learner ──────────────────────────────────

def test_execution_lease_is_exclusive_and_expires(db, client, lab):
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    gate = service.ExecutionGate()
    token = gate.acquire(db, user_id, attempt_id, "run")
    assert token is not None
    assert gate.acquire(db, user_id, attempt_id, "check") is None  # one at a time
    gate.release(db, user_id, "not-the-owner")                      # a stale token releases nothing
    assert gate.acquire(db, user_id, attempt_id, "check") is None
    gate.release(db, user_id, token)
    second = gate.acquire(db, user_id, attempt_id, "check")
    assert second is not None

    # A worker that died mid-run leaves a lease that simply expires.
    lease = db.query(LabExecutionLease).filter_by(user_id=user_id).one()
    lease.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db.commit()
    third = gate.acquire(db, user_id, attempt_id, "run")
    assert third is not None and third != second
    gate.release(db, user_id, third)
    assert db.query(LabExecutionLease).filter_by(user_id=user_id).count() == 0


def _counter(name: str, **labels) -> float:
    from prometheus_client import REGISTRY

    value = REGISTRY.get_sample_value(name, labels)
    return value or 0.0


def test_concurrent_run_or_check_is_refused_with_409(client, db, lab):
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    token = service.EXECUTION_GATE.acquire(db, user_id, attempt_id, "run")  # "another tab" is running
    before = _counter("project_lab_rejected_total", reason="concurrent")
    try:
        run = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers)
        check = client.post(f"{API}/attempts/{attempt_id}/tasks/headline-kpis/check", json={}, headers=headers)
        for response in (run, check):
            assert response.status_code == 409 and response.json()["detail"]["code"] == "EXECUTION_IN_PROGRESS"
        assert _counter("project_lab_rejected_total", reason="concurrent") == before + 2
        # Another learner is unaffected.
        _, other = _register(client)
        other_attempt = _start(client, other, lab)
        assert client.post(f"{API}/attempts/{other_attempt}/run", json={"path": "analysis/kpis.py"},
                           headers=other).status_code == 200
    finally:
        service.EXECUTION_GATE.release(db, user_id, token)
    assert client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"},
                       headers=headers).status_code == 200


class _Exploding(ExecutionBackend):
    name = "exploding"

    async def execute(self, job):
        raise RuntimeError("backend bug")


def test_lease_is_released_after_infrastructure_failure(client, db, lab, use_backend):
    use_backend(_Exploding())
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert body["status"] == "infrastructure_error"
    assert db.query(LabExecutionLease).filter_by(user_id=user_id).count() == 0
    again = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers)
    assert again.status_code == 200  # recovered, not locked out


def test_lease_is_released_after_timeout(client, db, lab, use_backend):
    use_backend(LocalSubprocessBackend(timeout_seconds=1, memory_mb=1024))
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "while True:\n    pass\n")
    assert client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"},
                       headers=headers).json()["status"] == "timeout"
    assert db.query(LabExecutionLease).filter_by(user_id=user_id).count() == 0


# ─── Artifacts, workspace cap ────────────────────────────────────────────────

def test_run_keeps_chart_artifacts_for_the_report(client, db, lab):
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id)
    body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/visualize.py"}, headers=headers).json()
    assert body["status"] == "success" and len(body["generated_files"]) == 3
    listed = client.get(f"{API}/attempts/{attempt_id}/artifacts", headers=headers).json()
    assert [a["path"] for a in listed] == ["charts/monthly_revenue.png", "charts/revenue_by_category.png",
                                           "charts/revenue_by_region.png"]
    assert all("content" not in a and a["media_type"] == "image/png" and len(a["sha256"]) == 64 for a in listed)
    one = client.get(f"{API}/attempts/{attempt_id}/artifacts/content", params={"path": "charts/monthly_revenue.png"},
                     headers=headers).json()
    assert mc.png_size(one["content"]) is not None
    missing = client.get(f"{API}/attempts/{attempt_id}/artifacts/content", params={"path": "charts/nope.png"},
                         headers=headers)
    assert missing.status_code == 404 and missing.json()["detail"]["code"] == "ARTIFACT_NOT_FOUND"
    # Running again replaces, never duplicates.
    client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/visualize.py"}, headers=headers)
    assert db.query(LabArtifact).filter_by(attempt_id=attempt_id).count() == 3


def test_workspace_size_is_capped(client, lab, monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "PROJECT_LAB_MAX_WORKSPACE_BYTES", 60_000)
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _put(client, headers, attempt_id, "analysis/kpis.py", "# x\n" * 5_000)
    response = client.put(f"{API}/attempts/{attempt_id}/files", params={"path": "analysis/products.py"},
                          json={"content": "# y\n" * 15_000}, headers=headers)
    assert response.status_code == 413 and response.json()["detail"]["code"] == "WORKSPACE_TOO_LARGE"


# ─── Content changes and retired demo tasks ──────────────────────────────────

def test_retiring_demo_content_keeps_reused_progress_and_reopens_finished_attempts(client, db, lab):
    user_id, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id)
    assert _check(client, headers, attempt_id, "headline-kpis")["outcome"] == "pass"

    # Pretend this learner finished an older, smaller version of the project.
    project = db.query(LabProject).filter_by(slug=lab).one()
    old = LabMilestone(project_id=project.id, slug="basic-kpis", position=99, title="Old", skills=[])
    db.add(old)
    db.flush()
    retired = LabTask(project_id=project.id, milestone_id=old.id, slug="state-the-objective", position=1,
                      title="Old task", instructions="x", hints=[], validator_key="common.markdown_section",
                      validator_config={})
    db.add(retired)
    headline = db.query(LabTask).filter_by(project_id=project.id, slug="headline-kpis").one()
    headline.milestone_id = old.id
    attempt = db.get(LabAttempt, attempt_id)
    attempt.status = "completed"
    db.commit()

    definition = dict(MASAR_COMMERCE, slug=lab, track_slug=project.track.slug)
    sync_definitions(db, [definition])
    assert db.query(LabTask).filter_by(project_id=project.id, slug="state-the-objective").count() == 0
    assert db.query(LabMilestone).filter_by(project_id=project.id, slug="basic-kpis").count() == 0
    done = db.query(LabTaskProgress).join(LabTask).filter(LabTaskProgress.attempt_id == attempt_id,
                                                          LabTask.slug == "headline-kpis").one()
    assert done.status == "completed"  # moved to its new milestone with its progress

    db.expire_all()
    view = client.get(f"{API}/attempts/{attempt_id}", headers=headers).json()
    assert view["progress"]["completed_tasks"] == 1 and view["progress"]["total_tasks"] == 29


# ─── Observability and the runner client ─────────────────────────────────────

def test_execution_metrics_and_logs_carry_no_learner_content(client, lab, caplog, logs_enabled):  # noqa: F811
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    secret = "LEARNER-SECRET-7f3a"
    _put(client, headers, attempt_id, "analysis/kpis.py", f"token = '{secret}'\nprint(token)\n")
    before = _counter("project_lab_executions_total", action="run", kind="python", status="success")
    checks_before = _counter("project_lab_checks_total", outcome="error", error_kind="execution")
    with caplog.at_level(logging.INFO, logger="app.services.project_lab.execution"):
        body = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert secret in body["stdout"]  # the learner sees their own output
    assert _counter("project_lab_executions_total", action="run", kind="python", status="success") == before + 1
    records = [r for r in caplog.records if getattr(r, "event", None) == "project_lab.execution"]
    assert records and records[-1].status == "success" and records[-1].purpose == "run"
    for record in caplog.records:
        assert secret not in record.getMessage() and secret not in str(record.__dict__)

    _put(client, headers, attempt_id, "analysis/kpis.py", "raise ValueError('x')\n")
    _check(client, headers, attempt_id, "headline-kpis")
    assert _counter("project_lab_checks_total", outcome="error", error_kind="execution") == checks_before + 1


def _runner(handler, *, require_gvisor=False):
    backend = RunnerServiceBackend(socket_path="/nonexistent.sock", token="t" * 32, timeout_seconds=5,
                                   require_gvisor=require_gvisor)
    backend._client = lambda: httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=5)
    return backend


def test_runner_client_requires_gvisor_when_configured():
    calls = []

    def handler(request):
        calls.append(request.url.path)
        if request.url.path == "/healthz":
            return httpx.Response(200, json={"ok": True, "runtime": "runc"})
        return httpx.Response(200, json={"status": "success", "stdout": "hi"})

    refused = asyncio.run(_runner(handler, require_gvisor=True).execute({"mode": "python"}))
    assert refused.status == "infrastructure_error" and calls == ["/healthz"]

    calls.clear()
    allowed = asyncio.run(_runner(handler).execute({"mode": "python"}))
    assert allowed.status == "success" and calls == ["/v1/jobs"]


def test_runner_client_maps_failures_to_infrastructure_errors():
    for response in (httpx.Response(503, json={"error": "busy"}), httpx.Response(500), httpx.Response(200, text="nope")):
        outcome = asyncio.run(_runner(lambda request, r=response: r).execute({"mode": "python"}))
        assert isinstance(outcome, JobOutcome) and outcome.status == "infrastructure_error"

    def unreachable(request):
        raise httpx.ConnectError("no socket")

    assert asyncio.run(_runner(unreachable).execute({"mode": "python"})).status == "infrastructure_error"


# ─── Fail closed: no silent fallback from gVisor ─────────────────────────────

RUNNER_SERVER = pathlib.Path(__file__).resolve().parents[1] / "project_runner" / "server.py"


def test_runner_refuses_to_start_without_gvisor_when_required(tmp_path):
    """RUNNER_REQUIRE_GVISOR=1 on a host without gVisor: the service exits at
    start-up with a clear message instead of serving jobs under runc."""
    env = {"PATH": os.environ.get("PATH", ""), "RUNNER_TOKEN": "t" * 32, "RUNNER_REQUIRE_GVISOR": "1",
           "RUNNER_SOCKET": str(tmp_path / "runner.sock")}
    result = subprocess.run([sys.executable, "-I", str(RUNNER_SERVER)], env=env, capture_output=True, text=True,
                            timeout=60)
    assert result.returncode != 0
    if os.geteuid() == 0:  # the test container runs as root: the gVisor check is what stops it
        assert "RUNNER_REQUIRE_GVISOR=1 but this container runs under 'runc'" in result.stderr
    else:
        assert "must start as root" in result.stderr
    assert not (tmp_path / "runner.sock").exists()


def test_required_gvisor_turns_a_check_into_a_platform_error_for_the_learner(client, lab, use_backend):
    def handler(request):
        if request.url.path == "/healthz":
            return httpx.Response(200, json={"ok": True, "runtime": "runc"})
        raise AssertionError("a job must never reach a runner that is not gVisor")

    use_backend(_runner(handler, require_gvisor=True))
    _, headers = _register(client)
    attempt_id = _start(client, headers, lab)
    _write_solution(client, headers, attempt_id)
    result = _check(client, headers, attempt_id, "headline-kpis")
    assert result["outcome"] == "error" and result["error"]["kind"] == "infrastructure"
    assert result["newly_completed"] is False and result["progress"]["completed_tasks"] == 0
    run = client.post(f"{API}/attempts/{attempt_id}/run", json={"path": "analysis/kpis.py"}, headers=headers).json()
    assert run["status"] == "infrastructure_error"
