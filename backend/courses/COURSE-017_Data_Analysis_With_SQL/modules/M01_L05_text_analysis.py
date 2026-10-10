"""M01.L05 — Text Analysis.

One source chapter -> one complete learner-facing lesson + essential inline Images +
inline Exercises + lesson Quiz.
Source alignment: Chapter 5, "Text Analysis".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build practical SQL analysis skills from data preparation and time-based "
    "reasoning through cohort analysis, text analysis, anomaly detection, and "
    "other common analytical workflows."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Text Analysis",

    "slug": "data-analysis-sql-m01-l05",

    "description": (
        "A practical introduction to text analysis with SQL: decide when SQL is "
        "the right tool, profile and parse semistructured text, standardize and "
        "convert values, search and categorize text with LIKE and IN, use regular "
        "expressions for flexible pattern matching, and construct or reshape text "
        "for downstream analysis."
    ),

    "order": 5,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "sql",
        "text-analysis",
        "string-functions",
        "text-parsing",
        "data-cleaning",
        "pattern-matching",
        "regular-expressions",
        "categorization",
        "data-preparation",
        "data-analysis",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
    ],

    # =======================================================================
    # ESSENTIAL IMAGE POLICY
    # =======================================================================
    #
    # Only figures that materially improve understanding are requested.
    # Frequency charts from the source chapter are intentionally omitted because
    # the underlying ideas are clearer from the SQL result tables themselves.
    #
    # Essential figures requested:
    # - IMG-M01-L05-01: choosing SQL vs search tools vs Python/NLP vs humans
    # - IMG-M01-L05-02: semistructured text -> parsed structured columns
    # - IMG-M01-L05-03: anatomy of a regex pattern
    # - IMG-M01-L05-04: text reshaping with string_agg and split-to-rows
    #

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Text Analysis",

        "content": """# Text Analysis

> **Course:** Data Analysis with SQL  
> **Lesson:** M01.L05  
> **Module:** Foundations of Data Analysis with SQL  
> **Source alignment:** Chapter 5, *Text Analysis*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what SQL is good at—and not good at—for text analysis.
- Distinguish structured, semistructured, and largely unstructured text.
- Profile text fields with length distributions, samples, and frequency counts.
- Parse overstuffed text fields using delimiters and functions such as `split_part`.
- Explain when fixed-position functions such as `left` and `right` are appropriate.
- Standardize capitalization, whitespace, spelling, and common variants.
- Safely cast parsed strings into dates, timestamps, or other data types.
- Search text with `LIKE`, `ILIKE`, wildcards, and negated patterns.
- Categorize text with `CASE`, binary flags, `IN`, and `NOT IN`.
- Explain when a rule-based SQL approach becomes difficult to maintain.
- Read and build useful regular expressions for analytical tasks.
- Use regex matching, extraction, and replacement to clean text.
- Construct new text with concatenation.
- Reshape text using string aggregation and string-to-row splitting.
- Remove stop words when building simple word-frequency analyses.
- Design a maintainable SQL text-analysis workflow for repeated use.

---

## 1. What text analysis means—and where SQL fits

Text is everywhere in analytical systems:

- product names;
- location descriptions;
- survey comments;
- support tickets;
- log messages;
- social posts;
- review text;
- free-form notes;
- semistructured application fields.

**Text analysis** means turning text into information that can be inspected, grouped, counted, compared, or otherwise used to answer a question.

There are two broad families of text analysis.

### Qualitative text analysis

The goal is to understand meaning, context, themes, and nuance.

Examples:

```text
Why are users frustrated with onboarding?
What themes appear in customer interviews?
How does the language in these reports differ?
```

Humans—or advanced NLP/LLM systems with suitable evaluation—are often better suited to this kind of task.

### Quantitative text analysis

The goal is to create structured or countable information.

Examples:

```text
How many tickets mention "refund"?
What percentage of reports mention "battery"?
Which cities appear most often?
How many rows belong to each parsed category?
```

This is where SQL can be very effective.

### Why SQL is useful

SQL is a strong choice when:

- the text already lives in a database;
- the task is rule based;
- you know what you want to search for;
- you need to clean or standardize many rows;
- you need to extract categories or fields;
- the final output will be counts, rates, groups, or other structured metrics.

For example:

```sql
SELECT COUNT(*)
FROM support_tickets
WHERE LOWER(message) LIKE '%refund%';
```

This is a clear SQL problem.

### When SQL is not the best choice

SQL becomes less attractive when the task is:

#### Open-ended interpretation

```text
Why are these users unhappy?
```

A fixed set of SQL rules may miss synonyms, sarcasm, context, and indirect language.

#### Low-latency full-text retrieval

If the application must instantly retrieve documents containing complex text patterns, specialized search systems such as Elasticsearch or Splunk may be more suitable.

#### Advanced NLP

Tasks such as:

- robust sentiment analysis;
- part-of-speech tagging;
- named-entity recognition;
- semantic similarity;
- text generation;
- learned classification;

are usually better handled with Python/NLP or machine-learning tooling.

### SQL is rule based

This is important.

If you write:

```sql
CASE
    WHEN LOWER(review) LIKE '%excellent%' THEN 'positive'
    WHEN LOWER(review) LIKE '%terrible%' THEN 'negative'
END
```

