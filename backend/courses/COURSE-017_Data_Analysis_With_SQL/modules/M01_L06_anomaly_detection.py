"""M01.L06 — Anomaly Detection.

One source chapter -> one complete learner-facing lesson + essential inline Images +
inline Exercises + lesson Quiz.
Source alignment: Chapter 6, "Anomaly Detection".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L06"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from data preparation and time-based "
    "reasoning through cohort analysis, text analysis, anomaly detection, and "
    "other common analytical workflows."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Anomaly Detection",

    "slug": "data-analysis-sql-m01-l06",

    "description": (
        "A practical introduction to anomaly detection with SQL: distinguish real "
        "extreme events from data-quality problems, profile distributions, detect "
        "outliers with sorting, percentiles, z-scores, and visual summaries, find "
        "anomalous values, frequencies, and absences, investigate root causes, and "
        "choose appropriate handling strategies such as removal, replacement, "
        "winsorization, or rescaling."
    ),

    "order": 6,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "sql",
        "anomaly-detection",
        "outliers",
        "percentiles",
        "z-score",
        "standard-deviation",
        "box-plots",
        "time-series",
        "data-quality",
        "winsorization",
        "data-profiling",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L05",
    ],

    # =======================================================================
    # ESSENTIAL IMAGE POLICY
    # =======================================================================
    #
    # Only figures that materially improve understanding are requested.
    #
    # Essential figures requested:
    # - IMG-M01-L06-01: real anomaly vs data-quality anomaly decision model
    # - IMG-M01-L06-02: Source Figure 6-2, z-scores and standard deviations
    # - IMG-M01-L06-03: Source Figure 6-8, box-plot anatomy
    # - IMG-M01-L06-04: Source Figure 6-11, anomaly drill-down by status
    #

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Anomaly Detection",

        "content": """# Anomaly Detection

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L06  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapter 6, *Anomaly Detection*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what an anomaly is and why an unusual value is not automatically an error.
- Distinguish real-world extreme events from anomalies caused by bad data collection or processing.
- Decide when SQL is a suitable tool for anomaly detection and when another system is more appropriate.
- Use sorting, frequencies, grouping, percentiles, and standard deviations to identify unusual observations.
- Explain `percent_rank`, `ntile`, `percentile_cont`, and `percentile_disc`.
- Calculate and interpret a z-score.
- Use histograms, scatter plots, and box plots as anomaly-detection aids.
- Distinguish anomalous values, anomalous counts/frequencies, and anomalous absences.
- Detect anomalies relative to a subgroup rather than only to the full population.
- Use time-series drill-downs to investigate spikes and structural changes.
- Use gap and "time since last seen" analysis to detect absence-based anomalies.
- Investigate root cause before deciding what to do with an anomaly.
- Compare removal, selective exclusion, replacement, winsorization, and rescaling.
- Explain why domain knowledge is essential when interpreting outliers.
- Build a practical anomaly-detection workflow that is transparent and reproducible.

---

## 1. What is an anomaly?

An **anomaly** is an observation that differs from the rest of the data in a way that deserves attention.

You may also hear:

- outlier;
- deviation;
- exception;
- novelty;
- unusual value;
- noise.

The important word is not "different."

The important phrase is:

> **Different enough that we need to understand why.**

Suppose most purchases are between 100 and 500 EGP and one purchase is 80,000 EGP.

That could be:

```text
a fraudulent transaction
a legitimate enterprise order
a duplicated payment
a unit-conversion problem
a test transaction
```

The number alone does not tell us the cause.

### Two broad sources of anomalies

Most anomalies come from one of two places.

#### 1. A real unusual event

Examples:

- fraud;
- a cyberattack;
- a highly successful campaign;
- a product being used in an unexpected way;
- a major earthquake;
- an unusually valuable customer.

The data may be perfectly correct.

The event itself is unusual.

#### 2. A data-quality or processing problem

Examples:

- a typo;
- missing validation;
- duplicated rows;
- a failed pipeline;
- a logging change;
- a unit mismatch;
- a default placeholder stored as if it were a real value.

The event may not be unusual at all.

The **representation of the event** is wrong.

[[IMAGE_NEEDED: IMG-M01-L06-01 / Instructor Figure — Two sources of anomalies and what to do next | Start with an unusual observation, branch into Real Event and Data/Processing Error; under Real Event show investigate business/security/scientific meaning and usually preserve the record, under Data Error show validate source, correct/remove if justified, and fix upstream; both branches feed into documented analysis decisions | Learner should notice that anomaly detection does not automatically mean anomaly deletion]]

### Positive anomalies also matter

Anomaly detection is not only for problems.

You may want to detect:

```text
customers with unusually high lifetime value
campaigns with unusually high conversion
products with unusually low return rates
teams with unusually fast response times
```

An anomaly is simply unusual relative to a baseline.

Whether "unusual" is good or bad depends on context.

---

## 2. When SQL is a good anomaly-detection tool

SQL is useful when:

