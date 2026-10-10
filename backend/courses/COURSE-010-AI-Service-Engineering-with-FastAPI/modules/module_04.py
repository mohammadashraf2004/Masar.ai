"""M01.L04 — Implementing Type-Safe AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 4, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Make GenAI services safer to change by typing data flows, validating untrusted "
    "inputs and outputs with Pydantic, centralizing configuration with validated "
    "settings, and designing FastAPI request/response contracts that expose mistakes early."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Implementing Type-Safe AI Services",

    "slug": "generative-ai-services-m01-l04",

    "description": (
        "Learn why type safety matters in changing GenAI backends, how Python type "
        "annotations and dataclasses improve data flow, how Pydantic performs runtime "
        "validation and serialization, how to build custom validators and computed "
        "fields, and how to validate application settings and FastAPI schemas."
    ),

    "order": 4,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "python-typing",
        "type-safety",
        "mypy",
        "annotated",
        "dataclasses",
        "pydantic",
        "data-validation",
        "fastapi",
        "api-schemas",
        "environment-variables",
        "settings",
        "genai-services",
    ],

    "prerequisite_ids": [
        "M01.L03",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Implementing Type-Safe AI Services",

        "content": """
# Implementing Type-Safe AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L04  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 4 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why type safety becomes increasingly valuable as a GenAI service grows.
- Distinguish Python's dynamic runtime behavior from static type analysis.
- Add useful type annotations to variables, function parameters, and return values.
- Use unions, `Literal`, reusable aliases, and `Annotated` to make data contracts clearer.
- Explain what dataclasses solve and what they do not provide by themselves.
- Create Pydantic `BaseModel` schemas for GenAI request and response data.
- Use model inheritance to share common request/response fields.
- Add Pydantic field constraints and constrained data types.
- Distinguish field-level validation from validation involving multiple fields.
- Use computed fields for derived response values.
- Serialize Pydantic models to dictionaries and JSON while controlling which fields are emitted.
- Validate environment configuration with Pydantic Settings.
- Use typed request and response models in FastAPI endpoints.
- Explain how type safety reduces risk when databases, model providers, or API schemas change.
- Combine static analysis, runtime validation, testing, and deployment checks rather than treating any one of them as sufficient.

---

## 1. Why type safety matters in GenAI services

A backend service moves data through many components.

A GenAI service may receive data from:

- browser clients,
- mobile clients,
- model providers,
- databases,
- vector stores,
- environment variables,
- third-party APIs,
- internal microservices.

Each boundary introduces uncertainty.

Suppose one function expects a Unix timestamp:

```python
from datetime import datetime


def timestamp_to_isostring(date: int) -> str:
    return datetime.fromtimestamp(date).isoformat()
```

This call matches the declared contract:

```python
timestamp_to_isostring(1736680773)
```

But this one does not:

```python
timestamp_to_isostring("27 Jan 2025 14:48:00")
```

A static type checker can flag the second call before the program reaches production.

### What is type safety?

**Type safety** is the practice of ensuring that values are used in ways compatible with their expected types.

For example:

```text
function expects int
        ↓
caller passes int
        ↓
operation is compatible
```

versus:

```text
function expects int
        ↓
caller passes str
        ↓
potential bug
```

### Why this matters more as complexity grows

In a tiny script, you may remember every variable.

In a production service, you may have:

```text
route
  ↓
schema
  ↓
service
  ↓
provider
  ↓
database
  ↓
external API
```

A field may travel through many layers.

If a database column changes, an API changes its response shape, or another developer updates a model object, untyped code may fail much later in an unrelated component.

Type information gives tools a map of expected data flow.

### Type safety is early feedback

The source emphasizes a practical advantage:

> **Types can turn some production failures into development-time warnings.**

That can save debugging time because the problem is discovered closer to where the incompatible change was introduced.

[[IMAGE_NEEDED: Static type error in an IDE | A Python editor showing a function annotated to accept an integer timestamp and an incorrect call passing a string, with the type checker highlighting the argument mismatch | Learner should notice that the problem is surfaced before the code is run in production]]

---

## 2. Dynamic Python and static type analysis

Python is a **dynamically typed language**.

That means Python does not require you to declare every variable type before running the program.

For example:

```python
value = 10
value = "ten"
```

Python allows the variable name to refer to different types at runtime.

This flexibility helps developers prototype quickly.

But flexibility can become uncertainty as a system grows.

### Static languages versus Python's optional typing

The chapter contrasts two broad styles.

```text
Statically typed language
→ type rules are strongly enforced before execution

Python
→ runtime remains dynamic
→ optional type annotations can be analyzed by tools
```

Python type annotations do not transform Python into a fully statically typed runtime.

They create information that tools can analyze.

### Static type checkers

Tools mentioned in the source include:

- mypy,
- pyright,
- pyre.

They inspect code without needing every path to execute.

Example:

```python
def repeat(text: str, count: int) -> str:
    return text * count


repeat("AI", 3)       # compatible
repeat("AI", "three") # type checker can warn
```

### Type annotations do not replace tests

A type checker can tell you that a function receives an `int`.

It cannot prove that the integer has the correct business meaning.

For example:

```python
temperature: float
```

does not guarantee that:

```text
0.0 <= temperature <= 1.0
```

That requires validation logic.

### The protection layers

Use this mental model:

```text
Type annotations
→ describe expected kinds of values

Static type checker
→ checks code against those declarations

Runtime validation
→ checks actual incoming data

Tests
→ verify behavioral expectations
```

A robust service benefits from all four.

---

## 3. Type annotations for clearer data flow

Python type annotations can describe:

- variables,
- function parameters,
- return values,
- containers,
- limited sets of values,
- optional values.

### Function annotations

```python
def count_tokens(text: str | None) -> int:
    if text is None:
        return 0

    return len(text)
```

