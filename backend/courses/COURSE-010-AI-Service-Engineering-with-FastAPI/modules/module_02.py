"""M01.L02 — Getting Started with FastAPI.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 2, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Build the FastAPI foundation needed for GenAI services: create and run an API, "
    "understand FastAPI's core features, organize growing projects, apply layered "
    "design, compare framework trade-offs, recognize AI-serving limitations, and "
    "set up professional Python tooling."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Getting Started with FastAPI",

    "slug": "generative-ai-services-m01-l02",

    "description": (
        "Learn how FastAPI works, create a small API service, understand routing, "
        "validation, serialization, concurrency, dependency injection, lifespan "
        "management, project structures, layered architecture, framework trade-offs, "
        "AI-serving limitations, and the tooling needed to maintain a growing backend."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "fastapi",
        "python-backend",
        "asgi",
        "api-design",
        "dependency-injection",
        "project-structure",
        "layered-architecture",
        "genai-services",
        "python-tooling",
    ],

    "prerequisite_ids": [
        "M01.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Getting Started with FastAPI",

        "content": """
# Getting Started with FastAPI

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L02  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 2 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what FastAPI is and why its ASGI foundation matters.
- Create and run a basic FastAPI project.
- Define routes with decorators and understand how requests become Python function calls.
- Explain serialization, validation, and automatic OpenAPI/Swagger documentation.
- Distinguish synchronous and asynchronous route handling at a high level.
- Explain background tasks, middleware, CORS, lifespan events, and dependency injection.
- Recognize REST, WebSocket, SSE, and GraphQL as different API communication patterns.
- Choose among flat, nested, and modular FastAPI project structures based on project complexity.
- Explain the onion/layered design pattern and the responsibilities of routers, controllers, services, providers, repositories, schemas, guards, and related components.
- Compare FastAPI conceptually with Django and Flask using the chapter's trade-offs.
- Identify FastAPI limitations for resource-intensive AI inference.
- Explain when a separate model-serving layer such as BentoML may be useful.
- Set up a maintainable Python development workflow with dependency management, formatting, linting, security scanning, type checking, and version control.

---

## 1. What FastAPI is

FastAPI is a Python web framework for building APIs and backend web services.

The chapter describes it as an **ASGI framework**. ASGI stands for **Asynchronous Server Gateway Interface**.

That matters because modern backend services often spend time waiting for external work such as:

- database queries,
- HTTP requests,
- network services,
- file operations,
- interactions with external model servers.

An asynchronous server can use that waiting time more efficiently by working on other requests instead of blocking the entire server.

FastAPI also provides several features that are especially useful for API development:

- route definitions using Python decorators,
- request and response validation,
- data serialization,
- automatic OpenAPI specifications,
- interactive Swagger documentation,
- dependency injection,
- support for synchronous and asynchronous handlers,
- middleware and security integration,
- WebSocket and other non-REST communication patterns.

FastAPI itself is built on top of **Starlette**, while **Pydantic** is central to its data validation and serialization experience.

### FastAPI, Uvicorn, Starlette, and Pydantic

It helps to separate their roles:

| Component | Role in the stack |
|---|---|
| FastAPI | The application framework you write your API with |
| Starlette | The underlying ASGI toolkit/framework used by FastAPI |
| Uvicorn | The ASGI web server that runs the application |
| Pydantic | Data parsing, schema definition, validation, and serialization support |

A beginner mistake is to think that `FastAPI()` itself opens a network port.

It does not.

You define the application with FastAPI, then an ASGI server such as Uvicorn runs it.

### Why this is relevant for GenAI

A GenAI backend often needs to coordinate:

```text
Client request
    ↓
Authentication / validation
    ↓
Database or external API
    ↓
Prompt/context preparation
    ↓
Model call
    ↓
Post-processing
    ↓
Response
```

Many of those steps involve external I/O, so a framework designed for modern API workloads is a useful foundation.

---

## 2. Set up the Python environment

The source chapter tests its examples against **Python 3.11** and warns that other Python versions or dependency combinations may behave differently.

The first goal is to create an isolated environment so the packages for this project do not interfere with packages from other projects.

### Windows with Conda

```bash
conda create -n genaiservice python=3.11
conda activate genaiservice
```

### macOS or Linux with `venv`

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the core packages

The chapter installs:

```bash
pip install "fastapi[standard]" uvicorn openai
```

The central idea is more important than memorizing the command:

> **Create an isolated environment, then install only the dependencies your service needs.**

This improves reproducibility and reduces package conflicts.

### Why virtual environments matter

Without isolation, two projects might need incompatible versions of the same package.

For example:

```text
Project A → package X version 1
Project B → package X version 2
```

If both rely on one global Python installation, changing the package for one project may break the other.

A virtual environment gives each project its own dependency space.

---

## 3. Build your first FastAPI server

A minimal FastAPI application begins by creating an application object.

```python
from fastapi import FastAPI

app = FastAPI()
```

Now we can turn Python functions into HTTP endpoints.

### A health endpoint

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_controller():
    return {"status": "healthy"}
```

There are three important ideas here.

### 1. `app = FastAPI()`

This creates the application object.

### 2. `@app.get("/")`

This decorator connects an HTTP request to a Python function.

It means:

```text
HTTP GET /
    ↓
root_controller()
```

### 3. Returning a Python dictionary

The route returns:

```python
{"status": "healthy"}
```

FastAPI serializes that Python object into JSON so it can travel over HTTP.

A client then receives something equivalent to:

```json
{
  "status": "healthy"
}
```

### Adding a simple GenAI route

The source chapter demonstrates a route that passes a prompt to a language-model API.

A simplified conceptual form is:

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key="your_api_key")


@app.get("/chat")
def chat_controller(prompt: str = "Inspire me"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    statement = response.choices[0].message.content
    return {"statement": statement}
```

Study the flow rather than memorizing every library call:

```text
GET /chat?prompt=...
        ↓
FastAPI reads the query parameter
        ↓
chat_controller(prompt)
        ↓
model API request
        ↓
model response
        ↓
Python dictionary
        ↓
JSON response
```

The route is already a tiny GenAI service because the model is exposed through a web API.

### Run the development server

The chapter uses:

```bash
fastapi dev
```

During development, the server can watch your files and reload when the code changes.

The service becomes available locally, with endpoints such as:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/chat
```

and automatically generated documentation at:

```text
http://127.0.0.1:8000/docs
```

### What Uvicorn is doing

Conceptually:

```text
Browser / API client
        ↓
HTTP request
        ↓
Uvicorn
        ↓
FastAPI application
        ↓
Route handler
        ↓
HTTP response
```

FastAPI defines application behavior.

Uvicorn serves that application over the network.

{{exercise:M01.L02.EX01}}

---

## 4. Automatic docs, serialization, and validation

One of FastAPI's strongest beginner advantages is that several pieces of API infrastructure appear automatically from your Python declarations.

### OpenAPI and Swagger documentation

FastAPI generates an **OpenAPI specification** for your service.

That specification can power a Swagger UI page at `/docs`.

The page lets you:

- inspect endpoints,
- see expected parameters,
- see schemas,
- send test requests,
- inspect responses.

[[IMAGE_NEEDED: FastAPI Swagger UI | A screenshot or recreated local development view of a FastAPI `/docs` page showing at least two endpoints, their HTTP methods, parameters, and the interactive 'Try it out' workflow | Learner should notice that endpoint documentation and interactive testing are generated from the API definitions rather than being written manually]]

Interactive docs are useful during development, but the chapter emphasizes that they **do not replace automated tests**.

A mature service still needs systematic tests because clicking endpoints manually does not reliably verify every behavior after every code change.

### Serialization

HTTP does not transmit arbitrary live Python objects.

Data must be converted into a transferable representation such as JSON.

Conceptually:

```text
Python dictionary
      ↓
serialization
      ↓
JSON
      ↓
HTTP
      ↓
client
      ↓
deserialization
      ↓
client-side object
```

If a route returns a Python dictionary, FastAPI handles the serialization for you.

### Validation

Validation asks:

> Does the incoming data satisfy the rules required by this API?

For a user-creation request, you may want rules such as:

- username must be text,
- password must meet policy requirements,
- email must have a valid format.

Pydantic schemas let you express and enforce these kinds of runtime constraints.

A conceptual model looks like this:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
```

FastAPI can use the schema to parse and validate incoming request data before your business logic operates on it.

### Static typing is not runtime validation

A type checker can warn about code during development.

Runtime validation protects the live application from bad incoming data.

These solve different problems.

```text
Static type checking
→ analyzes your code before runtime

Runtime validation
→ checks actual data entering the running service
```

Both become increasingly important as an API grows.

---

## 5. Concurrency, background tasks, middleware, and CORS

### Synchronous and asynchronous route handlers

FastAPI supports both:

```python
@app.get("/sync")
def sync_route():
    ...
```

and:

```python
@app.get("/async")
async def async_route():
    ...
```

The chapter explains that asynchronous routes run through the main event loop, while synchronous handlers can be executed through worker threads.

The practical lesson is:

> **Concurrency is most useful when a request spends time waiting for I/O.**

Examples include:

- database access,
- HTTP calls,
- external services,
- network communication.

### Async does not make CPU-heavy work free

This is a crucial boundary.

Suppose a route performs expensive model inference directly inside the web process.

That workload is not simply "waiting."

It may consume substantial CPU or GPU compute.

Even an `async def` route can become a bottleneck if it performs blocking compute-heavy work.

We will revisit this in the FastAPI limitations section.

### Background tasks

Some work does not need to finish before the client receives an acknowledgement.

Examples include:

- sending an email,
- post-processing an upload,
- indexing a large document,
- inserting embeddings into a vector database.

A useful pattern is:

```text
Client request
      ↓
Server validates request
      ↓
Server accepts work
      ↓
Immediate response to client
      ↓
Background operation continues
```

The chapter specifically uses document processing for vector storage as a GenAI example.

This helps prevent a long-running operation from keeping a user-facing request open unnecessarily.

### Middleware

Middleware sits around request handling.

Think of it as a layer that sees requests before they reach the endpoint and responses before they return to the client.

```text
Client
  ↓
Middleware
  ↓
Route handler
  ↓
Middleware
  ↓
Client
```

Middleware can support tasks such as:

- logging,
- adding or modifying headers,
- cookies,
- request checks,
- monitoring,
- CORS behavior.

### CORS

CORS is relevant when a frontend and backend operate across different origins.

For example:

```text
Frontend: https://app.example.com
Backend:  https://api.example.com
```

Browser security rules may require the backend to explicitly allow the frontend origin.

FastAPI supports middleware for this kind of configuration.

### Customization

Because FastAPI builds on Starlette, the chapter notes that you can customize behavior through mechanisms such as:

- custom exception handlers,
- ASGI middleware,
- custom responses,
- custom serialization.

This gives you flexibility when default framework behavior is not sufficient.

{{exercise:M01.L02.EX02}}

---

## 6. Dependency injection: reusable logic without duplication

FastAPI has a dependency injection system built around `Depends`.

The chapter connects this to **inversion of control**.

The practical problem it solves is easy to see.

Imagine many endpoints need the same pagination logic:

```python
def paginate(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

Without reuse, every route may repeat the same parameter parsing.

With dependency injection:

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def paginate(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/messages")
def list_messages_controller(
    pagination: dict = Depends(paginate),
):
    return {"pagination": pagination}


@app.get("/conversations")
def list_conversations_controller(
    pagination: dict = Depends(paginate),
):
    return {"pagination": pagination}
```

Both routes depend on the same reusable function.

### Why dependency injection matters

Dependencies can centralize reusable concerns such as:

- pagination,
- database sessions,
- authentication,
- authorization,
- shared request parsing,
- feature checks,
- user loading.

