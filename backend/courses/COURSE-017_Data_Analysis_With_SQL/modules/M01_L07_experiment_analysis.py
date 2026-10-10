"""M01.L07 — Experiment Analysis.

One source chapter -> one complete learner-facing lesson + essential inline Images +
inline Exercises + lesson Quiz.
Source alignment: Chapter 7, "Experiment Analysis".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L07"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from preparation and time-based reasoning "
    "through cohort analysis, text analysis, anomaly detection, experimentation, "
    "and other common analytical workflows."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Experiment Analysis",

    "slug": "data-analysis-sql-m01-l07",

    "description": (
        "A practical introduction to experiment analysis with SQL: define hypotheses "
        "and success metrics, understand random assignment, analyze binary and "
        "continuous outcomes, diagnose flawed experiments, control observation windows, "
        "reason about repeated exposure, and use quasi-experimental approaches when "
        "randomized experiments are not possible."
    ),

    "order": 7,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "sql",
        "experimentation",
        "ab-testing",
        "causality",
        "binary-metrics",
        "continuous-metrics",
        "chi-square",
        "t-test",
        "time-boxing",
        "experiment-quality",
        "quasi-experiments",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L06",
    ],

    # =======================================================================
    # ESSENTIAL IMAGE POLICY
    # =======================================================================
    #
    # Only figures that materially improve understanding are requested.
    # Source figures that merely show sample tables or SQL outputs are omitted.
    #
    # Essential figures requested:
    # - IMG-M01-L07-01: correlation vs causation possibilities
    # - IMG-M01-L07-02: experiment anatomy and random assignment
    # - IMG-M01-L07-03: binary vs continuous experiment analysis
    # - IMG-M01-L07-04: randomized experiments vs quasi-experimental alternatives
    #

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Experiment Analysis",

        "content": """# Experiment Analysis

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L07  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapter 7, *Experiment Analysis*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why randomized experiments are stronger for causal inference than ordinary observational analysis.
- Distinguish correlation from causation and recognize several different explanations for an observed relationship.
- Define a clear experiment hypothesis.
- Choose a primary success metric and appropriate guardrail metrics.
- Explain why too many success metrics increase the risk of false discoveries.
- Describe random assignment and why it is essential to experiment validity.
- Build SQL summaries for binary-outcome experiments.
- Build SQL summaries for continuous-outcome experiments.
- Explain the role of chi-squared tests and two-sample t-tests in the chapter's experiment workflow.
- Preserve zero-outcome users correctly with `LEFT JOIN` and `COALESCE`.
- Diagnose assignment problems, eligibility problems, and sample-size problems.
- Detect experiment contamination such as users appearing in multiple variants.
- Recognize how outliers can distort continuous experiment metrics.
- Apply time boxing so participants receive comparable observation windows.
- Explain novelty effects, regression to the mean, and long-term holdouts in repeated-exposure experiments.
- Use pre/post analysis, natural experiments, and threshold-based analysis when randomized experiments are unavailable.
- State clearly when evidence is causal and when it is only suggestive.

---

## 1. Why experimentation matters: correlation is not causation

A large amount of data analysis is observational.

You may find:

```text
users who use Feature X retain longer
customers who contact support spend more
people who open emails purchase more
```

These observations may be useful.

But they do not automatically prove:

```text
Feature X causes retention
support causes spending
email opening causes purchasing
```

### Five possible explanations for a relationship

If variables `X` and `Y` move together, several explanations are possible.

#### 1. X causes Y

```text
X -> Y
```

This is the causal relationship an experiment often tries to establish.

#### 2. Y causes X

```text
Y -> X
```

The relationship is real, but the direction is reversed.

Example:

```text
rain -> umbrellas
```

rather than:

```text
umbrellas -> rain
```

#### 3. A third variable causes both

```text
      Z
     / \
    X   Y
```

Example:

```text
hot weather -> ice-cream sales
hot weather -> air-conditioner usage
```

Ice-cream sales and air-conditioner usage can be correlated without causing each other.

#### 4. A feedback loop exists

```text
X -> Y -> X -> Y ...
```

Example:

```text
lower engagement
-> fewer recommendations
-> lower engagement
```

The direction becomes hard to untangle observationally.

#### 5. The apparent relationship is random

With enough metrics and enough comparisons, some correlations will occur by chance.

[[IMAGE_NEEDED: IMG-M01-L07-01 / Instructor Figure — Five explanations for correlation | Show X and Y with five small relationship diagrams: X causes Y, Y causes X, common cause Z points to both, feedback loop between X and Y, and no real relationship/random coincidence | Learner should notice that observing correlation alone cannot identify which causal structure produced it]]

### Why randomization helps

A randomized experiment tries to make the treatment assignment independent of user characteristics.

If randomization works well:

```text
control
```

and:

```text
variant
```

should be similar before treatment.

The important systematic difference should be:

```text
which experience they received
```