- the data is already in a database;
- the detection logic can be expressed as transparent rules;
- you need to summarize millions of rows;
- anomaly detection is one stage in a larger SQL analysis;
- you need reproducible calculations;
- latency does not need to be instantaneous.

SQL is especially strong for questions such as:

```text
Which values are in the top 1%?
Which customers purchased much more than usual?
Which days had unusually high traffic?
Which locations have values outside their normal range?
Which accounts have not been seen for much longer than normal?
```

### Why SQL is attractive

A SQL anomaly rule can be inspected.

For example:

```sql
CASE
    WHEN amount > p99_amount THEN 1
    ELSE 0
END AS is_outlier
```

is explicit.

Another analyst can see exactly why a row was flagged.

### Where SQL becomes weaker

SQL may not be the best tool when:

#### Advanced statistical modeling is required

Python and R provide broader statistical and machine-learning ecosystems.

#### Millisecond real-time detection is required

Fraud or intrusion systems may need streaming infrastructure rather than an analytics warehouse that receives data with delay.

#### The pattern changes adaptively

Rule-based SQL does not automatically learn new attacker behavior.

Machine learning may be better when the decision boundary must adapt from data.

### A common production pattern

A useful architecture is:

```text
historical data in SQL
        ↓
learn typical ranges and suspicious patterns
        ↓
define interpretable features and thresholds
        ↓
implement real-time checks in streaming / serving infrastructure
```

SQL remains valuable even when it is not the final detection engine.

---

## 3. First-pass detection: sort, count, and compare groups

The simplest anomaly-detection tools are often the most useful.

### Sort the values

To inspect high values:

```sql
SELECT amount
FROM transactions
WHERE amount IS NOT NULL
ORDER BY amount DESC;
```

To inspect low values:

```sql
SELECT amount
FROM transactions
WHERE amount IS NOT NULL
ORDER BY amount ASC;
```

Always inspect **both ends**.

A suspicious value can be extremely high or extremely low.

### Do not ignore nulls

If sorting reveals many nulls, that is useful information.

A missing value might represent:

- optional data;
- collection failure;
- pipeline failure;
- an unknown measurement;
- a legitimate non-applicable case.

The null itself may be part of the anomaly investigation.

### Add frequency

A value can look strange because it is rare.

```sql
SELECT
    amount,
    COUNT(*) AS records
FROM transactions
GROUP BY amount
ORDER BY amount DESC;
```

You can also calculate the share of records:

```sql
SELECT
    amount,
    COUNT(*) AS records,
    COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER () AS pct_records
FROM transactions
GROUP BY amount
ORDER BY amount DESC;
```

Now you can distinguish:

```text
one strange value
```

from:

```text
a strange value occurring thousands of times
```

The second pattern may suggest a sentinel value or systematic processing issue.

### Global anomalies vs local anomalies

An anomaly should often be judged relative to a **group**.

Suppose:

```text
purchase = 20,000 EGP
```

It may be an outlier for individual consumers but normal for enterprise accounts.

Instead of only asking:

```text
Is this unusual overall?
```

also ask:

```text
Is this unusual for this customer type?
Is this unusual for this country?
Is this unusual for this product?
Is this unusual for this device?
```

Example:

```sql
SELECT
    account_type,
    amount,
    COUNT(*) AS records
FROM transactions
GROUP BY account_type, amount
ORDER BY account_type, amount DESC;
```

Context changes what "normal" means.

---

## 4. Quantify unusualness with percentiles

Sorting helps you see extremes.

Percentiles help you **measure** where a value lies in a distribution.

If a value is at the 95th percentile, roughly 95% of the observations are below it.

Useful reference points include:

```text
25th percentile
50th percentile = median
75th percentile
95th percentile
99th percentile
```

### `percent_rank`

A window function can calculate the relative rank of each row.

```sql
SELECT
    customer_id,
    amount,
    PERCENT_RANK() OVER (
        ORDER BY amount
    ) AS percentile
FROM transactions;
```

For group-specific comparison:

```sql
SELECT
    customer_id,
    account_type,
    amount,
    PERCENT_RANK() OVER (
        PARTITION BY account_type
        ORDER BY amount
    ) AS percentile
FROM transactions;
```

This is often more meaningful than a global percentile.

### Calculate rank before aggregation

If repeated values matter to the distribution, calculate the percentile at row level first.

Bad sequence:

```text
aggregate values
-> percentile
```

when your goal is row-level ranking.

Better sequence:

```text
row-level values
-> percentile
-> aggregate or summarize if needed
```

### `ntile`

`ntile` divides the ordered rows into a chosen number of buckets.

```sql
SELECT
    amount,
    NTILE(100) OVER (
        ORDER BY amount
    ) AS percentile_bucket
FROM transactions;
```

You can also use:

```text
NTILE(4)   -> quartiles
NTILE(10)  -> deciles
NTILE(100) -> percentile-like buckets
```

`ntile` is useful when the exact percentile is less important than grouping records into relative bands.

### Exact percentile thresholds

Sometimes you want the actual threshold value.

```sql
SELECT
    PERCENTILE_CONT(0.95)
        WITHIN GROUP (ORDER BY amount) AS p95
FROM transactions;
```

