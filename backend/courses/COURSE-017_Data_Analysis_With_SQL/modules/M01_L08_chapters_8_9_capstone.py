"""M01.L08 — Building Production-Ready Analytical Datasets & Applied SQL Patterns.

Two source chapters -> one complete learner-facing capstone Lesson + essential inline Images +
inline Exercises + lesson Quiz.
Source alignment: Chapters 8–9, "Creating Complex Data Sets for Analysis" and "Conclusion".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L08"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from data preparation and time-based reasoning "
    "through cohort analysis, text analysis, anomaly detection, experimentation, complex "
    "analytical data-set construction, and integrated business analysis patterns."
)

SOURCE_CHAPTER = "8–9"

SOURCE_PAGES = "Not provided in the supplied chapter extracts"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building Production-Ready Analytical Datasets & Applied SQL Patterns",

    "slug": "data-analysis-sql-m01-l08",

    "description": (
        "A capstone lesson that combines Chapters 8 and 9: deciding where analytical "
        "logic should live, organizing and maintaining complex SQL, understanding query "
        "evaluation order, choosing among subqueries, temp tables, and CTEs, producing "
        "multi-level aggregations, controlling data-set size and privacy, and applying "
        "the full SQL toolkit to funnel, churn/lapse, and basket analysis."
    ),

    "order": 8,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 6.0,

    "skill_tags": [
        "sql",
        "complex-sql",
        "etl",
        "views",
        "ctes",
        "subqueries",
        "temporary-tables",
        "grouping-sets",
        "cube",
        "rollup",
        "sampling",
        "data-privacy",
        "pii",
        "funnel-analysis",
        "churn",
        "basket-analysis",
        "analytical-engineering",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
    ],

    # =======================================================================
    # ESSENTIAL IMAGE POLICY
    # =======================================================================
    #
    # Chapters 8 and 9 are intentionally merged into this single final lesson.
    # Only figures that materially improve understanding are requested.
    # Source screenshots and sample-table figures are omitted.
    #
    # Essential figures requested:
    # - IMG-M01-L08-01: where analytical logic should live
    # - IMG-M01-L08-02: SQL clause evaluation order
    # - IMG-M01-L08-03: funnel conversion model
    # - IMG-M01-L08-04: churn/lapse threshold from activity gaps
    # - IMG-M01-L08-05: basket-analysis self-join
    #

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Building Production-Ready Analytical Datasets & Applied SQL Patterns",

        "content": """# Building Production-Ready Analytical Datasets & Applied SQL Patterns

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L08  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapters 8–9, *Creating Complex Data Sets for Analysis* and *Conclusion*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this capstone lesson, you should be able to:

- Decide whether analytical logic should remain in SQL, move upstream into ETL, live behind a view, or be performed downstream in BI/Python/R.
- Explain the trade-offs between flexibility, performance, freshness, visibility, and maintainability.
- Organize long SQL queries with comments, formatting, naming, and version control.
- Explain the logical evaluation order of major SQL clauses.
- Choose appropriately among subqueries, lateral subqueries, temporary tables, and common table expressions.
- Use `GROUPING SETS`, `CUBE`, and `ROLLUP` to produce multi-level aggregations without large stacks of `UNION` queries.
- Reduce data-set size through sampling, coarser time grain, category grouping, and flags.
- Choose the correct entity when sampling so related records remain together.
- Recognize sampling bias and validate that a sampling key behaves approximately randomly.
- Minimize personally identifiable information in analytical outputs.
- Explain the difference between masking/hashing and strong encryption.
- Build a funnel analysis with the correct eligible population and join structure.
- Distinguish sequential funnels from funnels with skippable steps.
- Calculate overall and step-to-step conversion.
- Use historical gap distributions to define active, lapsed, and churned states.
- Build "time since last activity" metrics.
- Perform basket analysis using string aggregation and self-joins.
- Avoid duplicate/reversed item pairs in basket analysis.
- Recognize performance and interpretation traps in basket analysis.
- Combine techniques from earlier lessons into complete analytical workflows.
- Treat SQL as one tool in a larger data-analysis ecosystem.
- Communicate analytical results in a way that supports decisions.

---

## 1. From one-off query to reusable analytical data set

Earlier lessons focused on specific analytical questions:

- time-series trends;
- cohort retention;
- text parsing;
- anomaly detection;
- experiments.

In real work, you are often asked to create something broader:

> **Build a data set that can support many future analyses.**

The destination might be:

- a BI dashboard;
- a CSV or Parquet export;
- a table in a warehouse;
- a Python notebook;
- a machine-learning pipeline;
- a recurring report.

This changes the problem.

A one-off query only needs to answer today's question correctly.

A reusable analytical data set also needs to be:

```text
correct
maintainable
understandable
reasonably fast
stable enough for repeated use
appropriately detailed
privacy-aware
```

### Why complexity grows

A reusable data set may combine:

```text
customer attributes
+ transaction summaries
+ cohort information
+ status flags
+ rolling metrics
+ parsed text fields
+ experiment assignments
+ anomaly-cleaning rules
```

Stakeholders may then ask:

```text
Can you add country?
Can you add first purchase?
Can you add 30-day revenue?
Can we split this by plan?
Can we exclude test users?
```

The query can become difficult to understand long before it becomes technically impossible to run.

This is why **organization and architecture** become analytical skills.

---

## 2. Decide where the logic should live

A transformation can often be implemented in several places:

```text
raw database tables
-> SQL query
-> view / materialized view
-> ETL / transformation pipeline
-> BI tool
-> Python / R / ML environment
```

There is rarely one universal answer.

The correct location depends on the use case.

[[IMAGE_NEEDED: IMG-M01-L08-01 / Instructor Figure — Where analytical logic should live | Show a left-to-right pipeline Raw Data -> SQL Query -> View/Materialized View -> ETL/Curated Table -> BI/Python/R, with decision callouts for rapid iteration, reuse, performance, freshness, governance, and specialized analytics | Learner should notice that logic placement is a trade-off between flexibility, speed, visibility, maintainability, and downstream needs rather than a rule that everything must live in SQL]]

### Keep logic in SQL when

SQL is attractive when:

- the analysis is still changing rapidly;
- you need quick iteration;
- the query runs fast enough;
- the source data is already in the database;
- the result is needed on demand;
- you can modify the logic without waiting for a deployment process.

During exploration, this flexibility is extremely valuable.

A typical workflow is:

```text
profile data
-> write one transformation
-> inspect output
-> discover an exception
-> add another transformation
-> validate
-> repeat
```

### Move logic into ETL when

ETL or a scheduled transformation layer becomes attractive when:

- the query is expensive;
- many people need the same result;
- logic has stabilized;
- repeated computation is wasteful;
- historical snapshots must be preserved;
- data needs stronger governance and review.

A complex transformation can run once in the background and write:

```text
analytics_customer_daily
```

Then downstream users query the prepared table quickly.

### Daily snapshots

Snapshot tables are especially useful when attributes are overwritten in operational systems.

Example:

```text
customer_status today = "Enterprise"
```

does not tell you:

```text
what was the customer's status six months ago?
```

A daily snapshot can preserve:

```text
customer_id
snapshot_date
plan
pipeline_status
lifetime_orders
lifetime_revenue
...
```

This may be expensive to recreate from raw history every time, so materializing it can be worthwhile.

---

## 3. Views and materialized views

A **view** is essentially a saved query that can be referenced like a table.

Example:

```sql
CREATE VIEW analytics_orders AS
SELECT *
FROM orders
WHERE is_test = FALSE;
```

Now analysts can query:

```sql
SELECT *
FROM analytics_orders;
```

without remembering the test-account rule every time.

### Why views are useful

Views can provide:

- reusable definitions;
- simpler interfaces to complex joins;
- consistent filtering;
- controlled access to columns;
- code visibility.

A view can hide PII:

```text
raw customer table:
email
phone
address
plan
country

analytical view:
customer_id
plan
country
```

### Important limitation

A normal view does **not** usually store the result.

When queried, the database still executes the underlying logic.

So:

```text
view != precomputed table
```

A view can improve maintainability without improving a fundamentally expensive computation.

### Materialized views

A materialized view stores the output.

This can improve performance, but now you must decide:

- when it refreshes;
- how stale it may become;
- whether incremental refresh is possible;
- what resources it consumes.

That makes it closer to an ETL-managed analytical table.

---

## 4. When to leave work for BI, Python, or R

The goal is not:

> **Do everything in SQL.**

The goal is:

> **Do each part where it is most appropriate.**

### Spreadsheets

Spreadsheets are flexible and familiar but often struggle with:

- millions of rows;
- repeated manual transformations;
- complex joins;
- reproducibility.

A good pattern is:

```text
database performs heavy filtering/aggregation
-> spreadsheet receives a compact result
```

### BI tools

BI tools differ.

Some:

- cache imported data;
- compute locally;
- support rich calculations.

Others send queries back to the database whenever a report changes.

You need to understand the tool.

For exploratory dashboards, you may deliberately preserve more dimensional detail than a fixed report needs.

### Python and R

For:

- statistics;
- machine learning;
- advanced NLP;
- custom visualization;

Python or R may be better.

But moving raw billions of rows out of the database is often unnecessary.

A strong workflow is frequently:

```text
SQL performs joins, filters, and basic feature creation
-> Python/R receives the analytical grain needed for modeling
```

### Avoid manual steps

A key engineering principle:

> **If a transformation matters, encode it in code.**

Avoid:

```text
export CSV
open spreadsheet
delete two columns
rename values manually
save new CSV
```

Manual steps are:

- hard to reproduce;
- easy to forget;
- difficult to review;
- inconsistent across reruns.

Even a "one-off" analysis often comes back.

---

## 5. Organize SQL for your future self

SQL is permissive about whitespace and capitalization.

The database may accept:

```sql
select customer_id,sum(amount) from orders where status='paid' group by customer_id;
```

But humans benefit from structure:

```sql
SELECT
    customer_id,
    SUM(amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY customer_id;
```

The output is the same.

The maintainability is not.

### Comments

Use single-line comments:

```sql
-- Exclude internal QA accounts
WHERE account_type <> 'test'
```

and block comments:

```sql
/*
The source system called these users "Live"
before the 2025 taxonomy migration.
*/
```

### What deserves a comment

Good candidates include:

- nonobvious business codes;
- strange source-system behavior;
- known data-quality issues;
- important assumptions;
- complicated calculations;
- purpose of a subquery/CTE.

Example:

```sql
WHERE status IN (1, 2)
-- 1 = Active, 2 = Pending
```

Avoid comments that merely repeat obvious syntax.

### Formatting

Useful habits:

- main clauses on new lines;
- consistent indentation;
- one complex expression per line;
- multi-line `CASE` expressions;
- clear aliases;
- aligned nested queries.

The goal is not one universal SQL style.

The goal is **consistent readability**.

### Store analytical code

SQL is text.

Store important queries in version control when practical.

Benefits include:

- backup;
- collaboration;
- review;
- history;
- traceability.

A reusable analytical query is code and should be treated like code.

---

## 6. Understand SQL's logical evaluation order

SQL is written starting with:

```text
SELECT
```

but that is not the first part logically evaluated.

A useful simplified order is:

```text
1. FROM + JOIN + ON
2. WHERE
3. GROUP BY + aggregates
4. HAVING
5. window functions
6. SELECT
7. DISTINCT
8. UNION / UNION ALL
9. ORDER BY
10. LIMIT / OFFSET
```

[[IMAGE_NEEDED: IMG-M01-L08-02 / Instructor Figure — SQL logical evaluation order | Show the 10-stage sequence FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> Window Functions -> SELECT -> DISTINCT -> UNION -> ORDER BY -> LIMIT/OFFSET as a vertical execution pipeline, with a side note that SQL is written in a different order than it is logically evaluated | Learner should notice why aliases or aggregate results are unavailable in some earlier clauses]]

### Why this matters

Suppose you write:

```sql
SELECT
    customer_id,
    SUM(amount) AS revenue
FROM orders
WHERE revenue > 1000
GROUP BY customer_id;
```

This fails in many databases because:

```text
WHERE
```

is evaluated before:

```text
SUM(amount) AS revenue
```

exists.

Correct:

```sql
SELECT
    customer_id,
    SUM(amount) AS revenue
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

### `WHERE` versus `HAVING`

Use:

```text
WHERE
```

to filter rows before aggregation.

Use:

```text
HAVING
```

to filter aggregated groups.

### Aggregates inside window functions

Because grouped aggregates are logically available before window functions, patterns like this are possible:

```sql
SELECT
    state,
    COUNT(*) AS terms,
    RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS state_rank
FROM terms
GROUP BY state;
```

### `DISTINCT` happens late

`DISTINCT` removes duplicate output rows after `SELECT` expressions are produced.

It should not be used as a substitute for understanding why a join created duplicates.

### `LIMIT` does not necessarily save database work

Because `LIMIT` is logically late, the database may still need to calculate a large result before returning only a few rows.

It is useful for:

- inspection;
- reducing transfer to your client.

It is not automatically a performance fix.

---

## 7. Subqueries: isolate one calculation before another

A subquery creates an intermediate result.

Example:

```sql
SELECT
    customer_id,
    revenue