This gives us a much stronger basis for attributing differences in outcomes to the treatment.

---

## 2. The three required parts of an experiment

A useful online experiment needs at least three things.

### 1. A hypothesis

A hypothesis is a specific prediction about what will happen when something changes.

Weak:

```text
The new onboarding is better.
```

Better:

```text
Reducing onboarding from six screens to four will increase the percentage
of new users who complete onboarding.
```

A good hypothesis includes:

```text
change
-> expected behavioral effect
```

### 2. A success metric

The metric should measure the behavior the hypothesis is about.

Examples:

```text
checkout completion rate
click-through rate
time to complete onboarding
purchase conversion
articles read
amount spent
```

A useful success metric should be:

- measurable;
- reasonably sensitive to the treatment;
- understandable;
- connected to the behavior of interest.

A distant metric such as long-term satisfaction may be strategically important but too noisy to detect the effect of a small UI experiment.

### 3. Random assignment

Users—or another chosen experimental unit—must be assigned to:

```text
control
variant A
variant B
...
```

through a random assignment system.

The assignment data must be available for analysis.

A typical data model contains:

```text
experiment_assignment
---------------------
experiment_name
user_id
variant
assignment_time
```

and separate behavior tables such as:

```text
events
purchases
sessions
```

[[IMAGE_NEEDED: IMG-M01-L07-02 / Instructor Figure — Anatomy of an online experiment | Show eligible users entering a random-assignment step, splitting into Control and Variant, each receiving a different experience, then both producing behavior events that flow into the same success-metric calculation; add a small guardrail-metrics branch beneath | Learner should notice that the analysis depends on a predefined hypothesis, random assignment, and the same measurement logic for both groups]]

---

## 3. Primary metrics, guardrails, and the multiple-comparisons problem

It is easy to calculate many metrics with SQL.

That does not mean every metric should be considered a success metric.

### Primary metric

The **primary success metric** answers the main hypothesis.

Example:

```text
Hypothesis:
New onboarding increases completion.

Primary metric:
Onboarding completion rate.
```

### Guardrail metrics

Guardrails protect against unintended harm.

Example:

```text
Primary:
checkout conversion

Guardrails:
page load time
refund rate
support contacts
```

The experiment can improve the main metric while damaging something else.

### Too many metrics create a problem

If you test enough metrics, some may look significant by chance.

This is the **multiple comparisons problem**.

A practical rule from the chapter is to keep the number of primary metrics small—often one or two—and use a limited set of guardrails.

### Choose metrics before seeing the result

If analysts choose the metric only after looking at the data, they can unconsciously select whichever metric makes the experiment look successful.

A better workflow is:

```text
hypothesis
-> primary metric
-> guardrails
-> experiment
-> analysis
```

not:

```text
experiment
-> calculate 40 metrics
-> choose the nicest result
```

---

## 4. Binary-outcome experiments

A binary outcome has two states:

```text
completed / not completed
clicked / did not click
purchased / did not purchase
graduated / did not graduate
```

The key metric is usually a rate:

```text
successes / exposed units
```

### Example question

Suppose we test a new onboarding flow.

The experiment table contains:

```text
user_id
experiment_name
variant
```

The event table contains:

```text
user_id
action
event_time
```

The desired result is:

```text
variant      total_users      completions      completion_rate
control      ...              ...              ...
variant      ...              ...              ...
```

### Use `LEFT JOIN`

This is critical.

If you use an inner join to the success event, you will keep only users who succeeded.

Then:

```text
completion rate = 100%
```

by construction.

Correct pattern:

```sql
SELECT
    a.variant,
    COUNT(DISTINCT a.user_id) AS total_users,
    COUNT(DISTINCT b.user_id) AS completions,
    COUNT(DISTINCT b.user_id) * 1.0
        / COUNT(DISTINCT a.user_id) AS completion_rate
FROM experiment_assignment a
LEFT JOIN actions b
    ON a.user_id = b.user_id
   AND b.action = 'onboarding_complete'
WHERE a.experiment_name = 'Onboarding'
GROUP BY a.variant;
```

The assignment table supplies the denominator.

The event table supplies the numerator.

### Contingency table

A binary experiment can also be represented as:

| Variant | Completed | Not completed |
|---|---:|---:|
| Control | ... | ... |
| Variant | ... | ... |

This is the typical structure used for a chi-squared comparison of categorical outcomes.

### In this chapter's workflow

SQL prepares:

```text
number assigned
number successful
success rate
```

The statistical significance calculation is performed outside SQL with an appropriate statistical tool or calculator.

### Statistical significance is not practical significance

Suppose:

```text
control = 40.00%
variant = 40.08%
```

A huge sample may make that difference statistically detectable.

But the business question remains:

```text
Is +0.08 percentage points worth shipping?
```

Always interpret both:

```text
statistical evidence
```

and:

```text
effect size / business value
```

{{exercise:M01.L07.EX01}}

