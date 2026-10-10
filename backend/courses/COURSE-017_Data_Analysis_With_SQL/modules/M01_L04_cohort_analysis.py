"""M01.L04 — Cohort Analysis.

One source chapter -> one complete learner-facing lesson + essential inline Images +
inline Exercises + lesson Quiz.
Source alignment: Chapter 4, "Cohort Analysis".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from data preparation and time-based "
    "reasoning through cohort analysis, retention, repeat behavior, lifetime "
    "value thinking, and population-mix analysis."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Cohort Analysis",

    "slug": "data-analysis-sql-m01-l04",

    "description": (
        "A practical introduction to cohort analysis with SQL: define cohorts, "
        "normalize time from a starting event, calculate retention accurately, "
        "handle sparse cohorts, and extend the same framework to survivorship, "
        "returnship, cumulative behavior, lifetime value, and cross-sectional analysis."
    ),

    "order": 4,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "sql",
        "cohort-analysis",
        "retention",
        "survivorship",
        "repeat-purchase",
        "lifetime-value",
        "window-functions",
        "date-dimensions",
        "product-analytics",
        "business-analysis",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
    ],

    # =======================================================================
    # ESSENTIAL IMAGE POLICY
    # =======================================================================
    #
    # Only figures that materially improve understanding are requested.
    # This lesson intentionally does NOT reproduce every figure from the source.
    #
    # Essential figures requested:
    # - IMG-M01-L04-01: cohort-analysis mental model
    # - IMG-M01-L04-02: corrected retention curve (Source Figure 4-4)
    # - IMG-M01-L04-03: retention vs survivorship vs returnship vs cumulative
    # - IMG-M01-L04-04: survivorship-bias illustration
    # - IMG-M01-L04-05: cohort-mix shift over calendar time (Source Figure 4-13)
    #

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Cohort Analysis",

        "content": """# Cohort Analysis

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L04  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapter 4, *Cohort Analysis*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what a cohort is and distinguish a cohort from a segment.
- Identify the three core ingredients of a cohort analysis: cohort definition, time series, and aggregate metric.
- Normalize calendar dates into elapsed periods so cohorts with different starting dates can be compared fairly.
- Build a basic retention analysis in SQL.
- Explain why event-only data can produce a misleading retention curve.
- Use start/end dates, a date dimension, or generated dates to represent continuous presence correctly.
- Define cohorts from the first event, from an attribute in the time series, or from a separate table.
- Prevent changing attributes from placing the same entity into multiple cohorts.
- Recognize sparse-cohort problems and create complete cohort-period grids.
- Define cohorts from dates other than the entity's first date.
- Distinguish retention, survivorship, returnship, and cumulative cohort analysis.
- Use fixed time boxes to make repeat-behavior and cumulative comparisons fair.
- Explain how cumulative cohort analysis relates to customer lifetime value.
- Recognize mix shifts and survivorship bias when examining current populations.
- Use cohort analysis as evidence for hypotheses without confusing correlation with causation.

---

## 1. The cohort mental model

A **cohort** is a group of entities that share a meaningful characteristic at the point where you start observing them.

The entities are often people:

- customers who signed up in the same month;
- students who started university in the same year;
- employees hired in the same quarter;
- patients who began a treatment in the same period.

But a cohort can also contain companies, products, devices, stores, or other entities.

The key idea is:

> **Group entities at a starting point, then follow their behavior over elapsed time.**

Suppose an app has three signup cohorts:

```text
January cohort
February cohort
March cohort
```

Comparing their activity in calendar March would be unfair:

- January users have had roughly two months to behave.
- February users have had roughly one month.
- March users may have had only days.

Instead, cohort analysis creates a normalized clock:

```text
Period 0 = starting period
Period 1 = one period after start
Period 2 = two periods after start
...
```

Now January period 2 can be compared with February period 2 and March period 2 once each cohort has had enough time to reach that point.

### The three parts of every cohort analysis

A useful cohort analysis needs:

1. **A cohort definition**  
   Who belongs together?

2. **A time series**  
   What actions or states are observed after the starting point?

3. **A metric**  
   What behavior are you measuring?

Example:

```text
Cohort:
Customers grouped by signup month

Time series:
Monthly purchases

Metric:
Percentage of customers who purchase again
```

[[IMAGE_NEEDED: IMG-M01-L04-01 / Instructor Figure — Anatomy of cohort analysis | Show three signup cohorts beginning in different calendar months, then align them onto a common Period 0, Period 1, Period 2 timeline, with an example retention metric below | Learner should notice that cohort analysis compares behavior by elapsed time from a common starting point rather than by raw calendar date]]

### Cohort versus segment

These ideas are related but not identical.

A **segment** groups entities by a characteristic at a point in time:

```text
enterprise customers
mobile users
customers in Egypt
high-value customers
```

A **cohort** usually adds a starting point and follows the entities across time:

```text
customers acquired in January 2026
users who activated during launch week
students who enrolled in 2025
```

A segment can become the basis of a cohort analysis. For example:

```text
Cohort = customers acquired in January
Segment inside cohort = organic vs paid acquisition
```

The important question is not the label you use. The important question is whether every entity is assigned consistently and whether the time comparison is fair.

---

## 2. Four major cohort-analysis questions

The chapter develops four related forms of cohort analysis.

### Retention

**Question:** Is the entity present in a specific period after starting?

Example:

```text
What percentage of January signups were active in month 3?
```

### Survivorship

**Question:** Did the entity remain until at least a threshold?

Example:

```text
What percentage of subscribers stayed for 12 months or longer?
```

### Returnship

Also called repeat behavior.

**Question:** Did the entity return or repeat an action within a fixed time window?

Example:

```text
What percentage of first-time buyers made a second purchase within 90 days?
```

### Cumulative behavior

**Question:** How much total value or activity has accumulated within a fixed time window?

Example:

```text
How much revenue did each acquisition cohort generate during its first 12 months?
```

These four questions are similar, but they are not interchangeable.

```text
Retention   -> present at period N?
Survivorship -> lasted until period N or beyond?
Returnship  -> repeated by period N?
Cumulative  -> how much accumulated by period N?
```

[[IMAGE_NEEDED: IMG-M01-L04-03 / Instructor Figure — Four cohort-analysis questions | Show one horizontal customer timeline with events and four callouts: retention asks whether an event/state exists at Period N; survivorship asks whether the entity reaches N or later; returnship asks whether another action occurs before a deadline; cumulative asks for total activity/value accumulated by the deadline | Learner should notice that all four analyses use the same entity timeline but answer different business questions]]

This distinction is extremely useful in product analytics.

A user might:

- fail retention in month 3 because they did not use the product that month;
- still count as a survivor if they return in month 4;
- count as a repeat customer if they purchased twice during the first 90 days;
- generate high cumulative revenue despite irregular activity.

Choose the metric that matches the real business question.

---

## 3. Building a basic retention analysis

Retention is the best place to learn the mechanics because the same building blocks appear in the other cohort analyses.

Assume a table:

```text
customer_events

customer_id
event_date
event_type
```

We first need the starting date for each customer.

```sql
SELECT
    customer_id,
    MIN(event_date) AS first_date
FROM customer_events
GROUP BY customer_id;
```

Then join each customer back to their later events and calculate elapsed periods.

For a monthly analysis in PostgreSQL:

```sql
WITH starts AS (
    SELECT
        customer_id,
        MIN(event_date) AS first_date
    FROM customer_events
    GROUP BY customer_id
)
SELECT
    DATE_PART(
        'month',
        AGE(DATE_TRUNC('month', e.event_date),
            DATE_TRUNC('month', s.first_date))
    ) AS period,
    COUNT(DISTINCT s.customer_id) AS retained
FROM starts s
JOIN customer_events e
    ON s.customer_id = e.customer_id
GROUP BY 1
ORDER BY 1;
```

The exact date-difference syntax varies by database, but the logic is stable:

```text
period = current activity date - cohort start date
```

Next, we need the cohort's starting size.

A convenient method is `first_value`:

```sql
WITH retention AS (
    -- one row per period with retained count
    SELECT
        period,
        COUNT(DISTINCT customer_id) AS retained
    FROM ...
    GROUP BY period
)
SELECT
    period,
    FIRST_VALUE(retained) OVER (ORDER BY period) AS cohort_size,
    retained,
    retained * 1.0
        / FIRST_VALUE(retained) OVER (ORDER BY period) AS retention_rate
FROM retention;
```

The expected shape is:

```text
period   cohort_size   retained   retention_rate
0        1000          1000       1.00
1        1000           620       0.62
2        1000           510       0.51
3        1000           470       0.47
```

### Reading a retention curve

The beginning of the curve often tells the most important story.

A sharp early drop can indicate:

- weak onboarding;
- low-quality acquisition;
- users not reaching the product's value quickly;
- a mismatch between marketing promises and real experience.

A curve that later flattens suggests a stable core population remains.

A curve that continues declining toward zero suggests that even long-term users keep disappearing.

For money-based retention, the curve can sometimes exceed 100% because the remaining customers may spend more over time. Count-based customer retention normally cannot exceed 100% if membership is fixed correctly.

{{exercise:M01.L04.EX01}}

---

## 4. Event records are not the same as continuous presence

This is one of the most important lessons in cohort analysis.

Suppose you analyze subscriptions.

The database stores:

```text
subscription_start = 2026-01-01
subscription_end   = 2026-12-31
```

If you count only rows where a subscription starts, the customer appears in January but seems to disappear in February through December.

That conclusion is false.

The row represents a state that persists across an interval.

The same issue appears with:

- employment contracts;
- memberships;
- insurance policies;
- school enrollment;
- elected terms;
- product licenses.

### The correct question

Do not ask:

```text
Did a new record occur in this period?
```

Ask:

```text
Was the entity active during this period?
```

If both start and end dates exist, generate or join to the dates inside that range.

A date dimension is especially useful:

```sql
SELECT
    s.customer_id,
    d.month_start
FROM subscriptions s
JOIN date_dim d
    ON d.month_start BETWEEN DATE_TRUNC('month', s.start_date)
                         AND DATE_TRUNC('month', s.end_date);
```

Now an annual subscription has one active row for each month it actually covers.

The same idea is used in the source chapter to make the legislators' retention curve truthful by filling the years between a term's start and end dates rather than counting only new term-start records.

{{image:legislator-retention-corrected}}

### When an end date does not exist

There are several possibilities.

#### 1. Known fixed duration

If every plan lasts one year:

```sql
start_date + INTERVAL '1 year'
```

can provide an estimated end date.

#### 2. Next event implies the current interval ended

You can use `lead`:

```sql
LEAD(start_date) OVER (
    PARTITION BY customer_id
    ORDER BY start_date
) - INTERVAL '1 day'
```

#### 3. No reliable duration information

Do not silently invent one.

The result may require:

- a different metric;
- a documented assumption;
- or a request for better source data.

### Practical rule

Whenever a row represents **state**, ask how long that state remains true.

Whenever a row represents **an event**, ask only when the event happened.

Confusing states with events is a common cause of wrong cohort metrics.

---

## 5. Defining cohorts correctly

A cohort is only as useful as its definition.

### Cohort from first date

The most common approach:

```sql
SELECT
    customer_id,
    MIN(order_date) AS first_order_date
FROM orders
GROUP BY customer_id;
```

Then derive:

```text
signup month
first purchase quarter
first active year
```

with date functions.

### Cohort from the first value of a changing attribute

Suppose a user can change plan:

```text
Free -> Pro -> Enterprise
```

If you want the **acquisition plan**, do not simply group by every plan value observed across the user's life.

Use the value associated with the starting record.

```sql
FIRST_VALUE(plan) OVER (
    PARTITION BY customer_id
    ORDER BY event_date
)
```

The same logic applies to:

- first marketing channel;
- first region;
- first device;
- first product category;
- first sales representative.

### Cohort from a separate table

Sometimes the time-series table stores actions while a customer table stores cohort attributes.

```text
customers
---------
customer_id
signup_date
acquisition_channel
country

orders
------
customer_id
order_date
amount
```

You can define the cohort from `customers` and observe behavior in `orders`.

```sql
SELECT
    c.acquisition_channel,
    ...
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id;
```

### The changing-attribute trap

Imagine this user:

```text
Jan: Free
Feb: Pro
Mar: Pro
```

If you group every row by plan, the same user can appear in both the Free and Pro cohorts.

That breaks the interpretation of the cohort.

If the question is:

```text
Does the plan at acquisition affect long-term retention?
```

freeze the starting plan.

If the question is instead:

```text
How does retention change after upgrading to Pro?
```

then the **upgrade date becomes a new cohort starting point**.

### Avoid cohorts that are too small

Adding more grouping variables gives more detail:

```text
signup month
+ country
+ acquisition channel
+ device
+ plan
```

but cohort sizes can quickly collapse.

A cohort of 4 users may move from 100% retention to 75% because one person disappears.

That is mathematically correct but may not be analytically useful.

Always show or inspect cohort size alongside the rate.

---

## 6. Sparse cohorts and missing periods

A cohort result can disappear entirely from a period when no members had a record.

This is different from a retention value of zero.

Consider:

```text
cohort     period     retained
A          0          100
A          1           70
A          3           40
```

Where is period 2?

Two possibilities exist:

```text
1. retention in period 2 was 0
2. period 2 was not generated at all
```

Those are analytically different.

### Build the complete cohort-period grid

A reliable pattern is:

1. Create all cohort groups.
2. Create all periods you want to report.
3. Cartesian join them.
4. Left join the actual results.
5. Replace missing counts with zero when zero is the correct meaning.

For PostgreSQL:

```sql
WITH periods AS (
    SELECT generate_series(0, 12, 1) AS period
),
cohorts AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
),
grid AS (
    SELECT
        c.cohort_month,
        c.cohort_size,
        p.period
    FROM cohorts c
    CROSS JOIN periods p
)
SELECT
    g.cohort_month,
    g.period,
    g.cohort_size,
    COALESCE(r.retained, 0) AS retained,
    COALESCE(r.retained, 0) * 1.0 / g.cohort_size AS retention_rate
FROM grid g
LEFT JOIN retention_counts r
    ON g.cohort_month = r.cohort_month
   AND g.period = r.period;
```

### Do not blindly turn every null into zero

A recent cohort may not yet have had enough time to reach month 12.

That is not zero retention.

It is **not yet observable**.

This distinction matters:

```text
0% retention
```

means:

> the cohort had the opportunity to reach the period, but nobody remained.

```text
not observable
```

means:

> the cohort has not existed long enough to measure the period fairly.

This is one of the most important rules for cohort dashboards.

{{exercise:M01.L04.EX02}}

---

## 7. Cohorts do not always need to start at the first-ever event

The default cohort starting point is often:

```text
first signup
first purchase
first subscription
```

But sometimes the business question starts later.

Examples:

- users active when a redesign launched;
- customers at the moment they upgrade;
- accounts after reaching 10 purchases;
- users who crossed a usage threshold;
- employees who entered management;
- subscribers active during a particular calendar month.

In these cases, define a **midstream cohort**.

Example:

```text
Cohort:
all customers active during January 2026

Period 0:
January 2026

Question:
what percentage remains active after 1, 3, 6, and 12 months?
```

### Define inclusion precisely

Suppose a customer is considered active in January if any subscription interval overlaps January.

The correct condition resembles:

```sql
WHERE subscription_start <= DATE '2026-01-31'
  AND subscription_end   >= DATE '2026-01-01'
```

This includes users whose subscription began before January but remained active during the month.

### Why this matters

Changing the cohort starting point changes the interpretation.

```text
Signup cohort -> measures behavior after acquisition
Upgrade cohort -> measures behavior after upgrade
Active-on-date cohort -> measures future behavior of an existing base
```

All are valid, but they answer different questions.

---

## 8. Survivorship: how long do entities last?

Retention asks:

```text
Was the entity present in period 6?
```

Survivorship asks:

```text
Did the entity make it to period 6 or beyond?
```

That difference is subtle but important.

Suppose a customer purchases in:

```text
Month 0
Month 1
Month 4
Month 8
```

At month 6:

- month-6 retention may say **no**, because there was no purchase in month 6;
- six-month survivorship may say **yes**, because the customer later returned in month 8.

### Basic survivorship calculation

Start with each entity's first and last observed dates:

```sql
SELECT
    customer_id,
    MIN(event_date) AS first_date,
    MAX(event_date) AS last_date
FROM customer_events
GROUP BY customer_id;
```

Then calculate duration:

```sql
SELECT
    customer_id,
    DATE_PART(
        'month',
        AGE(last_date, first_date)
    ) AS tenure_months
FROM customer_lifetimes;
```

Now calculate the share reaching a threshold:

```sql
SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) AS cohort_size,
    COUNT(DISTINCT CASE
        WHEN tenure_months >= 12 THEN customer_id
    END) AS survived_12,
    COUNT(DISTINCT CASE
        WHEN tenure_months >= 12 THEN customer_id
    END) * 1.0
        / COUNT(DISTINCT customer_id) AS pct_survived_12
FROM customer_lifetimes
GROUP BY cohort_month;
```

You can repeat this across many thresholds:

```text
1 month
3 months
6 months
12 months
24 months
```

to create a survival-style curve.

### What survivorship is good for

- subscription longevity;
- employee tenure;
- product lifespan;
- patient survival or treatment duration;
- account lifetime;
- long-term participation.

Be careful with recent cohorts: if a cohort started six months ago, you cannot yet make a fair 12-month survivorship comparison.

---

## 9. Returnship: did the entity repeat the behavior?

Returnship focuses on repeat action.

For ecommerce:

```text
Did a first-time buyer make another purchase?
```

For education:

```text
Did a student enroll in a second course?
```

For SaaS:

```text
Did a new account perform the key workflow again?
```

The most important concept is the **time box**.

### Why a time box is necessary

Suppose:

```text
Cohort A started 2 years ago.
Cohort B started 2 months ago.
```

If you simply ask:

```text
How many users ever purchased again?
```

Cohort A had much more time to succeed.

That comparison is biased.

Instead ask:

```text
What percentage purchased again within 90 days?
```

Now every eligible cohort receives the same observation window.

Example:

```sql
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order
    FROM orders
    GROUP BY customer_id
)
SELECT
    DATE_TRUNC('month', f.first_order) AS cohort_month,
    COUNT(DISTINCT f.customer_id) AS cohort_size,
    COUNT(DISTINCT CASE
        WHEN o.order_date > f.first_order
         AND o.order_date <= f.first_order + INTERVAL '90 days'
        THEN f.customer_id
    END) AS repeat_buyers
FROM first_purchase f
LEFT JOIN orders o
    ON f.customer_id = o.customer_id
GROUP BY 1;
```

