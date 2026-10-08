"""Generate the synthetic Masar Commerce datasets for the Project Lab capstone.

Deterministic: a fixed seed and no dependency on the clock, so re-running it
reproduces the committed CSVs byte for byte, and every expected metric the
private validators compute is reproducible. The data is invented: no names,
no contact details, no real customers.

    python scripts/generate_masar_commerce_data.py

Writes backend/project_templates/masar-commerce-analysis/workspace/data/*.csv
and prints a summary. DATASET_VERSION must match the project definition's
template_version suffix when the data changes.

Intentional, documented quality issues (the README's "Known data issues"
section and the capstone's milestones 2-3 are built on exactly these):

  1. orders.csv contains DUPLICATE_ORDER_ROWS exact duplicate rows (the export
     job re-sent some orders). Joining order lines to undeduplicated orders
     double-counts those orders' revenue.
  2. order_items.csv contains DUPLICATE_ITEM_ROWS exact duplicate rows (same
     order_item_id). Summing them double-counts revenue.
  3. customers.country is inconsistently formatted for some rows (extra
     spaces, lower/upper case), e.g. " egypt" or "SAUDI ARABIA". Applying
     strip() + title-case restores the canonical spelling in every case.
  4. customers.city is missing for some customers (empty field).
  5. orders.status mixes completed / cancelled / returned / pending; only
     completed orders are recognised revenue.

Analytical structure (stable, so findings are real and repeatable):
  * a growth trend through 2025, a Ramadan lift in March, a summer dip, and
    a White Friday / year-end peak in November-December;
  * four regions with different order volumes and basket values;
  * repeat customers and one-time customers; some registered customers never
    ordered;
  * popular and unpopular products, and two products that never sold;
  * category-specific discounting (unit_price below list_price).
No exact duplicates of any other kind, no other missing values, and no ties
among the top customers or top products (asserted below).
"""
from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

SEED = 2026_10_02
DATASET_VERSION = "2026.10.2"
OUT = Path(__file__).resolve().parents[1] / "project_templates" / "masar-commerce-analysis" / "workspace" / "data"

DUPLICATE_ORDER_ROWS = 24
DUPLICATE_ITEM_ROWS = 41

# country -> (region, cities, customer weight, basket multiplier)
COUNTRIES = {
    "Egypt": ("Egypt", ["Cairo", "Alexandria", "Giza", "Mansoura"], 0.42, 0.85),
    "Saudi Arabia": ("Gulf", ["Riyadh", "Jeddah", "Dammam"], 0.18, 1.35),
    "United Arab Emirates": ("Gulf", ["Dubai", "Abu Dhabi", "Sharjah"], 0.12, 1.45),
    "Qatar": ("Gulf", ["Doha"], 0.04, 1.5),
    "Kuwait": ("Gulf", ["Kuwait City"], 0.04, 1.4),
    "Jordan": ("Levant", ["Amman", "Irbid"], 0.08, 1.0),
    "Lebanon": ("Levant", ["Beirut"], 0.03, 1.05),
    "Morocco": ("North Africa", ["Casablanca", "Rabat", "Marrakesh"], 0.06, 0.9),
    "Tunisia": ("North Africa", ["Tunis", "Sfax"], 0.03, 0.88),
}