---

## 5. Continuous-outcome experiments

A continuous metric can take many numeric values.

Examples:

```text
revenue per user
session duration
articles read
days active
time to complete a process
```

For these experiments, we often compare the **mean** between variants.

### Calculate one value per experimental unit first

Suppose users can make multiple purchases.

Do not calculate the average purchase row and call it average user spending.

First aggregate to user level:

```sql
WITH user_spend AS (
    SELECT
        a.variant,
        a.user_id,
        SUM(COALESCE(p.amount, 0)) AS amount
    FROM experiment_assignment a
    LEFT JOIN purchases p
        ON a.user_id = p.user_id
    WHERE a.experiment_name = 'Onboarding'
    GROUP BY a.variant, a.user_id
)
SELECT
    variant,
    COUNT(*) AS users,
    AVG(amount) AS mean_amount,
    STDDEV(amount) AS stddev_amount
FROM user_spend
GROUP BY variant;
```

The experiment unit is the user.

So the success metric must be calculated **per user first**.

### Why zeroes matter

A user who made no purchase should usually contribute:

```text
0
```

to spending per user.

If they remain `NULL`, functions such as `AVG` typically ignore them.

That changes the question from:

```text
How much does the average assigned user spend?
```

to:

```text
How much does the average purchaser spend?
```

Those are different metrics.

Use:

```sql
COALESCE(p.amount, 0)
```

when zero is the correct business meaning.

### Two-sample t-test

For continuous outcomes, the chapter uses a two-sample t-test workflow.

The summary inputs are:

```text
mean
standard deviation
number of observations
```

for each variant.

[[IMAGE_NEEDED: IMG-M01-L07-03 / Instructor Figure — Binary versus continuous experiment analysis | Split into two paths: Binary outcome -> successes + total exposed -> conversion rate -> chi-squared-style significance test; Continuous outcome -> one metric value per user -> mean + standard deviation + count -> two-sample t-test; beneath both paths show final interpretation as statistical evidence + effect size + business meaning | Learner should notice that the SQL summary required depends on the type of outcome being measured]]

### Do not change the success metric after the result

Imagine:

```text
Variant improves onboarding completion.
Variant does not improve overall spend.
Among completers, control users spend more.
```

Which result determines success?

The answer depends on the hypothesis and primary metric that were defined before the experiment.

If the hypothesis was:

```text
improve onboarding completion
```

then completion is the primary test.

If the hypothesis was:

```text
improve revenue by increasing onboarding completion
```

then the revenue result matters directly.

Metric definition is part of experiment design, not a post-analysis decoration.

---

## 6. Validate variant assignment before trusting the result

Randomization is the foundation of experiment validity.

Before reading the outcome, profile the assignment data.

### Check variant sizes

```sql
SELECT
    variant,
    COUNT(DISTINCT user_id) AS users
FROM experiment_assignment
WHERE experiment_name = 'Onboarding'
GROUP BY variant;
```

Unequal groups are not automatically invalid.

But unexpected imbalance deserves investigation.

### Check users assigned to multiple variants

```sql
SELECT
    user_id,
    COUNT(DISTINCT variant) AS variants
FROM experiment_assignment
WHERE experiment_name = 'Onboarding'
GROUP BY user_id
HAVING COUNT(DISTINCT variant) > 1;
```

A user simultaneously appearing in control and treatment can contaminate the experiment.

### Check eligibility

An experiment may intend to target:

```text
new users only
```

while the assignment system accidentally includes all users.

SQL can restrict the analysis to intended eligible users:

```sql
JOIN users u
    ON a.user_id = u.user_id
WHERE u.created_at >= <eligibility cutoff>
```

But be careful.

Filtering after the fact does not repair every possible experimental flaw.

### Too few assigned users

If the sample is too small, the experiment may not have enough information to detect meaningful differences.

The correct response may be:

```text
continue or rerun the experiment
```

rather than force a conclusion.

### Nonrandom missing populations

Suppose older app versions cannot enter the experiment.

If those users systematically differ from included users, the final result may not generalize to the full user population.

Ask:

```text
Who was excluded?
Why?
How large is that group?
Is it behaviorally different?
```

### A/A tests

An **A/A test** assigns users into two randomized groups but gives both groups the same experience.

Expected result:

```text
no meaningful systematic difference
```

If the groups consistently differ, investigate:

- assignment logic;
- tracking;
- metric calculation;
- experiment infrastructure.

A/A tests are useful checks of the experimentation system itself.

---

## 7. Outliers can distort continuous experiment metrics

Continuous metrics often depend on averages.

A few extreme values can have a large influence.

Example:

```text
Control:
most users spend 0–20
one user spends 20,000

Variant:
most users spend 0–20
```

The single control user may dramatically change the mean.

### Apply anomaly-detection techniques

You can:

- inspect percentile distributions;
- calculate z-scores;
- compare means with and without extreme observations;
- winsorize;
- transform the metric if justified.

