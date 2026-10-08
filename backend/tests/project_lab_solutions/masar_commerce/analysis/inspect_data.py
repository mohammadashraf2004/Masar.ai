import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
order_items = pd.read_csv("data/order_items.csv")
products = pd.read_csv("data/products.csv")

row_counts = {"customers": len(customers), "orders": len(orders),
              "order_items": len(order_items), "products": len(products)}
order_date_range = [orders["order_date"].min(), orders["order_date"].max()]

duplicate_rows = {"orders": int(orders.duplicated().sum()), "order_items": int(order_items.duplicated().sum())}
missing_city = int(customers["city"].isna().sum())
inconsistent_countries = int((customers["country"] != customers["country"].str.strip().str.title()).sum())

orders_by_status = orders.drop_duplicates()["status"].value_counts().to_dict()
customers_without_orders = int((~customers["customer_id"].isin(orders["customer_id"])).sum())
print(row_counts, order_date_range, duplicate_rows, missing_city, inconsistent_countries)
print(orders_by_status, customers_without_orders)