# category -> (products [(name, list_price, popularity)], typical discount choices)
CATALOGUE = {
    "Electronics": ([
        ("Wireless Earbuds", 1450, 9), ("Smart Watch", 3200, 6), ("Power Bank 20000mAh", 780, 8),
        ("Bluetooth Speaker", 1150, 5), ("USB-C Charger 65W", 620, 7), ("Laptop Stand", 540, 3),
        ("Mechanical Keyboard", 1890, 3), ("Noise Cancelling Headphones", 4600, 4),
    ], [0, 0, 0, 0.05, 0.10]),
    "Home & Kitchen": ([
        ("Coffee Grinder", 950, 4), ("Air Fryer", 2750, 8), ("Non-stick Pan Set", 1320, 5),
        ("Water Filter Jug", 410, 4), ("Desk Lamp", 480, 3), ("Storage Box Set", 260, 2),
        ("Electric Kettle", 690, 5),
    ], [0, 0, 0.05, 0.10]),
    "Fashion": ([
        ("Linen Shirt", 520, 6), ("Running Sneakers", 1650, 7), ("Leather Wallet", 390, 4),
        ("Travel Backpack", 980, 4), ("Cotton Abaya", 1150, 6), ("Sunglasses", 610, 3), ("Wool Scarf", 340, 1),
    ], [0, 0.10, 0.15, 0.20, 0.25]),
    "Beauty": ([
        ("Argan Oil Serum", 310, 6), ("Oud Perfume 50ml", 1750, 7), ("Sunscreen SPF50", 280, 6),
        ("Hair Dryer", 870, 3), ("Skincare Gift Set", 990, 3), ("Beard Trimmer", 760, 2),
    ], [0, 0, 0.05, 0.10]),
    "Books": ([
        ("Python for Data Analysis", 640, 3), ("Arabic Calligraphy Workbook", 220, 2),
        ("Statistics Made Simple", 450, 2), ("Business Strategy Guide", 380, 1), ("Children's Story Set", 290, 2),
    ], [0, 0, 0.05]),
    "Sports": ([
        ("Yoga Mat", 360, 4), ("Adjustable Dumbbells", 2400, 3), ("Football", 330, 3),
        ("Cycling Helmet", 720, 2), ("Resistance Bands", 190, 3), ("Insulated Bottle", 230, 4), ("Padel Racket", 1980, 3),
    ], [0, 0.05, 0.10]),
}
NEVER_SOLD = {"Wool Scarf", "Business Strategy Guide"}

# 2025 monthly demand: growth trend + Ramadan (March) + summer dip + Q4 peak.
MONTH_WEIGHT = {1: 0.78, 2: 0.80, 3: 1.05, 4: 0.88, 5: 0.90, 6: 0.80, 7: 0.76, 8: 0.82,
                9: 0.97, 10: 1.05, 11: 1.42, 12: 1.36}
N_CUSTOMERS = 1500
N_ORDERS = 4200


def _messy(country: str, rng: random.Random) -> str:
    return rng.choice([f" {country.lower()}", country.upper(), f"{country.lower()} ", f"  {country}"])


