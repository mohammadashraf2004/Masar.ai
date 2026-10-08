"""Expected results for the Masar Commerce capstone, computed from raw CSV rows.

Pure standard library and deterministic. The validators in masar_commerce.py
compare what a learner's code produced with these facts; nothing here is
ever sent to the sandbox or to the browser.

`analyze()` is the reference analysis — the business rules from the
project README:

* duplicates: exact duplicate rows in orders.csv and order_items.csv are
  export errors and are removed (one row per order_id / order_item_id);
* recognised revenue counts COMPLETED orders only;
* line revenue = quantity × unit_price (the price actually charged);
* country spelling is canonicalised with strip() + title case; a missing
  city does not remove a customer.

`analyze()` also accepts the mistakes learners typically make (keeping
duplicates, counting every status, using list_price), so a validator can
recognise a wrong number as a *specific* mistake and say what to
reconsider — without ever showing the expected value.

`variant()` derives the second, deterministic dataset every data check
reruns the learner's code on, so typed-in answers fail.
"""
from __future__ import annotations

import csv
import io
from collections import defaultdict
from dataclasses import dataclass, field

TABLES = ("customers", "orders", "order_items", "products")
STATUSES = ("completed", "cancelled", "returned", "pending")
REGIONS = ("Egypt", "Gulf", "Levant", "North Africa")
# Price bands used by sql/price_bands.sql (list_price, EGP).
BUDGET_BELOW = 500.0
PREMIUM_FROM = 1500.0

Data = dict[str, list[dict[str, str]]]


def canonical_country(value: str) -> str:
    return value.strip().title()


def price_band(list_price: float) -> str:
    if list_price < BUDGET_BELOW:
        return "budget"
    if list_price < PREMIUM_FROM:
        return "mid"
    return "premium"


def _unique_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple] = set()
    out = []
    for row in rows:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            out.append(row)
    return out


@dataclass
class Facts:
    # ── raw profile (milestone 2) ──
    row_counts: dict[str, int] = field(default_factory=dict)
    order_date_range: tuple[str, str] = ("", "")
    duplicate_rows: dict[str, int] = field(default_factory=dict)
    missing_city: int = 0
    inconsistent_countries: int = 0
    orders_by_status: dict[str, int] = field(default_factory=dict)
    customers_without_orders: int = 0
    # ── cleaned tables (milestone 3) ──
    order_ids: set[str] = field(default_factory=set)
    order_item_ids: set[str] = field(default_factory=set)
    customer_ids: set[str] = field(default_factory=set)
    countries: set[str] = field(default_factory=set)
    sales_rows: int = 0
    sales_order_ids: set[str] = field(default_factory=set)
    sales_quantity: int = 0
    # ── KPIs (milestone 5) ──
    revenue: float = 0.0
    completed_orders: int = 0
    aov: float = 0.0
    unique_customers: int = 0
    items_sold: int = 0
    status_value: dict[str, float] = field(default_factory=dict)
    cancellation_rate: float = 0.0
    # ── customers (milestone 6) ──
    customer_revenue: dict[str, float] = field(default_factory=dict)
    customer_orders: dict[str, int] = field(default_factory=dict)
    top_customers: list[str] = field(default_factory=list)
    repeat_customer_rate: float = 0.0
    one_time_customers: int = 0
    avg_orders_per_customer: float = 0.0
    segment_revenue: dict[str, float] = field(default_factory=dict)
    segment_aov: dict[str, float] = field(default_factory=dict)
    # ── products (milestone 7) ──
    category_revenue: dict[str, float] = field(default_factory=dict)
    category_share: dict[str, float] = field(default_factory=dict)
    product_revenue: dict[str, float] = field(default_factory=dict)
    product_units: dict[str, int] = field(default_factory=dict)
    products: dict[str, dict[str, str]] = field(default_factory=dict)
    top_products: list[str] = field(default_factory=list)
    unsold_products: set[str] = field(default_factory=set)
    discount_by_category: dict[str, float] = field(default_factory=dict)
    price_bands: dict[str, dict[str, float]] = field(default_factory=dict)
    # ── time and regions (milestone 8) ──
    monthly_revenue: dict[str, float] = field(default_factory=dict)
    monthly_orders: dict[str, int] = field(default_factory=dict)
    mom_growth: dict[str, float] = field(default_factory=dict)
    best_month: str = ""
    h2_vs_h1_growth: float = 0.0
    region_revenue: dict[str, float] = field(default_factory=dict)
    region_orders: dict[str, int] = field(default_factory=dict)
    region_customers: dict[str, int] = field(default_factory=dict)
    region_aov: dict[str, float] = field(default_factory=dict)
    top_region: str = ""
    top_category: str = ""
    # ── concentration and value (milestones 6-8) ──
    top_decile_share: float = 0.0      # revenue share of the top 10% of purchasing customers (floor)
    top_order_counts: list[int] = field(default_factory=list)  # the 10 largest per-customer order counts
    top5_product_share: float = 0.0
    top10_product_share: float = 0.0
    region_share: dict[str, float] = field(default_factory=dict)
    region_revenue_per_customer: dict[str, float] = field(default_factory=dict)