Then:

```text
repeat_rate = repeat_buyers / cohort_size
```

### Compare several windows

You can calculate:

```text
repeat within 30 days
repeat within 90 days
repeat within 180 days
```

in the same query using conditional counts.

This shows not only whether cohorts return, but **how quickly** they return.

---

## 10. Cumulative cohort behavior and lifetime value

Cumulative analysis asks:

```text
How much total activity or value has accumulated by a deadline?
```

Common metrics include:

- revenue per customer;
- gross margin per customer;
- orders per customer;
- support tickets per account;
- sessions per user;
- total claims per patient;
- total usage per device.

### Use equal observation windows

Again, compare cohorts fairly.

If one cohort has existed for three years and another for six months, comparing lifetime revenue directly makes the older cohort look better simply because it had more time.

Instead compare:

```text
revenue in first 30 days
revenue in first 90 days
revenue in first 12 months
```

Example:

```sql
WITH cohorts AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order
    FROM orders
    GROUP BY customer_id
)
SELECT
    DATE_TRUNC('month', c.first_order) AS cohort_month,
    COUNT(DISTINCT c.customer_id) AS cohort_size,
    SUM(o.amount) AS revenue_12m,
    SUM(o.amount)
        / COUNT(DISTINCT c.customer_id) AS revenue_per_customer_12m
FROM cohorts c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
   AND o.order_date >= c.first_order
   AND o.order_date < c.first_order + INTERVAL '12 months'
GROUP BY 1;
```

### Connection to LTV

**Customer lifetime value (LTV/CLTV)** asks how much economic value a customer creates across their relationship with the organization.

Cohort analysis helps because early cumulative behavior can be compared across cohorts:

```text
Month 1 revenue per customer
Month 3 revenue per customer
Month 6 revenue per customer
Month 12 revenue per customer
```

If early cumulative behavior is strongly related to later behavior, newer cohorts can provide an early indication of future LTV.

Do not confuse:

```text
total cohort revenue
```

with:

```text
revenue per customer
```

A huge cohort can produce more total revenue while having worse customer-level economics.

Always decide whether the question is about:

- total organizational contribution; or
- average value per entity.

{{exercise:M01.L04.EX03}}

---

## 11. Cross-sectional analysis, mix shifts, and survivorship bias

Cohort analysis follows groups through time.

**Cross-sectional analysis** examines a population at a particular moment.

Example:

```text
Who are our customers today?
```

You might calculate:

```text
40% organic acquisition
35% paid search
25% referrals
```

That can be useful, but it can hide how the population arrived at that composition.

### Mix shift

A **mix shift** occurs when the composition of the population changes.

Examples:

- the company expands into new countries;
- paid acquisition replaces organic acquisition;
- enterprise customers become a larger share of revenue;
- a product moves from early adopters to mainstream users.

An overall retention metric may change even if the retention of every individual cohort remains stable.

Why?

Because the **weights of the cohorts changed**.

Example:

```text
Cohort A retention = 80%
Cohort B retention = 40%
```

If your population shifts from mostly A to mostly B, overall retention will fall even if neither cohort's behavior changed.

### Survivorship bias

Survivorship bias happens when analysis focuses on the entities still visible and ignores those that disappeared.

Imagine asking:

```text
What do our best current customers have in common?
```

You discover:

```text
many are mobile users
many live in large cities
many use Feature X
```

That does not prove those traits create successful customers.

Perhaps thousands of churned customers had the same traits.

The missing entities matter.

[[IMAGE_NEEDED: IMG-M01-L04-04 / Instructor Figure — Survivorship bias in customer analysis | Show an original customer cohort entering a funnel, with many churned customers disappearing from the visible population and only survivors remaining at the end; contrast 'analyze survivors only' with 'compare survivors and non-survivors from the original cohort' | Learner should notice that characteristics common among survivors are not necessarily causes of survival]]

### Use a cohort lens on cross sections

A powerful approach is to ask:

```text
At each calendar date, what share of the current population came from each original cohort?
```

This creates a time series of cross-sectional composition.

{{image:cohort-composition-by-century}}

This idea generalizes directly to business:

```text
share of active customers by acquisition year
share of revenue by signup cohort
share of users by tenure band
share of accounts by first plan
```

Cohort behavior and population composition should often be examined together.

---

## 12. A practical workflow for cohort analysis

When you receive a cohort-analysis task, use this sequence.

### Step 1 — Define the entity

What exactly are you tracking?

