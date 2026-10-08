from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]

category_revenue = sales.groupby("category")["line_revenue"].sum()
category_share = category_revenue / category_revenue.sum()
sales = sales.assign(list_value=sales["quantity"] * sales["list_price"])
totals = sales.groupby("category")[["line_revenue", "list_value"]].sum()
discount_by_category = (1 - totals["line_revenue"] / totals["list_value"]).to_dict()

product_revenue = sales.groupby("product_id")["line_revenue"].sum().sort_values(ascending=False)
top5_share = product_revenue.head(5).sum() / product_revenue.sum()
top10_share = product_revenue.head(10).sum() / product_revenue.sum()
print(category_share, discount_by_category, top5_share, top10_share)
