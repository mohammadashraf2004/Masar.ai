"""M01.L11 — Testing AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 11, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L11"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Build confidence in GenAI services through planned testing boundaries, static "
    "checks, unit and integration tests, pytest fixtures and parameterization, async "
    "test isolation, test doubles, RAG retrieval metrics, behavioral evaluation, "
    "auto-evaluation, and focused end-to-end workflows."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Testing AI Services",

    "slug": "generative-ai-services-m01-l11",

    "description": (
        "Learn how to plan and implement tests for deterministic application code and "
        "probabilistic GenAI behavior. Cover testing boundaries, V&V, pytest, fixtures, "
        "parameterization, setup/teardown, async isolation, mocks and other test doubles, "
        "integration testing, RAG precision/recall, behavioral tests, auto-evaluation, "
        "and vertical/horizontal end-to-end testing."
    ),

    "order": 11,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.0,

    "skill_tags": [
        "software-testing",
        "pytest",
        "unit-testing",
        "integration-testing",
        "e2e-testing",
        "behavioral-testing",
        "fixtures",
        "parameterization",
        "async-testing",
        "mocking",
        "test-doubles",
        "dependency-injection",
        "rag-evaluation",
        "precision-recall",
        "auto-evaluation",
        "regression-testing",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L10",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Testing AI Services",

        "content": """
# Testing AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L11  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 11 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why testing becomes increasingly important as an AI service approaches production.
- Distinguish unit, integration, end-to-end, behavioral, and static testing.
- Define testing boundaries without over-testing implementation details.
- Explain verification versus validation.
- Explain why 100% code coverage does not prove that the application solves the right problem.
- Apply shift-left testing and the test-driven-development loop conceptually.
- Plan test scope, coverage, and comprehensiveness.
- Design valid, invalid, boundary, and huge-data test cases.
- Structure tests using Given–When–Then or Arrange–Act–Assert–Cleanup.
- Compare testing pyramid, trophy, honeycomb, and common testing anti-patterns.
- Explain why probabilistic GenAI output makes deterministic equality tests insufficient.
- Recognize model/output variability, performance cost, regression, drift, bias, adversarial risk, and effectively unbounded input space as GenAI testing challenges.
- Organize pytest test files and write focused assertions.
- Create reusable pytest fixtures with appropriate scope.
- Use parameterization to test multiple inputs without duplicating test functions.
- Use `conftest.py` for shared test configuration and fixtures.
- Implement setup and teardown with yield fixtures.
- Explain why isolation and idempotency reduce flaky tests.
- Test asynchronous code while managing event-loop and I/O-related flakiness.
- Distinguish fake, dummy, stub, spy, and mock test doubles.
- Explain when mocking helps and when over-mocking hides integration problems.
- Test interactions with real dependencies in integration tests.
- Calculate and interpret retrieval precision and recall for RAG.
- Test structured LLM decisions over representative input distributions.
- Use behavioral black-box tests for variable natural-language outputs.
- Distinguish minimum functionality, invariance, and directional expectation tests.
- Explain auto-evaluation with an evaluator/discriminator model.
- Design vertical and horizontal E2E tests around real user workflows.
- Build a balanced GenAI test strategy rather than maximizing one test type.

---

## 1. Why testing matters

Testing trades engineering effort for confidence.

Without tests, teams often discover failures only after:

- users report them,
- payments fail,
- data becomes inconsistent,
- external integrations change,
- several components interact in unexpected ways.

The source describes a complex payment/webhook system that became so difficult and flaky that it had to be rewritten.

The broader lesson is:

> **Testing becomes more valuable as the cost of failure increases.**

A quick prototype may tolerate little formal testing.

A system handling:

- customer payments,
- authentication,
- sensitive information,
- multiple contributors,
- many external dependencies

needs a deliberate testing plan.

### Signals that testing should increase

The chapter highlights situations such as:

- several contributors changing the code,
- dependencies changing,
- more interacting components,
- increasing bug frequency,
- high consequences if something fails.

### Testing is proactive debugging

Without tests:

```text
failure happens
    ↓
user notices
    ↓
team investigates
    ↓
fix is written
```

With good tests:

```text
change is made
    ↓
test catches regression
    ↓
fix happens before release
```

Testing does not prove that software is perfect.

It gives evidence that defined expectations still hold.

---

## 2. Unit, integration, and end-to-end tests

The chapter introduces three common runtime test types.

### Unit test

Tests one small component in isolation.

Example:

```text
chunk(tokens, chunk_size)
```

The unit-test boundary ends around that function.

External systems should usually not participate.

### Integration test

Tests the interface between components.

Example:

```text
retrieval service
    ↔
vector database
```

The goal is to verify that the two pieces communicate correctly.

### End-to-end test

Tests a larger user-facing workflow across many components.

Example:

```text
login
→ upload document
→ index document
→ ask question
→ retrieve context
→ generate answer
→ persist result
```

### Trade-off

As scope grows:

```text
confidence ↑
cost ↑
execution time ↑
maintenance ↑
flakiness risk ↑
```

{{image:test-boundaries}}

### Static checks come even earlier

Before runtime tests, tools such as static type checkers can catch:

- type problems,
- some code misuse,
- dead/unused code,
- style or data-flow issues.

In Python, static type checks add value when code uses type hints.

Runtime validation tools such as Pydantic catch malformed data while the application executes.

{{exercise:M01.L11.EX01}}

---

## 3. Test behavior, not implementation details

One of the hardest decisions is:

> **What exactly should the test assert?**

Suppose:

```python
def count_tokens(text):
    ...
```

If a test asserts the exact internal string-processing steps, a harmless refactor may break the test.

But if the requirement is:

```text
given this text
→ return this token count
```

the test should usually focus on input/output behavior.

### Black-box thinking

Treat the component as:

```text
input
→ system under test
→ output
```

Do not depend on internal implementation unless that internal behavior is itself a requirement.

### Two warning signs

Tests may be too coupled to implementation details when:

1. refactoring without behavior change breaks many tests;
2. a real behavioral bug can be introduced while tests still pass.

### Define a testing boundary

A boundary answers:

```text
What is inside this test?
What is outside this test?
```

Example unit boundary:

```text
inside:
chunking logic

outside:
filesystem
vector DB
LLM API
```

Clear boundaries make failures easier to diagnose.

---

## 4. Verification versus validation

The chapter uses the verification and validation model.

### Validation

Ask:

> **Are we building the right system?**

This is about requirements and business needs.

### Verification

Ask:

> **Did we build the system according to those requirements?**

Tests verify implementation against defined expectations.

### Why code coverage is insufficient

You can achieve:

```text
100% code coverage
+
all tests pass
```

and still have the wrong product behavior.

Example:

```text
Every line of a payment function is tested,
but the workflow does not match how payment events actually arrive.
```

That is a validation failure.

### V-model intuition

The source presents a V-shaped flow.

On the left:

```text
business requirements
→ system design
→ implementation
```

On the right:

```text
unit tests
→ integration tests
→ E2E/acceptance confidence
```

[[IMAGE_NEEDED: Verification and validation V-model | V-shaped diagram with requirements and design descending toward implementation on the left, then unit/integration/E2E verification ascending on the right | Learner should notice that tests verify implementation while validation begins from having the correct requirements]]

---

## 5. Shift testing left and use TDD when useful

A reactive process is:

```text
build system
→ bugs appear late
→ create tests after failure
```

Shift-left testing moves testing earlier.

```text
requirements
→ design
→ tests
→ implementation
```

### Test-driven development

The source presents TDD as an iterative loop.

```text
write failing test
    ↓
write minimum code
    ↓
test passes
    ↓
refactor
    ↓
keep tests passing
```

### GenAI application: prompt engineering

The chapter highlights prompt engineering as a useful TDD-like case.

You can:

1. define representative expected behaviors,
2. write evaluation tests,
3. iterate on prompt/model settings,
4. rerun the same test set,
5. check regressions when changing models.

This turns prompt design into a measurable iteration process instead of purely subjective trial and error.

---

## 6. Scope, coverage, and comprehensiveness

The chapter separates three dimensions.

### Scope

What systems and scenarios are inside the plan?

Example:

```text
RAG retrieval only
```

versus:

```text
complete chatbot product
```