### Do not remove outliers only because they hurt the result

Ask:

```text
Is the value valid?
Is it part of the population the experiment was intended to affect?
Would the same rule be applied to both variants?
Was the handling strategy decided consistently?
```

### Convert a continuous metric into a binary metric when useful

Instead of:

```text
average spend
```

you might measure:

```text
did user purchase? yes/no
```

This answers a different question, but it may be less sensitive to a handful of huge purchases.

Another threshold metric could be:

```text
read at least 3 articles
used app at least twice this week
spent at least 100 EGP
```

The threshold must be meaningful, not chosen simply to manufacture significance.

---

## 8. Time boxing creates fair observation windows

Suppose an experiment runs for three weeks.

User A enters on day 1.

User B enters on day 20.

If you measure total purchases through day 21:

```text
User A had 21 days
User B had 1 day
```

That is not a fair comparison.

### Define a fixed window from assignment

Example:

```text
7 days after assignment
```

SQL pattern:

```sql
LEFT JOIN purchases p
    ON a.user_id = p.user_id
   AND p.purchase_time >= a.assignment_time
   AND p.purchase_time < a.assignment_time + INTERVAL '7 days'
```

Every user gets the same opportunity window.

### Choose the window based on behavior

Examples:

```text
ad click -> minutes or hours
checkout -> hours or days
purchase -> several days
subscription renewal -> much longer
```

A shorter window gives faster results but may miss behavior that normally takes longer.

A longer window is more complete but delays analysis.

### Wait until users have had the full window

If the metric is seven-day revenue, users assigned yesterday do not yet have a seven-day outcome.

Either:

- wait;
- exclude users who have not matured through the full window;
- or clearly mark their outcomes as incomplete.

Time-boxing logic should be part of the metric definition.

{{exercise:M01.L07.EX02}}

---

## 9. Repeated-exposure experiments require longer-term thinking

Some experiments are **one-and-done**.

Examples:

```text
signup flow
one-time registration
first onboarding
```

The user sees the treatment once.

Other experiments create **repeated exposure**.

Examples:

- navigation design;
- button placement;
- recommendation interface;
- recurring email campaigns;
- repeated promotions.

The user experiences the treatment many times.

### Novelty effect

A new interface can attract attention simply because it is new.

Initial behavior may increase even if the design is not actually better long term.

### Regression to the mean

An unusually high or low metric may move back toward a more typical level over time.

A treatment might produce:

```text
Week 1: large lift
Week 2: smaller lift
Week 4: nearly baseline
```

The important question is:

```text
What is the stable long-term effect?
```

### Allow enough time

For repeated exposure, measuring too early can mistake novelty for durable improvement.

The correct duration depends on the product and behavior.

### Long-term holdouts

A long-term holdout is a randomly selected group that does not receive the ongoing treatment.

For a marketing program:

```text
Treatment -> receives recurring campaigns
Holdout   -> receives no campaign
```

This helps estimate the cumulative incremental value of the whole program.

Do not substitute:

```text
people who opted out
```

for a randomized holdout.

Opt-out users are self-selected and may differ systematically.

### Cohort analysis can extend experiment analysis

You can follow control and treatment cohorts over weeks or months and compare:

- retention;
- cumulative revenue;
- repeated usage;
- long-term engagement.

Experimentation and cohort analysis often work together.

---

## 10. What SQL can—and cannot—rescue in a flawed experiment

Experiments cost:

- engineering time;
- design time;
- marketing effort;
- user exposure;
- opportunity cost.

So analysts naturally want to rescue imperfect experiments.

Sometimes that is possible.

Sometimes it is not.

### Potentially recoverable

Examples:

```text
too many users were assigned, but eligibility can be identified exactly
a known subset never had a chance to see the treatment
a small number of clearly invalid data rows can be corrected
```

SQL can sometimes define the correct analysis population.

### Potentially fatal

Examples:

```text
assignment was not random
control users received treatment
treatment users also appeared in control
tracking differs systematically by variant
```

If the experiment's causal foundation is broken, filtering cannot always restore it.

### Be explicit about limitations

Do not turn:

```text
we salvaged a usable subset
```

into:

```text
the original experiment was valid
```

Report:

- what went wrong;
- what was excluded;
- why the revised population is considered usable;
- what uncertainty remains.

---

## 11. When randomized experiments are not possible

Randomized experiments are not always feasible.

Reasons include:

- ethics;
- regulation;
- operational constraints;
- historical changes that already happened;
- outages or bugs;
- natural events;
- inability to withhold treatment.

In these cases, analysts can use weaker but still useful **quasi-experimental** approaches.

These attempt to construct treatment and comparison groups from observational data.

