"""M01.L07 — Integrating Databases into AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 7, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L07"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Learn when AI services need persistent storage, choose relational or nonrelational "
    "databases appropriately, integrate PostgreSQL with FastAPI through SQLAlchemy, "
    "structure CRUD logic with repositories and services, manage schema evolution "
    "with Alembic, and persist conversation data around streaming workflows."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Integrating Databases into AI Services",

    "slug": "generative-ai-services-m01-l07",

    "description": (
        "Learn how databases fit into GenAI backends, when a database is unnecessary, "
        "how SQL and NoSQL systems differ, how to use PostgreSQL with SQLAlchemy and "
        "FastAPI, how to design async sessions and CRUD APIs, how repository/service "
        "patterns improve maintainability, and how Alembic migrations keep evolving "
        "schemas under control."
    ),

    "order": 7,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "databases",
        "postgresql",
        "sql",
        "nosql",
        "sqlalchemy",
        "alembic",
        "fastapi",
        "async-database",
        "crud",
        "repositories",
        "services",
        "migrations",
        "streaming-persistence",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L06",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Integrating Databases into AI Services",

        "content": """
# Integrating Databases into AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L07  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 7 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Decide whether an AI service needs a database at all.
- Explain the roles of relational and nonrelational databases.
- Recognize common NoSQL categories and the problems they are suited to.
- Explain how several database types can coexist in one GenAI/RAG architecture.
- Run PostgreSQL as a development database.
- Explain what an ORM does and why SQLAlchemy is useful.
- Define SQLAlchemy ORM models with primary keys, foreign keys, relationships, indexes, and timestamps.
- Create an asynchronous SQLAlchemy engine and session factory.
- Manage database sessions through FastAPI dependency injection.
- Separate database entities from Pydantic API schemas.
- Implement RESTful CRUD operations for conversation records.
- Use pagination and avoid unnecessary database round-trips.
- Explain the repository and service patterns.
- Keep business logic out of repositories.
- Explain why production systems need database migrations.
- Create and apply Alembic migrations conceptually.
- Explain upgrade/downgrade workflows and migration history.
- Avoid schema drift and migration-history problems in teams.
- Persist complete LLM conversations after streaming responses finish.
- Explain how background tasks can help persistence around streamed outputs.

---

## 1. Do you actually need a database?

A database is useful, but it is not mandatory for every application.

The chapter begins with an important architectural principle:

> **Do not add a database simply because production systems often have one. Add it when the application has persistent state or data-management requirements that justify the complexity.**

A database may be unnecessary when:

- every session can start fresh,
- data can be recomputed cheaply,
- the amount of data is tiny enough for memory,
- losing data is acceptable,
- users or instances do not need shared state,
- required information already lives in external systems,
- users can tolerate recomputation,
- files, browser storage, or cloud storage are sufficient,
- the project is only a proof of concept.

### Example: disposable image-generation demo

Imagine:

```text
User enters prompt
      ↓
model creates image
      ↓
image shown
      ↓
session ends
```

If:

- no login is required,
- images are not stored,
- history is irrelevant,
- regeneration is cheap,

then adding a relational database may add work without adding meaningful value.

### When a database becomes necessary

A database becomes much more valuable when your service needs:

- persistence across restarts,
- user accounts,
- conversation history,
- usage tracking,
- billing records,
- shared state,
- reliable querying,
- indexing,
- concurrent access,
- backups and restoration,
- authorization around stored data.

For a production conversational AI service, persistent conversation and user data are common reasons to introduce a database.

{{exercise:M01.L07.EX01}}

---

## 2. A mental model of database systems

The chapter groups databases into two broad categories:

```text
Relational
→ SQL

Nonrelational
→ NoSQL
```

The distinction is not simply "old versus new."

It is mainly about:

- data model,
- schema behavior,
- query style,
- consistency/scale characteristics,
- use case.

### Common structural hierarchy

The source gives a useful general mental model:

```text
Database server
    ↓
one or more databases
    ↓
one or more schemas
    ↓
tables or collections
    ↓
rows or documents/items
```

Relational systems usually use:

```text
tables
rows
columns
relationships
constraints
```

Nonrelational systems may instead organize information as:

- key-value pairs,
- documents,
- graph nodes/edges,
- vectors,
- wide-column records.

[[IMAGE_NEEDED: Database system hierarchy | Diagram showing database server → database → schema → table/collection → rows/documents, with SQL and NoSQL branches | Learner should notice that different database products still share a broad hierarchy of server, logical databases, structures, and records]]

---

## 3. Relational and nonrelational databases

### Relational databases

Relational databases organize data into tables.

Example:

```text
conversations
-----------------------------------------
id | title | model_type | created_at

messages
---------------------------------------------------------
id | conversation_id | prompt | response | created_at
```

Relationships can connect records.

For example:

```text
Conversation 1
   ├── Message 1
   ├── Message 2
   └── Message 3
```

SQL is used to query and manipulate this structured data.

Relational databases are a strong fit when:

- relationships matter,
- consistency matters,
- transactions matter,
- structured querying is important.

### Nonrelational databases

NoSQL systems use several different data models.

The chapter introduces several categories.

| Type | Data model | Example use cases |
|---|---|---|
| Key-value | key → value | caching, sessions |
| Graph | nodes + edges | relationships, recommendations, fraud graphs |
| Document | flexible documents | content, flexible schemas |
| Vector | high-dimensional vectors | semantic search, RAG |
| Wide-column | column-family records | analytics, logging, time-oriented workloads |

### Key-value stores

Example mental model:

```text
"session:123" → {...}
"cache:prompt_hash" → cached response
```

Useful when access is primarily by key.

### Graph databases

Represent:

```text
node ──edge── node
```

Useful when relationships themselves are important.

### Document databases

Store flexible document-like objects.

Useful when records can vary structurally or evolve often.

### Vector databases

Store embeddings and support similarity search.

This is especially relevant for:

- RAG,
- semantic search,
- recommendations.

