"""Milestone 8 — time and regional analysis."""
from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]

# Growth and seasonality
mom_growth = {}              # {"2025-02": fraction, ..., "2025-12": fraction}
best_month = None            # "YYYY-MM"
h2_vs_h1_growth = None       # fraction

# Regional value
region_share = {}            # {region: fraction of recognised revenue}
revenue_per_customer = {}    # {region: recognised revenue per purchasing customer}

print(mom_growth)
print(best_month, h2_vs_h1_growth)
print(region_share, revenue_per_customer)
