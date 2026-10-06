"""M01.L10 — Optimizing AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 10, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L10"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Optimize GenAI services for performance, cost, throughput, latency, and output "
    "quality using batch processing, exact and semantic caching, provider prompt "
    "caching, model quantization, structured outputs, systematic prompt engineering, "
    "agentic prompting patterns, and carefully justified fine-tuning."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Optimizing AI Services",

    "slug": "generative-ai-services-m01-l10",

    "description": (
        "Learn how to optimize GenAI systems by distinguishing performance problems "
        "from quality problems, choosing batch APIs and caching strategies, understanding "
        "quantization trade-offs, making model outputs more structured, applying systematic "
        "prompting techniques, and deciding when fine-tuning is actually worth the cost."
    ),

    "order": 10,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.0,

    "skill_tags": [
        "ai-optimization",
        "batch-processing",
        "keyword-cache",
        "semantic-cache",
        "prompt-cache",
        "qdrant",
        "model-quantization",
        "structured-output",
        "prompt-engineering",
        "few-shot",
        "decomposition",
        "ensembling",
        "self-criticism",
        "agentic-systems",
        "fine-tuning",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L09",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Optimizing AI Services",

        "content": """
# Optimizing AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L10  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 10 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Separate performance optimization from output-quality optimization.
- Explain when batch processing is preferable to many individual model requests.
- Design structured batch requests and understand provider batch-job workflows.
- Explain what caching saves and why cache freshness matters.
- Distinguish keyword, semantic, and context/prompt caching.
- Explain how Redis can centralize application caches across several FastAPI instances.
- Design a semantic cache around embeddings, similarity search, and a vector store.
- Explain why a semantic cache can create incorrect hits even when two queries are similar.
- Tune semantic-cache thresholds and choose an eviction policy.
- Explain how prompt/context caching differs from response caching.
- Explain the relationship between model precision, memory requirements, and quantization.
- Compare FP32, FP16, BF16, INT8, INT4, and lower-precision formats conceptually.
- Describe the purpose of GPTQ-style post-training quantization.
- Use schema-driven structured outputs for reliable model-to-application integration.
- Explain why structured outputs are stronger than "please return JSON" alone.
- Build prompts using a role-context-task structure.
- Distinguish zero-shot, few-shot, and dynamic few-shot prompting.
- Explain the prompting families introduced in the chapter: thought generation, decomposition, ensembling, self-criticism, and agentic prompting.
- Explain how tool/function calling turns an LLM into a component of an agentic workflow.
- Recognize when fine-tuning may help and why it should usually not be the first optimization attempted.
- Describe the basic fine-tuning workflow: prepare data, train, evaluate, and deploy.
- Choose an optimization technique based on whether the bottleneck is cost, latency, throughput, memory, or output quality.

---

## 1. Start by identifying what you are optimizing

The chapter begins with an important distinction:

```text
Optimization does not mean one thing.
```

An AI service may need to improve:

- latency,
- throughput,
- operating cost,
- memory usage,
- output quality,
- output consistency,
- downstream reliability.

The source groups techniques into two broad categories.

### Performance-oriented optimizations

- batch processing,
- caching,
- model quantization.

### Quality-oriented optimizations

- structured outputs,
- prompt engineering,
- fine-tuning.

A technique may affect more than one dimension, but this classification gives you a useful starting point.

### Diagnose before optimizing

Suppose your application is too expensive.

Possible causes:

```text
same queries repeated
→ caching problem

thousands of offline items
→ batching problem

large self-hosted model barely fits GPU
→ quantization problem

huge repeated prompt
→ context-cache problem
```

Now suppose responses are unreliable.

Possible causes:

```text
invalid JSON
→ structured-output problem

vague instructions
→ prompt-design problem

specialized behavior not learned well enough
→ possibly fine-tuning problem
```

### Optimization is trade-off management

A useful engineering rule is:

> **Every optimization should have a target metric and an acceptable trade-off.**

For example:

```text
quantization
→ lower memory
↔ possible quality/speed trade-off

semantic cache
→ fewer expensive retrieval/model calls
↔ stale or incorrect cache hits

ensembling
→ potentially more reliable answers
↔ more model calls and higher cost
```

[[IMAGE_NEEDED: AI service optimization map | Diagram splitting optimization goals into performance (latency, throughput, memory, cost) and quality (reliability, structure, alignment), with techniques connected to each side: batching/caching/quantization and structured output/prompting/fine-tuning | Learner should notice that each technique addresses a specific bottleneck rather than being a universal improvement]]

{{exercise:M01.L10.EX01}}

---

## 2. Batch processing: stop sending one request per item

Imagine you need to classify:

```text
10,000 document titles
```

The naïve design is:

```text
document 1 → API call
document 2 → API call
document 3 → API call
...
document 10,000 → API call
```

Problems include:

- large request volume,
- rate-limit pressure,
- network overhead,
- higher cost,
- long total processing time.

The chapter presents two batching strategies.

### Strategy A — return several outputs in one normal request

Instead of a schema representing one classification:

```python
class DocumentClassification(BaseModel):
    document_id: str
    category: list[str]
```

define a batch schema:

```python
class BatchDocumentClassification(BaseModel):
    class Category(BaseModel):
        document_id: str
        category: list[str]

    categories: list[Category]
```

Then one model request can process several inputs.

### Strategy B — use a provider batch API

For large offline jobs, a provider may expose a dedicated batch service.

Conceptually:

```text
prepare batch file
    ↓
upload file
    ↓
submit background batch job
    ↓
provider queues/processes work
    ↓
poll/retrieve job status
    ↓
download results
```

This is particularly suitable when users do **not** need an immediate answer.

Examples:

- document classification,
- large translation jobs,
- offline extraction,
- bulk summarization.

### JSONL

The source creates a JSON Lines file.

Each line is one request object.

Example concept:

```text
{"custom_id": "request-1", ...}
{"custom_id": "request-2", ...}
{"custom_id": "request-3", ...}
```

The `custom_id` lets you connect returned results to original items.

### Batch work versus interactive work

A useful distinction is:

```text
Interactive request
→ user is waiting
→ optimize response latency

Offline batch
→ user does not need immediate output
→ optimize cost/throughput
```

Do not force an offline workload through an interactive endpoint if a proper batch mechanism exists.

{{exercise:M01.L10.EX02}}

---

## 3. Caching: reuse expensive work

Many GenAI operations are expensive.

Examples:

- model generation,
- semantic retrieval,
- parsing documents,
- computing embeddings,
- accessing external services.

If several requests ask for the same result, recomputing it wastes resources.

Caching changes:

```text
request
→ expensive computation
→ response
```

into:

```text
request
→ cache lookup

cache hit
→ return stored result

cache miss
→ compute
→ store
→ return
```

### Benefits

The source emphasizes:

- lower latency,
- lower server load,
- lower bandwidth usage,
- reduced operating cost.

### Staleness

Cached data can become outdated.

So every cache needs a freshness policy.

Ask:

```text
How long can this answer remain valid?
```

A public FAQ may tolerate a longer cache lifetime.

A highly personalized, frequently changing answer may require:

- short lifetime,
- active invalidation,
- no cache.

### Three cache categories in the chapter

1. keyword/exact caching,
2. semantic caching,
3. context/prompt caching.

These cache **different things** and should not be confused.

---

## 4. Keyword caching: exact input, exact key

Keyword caching is the simplest form.

