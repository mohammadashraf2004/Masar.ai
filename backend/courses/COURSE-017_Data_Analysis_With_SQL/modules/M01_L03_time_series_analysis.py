"""M01.L03 — Time Series Analysis.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Source alignment: Chapter 3, "Time Series Analysis".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from data preparation through time-based "
    "reasoning, trend analysis, rolling metrics, seasonality, and comparable-period "
    "analysis that can be used in dashboards, product analytics, and business reporting."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Time Series Analysis",

    "slug": "data-analysis-sql-m01-l03",

    "description": (
        "A practical introduction to time series analysis with SQL: normalize dates and "
        "time zones, build trends, compare related series, calculate shares and indices, "
        "construct rolling and cumulative metrics, handle sparse periods, and analyze "
        "seasonality with period-over-period comparisons."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "sql",
        "time-series",
        "date-time",
        "window-functions",
        "rolling-windows",
        "seasonality",
        "trend-analysis",
        "business-analysis",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Time Series Analysis",

        "content": """# Time Series Analysis

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L03  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapter 3, *Time Series Analysis*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what makes a data set a time series and distinguish trend, noise, seasonality, and structural change.
- Normalize timestamps across time zones and explain why daylight-saving transitions can distort analysis.
- Use SQL date and time functions such as `date_trunc`, `date_part`, `extract`, `to_char`, and date constructors.
- Perform date and time arithmetic with intervals and calculate elapsed time safely.
- Recognize timestamp problems when joining data from different source systems.
- Build monthly and yearly trends and explain how aggregation changes what patterns are visible.
- Compare multiple components of a time series using differences, ratios, and percent differences.
- Calculate percent-of-total metrics with self-joins or window functions.
- Index a time series to a base period and interpret positive and negative change from that baseline.
- Explain moving averages, LTM/TTM, DAU/WAU/MAU, and choose an appropriate rolling-window size.
- Calculate rolling metrics with self-joins and SQL window-frame clauses.
- Handle sparse time series with a date dimension or another complete set of time periods.
- Calculate cumulative values such as YTD, QTD, and MTD.
- Detect and reason about seasonality at monthly, weekly, daily, and intraday scales.
- Calculate MoM, YoY, and same-period-last-year comparisons using `lag`.
- Compare a current period with multiple comparable prior periods to reduce noise.

---

## 1. What a time series is — and what you are really trying to learn

A **time series** is a sequence of measurements arranged in time order. The measurements may occur every second, hour, day, week, month, quarter, or year.

Examples include:

- daily orders placed on an ecommerce site;
- hourly API latency;
- weekly active users;
- monthly revenue;
- quarterly customer churn;
- yearly population;
- a sensor reading every five seconds.

The important part is not simply that a table contains a timestamp. The important part is that **time is part of the analytical meaning**.

Imagine monthly revenue:

```text
Month       Revenue
2026-01     110,000
2026-02     114,000
2026-03     119,000
2026-04      91,000
2026-05     123,000
```

A normal aggregation might tell you the average revenue. A time-series analysis asks different questions:

- Is revenue generally increasing?
- Is April a real anomaly or a seasonal event?
- How does this month compare with last month?
- How does it compare with the same month last year?
- What is the 3-month or 12-month moving average?
- Has the contribution from one product category changed over time?

### Four ideas to keep separate

A useful beginner mental model is:

| Idea | Meaning | Example |
|---|---|---|
| Trend | Long-term direction | sales gradually rising over several years |
| Noise | Short-term irregular variation | one unusually weak Tuesday |
| Seasonality | Pattern that repeats on a regular cycle | December retail peak every year |
| Structural change | The process itself changes | a new product, regulation, pandemic, or pricing model |

Forecasting often uses past observations, but historical data does **not** guarantee future behavior. A forecast assumes that at least some patterns learned from the past remain relevant. A major structural change can break that assumption.

[[IMAGE_NEEDED: IMG-M01-L03-01 / Instructor Figure — Anatomy of a time series | Show a single time-series line annotated with long-term trend, repeated seasonal peaks, random noise, and one structural break | Learner should notice that an observed series can contain several different kinds of movement at once]]

### Why this matters in practice

A stakeholder may say, “Sales dropped 15%.” That statement is incomplete until you know **compared with what**:

- yesterday?
- the previous week?
- the same weekday last week?
- last month?
- the same month last year?
- a rolling baseline?

Good time-series analysis chooses a comparison that matches the business process.

---

## 2. Time zones: the first source of silent time-series errors

A timestamp is only meaningful if you know what clock it belongs to.

Many analytical systems store events in **UTC (Coordinated Universal Time)**. UTC is useful because it provides one consistent reference across regions and does not shift for daylight-saving time.

But users live in local time.

Suppose an event is stored as:

```text
2026-10-01 18:00:00 UTC
```

For a user in another time zone, that may correspond to evening, afternoon, or the next calendar day. If your question is “At what local hour do customers use the product?”, analyzing only UTC hour can be misleading.

### Daylight-saving time can change the length of a day

On a daylight-saving transition, a local calendar day may contain **23 hours** or **25 hours** rather than 24. A daily metric can therefore appear unusually low or high even when the underlying hourly rate is normal.

That is why you should ask early:

1. In what time zone was this timestamp recorded?
2. Does the timestamp itself contain an offset?
3. Do I need machine time or the user's local time?
4. Does the region observe daylight-saving changes?

[[IMAGE_NEEDED: IMG-M01-L03-02 / Instructor Figure — UTC event to local analytical time | Show one event timestamp stored in UTC branching into several local time zones, including a daylight-saving boundary, with local date/hour changing | Learner should notice that the same instant can belong to different local hours or even different calendar dates]]

### PostgreSQL-style conversion

```sql
SELECT timestamp_with_timezone AT TIME ZONE 'America/New_York';
```