### Wide-column stores

Designed for large distributed datasets and high-throughput patterns.

### One application can use several databases

A sophisticated GenAI service may combine:

```text
PostgreSQL
→ users, conversations, usage

Vector DB
→ embeddings

Graph DB
→ knowledge relationships

Redis
→ cache/session state

Document DB
→ flexible prompts/configuration
```

[[IMAGE_NEEDED: Multi-database GenAI architecture | Diagram showing a GenAI/RAG application connected to PostgreSQL for users/conversations, a vector database for embeddings, a graph database for document relationships, Redis for caching, and a document database for flexible prompt templates | Learner should notice that database choice is per problem rather than one database replacing every other type]]

### Principle

> **Choose a database because its data model matches a problem, not because one database category is universally superior.**

{{exercise:M01.L07.EX02}}

---

## 4. Project goal: persist LLM conversations

The chapter's main project stores:

- conversations,
- messages,
- prompt/response content,
- token usage,
- request success metadata.

The selected database is PostgreSQL.

### Why PostgreSQL here?

The data has clear relationships:

```text
one conversation
→ many messages
```

This is a natural relational model.

### Local development with Docker

The source uses a PostgreSQL container.

Conceptually:

```bash
docker run \
  -p 5432:5432 \
  -e POSTGRES_USER=fastapi \
  -e POSTGRES_PASSWORD=... \
  -e POSTGRES_DB=backend_db \
  -v ./dbstorage:/var/lib/postgresql/data \
  postgres
```

Important ideas:

- expose the database port,
- configure credentials,
- create a database,
- mount storage so data survives container recreation.

### Python packages

The chapter uses:

```text
psycopg
→ PostgreSQL Python driver

SQLAlchemy
→ SQL toolkit + ORM

Alembic
→ schema migration tool
```

These solve different layers of the database workflow.

---

## 5. What an ORM does

An **object-relational mapper (ORM)** maps database concepts into object-oriented code.

Conceptually:

```text
SQL table
↔ Python class

SQL column
↔ class attribute

SQL row
↔ class instance
```

Instead of writing:

```sql
SELECT * FROM users WHERE id = 1;
```

an ORM can let you express equivalent operations in Python.

### Why use an ORM?

Advantages from the chapter include:

- abstraction over SQL,
- faster development,
- maintainability,
- reusable application patterns.

Trade-offs include:

- learning curve,
- less direct control,
- harder debugging,
- possible performance issues in complex queries.

### The key lesson

An ORM does **not** make database performance irrelevant.

You still need to understand:

- queries,
- indexes,
- relationships,
- transactions,
- joins,
- pagination.

An ORM changes the interface, not the underlying database realities.

---

## 6. Define conversation and message ORM models

The chapter defines two related tables.

### Conversation

Conceptually:

```python
class Conversation(Base):
    __tablename__ = "conversations"

    id = ...
    title = ...
    model_type = ...
    created_at = ...
    updated_at = ...
```

### Message

```python
class Message(Base):
    __tablename__ = "messages"

    id = ...
    conversation_id = ...
    prompt_content = ...
    response_content = ...
    prompt_tokens = ...
    response_tokens = ...
    total_tokens = ...
    is_success = ...
    status_code = ...
    created_at = ...
    updated_at = ...
```

### Relationship

```text
Conversation
    1
    │
    │ has many
    ▼
Messages
```

A message contains a foreign key referencing the conversation.

### Primary key

Uniquely identifies one row.

```text
Conversation.id
Message.id
```

### Foreign key

References another table.

```text
Message.conversation_id
→ Conversation.id
```

### Cascade delete

The source configures message records to be deleted when their parent conversation is deleted.

Conceptually:

```text
delete conversation
       ↓
delete its messages
```

This keeps related data consistent.

### Indexes

The chapter adds indexes to values likely to be filtered.

For example:

```text
model_type
conversation_id
```

An index can improve query speed at the cost of:

- additional storage,
- extra update overhead.

### Nullable fields

Fields such as usage metrics may allow `NULL`.

That reflects the reality that some information may not be available for every request.

[[IMAGE_NEEDED: Conversation-message relational schema | Simple ER diagram showing `conversations` with primary key `id`, and `messages` with primary key `id` plus foreign key `conversation_id`; draw a one-to-many relationship and note cascade delete | Learner should notice how relational modeling connects conversation history]]

{{exercise:M01.L07.EX03}}

---

## 7. Create an asynchronous SQLAlchemy engine

FastAPI is often used with asynchronous I/O.

Database access is a strong candidate for async because the application frequently waits for the database server.

The source uses:

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    database_url,
    echo=True,
)
```

### Database URL

The connection string conceptually contains:

```text
driver://username:password@host/database
```

Example structure:

```text
postgresql+psycopg://...
```

### Why async?

The main FastAPI process can await database I/O while serving other requests.

```text
request A → waiting for PostgreSQL
request B → can progress
request C → can progress
```

### Development-only `create_all`

The source demonstrates dropping and creating tables programmatically.

That can be acceptable in an early prototype.

But it is dangerous for production.

Why?

Because:

```text
drop tables
→ data disappears
```

And `create_all()` is not a migration system for evolving existing schemas.

The chapter therefore transitions to Alembic later.

---

## 8. Manage database sessions safely

A database session represents an interaction context with the database.

The application should:

1. open a session,
2. perform work,
3. commit or rollback,
4. close the session.

### Session factory

The chapter creates an async session factory:

```python
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)
```

### FastAPI dependency

```python
async def get_db_session():
    try:
        async with async_session() as session:
            yield session

    except:
        await session.rollback()
        raise

    finally:
        await session.close()
```

This expresses a resource lifecycle:

```text
request begins
    ↓
open session
    ↓
yield to controller
    ↓
controller/repository uses DB
    ↓
commit or rollback
    ↓
close session
```

### Why `yield` is useful

FastAPI can treat the dependency like a context-managed resource.

Code before `yield` performs setup.

Code after it performs cleanup.

### Rollback

If an exception occurs during a transaction:

```text
partial changes
    ↓