Conceptually:

```text
key = exact input
value = cached result
```

Example:

```text
"What is FastAPI?"
→ cached answer
```

A different input:

```text
"Explain FastAPI."
```

may miss even if the intent is similar.

### Good use cases

- frequently repeated exact API calls,
- deterministic helper functions,
- stable endpoint results,
- repeated identical requests.

### FastAPI cache pattern

The source demonstrates initializing a shared cache during application lifespan.

Conceptually:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = ...
    initialize_cache(redis)
    yield
```

Then:

```python
@cache(expire=60)
async def expensive_operation(...):
    ...
```

### Why Redis?

If you have several application replicas:

```text
FastAPI A
FastAPI B
FastAPI C
```

local process memory is not shared.

A centralized Redis cache lets all instances access the same entries.

### Cache-Control headers

The source introduces common HTTP cache directives.

| Directive | Meaning |
|---|---|
| `max-age` | Response is fresh for a given duration |
| `no-cache` | Client should revalidate before reuse |
| `no-store` | Do not store response |
| `private` | Store only in a private cache such as a browser |

### Exact caching limitation

Keyword caching works best when repeated queries are literally the same.

Natural-language interfaces often generate many semantically equivalent phrasings.

That motivates semantic caching.

---

## 5. Semantic caching: cache by meaning

Semantic caching uses vector representations.

Instead of asking:

```text
Are these strings identical?
```

it asks:

```text
Are these queries semantically similar enough?
```

Example:

```text
How do you build generative services with FastAPI?

What is the process of developing FastAPI services for GenAI?
```

These are different strings but similar intents.

### Pipeline

```text
New query
   ↓
embedding model
   ↓
query vector
   ↓
search cache vectors
   ↓
similar enough?
   ├── yes → cache hit
   └── no  → perform expensive operation
                ↓
            cache result
```

[[IMAGE_NEEDED: Keyword versus semantic cache | Side-by-side flow: keyword cache compares exact text keys, semantic cache embeds queries and compares vectors; show two differently worded but equivalent questions missing exact cache yet hitting semantic cache | Learner should notice that semantic caching uses meaning rather than exact wording]]

### Why it can save substantial work

A Q&A system may repeatedly receive variations of the same questions.

A semantic cache can avoid repeated:

- vector-store search,
- document retrieval,
- model generation.

### But semantic similarity is not task equivalence

This is the most important risk.

Consider:

```text
Summarize this text in 100 words.

Summarize this text in 50 words.
```

The queries are semantically close.

But returning the same cached output violates one request.

Therefore:

> **Semantic similarity does not automatically mean the cached result is reusable.**

This is why the source chooses to demonstrate a semantic cache for **retrieved RAG documents**, rather than blindly caching final model responses in every case.

{{exercise:M01.L10.EX03}}

---

## 6. Place semantic caching inside a RAG pipeline

The chapter identifies two useful cache locations.

### Option A — before the LLM

```text
query
→ semantic response cache
→ cached final answer?
```

Potential benefit:

- skips both retrieval and generation.

Risk:

- similar questions may require different outputs.

### Option B — before the vector store

```text
query
→ semantic retrieval cache
→ cached relevant documents?
```

Potential benefit:

- skips repeated vector-store searches,
- still allows the model to generate a fresh response.

The source implements the second approach.

### Architecture

```text
User query
   ↓
query embedding
   ↓
semantic cache
   ├── hit → cached documents
   │
   └── miss
         ↓
      vector DB
         ↓
      relevant documents
         ↓
      insert documents into cache
         ↓
LLM receives context
```

[[IMAGE_NEEDED: Semantic cache in RAG | Diagram showing user query → embedding → semantic cache; cache hit returns documents directly, cache miss queries document vector store and stores retrieved documents in cache before prompt augmentation and LLM generation | Learner should notice that this cache avoids repeated retrieval while preserving fresh generation]]

### Cache-client responsibilities

The source's custom cache holds:

- query vector,
- cached document payload.

Operations:

```text
initialize
insert
search
```

### Document-store responsibilities

The vector store contains actual indexed knowledge.

Operations:

```text
initialize documents
search query vector
return top documents
```

### Semantic-cache service

The orchestration layer:

1. embeds query,
2. searches cache,
3. checks distance/threshold,
4. returns cached documents on hit,
5. otherwise searches document store,
6. stores retrieved documents in cache,
7. returns documents.

This is a clean example of combining:

- embeddings,
- vector search,
- cache policy,
- async database calls.

---

## 7. Tune semantic-cache thresholds

A semantic cache needs a decision boundary.

The cache asks:

```text
Is this new query similar enough to reuse the stored value?
```

The answer depends on the similarity/distance metric.

In the source's Euclidean-distance example:

```text
smaller distance
→ more similar

distance <= chosen threshold
→ cache hit
```

Other libraries may expose a similarity score with the opposite direction.

So always understand the metric before setting the threshold.

### Threshold too permissive

Unrelated or meaningfully different queries may hit the same cache entry.

Result:

- wrong answer,
- ignored user constraints,
- stale-looking behavior.

### Threshold too strict

Queries that are effectively equivalent may miss.

Result:

- lower cache hit rate,
- less cost/latency savings.

### Tune empirically

Collect representative queries.

For candidate thresholds, measure:

- hit rate,
- false-hit rate,
- latency,
- saved requests,
- output quality.

Do not select a semantic threshold only because a library default exists.

---

## 8. Cache eviction policies

Cache memory is finite.

Eventually, entries must be removed.

The chapter introduces several policies.

### FIFO — first in, first out

Remove the oldest entry.

Useful when all items have similar value.

### LRU — least recently used

Remove the item that has not been accessed for the longest time.

A common starting choice.

### LFU — least frequently used

Remove items with the lowest access count.

Useful when frequently accessed items should remain.

### MRU — most recently used

Remove the most recently accessed item.

Less common, but useful for special access patterns.

### Random replacement

Remove a random entry.

Simple and low-overhead.

### Choosing a policy

Ask:

```text
Does recent use predict future use?
Does frequency matter?
Are all entries equal?
How expensive is tracking metadata?
```

The source suggests LRU as a reasonable default starting point before testing alternatives.

{{exercise:M01.L10.EX04}}

---

## 9. Context/prompt caching: reuse large repeated prefixes

Prompt caching is different from output caching.

It does **not** mean:

```text
same prompt → same answer
```

Instead, it reuses work associated with a large repeated context.

Use case:

```text
huge system prompt/document corpus
       +
small new user question
```

Repeatedly processing the huge context is wasteful.

### Conceptual architecture

```text
Large reusable context
      ↓
provider/model computes reusable internal state
      ↓
cache
      ↓