Other databases expose functions such as `convert_timezone` or `convert_tz`. The exact function names and argument order are database-specific.

**Do not guess a missing time zone.** If a timestamp column has no zone information, verify the convention with documentation or the system owner.

---

## 3. Converting, truncating, extracting, and rebuilding dates

Raw timestamps are often more detailed than the question you want to answer.

If the source contains one timestamp per purchase:

```text
2026-01-05 14:23:11
2026-01-05 15:42:02
2026-02-02 09:03:55
```

but your question is about **monthly sales**, you need to map those detailed timestamps to a monthly grain.

### Current date and time

Common functions include:

```sql
SELECT current_date;
SELECT current_timestamp;
```

Other databases may use functions such as `now()` or `getdate()`.

### Truncating to a larger period

In PostgreSQL:

```sql
SELECT date_trunc('month', TIMESTAMP '2026-10-04 12:33:35');
```

returns the beginning of the month:

```text
2026-10-01 00:00:00
```

The same idea can be used for hour, day, week, quarter, or year.

A powerful habit is to think of `date_trunc` as answering:

> “Which time bucket does this timestamp belong to?”

### Extracting one component

```sql
SELECT extract(year  FROM order_timestamp) AS order_year,
       extract(month FROM order_timestamp) AS order_month,
       extract(hour  FROM order_timestamp) AS order_hour
FROM orders;
```

`date_part` provides similar functionality in some databases.

Use extraction when you want the **component itself**, such as month number `1` through `12`. Use truncation when you want a **date/timestamp representing the bucket**, such as `2026-10-01`.

### Formatting as text

`to_char` can return human-readable labels:

```sql
SELECT to_char(order_date, 'Month') AS month_name
FROM orders;
```

Be careful: formatted text is useful for presentation, but it usually should not replace the real date used for sorting and date arithmetic.

### Constructing a date from pieces

If year, month, and day are stored separately:

```sql
SELECT make_date(order_year, order_month, order_day)
FROM source_table;
```

Database vendors may call this `date_from_parts`, `datefromparts`, or another equivalent.

### Unix timestamps

Some systems store time as the number of seconds since the Unix epoch. In PostgreSQL, `to_timestamp` can convert such values into a normal timestamp.

The key principle is simple:

> **Keep time values as true date/time types for analysis; convert to display text only when you actually need display text.**

---

## 4. Date math, time math, intervals, and cross-source timestamps

Time-series analysis constantly asks “how long?” and “how far from?”

### Subtracting dates

```sql
SELECT DATE '2026-06-30' - DATE '2026-05-31' AS days_elapsed;
```

The result is the elapsed number of days.

Other systems provide `datediff`:

```sql
SELECT datediff('day', start_date, end_date);
```

### Adding or subtracting an interval

```sql
SELECT DATE '2026-06-01' + INTERVAL '7 days';
SELECT DATE '2026-06-01' - INTERVAL '3 months';
```

Intervals are important because months, years, and days do not have one fixed numeric conversion. A month may contain 28, 29, 30, or 31 days.

### Measuring tenure

A customer-tenure calculation may look conceptually like:

```sql
SELECT customer_id,
       current_date - signup_date AS tenure_days
FROM customers;
```

or use a vendor-specific month/year difference function when that is the required business unit.

### Time-of-day calculations

Elapsed time can also be measured below the day level:

```sql
SELECT resolved_at - opened_at AS response_time
FROM support_tickets;
```

This is useful for support response time, delivery duration, job execution time, and system latency.

### Combining different sources: normalize before you compare

Two source systems may disagree because:

- one stores UTC and the other local time;
- one records event time and the other ingestion time;
- a client device clock is several minutes wrong;
- mobile events arrive late after offline use;
- one source records seconds while another records milliseconds;
- corrupted timestamps appear impossibly far in the past or future.

A dangerous join is:

```sql
... ON mobile_event_time >= experiment_assignment_time
```

if the mobile device clock can be a few minutes behind the server. Valid events may be excluded.

Sometimes a tolerance window is more appropriate:

```sql
... ON mobile_event_time BETWEEN experiment_assignment_time - INTERVAL '5 minutes'
                         AND experiment_assignment_time + INTERVAL '1 day'
```

The exact tolerance must come from the system behavior, not from guesswork.

---

## 5. Start with the raw series, then change the grain deliberately

The chapter uses monthly US retail-sales data with multiple retail categories. The important learning point is not the specific industry; it is how changing grain changes what you can see.

[[IMAGE_NEEDED: IMG-M01-L03-03 / Source Figure 3-1 — Preview of the retail_sales table | Reproduce or recreate the source figure showing representative rows and fields from the monthly US retail sales data set | Learner should notice that the table contains a month, a business category, and a sales measure, which together define the basic analytical grain]]

### A simple monthly trend

```sql
SELECT sales_month,
       sales
FROM retail_sales
WHERE kind_of_business = 'Retail and food services sales, total'
ORDER BY sales_month;
```

This is already useful: one row per month and one measure per row.

[[IMAGE_NEEDED: IMG-M01-L03-04 / Source Figure 3-2 — Monthly retail and food-services sales trend | Recreate the source line chart of monthly total retail and food-services sales across time | Learner should notice the long-term direction together with short-term monthly variation]]

### Aggregating can reveal the long-term trend

```sql
SELECT extract(year FROM sales_month) AS sales_year,
       sum(sales) AS sales
FROM retail_sales
WHERE kind_of_business = 'Retail and food services sales, total'
GROUP BY 1
ORDER BY 1;
```

Yearly aggregation removes much of the month-to-month variation.

[[IMAGE_NEEDED: IMG-M01-L03-05 / Source Figure 3-3 — Yearly total retail and food-services sales | Recreate the yearly aggregate trend corresponding to Source Figure 3-3 | Learner should notice how aggregation smooths monthly noise and makes long-run rises or disruptions easier to see]]

