"""
backend/seeds/seed_data_analyst_topic1.py

Seeds full content (lesson + exercises + quiz + project) for:
  Track:  data-analyst
  Level:  order=1  (Python & SQL foundations)
  Topic:  order=1  (Python & SQL foundations)

Level and Topic are assumed to already exist as empty shells (titles seeded).
This script FETCHES them and only CREATES them if they genuinely don't exist.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz, DifficultyLevel
from app.models.progress import Enrollment, UserProgress, QuizAttempt, ProjectSubmission, MentorSession, UserSkillScore, EngineerScorecard
from app.models.community import Post, PostLike, PostComment, UserFollow
from app.models.exam import Exam, ExamAttempt, ProctoringEvent, Certificate
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage
from app.models.challenge import ChallengeProject, ChallengeAttempt, ExamPayment

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# LESSON CONTENT
# ---------------------------------------------------------------------------

LESSON_CONTENT = r"""# Python & SQL Foundations for Data Analysis

If you've ever opened a CSV export from a company's database and felt your stomach
drop at 200,000 rows of messy transaction data, this lesson is for you. Every data
analyst job in Cairo, Dubai, or Riyadh starts the same way: someone hands you raw
data and asks "can you tell me what's going on here?" Python and SQL are how you
answer that question.

This lesson assumes you know basic programming concepts (variables, loops,
functions) but have never used Python specifically for data work, and have never
written SQL before.

## Why Python *and* SQL?

They solve different problems:

- **SQL** lives where the data lives -- inside a database. It's how you ask a
  database a question and get back exactly the rows you need, without dragging
  millions of records into memory first.
- **Python** is what you use once the data is in your hands -- cleaning it,
  reshaping it, calculating things SQL is clumsy at, and eventually visualizing it.

A realistic day at a company like **Breadfast** (the Cairo grocery delivery
startup) looks like this: a product manager asks "which neighborhoods had the
highest order cancellation rate last month?" You write a SQL query against the
orders database to pull exactly the rows you need (orders from last month, joined
with neighborhood data), then you pull that result into Python with `pandas` to
calculate the cancellation rate per neighborhood and rank them.

You rarely use just one. Let's build both skills together.

## Part 1: SQL -- Asking the Database the Right Question

### SELECT, WHERE, and the shape of a query

Every SQL query that pulls data starts with the same three building blocks:

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

Imagine a simplified `orders` table for Breadfast:

| order_id | customer_id | neighborhood | order_total | status      | created_at          |
|----------|-------------|--------------|-------------|-------------|----------------------|
| 1001     | 55          | Maadi        | 340.50      | delivered   | 2026-05-03 14:22:00  |
| 1002     | 58          | Nasr City    | 120.00      | cancelled   | 2026-05-03 15:01:00  |
| 1003     | 55          | Maadi        | 89.25       | delivered   | 2026-05-04 09:10:00  |

To find every cancelled order:

```sql
SELECT order_id, customer_id, neighborhood, order_total
FROM orders
WHERE status = 'cancelled';
```

### Filtering with AND, OR, and IN

Real questions are rarely single-condition. "Cancelled orders in Maadi or Nasr
City during May 2026":

```sql
SELECT order_id, neighborhood, order_total, created_at
FROM orders
WHERE status = 'cancelled'
  AND neighborhood IN ('Maadi', 'Nasr City')
  AND created_at >= '2026-05-01'
  AND created_at <  '2026-06-01';
```

`IN` is cleaner than chaining `OR neighborhood = 'X' OR neighborhood = 'Y'` --
use it whenever you're checking membership in a list.

### Aggregation: GROUP BY, COUNT, AVG, SUM

This is where SQL stops being a filter and starts answering business questions.

"What's the cancellation rate per neighborhood?" requires two numbers per
neighborhood: total orders, and cancelled orders.

```sql
SELECT
    neighborhood,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM orders
WHERE created_at >= '2026-05-01' AND created_at < '2026-06-01'
GROUP BY neighborhood
ORDER BY cancellation_rate_pct DESC;
```

