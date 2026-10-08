"""Private validators for "Masar Commerce — Business Performance Analysis".

Every expected value comes from masar_commerce_facts.analyze(), run here on
the canonical template datasets. Nothing expected ever reaches the sandbox
or the browser: the sandbox returns observations (the learner's variables
or query result) and they are compared in this process.

Pattern for every data task:

1. run the learner's saved file on the real data and compare;
2. when a value is wrong, check whether it equals the result of a KNOWN
   mistake (cancelled orders counted, duplicates kept, list price used) and
   say so in words — never the expected number;
3. when everything matches, run the same file again on the hidden variant
   dataset (facts.variant) and compare against the variant's facts. Code
   that computes passes both; typed-in answers fail the second run.

Validators judge results, never source text, so any correct pandas or SQL
approach passes. Row order matters only where the task asks for an order
(calendar months, top-N rankings).
"""
from __future__ import annotations

import base64
import math
import re
import struct
from functools import lru_cache
from typing import Any, Callable

from ..templates import load_template
from ..validation import (
    MISSING, CheckResult, ValidationContext, ValidationResult, as_number, execution_error, from_checks, observed,
    validator,
)
from . import masar_commerce_facts as F
from .common import find_section, section_checks

Message = dict[str, str]


# ─── Reference data ──────────────────────────────────────────────────────────

class Reference:
    def __init__(self, data: F.Data):
        self.data = data
        self.facts = F.analyze(data)
        self.mistakes = {
            "all_statuses": F.analyze(data, statuses=F.STATUSES),
            "duplicates": F.analyze(data, dedupe=False),
            "list_price": F.analyze(data, price="list_price"),
        }
        self.variant_data = F.variant(data)
        self.variant_facts = F.analyze(self.variant_data)
        self.variant_inline = F.inline(self.variant_data)


@lru_cache(maxsize=4)
def _reference_for(template_key: str) -> Reference:
    """Computed once per process per template: the datasets are read-only."""
    template = load_template(template_key)
    return Reference({name: template.read_csv(f"data/{name}.csv") for name in F.TABLES})


def reference(ctx: ValidationContext) -> Reference:
    return _reference_for(ctx.template.key)


# ─── Messages ────────────────────────────────────────────────────────────────

MISTAKES: dict[str, Message] = {
    "all_statuses": {
        "en": "Cancelled, returned or pending orders appear to be included. Recognised revenue counts completed orders only.",
        "ar": "يبدو أن الطلبات الملغاة أو المرتجعة أو المعلّقة مُدرجة. الإيرادات المعترف بها تشمل الطلبات المكتملة فقط.",
    },
    "duplicates": {
        "en": "Duplicate export rows appear to be counted twice. Remove exact duplicates from orders and order_items "
              "before joining or summing.",
        "ar": "يبدو أن صفوف التصدير المكررة محسوبة مرتين. احذف الصفوف المكررة تمامًا من orders وorder_items "
              "قبل الربط أو الجمع.",
    },
    "list_price": {
        "en": "The catalogue list_price appears to be used. Revenue uses unit_price — the price actually charged "
              "after discounts.",
        "ar": "يبدو أنك استخدمت سعر الكتالوج list_price. الإيرادات تُحسب بـ unit_price — السعر المدفوع فعلًا "
              "بعد الخصم.",
    },
}
COMPUTED_FROM_DATA: Message = {
    "en": "Your code must calculate its results from the files in data/. When the data changed, it did not produce "
          "matching results — avoid typing numbers or names in by hand.",
    "ar": "يجب أن يحسب برنامجك نتائجه من ملفات data/. عندما تغيّرت البيانات لم تتطابق نتائجه — تجنّب كتابة "
          "الأرقام أو الأسماء يدويًا.",
}
AFTER_ABOVE: Message = {
    "en": "This check runs once the checks above pass.",
    "ar": "يُجرى هذا الفحص بعد نجاح الفحوص السابقة.",
}
COMPUTED_LABEL: Message = {"en": "Calculated from the data (checked on a changed copy)",
                           "ar": "محسوب من البيانات (يُفحص على نسخة معدّلة)"}


def _msg(en: str, ar: str) -> Message:
    return {"en": en, "ar": ar}


# ─── Comparing observations ──────────────────────────────────────────────────

def money_close(value: Any, expected: float) -> bool:
    """Equal up to float noise or rounding to cents."""
    number = as_number(value)
    return number is not None and math.isclose(number, expected, rel_tol=1e-7, abs_tol=0.011)


def rate_close(value: Any, expected: float) -> bool:
    """A fraction (0-1), equal up to rounding to 3 decimals."""
    number = as_number(value)
    return number is not None and math.isclose(number, expected, abs_tol=6e-4)


def count_equal(value: Any, expected: int) -> bool:
    number = as_number(value)
    return number is not None and number == float(expected)


_MONTH = re.compile(r"^(\d{4})-(\d{2})")


def month_key(value: Any) -> str | None:
    """'2025-03', '2025-03-01', '2025-03-01 00:00:00' and Period('2025-03') -> '2025-03'."""
    match = _MONTH.match(str(value).strip()) if value is not None else None
    return f"{match.group(1)}-{match.group(2)}" if match else None


def as_mapping(value: Any, *, months: bool = False) -> dict[str, Any] | None:
    """A dict observation (a dict or a pandas Series). A two-column DataFrame
    also counts: first column -> second column."""
    if value is MISSING or value is None:
        return None
    if isinstance(value, dict) and value.get("__dataframe__"):
        columns = value.get("columns") or []
        if len(columns) != 2:
            return None
        value = {str(r.get(columns[0])): r.get(columns[1]) for r in value.get("records") or []}
    if not isinstance(value, dict) or any(str(k).startswith("__") for k in value):
        return None
    if months:
        converted: dict[str, Any] = {}
        for key, item in value.items():
            month = month_key(key)
            if month is None:
                return None
            converted[month] = item
        return converted
    return {str(k).strip(): v for k, v in value.items()}


def as_id_list(value: Any) -> list[str] | None:
    """An ordered list of ids: a list/array/Index, or the keys of a Series
    (e.g. revenue.nlargest(10))."""
    if value is MISSING or value is None:
        return None
    if isinstance(value, dict) and not value.get("__dataframe__") and not any(str(k).startswith("__") for k in value):
        return [str(k) for k in value]
    if isinstance(value, list) and all(not isinstance(v, (dict, list)) for v in value):
        return [str(v) for v in value]
    return None


def mapping_matches(observed_map: dict[str, Any] | None, expected: dict[str, float],
                    same: Callable[[Any, float], bool]) -> bool:
    return (observed_map is not None and set(observed_map) == set(expected)
            and all(same(observed_map[k], v) for k, v in expected.items()))


def diagnose(matches: Callable[[F.Facts], bool], ref: Reference, fallback: Message) -> Message:
    """The message for a wrong value: a known mistake if the value equals that
    mistake's result, otherwise the task's own guidance."""
    for name, facts in ref.mistakes.items():
        try:
            if matches(facts):
                return MISTAKES[name]
        except (KeyError, TypeError, ZeroDivisionError):
            continue
    return fallback


def check(check_id: str, ok: bool, label: Message, message: Message | Callable[[], Message]) -> CheckResult:
    if ok:
        return CheckResult(check_id, True, None, label)
    return CheckResult(check_id, False, message() if callable(message) else message, label)


# ─── Running learner code twice (real data, then the hidden variant) ──────────

Checker = Callable[[Any, F.Facts, Reference], list[CheckResult]]


async def python_task(ctx: ValidationContext, path: str, capture: list[str], checker: Checker) -> ValidationResult:
    ref = reference(ctx)
    run = await ctx.run_python(path, capture)
    if not run.succeeded:
        return execution_error(path, run)
    checks = checker(run.captured, ref.facts, ref)
    return await _variant_step(ctx, checks, lambda: ctx.run_python(path, capture, ref.variant_inline),
                               lambda result: checker(result.captured, ref.variant_facts, ref), path)


async def sql_task(ctx: ValidationContext, path: str, checker: Checker) -> ValidationResult:
    ref = reference(ctx)
    run = await ctx.run_sql(path)
    if not run.succeeded:
        return execution_error(path, run)
    checks = checker(run.table, ref.facts, ref)
    return await _variant_step(ctx, checks, lambda: ctx.run_sql(path, ref.variant_inline),
                               lambda result: checker(result.table, ref.variant_facts, ref), path)


