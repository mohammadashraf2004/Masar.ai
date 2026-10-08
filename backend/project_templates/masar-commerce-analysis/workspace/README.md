# Masar Commerce — Business Performance Analysis

You have just joined **Masar Commerce** as a junior Data Analyst.

Masar Commerce is an online retailer selling electronics, home goods,
fashion, beauty products, books and sports equipment to customers in Egypt,
the Gulf, the Levant and North Africa. Sales have clearly changed during
2025, but management cannot say *why*. They have asked you to investigate
the company's data and deliver an executive report that answers:

1. How did the business perform overall in 2025?
2. How did revenue and orders move month by month?
3. Who are our customers — how many come back, and who matters most?
4. Which categories and products drive revenue, and which do not?
5. How do our regions compare?
6. What risks do you see, and what should we do next?

Your stakeholders are the CEO, the Head of Sales and the Head of Marketing.
They read conclusions and charts, not code.

## Your workspace

```
masar-commerce-analysis/
├── README.md                     this brief (read-only)
├── README.ar.md                  the same brief in Arabic (read-only)
├── analysis_plan.md              your plan: objective, questions, KPI definitions
├── findings.md                   your analysis log: what each result means
├── data/                         the company's data exports (read-only)
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── products.csv
├── sql/
│   ├── revenue_by_category.sql
│   ├── monthly_revenue.sql
│   ├── top_customers.sql
│   ├── product_performance.sql
│   ├── regional_performance.sql
│   └── price_bands.sql
├── analysis/
│   ├── inspect_data.py           understand the raw data
│   ├── clean_data.py             prepare analysis-ready data (other scripts import it)
│   ├── kpis.py                   core business KPIs
│   ├── customers.py              customer analysis
│   ├── products.py               category and product analysis
│   ├── trends.py                 time and regional analysis
│   └── visualize.py              decision-oriented charts
├── charts/                       charts your scripts save appear here
└── report.md                     the executive report
```

All paths are relative to the project root: read data with
`pd.read_csv("data/orders.csv")`. Scripts can reuse your cleaning code with
`from analysis.clean_data import load_clean_data`.

In SQL files, each raw dataset is a table named after its file: `customers`,
`orders`, `order_items` and `products`. SQL uses the DuckDB dialect.

All amounts are in Egyptian pounds (EGP). The data covers orders placed in
calendar year 2025.

## Data dictionary

**customers.csv** — one row per registered customer

| column | meaning |
| --- | --- |
| customer_id | unique customer id, e.g. `C0042` |
| city | city on the account (can be missing) |
| country | country on the account (see *Known data issues*) |
| region | sales region: `Egypt`, `Gulf`, `Levant` or `North Africa` |
| segment | `consumer` or `business` |
| signup_date | date the account was created |

**orders.csv** — one row per order

| column | meaning |
| --- | --- |
| order_id | unique order id, e.g. `O00042` |
| customer_id | who placed the order |
| order_date | date the order was placed (`YYYY-MM-DD`) |
| status | `completed`, `cancelled`, `returned` or `pending` |
| payment_method | `card`, `cash_on_delivery` or `wallet` |
| channel | `web` or `app` |

**order_items.csv** — one row per product line in an order

| column | meaning |
| --- | --- |
| order_item_id | unique line id |
| order_id | the order this line belongs to |
| product_id | the product sold |
| quantity | units on this line |
| unit_price | price actually charged per unit, after any discount |

**products.csv** — one row per product

| column | meaning |
| --- | --- |
| product_id | unique product id, e.g. `P007` |
| product_name | display name |
| category | product category |
| list_price | catalogue price before discounts |

Relationships: `orders.customer_id → customers.customer_id`,
`order_items.order_id → orders.order_id`,
`order_items.product_id → products.product_id`.

## Business rules

* **Recognised revenue** counts only **completed** orders. Cancelled and
  returned orders brought in no money; pending orders have not been paid yet.
* Revenue of an order line is `quantity × unit_price`.

## Known data issues

The data engineering team warned you that the exports are not clean. Part of
your job is to find and handle these problems before you trust any number.
Milestones 2 and 3 walk you through them.

## Available tools

Python with `pandas`, `numpy`, `matplotlib` and `duckdb`, and SQL (DuckDB).
There is no internet access and no package installation.

## How you work

1. Read the task on the left; it starts from a business question.
2. Edit the file the task names and press **Run** as often as you like.
3. Press **Check Step** when you think the task is done. Checks run your
   saved files against the data — and against a changed copy of the data, so
   your code must compute answers rather than contain typed-in numbers. They
   never look for exact code.