A few things to notice:
- `GROUP BY neighborhood` collapses all rows for each neighborhood into one row.
- Any column in `SELECT` that isn't being aggregated (`COUNT`, `SUM`, etc.) must
  appear in `GROUP BY` -- this trips up almost every beginner at least once.
- The `CASE WHEN ... THEN ... ELSE ... END` pattern is how you do conditional
  counting/summing in SQL. Memorize this -- you'll use it constantly.
- `100.0 * ...` rather than `100 * ...` forces floating-point division.
  `100 * 3 / 7` in integer math can silently round wrong in some databases --
  always make at least one operand a decimal when you need a percentage.

### JOIN -- combining tables

Data is rarely in one table. Suppose `customers` looks like:

| customer_id | signup_date | tier     |
|-------------|-------------|----------|
| 55          | 2025-11-02  | gold     |
| 58          | 2026-01-15  | standard |

To find the cancellation rate **by customer tier** instead of neighborhood, you
need to join:

```sql
SELECT
    c.tier,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.tier
ORDER BY cancelled_orders DESC;
```

`JOIN` (specifically `INNER JOIN`) only keeps rows where the match exists in
both tables. If you wanted to keep all orders even when customer data is
missing, you'd use `LEFT JOIN` -- common when a customer record gets deleted but
their orders are kept for accounting.

## Part 2: Python -- Once the Data Is in Your Hands

You won't always have direct SQL access (sometimes you're handed a CSV export
from a tool like Metabase or a teammate's email). `pandas` is the standard
library for this.

### Loading and inspecting data

```python
import pandas as pd

orders = pd.read_csv("breadfast_orders_may2026.csv")

print(orders.shape)        # (rows, columns)
print(orders.head())       # first 5 rows
print(orders.dtypes)       # data type of each column
print(orders["status"].value_counts())   # frequency count per category
```

`.value_counts()` is one of the most useful one-liners in pandas -- it instantly
shows you the distribution of a categorical column, which is usually the first
thing you check on any new dataset.

### Filtering -- the pandas equivalent of WHERE

```python
cancelled = orders[orders["status"] == "cancelled"]

cancelled_maadi = orders[
    (orders["status"] == "cancelled") &
    (orders["neighborhood"] == "Maadi")
]
```

Note the parentheses around each condition -- pandas requires them when combining
conditions with `&` (and) or `|` (or), because Python's operator precedence
would otherwise evaluate `&` before `==`.

### Grouping -- the pandas equivalent of GROUP BY

```python
summary = (
    orders.groupby("neighborhood")
    .agg(
        total_orders=("order_id", "count"),
        cancelled_orders=("status", lambda s: (s == "cancelled").sum())
    )
)

summary["cancellation_rate_pct"] = (
    100 * summary["cancelled_orders"] / summary["total_orders"]
).round(2)

summary = summary.sort_values("cancellation_rate_pct", ascending=False)
print(summary)
```

This is the named-aggregation pattern (`pd.NamedAgg` style via keyword
arguments) -- it's more readable than the older `.agg({"col": "func"})` dict
style, especially once you have more than two aggregations.

### Merging -- the pandas equivalent of JOIN

```python
customers = pd.read_csv("breadfast_customers.csv")

merged = orders.merge(customers, on="customer_id", how="left")
```

`how="left"` keeps every row from `orders` even if no matching customer is
found -- equivalent to SQL's `LEFT JOIN`. `how="inner"` (the default) matches
SQL's plain `JOIN`.

### A common trap: silent type mismatches

If `customer_id` is stored as an integer in `orders` but as a string in
`customers` (very common when one file came from Excel and the other from a
database export), the merge will silently produce zero matches instead of
throwing an error. Always check:

```python
print(orders["customer_id"].dtype, customers["customer_id"].dtype)
```

before merging, and cast with `.astype(int)` or `.astype(str)` if they don't
match.

