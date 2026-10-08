"""Milestone 2 — profile the RAW exports. Check Step reads the variables below."""
import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
order_items = pd.read_csv("data/order_items.csv")
products = pd.read_csv("data/products.csv")

for name, table in [("customers", customers), ("orders", orders),
                    ("order_items", order_items), ("products", products)]:
    print(f"--- {name}: {table.shape}")
    print(table.dtypes)
    print(table.head(3))

# Task: Profile the tables
row_counts = {}            # {"customers": ..., "orders": ..., "order_items": ..., "products": ...}
order_date_range = []      # ["YYYY-MM-DD", "YYYY-MM-DD"]: first and last order date

# Task: Find the data quality issues
duplicate_rows = {}        # {"orders": ..., "order_items": ...}: rows that exactly repeat an earlier row
missing_city = None        # customers with no city
inconsistent_countries = None  # customer rows whose country is not in its clean, canonical form

# Task: Understand orders and customers
orders_by_status = {}      # {status: number of distinct orders}
customers_without_orders = None  # registered customers who never placed an order

print("row_counts:", row_counts)
print("order_date_range:", order_date_range)
print("duplicate_rows:", duplicate_rows)
print("missing_city:", missing_city, "| inconsistent_countries:", inconsistent_countries)
print("orders_by_status:", orders_by_status)
print("customers_without_orders:", customers_without_orders)