the database will apply exactly those rules.

It will not automatically learn that:

```text
"not excellent"
```

may be negative, or that:

```text
"surprisingly decent"
```

may be positive.

Rules are valuable because they are:

- transparent;
- testable;
- reproducible.

But they become harder to maintain as the number of special cases grows.

[[IMAGE_NEEDED: IMG-M01-L05-01 / Instructor Figure — Choosing a tool for text analysis | Show a decision map with four destinations: SQL for known rule-based extraction/cleaning/counting, search engines for fast full-text retrieval, Python/NLP for learned language tasks, and human qualitative review for small/open-ended interpretation tasks | Learner should notice that SQL is strongest when the target pattern and output structure are known in advance]]

---

## 2. Profile text before trying to clean it

Text columns can look simple while hiding a lot of variation.

Before writing complex parsing rules, inspect the data.

### Step 1 — Look at representative rows

```sql
SELECT description
FROM reports
LIMIT 20;
```

Do not immediately assume that the first few rows represent the whole table.

Look for:

- repeated labels;
- delimiters;
- inconsistent capitalization;
- missing pieces;
- extra whitespace;
- malformed values;
- very long records;
- unexpected symbols.

### Step 2 — Measure string length

Many databases provide `length`; some use `len`.

```sql
SELECT LENGTH(description)
FROM reports;
```

A distribution is more useful:

```sql
SELECT
    LENGTH(description) AS text_length,
    COUNT(*) AS records
FROM reports
GROUP BY 1
ORDER BY 1;
```

This can reveal:

- empty strings;
- unexpectedly tiny values;
- unusually large records;
- multiple structural formats.

### Step 3 — Count repeated values

For a categorical text field:

```sql
SELECT
    status_text,
    COUNT(*) AS records
FROM events
GROUP BY status_text
ORDER BY records DESC;
```

This often exposes differences such as:

```text
Active
ACTIVE
active
active 
```

which humans interpret as the same value but SQL may treat as separate strings.

### Structured vs semistructured vs unstructured

A useful mental model:

**Structured text**

```text
city = "Cairo"
status = "Active"
```

Each field already has a clear meaning.

**Semistructured text**

```text
Occurred: 2018-03-04
Location: Cairo
Shape: Light
Duration: 5 minutes
```

The text contains structure, but multiple attributes are packed together.

**Mostly unstructured text**

```text
"I was walking home and saw several bright lights..."
```

The meaning is present, but there are no reliable columns or delimiters.

The more structure the text already has, the more naturally SQL can work with it.

---

## 3. Parsing semistructured text into useful fields

**Parsing** means extracting useful pieces from a larger text value.

Suppose a column contains:

```text
Occurred: 2018-03-04 19:07 | Location: Cairo | Shape: Light | Duration: 5 minutes
```

but the desired output is:

```text
occurred              location   shape   duration
2018-03-04 19:07      Cairo      Light   5 minutes
```

[[IMAGE_NEEDED: IMG-M01-L05-02 / Instructor Figure — From overstuffed text to structured columns | Show one semistructured source string with labeled regions Occurred, Location, Shape, Duration on the left, arrows through Parse -> Clean -> Convert, and four typed columns on the right | Learner should notice that text preparation is a pipeline: identify boundaries, extract values, standardize them, then assign useful data types]]

### Start by defining the desired output

Before coding, write down the target fields.

For example:

```text
occurred
reported
posted
location
shape
duration
```

This keeps the parsing effort focused.

### Fixed-position extraction: `left` and `right`

If the position is truly fixed:

```sql
SELECT LEFT('ABC-12345', 3);
```

returns:

```text
ABC
```

and:

```sql
SELECT RIGHT('ABC-12345', 5);
```

returns:

```text
12345
```

These functions are simple and fast, but fragile when field lengths vary.

Imagine dates such as:

```text
3/4/2018
10/16/2017
```

The number of characters changes, so fixed character positions are unreliable.

### Delimiter-based extraction

When the text has labels or separators, split on meaningful boundaries.

In PostgreSQL:

```sql
split_part(string, delimiter, index)
```

Example:

```sql
SELECT SPLIT_PART(
    'Location: Cairo | Shape: Light',
    ' | ',
    1
);
```

returns:

```text
Location: Cairo
```

Then split again:

```sql
SELECT SPLIT_PART(
    SPLIT_PART(
        'Location: Cairo | Shape: Light',
        ' | ',
        1
    ),
    'Location: ',
    2
);
```

returns:

```text
Cairo
```

### Nesting parsing functions

Real-world parsing often requires multiple steps:

```text
1. isolate the broad region;
2. remove the label;
3. remove an optional trailing region;
4. clean whitespace;
5. convert the data type.
```

A nested query can make this easier to debug:

```sql
WITH parsed AS (
    SELECT
        SPLIT_PART(
            SPLIT_PART(raw_text, ' | Shape:', 1),
            'Location: ',
            2
        ) AS location
    FROM raw_reports
)
SELECT TRIM(location)
FROM parsed;
```

### Why parsing usually takes several iterations

A rule that works on 100 rows may fail on row 50,000.

Possible exceptions include:

- missing labels;
- extra delimiters;
- alternative spelling;
- incomplete dates;
- blank values;
- text entered in an unexpected order.

