import pandas as pd

TABLES = ("customers", "orders", "order_items", "products")


def load_raw():
    return {name: pd.read_csv(f"data/{name}.csv") for name in TABLES}


def clean_orders(orders):
    orders = orders.drop_duplicates().reset_index(drop=True)
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    return orders


def clean_order_items(order_items):
    return order_items.drop_duplicates().reset_index(drop=True)


def clean_customers(customers):
    customers = customers.copy()
    customers["country"] = customers["country"].str.strip().str.title()
    customers["city"] = customers["city"].fillna("Unknown")
    return customers


def clean_products(products):
    return products.copy()


def build_sales(orders, order_items, customers, products):
    completed = orders[orders["status"] == "completed"]
    sales = (order_items.merge(completed, on="order_id")
             .merge(customers, on="customer_id")
             .merge(products, on="product_id"))
    sales["line_revenue"] = sales["quantity"] * sales["unit_price"]
    return sales[["order_id", "order_date", "customer_id", "region", "segment", "product_id",
                  "product_name", "category", "quantity", "unit_price", "list_price", "line_revenue"]]


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
    print(sales.shape)