This contract says:

```text
input  → str or None
output → int
```

The `|` syntax represents a union of allowed types.

### Container types

```python
prices: dict[str, float] = {
    "model-a": 0.003,
    "model-b": 0.02,
}
```

This declares:

```text
dictionary keys   → str
dictionary values → float
```

### Tuples

A function can declare a tuple return value:

```python
def calculate_costs(...) -> tuple[float, float, float]:
    ...
```

The caller now knows to expect exactly three float values according to the type contract.

### `Literal`

Sometimes a string can technically contain anything, but your application only supports a few valid options.

```python
from typing import Literal

SupportedModel = Literal[
    "gpt-3.5",
    "gpt-4",
]
```

Now a type checker can distinguish:

```python
model = "gpt-4"
```

from an unsupported literal.

### Reusable aliases

The source uses reusable type aliases to avoid rewriting complicated declarations.

Conceptually:

```python
from typing import TypeAlias

PriceTable: TypeAlias = dict[SupportedModel, float]
```

This improves readability.

Instead of seeing:

```python
dict[Literal["..."], float]
```

everywhere, the code can use a meaningful domain name.

### Runtime checks still matter

The source explicitly keeps runtime checks even after adding static types.

That is important.

A caller can:

- ignore type-checker warnings,
- send invalid network input,
- call Python dynamically,
- bypass editor checks.

So critical logic should still reject unsupported values at runtime.

Example:

```python
if model not in prices:
    raise ValueError(
        f"Cost calculation is not supported for {model}"
    )
```

Static typing and runtime protection are complementary.

{{exercise:M01.L04.EX01}}

---

## 4. `Annotated`: type plus metadata

The chapter introduces `Annotated` as a way to attach metadata to a type.

```python
from typing import Annotated, Literal

SupportedModels = Annotated[
    Literal["gpt-3.5-turbo", "gpt-4o"],
    "Supported text models",
]
```

The first argument is the underlying type.

Additional arguments carry metadata.

Conceptually:

```text
Annotated[
    actual type,
    metadata,
    more metadata,
]
```

### Why metadata is useful

The metadata can support:

- documentation,
- runtime inspection,
- validation declarations,
- framework integration.

FastAPI and Pydantic can use annotations to express richer API requirements without separating the type from its constraints.

### Example

Later in the chapter, the pattern becomes:

```python
temperature: Annotated[
    float,
    Field(
        ge=0.0,
        le=1.0,
        default=0.0,
    ),
]
```

Read this as:

```text
temperature is a float
AND
it has validation metadata
```

This is a useful bridge between **type meaning** and **runtime data constraints**.

---

## 5. Dataclasses: organizing related typed data

Long function signatures can become hard to read.

Imagine a cost function like:

```python
def calculate_usage_costs(
    prompt,
    response,
    model,
    request_id,
    created_at,
    ...
):
    ...
```

If several values belong to one conceptual object, a dataclass can group them.

```python
from dataclasses import dataclass


@dataclass
class Message:
    prompt: str
    response: str | None
    model: str
```

Then:

```python
def calculate_usage_costs(
    message: Message,
):
    ...
```

### Why dataclasses help

The chapter uses dataclasses to improve:

- organization,
- readability,
- encapsulation,
- repeated data grouping,
- function signatures.

A dataclass can reduce a "data clump":

```text
prompt
response
model
```

into one meaningful object:

```text
Message
```

### Response dataclass

You can also return a structured object:

```python
@dataclass
class MessageCostReport:
    req_costs: float
    res_costs: float
    total_costs: float
```

Now the function contract is clearer:

```python
def calculate_usage_costs(
    message: Message,
) -> MessageCostReport:
    ...
```

### What vanilla dataclasses do not automatically provide

The chapter later draws an important boundary.

Standard dataclasses do not natively give you all the API-focused functionality provided by Pydantic, including advanced:

- automatic parsing,
- runtime field validation,
- rich serialization/deserialization,
- field filtering.

A dataclass is therefore excellent for **typed data organization**, but it is not automatically a complete input-validation system.

### Dataclass versus dictionary

Compare:

```python
message = {
    "prompt": "...",
    "response": None,
    "model": "gpt-4",
}
```

with:

```python
message = Message(
    prompt="...",
    response=None,
    model="gpt-4",
)
```

The dataclass gives the object an explicit schema that IDEs and static type tools can understand more easily.

[[IMAGE_NEEDED: Dictionary to dataclass refactor | Side-by-side illustration showing several loose function parameters or dictionary fields being grouped into a typed `Message` dataclass passed as one object | Learner should notice that related values become one explicit data contract]]

{{exercise:M01.L04.EX02}}

---

## 6. Pydantic models: typed data plus runtime validation

Pydantic builds on Python type annotations to provide runtime data processing.

The core abstraction is `BaseModel`.

```python
from pydantic import BaseModel


class TextModelRequest(BaseModel):
    prompt: str
    temperature: float = 0.0
```

This class does more than group fields.

Pydantic can use it for:

- parsing,
- validation,
- serialization,
- JSON schema generation.

These features are especially useful at API boundaries.

### Why API boundaries need validation

Your own Python code may be typed.

But an HTTP client can still send:

```json
{
  "prompt": 123,
  "temperature": "very hot"
}
```

Network data is untrusted until validated.

A Pydantic model becomes a boundary contract.

```text
untrusted external data
        ↓
Pydantic schema
        ↓
validated application data
```

### FastAPI integration

FastAPI uses Pydantic models to understand:

- request bodies,
- response structures,
- validation requirements,
- OpenAPI schemas.

This is why typed schema design improves both runtime safety and generated API documentation.

### Pydantic and dataclasses

The source presents an important distinction:

```text
dataclass
→ typed data organization

Pydantic BaseModel
→ typed organization + parsing + validation + serialization + schema generation
```

This does not mean dataclasses are useless.

It means Pydantic is often more convenient when data crosses an API boundary.

---

## 7. Reuse schemas with model inheritance

GenAI endpoints often share fields.

For example, every model request may contain a prompt.

```python
from pydantic import BaseModel


class ModelRequest(BaseModel):
    prompt: str
```

Then specific request schemas can inherit that field:

```python
class TextModelRequest(ModelRequest):
    model: str
    temperature: float = 0.0


class ImageModelRequest(ModelRequest):
    model: str
    output_size: tuple[int, int]
    num_inference_steps: int = 200
```

This avoids duplicating the common `prompt` field.

### Shared response fields

The same idea applies to responses.

```python
from datetime import datetime


class ModelResponse(BaseModel):
    request_id: str
    ip: str | None
    content: str | None
    created_at: datetime
```

Specialized response models can extend it:

```python
class TextModelResponse(ModelResponse):
    tokens: int
```

or:

```python
class ImageModelResponse(ModelResponse):
    size: tuple[int, int]
    url: str | None
```

### Why this matters

Inheritance can encode the relationship:

```text
All text requests are model requests
All image requests are model requests
```

and:

```text
All specialized responses share common response metadata
```

This can make API schemas more consistent as the number of endpoints grows.

---

## 8. Field constraints: reject bad values early

A normal type can be too broad.

For example:

```python
temperature: float
```

accepts values such as:

```text
-500.0
1000000.0
```

even if your application only wants a small range.

Pydantic's `Field` metadata allows you to add constraints.

### Prompt length

```python
from typing import Annotated
from pydantic import Field


Prompt = Annotated[
    str,
    Field(
        min_length=1,
        max_length=10000,
    ),
]
```

Now an empty prompt or excessively large prompt can be rejected at validation time.

### Numeric ranges

```python
Temperature = Annotated[
    float,
    Field(
        ge=0.0,
        le=1.0,
    ),
]
```

Here:

```text
ge → greater than or equal
le → less than or equal
```

### Positive integers

For dimensions such as image width and height:

```python
from pydantic import PositiveInt

ImageSize = tuple[
    PositiveInt,
    PositiveInt,
]
```

Now negative dimensions are not accepted.

### Specialized validated types

The source mentions types for common formats such as:

- IP addresses,
- URLs,
- positive integers,
- email-style values,
- UUIDs.

The important pattern is:

> If a common data format already has a validation type, use that instead of repeatedly writing manual string checks.

### Default factories

Some values should be created for each model instance.

For a request ID, the chapter uses the idea of a default factory.

```python
from uuid import uuid4

request_id: str = Field(
    default_factory=lambda: uuid4().hex
)
```

A factory is important because it produces a **new value for each instance**.

### FastAPI validation failures

When a request violates the schema, FastAPI can return structured validation details.

[[IMAGE_NEEDED: FastAPI request validation boundary | A client sending a request body through a Pydantic request model; valid input continues to the route while invalid input branches to a structured validation error response | Learner should notice that malformed data is rejected before normal business/model logic runs]]

{{exercise:M01.L04.EX03}}

---

## 9. Custom validators for domain rules

Built-in constraints handle many cases.

But application rules can be more specific.

Imagine an image endpoint with this requirement:

```text
only square output
AND
allowed dimensions are 512×512 or 1024×1024
```

A normal `tuple[int, int]` type cannot express that whole rule.

### Field-level validation

A field validator can inspect one value.

Conceptually:

```python
def is_square_image(
    value: tuple[int, int],
) -> tuple[int, int]:
    width, height = value

    if width != height:
        raise ValueError(
            "Only square images are supported"
        )

    if width not in (512, 1024):
        raise ValueError(
            "Expected 512 or 1024"
        )

    return value
```

The key behavior is:

```text
valid value
→ return it

invalid value
→ raise validation error
```

### Multi-field validation

Some rules depend on more than one field.

Example:

```text
If model == "tinysd",
then num_inference_steps must stay under a model-specific limit.
```

This is not just a property of `num_inference_steps`.

It depends on:

```text
model
+
num_inference_steps
```

The source distinguishes validation that targets one field from validation that checks relationships across model fields.

### Why this matters for GenAI

Model APIs often have conditional configuration rules.

Examples:

```text
supported image size depends on model
supported generation option depends on model
parameter range depends on backend
```

Encoding these rules in schemas prevents invalid configurations from reaching expensive inference code.

### Validation before expensive work

A powerful production principle is:

```text
cheap validation
      ↓
expensive model inference
```

not:

```text
expensive model setup/inference
      ↓
discover request was invalid
```

The earlier you reject impossible requests, the fewer resources you waste.

{{exercise:M01.L04.EX04}}

---

## 10. Computed fields: derive response values from validated data

Some response fields are not directly provided by the caller.

They are derived.

For example:

- token count,
- request cost.

The source uses computed fields to keep this calculation close to the response model.

Conceptually:

```python
class TextModelResponse(ModelResponse):
    content: str | None
    price: float

    @property
    @computed_field
    def tokens(self) -> int:
        return count_tokens(self.content)

    @property
    @computed_field
    def cost(self) -> float:
        return self.price * self.tokens
```

### Why encapsulate derived values?

Without this pattern, many controllers might repeat:

```python
tokens = count_tokens(output)
cost = price * tokens
```

Putting the derivation on the model can make the data contract self-contained.

### Source of truth

A useful mental model is:

```text
stored fields
   ↓
computed property
   ↓
derived response field
```

If the content changes, the token/cost computation follows from the response object's current values.

---

## 11. Export and serialize Pydantic models

Pydantic models are useful internally, but APIs ultimately need transferable data.

Pydantic can export models to:

- Python dictionaries,
- JSON strings.

### Dictionary export

Conceptually:

```python
response.model_dump()
```

returns structured Python data.

### JSON export

Conceptually:

```python
response.model_dump_json()
```

returns a JSON representation.

### Excluding fields

The chapter highlights useful filtering options.

#### Exclude `None`

Useful when optional fields should disappear instead of being returned as `null`.

#### Exclude unset values

Useful when a model has many optional filter fields and the client only supplied a few.

#### Exclude defaults

Useful when default-valued fields do not need to be emitted.

### Filtering example

Imagine:

```python
class SearchFilters(BaseModel):
    category: str | None = None
    min_price: float | None = None
    max_price: float | None = None
```

A user only specifies:

```text
min_price
```

Exporting only explicitly set fields can produce:

```python
{
    "min_price": 100.0
}
```

instead of carrying unused filters through the application.

### Serialization is part of the contract

Pydantic is therefore useful in two directions:

```text
incoming
external data
   ↓
parse + validate
   ↓
Python model
```

and:

```text
Python model
   ↓
serialize
   ↓
API response / JSON
```

---

## 12. Validate environment variables with Pydantic Settings

Application configuration is another untrusted boundary.

A deployment environment may provide:

- application secrets,
- database URLs,
- CORS origins,
- ports,
- API keys.

If configuration is malformed, the application should ideally fail early.

The source uses the `pydantic-settings` package and `BaseSettings`.

### Why environment variables?

Secrets should not be hard-coded into normal source files.

For example, avoid:

```python
APP_SECRET = "real-production-secret"
```

in committed application code.

Instead:

```text
environment / secret source
        ↓
settings model
        ↓
validated application configuration
```

### Settings schema

A teaching example:

```python
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    port: int = 8000
    app_secret: str
```

The schema can become much richer.

The source validates configuration such as:

- secret length,
- PostgreSQL connection strings,
- URL lists.

### Environment aliases

A Python field name can map to an environment variable name.

For example:

```text
Python field:
pg_dsn

Environment variable:
DATABASE_URL
```

This lets the code use readable domain names while respecting deployment naming conventions.

### `.env` files

For local development, a `.env` file can hold key/value pairs.

Example:

```text
APP_SECRET=...
DATABASE_URL=...
CORS_WHITELIST=...
```

The settings object can load and validate those values.

[[IMAGE_NEEDED: Pydantic Settings configuration flow | Diagram showing `.env` / deployment environment variables flowing into an `AppSettings` model, where URL/secret/type validation occurs, then validated settings being supplied to the FastAPI application | Learner should notice that configuration is validated at startup rather than read as arbitrary strings everywhere]]

### Different environment files

The source also shows that tests can load a separate environment file.

That helps isolate:

```text
development configuration
testing configuration
production configuration
```

while keeping one typed settings contract.

{{exercise:M01.L04.EX05}}

---

## 13. Dataclasses or Pydantic models in FastAPI?

FastAPI can work with both.

### Vanilla dataclass

```python
from dataclasses import dataclass


@dataclass
class TextModelRequest:
    model: str
    prompt: str
    temperature: float
```

The chapter explains that FastAPI can adapt dataclasses through its Pydantic integration for request/response processing.

This is useful if you already have an existing codebase full of dataclasses.

### Pydantic model

```python
from pydantic import BaseModel


class TextModelRequest(BaseModel):
    model: str
    prompt: str
    temperature: float
```

For a new API project, the source favors direct Pydantic usage because it exposes richer features naturally.

### Comparison

| Capability | Vanilla dataclass | Pydantic model |
|---|---|---|
| Typed fields | Yes | Yes |
| Compact data-centric class | Yes | Yes |
| Runtime parsing | Limited without extra logic | Built in |
| Rich field constraints | Not native in the same way | Built in |
| Custom validation | Requires manual logic | Built in |
| Serialization controls | More manual | Built in |
| JSON schema generation | Not a native dataclass feature | Built in |
| FastAPI integration | Supported | Native/tightly integrated |

The decision is therefore not:

```text
dataclass bad
Pydantic good
```

It is:

```text
use the tool whose features fit the boundary
```

For internal structured data, a dataclass may be enough.

For API contracts with untrusted input, Pydantic is often more convenient.

---

## 14. Build a type-safe FastAPI model endpoint

Now we combine the chapter's ideas.

A route that used loose query parameters can be refactored into a typed POST endpoint.

### Request schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class TextModelRequest(BaseModel):
    model: Literal[
        "tinyllama",
        "gemma2b",
    ]

    prompt: str = Field(
        min_length=1,
        max_length=4000,
    )

    temperature: float = Field(
        ge=0.0,
        le=1.0,
        default=0.0,
    )
```

### Response schema

```python
class TextModelResponse(BaseModel):
    request_id: str
    ip: str | None
    content: str | None
```

The source extends the response further with metadata and computed values.

### Route

Conceptually:

```python
from fastapi import Body, FastAPI, Request

app = FastAPI()


@app.post("/generate/text")
def generate_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
) -> TextModelResponse:
    output = generate_text(
        body.prompt,
        body.temperature,
    )

    return TextModelResponse(
        request_id="...",
        ip=request.client.host,
        content=output,
    )
```

### What happens before the model call?

The request flows through several checks:

```text
HTTP body
   ↓
JSON parsing
   ↓
Pydantic request schema
   ↓
type checks / constraints
   ↓
route receives validated object
   ↓
model generation
```

This is much safer than allowing arbitrary dictionaries to move directly into the inference layer.

### What happens on the way out?

```text
model output
   ↓
response object
   ↓
Pydantic response schema
   ↓
computed fields / serialization
   ↓
JSON
   ↓
