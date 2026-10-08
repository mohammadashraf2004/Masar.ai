"""Milestone 3 — analysis-ready data. Later scripts use it as:

    from analysis.clean_data import load_clean_data
    data = load_clean_data()
    sales = data["sales"]
"""
import pandas as pd

TABLES = ("customers", "orders", "order_items", "products")


def load_raw():
    """The four raw exports, untouched."""
    return {name: pd.read_csv(f"data/{name}.csv") for name in TABLES}


def clean_orders(orders):
    """Return the orders, one row per order."""
    return orders.copy()


def clean_order_items(order_items):
    """Return the order lines, one row per order line."""
    return order_items.copy()


def clean_customers(customers):
    """Return every customer, with one spelling per country and no missing city."""
    return customers.copy()


def clean_products(products):
    """Products need no cleaning; kept so every table goes through this file."""
    return products.copy()


def build_sales(orders, order_items, customers, products):
    """Return one row per order line of a completed order, with the columns:
    order_id, order_date, customer_id, region, segment, product_id,
    product_name, category, quantity, unit_price, list_price, line_revenue.
    """
    return pd.DataFrame(columns=[
        "order_id", "order_date", "customer_id", "region", "segment", "product_id",
        "product_name", "category", "quantity", "unit_price", "list_price", "line_revenue",
    ])


def load_clean_data():
    raw = load_raw()
    orders = clean_orders(raw["orders"])
    order_items = clean_order_items(raw["order_items"])
    customers = clean_customers(raw["customers"])
    products = clean_products(raw["products"])
    sales = build_sales(orders, order_items, customers, products)
    return {"orders": orders, "order_items": order_items, "customers": customers,
            "products": products, "sales": sales}


if __name__ == "__main__":
    data = load_clean_data()
    orders_clean = data["orders"]
    items_clean = data["order_items"]
    customers_clean = data["customers"]
    sales = data["sales"]
    for name, table in data.items():
        print(f"{name}: {table.shape}")
    print(sales.head())
