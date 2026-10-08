from analysis.clean_data import load_clean_data

sales = load_clean_data()["sales"]

customer_revenue = sales.groupby("customer_id")["line_revenue"].sum()
ranked = customer_revenue.sort_values(ascending=False)
top_decile_share = ranked.head(len(ranked) // 10).sum() / ranked.sum()

per_customer = sales.groupby("customer_id")["order_id"].nunique()
repeat_customer_rate = (per_customer >= 2).mean()
one_time_customers = int((per_customer == 1).sum())
avg_orders_per_customer = per_customer.mean()

g = sales.groupby("segment")
segment_revenue = g["line_revenue"].sum()
segment_aov = segment_revenue / g["order_id"].nunique()
print(top_decile_share, repeat_customer_rate)