This reduces duplication and makes responsibilities easier to test independently.

### Database-session example

The chapter gives a pattern where a dependency creates a database session, yields it to the route, then closes it.

Conceptually:

```python
def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()
```

The request flow becomes:

```text
Request begins
    ↓
get_db() opens session
    ↓
route receives session
    ↓
route performs database work
    ↓
response completes
    ↓
get_db() cleanup closes session
```

This helps prevent resource leaks.

### Dependencies are request-scoped and reusable

The chapter notes that a dependency result can be cached within the context of one request.

If several parts of the same request depend on the same dependency, FastAPI can reuse its result rather than repeating the work unnecessarily.

On the next request, the dependency runs again.

### Hierarchical dependency graphs

A dependency can depend on another dependency.

For example:

```text
get_db
  ↓
get_current_user
  ↓
require_admin
  ↓
admin-only endpoint
```

This creates a dependency graph.

It is especially useful for:

- authentication,
- authorization,
- nested data retrieval,
- decision logic.

{{image:dependency-injection}}

### Dependency injection is not just convenience

Used well, it changes the structure of your application.

Instead of a controller manually constructing everything it needs, the controller declares its requirements.

That is an important step toward a layered architecture.

{{exercise:M01.L02.EX03}}

---

## 7. Lifespan events, security, and communication patterns

### Lifespan events

Some resources are expensive to create for every request.

Examples include:

- database connection pools,
- large AI models,
- shared clients,
- caches.

FastAPI lifespan events allow you to initialize shared resources during application startup and clean them up during shutdown.

The pattern is:

```text
Application starts
       ↓
Load shared resources
       ↓
Serve many requests
       ↓
Application stops
       ↓
Clean up resources
```

For GenAI, this is especially useful when a model should be loaded once and reused.

Loading the same model from disk for every request would be inefficient.

### Security and authentication

FastAPI provides security components but does not force one specific authentication implementation.

The chapter emphasizes flexibility:

- you can build your own authentication layer,
- you can use third-party packages,
- you can integrate external identity providers.

This fits FastAPI's generally nonopinionated style.

### REST endpoints

REST commonly uses HTTP methods such as:

```text
GET     → retrieve
POST    → create
PUT     → replace/update
PATCH   → partially update
DELETE  → delete
```

Example resource routes:

```text
GET    /api/messages
POST   /api/messages
GET    /api/messages/{id}
PUT    /api/messages/{id}
PATCH  /api/messages/{id}
DELETE /api/messages/{id}
```

### WebSockets and SSE

A normal request/response exchange is not always ideal for GenAI.

When generating text token by token, the client may want the response progressively.

The chapter points to:

- **WebSockets (WS)** for persistent bidirectional communication,
- **Server-Sent Events (SSE)** for streamed server-to-client updates.

These are useful for real-time AI interfaces.

### GraphQL

The chapter also mentions GraphQL as an alternative API approach where clients can request selected fields and avoid retrieving unnecessary data.

FastAPI can integrate GraphQL through external packages, although GraphQL is not the chapter's main focus.

### Modern Python and IDE support

Because FastAPI makes strong use of modern Python features such as type annotations, editors and developer tools can provide:

- autocomplete,
- type diagnostics,
- formatting,
- linting,
- easier navigation.

This contributes to developer experience as a project grows.

---

## 8. Structuring a FastAPI project

A one-file FastAPI application is easy to understand.

A production service is not.

As features accumulate, a project may contain:

- routes,
- schemas,
- database models,
- repositories,
- business logic,
- authentication,
- external APIs,
- AI model clients,
- prompts,
- retrieval logic,
- background tasks,
- utilities.

Without organization, developers can end up with:

- enormous files,
- unclear ownership,
- circular imports,
- hard-to-find functions,
- changes that unexpectedly affect many files.

The chapter presents three project structures: **flat, nested, and modular**.

### 8.1 Flat structure

A flat project keeps a small number of files close together.

```text
flat-project/
├── app/
│   ├── services.py
│   ├── database.py
│   ├── models.py
│   ├── routers.py
│   └── main.py
├── requirements.txt
├── .env
└── .gitignore
```

This works well when:

- the service is small,
- you are prototyping,
- the architecture is still evolving,
- there are only a few files.

The advantage is simplicity.

The problem appears when each file grows into a large global bucket.

### 8.2 Nested structure

A nested structure groups code by technical category.

```text
nested-project/
├── app/
│   ├── main.py
│   ├── dependencies.py
│   ├── services/
│   │   ├── users.py
│   │   └── profiles.py
│   ├── models/
│   │   ├── users.py
│   │   └── profiles.py
│   └── routers/
│       ├── users.py
│       └── profiles.py
├── requirements.txt
├── .env
└── .gitignore
```

This makes it easier to locate code by its technical role.

However, one feature may be spread across many directories.

Changing one domain concept can require edits in several places.

The chapter describes broad cascading edits as **shotgun updates**.

### 8.3 Modular structure

A modular structure groups closely related components by domain or feature.

```text
modular-project/
├── app/
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── routers.py
│   │   │   ├── models.py
│   │   │   ├── dependencies.py
│   │   │   ├── guards.py
│   │   │   └── services.py
│   │   ├── users/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── dependencies.py
│   │   │   ├── services.py
│   │   │   ├── mappers.py
│   │   │   └── pipes.py
│   │   └── profiles/
│   ├── providers/
│   │   ├── email.py
│   │   └── stripe.py
│   ├── settings.py
│   ├── middlewares.py
│   ├── models.py
│   ├── exceptions.py
│   └── main.py
├── requirements.txt
├── .env
└── .gitignore
```

The main idea is **feature encapsulation**.

Everything strongly related to authentication lives near authentication.

Everything strongly related to users lives near users.

This can make it easier to predict where a change belongs and what it may affect.

### Progressive reorganization

The chapter does not tell you to begin every project with maximum architecture.

Instead, it recommends allowing structure to evolve:

```text
Flat
  ↓
Nested
  ↓
Modular
```

A useful decision rule is:

| Project state | Reasonable structure |
|---|---|
| Small experiment or first version | Flat |
| Growing microservice with several technical areas | Nested |
| Larger backend with multiple domains/features | Modular |

The important lesson is not that one structure is universally correct.

It is:

> **Your structure should make the location, responsibility, and impact of code easy to understand.**

If another developer cannot understand why a file lives where it does, the structure may need reconsideration.

{{exercise:M01.L02.EX04}}

---

## 9. Onion/layered application design

Project structure tells you **where files live**.

Layered design tells you **what responsibilities different parts of the system should have and how they should depend on each other**.

The chapter introduces the **onion design pattern**.

The core idea is separation of concerns.

At the center are domain concepts and business rules.

Outer layers handle details such as APIs, external services, persistence, and user interaction.

{{image:onion-architecture}}
{{image:controllers-services-providers-repositories}}

### Dependency inversion

The chapter connects onion architecture to the **dependency inversion principle**.

Instead of high-level logic constructing and depending directly on low-level implementations, components declare what they need and receive compatible dependencies.

This reduces coupling.

For example, a business service should not need to know every detail of how a database connection was created.

It can depend on a repository interface that provides the data operation it needs.

### Layer responsibilities

Let's walk from the HTTP boundary inward.

### API routers

Routers group related route handlers.

For example:

```text
/users
/users/{id}
/users/{id}/messages
```

may belong to one router.

FastAPI provides `APIRouter` for this purpose.

### Controllers / route handlers

Controllers receive requests and return responses.

A controller should coordinate a request, not contain every implementation detail.

Conceptually:

```text
HTTP request
    ↓
controller
    ↓
service
    ↓
repository/provider
    ↓
result
    ↓
controller
    ↓
HTTP response
```

A clean controller often receives dependencies rather than constructing them manually.

### Services

Services orchestrate internal operations to implement business logic.

For example, a payment workflow may need to:

1. fetch a user,
2. check an order,
3. call a payment provider,
4. record the result,
5. send confirmation.

The service coordinates those steps.

### Providers

Providers communicate with external systems.

Examples include clients for:

- email services,
- payment gateways,
- third-party APIs,
- other microservices,
- model APIs.

The distinction is useful:

```text
Service
→ implements application/business workflow

Provider
→ interfaces with an external system
```

### Repositories

Repositories encapsulate data-access and mutation logic.

They may use:

- an ORM,
- raw SQL,
- a memory store,
- another persistence mechanism.

Typical repository operations include CRUD:

- create,
- read,
- update,
- delete.

A repository lets higher layers ask for data without embedding database implementation details everywhere.

### Schemas / models

Schemas and models help enforce:

- data shape,
- type safety,
- validation rules.

They define the expected structure of information as it flows through the service.

### Cross-cutting components

Some components do not belong to only one layer.

#### Middleware

Runs around requests and responses.

#### Dependencies

Reusable injectable functions or resources.

#### Pipes

Transform data.

Examples:

- cleaners,
- parsers,
- aggregators,
- translators.

#### Mappers

Convert data from one schema or representation to another.

Example:

```text
UserRequest
    ↓ mapper
UserInDB
```

#### Exception filters

Handle errors consistently.

#### Guards

Protect routes or operations.

Authentication and authorization checks are common examples.

### Why this matters for GenAI

A GenAI backend can become difficult to maintain if one route contains everything:

```text
authenticate user
+ retrieve data
+ construct prompt
+ call model
+ call payment API
+ write database record
+ catch every error
+ format response
```

Layering helps separate those concerns.

A clearer design might be:

```text
Router
  ↓
Controller
  ↓
GenAI service
  ├── Retrieval repository
  ├── Model provider
  ├── External API provider
  └── Conversation repository
```

This is easier to test and reason about because each part has a narrower responsibility.

{{image:course-service-architecture}}

{{exercise:M01.L02.EX05}}

---

## 10. FastAPI compared with Django and Flask

The chapter frames framework choice partly around how **opinionated** a framework is.

### Opinionated frameworks

An opinionated framework gives you more built-in structure and conventions.

The chapter uses Django as the main Python example.

Advantages include:

- many integrated features,
- built-in architectural expectations,
- mature ecosystem,
- less need to choose every component yourself.

Trade-off:

- you accept more of the framework's structure.

### Nonopinionated frameworks

FastAPI and Flask give developers more architectural freedom.

Advantages:

- flexibility,
- leaner services,
- freedom to choose supporting components.

Trade-off:

- more decisions,
- more integration work,
- more responsibility for keeping the codebase organized.

### Django

The chapter highlights Django's strong integrated capabilities, including areas such as:

- ORM,
- migrations,
- administration,
- authentication,
- authorization,
- security features,
- mature ecosystem.

It is presented as a strong fit for larger monolithic web applications where the integrated stack is valuable.

### Flask

Flask is presented as very lightweight.

Its simplicity is useful for small services, but the chapter notes that features such as:

- built-in schema validation,
- automatic documentation,
- dependency injection

are not included in the same way as FastAPI and may require additional packages or design work.

### WSGI versus ASGI

The chapter contrasts Flask's traditional WSGI serving model with FastAPI's ASGI model.

A simplified mental model:

```text
WSGI
→ traditionally synchronous request handling

ASGI
→ designed for asynchronous/concurrent application patterns
```

ASGI is especially useful for workloads involving many I/O waits and long-lived connection patterns.

### Framework choice is contextual

The chapter's comparison can be summarized as:

| Need | Chapter's framing |
|---|---|
| Integrated monolithic web application | Django can be attractive |
| Very simple lightweight API | Flask can be attractive |
| Modern API with validation, docs, DI, async support, AI integrations | FastAPI is attractive |

The lesson is not "FastAPI is always better."

The lesson is:

> **Choose a framework whose defaults and trade-offs fit the system you are building.**

---

## 11. FastAPI limitations for AI workloads