FINDINGS = "findings.md"


def insight_checks(ctx: ValidationContext) -> list[CheckResult]:
    """A task may also ask the learner to record what the result MEANS in
    findings.md (config `insight`: heading, aliases, min_words, min_items).
    Only presence and length are checked — the interpretation is theirs."""
    spec = ctx.config.get("insight")
    return section_checks(ctx, FINDINGS, spec) if spec else []


async def _variant_step(ctx, checks, rerun, recheck, path) -> ValidationResult:
    if all(c.passed for c in checks):
        result = await rerun()
        if result.status == "infrastructure_error":
            return execution_error(path, result)
        same = result.succeeded and all(c.passed for c in recheck(result))
        checks.append(CheckResult("computed_from_data", same, None if same else COMPUTED_FROM_DATA, COMPUTED_LABEL))
    else:
        checks.append(CheckResult("computed_from_data", False, AFTER_ABOVE, COMPUTED_LABEL, pending=True))
    return from_checks(checks + insight_checks(ctx))


# ─── Milestone 2 — Understand the data (analysis/inspect_data.py) ────────────

def _profile(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    counts = as_mapping(observed(captured, "row_counts"))
    keys_ok = counts is not None and set(counts) == set(F.TABLES)
    values_ok = keys_ok and all(count_equal(counts[t], facts.row_counts[t]) for t in F.TABLES)
    deduped = keys_ok and count_equal(counts.get("orders"), facts.row_counts["orders"] - facts.duplicate_rows["orders"])
    span = observed(captured, "order_date_range")
    span_ok = (isinstance(span, list) and len(span) == 2
               and [str(v)[:10] for v in span] == list(facts.order_date_range))
    return [
        check("row_counts_keys", keys_ok, _msg("row_counts has the four tables", "يضم row_counts الجداول الأربعة"),
              _msg("row_counts must be a dictionary with exactly the keys customers, orders, order_items and products.",
                   "يجب أن يكون row_counts قاموسًا مفاتيحه customers وorders وorder_items وproducts فقط.")),
        check("row_counts_values", values_ok, _msg("Row count of each raw file", "عدد صفوف كل ملف خام"),
              _msg("Count the rows of each file exactly as exported — before removing anything." if deduped else
                   "Each value should be the number of data rows in that file (not counting the header).",
                   "احسب صفوف كل ملف كما صُدِّر تمامًا — قبل حذف أي شيء." if deduped else
                   "يجب أن تكون كل قيمة عدد صفوف البيانات في ذلك الملف (من دون سطر العناوين).")),
        check("order_date_range", span_ok, _msg("First and last order date", "أول وآخر تاريخ طلب"),
              _msg("order_date_range should be a list of two dates, [first, last], taken from order_date in orders.csv.",
                   "يجب أن تكون order_date_range قائمة من تاريخين [الأول، الأخير] من العمود order_date في orders.csv.")),
    ]


@validator("masar_commerce.profile_tables")
async def profile_tables(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/inspect_data.py"),
                             ["row_counts", "order_date_range"], _profile)


def _quality(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    dups = as_mapping(observed(captured, "duplicate_rows"))
    dups_ok = (dups is not None and set(dups) == {"orders", "order_items"}
               and all(count_equal(dups[k], facts.duplicate_rows[k]) for k in ("orders", "order_items")))
    doubled = dups is not None and all(count_equal(dups.get(k), 2 * facts.duplicate_rows[k]) for k in ("orders", "order_items"))
    city_ok = count_equal(observed(captured, "missing_city"), facts.missing_city)
    country_ok = count_equal(observed(captured, "inconsistent_countries"), facts.inconsistent_countries)
    return [
        check("duplicate_rows", dups_ok, _msg("Exact duplicate rows in orders and order_items",
                                              "الصفوف المكررة تمامًا في orders وorder_items"),
              _msg("Count only the extra copies: a row that repeats an earlier row counts once, the original does not."
                   if doubled else
                   "duplicate_rows needs the keys orders and order_items, each the number of rows that exactly repeat "
                   "an earlier row in that file.",
                   "احسب النسخ الزائدة فقط: الصف الذي يكرر صفًا سابقًا يُحسب مرة واحدة، والأصل لا يُحسب."
                   if doubled else
                   "يحتاج duplicate_rows إلى المفتاحين orders وorder_items، وقيمة كل منهما عدد الصفوف التي تكرر "
                   "صفًا سابقًا تمامًا في ذلك الملف.")),
        check("missing_city", city_ok, _msg("Customers with no city", "العملاء بلا مدينة"),
              _msg("missing_city should count customers whose city is empty in customers.csv.",
                   "يجب أن يعدّ missing_city العملاء الذين حقل المدينة لديهم فارغ في customers.csv.")),
        check("inconsistent_countries", country_ok, _msg("Badly formatted country values", "قيم الدولة غير المنسّقة"),
              _msg("Count customer rows whose country differs from its clean form — extra spaces or the wrong "
                   "capitalisation (compare each value with its stripped, title-cased version).",
                   "اعدد صفوف العملاء التي تختلف فيها الدولة عن صيغتها النظيفة — مسافات زائدة أو حالة أحرف خاطئة "
                   "(قارن كل قيمة بنسختها بعد strip وtitle).")),
    ]


@validator("masar_commerce.quality_issues")
async def quality_issues(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/inspect_data.py"),
                             ["duplicate_rows", "missing_city", "inconsistent_countries"], _quality)


def _orders_customers(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    by_status = as_mapping(observed(captured, "orders_by_status"))
    status_ok = mapping_matches(by_status, {k: float(v) for k, v in facts.orders_by_status.items()}, count_equal)
    raw_counts: dict[str, float] = {}
    for order in ref.data["orders"]:
        raw_counts[order["status"]] = raw_counts.get(order["status"], 0) + 1
    raw = mapping_matches(by_status, raw_counts, count_equal)
    never_ok = count_equal(observed(captured, "customers_without_orders"), facts.customers_without_orders)
    return [
        check("orders_by_status", status_ok, _msg("Orders per status", "الطلبات لكل حالة"),
              _msg("Count each order once — the raw file repeats some orders." if raw else
                   "orders_by_status should map every status in orders.csv to its number of distinct orders.",
                   "احسب كل طلب مرة واحدة — الملف الخام يكرر بعض الطلبات." if raw else
                   "يجب أن يربط orders_by_status كل حالة في orders.csv بعدد طلباتها المختلفة.")),
        check("customers_without_orders", never_ok, _msg("Registered customers who never ordered",
                                                         "عملاء مسجلون لم يطلبوا قط"),
              _msg("Count customers in customers.csv whose customer_id never appears in orders.csv (any status).",
                   "اعدد العملاء في customers.csv الذين لا يظهر customer_id الخاص بهم في orders.csv إطلاقًا "
                   "(بأي حالة).")),
    ]


@validator("masar_commerce.orders_and_customers")
async def orders_and_customers(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/inspect_data.py"),
                             ["orders_by_status", "customers_without_orders"], _orders_customers)


# ─── Milestone 3 — Prepare and clean (analysis/clean_data.py) ────────────────

def _frame(value: Any) -> tuple[list[str], list[dict], int] | None:
    if isinstance(value, dict) and value.get("__dataframe__"):
        shape = value.get("shape") or [0, 0]
        return [str(c) for c in value.get("columns") or []], value.get("records") or [], int(shape[0])
    return None


NOT_A_FRAME = {
    "en": "{name} must be a pandas DataFrame — run the file and check it builds the table.",
    "ar": "يجب أن يكون {name} جدول DataFrame من pandas — شغّل الملف وتأكد أنه يبني الجدول.",
}


def _not_frame(name: str) -> Message:
    return {k: v.format(name=name) for k, v in NOT_A_FRAME.items()}


def _clean_duplicates(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    orders = _frame(observed(captured, "orders_clean"))
    items = _frame(observed(captured, "items_clean"))
    checks = []
    for name, frame, key, expected_ids, raw in (
        ("orders_clean", orders, "order_id", facts.order_ids, facts.row_counts["orders"]),
        ("items_clean", items, "order_item_id", facts.order_item_ids, facts.row_counts["order_items"]),
    ):
        label = _msg(f"{name}: one row per {key}", f"{name}: صف واحد لكل {key}")
        if frame is None:
            checks.append(check(f"{name}_unique", False, label, _not_frame(name)))
            continue
        columns, records, rows = frame
        ids = [str(r.get(key)) for r in records] if key in columns else []
        ok = rows == len(expected_ids) and len(ids) == rows and set(ids) == expected_ids
        if rows == raw:
            message = _msg(f"{name} still has the duplicate rows you found in milestone 2.",
                           f"ما زال {name} يحتوي الصفوف المكررة التي وجدتها في المرحلة 2.")
        elif key in columns and set(ids) < expected_ids:
            message = _msg(f"{name} lost real rows: remove only exact duplicates, keep every distinct {key}.",
                           f"فقد {name} صفوفًا حقيقية: احذف المكرر تمامًا فقط، واحتفظ بكل {key} مختلف.")
        else:
            message = _msg(f"{name} should keep every column and contain each {key} exactly once.",
                           f"يجب أن يحتفظ {name} بكل الأعمدة وأن يحتوي كل {key} مرة واحدة بالضبط.")
        checks.append(check(f"{name}_unique", ok, label, message))
    return checks


@validator("masar_commerce.clean_duplicates")
async def clean_duplicates(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/clean_data.py"),
                             ["orders_clean", "items_clean"], _clean_duplicates)


def _missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _clean_customers(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    frame = _frame(observed(captured, "customers_clean"))
    label_rows = _msg("Every customer kept", "الاحتفاظ بكل العملاء")
    label_country = _msg("Country names standardised", "توحيد أسماء الدول")
    label_city = _msg("No missing city values", "لا قيم مدينة مفقودة")
    if frame is None:
        return [check("customers_kept", False, label_rows, _not_frame("customers_clean"))]
    columns, records, rows = frame
    ids = [str(r.get("customer_id")) for r in records]
    kept = rows == len(facts.customer_ids) and set(ids) == facts.customer_ids
    dropped_missing = rows == len(facts.customer_ids) - facts.missing_city
    countries = {r.get("country") for r in records}
    country_ok = "country" in columns and countries == facts.countries
    city_ok = "city" in columns and rows > 0 and not any(_missing(r.get("city")) for r in records)
    return [
        check("customers_kept", kept, label_rows,
              _msg("Customers with a missing city were dropped. Keep every customer and fill the city instead "
                   "(for example with \"Unknown\")." if dropped_missing else
                   "customers_clean should have exactly one row for every customer in customers.csv.",
                   "تم حذف العملاء الذين مدينتهم مفقودة. احتفظ بكل العملاء واملأ المدينة بدلًا من ذلك "
                   "(مثلًا بـ \"Unknown\")." if dropped_missing else
                   "يجب أن يحتوي customers_clean صفًا واحدًا بالضبط لكل عميل في customers.csv.")),
        check("countries_standardised", country_ok, label_country,
              _msg("Some country values still differ only by spaces or capitalisation. Strip spaces and use one "
                   "consistent capitalisation so each country has a single spelling.",
                   "ما زالت بعض قيم الدولة تختلف فقط في المسافات أو حالة الأحرف. احذف المسافات ووحّد حالة الأحرف "
                   "ليصبح لكل دولة تهجئة واحدة.")),
        check("city_filled", city_ok, label_city,
              _msg("Some customers still have no city. Fill missing cities with a clear placeholder such as "
                   "\"Unknown\" rather than dropping the customer.",
                   "ما زال بعض العملاء بلا مدينة. املأ المدن المفقودة بقيمة واضحة مثل \"Unknown\" بدلًا من حذف العميل.")),
    ]


@validator("masar_commerce.clean_customers")
async def clean_customers(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/clean_data.py"), ["customers_clean"], _clean_customers)


SALES_COLUMNS = ("order_id", "order_date", "customer_id", "region", "segment", "product_id", "product_name",
                 "category", "quantity", "unit_price", "list_price", "line_revenue")


def _sales(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    frame = _frame(observed(captured, "sales"))
    label_cols = _msg("sales has the required columns", "يضم sales الأعمدة المطلوبة")
    label_rows = _msg("One row per order line of a completed order", "صف لكل سطر من طلب مكتمل")
    label_rev = _msg("line_revenue adds up to recognised revenue", "مجموع line_revenue يساوي الإيرادات المعترف بها")
    if frame is None:
        return [check("sales_columns", False, label_cols, _not_frame("sales"))]
    columns, records, rows = frame
    missing = [c for c in SALES_COLUMNS if c not in columns]
    cols_ok = not missing
    order_ids = {str(r.get("order_id")) for r in records}
    rows_ok = cols_ok and rows == facts.sales_rows and len(records) == rows and order_ids == facts.sales_order_ids
    total = sum(as_number(r.get("line_revenue")) or 0.0 for r in records) if cols_ok else None
    rev_ok = rows_ok and total is not None and money_close(total, facts.revenue)

    def rows_message() -> Message:
        if rows == 0:
            return _msg("sales is empty — build it in build_sales().", "الجدول sales فارغ — ابنِه داخل build_sales().")
        return diagnose(lambda m: rows == m.sales_rows, ref, _msg(
            "sales should contain exactly the order lines of completed orders. Check the status filter and the joins: "
            "an inner join to a table with missing or repeated keys changes the row count.",
            "يجب أن يحتوي sales أسطر الطلبات المكتملة فقط بالضبط. راجع شرط الحالة وعمليات الربط: الربط مع جدول "
            "فيه مفاتيح مفقودة أو مكررة يغيّر عدد الصفوف."))
    return [
        check("sales_columns", cols_ok, label_cols,
              _msg("sales is missing columns: " + ", ".join(missing) + ".", "ينقص sales الأعمدة: " + "، ".join(missing) + ".")),
        check("sales_rows", rows_ok, label_rows, rows_message),
        check("sales_revenue", rev_ok, label_rev, lambda: diagnose(
            lambda m: total is not None and money_close(total, m.revenue), ref,
            _msg("line_revenue should be quantity × unit_price for each line.",
                 "يجب أن يكون line_revenue هو quantity × unit_price لكل سطر."))),
    ]


@validator("masar_commerce.build_sales")
async def build_sales(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/clean_data.py"), ["sales"], _sales)


# ─── SQL helpers (milestones 4 and 7) ────────────────────────────────────────

def _table(table: Any, required: tuple[str, ...]) -> tuple[list[dict[str, Any]] | None, list[str]]:
    """Records keyed by lower-case column name, and the required columns missing."""
    if not isinstance(table, dict):
        return None, list(required)
    columns = [str(c).strip().lower() for c in table.get("columns") or []]
    missing = [c for c in required if c not in columns]
    records = [dict(zip(columns, row)) for row in table.get("rows") or []]
    return records, missing


def _columns_check(missing: list[str], required: tuple[str, ...]) -> CheckResult:
    return check("columns", not missing, _msg("Columns: " + ", ".join(required), "الأعمدة: " + "، ".join(required)),
                 _msg("Name the result columns exactly " + ", ".join(required) + " (use AS). Missing: "
                      + ", ".join(missing) + ".",
                      "سمِّ أعمدة النتيجة بالضبط " + "، ".join(required) + " (استخدم AS). الناقص: "
                      + "، ".join(missing) + "."))


def _keyed(records: list[dict], key: str, value: str, *, months: bool = False) -> dict[str, Any] | None:
    out: dict[str, Any] = {}
    for record in records:
        k = month_key(record.get(key)) if months else str(record.get(key)).strip()
        if k is None or k in out:
            return None
        out[k] = record.get(value)
    return out


def _sql_category(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("category", "revenue")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    got = _keyed(records, "category", "revenue")
    rows_ok = got is not None and set(got) == set(facts.category_revenue)
    values_ok = rows_ok and mapping_matches(got, facts.category_revenue, money_close)
    checks.append(check("rows", rows_ok, _msg("One row per category", "صف لكل فئة"),
                        _msg("Return exactly one row per product category that sold.",
                             "أعد صفًا واحدًا بالضبط لكل فئة منتجات بيعت.")))
    checks.append(check("revenue", values_ok, _msg("Recognised revenue per category", "الإيرادات المعترف بها لكل فئة"),
                        lambda: diagnose(lambda m: mapping_matches(got, m.category_revenue, money_close), ref,
                                         _msg("Revenue per category should be the sum of quantity × unit_price over "
                                              "completed, deduplicated order lines.",
                                              "يجب أن تكون إيرادات كل فئة مجموع quantity × unit_price لأسطر الطلبات "
                                              "المكتملة بعد حذف المكرر."))))
    return checks


@validator("masar_commerce.sql_revenue_by_category")
async def sql_revenue_by_category(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/revenue_by_category.sql"), _sql_category)


def _sql_monthly(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("month", "revenue", "orders")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    months = [month_key(r.get("month")) for r in records]
    revenue = _keyed(records, "month", "revenue", months=True)
    orders = _keyed(records, "month", "orders", months=True)
    rows_ok = revenue is not None and set(revenue) == set(facts.monthly_revenue)
    order_ok = rows_ok and months == sorted(facts.monthly_revenue)
    rev_ok = rows_ok and mapping_matches(revenue, facts.monthly_revenue, money_close)
    orders_ok = rows_ok and mapping_matches(orders, {k: float(v) for k, v in facts.monthly_orders.items()}, count_equal)
    checks += [
        check("rows", rows_ok, _msg("One row per month", "صف لكل شهر"),
              _msg("Return one row per calendar month that has completed orders (month as '2025-01' or a date).",
                   "أعد صفًا لكل شهر فيه طلبات مكتملة (الشهر بصيغة '2025-01' أو تاريخ).")),
        check("calendar_order", order_ok, _msg("Months in calendar order", "الأشهر بالترتيب الزمني"),
              _msg("Sort the result by month, January first (ORDER BY).", "رتّب النتيجة حسب الشهر، يناير أولًا (ORDER BY).")),
        check("revenue", rev_ok, _msg("Revenue per month", "الإيرادات لكل شهر"),
              lambda: diagnose(lambda m: mapping_matches(revenue, m.monthly_revenue, money_close), ref,
                               _msg("Monthly revenue should sum quantity × unit_price of completed, deduplicated lines, "
                                    "grouped by the month of order_date.",
                                    "يجب أن تجمع إيرادات الشهر quantity × unit_price لأسطر الطلبات المكتملة بعد حذف "
                                    "المكرر، مجمّعة حسب شهر order_date."))),
        check("orders", orders_ok, _msg("Completed orders per month", "الطلبات المكتملة لكل شهر"),
              _msg("orders should count DISTINCT completed orders in each month, not order lines.",
                   "يجب أن يعدّ orders الطلبات المكتملة المختلفة (DISTINCT) في كل شهر، لا أسطر الطلبات.")),
    ]
    return checks


@validator("masar_commerce.sql_monthly_revenue")
async def sql_monthly_revenue(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/monthly_revenue.sql"), _sql_monthly)


def _sql_top_customers(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("customer_id", "revenue", "orders")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    ids = [str(r.get("customer_id")) for r in records]
    count_ok = len(records) == 10
    ids_ok = count_ok and ids == facts.top_customers
    # Judged per row, whatever the order: a ranking mistake is reported once, above.
    values_ok = bool(records) and all(
        str(r.get("customer_id")) in facts.customer_revenue
        and money_close(r.get("revenue"), facts.customer_revenue[str(r.get("customer_id"))])
        and count_equal(r.get("orders"), facts.customer_orders[str(r.get("customer_id"))])
        for r in records)
    same_set = count_ok and set(ids) == set(facts.top_customers)
    by_orders = (count_ok and not same_set and all(i in facts.customer_orders for i in ids)
                 and [facts.customer_orders[i] for i in ids] == facts.top_order_counts)
    checks += [
        check("ten_rows", count_ok, _msg("Exactly 10 customers", "10 عملاء بالضبط"),
              _msg("Return exactly 10 rows (LIMIT 10).", "أعد 10 صفوف بالضبط (LIMIT 10).")),
        check("ranking", ids_ok, _msg("The ten highest-revenue customers, highest first",
                                      "أعلى عشرة عملاء إيرادًا، الأعلى أولًا"),
              lambda: _msg("These are the right customers, but sort them by revenue, highest first.",
                           "هؤلاء هم العملاء الصحيحون، لكن رتّبهم حسب الإيرادات تنازليًا.") if same_set else
              _msg("The ranking appears to be based on the number of orders. Management asked for the most valuable "
                   "customers: rank by recognised revenue.",
                   "يبدو أن الترتيب مبني على عدد الطلبات. طلبت الإدارة العملاء الأعلى قيمةً: رتّب حسب الإيرادات "
                   "المعترف بها.") if by_orders else
              diagnose(lambda m: ids == m.top_customers, ref,
                       _msg("Rank customers by their recognised revenue (completed, deduplicated lines).",
                            "رتّب العملاء حسب إيراداتهم المعترف بها (أسطر مكتملة بعد حذف المكرر)."))),
        check("values", values_ok, _msg("Revenue and completed orders of each customer",
                                        "إيرادات كل عميل وطلباته المكتملة"),
              _msg("revenue is the customer's recognised revenue; orders counts their distinct completed orders.",
                   "revenue هي إيرادات العميل المعترف بها؛ وorders يعدّ طلباته المكتملة المختلفة.")),
    ]
    return checks


@validator("masar_commerce.sql_top_customers")
async def sql_top_customers(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/top_customers.sql"), _sql_top_customers)


def _sql_products(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("product_id", "product_name", "category", "units_sold", "revenue")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    by_id = {str(r.get("product_id")): r for r in records}
    all_ok = len(records) == len(facts.products) and set(by_id) == set(facts.products)
    lost_unsold = set(by_id) == set(facts.products) - facts.unsold_products
    present = [p for p in by_id if p in facts.products]
    nulls = any(by_id[p].get("units_sold") is None or by_id[p].get("revenue") is None for p in present)
    # Judged on the products that are present: missing ones are reported once, above.
    values_ok = bool(present) and not nulls and all(
        count_equal(by_id[p].get("units_sold"), facts.product_units[p])
        and money_close(by_id[p].get("revenue"), facts.product_revenue[p]) for p in present)
    checks += [
        check("every_product", all_ok, _msg("Every product in the catalogue appears once", "كل منتج في الكتالوج مرة واحدة"),
              _msg("Products that never sold are missing. Start from products and LEFT JOIN the sales to it."
                   if lost_unsold else "Return exactly one row for every product in products.csv.",
                   "المنتجات التي لم تُبع مفقودة. ابدأ من products واربط المبيعات بها بـ LEFT JOIN."
                   if lost_unsold else "أعد صفًا واحدًا بالضبط لكل منتج في products.csv.")),
        check("values", values_ok, _msg("Units sold and revenue per product", "الوحدات المبيعة والإيرادات لكل منتج"),
              lambda: _msg("Unsold products show NULL. Show them as 0 (COALESCE).",
                           "المنتجات غير المبيعة تظهر NULL. اعرضها 0 (COALESCE).") if nulls else
              diagnose(lambda m: bool(present) and all(money_close(by_id[p].get("revenue"), m.product_revenue[p])
                                                      for p in present),
                       ref, _msg("units_sold and revenue should count completed, deduplicated order lines only.",
                                 "يجب أن يحسب units_sold وrevenue أسطر الطلبات المكتملة بعد حذف المكرر فقط."))),
    ]
    return checks


@validator("masar_commerce.sql_product_performance")
async def sql_product_performance(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/product_performance.sql"), _sql_products)


def _sql_regions(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("region", "customers", "orders", "revenue", "aov")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    by_region = {str(r.get("region")).strip(): r for r in records}
    rows_ok = len(records) == len(facts.region_revenue) and set(by_region) == set(facts.region_revenue)
    rev = {k: r.get("revenue") for k, r in by_region.items()}
    rev_ok = rows_ok and mapping_matches(rev, facts.region_revenue, money_close)
    counts_ok = rows_ok and all(count_equal(by_region[k].get("customers"), facts.region_customers[k])
                                and count_equal(by_region[k].get("orders"), facts.region_orders[k])
                                for k in facts.region_revenue)
    aov_ok = rows_ok and all(money_close(by_region[k].get("aov"), facts.region_aov[k]) for k in facts.region_revenue)
    customers_are_orders = rows_ok and all(count_equal(by_region[k].get("customers"), facts.region_orders[k])
                                           for k in facts.region_revenue)
    checks += [
        check("rows", rows_ok, _msg("One row per region", "صف لكل منطقة"),
              _msg("Return one row per sales region (the region column of customers).",
                   "أعد صفًا لكل منطقة مبيعات (العمود region في customers).")),
        check("revenue", rev_ok, _msg("Revenue per region", "الإيرادات لكل منطقة"),
              lambda: diagnose(lambda m: mapping_matches(rev, m.region_revenue, money_close), ref,
                               _msg("Region revenue should sum completed, deduplicated order lines of that region's "
                                    "customers.", "يجب أن تجمع إيرادات المنطقة أسطر الطلبات المكتملة بعد حذف المكرر "
                                    "لعملاء تلك المنطقة."))),
        check("counts", counts_ok, _msg("Customers and completed orders per region", "العملاء والطلبات المكتملة لكل منطقة"),
              _msg("The customer count appears to count orders instead: a customer with three orders is still one "
                   "customer." if customers_are_orders else
                   "customers counts DISTINCT customers with a completed order; orders counts DISTINCT completed orders.",
                   "يبدو أن عدد العملاء يعدّ الطلبات بدلًا منهم: العميل صاحب ثلاثة طلبات يبقى عميلًا واحدًا."
                   if customers_are_orders else
                   "customers يعدّ العملاء المختلفين الذين لديهم طلب مكتمل؛ وorders يعدّ الطلبات المكتملة المختلفة.")),
        check("aov", aov_ok, _msg("Average order value per region", "متوسط قيمة الطلب لكل منطقة"),
              _msg("aov is the region's revenue divided by its completed orders.",
                   "aov هو إيرادات المنطقة مقسومة على عدد طلباتها المكتملة.")),
    ]
    return checks


@validator("masar_commerce.sql_regional_performance")
async def sql_regional_performance(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/regional_performance.sql"), _sql_regions)


def _sql_price_bands(table: Any, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    required = ("price_band", "products", "units_sold", "revenue")
    records, missing = _table(table, required)
    checks = [_columns_check(missing, required)]
    if missing or records is None:
        return checks
    by_band = {str(r.get("price_band")).strip().lower(): r for r in records}
    rows_ok = len(records) == 3 and set(by_band) == set(facts.price_bands)
    products_ok = rows_ok and all(count_equal(by_band[b].get("products"), facts.price_bands[b]["products"])
                                  for b in facts.price_bands)
    values_ok = rows_ok and all(count_equal(by_band[b].get("units_sold"), facts.price_bands[b]["units_sold"])
                                and money_close(by_band[b].get("revenue"), facts.price_bands[b]["revenue"])
                                for b in facts.price_bands)
    checks += [
        check("bands", rows_ok, _msg("Three bands: budget, mid, premium", "ثلاث شرائح: budget وmid وpremium"),
              _msg("Return exactly three rows labelled budget, mid and premium, using a CASE expression on list_price.",
                   "أعد ثلاثة صفوف بالضبط باسم budget وmid وpremium، باستخدام CASE على list_price.")),
        check("products", products_ok, _msg("Products per band (whole catalogue)", "المنتجات في كل شريحة (الكتالوج كله)"),
              _msg("products counts every catalogue product in the band — including ones that never sold. Check the "
                   "band boundaries: budget is below 500, premium is 1,500 and above.",
                   "products يعدّ كل منتجات الكتالوج في الشريحة — ومنها التي لم تُبع. راجع حدود الشرائح: budget أقل من "
                   "500، وpremium من 1,500 فأكثر.")),
        check("values", values_ok, _msg("Units sold and revenue per band", "الوحدات المبيعة والإيرادات لكل شريحة"),
              _msg("units_sold and revenue should come from completed, deduplicated order lines, with unsold "
                   "products contributing 0.",
                   "يجب أن يأتي units_sold وrevenue من أسطر الطلبات المكتملة بعد حذف المكرر، والمنتجات غير المبيعة "
                   "تُسهم بصفر.")),
    ]
    return checks


@validator("masar_commerce.sql_price_bands")
async def sql_price_bands(ctx: ValidationContext) -> ValidationResult:
    return await sql_task(ctx, ctx.config.get("file", "sql/price_bands.sql"), _sql_price_bands)


# ─── Milestone 5 — Core KPIs (analysis/kpis.py) ──────────────────────────────

KPI_GUIDE: dict[str, tuple[Message, Message, Callable[[Any, F.Facts], bool]]] = {
    "revenue": (_msg("Recognised revenue", "الإيرادات المعترف بها"),
                _msg("Recognised revenue is the sum of quantity × unit_price over completed order lines.",
                     "الإيرادات المعترف بها هي مجموع quantity × unit_price لأسطر الطلبات المكتملة."),
                lambda v, f: money_close(v, f.revenue)),
    "completed_orders": (_msg("Completed orders", "الطلبات المكتملة"),
                         _msg("Count distinct orders whose status is completed.",
                              "اعدد الطلبات المختلفة التي حالتها completed."),
                         lambda v, f: count_equal(v, f.completed_orders)),
    "aov": (_msg("Average order value (AOV)", "متوسط قيمة الطلب (AOV)"),
            _msg("AOV is recognised revenue divided by the number of completed orders — not the average order line.",
                 "AOV هو الإيرادات المعترف بها مقسومة على عدد الطلبات المكتملة — لا متوسط سطر الطلب."),
            lambda v, f: money_close(v, f.aov)),
    "unique_customers": (_msg("Purchasing customers", "العملاء المشترون"),
                         _msg("Count distinct customers with at least one completed order.",
                              "اعدد العملاء المختلفين الذين لديهم طلب مكتمل واحد على الأقل."),
                         lambda v, f: count_equal(v, f.unique_customers)),
    "items_sold": (_msg("Items sold", "القطع المبيعة"),
                   _msg("Sum the quantity of completed order lines (units, not lines).",
                        "اجمع quantity لأسطر الطلبات المكتملة (القطع، لا عدد الأسطر)."),
                   lambda v, f: count_equal(v, f.items_sold)),
}


def _kpis(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    kpis = as_mapping(observed(captured, "kpis"))
    defined = kpis is not None and all(k in kpis for k in KPI_GUIDE)
    checks = [check("kpis_defined", defined, _msg("kpis has the five keys", "يضم kpis المفاتيح الخمسة"),
                    _msg("kpis must be a dictionary with the keys " + ", ".join(KPI_GUIDE) + ".",
                         "يجب أن يكون kpis قاموسًا بالمفاتيح " + "، ".join(KPI_GUIDE) + "."))]
    values = kpis or {}
    for key, (label, guide, same) in KPI_GUIDE.items():
        value = values.get(key, MISSING)
        if key == "unique_customers" and count_equal(value, facts.completed_orders):
            guide = _msg("Purchasing customers appear to count orders instead: count each customer once, however many "
                         "orders they placed.",
                         "يبدو أن عدد العملاء المشترين يعدّ الطلبات بدلًا منهم: احسب كل عميل مرة واحدة مهما كان عدد "
                         "طلباته.")
        checks.append(check(key, same(value, facts), label,
                            lambda value=value, guide=guide, same=same: diagnose(lambda m: same(value, m), ref, guide)))
    return checks


@validator("masar_commerce.headline_kpis")
async def headline_kpis(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/kpis.py"), ["kpis"], _kpis)


def _at_risk(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    value = as_mapping(observed(captured, "status_value"))
    value_ok = mapping_matches(value, facts.status_value, money_close)
    rate_ok = rate_close(observed(captured, "cancellation_rate"), facts.cancellation_rate)
    return [
        check("status_value", value_ok, _msg("Order value by non-completed status", "قيمة الطلبات لكل حالة غير مكتملة"),
              _msg("status_value maps cancelled, returned and pending to the total quantity × unit_price of their "
                   "(deduplicated) order lines.",
                   "يربط status_value كلًا من cancelled وreturned وpending بمجموع quantity × unit_price لأسطر "
                   "طلباتها (بعد حذف المكرر).")),
        check("cancellation_rate", rate_ok, _msg("Cancellation rate", "معدل الإلغاء"),
              _msg("cancellation_rate is cancelled orders divided by ALL distinct orders, as a fraction between 0 and 1.",
                   "cancellation_rate هو الطلبات الملغاة مقسومة على كل الطلبات المختلفة، ككسر بين 0 و1.")),
    ]


@validator("masar_commerce.revenue_at_risk")
async def revenue_at_risk(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/kpis.py"),
                             ["status_value", "cancellation_rate"], _at_risk)


# ─── Milestone 6 — Customers (analysis/customers.py) ─────────────────────────

def _concentration(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    revenue = as_mapping(observed(captured, "customer_revenue"))
    share = observed(captured, "top_decile_share")
    percent = as_number(share) is not None and math.isclose(as_number(share) or 0, 100 * facts.top_decile_share, abs_tol=0.06)
    return [
        check("customer_revenue", mapping_matches(revenue, facts.customer_revenue, money_close),
              _msg("Revenue of every purchasing customer", "إيرادات كل عميل مشترٍ"),
              lambda: diagnose(lambda m: mapping_matches(revenue, m.customer_revenue, money_close), ref,
                               _msg("customer_revenue maps each customer with a completed order to their recognised "
                                    "revenue — no other customers.",
                                    "يربط customer_revenue كل عميل لديه طلب مكتمل بإيراداته المعترف بها — ولا أحد "
                                    "غيرهم."))),
        check("top_decile_share", rate_close(share, facts.top_decile_share),
              _msg("Revenue share of the top 10% of customers", "حصة أعلى 10% من العملاء من الإيرادات"),
              _msg("Give the share as a fraction between 0 and 1, not a percentage." if percent else
                   "Take the top 10% of purchasing customers by revenue (rounded down to a whole number of customers) "
                   "and divide their revenue by total recognised revenue.",
                   "اكتب الحصة ككسر بين 0 و1، لا كنسبة مئوية." if percent else
                   "خذ أعلى 10% من العملاء المشترين حسب الإيرادات (مقرّبًا لأسفل إلى عدد صحيح من العملاء) واقسم "
                   "إيراداتهم على إجمالي الإيرادات المعترف بها.")),
    ]


@validator("masar_commerce.customer_concentration")
async def customer_concentration(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/customers.py"),
                             ["customer_revenue", "top_decile_share"], _concentration)


def _repeat(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    rate = observed(captured, "repeat_customer_rate")
    rate_ok = rate_close(rate, facts.repeat_customer_rate)
    one_ok = count_equal(observed(captured, "one_time_customers"), facts.one_time_customers)
    avg = observed(captured, "avg_orders_per_customer")
    avg_ok = math.isclose(as_number(avg) or -1, facts.avg_orders_per_customer, abs_tol=6e-3)
    percent = as_number(rate) is not None and math.isclose(as_number(rate) or 0, 100 * facts.repeat_customer_rate, abs_tol=0.06)
    return [
        check("repeat_customer_rate", rate_ok, _msg("Repeat customer rate", "معدل العملاء المتكررين"),
              _msg("Give the rate as a fraction between 0 and 1, not a percentage." if percent else
                   "The repeat rate is the share of purchasing customers with two or more DISTINCT completed orders.",
                   "اكتب المعدل ككسر بين 0 و1، لا كنسبة مئوية." if percent else
                   "معدل التكرار هو نسبة العملاء المشترين الذين لديهم طلبان مكتملان مختلفان أو أكثر.")),
        check("one_time_customers", one_ok, _msg("One-time customers", "العملاء لمرة واحدة"),
              _msg("Count purchasing customers with exactly one distinct completed order.",
                   "اعدد العملاء المشترين الذين لديهم طلب مكتمل واحد فقط.")),
        check("avg_orders_per_customer", avg_ok, _msg("Average orders per purchasing customer", "متوسط الطلبات لكل عميل مشترٍ"),
              _msg("Average the number of DISTINCT completed orders per purchasing customer — not order lines.",
                   "احسب متوسط عدد الطلبات المكتملة المختلفة لكل عميل مشترٍ — لا أسطر الطلبات.")),
    ]


@validator("masar_commerce.repeat_behaviour")
async def repeat_behaviour(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/customers.py"),
                             ["repeat_customer_rate", "one_time_customers", "avg_orders_per_customer"], _repeat)


def _segments(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    revenue = as_mapping(observed(captured, "segment_revenue"))
    aov = as_mapping(observed(captured, "segment_aov"))
    return [
        check("segment_revenue", mapping_matches(revenue, facts.segment_revenue, money_close),
              _msg("Revenue per segment", "الإيرادات لكل شريحة عملاء"),
              lambda: diagnose(lambda m: mapping_matches(revenue, m.segment_revenue, money_close), ref,
                               _msg("segment_revenue maps consumer and business to their recognised revenue.",
                                    "يربط segment_revenue كلًا من consumer وbusiness بإيراداته المعترف بها."))),
        check("segment_aov", mapping_matches(aov, facts.segment_aov, money_close),
              _msg("Average order value per segment", "متوسط قيمة الطلب لكل شريحة"),
              _msg("A segment's AOV is its revenue divided by its DISTINCT completed orders.",
                   "AOV الشريحة هو إيراداتها مقسومة على طلباتها المكتملة المختلفة.")),
    ]


@validator("masar_commerce.customer_segments")
async def customer_segments(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/customers.py"),
                             ["segment_revenue", "segment_aov"], _segments)


# ─── Milestone 7 — Products (analysis/products.py) ───────────────────────────

def _category_mix(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    share = as_mapping(observed(captured, "category_share"))
    depth = as_mapping(observed(captured, "discount_by_category"))
    percent = share is not None and mapping_matches(share, {k: 100 * v for k, v in facts.category_share.items()},
                                                    lambda a, b: math.isclose(as_number(a) or -1, b, abs_tol=0.06))
    return [
        check("category_share", mapping_matches(share, facts.category_share, rate_close),
              _msg("Share of revenue per category", "حصة كل فئة من الإيرادات"),
              lambda: _msg("Give shares as fractions between 0 and 1 that add up to 1, not percentages.",
                           "اكتب الحصص ككسور بين 0 و1 مجموعها 1، لا كنسب مئوية.") if percent else
              diagnose(lambda m: mapping_matches(share, m.category_share, rate_close), ref,
                       _msg("A category's share is its recognised revenue divided by total recognised revenue.",
                            "حصة الفئة هي إيراداتها المعترف بها مقسومة على إجمالي الإيرادات المعترف بها."))),
        check("discount_by_category", mapping_matches(depth, facts.discount_by_category, rate_close),
              _msg("Discount depth per category", "عمق الخصم لكل فئة"),
              _msg("For each category compare what completed sales brought in with what the same units would have "
                   "brought at list price: 1 − (revenue ÷ list-price value), as a fraction.",
                   "لكل فئة قارن ما جلبته المبيعات المكتملة بما كانت ستجلبه الوحدات نفسها بسعر الكتالوج: "
                   "1 − (الإيرادات ÷ القيمة بسعر الكتالوج)، ككسر.")),
    ]


@validator("masar_commerce.category_mix")
async def category_mix(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/products.py"),
                             ["category_share", "discount_by_category"], _category_mix)


def _product_concentration(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    top5, top10 = observed(captured, "top5_share"), observed(captured, "top10_share")
    percent = as_number(top5) is not None and (as_number(top5) or 0) > 1
    guide = _msg("Rank products by recognised revenue, add up the revenue of the top 5 (or 10) and divide by total "
                 "recognised revenue." if not percent else "Give shares as fractions between 0 and 1, not percentages.",
                 "رتّب المنتجات حسب الإيرادات المعترف بها، واجمع إيرادات أعلى 5 (أو 10) واقسمها على إجمالي الإيرادات."
                 if not percent else "اكتب الحصص ككسور بين 0 و1، لا كنسب مئوية.")
    return [
        check("top5_share", rate_close(top5, facts.top5_product_share),
              _msg("Revenue share of the top 5 products", "حصة أعلى 5 منتجات من الإيرادات"),
              lambda: diagnose(lambda m: rate_close(top5, m.top5_product_share), ref, guide)),
        check("top10_share", rate_close(top10, facts.top10_product_share),
              _msg("Revenue share of the top 10 products", "حصة أعلى 10 منتجات من الإيرادات"),
              lambda: diagnose(lambda m: rate_close(top10, m.top10_product_share), ref, guide)),
    ]


@validator("masar_commerce.product_concentration")
async def product_concentration(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/products.py"),
                             ["top5_share", "top10_share"], _product_concentration)


# ─── Milestone 8 — Time and regions (analysis/trends.py) ─────────────────────

def _growth(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    mom = as_mapping(observed(captured, "mom_growth"), months=True)
    if mom is not None:
        mom = {k: v for k, v in mom.items() if v is not None}  # a leading NaN (January) serialises as null
    percent = mom is not None and mapping_matches(mom, {k: 100 * v for k, v in facts.mom_growth.items()},
                                                  lambda a, b: math.isclose(as_number(a) or -1e9, b, abs_tol=0.06))
    best = month_key(observed(captured, "best_month"))
    h2 = observed(captured, "h2_vs_h1_growth")
    return [
        check("mom_growth", mapping_matches(mom, facts.mom_growth, rate_close),
              _msg("Month-over-month growth", "النمو الشهري"),
              _msg("Give growth as fractions (0.25 means +25%), not percentages." if percent else
                   "mom_growth maps February to December to (this month's revenue ÷ the previous month's) − 1.",
                   "اكتب النمو ككسور (0.25 تعني ‎+25%)، لا كنسب مئوية." if percent else
                   "يربط mom_growth الأشهر من فبراير إلى ديسمبر بـ (إيرادات الشهر ÷ إيرادات الشهر السابق) − 1.")),
        check("best_month", best == facts.best_month, _msg("Best month", "أفضل شهر"),
              _msg("best_month is the 'YYYY-MM' month with the highest recognised revenue.",
                   "best_month هو الشهر بصيغة 'YYYY-MM' صاحب أعلى إيرادات معترف بها.")),
        check("h2_vs_h1_growth", rate_close(h2, facts.h2_vs_h1_growth), _msg("Second half vs first half", "النصف الثاني مقابل الأول"),
              _msg("h2_vs_h1_growth is (July–December revenue ÷ January–June revenue) − 1, as a fraction.",
                   "h2_vs_h1_growth هو (إيرادات يوليو–ديسمبر ÷ إيرادات يناير–يونيو) − 1، ككسر.")),
    ]


@validator("masar_commerce.growth")
async def growth(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/trends.py"),
                             ["mom_growth", "best_month", "h2_vs_h1_growth"], _growth)


def _regional_value(captured: dict, facts: F.Facts, ref: Reference) -> list[CheckResult]:
    share = as_mapping(observed(captured, "region_share"))
    per_customer = as_mapping(observed(captured, "revenue_per_customer"))
    return [
        check("region_share", mapping_matches(share, facts.region_share, rate_close),
              _msg("Share of revenue per region", "حصة كل منطقة من الإيرادات"),
              lambda: diagnose(lambda m: mapping_matches(share, m.region_share, rate_close), ref,
                               _msg("A region's share is its recognised revenue divided by total recognised revenue, "
                                    "as a fraction.",
                                    "حصة المنطقة هي إيراداتها المعترف بها مقسومة على إجمالي الإيرادات، ككسر."))),
        check("revenue_per_customer", mapping_matches(per_customer, facts.region_revenue_per_customer, money_close),
              _msg("Revenue per purchasing customer in each region", "الإيراد لكل عميل مشترٍ في كل منطقة"),
              _msg("Divide each region's recognised revenue by its number of DISTINCT purchasing customers — not by "
                   "its orders, and not by every registered customer.",
                   "اقسم إيرادات كل منطقة المعترف بها على عدد عملائها المشترين المختلفين — لا على طلباتها، ولا على كل "
                   "العملاء المسجلين.")),
    ]


@validator("masar_commerce.regional_value")
async def regional_value(ctx: ValidationContext) -> ValidationResult:
    return await python_task(ctx, ctx.config.get("file", "analysis/trends.py"),
                             ["region_share", "revenue_per_customer"], _regional_value)


# ─── Milestone 9 — Charts (analysis/visualize.py) ────────────────────────────

MIN_WIDTH, MIN_HEIGHT = 400, 250


def png_size(content_b64: str) -> tuple[int, int] | None:
    """(width, height) of a PNG, or None if it is not one."""
    try:
        raw = base64.b64decode(content_b64, validate=True)
    except (ValueError, TypeError):
        return None
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", raw[16:24])


CHART_DATA: dict[str, tuple[str, bool]] = {
    # expected fact -> (fact attribute, keys are months)
    "monthly_revenue": ("monthly_revenue", True),
    "category_revenue": ("category_revenue", False),
    "region_revenue": ("region_revenue", False),
}


@validator("masar_commerce.chart")
async def chart(ctx: ValidationContext) -> ValidationResult:
    """config: file, chart (path of the PNG), data_var, expected (CHART_DATA key)."""
    path = ctx.config.get("file", "analysis/visualize.py")
    chart_path = ctx.config["chart"]
    data_var = ctx.config["data_var"]
    attribute, months = CHART_DATA[ctx.config["expected"]]
    ref = reference(ctx)
    run = await ctx.run_python(path, [data_var])
    if not run.succeeded:
        return execution_error(path, run)
    produced = next((f for f in run.generated_files if f.get("path") == chart_path), None)
    size = png_size(produced["content"]) if produced and produced.get("encoding") == "base64" and produced.get("content") else None
    big_enough = size is not None and size[0] >= MIN_WIDTH and size[1] >= MIN_HEIGHT

    def data_ok(captured: dict, facts: F.Facts) -> bool:
        return mapping_matches(as_mapping(observed(captured, data_var), months=months), getattr(facts, attribute), money_close)

    checks = [
        check("chart_saved", produced is not None, _msg(f"{chart_path} is saved", f"تم حفظ {chart_path}"),
              _msg(f"Save the chart with plt.savefig(\"{chart_path}\") — exactly that path.",
                   f"احفظ الرسم بـ plt.savefig(\"{chart_path}\") — بهذا المسار بالضبط.")),
        check("chart_valid", big_enough, _msg("A readable PNG image", "صورة PNG مقروءة"),
              _msg(f"{chart_path} must be a PNG of at least {MIN_WIDTH}×{MIN_HEIGHT} pixels (the default figure size is fine).",
                   f"يجب أن يكون {chart_path} صورة PNG لا تقل عن {MIN_WIDTH}×{MIN_HEIGHT} بكسل (حجم الرسم الافتراضي مناسب).")),
        check("chart_data", data_ok(run.captured, ref.facts), _msg(f"{data_var} holds the plotted numbers",
                                                                   f"يحمل {data_var} الأرقام المرسومة"),
              lambda: diagnose(lambda m: data_ok(run.captured, m), ref,
                               _msg(f"{data_var} should hold exactly the values the chart plots, computed from the "
                                    "cleaned sales data (see the task for its shape).",
                                    f"يجب أن يحمل {data_var} القيم التي يرسمها الرسم بالضبط، محسوبة من بيانات المبيعات "
                                    "النظيفة (انظر المهمة لشكلها)."))),
    ]
    return await _variant_step(
        ctx, checks, lambda: ctx.run_python(path, [data_var], ref.variant_inline),
        lambda result: [CheckResult("x", data_ok(result.captured, ref.variant_facts))], path)


# ─── Milestone 10 — Executive report (report.md) ─────────────────────────────

REPORT = "report.md"
SECTION_AR = {
    "Executive Summary": ["الملخص التنفيذي"],
    "Business Performance": ["أداء الأعمال"],
    "Customer Insights": ["رؤى العملاء"],
    "Product Insights": ["رؤى المنتجات"],
    "Regional and Time Trends": ["الاتجاهات الإقليمية والزمنية"],
    "Key Risks": ["المخاطر الرئيسية"],
    "Recommendations": ["التوصيات"],
}
_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")
_NUMBER = re.compile(
    r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?\s*(million|mn|m|k|thousand|مليون|ملايين|ألف|الف|آلاف)?(?![a-z])",
    re.IGNORECASE)
_PERCENT = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(%|٪|percent|بالمئة|بالمائة|في المئة|في المائة)", re.IGNORECASE)
_SCALE = {"million": 1e6, "mn": 1e6, "m": 1e6, "مليون": 1e6, "ملايين": 1e6,
          "k": 1e3, "thousand": 1e3, "ألف": 1e3, "الف": 1e3, "آلاف": 1e3}
MONTH_NAMES = {
    "01": ["january", "jan", "يناير", "كانون الثاني"], "02": ["february", "feb", "فبراير", "شباط"],
    "03": ["march", "مارس", "آذار"], "04": ["april", "أبريل", "ابريل", "نيسان"], "05": ["may", "مايو", "أيار"],
    "06": ["june", "يونيو", "حزيران"], "07": ["july", "يوليو", "تموز"], "08": ["august", "أغسطس", "آب"],
    "09": ["september", "سبتمبر", "أيلول"], "10": ["october", "أكتوبر", "اكتوبر", "تشرين الأول"],
    "11": ["november", "نوفمبر", "تشرين الثاني"], "12": ["december", "ديسمبر", "كانون الأول"],
}
NAMES_AR = {
    "Egypt": ["مصر"], "Gulf": ["الخليج"], "Levant": ["الشام", "المشرق"], "North Africa": ["شمال أفريقيا", "شمال إفريقيا"],
    "Electronics": ["الإلكترونيات", "الالكترونيات", "إلكترونيات", "الكترونيات"],
    "Home & Kitchen": ["المنزل والمطبخ", "home and kitchen"], "Fashion": ["الأزياء", "الموضة"],
    "Beauty": ["التجميل", "الجمال"], "Books": ["الكتب"], "Sports": ["الرياضة", "الرياضية"],
}


def report_numbers(text: str) -> list[float]:
    text = text.translate(_ARABIC_DIGITS)
    out = []
    for match in _NUMBER.finditer(text):
        value = float(match.group(1).replace(",", "") + (match.group(2) or ""))
        scale = (match.group(3) or "").lower()
        out.append(value * _SCALE.get(scale, 1.0))
    return out


def report_percents(text: str) -> list[float]:
    return [float(m.group(1)) for m in _PERCENT.finditer(text.translate(_ARABIC_DIGITS))]


def mentions_number(text: str, expected: float, rel: float) -> bool:
    return any(math.isclose(n, expected, rel_tol=rel) for n in report_numbers(text))


def mentions_name(text: str, name: str) -> bool:
    lowered = text.casefold()
    return any(option.casefold() in lowered for option in [name, *NAMES_AR.get(name, [])])


def mentions_month(text: str, month: str) -> bool:
    lowered = text.casefold().translate(_ARABIC_DIGITS)
    names = MONTH_NAMES[month[5:7]]
    return month in lowered or any(re.search(rf"(?<!\w){re.escape(n)}(?!\w)", lowered) for n in names)


@validator("masar_commerce.report_metrics")
async def report_metrics(ctx: ValidationContext) -> ValidationResult:
    """The report states the analysis' key results in the right sections.
    Facts come from the real data; the report is prose, so tolerance allows
    rounding ("3.8 million", "3,812 EGP", "27%")."""
    facts = reference(ctx).facts
    text = ctx.file_text(REPORT) or ""

    def body(heading: str) -> str:
        return find_section(text, heading, SECTION_AR[heading]) or ""

    business, customers = body("Business Performance"), body("Customer Insights")
    products, trends = body("Product Insights"), body("Regional and Time Trends")
    repeat_pct = 100 * facts.repeat_customer_rate
    repeat_ok = (any(abs(p - repeat_pct) <= 1.0 for p in report_percents(customers))
                 or any(abs(n - facts.repeat_customer_rate) <= 0.01 for n in report_numbers(customers)))
    return from_checks([
        check("revenue", mentions_number(business, facts.revenue, 0.005),
              _msg("Business Performance states recognised revenue", "قسم أداء الأعمال يذكر الإيرادات المعترف بها"),
              _msg("State the recognised revenue you calculated in milestone 5 under Business Performance "
                   "(rounding such as “3.8 million” is fine).",
                   "اذكر الإيرادات المعترف بها التي حسبتها في المرحلة 5 تحت أداء الأعمال (التقريب مثل “3.8 مليون” مقبول).")),
        check("completed_orders", mentions_number(business, facts.completed_orders, 0.005),
              _msg("Business Performance states completed orders", "قسم أداء الأعمال يذكر الطلبات المكتملة"),
              _msg("State the number of completed orders under Business Performance.",
                   "اذكر عدد الطلبات المكتملة تحت أداء الأعمال.")),
        check("aov", mentions_number(business, facts.aov, 0.01),
              _msg("Business Performance states the average order value", "قسم أداء الأعمال يذكر متوسط قيمة الطلب"),
              _msg("State the average order value (AOV) under Business Performance.",
                   "اذكر متوسط قيمة الطلب (AOV) تحت أداء الأعمال.")),
        check("repeat_rate", repeat_ok,
              _msg("Customer Insights states the repeat customer rate", "قسم رؤى العملاء يذكر معدل العملاء المتكررين"),
              _msg("State the repeat customer rate from milestone 6 under Customer Insights, e.g. as a percentage.",
                   "اذكر معدل العملاء المتكررين من المرحلة 6 تحت رؤى العملاء، مثلًا كنسبة مئوية.")),
        check("top_category", mentions_name(products, facts.top_category),
              _msg("Product Insights names the leading category", "قسم رؤى المنتجات يسمّي الفئة الأولى"),
              _msg("Name the category that brings in the most revenue under Product Insights.",
                   "سمِّ الفئة صاحبة أعلى إيرادات تحت رؤى المنتجات.")),
        check("top_region", mentions_name(trends, facts.top_region),
              _msg("Regional and Time Trends names the leading region", "قسم الاتجاهات يسمّي المنطقة الأولى"),
              _msg("Name the region with the highest revenue under Regional and Time Trends.",
                   "سمِّ المنطقة صاحبة أعلى إيرادات تحت الاتجاهات الإقليمية والزمنية.")),
        check("best_month", mentions_month(trends, facts.best_month),
              _msg("Regional and Time Trends names the best month", "قسم الاتجاهات يسمّي أفضل شهر"),
              _msg("Name the month with the highest revenue under Regional and Time Trends.",
                   "سمِّ الشهر صاحب أعلى إيرادات تحت الاتجاهات الإقليمية والزمنية.")),
    ])


_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")


@validator("masar_commerce.report_charts")
async def report_charts(ctx: ValidationContext) -> ValidationResult:
    """report.md embeds the required charts, and each one exists (generated
    by a Run or Check of the visualisation script)."""
    required = list(ctx.config.get("required", []))
    minimum = int(ctx.config.get("min_charts", 3))
    # Code spans are examples, not embeds (the template shows one).
    text = re.sub(r"`[^`\n]*`", "", ctx.file_text(REPORT) or "")
    embedded = []
    for match in _IMAGE.finditer(text):
        target = match.group(1).lstrip("./")
        if target.startswith("charts/") and target not in embedded:
            embedded.append(target)
    missing_files = [p for p in embedded if p not in ctx.artifacts]
    absent_required = [p for p in required if p not in embedded]
    return from_checks([
        check("embedded", len(embedded) >= minimum,
              _msg(f"At least {minimum} charts embedded", f"تضمين {minimum} رسوم على الأقل"),
              _msg(f"Embed at least {minimum} of your charts with Markdown image syntax, e.g. "
                   "![Monthly revenue](charts/monthly_revenue.png).",
                   f"ضمّن {minimum} من رسومك على الأقل بصيغة صور Markdown، مثل "
                   "![Monthly revenue](charts/monthly_revenue.png).")),
        check("required", not absent_required, _msg("The required charts are embedded", "الرسوم المطلوبة مضمّنة"),
              _msg("Also embed: " + ", ".join(absent_required) + ".", "ضمّن أيضًا: " + "، ".join(absent_required) + ".")),
        check("generated", bool(embedded) and not missing_files,
              _msg("Every embedded chart has been generated", "كل رسم مضمّن تم توليده"),
              _msg("Not generated yet: " + ", ".join(missing_files) + ". Run analysis/visualize.py, then check again.",
                   "لم يُولَّد بعد: " + "، ".join(missing_files) + ". شغّل analysis/visualize.py ثم أعد التحقق.")
              if missing_files else _msg("Embed your charts first.", "ضمّن رسومك أولًا.")),
    ])