### Coverage

How much of the defined system is touched by tests?

Often discussed as:

- code coverage,
- feature coverage,
- interface coverage.

### Comprehensiveness

How deeply do you test within the scope?

Questions include:

- success paths?
- failure paths?
- edge cases?
- misuse?
- performance extremes?

### Helpful geometry analogy

The source describes them roughly as:

```text
scope
→ volume / boundaries

coverage
→ surface area

comprehensiveness
→ depth
```

A test plan can have broad scope but shallow depth, or narrow scope with extremely detailed edge-case testing.

---

## 7. Design test data intentionally

The source defines four useful categories.

### Valid data

Normal expected inputs.

Example:

```text
chunk_size = 100
```

### Invalid data

Inputs outside accepted rules.

Example:

```text
chunk_size = -1
```

### Boundary data

Inputs near minimum/maximum accepted limits.

Example:

```text
max_upload_size
max_context_length
```

### Huge data

Large workloads used to explore performance/resource limits.

Example:

```text
100,000 chunks
very large file
large batch
```

### Why all four matter

Testing only the happy path creates false confidence.

A robust component should also behave predictably when:

- inputs are empty,
- values are invalid,
- boundaries are reached,
- workload size becomes extreme.

{{exercise:M01.L11.EX02}}

---

## 8. Structure tests with Given–When–Then

The chapter describes the Given–When–Then model.

### Given

Prepare the initial state.

```text
tokens = [1, 2, 3, 4, 5]
chunk_size = 2
```

### When

Call the system under test.

```text
result = chunk(tokens, 2)
```

### Then

Assert expected behavior.

```text
result == [[1, 2], [3, 4], [5]]
```

### Cleanup

Remove resources or reset state if needed.

Pytest commonly uses a similar framing:

```text
Arrange
Act
Assert
Cleanup
```

### Why phases help

Clear phases make failures easier to read.

A test should communicate:

```text
what state existed
what action occurred
what outcome was expected
```

---

## 9. Test across static, build, and runtime environments

Testing is not limited to runtime endpoint calls.

### Static checks

Python can use tools such as type checkers before execution.

These can identify certain classes of issues early.

### Build-time checks

A GenAI application may need setup such as:

- dependency installation,
- model downloads,
- model preloading,
- generated assets.

These build steps can also fail.

### Runtime tests

Unit, integration, and E2E tests execute application behavior.

Pydantic may validate runtime data.

### Layered verification

A useful progression is:

```text
static checks
→ build checks
→ unit tests
→ integration tests
→ E2E tests
→ behavioral/model evaluation
```

Each layer catches different classes of defects.

---

## 10. Testing pyramid, trophy, and honeycomb

Test suites need a balanced distribution.

### Testing pyramid

Many unit tests.

Fewer integration tests.

Even fewer E2E tests.

Why?

```text
unit tests
→ fast and cheap

E2E
→ slow and expensive
```

### Testing trophy

The source highlights this strategy for GenAI services.

It uses:

- strong static checks,
- unit tests,
- a large emphasis on integration tests,
- fewer E2E tests.

Why integration tests?

GenAI applications commonly depend on:

- databases,
- model providers,
- vector stores,
- filesystems,
- APIs.

Many important failures happen at interfaces.

### Testing honeycomb

Gives more balanced attention to multiple test categories, potentially including:

- performance,
- security,
- exploratory testing.

This may suit systems requiring comprehensive multi-dimensional testing.

### No universal distribution

The test strategy should reflect:

- system risk,
- architecture,
- dependencies,
- CI budget,
- performance needs.

[[IMAGE_NEEDED: Testing strategies comparison | Three simplified diagrams comparing testing pyramid, trophy, and honeycomb distributions across static/unit/integration/E2E and other testing types | Learner should notice that the chapter favors strong integration coverage for dependency-heavy GenAI services]]

---

## 11. Testing anti-patterns

The chapter warns against several distributions.

### Ice-cream cone

Too many:

- integration,
- E2E,
- manual tests.

Too few unit tests.

Result:

- slow suite,
- expensive maintenance,
- brittle tests.

### Cupcake

Similar imbalance with substantial manual/GUI testing and organizational separation among test types.

Potential problems:

- communication overhead,
- slow feedback,
- brittle workflows.

### Hourglass

Many unit tests.

Many E2E tests.

Too few integration tests.

This can create a gap where component interfaces are not tested efficiently.

### General lesson

Do not maximize test size.

Use the smallest test that provides the confidence needed for the behavior you are checking.

---

## 12. Why GenAI testing is different

Traditional deterministic code often supports assertions like:

```text
input X
→ exactly output Y
```

GenAI models may instead produce:

```text
input X
→ output A

same input X
→ output B

same input X
→ output C
```

All three may be acceptable.

This changes test design.

The chapter identifies several challenge categories:

- variable/flaky outputs,
- high test cost and latency,
- regression/model drift,
- bias,
- adversarial behavior,
- effectively unbounded input/output space.

The key change is:

> **GenAI model testing often asks whether behavior falls inside an acceptable region rather than whether output equals one exact string.**

---

## 13. Probabilistic output and statistical confidence

Language models sample from probability distributions.

Output variability can be affected by settings such as temperature.

This makes exact equality tests unreliable for open-ended generation.

### Wrong test

```python
assert response == (
    "The exact sentence I received yesterday."
)
```

A good answer with different wording would fail.

### Better mindset

Test properties across representative samples.

Possible properties:

- relevant to input,
- valid format,
- low toxicity,
- grounded in context,
- appropriate length,
- acceptable readability.

### Representative distribution

The source recommends test inputs that reflect actual intended usage.

Do not sample arbitrary prompts unrelated to the product and assume the resulting score represents production behavior.

### Statistical confidence

You cannot enumerate the complete model input space.

Instead:

```text
representative sample
+
behavior metrics
+
thresholds
→ evidence/confidence
```

not absolute proof.

---

## 14. Cost, latency, and regression challenges

### GenAI tests can be expensive

If every test calls a paid model:

```text
test count ↑
→ API calls ↑
→ token cost ↑
→ suite time ↑
```

Multi-model evaluator tests multiply the problem.

The source recommends controlling testing scope and using techniques such as:

- mocks,
- patching,
- dependency injection,
- less frequent expensive tests,
- statistical approaches.

### Regression

Even if application code does not change, model behavior can change.

Potential causes discussed include:

- provider model updates,
- retraining/fine-tuning changes,
- changing user patterns,
- environmental changes.

### Model drift

Performance changes over time.

### Concept drift

The relationship between target concepts and real-world behavior changes.

Example:

```text
language, events, norms, knowledge
→ change over time
```

### Data drift

Input distributions change.

Possible causes include:

- population changes,
- sampling changes,
- seasonality,
- source changes,
- processing-quality changes.

### Testing implication

Maintain regression datasets and rerun them when:

- provider models change,
- prompts change,
- retrieval changes,
- user traffic changes.

---

## 15. Bias and adversarial testing

### Bias

Foundation models can encode or produce unwanted bias.

The source gives examples involving demographic representation.

Bias testing may require separate metrics and test sets for dimensions such as:

- gender,
- race,
- age,
- other relevant groups.

The important point is:

> **You cannot claim to have tested a bias dimension if you have not defined how it will be measured.**

### Adversarial tests

Public-facing GenAI services should also test defensive layers against threats such as:

- prompt injection,
- jailbreak attempts,
- sensitive-information leakage,
- denial of service,
- unsafe tool agency,
- data poisoning or insecure data paths.

These tests should also verify:

- authentication guards,
- authorization guards,
- moderation/safeguards.

### Security testing cost

Safeguard models and classifiers can be expensive and still imperfect.

Testing them should include both:

- effectiveness,
- performance impact.

---

## 16. You cannot fully cover a generative model

A GenAI model can respond to effectively unlimited input variations.

Therefore:

```text
100% model-behavior coverage
```

is not realistically achievable through enumerated examples.

The chapter proposes behavioral testing.

Instead of asking:

```text
Did the output equal exactly this sentence?
```

ask:

```text
Was it coherent?
Was it relevant?
Was it grounded?
Was it non-toxic?
Did it respect the required behavior?
```

This is especially important in:

- RAG systems,
- agentic workflows,
- multi-model pipelines,
- external-tool integrations.

