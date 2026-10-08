"""M01.L01 — Analysis with SQL.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Source alignment: Chapter 1, "Analysis with SQL".
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Data Analysis with SQL"

MODULE_DESCRIPTION = (
    "Build a practical mental model of data analysis, understand why SQL is central "
    "to analytical work, compare SQL with Python and R, follow the end-to-end data "
    "analysis workflow, and recognize the database architectures and data stores an "
    "analyst is likely to encounter."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Analysis with SQL",

    "slug": "data-analysis-sql-m01-l01",

    "description": (
        "A beginner-friendly but complete introduction to data analysis with SQL: "
        "what analysts actually do, how SQL works with databases, where SQL fits "
        "alongside Python and R, how analytical data flows through an organization, "
        "and why row-store, column-store, and other data systems behave differently."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "data-analysis",
        "sql",
        "databases",
        "analytics-workflow",
        "data-warehousing",
        "module-01",
    ],

    "prerequisite_ids": [],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Analysis with SQL",

        "content": (
            "# Analysis with SQL\n"
            "\n"
            "> **Course:** Data Analysis with SQL  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Foundations of Data Analysis with SQL  \n"
            "> **Source alignment:** Chapter 1, *Analysis with SQL*. This lesson is "
            "an instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain data analysis as a process of discovery, interpretation, and communication rather than simply calculating numbers.\n"
            "- Describe what SQL is, what it can do, and how database objects such as schemas, tables, views, functions, and indexes fit together.\n"
            "- Distinguish DQL, DDL, DCL, and DML and recognize the common commands in each group.\n"
            "- Explain the main reasons SQL remains a core tool for analytical work.\n"
            "- Choose sensibly between SQL, Python, and R for different analytical situations.\n"
            "- Trace data from source systems through ETL or ELT into a warehouse and then through analysis and presentation.\n"
            "- Compare row-store and column-store databases and explain why their physical storage models affect analytical performance.\n"
            "- Recognize data lakes, Hadoop-style systems, NoSQL stores, and search-oriented stores and understand where they fit in a modern data stack.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. What data analysis really is\n"
            "\n"
            "Data analysis is not simply the act of running a query and reporting a number. A useful analysis starts with a question, investigates evidence, interprets what the evidence means, and communicates the result so that a person or system can make a better decision.\n"
            "\n"
            "A helpful mental model is:\n"
            "\n"
            "```text\n"
            "Question -> Data -> Investigation -> Interpretation -> Communication -> Decision\n"
            "```\n"
            "\n"
            "The technical part matters, but the reasoning around the technical work matters just as much. An analyst needs curiosity: Why did sales fall? Why are users leaving? Why did conversion improve in one market but decline in another? Numbers are clues, not conclusions.\n"
            "\n"
            "Modern data analysis combines computing with ideas from statistics and other quantitative disciplines. In practice, the work often has three connected parts:\n"
            "\n"
            "1. **Discovery** — finding useful patterns, anomalies, relationships, and changes in data.\n"
            "2. **Interpretation** — deciding what those patterns may mean in the real-world context that generated the data.\n"
            "3. **Communication** — presenting the result clearly enough that somebody can act on it.\n"
            "\n"
            "Different organizations use labels such as **analytics**, **business intelligence (BI)**, **data science**, or **decision science**. Job titles also vary. What matters is the underlying activity: using evidence to understand what happened and support better decisions.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-01 / Instructor Figure — Data analysis as a decision loop | "
            "A circular workflow showing business question -> collect or locate data -> explore/analyze -> interpret -> communicate -> decision/action -> new questions | "
            "Learner should notice that analysis is iterative and decision-oriented, not a one-time calculation]]\n"
            "\n"
            "### Historical data is useful, but not magical\n"
            "\n"
            "Analysts usually work with observations that have already happened. Historical data can reveal customer behavior, process weaknesses, operational gaps, fraud patterns, and opportunities. It can also support forecasts and ranges of likely outcomes.\n"
            "\n"
            "However, the past is not guaranteed to repeat itself. Products change, competitors change, policies change, user preferences change, and unexpected events happen. A strong analyst therefore separates two statements:\n"
            "\n"
            "- **The data shows that this happened in the past.**\n"
            "- **We expect something similar to happen in the future.**\n"
            "\n"
            "The first can be directly supported by historical data. The second is a prediction and requires assumptions.\n"
            "\n"
            "### Analysis is also a human skill\n"
            "\n"
            "An elegant query has little value if the result is confusing or cannot be acted on. In real organizations, a simple analysis explained persuasively can create more impact than a sophisticated method that stakeholders do not understand. Analysts also depend on collaboration: somebody must trust the result and be able to execute the recommendation.\n"
            "\n"
            "Ethics belongs in this mental model from the beginning. Not every piece of data that can be collected should be collected. Sensitive information, privacy, consent, retention, and regulation all affect what responsible analysis looks like.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. SQL and the structure of a database\n"
            "\n"
            "**SQL** stands for **Structured Query Language**. Its main purpose is to communicate with data stored in database systems. SQL is not a general-purpose programming language like Python, but for structured data inside databases it is extremely powerful.\n"
            "\n"
            "SQL grew out of the relational model, where information is represented through related tables. Standards helped give SQL a common foundation, but database vendors added their own functions and behavior. That is why SQL written for PostgreSQL, SQL Server, Oracle, Snowflake, or another system can look familiar while still containing differences. These variants are often called **SQL dialects**.\n"
            "\n"
            "To work confidently with SQL, first understand the objects it interacts with.\n"
            "\n"
            "| Object | What it means | Why an analyst cares |\n"
            "|---|---|---|\n"
            "| Database | A managed environment containing stored data and related objects | The main system SQL connects to |\n"
            "| Schema | A logical container used to organize database objects | Helps you locate the correct tables and avoid naming conflicts |\n"
            "| Table | Rows and columns that physically store records | The most common source queried during analysis |\n"
            "| View | A stored query exposed like a table | Can simplify repeated logic or expose curated data |\n"
            "| Function | Reusable database logic or calculations | Lets queries reuse database-side operations |\n"
            "| Index | A structure that speeds up selected lookups | Can make filters and joins much faster in row-oriented systems |\n"
            "\n"
            '{{image:database-organization-objects}}'
            '\n'
            "\n"
            "### A first mental SQL example\n"
            "\n"
            "Imagine a table called `orders` containing one row per order:\n"
            "\n"
            "```text\n"
            "order_id | customer_id | order_date | amount\n"
            "101      | 7           | 2026-01-05 | 120.00\n"
            "102      | 9           | 2026-01-05 | 85.00\n"
            "103      | 7           | 2026-01-06 | 210.00\n"
            "```\n"
            "\n"
            "A query can ask the database a question such as: *How much revenue came from each customer?*\n"
            "\n"
            "```sql\n"
            "SELECT customer_id, SUM(amount) AS total_revenue\n"
            "FROM orders\n"
            "GROUP BY customer_id;\n"
            "```\n"
            "\n"
            "Notice the analytical style: instead of writing a loop that visits each row manually, SQL describes the result we want and lets the database determine how to produce it. This declarative style is one of SQL's defining strengths.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. The four SQL sublanguages\n"
            "\n"
            "SQL commands are commonly grouped into four families. Analysts spend most of their time with querying, but understanding all four groups makes conversations with database administrators and data engineers much easier.\n"
            "\n"
            "| Sublanguage | Purpose | Common commands |\n"
            "|---|---|---|\n"
            "| **DQL** — Data Query Language | Read and analyze data | `SELECT` |\n"
            "| **DDL** — Data Definition Language | Create or change database structure | `CREATE`, `ALTER`, `DROP` |\n"
            "| **DCL** — Data Control Language | Manage permissions | `GRANT`, `REVOKE` |\n"
            "| **DML** — Data Manipulation Language | Change the stored records | `INSERT`, `UPDATE`, `DELETE` |\n"
            "\n"
            "### DQL: asking questions\n"
            "\n"
            "DQL is the heart of analytical SQL. A `SELECT` query can read one table, combine many tables with joins, aggregate millions of rows, and return a small result that answers a business question.\n"
            "\n"
            "### DDL: changing structure\n"
            "\n"
            "DDL works on objects rather than on individual business records. Creating a temporary analysis table is a practical example.\n"
            "\n"
            "```sql\n"
            "CREATE TABLE high_value_customers (\n"
            "    customer_id INTEGER,\n"
            "    total_revenue NUMERIC\n"
            ");\n"
            "```\n"
            "\n"
            "`ALTER` changes the structure of an existing object, while `DROP` removes the object itself.\n"
            "\n"
            "### DCL: controlling access\n"
            "\n"
            "A database may contain a table that exists but is invisible or inaccessible to your account. Permissions determine whether you may read or modify it. `GRANT` adds permission; `REVOKE` removes it.\n"
            "\n"
            "### DML: changing records\n"
            "\n"
            "DML acts on data inside tables. `INSERT` adds rows, `UPDATE` changes existing values, and `DELETE` removes rows. Analysts may encounter DML when managing temporary tables, sandboxes, or self-owned analytical datasets.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-03 / Instructor Figure — SQL command families | "
            "Four labeled blocks for DQL, DDL, DCL, and DML surrounding a central database, with representative commands beside each block | "
            "Learner should notice that SQL is broader than SELECT and that each family operates on a different aspect of the database]]\n"
            "\n"
            "### SQL dialects matter\n"
            "\n"
            "The core structure of SQL is widely shared, but details vary. When moving between database systems, pay special attention to:\n"
            "\n"
            "- null handling\n"
            "- date and timestamp functions\n"
            "- integer division\n"
            "- case sensitivity\n"
            "- vendor-specific functions and syntax\n"
            "\n"
            "Learning standard SQL gives you a transferable foundation; learning a dialect teaches you how one specific engine expresses the details.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Why SQL remains so useful for analysis\n"
            "\n"
            "SQL has survived for decades because it solves several practical problems at once.\n"
            "\n"
            "### 4.1 The data is often already in a database\n"
            "\n"
            "Organizations usually generate operational data continuously: orders, users, payments, events, inventory, support tickets, and much more. If the data already lives in a database or warehouse, SQL works close to the source instead of forcing the analyst to export everything first.\n"
            "\n"
            "### 4.2 The database does the heavy computation\n"
            "\n"
            "A query normally runs on the database server or data warehouse. That server may have far more memory, CPU, and storage bandwidth than an analyst's laptop. Instead of downloading billions of records and processing them locally, SQL can aggregate them near the data and return only the result.\n"
            "\n"
            "### 4.3 SQL connects to the rest of the analytics ecosystem\n"
            "\n"
            "BI tools, spreadsheets, visualization systems, Python, and R can all connect to SQL databases. This means SQL often becomes the common layer that prepares data before another tool presents or models it.\n"
            "\n"
            "### 4.4 A small syntax can express many questions\n"
            "\n"
            "A relatively compact set of concepts—selection, filtering, grouping, joining, sorting, conditional logic, and window calculations—can be combined in many ways. SQL is also naturally iterative: write a small query, inspect the result, then refine it.\n"
            "\n"
            "### 4.5 SQL is approachable\n"
            "\n"
            "The first useful queries are simple enough for beginners to learn quickly. Mastery still takes time because real datasets are messy and business questions can be ambiguous, but the entry barrier is comparatively low.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. SQL versus Python or R\n"
            "\n"
            "The most useful question is not *Which language is best?* It is *Which tool fits this part of the job?*\n"
            "\n"
            "| Consideration | SQL | Python / R |\n"
            "|---|---|---|\n"
            "| Typical execution location | Database or warehouse | Often local machine, notebook, or application server |\n"
            "| Natural data structure | Tables with rows and columns | Tables plus lists, dictionaries, arrays, objects, and more |\n"
            "| Large database aggregation | Excellent | Often best after querying only needed data |\n"
            "| Loops and general program flow | Limited in standard analytical SQL | Natural and flexible |\n"
            "| Statistics and machine learning | Basic to moderate, vendor dependent | Rich ecosystems and libraries |\n"
            "| Direct work with local files and web APIs | Usually indirect | Excellent |\n"
            "| Repeated dashboard refreshes | Excellent when data is already in a database | Often complementary to SQL |\n"
            "\n"
            "### Where the code runs\n"
            "\n"
            "If the data lives in a warehouse, SQL can push computation to the system that already stores the data. Python or R can also run on powerful servers, but analysts commonly use them in notebooks or local environments. For large data, avoiding unnecessary transfer is often a major advantage.\n"
            "\n"
            "### Data structures\n"
            "\n"
            "SQL assumes tabular data. Python and R support tables too, but they also offer many other structures. This flexibility is valuable for machine learning, simulation, application logic, and specialized statistical work.\n"
            "\n"
            "### Loops versus set-based thinking\n"
            "\n"
            "In Python, you may explicitly iterate over values. In SQL, you usually describe an operation over a set of rows and the database handles the iteration internally.\n"
            "\n"
            "```python\n"
            "# Python-style explicit iteration\n"
            "total = 0\n"
            "for value in amounts:\n"
            "    total += value\n"
            "```\n"
            "\n"
            "```sql\n"
            "-- SQL-style set aggregation\n"
            "SELECT SUM(amount)\n"
            "FROM orders;\n"
            "```\n"
            "\n"
            "### Statistics and machine learning\n"
            "\n"
            "SQL can calculate useful descriptive statistics such as counts, averages, and standard deviations. More advanced statistical inference and machine learning are usually better handled with Python or R and their specialized libraries.\n"
            "\n"
            "### A practical decision checklist\n"
            "\n"
            "Before choosing a tool, ask:\n"
            "\n"
            "1. Where is the data: database, file, or website/API?\n"
            "2. How large is it?\n"
            "3. What will happen to the result: dashboard, visualization, statistical test, ML model?\n"
            "4. Does the analysis need to refresh automatically?\n"
            "5. What tools are already standard in the team?\n"
            "\n"
            "The strongest analysts are often comfortable combining tools—for example, SQL for extracting and shaping large data, followed by Python for modeling and visualization.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-04 / Instructor Figure — Choosing SQL versus Python or R | "
            "A decision diagram starting from data location and task type: database + aggregation/dashboard -> SQL; local files/APIs or advanced statistics/ML -> Python/R; hybrid tasks -> SQL plus Python/R | "
            "Learner should notice that the tools are complementary rather than mutually exclusive]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. SQL inside the end-to-end data analysis workflow\n"
            "\n"
            "SQL is powerful, but it is only one part of a broader workflow. A typical analysis moves through several stages.\n"
            "\n"
            "### Stage 1: A question is framed\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- How many new customers did we acquire this month?\n"
            "- Is revenue growing or declining?\n"
            "- Which users remain active after 90 days?\n"
            "- Where are operational failures increasing?\n"
            "\n"
            "A vague question creates vague analysis. Before writing SQL, define the metric, population, time range, and intended decision whenever possible.\n"
            "\n"
            "### Stage 2: Source systems generate data\n"
            "\n"
            "Source systems are the human or machine processes that create the raw evidence. Examples include checkout applications, website event trackers, marketing systems, forms, support systems, and operational databases.\n"
            "\n"
            "### Stage 3: Data is moved into analytical storage\n"
            "\n"
            "Organizations often consolidate data into a **data warehouse**. A smaller subject-focused warehouse may be called a **data mart**. A broader file-based or lightly transformed storage environment may be called a **data lake**.\n"
            "\n"
            "The movement process is commonly described as **ETL** or **ELT**:\n"
            "\n"
            "```text\n"
            "ETL: Extract -> Transform -> Load\n"
            "ELT: Extract -> Load -> Transform\n"
            "```\n"
            "\n"
            "In ETL, transformation occurs before the final load. In ELT, raw or lightly processed data is loaded first, then transformed inside the destination system—often using SQL.\n"
            "\n"
            '{{image:data-analysis-process-steps}}'
            '\n'
            "\n"
            "### Stage 4: Query and analyze\n"
            "\n"
            "Once data is available, analytical work commonly cycles through five activities:\n"
            "\n"
            "1. **Explore** — learn what tables, fields, and business processes exist.\n"
            "2. **Profile** — inspect distributions, distinct values, ranges, missingness, and suspicious records.\n"
            "3. **Clean** — fix or account for errors, nulls, inconsistent categories, or incomplete records.\n"
            "4. **Shape** — arrange the data into the rows, columns, categories, and metrics needed for the question.\n"
            "5. **Analyze** — inspect patterns and produce conclusions or insights.\n"
            "\n"
            '{{image:query-analysis-stages}}'
            '\n'
            "\n"
            "### Stage 5: Present the result\n"
            "\n"
            "Stakeholders usually need an explanation, chart, dashboard, recommendation, or downstream dataset—not the SQL source code itself. Sometimes the SQL result is passed into a BI tool. In other cases, it becomes input for statistical software or a machine learning workflow.\n"
            "\n"
            "The workflow therefore separates two different kinds of quality:\n"
            "\n"
            "- **Technical correctness:** the query calculates what you intended.\n"
            "- **Decision usefulness:** the output helps the audience understand and act.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Row-store versus column-store databases\n"
            "\n"
            "To understand database performance, you need to know one physical idea: a table may look like a grid to you, but the database must serialize those values for storage. How it groups the values strongly affects which workloads are fast.\n"
            "\n"
            "### Row-store databases\n"
            "\n"
            "A row-store keeps the values belonging to one row close together. This is excellent for transactional systems where applications frequently insert, update, delete, or retrieve complete individual records. PostgreSQL and MySQL are common examples of row-oriented systems.\n"
            "\n"
            "```text\n"
            "Row 1: [order_id=101, customer=7, date=..., amount=120]\n"
            "Row 2: [order_id=102, customer=9, date=..., amount=85 ]\n"
            "Row 3: [order_id=103, customer=7, date=..., amount=210]\n"
            "```\n"
            "\n"
            "If an application wants one order, reading the whole row is convenient. But if an analyst wants only the `amount` column across hundreds of millions of rows, the system may need to read more unrelated data than necessary.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-07 / Source Figure 1-4 — Row-wise physical storage | "
            "A table on the left and disk blocks on the right showing all values from each row stored together sequentially | "
            "Learner should notice why row-oriented storage is efficient for retrieving or updating complete records]]\n"
            "\n"
            "### Normalization and analytical complexity\n"
            "\n"
            "Transactional databases are often modeled so that the same fact is stored only once. This reduces duplication and inconsistency, but it can create many narrow related tables. Analytical queries may therefore require several joins to reconstruct a business-friendly dataset.\n"
            "\n"
            "A **primary key** uniquely identifies a record. A table may also have a meaningful multi-column **composite key** or **business key**. **Indexes** speed up selected lookups and joins, but they consume storage and can make writes more expensive because the index must be maintained.\n"
            "\n"
            "### Star schemas\n"
            "\n"
            "Analytics-oriented designs often use a **star schema**:\n"
            "\n"
            "- A **fact table** records events or measurements, such as orders or transactions.\n"
            "- **Dimension tables** describe the entities around those events, such as customers, products, or locations.\n"
            "\n"
            "A **snowflake schema** extends this idea by further normalizing some dimensions.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-08 / Instructor Figure — Star schema for sales analytics | "
            "A central sales fact table connected to customer, product, date, and store dimension tables | "
            "Learner should notice that analytical models organize events in the center and descriptive context around them]]\n"
            "\n"
            "### Column-store databases\n"
            "\n"
            "A column-store keeps values from the same column together. This design is well suited to analytical workloads that scan many records but use only a subset of columns. Systems such as Snowflake, Amazon Redshift, and Vertica are associated with column-oriented analytical storage.\n"
            "\n"
            "```text\n"
            "order_id:    [101, 102, 103, ...]\n"
            "customer_id: [7,   9,   7,   ...]\n"
            "amount:      [120, 85,  210, ...]\n"
            "```\n"
            "\n"
            "Column-oriented storage also enables strong compression because nearby values often repeat or have similar patterns. Repeated categories can be represented compactly rather than stored as long text again and again.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-09 / Instructor Figure — Row-store versus column-store | "
            "Side-by-side disk layouts of the same table: left stores complete rows together, right stores each column together; highlight an analytics query reading only the amount column | "
            "Learner should notice that the column-store reads far less irrelevant data for column-focused aggregation]]\n"
            "\n"
            "Column stores trade some transactional convenience for analytical speed. Updates and deletes can be expensive, and data quality requires care because analytical systems may not enforce uniqueness in the same way as transactional databases. Performance can also depend on sort order, partitioning, compression, and how large-table joins are executed.\n"
            "\n"
            "### The key trade-off\n"
            "\n"
            "| Workload | Row-store tends to fit | Column-store tends to fit |\n"
            "|---|---|---|\n"
            "| Frequent small inserts/updates | Strong | Often less ideal |\n"
            "| Retrieve a complete single record | Strong | Usually not the main optimization target |\n"
            "| Scan millions of rows using a few columns | Can be expensive | Strong |\n"
            "| Large aggregations | Possible, often tuning-dependent | Usually excellent |\n"
            "| Compression of repeated analytical values | Moderate | Often excellent |\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. Data lakes, Hadoop, NoSQL, and search-oriented stores\n"
            "\n"
            "Not all analytical data lives in a traditional relational database. Modern organizations often use multiple storage technologies because different workloads need different trade-offs.\n"
            "\n"
            "### Data lakes and distributed file storage\n"
            "\n"
            "A data lake commonly stores large volumes of files, often before the data has been transformed into the polished schemas expected in a warehouse. Distributed file systems such as Hadoop's HDFS helped organizations store very large datasets by splitting files into blocks and distributing those blocks across many machines. Computation could then be sent to the machines holding the data so work could happen in parallel.\n"
            "\n"
            "This approach made very large-scale storage affordable, although early Hadoop ecosystems required specialized skills and could be slow for interactive analysis. Later tools added SQL or SQL-like interfaces and improved query performance.\n"
            "\n"
            "### NoSQL systems\n"
            "\n"
            "**NoSQL** refers to data systems that are not limited to the relational table model. Important families include:\n"
            "\n"
            "- **Key-value stores** for extremely fast access by key.\n"
            "- **Document stores** for flexible records such as JSON-like documents.\n"
            "- **Graph databases** for relationships represented as nodes and edges.\n"
            "\n"
            "These systems are often designed for application performance rather than for scanning huge numbers of records to compute analytical summaries. Analytical copies of their data may therefore be moved into a warehouse. Graph databases are an exception for relationship-heavy questions, where specialized graph query languages can be useful.\n"
            "\n"
            "### Search-oriented stores\n"
            "\n"
            "Systems such as Elasticsearch and Splunk are commonly used for logs and machine-generated events. Their strength is fast search and investigation—finding specific events or patterns inside a large stream. They can support analytics, but they are optimized differently from a warehouse that continuously aggregates large tables.\n"
            "\n"
            "[[IMAGE_NEEDED: IMG-M01-L01-10 / Instructor Figure — Modern analytical storage landscape | "
            "A comparison diagram with relational row-store, column-store warehouse, data lake/distributed files, NoSQL, and search store, each labeled with its typical strength | "
            "Learner should notice that storage technologies coexist because they optimize for different access patterns]]\n"
            "\n"
            "### Why SQL keeps reappearing\n"
            "\n"
            "An important industry pattern is that even storage systems created outside the traditional relational world often add SQL-compatible query layers. The reason is practical: SQL is familiar, expressive for tabular analysis, and already integrated with a large ecosystem of analytical tools.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> Data analysis is mainly about calculating the correct metric.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A correct metric can still lead to a poor decision if the question is badly framed, the data is misunderstood, the interpretation is weak, or the result is communicated badly. Analysis is an end-to-end reasoning process.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> SQL and Python compete, so an analyst should choose one and avoid the other.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "They often solve different parts of the same workflow. SQL is excellent for relational data retrieval and aggregation near a database. Python and R add general programming, statistical, and machine-learning capabilities.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> A faster database means the SQL logic itself does not matter.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Physical storage, sorting, indexing, table size, joins, filters, and query structure still affect how much work the engine must perform. Understanding the system helps you write more efficient analysis.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Data analysis | Using data to discover, interpret, and communicate evidence for decisions |\n"
            "| SQL | Structured Query Language used to interact with database systems |\n"
            "| SQL dialect | Vendor-specific variation of SQL syntax or behavior |\n"
            "| Schema | Logical container that organizes database objects |\n"
            "| Table | Data stored as rows and columns |\n"
            "| View | Stored query that can be queried similarly to a table |\n"
            "| Index | Auxiliary structure that speeds selected lookups and joins |\n"
            "| DQL | Querying language family, primarily `SELECT` |\n"
            "| DDL | Commands that create or change database structure |\n"
            "| DCL | Commands that manage database permissions |\n"
            "| DML | Commands that insert, update, or delete stored records |\n"
            "| ETL | Extract, transform, then load data |\n"
            "| ELT | Extract, load, then transform data in the destination |\n"
            "| Data warehouse | Central analytical repository that consolidates organizational data |\n"
            "| Data mart | Smaller subject-focused analytical repository |\n"
            "| Data lake | Large storage environment, often file-based and less transformed than a warehouse |\n"
            "| Row-store | Database layout that stores values from the same row together |\n"
            "| Column-store | Database layout that stores values from the same column together |\n"
            "| Primary key | Field or fields that uniquely identify a row |\n"
            "| Composite key | Multiple fields whose combination identifies a row |\n"
            "| Fact table | Analytical table containing events or measurements |\n"
            "| Dimension table | Descriptive table providing context for facts |\n"
            "| NoSQL | Non-relational or not-only-relational data storage technologies |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is data analysis more than producing a correct number?\n"
            "2. What is the difference between a table, a view, and an index?\n"
            "3. Which SQL command family would you use to query data, modify table structure, manage permissions, or change records?\n"
            "4. Give one situation where SQL is the natural first choice and one where Python or R is better suited.\n"
            "5. Explain ETL and ELT in your own words.\n"
            "6. Why can a column-store be faster than a row-store for a query that aggregates one numeric column across millions of rows?\n"
            "7. Why might data from a NoSQL application eventually be copied into a relational warehouse for analysis?\n"
            "8. What is the difference between technical correctness and decision usefulness?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**SQL is not the whole of data analysis; it is the central language that lets analysts turn data stored in analytical systems into evidence, while database design, workflow, tool choice, interpretation, and communication determine whether that evidence becomes useful insight.**\n"
        ),

        "estimated_minutes": 120,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "what-data-analysis-really-is",
                "title": "What data analysis really is",
                "order": 1,
            },
            {
                "id": "sql-and-database-objects",
                "title": "SQL and the structure of a database",
                "order": 2,
            },
            {
                "id": "sql-sublanguages",
                "title": "The four SQL sublanguages",
                "order": 3,
            },
            {
                "id": "why-sql-is-powerful",
                "title": "Why SQL remains so useful for analysis",
                "order": 4,
            },
            {
                "id": "sql-vs-python-r",
                "title": "SQL versus Python or R",
                "order": 5,
            },
            {
                "id": "analysis-workflow",
                "title": "SQL inside the end-to-end data analysis workflow",
                "order": 6,
            },
            {
                "id": "row-vs-column-databases",
                "title": "Row-store versus column-store databases",
                "order": 7,
            },
            {
                "id": "other-data-infrastructure",
                "title": "Data lakes, Hadoop, NoSQL, and search-oriented stores",
                "order": 8,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Choose the Right Analysis Tool",

            "lesson_code": "M01.L01",

            "section_id": "why-sql-is-powerful",

            "placement": "after_section",

            "description": (
                "Practice deciding when SQL should perform the work and when another "
                "tool should take over."
            ),

            "instructions": (
                "For each scenario, choose SQL, Python/R, or a combination and explain why.\n"
                "1. A dashboard must refresh every morning from a warehouse containing 500 million order rows.\n"
                "2. A CSV file with 5,000 experimental observations requires a statistical significance test and visualization.\n"
                "3. A machine-learning model needs a training table built from several warehouse tables, followed by model training.\n"
                "4. For each choice, identify where the data is stored, where the computation should run, and what the final output will be."
            ),

            "expected_output": (
                "A three-row decision table containing the recommended tool(s) and a short "
                "justification based on data location, scale, computation type, and output."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tool-selection",
                "sql-reasoning",
                "analytics-workflow",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Match the Database to the Workload",

            "lesson_code": "M01.L01",

            "section_id": "row-vs-column-databases",

            "placement": "after_section",

            "description": (
                "Apply the physical-storage mental model to decide whether a row-store "
                "or column-store better matches a workload."
            ),

            "instructions": (
                "1. Consider an ecommerce checkout database that constantly inserts orders and updates payment status.\n"
                "2. Consider an analytics warehouse that scans billions of historical order rows to calculate revenue by country and month.\n"
                "3. Choose the better default architecture for each case: row-store or column-store.\n"
                "4. Explain the decision using physical storage behavior, read/write patterns, and the amount of data each query needs to scan.\n"
                "5. Identify one disadvantage of your chosen architecture in each case."
            ),

            "expected_output": (
                "A short comparison explaining the recommended database orientation for "
                "each workload, the performance reason, and one trade-off."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "database-architecture",
                "row-store",
                "column-store",
                "performance-reasoning",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Analysis with SQL — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "what-data-analysis-really-is",

                "question": (
                    "Which statement best captures the role of data analysis?"
                ),

                "options": [
                    "It is mainly the process of calculating exact metrics.",
                    "It combines discovery, interpretation, and communication to support decisions.",
                    "It is the same activity as building machine-learning models.",
                    "It is useful only when historical data perfectly predicts the future.",
                ],

                "correct": 1,

                "explanation": (
                    "Useful analysis goes beyond calculation. It investigates evidence, "
                    "interprets the result in context, and communicates it so that a decision "
                    "or action can follow."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "sql-sublanguages",

                "question": (
                    "A colleague needs permission to query a table you created. Which SQL "
                    "family is directly concerned with this task?"
                ),

                "options": [
                    "DQL",
                    "DDL",
                    "DCL",
                    "DML",
                ],

                "correct": 2,

                "explanation": (
                    "DCL manages access control. Commands such as GRANT and REVOKE change "
                    "permissions without changing the table's business records."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "sql-vs-python-r",

                "question": (
                    "Which workload is the strongest natural fit for combining SQL with Python?"
                ),

                "options": [
                    "Aggregating a warehouse table and then training a machine-learning model on the result",
                    "Renaming a single database column only",
                    "Granting a user permission to read a table",
                    "Dropping a temporary table after analysis",
                ],

                "correct": 0,

                "explanation": (
                    "SQL can efficiently extract and shape large warehouse data, while Python "
                    "provides the general-purpose and machine-learning libraries needed for model training."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "analysis-workflow",

                "question": (
                    "Which sequence correctly describes ELT?"
                ),

                "options": [
                    "Extract -> Transform -> Load",
                    "Explore -> Load -> Transform",
                    "Extract -> Load -> Transform",
                    "Extract -> Link -> Test",
                ],

                "correct": 2,

                "explanation": (
                    "ELT loads data into the destination before performing transformations, "
                    "often taking advantage of the computing power of the warehouse itself."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "row-vs-column-databases",

                "question": (
                    "Why is a column-store often efficient for a query such as SUM(revenue) "
                    "across hundreds of millions of rows?"
                ),

                "options": [
                    "Because it always stores every complete row in memory",
                    "Because it can read values from the needed column without scanning every unrelated column in each row",
                    "Because it requires a primary key on every analytical table",
                    "Because updates and deletes are always cheaper in a column-store",
                ],

                "correct": 1,

                "explanation": (
                    "Column-oriented storage groups values from the same column together. For a "
                    "large aggregation using only a few columns, this can reduce unnecessary I/O "
                    "and enable effective compression."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "other-data-infrastructure",

                "question": (
                    "Why might an organization copy application data from a NoSQL store into a SQL warehouse?"
                ),

                "options": [
                    "Because NoSQL systems cannot store any structured data",
                    "Because warehouses are usually better optimized for large-scale analytical scans and aggregations",
                    "Because SQL warehouses cannot connect to BI tools",
                    "Because NoSQL databases never support low-latency application access",
                ],

                "correct": 1,

                "explanation": (
                    "NoSQL systems are often chosen for application access patterns such as low-latency "
                    "key retrieval, while analytical warehouses are designed to scan and aggregate large "
                    "numbers of records efficiently."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "analysis-workflow",

                "type": "open",

                "question": (
                    "A company asks, 'Why did customer retention fall last quarter?' Describe a "
                    "reasonable end-to-end analysis workflow from the business question to the final "
                    "communication. Mention where SQL would be used and where another tool might be appropriate."
                ),
            },
        ],

        "passing_score": 70,
    },
}
