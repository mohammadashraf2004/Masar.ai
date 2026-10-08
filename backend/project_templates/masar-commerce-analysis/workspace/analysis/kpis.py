"""Milestone 5 — the core business KPIs management asked for."""
from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]            # completed order lines only
orders = data["orders"]          # every order, any status (deduplicated)
order_items = data["order_items"]

# Task: Headline KPIs
kpis = {
    "revenue": None,             # recognised revenue
    "completed_orders": None,
    "aov": None,                 # average order value
    "unique_customers": None,    # customers with at least one completed order
    "items_sold": None,          # units sold in completed orders
}

# Task: Revenue at risk
status_value = {}                # {"cancelled": ..., "returned": ..., "pending": ...}: order-line value per status
cancellation_rate = None         # share of all orders that were cancelled (0-1)

print(kpis)
print(status_value, cancellation_rate)