[[IMAGE_NEEDED: IMG-M01-L07-04 / Instructor Figure — Evidence ladder for causal analysis | Show randomized A/B test at the top as strongest causal design, then below it pre/post analysis, natural experiment, and threshold/RDD-style analysis; annotate that SQL can construct and summarize all groups, but confidence in causality weakens as random assignment disappears | Learner should notice that alternative analyses can provide evidence but do not automatically equal randomized causal proof]]

---

## 12. Pre/post analysis

A **pre/post analysis** compares behavior before and after a clearly timed change.

Example:

```text
Before:
old email opt-in design

After:
new regulated opt-in design
```

### Create synthetic variants

```sql
SELECT
    CASE
        WHEN created_at BETWEEN DATE '2026-01-01' AND DATE '2026-01-14'
            THEN 'pre'
        WHEN created_at BETWEEN DATE '2026-01-15' AND DATE '2026-01-28'
            THEN 'post'
    END AS variant,
    ...
FROM users;
```

### Use similar-length windows

If you compare:

```text
2 weeks before
```

use approximately:

```text
2 weeks after
```

so exposure opportunity is comparable.

You can repeat the analysis using:

```text
1-week window
2-week window
3-week window
4-week window
```

If the conclusion is stable across several reasonable windows, confidence improves.

### Main limitation

Many other things can change across time:

- seasonality;
- marketing;
- holidays;
- economic conditions;
- external events;
- product changes.

So:

```text
post != pre
```

does not prove:

```text
the target change caused the difference
```

Pre/post analysis can support a hypothesis, but causal evidence is weaker than randomized experimentation.

---

## 13. Natural experiments

A **natural experiment** occurs when different groups receive different experiences through a process that approximately resembles random exposure.

Examples:

- a software bug affects one country;
- an outage affects one region;
- a policy changes in one jurisdiction;
- a feature accidentally reaches one platform first.

### Requirements

You need:

1. a clearly exposed group;
2. a comparison group;
3. groups that are reasonably similar before the event.

### Choose the comparison group carefully

Do not automatically compare:

```text
affected country
```

to:

```text
everyone else
```

A better comparison may be a specific country with:

- similar user behavior;
- similar language;
- similar product penetration;
- similar demographics.

The hardest part is usually not the SQL.

It is justifying:

```text
Why is this comparison group credible?
```

### SQL still prepares the same outcome summaries

For binary outcomes:

```text
group
total exposed
successes
success rate
```

For continuous outcomes:

```text
group
count
mean
standard deviation
```

The statistical mechanics may resemble an A/B test, but the causal interpretation must be more cautious.

---

## 14. Analysis around a treatment threshold

Sometimes treatment is assigned using a threshold.

Examples:

```text
GPA >= threshold -> scholarship
income < threshold -> subsidy
churn score > threshold -> sales intervention
```

People immediately above and below the threshold may be quite similar.

This creates an opportunity to compare near-boundary groups.

The formal method discussed in the chapter is **regression discontinuity design (RDD)**.

### Basic intuition

Suppose treatment starts at score 80.

Instead of comparing:

```text
all people below 80
vs
all people above 80
```

compare:

```text
75–79.99
vs
80–84.99
```

Those populations may be more comparable.

### Bandwidth matters

How wide should the range be?

There is no universal answer.

You might compare:

```text
±5%
±7.5%
±10%
```

around the threshold.

If the conclusions are consistent across reasonable bands, confidence improves.

If they change substantially, the result may be inconclusive.

### Confounding still matters

Suppose high-risk customers receive:

```text
sales call
discount
special email
priority support
```

at the same threshold.

Then the observed effect cannot easily be attributed to only the sales call.

RDD-style analysis can strengthen observational evidence but still requires careful assumptions.

---

## 15. A practical experiment-analysis workflow

Use this sequence before declaring a winner.

### Step 1 — Write the hypothesis

Example:

```text
Reducing onboarding from six screens to four
will increase onboarding completion.
```

### Step 2 — Define the experimental unit

Examples:

```text
user
account
session
store
device
```

Do not mix units accidentally.

### Step 3 — Define the primary metric

Write the exact numerator, denominator, or per-unit measure.

Example:

```text
completion_rate =
users with onboarding_complete
/
all assigned eligible users
```

### Step 4 — Define guardrails

Examples:

```text
crash rate
page load time
refund rate
support contacts
```

### Step 5 — Validate assignment

Check:

- group sizes;
- duplicate assignments;
- users in multiple variants;
- eligibility;
- missing assignment data.

### Step 6 — Build one metric value per unit

Binary:

```text
success = 0 or 1 per user
```

Continuous:

```text
revenue = total revenue per user
```

### Step 7 — Apply a fair observation window

Use the assignment time as the start.

Ensure every analyzed unit has had enough time.

### Step 8 — Profile outliers

Especially for continuous metrics.

Do not manipulate them differently by variant.

### Step 9 — Produce statistical inputs

Binary:

```text
successes
total units
rate
```

Continuous:

```text
mean
standard deviation
count
```

### Step 10 — Evaluate statistical evidence