FROM (
    SELECT
        customer_id,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY customer_id
) customer_revenue
WHERE revenue > 1000;
```

The inner query creates:

```text
one row per customer
```

The outer query filters that result.

### Why subqueries help

They are useful when:

- a later calculation depends on an earlier aggregation;
- you want to change grain;
- you want to isolate one logical step;
- a long expression would otherwise be repeated.

### Nested subqueries can become difficult

This:

```text
query
  -> subquery
      -> subquery
          -> subquery
```

may work correctly but become hard to reason about.

That is when CTEs or temporary tables may improve clarity.

### Lateral subqueries

A lateral subquery can reference rows produced earlier in the `FROM` clause.

This is useful for certain per-row dependent calculations.

Conceptually:

```text
for each row in A
run a small dependent query B
```

But lateral syntax is less widely familiar.

Use it when it genuinely improves the solution, not simply because it is advanced syntax.

---

## 8. Temporary tables: materialize an intermediate result for the session

A temporary table persists only for the current database session.

Typical syntax:

```sql
CREATE TEMPORARY TABLE temp_active_users AS
SELECT
    user_id
FROM users
WHERE last_seen >= CURRENT_DATE - INTERVAL '30 days';
```

Then:

```sql
SELECT ...
FROM temp_active_users a
JOIN ...
```

### Temp tables are useful when

- the intermediate result will be reused several times;
- the source table is huge but the relevant subset is small;
- materializing the intermediate result improves performance;
- you want to inspect intermediate output repeatedly.

### Benefits

Unlike copying the same subquery multiple times:

```text
compute once
reuse many times
```

### Drawbacks

Temp tables may require:

- write permissions;
- multiple SQL statements;
- session state.

Some BI tools accept only one SQL statement, which makes temp tables awkward or impossible in that environment.

---

## 9. Common table expressions: name the stages of your query

A common table expression uses:

```text
WITH
```

to define named intermediate results.

Example:

```sql
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    revenue
FROM customer_revenue
WHERE revenue > 1000;
```

### Multiple CTEs

```sql
WITH first_order AS (
    ...
),
customer_revenue AS (
    ...
),
customer_status AS (
    ...
)
SELECT ...
```

This can make a complex query read like a pipeline.

### CTEs are useful for

- separating logical stages;
- avoiding repeated query text;
- giving intermediate calculations meaningful names;
- organizing complex transformations.

### Do not assume CTE = faster

Optimizer behavior differs by database and version.

Use CTEs primarily for:

```text
clarity
reuse
logical decomposition
```

and measure performance when it matters.

### Subquery vs temp table vs CTE

A practical comparison:

| Tool | Best fit |
|---|---|
| Subquery | Small intermediate calculation used once |
| CTE | Named logical stages within one query |
| Temp table | Intermediate result reused across several statements or worth materializing |
| ETL table | Stable shared result needed repeatedly across sessions/users |

The correct choice depends on readability, reuse, permissions, and performance.

{{exercise:M01.L08.EX01}}

---

## 10. Multi-level aggregation with `GROUPING SETS`, `CUBE`, and `ROLLUP`

Suppose you need sales totals by:

```text
platform
genre
publisher
```

You could write:

```sql
SELECT platform, NULL AS genre, NULL AS publisher, SUM(sales)
FROM games
GROUP BY platform

UNION ALL

SELECT NULL, genre, NULL, SUM(sales)
FROM games
GROUP BY genre

UNION ALL

SELECT NULL, NULL, publisher, SUM(sales)
FROM games
GROUP BY publisher;
```

This works, but becomes long.

### `GROUPING SETS`

Many databases support:

```sql
SELECT
    platform,
    genre,
    publisher,
    SUM(sales) AS sales
FROM games
GROUP BY GROUPING SETS (
    (platform),
    (genre),
    (publisher)
);
```

You can include a grand total:

```sql
GROUP BY GROUPING SETS (
    (),
    (platform),
    (genre),
    (publisher)
)
```

### `CUBE`

`CUBE` produces all combinations of the listed dimensions.

```sql
GROUP BY CUBE (
    platform,
    genre,
    publisher
)
```

This can produce:

```text
grand total
platform
genre
publisher
platform + genre
platform + publisher
genre + publisher
platform + genre + publisher
```

### `ROLLUP`

`ROLLUP` follows hierarchy order.

```sql
GROUP BY ROLLUP (
    platform,
    genre,
    publisher
)
```

produces levels such as:

```text
platform + genre + publisher
platform + genre
platform
grand total
```

but not every arbitrary combination.

### When these tools help

They are useful for:

- dashboards;
- hierarchical reports;
- precomputed filter combinations;
- multi-level summary tables.

They can replace huge repeated `UNION` blocks and reduce repeated scans of the same source data.

---

## 11. Control the size of analytical data sets

A query can be logically correct and still produce an impractical result.

Large outputs create problems for:

- BI tools;
- network transfer;
- spreadsheets;
- local machines;
- model training workflows;
- storage.

You can reduce size in several ways:

```text
sampling
coarser date grain
fewer dimensions
category consolidation
flags / bins
shorter time window
```

The key is to reduce size without removing information needed for the decision.

---

## 12. Sampling: choose both the percentage and the entity

Suppose you have:

```text
1 billion pageview rows
```

and need only a representative development sample.

A numeric identifier can be sampled with modulo:

```sql
WHERE user_id % 100 = 7
```

This selects approximately 1% if the IDs are sufficiently well distributed.

For 10%:

```sql
WHERE user_id % 10 = 7
```

For 0.1%:

```sql
WHERE user_id % 1000 = 7
```

### Sample the right entity

This matters enormously.

If the question is:

```text
How do users navigate the site?
```

do not sample:

```text
1% of pageviews
```

because that may keep random fragments from many users.

Instead sample:

```text
1% of users
```

and preserve all their pageviews.

This maintains the behavioral sequence.

### Alphanumeric IDs

You can sometimes sample on characters:

```sql
WHERE RIGHT(user_id, 1) = 'b'
```

But this is only reasonable if suffix characters are approximately well distributed.

### Validate the sample

Do not assume an ID-based method is random.

Compare sample and population on important attributes:

```text
country
device
plan
activity level
signup year
```

ID generation systems can embed structure.

A sample can be reproducible and still biased.

---

## 13. Reduce dimensionality without destroying useful signal

Each additional grouping dimension can multiply the number of output rows.

Suppose:

```text
field A has 10 values
field B has 10 values
field C has 10 values
```

Maximum combinations:

```text
10 × 10 × 10 = 1000
```

Add more dimensions and result size can grow quickly.

### Reduce time granularity

Ask whether you really need:

```text
hourly
```

or whether:

```text
daily
weekly
monthly
```

is sufficient.

A useful compromise might be:

```text
monthly history for 5 years
+ daily detail for the last 90 days
```

### Standardize text categories

These:

```text
Cairo
cairo
 Cairo