client
```

That means request **and** response contracts are explicit.

### OpenAPI gets richer

FastAPI can use these schemas to generate documentation that shows:

- allowed fields,
- field types,
- defaults,
- constraints,
- response structure.

[[IMAGE_NEEDED: Typed FastAPI Swagger schema | A FastAPI Swagger/OpenAPI page showing a POST `/generate/text` request schema with model, prompt, and temperature fields plus a structured response model | Learner should notice that the typed Pydantic contract becomes visible to API consumers automatically]]

{{exercise:M01.L04.EX06}}

---

## 15. Reduce uncertainty when schemas change

The chapter's deeper goal is not merely "learn Pydantic syntax."

It is to make changing systems safer.

### External API change

Suppose your application expects:

```python
class ProviderResponse(BaseModel):
    content: str
```

Then a provider changes its SDK or schema.

With typed clients and models, affected usage can become visible through:

- type-checker errors,
- validation failures,
- test failures.

Without explicit contracts, the change may travel farther before failing.

### Database schema change

Imagine a field changes from:

```text
user_id: int
```

to:

```text
user_id: str
```

If services and repositories are typed, static analysis can expose locations that still assume an integer.

### Model response uncertainty

GenAI systems add another unstable boundary.

A model can produce probabilistic output.

If your application expects structured information, the chapter's Pydantic approach gives you a way to validate that the result matches your required schema before downstream code trusts it.

### Types make refactoring visible

Think of a typed codebase as a network of contracts.

```text
Schema A
   ↓
Function B
   ↓
Service C
   ↓
Provider D
```

If a contract changes, tools can show which connected parts no longer match.

That is especially valuable in codebases with:

- several contributors,
- many external systems,
- changing prompts,
- changing providers,
- changing database schemas.

### Add checks to the delivery pipeline

The chapter recommends taking static checks beyond the editor.

A development pipeline can include:

```text
write change
   ↓
format/lint
   ↓
static type check
   ↓
tests
   ↓
build/deploy checks
   ↓
production
```

If the type check fails, the change can be stopped before deployment.

### The complete protection model

A mature GenAI backend should combine:

```text
Type annotations
    ↓
Static analysis
    ↓
Pydantic runtime validation
    ↓
Explicit error handling
    ↓
Automated tests
    ↓