def build() -> dict[str, list[dict]]:
    rng = random.Random(SEED)

    products, popularity, discounts = [], [], {}
    pid = 1
    for category, (items, discount_choices) in CATALOGUE.items():
        discounts[category] = discount_choices
        for name, price, weight in items:
            products.append({"product_id": f"P{pid:03d}", "product_name": name, "category": category,
                             "list_price": f"{price:.2f}"})
            popularity.append(0 if name in NEVER_SOLD else weight)
            pid += 1

    customers, customer_meta = [], {}
    country_names = list(COUNTRIES)
    country_weights = [COUNTRIES[c][2] for c in country_names]
    for i in range(1, N_CUSTOMERS + 1):
        country = rng.choices(country_names, country_weights)[0]
        region, cities, _, basket = COUNTRIES[country]
        cid = f"C{i:04d}"
        customers.append({
            "customer_id": cid,
            "city": "" if rng.random() < 0.035 else rng.choice(cities),
            "country": _messy(country, rng) if rng.random() < 0.06 else country,
            "region": region,
            "segment": "business" if rng.random() < 0.16 else "consumer",
            "signup_date": (date(2024, 1, 1) + timedelta(days=rng.randrange(640))).isoformat(),
        })
        # Activity: about 9% never order, a long tail of one-time buyers, a
        # core of repeat buyers.
        roll = rng.random()
        activity = 0.0 if roll < 0.09 else (0.12 if roll < 0.60 else rng.choice([1.0, 1.5, 2.5, 4.0]))
        customer_meta[cid] = (activity, basket, customers[-1]["segment"])

    active = [c for c in customer_meta if customer_meta[c][0] > 0]
    active_weights = [customer_meta[c][0] for c in active]
    month_days = defaultdict(list)
    day = date(2025, 1, 1)
    while day.year == 2025:
        month_days[day.month].append(day)
        day += timedelta(days=1)
    months = list(MONTH_WEIGHT)
    month_weights = [MONTH_WEIGHT[m] * len(month_days[m]) for m in months]

    orders, items = [], []
    item_id = 1
    seen_customers: set[str] = set()
    for i in range(1, N_ORDERS + 1):
        # Guarantee every active customer appears at least once, then sample.
        cid = active[i - 1] if i - 1 < len(active) else rng.choices(active, active_weights)[0]
        seen_customers.add(cid)
        _, basket, segment = customer_meta[cid]
        month = rng.choices(months, month_weights)[0]
        order_day = rng.choice(month_days[month])
        status = rng.choices(["completed", "cancelled", "returned", "pending"], [80, 9, 5, 6])[0]
        if order_day >= date(2025, 12, 22):
            status = rng.choices(["completed", "pending"], [55, 45])[0]
        order_id = f"O{i:05d}"
        orders.append({"order_id": order_id, "customer_id": cid, "order_date": order_day.isoformat(),
                       "status": status, "payment_method": rng.choices(["card", "cash_on_delivery", "wallet"], [5, 3, 2])[0],
                       "channel": rng.choices(["web", "app"], [4, 6])[0]})
        n_lines = rng.choices([1, 2, 3, 4], [40, 33, 18, 9])[0]
        if basket > 1.2:
            n_lines = min(4, n_lines + rng.choice([0, 0, 1]))
        chosen = set()
        for _ in range(n_lines):
            product = rng.choices(products, popularity)[0]
            if product["product_id"] in chosen:
                continue
            chosen.add(product["product_id"])
            qty = rng.choices([1, 2, 3], [70, 22, 8])[0]
            if segment == "business":
                qty += rng.choice([0, 1, 2])
            discount = rng.choice(discounts[product["category"]])
            if month in (11, 12) and rng.random() < 0.4:
                discount = max(discount, 0.15)
            items.append({"order_item_id": f"OI{item_id:06d}", "order_id": order_id,
                          "product_id": product["product_id"], "quantity": qty,
                          "unit_price": f"{round(float(product['list_price']) * (1 - discount), 2):.2f}"})
            item_id += 1

    # Issue 1 and 2: exact duplicate rows, appended at deterministic positions.
    for row in rng.sample(orders, DUPLICATE_ORDER_ROWS):
        orders.insert(rng.randrange(len(orders)), dict(row))
    for row in rng.sample(items, DUPLICATE_ITEM_ROWS):
        items.insert(rng.randrange(len(items)), dict(row))

    return {"customers": customers, "products": products, "orders": orders, "order_items": items}


def _check(data: dict[str, list[dict]]) -> dict:
    """Invariants the capstone's expected answers rely on."""
    orders = {o["order_id"]: o for o in data["orders"]}
    items = {i["order_item_id"]: i for i in data["order_items"]}
    assert len(data["orders"]) - len(orders) == DUPLICATE_ORDER_ROWS
    assert len(data["order_items"]) - len(items) == DUPLICATE_ITEM_ROWS
    completed = {k for k, o in orders.items() if o["status"] == "completed"}
    by_customer, by_product = defaultdict(float), defaultdict(float)
    for line in items.values():
        if line["order_id"] in completed:
            value = int(line["quantity"]) * float(line["unit_price"])
            by_customer[orders[line["order_id"]]["customer_id"]] += value
            by_product[line["product_id"]] += value
    top_c = sorted(by_customer.values(), reverse=True)[:11]
    top_p = sorted(by_product.values(), reverse=True)[:6]
    assert len(set(round(v, 2) for v in top_c)) == len(top_c), "tie among the top customers"
    assert len(set(round(v, 2) for v in top_p)) == len(top_p), "tie among the top products"
    sold = set(by_product)
    unsold = {p["product_id"] for p in data["products"]} - sold
    names = {p["product_id"]: p["product_name"] for p in data["products"]}
    assert {names[p] for p in unsold} == NEVER_SOLD, unsold
    return {"revenue": round(sum(by_product.values()), 2), "completed_orders": len(completed),
            "unsold": sorted(unsold)}


def main() -> None:
    data = build()
    summary = _check(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in data.items():
        with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{name}.csv: {len(rows)} rows")
    print(f"dataset {DATASET_VERSION}: {summary}")


if __name__ == "__main__":
    main()