Use the appropriate statistical method for the outcome type.

### Step 11 — Interpret practical value

Ask:

```text
How large is the effect?
Does it matter to the business?
Did guardrails worsen?
```

### Step 12 — State the conclusion in the right strength

Good:

```text
The randomized variant increased onboarding completion in this experiment.
```

Too strong:

```text
This design will improve every future user metric.
```

### Step 13 — If the experiment was flawed, report the flaw

Do not hide:

- assignment problems;
- incomplete windows;
- exclusion rules;
- contamination;
- external events.

Good experiment analysis is as much about credibility as calculation.

{{exercise:M01.L07.EX03}}

---

## Important misconceptions

### Misconception 1

> If two metrics move together, one must cause the other.

Correlation can arise from reverse causality, common causes, feedback loops, or chance.

### Misconception 2

> More success metrics make an experiment more informative.

Too many comparisons increase the chance of finding apparently significant results by chance.

### Misconception 3

> Only users who performed the success action belong in the denominator.

The denominator usually includes all eligible assigned units, including failures.

### Misconception 4

> A statistically significant effect is automatically valuable.

A tiny effect can be statistically detectable but practically unimportant.

### Misconception 5

> A user with no purchases should simply remain `NULL` in spend-per-user analysis.

If zero purchases means zero spend, using `NULL` can incorrectly remove nonbuyers from the average.

### Misconception 6

> Filtering bad assignments always repairs a flawed experiment.

Some assignment failures destroy randomization and therefore causal validity.

### Misconception 7

> Repeated-exposure experiments should be analyzed as quickly as possible.

Early effects can reflect novelty rather than a durable behavior change.

### Misconception 8

> Pre/post analysis proves causality if the difference is statistically significant.

Without randomization, other time-varying factors may explain the change.

---

## Key terminology

| Term | Meaning |
|---|---|
| Experiment | Controlled comparison of different experiences |
| A/B test | Experiment comparing control with one or more variants |
| Hypothesis | Prediction about how a treatment will change behavior |
| Control | Baseline experience |
| Variant / treatment | Modified experience being tested |
| Experimental unit | Entity randomized into a variant, such as a user or account |
| Primary metric | Main outcome used to judge the hypothesis |
| Guardrail metric | Metric used to detect unintended harm |
| Random assignment | Allocation to variants by chance rather than user characteristics |
| Binary outcome | Outcome with two states such as success/failure |
| Continuous outcome | Numeric outcome that can take many values |
| Contingency table | Table of counts across categorical outcomes and variants |
| Chi-squared test | Statistical test used for categorical/binary-style comparisons |
| Two-sample t-test | Statistical test comparing means between two groups |
| Statistical significance | Evidence that an observed difference is unlikely under a specified null hypothesis |
| Effect size | Magnitude of the difference between groups |
| A/A test | Experiment infrastructure test where both randomized groups receive the same experience |
| Time boxing | Restricting outcome measurement to the same elapsed window after assignment |
| Novelty effect | Temporary behavior change caused by something being new |
| Regression to the mean | Tendency for unusually extreme measurements to move closer to typical levels |
| Holdout | Group intentionally not exposed to an ongoing treatment |
| Quasi-experiment | Nonrandomized design intended to approximate a controlled comparison |
| Pre/post analysis | Comparison of outcomes before and after a change |
| Natural experiment | Observational setting in which exposure differs in an approximately random way |
| Regression discontinuity design | Comparison of units just above and below a treatment threshold |
| Confounder | Variable related to both treatment/exposure and outcome that can distort interpretation |

---

## Self-check

Before continuing, make sure you can answer:

1. Why does correlation not prove causation?
2. What are the three core components required for an experiment?
3. Why should the primary metric be selected before viewing results?
4. What is a guardrail metric?
5. Why does a binary-outcome query usually require a `LEFT JOIN` from assignments to success events?
6. Why should continuous metrics be calculated at the experimental-unit level first?
7. Why should nonpurchasers often contribute zero to spend-per-user?
8. What inputs are needed for the chapter's binary significance workflow?
9. What inputs are needed for the chapter's continuous significance workflow?
10. What can an A/A test reveal?
11. Why can continuous outcomes be sensitive to outliers?
12. What problem does time boxing solve?
13. Why are repeated-exposure experiments vulnerable to novelty effects?
14. Why is an opt-out population not equivalent to a randomized holdout?
15. Why is pre/post analysis weaker for causal inference than an A/B test?
16. What makes a natural experiment comparison credible?
17. What is the intuition behind regression discontinuity design?

---

## Retain this idea

