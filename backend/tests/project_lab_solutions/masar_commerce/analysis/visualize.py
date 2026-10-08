import matplotlib.pyplot as plt
import pandas as pd

from analysis.clean_data import load_clean_data

sales = load_clean_data()["sales"]
month = pd.to_datetime(sales["order_date"]).dt.strftime("%Y-%m")

monthly_chart_data = sales.groupby(month)["line_revenue"].sum().to_dict()
plt.figure(figsize=(8, 4.5))
plt.plot(list(monthly_chart_data), list(monthly_chart_data.values()), marker="o")
plt.title("When does Masar Commerce earn its revenue?")
plt.ylabel("EGP")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png")
plt.close()

category_chart_data = sales.groupby("category")["line_revenue"].sum().sort_values(ascending=False).to_dict()
plt.figure(figsize=(8, 4.5))
plt.bar(list(category_chart_data), list(category_chart_data.values()))
plt.title("Revenue by category")
plt.ylabel("EGP")
plt.tight_layout()
plt.savefig("charts/revenue_by_category.png")
plt.close()

region_chart_data = sales.groupby("region")["line_revenue"].sum().sort_values().to_dict()
plt.figure(figsize=(8, 4.5))
plt.barh(list(region_chart_data), list(region_chart_data.values()))
plt.title("Revenue by region")
plt.xlabel("EGP")
plt.tight_layout()
plt.savefig("charts/revenue_by_region.png")
plt.close()