Question A → reuse cached context
Question B → reuse cached context
Question C → reuse cached context
```

{{image:context-caching}}

### Suitable scenarios from the chapter

- long system instructions,
- long multiturn context,
- repeated analysis of large files,
- repeated queries against document sets,
- codebase analysis,
- long-form document summarization,
- many in-context examples.

### TTL

A cache may have a time-to-live.

```text
TTL
→ how long cached context remains available
```

Longer TTL:

- more reuse,
- more retained state/storage.

Shorter TTL:

- less staleness/state,
- fewer opportunities for reuse.

### Statefulness

The source warns that adopting provider-side context caching introduces statefulness across requests.

The provider may reuse content submitted previously.

That can matter for:

- privacy,
- retention,
- data lifecycle,
- architecture.

### Prompt caching does not cache output

Even if the same cached context and same question are reused, an LLM can produce a different response because generation is nondeterministic.

This distinction is essential.

---

## 10. Choose the right caching layer

Use this comparison:

| Cache | Key/trigger | Reuses | Main benefit | Main risk |
|---|---|---|---|---|
| Keyword | Exact request/input | Final result/function result | Simple, fast | Low hit rate for varied language |
| Semantic | Similar vector meaning | Response or retrieved context | Handles paraphrases | False semantic hits |
| Context/prompt | Repeated large input prefix/context | Provider/model input computation | Reduces repeated long-context work/cost | Stateful provider cache, TTL/privacy concerns |

### Example decisions

**FAQ endpoint with exact repeated questions**

```text
keyword cache
```

**RAG app with many paraphrased queries**

```text
semantic retrieval cache
```

**Book Q&A with the same 300-page context for many questions**

```text
prompt/context cache
```

### Cache invalidation remains central

A cache is useful only while its content is valid.

Every caching design should answer:

```text
When is the cache created?
When is it reused?
When does it expire?
When is it invalidated early?
What data must never be cached?
```

---

## 11. Model quantization: reduce numerical precision

When self-hosting large models, model weights consume substantial memory.

Quantization reduces the numerical precision used to represent model parameters and sometimes activations.

Conceptually:

```text
higher precision weights
       ↓
quantization/calibration
       ↓
lower precision representation
       ↓
smaller memory footprint
```

### Why lower precision helps

If one parameter uses fewer bits:

```text
less storage per parameter
→ lower RAM/VRAM usage
```

Lower-precision arithmetic may also improve certain operations and enable deployment on more constrained hardware.

### Example memory intuition

A 32-bit float uses:

```text
32 bits = 4 bytes
```

So approximately:

```text
1 billion FP32 parameters
→ about 4 GB just for raw weights
```

Training requires much more memory because it may also hold:

- gradients,
- optimizer states,
- activations,
- temporary buffers.

Inference is therefore much less memory-intensive than training.

[[IMAGE_NEEDED: Model quantization pipeline | Flow showing FP32/high-precision model weights → calibration/scaling/quantization → lower-precision INT8/INT4 model → inference, with memory footprint decreasing along the path | Learner should notice that quantization changes numeric representation rather than deleting model layers]]

---

## 12. Precision versus memory and quality

The chapter compares several numerical formats.

### FP32

High precision.

Large memory requirement.

### FP16

Uses half as many bits as FP32.

Can significantly reduce memory while often preserving useful quality.

### BF16

Uses 16 bits but preserves a broad exponent range.

The source presents it as another balance between memory and numerical behavior.

### INT8

Eight-bit integer representation.

Large memory savings.

The quality/performance result depends on the model and quantization method.

### INT4

Four-bit representation.

Even greater memory reduction.

Useful when aggressive compression is needed.

### Very low precision

Research continues on lower-bit models.

The lower the precision, the more carefully quality and hardware performance must be evaluated.

### Trade-off is empirical

Do not assume:

```text
fewer bits = always faster
```

The source notes that quantization can save memory yet sometimes reduce inference speed depending on implementation/hardware.

The correct evaluation is:

```text
memory
latency
throughput
quality
hardware compatibility
```

[[IMAGE_NEEDED: Precision ladder | Vertical ladder showing FP32 → FP16/BF16 → INT8 → INT4 → lower-bit formats, with memory decreasing downward and potential quantization error/quality risk increasing | Learner should notice the memory-versus-precision trade-off]]

{{exercise:M01.L10.EX05}}

---

## 13. Why lower precision changes memory use

The source briefly explains floating-point representation.

A floating-point value includes:

- sign,
- exponent,
- mantissa/fraction.

Conceptually:

```text
sign
→ positive/negative

exponent
→ scale/range

mantissa
→ precision
```

Moving from one format to another reduces or redistributes the available bits.

That changes:

- representable range,
- precision,
- memory footprint.

You do not need to memorize every bit layout for this course.

The important system insight is:

> **Model parameters are numbers. Changing how many bits are used to represent those numbers changes how much memory the model requires and can affect numerical accuracy.**

---

## 14. Quantize a pretrained model with GPTQ

The source introduces GPTQ as a post-training quantization technique for large language models.

High-level workflow:

```text
pretrained model
     ↓
calibration dataset
     ↓
quantization algorithm
     ↓
lower-bit model
     ↓
evaluate
     ↓
serve
```

### Calibration dataset

Quantization algorithms may use representative data to estimate how to map high-precision parameters into lower-precision representations.

### Example structure

Conceptually:

```python
quantizer = GPTQQuantizer(
    bits=4,
    dataset="c4",
    model_seqlen=2048,
)

quantized_model = quantizer.quantize_model(
    model,
    tokenizer,
)
```

The specific library API can change over time.

The durable lesson is:

- choose target bit width,
- use an appropriate calibration dataset,
- quantize the relevant model blocks,
- evaluate the result.

### Prefer prequantized models when appropriate

Quantization can itself require substantial GPU time.

The source recommends checking model repositories for compatible prequantized versions before doing the work yourself.

### Never skip evaluation

A model that fits into memory but loses unacceptable task quality is not an optimization.

---

## 15. Structured outputs: make model responses usable by software

Many GenAI systems do not display free-form prose directly.

Instead, the model participates in a pipeline.

Example:

```text
Document
   ↓
LLM extraction
   ↓
JSON
   ↓
database/API/business logic
```

If the model returns invalid structure:

```text
downstream parser fails
```

### Weak approach

Ask:

```text
"Return JSON."
```

Then manually parse text.

The model may still return:

- prose before JSON,
- malformed JSON,
- wrong fields,
- missing values.

### Better approach: schema-driven output

The source shows provider-supported structured output using a Pydantic schema.

Example:

```python
class DocumentClassification(BaseModel):
    category: str = Field(
        ...,
        description="Classification category",
    )
```

Then the schema is supplied to the model provider.

Conceptually:

```text
model request
+
output schema
      ↓
provider/model
      ↓
parsed structured result
```

[[IMAGE_NEEDED: Free-form JSON versus schema-driven structured output | Side-by-side pipeline where prompt-only JSON can produce malformed text and parser failure, while schema-driven output produces validated fields matching a Pydantic model | Learner should notice why structured output improves downstream reliability]]

### Fallback when native structured output is unavailable

The source also shows a prompt-based technique:

- specify exact JSON format,
- prefill the beginning of the assistant response,
- limit output length,
- parse returned JSON,
- catch decode failures.

This is less robust than true schema support but can improve behavior.

{{exercise:M01.L10.EX06}}

---

## 16. Prompt engineering as an optimization discipline

Prompt engineering is the practice of refining model instructions to improve useful outputs.

The chapter emphasizes a communication analogy.

Treat the model like:

```text
a knowledgeable colleague
+
limited knowledge of your exact local context
```

You must explain:

- what role it should play,
- what information matters,
- what task it should perform,
- what output you expect.

Vague request:

```text
"Analyze this."
```

Specific request:

```text
"Act as a document classifier. Using the policy below, assign exactly one category and return the result in the required schema."
```

The second gives the model a clearer target.

### Prompting can be tested

The source proposes treating prompt refinement more like software engineering.

Conceptually:

```text
prompt version 1
→ evaluate

prompt version 2
→ evaluate

