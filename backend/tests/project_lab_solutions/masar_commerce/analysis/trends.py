import pandas as pd

from analysis.clean_data import load_clean_data

sales = load_clean_data()["sales"]
month = pd.to_datetime(sales["order_date"]).dt.strftime("%Y-%m")

s = sales.groupby(month)["line_revenue"].sum().sort_index()
mom_growth = s.pct_change().dropna().to_dict()
best_month = s.idxmax()
h2_vs_h1_growth = s[s.index > "2025-06"].sum() / s[s.index <= "2025-06"].sum() - 1

g = sales.groupby("region")
region_revenue = g["line_revenue"].sum()
region_share = region_revenue / region_revenue.sum()
revenue_per_customer = region_revenue / g["customer_id"].nunique()
print(best_month, h2_vs_h1_growth, region_share, revenue_per_customer)