FastAPI is an excellent API framework, but the chapter is careful not to present it as a complete model-serving solution for every workload.

This is one of the most important parts of the chapter.

### 11.1 Model memory management

Large models consume substantial memory.

When application workers scale across processes or containers, each worker may need its own model instance.

That can multiply memory use.

Conceptually:

```text
Worker 1 → model copy
Worker 2 → model copy
Worker 3 → model copy
Worker 4 → model copy
```

If one model is already large, this can become expensive.

### 11.2 Limited thread capacity

FastAPI can run synchronous work in a thread pool, but a thread pool is finite.

Heavy synchronous work can exhaust those workers and reduce throughput.

### 11.3 The Python GIL and compute-heavy workloads

The chapter discusses the **Global Interpreter Lock (GIL)** as a limitation for Python multithreading with CPU-heavy work.

A key distinction:

```text
I/O-heavy task
→ spends time waiting
→ concurrency can help greatly

CPU/GPU-heavy inference
→ spends time computing
→ can still block useful request processing
```

This is why simply adding `async` does not solve heavy inference.

### 11.4 Lack of efficient micro-batching

Deep-learning inference can often be more efficient when several inputs are processed as a batch.

A general-purpose FastAPI request model handles requests independently and does not automatically combine them into optimized inference batches.

That can waste accelerator capacity for heavy serving workloads.

### 11.5 CPU/GPU workload splitting

A specialized model-serving architecture can separate responsibilities:

```text
CPU:
- validation
- preprocessing
- request transformation
- post-processing

GPU:
- neural-network inference
```

The chapter notes that FastAPI itself is not designed to efficiently orchestrate every aspect of this split for demanding inference workloads.

### 11.6 Dependency conflicts

ML systems often depend on:

- hardware-specific libraries,
- CUDA versions,
- native packages,
- model runtimes,
- Python packages with strict version relationships.

Deployment can therefore be more difficult than deploying an ordinary web API.

### 11.7 Resource-intensive models

For large, expensive models, a general-purpose API framework may not be the ideal model server.

The chapter introduces **BentoML** as a specialized ML-serving framework that can handle concerns such as:

- model runners,
- dependency management,
- model versioning,
- deployment configuration,
- separating web request handling from model inference.

### A hybrid architecture

The chapter suggests an important production pattern:

```text
Client
  ↓
FastAPI
  ├── authentication
  ├── authorization
  ├── caching
  ├── business logic
  └── request/response handling
        ↓
Specialized model server
        ↓
Heavy AI inference
```

This preserves FastAPI where it is strong while delegating expensive model serving to infrastructure designed for that job.

### The central engineering lesson

Do not confuse:

> **a good API framework**

with:

> **a complete high-performance inference platform**

FastAPI can be an excellent control and application layer even when heavy models are served elsewhere.

{{exercise:M01.L02.EX06}}

---

## 12. Managed environments and professional Python tooling

As a project grows, code quality becomes a system feature.

The chapter recommends managing dependencies and adding tools that catch mistakes before production.

### Dependency-management choices

The source mentions:

- `requirements.txt` with `pip` for simpler projects,
- `uv` or Conda for pip-oriented workflows,
- Poetry for more complex projects.

The exact tool can vary.

The deeper requirement is reproducibility:

> Another developer or deployment environment should be able to recreate the dependencies your service expects.

### Linters

Linters analyze source code for problems.

The chapter lists examples such as:

- Autoflake,
- Flake8,
- Ruff.

They can identify issues including:

- unused imports,
- style problems,
- suspicious code,
- inconsistent patterns.

### Formatters

Formatters make code presentation consistent.

The chapter mentions:

- isort,
- Black,
- Ruff.

Consistent formatting reduces review noise and makes code easier to scan.

### Logging

The chapter mentions Loguru as an alternative logging tool.

Logging becomes important when a service has multiple interacting layers and external systems.

A useful log may answer:

```text
What request failed?
Which component failed?
What operation was being attempted?
What information can help reproduce the issue?
```

### Security scanners

The chapter names:

- Bandit,
- Safety.

These tools aim to catch categories of insecure code or vulnerable dependencies.

They do not replace secure architecture, but they can catch mistakes early.

### Type checkers

The chapter lists:

- Mypy,
- Pylance.

Type checking becomes especially valuable when schemas and function interfaces evolve.

For example, if a data model changes from:

```text
user_id: int
```

to:

```text
user_id: str
```

type-aware tooling may expose downstream assumptions that need updating.

### Git and `.gitignore`

Git provides version control.

A `.gitignore` file keeps selected files out of version tracking.

Typical reasons to exclude files include:

- local virtual environments,
- generated caches,
- machine-specific files,
- local secrets.

### IDE integration and automated checks

The chapter encourages configuring editors such as VS Code or PyCharm to run helpful tools during development.

It also recommends automated checks before committing or deploying.

A professional workflow may conceptually look like:

```text
Write code
   ↓
Format
   ↓
Lint
   ↓
Type-check
   ↓
Security scan
   ↓
Run tests
   ↓
Commit
```

The exact tools may change.

The engineering discipline remains useful.

---

## Important misconceptions

### Misconception 1

> `async def` automatically makes any FastAPI route scalable.

### Why this is wrong

Async helps most when code spends time waiting on asynchronous I/O. Heavy CPU/GPU computation can still block useful processing and may require processes or specialized model-serving infrastructure.

### Misconception 2

> Swagger UI means you no longer need tests.

### Why this is wrong

Swagger UI is excellent for interactive exploration and debugging, but automated tests are needed to systematically verify behavior as the code changes.

### Misconception 3

> A modular project structure is always the best place to start.

### Why this is wrong

The chapter recommends progressive reorganization. Small projects can begin flat, become nested as technical complexity grows, and become modular when domains and features justify the additional structure.

### Misconception 4

> Dependency injection is just a shortcut for fewer lines of code.

### Why this is wrong

It also reduces coupling, centralizes reusable behavior, manages resources, supports hierarchical dependencies, and helps separate concerns.