A human review layer can also help catch unexpected failures that automated tests miss.

---

## 17. Testing project: a RAG system

The chapter applies testing ideas to a RAG pipeline involving:

- filesystem operations,
- text transformation,
- vector retrieval,
- an LLM,
- asynchronous interfaces.

Potential boundaries include:

```text
loader
→ unit test

transform/chunk
→ unit test

retrieval service ↔ vector DB
→ integration test

generator ↔ LLM
→ integration/behavioral test

upload → index → retrieve → answer
→ E2E test
```

{{image:e2e-boundaries}}

---

## 18. Organize and run pytest tests

Pytest discovers test files and functions using naming conventions.

A typical project:

```text
project/
├── main.py
└── tests/
    ├── test_rag_loader.py
    ├── test_rag_transform.py
    └── test_rag_retrieval.py
```

### Simple test

```python
def test_chunking():
    tokens = [1, 2, 3, 4, 5]

    result = chunk(
        tokens,
        chunk_size=2,
    )

    assert result == [
        [1, 2],
        [3, 4],
        [5],
    ]
```

### Run suite

```bash
pytest tests
```

Pytest reports:

- collected tests,
- passes,
- failures,
- assertion details.

### Keep tests small

The source warns against large unit tests.

One focused test should make it easy to understand:

```text
what failed
and why
```

{{exercise:M01.L11.EX03}}

---

## 19. Pytest fixtures and fixture scope

A fixture is test setup data or a reusable dependency.

### Fresh fixture

Defined within one test.

Example:

```python
tokens = [1, 2, 3, 4, 5]
```

It is naturally isolated.

### Shared fixture

Reusable across tests.

The source warns about shared mutable global data because one test can modify it and affect another.

### Pytest fixture function

```python
@pytest.fixture(scope="module")
def tokens():
    return [1, 2, 3, 4, 5]
```

A test requests the fixture by parameter name:

```python
def test_chunking(tokens):
    ...
```

### Fixture scopes

Pytest can create/destroy a fixture at different lifetimes such as:

- function,
- class,
- module,
- package,
- session.

### Choose the narrowest useful scope

A short-lived fixture improves isolation.

A broader scope can reduce expensive repeated setup.

Example from the chapter:

```text
external API fixture
→ maybe reuse at wider scope to avoid repeated calls
```

But broader mutable state increases coupling risk.

---

## 20. Parameterize test cases

Without parameterization, you may write:

```text
test_chunk_size_1
test_chunk_size_2
test_chunk_size_3
test_invalid_chunk_size
...
```

Pytest can run one test function against many cases.

```python
@pytest.mark.parametrize(
    "tokens, chunk_size, expected",
    [
        ([1, 2, 3], 1, [[1], [2], [3]]),
        ([1, 2, 3], 5, [[1, 2, 3]]),
        ([], 3, []),
    ],
)
def test_chunk(
    tokens,
    chunk_size,
    expected,
):
    assert chunk(
        tokens,
        chunk_size,
    ) == expected
```

### Include different data classes

A useful parameterized set includes:

- valid,
- empty,
- invalid,
- boundary,
- huge cases.

### Expected exceptions

Use:

```python
with pytest.raises(ValueError):
    ...
```

when invalid input should fail.

### External test data

The source also shows loading cases from a JSON file.

That can make large evaluation datasets easier to maintain separately from test code.

{{exercise:M01.L11.EX04}}

---

## 21. Share fixtures with `conftest.py`

Pytest automatically discovers fixtures in `conftest.py`.

Example:

```text
tests/
├── conftest.py
├── test_rag_transform.py
└── test_rag_retrieval.py
```

`conftest.py` can hold shared:

- fixtures,
- setup helpers,
- test configuration.

Example:

```python
@pytest.fixture
def tokens():
    return [1, 2, 3, 4, 5]
```

Both test modules can request `tokens`.

### Avoid a giant test utility module

Shared configuration is useful, but maintain clear ownership.

A fixture should have one understandable purpose.

---

## 22. Setup and teardown with yield fixtures

Some tests need resources that must be cleaned up.

Examples:

- database clients,
- temporary files,
- API clients,
- test collections.

Pytest yield fixtures support this lifecycle.

```python
@pytest.fixture
def db_client():
    client = create_test_client()

    client.create_collection(
        "test"
    )

    yield client

    client.close()
```

Everything before `yield` is setup.

Everything after `yield` is teardown.

### Lifecycle

```text
create resource
    ↓
prepare test data
    ↓
yield resource
    ↓
run test
    ↓
cleanup
```

[[IMAGE_NEEDED: Pytest yield fixture lifecycle | Timeline showing setup → yield fixture into test → assertions → teardown, with a database client created and later closed | Learner should notice that cleanup is part of fixture ownership rather than being scattered across tests]]

### Why cleanup matters

Unclosed resources can cause:

- connection leaks,
- leftover data,
- port conflicts,
- later test failures.

These are common sources of nondeterminism.

---

## 23. Test asynchronous code carefully

The chapter uses `pytest-asyncio` to run async tests.

Example:

```python
@pytest.mark.asyncio
async def test_search(
    async_db_client,
):
    result = await async_db_client.search(
        ...
    )

    assert result is not None
```

### Why async tests can become flaky

Async code introduces variability in:

- task scheduling,
- completion order,
- I/O timing,
- event-loop state.

External dependencies add more uncertainty.

### Test isolation

The source emphasizes:

```text
one test should not change assumptions of another
```

A test suite should be idempotent:

```text
same code
same configuration
same test inputs
→ same test outcomes
```

Repeated execution should not depend on:

- previous test order,
- leftover database state,
- lingering tasks,
- shared mutated fixtures.

### Async mitigation techniques from the chapter

- await asynchronous I/O,
- avoid blocking sync I/O inside async tests,
- use correct timeouts,
- control ordering where necessary,
- isolate event-loop and fixture state.

### Unit-test alternative

If an async unit depends mostly on external I/O, the source suggests that mocking the external dependency can make unit tests:

- faster,
- synchronous,
- more predictable.

Use real async dependencies where their interaction is actually what you intend to test.

{{exercise:M01.L11.EX05}}

---

## 24. Test doubles: fake, dummy, stub, spy, mock

A test double replaces a real dependency during testing.

Think of a stunt double:

```text
looks sufficiently like dependency
for the test scenario
```

The source introduces five types.

### Fake

A simplified but functional implementation.

Example:

```text
in-memory database
instead of production DB
```

or a local fake LLM service.

### Dummy

A placeholder passed only because an interface requires it.

Example:

```text
fake_token
```

when the tested path never uses authentication.

### Stub

Returns predefined values.

```python
class StubLLM:
    def invoke(self, query):
        return "known response"
```

### Spy

Records interactions.

Example:

```text
how many times was invoke called?
with which arguments?
```

### Mock

Encodes expected interactions and can fail if the component uses the dependency incorrectly.

{{image:test-doubles}}

### Do not replace the behavior you want to test

If you are testing a content-filtering function that calls an LLM:

```text
replace:
LLM dependency

keep real:
content-filtering logic
```

Otherwise you are only testing the test double.

{{exercise:M01.L11.EX06}}

---

## 25. Mocking and patching with pytest

The chapter demonstrates `pytest-mock`.

A mock can return a canned value:

```python
llm_client = mocker.Mock()

llm_client.invoke.return_value = (
    "mock response"
)
```

It can also verify interactions:

```python
assert (
    llm_client.invoke.call_count
    == 2
)
```

and:

```python
llm_client.invoke.assert_any_call(
    "some query"
)
```

### Why mocks help

They let unit tests avoid:

- paid API calls,
- slow network calls,
- unreliable remote services,
- heavy model inference.

### Why mocks can hurt

Over-mocking can create false confidence.

If every dependency is mocked:

```text
all unit tests pass
```

while:

```text
real database/API contract is broken
```

The test suite missed the actual integration failure.

### Best balance from the chapter

Use simple mocks where needed for isolated unit tests.

Then complement them with integration tests against real dependencies.

---

## 26. Prefer dependency injection when it reduces brittle patching

The chapter notes that patching runtime code can make tests brittle.

Dependency injection offers another pattern.

Production:

```python
service = RAGService(
    llm_client=RealLLMClient(),
)
```

Test:

```python
service = RAGService(
    llm_client=StubLLMClient(),
)
```

No runtime monkey-patching is required.

### Why this improves testability

The component explicitly declares:

```text
I depend on an LLM client interface.
```

The test can provide a controlled implementation.

This keeps the unit boundary clear.

The source uses the same dependency-injection idea through pytest fixtures:

```text
test asks for fixture/dependency
→ pytest injects it
```

---

## 27. Integration tests verify interfaces

An integration test intentionally crosses a component boundary.

The source suggests focusing on two, or at most a few, interacting components.

Example:

```text
retrieval logic
    ↔
real Qdrant/vector database
```

Questions include:

- Was the query sent correctly?
- Does the real dependency accept it?
- Are results returned in the expected format?
- Does ranking/retrieval behavior meet the requirement?

### Integration boundary

```text
inside:
retrieval service
vector database

outside:
full UI
unrelated business workflows
```

This is larger than a unit test but smaller than an E2E user journey.

### Why this layer is valuable for GenAI

Many real failures come from interfaces:

- SDK changes,
- schema mismatch,
- database assumptions,
- async behavior,
- model-provider response shapes.

Integration tests exercise those real contracts.

---

## 28. Measure RAG retrieval with precision and recall

The chapter uses context precision and recall to test retrieval quality.

Assume:

```text
expected relevant document IDs
=
[1, 2, 3, 4, 5]

retrieved IDs
=
[2, 3, 6, 7]
```

Correctly retrieved:

```text
{2, 3}
```

So:

```text
true positives = 2
```

### Recall

How much of the expected relevant information was retrieved?

```text
recall
=
correct relevant retrieved
/
all expected relevant
```

For the example:

```text
2 / 5 = 0.40
```

### Precision

How much of the retrieved set was actually relevant?

```text
precision
=
correct relevant retrieved
/
all retrieved
```

For the example:

```text
2 / 4 = 0.50
```

### Interpretation

High recall:

```text
few relevant items were missed
```

High precision:

```text
little irrelevant noise was retrieved
```

[[IMAGE_NEEDED: RAG precision and recall sets | Venn-style diagram showing expected relevant documents and retrieved documents with overlap as true positives; annotate recall as overlap/expected and precision as overlap/retrieved | Learner should notice that recall measures completeness while precision measures signal-to-noise]]

### Test threshold

A retrieval integration test may assert:

```python
assert recall >= 0.66
assert precision >= 0.66
```

Thresholds should match application requirements.

### Trade-off

Increasing retrieval count may improve recall while reducing precision.

That is why both metrics matter.

{{exercise:M01.L11.EX07}}

---

## 29. Test structured LLM decisions statistically

If an LLM returns structured output, tests can sometimes assert exact fields.

Example:

```text
query:
"Summarize this page"

expected selected tool:
"SUMMARIZER"
```

A parameterized test can include many examples.

The source recommends using a balanced distribution across categories.

### Why many examples?

One or two prompts do not reveal the model's behavior distribution.

A larger representative set provides better evidence.

### Example target

```text
100 user-query examples
balanced across tool categories
```

Then measure:

```text
correct tool-selection rate
failure distribution
confusion between categories
```

### Avoid assuming one run proves reliability

A probabilistic model can occasionally fail.

The goal is to understand:

- how often,
- where,
- under which prompt patterns.

---

## 30. Behavioral testing for dynamic model output

Natural-language output is difficult to test using exact equality.

Behavioral testing treats the model as a black box.

```text
input
→ model
→ evaluate properties
```

Possible properties listed in the source include:

- sentiment,
- response length,
- readability,
- factual/grounded behavior,
- "I don't know" behavior when context is insufficient.

### Why behavioral tests fit GenAI

You do not need the exact same sentence.

You need properties such as:

```text
relevant
professional
grounded
not toxic
appropriate detail
```

### Representative samples

You cannot cover the full input space.

Select test cases that represent:

- normal usage,
- edge cases,
- failure scenarios,
- key user groups,
- important workflows.

### TDD for model behavior

The source suggests using behavioral tests while iterating:

- prompts,
- temperature,
- other model settings.

The test suite becomes the target behavior contract.

---

## 31. Minimum functionality tests (MFTs)

Minimum functionality tests verify basic expected behaviors on simple, well-defined cases.

Examples include:

- grammatically acceptable output,
- well-known factual behavior,
- zero/low toxicity,
- rejection of clearly inappropriate inputs,
- empathy when required,
- readable/professional output.

### Readability example

The source uses a readability metric.

Conceptually:

```python
response = llm.invoke(prompt)

score = readability(response)

assert expected_min < score < upper_bound
```

Why an upper bound?

An extremely high simplicity score could indicate that the answer became too shallow.

The lesson is broader than one readability formula:

> **Convert a product requirement into a measurable property and assert an acceptable range.**

---

## 32. Invariance tests (ITs)

An invariance test asks:

> **Does irrelevant input variation leave important behavior effectively unchanged?**

The source gives examples such as changing:

- case,
- whitespace,
- special characters,
- spelling variants/typos,
- synonyms,
- number formats,
- ordering of context chunks.

Example:

```text
"Explain behavioral testing"

"EXPLAIN BEHAVIORAL TESTING"

"Explain behavioural testing"
```

If the product should treat these as equivalent, measured output properties should remain within acceptable bounds.

### What invariance tests reveal

They test robustness to perturbations.

A fragile system may behave very differently after minor irrelevant formatting changes.

{{exercise:M01.L11.EX08}}

---

## 33. Directional expectation tests (DETs)

A directional expectation test checks whether changing the input causes the output property to move in the expected direction.

Example:

```text
simple prompt
→ shorter/simple response

more complex prompt
→ more detailed response
```

An assertion might be:

```python
assert len(complex_response) > (
    len(simple_response)
)
```

Length is only a proxy, but the pattern is what matters.

Other directional expectations might include:

```text
more specificity requested
→ more specific output

stronger negative sentiment
→ response acknowledges emotional context more clearly
```

DETs test logical sensitivity to meaningful changes.

---

## 34. Auto-evaluation with another model

Some output properties are difficult to measure using deterministic code.

The chapter introduces **auto-evaluation**.

Flow:

```text
test prompt
    ↓
model under test
    ↓
response
    ↓
evaluator/discriminator model
    ↓
structured score/judgment
    ↓
assert threshold
```

Example property:

```text
toxicity
```

The evaluator may return:

```json
{
  "is_toxic": false,
  "reason": "..."
}
```

### Why structured evaluator output?

Tests need predictable fields.

Do not make assertions against arbitrary evaluator prose.

### Benefits

Evaluator models can assess:

- relevance,
- correctness,
- toxicity,
- hallucination,
- other qualitative properties.

### Drawbacks

Each evaluator introduces:

- additional model cost,
- additional latency,
- another probabilistic component.

An evaluator can also be wrong.

So thresholds and representative validation are still necessary.

[[IMAGE_NEEDED: Auto-evaluation testing loop | Diagram showing test prompt → model under test → candidate response → evaluator model → structured score → assertion threshold | Learner should notice that evaluator-based tests add a second probabilistic model to the testing system]]

{{exercise:M01.L11.EX09}}

---

## 35. End-to-end testing

E2E testing verifies a larger functional journey.

In the chapter's RAG project:

```text
upload file
→ extract content
→ transform/chunk
→ store vectors
→ ask question
→ retrieve context
→ invoke model
→ return answer
```

This crosses many boundaries.

### Why E2E tests are valuable

They can reveal:

- integration gaps,
- unexpected component interaction,
- system-level behavior,
- missing assumptions not visible in unit tests.

### Why they are expensive

They are:

- slower,
- harder to set up,
- more brittle,
- more likely to depend on external systems.

The source recommends running them less frequently than unit tests.

### Manual E2E is still useful

A human interacting with the real UI can find:

- usability problems,
- unexpected visual/flow issues,
- failures that automated assertions did not anticipate.

Automation should reduce repetitive manual work, not necessarily eliminate every human check.

---

## 36. Vertical E2E tests

A vertical test checks one feature across several application layers.

Example from the chapter:

```text
POST /upload
    ↓
API controller
    ↓
file processing
    ↓
vector storage
    ↓
verify stored document
```