prompt version 3
→ evaluate
```

Use representative test cases rather than choosing prompts only by intuition.

---

## 17. Role, Context, Task (RCT)

The chapter recommends a systematic prompt structure.

### Role

Who should the model behave like?

Example:

```text
You are a technical API reviewer.
```

A role changes expected perspective and behavior.

### Context

What information does the model need?

Example:

```text
Here are our API conventions.
Here is the relevant retrieved documentation.
```

RAG content often becomes part of context.

### Task

What exactly should the model do?

Example:

```text
Review the endpoint against the rules.
Return three violations and one recommendation.
```

### Template

```text
Role:
You are ...

Context:
...

Task:
...
```

[[IMAGE_NEEDED: Role-Context-Task prompt template | Three stacked blocks labeled Role, Context, Task feeding into the LLM, followed by a more precise output | Learner should notice that clear role, relevant context, and explicit task jointly reduce ambiguity]]

---

## 18. In-context learning: zero-shot and few-shot

One of the powerful properties of foundation models is adapting behavior from examples placed in the prompt.

### Zero-shot

No examples.

```text
Classify this document as A, B, or C.
```

Use when the task is already understood well enough.

### Few-shot

Provide several demonstrations.

```text
Input A → category 1
Input B → category 2
Input C → category 1

Now classify:
Input D
```

Useful when:

- labels are nuanced,
- output format matters,
- examples communicate intent better than prose.

### Dynamic few-shot

Examples are retrieved at runtime.

Pipeline:

```text
new input
    ↓
search example store/vector DB
    ↓
select relevant examples
    ↓
insert into prompt
    ↓
model
```

This can personalize or adapt examples to each query.

### In-context learning versus fine-tuning

In-context learning:

```text
changes prompt/context
does not modify model weights
```

Fine-tuning:

```text
changes model parameters
```

That distinction will matter later.

---

## 19. Thought-generation and decomposition prompts

The source groups several advanced prompting techniques around reasoning and task breakdown.

### Thought-generation family

The chapter discusses approaches such as:

- zero-shot chain-of-thought,
- few-shot chain-of-thought,
- thread-of-thought.

The general goal is to encourage a difficult problem to be handled in intermediate reasoning stages rather than through one immediate jump.

### Decomposition family

Break a hard task into smaller tasks.

The source introduces:

#### Least-to-most

```text
break problem into smaller subproblems
→ solve simpler parts
→ build toward final problem
```

#### Plan-and-solve

```text
create plan
→ execute plan
```

#### Tree of thoughts

```text
generate several possible branches
→ evaluate branches
→ continue promising branches
```

### When decomposition helps

- software design,
- complex analysis,
- multi-step planning,
- problems with several plausible paths.

### Trade-off

More steps can increase:

- model calls,
- tokens,
- latency,
- implementation complexity.

Use them when the quality improvement justifies the extra work.

---

## 20. Ensembling: use several candidate outputs

Ensembling generates multiple outputs and combines them.

The objective is to reduce response variance and improve reliability.

### Self-consistency

Generate several candidate reasoning paths/answers.

Then select the most consistent or common result.

### Mixture of reasoning experts (MoRE)

Use specialized prompts/models as different reviewers or experts.

Example:

```text
Expert A → factual review
Expert B → logical review
Expert C → domain review
      ↓
aggregate
```

### Demonstration ensembling

Use different few-shot example sets and aggregate the results.

### Prompt paraphrasing

Ask equivalent questions using several formulations.

Then compare/aggregate outputs.

### Cost trade-off

Ensembling deliberately performs more generation.

So:

```text
potential quality gain
↔
higher token/API cost
+
higher latency
```

Use it only when reliability matters enough to justify multiple calls.

{{exercise:M01.L10.EX07}}

---

## 21. Self-criticism and verification prompts

The chapter introduces several prompting strategies where a model evaluates or improves candidate output.

### Self-calibration

Ask for an assessment of a response's correctness/confidence.

### Self-refine

Pattern:

```text
generate draft
→ critique draft
→ improve draft
```

### Reversing chain-of-thought

Reconstruct the original problem from the generated answer and compare for inconsistencies.

### Self-verification

Generate candidate solutions, then evaluate them against modified/partial versions of the problem.

### Chain of verification

Pattern:

```text
answer
→ generate verification questions
→ answer verification questions
→ revise/select final answer
```

### Cumulative reasoning

Generate steps, evaluate whether each is useful, and continue until a satisfactory answer is reached.

### Engineering lesson

These methods turn one model call into a workflow.

That means you should measure:

- quality gain,
- latency,
- token usage,
- failure modes.

Do not assume an extra "judge" call always improves truthfulness.

---

## 22. Agentic prompting and tools

Agentic systems go beyond producing text.

They combine language models with external tools.

Conceptually:

```text
User goal
   ↓
LLM chooses action
   ↓
tool call
   ↓
observation
   ↓
LLM continues
   ↓
final result
```

The chapter introduces several agentic prompting patterns.

### MRKL

An LLM chooses among multiple external tools/modules.

### CRITIC

Generate a response, critique/check it, then use tools to verify or improve it.

### PAL

Generate code and execute it in a code interpreter to derive an answer.

### ToRA

Interleave reasoning and tool use over several steps.

### ReAct

Loop through:

```text
reason
→ act
→ observe
→ reason
→ act
→ observe
```

until the task is complete.

### Function/tool calling

The source demonstrates defining a tool schema:

```text
tool name
description
JSON parameters
required fields
```

The model can request that tool when appropriate.

### Security connection

Recall earlier lessons:

> **The model may propose a tool call, but trusted application logic must validate and authorize it before execution.**

Tool access increases capability and therefore increases the importance of:

- authorization,
- input validation,
- output validation,
- monitoring.

[[IMAGE_NEEDED: Agentic tool-calling loop | Diagram showing user → LLM → tool/function request → application validates/executes tool → observation returned to LLM → final answer, with an authorization/validation gate before execution | Learner should notice that the model proposes actions while application code controls actual tool execution]]

---

## 23. Fine-tuning: change model parameters

Prompting changes model inputs.

Fine-tuning changes model weights/parameters using training examples.

The source emphasizes:

> **Fine-tuning should usually not be your first optimization.**

Why?

It requires:

- dataset collection,
- data preparation,
- training jobs,
- evaluation,
- ongoing model/version management.

Prompt changes have a much faster feedback loop.

### Situations where fine-tuning may help

The chapter lists examples such as:

- specialized domain behavior,
- consistent tone or brand style,
- highly consistent output format,
- nuanced classification,
- handling edge cases,
- skills that are difficult to specify clearly in prompts,
- reducing large repeated prompt/example overhead,
- improving lower-cost model performance for a specific task,
- teaching patterns of tool/API use.

### Fine-tuning and knowledge

The source includes private-domain learning among possible motivations.

In practical system design, still distinguish:

```text
behavior/style adaptation
from
fresh retrievable knowledge
```

The chapter's central decision principle remains:

```text
try prompt/architecture optimizations first
then justify fine-tuning if needed
```

---

## 24. Fine-tuning workflow

The chapter presents three major steps.

### Step 1 — prepare training data

For a chat model, examples may be represented as conversations:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

Many examples are stored in a JSONL dataset.

### Step 2 — submit training job

Conceptually:

```text
training_data.jsonl
      ↓
upload
      ↓
file ID
      ↓
fine-tuning job
      ↓