A good parsing workflow is iterative:

```text
inspect
-> write a rule
-> test
-> profile failures
-> adjust
-> test again
```

The goal is not clever SQL.

The goal is **reliable structure**.

{{exercise:M01.L05.EX01}}

---

## 4. Clean and standardize parsed text

Once a value has been extracted, it may still be inconsistent.

SQL provides several simple but powerful transformation functions.

### Capitalization

```sql
UPPER(text)
LOWER(text)
```

Example:

```sql
SELECT LOWER('CaLiForNiA');
```

returns:

```text
california
```

Some databases also support:

```sql
INITCAP(text)
```

which converts:

```text
golden gate bridge
```

to:

```text
Golden Gate Bridge
```

### Why case normalization matters

These values:

```text
Triangle
TRIANGLE
triangle
TriAngle
```

may represent the same category.

Without normalization:

```sql
GROUP BY shape
```

can count them separately.

A common pattern is:

```sql
SELECT
    LOWER(TRIM(shape)) AS shape_clean,
    COUNT(*)
FROM reports
GROUP BY 1;
```

### Whitespace

Use `trim` to remove unwanted leading and trailing characters:

```sql
SELECT TRIM('   Cairo   ');
```

returns:

```text
Cairo
```

You may also encounter database-specific variants such as:

```text
LTRIM
RTRIM
TRIM(LEADING ...)
TRIM(TRAILING ...)
```

### Replacing known values

`replace` is useful when a specific string should be changed:

```sql
SELECT REPLACE(
    'Tombstone (outside of)',
    'outside of',
    'near'
);
```

Multiple replacements can be nested:

```sql
REPLACE(
    REPLACE(location, 'close to', 'near'),
    'outside of',
    'near'
)
```

### Standardization is analytical work

Do not automatically remove every difference.

For example:

```text
10 minutes+
10 minutes?
10 minutes
```

The `+` and `?` may communicate uncertainty.

You need to decide whether that information is:

- irrelevant noise;
- useful metadata;
- a separate quality flag.

Cleaning is not merely cosmetic. It changes the meaning available for analysis.

---

## 5. Convert parsed strings into useful data types safely

A parsed value may still be text even when it represents a date or number.

Example:

```text
"2018-03-04 19:07"
```

should normally become a timestamp.

### Casting

Common approaches include:

```sql
CAST(value AS timestamp)
```

or, in PostgreSQL:

```sql
value::timestamp
```

Example:

```sql
SELECT '2018-03-04 19:07'::timestamp;
```

### The danger of malformed strings

A cast can fail if a row contains:

```text
''
'unknown'
'12:30'
'not provided'
```

A single bad value may cause the entire query to fail.

### Validate before casting

One approach is:

```sql
CASE
    WHEN parsed_date = '' THEN NULL
    WHEN LENGTH(parsed_date) < 8 THEN NULL
    ELSE parsed_date::timestamp
END
```

The exact validation rule depends on the data.

The important pattern is:

```text
parse
-> validate
-> convert
```

not:

```text
parse
-> blindly cast
```

### Empty string is not always the same as `NULL`

A database may distinguish:

```text
''
```

from:

```text
NULL
```

The first is a real string of length zero.

The second means that no value exists.

This distinction matters when:

- casting;
- counting;
- filtering;
- joining;
- applying text functions.

---

## 6. Search text with `LIKE`, `ILIKE`, and wildcards

When you know the text pattern you are looking for, `LIKE` is one of the simplest tools.

### `%` wildcard

`%` matches zero or more characters.

```sql
WHERE LOWER(description) LIKE '%battery%'
```

This finds:

```text
battery
short battery life
battery was overheating
```

### `_` wildcard

`_` matches exactly one character.

For example:

```sql
LIKE 'A_C'
```

can match:

```text
ABC
A7C
A-C
```

but not:

```text
AC
ABBC
```

### Case sensitivity

Case behavior varies by database and collation.

A portable strategy is:

```sql
WHERE LOWER(description) LIKE '%wife%'
```

PostgreSQL also supports:

```sql
WHERE description ILIKE '%wife%'
```

for case-insensitive matching.

### Negation

```sql
WHERE LOWER(description) NOT LIKE '%wife%'
```

### Multiple conditions

```sql
WHERE LOWER(description) LIKE '%refund%'
   OR LOWER(description) LIKE '%cancel%'
```

Be careful when combining `AND` and `OR`.

Compare:

```sql
WHERE condition_a
   OR condition_b
  AND condition_c
```

with:

```sql
WHERE (condition_a OR condition_b)
  AND condition_c
```

Parentheses make the intended logic explicit.

### Pattern matching is useful in several SQL clauses

You can use it for:

**Filtering**

```sql
WHERE description ILIKE '%refund%'
```

**Categorization**

```sql
CASE
    WHEN description ILIKE '%driving%' THEN 'driving'
    WHEN description ILIKE '%walking%' THEN 'walking'
    ELSE 'other'
END
```

**Conditional aggregation**

```sql
COUNT(
    CASE
        WHEN description ILIKE '%refund%' THEN 1
    END
)
```

These patterns turn text into measurable data.

---

## 7. Categorize text carefully: one label or many flags?