### Misconception 5

> FastAPI should directly serve every AI model.

### Why this is wrong

FastAPI is a general-purpose API framework. Heavy models may require specialized serving infrastructure for memory management, batching, compute isolation, and CPU/GPU coordination.

### Misconception 6

> Project structure and architecture are the same thing.

### Why this is wrong

Project structure determines how files and packages are organized. Architecture defines component responsibilities, boundaries, and dependencies. You can apply layered architecture inside different directory structures.

---

## Key terminology

| Term | Meaning |
|---|---|
| FastAPI | A Python framework for building APIs and backend services |
| ASGI | An asynchronous server interface standard used by modern Python web applications |
| Uvicorn | An ASGI server commonly used to run FastAPI applications |
| Route | A mapping between an HTTP path/method and application logic |
| Controller / route handler | A function that handles an incoming request and returns a response |
| Serialization | Converting application data into a transferable format such as JSON |
| Validation | Checking that incoming data satisfies required rules and structure |
| OpenAPI | A machine-readable specification describing an API |
| Swagger UI | Interactive documentation generated from an OpenAPI specification |
| Concurrency | Making progress on multiple tasks during overlapping periods |
| Background task | Work performed after a response can be returned to the client |
| Middleware | Logic that processes requests/responses around route handlers |
| CORS | Browser-oriented controls for cross-origin requests |
| Dependency injection | Supplying reusable functions/resources to components that declare them as dependencies |
| Lifespan event | Startup/shutdown logic used to initialize and clean up shared resources |
| REST | An API style commonly organized around resources and HTTP methods |
| WebSocket | Persistent bidirectional client-server communication |
| SSE | Server-to-client event streaming over an HTTP connection |
| Flat structure | Project organization with a small number of files near the root |
| Nested structure | Organization by technical categories such as routers, models, and services |
| Modular structure | Organization by domain or feature, keeping closely related code together |
| Onion/layered architecture | A design that separates responsibilities into layers with controlled dependency direction |
| Service | Component that orchestrates internal business operations |
| Provider | Component that communicates with external systems |
| Repository | Component responsible for data access and mutation |
| Pipe | Reusable data-transformation component |
| Mapper | Component that converts data from one schema/representation to another |
| Guard | Component that protects routes or operations, often through authentication or authorization |
| GIL | Python's Global Interpreter Lock, relevant to CPU-heavy multithreaded workloads |
| Micro-batching | Combining inference requests into batches for more efficient model execution |

---

## Self-check

Before continuing, make sure you can answer:

1. What roles do FastAPI, Starlette, Uvicorn, and Pydantic each play?
2. Why should a Python project use an isolated environment?
3. What does `@app.get("/path")` do?
4. Why must Python objects be serialized before traveling over HTTP?
5. What is the difference between runtime validation and static type checking?
6. When is asynchronous request handling most useful?
7. Why can CPU/GPU-heavy inference still cause problems inside an async route?
8. What kinds of tasks are suitable for background processing?
9. What is middleware?
10. What problem does dependency injection solve?
11. Why might a dependency use `yield` for a database session?
12. What is a hierarchical dependency graph?
13. When would a lifespan event be useful in a GenAI service?
14. What are the differences among flat, nested, and modular project structures?
15. What are shotgun updates?
16. What is the dependency inversion idea behind onion architecture?
17. What are the responsibilities of controllers, services, providers, and repositories?
18. How do Django, Flask, and FastAPI differ in the chapter's comparison?
19. Why is FastAPI not always sufficient as a heavy model-serving platform?
20. Why might FastAPI and a specialized model server be used together?
21. What development tools can help keep a Python backend maintainable?

---

## Retain this idea