CAIRO
```

can create unnecessary dimensionality.

Use:

```text
TRIM
LOWER
INITCAP
CASE
REPLACE
```

as appropriate.

### Group the long tail into "Other"

Suppose a report has 200 countries but 90% of activity comes from 8.

You might preserve the top countries and group the rest:

```sql
CASE
    WHEN country IN (
        'Egypt',
        'Saudi Arabia',
        'UAE',
        'Jordan'
    ) THEN country
    ELSE 'Other'
END
```

### Dynamic top-N categories

Instead of hard-coding, rank categories:

```sql
WITH ranked AS (
    SELECT
        country,
        COUNT(*) AS users,
        RANK() OVER (
            ORDER BY COUNT(*) DESC
        ) AS country_rank
    FROM customers
    GROUP BY country
)
...
```

Then preserve:

```text
top 10
```

and collapse the rest.

### Convert detail into flags or bands

Instead of exact:

```text
orders = 0,1,2,3,4,5,6,...
```

you may only need:

```text
has_2_plus_orders
```

or:

```text
1
2–9
10+
```

The correct transformation depends on what stakeholders need to distinguish.

---

## 14. PII and data privacy

Analytical usefulness does not justify unnecessary exposure of personal information.

Personally identifiable information can include obvious fields such as:

- name;
- email;
- home address;
- phone number;
- government identifiers.

It can also include sensitive or identifying combinations involving:

- precise location;
- health data;
- birth date;
- financial information.

### Best rule: do not output PII unless you need it

If the analysis only needs:

```text
customers by country and plan
```

do not export:

```text
email
phone
address
```

"Maybe useful later" is not a strong reason to proliferate sensitive fields.

### Aggregation helps—but small groups can still identify people

This:

```text
country
plan
age
rare_job_title
customers = 1
```

may effectively identify a person even without their name.

Consider minimum group-size policies where appropriate.

### Pseudonymous identifiers

If downstream analysis needs stable identity but not direct contact information, use an approved pseudonymous ID.

The source chapter discusses techniques such as row numbering and hashing.

However:

> Hashing is not the same as encryption.

A simple hash of predictable inputs such as email addresses can be vulnerable to guessing or lookup attacks.

For sensitive real systems, follow organizational privacy/security standards and use approved pseudonymization or encryption methods.

### Work with specialists

Privacy laws and organizational requirements evolve.

Coordinate with:

- security;
- privacy;
- legal;
- data engineering;
- database administration.

The analytical principle is stable:

> **Minimize sensitive data exposure while retaining only what the analysis genuinely requires.**

{{exercise:M01.L08.EX02}}

---

## 15. From data-set engineering to applied analysis

Once the data is organized, performant, appropriately sized, and privacy-aware, the next question is:

> **What business analysis do we perform with it?**

The final source chapter demonstrates three useful patterns:

1. funnel analysis;
2. churn/lapse analysis;
3. basket analysis.

These are valuable because they combine techniques from nearly every earlier lesson.

---

## 16. Funnel analysis

A funnel is a series of actions leading to a goal.

Examples:

### Ecommerce

```text
View product
-> Add to cart
-> Enter shipping
-> Submit payment
-> Purchase
```

### Learning platform

```text
Enroll
-> Start lesson
-> Finish module
-> Complete project
-> Finish course
-> Earn certificate
```

### SaaS

```text
Sign up
-> Create workspace
-> Complete first workflow
-> Invite teammate
-> Upgrade
```

Funnel analysis identifies where entities disappear from the process.

[[IMAGE_NEEDED: IMG-M01-L08-03 / Instructor Figure — Funnel analysis with overall and step conversion | Show an eligible population flowing through four narrowing stages toward a final goal; label both overall conversion from the top and step-to-step conversion between adjacent stages, and highlight one large drop as the main friction point | Learner should notice that a funnel requires a clearly defined starting population and that different conversion denominators answer different questions]]

### Begin with the eligible population

Ask:

```text
Who genuinely had the opportunity to start?
```

Possible denominators:

```text
all site visitors
all checkout starters
all users exposed to a feature
all enrolled learners
```

These are not interchangeable.

### Sequential required-step funnel

If every step is required:

```sql
FROM eligible a
LEFT JOIN step_one b
    ON a.user_id = b.user_id
LEFT JOIN step_two c
    ON b.user_id = c.user_id
LEFT JOIN step_three d
    ON c.user_id = d.user_id
```

This enforces the chain.

### Skippable-step funnel

If users may skip a stage:

```sql
FROM eligible a
LEFT JOIN step_one b
    ON a.user_id = b.user_id
LEFT JOIN step_two c
    ON a.user_id = c.user_id
LEFT JOIN step_three d
    ON a.user_id = d.user_id
```

Each event is evaluated relative to the base population.

### Overall conversion

```text
step users / eligible users
```

### Step-to-step conversion

```text
current step / previous step
```

Both are useful.

Overall conversion tells you how much of the starting population remains.

Step conversion tells you where friction is concentrated.

### Time-box the funnel when needed

Example:

```text
purchase within 7 days of checkout start
```

Without a time box, an old user returning months later may be counted as part of the original funnel episode.

### Segment funnels

Compare by:

- device;
- country;
- plan;
- acquisition cohort;
- traffic source;
- experiment variant.

Large differences generate better hypotheses than one overall number.

{{exercise:M01.L08.EX03}}

---

## 17. Define churn from actual usage behavior

Churn is the opposite of retention, but its exact meaning depends on the product.

Some systems have explicit departure:

```text
subscription canceled
contract ended
account closed
```

Others do not.

A customer simply stops appearing.

### Avoid arbitrary churn thresholds

Do not choose:

```text
30 inactive days
```

simply because another company does.

A grocery-delivery app and a travel-booking platform have very different natural usage frequencies.

Instead analyze **historical gaps** between actions.

### Gap analysis with `lag`

```sql
WITH event_gaps AS (
    SELECT
        customer_id,
        event_date,
        LAG(event_date) OVER (
            PARTITION BY customer_id
            ORDER BY event_date
        ) AS previous_event
    FROM customer_events
)
SELECT
    event_date - previous_event AS gap,
    COUNT(*) AS instances
FROM event_gaps
WHERE previous_event IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

This tells you how long customers normally disappear before returning.

### Use the distribution

Suppose the observed pattern is:

```text
most customers return within 7 days
90% return within 21 days
97% return within 45 days
almost nobody returns after 90 days
```

A defensible status definition might be:

```text
Active  = 0–21 days
Lapsed  = 22–45 days
Churned = 46+ days
```

The exact threshold is a business decision informed by data.

[[IMAGE_NEEDED: IMG-M01-L08-04 / Instructor Figure — From gap distribution to Active/Lapsed/Churned thresholds | Show a historical distribution of return gaps above a horizontal time-since-last timeline; mark two chosen threshold lines dividing Active, Lapsed, and Churned, and show that thresholds are selected after inspecting actual return behavior | Learner should notice that inactivity states should be derived from product behavior rather than copied from an arbitrary universal rule]]

### Time since last

Find each user's latest activity:

```sql
WITH latest AS (
    SELECT
        customer_id,
        MAX(event_date) AS last_event
    FROM customer_events
    GROUP BY customer_id
)
SELECT
    customer_id,
    CURRENT_DATE - last_event AS days_since_last
FROM latest;
```

For historical datasets, use the dataset's final date rather than the real current date.

### Classify status

```sql
CASE
    WHEN days_since_last <= 21 THEN 'Active'
    WHEN days_since_last <= 45 THEN 'Lapsed'
    ELSE 'Churned'
END
```

### Why "Lapsed" is useful

A lapsed customer is not fully healthy but is still plausibly recoverable.

That group can become the target of:

- reminder campaigns;
- personalized outreach;
- reactivation discounts;
- support intervention.

Then experimentation can test whether the intervention actually improves return behavior.

---

## 18. Basket analysis

Basket analysis asks:

> **Which items occur together?**

The "items" do not have to be physical products.

They can be:

- services;
- courses;
- product features;
- travel components;
- content categories;
- software tools.

### Define the basket grain

Possible basket definitions:

```text
one order
one customer lifetime
one session
one day
one subscription
```

The business question determines the grain.

### Whole-basket aggregation

For relatively small baskets:

```sql
SELECT
    customer_id,
    STRING_AGG(
        product,
        ', ' ORDER BY product
    ) AS products
FROM purchases
GROUP BY customer_id;
```

Then count recurring complete baskets.

Ordering ensures:

```text
Milk, Bread
```

and:

```text
Bread, Milk
```

receive the same representation.

### Product pairs with a self-join

```sql
SELECT
    a.customer_id,
    a.product AS product_1,
    b.product AS product_2
FROM purchases a
JOIN purchases b
    ON a.customer_id = b.customer_id
   AND b.product > a.product;
```

The inequality prevents:

```text
A + A
```

and keeps only one of:

```text
A + B
B + A
```

[[IMAGE_NEEDED: IMG-M01-L08-05 / Instructor Figure — Basket-analysis self-join | Show a three-item basket such as SQL Course, Power BI Course, Statistics Course duplicated into table A and table B; draw only the valid A<B pair connections and show the three resulting unique pairs, with self-pairs and reverse pairs crossed out | Learner should notice how the inequality condition generates unique unordered pairs]]

Then aggregate:

```sql
WITH pairs AS (
    SELECT
        a.customer_id,
        a.product AS product_1,
        b.product AS product_2
    FROM purchases a
    JOIN purchases b
        ON a.customer_id = b.customer_id
       AND b.product > a.product
)
SELECT
    product_1,
    product_2,
    COUNT(DISTINCT customer_id) AS customers
FROM pairs
GROUP BY product_1, product_2
ORDER BY customers DESC;
```

---

## 19. Basket-analysis pitfalls

Basket analysis looks simple but contains important traps.

### Performance

A basket with `n` unique items contains:

```text
n × (n - 1) / 2
```

pairs.

For 100 items:

```text
100 × 99 / 2 = 4,950 pairs
```

Large baskets across millions of users can explode in size.

Possible mitigations:

- filter to a time window;
- remove extremely rare items;
- analyze one category;
- preaggregate unique user-item membership;
- restrict to relevant products.

### Dominant items

If nearly everyone buys:

```text
milk
```

then milk may appear in almost every top pair.

That does not automatically mean:

```text
milk + X
```

is a uniquely strong relationship.

Always consider individual item frequency.

More advanced association analysis may use concepts such as:

- support;
- confidence;
- lift.

But simple SQL pair counts are still a valuable exploratory starting point.

### Self-fulfilling recommendations

Suppose:

```text
A and B frequently co-occur
```

so the product starts recommending B after A.

Now A and B will co-occur more often partly **because of the recommendation**.

Future observational data then reinforces the original rule.

This is a feedback loop.

The solution is not to abandon basket analysis.

It is to validate recommendation value with experimentation.

---

## 20. Combine the whole course into analytical workflows

The most important final skill is integration.

### Example: improve course completion

Suppose a learning platform sees declining completion.

#### Step 1 — Build a reliable analytical dataset

Use Chapter 8 ideas:

```text
clean event model
stable learner grain
documented SQL
CTEs
daily snapshots if needed
privacy-safe IDs
```

#### Step 2 — Funnel analysis

```text
Enroll
-> Start
-> Complete Module 1
-> Complete Project
-> Finish Course
```

Find the largest drop.

#### Step 3 — Time-series analysis

Ask:

```text
When did the drop begin?
```

#### Step 4 — Cohort analysis

Ask:

```text
Did recent enrollment cohorts behave differently?
```

#### Step 5 — Anomaly detection

Ask:

```text
Was there a sudden instrumentation or platform anomaly?
```

#### Step 6 — Text analysis

Analyze:

```text
support tickets
learner feedback
exercise-error notes
```

for recurring friction themes.

#### Step 7 — Churn/lapse analysis

Identify learners at risk before they disappear completely.

#### Step 8 — Basket analysis

Find:

```text
which courses learners commonly take together
```

to inform next-course suggestions.

#### Step 9 — Experiment

Test:

```text
new onboarding
new reminder cadence
new project guidance
course recommendation
```

The chapters are not separate islands.

They form one analytical toolbox.

---

## 21. A production-ready analytical SQL checklist

Before handing off a complex analytical data set, verify the following.

### Grain

Can you complete this sentence?

```text
One row represents one ________.
```

If not, the dataset is not ready.

### Join cardinality

For every join, do you know whether it is:

```text
one-to-one
one-to-many
many-to-one
many-to-many
```

Unexpected many-to-many joins are a common source of inflated metrics.

### Filters

Are business exclusions documented?

Examples:

```text
test users
internal accounts
refunded transactions
invalid sensor rows
```

### Null semantics

Does null mean:

```text
missing
not applicable
not yet observed
zero
```

Do not collapse these meanings accidentally.