Suppose a description can mention:

```text
driving
walking
running
cycling
```

A single `CASE` can assign one label:

```sql
CASE
    WHEN description ILIKE '%driving%' THEN 'driving'
    WHEN description ILIKE '%walking%' THEN 'walking'
    WHEN description ILIKE '%running%' THEN 'running'
    WHEN description ILIKE '%cycling%' THEN 'cycling'
    ELSE 'none'
END
```

But `CASE` stops at the first matching branch.

If a row contains both:

```text
driving
walking
```

only the first matching label is returned.

### Use separate flags for multi-label data

```sql
SELECT
    description ILIKE '%north%' AS mentions_north,
    description ILIKE '%south%' AS mentions_south,
    description ILIKE '%east%' AS mentions_east,
    description ILIKE '%west%' AS mentions_west
FROM reports;
```

Now one row can belong to several categories.

This is useful for:

- keywords;
- issue tags;
- topics;
- directions;
- product features;
- symptoms;
- complaint categories.

### Rule order matters

If categories overlap:

```text
"payment failed"
"payment"
```

put the more specific rule first:

```sql
CASE
    WHEN text ILIKE '%payment failed%' THEN 'payment_failure'
    WHEN text ILIKE '%payment%' THEN 'payment_general'
END
```

This is another reason large rule sets can become difficult to maintain.

---

## 8. Use `IN` and `NOT IN` for known exact sets

Sometimes pattern matching is unnecessary.

Suppose the first word has already been extracted:

```text
Red
Orange
Yellow
Green
Blue
Purple
White
```

Instead of:

```sql
WHERE first_word = 'Red'
   OR first_word = 'Orange'
   OR first_word = 'Yellow'
   OR first_word = 'Green'
```

use:

```sql
WHERE first_word IN (
    'Red',
    'Orange',
    'Yellow',
    'Green',
    'Blue',
    'Purple',
    'White'
);
```

This is usually:

- shorter;
- easier to read;
- easier to maintain;
- less error-prone.

### Combine exact and pattern rules

```sql
CASE
    WHEN LOWER(first_word) IN (
        'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'white'
    ) THEN 'color'

    WHEN LOWER(first_word) IN (
        'round', 'circular', 'oval', 'cigar'
    ) THEN 'shape'

    WHEN LOWER(first_word) LIKE 'triang%' THEN 'shape'

    WHEN LOWER(first_word) LIKE 'hover%' THEN 'motion'

    ELSE 'other'
END
```

This illustrates an important principle:

> Use the simplest rule that correctly captures the pattern.

Do not reach for regex when an exact match or `LIKE` is enough.

---

## 9. Regular expressions: a compact language for text patterns

A **regular expression**, or **regex**, describes a text pattern.

Regex becomes useful when the pattern is more flexible than a simple wildcard search.

For example:

```text
one or more digits
followed by a space
followed by "light" or "lights"
```

can be represented with a compact pattern.

### Database support varies

PostgreSQL includes POSIX-style regex operators such as:

```text
~     case-sensitive match
~*    case-insensitive match
!~    case-sensitive non-match
!~*   case-insensitive non-match
```

Other databases may use functions such as:

```text
REGEXP_LIKE
RLIKE
REGEXP_SUBSTR
REGEXP_REPLACE
```

The exact syntax varies, but the pattern concepts are transferable.

### Core regex building blocks

#### Literal text

```regex
data
```

matches the text `data`.

#### `.` — any single character

```regex
c.t
```

can match:

```text
cat
cot
c7t
```

#### Character set

```regex
[abc]
```

matches one character that is `a`, `b`, or `c`.

#### Character range

```regex
[0-9]
```

matches one digit.

```regex
[a-z]
```

matches one lowercase letter.

```regex
[A-Za-z0-9]
```

matches a letter or digit.

#### Repetition

```regex
[0-9]+
```

means:

```text
one or more digits
```

```regex
[0-9]*
```

means:

```text
zero or more digits
```

```regex
[0-9]?
```

means:

```text
zero or one digit
```

```regex
[0-9]{3}
```

means:

```text
exactly three digits
```

```regex
[0-9]{3,5}
```

means:

```text
between three and five digits
```

#### Whitespace

```regex
\\s
```

matches whitespace.

```regex
\\s+
```

matches one or more whitespace characters.

#### Grouping

```regex
([0-9]{2}[a-z]){3}
```

means:

```text
two digits + one lowercase letter,
repeated three times
```

#### Escaping special characters

A backslash can make a special character literal.

For example:

```regex
\\?
```

matches an actual question mark.

### Anchors and boundaries

Regex implementations differ, but many provide ways to indicate:

- beginning of string;
- end of string;
- beginning of word;
- end of word.

Anchors are useful when:

```text
"car" anywhere
```

and:

```text
"car" at the beginning
```

should mean different things.

[[IMAGE_NEEDED: IMG-M01-L05-03 / Instructor Figure — Anatomy of a regular expression | Break the pattern `[0-9]+ light[s ,.]` into labeled colored blocks: `[0-9]` digit class, `+` one-or-more quantifier, literal space, `light` literal text, `[s ,.]` allowed following character; underneath show matching examples `3 lights`, `12 light,`, and a non-match `many lights` | Learner should notice that regex is built by combining small pattern primitives rather than memorizing an opaque string]]

