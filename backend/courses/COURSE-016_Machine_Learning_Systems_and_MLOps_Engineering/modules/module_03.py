"""M03.L01 — Data Engineering Fundamentals.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 3, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Data Engineering for Machine Learning Systems"

MODULE_DESCRIPTION = (
    "Build the data-engineering foundation needed for production ML: understand "
    "where data comes from, how it is serialized and modeled, how storage and "
    "processing systems differ, how data moves between services, and when to use "
    "batch or stream processing."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Data Engineering Fundamentals",

    "slug": "ml-systems-design-m03-l01",

    "description": (
        "A practical introduction to the data systems behind production machine "
        "learning, including data sources, serialization formats, row-major and "
        "column-major storage, relational/document/graph models, structured and "
        "unstructured data, OLTP and OLAP, ETL and ELT, inter-service dataflow, "
        "and batch versus stream processing."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "data-engineering",
        "data-sources",
        "serialization",
        "json",
        "csv",
        "parquet",
        "row-major",
        "column-major",
        "relational-data",
        "nosql",
        "document-database",
        "graph-database",
        "data-warehouse",
        "data-lake",
        "oltp",
        "olap",
        "acid",
        "etl",
        "elt",
        "dataflow",
        "microservices",
        "event-driven",
        "batch-processing",
        "stream-processing",
    ],

    "prerequisite_ids": ["M02.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Data Engineering Fundamentals",

        "content": (
            "# Data Engineering Fundamentals\n"
            "\n"
            "> **Lesson:** M03.L01  \n"
            "> **Module:** Data Engineering for Machine Learning Systems  \n"
            "> **Source alignment:** Chapter 3. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Identify common data sources used by production ML systems.\n"
            "- Explain why user-generated, system-generated, internal, and "
            "third-party data require different handling.\n"
            "- Explain data serialization and compare common formats such as "
            "JSON, CSV, Parquet, Avro, Protobuf, and Pickle at a high level.\n"
            "- Distinguish row-major from column-major storage and choose between "
            "them based on access patterns.\n"
            "- Explain why binary formats are often more compact than text formats.\n"
            "- Distinguish relational, document, and graph data models.\n"
            "- Explain structured versus unstructured data and the roles of data "
            "warehouses and data lakes.\n"
            "- Compare transactional and analytical workloads and explain ACID.\n"
            "- Explain ETL, ELT, and why hybrid lakehouse designs emerged.\n"
            "- Compare data passing through databases, services, and real-time transports.\n"
            "- Explain request-driven versus event-driven architectures.\n"
            "- Distinguish batch processing from stream processing and static from "
            "dynamic features.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why data engineering matters for ML\n"
            "\n"
            "Machine learning systems do not begin with a model. They begin with "
            "data that must be collected, validated, stored, moved, transformed, "
            "retrieved, and processed before a model can use it.\n"
            "\n"
            "In production, these operations often span many systems and services. "
            "A feature engineering service may transform raw events into features, "
            "while a prediction service consumes those features to make predictions. "
            "The data has to move reliably between them.\n"
            "\n"
            "This means data engineering answers practical questions such as:\n"
            "\n"
            "- Where does the data come from?\n"
            "- In what format should we store it?\n"
            "- How should we model its structure?\n"
            "- Which storage engine should we use?\n"
            "- How should one service pass data to another?\n"
            "- Should we process data periodically or continuously?\n"
            "\n"
            "A useful mental model for this chapter is:\n"
            "\n"
            "```text\n"
            "Sources → Formats → Models → Storage/Processing → Dataflow → ML features\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: End-to-end data engineering pipeline for ML | "
            "A left-to-right diagram showing data sources feeding serialization "
            "formats, data models, storage/processing systems, inter-service "
            "dataflow, feature generation, and finally an ML model | Learner "
            "should notice that the model is only one consumer at the end of a "
            "larger data pipeline]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Data sources in production ML\n"
            "\n"
            "Different data sources have different quality, latency, privacy, and "
            "processing characteristics. Understanding the source helps you decide "
            "how to validate and process the data.\n"
            "\n"
            "### User input data\n"
            "\n"
            "Users may provide text, images, video, files, numerical fields, or "
            "other inputs.\n"
            "\n"
            "User input should be treated as potentially malformed. A user may:\n"
            "\n"
            "- enter text where a number is expected,\n"
            "- upload a file in the wrong format,\n"
            "- provide unusually short or long text,\n"
            "- submit unexpected values.\n"
            "\n"
            "Because users usually expect immediate feedback, user input often "
            "requires both **strong validation** and **low-latency processing**.\n"
            "\n"
            "### System-generated data\n"
            "\n"
            "Systems generate logs, model predictions, job results, metrics, and "
            "events describing user behavior.\n"
            "\n"
            "Logs can record information such as:\n"
            "\n"
            "- memory usage,\n"
            "- service calls,\n"
            "- package or dependency versions,\n"
            "- training-job outcomes,\n"
            "- batch-processing results,\n"
            "- application errors.\n"
            "\n"
            "Logs are usually more regular than user input because software creates "
            "them. However, their volume can become enormous. Logging everything "
            "can make debugging difficult because useful signals become hidden in "
            "noise.\n"
            "\n"
            "Log retention also matters. Old logs that are rarely accessed can "
            "often be moved to cheaper storage or deleted when no longer useful.\n"
            "\n"
            "### Behavioral data is still user data\n"
            "\n"
            "Clicks, scrolling, time spent on pages, ignored popups, and purchase "
            "history may be automatically generated by the system, but they still "
            "describe user behavior. The chapter emphasizes that such data can be "
            "subject to privacy requirements.\n"
            "\n"
            "### Internal databases\n"
            "\n"
            "Organizations maintain internal databases for inventory, users, "
            "customer relationships, assets, transactions, and other business data.\n"
            "\n"
            "An ML model may depend on these databases directly. For example, a "
            "search system can understand a query but still needs inventory data "
            "before ranking products that are actually available.\n"
            "\n"
            "### First-, second-, and third-party data\n"
            "\n"
            "- **First-party data:** collected by your own organization from your "
            "users or customers.\n"
            "- **Second-party data:** collected by another organization from its "
            "own customers and made available to you.\n"
            "- **Third-party data:** collected by organizations about people who "
            "are not necessarily their direct customers.\n"
            "\n"
            "The chapter notes that privacy changes have reduced some forms of "
            "third-party tracking and increased the importance of first-party data.\n"
            "\n"
            "{{exercise:M03.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Data serialization and common formats\n"
            "\n"
            "Once data exists, you often need to persist or transmit it.\n"
            "\n"
            "**Serialization** is the process of converting a data structure or "
            "object state into a format that can be stored or transmitted and later "
            "reconstructed.\n"
            "\n"
            "When choosing a format, ask:\n"
            "\n"
            "- Is it human-readable?\n"
            "- Is it text or binary?\n"
            "- How large will the stored data be?\n"
            "- How will the data usually be accessed?\n"
            "- Does the format need to support complex or nested objects?\n"
            "\n"
            "The chapter introduces several common formats:\n"
            "\n"
            "| Format | Text/Binary | Human-readable | Typical use |\n"
            "|---|---|---|---|\n"
            "| JSON | Text | Yes | APIs and general data interchange |\n"
            "| CSV | Text | Yes | Tabular data |\n"
            "| Parquet | Binary | No | Column-oriented analytical data |\n"
            "| Avro | Primarily binary | No | Data systems such as Hadoop |\n"
            "| Protobuf | Primarily binary | No | Compact schema-based serialization |\n"
            "| Pickle | Binary | No | Python object serialization |\n"
            "\n"
            "### JSON\n"
            "\n"
            "JSON is popular because it is simple, human-readable, language "
            "independent in practice, and can represent nested structures.\n"
            "\n"
            "Example:\n"
            "\n"
            "```json\n"
            "{\n"
            '  "firstName": "Boatie",\n'
            '  "lastName": "McBoatFace",\n'
            '  "isVibing": true,\n'
            '  "age": 12,\n'
            '  "address": {\n'
            '    "streetAddress": "12 Ocean Drive",\n'
            '    "city": "Port Royal",\n'
            '    "postalCode": "10021-3100"\n'
            "  }\n"
            "}\n"
            "```\n"
            "\n"
            "However, JSON is text-based, so it can consume more space than binary "
            "formats. Schema changes can also become painful once many applications "
            "depend on an established JSON structure.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Row-major versus column-major storage\n"
            "\n"
            "CSV and Parquet illustrate two different storage ideas.\n"
            "\n"
            "### Row-major\n"
            "\n"
            "In row-major storage, values belonging to the same row are stored "
            "close together.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Row 1: id, time, location, distance, price\n"
            "Row 2: id, time, location, distance, price\n"
            "Row 3: id, time, location, distance, price\n"
            "```\n"
            "\n"
            "This is useful when you often read or write complete records.\n"
            "\n"
            "### Column-major\n"
            "\n"
            "In column-major storage, values from the same column are stored close "
            "together.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "id:       1, 2, 3, ...\n"
            "time:     t1, t2, t3, ...\n"
            "location: A, B, C, ...\n"
            "price:    20, 25, 18, ...\n"
            "```\n"
            "\n"
            "This is useful when analytical workloads read only a subset of columns.\n"
            "\n"
            "### Example\n"
            "\n"
            "Suppose a ride-sharing table has 1,000 features, but an analysis only "
            "needs four: time, location, distance, and price.\n"
            "\n"
            "A column-oriented format can read just those columns. A row-oriented "
            "format may need to read much more of each row before filtering to the "
            "needed values.\n"
            "\n"
            "### General rule from the chapter\n"
            "\n"
            "- Row-major formats tend to be attractive for frequent writes of "
            "individual records.\n"
            "- Column-major formats tend to be attractive for column-based reads "
            "and analytical workloads.\n"
            "\n"
            "[[IMAGE_NEEDED: Row-major versus column-major memory layout | "
            "A small table shown beside two storage layouts: one grouped by rows "
            "and one grouped by columns | Learner should notice why selecting a few "
            "columns is efficient in column-major storage while writing full rows "
            "fits naturally with row-major storage]]\n"
            "\n"
            "### NumPy versus pandas intuition\n"
            "\n"
            "The chapter points out that pandas is organized around the DataFrame "
            "and column-oriented operations. NumPy arrays, by contrast, are "
            "row-major by default unless another order is specified.\n"
            "\n"
            "This helps explain why repeatedly iterating through pandas rows can be "
            "slow compared with vectorized or column-oriented operations.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Text versus binary formats\n"
            "\n"
            "Text formats such as JSON and CSV can be opened and read directly by "
            "humans. Binary formats such as Parquet are intended to be interpreted "
            "by software that understands their byte layout.\n"
            "\n"
            "Binary formats are often more compact.\n"
            "\n"
            "For example, storing the number `1000000` as text requires seven "
            "characters. If one character takes one byte, that is seven bytes. As "
            "a 32-bit integer, the same value can fit in four bytes.\n"
            "\n"
            "The chapter gives an example where a 14 MB CSV version of a dataset "
            "became 6 MB when stored as Parquet.\n"
            "\n"
            "The important trade-off is not simply \"binary is better.\" The choice "
            "depends on readability, interoperability, storage cost, and access "
            "patterns.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Data models: relational, document, and graph\n"
            "\n"
            "A **data model** describes how real-world information is represented.\n"
            "\n"
            "The same real-world object can be represented differently depending "
            "on what questions the application needs to answer.\n"
            "\n"
            "For example, a car could be modeled with:\n"
            "\n"
            "- make, model, year, color, and price, or\n"
            "- owner, license plate, and registered addresses.\n"
            "\n"
            "The first representation may help buyers search for cars. The second "
            "may help trace ownership history.\n"
            "\n"
            "### Relational model\n"
            "\n"
            "The relational model organizes data into relations. Tables are the "
            "common visual representation, and each row corresponds to a tuple.\n"
            "\n"
            "A key idea is **normalization**: splitting repeated information into "
            "separate relations to reduce duplication and improve consistency.\n"
            "\n"
            "Suppose a book table repeats publisher name and country on every book "
            "row. If the publisher changes its name, many rows must be updated.\n"
            "\n"
            "Normalization can separate publisher information:\n"
            "\n"
            "```text\n"
            "BOOK\n"
            "title | author | format | publisher_id | price\n"
            "\n"
            "PUBLISHER\n"
            "publisher_id | publisher_name | country\n"
            "```\n"
            "\n"
            "Now publisher information can be updated in one place.\n"
            "\n"
            "The cost is that data may need to be joined across multiple tables, "
            "and joins can be expensive on large datasets.\n"
            "\n"
            "### SQL is declarative\n"
            "\n"
            "SQL is mainly **declarative**: you describe the result you want, while "
            "the database decides how to execute the query.\n"
            "\n"
            "By contrast, an imperative program typically describes the sequence of "
            "steps to follow.\n"
            "\n"
            "The database's query optimizer examines possible execution strategies "
            "and tries to select an efficient one.\n"
            "\n"
            "### Declarative ML\n"
            "\n"
            "The chapter draws an analogy with declarative ML systems. Instead of "
            "manually constructing and tuning every model, users can specify the "
            "features and task, while a system explores model choices.\n"
            "\n"
            "However, this does **not** remove the hardest production challenges: "
            "feature engineering, data processing, evaluation, distribution shift, "
            "and continual learning still remain.\n"
            "\n"
            "### Document model\n"
            "\n"
            "A document database stores self-contained documents, often encoded as "
            "JSON, XML, BSON, or another format. Each document has a key.\n"
            "\n"
            "Unlike a relational table, documents in one collection can have "
            "different structures.\n"
            "\n"
            "Calling this completely \"schemaless\" is misleading. The application "
            "that reads the documents still expects some structure. The "
            "responsibility for enforcing structure simply shifts.\n"
            "\n"
            "Document storage provides strong **locality** when information that "
            "belongs together can live inside one document.\n"
            "\n"
            "The downside is that cross-document relationships and joins can be "
            "more difficult or less efficient than in relational systems.\n"
            "\n"
            "### Graph model\n"
            "\n"
            "A graph consists of **nodes** and **edges**. Edges explicitly represent "
            "relationships between nodes.\n"
            "\n"
            "Graph databases are valuable when the relationships themselves are "
            "central to the query.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- social networks,\n"
            "- recommendation relationships,\n"
            "- organization networks,\n"
            "- connected entities across several hops.\n"
            "\n"
            "A query such as \"find all people connected to this country through "
            "an unknown number of relationship hops\" fits a graph model more "
            "naturally than a fixed relational join structure.\n"
            "\n"
            "[[IMAGE_NEEDED: Relational vs document vs graph models | "
            "Three side-by-side mini diagrams: normalized relational tables with "
            "foreign keys, a self-contained nested document, and a node-edge graph "
            "| Learner should notice that relational models emphasize tables, "
            "document models emphasize locality, and graph models emphasize "
            "relationships]]\n"
            "\n"
            "{{exercise:M03.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Structured and unstructured data\n"
            "\n"
            "**Structured data** follows a predefined schema.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "name: string up to 50 characters\n"
            "age: integer between 0 and 200\n"
            "```\n"
            "\n"
            "A predefined structure makes querying and analysis easier. For "
            "example, calculating average age is straightforward when every record "
            "has a defined age field.\n"
            "\n"
            "The downside is schema evolution. If you add a new field or change an "
            "old one, historical records may require migration. Poor migration "
            "choices can create subtle ML bugs—for example, replacing an unknown "
            "age with `0` can make the model treat missing values as newborn users.\n"
            "\n"
            "**Unstructured data** does not have to conform to a predefined schema. "
            "It can include text, logs, images, audio, dates, or mixed content.\n"
            "\n"
            "Unstructured does not mean pattern-free. A log file may contain "
            "repeated structure, but the storage system does not guarantee that "
            "every item follows the same schema.\n"
            "\n"
            "### Data warehouse versus data lake\n"
            "\n"
            "The chapter uses the following broad distinction:\n"
            "\n"
            "| Repository | Typical role |\n"
            "|---|---|\n"
            "| Data warehouse | Stores structured, processed, analysis-ready data |\n"
            "| Data lake | Stores raw or less-structured data before later processing |\n"
            "\n"
            "The underlying design question is often: **who carries the burden of "
            "structure—the writer or the reader?**\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Storage engines: transactional and analytical workloads\n"
            "\n"
            "A data format defines how information is encoded. A data model defines "
            "how information is represented. A **storage engine** or database "
            "implements how that information is stored and retrieved on machines.\n"
            "\n"
            "Two historically important workload categories are transactional and "
            "analytical processing.\n"
            "\n"
            "### Transactional processing (OLTP)\n"
            "\n"
            "Transactions include actions such as:\n"
            "\n"
            "- ordering a ride,\n"
            "- uploading a model,\n"
            "- posting content,\n"
            "- purchasing an item.\n"
            "\n"
            "These operations usually require low latency and high availability "
            "because users are waiting for them.\n"
            "\n"
            "Transactional systems are often associated with **ACID**:\n"
            "\n"
            "| Property | Meaning |\n"
            "|---|---|\n"
            "| Atomicity | All steps of a transaction succeed together or fail together. |\n"
            "| Consistency | Transactions obey predefined rules and preserve valid state. |\n"
            "| Isolation | Concurrent transactions behave as though appropriately isolated from one another. |\n"
            "| Durability | Once committed, a transaction remains committed despite failures. |\n"
            "\n"
            "Example: if a user's payment fails, the system should not still assign "
            "a driver. That illustrates atomicity.\n"
            "\n"
            "### Analytical processing (OLAP)\n"
            "\n"
            "Analytical workloads ask aggregate questions across large amounts of "
            "data, such as:\n"
            "\n"
            "> What was the average ride price in a city during September?\n"
            "\n"
            "These workloads often benefit from column-oriented access because "
            "they aggregate selected fields across many records.\n"
            "\n"
            "### The boundary is becoming less strict\n"
            "\n"
            "The chapter stresses that OLTP and OLAP are useful historical concepts, "
            "but modern systems increasingly blur the distinction.\n"
            "\n"
            "Another major trend is **decoupling storage from compute**. Instead of "
            "requiring one tightly coupled engine for both, organizations can keep "
            "data in shared storage while using different processing layers for "
            "different workloads.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. ETL, ELT, and the lakehouse idea\n"
            "\n"
            "### ETL\n"
            "\n"
            "**ETL** means:\n"
            "\n"
            "```text\n"
            "Extract → Transform → Load\n"
            "```\n"
            "\n"
            "#### Extract\n"
            "\n"
            "Collect the required data from source systems. This stage should also "
            "validate incoming data and reject malformed or unacceptable records "
            "before they create downstream problems.\n"
            "\n"
            "#### Transform\n"
            "\n"
            "This is where most data processing happens. Transformations may include:\n"
            "\n"
            "- joining multiple sources,\n"
            "- cleaning values,\n"
            "- standardizing representations,\n"
            "- deduplicating,\n"
            "- sorting,\n"
            "- aggregating,\n"
            "- deriving features,\n"
            "- performing additional validation.\n"
            "\n"
            "#### Load\n"
            "\n"
            "Write the transformed result into its destination, such as a file, "
            "database, or warehouse, at the required frequency.\n"
            "\n"
            "[[IMAGE_NEEDED: ETL pipeline | "
            "A simple three-stage pipeline showing raw sources entering Extract, "
            "then Transform with cleaning/joining/validation, then Load into a "
            "warehouse or database | Learner should notice that transformation "
            "happens before data reaches the target store]]\n"
            "\n"
            "### ELT\n"
            "\n"
            "As data volume and variety increased, some organizations adopted:\n"
            "\n"
            "```text\n"
            "Extract → Load → Transform\n"
            "```\n"
            "\n"
            "Raw data is loaded into storage first and transformed later when an "
            "application needs it. This enables fast ingestion and reduces the need "
            "to define every structure upfront.\n"
            "\n"
            "However, a huge raw data lake can become difficult to search and "
            "manage efficiently.\n"
            "\n"
            "### Lakehouse\n"
            "\n"
            "Hybrid designs called **data lakehouses** attempt to combine the "
            "flexibility of data lakes with the management and structure associated "
            "with data warehouses.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. How data moves between processes\n"
            "\n"
            "Production systems contain many processes that do not share memory. "
            "Data therefore has to flow from one process or service to another.\n"
            "\n"
            "The chapter describes three major modes:\n"
            "\n"
            "1. passing data through a database,\n"
            "2. passing data through services using requests,\n"
            "3. passing data through a real-time transport.\n"
            "\n"
            "### Passing data through a database\n"
            "\n"
            "Process A writes data to a database. Process B reads it.\n"
            "\n"
            "This approach is simple, but it requires both processes to access the "
            "same database, and database reads/writes may be too slow for strict "
            "latency requirements.\n"
            "\n"
            "### Passing data through services\n"
            "\n"
            "One service sends a request to another service and waits for a response.\n"
            "\n"
            "This is a **request-driven** pattern.\n"
            "\n"
            "REST and RPC are common styles. The chapter notes that REST is common "
            "for public APIs, while RPC is often used for communication between "
            "services owned by the same organization.\n"
            "\n"
            "A service-oriented design allows different components to be developed "
            "and maintained independently, leading to microservice architectures.\n"
            "\n"
            "### Ride-sharing example\n"
            "\n"
            "Imagine three services:\n"
            "\n"
            "- **Driver management:** predicts available drivers.\n"
            "- **Ride management:** predicts ride demand.\n"
            "- **Price optimization:** predicts an appropriate ride price.\n"
            "\n"
            "The price optimization service needs predictions from both supply and "
            "demand services.\n"
            "\n"
            "With only a few services, direct requests are manageable. With hundreds "
            "of interdependent services, the communication graph becomes complex.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Real-time transports and event-driven systems\n"
            "\n"
            "Direct service-to-service communication is synchronous: the target "
            "service has to be available for the request to succeed. If a dependent "
            "service is down, failures can propagate.\n"
            "\n"
            "A different approach introduces a **broker** or real-time transport.\n"
            "\n"
            "Instead of every service talking directly to every other service:\n"
            "\n"
            "```text\n"
            "Service A ─┐\n"
            "Service B ─┼──> Broker / Event Bus ───> Consumers\n"
            "Service C ─┘\n"
            "```\n"
            "\n"
            "A producer publishes data to the transport. Other services consume "
            "that data when needed.\n"
            "\n"
            "A piece of data published to such a transport is called an **event**. "
            "This is why the architecture is called **event-driven**.\n"
            "\n"
            "The chapter contrasts the two styles broadly:\n"
            "\n"
            "- Request-driven systems fit systems where direct logic and immediate "
            "request/response interactions dominate.\n"
            "- Event-driven systems are especially useful for data-heavy systems "
            "with many producers and consumers.\n"
            "\n"
            "### Publish-subscribe\n"
            "\n"
            "In pubsub, services publish events to topics. Any service subscribed "
            "to a topic can consume the events from that topic.\n"
            "\n"
            "The producer does not need to know which consumers will use the data.\n"
            "\n"
            "Examples given in the chapter include Apache Kafka and Amazon Kinesis.\n"
            "\n"
            "### Message queue\n"
            "\n"
            "In a message queue, a message often has an intended consumer or set "
            "of consumers, and the queue is responsible for delivering it appropriately.\n"
            "\n"
            "Examples given include Apache RocketMQ and RabbitMQ.\n"
            "\n"
            "[[IMAGE_NEEDED: Request-driven versus event-driven dataflow | "
            "Side-by-side diagrams showing many direct service-to-service requests "
            "versus services communicating through a central event broker | Learner "
            "should notice how the broker reduces direct coupling among many services]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Batch processing versus stream processing\n"
            "\n"
            "Once data is stored in databases, lakes, or warehouses, it becomes "
            "historical data. Historical data is commonly processed in scheduled "
            "batch jobs.\n"
            "\n"
            "### Batch processing\n"
            "\n"
            "A batch job processes a collection of data periodically.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- compute yesterday's average surge price once per day,\n"
            "- rebuild a reporting table every night,\n"
            "- calculate features that change slowly.\n"
            "\n"
            "Distributed systems such as MapReduce and Spark were developed to "
            "process large batches efficiently.\n"
            "\n"
            "### Stream processing\n"
            "\n"
            "Streaming data is still arriving through real-time transports such as "
            "Kafka or Kinesis. Stream processing computes on that data continuously "
            "or at short intervals.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- number of available drivers right now,\n"
            "- rides requested in the last minute,\n"
            "- median price of the most recent rides,\n"
            "- recent activity used for fraud detection.\n"
            "\n"
            "Stream processing can reduce latency because data can be processed as "
            "it arrives rather than first waiting for long-term storage and a later "
            "batch job.\n"
            "\n"
            "### Stateful streaming\n"
            "\n"
            "Stream processing can preserve intermediate state. Suppose you need a "
            "30-day engagement statistic.\n"
            "\n"
            "A naive daily batch job may repeatedly recompute much of the same "
            "30-day history. A stateful stream processor can update yesterday's "
            "state using only the newly arriving data.\n"
            "\n"
            "### Static versus dynamic features\n"
            "\n"
            "The chapter connects processing mode to feature behavior:\n"
            "\n"
            "| Feature type | Typical source | Example |\n"
            "|---|---|---|\n"
            "| Static / batch feature | Batch processing | A driver's long-term rating |\n"
            "| Dynamic / streaming feature | Stream processing | Drivers available right now |\n"
            "\n"
            "Many production ML systems need both kinds of features.\n"
            "\n"
            "A price optimization model, for example, might combine a slowly changing "
            "driver rating with rapidly changing supply and demand information.\n"
            "\n"
            "### Stream processing is harder\n"
            "\n"
            "Streaming systems deal with unbounded data arriving at changing rates. "
            "Complex ML applications may require hundreds or thousands of streaming "
            "features, joins, aggregations, and stateful computations.\n"
            "\n"
            "The chapter names technologies such as Apache Flink, KSQL, and Spark "
            "Streaming as examples of stream-processing tools.\n"
            "\n"
            "[[IMAGE_NEEDED: Batch versus stream feature computation | "
            "A split diagram showing historical data feeding a periodic batch job "
            "to create static features and a live event stream feeding a stream "
            "processor to create dynamic features, with both joining before model "
            "inference | Learner should notice that real production models may need "
            "both slowly changing and real-time features]]\n"
            "\n"
            "{{exercise:M03.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: A data format and a data model are the same thing\n"
            "\n"
            "They are different. A format describes how data is encoded or "
            "serialized, while a model describes how information is structured "
            "conceptually.\n"
            "\n"
            "### Misconception 2: Schemaless means no structure exists\n"
            "\n"
            "Document databases may not enforce one rigid schema at write time, but "
            "applications reading the documents still make assumptions about their "
            "structure. The responsibility is shifted rather than eliminated.\n"
            "\n"
            "### Misconception 3: OLTP and OLAP describe completely separate modern worlds\n"
            "\n"
            "They remain useful workload categories, but modern systems increasingly "
            "support both styles or separate storage from compute so multiple engines "
            "can operate on the same data.\n"
            "\n"
            "### Misconception 4: Event-driven architecture means data never needs storage\n"
            "\n"
            "Real-time transports usually retain events for a period and can move "
            "them into durable storage. They complement databases rather than make "
            "persistent storage unnecessary.\n"
            "\n"
            "### Misconception 5: Streaming replaces batch processing in every case\n"
            "\n"
            "Many features change slowly and are efficiently computed in batch. "
            "Production systems often combine batch and streaming pipelines.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Data serialization | Converting data into a form that can be stored or transmitted and reconstructed later. |\n"
            "| Access pattern | The way a system typically reads or writes data. |\n"
            "| Row-major | Storage layout that keeps values from the same row together. |\n"
            "| Column-major | Storage layout that keeps values from the same column together. |\n"
            "| Data model | A conceptual representation of how data and relationships are structured. |\n"
            "| Relational model | Data model based on relations, commonly represented as tables. |\n"
            "| Normalization | Organizing relational data to reduce duplication and improve integrity. |\n"
            "| Document model | Model based on self-contained documents such as JSON or BSON documents. |\n"
            "| Graph model | Model based on nodes and edges where relationships are first-class objects. |\n"
            "| Structured data | Data that conforms to a predefined schema. |\n"
            "| Unstructured data | Data not required to conform to one predefined schema. |\n"
            "| Data warehouse | Repository commonly used for structured, processed, analysis-ready data. |\n"
            "| Data lake | Repository commonly used for raw or less-structured data. |\n"
            "| OLTP | Processing optimized for frequent user-facing transactions. |\n"
            "| OLAP | Processing optimized for analytical queries across large amounts of data. |\n"
            "| ACID | Atomicity, consistency, isolation, and durability properties associated with transactional systems. |\n"
            "| ETL | Extract, transform, then load. |\n"
            "| ELT | Extract, load, then transform. |\n"
            "| Lakehouse | Hybrid approach combining ideas from data lakes and data warehouses. |\n"
            "| Request-driven | Communication where one service requests data directly from another. |\n"
            "| Event-driven | Communication where producers publish events that consumers can process through a broker. |\n"
            "| Pubsub | Publish-subscribe model where consumers subscribe to topics. |\n"
            "| Message queue | Messaging model where messages are delivered to intended consumers. |\n"
            "| Batch processing | Periodic processing of bounded collections of historical data. |\n"
            "| Stream processing | Processing data as it continuously arrives. |\n"
            "| Static feature | Feature that changes relatively slowly and is commonly computed in batch. |\n"
            "| Dynamic feature | Feature representing rapidly changing state and commonly computed from streams. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does user input usually require stronger validation than "
            "system-generated logs?\n"
            "2. What is serialization?\n"
            "3. When is column-major storage more attractive than row-major storage?\n"
            "4. Why are binary formats often smaller than text formats?\n"
            "5. What problem does normalization solve, and what cost can it introduce?\n"
            "6. When would a document model be more natural than a relational model?\n"
            "7. When would a graph model be especially useful?\n"
            "8. Who carries the structure responsibility in structured versus "
            "unstructured storage?\n"
            "9. What do atomicity and durability mean?\n"
            "10. What is the difference between ETL and ELT?\n"
            "11. Why can direct request-driven communication become difficult with "
            "hundreds of services?\n"
            "12. How does a broker reduce service coupling?\n"
            "13. What is the difference between pubsub and a message queue at a "
            "high level?\n"
            "14. Why would a model need both static and dynamic features?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Production ML depends on the full data lifecycle: choosing the right "
            "source, representation, storage, movement, and processing strategy is "
            "part of ML system design—not separate plumbing around the model.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-data-engineering",
                "title": "Why data engineering matters for ML",
                "order": 1,
            },
            {
                "id": "data-sources",
                "title": "Data sources in production ML",
                "order": 2,
            },
            {
                "id": "data-formats",
                "title": "Data serialization and common formats",
                "order": 3,
            },
            {
                "id": "row-column",
                "title": "Row-major versus column-major storage",
                "order": 4,
            },
            {
                "id": "text-binary",
                "title": "Text versus binary formats",
                "order": 5,
            },
            {
                "id": "data-models",
                "title": "Data models: relational, document, and graph",
                "order": 6,
            },
            {
                "id": "structured-unstructured",
                "title": "Structured and unstructured data",
                "order": 7,
            },
            {
                "id": "storage-processing",
                "title": "Storage engines: transactional and analytical workloads",
                "order": 8,
            },
            {
                "id": "etl-elt",
                "title": "ETL, ELT, and the lakehouse idea",
                "order": 9,
            },
            {
                "id": "dataflow",
                "title": "How data moves between processes",
                "order": 10,
            },
            {
                "id": "event-driven",
                "title": "Real-time transports and event-driven systems",
                "order": 11,
            },
            {
                "id": "batch-stream",
                "title": "Batch processing versus stream processing",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Classify and validate production data sources",

            "lesson_code": "M03.L01",

            "section_id": "data-sources",

            "placement": "after_section",

            "description": (
                "Practice identifying data sources and reasoning about their "
                "validation, latency, and privacy requirements."
            ),

            "instructions": (
                "You are designing an ML system for an ecommerce platform. It uses:\n"
                "- product images uploaded by sellers,\n"
                "- customer clicks and browsing history,\n"
                "- application error logs,\n"
                "- the internal inventory database,\n"
                "- a purchased demographic dataset from an external vendor.\n\n"
                "For each source:\n"
                "1. Classify it as user input, system-generated, internal database, "
                "or external/third-party data.\n"
                "2. State one likely data-quality or validation concern.\n"
                "3. State whether low-latency processing is likely important.\n"
                "4. Identify any privacy concern explicitly supported by the lesson."
            ),

            "expected_output": (
                "A five-row table listing the source type, quality concern, "
                "latency consideration, and privacy consideration for each input."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "data-source-classification",
                "data-validation",
                "privacy-awareness",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Choose a data model for the query",

            "lesson_code": "M03.L01",

            "section_id": "data-models",

            "placement": "after_section",

            "description": (
                "Practice selecting relational, document, or graph modeling based "
                "on the kinds of access patterns an application needs."
            ),

            "instructions": (
                "For each scenario, choose the most natural model discussed in "
                "the lesson and explain why:\n\n"
                "1. A payroll system with employees, departments, salaries, and "
                "well-defined relationships that require strong consistency.\n"
                "2. A content system where each article is stored with nested "
                "metadata that may differ from article to article.\n"
                "3. A fraud investigation tool that repeatedly asks how accounts, "
                "devices, payments, and users are connected across multiple hops.\n"
                "4. For one scenario, explain one disadvantage of your chosen model."
            ),

            "expected_output": (
                "Three model choices with short justifications and one explicitly "
                "identified trade-off."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "relational-modeling",
                "document-modeling",
                "graph-modeling",
                "tradeoff-reasoning",
            ],
        },

        {
            "id": "M03.L01.EX03",

            "title": "Design batch and streaming features",

            "lesson_code": "M03.L01",

            "section_id": "batch-stream",

            "placement": "after_section",

            "description": (
                "Practice deciding which features should be computed in batch and "
                "which require stream processing."
            ),

            "instructions": (
                "You are building a ride-price prediction service. Consider these features:\n"
                "- driver's long-term rating,\n"
                "- number of available drivers right now,\n"
                "- average ride price over the last 30 days,\n"
                "- number of ride requests in the last 60 seconds,\n"
                "- driver's total completed rides,\n"
                "- median price of the most recent 10 rides in the area.\n\n"
                "1. Classify each as mainly batch/static or streaming/dynamic.\n"
                "2. Explain the reason for each classification.\n"
                "3. Sketch, in words, how both feature groups could be joined before "
                "the model makes a prediction."
            ),

            "expected_output": (
                "A table classifying all six features and a short description of "
                "how the batch and streaming feature pipelines meet at inference."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "batch-processing",
                "stream-processing",
                "feature-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Data Engineering Fundamentals — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",
                "section_id": "data-sources",
                "question": (
                    "Which source is most likely to require both heavy validation "
                    "and fast processing because malformed values are common and "
                    "users expect immediate results?"
                ),
                "options": [
                    "Archived system logs",
                    "User input",
                    "A static internal reference table",
                    "A nightly backup",
                ],
                "correct": 1,
                "explanation": (
                    "User input can be malformed in many ways and is often part of "
                    "an interactive request where the user expects a fast response."
                ),
            },

            {
                "id": "M03.L01.Q02",
                "section_id": "data-formats",
                "question": "What is data serialization?",
                "options": [
                    "Training a model on data in chronological order",
                    "Converting a data structure into a storable or transmittable representation",
                    "Normalizing a relational database",
                    "Moving logs into cheaper storage",
                ],
                "correct": 1,
                "explanation": (
                    "Serialization converts a data structure or object state into "
                    "a format that can later be stored, transmitted, and reconstructed."
                ),
            },

            {
                "id": "M03.L01.Q03",
                "section_id": "row-column",
                "question": (
                    "You have a table with 1,000 columns and repeatedly analyze only "
                    "four of them across millions of rows. Which layout is generally "
                    "more suitable?"
                ),
                "options": [
                    "Column-major",
                    "Row-major",
                    "Only plain text",
                    "Only graph storage",
                ],
                "correct": 0,
                "explanation": (
                    "Column-major layouts allow reading selected columns without "
                    "necessarily scanning every field of each row."
                ),
            },

            {
                "id": "M03.L01.Q04",
                "section_id": "data-models",
                "question": (
                    "What is one important benefit of normalization in a relational model?"
                ),
                "options": [
                    "It eliminates the need for joins.",
                    "It reduces duplicated information and makes updates more consistent.",
                    "It turns every query into a graph traversal.",
                    "It guarantees every workload is low latency.",
                ],
                "correct": 1,
                "explanation": (
                    "Normalization can move repeated information into its own relation "
                    "so it can be updated in one place."
                ),
            },

            {
                "id": "M03.L01.Q05",
                "section_id": "data-models",
                "question": (
                    "Which model is most natural when relationships across an unknown "
                    "number of hops are central to the query?"
                ),
                "options": [
                    "Graph model",
                    "Flat CSV only",
                    "Simple document model",
                    "Plain text log",
                ],
                "correct": 0,
                "explanation": (
                    "Graph models represent relationships explicitly and make "
                    "multi-hop traversal a natural operation."
                ),
            },

            {
                "id": "M03.L01.Q06",
                "section_id": "structured-unstructured",
                "question": (
                    "Why is calling a document database completely 'schemaless' misleading?"
                ),
                "options": [
                    "Because every document database is relational.",
                    "Because readers still make assumptions about document structure.",
                    "Because documents cannot contain JSON.",
                    "Because document databases cannot store nested fields.",
                ],
                "correct": 1,
                "explanation": (
                    "The structural assumptions are often shifted from the writer "
                    "or database to the applications that read the documents."
                ),
            },

            {
                "id": "M03.L01.Q07",
                "section_id": "storage-processing",
                "question": (
                    "Which ACID property means that all steps of a transaction "
                    "succeed together or fail together?"
                ),
                "options": [
                    "Atomicity",
                    "Consistency",
                    "Isolation",
                    "Durability",
                ],
                "correct": 0,
                "explanation": (
                    "Atomicity treats the transaction as one indivisible unit."
                ),
            },

            {
                "id": "M03.L01.Q08",
                "section_id": "etl-elt",
                "question": "What is the key difference between ETL and ELT?",
                "options": [
                    "ETL has no extraction stage.",
                    "ELT loads data before transformation.",
                    "ELT cannot use a data lake.",
                    "ETL never validates data.",
                ],
                "correct": 1,
                "explanation": (
                    "ETL transforms before loading to the target; ELT loads first "
                    "and transforms later."
                ),
            },

            {
                "id": "M03.L01.Q09",
                "section_id": "event-driven",
                "question": (
                    "What is a major motivation for introducing a broker into a "
                    "system with many communicating services?"
                ),
                "options": [
                    "To force every service to use the same programming language",
                    "To reduce the number of direct service-to-service dependencies",
                    "To eliminate all persistent storage",
                    "To make every interaction synchronous",
                ],
                "correct": 1,
                "explanation": (
                    "A broker lets producers and consumers communicate through a "
                    "shared transport instead of requiring a dense web of direct calls."
                ),
            },

            {
                "id": "M03.L01.Q10",
                "section_id": "batch-stream",
                "question": (
                    "Which feature is the clearest example of a dynamic streaming feature?"
                ),
                "options": [
                    "A driver's long-term average rating",
                    "A user's birth year",
                    "The number of available drivers right now",
                    "A product's original launch date",
                ],
                "correct": 2,
                "explanation": (
                    "The number of available drivers changes quickly and represents "
                    "the current state of the system."
                ),
            },

            {
                "id": "M03.L01.Q11",
                "section_id": "batch-stream",
                "question": (
                    "Why can stateful stream processing avoid redundant computation "
                    "for some continuously updated statistics?"
                ),
                "options": [
                    "It can preserve previous computation and update it with new data.",
                    "It never stores any intermediate state.",
                    "It requires recomputing all historical data on every event.",
                    "It only works on static files.",
                ],
                "correct": 0,
                "explanation": (
                    "Stateful stream processing can carry forward earlier results "
                    "and update them as new events arrive."
                ),
            },

            {
                "id": "M03.L01.Q12",
                "section_id": "dataflow",
                "type": "open",
                "question": (
                    "You have five ML services that increasingly depend on each "
                    "other's outputs. Compare direct request-driven communication "
                    "with an event-driven broker for this system. Explain one benefit "
                    "and one limitation or trade-off of each using only ideas from "
                    "this lesson."
                ),
            },
        ],

        "passing_score": 70,
    },
}