rollback
    ↓
database returns to previous consistent transaction state
```

### Why disable autocommit?

The source favors explicit transaction control.

This lets the application decide:

```text
when a unit of work is complete
→ commit
```

rather than writing changes automatically at unexpected points.

{{exercise:M01.L07.EX04}}

---

## 9. Separate database entities from API schemas

The chapter intentionally keeps two model layers.

### SQLAlchemy model

Represents:

```text
database structure
```

### Pydantic model

Represents:

```text
API input/output contract
```

Example:

```python
class ConversationBase(BaseModel):
    title: str
    model_type: str


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(ConversationBase):
    pass


class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

### Why duplicate-looking models?

Because the database and API may evolve independently.

For example:

```text
database
→ contains internal fields

API
→ should expose only selected fields
```

Or:

```text
API create request
→ should not allow client to set ID
```

The apparent duplication creates architectural freedom.

### `from_attributes=True`

The source enables Pydantic to validate data from SQLAlchemy objects.

That makes conversion straightforward:

```python
ConversationOut.model_validate(
    conversation_entity
)
```

### Alternative mentioned in the chapter

The source mentions SQLModel as a way to combine Pydantic and SQLAlchemy concepts.

But it also notes that separate models can offer more flexibility in complex applications.

---

## 10. Build CRUD endpoints

CRUD stands for:

```text
Create
Read
Update
Delete
```

For conversations, a REST-style API may expose:

```text
GET    /conversations
GET    /conversations/{id}
POST   /conversations
PUT    /conversations/{id}
DELETE /conversations/{id}
```

### List records

The chapter uses pagination:

```python
select(Conversation)
    .offset(skip)
    .limit(take)
```

Why?

Returning an unlimited table is inefficient.

### Retrieve one record

A reusable dependency fetches a conversation by ID.

If it does not exist:

```text
404 Not Found
```

The source then reuses this dependency across:

- GET one,
- UPDATE,
- DELETE.

That can reduce duplicated lookup logic within the request.

### Create

Conceptually:

```python
new_conversation = Conversation(
    **body.model_dump()
)

session.add(new_conversation)
await session.commit()
await session.refresh(new_conversation)
```

### Update

```text
load existing row
    ↓
apply validated fields
    ↓
commit
    ↓
refresh
```

### Delete

```text
load existing row
    ↓
delete
    ↓
commit
```

### Status codes highlighted in the chapter

| Operation | Typical success status shown |
|---|---:|
| Read | 200 |
| Create | 201 |
| Update | 202 |
| Delete | 204 |

### Avoid unnecessary round-trips

A database round-trip is communication from your service to the database and back.

The source encourages reusing request-scoped dependencies where possible.

FastAPI dependency caching applies within a request, not globally across every request.

{{exercise:M01.L07.EX05}}

---

## 11. Move database logic into repositories

Controllers become hard to maintain if they contain:

- HTTP handling,
- SQL queries,
- transaction logic,
- business logic,
- error mapping.

The repository pattern separates data-access operations.

Conceptually:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
Database
```

### Abstract repository interface

The source introduces an abstract base class with methods such as:

```text
list
get
create
update
delete
```

A concrete repository implements those operations for a specific entity.

### ConversationRepository

Responsibilities:

- list conversations,
- retrieve one,
- create one,
- update one,
- delete one.

### Why this improves the code

Controllers can become closer to:

```python
conversation = await repository.get(id)
```

instead of directly managing query syntax and transactions everywhere.

### Important boundary

Repositories should focus on:

> **data access and persistence**

They should not become giant containers for all application behavior.

---

## 12. Add a service layer for business logic

The chapter extends the repository pattern with services.

### Repository

Answers:

```text
How do I read or write this data?
```

### Service

Answers:

```text
What business operation should happen?
```

For example:

```text
list messages in a conversation
```

may require a domain-oriented operation beyond a basic generic CRUD method.

A `ConversationService` can coordinate this.

### Why separate services?

A business operation may eventually require:

```text
check user permission
    ↓
read conversation
    ↓
read messages
    ↓
call model
    ↓
update usage
    ↓
persist result
```

That workflow does not belong inside a low-level repository.

### Avoid inheritance confusion

The source demonstrates a service extending the repository for convenience.

The architectural principle to retain is broader:

> Repositories own persistence concerns; services own business workflows.

The exact class relationship can vary.

### Keep responsibilities narrow

The chapter warns against:

- tightly coupling services to implementations,
- overloading services,
- placing business rules inside repositories.

{{exercise:M01.L07.EX06}}

---

## 13. Query efficiency and database round-trips

The chapter repeatedly emphasizes efficiency.

### Pagination

Avoid:

```text
SELECT every row
```

when the client only needs a small page.

Use:

```text
offset
limit
```

### Indexes

Useful for fields frequently involved in:

- filters,
- joins,
- lookups.

But every index has a write/storage cost.

### Reduce duplicated lookups

If one request needs the same conversation several times, request-scoped dependency reuse can avoid repeating identical database work.

### Be careful with joins

The chapter warns that complex queries with many JOINs can become expensive.

The ORM does not remove this cost.

### Let the database do database work

Relational engines are highly optimized for:

- filtering,
- sorting,
- joining,
- indexing,
- aggregation.

Do not pull massive datasets into Python only to reimplement operations the database can perform more efficiently.

---

## 14. Why schema migrations are necessary

During prototyping, you can delete and recreate tables.

In production, that is unacceptable.

Suppose your application already has:

```text
100,000 conversations
500,000 messages
```

Then you decide to add:

```text
messages.cost
```

You cannot simply drop and recreate everything.

You need a controlled schema change.

### Migration mental model

The chapter compares Alembic to version control for database schemas.

```text
code history
→ Git commits

database schema history
→ migration revisions
```

A migration records:

- how to move schema forward,
- how to reverse it when possible.

### Alembic structure

After initialization:

```text
alembic.ini