```text
customer
account
subscription
student
device
company
```

Do not mix grains.

### Step 2 — Define the starting event

Examples:

```text
signup
first purchase
activation
upgrade
first treatment
start of employment
```

### Step 3 — Define the cohort attribute

Examples:

```text
signup month
acquisition channel
country
first plan
first product
```

Freeze changing attributes at the correct starting point.

### Step 4 — Define the behavior

What counts as success?

```text
active
purchased
renewed
logged in
completed course
generated revenue
```

### Step 5 — Define time granularity

Choose:

```text
days
weeks
months
quarters
years
```

based on how often behavior naturally occurs.

### Step 6 — Normalize to elapsed period

Create:

```text
Period 0
Period 1
Period 2
...
```

Do not compare cohorts only by raw calendar dates.

### Step 7 — Make opportunity windows fair

For 12-month retention, returnship, or cumulative value:

```text
include only cohorts old enough to have 12 months of observation
```

or clearly mark later periods as not observable.

### Step 8 — Build complete cohort-period combinations

Prevent missing rows from being confused with zeros.

### Step 9 — Keep cohort sizes visible

A rate without its denominator can be misleading.

### Step 10 — Interpret, do not overclaim

Cohort analysis is observational.

It can reveal:

- patterns;
- correlations;
- hypotheses;
- possible changes in customer quality.

It does not by itself prove causality.

Randomized experiments are the stronger tool when the goal is causal inference.

---

## Important misconceptions

### Misconception 1

> A missing cohort-period row means retention is zero.

Not necessarily. The period may not have been generated, or the cohort may not yet have had enough time to reach it.

### Misconception 2

> If a user has no event in month 2, they were not present in month 2.

Not necessarily. A state such as a subscription or employment can remain active between events.

### Misconception 3

> The latest cohort has the worst 12-month retention because its later cells are empty.

The cohort may simply be too young to observe those periods.

### Misconception 4

> If a characteristic is common among today's best customers, it must explain why they became good customers.

This is vulnerable to survivorship bias and confounding.

### Misconception 5

> More cohort dimensions always make the analysis better.

Over-segmentation creates tiny, noisy cohorts and can make the output harder to trust.

---

## Key terminology

| Term | Meaning |
|---|---|
| Cohort | Group of entities sharing a starting characteristic and followed over time |
| Segment | Group sharing a characteristic, not necessarily aligned to a common starting time |
| Period 0 | The starting observation period for a cohort |
| Retention | Share or amount present in a specific elapsed period |
| Retention curve | Retention values plotted across elapsed periods |
| Survivorship | Share reaching a specified duration or later |
| Returnship | Share repeating an action within a fixed time window |
| Cumulative behavior | Total activity or value accumulated by a deadline |
| Time box | Fixed observation window used for fair cohort comparison |
| Cohort size | Number or starting amount in a cohort |
| Sparse cohort | Cohort whose data is missing for some periods because of small size or sparse activity |
| Date dimension | Complete calendar table used to generate or align time periods |
| Mix shift | Change in the composition of a population over time |
| Survivorship bias | Bias caused by focusing only on entities that remain visible |
| LTV / CLTV | Customer lifetime value |
| Cross-sectional analysis | Analysis of a population at a particular point in time |

---

## Self-check

Before continuing, make sure you can answer:

1. What makes a cohort different from a normal segment?
2. Why do we compare cohorts by elapsed period rather than only by calendar date?
3. What are the three components required for a cohort analysis?
4. Why can event-only data underestimate retention for subscriptions?
5. When should `first_value` be used to freeze a cohort attribute?
6. What is the difference between zero retention and a period that is not yet observable?
7. How does survivorship differ from retention?
8. Why does returnship require a fixed time box?
9. Why should cumulative cohort metrics often be divided by cohort size?
10. What is a mix shift?
11. How can survivorship bias distort an analysis of current customers?
12. Why should cohort analysis not automatically be interpreted causally?

---

## Retain this idea