### Time logic

Are:

```text
time zones
observation windows
cohort dates
snapshot dates
```

defined consistently?

### Reproducibility

Can another analyst rerun the work without manual spreadsheet edits?

### Performance

Is the query fast enough for its intended use?

If not, consider:

- materialization;
- ETL;
- a materialized view;
- smaller source subsets;
- preaggregation.

### Privacy

Does the output contain only the minimum sensitive data required?

### Validation

Have you checked:

- row counts;
- duplicate keys;
- unexpected nulls;
- min/max;
- category frequencies;
- sample records;
- totals against a trusted source?

### Documentation

Does the code explain the nonobvious parts?

---

## 22. Continue learning through real problems

The final source chapter emphasizes practice on real data.

That is the right way to continue.

### Technical skill is only one part

Strong analysis combines:

```text
SQL skill
+ domain knowledge
+ curiosity
+ statistical judgment
+ communication
```

A technically perfect query can answer the wrong question.

A simple query can be extremely valuable if it answers the right one.

### Useful practice loop

```text
1. Choose a real question.
2. Define the entity and grain.
3. Profile the data.
4. Build the smallest correct query.
5. Validate assumptions.
6. Expand only as needed.
7. Interpret with domain context.
8. Communicate the decision implication.
```

### Useful sources of practice data

The source chapter points learners toward:

- public datasets;
- journalism datasets;
- development indicators;
- government open-data portals;
- competition/dataset platforms;
- organizational data when available.

The exact source matters less than working on questions that force you to reason about imperfect real data.

### Communicate decisions, not only metrics

Weak conclusion:

```text
Conversion fell from 44.1% to 39.8%.
```

Better conclusion:

```text
The decline is concentrated between payment submission and confirmation,
started immediately after the mobile payment change, and does not appear
on desktop. The payment step should be investigated first, and any fix
should be validated with an experiment.
```

SQL produces evidence.

Analysis turns that evidence into action.

---

## Important misconceptions

### Misconception 1

> Complex analytical logic should always stay in SQL.

No. Stable expensive logic may belong in ETL or materialized tables, while specialized modeling may belong downstream.

### Misconception 2

> A view automatically makes an expensive query fast.

A standard view usually stores query logic, not the output.

### Misconception 3

> CTEs are always faster than subqueries.

Performance depends on the database optimizer. CTEs are often chosen for clarity and reuse.

### Misconception 4

> `LIMIT 100` means the database only processes 100 rows.

Not necessarily. `LIMIT` is logically late and may only reduce what is returned.

### Misconception 5

> A 1% modulo sample is automatically unbiased.

Only if the sampled identifier is sufficiently well distributed relative to the variables of interest.

### Misconception 6

> Hashed PII is automatically secure.

Hashing is not equivalent to encryption, and predictable inputs may still be vulnerable.

### Misconception 7

> Funnel conversion should always use the previous step as denominator.

Not when steps are optional or independently reachable.

### Misconception 8

> Churn always means 30 days without activity.

The threshold should reflect actual product behavior and business context.

### Misconception 9

> The most frequent basket pair is automatically the best recommendation.

A very common item can dominate pair counts without a special association.

### Misconception 10

> More complicated SQL means better analysis.

The best analysis uses the simplest reliable method that represents the process correctly and supports the decision.

---

## Key terminology

| Term | Meaning |
|---|---|
| Analytical data set | Data shaped for repeated analysis or downstream tools |
| ETL | Extract-transform-load process that materializes transformed data |
| View | Saved query exposed like a table |
| Materialized view | View-like object that stores query results |
| Snapshot table | Table capturing entity state at repeated points in time |
| Query evaluation order | Logical sequence in which SQL clauses are resolved |
| Subquery | Query nested inside another query |
| Lateral subquery | Subquery that can reference earlier FROM items |
| Temporary table | Session-scoped materialized table |
| CTE | Named intermediate result defined with `WITH` |
| `GROUPING SETS` | Syntax for several explicit aggregation groupings |
| `CUBE` | Produces all combinations of listed grouping dimensions |
| `ROLLUP` | Produces hierarchical aggregation levels |
| Sampling | Selecting a subset of observations |
| Dimensionality | Number and combination of attribute values represented |
| PII | Personally identifiable information |
| Pseudonymization | Replacing direct identifiers with indirect stable identifiers |
| Funnel | Sequence of actions leading toward a goal |
| Eligible population | Entities with an opportunity to enter the funnel |
| Step conversion | Share moving from one funnel stage to the next |
| Churn | Operational definition of departure/inactivity |
| Lapsed | Intermediate inactivity state before churn |
| Gap analysis | Analysis of elapsed time between events |
| Time since last | Elapsed time since most recent activity |
| Basket analysis | Analysis of items or behaviors that occur together |
| Self-join | Joining a table to itself |
| Dominant item | Very common item that can overwhelm basket-pair counts |

---

## Self-check

Before completing the course, make sure you can answer:

1. When should transformation logic remain in SQL?
2. When is ETL preferable?
3. What is the difference between a view and a materialized view?
4. Why should manual transformation steps be avoided?
5. What is the logical evaluation order of `FROM`, `WHERE`, `GROUP BY`, `HAVING`, window functions, and `SELECT`?
6. Why can `HAVING` filter aggregate values when `WHERE` cannot?
7. When is a subquery a good choice?
8. When is a temp table preferable?
9. Why might a CTE improve maintainability?
10. What problem do `GROUPING SETS`, `CUBE`, and `ROLLUP` solve?
11. Why should sampling often happen at user level rather than event level?
12. How would you validate that an ID-based sample is not biased?
13. How can category grouping reduce dimensionality?
14. Why should PII be removed from analytical outputs whenever possible?
15. Why is hashing not the same as encryption?
16. What defines the top of a funnel?
17. When should funnel steps be joined sequentially?
18. What is the difference between overall and step conversion?
19. Why should churn thresholds be informed by historical gaps?
20. What is the purpose of a Lapsed state?
21. How does `b.product > a.product` help in a basket self-join?
22. Why can common products dominate basket-analysis results?
23. How can experiments improve recommendation systems built from basket analysis?
24. What does it mean to define the analytical grain?
25. Why is communication part of analytical correctness?

---

## Retain this idea