## Putting It Together

In practice, the workflow at a company like **Vezeeta** (the healthcare booking
platform) or **Instabug** would be:

1. Write a SQL query to pull only the data you need -- don't `SELECT *` from a
   10-million-row table when you need 3 columns and a date filter.
2. Load the result into pandas for anything SQL is awkward at: percent-change
   calculations across time periods, pivoting, or feeding into a chart.
3. Keep the heavy lifting (filtering, joining, aggregating large volumes) in
   SQL where possible -- it's almost always faster than doing the equivalent in
   Python after pulling everything into memory.

Ready to practice? Head to Exercise 1, where you'll write SQL and pandas code
side by side against the same dataset to see how the two approaches mirror
each other.

## Key Takeaways

- SQL's `SELECT / WHERE / GROUP BY / JOIN` and pandas' filtering / `.groupby()` /
  `.merge()` solve the same problems with different syntax -- learning one
  reinforces the other.
- Use `CASE WHEN` for conditional counting in SQL; use boolean masks
  (`s == "cancelled"`) for the same purpose in pandas.
- Force floating-point math (`100.0 *` in SQL, or relying on Python's default
  float division) whenever calculating percentages or rates -- integer division
  bugs are a classic source of wrong dashboards.
- `LEFT JOIN` / `how="left"` keeps unmatched rows; plain `JOIN` / `how="inner"`
  (the default in pandas) drops them -- picking the wrong one silently changes
  your row counts.
- Always check column dtypes before merging/joining on a key -- type mismatches
  fail silently and produce zero matches instead of an error.