alembic/
    env.py
    versions/
        migration_001.py
        migration_002.py
        ...
```

### `env.py`

Connects Alembic to:

- database URL,
- SQLAlchemy metadata.

### Autogenerate

Conceptually:

```bash
alembic revision --autogenerate -m "Initial migration"
```

Alembic compares:

```text
SQLAlchemy model metadata
vs.
current database schema
```

and generates a migration candidate.

### Important practice

Autogenerated migrations should still be reviewed.

A tool can generate operations, but developers remain responsible for ensuring the migration is safe.

[[IMAGE_NEEDED: Code and database migration history | Parallel timelines showing Git commits for application code and Alembic revisions for database schema; arrows should show application versions aligning with schema versions across development/staging/production | Learner should notice that schema evolution is versioned and deployed deliberately]]

{{exercise:M01.L07.EX07}}

---

## 15. Upgrade, downgrade, and migration history

A migration commonly defines:

```python
def upgrade():
    ...
```

and:

```python
def downgrade():
    ...
```

### Upgrade

Moves the schema forward.

Examples:

- create a table,
- add a column,
- create an index.

### Downgrade

Attempts to reverse the migration.

Examples:

- drop the new column,
- remove the newly created table.

### Apply latest migrations

Conceptually:

```bash
alembic upgrade head
```

### Revert

Conceptually:

```bash
alembic downgrade ...
```

### Alembic version table

Alembic records applied migration revisions in the database.

This lets it know:

```text
which migrations already ran
```

so it does not repeat them every time.

### Do not rewrite applied migrations

The source strongly warns:

> Once a migration has been applied, commit it and create a new migration for later changes.

Why?

Because the database only knows that a revision ID was applied.

Editing the already-applied file does not automatically cause Alembic to rerun it.

### Team workflow

A healthy workflow is:

```text
change ORM models
    ↓
create new migration
    ↓
review migration
    ↓
test upgrade
    ↓
test downgrade where appropriate
    ↓
commit code + migration
    ↓
apply in target environment
```

---

## 16. Prevent code, schema, and data drift

Several things evolve at the same time:

```text
application code
database schema
migration history
actual stored data
```

If they get out of sync, the application can fail in surprising ways.

### Schema drift

The live database structure no longer matches what the code expects.

Example:

```text
code expects column: total_cost
database does not have it
```

### Migration drift

Different environments have applied different migration histories.

Example:

```text
developer A → revision 5
staging → revision 4
production → revision 3
```

### Data drift

Stored values no longer match new assumptions.

Example:

```text
old records allow NULL
new business logic assumes non-NULL
```

### Team discipline

The chapter emphasizes:

- committing migrations,
- creating new migration files for new changes,
- keeping environments aligned,
- handling transactions carefully,
- avoiding hard-coded configuration.

The main principle is:

> **Changing database code safely requires coordinating code, schema, migration history, and existing data.**

---

## 17. Persist streamed LLM conversations

Streaming creates a special persistence problem.

The response arrives piece by piece:

```text
token 1
token 2
token 3
...
```

But a relational message record usually wants:

```text
complete prompt
complete response
conversation_id
metadata
```

### Why not commit every token?

The chapter argues that traditional relational transactions are not naturally suited to treating each streamed token as part of one long-lived transaction.

Instead:

```text
stream full answer to user
        ↓
collect final complete content
        ↓
persist complete message
```

### Background task pattern

Conceptually:

```text
LLM stream
  ├── copy A → client
  └── copy B → collect complete answer
                 ↓
          background database write
```

The source uses stream duplication so one copy goes to `StreamingResponse` and another can be stored.

### Simplified conceptual implementation

```python
async def store_message(
    prompt: str,
    response: str,
    conversation_id: int,
    session: AsyncSession,
):
    ...
```

Then:

```python
background_tasks.add_task(
    store_message,
    prompt,
    full_response,
    conversation_id,
    session,
)
```

### Architectural lesson

Separate:

```text
real-time delivery
```

from:

```text
durable persistence
```

The client should not have to wait for the database write after the visible stream has already completed.

### Important production consideration

The chapter demonstrates FastAPI background tasks as the mechanism.

For more durable or failure-sensitive workflows, the same principle may later be implemented with a stronger job/queue architecture.

---

## 18. Generate conversation metadata with the LLM

The source also uses the LLM to generate a conversation title.

Flow:

```text
first user prompt
      ↓
small LLM request:
"suggest title"
      ↓
generated title
      ↓
create Conversation row
```

This is a useful example of combining:

- AI inference,
- application metadata,
- relational persistence.

### Why store the title?

A conversation list can display meaningful labels such as:

```text
FastAPI database migration help
```

instead of:

```text
Conversation 42
```

### Keep generation and persistence separate

The service can:

1. request a title,
2. validate/clean the result,
3. create the database entity.

The model does not directly write database rows.

Trusted application logic remains responsible for persistence.

---

## 19. Put the database architecture together

A clean GenAI backend from this chapter can look like:

```text
                         ┌───────────────────┐
                         │      Client       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ FastAPI Router    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Controller/API    │
                         │ + Pydantic schema │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Service layer     │
                         └─────────┬─────────┘
                                   │
                       ┌───────────┴───────────┐
                       │                       │
                       ▼                       ▼
             ┌───────────────────┐    ┌───────────────────┐
             │ Repository        │    │ Model Provider    │
             └─────────┬─────────┘    └───────────────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ SQLAlchemy        │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ PostgreSQL        │
             └───────────────────┘

Schema evolution:
SQLAlchemy models → Alembic revisions → PostgreSQL schema
```

### Request lifecycle example

Create a conversation:

```text
POST /conversations
      ↓
Pydantic validation
      ↓
controller
      ↓
service/repository
      ↓
SQLAlchemy session
      ↓
PostgreSQL transaction
      ↓
Pydantic response
```

### Streaming conversation lifecycle

```text
User prompt
    ↓