This crosses layers while focusing on one workflow.

### FastAPI test client

A global fixture can expose a reusable test client.

Conceptually:

```python
@pytest.fixture
async def test_client():
    async with ClientSession() as client:
        yield client
```

Then:

```python
response = await test_client.post(
    "/upload",
    files=file_data,
)
```

The test can verify:

- API status,
- downstream side effect,
- stored data.

### Mock or real dependency?

If the database is mocked:

```text
you verify correct database call
```

If the database is real:

```text
you verify actual storage/retrieval
```

These provide different levels of confidence.

---

## 37. Horizontal E2E tests

Horizontal E2E tests follow a broader user scenario across integrated systems.

Example:

```text
user uploads document
    ↓
document is indexed
    ↓
user asks question
    ↓
RAG retrieves uploaded information
    ↓
LLM answers from that information
```

A test can assert:

```text
upload succeeded
and
answer contains expected grounded fact
```

### Negative case

The source suggests a valuable complementary check:

Before the document is uploaded:

```text
question asks for document-specific fact
→ model should not invent the answer
```

After upload:

```text
same question
→ answer should be grounded in uploaded content
```

This tests both:

- retrieval behavior,
- hallucination/grounding behavior.

[[IMAGE_NEEDED: Vertical versus horizontal E2E | Side-by-side RAG diagrams: vertical test moving through layers for one upload/storage feature, horizontal test following an entire user scenario from upload through question answering | Learner should notice that vertical tests are feature-focused while horizontal tests follow broader user journeys]]

---

## 38. Build a balanced test strategy for GenAI

A practical GenAI testing plan should not be:

```text
only unit tests
```

or:

```text
only expensive E2E tests
```

A balanced plan can include:

### Static layer

- typing,
- linting/static checks,
- schema validation.

### Unit layer

Test deterministic application logic:

- chunking,
- filtering,
- formatting,
- prompt construction helpers,
- authorization rules.

Mock external services where appropriate.

### Integration layer

Test real interfaces:

- vector database retrieval,
- relational database contracts,
- provider response schema,
- embedding/vector compatibility.

### Behavioral/model layer

Test:

- relevance,
- groundedness,
- readability,
- toxicity,
- robustness,
- directional behavior.

### E2E layer

Test critical workflows:

- document upload and indexing,
- RAG Q&A,
- login → generation → persistence,
- other high-value user journeys.

### Regression layer

Maintain representative test datasets and rerun when:

- prompts change,
- models change,
- retrieval changes,
- provider SDKs change.

### Design for idempotency

Each test should be able to run:

```text
once
or
100 times
```

without depending on leftover state.

### Final test-design question

For every test, ask:

```text
What behavior am I gaining confidence in?
What is the smallest boundary that can verify it?
What dependency must be real?
What dependency should be isolated?
What failure would this test catch?
```

That question is more valuable than maximizing raw test count.

---

## Important misconceptions

### Misconception 1

> Tests are only worthwhile after the product is finished.

### Why this is wrong

The chapter advocates earlier testing because late failures become harder and more expensive to diagnose.

### Misconception 2

> 100% code coverage means the system is correct.

### Why this is wrong

Coverage verifies executed code paths, not whether the application satisfies the correct business requirements.

### Misconception 3

> Unit, integration, and E2E tests differ only in how many assertions they contain.

### Why this is wrong

They differ mainly in testing boundary and number/type of components involved.

### Misconception 4

> Tests should verify internal implementation so they detect every refactor.

### Why this is wrong

Tests coupled to implementation details can fail even when observable behavior remains correct.

### Misconception 5

> Shared mutable global fixtures are harmless because tests run separately.

### Why this is wrong

One test can mutate shared state and cause order-dependent or flaky behavior.

### Misconception 6

> Parameterization is only a way to reduce lines of test code.

### Why this is incomplete

It also encourages systematic coverage of valid, invalid, boundary, and large-input cases through one consistent behavior contract.

### Misconception 7

> Async tests are flaky because asyncio is unreliable.

### Why this is wrong

Flakiness often comes from poor isolation, external I/O timing, unawaited operations, shared state, or uncontrolled execution order.

### Misconception 8

> Mock every dependency in every test.

### Why this is wrong

Over-mocking can hide real interface and integration failures.

### Misconception 9

> A mock and a stub are the same concept.

### Why this is wrong

A stub mainly supplies predefined behavior, while a mock additionally verifies expected interactions.

### Misconception 10

> Integration tests should cover the entire application.

### Why this is wrong

The source scopes integration tests around interfaces between a small number of components.

### Misconception 11

> RAG recall and precision measure the same thing.

### Why this is wrong

Recall measures how much relevant information was retrieved; precision measures how much retrieved information was relevant.

### Misconception 12

> Natural-language LLM output should be tested with exact string equality.

### Why this is wrong

Valid model outputs can vary. Behavioral properties and statistical evaluation are often more appropriate.

### Misconception 13

> A model that passes ten prompts is proven reliable for all user inputs.

### Why this is wrong

The GenAI input space is too large; tests provide statistical confidence over representative samples rather than complete coverage.

### Misconception 14

> An invariance test expects every output string to be identical.

### Why this is wrong

It checks that important behavior/properties remain stable under irrelevant input perturbations.

### Misconception 15

> A directional expectation test means the output must stay unchanged.

### Why this is wrong

It checks that output properties change in the expected direction when meaningful input properties change.

### Misconception 16

> LLM-as-judge auto-evaluation gives objective ground truth.

### Why this is wrong

The evaluator is also probabilistic and adds cost, latency, and its own error modes.

### Misconception 17

> E2E tests should be run for every tiny code change because they give the highest confidence.

### Why this is wrong

They are expensive, brittle, and slow. The source recommends using fewer of them and running them less frequently.

### Misconception 18

> Calling one FastAPI endpoint always counts as an integration test.

### Why this is wrong

An endpoint can invoke many layers/services, so endpoint-level invocation often crosses an E2E-sized boundary.

---

## Key terminology

| Term | Meaning |
|---|---|
| Unit test | Test of one isolated component/function |
| Integration test | Test of the interaction/contract between components |
| E2E test | Test of a broader application workflow across many components |
| Static check | Verification performed without executing full runtime behavior |
| Test boundary | Explicit definition of what components are inside/outside a test |
| Black-box testing | Testing observable inputs/outputs without relying on internal implementation |
| Validation | Confirming that the right requirements/system are being built |
| Verification | Confirming implementation satisfies defined requirements |
| Code coverage | Measure of how much code is executed by tests |
| Shift-left testing | Moving testing earlier in the development lifecycle |
| TDD | Test-driven development: test first, minimal code, then refactor |
| Scope | Systems/scenarios included in a test plan |
| Coverage | Portion of the defined system touched by tests |
| Comprehensiveness | Depth and completeness of cases within scope |
| Fixture | Fixed setup data/dependency used by tests |
| Fixture scope | Lifetime over which a pytest fixture is reused |
| Parameterization | Running one test definition across multiple input/expected cases |
| `conftest.py` | Pytest configuration module for shared fixtures/config |
| Setup | Resource/state preparation before a test |
| Teardown | Cleanup after a test |
| Isolation | Preventing tests from interfering with each other |
| Idempotent test | Repeated test execution yields the same result under the same conditions |
| Flaky test | Test that passes/fails inconsistently without relevant code changes |
| Test double | Replacement for a real dependency during testing |
| Fake | Simplified functional dependency implementation |
| Dummy | Placeholder object/argument |
| Stub | Dependency returning canned values |
| Spy | Dependency double that records interactions |
| Mock | Test double that verifies expected interactions |
| Patch | Runtime replacement of a dependency/function during a test |
| Dependency injection | Supplying dependencies explicitly so tests can substitute controlled implementations |
| Precision | Fraction of retrieved items that are relevant |
| Recall | Fraction of relevant expected items that were retrieved |
| Behavioral testing | Testing output properties/behavior rather than exact generated content |
| MFT | Minimum functionality test |
| IT | Invariance test |
| DET | Directional expectation test |
| Auto-evaluation | Using another model/evaluator to score model output |
| Regression test | Test guarding against previously working behavior degrading |
| Model drift | Model performance/behavior changing over time |
| Concept drift | Target relationships/meaning changing over time |
| Data drift | Input distribution changing over time |
| Vertical E2E | One feature tested through multiple application layers |
| Horizontal E2E | Broad user scenario tested across integrated systems |

