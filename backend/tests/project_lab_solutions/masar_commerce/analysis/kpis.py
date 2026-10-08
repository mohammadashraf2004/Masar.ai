from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]
orders = data["orders"]
order_items = data["order_items"]

revenue = sales["line_revenue"].sum()
completed_orders = sales["order_id"].nunique()
kpis = {
    "revenue": revenue,
    "completed_orders": completed_orders,
    "aov": revenue / completed_orders,
    "unique_customers": sales["customer_id"].nunique(),
    "items_sold": sales["quantity"].sum(),
}

lines = order_items.merge(orders, on="order_id")
lines["value"] = lines["quantity"] * lines["unit_price"]
by_status = lines.groupby("status")["value"].sum()
status_value = {s: by_status.get(s, 0.0) for s in ("cancelled", "returned", "pending")}
cancellation_rate = (orders["status"] == "cancelled").mean()
print(kpis, status_value, cancellation_rate)