You may also encounter:

```text
PERCENTILE_DISC
```

The difference is important.

### `percentile_cont`

Returns an interpolated value at the requested percentile.

That number might not exist in the raw data.

### `percentile_disc`

Returns an actual observed value nearest the requested percentile boundary.

A practical rule:

```text
continuous numeric measures -> percentile_cont is often natural
discrete or categorical-like ordered values -> percentile_disc may be more intuitive
```

The exact database syntax varies.

### Performance note

Exact percentile calculations may require large sorts.

On very large tables, approximate percentile functions can be much faster and may be sufficiently accurate for anomaly thresholds.

---

## 5. Standard deviation and z-scores

Percentiles answer:

```text
What share of observations are below this value?
```

A z-score answers:

```text
How many standard deviations is this value away from the mean?
```

### Standard deviation

Standard deviation describes how spread out values are around the mean.

Small standard deviation:

```text
values are tightly clustered
```

Large standard deviation:

```text
values are more spread out
```

For an approximately normal distribution:

```text
about 68% of values fall within ±1 standard deviation
about 95% fall within ±2 standard deviations
```

These are useful intuitions, not universal laws for every real-world distribution.

### Population vs sample

Many databases provide:

```text
STDDEV_POP
STDDEV_SAMP
STDDEV
```

Use `STDDEV_POP` when your dataset represents the full population of interest.

Use `STDDEV_SAMP` when your rows are a sample from a larger population.

For very large datasets, the numerical difference may be small, but the statistical meaning is different.

### Z-score formula

For a value `x`:

```text
z = (x - mean) / standard deviation
```

Interpretation:

```text
z = 0    -> exactly at the mean
z = +1   -> one standard deviation above the mean
z = -2   -> two standard deviations below the mean
z = +5   -> extremely far above the mean
```

{{image:normal-distribution-z-scores}}

### Calculate z-scores in SQL

First calculate the overall mean and standard deviation:

```sql
WITH stats AS (
    SELECT
        AVG(amount) AS avg_amount,
        STDDEV_POP(amount) AS std_amount
    FROM transactions
    WHERE amount IS NOT NULL
)
SELECT
    t.customer_id,
    t.amount,
    s.avg_amount,
    s.std_amount,
    (t.amount - s.avg_amount) / NULLIF(s.std_amount, 0) AS z_score
FROM transactions t
CROSS JOIN stats s
WHERE t.amount IS NOT NULL;
```

`NULLIF` protects against division by zero if all values are identical.

### Group-specific z-scores

A customer transaction may be normal for one segment and extreme for another.

You can compute statistics by segment:

```sql
WITH stats AS (
    SELECT
        account_type,
        AVG(amount) AS avg_amount,
        STDDEV_POP(amount) AS std_amount
    FROM transactions
    GROUP BY account_type
)
SELECT
    t.customer_id,
    t.account_type,
    t.amount,
    (t.amount - s.avg_amount)
        / NULLIF(s.std_amount, 0) AS z_score
FROM transactions t
JOIN stats s
    ON t.account_type = s.account_type;
```

### A warning about z-score thresholds

You may hear simple rules such as:

```text
|z| > 3 means anomaly
```

That can be useful as a screening heuristic.

It is not a universal truth.

If the distribution is highly skewed or heavy-tailed, z-score thresholds can behave poorly.

Use them with knowledge of the data distribution.

{{exercise:M01.L06.EX01}}

---

## 6. Visual tools: histogram, scatter plot, and box plot

SQL can prepare the data.

A graph can make the anomaly obvious.

### Histogram or frequency plot

A histogram helps answer:

```text
What is the shape of the distribution?
Is it symmetric or skewed?
Are there multiple peaks?
Are some values unexpectedly frequent?
Are the tails very long?
```

SQL preparation may look like:

```sql
SELECT
    ROUND(amount, 0) AS amount_bucket,
    COUNT(*) AS records
FROM transactions
GROUP BY 1
ORDER BY 1;
```

### Scatter plot

A scatter plot is useful when two numeric variables matter.

Examples:

```text
transaction amount vs account age
delivery time vs distance
model error vs input size
earthquake magnitude vs depth
```

A point may not be unusual in either variable individually but may be unusual in the **combination**.

### Box plot

A box plot summarizes a numeric distribution.

Its central components are:

```text
Q1 = 25th percentile
median = 50th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
```

A common whisker rule is:

```text
lower boundary = Q1 - 1.5 × IQR
upper boundary = Q3 + 1.5 × IQR
```

Values outside those boundaries are plotted as outliers.

{{image:box-plot-anatomy}}

### Box plot is not "automatic truth"

A point outside 1.5 × IQR is mathematically unusual according to that rule.

It is not automatically:

```text
wrong
fraudulent
irrelevant
```

Always separate:

```text
statistically unusual
```

from:

```text
invalid
```

---

## 7. Three important forms of anomalies

Anomalies do not always look like one giant number.

A useful framework is:

1. anomalous **values**;
2. anomalous **counts or frequencies**;
3. anomalous **presence or absence**.