def analyze(data: Data, *, dedupe: bool = True, statuses: tuple[str, ...] = ("completed",),
            price: str = "unit_price") -> Facts:
    """The reference analysis (defaults), or a known mistake (arguments)."""
    facts = Facts()
    raw_orders, raw_items = data["orders"], data["order_items"]
    customers, products = data["customers"], data["products"]

    facts.row_counts = {name: len(data[name]) for name in TABLES}
    dates = sorted(o["order_date"] for o in raw_orders)
    facts.order_date_range = (dates[0], dates[-1]) if dates else ("", "")
    unique_orders, unique_items = _unique_rows(raw_orders), _unique_rows(raw_items)
    facts.duplicate_rows = {"orders": len(raw_orders) - len(unique_orders),
                            "order_items": len(raw_items) - len(unique_items)}
    facts.missing_city = sum(1 for c in customers if not c["city"].strip())
    facts.inconsistent_countries = sum(1 for c in customers if c["country"] != canonical_country(c["country"]))
    facts.orders_by_status = defaultdict(int)
    for order in unique_orders:
        facts.orders_by_status[order["status"]] += 1
    facts.orders_by_status = dict(facts.orders_by_status)
    ordering = {o["customer_id"] for o in raw_orders}
    facts.customers_without_orders = sum(1 for c in customers if c["customer_id"] not in ordering)

    orders = unique_orders if dedupe else raw_orders
    items = unique_items if dedupe else raw_items
    facts.order_ids = {o["order_id"] for o in unique_orders}
    facts.order_item_ids = {i["order_item_id"] for i in unique_items}
    facts.customer_ids = {c["customer_id"] for c in customers}
    facts.countries = {canonical_country(c["country"]) for c in customers}

    customer_by_id = {c["customer_id"]: c for c in customers}
    facts.products = {p["product_id"]: p for p in products}
    # An inner join, as pandas merge / SQL JOIN do: undeduplicated orders
    # multiply their lines, which is the classic double count.
    lines_by_order: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in items:
        lines_by_order[item["order_id"]].append(item)

    sales = []
    for order in orders:
        if order["status"] not in statuses:
            continue
        customer = customer_by_id.get(order["customer_id"])
        if customer is None:
            continue
        for item in lines_by_order.get(order["order_id"], []):
            product = facts.products.get(item["product_id"])
            if product is None:
                continue
            quantity = int(item["quantity"])
            unit = float(item["unit_price"] if price == "unit_price" else product["list_price"])
            sales.append({
                "order_id": order["order_id"], "month": order["order_date"][:7], "status": order["status"],
                "customer_id": order["customer_id"], "region": customer["region"], "segment": customer["segment"],
                "product_id": item["product_id"], "category": product["category"], "quantity": quantity,
                "revenue": quantity * unit, "list_value": quantity * float(product["list_price"]),
            })

    facts.sales_rows = len(sales)
    facts.sales_order_ids = {s["order_id"] for s in sales}
    facts.sales_quantity = sum(s["quantity"] for s in sales)
    facts.revenue = sum(s["revenue"] for s in sales)
    facts.completed_orders = len(facts.sales_order_ids)
    facts.aov = facts.revenue / facts.completed_orders if facts.completed_orders else 0.0
    facts.unique_customers = len({s["customer_id"] for s in sales})
    facts.items_sold = facts.sales_quantity

    # Order-line value of the orders that are NOT recognised revenue, on
    # deduplicated data whatever mistake is being modelled.
    value_by_status: dict[str, float] = defaultdict(float)
    unique_lines = lines_by_order_unique(unique_items)
    for order in unique_orders:
        for item in unique_lines.get(order["order_id"], []):
            value_by_status[order["status"]] += int(item["quantity"]) * float(item["unit_price"])
    facts.status_value = {s: value_by_status.get(s, 0.0) for s in ("cancelled", "returned", "pending")}
    facts.cancellation_rate = (facts.orders_by_status.get("cancelled", 0) / len(unique_orders)) if unique_orders else 0.0

    by_customer: dict[str, float] = defaultdict(float)
    orders_by_customer: dict[str, set[str]] = defaultdict(set)
    by_segment: dict[str, float] = defaultdict(float)
    segment_orders: dict[str, set[str]] = defaultdict(set)
    by_category: dict[str, float] = defaultdict(float)
    list_by_category: dict[str, float] = defaultdict(float)
    by_product: dict[str, float] = defaultdict(float)
    units_by_product: dict[str, int] = defaultdict(int)
    by_month: dict[str, float] = defaultdict(float)
    month_orders: dict[str, set[str]] = defaultdict(set)
    by_region: dict[str, float] = defaultdict(float)
    region_orders: dict[str, set[str]] = defaultdict(set)
    region_customers: dict[str, set[str]] = defaultdict(set)
    for s in sales:
        by_customer[s["customer_id"]] += s["revenue"]
        orders_by_customer[s["customer_id"]].add(s["order_id"])
        by_segment[s["segment"]] += s["revenue"]
        segment_orders[s["segment"]].add(s["order_id"])
        by_category[s["category"]] += s["revenue"]
        list_by_category[s["category"]] += s["list_value"]
        by_product[s["product_id"]] += s["revenue"]
        units_by_product[s["product_id"]] += s["quantity"]
        by_month[s["month"]] += s["revenue"]
        month_orders[s["month"]].add(s["order_id"])
        by_region[s["region"]] += s["revenue"]
        region_orders[s["region"]].add(s["order_id"])
        region_customers[s["region"]].add(s["customer_id"])

    facts.customer_revenue = dict(by_customer)
    facts.customer_orders = {k: len(v) for k, v in orders_by_customer.items()}
    facts.top_customers = [k for k, _ in sorted(by_customer.items(), key=lambda kv: (-kv[1], kv[0]))[:10]]
    buyers = len(facts.customer_orders)
    facts.repeat_customer_rate = (sum(1 for n in facts.customer_orders.values() if n >= 2) / buyers) if buyers else 0.0
    facts.one_time_customers = sum(1 for n in facts.customer_orders.values() if n == 1)
    facts.avg_orders_per_customer = (sum(facts.customer_orders.values()) / buyers) if buyers else 0.0
    facts.segment_revenue = dict(by_segment)
    facts.segment_aov = {k: by_segment[k] / len(segment_orders[k]) for k in by_segment}

    facts.category_revenue = dict(by_category)
    facts.category_share = {k: v / facts.revenue for k, v in by_category.items()} if facts.revenue else {}
    facts.product_revenue = {pid: by_product.get(pid, 0.0) for pid in facts.products}
    facts.product_units = {pid: units_by_product.get(pid, 0) for pid in facts.products}
    facts.top_products = [k for k, _ in sorted(by_product.items(), key=lambda kv: (-kv[1], kv[0]))[:5]]
    facts.unsold_products = {pid for pid in facts.products if units_by_product.get(pid, 0) == 0}
    facts.discount_by_category = {k: 1 - by_category[k] / list_by_category[k] for k in by_category if list_by_category[k]}
    bands: dict[str, dict[str, float]] = {b: {"products": 0, "units_sold": 0, "revenue": 0.0}
                                          for b in ("budget", "mid", "premium")}
    for pid, product in facts.products.items():
        band = bands[price_band(float(product["list_price"]))]
        band["products"] += 1
        band["units_sold"] += units_by_product.get(pid, 0)
        band["revenue"] += by_product.get(pid, 0.0)
    facts.price_bands = bands

    months = sorted(by_month)
    facts.monthly_revenue = {m: by_month[m] for m in months}
    facts.monthly_orders = {m: len(month_orders[m]) for m in months}
    facts.mom_growth = {months[i]: by_month[months[i]] / by_month[months[i - 1]] - 1
                        for i in range(1, len(months)) if by_month[months[i - 1]]}
    facts.best_month = max(months, key=lambda m: by_month[m]) if months else ""
    h1 = sum(v for m, v in by_month.items() if m[5:7] <= "06")
    h2 = sum(v for m, v in by_month.items() if m[5:7] > "06")
    facts.h2_vs_h1_growth = h2 / h1 - 1 if h1 else 0.0
    facts.region_revenue = dict(by_region)
    facts.region_orders = {k: len(v) for k, v in region_orders.items()}
    facts.region_customers = {k: len(v) for k, v in region_customers.items()}
    facts.region_aov = {k: by_region[k] / len(region_orders[k]) for k in by_region}
    facts.top_region = max(by_region, key=by_region.get) if by_region else ""
    facts.top_category = max(by_category, key=by_category.get) if by_category else ""

    # Concentration: sums of the n largest values are the same whatever order
    # ties come in, so these never depend on tie-breaking.
    ranked_customers = sorted(by_customer.values(), reverse=True)
    decile = len(ranked_customers) // 10
    facts.top_decile_share = sum(ranked_customers[:decile]) / facts.revenue if facts.revenue else 0.0
    facts.top_order_counts = sorted(facts.customer_orders.values(), reverse=True)[:10]
    ranked_products = sorted(facts.product_revenue.values(), reverse=True)
    facts.top5_product_share = sum(ranked_products[:5]) / facts.revenue if facts.revenue else 0.0
    facts.top10_product_share = sum(ranked_products[:10]) / facts.revenue if facts.revenue else 0.0
    facts.region_share = {k: v / facts.revenue for k, v in by_region.items()} if facts.revenue else {}
    facts.region_revenue_per_customer = {k: by_region[k] / len(region_customers[k]) for k in by_region}
    return facts