---

## Self-check

Before continuing, make sure you can answer:

1. Why does the value of testing increase as system risk increases?
2. Which project conditions make testing especially important?
3. What is a unit-test boundary?
4. What does an integration test verify?
5. What does an E2E test verify?
6. Why do larger test boundaries tend to be slower and more brittle?
7. What can static checks catch before runtime?
8. What is black-box testing?
9. Why can testing implementation details make refactoring painful?
10. What is validation?
11. What is verification?
12. Why does 100% code coverage not guarantee correct product behavior?
13. What is shift-left testing?
14. What is the TDD loop?
15. Why can TDD-like testing help prompt engineering?
16. What is test scope?
17. What is test coverage?
18. What is test comprehensiveness?
19. What are the four test-data classes described in the chapter?
20. Why test invalid inputs?
21. Why test boundary values?
22. Why use huge test inputs?
23. What are Given, When, and Then?
24. How does Arrange–Act–Assert relate to GWT?
25. What belongs in cleanup?
26. What does the testing pyramid recommend?
27. Why does the chapter consider the testing trophy attractive for GenAI services?
28. When might a honeycomb approach be useful?
29. Why is the ice-cream cone considered an anti-pattern?
30. What is wrong with an hourglass test distribution?
31. Why are GenAI outputs more difficult to test deterministically?
32. What does representative input distribution mean?
33. Why is statistical confidence more realistic than full model coverage?
34. Why can GenAI test suites become expensive?
35. What is regression testing for a model-backed service?
36. What is model drift?
37. What is concept drift?
38. What is data drift?
39. Why should provider model changes trigger regression evaluation?
40. Why is bias testing use-case specific?
41. What are adversarial tests intended to verify?
42. Why is full GenAI input-space coverage impossible in practice?
43. What is behavioral testing?
44. Which parts of a RAG pipeline are good unit-test candidates?
45. Which RAG boundary is suitable for integration testing?
46. How does pytest discover test modules?
47. What should a focused unit test contain?
48. What is a fresh fixture?
49. Why are mutable shared fixtures risky?
50. What does pytest fixture scope control?
51. Why might a broad fixture scope still be useful?
52. What does parameterization solve?
53. How would you parameterize valid, invalid, boundary, and huge cases?
54. What is `pytest.raises` used for?
55. What is `conftest.py` used for?
56. What happens before and after `yield` in a fixture?
57. Why is teardown important?
58. How does `pytest-asyncio` help?
59. What is test isolation?
60. What does idempotency mean for tests?
61. Why can async scheduling expose flakiness?
62. Why should blocking sync I/O be avoided inside async tests?
63. When can mocking make an async unit test simpler?
64. What is a fake?
65. What is a dummy?
66. What is a stub?
67. What is a spy?
68. What is a mock?
69. Why should you never mock the behavior you are trying to test?
70. What can `pytest-mock` verify?
71. Why is excessive mocking dangerous?
72. How does dependency injection reduce brittle patching?
73. What should be real inside an integration test?
74. What does RAG recall measure?
75. What does RAG precision measure?
76. Why can increasing retrieval count improve recall while hurting precision?
77. Why use thresholds in retrieval integration tests?
78. Why should structured LLM tests include many representative examples?
79. Why balance test categories?
80. What does an MFT test?
81. What does an invariance test test?
82. What does a directional expectation test test?
83. Give one example of an irrelevant prompt perturbation.
84. Give one example of a meaningful directional prompt change.
85. What is auto-evaluation?
86. Why should evaluator output be structured?
87. What are two drawbacks of LLM-as-judge tests?
88. Why are E2E tests valuable?
89. Why should E2E tests run less frequently?
90. What is a vertical E2E test?
91. What is a horizontal E2E test?
92. Why might a real database provide stronger E2E confidence than a mock?
93. What negative RAG E2E test can check hallucination before document upload?
94. How do static, unit, integration, behavioral, and E2E layers complement one another?
95. What makes a test suite balanced rather than merely large?
96. What is the smallest boundary principle for choosing a test type?

---

## Retain this idea