Each form requires a different question.

---

## 8. Anomalous values

A value anomaly may be:

```text
extremely high
extremely low
unusually precise
unexpectedly formatted
invalid for its category
```

### Extreme numeric values

Examples:

```text
purchase amount = 10,000× normal
temperature = -999
duration = 0.000001 seconds
```

### Suspicious precision

Suppose a measurement usually has two decimal places:

```text
1.08
1.09
1.10
1.11
```

but occasionally contains:

```text
1.08000004
```

That might reflect:

- a different measurement instrument;
- floating-point conversion;
- a processing path;
- a valid increase in precision.

The anomaly is not necessarily the numeric magnitude.

The anomaly may be the **representation**.

### Text anomalies

You can detect capitalization differences by comparing cardinality.

```sql
SELECT
    COUNT(DISTINCT event_type) AS distinct_types,
    COUNT(DISTINCT LOWER(event_type)) AS distinct_lower_types
FROM events;
```

If:

```text
distinct_types = 25
distinct_lower_types = 24
```

then at least one category differs only by capitalization.

You can investigate:

```sql
SELECT
    event_type,
    LOWER(event_type) AS normalized_type,
    COUNT(*) AS records
FROM events
GROUP BY 1, 2
ORDER BY normalized_type, records DESC;
```

### Validate against known allowed values

If a trusted list exists:

```text
earthquake
explosion
ice quake
landslide
```

join the incoming data to the reference table.

Unexpected unmatched values become investigation candidates.

This is stronger than guessing which rare spelling is wrong.

### Investigate correlated attributes

When an extreme value is found, inspect:

- timestamp;
- location;
- source system;
- device;
- customer;
- product;
- status;
- ingestion batch.

The goal is to understand:

```text
What else is different about the anomalous rows?
```

That is often how root cause is found.

---

## 9. Anomalous counts, spikes, and frequency changes

Sometimes every individual row looks normal.

The anomaly is that **too many rows occur together**.

Example:

```text
A purchase of 100 EGP is normal.
100 EGP every minute for 48 hours is not.
```

The value is normal.

The frequency is anomalous.

### Start broad

For event data:

```sql
SELECT
    DATE_TRUNC('year', event_time) AS year,
    COUNT(*) AS events
FROM events
GROUP BY 1
ORDER BY 1;
```

Then move to months:

```sql
SELECT
    DATE_TRUNC('month', event_time) AS month,
    COUNT(*) AS events
FROM events
GROUP BY 1
ORDER BY 1;
```

Then days or hours if needed.

### Drill down iteratively

A good investigation often looks like:

```text
year
↓
month
↓
day
↓
hour
↓
split by status/source/product/location
```

You are asking:

```text
Where does the anomaly first appear?
Which subgroup explains it?
```

### Structural changes can masquerade as behavioral changes

Imagine monthly event counts suddenly jump.

Possible explanations include:

```text
real user growth
new product launch
duplicate logging
new instrumentation
different review status
new data source
```

This is why anomaly analysis should not stop at the first graph.

{{image:earthquakes-by-status-monthly}}

### Combine prior techniques

Frequency-anomaly analysis often reuses:

- time-series aggregation;
- cohort ideas;
- text parsing;
- percentiles;
- rolling averages;
- z-scores;
- group comparisons.

Anomaly detection is not isolated from the rest of data analysis.

It combines those skills.

{{exercise:M01.L06.EX02}}

---

## 10. Absence can be an anomaly too

Analysts often search for:

```text
too much
too high
too frequent
```

but anomalies can also be:

```text
nothing happened
```

Examples:

- a server stopped sending heartbeats;
- a customer stopped logging in;
- a sensor stopped reporting;
- a store stopped recording sales;
- a subscription produced no expected renewal event.

### The difficulty

A missing row is hard to see because it is not there.

To detect absence, you often need an **expected grid**.

Example:

```text
every customer
×
every day
```

Then left join actual activity.

This is the same technique used for sparse time-series and cohort data.

### Time since last seen

Another useful technique is:

```text
How long has it been since the last event?
```

You can calculate gaps with `lead` or `lag`.

```sql
SELECT
    customer_id,
    event_time,
    LEAD(event_time) OVER (
        PARTITION BY customer_id
        ORDER BY event_time
    ) AS next_event
FROM activity;
```

Then:

```text
gap = next_event - event_time
```

For the current gap:

```text
current_time - latest_event
```

### Compare current gap with historical behavior

Suppose a customer usually returns every:

```text
5–8 days
```

and is now absent for:

```text
45 days
```

That is much more informative than simply saying:

```text
last seen 45 days ago
```

Useful features include:

```text
average historical gap
maximum historical gap
median historical gap
current gap
current gap / average gap
```

This pattern is valuable for:

- churn risk;
- device monitoring;
- maintenance;
- sensor health;
- recurring purchase behavior.

### Absence is not automatically failure

Some behavior is naturally irregular.

Use the historical pattern and domain context before setting an alert threshold.

---

## 11. Investigate before changing the data

