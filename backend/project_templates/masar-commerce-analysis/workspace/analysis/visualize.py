"""Milestone 9 — charts that answer a business question each.

Save every chart into charts/ with plt.savefig(...). Keep the numbers you
plot in the *_chart_data variables: Check Step compares them with the data.
"""
import matplotlib.pyplot as plt

from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]

# Task: Monthly revenue trend -> charts/monthly_revenue.png
monthly_chart_data = {}    # {"2025-01": revenue, ...}

# Task: Revenue by category -> charts/revenue_by_category.png
category_chart_data = {}   # {category: revenue}

# Task: Regional performance -> charts/revenue_by_region.png
region_chart_data = {}     # {region: revenue}