### Learn regex incrementally

A good workflow is:

```text
start with literal text
-> add one flexible component
-> test
-> add another component
-> test again
```

Do not begin with a large unreadable regex.

---

## 10. Extract and standardize text with regex

Regex becomes especially useful when you want not only to find a row, but to extract the matching portion.

Suppose descriptions contain:

```text
Saw 3 lights above the road
There were 12 lights moving east
One bright object
```

A pattern such as:

```regex
[0-9]+ light[s ,.]
```

can locate rows with a numeric light count.

In PostgreSQL:

```sql
SELECT description
FROM reports
WHERE description ~ '[0-9]+ light[s ,.]';
```

### Extract the matching text

PostgreSQL offers `regexp_matches`.

A simplified example:

```sql
SELECT
    (REGEXP_MATCHES(
        description,
        '[0-9]+ light[s ,.]'
    ))[1] AS matched_text
FROM reports
WHERE description ~ '[0-9]+ light[s ,.]';
```

Other databases may offer functions such as:

```text
REGEXP_SUBSTR
```

instead.

Once extracted, the value can be parsed again:

```sql
SPLIT_PART(matched_text, ' ', 1)::int
```

to get the numeric count.

### Regex replacement

Text often contains many spelling variants:

```text
10 minute
10 minutes
10 mins
10 MINUTES
```

A long list of exact replacements is possible, but regex may express the family of spellings more compactly.

Conceptually:

```sql
REGEXP_REPLACE(
    duration,
    <pattern matching minute/minutes/mins>,
    'min'
)
```

can standardize these values.

### Preserve meaning while standardizing

If the original value is:

```text
10 minutes?
```

the question mark may express uncertainty.

If you normalize it to:

```text
10 min
```

you may lose information.

A better output may be:

```text
duration_value = 10
duration_unit = 'min'
duration_uncertain = TRUE
```

This is a useful analytical principle:

> Separate useful structure from uncertainty instead of deleting uncertainty blindly.

### Validate intermediate matches

When writing regex cleaning logic, return the intermediate matched text while developing:

```text
original_value
matched_text
clean_value
```

This makes mistakes visible before they become part of a production transformation.

{{exercise:M01.L05.EX02}}

---

## 11. Construct new text from existing values

Text analysis is not only about breaking strings apart.

SQL can also combine values into new strings.

### `concat`

```sql
SELECT CONCAT(
    city,
    ' - ',
    country
);
```

Example result:

```text
Cairo - Egypt
```

### `concat_ws`

Some databases support:

```sql
CONCAT_WS(' - ', city, country)
```

where the first argument is the separator.

### Concatenation operator

Many databases support:

```sql
city || ' - ' || country
```

SQL Server commonly uses `+` instead.

### Null behavior

Concatenation and null handling vary by database.

Use `coalesce` when necessary:

```sql
CONCAT(
    COALESCE(city, 'Unknown city'),
    ' - ',
    COALESCE(country, 'Unknown country')
)
```

### Dynamic summaries

Concatenation can generate report-friendly strings:

```sql
SELECT CONCAT(
    'There were ',
    COUNT(*),
    ' reports for ',
    category,
    '.'
)
FROM reports
GROUP BY category;
```

This is useful for:

- automated emails;
- exports;
- labels;
- dashboard annotations;
- simple report sentences.

It is still rule-based text generation, not learned natural-language generation.

---

## 12. Reshape text between rows and strings

Sometimes multiple rows need to become one text field.

At other times, one text field needs to become multiple rows.

These are opposite operations.

### Many rows -> one string

PostgreSQL provides `string_agg`:

```sql
SELECT
    customer_id,
    STRING_AGG(tag, ', ' ORDER BY tag) AS tags
FROM customer_tags
GROUP BY customer_id;
```

Input:

```text
customer_id   tag
42            analytics
42            python
42            sql
```

Output:

```text
42   analytics, python, sql
```

Equivalent functions in other systems may include:

```text
GROUP_CONCAT
LISTAGG
```

### One string -> many rows

PostgreSQL provides functions such as:

```sql
REGEXP_SPLIT_TO_TABLE(
    'Red, Orange, Yellow, Green',
    ', '
);
```

Output:

```text
Red
Orange
Yellow
Green
```

Other databases may provide:

```text
SPLIT_TO_TABLE
STRING_SPLIT
```

or other equivalents.

[[IMAGE_NEEDED: IMG-M01-L05-04 / Instructor Figure — Reshaping text in both directions | Left side show three rows for one customer with tags `analytics`, `python`, `sql` flowing through `string_agg` into one comma-separated field; right side show one sentence or comma-separated string flowing through split-to-rows into multiple records | Learner should notice that text can be aggregated like numeric data or exploded into row-level tokens depending on the analysis grain needed]]

### Word-frequency analysis

Splitting text into words makes simple frequency analysis possible:

```sql
SELECT
    word,
    COUNT(*) AS frequency
FROM (
    SELECT
        REGEXP_SPLIT_TO_TABLE(
            LOWER(description),
            '\\s+'
        ) AS word
    FROM reports
) words
GROUP BY word
ORDER BY frequency DESC;
```

The most common words will often be uninformative:

```text
the
and
a
to
```

These are called **stop words**.

### Remove stop words

Suppose a table contains:

```text
stop_words
----------
the
and
a
to
of
...
```

Then:

```sql
SELECT
    w.word,
    COUNT(*) AS frequency
FROM (
    SELECT
        REGEXP_SPLIT_TO_TABLE(
            LOWER(description),
            '\\s+'
        ) AS word
    FROM reports
) w
LEFT JOIN stop_words s
    ON w.word = s.stop_word
WHERE s.stop_word IS NULL
GROUP BY w.word
ORDER BY frequency DESC;
```

This gives a more meaningful vocabulary profile.

### Limits of simple word counts

A word-frequency table does not understand:

- word meaning;
- phrases;
- negation;
- synonyms;
- context.

For example:

```text
"not good"
```

contains the word:

```text
good
```

but the sentiment is not positive.

Word counts are exploratory signals, not full language understanding.

---

## 13. A practical workflow for real text-analysis projects

Text analysis becomes much easier when it is approached systematically.

### Step 1 — Define the question

Avoid:

```text
Analyze this text.
```

Prefer:

```text
How many support tickets mention billing problems?
```

or:

```text
Extract the location and duration from this semistructured field.
```

### Step 2 — Decide whether SQL is the right tool

Use SQL when:

```text
the pattern is known
+ data is already in the database
+ output is structured/countable
```

Consider other tools when:

```text
the task requires semantic interpretation
or fast search at application scale
or advanced NLP
```

### Step 3 — Profile the source

Inspect:

- samples;
- length distribution;
- nulls;
- empty strings;
- common values;
- outliers;
- malformed rows.

### Step 4 — Parse before transforming

Separate the tasks mentally:

```text
extract the target
-> clean it
-> validate it
-> cast it
```

### Step 5 — Prefer simple rules

Use:

```text
IN
```

before a huge `OR` chain.

Use:

```text
LIKE
```

before regex when it is sufficient.

Use regex only when the pattern genuinely requires it.

### Step 6 — Validate across the full dataset

A parsing rule that works on a few examples may still fail in production.

Create quality checks such as:

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(parsed_date) AS valid_dates,
    COUNT(*) - COUNT(parsed_date) AS failed_dates
FROM parsed_data;
```

### Step 7 — Keep the raw value

Do not throw away the original field too early.

A useful transformation table often contains:

```text
raw_text
parsed_value
clean_value
quality_flag
```

This makes debugging possible.

### Step 8 — Promote repeated logic into the pipeline

If the analysis will be rerun:

```text
raw source
-> repeatable parsing/cleaning
-> structured table/view
-> downstream analysis
```

is usually better than copying a large nested query into every report.

### Step 9 — Document rule assumptions

For example:

```text
Rule:
anything beginning with "triang" is categorized as Shape.