After detecting an anomaly, do not immediately delete it.

A strong workflow is:

```text
detect
-> inspect
-> compare related rows
-> identify possible source
-> measure analytical impact
-> decide action
```

### Inspect the full row

If an amount is extreme:

```sql
SELECT *
FROM transactions
WHERE transaction_id = ...;
```

Look for clues:

- source;
- user;
- timestamp;
- status;
- region;
- batch;
- version;
- other related fields.

### Compare neighboring or related records

Ask:

```text
Did other rows from the same day behave similarly?
Did the same data source create other strange rows?
Did the same customer have similar values before?
Did a logging change happen at that time?
```

### Ask domain experts

A value that looks impossible statistically may be expected operationally.

A domain expert may know:

```text
a policy changed
a sensor was replaced
a promotion launched
a new product category appeared
a data-collection rule changed
```

Anomaly detection is partly statistics and partly detective work.

---

## 12. Handling anomalies: preserve, remove, or replace?

Once the root cause is understood as far as possible, choose a handling strategy.

### Option 1 — Keep it

Use when:

- the event is real;
- it matters to the analysis;
- removing it would hide important behavior.

Example:

```text
a legitimate high-value customer
```

### Option 2 — Remove the row

Appropriate when:

- the whole row is likely corrupted;
- the record is a duplicate;
- the source event is invalid;
- the dataset is large and the few bad rows do not materially affect coverage.

Example:

```sql
WHERE amount NOT IN (-999, -9999)
```

But removal should be justified, not automatic.

### Measure impact before removing

Compare metrics:

```sql
SELECT
    AVG(amount) AS avg_raw,
    AVG(
        CASE
            WHEN amount > -999 THEN amount
        END
    ) AS avg_adjusted
FROM transactions;
```

Sometimes an anomaly barely changes the overall result.

Sometimes it changes a subgroup dramatically.

Both facts matter.

### Global removal vs calculation-specific exclusion

A `WHERE` clause removes the row from everything.

A `CASE` expression can exclude it only from one calculation.

Example:

```sql
SELECT
    COUNT(*) AS total_rows,
    AVG(
        CASE
            WHEN is_valid = 1 THEN amount
        END
    ) AS valid_avg
FROM transactions;
```

This preserves row counts and other fields while protecting the calculation.

### Option 3 — Replace with a known correct value

If the cause is known and correction is defensible:

```sql
CASE
    WHEN unit = 'cents'
        THEN amount / 100.0
    ELSE amount
END
```

or map a known category typo to its canonical value.

### Option 4 — Collapse rare categories

If many rare categories add no analytical value:

```sql
CASE
    WHEN event_type = 'purchase' THEN 'purchase'
    ELSE 'other'
END
```

This simplifies reporting but loses detail.

Document the decision.

---

## 13. Winsorization: cap extreme values instead of deleting them

**Winsorization** replaces values beyond chosen percentile boundaries with the boundary values.

Example:

```text
below 5th percentile -> set to p05
above 95th percentile -> set to p95
```

This preserves every row while reducing the impact of extremes.

### Calculate thresholds

```sql
WITH limits AS (
    SELECT
        PERCENTILE_CONT(0.05)
            WITHIN GROUP (ORDER BY amount) AS p05,
        PERCENTILE_CONT(0.95)
            WITHIN GROUP (ORDER BY amount) AS p95
    FROM transactions
)
SELECT
    t.amount,
    CASE
        WHEN t.amount < l.p05 THEN l.p05
        WHEN t.amount > l.p95 THEN l.p95
        ELSE t.amount
    END AS amount_winsorized
FROM transactions t
CROSS JOIN limits l;
```

### What winsorization changes

Suppose:

```text
p05 = 20
p95 = 500
```

Then:

```text
5     -> 20
50    -> 50
300   -> 300
800   -> 500
10000 -> 500
```

The rows remain.

The extreme numeric influence is reduced.

### There is no universal percentile

Possible choices include:

```text
1st / 99th
5th / 95th
0.1th / 99.9th
```

The threshold depends on:

- the distribution;
- how many extremes exist;
- the business meaning;
- the downstream model or metric.

Winsorization should not be used simply because outliers are inconvenient.

---

## 14. Rescaling while retaining the observations

Another strategy is to keep every value but change the scale.

### Z-score scaling

Convert values into standard-deviation units:

```text
z = (x - mean) / stddev
```

This makes variables with different units easier to compare.

It also preserves whether a value is above or below the mean.

### Log transformation

For positive values with a very wide range:

```sql
SELECT
    amount,
    LOG(amount) AS log_amount
FROM transactions
WHERE amount > 0;
```

A log transformation:

- preserves ordering;
- compresses large values;
- spreads small positive values;
- can make skewed patterns easier to inspect.

Example:

```text
1       -> log10 = 0
10      -> log10 = 1
100     -> log10 = 2
1000    -> log10 = 3
```

A 1000× range becomes a 3-unit range.

### Important limitation

A logarithm is not defined for zero or negative values in ordinary real-number analysis.

You need to decide how to handle:

```text
0
negative values
```