### Aggregation is not automatically “better”

A yearly trend is smoother, but it may hide:

- a short outage;
- a one-month campaign;
- a sudden product launch;
- a holiday spike;
- a rapid decline that begins midyear.

Choose the grain that matches the question. It is often useful to examine **more than one grain** before deciding which tells the clearest story.

---

## 6. Comparing components: difference, ratio, and percent difference

A time-series table often contains several related series. Comparing them can reveal changes that are invisible when each series is viewed alone.

For example, aggregate several retail categories by year:

```sql
SELECT extract(year FROM sales_month) AS sales_year,
       kind_of_business,
       sum(sales) AS sales
FROM retail_sales
WHERE kind_of_business IN (
    'Book stores',
    'Sporting goods stores',
    'Hobby, toy, and game stores'
)
GROUP BY 1, 2
ORDER BY 1, 2;
```

[[IMAGE_NEEDED: IMG-M01-L03-06 / Source Figure 3-4 — Yearly sales for three leisure-related retail categories | Recreate the source multi-line trend for book stores, sporting-goods stores, and hobby/toy/game stores | Learner should notice that related categories can have very different long-run trajectories]]

Another comparison in the chapter uses men's and women's clothing-store sales.

[[IMAGE_NEEDED: IMG-M01-L03-07 / Source Figure 3-5 — Monthly men's versus women's clothing-store sales | Recreate the two monthly series from Source Figure 3-5 | Learner should notice both the level difference and the repeated seasonal movement in each series]]

Aggregating to years changes the view again:

[[IMAGE_NEEDED: IMG-M01-L03-08 / Source Figure 3-6 — Yearly men's versus women's clothing-store sales | Recreate the source yearly comparison | Learner should notice that the gap between the series changes over time rather than remaining fixed]]

### Step 1: pivot related measures onto one row

```sql
SELECT extract(year FROM sales_month) AS sales_year,
       sum(CASE WHEN kind_of_business = 'Women''s clothing stores'
                THEN sales END) AS womens_sales,
       sum(CASE WHEN kind_of_business = 'Men''s clothing stores'
                THEN sales END) AS mens_sales
FROM retail_sales
WHERE kind_of_business IN (
    'Men''s clothing stores',
    'Women''s clothing stores'
)
GROUP BY 1
ORDER BY 1;
```

Once both values are on the same row, several comparisons become easy.

### Absolute difference

```sql
womens_sales - mens_sales
```

This answers a question in original units, such as dollars.

[[IMAGE_NEEDED: IMG-M01-L03-09 / Source Figure 3-7 — Yearly absolute difference between women's and men's clothing sales | Recreate Source Figure 3-7 showing the difference across years | Learner should notice that an absolute gap can widen or narrow even if both underlying series move in the same direction]]

### Ratio

```sql
womens_sales / NULLIF(mens_sales, 0)
```

A ratio of `3.2` means one series is 3.2 times the other.

[[IMAGE_NEEDED: IMG-M01-L03-10 / Source Figure 3-8 — Ratio of women's to men's clothing sales | Recreate Source Figure 3-8 | Learner should notice that ratio and absolute difference tell related but not identical stories]]

### Percent difference

```sql
(womens_sales / NULLIF(mens_sales, 0) - 1) * 100
```

A statement such as “390% higher” can describe the same relationship as “4.9 times as large.” Choose the form that your audience can interpret correctly.

**Practical rule:** protect denominators with `NULLIF(..., 0)` when zero is possible.

{{exercise:M01.L03.EX01}}

---

## 7. Percent of total and indexing: two different reference frames

Two very useful time-series questions are:

1. **What share of the whole does this component represent?**
2. **How far has this series moved from a chosen baseline?**

These sound similar but answer different questions.

### Percent of total with a window function

```sql
SELECT sales_month,
       kind_of_business,
       sales,
       sum(sales) OVER (PARTITION BY sales_month) AS total_sales,
       sales * 100.0 /
           NULLIF(sum(sales) OVER (PARTITION BY sales_month), 0) AS pct_total
FROM retail_sales
WHERE kind_of_business IN (
    'Men''s clothing stores',
    'Women''s clothing stores'
);
```

The window function calculates a total for the relevant month without collapsing the individual category rows.