**FastAPI is most valuable when you treat it as the application and API layer around your AI system: use it to validate requests, expose routes, manage dependencies, organize business logic, enforce security, connect external systems, and coordinate model access—while keeping project structure and model-serving infrastructure appropriate to the scale of the workload.**
""",

        "estimated_minutes": 150,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "fastapi-foundations",
                "title": "What FastAPI is",
                "order": 1,
            },
            {
                "id": "environment-setup",
                "title": "Set up the Python environment",
                "order": 2,
            },
            {
                "id": "first-fastapi-server",
                "title": "Build your first FastAPI server",
                "order": 3,
            },
            {
                "id": "docs-serialization-validation",
                "title": "Automatic docs, serialization, and validation",
                "order": 4,
            },
            {
                "id": "concurrency-background-middleware",
                "title": "Concurrency, background tasks, middleware, and CORS",
                "order": 5,
            },
            {
                "id": "dependency-injection",
                "title": "Dependency injection: reusable logic without duplication",
                "order": 6,
            },
            {
                "id": "lifespan-security-protocols",
                "title": "Lifespan events, security, and communication patterns",
                "order": 7,
            },
            {
                "id": "project-structures",
                "title": "Structuring a FastAPI project",
                "order": 8,
            },
            {
                "id": "layered-design",
                "title": "Onion/layered application design",
                "order": 9,
            },
            {
                "id": "framework-comparison",
                "title": "FastAPI compared with Django and Flask",
                "order": 10,
            },
            {
                "id": "fastapi-limitations",
                "title": "FastAPI limitations for AI workloads",
                "order": 11,
            },
            {
                "id": "tooling",
                "title": "Managed environments and professional Python tooling",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L02.EX01",

            "title": "Run and Explain a Minimal FastAPI Service",

            "lesson_code": "M01.L02",

            "section_id": "first-fastapi-server",

            "placement": "after_section",

            "description": (
                "Build the smallest useful FastAPI service and explain how an HTTP "
                "request reaches a Python route handler."
            ),

            "instructions": (
                "1. Create a FastAPI application with a GET `/` endpoint that returns "
                "`{\"status\": \"healthy\"}`.\n"
                "2. Add a GET `/hello` endpoint with a `name` query parameter.\n"
                "3. Return `{\"message\": \"Hello, <name>\"}` from the second route.\n"
                "4. Run the application in development mode.\n"
                "5. Test both routes from the browser or the generated docs page.\n"
                "6. In 4-6 sentences, explain the roles of the FastAPI app object, "
                "route decorator, route function, Uvicorn/server layer, and JSON response."
            ),

            "expected_output": (
                "A working two-route FastAPI application plus a short explanation of "
                "the request-to-response flow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "fastapi-routing",
                "api-basics",
                "http-request-flow",
            ],
        },

        {
            "id": "M01.L02.EX02",

            "title": "Classify Work as Async, Sync, or Background",

            "lesson_code": "M01.L02",

            "section_id": "concurrency-background-middleware",

            "placement": "after_section",

            "description": (
                "Practice distinguishing request work that benefits from async I/O, "
                "ordinary synchronous handling, or background execution."
            ),

            "instructions": (
                "For each task below, choose the most appropriate category from this "
                "lesson: `async I/O`, `ordinary synchronous work`, or `background task`.\n\n"
                "1. Waiting for a remote HTTP API.\n"
                "2. Sending a confirmation email after the response can be returned.\n"
                "3. Parsing a tiny in-memory dictionary.\n"
                "4. Indexing a large uploaded document after acknowledging the upload.\n"
                "5. Waiting for an async database query.\n\n"
                "For each choice, write one sentence explaining why."
            ),

            "expected_output": (
                "Five classifications with one-sentence explanations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "concurrency-reasoning",
                "background-processing",
            ],
        },

        {
            "id": "M01.L02.EX03",

            "title": "Build a Reusable FastAPI Dependency",

            "lesson_code": "M01.L02",

            "section_id": "dependency-injection",

            "placement": "after_section",

            "description": (
                "Use FastAPI dependency injection to remove duplicated query-parameter "
                "logic from multiple routes."
            ),

            "instructions": (
                "1. Create a `pagination` dependency that accepts `skip` and `limit`.\n"
                "2. Inject it into both `/messages` and `/conversations` routes.\n"
                "3. Return the resolved pagination values from each route.\n"
                "4. Explain what FastAPI is injecting into the route function.\n"
                "5. Describe one other concern—such as authentication or database "
                "access—that would benefit from the same pattern."
            ),

            "expected_output": (
                "A runnable dependency example used by two routes plus a short explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "dependency-injection",
                "dry-principle",
                "fastapi-depends",
            ],
        },

        {
            "id": "M01.L02.EX04",

            "title": "Choose a Project Structure",

            "lesson_code": "M01.L02",

            "section_id": "project-structures",

            "placement": "after_section",

            "description": (
                "Select a project structure based on the size and coupling of a backend."
            ),

            "instructions": (
                "Choose `flat`, `nested`, or `modular` for each scenario and justify "
                "your answer:\n\n"
                "1. A weekend prototype with four routes and one external API.\n"
                "2. A growing AI microservice with routers, schemas, models, and services.\n"
                "3. A production backend with authentication, billing, users, messaging, "
                "retrieval, model providers, and several external integrations.\n\n"
                "Then explain one signal that would tell you it is time to reorganize "
                "a project into a more structured form."
            ),

            "expected_output": (
                "Three structure choices with reasoning plus one reorganization signal."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "project-architecture",
                "maintainability-reasoning",
            ],
        },

        {
            "id": "M01.L02.EX05",

            "title": "Decompose a GenAI Endpoint into Layers",

            "lesson_code": "M01.L02",

            "section_id": "layered-design",

            "placement": "after_section",

            "description": (
                "Apply the onion/layered design pattern to a realistic GenAI request."
            ),

            "instructions": (
                ('1. A user sends a question about an uploaded document. The system must authenticate the user, retrieve relevant chunks from a vector store, call a language model, save the conversation, and return an answer.\n'
                 '2. Assign each responsibility to an appropriate component such as:\n'
                 '   - router,\n'
                 '   - controller,\n'
                 '   - service,\n'
                 '   - provider,\n'
                 '   - repository,\n'
                 '   - schema,\n'
                 '   - dependency/guard.\n'
                 '3. Then draw the request flow using arrows.')
            ),

            "expected_output": (
                "A responsibility table plus a layered request-flow diagram."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "layered-architecture",
                "separation-of-concerns",
                "genai-backend-design",
            ],
        },

        {
            "id": "M01.L02.EX06",

            "title": "Separate the API Layer from Heavy Inference",

            "lesson_code": "M01.L02",

            "section_id": "fastapi-limitations",

            "placement": "after_section",

            "description": (
                "Reason about when FastAPI should coordinate model access rather than "
                "perform heavy model inference directly."
            ),

            "instructions": (
                "Imagine a service must host a very large GPU model while also handling "
                "authentication, rate limits, conversation storage, and many concurrent "
                "clients.\n\n"
                "1. List at least three FastAPI limitations from this lesson that could "
                "matter for this workload.\n"
                "2. Sketch an architecture in which FastAPI remains the API/control "
                "layer and a specialized model server handles inference.\n"
                "3. Assign authentication, validation, model execution, and response "
                "formatting to the appropriate layer.\n"
                "4. Explain why adding `async` alone would not solve the heavy-inference problem."
            ),

            "expected_output": (
                "A short risk analysis and a two-layer FastAPI + model-server architecture."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "model-serving-architecture",
                "fastapi-limitations",
                "scalability-reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L02.QZ01",

        "title": "Getting Started with FastAPI — Knowledge Check",

        "lesson_code": "M01.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",

                "section_id": "fastapi-foundations",

                "question": "What is Uvicorn's primary role in the FastAPI stack?",

                "options": [
                    "It defines Pydantic validation schemas",
                    "It runs the FastAPI application as an ASGI web server",
                    "It replaces all route decorators",
                    "It acts as the database ORM",
                ],

                "correct": 1,

                "explanation": (
                    "FastAPI defines the application, while Uvicorn is the ASGI server "
                    "that runs it and handles network requests."
                ),
            },

            {
                "id": "M01.L02.Q02",

                "section_id": "first-fastapi-server",

                "question": "What does `@app.get('/chat')` primarily do?",

                "options": [
                    "Creates a Python virtual environment",
                    "Connects a GET request on `/chat` to the decorated function",
                    "Automatically trains a language model",
                    "Creates a database table named `chat`",
                ],

                "correct": 1,

                "explanation": (
                    "The decorator registers the function as the handler for GET "
                    "requests to that path."
                ),
            },

            {
                "id": "M01.L02.Q03",

                "section_id": "docs-serialization-validation",

                "question": "Why is serialization required in an HTTP API?",

                "options": [
                    "Because arbitrary live Python objects cannot be transmitted directly over HTTP",
                    "Because every endpoint must use a database",
                    "Because serialization makes all requests asynchronous",
                    "Because Uvicorn can only execute JSON files",
                ],

                "correct": 0,

                "explanation": (
                    "Application data must be represented in a transferable format such "
                    "as JSON or binary data before it can travel over HTTP."
                ),
            },

            {
                "id": "M01.L02.Q04",

                "section_id": "concurrency-background-middleware",

                "question": (
                    "Which task is the clearest candidate for background processing "
                    "according to the chapter?"
                ),

                "options": [
                    "Returning a tiny in-memory dictionary",
                    "Reading one already available query parameter",
                    "Processing a large uploaded document for later vector retrieval",
                    "Selecting the HTTP method for a route",
                ],

                "correct": 2,

                "explanation": (
                    "Large document processing can continue after the client receives "
                    "an acknowledgement, avoiding an unnecessarily long open request."
                ),
            },

            {
                "id": "M01.L02.Q05",

                "section_id": "dependency-injection",

                "question": "What is a major benefit of FastAPI dependency injection?",

                "options": [
                    "It eliminates the need for application architecture",
                    "It lets reusable logic and resources be declared and injected instead of duplicated",
                    "It forces every project to use the same database",
                    "It converts CPU-heavy inference into asynchronous I/O",
                ],

                "correct": 1,

                "explanation": (
                    "Dependencies let routes reuse common logic and resources such as "
                    "pagination, database sessions, authentication, and authorization."
                ),
            },

            {
                "id": "M01.L02.Q06",

                "section_id": "project-structures",

                "question": (
                    "Which structure groups code primarily by domain or feature rather "
                    "than only by technical category?"
                ),

                "options": [
                    "Flat structure",
                    "Modular structure",
                    "Single-file structure",
                    "WSGI structure",
                ],

                "correct": 1,

                "explanation": (
                    "A modular structure keeps related components for a feature or domain "
                    "together, such as routers, services, models, and guards for authentication."
                ),
            },

            {
                "id": "M01.L02.Q07",

                "section_id": "layered-design",

                "question": (
                    "Which component is primarily responsible for data-access and "
                    "mutation logic in the layered design described in the chapter?"
                ),

                "options": [
                    "Repository",
                    "Router",
                    "Middleware",
                    "Guard",
                ],

                "correct": 0,

                "explanation": (
                    "Repositories encapsulate operations against data sources using "
                    "mechanisms such as an ORM, SQL, or other storage adapters."
                ),
            },

            {
                "id": "M01.L02.Q08",

                "section_id": "layered-design",

                "question": "What is the main role of a provider?",

                "options": [
                    "To define all HTTP status codes",
                    "To communicate with an external system or service",
                    "To replace every repository",
                    "To format the entire codebase",
                ],

                "correct": 1,

                "explanation": (
                    "Providers specialize in external integrations such as payment "
                    "gateways, email services, APIs, or other microservices."
                ),
            },

            {
                "id": "M01.L02.Q09",

                "section_id": "framework-comparison",

                "question": (
                    "What trade-off does the chapter associate with nonopinionated "
                    "frameworks such as FastAPI?"
                ),

                "options": [
                    "They prohibit third-party integrations",
                    "They provide more freedom but require more architectural and package decisions",
                    "They cannot expose REST endpoints",
                    "They require a monolithic frontend",
                ],

                "correct": 1,

                "explanation": (
                    "More flexibility means developers must make more decisions about "
                    "structure, dependencies, integrations, and supporting libraries."
                ),
            },

            {
                "id": "M01.L02.Q10",

                "section_id": "fastapi-limitations",

                "question": (
                    "Why does declaring a heavy model-inference route as `async def` "
                    "not automatically remove the scalability problem?"
                ),

                "options": [
                    "Because async routes cannot return JSON",
                    "Because compute-intensive inference can still block useful processing rather than merely waiting on I/O",
                    "Because FastAPI disables GPUs for async routes",
                    "Because ASGI only supports synchronous Python",
                ],

                "correct": 1,

                "explanation": (
                    "Async is most effective for waiting on non-blocking I/O. Heavy "
                    "CPU/GPU inference is compute work and can still monopolize resources."
                ),
            },

            {
                "id": "M01.L02.Q11",

                "section_id": "fastapi-limitations",

                "question": (
                    "What architecture does the chapter suggest for resource-intensive "
                    "AI serving?"
                ),

                "options": [
                    "Remove the API layer and expose the GPU directly",
                    "Use FastAPI for application concerns and delegate heavy inference to a specialized model server",
                    "Run every model once for every route import",
                    "Use only synchronous endpoints and no worker processes",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter presents a separation where FastAPI manages concerns "
                    "such as security and business logic while a specialized ML-serving "
                    "system handles resource-intensive inference."
                ),
            },

            {
                "id": "M01.L02.Q12",

                "section_id": "tooling",

                "type": "open",

                "question": (
                    "You are starting a FastAPI GenAI backend expected to grow over the "
                    "next year. Propose a development workflow using at least four tooling "
                    "categories from this lesson, and explain what type of problem each "
                    "category helps catch or prevent."
                ),
            },
        ],

        "passing_score": 70,
    },
}