before applying the transformation.

### Other transformations

Depending on the problem:

```text
square root
cube root
reciprocal
unit conversion
```

may help.

Rescaling is not the same as fixing bad data.

It changes representation while keeping the observation.

---

## 15. A practical anomaly-detection workflow

Use this workflow when approaching a new dataset.

### Step 1 — Define what "anomalous" could mean

Consider:

```text
value
frequency
absence
combination of variables
group-specific behavior
```

### Step 2 — Profile the raw data

Check:

- nulls;
- minimum;
- maximum;
- distinct values;
- frequency;
- basic percentiles;
- sample rows;
- subgroup differences.

### Step 3 — Visualize key distributions

Use:

```text
histogram
scatter plot
box plot
time series
```

depending on the question.

### Step 4 — Quantify extremity

Try:

```text
percentiles
ntiles
IQR boundaries
z-scores
```

Do not rely on only one method.

### Step 5 — Compare local baselines

Ask whether the row is unusual:

```text
for this segment
for this location
for this customer
for this product
for this period
```

### Step 6 — Investigate context

Check:

- source system;
- status;
- event time;
- ingestion version;
- related rows;
- recent logging changes.

### Step 7 — Measure impact

Compare important metrics:

```text
with anomaly
without anomaly
with corrected value
```

### Step 8 — Choose a handling strategy

Possible actions:

```text
keep
flag
remove
exclude from a calculation
replace
winsorize
rescale
```

### Step 9 — Fix the source when possible

If a broken validation rule creates a bad value every day, a SQL cleanup query is only treating the symptom.

Fix:

```text
data-entry validation
logging logic
ETL transformation
deduplication
unit conversion
schema constraint
```

upstream when you can.

### Step 10 — Document the assumption

Record:

```text
why the value was considered anomalous
how it was handled
which thresholds were used
which business context supported the decision
```

This makes the analysis reproducible and auditable.

{{exercise:M01.L06.EX03}}

---

## Important misconceptions

### Misconception 1

> Every outlier is bad data.

False. Some outliers are the most important real events in the dataset.

### Misconception 2

> A value is anomalous if it is large.

Anomaly is relative. A large value may be normal for one subgroup and extreme for another.

### Misconception 3

> A z-score above 3 is always invalid.

A high z-score means statistically extreme relative to the chosen distribution. It does not prove that the data is wrong.

### Misconception 4

> Missing rows cannot be detected because they do not exist.

Expected grids, date dimensions, and gap analysis can reveal absence.

### Misconception 5

> The safest response to outliers is deletion.

Deletion can remove real and valuable information. Investigate first.

### Misconception 6

> Winsorization corrects bad data.

Winsorization caps extremes. It does not discover or fix their root cause.

### Misconception 7

> A sudden increase in events means user behavior changed.

It may instead reflect instrumentation, status, source, or processing changes.

---

## Key terminology

| Term | Meaning |
|---|---|
| Anomaly | Observation or pattern that differs enough from the baseline to merit investigation |
| Outlier | Common synonym for anomaly, especially for unusual values |
| Ground truth | Trusted label or external reference indicating what is normal or anomalous |
| Local anomaly | Observation that is unusual within a subgroup even if not globally extreme |
| Percentile | Position of a value relative to the rest of a distribution |
| `percent_rank` | Window function returning a row's relative rank in an ordered set |
| `ntile` | Window function splitting ordered rows into a specified number of buckets |
| `percentile_cont` | Interpolated percentile threshold |
| `percentile_disc` | Observed value nearest the requested percentile |
| Standard deviation | Measure of spread around the mean |
| Z-score | Distance from the mean measured in standard deviations |
| IQR | Interquartile range: Q3 minus Q1 |
| Box plot | Visualization of quartiles, median, whiskers, and outliers |
| Frequency anomaly | Unusual count or rate of events |
| Absence anomaly | Unexpected lack of events or records |
| Gap analysis | Analysis of elapsed time between events |
| Winsorization | Capping extreme values at selected percentile boundaries |
| Rescaling | Transforming values onto a different scale while retaining observations |
| Root cause | Underlying reason an anomaly occurred |

---

## Self-check

Before continuing, make sure you can answer:

1. What are the two broad sources of anomalies?
2. Why should real extreme events usually not be deleted automatically?
3. When is SQL a strong tool for anomaly detection?
4. Why should both high and low ends of a distribution be inspected?
5. How can frequency help distinguish a one-off outlier from a systematic issue?
6. Why might a value be globally normal but locally anomalous?
7. What is the difference between `percentile_cont` and `percentile_disc`?
8. What does a z-score of +4 mean?
9. Why can z-score thresholds be misleading on a highly skewed distribution?
10. What information does a box plot summarize?
11. What is an anomalous frequency?
12. How can absence of data become detectable?
13. Why should you compare results with and without an outlier before removing it?
14. What is the difference between row removal and calculation-specific exclusion?
15. What does winsorization do?
16. When is log rescaling useful?
17. Why is root-cause investigation more important than the anomaly score itself?

---

## Retain this idea