def lines_by_order_unique(unique_items: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in unique_items:
        grouped[item["order_id"]].append(item)
    return grouped


def variant(data: Data) -> Data:
    """The hidden-data rerun. Derived from the original so that every count,
    total AND ranking moves — a typed-in answer of any kind fails:

    * every order whose number is a multiple of 3 is dropped;
    * in the top region, orders numbered 1 mod 3 are dropped too (another
      region takes the lead);
    * in the best month, even-numbered orders are dropped too (another month
      becomes the best);
    * every line of the top product is dropped (it becomes unsold, and the
      product ranking shifts);
    * orders placed on the first or the last date are dropped (the date
      range moves);
    * even-numbered customers left without any order are dropped.

    Order lines and duplicate rows follow their orders, products are
    unchanged, and every intentional data issue stays present, so a correct
    analysis passes on the variant exactly as on the original."""
    reference = analyze(data)
    region_of = {c["customer_id"]: c["region"] for c in data["customers"]}

    def keep(order: dict[str, str]) -> bool:
        number = int(order["order_id"].lstrip("O"))
        if number % 3 == 0 or order["order_date"] in reference.order_date_range:
            return False
        if region_of.get(order["customer_id"]) == reference.top_region and number % 3 == 1:
            return False
        return not (order["order_date"][:7] == reference.best_month and number % 2 == 0)

    orders = [o for o in data["orders"] if keep(o)]
    kept = {o["order_id"] for o in orders}
    ordering = {o["customer_id"] for o in orders}
    customers = [c for c in data["customers"]
                 if c["customer_id"] in ordering or int(c["customer_id"].lstrip("C")) % 2 != 0]
    top_product = reference.top_products[0] if reference.top_products else None
    items = [i for i in data["order_items"] if i["order_id"] in kept and i["product_id"] != top_product]
    return dict(data, orders=orders, customers=customers, order_items=items)


def csv_text(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def inline(data: Data) -> dict[str, str]:
    """The variant as the runner's data_inline (replaces data/*.csv)."""
    return {f"data/{name}.csv": csv_text(data[name]) for name in ("customers", "orders", "order_items")}