**A trustworthy experiment is designed before it is analyzed: define the hypothesis and metric, randomize correctly, give each unit a fair observation window, preserve failures in the denominator, calculate the metric at the right grain, and interpret statistical evidence together with effect size and business meaning.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "causality", "title": "Why experimentation matters: correlation is not causation", "order": 1},
            {"id": "experiment-anatomy", "title": "The three required parts of an experiment", "order": 2},
            {"id": "metrics", "title": "Primary metrics, guardrails, and the multiple-comparisons problem", "order": 3},
            {"id": "binary", "title": "Binary-outcome experiments", "order": 4},
            {"id": "continuous", "title": "Continuous-outcome experiments", "order": 5},
            {"id": "assignment-quality", "title": "Validate variant assignment before trusting the result", "order": 6},
            {"id": "outliers", "title": "Outliers can distort continuous experiment metrics", "order": 7},
            {"id": "time-boxing", "title": "Time boxing creates fair observation windows", "order": 8},
            {"id": "repeated-exposure", "title": "Repeated-exposure experiments require longer-term thinking", "order": 9},
            {"id": "when-experiments-fail", "title": "What SQL can—and cannot—rescue in a flawed experiment", "order": 10},
            {"id": "quasi-experiments", "title": "When randomized experiments are not possible", "order": 11},
            {"id": "pre-post", "title": "Pre/post analysis", "order": 12},
            {"id": "natural-experiment", "title": "Natural experiments", "order": 13},
            {"id": "threshold-analysis", "title": "Analysis around a treatment threshold", "order": 14},
            {"id": "workflow", "title": "A practical experiment-analysis workflow", "order": 15},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L07.EX01",

            "title": "Analyze a Binary Conversion Experiment",

            "lesson_code": "M01.L07",

            "section_id": "binary",

            "placement": "after_section",

            "description": (
                "Build the SQL summary required to compare conversion rates between "
                "control and treatment."
            ),

            "instructions": (
                "Assume `experiment_assignment(user_id, experiment_name, variant, assignment_time)` "
                "and `orders(user_id, order_time)`.\n"
                "1. Count all eligible users assigned to each variant.\n"
                "2. Count users who placed at least one order after assignment.\n"
                "3. Calculate conversion rate by variant.\n"
                "4. Explain why the assignment table must drive the denominator.\n"
                "5. Produce the success and total counts needed for a binary significance test.\n"
                "6. State one guardrail metric you would monitor."
            ),

            "expected_output": (
                "SQL or clear pseudocode returning variant, total_users, purchasers, "
                "conversion_rate, plus a brief interpretation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "ab-testing",
                "binary-metrics",
                "left-join",
                "conversion-rate",
            ],
        },

        {
            "id": "M01.L07.EX02",

            "title": "Add a Fair Seven-Day Revenue Window",

            "lesson_code": "M01.L07",

            "section_id": "time-boxing",

            "placement": "after_section",

            "description": (
                "Convert a biased cumulative-spend metric into a fair time-boxed "
                "experiment metric."
            ),

            "instructions": (
                "You have users assigned throughout a three-week experiment.\n"
                "1. Calculate revenue per user only during the first seven days after assignment.\n"
                "2. Include users with no purchases as zero revenue.\n"
                "3. Exclude or flag users who have not yet had seven full days of observation.\n"
                "4. Summarize count, mean revenue, and standard deviation by variant.\n"
                "5. Explain why using all revenue through the experiment end date would bias early entrants."
            ),

            "expected_output": (
                "A time-boxed SQL design that produces one seven-day revenue value per "
                "eligible user and correct summary statistics by variant."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "time-boxing",
                "continuous-metrics",
                "coalesce",
                "experimental-grain",
            ],
        },

        {
            "id": "M01.L07.EX03",

            "title": "Choose the Strongest Available Causal Design",

            "lesson_code": "M01.L07",

            "section_id": "workflow",

            "placement": "after_section",

            "description": (
                "Choose between a randomized experiment and quasi-experimental alternatives."
            ),

            "instructions": (
                "For each case, choose the strongest reasonable design and justify it:\n"
                "1. A new checkout button can be randomly shown to half of users.\n"
                "2. A pricing bug affected Canada for three days but not the United States.\n"
                "3. A regulation changed an opt-in default for everyone on one known date.\n"
                "4. Customers above a churn-risk score of 80 automatically receive a sales call.\n"
                "For each, choose A/B test, natural experiment, pre/post analysis, or "
                "threshold/RDD-style analysis, and state the biggest validity risk."
            ),

            "expected_output": (
                "Four design choices with a concise explanation of why each method fits "
                "and what limitation must be reported."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "causal-inference",
                "experiment-design",
                "quasi-experiments",
                "analytical-judgment",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L07.QZ01",

        "title": "Experiment Analysis — Knowledge Check",

        "lesson_code": "M01.L07",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L07.Q01",

                "section_id": "causality",

                "question": (
                    "If X and Y are correlated, which statement is correct?"
                ),

                "options": [
                    "X must cause Y",
                    "Y must cause X",
                    "Several causal structures or even chance could explain the relationship",
                    "Randomization is unnecessary",
                ],

                "correct": 2,

                "explanation": (
                    "Correlation alone cannot distinguish direct causality, reverse causality, "
                    "common causes, feedback loops, or random coincidence."
                ),
            },

            {
                "id": "M01.L07.Q02",

                "section_id": "metrics",

                "question": (
                    "Why should an experiment usually have only a small number of primary success metrics?"
                ),

                "options": [
                    "SQL supports only two metrics",
                    "Testing many metrics increases the chance of finding an apparently significant result by chance",
                    "Guardrail metrics cannot be calculated",
                    "Continuous metrics are invalid",
                ],

                "correct": 1,

                "explanation": (
                    "This is the multiple-comparisons problem: more tests create more "
                    "opportunities for chance findings."
                ),
            },

            {
                "id": "M01.L07.Q03",

                "section_id": "binary",

                "question": (
                    "Why should a binary conversion query generally start from experiment assignments and LEFT JOIN the success event?"
                ),

                "options": [
                    "To keep users who did not convert in the denominator",
                    "To remove the control group",
                    "To guarantee statistical significance",
                    "To calculate a standard deviation",
                ],

                "correct": 0,

                "explanation": (
                    "Failures are part of the assigned population and must remain in the "
                    "denominator when calculating conversion."
                ),
            },

            {
                "id": "M01.L07.Q04",

                "section_id": "continuous",

                "question": (
                    "Why should purchase rows be aggregated to one spend value per user before comparing experiment variants?"
                ),

                "options": [
                    "The user is the experimental unit, so each user should contribute one outcome value",
                    "SQL cannot average purchase rows",
                    "Purchases are binary outcomes",
                    "It removes all outliers",
                ],

                "correct": 0,

                "explanation": (
                    "Experiment outcomes should be measured at the same grain as the "
                    "randomized experimental unit unless the design specifies otherwise."
                ),
            },

            {
                "id": "M01.L07.Q05",

                "section_id": "assignment-quality",

                "question": (
                    "What does an A/A test primarily help validate?"
                ),

                "options": [
                    "Whether two different treatments have equal business value",
                    "Whether random assignment, tracking, and analysis infrastructure behave as expected",
                    "Whether a continuous metric has outliers",
                    "Whether a pre/post design is causal",
                ],

                "correct": 1,

                "explanation": (
                    "Both groups receive the same experience, so persistent differences can "
                    "signal assignment, tracking, or analysis problems."
                ),
            },

            {
                "id": "M01.L07.Q06",

                "section_id": "time-boxing",

                "question": (
                    "What problem does time boxing solve?"
                ),

                "options": [
                    "Users entering earlier otherwise receive longer opportunity to generate outcomes",
                    "It makes the treatment random",
                    "It removes multiple comparisons",
                    "It converts a continuous metric to binary",
                ],

                "correct": 0,

                "explanation": (
                    "A fixed elapsed window after assignment gives analyzed units comparable "
                    "opportunity to produce the outcome."
                ),
            },

            {
                "id": "M01.L07.Q07",

                "section_id": "repeated-exposure",

                "question": (
                    "Why can evaluating a repeated-exposure experiment too early be misleading?"
                ),

                "options": [
                    "The metric cannot be calculated with SQL",
                    "Novelty can cause a temporary behavior change that later fades",
                    "Control users always churn first",
                    "All repeated-exposure experiments require one year",
                ],

                "correct": 1,

                "explanation": (
                    "Initial attention to a new experience may not represent the stable "
                    "long-term effect."
                ),
            },

            {
                "id": "M01.L07.Q08",

                "section_id": "pre-post",

                "question": (
                    "What is the main causal limitation of pre/post analysis?"
                ),

                "options": [
                    "Before and after periods cannot contain users",
                    "Other changes over time may explain the observed difference",
                    "It cannot calculate rates",
                    "It always requires a natural disaster",
                ],

                "correct": 1,

                "explanation": (
                    "Seasonality, marketing, external events, and other changes can differ "
                    "between the before and after periods."
                ),
            },

            {
                "id": "M01.L07.Q09",

                "section_id": "threshold-analysis",

                "question": (
                    "What is the core intuition behind regression discontinuity design?"
                ),

                "options": [
                    "Compare entities near opposite sides of a treatment threshold because they may be otherwise similar",
                    "Randomly assign every entity",
                    "Compare the oldest and newest users",
                    "Remove all values near the threshold",
                ],

                "correct": 0,

                "explanation": (
                    "Units just above and below a threshold may be much more comparable "
                    "than the full treated and untreated populations."
                ),
            },

            {
                "id": "M01.L07.Q10",

                "section_id": "workflow",

                "type": "open",

                "question": (
                    "An experiment shows a statistically significant improvement in its "
                    "primary metric but a tiny effect size and a meaningful decline in a "
                    "guardrail metric. Explain how you would present the result and decide "
                    "whether to ship the treatment."
                ),
            },
        ],

        "passing_score": 70,
    },
}