**Anomaly detection is not the process of deleting strange values. It is the process of defining a baseline, finding observations or patterns that deviate from it, investigating why they differ, and then choosing a treatment that matches the real cause and the analytical goal.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "anomaly-mental-model", "title": "What is an anomaly?", "order": 1},
            {"id": "sql-fit", "title": "When SQL is a good anomaly-detection tool", "order": 2},
            {"id": "first-pass", "title": "First-pass detection: sort, count, and compare groups", "order": 3},
            {"id": "percentiles", "title": "Quantify unusualness with percentiles", "order": 4},
            {"id": "zscore", "title": "Standard deviation and z-scores", "order": 5},
            {"id": "visual-detection", "title": "Visual tools: histogram, scatter plot, and box plot", "order": 6},
            {"id": "forms", "title": "Three important forms of anomalies", "order": 7},
            {"id": "value-anomalies", "title": "Anomalous values", "order": 8},
            {"id": "frequency-anomalies", "title": "Anomalous counts, spikes, and frequency changes", "order": 9},
            {"id": "absence-anomalies", "title": "Absence can be an anomaly too", "order": 10},
            {"id": "investigation", "title": "Investigate before changing the data", "order": 11},
            {"id": "handling", "title": "Handling anomalies: preserve, remove, or replace?", "order": 12},
            {"id": "winsorization", "title": "Winsorization: cap extreme values instead of deleting them", "order": 13},
            {"id": "rescaling", "title": "Rescaling while retaining the observations", "order": 14},
            {"id": "practical-workflow", "title": "A practical anomaly-detection workflow", "order": 15},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L06.EX01",

            "title": "Flag Unusual Transaction Amounts",

            "lesson_code": "M01.L06",

            "section_id": "zscore",

            "placement": "after_section",

            "description": (
                "Use percentiles and z-scores to identify unusually large or small "
                "transactions without assuming every extreme value is invalid."
            ),

            "instructions": (
                "Assume a `transactions` table with `transaction_id`, `account_type`, "
                "`amount`, and `created_at`.\n"
                "1. Calculate the 1st, 50th, and 99th percentile of amount.\n"
                "2. Calculate the overall mean and standard deviation.\n"
                "3. Calculate a z-score for each transaction.\n"
                "4. Repeat the z-score calculation within each account_type.\n"
                "5. Find one example that is globally ordinary but locally extreme, or "
                "explain how such a case could occur.\n"
                "6. Explain why you would flag these rows for investigation instead of "
                "deleting them immediately."
            ),

            "expected_output": (
                "SQL or clear pseudocode producing percentile thresholds and global/local "
                "z-scores, followed by a short interpretation of the flagged rows."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "percentiles",
                "standard-deviation",
                "z-score",
                "local-anomalies",
            ],
        },

        {
            "id": "M01.L06.EX02",

            "title": "Investigate a Sudden Traffic Spike",

            "lesson_code": "M01.L06",

            "section_id": "frequency-anomalies",

            "placement": "after_section",

            "description": (
                "Use progressive time aggregation and dimensional drill-down to explain "
                "an anomalous event-count spike."
            ),

            "instructions": (
                "You have an `events` table with `event_time`, `source`, `status`, "
                "`country`, and `event_name`.\n"
                "1. Count events by month.\n"
                "2. Identify the month with the largest unexpected spike.\n"
                "3. Drill into that month by day.\n"
                "4. Split the anomalous days by source and status.\n"
                "5. Describe at least three possible explanations for the spike.\n"
                "6. State what evidence would help distinguish real user behavior from a "
                "logging or pipeline change."
            ),

            "expected_output": (
                "A sequence of SQL queries or pseudocode that moves from broad trend to "
                "granular root-cause investigation, plus a short evidence-based conclusion."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "frequency-anomalies",
                "time-series",
                "drill-down-analysis",
                "root-cause-analysis",
            ],
        },

        {
            "id": "M01.L06.EX03",

            "title": "Choose the Right Treatment for Four Anomalies",

            "lesson_code": "M01.L06",

            "section_id": "practical-workflow",

            "placement": "after_section",

            "description": (
                "Decide whether to keep, remove, replace, winsorize, rescale, or escalate "
                "different anomalies based on their likely causes."
            ),

            "instructions": (
                "For each case, choose a treatment and justify it:\n"
                "1. A legitimate enterprise order is 40x larger than the normal consumer order.\n"
                "2. A duplicate ETL load created each transaction twice for one hour.\n"
                "3. One sensor stored `-999` when a reading was unavailable.\n"
                "4. A valid positive revenue field ranges from 1 to 10,000,000 and the "
                "distribution is difficult to visualize.\n"
                "For each case, state whether you would keep, remove, replace, flag, "
                "winsorize, or rescale the data, and whether an upstream fix is needed."
            ),

            "expected_output": (
                "Four short decisions with reasoning tied to root cause and analytical goal."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "anomaly-handling",
                "data-quality",
                "winsorization",
                "rescaling",
                "analytical-judgment",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L06.QZ01",

        "title": "Anomaly Detection — Knowledge Check",

        "lesson_code": "M01.L06",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L06.Q01",

                "section_id": "anomaly-mental-model",

                "question": (
                    "Which statement best describes an anomaly?"
                ),

                "options": [
                    "A value that must always be deleted",
                    "An observation or pattern that differs enough from a baseline to merit investigation",
                    "Any value above the mean",
                    "Any null value",
                ],

                "correct": 1,

                "explanation": (
                    "Anomalies are observations or patterns that deserve investigation; "
                    "they may be valid real events or data-quality problems."
                ),
            },

            {
                "id": "M01.L06.Q02",

                "section_id": "first-pass",

                "question": (
                    "Why should anomaly detection often be performed within subgroups?"
                ),

                "options": [
                    "SQL requires a GROUP BY for every query",
                    "A value can be normal globally but unusual relative to its local context",
                    "Subgroups always have normal distributions",
                    "It removes all null values",
                ],

                "correct": 1,

                "explanation": (
                    "The correct baseline may depend on customer type, location, product, "
                    "device, or another meaningful subgroup."
                ),
            },

            {
                "id": "M01.L06.Q03",

                "section_id": "percentiles",

                "question": (
                    "What is the main difference between `percentile_cont` and `percentile_disc`?"
                ),

                "options": [
                    "`percentile_cont` can interpolate a threshold, while `percentile_disc` returns an observed value",
                    "`percentile_disc` works only with dates",
                    "`percentile_cont` always returns the mean",
                    "There is no difference",
                ],

                "correct": 0,

                "explanation": (
                    "`percentile_cont` may return an interpolated value, whereas "
                    "`percentile_disc` chooses a value from the observed distribution."
                ),
            },

            {
                "id": "M01.L06.Q04",

                "section_id": "zscore",

                "question": (
                    "A z-score of -2.5 means that the value is:"
                ),

                "options": [
                    "2.5 percent below the mean",
                    "2.5 standard deviations below the mean",
                    "In the 2.5th percentile by definition",
                    "Invalid",
                ],

                "correct": 1,

                "explanation": (
                    "A z-score measures distance from the mean in standard-deviation units."
                ),
            },

            {
                "id": "M01.L06.Q05",

                "section_id": "visual-detection",

                "question": (
                    "What does the box in a standard box plot usually represent?"
                ),

                "options": [
                    "The minimum and maximum values",
                    "The range from the 25th to the 75th percentile",
                    "Exactly one standard deviation",
                    "Only anomalous values",
                ],

                "correct": 1,

                "explanation": (
                    "The box spans Q1 to Q3, and its height or width is the interquartile range."
                ),
            },

            {
                "id": "M01.L06.Q06",

                "section_id": "frequency-anomalies",

                "question": (
                    "A normally sized purchase occurs hundreds of times per hour for one account. "
                    "What type of anomaly is this primarily?"
                ),

                "options": [
                    "A frequency anomaly",
                    "A missing-data anomaly",
                    "A data-type anomaly",
                    "A percentile function error",
                ],

                "correct": 0,

                "explanation": (
                    "The individual value may be normal, but the rate or count of events is unusual."
                ),
            },

            {
                "id": "M01.L06.Q07",

                "section_id": "absence-anomalies",

                "question": (
                    "Which technique is most useful for making missing expected periods visible?"
                ),

                "options": [
                    "Deleting nulls",
                    "Joining to a complete date/entity grid",
                    "Sorting descending",
                    "Converting values to uppercase",
                ],

                "correct": 1,

                "explanation": (
                    "A complete expected grid creates explicit rows against which actual activity "
                    "can be left joined, making absences detectable."
                ),
            },

            {
                "id": "M01.L06.Q08",

                "section_id": "handling",

                "question": (
                    "What is an advantage of excluding an anomaly inside a CASE expression "
                    "rather than filtering it out with WHERE?"
                ),

                "options": [
                    "The row can remain available for counts or other valid fields",
                    "CASE permanently deletes the source record",
                    "WHERE cannot filter numbers",
                    "CASE automatically repairs the source system",
                ],

                "correct": 0,

                "explanation": (
                    "Calculation-specific exclusion can preserve the row for other analyses "
                    "while preventing the anomalous value from affecting one metric."
                ),
            },

            {
                "id": "M01.L06.Q09",

                "section_id": "winsorization",

                "question": (
                    "What does winsorization do?"
                ),

                "options": [
                    "Deletes every outlier row",
                    "Caps extreme values at selected boundary values such as chosen percentiles",
                    "Converts all values to z-scores",
                    "Finds the root cause automatically",
                ],

                "correct": 1,

                "explanation": (
                    "Winsorization retains rows but replaces extreme numeric values with "
                    "chosen lower or upper boundary values."
                ),
            },

            {
                "id": "M01.L06.Q10",

                "section_id": "practical-workflow",

                "type": "open",

                "question": (
                    "A KPI suddenly increases 70% overnight. Describe the investigation you "
                    "would perform before deciding that user behavior truly changed."
                ),
            },
        ],

        "passing_score": 70,
    },
}