[[IMAGE_NEEDED: IMG-M01-L03-11 / Source Figure 3-9 — Men's and women's clothing sales as percent of monthly total | Recreate Source Figure 3-9 | Learner should notice how category share can change even when both categories' raw sales are moving]]

You can also calculate each month's share of its own year's sales by partitioning on year and category.

[[IMAGE_NEEDED: IMG-M01-L03-12 / Source Figure 3-10 — Percent of yearly sales by month for 2019 | Recreate Source Figure 3-10 for men's and women's clothing stores | Learner should notice that percent-of-year metrics expose how sales are distributed across months and reveal seasonal timing differences]]

### Indexing to a baseline

An **index** asks how a series changed relative to a chosen reference period.

First calculate one value per year, then use `first_value`:

```sql
WITH yearly AS (
    SELECT extract(year FROM sales_month) AS sales_year,
           sum(sales) AS sales
    FROM retail_sales
    WHERE kind_of_business = 'Women''s clothing stores'
    GROUP BY 1
)
SELECT sales_year,
       sales,
       first_value(sales) OVER (ORDER BY sales_year) AS base_sales,
       (sales / NULLIF(first_value(sales) OVER (ORDER BY sales_year), 0) - 1) * 100
           AS pct_from_base
FROM yearly
ORDER BY sales_year;
```

If the base period is `0%`, then:

- `+20%` means the value is 20% above the baseline;
- `-15%` means it is 15% below the baseline.

[[IMAGE_NEEDED: IMG-M01-L03-13 / Source Figure 3-11 — Men's and women's clothing sales indexed to 1992 | Recreate the source indexed comparison with 1992 as the base | Learner should notice that indexing removes the original scale difference and makes relative trajectories easier to compare]]

### Do not confuse share with index

- **Percent of total** compares a component with a whole at the same time.
- **Indexing** compares a series with itself at a baseline time.

---

## 8. Rolling windows: smooth noise without throwing away the timeline

Aggregating monthly data into years smooths noise, but it changes the grain. A **rolling window** keeps the original timeline while summarizing several neighboring periods.

Common names include:

- moving average;
- rolling sum;
- trailing twelve months (**TTM**);
- last twelve months (**LTM**);
- rolling count.

A 12-month moving average for December uses December plus the previous 11 months. In January, the window moves forward one month.

[[IMAGE_NEEDED: IMG-M01-L03-14 / Source Figure 3-12 — LTM versus YTD window | Recreate Source Figure 3-12 showing a fixed trailing window and a year-to-date cumulative window around the same focal month | Learner should notice that LTM has a fixed width while YTD expands from a reset point]]

### Three design decisions

Every rolling metric needs three decisions:

1. **Window size** — 7 days, 30 days, 12 months, etc.
2. **Aggregation** — `avg`, `sum`, `count`, `min`, `max`, or another calculation.
3. **Partitioning** — whether the window is separate per product, customer, region, year, or other group.

A longer window smooths more noise but reacts more slowly. A shorter window reacts faster but is less stable.

### DAU, WAU, and MAU

Product teams often use:

- **DAU** — daily active users;
- **WAU** — users active in a recent 7-day window;
- **MAU** — users active in a recent ~30-day window.

These are not interchangeable.

DAU is sensitive to daily usage. WAU smooths weekday/weekend differences while reacting faster than MAU. MAU is more stable but can hide churn for weeks because a user may remain inside the 30-day window after they stop returning.

There is no universally “best” active-user window. The correct window depends on the natural usage rhythm of the product.

---

## 9. Calculating rolling metrics with self-joins and window frames

There are two major SQL strategies.

### Method A: self-join by date range

For each anchor month, join the months inside the trailing interval:

```sql
SELECT a.sales_month,
       avg(b.sales) AS moving_avg,
       count(b.sales) AS records_count
FROM retail_sales a
JOIN retail_sales b
  ON a.kind_of_business = b.kind_of_business
 AND b.sales_month BETWEEN a.sales_month - INTERVAL '11 months'
                       AND a.sales_month
WHERE a.kind_of_business = 'Women''s clothing stores'
GROUP BY 1
ORDER BY 1;
```

Why `11 months`, not `12`? Because `BETWEEN` is inclusive. The current month plus the previous 11 months gives 12 months.

A useful quality check is `count(b.sales)`. If a “12-month” window contains only 9 observations, you should know that before interpreting the average.

[[IMAGE_NEEDED: IMG-M01-L03-15 / Source Figure 3-13 — Monthly sales and 12-month moving average | Recreate Source Figure 3-13 for women's clothing-store sales | Learner should notice that the rolling average preserves the monthly timeline while smoothing short-term volatility]]

### Method B: a window frame

```sql
SELECT sales_month,
       sales,
       avg(sales) OVER (
           ORDER BY sales_month
           ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
       ) AS moving_avg,
       count(sales) OVER (
           ORDER BY sales_month
           ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
       ) AS records_count
FROM retail_sales
WHERE kind_of_business = 'Women''s clothing stores'
ORDER BY sales_month;
```

The frame tells SQL exactly which rows around the current row belong to the calculation.

Common boundaries include:

```text
UNBOUNDED PRECEDING
n PRECEDING
CURRENT ROW
n FOLLOWING
UNBOUNDED FOLLOWING
```

[[IMAGE_NEEDED: IMG-M01-L03-16 / Source Figure 3-14 — Window frame boundaries | Recreate Source Figure 3-14 illustrating PRECEDING, CURRENT ROW, FOLLOWING, and UNBOUNDED frame choices relative to a current row | Learner should notice that a window frame is defined relative to the current ordered row]]

### `ROWS`, `RANGE`, and `GROUPS`

- `ROWS` counts physical rows.
- `RANGE` works by value boundaries relative to the ordering key.
- `GROUPS` works with peer groups that share ordering values.

For a beginner, `ROWS` is often the easiest to reason about. But it is only correct for a monthly moving window if one row really represents one month.

**Important:** `ROWS BETWEEN 11 PRECEDING ...` means 12 rows, not necessarily 12 calendar months.

That distinction becomes critical when periods are missing.

---

## 10. Sparse time series: missing rows are not the same as zero

A real event table often has no row for a period in which nothing happened.

Imagine product sales:

```text
Month     Product   Sales
Jan       A         20
Mar       A         15
Jun       A         25
```

A window of “previous 3 rows” is **not** a three-month window here. It spans January to June.

This is why sparse time series require a complete calendar scaffold.

### Use a date dimension

A **date dimension** contains one row per day or period, whether or not a business event occurred. It can provide:

- calendar date;
- first day of month;
- month number/name;
- quarter;
- year;
- weekday;
- fiscal attributes.

Join the complete calendar to the sparse event data, then calculate the interval-based rolling metric.

Conceptually:

```sql
SELECT calendar.month_start,
       avg(sales.sales) AS moving_avg,
       count(sales.sales) AS observations
FROM month_calendar AS calendar
LEFT JOIN monthly_sales AS sales
  ON sales.sales_month BETWEEN calendar.month_start - INTERVAL '11 months'
                           AND calendar.month_start
GROUP BY calendar.month_start
ORDER BY calendar.month_start;
```

The complete calendar ensures every analytical month exists, even when no event row exists.

### Zero, missing, and not applicable

Do not automatically replace a missing month with zero. Ask what the absence means:

- product available but no sales → zero may be correct;
- tracking outage → unknown, not zero;
- product did not exist yet → not applicable;
- source data arrived late → temporarily missing.

{{exercise:M01.L03.EX02}}

---

## 11. Cumulative values: YTD, QTD, and MTD

A rolling window has a fixed size. A **cumulative window** grows from a defined starting point.

Examples:

- **YTD** — from the start of the year through the current row;
- **QTD** — from the start of the quarter;
- **MTD** — from the start of the month.

For monthly sales, YTD can be calculated with a window function that resets each year:

```sql
SELECT sales_month,
       sales,
       sum(sales) OVER (
           PARTITION BY extract(year FROM sales_month)
           ORDER BY sales_month
       ) AS sales_ytd
FROM retail_sales
WHERE kind_of_business = 'Women''s clothing stores'
ORDER BY sales_month;
```

In January, YTD contains one month. In February, it contains two. By December, it contains the whole year. In the next January, the partition resets.

[[IMAGE_NEEDED: IMG-M01-L03-17 / Source Figure 3-15 — Monthly and cumulative annual sales | Recreate Source Figure 3-15 showing monthly women's clothing-store sales together with the YTD cumulative series | Learner should notice that the cumulative line grows within a year and resets when a new year begins]]

You can also implement cumulative logic with a self-join, but the window-function form is usually shorter and easier to audit.

### Cumulative is not rolling

For October:

- 12-month rolling sales might include November of the prior year through October;
- YTD includes January through October of the current year.

The windows answer different questions.

---

## 12. Seasonality: recurring patterns are signal, not random noise

**Seasonality** is a pattern that repeats on a regular schedule.

It can occur at many scales:

- every hour — lunch and dinner peaks for a restaurant;
- every day — morning versus evening product usage;
- every week — weekday versus weekend behavior;
- every month — billing-cycle effects;
- every year — holidays, weather, school schedules;
- every several years — election or contract cycles.

To detect seasonality:

1. graph the series;
2. inspect more than one time grain;
3. use domain knowledge;
4. ask whether peaks and dips recur at roughly the same position in the cycle.

The retail examples show different seasonal strength: some categories have dramatic annual peaks, others have modest variation.

[[IMAGE_NEEDED: IMG-M01-L03-18 / Source Figure 3-16 — Contrasting seasonal patterns | Recreate Source Figure 3-16 comparing book-store, grocery-store, and jewelry-store monthly patterns | Learner should notice that seasonality can be strong, weak, or have multiple peaks depending on the business process]]

### Two broad strategies

You can deal with seasonality by:

- **smoothing it**, using aggregation or rolling windows; or
- **comparing like with like**, such as this December versus last December.

The second strategy leads directly to period-over-period analysis.

---

## 13. MoM and YoY with `lag`

The `lag` window function returns a previous value from an ordered series.

Basic form:

```sql
lag(value, offset, default) OVER (...)
```

The default offset is `1`.

### Month-over-month comparison

```sql
SELECT sales_month,
       sales,
       lag(sales) OVER (ORDER BY sales_month) AS prev_month_sales,
       (sales / NULLIF(lag(sales) OVER (ORDER BY sales_month), 0) - 1) * 100
           AS mom_growth_pct
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month;
```

For the first row, there is no previous row, so `lag` returns `NULL` unless a default is supplied.

[[IMAGE_NEEDED: IMG-M01-L03-19 / Source Figure 3-17 — Month-over-month growth for book-store sales | Recreate Source Figure 3-17 | Learner should notice that MoM growth can still contain strong seasonality rather than eliminating it]]

### Year-over-year on annual aggregates

If your data has first been aggregated to years, the same `lag` pattern compares one year with the prior year.

```sql
WITH yearly AS (
    SELECT extract(year FROM sales_month) AS sales_year,
           sum(sales) AS yearly_sales
    FROM retail_sales
    WHERE kind_of_business = 'Book stores'
    GROUP BY 1
)
SELECT sales_year,
       yearly_sales,
       lag(yearly_sales) OVER (ORDER BY sales_year) AS prev_year_sales,
       (yearly_sales /
            NULLIF(lag(yearly_sales) OVER (ORDER BY sales_year), 0) - 1) * 100
           AS yoy_growth_pct
FROM yearly
ORDER BY sales_year;
```

### `lead` looks forward

`lead` uses the same idea but returns a later row. It can be useful when labeling what happens after an event, though in most historical comparison reports `lag` is the more natural direction.

---

## 14. Same period last year: compare comparable seasonal positions

MoM compares neighboring months. That can be misleading when the business has strong seasonality.

A December-to-January comparison mixes two different seasonal positions. A better question may be:

> How did this January compare with last January?

One elegant method is to partition by month number and order by year:

```sql
SELECT sales_month,
       sales,
       lag(sales) OVER (
           PARTITION BY extract(month FROM sales_month)
           ORDER BY sales_month
       ) AS same_month_last_year_sales
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month;
```

Within the January partition, SQL sees January 1992, January 1993, January 1994, and so on. `lag` therefore returns the prior January.

Now calculate:

```sql
sales - same_month_last_year_sales
```

or:

```sql
(sales / NULLIF(same_month_last_year_sales, 0) - 1) * 100
```

[[IMAGE_NEEDED: IMG-M01-L03-20 / Source Figure 3-18 — Same-month YoY difference and growth for book stores | Recreate Source Figure 3-18 showing book-store sales together with absolute and percent YoY change | Learner should notice that comparing the same seasonal position makes unusually strong or weak months easier to identify]]

### Align months across years

Another useful output puts January through December on the x-axis and draws one line per year. SQL can produce the wide structure with conditional aggregation:

```sql
SELECT extract(month FROM sales_month) AS month_number,
       to_char(sales_month, 'Month') AS month_name,
       max(CASE WHEN extract(year FROM sales_month) = 2024 THEN sales END) AS sales_2024,
       max(CASE WHEN extract(year FROM sales_month) = 2025 THEN sales END) AS sales_2025,
       max(CASE WHEN extract(year FROM sales_month) = 2026 THEN sales END) AS sales_2026
FROM retail_sales
WHERE kind_of_business = 'Book stores'
  AND sales_month BETWEEN DATE '2024-01-01' AND DATE '2026-12-31'
GROUP BY 1, 2
ORDER BY 1;
```

[[IMAGE_NEEDED: IMG-M01-L03-21 / Source Figure 3-19 — Book-store years aligned by month | Recreate Source Figure 3-19 with multiple yearly lines aligned from January through December | Learner should notice recurring month-of-year shape and how the level changes from one year to another]]

This view is especially useful for inventory planning, staffing, marketing schedules, and any process where the shape of the year matters.

---

## 15. Comparing with multiple prior periods

A single prior period can itself be unusual.

Suppose this month's comparison month last year had:

- a major outage;
- extreme weather;
- a one-time campaign;
- a supply shortage;
- a holiday shifted into another week.

Comparing against several prior comparable periods can create a more stable baseline.

### Multiple `lag` offsets

```sql
SELECT sales_month,
       sales,
       lag(sales, 1) OVER (
           PARTITION BY extract(month FROM sales_month)
           ORDER BY sales_month
       ) AS prev_1,
       lag(sales, 2) OVER (
           PARTITION BY extract(month FROM sales_month)
           ORDER BY sales_month
       ) AS prev_2,
       lag(sales, 3) OVER (
           PARTITION BY extract(month FROM sales_month)
           ORDER BY sales_month
       ) AS prev_3
FROM retail_sales
WHERE kind_of_business = 'Book stores';
```

Then compare the current value with their average.

A cleaner window-frame version is:

```sql
SELECT sales_month,
       sales,
       avg(sales) OVER (
           PARTITION BY extract(month FROM sales_month)
           ORDER BY sales_month
           ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
       ) AS avg_same_month_prev_3_years
FROM retail_sales
WHERE kind_of_business = 'Book stores';
```

This frame deliberately excludes the current row.

### Why this can be better

If one previous year was abnormal, the average of several comparable years can reduce its influence. But there is a tradeoff: more historical averaging can also hide a genuine recent structural change.

Always ask:

- Is the process stable enough for old periods to remain relevant?
- Did the product, market, or tracking system change?
- Are prices nominal or inflation-adjusted?
- Has the customer mix changed?

Time-series SQL is powerful, but the query cannot decide whether the past is still comparable. That remains an analytical judgment.

{{exercise:M01.L03.EX03}}

---

## Important misconceptions

### Misconception 1: “A timestamp column automatically makes my analysis correct over time.”

A timestamp is only the starting point. You still need to understand time zone, grain, missing periods, event time versus ingestion time, and the comparison window.

### Misconception 2: “A moving average is always more truthful than the raw series.”

A moving average is smoother, not automatically more truthful. It may hide meaningful short-lived changes and reacts to shocks for several later periods because the shock remains inside the window.

### Misconception 3: “MoM growth removes seasonality.”

It often does not. If December is normally much larger than November, the same seasonal jump can appear every year in MoM growth. Same-period-last-year comparisons are often more appropriate.

### Misconception 4: “If a month is absent from the table, its value is zero.”

Absence may mean zero, missing data, not applicable, outage, or late arrival. A complete calendar helps you expose missing periods, but business meaning determines how to label them.

### Misconception 5: “`ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` always means twelve months.”

It means twelve rows. It represents twelve months only when there is exactly one correctly ordered row per month in that partition.

---

## Key terminology

| Term | Meaning |
|---|---|
| Time series | Measurements ordered over time |
| Time grain | The unit represented by one time bucket, such as hour, day, or month |
| UTC | Global reference time commonly used for machine timestamps |
| Interval | A duration such as 7 days or 3 months used in date/time math |
| Trend | Long-term direction of a series |
| Noise | Irregular short-term variation |
| Seasonality | A repeating pattern at a regular time interval |
| Structural change | A change in the underlying process that may make earlier history less comparable |
| Percent of total | A component divided by the relevant whole for the same period |
| Index | Change in a series relative to a selected baseline period |
| Rolling window | A moving set of periods used for an aggregation |
| LTM / TTM | Last/trailing twelve months |
| DAU / WAU / MAU | Daily, weekly, and monthly active users |
| Window frame | The subset of ordered rows included in a window calculation |
| Sparse time series | A series where some expected time periods have no row |
| Date dimension | A complete calendar table containing one row per date/period plus date attributes |
| YTD / QTD / MTD | Cumulative year-, quarter-, or month-to-date measures |
| MoM | Month-over-month comparison |
| YoY | Year-over-year comparison |
| `lag` | Window function returning a prior row's value |
| `lead` | Window function returning a later row's value |

---

## Self-check

Before continuing, make sure you can answer:

1. Why can daylight-saving changes make a daily sales total look abnormal?
2. What is the difference between `date_trunc('month', ts)` and `extract(month FROM ts)`?
3. Why are intervals safer than assuming every month has 30 days?
4. What can go wrong when one data source stores UTC and another stores local time?
5. Why can yearly aggregation make a trend easier to see, and what can it hide?
6. When would an absolute difference be more useful than a ratio?
7. How is percent-of-total different from indexing to a base year?
8. What three choices define a rolling metric?
9. Why does a 12-row frame not always equal 12 months?
10. Why is a date dimension useful with sparse event data?
11. What causes a cumulative YTD calculation to reset?
12. Why might MoM growth still contain seasonality?
13. How does partitioning `lag` by month number create same-month-last-year comparisons?
14. What tradeoff is introduced when comparing against the average of several prior years?

---

## Retain this idea

**Time-series analysis is mostly about choosing the correct temporal reference frame. Before trusting a trend, rolling metric, or growth rate, make sure the timestamps, grain, missing periods, window, seasonality, and comparison baseline all match the question you are actually trying to answer.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "time-series-mental-model",
                "title": "What a time series is — and what you are really trying to learn",
                "order": 1,
            },
            {
                "id": "time-zones",
                "title": "Time zones: the first source of silent time-series errors",
                "order": 2,
            },
            {
                "id": "date-time-formatting",
                "title": "Converting, truncating, extracting, and rebuilding dates",
                "order": 3,
            },
            {
                "id": "date-time-math",
                "title": "Date math, time math, intervals, and cross-source timestamps",
                "order": 4,
            },
            {
                "id": "retail-data-and-basic-trends",
                "title": "Start with the raw series, then change the grain deliberately",
                "order": 5,
            },
            {
                "id": "comparing-components",
                "title": "Comparing components: difference, ratio, and percent difference",
                "order": 6,
            },
            {
                "id": "percent-of-total-and-indexing",
                "title": "Percent of total and indexing: two different reference frames",
                "order": 7,
            },
            {
                "id": "rolling-window-concepts",
                "title": "Rolling windows: smooth noise without throwing away the timeline",
                "order": 8,
            },
            {
                "id": "rolling-window-sql",
                "title": "Calculating rolling metrics with self-joins and window frames",
                "order": 9,
            },
            {
                "id": "sparse-time-series",
                "title": "Sparse time series: missing rows are not the same as zero",
                "order": 10,
            },
            {
                "id": "cumulative-values",
                "title": "Cumulative values: YTD, QTD, and MTD",
                "order": 11,
            },
            {
                "id": "seasonality",
                "title": "Seasonality: recurring patterns are signal, not random noise",
                "order": 12,
            },
            {
                "id": "mom-yoy",
                "title": "MoM and YoY with lag",
                "order": 13,
            },
            {
                "id": "same-period-last-year",
                "title": "Same period last year: compare comparable seasonal positions",
                "order": 14,
            },
            {
                "id": "multiple-prior-periods",
                "title": "Comparing with multiple prior periods",
                "order": 15,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Compare Two Time Series Correctly",

            "lesson_code": "M01.L03",

            "section_id": "comparing-components",

            "placement": "after_section",

            "description": (
                "Practice converting two related monthly series into yearly comparison "
                "metrics and deciding which comparison communicates the business question best."
            ),

            "instructions": (
                "Assume a monthly retail_sales table has sales_month, kind_of_business, and sales.\n"
                "1. Aggregate Men's clothing stores and Women's clothing stores to yearly sales.\n"
                "2. Pivot the two categories so each year has womens_sales and mens_sales columns.\n"
                "3. Calculate the absolute difference.\n"
                "4. Calculate the ratio using NULLIF to protect the denominator.\n"
                "5. Calculate the percent difference.\n"
                "6. Explain one situation where absolute difference is easier to interpret and one "
                "where ratio or percent difference is more useful."
            ),

            "expected_output": (
                "A SQL query or staged SQL solution returning one row per year with both sales "
                "series, absolute difference, ratio, and percent difference, plus a short interpretation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "time-series-comparison",
                "conditional-aggregation",
                "ratio-analysis",
                "percent-change",
                "sql-reasoning",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Build a Rolling Metric on Sparse Data",

            "lesson_code": "M01.L03",

            "section_id": "sparse-time-series",

            "placement": "after_section",

            "description": (
                "Practice recognizing when row-based windows fail and use a complete calendar "
                "to build a time-correct rolling metric."
            ),

            "instructions": (
                "A product_sales table contains monthly rows only when a product sold at least once.\n"
                "1. Explain why ROWS BETWEEN 2 PRECEDING AND CURRENT ROW does not necessarily mean three months.\n"
                "2. Create or assume a month_calendar table containing one row per month.\n"
                "3. Join the calendar to product_sales so every analytical month exists.\n"
                "4. Calculate a trailing 3-calendar-month sum for one product.\n"
                "5. Return an observation count beside the sum.\n"
                "6. Explain how you would distinguish a true zero-sales month from an unknown/missing month."
            ),

            "expected_output": (
                "A calendar-based SQL pattern returning one row per month, a trailing three-month "
                "metric, an observation count, and a brief explanation of zero versus missing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "rolling-windows",
                "sparse-data",
                "date-dimension",
                "time-grain",
                "data-quality",
            ],
        },

        {
            "id": "M01.L03.EX03",

            "title": "Analyze Seasonality and Comparable Growth",

            "lesson_code": "M01.L03",

            "section_id": "multiple-prior-periods",

            "placement": "after_section",

            "description": (
                "Combine lag functions, seasonal partitioning, and multi-year baselines to "
                "separate recurring seasonal movement from more meaningful change."
            ),

            "instructions": (
                "Using monthly book-store sales:\n"
                "1. Calculate MoM percent growth with lag.\n"
                "2. Calculate same-month-last-year sales by partitioning lag by month number.\n"
                "3. Calculate YoY percent growth.\n"
                "4. Calculate the average sales for the same month across the three previous years "
                "using a window frame from 3 PRECEDING to 1 PRECEDING.\n"
                "5. Compare current sales to that three-year baseline.\n"
                "6. Explain which of MoM, YoY, and the three-year baseline is most robust to seasonality "
                "and what new risk the longer baseline introduces."
            ),

            "expected_output": (
                "SQL producing MoM growth, same-month YoY growth, and a three-prior-year comparable "
                "baseline, followed by a short interpretation of the strengths and limitations of each."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "seasonality",
                "lag",
                "period-over-period",
                "window-frames",
                "analytical-interpretation",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "Time Series Analysis — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",

                "section_id": "time-zones",

                "question": (
                    "Why can a daylight-saving transition make one local day's sales look unusually low?"
                ),

                "options": [
                    "SQL automatically deletes one hour of sales every year",
                    "The local day may contain only 23 clock hours even when the underlying hourly rate is normal",
                    "UTC changes its offset twice each year",
                    "Window functions cannot process daylight-saving dates",
                ],

                "correct": 1,

                "explanation": (
                    "A local daylight-saving transition can shorten a day to 23 hours. Comparing "
                    "its raw daily total with a normal 24-hour day can therefore be misleading."
                ),
            },

            {
                "id": "M01.L03.Q02",

                "section_id": "date-time-formatting",

                "question": (
                    "What is the main difference between date_trunc('month', ts) and extract(month FROM ts)?"
                ),

                "options": [
                    "date_trunc returns the timestamp bucket boundary, while extract returns the month component",
                    "extract converts UTC to local time, while date_trunc cannot",
                    "date_trunc works only on strings",
                    "There is no difference",
                ],

                "correct": 0,

                "explanation": (
                    "Truncation returns a date/timestamp representing the period bucket, while extraction "
                    "returns a component such as month number."
                ),
            },

            {
                "id": "M01.L03.Q03",

                "section_id": "comparing-components",

                "question": (
                    "Why can a ratio and an absolute difference tell different stories about the same two series?"
                ),

                "options": [
                    "Ratios ignore the denominator completely",
                    "Absolute difference measures original units while a ratio measures relative scale",
                    "Absolute difference cannot be negative",
                    "Ratios can only be used with dates",
                ],

                "correct": 1,

                "explanation": (
                    "The absolute gap answers how many units separate the values; the ratio answers how "
                    "large one value is relative to the other."
                ),
            },

            {
                "id": "M01.L03.Q04",

                "section_id": "percent-of-total-and-indexing",

                "question": (
                    "Which statement correctly distinguishes percent-of-total from indexing?"
                ),

                "options": [
                    "Percent-of-total compares a component with a contemporaneous whole; indexing compares a series with a time baseline",
                    "Both always produce the same number",
                    "Indexing can only be performed with a self-join",
                    "Percent-of-total requires a DATE field but indexing does not",
                ],

                "correct": 0,

                "explanation": (
                    "The two techniques use different reference frames: a whole at the same time versus "
                    "the same series at a chosen starting period."
                ),
            },

            {
                "id": "M01.L03.Q05",

                "section_id": "rolling-window-sql",

                "question": (
                    "When there is exactly one row per month, how many months are included by ROWS BETWEEN 11 PRECEDING AND CURRENT ROW?"
                ),

                "options": [
                    "10",
                    "11",
                    "12",
                    "It always includes the entire table",
                ],

                "correct": 2,

                "explanation": (
                    "The frame contains the current row plus eleven preceding rows, giving twelve observations."
                ),
            },

            {
                "id": "M01.L03.Q06",

                "section_id": "sparse-time-series",

                "question": (
                    "Why is a complete date dimension useful for a sparse time series?"
                ),

                "options": [
                    "It converts every missing value to zero automatically",
                    "It provides the expected time periods even when no event row exists",
                    "It eliminates the need to know the analytical grain",
                    "It guarantees all source timestamps are in UTC",
                ],

                "correct": 1,

                "explanation": (
                    "A calendar scaffold preserves the timeline. Analysts can then decide whether an "
                    "absent observation means zero, unknown, or not applicable."
                ),
            },

            {
                "id": "M01.L03.Q07",

                "section_id": "cumulative-values",

                "question": (
                    "What causes a YTD window calculation to reset at the beginning of each year?"
                ),

                "options": [
                    "LIMIT",
                    "A PARTITION BY expression based on year",
                    "The use of DISTINCT",
                    "The absence of ORDER BY",
                ],

                "correct": 1,

                "explanation": (
                    "Partitioning by year creates a separate running calculation for each year, while "
                    "ORDER BY determines the accumulation order inside the year."
                ),
            },

            {
                "id": "M01.L03.Q08",

                "section_id": "mom-yoy",

                "question": (
                    "Why might month-over-month growth still show strong seasonality?"
                ),

                "options": [
                    "Because lag cannot return numeric values",
                    "Because neighboring months can naturally occupy very different positions in a recurring seasonal cycle",
                    "Because MoM always compares the same month in different years",
                    "Because seasonality exists only in yearly data",
                ],

                "correct": 1,

                "explanation": (
                    "If December is regularly much stronger than November, that seasonal change will "
                    "reappear in MoM growth each year."
                ),
            },

            {
                "id": "M01.L03.Q09",

                "section_id": "same-period-last-year",

                "question": (
                    "How does partitioning lag by extract(month FROM sales_month) help analyze seasonality?"
                ),

                "options": [
                    "It groups all months into one partition",
                    "It makes each month number its own ordered sequence, so January is compared with previous Januaries, February with previous Februaries, and so on",
                    "It removes all null values",
                    "It automatically forecasts next year's sales",
                ],

                "correct": 1,

                "explanation": (
                    "Partitioning by month number aligns comparable seasonal positions across years."
                ),
            },

            {
                "id": "M01.L03.Q10",

                "section_id": "multiple-prior-periods",

                "type": "open",

                "question": (
                    "A product has strong monthly seasonality and last year's comparable month was distorted by a major outage. "
                    "Design a SQL comparison using several prior comparable periods, explain why it may be more robust than a single-year comparison, "
                    "and identify one reason the longer historical baseline could still mislead you."
                ),
            },
        ],

        "passing_score": 70,
    },
}