Known limitation:
may classify unrelated words beginning with the same letters.
```

This makes rule-based systems maintainable.

---

## Important misconceptions

### Misconception 1

> SQL is only useful for numerical data.

SQL has extensive string functions and is highly useful for structured and rule-based text processing.

### Misconception 2

> If parsing works on five sample rows, it is finished.

Real data usually contains exceptions. Always validate the rule against the full dataset.

### Misconception 3

> `LIKE '%good%'` is sentiment analysis.

It is only a string rule. It does not understand negation, context, irony, or synonyms.

### Misconception 4

> Regex is always better than `LIKE`.

Regex is more expressive, but also harder to read and maintain. Use the simplest correct tool.

### Misconception 5

> Cleaning means deleting unusual characters.

An unusual character may encode uncertainty or other useful information.

### Misconception 6

> A word-frequency table understands what the text means.

Frequency counts reveal repetition, not semantics.

---

## Key terminology

| Term | Meaning |
|---|---|
| Text analysis | Deriving structured information or insight from text |
| Qualitative analysis | Human- or context-oriented interpretation of meaning and themes |
| Quantitative text analysis | Converting text into countable or measurable information |
| Structured text | Text already stored in fields with clear meanings |
| Semistructured text | Text containing recognizable structure that still requires parsing |
| Unstructured text | Free-form text without reliable field boundaries |
| Parsing | Extracting a useful piece from a larger text value |
| Delimiter | Character or string that marks boundaries between parts |
| Standardization | Converting equivalent values into a consistent representation |
| Wildcard | Symbol representing one or more unspecified characters in a pattern |
| `LIKE` | SQL pattern-matching operator |
| `ILIKE` | Case-insensitive pattern matching in supporting databases |
| Regex | Language for describing flexible text patterns |
| Character class | Regex expression describing allowed characters, such as `[0-9]` |
| Quantifier | Regex symbol specifying repetition, such as `+`, `*`, or `{3}` |
| `regexp_replace` | Regex-aware text replacement function in supporting databases |
| Concatenation | Combining text values into one string |
| String aggregation | Combining text from multiple rows into one field |
| Tokenization | Splitting text into smaller units such as words |
| Stop word | Very common word often removed from simple frequency analyses |
| Rule-based system | Logic that follows explicitly written rules rather than learning patterns from data |

---

## Self-check

Before continuing, make sure you can answer:

1. What kinds of text-analysis tasks are a good fit for SQL?
2. When would Python/NLP or a search engine be a better choice?
3. Why should text be profiled before parsing rules are written?
4. When are `left` and `right` safer than delimiter-based parsing, and when are they more fragile?
5. What is the difference between parsing and transformation?
6. Why should values be validated before casting them?
7. What do `%` and `_` mean in a `LIKE` pattern?
8. Why can a single `CASE` lose information when multiple categories can occur in one row?
9. When is `IN` better than a collection of `OR` expressions?
10. What does `[0-9]+` mean in regex?
11. Why is regex not automatically better than `LIKE`?
12. What is the purpose of `regexp_replace`?
13. What is the difference between `string_agg` and a split-to-table function?
14. Why are stop words commonly removed from word-frequency analysis?
15. Why should the raw text often be preserved alongside cleaned outputs?

---

## Retain this idea

**SQL text analysis works best when you can describe the task as explicit, testable rules: profile the raw text, extract stable structure, standardize carefully, validate before converting data types, and use increasingly powerful pattern tools only as the problem requires.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "sql-fit", "title": "What text analysis means—and where SQL fits", "order": 1},
            {"id": "profiling-text", "title": "Profile text before trying to clean it", "order": 2},
            {"id": "parsing", "title": "Parsing semistructured text into useful fields", "order": 3},
            {"id": "transformations", "title": "Clean and standardize parsed text", "order": 4},
            {"id": "safe-conversion", "title": "Convert parsed strings into useful data types safely", "order": 5},
            {"id": "like-search", "title": "Search text with LIKE, ILIKE, and wildcards", "order": 6},
            {"id": "categorization", "title": "Categorize text carefully: one label or many flags?", "order": 7},
            {"id": "exact-matches", "title": "Use IN and NOT IN for known exact sets", "order": 8},
            {"id": "regex-foundations", "title": "Regular expressions: a compact language for text patterns", "order": 9},
            {"id": "regex-extract-replace", "title": "Extract and standardize text with regex", "order": 10},
            {"id": "construct-text", "title": "Construct new text from existing values", "order": 11},
            {"id": "reshape-text", "title": "Reshape text between rows and strings", "order": 12},
            {"id": "production-workflow", "title": "A practical workflow for real text-analysis projects", "order": 13},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L05.EX01",

            "title": "Parse an Overstuffed Support Field",

            "lesson_code": "M01.L05",

            "section_id": "parsing",

            "placement": "after_section",

            "description": (
                "Turn a semistructured support-ticket field into clean analytical columns."
            ),

            "instructions": (
                "Assume a column contains values such as:\n"
                "`Opened: 2026-04-03 | Product: Mobile App | Issue: Login | Priority: High`\n"
                "1. List the four output columns you want.\n"
                "2. Write SQL or pseudocode using delimiter-based parsing to extract them.\n"
                "3. Apply `trim` and case standardization where appropriate.\n"
                "4. Convert `Opened` to a date.\n"
                "5. Describe how you would detect rows missing one of the expected labels."
            ),

            "expected_output": (
                "A parsing query or clear pseudocode that produces opened_date, product, "
                "issue, and priority, plus a validation strategy for malformed rows."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "text-parsing",
                "split-part",
                "data-cleaning",
                "type-conversion",
            ],
        },

        {
            "id": "M01.L05.EX02",

            "title": "Design a Regex Extraction Rule",

            "lesson_code": "M01.L05",

            "section_id": "regex-extract-replace",

            "placement": "after_section",

            "description": (
                "Build and explain a regex for extracting simple quantities from free text."
            ),

            "instructions": (
                "You have descriptions such as `Saw 4 lights`, `Observed 12 lights, moving east`, "
                "and `Many lights overhead`.\n"
                "1. Write a regex that matches a number followed by `light` or `lights`.\n"
                "2. Explain each component of the pattern.\n"
                "3. Show how you would extract the numeric part.\n"
                "4. Explain why `Many lights overhead` should not match the numeric rule.\n"
                "5. Describe one data-quality check you would run on unusually large extracted numbers."
            ),

            "expected_output": (
                "A regex pattern, a component-by-component explanation, and SQL or "
                "pseudocode for extracting and validating the numeric value."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "regex",
                "pattern-matching",
                "text-extraction",
                "data-quality",
            ],
        },

        {
            "id": "M01.L05.EX03",

            "title": "Turn Comments into an Analysis Dataset",

            "lesson_code": "M01.L05",

            "section_id": "production-workflow",

            "placement": "after_section",

            "description": (
                "Choose the right SQL text techniques for a small customer-feedback project."
            ),

            "instructions": (
                "A `feedback` table contains `comment`, `country`, and `created_at`.\n"
                "The business wants monthly counts of comments mentioning billing, login, "
                "performance, and cancellation issues.\n"
                "1. Decide whether a single CASE label or separate Boolean flags are better.\n"
                "2. Write example rules using `LIKE`, `ILIKE`, `IN`, or regex as appropriate.\n"
                "3. Aggregate the results by month.\n"
                "4. Explain two limitations of the rule-based analysis.\n"
                "5. State when you would recommend moving part of the task to NLP instead."
            ),

            "expected_output": (
                "A maintainable SQL classification design, monthly aggregation approach, "
                "and a short explanation of the limitations and possible NLP handoff."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "text-categorization",
                "pattern-matching",
                "conditional-aggregation",
                "tool-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L05.QZ01",

        "title": "Text Analysis — Knowledge Check",

        "lesson_code": "M01.L05",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",

                "section_id": "sql-fit",

                "question": (
                    "Which task is the strongest fit for SQL text analysis?"
                ),

                "options": [
                    "Explain the emotional meaning of thousands of open-ended interviews with no predefined categories",
                    "Count support tickets containing known billing-related phrases",
                    "Generate original marketing copy from examples",
                    "Infer sarcasm in social media posts",
                ],

                "correct": 1,

                "explanation": (
                    "SQL is strongest when the target patterns and structured output are "
                    "known in advance and can be expressed as explicit rules."
                ),
            },

            {
                "id": "M01.L05.Q02",

                "section_id": "profiling-text",

                "question": (
                    "Why is a string-length distribution useful before parsing a text field?"
                ),

                "options": [
                    "It automatically translates the text",
                    "It can reveal unusual, empty, or structurally different records",
                    "It replaces the need to inspect samples",
                    "It converts every value to a number",
                ],

                "correct": 1,

                "explanation": (
                    "Length distributions are a simple profiling tool that can expose "
                    "outliers and multiple structural formats."
                ),
            },

            {
                "id": "M01.L05.Q03",

                "section_id": "parsing",

                "question": (
                    "Why can fixed-position extraction fail for dates such as `3/4/2018` "
                    "and `10/16/2017`?"
                ),

                "options": [
                    "SQL cannot work with dates",
                    "The values have different character lengths",
                    "Dates cannot contain slashes",
                    "LEFT and RIGHT only work on numbers",
                ],

                "correct": 1,

                "explanation": (
                    "Variable-width month and day values shift character positions, making "
                    "fixed-position rules unreliable."
                ),
            },

            {
                "id": "M01.L05.Q04",

                "section_id": "safe-conversion",

                "question": (
                    "What is the safest general sequence for turning parsed text into a timestamp?"
                ),

                "options": [
                    "Cast -> parse -> validate",
                    "Validate -> delete -> parse",
                    "Parse -> validate -> cast",
                    "Aggregate -> cast -> parse",
                ],

                "correct": 2,

                "explanation": (
                    "Parsing isolates the candidate value, validation identifies malformed "
                    "values, and casting should happen only after the value is safe."
                ),
            },

            {
                "id": "M01.L05.Q05",

                "section_id": "like-search",

                "question": (
                    "What does `%` mean in a SQL LIKE pattern?"
                ),

                "options": [
                    "Exactly one character",
                    "Zero or more characters",
                    "A numeric value",
                    "End of the string",
                ],

                "correct": 1,

                "explanation": (
                    "`%` is the wildcard for zero or more characters in a LIKE pattern."
                ),
            },

            {
                "id": "M01.L05.Q06",

                "section_id": "categorization",

                "question": (
                    "Why might separate Boolean flags be better than one CASE category for text?"
                ),

                "options": [
                    "A row may legitimately match multiple categories",
                    "CASE cannot inspect text",
                    "Boolean values cannot be aggregated",
                    "Flags make all searches case sensitive",
                ],

                "correct": 0,

                "explanation": (
                    "A single CASE generally returns only the first matching category, while "
                    "independent flags can preserve multiple simultaneous matches."
                ),
            },

            {
                "id": "M01.L05.Q07",

                "section_id": "regex-foundations",

                "question": (
                    "What does the regex `[0-9]+` represent?"
                ),

                "options": [
                    "Exactly one letter",
                    "One or more digits",
                    "Zero or more spaces",
                    "A literal plus sign",
                ],

                "correct": 1,

                "explanation": (
                    "`[0-9]` matches a digit and `+` means one or more repetitions."
                ),
            },

            {
                "id": "M01.L05.Q08",

                "section_id": "regex-extract-replace",

                "question": (
                    "What is the main advantage of `regexp_replace` over a simple "
                    "`replace` call?"
                ),

                "options": [
                    "It can replace values that match a flexible pattern rather than one exact string",
                    "It automatically understands sentence meaning",
                    "It never requires testing",
                    "It works identically in every database",
                ],

                "correct": 0,

                "explanation": (
                    "Regex replacement can match families of text variations through a "
                    "pattern instead of requiring one exact source string."
                ),
            },

            {
                "id": "M01.L05.Q09",

                "section_id": "reshape-text",

                "question": (
                    "Which operation turns multiple row-level text values into one string?"
                ),

                "options": [
                    "STRING_AGG or an equivalent function",
                    "REGEXP_SPLIT_TO_TABLE",
                    "LIKE",
                    "CAST",
                ],

                "correct": 0,

                "explanation": (
                    "String aggregation combines values across rows; split-to-table performs "
                    "the opposite transformation."
                ),
            },

            {
                "id": "M01.L05.Q10",

                "section_id": "production-workflow",

                "type": "open",

                "question": (
                    "A rule-based SQL classifier has grown from 5 lines to 120 lines and "
                    "breaks whenever the application changes wording. Explain what this "
                    "suggests about maintainability and what options you would consider next."
                ),
            },
        ],

        "passing_score": 70,
    },
}