**Cohort analysis becomes powerful when you align entities to a meaningful starting point, give every cohort a fair observation window, and distinguish absence, missing data, and not-yet-observable periods. Once that foundation is correct, the same SQL framework can answer retention, survivorship, repeat-behavior, lifetime-value, and population-mix questions.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "cohort-mental-model",
                "title": "The cohort mental model",
                "order": 1,
            },
            {
                "id": "four-cohort-analyses",
                "title": "Four major cohort-analysis questions",
                "order": 2,
            },
            {
                "id": "basic-retention",
                "title": "Building a basic retention analysis",
                "order": 3,
            },
            {
                "id": "continuous-presence",
                "title": "Event records are not the same as continuous presence",
                "order": 4,
            },
            {
                "id": "cohort-definition",
                "title": "Defining cohorts correctly",
                "order": 5,
            },
            {
                "id": "sparse-cohorts",
                "title": "Sparse cohorts and missing periods",
                "order": 6,
            },
            {
                "id": "midstream-cohorts",
                "title": "Cohorts do not always need to start at the first-ever event",
                "order": 7,
            },
            {
                "id": "survivorship",
                "title": "Survivorship: how long do entities last?",
                "order": 8,
            },
            {
                "id": "returnship",
                "title": "Returnship: did the entity repeat the behavior?",
                "order": 9,
            },
            {
                "id": "cumulative",
                "title": "Cumulative cohort behavior and lifetime value",
                "order": 10,
            },
            {
                "id": "cross-sectional",
                "title": "Cross-sectional analysis, mix shifts, and survivorship bias",
                "order": 11,
            },
            {
                "id": "practical-workflow",
                "title": "A practical workflow for cohort analysis",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",

            "title": "Build a Monthly Retention Table",

            "lesson_code": "M01.L04",

            "section_id": "basic-retention",

            "placement": "after_section",

            "description": (
                "Create the core retention calculation for a SaaS product using "
                "signup and activity data."
            ),

            "instructions": (
                "You have a `users` table with `user_id` and `signup_date`, and an "
                "`activity` table with `user_id` and `activity_date`.\n"
                "1. Create a `cohort_month` from each user's signup date.\n"
                "2. Join the activity table and calculate the elapsed month number.\n"
                "3. Count distinct active users for each cohort and elapsed month.\n"
                "4. Calculate the starting cohort size.\n"
                "5. Calculate the retention rate.\n"
                "6. Explain why period 0 should normally equal 100%."
            ),

            "expected_output": (
                "SQL or pseudocode producing cohort_month, period, cohort_size, "
                "retained_users, and retention_rate, plus a short interpretation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cohort-definition",
                "date-arithmetic",
                "retention",
                "window-functions",
            ],
        },

        {
            "id": "M01.L04.EX02",

            "title": "Diagnose a Sparse Cohort",

            "lesson_code": "M01.L04",

            "section_id": "sparse-cohorts",

            "placement": "after_section",

            "description": (
                "Distinguish true zero retention from missing or not-yet-observable periods."
            ),

            "instructions": (
                "A dashboard contains these rows for the April cohort:\n"
                "`period 0 = 80`, `period 1 = 52`, `period 3 = 31`.\n"
                "1. List at least three explanations for the missing period 2.\n"
                "2. Explain why replacing it with zero immediately can be wrong.\n"
                "3. Describe how to build a complete period grid.\n"
                "4. Explain how you would identify periods that are not yet observable "
                "for recent cohorts."
            ),

            "expected_output": (
                "A short diagnostic analysis and a SQL strategy using a generated "
                "period table or date dimension plus a LEFT JOIN."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sparse-cohorts",
                "data-quality",
                "left-joins",
                "analytical-reasoning",
            ],
        },

        {
            "id": "M01.L04.EX03",

            "title": "Compare Repeat Rate and 12-Month Value",

            "lesson_code": "M01.L04",

            "section_id": "cumulative",

            "placement": "after_section",

            "description": (
                "Use the same customer cohort to calculate both returnship and "
                "cumulative economic value."
            ),

            "instructions": (
                "Assume an `orders` table with `customer_id`, `order_date`, and `amount`.\n"
                "1. Find each customer's first order date.\n"
                "2. Group customers by first-order month.\n"
                "3. Calculate the percentage making another purchase within 90 days.\n"
                "4. Calculate revenue per customer during the first 12 months.\n"
                "5. Explain why cohorts that have not existed for 12 months should not "
                "be compared on the 12-month metric yet.\n"
                "6. Explain what different conclusions the repeat-rate and cumulative-value "
                "metrics could produce."
            ),

            "expected_output": (
                "SQL or clear pseudocode for 90-day repeat rate and 12-month revenue "
                "per customer, followed by a business interpretation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "returnship",
                "time-boxes",
                "cumulative-analysis",
                "lifetime-value",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Cohort Analysis — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",

                "section_id": "cohort-mental-model",

                "question": (
                    "Why are cohorts usually compared using elapsed periods such as "
                    "Period 0, Period 1, and Period 2?"
                ),

                "options": [
                    "Because SQL cannot compare calendar dates",
                    "Because elapsed periods give cohorts with different start dates a common comparison clock",
                    "Because every cohort must start in January",
                    "Because segments cannot contain dates",
                ],

                "correct": 1,

                "explanation": (
                    "Elapsed periods normalize time from each cohort's own starting point, "
                    "making comparisons between cohorts fair."
                ),
            },

            {
                "id": "M01.L04.Q02",

                "section_id": "four-cohort-analyses",

                "question": (
                    "Which analysis asks whether an entity repeated an action within "
                    "a fixed time window?"
                ),

                "options": [
                    "Retention",
                    "Survivorship",
                    "Returnship",
                    "Cross-sectional analysis",
                ],

                "correct": 2,

                "explanation": (
                    "Returnship or repeat-behavior analysis checks whether an entity "
                    "performed a subsequent action within a defined window."
                ),
            },

            {
                "id": "M01.L04.Q03",

                "section_id": "continuous-presence",

                "question": (
                    "Why can counting only subscription-start events create an "
                    "incorrect monthly retention curve?"
                ),

                "options": [
                    "Subscriptions cannot be analyzed with SQL",
                    "The start event does not represent the months in which the subscription remains active",
                    "Monthly retention must always use revenue",
                    "A subscription can never have an end date",
                ],

                "correct": 1,

                "explanation": (
                    "A subscription is a state that can persist between its start and "
                    "end dates, so intermediate active periods must be represented."
                ),
            },

            {
                "id": "M01.L04.Q04",

                "section_id": "cohort-definition",

                "question": (
                    "You want cohorts based on each customer's acquisition plan, but "
                    "customers can upgrade later. Which value should normally define the cohort?"
                ),

                "options": [
                    "The most recent plan",
                    "Every plan the customer has ever used",
                    "The plan associated with the acquisition/start event",
                    "A random plan",
                ],

                "correct": 2,

                "explanation": (
                    "The cohort attribute should be frozen at the relevant starting point "
                    "when the question concerns acquisition conditions."
                ),
            },

            {
                "id": "M01.L04.Q05",

                "section_id": "sparse-cohorts",

                "question": (
                    "A recent cohort has no row for month 12 because only six months have "
                    "elapsed. How should month 12 usually be interpreted?"
                ),

                "options": [
                    "0% retention",
                    "100% retention",
                    "Not yet observable",
                    "A duplicate",
                ],

                "correct": 2,

                "explanation": (
                    "The cohort has not had enough opportunity to reach month 12, so zero "
                    "would incorrectly imply observed failure."
                ),
            },

            {
                "id": "M01.L04.Q06",

                "section_id": "survivorship",

                "question": (
                    "What is the main conceptual difference between retention and survivorship?"
                ),

                "options": [
                    "Retention uses SQL and survivorship does not",
                    "Retention asks about presence in a specific period, while survivorship asks whether an entity lasted to that period or beyond",
                    "Survivorship can only be used for medical data",
                    "Retention always requires money",
                ],

                "correct": 1,

                "explanation": (
                    "Survivorship is threshold-based duration analysis, while retention "
                    "usually measures presence at a particular elapsed period."
                ),
            },

            {
                "id": "M01.L04.Q07",

                "section_id": "returnship",

                "question": (
                    "Why is a fixed time box important when comparing repeat purchase "
                    "rates across acquisition cohorts?"
                ),

                "options": [
                    "It makes SQL shorter",
                    "It ensures older and newer cohorts receive comparable opportunity to repeat",
                    "It guarantees every customer repeats",
                    "It removes the need for cohort sizes",
                ],

                "correct": 1,

                "explanation": (
                    "Without a common observation window, older cohorts have had more time "
                    "to generate repeat behavior and are not directly comparable."
                ),
            },

            {
                "id": "M01.L04.Q08",

                "section_id": "cumulative",

                "question": (
                    "Why might revenue per customer be more informative than total cohort "
                    "revenue when comparing cohorts?"
                ),

                "options": [
                    "Total revenue cannot be calculated in SQL",
                    "It normalizes for different cohort sizes",
                    "Revenue per customer always increases",
                    "It removes all seasonality",
                ],

                "correct": 1,

                "explanation": (
                    "Normalizing by cohort size separates customer-level economics from "
                    "the simple effect of having a larger cohort."
                ),
            },

            {
                "id": "M01.L04.Q09",

                "section_id": "cross-sectional",

                "question": (
                    "What is a mix shift?"
                ),

                "options": [
                    "An error caused by a bad JOIN",
                    "A change in the composition of the population over time",
                    "A type of date conversion",
                    "A synonym for duplicate records",
                ],

                "correct": 1,

                "explanation": (
                    "A mix shift occurs when the relative shares of cohorts or segments "
                    "inside the overall population change."
                ),
            },

            {
                "id": "M01.L04.Q10",

                "section_id": "cross-sectional",

                "type": "open",

                "question": (
                    "A team studies only its current highest-value customers and concludes "
                    "that using Feature X causes long-term success. Explain the survivorship "
                    "bias risk and describe a better cohort-based analysis."
                ),
            },
        ],

        "passing_score": 70,
    },
}