**Production-quality SQL analysis is not only about writing a correct query. It is about choosing the right grain, putting logic in the right layer, organizing it so others can maintain it, controlling performance and privacy, validating assumptions, and then combining SQL techniques to answer real questions such as where users drop out, when customers are truly inactive, and which behaviors occur together.**
""",

        "estimated_minutes": 360,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "complex-dataset-goal", "title": "From one-off query to reusable analytical data set", "order": 1},
            {"id": "where-logic-lives", "title": "Decide where the logic should live", "order": 2},
            {"id": "views", "title": "Views and materialized views", "order": 3},
            {"id": "downstream-tools", "title": "When to leave work for BI, Python, or R", "order": 4},
            {"id": "organize-code", "title": "Organize SQL for your future self", "order": 5},
            {"id": "evaluation-order", "title": "Understand SQL's logical evaluation order", "order": 6},
            {"id": "subqueries", "title": "Subqueries: isolate one calculation before another", "order": 7},
            {"id": "temp-tables", "title": "Temporary tables: materialize an intermediate result for the session", "order": 8},
            {"id": "ctes", "title": "Common table expressions: name the stages of your query", "order": 9},
            {"id": "grouping-sets", "title": "Multi-level aggregation with GROUPING SETS, CUBE, and ROLLUP", "order": 10},
            {"id": "dataset-size", "title": "Control the size of analytical data sets", "order": 11},
            {"id": "sampling", "title": "Sampling: choose both the percentage and the entity", "order": 12},
            {"id": "reduce-dimensionality", "title": "Reduce dimensionality without destroying useful signal", "order": 13},
            {"id": "privacy", "title": "PII and data privacy", "order": 14},
            {"id": "capstone-transition", "title": "From data-set engineering to applied analysis", "order": 15},
            {"id": "funnel", "title": "Funnel analysis", "order": 16},
            {"id": "churn", "title": "Define churn from actual usage behavior", "order": 17},
            {"id": "basket", "title": "Basket analysis", "order": 18},
            {"id": "basket-pitfalls", "title": "Basket-analysis pitfalls", "order": 19},
            {"id": "integrated-workflows", "title": "Combine the whole course into analytical workflows", "order": 20},
            {"id": "production-checklist", "title": "A production-ready analytical SQL checklist", "order": 21},
            {"id": "continue-learning", "title": "Continue learning through real problems", "order": 22},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L08.EX01",

            "title": "Refactor a Complex Analytics Query",

            "lesson_code": "M01.L08",

            "section_id": "ctes",

            "placement": "after_section",

            "description": (
                "Choose a maintainable structure for a query that combines several "
                "intermediate calculations."
            ),

            "instructions": (
                "You need a reusable customer data set containing first order date, "
                "lifetime revenue, last activity date, and current plan.\n"
                "1. Define the final row grain.\n"
                "2. Describe separate intermediate calculations for each metric.\n"
                "3. Organize them as CTEs or explain why a temp table would be preferable.\n"
                "4. Join the intermediate results into one final customer-level data set.\n"
                "5. Add comments for at least two nonobvious assumptions.\n"
                "6. Explain when you would move this logic into ETL."
            ),

            "expected_output": (
                "A clearly structured SQL design or pseudocode plus a short architecture "
                "decision explaining the chosen intermediate-result strategy."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "ctes",
                "analytical-grain",
                "query-organization",
                "etl-decision",
            ],
        },

        {
            "id": "M01.L08.EX02",

            "title": "Shrink and Privacy-Harden a Dashboard Dataset",

            "lesson_code": "M01.L08",

            "section_id": "privacy",

            "placement": "after_section",

            "description": (
                "Reduce data-set size while protecting sensitive information and preserving "
                "the analysis questions stakeholders need."
            ),

            "instructions": (
                "A dashboard extract contains user_id, email, GPS coordinates, event_time, "
                "country, device, plan, exact order_count, and revenue for 50 million users.\n"
                "Stakeholders need monthly trends by country, device, and plan.\n"
                "1. Identify which fields should not be included in the dashboard output.\n"
                "2. Change the time grain appropriately.\n"
                "3. Decide whether exact order_count is needed or whether a band/flag is enough.\n"
                "4. Explain whether sampling is appropriate for this dashboard.\n"
                "5. Describe how you would validate privacy risks from very small groups.\n"
                "6. State whether a view, materialized view, or ETL table would be a reasonable delivery layer."
            ),

            "expected_output": (
                "A proposed output schema and transformation plan that reduces size, "
                "protects PII, and preserves the dashboard's required analytical detail."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "dimensionality",
                "pii",
                "aggregation",
                "data-architecture",
            ],
        },

        {
            "id": "M01.L08.EX03",

            "title": "Build and Diagnose a Learning Funnel",

            "lesson_code": "M01.L08",

            "section_id": "funnel",

            "placement": "after_section",

            "description": (
                "Apply funnel analysis to a learning product and connect the result to "
                "other course techniques."
            ),

            "instructions": (
                "A learning platform tracks `enrolled`, `lesson_started`, `module_completed`, "
                "`project_submitted`, and `course_completed` events.\n"
                "1. Define the eligible population.\n"
                "2. Calculate the number and percentage reaching each stage.\n"
                "3. Calculate step-to-step conversion.\n"
                "4. Add a 30-day time box from enrollment.\n"
                "5. Compare the funnel by mobile versus desktop.\n"
                "6. If one stage suddenly worsened last week, explain how time-series and "
                "anomaly analysis would help investigate.\n"
                "7. Propose one experiment to improve the weakest stage."
            ),

            "expected_output": (
                "SQL or pseudocode for the funnel and a short multi-technique analysis plan."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "funnel-analysis",
                "conversion",
                "time-boxing",
                "integrated-analysis",
            ],
        },

        {
            "id": "M01.L08.EX04",

            "title": "Create a Churn and Reactivation Model",

            "lesson_code": "M01.L08",

            "section_id": "churn",

            "placement": "after_section",

            "description": (
                "Use historical activity gaps to build operational Active, Lapsed, and "
                "Churned states."
            ),

            "instructions": (
                "You have `activity(user_id, activity_date)`.\n"
                "1. Use `lag` to calculate historical gaps per user.\n"
                "2. Build a gap distribution.\n"
                "3. Propose two inactivity thresholds based on the observed distribution.\n"
                "4. Calculate each user's latest activity.\n"
                "5. Calculate days since last activity.\n"
                "6. Assign Active, Lapsed, and Churned status.\n"
                "7. Explain how you would test a reactivation campaign for Lapsed users."
            ),

            "expected_output": (
                "A gap-analysis query, status-classification logic, and an experiment "
                "proposal for evaluating reactivation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "gap-analysis",
                "lag",
                "churn",
                "experimentation",
            ],
        },

        {
            "id": "M01.L08.EX05",

            "title": "Find and Validate Course Recommendations",

            "lesson_code": "M01.L08",

            "section_id": "basket-pitfalls",

            "placement": "after_section",

            "description": (
                "Use basket-analysis SQL to generate course-pair candidates and design "
                "a more trustworthy recommendation evaluation."
            ),

            "instructions": (
                "Assume `course_enrollments(user_id, course_id)`.\n"
                "1. Self-join the table to create unique unordered course pairs.\n"
                "2. Count distinct users for each pair.\n"
                "3. Explain why a very popular foundation course may dominate the results.\n"
                "4. Propose one filtering or normalization step before choosing recommendations.\n"
                "5. Explain the self-fulfilling recommendation risk.\n"
                "6. Design an A/B test to determine whether showing a recommended course "
                "causes incremental enrollment."
            ),

            "expected_output": (
                "SQL or pseudocode for pair generation and a concise experimental "
                "validation plan."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "basket-analysis",
                "self-joins",
                "frequency-analysis",
                "experimentation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L08.QZ01",

        "title": "Complex Analytical Data Sets & Applied SQL Patterns — Knowledge Check",

        "lesson_code": "M01.L08",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L08.Q01",

                "section_id": "where-logic-lives",

                "question": (
                    "When is moving stable logic into ETL especially attractive?"
                ),

                "options": [
                    "When the query is still changing every hour",
                    "When the result is expensive to calculate repeatedly and widely reused",
                    "When no one else needs the result",
                    "Whenever the query contains a WHERE clause",
                ],

                "correct": 1,

                "explanation": (
                    "ETL is often valuable for stable, expensive, reusable transformations "
                    "that benefit from being materialized and governed."
                ),
            },

            {
                "id": "M01.L08.Q02",

                "section_id": "views",

                "question": (
                    "What is the key difference between a normal view and a materialized view?"
                ),

                "options": [
                    "A normal view stores data while a materialized view stores only SQL",
                    "A materialized view stores query results, while a normal view usually stores only the query definition",
                    "Views cannot contain joins",
                    "Materialized views cannot be refreshed",
                ],

                "correct": 1,

                "explanation": (
                    "A materialized view persists the result set, while a normal view "
                    "generally executes its underlying query when read."
                ),
            },

            {
                "id": "M01.L08.Q03",

                "section_id": "evaluation-order",

                "question": (
                    "Why can `HAVING SUM(amount) > 1000` work when `WHERE SUM(amount) > 1000` does not?"
                ),

                "options": [
                    "HAVING is evaluated after GROUP BY and aggregation",
                    "WHERE is only for strings",
                    "HAVING runs before FROM",
                    "SUM can only appear in HAVING",
                ],

                "correct": 0,

                "explanation": (
                    "WHERE is applied before aggregation, while HAVING can filter the "
                    "grouped aggregate results."
                ),
            },

            {
                "id": "M01.L08.Q04",

                "section_id": "ctes",

                "question": (
                    "Which statement about CTEs is most accurate?"
                ),

                "options": [
                    "They are always faster than every equivalent subquery",
                    "They are useful for naming and organizing intermediate query stages",
                    "They persist across database sessions",
                    "They require write permissions",
                ],

                "correct": 1,

                "explanation": (
                    "CTEs are especially valuable for logical decomposition and reuse within "
                    "one statement; performance depends on the database."
                ),
            },

            {
                "id": "M01.L08.Q05",

                "section_id": "grouping-sets",

                "question": (
                    "What is `CUBE` useful for?"
                ),

                "options": [
                    "Returning all combinations of aggregation dimensions",
                    "Sampling user IDs",
                    "Hashing PII",
                    "Creating temporary tables",
                ],

                "correct": 0,

                "explanation": (
                    "`CUBE` produces aggregation results for all combinations of the listed "
                    "grouping dimensions."
                ),
            },

            {
                "id": "M01.L08.Q06",

                "section_id": "sampling",

                "question": (
                    "If you want to study complete navigation journeys, why is sampling users usually better than sampling pageview rows?"
                ),

                "options": [
                    "It preserves all events for the selected users",
                    "Pageviews cannot be sampled",
                    "User sampling guarantees no bias",
                    "Modulo works only on users",
                ],

                "correct": 0,

                "explanation": (
                    "Sampling at the entity level preserves the behavioral sequences needed "
                    "to study journeys."
                ),
            },

            {
                "id": "M01.L08.Q07",

                "section_id": "privacy",

                "question": (
                    "Which privacy practice is generally strongest for analytical outputs?"
                ),

                "options": [
                    "Include all PII and delete it later",
                    "Avoid including PII at all when the analysis does not require it",
                    "Assume hashed email is fully encrypted",
                    "Share detailed data because analysts are internal",
                ],

                "correct": 1,

                "explanation": (
                    "Data minimization reduces privacy exposure by preventing unnecessary "
                    "sensitive information from propagating downstream."
                ),
            },

            {
                "id": "M01.L08.Q08",

                "section_id": "funnel",

                "question": (
                    "If a funnel step can be skipped, how should later steps usually be joined for an independent completion view?"
                ),

                "options": [
                    "Only through the skipped step",
                    "Back to the eligible base population",
                    "With a CROSS JOIN",
                    "Only to churned users",
                ],

                "correct": 1,

                "explanation": (
                    "Independent joins to the base population avoid enforcing a sequence "
                    "that the real process does not require."
                ),
            },

            {
                "id": "M01.L08.Q09",

                "section_id": "churn",

                "question": (
                    "Why should historical gap distributions inform churn definitions?"
                ),

                "options": [
                    "They show the natural cadence with which entities return",
                    "They guarantee the exact future churn date",
                    "They eliminate the need for business judgment",
                    "They convert churn into a basket problem",
                ],

                "correct": 0,

                "explanation": (
                    "Observed historical gaps help distinguish normal inactivity from "
                    "inactivity long enough to be operationally concerning."
                ),
            },

            {
                "id": "M01.L08.Q10",

                "section_id": "basket",

                "question": (
                    "Why use `b.product > a.product` in a basket self-join?"
                ),

                "options": [
                    "To select more expensive products",
                    "To prevent self-pairs and reverse duplicates",
                    "To convert text to numbers",
                    "To remove popular items",
                ],

                "correct": 1,

                "explanation": (
                    "A stable inequality ordering produces one representation of each "
                    "unordered pair and prevents an item from pairing with itself."
                ),
            },

            {
                "id": "M01.L08.Q11",

                "section_id": "integrated-workflows",

                "type": "open",

                "question": (
                    "A product team asks you to build a reusable learner analytics data set "
                    "and investigate falling course completion. Explain how you would decide "
                    "where the transformation logic lives, validate the final grain, protect "
                    "privacy, and combine funnel, cohort, anomaly, churn, and experiment "
                    "analysis to reach a trustworthy recommendation."
                ),
            },
        ],

        "passing_score": 70,
    },
}