**A strong GenAI test strategy separates deterministic application logic from probabilistic model behavior: use small isolated unit tests for code, real integration tests for important interfaces, behavioral and statistical evaluation for variable model outputs, and a small number of critical E2E workflows for system confidence. Design every test around a clear boundary, representative data, isolation, and a specific failure you want to detect.**
""",

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-testing", "title": "Why testing matters", "order": 1},
            {"id": "test-types", "title": "Unit, integration, and end-to-end tests", "order": 2},
            {"id": "test-boundaries", "title": "Test behavior, not implementation details", "order": 3},
            {"id": "verification-validation", "title": "Verification versus validation", "order": 4},
            {"id": "shift-left-tdd", "title": "Shift testing left and use TDD when useful", "order": 5},
            {"id": "test-dimensions", "title": "Scope, coverage, and comprehensiveness", "order": 6},
            {"id": "test-data", "title": "Design test data intentionally", "order": 7},
            {"id": "test-phases", "title": "Structure tests with Given–When–Then", "order": 8},
            {"id": "test-environments", "title": "Test across static, build, and runtime environments", "order": 9},
            {"id": "testing-strategies", "title": "Testing pyramid, trophy, and honeycomb", "order": 10},
            {"id": "testing-antipatterns", "title": "Testing anti-patterns", "order": 11},
            {"id": "genai-challenges", "title": "Why GenAI testing is different", "order": 12},
            {"id": "output-variability", "title": "Probabilistic output and statistical confidence", "order": 13},
            {"id": "cost-performance-regression", "title": "Cost, latency, and regression challenges", "order": 14},
            {"id": "bias-adversarial", "title": "Bias and adversarial testing", "order": 15},
            {"id": "unbounded-coverage", "title": "You cannot fully cover a generative model", "order": 16},
            {"id": "rag-test-project", "title": "Testing project: a RAG system", "order": 17},
            {"id": "pytest-basics", "title": "Organize and run pytest tests", "order": 18},
            {"id": "fixtures", "title": "Pytest fixtures and fixture scope", "order": 19},
            {"id": "parameterization", "title": "Parameterize test cases", "order": 20},
            {"id": "conftest", "title": "Share fixtures with conftest.py", "order": 21},
            {"id": "setup-teardown", "title": "Setup and teardown with yield fixtures", "order": 22},
            {"id": "async-tests", "title": "Test asynchronous code carefully", "order": 23},
            {"id": "test-doubles", "title": "Test doubles: fake, dummy, stub, spy, mock", "order": 24},
            {"id": "mocking-patching", "title": "Mocking and patching with pytest", "order": 25},
            {"id": "dependency-injection-testing", "title": "Prefer dependency injection when it reduces brittle patching", "order": 26},
            {"id": "integration-tests", "title": "Integration tests verify interfaces", "order": 27},
            {"id": "rag-precision-recall", "title": "Measure RAG retrieval with precision and recall", "order": 28},
            {"id": "structured-llm-tests", "title": "Test structured LLM decisions statistically", "order": 29},
            {"id": "behavioral-testing", "title": "Behavioral testing for dynamic model output", "order": 30},
            {"id": "mft", "title": "Minimum functionality tests (MFTs)", "order": 31},
            {"id": "invariance-tests", "title": "Invariance tests (ITs)", "order": 32},
            {"id": "directional-tests", "title": "Directional expectation tests (DETs)", "order": 33},
            {"id": "auto-evaluation", "title": "Auto-evaluation with another model", "order": 34},
            {"id": "e2e-testing", "title": "End-to-end testing", "order": 35},
            {"id": "vertical-e2e", "title": "Vertical E2E tests", "order": 36},
            {"id": "horizontal-e2e", "title": "Horizontal E2E tests", "order": 37},
            {"id": "balanced-test-strategy", "title": "Build a balanced test strategy for GenAI", "order": 38},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L11.EX01",
            "title": "Draw the Right Test Boundary",
            "lesson_code": "M01.L11",
            "section_id": "test-types",
            "placement": "after_section",
            "description": (
                "Choose unit, integration, or E2E boundaries for common GenAI service behaviors."
            ),
            "instructions": (
                "Classify each test as `unit`, `integration`, or `E2E`:\n\n"
                "1. Check that `chunk(tokens, 3)` returns the correct token groups.\n"
                "2. Query a real Qdrant collection through the retrieval repository and verify returned IDs.\n"
                "3. POST a document to `/upload`, then ask `/generate` a question grounded in that document.\n"
                "4. Test a prompt-formatting helper while replacing the LLM client with a stub.\n"
                "5. Verify that the SQLAlchemy repository stores and reads a row from a real test PostgreSQL database.\n\n"
                "For each, state what is inside and outside the test boundary."
            ),
            "expected_output": (
                "Five classifications plus explicit test boundaries."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "test-boundaries",
                "unit-testing",
                "integration-testing",
                "e2e-testing",
            ],
        },
        {
            "id": "M01.L11.EX02",
            "title": "Design Robust Input Cases",
            "lesson_code": "M01.L11",
            "section_id": "test-data",
            "placement": "after_section",
            "description": (
                "Apply valid, invalid, boundary, and huge-data categories to one component."
            ),
            "instructions": (
                "Assume a chunker accepts `chunk_size` values from 1 to 2000.\n\n"
                "Design:\n"
                "1. two valid cases,\n"
                "2. two invalid cases,\n"
                "3. two boundary cases,\n"
                "4. one huge-data case.\n\n"
                "For every case, specify the expected behavior or exception."
            ),
            "expected_output": (
                "A seven-case table containing input type, input value, and expected behavior."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "test-data-design",
                "boundary-testing",
                "negative-testing",
            ],
        },
        {
            "id": "M01.L11.EX03",
            "title": "Write a Focused Pytest Unit Test",
            "lesson_code": "M01.L11",
            "section_id": "pytest-basics",
            "placement": "after_section",
            "description": (
                "Practice Given–When–Then on deterministic RAG transformation logic."
            ),
            "instructions": (
                "Write a pytest unit test for:\n\n"
                "```python\n"
                "def chunk(tokens: list[int], chunk_size: int) -> list[list[int]]:\n"
                "    if chunk_size <= 0:\n"
                "        raise ValueError('Chunk size must be greater than 0')\n"
                "    return [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]\n"
                "```\n\n"
                "Requirements:\n"
                "1. mark Given, When, and Then with comments,\n"
                "2. test `[1,2,3,4,5]` with size 2,\n"
                "3. assert the complete returned value,\n"
                "4. write a second test for `chunk_size=0` using `pytest.raises`."
            ),
            "expected_output": (
                "Two small runnable pytest unit tests."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "pytest",
                "gwt",
                "unit-test-design",
            ],
        },
        {
            "id": "M01.L11.EX04",
            "title": "Parameterize the Chunker Test",
            "lesson_code": "M01.L11",
            "section_id": "parameterization",
            "placement": "after_section",
            "description": (
                "Use one behavior contract across several valid and invalid inputs."
            ),
            "instructions": (
                "Rewrite your chunker tests using `@pytest.mark.parametrize`.\n\n"
                "Include:\n"
                "- chunk sizes 1, 2, and 5,\n"
                "- empty token list,\n"
                "- chunk size larger than the list,\n"
                "- zero chunk size,\n"
                "- negative chunk size,\n"
                "- a large token list.\n\n"
                "Handle the error cases with `pytest.raises`."
            ),
            "expected_output": (
                "One parameterized pytest function covering normal, boundary, invalid, and large inputs."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "pytest-parameterization",
                "robustness-testing",
                "exceptions",
            ],
        },
        {
            "id": "M01.L11.EX05",
            "title": "Find the Flaky Async Test",
            "lesson_code": "M01.L11",
            "section_id": "async-tests",
            "placement": "after_section",
            "description": (
                "Recognize shared state and asynchronous I/O problems that break test idempotency."
            ),
            "instructions": (
                "You have an async test suite where:\n"
                "- all tests share one mutable list fixture,\n"
                "- one test appends records but does not reset them,\n"
                "- database calls are awaited inconsistently,\n"
                "- some tests use blocking `time.sleep()` inside async functions.\n\n"
                "Identify every source of flakiness and propose a correction for each.\n"
                "Then explain what it means for the corrected tests to be idempotent."
            ),
            "expected_output": (
                "A flakiness diagnosis with isolation, await, sleep, fixture, and cleanup fixes."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "async-testing",
                "test-isolation",
                "idempotency",
                "flaky-tests",
            ],
        },
        {
            "id": "M01.L11.EX06",
            "title": "Choose the Correct Test Double",
            "lesson_code": "M01.L11",
            "section_id": "test-doubles",
            "placement": "after_section",
            "description": (
                "Differentiate fake, dummy, stub, spy, and mock by testing need."
            ),
            "instructions": (
                "Choose `fake`, `dummy`, `stub`, `spy`, or `mock` for each situation:\n\n"
                "1. You need a lightweight in-memory replacement for a database.\n"
                "2. A function requires a token argument that the test path never uses.\n"
                "3. The LLM must always return the same canned response.\n"
                "4. You want to record how many times `send_email()` is called without failing automatically.\n"
                "5. The test must fail unless `llm.invoke()` is called exactly once with a specific prompt.\n\n"
                "Explain each selection."
            ),
            "expected_output": (
                "Five test-double choices with explanations."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "test-doubles",
                "mocking",
                "unit-isolation",
            ],
        },
        {
            "id": "M01.L11.EX07",
            "title": "Calculate RAG Retrieval Precision and Recall",
            "lesson_code": "M01.L11",
            "section_id": "rag-precision-recall",
            "placement": "after_section",
            "description": (
                "Compute the two retrieval metrics and interpret what each reveals."
            ),
            "instructions": (
                "Given:\n\n"
                "```text\n"
                "expected = [1, 2, 3, 4, 5]\n"
                "retrieved = [2, 3, 6, 7]\n"
                "```\n\n"
                "1. Identify the true-positive document IDs.\n"
                "2. Calculate recall.\n"
                "3. Calculate precision.\n"
                "4. Explain which metric indicates missing relevant documents.\n"
                "5. Explain which metric indicates noisy retrieved results.\n"
                "6. Describe one retrieval change that could increase recall but potentially reduce precision."
            ),
            "expected_output": (
                "Correct calculations (`recall=0.40`, `precision=0.50`) plus interpretation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "rag-evaluation",
                "precision",
                "recall",
            ],
        },
        {
            "id": "M01.L11.EX08",
            "title": "Create Three Behavioral Test Types",
            "lesson_code": "M01.L11",
            "section_id": "invariance-tests",
            "placement": "after_section",
            "description": (
                "Design MFT, invariance, and directional tests for one GenAI assistant."
            ),
            "instructions": (
                "For a beginner-facing AI tutor, design:\n\n"
                "1. one minimum functionality test checking readability/professional tone,\n"
                "2. one invariance test where case or minor spelling changes should not materially alter behavior,\n"
                "3. one directional expectation test where asking for more detail should increase response detail.\n\n"
                "For each, specify:\n"
                "- input(s),\n"
                "- measured property,\n"
                "- pass condition."
            ),
            "expected_output": (
                "Three behavioral test specifications with measurable properties and thresholds/conditions."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "behavioral-testing",
                "mft",
                "invariance-testing",
                "directional-expectation",
            ],
        },
        {
            "id": "M01.L11.EX09",
            "title": "Design an Auto-Evaluation Test",
            "lesson_code": "M01.L11",
            "section_id": "auto-evaluation",
            "placement": "after_section",
            "description": (
                "Use a second model to grade a dynamic response without relying on exact string equality."
            ),
            "instructions": (
                "Design a test for a customer-support LLM that must remain respectful.\n\n"
                "The test should:\n"
                "1. call the model under test using a difficult/rude input,\n"
                "2. send its response to an evaluator model,\n"
                "3. require structured evaluator output with `is_toxic: bool` and `reason: str`,\n"
                "4. assert `is_toxic == False`,\n"
                "5. explain one reason the evaluator itself may be wrong,\n"
                "6. explain one reason this test should not run on every tiny unit-test cycle."
            ),
            "expected_output": (
                "Auto-evaluation pseudocode and evaluator cost/reliability discussion."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "llm-as-judge",
                "auto-evaluation",
                "behavioral-metrics",
            ],
        },
        {
            "id": "M01.L11.EX10",
            "title": "Design Vertical and Horizontal RAG E2E Tests",
            "lesson_code": "M01.L11",
            "section_id": "horizontal-e2e",
            "placement": "after_section",
            "description": (
                "Separate a focused cross-layer feature test from a complete user workflow."
            ),
            "instructions": (
                "Design two tests.\n\n"
                "**Vertical test:**\n"
                "Upload `test.txt` and verify that its content is actually stored/retrievable from the vector database.\n\n"
                "**Horizontal test:**\n"
                "1. ask a document-specific question before upload and require an `I don't know`-style response,\n"
                "2. upload the document,\n"
                "3. ask the same question again,\n"
                "4. require the answer to use the uploaded fact.\n\n"
                "For both tests, list the components inside the boundary and the expected side effects."
            ),
            "expected_output": (
                "Two E2E test specifications with boundaries and assertions."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "vertical-e2e",
                "horizontal-e2e",
                "rag-grounding",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L11.QZ01",

        "title": "Testing AI Services — Knowledge Check",

        "lesson_code": "M01.L11",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L11.Q01",
                "section_id": "test-types",
                "question": "What is the defining characteristic of a unit test?",
                "options": [
                    "It tests a small component in isolation",
                    "It always calls every production dependency",
                    "It always starts from the UI",
                    "It must use a real LLM",
                ],
                "correct": 0,
                "explanation": (
                    "Unit tests intentionally use a small boundary around one component/function."
                ),
            },
            {
                "id": "M01.L11.Q02",
                "section_id": "verification-validation",
                "question": "Why does 100% code coverage not guarantee a correct product?",
                "options": [
                    "The tested implementation may still satisfy the wrong or incomplete requirements",
                    "Coverage cannot execute Python code",
                    "Coverage always ignores assertions",
                    "Validation is the same thing as coverage",
                ],
                "correct": 0,
                "explanation": (
                    "Coverage helps verification but cannot prove that the system implements the right business needs."
                ),
            },
            {
                "id": "M01.L11.Q03",
                "section_id": "test-data",
                "question": "What is boundary test data?",
                "options": [
                    "Inputs at or near accepted upper/lower limits",
                    "Only random valid inputs",
                    "Only data copied from production",
                    "Inputs that always crash intentionally",
                ],
                "correct": 0,
                "explanation": (
                    "Boundary tests probe behavior where accepted ranges begin or end."
                ),
            },
            {
                "id": "M01.L11.Q04",
                "section_id": "testing-strategies",
                "question": "Why does the chapter consider integration-heavy trophy testing attractive for GenAI services?",
                "options": [
                    "GenAI services often depend on many external systems and important failures occur at interfaces",
                    "Unit tests cannot be written in Python",
                    "E2E tests are always free",
                    "Static checking replaces runtime tests",
                ],
                "correct": 0,
                "explanation": (
                    "Databases, model APIs, vector stores, filesystems, and other interfaces make integration coverage especially valuable."
                ),
            },
            {
                "id": "M01.L11.Q05",
                "section_id": "output-variability",
                "question": "Why are exact string equality tests often inappropriate for open-ended LLM responses?",
                "options": [
                    "Several differently worded outputs may all be valid because generation is probabilistic",
                    "LLMs can never return strings",
                    "Pytest cannot compare strings",
                    "Exact equality only works with databases",
                ],
                "correct": 0,
                "explanation": (
                    "Open-ended model responses vary; behavior/property assertions are often more meaningful."
                ),
            },
            {
                "id": "M01.L11.Q06",
                "section_id": "fixtures",
                "question": "What is a major risk of a mutable shared fixture?",
                "options": [
                    "One test can modify it and change another test's outcome",
                    "It automatically becomes read-only",
                    "It disables pytest collection",
                    "It forces all tests to run as E2E tests",
                ],
                "correct": 0,
                "explanation": (
                    "Shared mutable state violates test isolation and can create order-dependent flakiness."
                ),
            },
            {
                "id": "M01.L11.Q07",
                "section_id": "parameterization",
                "question": "What is the main purpose of pytest parameterization?",
                "options": [
                    "Run one behavior test across many input and expected-output cases without duplicating the test logic",
                    "Replace every fixture with a production database",
                    "Make model output deterministic",
                    "Convert unit tests into E2E tests",
                ],
                "correct": 0,
                "explanation": (
                    "Parameterization applies one test contract to several representative inputs."
                ),
            },
            {
                "id": "M01.L11.Q08",
                "section_id": "async-tests",
                "question": "What does idempotency mean for a test suite in this chapter?",
                "options": [
                    "Repeated runs under the same conditions should produce the same outcomes",
                    "Every test should call an LLM twice",
                    "Every test should mutate a shared fixture",
                    "Async tests should run in random order",
                ],
                "correct": 0,
                "explanation": (
                    "Isolation and cleanup should make repeated test execution stable and independent of prior runs."
                ),
            },
            {
                "id": "M01.L11.Q09",
                "section_id": "test-doubles",
                "question": "Which test double primarily returns predefined canned responses?",
                "options": [
                    "Stub",
                    "Spy",
                    "Mock only",
                    "E2E client",
                ],
                "correct": 0,
                "explanation": (
                    "A stub supplies predefined behavior/data without requiring the real dependency."
                ),
            },
            {
                "id": "M01.L11.Q10",
                "section_id": "mocking-patching",
                "question": "What is a major danger of excessive mocking?",
                "options": [
                    "Tests can pass while real component interfaces are broken",
                    "Mocks always call paid APIs",
                    "Mocks prevent unit-test isolation",
                    "Mocks force mutable shared fixtures",
                ],
                "correct": 0,
                "explanation": (
                    "Mocks isolate dependencies, but overuse can hide failures that only real integrations expose."
                ),
            },
            {
                "id": "M01.L11.Q11",
                "section_id": "rag-precision-recall",
                "question": "What does retrieval recall measure?",
                "options": [
                    "The fraction of expected relevant items that were successfully retrieved",
                    "The fraction of retrieved items that were relevant",
                    "The model's output token count",
                    "The test suite's code coverage",
                ],
                "correct": 0,
                "explanation": (
                    "Recall measures completeness: how much of the relevant set was found."
                ),
            },
            {
                "id": "M01.L11.Q12",
                "section_id": "behavioral-testing",
                "question": "What does behavioral testing focus on for GenAI outputs?",
                "options": [
                    "Observable output properties and behavior rather than one exact generated string",
                    "Private model weights",
                    "Only source-code line coverage",
                    "Only database query speed",
                ],
                "correct": 0,
                "explanation": (
                    "Behavioral tests evaluate properties such as relevance, readability, toxicity, or groundedness."
                ),
            },
            {
                "id": "M01.L11.Q13",
                "section_id": "invariance-tests",
                "question": "What is the purpose of an invariance test?",
                "options": [
                    "Verify that irrelevant changes to input do not materially change the intended behavior",
                    "Require the response to become longer for more complex prompts",
                    "Verify database migrations",
                    "Always compare exact output strings",
                ],
                "correct": 0,
                "explanation": (
                    "Invariance tests probe robustness to perturbations that should not matter."
                ),
            },
            {
                "id": "M01.L11.Q14",
                "section_id": "directional-tests",
                "question": "What does a directional expectation test check?",
                "options": [
                    "That an output property moves in the expected direction when a meaningful input property changes",
                    "That every output remains identical",
                    "That all fixtures have session scope",
                    "That unit tests use production APIs",
                ],
                "correct": 0,
                "explanation": (
                    "Directional tests assert logical response changes, such as more detail for a more complex request."
                ),
            },
            {
                "id": "M01.L11.Q15",
                "section_id": "balanced-test-strategy",
                "type": "open",
                "question": (
                    "Design a test strategy for a production RAG chatbot. Include static checks, "
                    "unit tests, integration tests with the vector database, behavioral tests for "
                    "groundedness/readability, auto-evaluation where useful, and one critical E2E "
                    "workflow. Explain which dependencies you would mock and which you would keep real."
                ),
            },
        ],

        "passing_score": 70,
    },
}
