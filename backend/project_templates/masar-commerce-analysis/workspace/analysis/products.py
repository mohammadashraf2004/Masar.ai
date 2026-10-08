"""Milestone 7 — product analysis."""
from analysis.clean_data import load_clean_data

data = load_clean_data()
sales = data["sales"]
products = data["products"]

# Category mix and discounting
category_share = {}          # {category: fraction of recognised revenue}
discount_by_category = {}    # {category: fraction}

# Product concentration
top5_share = None            # fraction (0-1)
top10_share = None           # fraction (0-1)

print(category_share)
print(discount_by_category)
print(top5_share, top10_share)