provider training infrastructure
```

### Step 3 — evaluate and use the resulting model

After training:

```text
retrieve fine-tuned model identifier
    ↓
evaluate on held-out tests
    ↓
only then consider production
```

### Evaluation is mandatory

Fine-tuning changes model behavior.

Before deployment, evaluate:

- task quality,
- edge cases,
- regressions,
- safety,
- cost,
- latency.

### Versioning downside

The source warns that a fine-tuned model can lag behind improvements in newer foundation-model releases.

If the provider releases a substantially better base model, your fine-tuning investment may need to be repeated.

{{exercise:M01.L10.EX08}}

---

## 25. Choose the optimization that matches the bottleneck

Do not begin with:

```text
Which optimization technique is coolest?
```

Begin with:

```text
What metric is failing?
```

### If cost is high because requests repeat

Try:

- keyword caching,
- semantic caching,
- context caching.

### If offline workload is huge

Try:

- batch schemas,
- provider batch APIs.

### If a self-hosted model does not fit comfortably

Evaluate:

- smaller model,
- quantized model,
- external serving.

### If downstream parsing fails

Use:

- structured outputs,
- validation schemas.

### If the model misunderstands the task

Try:

1. clearer role/context/task,
2. zero-shot/few-shot experimentation,
3. decomposition,
4. verification/ensembling only where justified.

### If prompt engineering reaches a ceiling

Then evaluate whether fine-tuning is justified.

### Complete decision map

```text
Problem?
  │
  ├── repeated work
  │      └── cache
  │
  ├── large offline workload
  │      └── batch
  │
  ├── model too large
  │      └── quantize / smaller model
  │
  ├── invalid structured output
  │      └── structured output schema
  │
  ├── weak task alignment
  │      └── prompt engineering
  │
  └── persistent specialized behavior gap
         └── evaluate fine-tuning