"""

# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------

EXERCISES = [
    {
        "title": "Filter and Count Cancelled Orders",
        "difficulty": DifficultyLevel.beginner,
        "description": (
            "You're given a pandas DataFrame `orders` with columns: "
            "order_id, customer_id, neighborhood, order_total, status, created_at. "
            "Write a function `cancelled_orders_by_neighborhood(orders)` that returns "
            "a pandas Series: index = neighborhood, value = count of cancelled orders "
            "in that neighborhood, sorted in descending order by count. "
            "If two neighborhoods have the same count, keep the order pandas "
            "produces by default (no secondary sort key required)."
        ),
        "starter_code": (
            "import pandas as pd\n\n"
            "def cancelled_orders_by_neighborhood(orders: pd.DataFrame) -> pd.Series:\n"
            "    \"\"\"Return count of cancelled orders per neighborhood, descending.\"\"\"\n"
            "    # TODO: filter to status == 'cancelled', then group and count\n"
            "    pass\n"
        ),
        "solution_code": (
            "import pandas as pd\n\n"
            "def cancelled_orders_by_neighborhood(orders: pd.DataFrame) -> pd.Series:\n"
            "    \"\"\"Return count of cancelled orders per neighborhood, descending.\"\"\"\n"
            "    cancelled = orders[orders['status'] == 'cancelled']\n"
            "    counts = cancelled.groupby('neighborhood')['order_id'].count()\n"
            "    return counts.sort_values(ascending=False)\n"
        ),
        "skill_tested": ["pandas", "filtering", "groupby", "data-analysis"],
    },
    {
        "title": "SQL: Cancellation Rate by Customer Tier",
        "difficulty": DifficultyLevel.intermediate,
        "description": (
            "Given two tables: `orders` (order_id, customer_id, status, order_total, created_at) "
            "and `customers` (customer_id, tier, signup_date), write a single SQL query that "
            "returns, for each tier: total_orders, cancelled_orders, and cancellation_rate_pct "
            "(rounded to 2 decimal places). Only include orders from May 2026 "
            "(created_at >= '2026-05-01' AND created_at < '2026-06-01'). "
            "Order results by cancellation_rate_pct descending. "
            "Write your query as a Python string assigned to the variable `query`."
        ),
        "starter_code": (
            "# Write your SQL query as a string.\n"
            "query = \"\"\"\n"
            "-- TODO\n"
            "\"\"\"\n"
        ),
        "solution_code": (
            "query = \"\"\"\n"
            "SELECT\n"
            "    c.tier,\n"
            "    COUNT(*) AS total_orders,\n"
            "    SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,\n"
            "    ROUND(\n"
            "        100.0 * SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*),\n"
            "        2\n"
            "    ) AS cancellation_rate_pct\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "WHERE o.created_at >= '2026-05-01' AND o.created_at < '2026-06-01'\n"
            "GROUP BY c.tier\n"
            "ORDER BY cancellation_rate_pct DESC;\n"
            "\"\"\"\n"
        ),
        "skill_tested": ["sql", "joins", "aggregation", "case-when"],
    },
    {
        "title": "Merge, Detect Type Mismatch, and Reconcile",
        "difficulty": DifficultyLevel.advanced,
        "description": (
            "You're given two DataFrames: `orders` (customer_id stored as int64) and "
            "`customers` (customer_id stored as string, due to an Excel export). "
            "A naive merge silently returns 0 matched rows. Write a function "
            "`safe_merge(orders, customers)` that: (1) detects the dtype mismatch on "
            "customer_id, (2) casts customers['customer_id'] to int64 to match, "
            "(3) performs a left merge on customer_id keeping all order rows, "
            "(4) returns the merged DataFrame. Raise a ValueError with a clear message "
            "if customer_id in customers cannot be cast to int (e.g. contains non-numeric "
            "strings)."
        ),
        "starter_code": (
            "import pandas as pd\n\n"
            "def safe_merge(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:\n"
            "    \"\"\"Merge orders with customers, handling customer_id dtype mismatch.\"\"\"\n"
            "    # TODO\n"
            "    pass\n"
        ),
        "solution_code": (
            "import pandas as pd\n\n"
            "def safe_merge(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:\n"
            "    \"\"\"Merge orders with customers, handling customer_id dtype mismatch.\"\"\"\n"
            "    customers = customers.copy()\n"
            "    if orders['customer_id'].dtype != customers['customer_id'].dtype:\n"
            "        try:\n"
            "            customers['customer_id'] = customers['customer_id'].astype(\n"
            "                orders['customer_id'].dtype\n"
            "            )\n"
            "        except (ValueError, TypeError) as e:\n"
            "            raise ValueError(\n"
            "                f\"Cannot cast customers['customer_id'] to match orders \"\n"
            "                f\"dtype {orders['customer_id'].dtype}: {e}\"\n"
            "            )\n"
            "    return orders.merge(customers, on='customer_id', how='left')\n"
        ),
        "skill_tested": ["pandas", "merge", "data-cleaning", "dtype-handling", "error-handling"],
    },
]

# ---------------------------------------------------------------------------
# QUIZ
# ---------------------------------------------------------------------------

QUIZ_QUESTIONS = [
    {
        "question": "In SQL, which clause is required when SELECT includes both a non-aggregated column and an aggregate function like COUNT()?",
        "options": ["ORDER BY", "GROUP BY", "HAVING", "WHERE"],
        "correct": 1,
        "explanation": "GROUP BY is required for any non-aggregated column in SELECT alongside aggregate functions; omitting it causes an error or undefined behavior in most databases."
    },
    {
        "question": "What does `orders[(orders['status'] == 'cancelled') & (orders['neighborhood'] == 'Maadi')]` return if you remove the parentheses around each condition?",
        "options": [
            "The same result, parentheses are just style",
            "A TypeError or operator precedence error, because & binds tighter than ==",
            "An empty DataFrame",
            "All rows, ignoring both conditions"
        ],
        "correct": 1,
        "explanation": "Python's & operator has higher precedence than ==, so without parentheses pandas attempts to evaluate the & before the comparisons resolve, raising an error."
    },
    {
        "question": "Why does `100 * SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END) / COUNT(*)` risk an incorrect result in some SQL databases?",
        "options": [
            "CASE WHEN can't be used inside SUM()",
            "Integer division can truncate the result before multiplying by 100",
            "COUNT(*) doesn't work with GROUP BY",
            "SUM() ignores ELSE branches"
        ],
        "correct": 1,
        "explanation": "If both SUM(...) and COUNT(*) are integers, some databases perform integer division on the SUM/COUNT before the multiplication is applied in execution order, or the division itself truncates -- using 100.0 forces floating-point arithmetic."
    },
    {
        "question": "A pandas merge between orders.customer_id (int64) and customers.customer_id (string) with how='left' produces:",
        "options": [
            "A TypeError that stops execution",
            "All orders rows with NaN in customer columns, since no keys match across the dtypes",
            "Automatic type coercion and correct matches",
            "An empty DataFrame with zero rows"
        ],
        "correct": 1,
        "explanation": "pandas merge does not raise an error on dtype mismatch between key columns -- it silently fails to match any rows, so a left merge keeps all orders rows but customer columns come back as NaN."
    },
    {
        "question": "What is the difference between SQL's JOIN (without modifier) and LEFT JOIN?",
        "options": [
            "JOIN is faster but functionally identical to LEFT JOIN",
            "JOIN (INNER JOIN) only returns rows with matches in both tables; LEFT JOIN keeps all left-table rows even without a match",
            "LEFT JOIN only works with one table",
            "There is no difference in modern SQL"
        ],
        "correct": 1,
        "explanation": "INNER JOIN (the default for plain JOIN) requires a match in both tables; LEFT JOIN preserves every row from the left table, filling unmatched right-table columns with NULL."
    },
    {
        "question": "In pandas, what does `.value_counts()` called on a column return?",
        "options": [
            "The total number of rows in the DataFrame",
            "A Series of unique values in that column mapped to their frequency, sorted descending by default",
            "The sum of all numeric values in the column",
            "A boolean mask of duplicated values"
        ],
        "correct": 1,
        "explanation": "value_counts() returns a Series indexed by each unique value, with counts as the values, sorted from most to least frequent by default."
    },
    {
        "question": "Which pandas merge `how` parameter value is equivalent to SQL's INNER JOIN?",
        "options": ["'left'", "'right'", "'outer'", "'inner'"],
        "correct": 3,
        "explanation": "how='inner' is pandas' default merge behavior and keeps only rows with matching keys in both DataFrames, equivalent to SQL's INNER JOIN."
    },
    {
        "question": "Why is `IN ('Maadi', 'Nasr City')` generally preferred over `neighborhood = 'Maadi' OR neighborhood = 'Nasr City'` in SQL?",
        "options": [
            "IN executes faster on every database engine without exception",
            "IN is more concise and readable for checking membership in a list of values, with equivalent logic",
            "OR is deprecated in modern SQL",
            "IN only works with numeric columns"
        ],
        "correct": 1,
        "explanation": "IN and chained OR conditions are logically equivalent for this use case; IN is preferred mainly for readability and conciseness, especially as the list of values grows."
    }
]

# ---------------------------------------------------------------------------
# PROJECT
# ---------------------------------------------------------------------------

PROJECT = {
    "title": "Breadfast Order Cancellation Analysis",
    "description": (
        "You're a data analyst at Breadfast. The Operations team wants to understand "
        "why order cancellations spiked last month. You've been given two CSV exports: "
        "orders.csv (order_id, customer_id, neighborhood, order_total, status, created_at) "
        "and customers.csv (customer_id, tier, signup_date). Using SQL-style queries "
        "(via pandasql or sqlite3) AND pandas, produce a written analysis answering: "
        "which neighborhoods and customer tiers have the highest cancellation rates, "
        "whether cancellation rate correlates with order_total, and whether newer "
        "customers (signed up in the last 60 days) cancel more often than established "
        "customers. Deliver your findings as a short report (markdown or notebook) with "
        "supporting tables."
    ),
    "difficulty": DifficultyLevel.beginner,
    "tech_stack": ["Python", "pandas", "SQLite", "Jupyter"],
    "objectives": [
        "Load both CSV files into pandas and verify column dtypes match before any merge",
        "Write at least one raw SQL query (via sqlite3 or pandasql) computing cancellation rate by neighborhood",
        "Reproduce the same calculation in pure pandas using groupby and compare results match",
        "Calculate cancellation rate broken down by customer tier",
        "Determine whether average order_total differs meaningfully between cancelled and delivered orders",
        "Flag customers who signed up within 60 days of their order date and compare their cancellation rate to established customers",
        "Summarize findings in a short written report with at least 3 supporting tables or charts",
        "Clearly state any data quality issues found (e.g. missing values, dtype mismatches) and how you handled them"
    ],
    "rubric": {
        "Correct SQL query producing accurate cancellation rate by neighborhood": 15,
        "Correct pandas equivalent calculation matching SQL results": 15,
        "Correct cancellation rate breakdown by customer tier": 15,
        "Sound analysis of order_total vs cancellation status": 15,
        "Correct identification and analysis of new vs established customer cancellation rates": 15,
        "Data quality issues identified and handled appropriately": 10,
        "Clarity and completeness of written report with supporting tables/charts": 15
    },
    "starter_repo_url": None,
    "estimated_hours": 6.0,
}

# ---------------------------------------------------------------------------
# SEED LOGIC
# ---------------------------------------------------------------------------

def seed_topic(db, track_slug: str, level_order: int, topic_order: int = 1):
    track = db.query(CareerTrack).filter(CareerTrack.slug == track_slug).first()
    if not track:
        raise RuntimeError(f"CareerTrack with slug='{track_slug}' not found -- expected it to be pre-seeded.")

    level = db.query(TrackLevel).filter(
        TrackLevel.track_id == track.id, TrackLevel.order == level_order
    ).first()
    if not level:
        raise RuntimeError(
            f"TrackLevel order={level_order} for track='{track_slug}' not found -- "
            f"expected it to be pre-seeded as an empty shell."
        )

    topic = db.query(Topic).filter(
        Topic.level_id == level.id, Topic.order == topic_order
    ).first()
    if not topic:
        raise RuntimeError(
            f"Topic order={topic_order} for level_id={level.id} not found -- "
            f"expected it to be pre-seeded as an empty shell."
        )

    print(f"Seeding content into: track='{track.slug}' level='{level.title}' (order={level.order}) "
          f"topic='{topic.title}' (id={topic.id}, order={topic.order})")

    # --- Lesson ---
    if not db.query(Lesson).filter(Lesson.topic_id == topic.id).first():
        db.add(Lesson(
            topic_id=topic.id,
            title="Python & SQL Foundations for Data Analysis",
            content=LESSON_CONTENT,
            order=1,
            estimated_minutes=50,
            has_code_examples=True,
        ))
        print("  + Lesson added")
    else:
        print("  - Lesson already exists, skipping")

    # --- Exercises ---
    if db.query(Exercise).filter(Exercise.topic_id == topic.id).count() == 0:
        for ex in EXERCISES:
            db.add(Exercise(topic_id=topic.id, **ex))
        print(f"  + {len(EXERCISES)} exercises added")
    else:
        print("  - Exercises already exist, skipping")

    # --- Quiz ---
    if not db.query(Quiz).filter(Quiz.topic_id == topic.id).first():
        db.add(Quiz(
            topic_id=topic.id,
            title="Python & SQL Foundations Quiz",
            questions=QUIZ_QUESTIONS,
            passing_score=70,
        ))
        print("  + Quiz added")
    else:
        print("  - Quiz already exists, skipping")

    # --- Project ---
    if not db.query(Project).filter(Project.topic_id == topic.id).first():
        db.add(Project(topic_id=topic.id, **PROJECT))
        print("  + Project added")
    else:
        print("  - Project already exists, skipping")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_topic(db, track_slug="data-analyst", level_order=1, topic_order=1)
    finally:
        db.close()