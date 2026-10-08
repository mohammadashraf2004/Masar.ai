"""Milestone 6 — customer analysis."""
from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]

# Customer concentration
customer_revenue = {}        # {customer_id: recognised revenue}
top_decile_share = None      # fraction (0-1)

# Repeat purchase behaviour
repeat_customer_rate = None  # fraction (0-1)
one_time_customers = None
avg_orders_per_customer = None

# Consumer and business customers
segment_revenue = {}         # {"consumer": ..., "business": ...}
segment_aov = {}             # {"consumer": ..., "business": ...}

print(top_decile_share)
print(repeat_customer_rate, one_time_customers, avg_orders_per_customer)
print(segment_revenue, segment_aov)