```

### Measure before and after

For every optimization, record relevant metrics.

Possible performance metrics:

- p50/p95 latency,
- time to first token,
- throughput,
- cache hit rate,
- provider requests,
- tokens/request,
- GPU memory,
- cost/request.

Possible quality metrics:

- task accuracy,
- schema-validity rate,
- groundedness,
- human evaluation,
- domain-specific scores.

The optimization is successful only if the intended metric improves without an unacceptable regression elsewhere.

---

## Important misconceptions

### Misconception 1

> Optimization always means making the model faster.

### Why this is wrong

The chapter also optimizes cost, throughput, memory usage, response structure, alignment, and output quality.

### Misconception 2

> Batching is ideal for interactive chat.

### Why this is wrong

Batch jobs are especially useful for asynchronous/offline workloads where immediate response is unnecessary.

### Misconception 3

> A cache hit is always correct.

### Why this is wrong

Cached information can be stale, and semantic caches can match queries that are similar but require different outputs.

### Misconception 4

> Semantic caching requires exact text matches.

### Why this is wrong

It uses embeddings/similarity so differently worded queries can map to the same cached item.

### Misconception 5

> Prompt caching stores and reuses the generated answer.

### Why this is wrong

Prompt/context caching reuses repeated input/context computation. Model output can still vary.

### Misconception 6

> Cache entries should live forever once computed.

### Why this is wrong

Caches need TTL/invalidation and finite-capacity eviction policies.

### Misconception 7

> A more permissive semantic threshold always improves the cache.

### Why this is wrong

It may improve hit rate but can increase incorrect semantic matches.

### Misconception 8

> Quantization simply deletes unimportant model layers.

### Why this is wrong

Quantization changes how numerical parameters are represented, usually using fewer bits.

### Misconception 9

> Lower precision always guarantees faster inference.

### Why this is wrong

Memory savings are common, but actual speed depends on hardware, kernels, quantization method, and serving stack.

### Misconception 10

> If a quantized model fits into memory, no evaluation is needed.

### Why this is wrong

Compression can affect task quality and performance.

### Misconception 11

> Asking an LLM to "return JSON" guarantees valid structured output.

### Why this is wrong

Free-form generation can still violate the requested syntax or schema.

### Misconception 12

> A very long prompt is automatically a good prompt.

### Why this is wrong

Prompt quality comes from relevant context, explicit instructions, and useful examples—not length alone.

### Misconception 13

> Few-shot prompting modifies the model's weights.

### Why this is wrong

The examples live in the input context. The underlying model parameters remain unchanged.

### Misconception 14

> More reasoning/ensemble calls are free quality improvements.

### Why this is wrong

They consume additional tokens, time, and money and may still produce errors.

### Misconception 15

> Giving an LLM tools means it should be trusted to execute anything it proposes.

### Why this is wrong

Application logic must validate and authorize tool calls before execution.

### Misconception 16

> Fine-tuning should be the first response to mediocre model output.

### Why this is wrong

Prompt refinement and architecture changes have faster feedback loops and often solve the problem at lower cost.

### Misconception 17

> Once a model is fine-tuned, it will automatically benefit from every new base-model improvement.

### Why this is wrong

Fine-tuned versions can become tied to older base models and may require retraining/migration.

---

## Key terminology

| Term | Meaning |
|---|---|
| Optimization | Deliberate change intended to improve measured performance or quality |
| Batch processing | Processing many items together rather than one interactive request per item |
| Batch API | Provider service that queues and processes groups of requests asynchronously |
| JSONL | JSON Lines format with one JSON object per line |
| Cache | Store of reusable previously computed data/results |
| Cache hit | Requested item is found and reused |
| Cache miss | Requested item is not available and must be recomputed |
| Cache invalidation | Removing/expiring data that should no longer be reused |
| Keyword cache | Exact-input/key-based cache |
| Semantic cache | Cache lookup based on embedding similarity |
| Similarity threshold | Boundary used to decide whether a semantic cache lookup is close enough |
| Eviction policy | Rule deciding which cache item to remove when capacity is reached |
| FIFO | First in, first out eviction |
| LRU | Least recently used eviction |
| LFU | Least frequently used eviction |
| MRU | Most recently used eviction |
| Prompt/context cache | Cache of reusable large input context/model computation |
| TTL | Time to live before cached data expires |
| Quantization | Reducing numerical precision of model parameters/activations |
| FP32 | 32-bit floating-point format |
| FP16 | 16-bit floating-point format |
| BF16 | 16-bit brain floating-point format |
| INT8 | 8-bit integer representation |
| INT4 | 4-bit integer representation |
| Calibration | Using representative data to guide quantization mapping |
| GPTQ | Post-training quantization approach introduced in the chapter |
| Structured output | Model response constrained to a declared schema/format |
| Prompt engineering | Systematic design/refinement of model instructions |
| RCT | Role, Context, Task prompt structure |
| Zero-shot | Task instruction without examples |
| Few-shot | Task instruction with a small set of examples |
| Dynamic few-shot | Runtime retrieval/injection of relevant examples |
| In-context learning | Adapting behavior from information/examples inside the prompt |
| Decomposition | Breaking a complex problem into smaller tasks |
| Ensembling | Combining multiple model outputs |
| Self-consistency | Generating several candidates and selecting a consistent result |
| Self-refine | Iteratively critique and improve a response |
| Agentic system | LLM workflow that can plan/use external tools/actions |
| Function calling | Structured mechanism for an LLM to request an application-defined tool |
| Fine-tuning | Updating model parameters using task/domain training examples |

---

## Self-check

Before continuing, make sure you can answer:

1. What are the two broad optimization goals in the chapter?
2. Which techniques mainly target performance?
3. Which techniques mainly target quality?
4. Why should optimization begin with a measurable bottleneck?
5. Why can one API call per offline item be inefficient?
6. What are the chapter's two batching strategies?
7. What role does JSONL play in provider batch APIs?
8. Why are batch APIs better suited to offline jobs than interactive chat?
9. What three main benefits does caching provide?
10. Why does every cache need a freshness/invalidation policy?
11. What is keyword caching?
12. Why can Redis help with caching across multiple FastAPI instances?
13. What does `max-age` mean?
14. What does `no-store` mean?
15. Why does exact keyword caching have limited value for varied natural-language questions?
16. What is semantic caching?
17. Why can paraphrased questions hit the same semantic cache entry?
18. Why can semantic caching final LLM answers be dangerous?
19. Why does the chapter cache RAG documents rather than every final response?
20. Where are the two possible semantic-cache locations in a RAG system?
21. What does the custom semantic-cache service do on a cache miss?
22. In a Euclidean-distance cache, does a lower or higher distance indicate stronger similarity?
23. What happens if a similarity threshold is too permissive?
24. What happens if it is too strict?
25. Why should thresholds be tuned using real queries?
26. What does FIFO evict?
27. What does LRU evict?
28. What does LFU evict?
29. Why is LRU a reasonable first policy to try?
30. How is prompt/context caching different from response caching?
31. Which applications benefit from repeated large-context caching?
32. What is TTL?
33. Why does prompt caching make requests stateful?
34. Why can the same cached context still produce different model outputs?
35. What does quantization change in a model?
36. Why does fewer bits per parameter reduce memory?
37. Approximately how many bytes does FP32 use per parameter?
38. Why does training need more memory than inference?
39. How do FP16 and INT8 differ conceptually?
40. Why is lower precision not automatically better?
41. Why should a quantized model always be evaluated?
42. What is calibration data used for in a quantization workflow?
43. What does GPTQ do at a high level?
44. Why should you check for prequantized models before quantizing one yourself?
45. Why are structured outputs important in data pipelines?
46. Why can "return JSON" fail?
47. What role does Pydantic play in structured output?
48. What can be done when native structured outputs are unavailable?
49. What is prompt engineering?
50. What are Role, Context, and Task?
51. Why can RAG content be part of prompt context?
52. What is zero-shot prompting?
53. What is few-shot prompting?
54. What is dynamic few-shot prompting?
55. How does in-context learning differ from fine-tuning?
56. What is the purpose of decomposition prompting?
57. What is plan-and-solve?
58. What is tree-of-thought-style decomposition intended to explore?
59. What is ensembling?
60. What trade-off does self-consistency introduce?
61. What is the idea behind mixture-of-reasoning-experts?
62. What does self-refine do?
63. What is chain of verification intended to achieve?
64. What makes an LLM workflow agentic?
65. What role do tools play in MRKL/ReAct/PAL-style workflows?
66. Why must application code validate tool calls?
67. What is fine-tuning?
68. Why does the source recommend avoiding fine-tuning when prompt engineering is sufficient?
69. When might fine-tuning become justified?
70. What are the three broad stages of a fine-tuning workflow?
71. Why must a fine-tuned model be evaluated before production?
72. What is one downside of fine-tuning when newer base models are released?
73. Which technique would you choose for repeated exact requests?
74. Which technique would you choose for paraphrased RAG retrieval queries?
75. Which technique would you choose for a repeated 200-page context?
76. Which technique would you choose if a local model barely fits into GPU memory?
77. Which technique would you choose if your model frequently returns malformed JSON?
78. Which technique should you try before fine-tuning when task instructions are vague?
79. Which metrics would you measure before and after a performance optimization?
80. Why is an optimization unsuccessful if one metric improves but an unacceptable regression appears elsewhere?

---

## Retain this idea

**Optimize the bottleneck you actually have: batch work that does not need immediate answers, cache repeated computation at the right layer, quantize self-hosted models when memory is the constraint, use schemas and systematic prompting when output quality or structure is weak, and reserve fine-tuning for persistent behavior gaps that cheaper and faster techniques cannot solve. Every optimization should be measured against latency, throughput, cost, memory, and quality—not adopted just because it is available.**
""",

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "optimization-objectives", "title": "Start by identifying what you are optimizing", "order": 1},
            {"id": "batch-processing", "title": "Batch processing: stop sending one request per item", "order": 2},
            {"id": "cache-foundations", "title": "Caching: reuse expensive work", "order": 3},
            {"id": "keyword-cache", "title": "Keyword caching: exact input, exact key", "order": 4},
            {"id": "semantic-cache", "title": "Semantic caching: cache by meaning", "order": 5},
            {"id": "rag-semantic-cache", "title": "Place semantic caching inside a RAG pipeline", "order": 6},
            {"id": "semantic-threshold", "title": "Tune semantic-cache thresholds", "order": 7},
            {"id": "cache-eviction", "title": "Cache eviction policies", "order": 8},
            {"id": "prompt-cache", "title": "Context/prompt caching: reuse large repeated prefixes", "order": 9},
            {"id": "cache-selection", "title": "Choose the right caching layer", "order": 10},
            {"id": "quantization", "title": "Model quantization: reduce numerical precision", "order": 11},
            {"id": "precision-tradeoff", "title": "Precision versus memory and quality", "order": 12},
            {"id": "floating-point", "title": "Why lower precision changes memory use", "order": 13},
            {"id": "gptq", "title": "Quantize a pretrained model with GPTQ", "order": 14},
            {"id": "structured-outputs", "title": "Structured outputs: make model responses usable by software", "order": 15},
            {"id": "prompt-engineering", "title": "Prompt engineering as an optimization discipline", "order": 16},
            {"id": "rct-template", "title": "Role, Context, Task (RCT)", "order": 17},
            {"id": "in-context-learning", "title": "In-context learning: zero-shot and few-shot", "order": 18},
            {"id": "thought-and-decomposition", "title": "Thought-generation and decomposition prompts", "order": 19},
            {"id": "ensembling", "title": "Ensembling: use several candidate outputs", "order": 20},
            {"id": "self-criticism", "title": "Self-criticism and verification prompts", "order": 21},
            {"id": "agentic-prompting", "title": "Agentic prompting and tools", "order": 22},
            {"id": "fine-tuning", "title": "Fine-tuning: change model parameters", "order": 23},
            {"id": "fine-tuning-workflow", "title": "Fine-tuning workflow", "order": 24},
            {"id": "optimization-decision-framework", "title": "Choose the optimization that matches the bottleneck", "order": 25},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L10.EX01",
            "title": "Diagnose the Optimization Bottleneck",
            "lesson_code": "M01.L10",
            "section_id": "optimization-objectives",
            "placement": "after_section",
            "description": (
                "Choose an optimization target before selecting a technique."
            ),
            "instructions": (
                "For each symptom, identify the primary target metric and one chapter technique to investigate:\n\n"
                "1. Thousands of document-classification items must be processed overnight.\n"
                "2. The same FAQ questions trigger repeated paid LLM calls.\n"
                "3. A self-hosted model barely fits in available VRAM.\n"
                "4. The model often returns malformed JSON to a downstream service.\n"
                "5. A repeated 100-page context dominates input token costs.\n"
                "6. The task requires a specialized style that prompt iteration has not solved.\n\n"
                "Classify each as mainly latency, throughput, cost, memory, structure/reliability, or output-quality optimization."
            ),
            "expected_output": (
                "A six-row bottleneck → metric → candidate optimization table."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "optimization-diagnosis",
                "systems-tradeoffs",
                "technique-selection",
            ],
        },
        {
            "id": "M01.L10.EX02",
            "title": "Design an Offline Batch Classification Job",
            "lesson_code": "M01.L10",
            "section_id": "batch-processing",
            "placement": "after_section",
            "description": (
                "Convert a one-request-per-item workload into an asynchronous batch workflow."
            ),
            "instructions": (
                "You have 20,000 product descriptions to classify overnight.\n\n"
                "Design the workflow:\n"
                "1. define a structured classification output,\n"
                "2. assign each input a `custom_id`,\n"
                "3. write requests to JSONL,\n"
                "4. upload the file,\n"
                "5. submit the provider batch job,\n"
                "6. store the returned batch ID,\n"
                "7. poll/retrieve job status,\n"
                "8. match returned results to original records.\n\n"
                "Explain why this is preferable to keeping 20,000 interactive requests open."
            ),
            "expected_output": (
                "A batch-job architecture and a short cost/throughput explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "batch-processing",
                "jsonl",
                "offline-ai-workloads",
            ],
        },
        {
            "id": "M01.L10.EX03",
            "title": "Detect a Dangerous Semantic Cache Hit",
            "lesson_code": "M01.L10",
            "section_id": "semantic-cache",
            "placement": "after_section",
            "description": (
                "Learn that similar wording does not always imply reusable outputs."
            ),
            "instructions": (
                "Consider these pairs:\n\n"
                "A. `How do I build a FastAPI GenAI service?`\n"
                "   `What is the process for building GenAI services with FastAPI?`\n\n"
                "B. `Summarize this article in 100 words.`\n"
                "   `Summarize this article in 50 words.`\n\n"
                "C. `Show orders from the last 7 days.`\n"
                "   `Show orders from the last 30 days.`\n\n"
                "For each pair:\n"
                "1. judge whether semantic similarity is likely high,\n"
                "2. decide whether reusing the exact final cached response is safe,\n"
                "3. explain whether caching retrieved context instead would be safer."
            ),
            "expected_output": (
                "A three-pair semantic-cache safety analysis."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "semantic-caching",
                "cache-correctness",
                "rag-cache-design",
            ],
        },
        {
            "id": "M01.L10.EX04",
            "title": "Tune a Semantic Cache",
            "lesson_code": "M01.L10",
            "section_id": "cache-eviction",
            "placement": "after_section",
            "description": (
                "Design a measurable threshold and eviction experiment."
            ),
            "instructions": (
                "You have a semantic cache using Euclidean distance.\n\n"
                "1. Explain whether smaller or larger distance indicates a closer match.\n"
                "2. Test conceptually three thresholds: strict, medium, permissive.\n"
                "3. State how each affects hit rate and false-hit risk.\n"
                "4. Choose one metric set you would record in production.\n"
                "5. If the cache capacity is 10,000 items, choose FIFO, LRU, LFU, MRU, or random replacement and justify the choice for an FAQ workload."
            ),
            "expected_output": (
                "A threshold experiment plan, metrics, and an eviction-policy decision."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "cache-thresholds",
                "cache-metrics",
                "eviction-policy",
            ],
        },
        {
            "id": "M01.L10.EX05",
            "title": "Estimate Quantized Weight Memory",
            "lesson_code": "M01.L10",
            "section_id": "precision-tradeoff",
            "placement": "after_section",
            "description": (
                "Build intuition for how parameter precision changes raw model-weight memory."
            ),
            "instructions": (
                "Assume a model has 2 billion parameters and ignore runtime overhead.\n\n"
                "Estimate raw weight memory for:\n"
                "1. FP32 (4 bytes/parameter),\n"
                "2. FP16 (2 bytes/parameter),\n"
                "3. INT8 (1 byte/parameter),\n"
                "4. INT4 (0.5 byte/parameter).\n\n"
                "Then answer:\n"
                "- Which format gives the largest memory reduction?\n"
                "- Why can you not select the lowest precision only from memory numbers?\n"
                "- What additional measurements are required before deployment?"
            ),
            "expected_output": (
                "Four approximate memory calculations and a quality/performance evaluation explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "quantization",
                "memory-estimation",
                "precision-tradeoffs",
            ],
        },
        {
            "id": "M01.L10.EX06",
            "title": "Replace Prompt-Only JSON with a Schema",
            "lesson_code": "M01.L10",
            "section_id": "structured-outputs",
            "placement": "after_section",
            "description": (
                "Improve reliability of a model used inside a software pipeline."
            ),
            "instructions": (
                "You need to classify documents into `category`, `confidence`, and `reason`.\n\n"
                "1. Define a Pydantic output model.\n"
                "2. Add one sensible constraint to `confidence`.\n"
                "3. Show how that model would be passed conceptually as a provider structured-output schema.\n"
                "4. Describe the fallback if the provider has no native schema support.\n"
                "5. Explain why regex extraction from arbitrary prose is weaker."
            ),
            "expected_output": (
                "A Pydantic schema and a native-versus-fallback structured-output design."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "structured-output",
                "pydantic",
                "llm-pipeline-reliability",
            ],
        },
        {
            "id": "M01.L10.EX07",
            "title": "Choose a Prompting Strategy",
            "lesson_code": "M01.L10",
            "section_id": "ensembling",
            "placement": "after_section",
            "description": (
                "Select prompt techniques based on task complexity and cost constraints."
            ),
            "instructions": (
                "Choose a primary technique for each scenario:\n\n"
                "1. Simple summarization the base model already handles well.\n"
                "2. Nuanced classification with five labeled examples available.\n"
                "3. A difficult planning problem that should be broken into subtasks first.\n"
                "4. A high-value answer where several candidate outputs can be compared.\n"
                "5. A draft that should be critiqued and improved iteratively.\n"
                "6. A support assistant that must call an approved retrieval tool.\n\n"
                "Use zero-shot, few-shot, decomposition, ensembling, self-refine, or agentic tool calling. "
                "For each, explain the cost/complexity trade-off."
            ),
            "expected_output": (
                "Six prompting-strategy selections with reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "prompt-engineering",
                "few-shot",
                "decomposition",
                "ensembling",
                "agentic-tools",
            ],
        },
        {
            "id": "M01.L10.EX08",
            "title": "Decide Whether to Fine-Tune",
            "lesson_code": "M01.L10",
            "section_id": "fine-tuning-workflow",
            "placement": "after_section",
            "description": (
                "Decide whether a persistent quality problem justifies weight adaptation."
            ),
            "instructions": (
                "Evaluate these scenarios:\n\n"
                "A. The system prompt is vague and has not been systematically improved.\n"
                "B. A small model must follow a company-specific report style across millions of requests, and you have high-quality examples.\n"
                "C. The application needs fresh policy documents that change every week.\n"
                "D. A 200-class domain classifier remains unreliable after careful prompting and you have a large labeled dataset.\n\n"
                "For each, choose one of:\n"
                "- improve prompt,\n"
                "- use retrieval/context,\n"
                "- consider fine-tuning.\n\n"
                "For any fine-tuning choice, list the required data, evaluation, and deployment steps."
            ),
            "expected_output": (
                "Four optimization decisions plus a fine-tuning checklist where applicable."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "fine-tuning-decision",
                "rag-vs-fine-tuning",
                "model-optimization",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L10.QZ01",

        "title": "Optimizing AI Services — Knowledge Check",

        "lesson_code": "M01.L10",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L10.Q01",
                "section_id": "optimization-objectives",
                "question": "Which technique is primarily a performance optimization in the chapter?",
                "options": [
                    "Caching",
                    "Fine-tuning only",
                    "Role prompting only",
                    "Self-criticism only",
                ],
                "correct": 0,
                "explanation": (
                    "Caching avoids repeated expensive work and can improve latency, load, and operating cost."
                ),
            },
            {
                "id": "M01.L10.Q02",
                "section_id": "batch-processing",
                "question": "When is a provider batch API especially appropriate?",
                "options": [
                    "Large offline jobs that do not require an immediate response",
                    "Every single interactive chatbot token",
                    "WebSocket ping messages",
                    "Login password verification",
                ],
                "correct": 0,
                "explanation": (
                    "Batch APIs are designed for groups of requests that can be processed asynchronously."
                ),
            },
            {
                "id": "M01.L10.Q03",
                "section_id": "semantic-cache",
                "question": "What makes semantic caching different from keyword caching?",
                "options": [
                    "It can reuse results based on vector similarity rather than exact input equality",
                    "It never needs a cache key",
                    "It modifies model weights",
                    "It can only store images",
                ],
                "correct": 0,
                "explanation": (
                    "Semantic caches embed inputs and compare their meaning, enabling paraphrased queries to match."
                ),
            },
            {
                "id": "M01.L10.Q04",
                "section_id": "semantic-threshold",
                "question": "In the lesson's Euclidean-distance cache example, what indicates a closer semantic match?",
                "options": [
                    "A smaller distance",
                    "A larger distance",
                    "A longer query",
                    "A larger cache capacity",
                ],
                "correct": 0,
                "explanation": (
                    "With Euclidean distance, smaller distance means the vectors are closer."
                ),
            },
            {
                "id": "M01.L10.Q05",
                "section_id": "prompt-cache",
                "question": "What does prompt/context caching primarily reuse?",
                "options": [
                    "Computation/state associated with large repeated input context",
                    "Only final generated answers",
                    "User passwords",
                    "Database migrations",
                ],
                "correct": 0,
                "explanation": (
                    "Prompt caching avoids recomputing repeated large input context; it does not guarantee identical outputs."
                ),
            },
            {
                "id": "M01.L10.Q06",
                "section_id": "quantization",
                "question": "What does model quantization primarily change?",
                "options": [
                    "The numerical precision used to represent model parameters/activations",
                    "The number of API routes in FastAPI",
                    "The number of training documents",
                    "The user's authentication role",
                ],
                "correct": 0,
                "explanation": (
                    "Quantization compresses numeric representations to reduce memory and potentially improve deployment efficiency."
                ),
            },
            {
                "id": "M01.L10.Q07",
                "section_id": "precision-tradeoff",
                "question": "Why should the lowest-bit model not be selected automatically?",
                "options": [
                    "Memory savings may come with quality, compatibility, or speed trade-offs",
                    "Low-bit models cannot perform inference",
                    "Quantization always increases memory",
                    "INT formats cannot represent any values",
                ],
                "correct": 0,
                "explanation": (
                    "Deployment must evaluate quality and actual hardware performance in addition to memory."
                ),
            },
            {
                "id": "M01.L10.Q08",
                "section_id": "structured-outputs",
                "question": "Why are schema-driven structured outputs useful?",
                "options": [
                    "They improve reliability when downstream software expects a specific structure",
                    "They eliminate every model hallucination",
                    "They replace authentication",
                    "They automatically fine-tune the model",
                ],
                "correct": 0,
                "explanation": (
                    "Downstream systems can work with validated fields instead of trying to parse arbitrary prose."
                ),
            },
            {
                "id": "M01.L10.Q09",
                "section_id": "rct-template",
                "question": "What does RCT stand for in the chapter's prompt template?",
                "options": [
                    "Role, Context, Task",
                    "Rate, Cache, Throughput",
                    "Request, Connection, Token",
                    "Retrieval, Classification, Training",
                ],
                "correct": 0,
                "explanation": (
                    "The RCT template structures prompts around the role, relevant context, and explicit task."
                ),
            },
            {
                "id": "M01.L10.Q10",
                "section_id": "in-context-learning",
                "question": "What is few-shot prompting?",
                "options": [
                    "Supplying a small number of examples in the prompt",
                    "Training the model for a few gradient steps",
                    "Calling several different databases",
                    "Quantizing to a few bits",
                ],
                "correct": 0,
                "explanation": (
                    "Few-shot prompting provides examples inside the model context without updating model weights."
                ),
            },
            {
                "id": "M01.L10.Q11",
                "section_id": "ensembling",
                "question": "What is the main trade-off of ensembling?",
                "options": [
                    "Potentially improved reliability in exchange for more model calls, latency, and cost",
                    "Lower memory with no additional calls",
                    "No need to evaluate outputs",
                    "It permanently changes model weights",
                ],
                "correct": 0,
                "explanation": (
                    "Ensembling generates multiple candidates or expert outputs, so quality improvements cost additional inference."
                ),
            },
            {
                "id": "M01.L10.Q12",
                "section_id": "agentic-prompting",
                "question": "What turns a basic LLM workflow into an agentic workflow in this chapter?",
                "options": [
                    "The model can plan/select and use external tools or actions through an application-controlled loop",
                    "The prompt is longer than 1,000 tokens",
                    "The model uses a cache",
                    "The response is JSON",
                ],
                "correct": 0,
                "explanation": (
                    "Agentic systems combine model reasoning/selection with tools, actions, observations, and repeated interaction."
                ),
            },
            {
                "id": "M01.L10.Q13",
                "section_id": "fine-tuning",
                "question": "Why does the source recommend trying prompt engineering before fine-tuning?",
                "options": [
                    "Prompt iteration is faster and cheaper than building datasets and running training jobs",
                    "Fine-tuning cannot change model behavior",
                    "Prompt engineering modifies weights more accurately",
                    "Fine-tuning requires no evaluation",
                ],
                "correct": 0,
                "explanation": (
                    "Prompting has a much faster feedback loop and often solves quality problems without training."
                ),
            },
            {
                "id": "M01.L10.Q14",
                "section_id": "fine-tuning-workflow",
                "question": "What should happen before a fine-tuned model is deployed to production?",
                "options": [
                    "Evaluate it on representative tests and compare quality/safety/performance",
                    "Delete the training dataset immediately and skip testing",
                    "Remove every system prompt",
                    "Disable structured outputs",
                ],
                "correct": 0,
                "explanation": (
                    "Fine-tuning changes model behavior, so systematic evaluation is required before production use."
                ),
            },
            {
                "id": "M01.L10.Q15",
                "section_id": "optimization-decision-framework",
                "type": "open",
                "question": (
                    "A GenAI service has four problems: repeated FAQ costs, a self-hosted model that barely fits GPU memory, "
                    "occasional malformed JSON, and an overnight job processing 100,000 records. "
                    "Choose the optimization technique you would apply to each problem, state the metric you expect to improve, "
                    "and name one trade-off or failure mode you would measure."
                ),
            },
        ],

        "passing_score": 70,
    },
}
