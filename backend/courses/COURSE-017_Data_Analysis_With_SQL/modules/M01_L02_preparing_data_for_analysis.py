"""M01.L02 — Preparing Data for Analysis.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Source alignment: Chapter 2, "Preparing Data for Analysis".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build the core preparation skills needed before deeper SQL analysis: understand "
    "data types and sources, profile distributions and quality, clean and validate "
    "values, handle missing data, and shape rows and columns for downstream analysis."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Preparing Data for Analysis",

    "slug": "data-analysis-sql-m01-l02",

    "description": (
        "A practical, beginner-friendly guide to preparing analytical data with SQL: "
        "understanding types and structure, profiling distributions, detecting quality "
        "problems, cleaning and casting values, handling nulls and missing records, "
        "and reshaping data to the grain required by BI, statistics, or machine learning."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "data-preparation",
        "sql",
        "data-profiling",
        "data-quality",
        "data-cleaning",
        "window-functions",
        "data-shaping",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Preparing Data for Analysis",

        "content": (
            '# Preparing Data for Analysis\n'
            '\n'
            '> **Course:** Data Analysis with SQL  \n'
            '> **Lesson:** M01.L02  \n'
            '> **Module:** Foundations of Data Analysis with SQL  \n'
            '> **Source alignment:** Chapter 2, *Preparing Data for Analysis*. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain why data preparation is part of analysis rather than merely a task that happens before analysis.\n'
            '- Recognize common database data types and explain how type choices affect calculations and SQL functions.\n'
            '- Distinguish structured, semistructured, and unstructured data; quantitative and qualitative data; and first-, second-, and third-party data.\n'
            '- Recognize sparse data and explain why rare or missing observations require careful interpretation.\n'
            '- Read and write the core structure of an analytical SQL query using `SELECT`, `FROM`, joins, `WHERE`, and `GROUP BY`.\n'
            '- Use `LIMIT` or sampling while exploring large tables without mistaking a sample for the final answer.\n'
            '- Profile a new data set using frequencies, histograms, bins, n-tiles, and other distribution checks.\n'
            '- Use window functions such as `ntile`, `percent_rank`, `lag`, and `lead` for profiling and preparation.\n'
            '- Detect duplicates and distinguish duplicate source records from duplication created by a join.\n'
            '- Clean and enrich data with `CASE`, lookup tables, flags, type conversions, `coalesce`, and `nullif`.\n'
            '- Explain the difference between `NULL`, zero, and an empty string and handle each deliberately.\n'
            '- Diagnose missing data and choose among filtering, constant or derived replacements, and row-to-row imputation.\n'
            '- Use a date dimension or generated series to create missing dates or periods when the analysis requires them.\n'
            '- Choose an appropriate analytical grain and reshape data with aggregation, pivoting, unpivoting, `UNION ALL`, and database-specific helpers.\n'
            '- Shape output differently for BI, visualization, statistical analysis, and machine-learning workflows.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. Why data preparation is analytical work\n'
            '\n'
            'A common beginner expectation is that analysis starts when the “real” calculation starts. In practice, a large amount of analytical work happens earlier: understanding what the fields mean, checking whether the data is trustworthy, deciding which rows belong in the analysis, fixing or documenting irregular values, and arranging the data into a usable shape.\n'
            '\n'
            'That work is often called **data preparation**, **data wrangling**, **data munging**, or **data prep**.\n'
            '\n'
            'The important idea is that preparation is not mindless cleanup. Each preparation decision contains analytical assumptions.\n'
            '\n'
            'For example, suppose a sales table contains:\n'
            '\n'
            '```text\n'
            'order_id | status     | amount\n'
            '---------|------------|-------\n'
            '101      | completed  | 120\n'
            '102      | cancelled  | 95\n'
            '103      | completed  | NULL\n'
            '104      | test       | 500\n'
            '```\n'
            '\n'
            'Before calculating “total sales,” you already need to answer several questions:\n'
            '\n'
            '- Should cancelled orders be included?\n'
            '- Should test transactions be included?\n'
            '- Why is the amount missing for order `103`?\n'
            '- Does `NULL` mean zero, unknown, or a data-quality failure?\n'
            '- Is one row always one real order?\n'
            '\n'
            'If those questions are answered incorrectly, a perfectly valid `SUM()` can still produce a misleading answer.\n'
            '\n'
            'A useful preparation loop is:\n'
            '\n'
            '```text\n'
            'Understand -> Profile -> Question -> Clean -> Shape -> Check -> Analyze\n'
            '                         ^                         |\n'
            '                         |_________________________|\n'
            '```\n'
            '\n'
            'The loop matters because later steps often reveal problems that force you back to earlier ones.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-01 / Instructor Figure — Data preparation as an iterative analysis loop | Show Understand -> Profile -> Question -> Clean -> Shape -> Check -> Analyze in a loop, with arrows returning from Check and Analyze to Profile/Clean | Learner should notice that data preparation is iterative and analytical rather than a one-time preprocessing stage]]\n'
            '\n'
            '### Use a data dictionary when one exists\n'
            '\n'
            'A **data dictionary** documents fields, their meanings, possible values, collection rules, and relationships to other data. It can save hours of rediscovery.\n'
            '\n'
            'A good analyst still profiles the actual data even when documentation exists, because documentation can be incomplete or outdated. Profiling and documentation should reinforce each other:\n'
            '\n'
            '- the data dictionary tells you what should be present;\n'
            '- profiling tells you what is actually present;\n'
            '- discrepancies tell you what to investigate.\n'
            '\n'
            'When no useful dictionary exists, documenting what you learn during profiling is valuable work for both your team and your future self.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Database data types: what SQL thinks a value is\n'
            '\n'
            'Every database field has a **data type**. The type determines what values the field can store and which operations make sense.\n'
            '\n'
            'The most important families for analysis are strings, numerics, booleans, and date/time types.\n'
            '\n'
            '| Family | Common types | Typical values | Important analytical use |\n'
            '|---|---|---|---|\n'
            '| String | `CHAR`, `VARCHAR`, `TEXT` | names, codes, free text | grouping, parsing, matching |\n'
            '| Numeric | `INT`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL` | counts, prices, scores | arithmetic and aggregation |\n'
            '| Logical | `BOOLEAN` | `TRUE`, `FALSE` | flags and conditions |\n'
            '| Date/time | `DATE`, `TIMESTAMP`, `TIME` | dates and event times | time-series and cohort analysis |\n'
            '\n'
            'Some databases also support types such as JSON and geographic values.\n'
            '\n'
            "[[IMAGE_NEEDED: IMG-M01-L02-02 / Instructor Figure — Database data type map | Four main branches from a field: String, Numeric, Boolean, Date/Time, each with representative SQL types and one example value; show JSON/geographic as optional extended types | Learner should notice that a value's database type controls which operations and functions are valid]]\n"
            '\n'
            '### Strings\n'
            '\n'
            'Strings can contain letters, digits, symbols, whitespace, and other characters. A fixed-length `CHAR` may suit a consistently sized code, while `VARCHAR` allows variable length. Very long text may be stored in types such as `TEXT`, `CLOB`, or `BLOB`, depending on the database.\n'
            '\n'
            'A value that looks numeric is not necessarily numeric. For example:\n'
            '\n'
            '```text\n'
            "'$19.99'\n"
            '```\n'
            '\n'
            'is a string if the dollar sign is stored in the field. Mathematical aggregation cannot be trusted until the text is cleaned and converted.\n'
            '\n'
            '### Numeric values\n'
            '\n'
            'Integers store whole numbers. Decimal-capable types store values such as prices, ratios, and measurements.\n'
            '\n'
            'Be careful with arithmetic behavior. Some database systems treat integer division differently from decimal division. If both inputs are integers, a result you expected to be `2.5` may be reduced to an integer result unless you cast one input.\n'
            '\n'
            '### Booleans and flags\n'
            '\n'
            '`BOOLEAN` stores `TRUE` or `FALSE`. It is useful for properties such as:\n'
            '\n'
            '```text\n'
            'has_opened_email\n'
            'is_active\n'
            'is_test_account\n'
            '```\n'
            '\n'
            'Analytical data sets also commonly use `1` and `0` as flags when aggregation or modeling workflows benefit from numeric values.\n'
            '\n'
            '### Dates and timestamps\n'
            '\n'
            'Dates and timestamps should be stored in database date/time types when possible. That lets SQL use date-aware functions rather than forcing you to parse strings manually.\n'
            '\n'
            'Dates are central to later analyses because many business questions depend on:\n'
            '\n'
            '- when an event happened;\n'
            '- how long something took;\n'
            '- whether activity changed over time;\n'
            '- which cohort an entity belongs to.\n'
            '\n'
            '---\n'
            '\n'
            '## 3. How analysts classify data beyond database types\n'
            '\n'
            'Database types describe storage. Analysts also classify data conceptually because the source and structure influence how the data should be interpreted.\n'
            '\n'
            '### Structured, semistructured, and unstructured\n'
            '\n'
            '**Structured data** follows a predefined model. A relational table is the clearest example: each row represents an entity or event, and each column has a defined meaning and type.\n'
            '\n'
            '**Unstructured data** does not naturally fit a fixed rows-and-columns model. Examples include documents, images, audio, and video.\n'
            '\n'
            '**Semistructured data** sits between the two. An email, for example, contains structured metadata such as sender, recipient, subject, and timestamp, but also contains free-form body text.\n'
            '\n'
            "[[IMAGE_NEEDED: IMG-M01-L02-03 / Instructor Figure — Structured to unstructured spectrum | Three panels: structured relational table, semistructured email/JSON-like record with metadata plus free text, and unstructured image/audio/document; include an arrow from easiest to hardest for direct relational SQL querying | Learner should notice that 'unstructured' data may still contain structured metadata that SQL can use]]\n"
            '\n'
            '### Quantitative and qualitative\n'
            '\n'
            '**Quantitative data** represents measurable quantities. Examples include revenue, quantity, duration, weight, score, and counts.\n'
            '\n'
            '**Qualitative data** captures descriptions, opinions, or categories that are not inherently numerical. Survey comments, support messages, and social posts are examples.\n'
            '\n'
            'Analytical workflows often turn qualitative information into quantitative summaries. For example, an analyst might classify comments into categories and then count how frequently each category appears.\n'
            '\n'
            '### First-, second-, and third-party data\n'
            '\n'
            'The source of the data affects how much control you have over its generation and quality.\n'
            '\n'
            '| Category | Source | Typical analyst control |\n'
            '|---|---|---|\n'
            '| First-party | Collected by your organization | Highest |\n'
            '| Second-party | Generated by a vendor serving your organization | Moderate to low |\n'
            '| Third-party | Purchased or obtained from an external source | Usually low |\n'
            '\n'
            'A useful decision for vendor data is whether combining it with other organizational data creates enough analytical value to justify importing and maintaining it.\n'
            '\n'
            '### Sparse data\n'
            '\n'
            '**Sparse data** contains relatively little information inside a much larger possible space. A column may contain mostly nulls, or an event may occur only rarely.\n'
            '\n'
            'Sparse data deserves care because apparent patterns can be unstable when observations are rare. Possible responses include:\n'
            '\n'
            '- combining infrequent categories;\n'
            '- excluding a period that is too sparse for the question;\n'
            '- reporting descriptive statistics with a clear warning;\n'
            '- waiting for more observations.\n'
            '\n'
            'The correct response depends on why the data is sparse.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. The analytical SQL query skeleton\n'
            '\n'
            'Most analytical SQL queries are built from a small number of clauses.\n'
            '\n'
            '```sql\n'
            'SELECT ...\n'
            'FROM ...\n'
            'JOIN ... ON ...\n'
            'WHERE ...\n'
            'GROUP BY ...\n'
            '```\n'
            '\n'
            'Each clause has a distinct job.\n'
            '\n'
            '### `SELECT`: what should the result contain?\n'
            '\n'
            '`SELECT` defines the returned expressions. They may be:\n'
            '\n'
            '- fields;\n'
            '- aggregations such as `SUM()` or `COUNT()`;\n'
            '- calculations;\n'
            '- `CASE` expressions;\n'
            '- type conversions;\n'
            '- functions.\n'
            '\n'
            'Example:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    customer_id,\n'
            '    SUM(order_amount) AS total_spend\n'
            'FROM orders\n'
            'GROUP BY customer_id;\n'
            '```\n'
            '\n'
            '### `FROM`: where does the data come from?\n'
            '\n'
            '`FROM` can refer to:\n'
            '\n'
            '- a physical table;\n'
            '- a view;\n'
            '- a subquery.\n'
            '\n'
            'A subquery produces an intermediate result that the outer query treats like a table.\n'
            '\n'
            '### Joins: how do tables relate?\n'
            '\n'
            'A join combines rows using a relationship.\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    o.order_id,\n'
            '    c.customer_name\n'
            'FROM orders AS o\n'
            'JOIN customers AS c\n'
            '  ON o.customer_id = c.customer_id;\n'
            '```\n'
            '\n'
            'The important join types in this chapter are:\n'
            '\n'
            '- `INNER JOIN`: keep matches from both sides;\n'
            '- `LEFT JOIN`: keep every row from the left plus matching rows from the right;\n'
            '- `RIGHT JOIN`: the mirror of a left join;\n'
            '- `FULL OUTER JOIN`: keep rows from both sides whether matched or not.\n'
            '\n'
            'A join can also accidentally multiply rows. If one record on the left matches several records on the right, the result has several rows. This is not automatically wrong, but it must match the intended grain.\n'
            '\n'
            '### `WHERE`: which rows should remain?\n'
            '\n'
            '`WHERE` filters records before they reach the final result.\n'
            '\n'
            '```sql\n'
            "WHERE order_status = 'completed'\n"
            '```\n'
            '\n'
            '### `GROUP BY`: at what grain should aggregation happen?\n'
            '\n'
            'When a query contains an aggregation and also returns nonaggregated fields, those fields must generally appear in `GROUP BY`.\n'
            '\n'
            '```sql\n'
            'SELECT country, SUM(revenue)\n'
            'FROM orders\n'
            'GROUP BY country;\n'
            '```\n'
            '\n'
            'The output grain here is **one row per country**.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-04 / Instructor Figure — Anatomy of an analytical SQL query | A labeled SQL query with callouts showing SELECT = output columns, FROM/JOIN = source and relationships, WHERE = row filtering, GROUP BY = aggregation grain | Learner should notice that each clause answers a different question about the result set]]\n'
            '\n'
            '---\n'
            '\n'
            '## 5. Explore large tables safely: `LIMIT` and sampling\n'
            '\n'
            'Analytical tables can contain millions or billions of rows. During early exploration, returning or processing everything may be wasteful.\n'
            '\n'
            '### `LIMIT`\n'
            '\n'
            'A simple exploration query might be:\n'
            '\n'
            '```sql\n'
            'SELECT column_a, column_b\n'
            'FROM some_large_table\n'
            'LIMIT 1000;\n'
            '```\n'
            '\n'
            'The goal is not to make the final analysis smaller. The goal is to inspect enough data to understand structure and test logic quickly.\n'
            '\n'
            'SQL Server commonly uses `TOP` rather than `LIMIT`:\n'
            '\n'
            '```sql\n'
            'SELECT TOP 1000\n'
            '    column_a,\n'
            '    column_b\n'
            'FROM some_large_table;\n'
            '```\n'
            '\n'
            '### Sampling\n'
            '\n'
            'If an integer ID is reasonably distributed, a modulus can select a repeatable fraction:\n'
            '\n'
            '```sql\n'
            'WHERE mod(integer_order_id, 100) = 6\n'
            '```\n'
            '\n'
            'Conceptually, that chooses records whose remainder after division by `100` is `6`.\n'
            '\n'
            'A string ID can sometimes be sampled by a final character:\n'
            '\n'
            '```sql\n'
            "WHERE right(alphanum_order_id, 1) = 'B'\n"
            '```\n'
            '\n'
            'But any assumption about the distribution of IDs should be checked.\n'
            '\n'
            '### The important warning\n'
            '\n'
            'A limited or sampled subset may miss:\n'
            '\n'
            '- rare categories;\n'
            '- unusual values;\n'
            '- null patterns;\n'
            '- edge cases;\n'
            '- duplicates.\n'
            '\n'
            'Therefore:\n'
            '\n'
            '> **Use limits and samples to develop the query, not to silently define the final population.**\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-05 / Instructor Figure — Development sample versus final analysis | Show a very large table feeding a small development sample for fast query testing, then the validated query returning to the full required population for the final result | Learner should notice that sampling is a development technique and must not be confused with the final analysis population]]\n'
            '\n'
            '---\n'
            '\n'
            '## 6. Profiling: learn the shape of the data before trusting it\n'
            '\n'
            '**Profiling** means inspecting a data set to learn what is actually inside it.\n'
            '\n'
            'When opening a new analytical domain, build a mental model:\n'
            '\n'
            '1. What tables exist?\n'
            '2. What does one row in each table represent?\n'
            '3. How do the tables relate?\n'
            '4. Which values occur in important columns?\n'
            '5. Where are the nulls?\n'
            '6. Are there negative values, strange categories, or sudden changes?\n'
            '7. Is history preserved, or does the table only show current state?\n'
            '\n'
            'Profiling is closely related to exploratory data analysis.\n'
            '\n'
            '### Frequencies\n'
            '\n'
            'A frequency query answers: **How often does each value occur?**\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    fruit,\n'
            '    COUNT(*) AS quantity\n'
            'FROM fruit_inventory\n'
            'GROUP BY fruit;\n'
            '```\n'
            '\n'
            'This works for strings, numbers, dates, and booleans.\n'
            '\n'
            '{{image:fruit-frequency-plot}}\n'
            '\n'
            'A subtle but important distinction is:\n'
            '\n'
            '```sql\n'
            'COUNT(*)\n'
            '```\n'
            '\n'
            'versus:\n'
            '\n'
            '```sql\n'
            'COUNT(DISTINCT customer_id)\n'
            '```\n'
            '\n'
            'The first counts rows. The second counts unique customers. If a customer can appear more than once, these answer different questions.\n'
            '\n'
            '### Histograms\n'
            '\n'
            'A histogram shows the distribution of numeric values.\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    age,\n'
            '    COUNT(customer_id) AS customers\n'
            'FROM customers\n'
            'GROUP BY age;\n'
            '```\n'
            '\n'
            "{{image:customers-by-age-histogram}}\n"
            '\n'
            '### Profile an aggregation, not only raw fields\n'
            '\n'
            'Sometimes the quantity of interest must first be computed per entity.\n'
            '\n'
            'To profile **orders per customer**:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    orders,\n'
            '    COUNT(*) AS num_customers\n'
            'FROM (\n'
            '    SELECT\n'
            '        customer_id,\n'
            '        COUNT(order_id) AS orders\n'
            '    FROM orders\n'
            '    GROUP BY customer_id\n'
            ') AS a\n'
            'GROUP BY orders;\n'
            '```\n'
            '\n'
            'The inner query changes the grain to one row per customer. The outer query then counts how many customers fall at each order count.\n'
            '\n'
            'That pattern—**aggregate first, profile second**—is extremely useful.\n'
            '\n'
            '---\n'
            '\n'
            '## 7. Binning, n-tiles, and window functions\n'
            '\n'
            'Continuous numeric values often produce too many distinct values to interpret directly. **Binning** groups values into ranges.\n'
            '\n'
            '### Business-defined bins with `CASE`\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    CASE\n'
            "        WHEN order_amount <= 100 THEN 'up to 100'\n"
            "        WHEN order_amount <= 500 THEN '100 - 500'\n"
            "        ELSE '500+'\n"
            '    END AS amount_bin,\n'
            '    COUNT(*) AS orders\n'
            'FROM orders\n'
            'GROUP BY 1;\n'
            '```\n'
            '\n'
            '`CASE` conditions are evaluated in order. The first matching condition wins.\n'
            '\n'
            'That means boundary design matters.\n'
            '\n'
            'For a value of `80`:\n'
            '\n'
            '```text\n'
            'WHEN amount <= 100  -> matches\n'
            'WHEN amount <= 500  -> never reached\n'
            '```\n'
            '\n'
            '### Equal-width bins with rounding\n'
            '\n'
            'Rounding can reduce numeric precision:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    round(sales, -1) AS sales_bin,\n'
            '    COUNT(*) AS customers\n'
            'FROM customer_sales\n'
            'GROUP BY 1;\n'
            '```\n'
            '\n'
            'A negative precision can round to tens, hundreds, or larger units.\n'
            '\n'
            '### Logarithmic bins\n'
            '\n'
            'Logarithms are useful when values span very different scales. However, logarithms are not defined for zero or negative inputs in this context, so the analyst must check the input domain before applying them.\n'
            '\n'
            '### n-tiles\n'
            '\n'
            '`ntile` divides ordered rows into a requested number of groups.\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    customer_id,\n'
            '    order_amount,\n'
            '    ntile(10) OVER (ORDER BY order_amount) AS decile\n'
            'FROM orders;\n'
            '```\n'
            '\n'
            'The important difference from fixed-width bins is that n-tiles are based on **row counts after ordering**, not equal numeric ranges.\n'
            '\n'
            '### Window functions\n'
            '\n'
            '`ntile` belongs to the broader family of **window functions**.\n'
            '\n'
            'General form:\n'
            '\n'
            '```sql\n'
            'function_name(...) OVER (\n'
            '    PARTITION BY ...\n'
            '    ORDER BY ...\n'
            ')\n'
            '```\n'
            '\n'
            'A window function can calculate across related rows while still returning individual rows.\n'
            '\n'
            'For example:\n'
            '\n'
            '```sql\n'
            'ntile(10) OVER (ORDER BY order_amount)\n'
            '```\n'
            '\n'
            'ranks all rows into ten groups.\n'
            '\n'
            'With partitioning:\n'
            '\n'
            '```sql\n'
            'rank() OVER (\n'
            '    PARTITION BY country\n'
            '    ORDER BY revenue DESC\n'
            ')\n'
            '```\n'
            '\n'
            'the calculation restarts inside each country.\n'
            '\n'
            '`percent_rank()` returns a relative percentile-like position rather than a discrete tile.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-08 / Instructor Figure — Fixed bins versus n-tiles | Left panel shows equal-width numeric ranges containing uneven numbers of observations; right panel shows n-tiles containing roughly equal numbers of ordered observations but unequal numeric ranges | Learner should notice that equal-width bins and equal-count bins answer different questions]]\n'
            '\n'
            '{{exercise:M01.L02.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 8. Data quality and duplicate detection\n'
            '\n'
            'Good SQL cannot rescue a wrong assumption about the data.\n'
            '\n'
            'A strong quality check compares the data to **ground truth** when ground truth exists.\n'
            '\n'
            'Examples:\n'
            '\n'
            '- expected production row counts;\n'
            '- known monthly sales totals;\n'
            '- a trusted operational report;\n'
            '- a source system known to contain the authoritative value.\n'
            '\n'
            'When a result differs from expectation, investigate:\n'
            '\n'
            '- filters;\n'
            '- null handling;\n'
            '- spelling or category variations;\n'
            '- date boundaries;\n'
            '- join conditions;\n'
            '- duplication.\n'
            '\n'
            '### Detecting duplicates\n'
            '\n'
            'A duplicate means two or more rows repeat information that should not be repeated at the relevant grain.\n'
            '\n'
            'One direct check is:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    customer_id,\n'
            '    order_id,\n'
            '    COUNT(*) AS records\n'
            'FROM orders\n'
            'GROUP BY customer_id, order_id\n'
            'HAVING COUNT(*) > 1;\n'
            '```\n'
            '\n'
            'The phrase **at the relevant grain** is important. Two rows for the same customer may be correct if they represent two different orders. Two rows for the same `order_id` may be suspicious if an order should be unique.\n'
            '\n'
            '### Duplicates created by joins\n'
            '\n'
            'Not all duplicates originate in source data.\n'
            '\n'
            'Suppose one customer has three transactions:\n'
            '\n'
            '```text\n'
            'customers:     one row for customer 7\n'
            'transactions:  three rows for customer 7\n'
            '```\n'
            '\n'
            'After joining, the customer appears three times. The database did exactly what the relationship asked it to do.\n'
            '\n'
            'Before “deduplicating,” ask:\n'
            '\n'
            '> Is the duplication wrong, or is my expected grain wrong?\n'
            '\n'
            '### `DISTINCT` and `GROUP BY`\n'
            '\n'
            'If the goal is simply a unique customer list:\n'
            '\n'
            '```sql\n'
            'SELECT DISTINCT\n'
            '    c.customer_id,\n'
            '    c.customer_name,\n'
            '    c.customer_email\n'
            'FROM customers AS c\n'
            'JOIN transactions AS t\n'
            '  ON c.customer_id = t.customer_id;\n'
            '```\n'
            '\n'
            'A grouping can produce the same unique rows:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    c.customer_id,\n'
            '    c.customer_name,\n'
            '    c.customer_email\n'
            'FROM customers AS c\n'
            'JOIN transactions AS t\n'
            '  ON c.customer_id = t.customer_id\n'
            'GROUP BY 1, 2, 3;\n'
            '```\n'
            '\n'
            'Another option is to intentionally summarize to one row per entity:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    customer_id,\n'
            '    MIN(transaction_date) AS first_transaction_date,\n'
            '    MAX(transaction_date) AS last_transaction_date,\n'
            '    COUNT(*) AS total_orders\n'
            'FROM transactions\n'
            'GROUP BY customer_id;\n'
            '```\n'
            '\n'
            'That is not merely “removing duplicates.” It changes the grain deliberately.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-09 / Instructor Figure — Duplicate diagnosis | Show three causes feeding a duplicated result: true duplicate source rows, one-to-many valid relationships, and an accidental many-to-many join; beneath them show different responses: fix upstream, aggregate/change grain, or correct join logic | Learner should notice that DISTINCT can hide symptoms and that the cause of row multiplication should be understood first]]\n'
            '\n'
            '---\n'
            '\n'
            '## 9. Cleaning and enriching data with `CASE`\n'
            '\n'
            'Sometimes the data is accurate but inconsistent or inconvenient for analysis.\n'
            '\n'
            'Imagine a field containing:\n'
            '\n'
            '```text\n'
            'F\n'
            'female\n'
            'femme\n'
            '```\n'
            '\n'
            'If all three are intended to represent the same analytical category, a query can standardize them:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            "    WHEN gender = 'F' THEN 'Female'\n"
            "    WHEN gender = 'female' THEN 'Female'\n"
            "    WHEN gender = 'femme' THEN 'Female'\n"
            '    ELSE gender\n'
            'END AS gender_cleaned\n'
            '```\n'
            '\n'
            '### Categorization\n'
            '\n'
            '`CASE` can also create new categories.\n'
            '\n'
            'For NPS-style responses:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            "    WHEN likelihood <= 6 THEN 'Detractor'\n"
            "    WHEN likelihood <= 8 THEN 'Passive'\n"
            "    ELSE 'Promoter'\n"
            'END AS response_type\n'
            '```\n'
            '\n'
            'The ordering of the conditions matters. A value of `5` satisfies both `<= 6` and `<= 8`, but the first true branch is returned.\n'
            '\n'
            '### Multiple conditions\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN likelihood <= 6\n'
            "         AND country = 'US'\n"
            '         AND high_value = TRUE\n'
            "    THEN 'US high value detractor'\n"
            "    ELSE 'other'\n"
            'END\n'
            '```\n'
            '\n'
            '### When a lookup table is better\n'
            '\n'
            'A `CASE` expression works well when:\n'
            '\n'
            '- the list is short;\n'
            '- the mapping changes rarely;\n'
            '- the logic belongs specifically to this analysis.\n'
            '\n'
            'A lookup table is usually easier to maintain when:\n'
            '\n'
            '- there are many mappings;\n'
            '- mappings change frequently;\n'
            '- many queries need the same cleaned values.\n'
            '\n'
            'And if the same bad values keep being repaired downstream, investigate whether the upstream system can generate cleaner values instead.\n'
            '\n'
            '### Flags and dummy variables\n'
            '\n'
            'A useful pattern is converting a condition into `1` or `0`:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN likelihood IN (9, 10) THEN 1\n'
            '    ELSE 0\n'
            'END AS is_promoter\n'
            '```\n'
            '\n'
            'When there are multiple rows per customer, aggregate a row-level flag:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    customer_id,\n'
            "    MAX(CASE WHEN fruit = 'apple' THEN 1 ELSE 0 END) AS bought_apples\n"
            'FROM purchases\n'
            'GROUP BY customer_id;\n'
            '```\n'
            '\n'
            'If a customer bought an apple at least once, at least one row contains `1`, so `MAX()` returns `1`.\n'
            '\n'
            '---\n'
            '\n'
            '## 10. Type conversions and casting\n'
            '\n'
            'Sometimes a value is stored in one type but needs to be treated as another.\n'
            '\n'
            'Two common PostgreSQL-style forms are:\n'
            '\n'
            '```sql\n'
            'CAST(1234 AS VARCHAR)\n'
            '```\n'
            '\n'
            'and:\n'
            '\n'
            '```sql\n'
            '1234::varchar\n'
            '```\n'
            '\n'
            '### Why casting matters in `CASE`\n'
            '\n'
            'This is invalid if `order_items` is numeric:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN order_items <= 3 THEN order_items\n'
            "    ELSE '4+'\n"
            'END\n'
            '```\n'
            '\n'
            'The return branches mix numbers and strings.\n'
            '\n'
            'Convert the numeric branch:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN order_items <= 3 THEN order_items::varchar\n'
            "    ELSE '4+'\n"
            'END\n'
            '```\n'
            '\n'
            'Now both outputs are strings.\n'
            '\n'
            '### Cleaning numeric text before conversion\n'
            '\n'
            'A price such as:\n'
            '\n'
            '```text\n'
            '$19.99\n'
            '```\n'
            '\n'
            'must first lose the currency symbol:\n'
            '\n'
            '```sql\n'
            "replace('$19.99', '$', '')\n"
            '```\n'
            '\n'
            'Then the result can be converted:\n'
            '\n'
            '```sql\n'
            "replace('$19.99', '$', '')::float\n"
            '```\n'
            '\n'
            '### Timestamp to date\n'
            '\n'
            'If a timestamp includes hours, minutes, and seconds but the analysis needs one row per day:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    tx_timestamp::date AS tx_date,\n'
            '    COUNT(*) AS transactions\n'
            'FROM transactions\n'
            'GROUP BY 1;\n'
            '```\n'
            '\n'
            'The cast changes the analytical grain from individual timestamps to calendar dates.\n'
            '\n'
            '### Format-aware conversion helpers\n'
            '\n'
            'Some databases also provide conversion functions that accept a value and, for dates or timestamps, a format pattern. The chapter highlights these common PostgreSQL-style helpers:\n'
            '\n'
            '| Function | Purpose |\n'
            '|---|---|\n'
            '| `to_char` | Convert another type to text |\n'
            '| `to_number` | Convert compatible text or values to a numeric type |\n'
            '| `to_date` | Convert text or another compatible value to a date using a specified format |\n'
            '| `to_timestamp` | Convert text or another compatible value to a timestamp using specified date/time parts |\n'
            '\n'
            'These functions are especially useful when incoming date text does not already match the database\'s default date representation.\n'
            '\n'
            '### Type coercion\n'
            '\n'
            'Databases sometimes convert compatible types automatically. This is called **type coercion**.\n'
            '\n'
            'Do not assume that every database coerces values identically. When a type interaction is important to correctness, make the conversion explicit.\n'
            '\n'
            '---\n'
            '\n'
            '## 11. `NULL` is not zero, and it is not an empty string\n'
            '\n'
            '`NULL` represents missing or inapplicable information.\n'
            '\n'
            'Compare:\n'
            '\n'
            '```text\n'
            '0       -> a known numeric value\n'
            'NULL    -> no value is available\n'
            "''      -> a string value that contains no characters\n"
            '```\n'
            '\n'
            'Those states can carry different meanings.\n'
            '\n'
            "[[IMAGE_NEEDED: IMG-M01-L02-10 / Instructor Figure — Zero versus NULL versus empty string | Three cards: 0 = known zero quantity, NULL = missing/unknown/not applicable, '' = known blank text value; include one database example for each | Learner should notice that these values are not interchangeable and should not be replaced automatically]]\n"
            '\n'
            '### Nulls affect calculations\n'
            '\n'
            'Suppose the values are:\n'
            '\n'
            '```text\n'
            '5, 10, 15, 20, NULL\n'
            '```\n'
            '\n'
            'The sum of known values is straightforward, but interpretation of the average depends on how the missing observation should be treated. This is why the meaning of missingness matters, not merely SQL syntax.\n'
            '\n'
            '### Replace a null with `CASE`\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN num_orders IS NULL THEN 0\n'
            '    ELSE num_orders\n'
            'END\n'
            '```\n'
            '\n'
            '### `coalesce`\n'
            '\n'
            '`coalesce` returns the first non-null argument:\n'
            '\n'
            '```sql\n'
            'coalesce(num_orders, 0)\n'
            "coalesce(address, 'Unknown')\n"
            'coalesce(column_a, column_b, column_c)\n'
            '```\n'
            '\n'
            'It is concise, but replacing a null with zero or `"Unknown"` is still an analytical decision.\n'
            '\n'
            '\n'
            'Some database systems also provide `nvl(value, replacement)`, which is similar to a two-argument `coalesce`. The exact availability and behavior are vendor-specific, so prefer the function supported by the database you are using.\n'
            '### `nullif`\n'
            '\n'
            '`nullif(a, b)` returns `NULL` when the two values are equal; otherwise it returns the first value.\n'
            '\n'
            '```sql\n'
            "nullif(date, '1970-01-01')\n"
            '```\n'
            '\n'
            'This can be useful when a known placeholder value should be interpreted as missing.\n'
            '\n'
            '### Filtering nulls correctly\n'
            '\n'
            'To return null rows:\n'
            '\n'
            '```sql\n'
            'WHERE my_field IS NULL\n'
            '```\n'
            '\n'
            'A common trap is:\n'
            '\n'
            '```sql\n'
            "WHERE my_field <> 'apple'\n"
            '```\n'
            '\n'
            "Depending on SQL's three-valued logic, rows where `my_field` is null do not satisfy the comparison.\n"
            '\n'
            'If the requirement is “everything except apples, including missing values”:\n'
            '\n'
            '```sql\n'
            "WHERE my_field <> 'apple'\n"
            '   OR my_field IS NULL\n'
            '```\n'
            '\n'
            '---\n'
            '\n'
            '## 12. Missing data: first understand why it is missing\n'
            '\n'
            'Missing data can arise because:\n'
            '\n'
            '- a field was optional;\n'
            '- a bug prevented collection;\n'
            '- a process changed over time;\n'
            '- a referenced record has not arrived or was removed;\n'
            '- the available data is at the wrong granularity for the analysis.\n'
            '\n'
            'Different causes justify different responses.\n'
            '\n'
            '### Find missing related records\n'
            '\n'
            'If every transaction should have a customer record:\n'
            '\n'
            '```sql\n'
            'SELECT DISTINCT\n'
            '    t.customer_id\n'
            'FROM transactions AS t\n'
            'LEFT JOIN customers AS c\n'
            '  ON t.customer_id = c.customer_id\n'
            'WHERE c.customer_id IS NULL;\n'
            '```\n'
            '\n'
            'This is a powerful quality-check pattern: left join to what should exist, then search for unmatched rows.\n'
            '\n'
            '### Missingness can itself be information\n'
            '\n'
            'Do not assume that every missing value must be filled. Missingness can reveal:\n'
            '\n'
            '- optional behavior;\n'
            '- a tracking outage;\n'
            '- a process change;\n'
            '- a bias in data collection.\n'
            '\n'
            '### Imputation\n'
            '\n'
            '**Imputation** means filling missing values using a rule or estimate.\n'
            '\n'
            'Possible strategies in the chapter include:\n'
            '\n'
            '- a known constant;\n'
            '- a value derived from other columns;\n'
            '- an average or median;\n'
            '- a previous value;\n'
            '- a following value.\n'
            '\n'
            'A known correction:\n'
            '\n'
            '```sql\n'
            'CASE\n'
            '    WHEN price IS NULL\n'
            "         AND item_name = 'xyz'\n"
            '    THEN 20\n'
            '    ELSE price\n'
            'END AS price\n'
            '```\n'
            '\n'
            'A derived value:\n'
            '\n'
            '```sql\n'
            'gross_sales - discount AS net_sales\n'
            '```\n'
            '\n'
            '### Fill forward and fill backward\n'
            '\n'
            'Window functions can retrieve neighboring values.\n'
            '\n'
            'Previous row:\n'
            '\n'
            '```sql\n'
            'lag(product_price) OVER (\n'
            '    PARTITION BY product\n'
            '    ORDER BY order_date\n'
            ')\n'
            '```\n'
            '\n'
            'Next row:\n'
            '\n'
            '```sql\n'
            'lead(product_price) OVER (\n'
            '    PARTITION BY product\n'
            '    ORDER BY order_date\n'
            ')\n'
            '```\n'
            '\n'
            'These approaches make assumptions. The analyst should check whether the neighboring value is a plausible replacement and document that interpolation occurred.\n'
            '\n'
            '### Missing granularity: create rows instead of filling fields\n'
            '\n'
            'Sometimes the problem is not a missing field. The analysis needs rows that do not exist.\n'
            '\n'
            'For example, a yearly subscription amount may need to become monthly records. A **date dimension** provides a reusable calendar table with one row per date plus useful attributes.\n'
            '\n'
            '{{image:date-dimension-table}}\n'
            '\n'
            'PostgreSQL can generate dates dynamically:\n'
            '\n'
            '```sql\n'
            'SELECT *\n'
            'FROM generate_series(\n'
            "    '2020-01-01'::timestamp,\n"
            "    '2020-12-31',\n"
            "    '1 day'\n"
            ');\n'
            '```\n'
            '\n'
            'A generated or stored calendar can then be joined to event data so that days with no events still appear.\n'
            '\n'
            'This is especially useful when zero activity is analytically meaningful.\n'
            '\n'
            '{{exercise:M01.L02.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## 13. Shaping data: choose the grain before choosing the columns\n'
            '\n'
            '**Shaping data** means changing how information is represented in rows and columns.\n'
            '\n'
            'The central concept is **granularity**, or grain:\n'
            '\n'
            '> What does one row represent?\n'
            '\n'
            'Possible grains include:\n'
            '\n'
            '```text\n'
            'one row per country\n'
            'one row per customer\n'
            'one row per order\n'
            'one row per order item\n'
            'one row per customer per month\n'
            '```\n'
            '\n'
            'Changing grain changes the meaning of every metric.\n'
            '\n'
            '### Flattening\n'
            '\n'
            'Flattening reduces multiple rows or multiple tables into a more compact analytical structure.\n'
            '\n'
            'Examples:\n'
            '\n'
            '- joining customer attributes onto transactions;\n'
            '- aggregating many orders to one customer row;\n'
            '- pivoting categories into columns.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-12 / Instructor Figure — Analytical grain and flattening | Show the same business data at four levels: order item -> order -> customer-month -> customer, with arrows labeled aggregation/flattening | Learner should notice that shaping is fundamentally a choice about what one output row should represent]]\n'
            '\n'
            '### Shape for the destination\n'
            '\n'
            'There is no single best analytical shape.\n'
            '\n'
            'For **BI dashboards**, a detailed data set may support interactive slicing, while an executive dashboard may work better with a small pre-aggregated table.\n'
            '\n'
            'For **visualization**, a compact result at the exact plotting grain is often easiest to use.\n'
            '\n'
            'For **statistics or machine learning**, define the modeled entity and required features. A model might need:\n'
            '\n'
            '- one row per customer;\n'
            '- one row per transaction;\n'
            '- one row per customer-month.\n'
            '\n'
            'A useful tidy-data mental model is:\n'
            '\n'
            '```text\n'
            'Each variable -> one column\n'
            'Each observation -> one row\n'
            'Each value -> one cell\n'
            '```\n'
            '\n'
            'The correct shape follows the analytical question and downstream tool.\n'
            '\n'
            '---\n'
            '\n'
            '## 14. Pivoting: turn categories into columns\n'
            '\n'
            'A **pivot** converts values from one field into separate output columns.\n'
            '\n'
            'Suppose `orders` contains:\n'
            '\n'
            '```text\n'
            'order_date | product | order_amount\n'
            '```\n'
            '\n'
            'We can create one row per date with separate revenue columns:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    order_date,\n'
            '    SUM(\n'
            '        CASE\n'
            "            WHEN product = 'shirt' THEN order_amount\n"
            '            ELSE 0\n'
            '        END\n'
            '    ) AS shirts_amount,\n'
            '    SUM(\n'
            '        CASE\n'
            "            WHEN product = 'shoes' THEN order_amount\n"
            '            ELSE 0\n'
            '        END\n'
            '    ) AS shoes_amount,\n'
            '    SUM(\n'
            '        CASE\n'
            "            WHEN product = 'hat' THEN order_amount\n"
            '            ELSE 0\n'
            '        END\n'
            '    ) AS hats_amount\n'
            'FROM orders\n'
            'GROUP BY order_date;\n'
            '```\n'
            '\n'
            'The pattern is:\n'
            '\n'
            '```text\n'
            'GROUP BY row dimension\n'
            '+\n'
            'CASE chooses a column\n'
            '+\n'
            'aggregation fills the cell\n'
            '```\n'
            '\n'
            'For `SUM()`, `ELSE 0` is often useful. With `COUNT()` or `COUNT(DISTINCT ...)`, adding a non-null `ELSE` can accidentally inflate counts because SQL counts non-null values.\n'
            '\n'
            'Pivoting with `CASE` works best when the set of desired columns is known and reasonably stable. If new categories appear constantly, hardcoding every new value becomes difficult to maintain.\n'
            '\n'
            '[[IMAGE_NEEDED: IMG-M01-L02-13 / Instructor Figure — Pivot and unpivot transformation | Left side shows long data with columns date, product, amount; center arrow labeled PIVOT; right side shows one row per date with shirt/shoes/hat columns. Reverse arrow labeled UNPIVOT returns the wide columns to rows | Learner should notice that pivoting and unpivoting change representation, not the underlying business facts]]\n'
            '\n'
            '---\n'
            '\n'
            '## 15. Unpivoting with `UNION ALL`\n'
            '\n'
            'Sometimes the source is already wide:\n'
            '\n'
            '```text\n'
            'country | year_1980 | year_1990 | year_2000 | year_2010\n'
            '```\n'
            '\n'
            'But analysis needs:\n'
            '\n'
            '```text\n'
            'country | year | population\n'
            '```\n'
            '\n'
            'That transformation is **unpivoting**.\n'
            '\n'
            "{{image:country-population-wide-table}}\n"
            '\n'
            'A portable SQL approach is `UNION ALL`:\n'
            '\n'
            '```sql\n'
            'SELECT\n'
            '    country,\n'
            "    '1980' AS year,\n"
            '    year_1980 AS population\n'
            'FROM country_populations\n'
            '\n'
            'UNION ALL\n'
            '\n'
            'SELECT\n'
            '    country,\n'
            "    '1990' AS year,\n"
            '    year_1990 AS population\n'
            'FROM country_populations\n'
            '\n'
            'UNION ALL\n'
            '\n'
            'SELECT\n'
            '    country,\n'
            "    '2000' AS year,\n"
            '    year_2000 AS population\n'
            'FROM country_populations\n'
            '\n'
            'UNION ALL\n'
            '\n'
            'SELECT\n'
            '    country,\n'
            "    '2010' AS year,\n"
            '    year_2010 AS population\n'
            'FROM country_populations;\n'
            '```\n'
            '\n'
            '### `UNION` versus `UNION ALL`\n'
            '\n'
            'Both stack result sets.\n'
            '\n'
            '- `UNION` removes duplicate rows.\n'
            '- `UNION ALL` keeps every row.\n'
            '\n'
            '`UNION ALL` avoids the extra duplicate-removal step and is the safer choice when every source row should remain.\n'
            '\n'
            '### Vendor-specific helpers\n'
            '\n'
            'Some database systems provide `PIVOT` and `UNPIVOT` syntax. PostgreSQL also provides tools such as `crosstab` and array-oriented `unnest` patterns.\n'
            '\n'
            '\n'
            'A generic `PIVOT` pattern looks like:\n'
            '\n'
            '```sql\n'
            'SELECT ...\n'
            'FROM ...\n'
            'PIVOT (\n'
            '    SUM(value_column)\n'
            '    FOR label_column IN (label_1, label_2, ...)\n'
            ');\n'
            '```\n'
            '\n'
            'A generic `UNPIVOT` pattern reverses the orientation by turning selected columns into label/value rows. The exact syntax differs by database.\n'
            '\n'
            'In PostgreSQL, an array plus `unnest` can also turn several stored columns into rows. The main lesson is not to memorize vendor syntax yet, but to recognize the reshape operation being performed.\n'
            'These helpers can make syntax shorter, but the analytical reasoning is unchanged:\n'
            '\n'
            '1. define the desired output grain;\n'
            '2. decide which values belong in rows;\n'
            '3. decide which values belong in columns;\n'
            '4. make sure no records are silently lost or duplicated.\n'
            '\n'
            '{{exercise:M01.L02.EX03}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconceptions\n'
            '\n'
            '### Misconception 1\n'
            '\n'
            '> Data cleaning means replacing every `NULL` with zero.\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            '`NULL` can mean unknown, missing, not applicable, not yet loaded, or not collected. Zero is a known numeric value. Replacing one with the other changes the meaning of the data and can change counts, averages, and conclusions.\n'
            '\n'
            '### Misconception 2\n'
            '\n'
            '> `DISTINCT` is the normal fix whenever a join creates too many rows.\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'The extra rows may be evidence of a one-to-many or many-to-many relationship. `DISTINCT` can hide the symptom without correcting the analytical grain or join logic.\n'
            '\n'
            '### Misconception 3\n'
            '\n'
            '> A sample that makes the query work is enough for the final answer.\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'Samples can omit rare values and edge cases. Use them to develop logic, then run the validated query on the required population.\n'
            '\n'
            '### Misconception 4\n'
            '\n'
            '> Pivoting changes the data itself.\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'Pivoting changes the representation of the data. The same facts are arranged differently across rows and columns.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Data dictionary | Documentation describing fields, values, origins, and relationships |\n'
            '| Data profiling | Systematic inspection of the values, distributions, structure, and quality of a data set |\n'
            '| Grain / granularity | What one row in a data set represents |\n'
            '| Sparse data | Data in which useful observations are rare relative to the possible space |\n'
            '| Histogram | A representation of the distribution of numeric values |\n'
            '| Bin / bucket | A range used to group values for analysis |\n'
            '| Window function | A function that computes across related rows while retaining row-level output |\n'
            '| Ground truth | A trusted value or source used to validate data or results |\n'
            '| Duplicate | Repeated information at a grain where repetition is not intended |\n'
            '| Imputation | Replacing missing values using a specified rule or estimate |\n'
            '| Date dimension | A calendar table with one row per date and reusable date attributes |\n'
            '| Pivot | Transforming category values from rows into columns |\n'
            '| Unpivot | Transforming multiple columns into row values |\n'
            '| Tidy data | A structure where variables are columns, observations are rows, and values are cells |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. Why can a mathematically correct aggregation still be analytically wrong?\n'
            '2. What is the difference between a database data type and a conceptual data category?\n'
            '3. Why should you identify the grain of every important table?\n'
            '4. When would `COUNT(*)` and `COUNT(DISTINCT customer_id)` answer different questions?\n'
            '5. How does an n-tile differ from a fixed-width bin?\n'
            '6. Why can `DISTINCT` be dangerous as an automatic response to duplicate-looking rows?\n'
            "7. What is the difference between `NULL`, `0`, and `''`?\n"
            '8. When is a lookup table preferable to a long `CASE` expression?\n'
            '9. What assumption is made when you fill a missing value using `lag()` or `lead()`?\n'
            '10. Why might an analysis join to a date dimension even when no business event occurred on some dates?\n'
            '11. What does “one row per customer per month” tell you about the grain?\n'
            '12. When would you use pivoting, and when would you use unpivoting?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**Preparing data is not separate from analytical reasoning. Every choice about type, grain, missing values, duplicates, categories, and shape changes what the final result means.**\n'
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-data-preparation-matters",
                "title": "Why data preparation is analytical work",
                "order": 1,
            },
            {
                "id": "database-data-types",
                "title": "Database data types: what SQL thinks a value is",
                "order": 2,
            },
            {
                "id": "conceptual-data-categories",
                "title": "How analysts classify data beyond database types",
                "order": 3,
            },
            {
                "id": "sql-query-structure",
                "title": "The analytical SQL query skeleton",
                "order": 4,
            },
            {
                "id": "safe-exploration",
                "title": "Explore large tables safely: LIMIT and sampling",
                "order": 5,
            },
            {
                "id": "profiling-distributions",
                "title": "Profiling: learn the shape of the data before trusting it",
                "order": 6,
            },
            {
                "id": "binning-window-functions",
                "title": "Binning, n-tiles, and window functions",
                "order": 7,
            },
            {
                "id": "data-quality-and-duplicates",
                "title": "Data quality and duplicate detection",
                "order": 8,
            },
            {
                "id": "cleaning-with-case",
                "title": "Cleaning and enriching data with CASE",
                "order": 9,
            },
            {
                "id": "type-conversions",
                "title": "Type conversions and casting",
                "order": 10,
            },
            {
                "id": "nulls-empty-strings",
                "title": "NULL is not zero, and it is not an empty string",
                "order": 11,
            },
            {
                "id": "missing-data",
                "title": "Missing data: first understand why it is missing",
                "order": 12,
            },
            {
                "id": "shaping-granularity",
                "title": "Shaping data: choose the grain before choosing the columns",
                "order": 13,
            },
            {
                "id": "pivoting",
                "title": "Pivoting: turn categories into columns",
                "order": 14,
            },
            {
                "id": "unpivoting",
                "title": "Unpivoting with UNION ALL",
                "order": 15,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L02.EX01",

            "title": "Profile an Orders Table",

            "lesson_code": "M01.L02",

            "section_id": "binning-window-functions",

            "placement": "after_section",

            "description": (
                "Build a compact profiling plan that moves from raw values to a useful "
                "distribution and checks whether the table's apparent behavior is trustworthy."
            ),

            "instructions": (
                "Assume an orders table contains order_id, customer_id, order_amount, "
                "order_status, and order_date.\n"
                "1. Write a frequency query for order_status.\n"
                "2. Write a query that returns the number of orders placed by each customer.\n"
                "3. Wrap that query so the final result shows how many customers placed 1, 2, 3, ... orders.\n"
                "4. Add an amount category using CASE with three sensible bins.\n"
                "5. Explain one thing a LIMIT-based sample could fail to reveal.\n"
                "6. State the grain of each intermediate and final result."
            ),

            "expected_output": (
                "SQL for the requested profiling queries plus a short explanation of the "
                "grain, what each distribution reveals, and one sampling limitation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-profiling",
                "aggregation",
                "binning",
                "grain",
                "sql-reasoning",
            ],
        },

        {
            "id": "M01.L02.EX02",

            "title": "Diagnose and Repair a Messy Customer Dataset",

            "lesson_code": "M01.L02",

            "section_id": "missing-data",

            "placement": "after_section",

            "description": (
                "Practice distinguishing quality problems from missingness and choose a "
                "defensible SQL treatment instead of applying automatic replacements."
            ),

            "instructions": (
                "A customer table has gender values F, female, femme, and null; some order "
                "prices are stored as strings such as '$19.99'; some missing dates were "
                "loaded as 1970-01-01; and a LEFT JOIN shows transactions whose customer "
                "records are missing.\n"
                "1. Standardize the known gender variants with CASE while preserving unknown values.\n"
                "2. Convert the price text to a numeric value.\n"
                "3. Turn the known placeholder date back into null with nullif.\n"
                "4. Write a query pattern that returns transaction customer_ids with no matching customer.\n"
                "5. For each issue, explain whether it is a type problem, value-standardization problem, "
                "placeholder problem, or missing-related-record problem.\n"
                "6. Explain which fixes should ideally be investigated upstream."
            ),

            "expected_output": (
                "Four SQL snippets plus a short diagnosis table describing the meaning of "
                "each issue and why the chosen treatment is appropriate."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-cleaning",
                "casting",
                "null-handling",
                "missing-data",
                "data-quality",
            ],
        },

        {
            "id": "M01.L02.EX03",

            "title": "Choose the Right Data Shape",

            "lesson_code": "M01.L02",

            "section_id": "unpivoting",

            "placement": "after_section",

            "description": (
                "Apply grain, pivoting, and unpivoting concepts to three realistic downstream uses."
            ),

            "instructions": (
                "Consider three outputs.\n"
                "1. An executive dashboard needs daily revenue split into shirt, shoes, and hat columns.\n"
                "2. A machine-learning feature table needs exactly one row per customer with total_orders, "
                "total_spend, and bought_apples flags.\n"
                "3. A country population file has separate columns year_1980, year_1990, year_2000, and year_2010, "
                "but a visualization needs one row per country-year.\n"
                "For each output: state the required grain, identify whether you need aggregation, pivoting, "
                "unpivoting, or a combination, and sketch the SQL pattern you would use."
            ),

            "expected_output": (
                "A three-case design with the required grain, transformation choice, and representative SQL "
                "pattern for each downstream use."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-shaping",
                "granularity",
                "pivoting",
                "unpivoting",
                "downstream-design",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L02.QZ01",

        "title": "Preparing Data for Analysis — Knowledge Check",

        "lesson_code": "M01.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",

                "section_id": "database-data-types",

                "question": (
                    "A field stores values such as '$19.99'. Why can SUM() not be applied "
                    "reliably before additional preparation?"
                ),

                "options": [
                    "Because currency values must always be integers",
                    "Because the value is stored as text and must be cleaned and converted to a numeric type",
                    "Because SUM() works only on Boolean fields",
                    "Because SQL cannot calculate on monetary values",
                ],

                "correct": 1,

                "explanation": (
                    "The currency symbol makes the example a string representation. The text "
                    "must first be normalized and then converted to a numeric type before "
                    "numeric aggregation is appropriate."
                ),
            },

            {
                "id": "M01.L02.Q02",

                "section_id": "safe-exploration",

                "question": (
                    "What is the best reason to use LIMIT while developing a query on a very large table?"
                ),

                "options": [
                    "It guarantees the sample contains every edge case",
                    "It permanently defines the correct population for the analysis",
                    "It lets you inspect and test query logic quickly before running on the required population",
                    "It removes all duplicate rows automatically",
                ],

                "correct": 2,

                "explanation": (
                    "LIMIT is useful for fast exploration and development. A limited result can "
                    "miss rare values, so it should not silently replace the final required population."
                ),
            },

            {
                "id": "M01.L02.Q03",

                "section_id": "binning-window-functions",

                "question": (
                    "What is the key difference between a fixed-width bin and ntile(10)?"
                ),

                "options": [
                    "Fixed-width bins require strings, while ntile requires dates",
                    "Fixed-width bins divide the numeric scale, while ntile divides ordered rows into groups with roughly equal row counts",
                    "ntile can only return two groups",
                    "There is no practical difference",
                ],

                "correct": 1,

                "explanation": (
                    "A fixed-width strategy defines ranges on the value scale. ntile groups "
                    "ordered observations by row count, so the numeric width of each tile can differ."
                ),
            },

            {
                "id": "M01.L02.Q04",

                "section_id": "data-quality-and-duplicates",

                "question": (
                    "A join causes each customer to appear once for every transaction. What should "
                    "you determine before adding DISTINCT?"
                ),

                "options": [
                    "Whether the database supports VARCHAR",
                    "Whether one-to-many multiplication is correct for the intended output grain",
                    "Whether the table contains a BOOLEAN column",
                    "Whether the query uses LIMIT",
                ],

                "correct": 1,

                "explanation": (
                    "Multiple rows may be the correct consequence of a one-to-many relationship. "
                    "The analyst should first decide what one result row is supposed to represent."
                ),
            },

            {
                "id": "M01.L02.Q05",

                "section_id": "nulls-empty-strings",

                "question": (
                    "A column contains NULL values. Which statement is correct?"
                ),

                "options": [
                    "NULL always means the numeric value zero",
                    "NULL and an empty string are always identical",
                    "NULL represents the absence of a value and its business meaning must be interpreted before replacement",
                    "NULL rows automatically satisfy the condition field <> 'apple'",
                ],

                "correct": 2,

                "explanation": (
                    "NULL represents missing or inapplicable information, not a specific numeric "
                    "or string value. Replacing it requires understanding what the absence means."
                ),
            },

            {
                "id": "M01.L02.Q06",

                "section_id": "missing-data",

                "question": (
                    "Why might an analyst join a complete date dimension to an orders table?"
                ),

                "options": [
                    "To make every order amount a string",
                    "To ensure dates with zero orders can still appear in the analytical result",
                    "To remove every null automatically",
                    "To avoid using GROUP BY",
                ],

                "correct": 1,

                "explanation": (
                    "Event tables usually contain rows only when events happen. A calendar or "
                    "date dimension can supply the missing dates so zero-activity periods remain visible."
                ),
            },

            {
                "id": "M01.L02.Q07",

                "section_id": "pivoting",

                "question": (
                    "When pivoting product values into columns using SUM(CASE ...), why is ELSE 0 "
                    "often acceptable for SUM but potentially dangerous inside COUNT?"
                ),

                "options": [
                    "COUNT ignores every integer",
                    "SUM requires nulls, while COUNT requires zeros",
                    "COUNT counts non-null expressions, so substituting 0 can make rows count even when the condition did not match",
                    "ELSE 0 changes the database data type to DATE",
                ],

                "correct": 2,

                "explanation": (
                    "COUNT(expression) counts non-null expression results. Returning 0 on a nonmatch "
                    "still produces a non-null value, which can inflate counts."
                ),
            },

            {
                "id": "M01.L02.Q08",

                "section_id": "unpivoting",

                "question": (
                    "What is the main behavioral difference between UNION and UNION ALL?"
                ),

                "options": [
                    "UNION removes duplicate result rows, while UNION ALL retains them",
                    "UNION works only with dates",
                    "UNION ALL can combine only two queries",
                    "UNION changes columns into rows but UNION ALL does not",
                ],

                "correct": 0,

                "explanation": (
                    "Both operators stack compatible result sets. UNION adds duplicate removal; "
                    "UNION ALL retains every row and avoids that deduplication step."
                ),
            },

            {
                "id": "M01.L02.Q09",

                "section_id": "shaping-granularity",

                "type": "open",

                "question": (
                    "You are asked to build a customer-level machine-learning feature table from "
                    "orders, support tickets, and customer attributes. Explain how you would decide "
                    "the grain, detect accidental row multiplication, handle missing fields, and shape "
                    "the final result to one row per customer."
                ),
            },
        ],

        "passing_score": 70,
    },
}