LLM stream
    ├──→ client in real time
    │
    └──→ complete response
             ↓
        background persistence
             ↓
        messages table
```

This is the chapter's core integration story:

> **The database should act as a reliable persistence layer around the GenAI workflow, while the application maintains clear contracts, transactions, abstractions, and migration history.**

---

## Important misconceptions

### Misconception 1

> Every production AI application needs a database.

### Why this is wrong

A stateless or disposable proof of concept may not need persistence at all.

### Misconception 2

> SQL databases and NoSQL databases are competing solutions where only one can be used.

### Why this is wrong

A complex GenAI application may use relational, vector, graph, document, and key-value stores together for different problems.

### Misconception 3

> An ORM means I no longer need to understand database concepts.

### Why this is wrong

Queries, relationships, indexing, transactions, and performance still matter beneath the ORM abstraction.

### Misconception 4

> `create_all()` is enough for production schema evolution.

### Why this is wrong

It can create missing tables but is not a controlled migration history for evolving active production schemas.

### Misconception 5

> A database session can be opened and forgotten.

### Why this is wrong

Sessions must be committed or rolled back appropriately and closed so resources are released.

### Misconception 6

> Pydantic models and SQLAlchemy models are redundant duplicates.

### Why this is wrong

They serve different contracts: API schemas versus persistence schemas.

### Misconception 7

> Repositories should contain all business logic because they already access the database.

### Why this is wrong

Repositories should focus on persistence; higher-level services should coordinate business workflows.

### Misconception 8

> Pagination only matters for frontend UX.

### Why this is wrong

Pagination also reduces database and network load by preventing unnecessarily large result sets.

### Misconception 9

> Once an Alembic migration is applied, editing that same migration file updates the database automatically.

### Why this is wrong

Applied revision IDs are tracked. New schema changes should be represented by new migration revisions.

### Misconception 10

> Database schema changes only affect the database team.

### Why this is wrong

Schema changes affect ORM models, services, APIs, migrations, tests, and existing data assumptions.

### Misconception 11

> Streaming responses should write every token directly into one relational transaction.

### Why this is wrong

The chapter recommends completing the stream and persisting the full message afterward.

### Misconception 12

> If an LLM generates a conversation title, it should write the title directly to PostgreSQL.

### Why this is wrong

The model proposes content; trusted application logic performs validation and persistence.

---

## Key terminology

| Term | Meaning |
|---|---|
| Database | System for persisting, organizing, retrieving, and managing data |
| Relational database | Database structured mainly around tables, rows, relationships, and SQL |
| NoSQL | Broad category of nonrelational data stores |
| Key-value store | Database storing values accessed primarily by key |
| Graph database | Database representing entities as nodes and relationships as edges |
| Document database | Database storing document-like flexible records |
| Vector database | Database specialized for storing and searching high-dimensional vectors |
| Wide-column store | Distributed database organized around column families |
| PostgreSQL | Open-source relational database used in the chapter project |
| ORM | Object-relational mapper that maps tables/rows to program objects |
| SQLAlchemy | Python SQL toolkit and ORM used by the chapter |
| psycopg | PostgreSQL database adapter for Python |
| Alembic | Migration tool commonly used with SQLAlchemy |
| Primary key | Column/value that uniquely identifies a row |
| Foreign key | Column referencing a key in another table |
| Relationship | ORM/database association between related entities |
| Cascade delete | Automatically deleting dependent records when a parent is deleted |
| Index | Additional database structure that can speed selected queries |
| Async engine | SQLAlchemy engine designed for asynchronous database operations |
| Session | Unit of database interaction/transaction work |
| Commit | Make a transaction's changes durable |
| Rollback | Undo uncommitted changes from a failed transaction |
| CRUD | Create, read, update, delete |
| Pagination | Retrieving a bounded subset of rows |
| Repository | Abstraction focused on database access operations |
| Service | Higher-level component coordinating business logic/workflows |
| Migration | Versioned database schema change |
| Upgrade | Apply a migration forward |
| Downgrade | Revert a migration backward where supported |
| Schema drift | Live database structure no longer matching application expectations |
| Migration drift | Environments having inconsistent migration histories |
| Data drift | Existing stored data no longer matching new application assumptions |
| Background task | Work executed after the main client response path can complete |

---

## Self-check

Before continuing, make sure you can answer:

1. When can a GenAI service reasonably avoid having a database?
2. What problems become easier once a database is introduced?
3. What broad categories do SQL and NoSQL represent?
4. What is the hierarchy from database server down to individual records?
5. What is a key-value store good at?
6. What is a graph database good at?
7. Why are vector databases useful in RAG?
8. Why might one application use PostgreSQL, Redis, a vector database, and a graph database together?
9. Why is PostgreSQL a natural fit for conversations and messages?
10. What does an ORM map between?
11. What are two advantages and two disadvantages of ORMs?
12. What is the difference between a primary key and a foreign key?
13. What does cascade delete do in the conversation/message relationship?
14. Why add an index to `conversation_id` or another commonly filtered field?
15. Why are some message metrics nullable?
16. What does an asynchronous SQLAlchemy engine provide?
17. Why is `create_all()` not a production migration strategy?
18. What is the lifecycle of a database session?
19. When should a transaction be rolled back?
20. Why use `yield` in a FastAPI session dependency?
21. Why separate SQLAlchemy database models from Pydantic API schemas?
22. What does `from_attributes=True` enable?
23. What are the five CRUD operations/endpoints represented in the chapter?
24. Why paginate list endpoints?
25. What is a database round-trip?
26. Why can FastAPI dependency caching reduce duplicated work within one request?
27. What should belong in a repository?
28. What should belong in a service?
29. Why should repositories avoid business logic?
30. What problem does Alembic solve?
31. What does Alembic autogeneration compare?
32. Why should autogenerated migrations still be reviewed?
33. What does `alembic upgrade head` conceptually do?
34. What is the purpose of a migration downgrade?
35. How does Alembic know which revisions already ran?
36. Why should applied migrations not be edited in place?
37. What is schema drift?
38. What is migration drift?
39. What is data drift?
40. Why should code and migration files be committed together?
41. Why is storing each streamed LLM token directly in one relational transaction awkward?
42. How can a background task help persist a completed streamed answer?
43. What two consumers can receive duplicated stream content in the chapter's pattern?
44. How can an LLM help create a conversation title?
45. Why should application logic—not the model—perform the actual database write?
46. How do routers, services, repositories, SQLAlchemy, and PostgreSQL fit together?

---

## Retain this idea

**Use databases deliberately: choose storage technology according to the data problem, keep API schemas separate from persistence models, isolate database access behind repositories and business workflows behind services, manage transactions and query efficiency explicitly, and treat schema migrations as version-controlled production changes. In streaming GenAI workflows, deliver output in real time first and persist the completed interaction through a controlled application workflow.**
""",

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "do-you-need-database",
                "title": "Do you actually need a database?",
                "order": 1,
            },
            {
                "id": "database-mental-model",
                "title": "A mental model of database systems",
                "order": 2,
            },
            {
                "id": "sql-vs-nosql",
                "title": "Relational and nonrelational databases",
                "order": 3,
            },
            {
                "id": "project-postgres",
                "title": "Project goal: persist LLM conversations",
                "order": 4,
            },
            {
                "id": "orm",
                "title": "What an ORM does",
                "order": 5,
            },
            {
                "id": "orm-models",
                "title": "Define conversation and message ORM models",
                "order": 6,
            },
            {
                "id": "async-engine",
                "title": "Create an asynchronous SQLAlchemy engine",
                "order": 7,
            },
            {
                "id": "database-sessions",
                "title": "Manage database sessions safely",
                "order": 8,
            },
            {
                "id": "api-vs-db-models",
                "title": "Separate database entities from API schemas",
                "order": 9,
            },
            {
                "id": "crud",
                "title": "Build CRUD endpoints",
                "order": 10,
            },
            {
                "id": "repository-pattern",
                "title": "Move database logic into repositories",
                "order": 11,
            },
            {
                "id": "service-pattern",
                "title": "Add a service layer for business logic",
                "order": 12,
            },
            {
                "id": "query-efficiency",
                "title": "Query efficiency and database round-trips",
                "order": 13,
            },
            {
                "id": "schema-migrations",
                "title": "Why schema migrations are necessary",
                "order": 14,
            },
            {
                "id": "upgrade-downgrade",
                "title": "Upgrade, downgrade, and migration history",
                "order": 15,
            },
            {
                "id": "schema-drift",
                "title": "Prevent code, schema, and data drift",
                "order": 16,
            },
            {
                "id": "streaming-db-storage",
                "title": "Persist streamed LLM conversations",
                "order": 17,
            },
            {
                "id": "conversation-title",
                "title": "Generate conversation metadata with the LLM",
                "order": 18,
            },
            {
                "id": "full-architecture",
                "title": "Put the database architecture together",
                "order": 19,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L07.EX01",

            "title": "Decide Whether You Need a Database",

            "lesson_code": "M01.L07",

            "section_id": "do-you-need-database",

            "placement": "after_section",

            "description": (
                "Decide whether persistent database storage is justified for different AI applications."
            ),

            "instructions": (
                "For each scenario, choose `database needed`, `database optional`, or "
                "`database probably unnecessary`, then explain why:\n\n"
                "1. A one-page demo that generates an image and never stores it.\n"
                "2. A chatbot with logged-in users and conversation history.\n"
                "3. A batch classifier whose results can be recomputed cheaply from source files.\n"
                "4. A paid AI SaaS that tracks credits, usage, and invoices.\n"
                "5. A temporary local prototype used by one developer.\n\n"
                "Use the chapter's persistence, reliability, sharing, and recomputation criteria."
            ),

            "expected_output": (
                "A five-row decision table with justification for each scenario."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "database-selection",
                "architecture-reasoning",
                "persistence-requirements",
            ],
        },

        {
            "id": "M01.L07.EX02",

            "title": "Choose the Database Type",

            "lesson_code": "M01.L07",

            "section_id": "sql-vs-nosql",

            "placement": "after_section",

            "description": (
                "Match GenAI data problems to database models."
            ),

            "instructions": (
                "Choose the most appropriate primary database type for each need:\n\n"
                "1. User accounts, subscriptions, and conversations.\n"
                "2. Semantic retrieval over document embeddings.\n"
                "3. Frequently reused cached LLM responses by hash key.\n"
                "4. Rich relationships between entities in a knowledge graph.\n"
                "5. Prompt templates whose structure changes often.\n\n"
                "Use relational, vector, key-value, graph, or document storage and explain each choice."
            ),

            "expected_output": (
                "Five database-type selections with reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sql-nosql-selection",
                "genai-storage-design",
            ],
        },

        {
            "id": "M01.L07.EX03",

            "title": "Model Conversations and Messages",

            "lesson_code": "M01.L07",

            "section_id": "orm-models",

            "placement": "after_section",

            "description": (
                "Design the relational schema behind persisted chat history."
            ),

            "instructions": (
                "Design two SQLAlchemy-style entities: `Conversation` and `Message`.\n\n"
                "`Conversation` should include:\n"
                "- primary key,\n"
                "- title,\n"
                "- model type,\n"
                "- created/updated timestamps.\n\n"
                "`Message` should include:\n"
                "- primary key,\n"
                "- conversation foreign key,\n"
                "- prompt,\n"
                "- response,\n"
                "- token counters,\n"
                "- success/status information,\n"
                "- timestamps.\n\n"
                "Add the one-to-many relationship and explain where an index would be useful."
            ),

            "expected_output": (
                "Two ORM model definitions or detailed pseudocode plus an explanation of keys, relationship, and index."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "relational-modeling",
                "sqlalchemy-orm",
                "foreign-keys",
            ],
        },

        {
            "id": "M01.L07.EX04",

            "title": "Build a Safe Async Session Dependency",

            "lesson_code": "M01.L07",

            "section_id": "database-sessions",

            "placement": "after_section",

            "description": (
                "Practice transaction cleanup and resource handling with an async SQLAlchemy session."
            ),

            "instructions": (
                "Write a FastAPI dependency that:\n"
                "1. creates an `AsyncSession`,\n"
                "2. yields it to the route,\n"
                "3. rolls back if an exception occurs,\n"
                "4. re-raises the exception,\n"
                "5. closes the session in `finally`.\n\n"
                "Then explain why explicit commit/rollback control is useful in a service "
                "that may perform several database operations in one workflow."
            ),

            "expected_output": (
                "An async session dependency plus transaction-management explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sqlalchemy-session",
                "transactions",
                "fastapi-dependencies",
            ],
        },

        {
            "id": "M01.L07.EX05",

            "title": "Design Conversation CRUD Endpoints",

            "lesson_code": "M01.L07",

            "section_id": "crud",

            "placement": "after_section",

            "description": (
                "Build a resource-oriented CRUD interface with validation and pagination."
            ),

            "instructions": (
                "Design these routes:\n\n"
                "- `GET /conversations`\n"
                "- `GET /conversations/{id}`\n"
                "- `POST /conversations`\n"
                "- `PUT /conversations/{id}`\n"
                "- `DELETE /conversations/{id}`\n\n"
                "Requirements:\n"
                "1. use separate Pydantic create/update/output schemas,\n"
                "2. paginate the list endpoint,\n"
                "3. reuse a dependency that raises 404 when the conversation does not exist,\n"
                "4. commit mutations,\n"
                "5. return appropriate success status codes."
            ),

            "expected_output": (
                "A CRUD route design or implementation with pagination, dependency reuse, and response/status behavior."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "crud",
                "rest-api",
                "pydantic-sqlalchemy",
            ],
        },

        {
            "id": "M01.L07.EX06",

            "title": "Separate Repository and Service Responsibilities",

            "lesson_code": "M01.L07",

            "section_id": "service-pattern",

            "placement": "after_section",

            "description": (
                "Practice keeping persistence logic separate from business workflows."
            ),

            "instructions": (
                "You need a feature called `delete_conversation_for_user`.\n\n"
                "The workflow must:\n"
                "1. load the conversation,\n"
                "2. confirm the requesting user owns it,\n"
                "3. delete it,\n"
                "4. record an audit event.\n\n"
                "Decide which responsibilities belong in:\n"
                "- controller,\n"
                "- service,\n"
                "- repository.\n\n"
                "Explain why ownership checking should not be buried in a generic repository."
            ),

            "expected_output": (
                "A responsibility table and a layered flow for the business operation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "repository-pattern",
                "service-layer",
                "separation-of-concerns",
            ],
        },

        {
            "id": "M01.L07.EX07",

            "title": "Create a Safe Migration Workflow",

            "lesson_code": "M01.L07",

            "section_id": "schema-migrations",

            "placement": "after_section",

            "description": (
                "Model how a production team should introduce a schema change without resetting the database."
            ),

            "instructions": (
                "Assume you must add a nullable `cost` column to the `messages` table.\n\n"
                "Describe the workflow:\n"
                "1. update the ORM model,\n"
                "2. autogenerate a migration,\n"
                "3. inspect the migration,\n"
                "4. test upgrade,\n"
                "5. test downgrade where appropriate,\n"
                "6. commit the migration,\n"
                "7. deploy/apply it.\n\n"
                "Then explain why editing an already-applied migration file is unsafe."
            ),

            "expected_output": (
                "A migration checklist plus an explanation of immutable applied migration history."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "alembic",
                "schema-migrations",
                "database-change-management",
            ],
        },

        {
            "id": "M01.L07.EX08",

            "title": "Persist a Completed LLM Stream",

            "lesson_code": "M01.L07",

            "section_id": "streaming-db-storage",

            "placement": "after_section",

            "description": (
                "Combine real-time response streaming with durable relational persistence."
            ),

            "instructions": (
                "Design a flow for an SSE chatbot endpoint that:\n"
                "1. validates that the conversation exists,\n"
                "2. streams LLM chunks immediately to the client,\n"
                "3. builds or copies the full generated response,\n"
                "4. stores prompt + complete response after streaming,\n"
                "5. records the conversation ID,\n"
                "6. handles database failure without corrupting the already-delivered client stream.\n\n"
                "Draw the client-stream path separately from the persistence path."
            ),

            "expected_output": (
                "A two-path architecture diagram plus persistence/error-handling explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "streaming-persistence",
                "background-tasks",
                "conversation-storage",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L07.QZ01",

        "title": "Integrating Databases into AI Services — Knowledge Check",

        "lesson_code": "M01.L07",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L07.Q01",

                "section_id": "do-you-need-database",

                "question": (
                    "Which scenario most clearly does NOT require a database?"
                ),

                "options": [
                    "A disposable image-generation demo that stores nothing between sessions",
                    "A paid chatbot that stores user subscriptions",
                    "A system that must retain conversation history",
                    "An application that tracks usage across users",
                ],

                "correct": 0,

                "explanation": (
                    "If no state must persist and data can be regenerated cheaply, a database "
                    "may add unnecessary complexity."
                ),
            },

            {
                "id": "M01.L07.Q02",

                "section_id": "sql-vs-nosql",

                "question": "Which database type is most directly associated with semantic vector search?",

                "options": [
                    "Vector database",
                    "Key-value store",
                    "Relational database only",
                    "Wide-column store only",
                ],

                "correct": 0,

                "explanation": (
                    "Vector databases are designed to store and search high-dimensional vector representations."
                ),
            },

            {
                "id": "M01.L07.Q03",

                "section_id": "orm",

                "question": "What does an ORM primarily map?",

                "options": [
                    "Relational tables and rows to classes and objects",
                    "HTTP requests to GPU kernels",
                    "Vector embeddings to images",
                    "WebSocket frames to SQL migrations",
                ],

                "correct": 0,

                "explanation": (
                    "An ORM maps relational database structures to program objects and operations."
                ),
            },

            {
                "id": "M01.L07.Q04",

                "section_id": "orm-models",

                "question": (
                    "What is the purpose of `Message.conversation_id` in the chapter's schema?"
                ),

                "options": [
                    "It acts as a foreign key linking each message to its conversation",
                    "It stores the LLM temperature",
                    "It replaces the message primary key",
                    "It is used only for CORS",
                ],

                "correct": 0,

                "explanation": (
                    "The foreign key models the one-conversation-to-many-messages relationship."
                ),
            },

            {
                "id": "M01.L07.Q05",

                "section_id": "database-sessions",

                "question": "Why should a failed database transaction be rolled back?",

                "options": [
                    "To avoid leaving partial uncommitted changes in an inconsistent transaction state",
                    "To increase model temperature",
                    "To disable indexes",
                    "To regenerate the API schema",
                ],

                "correct": 0,

                "explanation": (
                    "Rollback cancels the incomplete transaction so later work starts from a consistent state."
                ),
            },

            {
                "id": "M01.L07.Q06",

                "section_id": "api-vs-db-models",

                "question": (
                    "Why does the chapter keep Pydantic API schemas separate from SQLAlchemy entities?"
                ),

                "options": [
                    "So API contracts and persistence models can evolve independently",
                    "Because FastAPI cannot use SQLAlchemy",
                    "Because PostgreSQL cannot store strings",
                    "Because Pydantic creates database indexes",
                ],

                "correct": 0,

                "explanation": (
                    "Separating the models reduces coupling and allows API and database structures "
                    "to change independently."
                ),
            },

            {
                "id": "M01.L07.Q07",

                "section_id": "crud",

                "question": "Why should a conversation list endpoint use pagination?",

                "options": [
                    "To avoid retrieving unnecessarily large result sets",
                    "To force every record to use the same primary key",
                    "To disable transactions",
                    "To replace indexing",
                ],

                "correct": 0,

                "explanation": (
                    "Pagination reduces database, memory, and network load by retrieving only a subset."
                ),
            },

            {
                "id": "M01.L07.Q08",

                "section_id": "repository-pattern",

                "question": "What belongs primarily in a repository?",

                "options": [
                    "Database access and persistence operations",
                    "All business rules and UI state",
                    "Model training",
                    "Browser rendering",
                ],

                "correct": 0,

                "explanation": (
                    "Repositories abstract persistence operations from higher application layers."
                ),
            },

            {
                "id": "M01.L07.Q09",

                "section_id": "service-pattern",

                "question": "What is the main responsibility of a service layer?",

                "options": [
                    "Coordinate higher-level business workflows",
                    "Replace every database table",
                    "Serve static HTML files only",
                    "Generate Alembic revision IDs",
                ],

                "correct": 0,

                "explanation": (
                    "Services coordinate application/business operations, often using repositories and providers."
                ),
            },

            {
                "id": "M01.L07.Q10",

                "section_id": "schema-migrations",

                "question": "Why is Alembic needed in production?",

                "options": [
                    "To apply versioned schema changes without resetting the entire database",
                    "To train embeddings",
                    "To create WebSocket connections",
                    "To replace Pydantic validation",
                ],

                "correct": 0,

                "explanation": (
                    "Alembic provides controlled schema evolution and migration history."
                ),
            },

            {
                "id": "M01.L07.Q11",

                "section_id": "upgrade-downgrade",

                "question": (
                    "Why should you create a new migration instead of editing one that has already been applied?"
                ),

                "options": [
                    "Applied revision IDs are already recorded, so editing the file does not automatically reapply it",
                    "Alembic supports only one migration ever",
                    "PostgreSQL cannot add new columns",
                    "New migrations delete all old data automatically",
                ],

                "correct": 0,

                "explanation": (
                    "Migration systems track applied revisions; subsequent schema changes should receive new revisions."
                ),
            },

            {
                "id": "M01.L07.Q12",

                "section_id": "schema-drift",

                "question": "What is schema drift?",

                "options": [
                    "The live database structure no longer matches what the application expects",
                    "An LLM generating a different answer twice",
                    "A WebSocket client reconnecting",
                    "A vector embedding changing dimensions during inference",
                ],

                "correct": 0,

                "explanation": (
                    "Schema drift occurs when deployed database structure and application expectations diverge."
                ),
            },

            {
                "id": "M01.L07.Q13",

                "section_id": "streaming-db-storage",

                "question": (
                    "What persistence pattern does the chapter recommend for an LLM stream?"
                ),

                "options": [
                    "Stream to the client, then persist the complete response through background work",
                    "Keep one relational transaction open for every generated token",
                    "Never store streamed conversations",
                    "Write each token as a new conversation row",
                ],

                "correct": 0,

                "explanation": (
                    "The source separates real-time delivery from storing the completed message."
                ),
            },

            {
                "id": "M01.L07.Q14",

                "section_id": "conversation-title",

                "question": (
                    "What role does the LLM play when creating a conversation title?"
                ),

                "options": [
                    "It proposes title content, while application code persists the record",
                    "It directly bypasses the application and writes to PostgreSQL",
                    "It creates Alembic migrations",
                    "It chooses database indexes",
                ],

                "correct": 0,

                "explanation": (
                    "The model generates content, while trusted application code performs database operations."
                ),
            },

            {
                "id": "M01.L07.Q15",

                "section_id": "full-architecture",

                "type": "open",

                "question": (
                    "Design the persistence layer for a production conversational AI service. "
                    "Explain which data belongs in PostgreSQL, how FastAPI obtains a database "
                    "session, where repositories and services sit, how schema migrations are "
                    "managed, and how a fully streamed LLM response is stored after delivery."
                ),
            },
        ],

        "passing_score": 70,
    },
}