Deployment checks
```

Each layer catches a different class of problem.

{{exercise:M01.L04.EX07}}

---

## Important misconceptions

### Misconception 1

> Python type annotations enforce types automatically at runtime.

### Why this is wrong

Python remains dynamically typed. Type annotations primarily describe expectations that static analysis tools, editors, FastAPI, and supporting libraries can use.

### Misconception 2

> If mypy passes, all incoming API data is valid.

### Why this is wrong

Static type checking analyzes your code. External HTTP data arrives at runtime and still needs validation.

### Misconception 3

> A dataclass automatically gives the same runtime validation features as a Pydantic model.

### Why this is wrong

Standard dataclasses are excellent for typed data organization but do not natively provide the full parsing, validation, filtering, and serialization toolset described for Pydantic.

### Misconception 4

> `float` is enough to represent a valid model temperature.

### Why this is wrong

The type says what kind of value it is. A field constraint expresses which numeric range your application accepts.

### Misconception 5

> Validation should happen after model inference.

### Why this is wrong

Invalid requests should be rejected before expensive model work whenever possible.

### Misconception 6

> One-field validation can express every business rule.

### Why this is wrong

Some requirements depend on combinations of fields, such as one model supporting a different inference-step range than another.

### Misconception 7

> Environment variables are safe just because they are outside the source code.

### Why this is wrong

They can still be missing or malformed. Pydantic Settings provides a typed validation boundary for configuration.

### Misconception 8

> Response schemas only help documentation.

### Why this is wrong

They also make return contracts explicit, support serialization, and can expose unexpected response-shape changes.

### Misconception 9

> Type safety eliminates the need for tests.

### Why this is wrong

Types catch compatibility problems; tests verify actual behavior and business rules. They solve overlapping but different problems.

---

## Key terminology

| Term | Meaning |
|---|---|
| Type | Category describing what kind of value a variable or field represents |
| Type safety | Practice of keeping values compatible with declared expectations |
| Dynamic typing | Runtime typing model where variables are not required to have fixed declared types |
| Static type analysis | Checking declared type compatibility without executing every code path |
| Type annotation | Python syntax that declares an expected type |
| Union | Type allowing more than one alternative, such as `str | None` |
| Literal | Type restricted to a predefined set of literal values |
| Type alias | Reusable name for another type expression |
| Annotated | Type wrapper that attaches metadata to a type |
| Dataclass | Python data-centric class with generated boilerplate for structured fields |
| Pydantic | Python data validation and serialization library driven by type annotations |
| BaseModel | Pydantic base class used to define validated data models |
| Schema | Formal structure defining expected data fields and types |
| Field constraint | Rule such as minimum length or allowed numeric range |
| Validator | Function or model logic that checks data beyond basic type compatibility |
| Field validator | Validation focused on one field |
| Model validator | Validation that can reason about multiple fields together |
| Computed field | Output field derived from other model values |
| Serialization | Converting model data into transferable structures such as dictionaries or JSON |
| Deserialization/parsing | Converting external representation into application data structures |
| `model_dump()` | Pydantic-style export to Python data |
| `model_dump_json()` | Pydantic-style export to JSON |
| BaseSettings | Pydantic Settings base class used to parse application configuration |
| Environment variable | External key/value configuration supplied to a running application |
| OpenAPI | Machine-readable API description FastAPI can derive from typed schemas |
| Runtime validation | Checking actual values while the application is running |
| Data contract | Explicit agreement about the shape, type, and constraints of exchanged data |

---

## Self-check

Before continuing, make sure you can answer:

1. What problem is type safety trying to reduce?
2. Why can a dynamically typed Python program still benefit from static type analysis?
3. What is the difference between a type annotation and runtime validation?
4. What does `str | None` mean?
5. When is `Literal` useful?
6. Why create reusable type aliases?
7. What does `Annotated` add to an ordinary type?
8. What problem can a dataclass solve in a long function signature?
9. Which API-focused capabilities do vanilla dataclasses lack compared with the Pydantic features described in this chapter?
10. What does inheriting from `BaseModel` provide?
11. Why use base request/response models and inherit specialized schemas?
12. Why is `temperature: float` weaker than a constrained temperature field?
13. Why use a `default_factory` for request IDs?
14. What is the difference between field validation and multi-field/model validation?
15. Why should invalid image dimensions be rejected before inference?
16. What is a computed field?
17. When is excluding unset fields useful?
18. What is the purpose of `BaseSettings`?
19. Why should secrets usually not be hard-coded into source files?
20. What advantage does validating a database URL at application startup provide?
21. Why can FastAPI work with both dataclasses and Pydantic models?
22. Why does the source recommend Pydantic directly for a new API project?
23. How can a typed request model improve `/generate/text`?
24. How can a typed response model improve reliability?
25. What happens when an external provider changes a schema?
26. Why can static checking in CI/CD reduce deployment risk?
27. Why do you still need tests in a fully typed codebase?
28. How do typing, validation, and testing complement each other?

---

## Retain this idea

**Treat every boundary in a GenAI service as a data contract: use Python types to make expectations visible before runtime, Pydantic to validate the real data crossing API and configuration boundaries, and automated checks to expose incompatible changes before they become expensive production failures.**
""",

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-type-safety",
                "title": "Why type safety matters in GenAI services",
                "order": 1,
            },
            {
                "id": "dynamic-vs-static",
                "title": "Dynamic Python and static type analysis",
                "order": 2,
            },
            {
                "id": "type-annotations",
                "title": "Type annotations for clearer data flow",
                "order": 3,
            },
            {
                "id": "annotated",
                "title": "Annotated: type plus metadata",
                "order": 4,
            },
            {
                "id": "dataclasses",
                "title": "Dataclasses: organizing related typed data",
                "order": 5,
            },
            {
                "id": "pydantic-models",
                "title": "Pydantic models: typed data plus runtime validation",
                "order": 6,
            },
            {
                "id": "compound-models",
                "title": "Reuse schemas with model inheritance",
                "order": 7,
            },
            {
                "id": "field-constraints",
                "title": "Field constraints: reject bad values early",
                "order": 8,
            },
            {
                "id": "custom-validators",
                "title": "Custom validators for domain rules",
                "order": 9,
            },
            {
                "id": "computed-fields",
                "title": "Computed fields: derive response values from validated data",
                "order": 10,
            },
            {
                "id": "serialization",
                "title": "Export and serialize Pydantic models",
                "order": 11,
            },
            {
                "id": "settings",
                "title": "Validate environment variables with Pydantic Settings",
                "order": 12,
            },
            {
                "id": "dataclass-vs-pydantic",
                "title": "Dataclasses or Pydantic models in FastAPI?",
                "order": 13,
            },
            {
                "id": "typed-fastapi-endpoint",
                "title": "Build a type-safe FastAPI model endpoint",
                "order": 14,
            },
            {
                "id": "schema-change-resilience",
                "title": "Reduce uncertainty when schemas change",
                "order": 15,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",

            "title": "Type a GenAI Cost Function",

            "lesson_code": "M01.L04",

            "section_id": "type-annotations",

            "placement": "after_section",

            "description": (
                "Practice describing a small GenAI utility with explicit Python type contracts."
            ),

            "instructions": (
                "Create type annotations for a function that calculates request and "
                "response cost.\n\n"
                "Requirements:\n"
                "1. `prompt` must be `str`.\n"
                "2. `response` may be `str` or `None`.\n"
                "3. `model` must be restricted with `Literal` to two model names.\n"
                "4. The function returns three floats: request cost, response cost, total cost.\n"
                "5. Create a reusable type alias for the pricing dictionary.\n"
                "6. Add a runtime error if an unsupported model somehow reaches the function.\n\n"
                "Explain why the runtime check is still useful even after adding `Literal`."
            ),

            "expected_output": (
                "A typed Python function signature, a model/pricing type declaration, "
                "and a short explanation of static versus runtime protection."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "python-type-annotations",
                "literal-types",
                "runtime-guards",
            ],
        },

        {
            "id": "M01.L04.EX02",

            "title": "Refactor a Data Clump into Dataclasses",

            "lesson_code": "M01.L04",

            "section_id": "dataclasses",

            "placement": "after_section",

            "description": (
                "Use dataclasses to make a data-heavy function easier to read."
            ),

            "instructions": (
                "Start with a hypothetical function receiving these parameters:\n"
                "`prompt`, `response`, `model`, `request_cost`, `response_cost`, "
                "`total_cost`.\n\n"
                "1. Create a `Message` dataclass for prompt/response/model.\n"
                "2. Create a `MessageCostReport` dataclass for the three costs.\n"
                "3. Rewrite the function signature to accept a `Message` and return "
                "a `MessageCostReport`.\n"
                "4. Explain which problem this refactor solves.\n"
                "5. State one validation feature you would still need Pydantic or "
                "manual logic to provide."
            ),

            "expected_output": (
                "Two dataclass definitions, a refactored function signature, and a "
                "short design explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "dataclasses",
                "data-organization",
                "refactoring",
            ],
        },

        {
            "id": "M01.L04.EX03",

            "title": "Constrain a Model Request Schema",

            "lesson_code": "M01.L04",

            "section_id": "field-constraints",

            "placement": "after_section",

            "description": (
                "Turn broad Python types into a stricter API contract."
            ),

            "instructions": (
                "Design an `ImageModelRequest` Pydantic model with:\n"
                "1. `prompt`: 1 to 4000 characters.\n"
                "2. `model`: restricted to two supported literals.\n"
                "3. `output_size`: two positive integers.\n"
                "4. `num_inference_steps`: integer in a bounded range with a default.\n"
                "5. Add one additional sensible constraint of your own using only "
                "the concepts from this chapter.\n\n"
                "Then give two example request bodies: one valid and one that should "
                "fail validation."
            ),

            "expected_output": (
                "A constrained Pydantic request schema plus one valid and one invalid example."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "pydantic-field-constraints",
                "request-validation",
                "api-schema-design",
            ],
        },

        {
            "id": "M01.L04.EX04",

            "title": "Write Domain Validation Rules",

            "lesson_code": "M01.L04",

            "section_id": "custom-validators",

            "placement": "after_section",

            "description": (
                "Separate single-field validation from rules that depend on multiple fields."
            ),

            "instructions": (
                "Implement or pseudocode these two rules:\n\n"
                "Rule A: `output_size` must be square and its width must be either "
                "512 or 1024.\n\n"
                "Rule B: if `model == \"tinysd\"`, `num_inference_steps` must not exceed "
                "a model-specific upper limit.\n\n"
                "For each rule:\n"
                "1. Identify whether it can be validated using one field alone or "
                "requires access to multiple model fields.\n"
                "2. Raise a clear error for invalid data.\n"
                "3. Explain why this validation belongs before image inference."
            ),

            "expected_output": (
                "Two validation implementations or pseudocode blocks with classification "
                "and reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "custom-validation",
                "field-validator",
                "model-validator",
            ],
        },

        {
            "id": "M01.L04.EX05",

            "title": "Create Validated Application Settings",

            "lesson_code": "M01.L04",

            "section_id": "settings",

            "placement": "after_section",

            "description": (
                "Model deployment configuration as typed, validated application data."
            ),

            "instructions": (
                "Create an `AppSettings` model using the chapter's Pydantic Settings ideas.\n\n"
                "Include:\n"
                "1. application port with a default,\n"
                "2. application secret with a minimum length,\n"
                "3. PostgreSQL DSN loaded from `DATABASE_URL`,\n"
                "4. CORS whitelist containing validated URLs,\n"
                "5. `.env` loading for local development.\n\n"
                "Then explain what should happen if the database URL is malformed at startup."
            ),

            "expected_output": (
                "A typed settings model and a short explanation of fail-fast configuration validation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "pydantic-settings",
                "environment-configuration",
                "configuration-validation",
            ],
        },

        {
            "id": "M01.L04.EX06",

            "title": "Refactor a Loose Endpoint into a Typed Endpoint",

            "lesson_code": "M01.L04",

            "section_id": "typed-fastapi-endpoint",

            "placement": "after_section",

            "description": (
                "Apply request and response models to a GenAI FastAPI route."
            ),

            "instructions": (
                "Refactor a text generation endpoint so that:\n"
                "1. It accepts a POST body through `TextModelRequest`.\n"
                "2. The schema validates model name, prompt length, and temperature.\n"
                "3. The controller returns `TextModelResponse`.\n"
                "4. The response includes request metadata plus generated content.\n"
                "5. Token count or cost is represented as a computed response field.\n"
                "6. Explain what invalid data is rejected before the model is called."
            ),

            "expected_output": (
                "A typed FastAPI route with request/response models plus an explanation "
                "of the validation boundary."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "fastapi-pydantic",
                "typed-api-contracts",
                "response-modeling",
            ],
        },

        {
            "id": "M01.L04.EX07",

            "title": "Trace a Breaking Schema Change",

            "lesson_code": "M01.L04",

            "section_id": "schema-change-resilience",

            "placement": "after_section",

            "description": (
                "Understand how explicit contracts help expose integration changes early."
            ),

            "instructions": (
                "Assume an external provider changes its response from:\n"
                "`{\"content\": \"...\"}`\n"
                "to:\n"
                "`{\"message\": \"...\"}`.\n\n"
                "1. Identify where a typed provider response schema would fail.\n"
                "2. Identify what a static type checker could catch after you update "
                "the internal field from `content` to `message`.\n"
                "3. State what automated test you would add or update.\n"
                "4. Explain how CI type checking can prevent an incomplete migration "
                "from reaching production."
            ),

            "expected_output": (
                "A short change-impact analysis covering validation, static checking, tests, and CI."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "schema-evolution",
                "integration-safety",
                "ci-type-checking",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Implementing Type-Safe AI Services — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",

                "section_id": "why-type-safety",

                "question": (
                    "What is a primary benefit of type safety in a growing backend service?"
                ),

                "options": [
                    "It makes every model response factually correct",
                    "It helps expose incompatible data usage earlier as code changes",
                    "It eliminates the need for API schemas",
                    "It automatically encrypts database fields",
                ],

                "correct": 1,

                "explanation": (
                    "Type contracts allow static tools and editors to identify many "
                    "incompatible changes closer to development time."
                ),
            },

            {
                "id": "M01.L04.Q02",

                "section_id": "dynamic-vs-static",

                "question": (
                    "Which statement best describes Python type annotations?"
                ),

                "options": [
                    "They make Python stop being dynamically typed at runtime",
                    "They describe expected types that tools and frameworks can use",
                    "They automatically test all business logic",
                    "They force every variable to remain immutable",
                ],

                "correct": 1,

                "explanation": (
                    "Python remains dynamically typed. Annotations provide type "
                    "information for static analysis, IDEs, and frameworks/libraries."
                ),
            },

            {
                "id": "M01.L04.Q03",

                "section_id": "type-annotations",

                "question": "What does `str | None` mean?",

                "options": [
                    "The value must contain both a string and an integer",
                    "The value may be a string or `None`",
                    "The string is automatically validated as a URL",
                    "The value is always converted to a string",
                ],

                "correct": 1,

                "explanation": (
                    "The union syntax allows either of the listed alternatives."
                ),
            },

            {
                "id": "M01.L04.Q04",

                "section_id": "annotated",

                "question": "What is the purpose of `Annotated` in this chapter?",

                "options": [
                    "To attach metadata such as validation information to a type",
                    "To execute GPU inference",
                    "To replace every Pydantic model with a dictionary",
                    "To disable static type checking",
                ],

                "correct": 0,

                "explanation": (
                    "`Annotated` preserves an underlying type while attaching additional "
                    "metadata that frameworks and validation tools can use."
                ),
            },

            {
                "id": "M01.L04.Q05",

                "section_id": "dataclasses",

                "question": (
                    "What is one strong use case for a dataclass in the lesson?"
                ),

                "options": [
                    "Grouping related typed values into a clearer data object",
                    "Automatically validating every possible external API format",
                    "Replacing the FastAPI server",
                    "Running model inference on a GPU",
                ],

                "correct": 0,

                "explanation": (
                    "Dataclasses are useful for organizing related data and simplifying "
                    "function signatures."
                ),
            },

            {
                "id": "M01.L04.Q06",

                "section_id": "pydantic-models",

                "question": (
                    "What major capability does a Pydantic `BaseModel` add at an API boundary?"
                ),

                "options": [
                    "Runtime parsing and validation of data against a declared schema",
                    "Guaranteed correctness of LLM output",
                    "Automatic GPU batching",
                    "Database replication",
                ],

                "correct": 0,

                "explanation": (
                    "Pydantic models use declared fields and types to parse and validate "
                    "actual runtime data."
                ),
            },

            {
                "id": "M01.L04.Q07",

                "section_id": "field-constraints",

                "question": (
                    "Why is `temperature: float` weaker than a constrained temperature field?"
                ),

                "options": [
                    "A float type says nothing about the allowed application-specific numeric range",
                    "Python cannot store floating-point values",
                    "Pydantic only accepts integers",
                    "FastAPI ignores float annotations",
                ],

                "correct": 0,

                "explanation": (
                    "The base type describes the kind of value, while a constraint "
                    "expresses allowed boundaries such as 0.0 to 1.0."
                ),
            },

            {
                "id": "M01.L04.Q08",

                "section_id": "custom-validators",

                "question": (
                    "Which rule clearly requires reasoning about more than one field?"
                ),

                "options": [
                    "Prompt must have at least one character",
                    "Width must be a positive integer",
                    "Maximum inference steps depend on which model was selected",
                    "Request ID must be a string",
                ],

                "correct": 2,

                "explanation": (
                    "That rule depends on the relationship between the selected model "
                    "and the inference-step value."
                ),
            },

            {
                "id": "M01.L04.Q09",

                "section_id": "computed-fields",

                "question": "What is a computed field?",

                "options": [
                    "A field derived from other values on the model",
                    "An environment variable stored only on disk",
                    "A field that cannot be serialized",
                    "A field that disables validation",
                ],

                "correct": 0,

                "explanation": (
                    "Computed fields represent values such as token count or cost that "
                    "are derived from other model data."
                ),
            },

            {
                "id": "M01.L04.Q10",

                "section_id": "serialization",

                "question": (
                    "Why might `exclude_unset` be useful when exporting a filter model?"
                ),

                "options": [
                    "It can emit only fields the caller actually supplied",
                    "It forces every optional field to become required",
                    "It encrypts the exported JSON",
                    "It makes the model immutable",
                ],

                "correct": 0,

                "explanation": (
                    "When many filter fields are optional, exporting only explicitly "
                    "set values avoids carrying unused fields forward."
                ),
            },

            {
                "id": "M01.L04.Q11",

                "section_id": "settings",

                "question": (
                    "What is the main reason to use a Pydantic Settings model?"
                ),

                "options": [
                    "To type and validate application configuration from environment sources",
                    "To train the language model",
                    "To replace the operating system environment",
                    "To store all prompts permanently",
                ],

                "correct": 0,

                "explanation": (
                    "A settings model gives application configuration an explicit, "
                    "validated schema."
                ),
            },

            {
                "id": "M01.L04.Q12",

                "section_id": "dataclass-vs-pydantic",

                "question": (
                    "According to the lesson, which choice is generally more convenient "
                    "for a new API schema requiring rich validation?"
                ),

                "options": [
                    "A plain untyped dictionary",
                    "A Pydantic model",
                    "A global tuple with no annotations",
                    "A text file",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter favors Pydantic directly for new API projects when "
                    "runtime validation, serialization, and constraints are needed."
                ),
            },

            {
                "id": "M01.L04.Q13",

                "section_id": "typed-fastapi-endpoint",

                "question": (
                    "What should happen to an invalid request body before expensive "
                    "model inference begins?"
                ),

                "options": [
                    "It should pass unchanged into the model",
                    "It should be rejected by the request validation boundary",
                    "It should be written directly into the database",
                    "It should disable OpenAPI",
                ],

                "correct": 1,

                "explanation": (
                    "Validating early prevents malformed or unsupported requests from "
                    "reaching expensive downstream inference."
                ),
            },

            {
                "id": "M01.L04.Q14",

                "section_id": "schema-change-resilience",

                "type": "open",

                "question": (
                    "A third-party AI provider changes one response field and your "
                    "database team changes one column type in the same release. Explain "
                    "how type annotations, Pydantic validation, tests, and CI checks can "
                    "work together to expose incomplete updates before production."
                ),
            },
        ],

        "passing_score": 70,
    },
}
