"""M01.L05 — Achieving Concurrency in AI Workloads.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 5, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Learn how to keep GenAI services responsive under multiple users by separating "
    "I/O-bound, compute-bound, and memory-bound work; applying async programming, "
    "threading, multiprocessing, external model serving, RAG concurrency, batching, "
    "paged attention, and background task patterns appropriately."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Achieving Concurrency in AI Workloads",

    "slug": "generative-ai-services-m01-l05",

    "description": (
        "Understand concurrency and parallelism in Python/FastAPI, avoid blocking the "
        "event loop, use asynchronous I/O for providers, web pages, files, and vector "
        "databases, build a simple RAG pipeline, externalize heavy model inference, "
        "and manage long-running AI jobs without making the application unresponsive."
    ),

    "order": 5,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "concurrency",
        "parallelism",
        "asyncio",
        "async-await",
        "fastapi",
        "thread-pool",
        "event-loop",
        "multiprocessing",
        "rag",
        "qdrant",
        "vector-search",
        "vllm",
        "continuous-batching",
        "paged-attention",
        "background-tasks",
        "genai-serving",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L04",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Achieving Concurrency in AI Workloads",

        "content": """
# Achieving Concurrency in AI Workloads

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L05  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 5 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Distinguish I/O-bound, compute-bound, and memory-bound operations.
- Explain the difference between concurrency and parallelism.
- Explain how Python's GIL affects multithreading.
- Choose among synchronous execution, async I/O, multithreading, and multiprocessing.
- Explain how `async`, `await`, coroutines, and the event loop work together.
- Use async provider clients without accidentally blocking FastAPI's main event loop.
- Explain how FastAPI uses the event loop and thread pool for async and sync handlers.
- Recognize common async-programming mistakes that destroy concurrency.
- Build the mental model for an asynchronous web scraper.
- Explain the complete RAG ingestion and retrieval pipeline.
- Use asynchronous file I/O and an asynchronous vector-database client conceptually.
- Explain why heavy self-hosted inference should often be externalized from the main FastAPI process.
- Distinguish latency from throughput in model serving.
- Explain KV caching, request batching, continuous batching, and paged attention at a practical level.
- Explain when FastAPI background tasks are useful and where their limits appear.
- Identify when a dedicated task queue or specialized model-serving framework is more appropriate.

---

## 1. Why AI services become blocked

A single-user demo can hide an important production problem.

Suppose one request arrives:

```text
User A
  ↓
FastAPI
  ↓
model inference
  ↓
response
```

If inference takes five seconds, the user waits five seconds.

That may be acceptable.

Now imagine many users:

```text
User A ─┐
User B ─┼→ same service
User C ─┤
User D ─┘
```

If the service cannot make progress on overlapping work, requests begin waiting behind each other.

The chapter classifies blocking operations into two main groups.

### I/O-bound operations

The program is waiting for data to move in or out.

Examples include:

- reading or writing files,
- network requests,
- external API calls,
- database queries,
- waiting for user input.

The CPU may have very little useful work to do while it waits.

### Compute-bound operations

The program is busy performing expensive calculations.

Examples include:

- AI model inference,
- training,
- large data transformations,
- simulation,
- 3D rendering.

Here the CPU or GPU is actively occupied.

### A third practical category: memory-bound model serving

Later in the chapter, the source explains that large-model serving can also become **memory-bound**.

The bottleneck can be moving huge model parameters and caches through GPU memory rather than arithmetic alone.

So for GenAI systems, a useful classification is:

```text
I/O-bound
→ waiting for data movement or external systems

Compute-bound
→ waiting for expensive calculation

Memory-bound
→ waiting on movement/access of large model state and caches
```

### Why the classification matters

The correct optimization depends on the bottleneck.

```text
I/O-bound
→ async I/O or threading

CPU-heavy compute
→ multiprocessing / separate workers

Large-model inference
→ specialized inference server + model optimizations

Long-running user job
→ background/queue workflow
```

Do not apply `async` simply because something is slow.

First determine **why** it is slow.

---

## 2. Concurrency versus parallelism

These words are related, but they are not identical.

### Concurrency

Concurrency means multiple tasks make progress during overlapping periods.

They do not have to execute at the exact same instant.

Imagine one worker handling several tasks:

```text
time ───────────────────────────→

Task A: ███ wait      ███
Task B:     ███ wait      ███
Task C:         ███ wait
```

The worker switches to another task when one task is waiting.

### Parallelism

Parallelism means tasks actually execute simultaneously on separate compute resources.

```text
CPU core 1: Task A █████████
CPU core 2: Task B █████████
CPU core 3: Task C █████████
```

### Restaurant analogy

The source uses a useful analogy.

**Concurrency:**

One person:

```text
take order
→ start cooking
→ while food cooks, take another order
→ return to cooking
```

**Parallelism:**

Several workers:

```text
worker 1 → takes orders
worker 2 → cooks
worker 3 → prepares drinks
```

Work truly happens at the same time.

{{image:concurrency-vs-parallelism}}

### Why GenAI services need both concepts

A service may simultaneously use:

```text
async concurrency
→ waiting on databases and APIs

parallel workers
→ CPU-heavy preprocessing

specialized GPU server
→ parallelized model inference
```

Large systems often combine these strategies rather than selecting only one.

{{exercise:M01.L05.EX01}}

---

## 3. The GIL, threads, and processes

### Threads

A **thread** is an execution flow within a process.

Threads in the same process share memory.

That makes communication convenient, but shared memory introduces concerns such as:

- race conditions,
- deadlocks,
- resource contention,
- thread safety.

### Python's GIL

The chapter introduces the **Global Interpreter Lock (GIL)**.

In the conventional Python runtime discussed in the source, the GIL means only one thread at a time executes Python bytecode within one process.

So threads do not automatically give you true CPU parallelism.

However, threading can still help I/O-heavy workloads.

Why?

While one thread waits for I/O, another can make progress.

### Multiprocessing

A **process** has its own isolated memory space.

With several processes on several CPU cores, tasks can execute in parallel.

```text
Process 1 → CPU core 1
Process 2 → CPU core 2
Process 3 → CPU core 3
```

This is useful for compute-heavy work.

But isolation has a cost.

Processes cannot casually share arbitrary in-memory objects.

### Why this becomes painful with large AI models

Suppose one model occupies a huge amount of memory.

If four worker processes each load their own copy:

```text
worker 1 → model copy
worker 2 → model copy
worker 3 → model copy
worker 4 → model copy
```

memory usage can become enormous.

That is why simply adding more FastAPI worker processes is not always a good way to scale large self-hosted models.

### Threading versus multiprocessing

| Property | Threads | Processes |
|---|---|---|
| Memory | Shared within process | Isolated |
| Python CPU parallelism | Limited by GIL in the chapter's model | Can use multiple cores |
| Communication | Easier | More complex |
| Best fit here | I/O waits / sync compatibility | CPU-heavy parallel work |
| AI-model concern | Shared state can be tricky | Large model may be duplicated |

### Core lesson

> **The way you scale ordinary web work is not automatically the way you should scale a large model.**

Heavy models often need specialized serving infrastructure.

---

## 4. Choose the concurrency strategy from the workload

The chapter compares four broad execution styles.

### No concurrency

Simple sequential code.

```text
Task A
  ↓
Task B
  ↓
Task C
```

Advantages:

- simple,
- predictable,
- easy to debug.

Disadvantage:

- every blocking operation delays everything after it.

Good for:

- tiny tools,
- infrequent tasks,
- single-user flows where waiting is acceptable.

### Async I/O

One event loop manages many tasks.

Good for:

- APIs,
- database calls,
- async file I/O,
- web scraping,
- provider model APIs.

Main requirement:

> Every operation inside the async path must cooperate by being nonblocking.

### Multithreading

Several threads in one process.

Useful when:

- you have blocking synchronous I/O libraries,
- replacing the library with async is impractical,
- the framework can move sync work to a thread pool.

Trade-offs include:

- thread overhead,
- race conditions,
- deadlocks,
- shared-state complexity.

### Multiprocessing

Several isolated processes.

Useful for:

- compute-heavy CPU work,
- independent chunks of processing,
- workload distribution across CPU cores.

Trade-offs:

- process startup cost,
- isolated memory,
- inter-process communication complexity,
- model duplication if each worker loads a large model.

### Decision shortcut

Ask:

```text
Is the task mostly waiting?
→ use async if the library supports it

Is it sync I/O that cannot be replaced?
→ thread pool can help

Is it CPU-heavy?
→ processes may help

Is it large-model GPU inference?
→ external specialized model serving may be better
```

---

## 5. Synchronous versus asynchronous execution

The chapter uses sleeping to demonstrate the difference between blocking and nonblocking waits.

### Synchronous version

```python
import time


def task():
    print("start")
    time.sleep(5)
    print("done")


for _ in range(3):
    task()
```

Conceptually:

```text
task 1 waits 5 s
task 2 waits 5 s
task 3 waits 5 s

total ≈ 15 s
```

### Async version

```python
import asyncio


async def task():
    print("start")
    await asyncio.sleep(5)
    print("done")


async def main():
    await asyncio.gather(
        task(),
        task(),
        task(),
    )


asyncio.run(main())
```

Now the three waits overlap.

```text
task 1 ─ wait ─┐
task 2 ─ wait ─┼→ all resume
task 3 ─ wait ─┘

total ≈ 5 s
```

### Why?

`await` tells the event loop:

> This coroutine cannot make progress until an asynchronous operation completes. You may run something else.

### `async def`

Declares a coroutine function.

```python
async def fetch_data():
    ...
```

Calling it does not behave exactly like calling a normal function.

It creates a coroutine that must be:

- awaited,
- scheduled,
- or run by an event loop.

### Important rule

You can only use `await` inside an `async def` function.

### More important rule

`async def` does **not** magically make blocking code nonblocking.

This is wrong:

```python
async def bad():
    time.sleep(5)
```

The blocking sleep still blocks the thread running the event loop.

Use an async operation:

```python
async def good():
    await asyncio.sleep(5)
```

{{exercise:M01.L05.EX02}}

---

## 6. Event loop and coroutines

The **event loop** is the central scheduler in `asyncio`.

A useful beginner mental model is:

```text
while application is running:
    find tasks that can make progress
    run one
    if it awaits I/O:
        pause it
        run another ready task
    resume paused tasks when their events complete
```

### Coroutines can pause without losing state

A coroutine can stop at an `await` and later resume from the same place.

Conceptually:

```text
coroutine starts
    ↓
does some work
    ↓
await network request
    ↓
state preserved
    ↓
event loop runs other work
    ↓
network completes
    ↓
coroutine resumes
```

{{image:async-event-loop}}

### `asyncio.gather`

`asyncio.gather(...)` is useful when several independent asynchronous operations can start together.

For example:

```python
results = await asyncio.gather(
    fetch(url_a),
    fetch(url_b),
    fetch(url_c),
)
```

Instead of:

```text
fetch A
wait
fetch B
wait
fetch C
wait
```

you can overlap their waiting periods.

### Concurrency primitives

The source also notes that asyncio includes tools such as:

- futures,
- semaphores,
- locks.

You will not need to master them in this introductory lesson.

The important idea is that real concurrent programs eventually need controls around:

- how many tasks run,
- how shared state is accessed,
- how completion is represented.

---

## 7. Async model-provider APIs

A self-hosted model may be compute-bound on your hardware.

A hosted provider changes the nature of the work **from your application's perspective**.

Your service does:

```text
send HTTP request
      ↓
wait for provider
      ↓
receive response
```

The expensive inference happens elsewhere.

For your FastAPI process, the operation is primarily network I/O.

That means async programming becomes very useful.

### Synchronous provider call

```python
@app.post("/sync")
def sync_generate(prompt: str):
    response = sync_client.generate(prompt)
    return response
```

FastAPI can move a normal synchronous handler into its thread pool.

### Asynchronous provider call

```python
@app.post("/async")
async def async_generate(prompt: str):
    response = await async_client.generate(prompt)
    return response
```

During the wait, the event loop can work on other requests.

### Rate limits

Concurrency does not mean:

```text
send unlimited requests immediately
```

External providers impose limits.

The chapter introduces strategies such as:

- throttling,
- exponential backoff,
- waiting before retrying,
- requesting higher limits where appropriate.

### Exponential backoff intuition

```text
failure 1 → short delay
failure 2 → longer delay
failure 3 → longer again
```

This reduces pressure on an overloaded or rate-limited API.

### Common async pitfalls

The source highlights several mistakes:

- mixing blocking sync libraries into async code,
- forgetting `await`,
- awaiting something that is not awaitable,
- using a sync HTTP client where an async one is needed,
- failing to close network/database resources,
- creating unlimited concurrent work,
- making debugging harder through complex nonlinear flow.

### Recommended learning approach from the source

Understand the synchronous logic first.

Then convert the appropriate I/O boundaries to async.

That makes the control flow easier to reason about.

{{exercise:M01.L05.EX03}}

---

## 8. FastAPI's event loop and thread pool

FastAPI supports both:

```python
def sync_handler():
    ...
```

and:

```python
async def async_handler():
    ...
```

These are treated differently.

### Async route

An async handler runs on the main event loop.

It should perform nonblocking asynchronous work.

```text
async route
   ↓
event loop
```

### Sync route

A normal synchronous route can contain blocking synchronous work.

FastAPI/Starlette can delegate it to an internal thread pool so the main event loop is not directly blocked.

```text
sync route
   ↓
thread pool worker
```

### Why async is often more efficient for I/O

Threads introduce overhead:

- scheduling,
- thread switching,
- GIL acquisition.

If an async-compatible library exists, the event loop can often manage I/O waits with less overhead.

### But sync routes are not automatically bad

A synchronous route can be a reasonable choice if the code is synchronous.

FastAPI can isolate it in the thread pool.

The dangerous mistake is putting blocking code inside an async route.

---

## 9. How an async route accidentally blocks the entire server

Consider:

```python
@app.get("/block")
async def block_server():
    result = sync_client.some_blocking_call()
    return result
```

The function is marked `async`.

FastAPI therefore expects it to cooperate with the event loop.

But the call inside it is synchronous and blocking.

So the event loop cannot move on until the call completes.

### Better option A: use an async client

```python
@app.get("/fast")
async def fast_route():
    result = await async_client.some_call()
    return result
```

### Better option B: keep the route synchronous

```python
@app.get("/slow-but-safe")
def sync_route():
    result = sync_client.some_blocking_call()
    return result
```

FastAPI can then move the work to its thread pool.

### Decision rule

```text
async def
→ use async libraries + await

def
→ acceptable for synchronous/blocking implementation
```

### Why this mistake is serious

If a blocking call runs directly on the event loop:

```text
request A blocks
        ↓
event loop cannot schedule
        ↓
requests B, C, D also wait
```

One incorrectly implemented route can reduce responsiveness for the whole application.

{{image:threadpool-vs-async}}

{{exercise:M01.L05.EX04}}

---

## 10. Project: asynchronously talk to the web

The chapter uses a web scraper to make the concurrency ideas practical.

The desired flow is:

```text
User prompt contains URLs
        ↓
extract URLs
        ↓
fetch pages concurrently
        ↓
parse useful text
        ↓
append page content to prompt
        ↓
send enriched prompt to LLM
```

### Step 1: extract URLs

A regex can identify URL-like text.

```python
import re


def extract_urls(text: str) -> list[str]:
    pattern = r"(?P<url>https?://[^\\s]+)"
    return re.findall(pattern, text)
```

The source notes that a simple regex is not full URL validation.

That distinction matters.

### Step 2: fetch pages asynchronously

The chapter uses `aiohttp`.

```python
import aiohttp


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
) -> str:
    async with session.get(url) as response:
        return await response.text()
```

### Step 3: fetch many pages concurrently

```python
import asyncio


async def fetch_all(urls: list[str]):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[fetch(session, url) for url in urls],
            return_exceptions=True,
        )
```

Network waits overlap.

### Step 4: parse text

The source demonstrates HTML parsing with BeautifulSoup.

The chapter deliberately keeps the scraper simple.

A production scraper may need:

- website-specific parsers,
- dynamic browser rendering,
- anti-bot handling,
- quality checks,
- legal/terms review.

### Important usage boundary from the chapter

Before scraping:

- review site terms,
- use APIs where possible,
- get permission when uncertain.

### Step 5: dependency injection

The source wraps scraping into a FastAPI dependency.

That keeps the model controller small.

Conceptually:

```text
TextModelRequest
      ↓
get_urls_content dependency
      ↓
async web fetch
      ↓
parsed page text
      ↓
controller
```

This combines concepts from earlier lessons:

- async I/O,
- dependency injection,
- prompt enrichment.

---

## 11. Project: talk to documents with RAG

The chapter then builds a simple **retrieval-augmented generation (RAG)** module.

RAG adds external information to the prompt before generation.

High-level idea:

```text
User question
     ↓
retrieve relevant source content
     ↓
add content to prompt
     ↓
LLM
     ↓
answer
```

The source motivates RAG for knowledge-intensive tasks where the model should use custom information rather than relying only on patterns from training.

### RAG does not guarantee correctness

This is essential.

RAG can provide relevant factual context.

The model can still:

- misunderstand the context,
- ignore instructions,
- retrieve the wrong evidence,
- hallucinate.

So RAG is a grounding technique, not a proof system.

### Complete RAG pipeline

The chapter breaks the pipeline into:

1. **Extraction**  
   Obtain text from documents.

2. **Transformation**  
   Clean and split text.

3. **Embedding**  
   Convert text chunks into vectors.

4. **Storage**  
   Save vectors and metadata in a vector database.

5. **Retrieval**  
   Embed the query and find semantically related vectors.

6. **Augmentation**  
   Add retrieved original text to the prompt.

7. **Generation**  
   Send question + retrieved context to the language model.

[[IMAGE_NEEDED: End-to-end RAG pipeline | Diagram showing document upload → text extraction → chunking/cleaning → embeddings → vector database, then user query → query embedding → semantic search → retrieved text chunks → augmented prompt → LLM answer | Learner should notice the separate ingestion path and query-time retrieval path]]

{{exercise:M01.L05.EX05}}

---

## 12. Asynchronous file uploads and document extraction

### Why upload in chunks?

Users may upload large documents.

Reading an entire huge file into memory at once can increase memory pressure.

FastAPI's `UploadFile` supports file-like operations that can be used asynchronously.

The source demonstrates chunked writes:

```python
import aiofiles


async def save_file(file: UploadFile) -> str:
    async with aiofiles.open(
        "uploads/document.pdf",
        "wb",
    ) as target:
        while chunk := await file.read(CHUNK_SIZE):
            await target.write(chunk)
```

### Validate before storing

The example restricts the upload to PDF content.

The broader principle is:

```text
validate type/size
    ↓
save
    ↓
process
```

### PDF extraction is synchronous in the source

The chapter uses a synchronous PDF library.

That means this function should **not** be called directly in an async event-loop path if it performs blocking work.

Conceptually:

```python
def extract_pdf_text(filepath: str):
    ...
```

This becomes an important concurrency design problem:

> How do we combine synchronous extraction with an asynchronous API?

The source solves it using background-task/thread-pool behavior.

---

## 13. Chunk, clean, and embed document content

After extracting PDF text, the chapter streams text content from disk.

### Async file loader

```python
async def load(filepath: str):
    async with aiofiles.open(
        filepath,
        "r",
        encoding="utf-8",
    ) as f:
        while chunk := await f.read(CHUNK_SIZE):
            yield chunk
```

This is an **asynchronous generator**.

It can produce chunks one at a time without loading everything into memory.

### Cleaner

Text can contain:

- redundant whitespace,
- line breaks,
- formatting artifacts.

The cleaner normalizes this before embedding.

### Embedder

The chapter uses an open-source embedding model.

The role is:

```text
text chunk
    ↓
embedding model
    ↓
vector
```

Semantically related chunks should have useful geometric relationships in the vector space.

### Important nuance

File reading may be asynchronous.

Embedding itself may be compute-bound.

That means one pipeline can contain different workload types:

```text
read file
→ I/O-bound

clean text
→ small CPU work

embed text
→ model computation

store vector
→ database I/O
```

Correct architecture requires identifying each stage rather than calling the whole pipeline "async."

---

## 14. Semantic search and asynchronous vector storage

The source uses Qdrant as its vector database example.

### What is stored?

For each chunk, the database keeps:

- embedding vector,
- source information,
- original text.

Keeping the original text is essential because the embedding is used for similarity search, but the LLM needs readable context.

### Cosine similarity

The source uses cosine similarity to compare vectors.

Beginner interpretation:

```text
higher similarity
→ vectors point in more similar directions
→ text is more semantically related
```

The query flow:

```text
user question
   ↓
query embedding
   ↓
compare with stored vectors
   ↓
rank by similarity
   ↓
return top matching chunks
```

### Retrieval limit

You may ask for:

```text
top 3 results
```

rather than every match.

### Similarity threshold

You can also reject weak matches below a threshold.

This prevents obviously unrelated content from automatically entering the prompt.

### Async database client

Database communication is I/O.

The source therefore uses an asynchronous Qdrant client.

A repository abstraction exposes operations such as:

- create collection,
- delete collection,
- insert vector,
- search.

### Repository pattern

Higher layers should not need to know every low-level database call.

```text
VectorService
     ↓
VectorRepository
     ↓
Async Qdrant client
```

This preserves the layered architecture introduced earlier.

{{exercise:M01.L05.EX06}}

---

## 15. Background document ingestion

The document ingestion pipeline can take time:

```text
upload
  ↓
extract PDF text
  ↓
load chunks
  ↓
clean
  ↓
embed
  ↓
store vectors
```

The user does not necessarily need to keep the upload HTTP connection open for the entire pipeline.

The source uses FastAPI `BackgroundTasks`.

Conceptually:

```python
@app.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile,
):
    filepath = await save_file(file)

    background_tasks.add_task(
        extract_pdf_text,
        filepath,
    )

    background_tasks.add_task(
        vector_service.store_file_content_in_db,
        filepath.replace(".pdf", ".txt"),
    )

    return {
        "message": "File uploaded successfully"
    }
```

### Why this improves user experience

The response can return after the file has been accepted.

The expensive downstream processing happens after the response.

### Ordering matters

In the source's flow:

```text
extract text first
then store processed chunks
```

The second operation depends on the first.

### Sync and async background functions

The source notes:

- synchronous background work can use FastAPI's thread-pool behavior,
- asynchronous background work can run through the event loop.

But this does **not** make heavy computation magically parallel.

We will revisit that limit later.

---

## 16. Query-time retrieval and prompt augmentation

After documents have been indexed, the service can retrieve relevant context for each user question.

The source creates a dependency that:

1. reads the request prompt,
2. embeds it,
3. searches the vector store,
4. retrieves a small number of sufficiently similar chunks,
5. extracts their original text,
6. returns that text to the controller.

Conceptually:

```python
async def get_rag_content(body):
    query_vector = embed(body.prompt)

    matches = await vector_service.search(
        collection_name="knowledgebase",
        query_vector=query_vector,
        retrieval_limit=3,
        score_threshold=0.7,
    )

    return "\n".join(
        match.payload["original_text"]
        for match in matches
    )
```

Then:

```text
original user prompt
      +
web content
      +
RAG content
      ↓
final model prompt
```

### Why retrieve only a few chunks?

Too much context can:

- increase latency,
- exceed the context window,
- introduce irrelevant material,
- confuse generation.

Retrieval is about **selecting useful evidence**, not dumping the whole database into the prompt.

### RAG limitations highlighted by the chapter

The simple RAG pipeline can still fail because:

- poor splitting damages chunks,
- retrieval may miss relevant facts,
- the knowledge base may be incomplete,
- queries may be ambiguous,
- prompt size may exceed model limits,
- context ordering may be suboptimal,
- the model may still hallucinate.

The chapter points toward more advanced improvements such as:

- better chunking,
- query transformation,
- prompt compression,
- sliding-window approaches,
- fallback retrieval,
- maximal marginal relevance,
- reranking,
- filtering,
- hierarchical indexes,
- RAG fusion,
- other advanced retrieval strategies.

The lesson here is:

> **RAG quality depends heavily on retrieval quality, not just the final language model.**

---

## 17. Why async does not solve heavy self-hosted inference

The chapter now returns to model serving.

Async programming helped with:

- HTTP requests,
- web pages,
- file I/O,
- databases.

But self-hosted inference remains expensive.

### GPU inference stages

A simplified flow:

```text
model on disk
    ↓
load into RAM
    ↓
move to GPU memory
    ↓
run inference
```

The source emphasizes that large-model inference can become strongly **memory-bound**.

GPU arithmetic may be extremely fast, while moving large model weights and cached state through memory remains expensive.

### Why one FastAPI process is a bad place for everything

If the same process is responsible for:

```text
API routing
+ user requests
+ business logic
+ large-model inference
```

then heavy inference can prevent the application layer from serving users efficiently.

The recommended architectural direction is:

```text
FastAPI application
        ↓
network call
        ↓
specialized model server
        ↓
GPU inference
```

Now, from FastAPI's perspective, model inference becomes an I/O operation to another service.

### Model compression strategies introduced in the chapter

The source lists:

- quantization,
- pruning,
- distillation,
- fine-tuning smaller models.

These techniques aim to reduce inference burden or improve task efficiency.

### Transformer-serving optimizations introduced

The chapter also lists:

- fast attention,
- KV caching,
- paged attention,
- request batching,
- continuous batching.

These target different bottlenecks within language-model inference.

{{exercise:M01.L05.EX07}}

---

## 18. Externalize LLM serving with vLLM

The source uses vLLM as a concrete specialized LLM server.

The important architectural concept is more general:

```text
Application server
→ handles application concerns

Inference server
→ handles model execution and GPU optimization
```

### Application server responsibilities

Your main FastAPI service can focus on:

- authentication,
- request validation,
- user/account logic,
- RAG retrieval,
- business rules,
- rate limits,
- response formatting.

### Model server responsibilities

The LLM server can focus on:

- model loading,
- GPU use,
- batching,
- caching,
- parallel model execution,
- token generation.

### Network boundary

Once the model lives outside the main service:

```python
async def generate_text(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "http://model-server/v1/chat",
            json={"prompt": prompt},
        )

        data = await response.json()
        return data["..."]
```

The main FastAPI route can then be asynchronous because it is waiting on a network response.

### No more local lifespan model load

If the application process no longer owns the model, it no longer needs to preload that model during FastAPI startup.

### Why this is concurrency-friendly

The architecture separates:

```text
web/application CPU work
```

from:

```text
GPU model-serving work
```

Each can scale according to its own needs.

[[IMAGE_NEEDED: FastAPI plus external vLLM architecture | Diagram showing users → main FastAPI application for validation/RAG/business logic → asynchronous HTTP call → vLLM inference server → multiple GPU resources → response back to FastAPI | Learner should notice that model inference no longer blocks the application server process]]

---

## 19. Latency versus throughput

Two model-serving metrics matter throughout the rest of the chapter.

### Latency

How long one request waits for useful output.

For example:

```text
request sent
→ 2.3 seconds
→ first response arrives
```

Lower latency generally feels more responsive.

### Throughput

How much work the server can process over time.

For LLMs, examples can include:

- requests per unit time,
- tokens per minute.

Higher throughput means the service handles more total work.

### Trade-off

A large, high-quality model may require more compute and memory.

That can mean:

```text
larger model
→ potentially higher output quality
→ often more latency
→ often lower throughput
→ higher infrastructure cost
```

So model selection is not only about benchmark quality.

Production design also asks:

```text
How many users?
How quickly must they receive output?
How much hardware is available?
```

---

## 20. KV caching: avoid recomputing attention state

Autoregressive LLM generation works token by token.

At each step:

```text
existing sequence
    ↓
attention computation
    ↓
next token
    ↓
append token
    ↓
repeat
```

Recomputing all previous attention state from scratch would be wasteful.

So serving systems keep a **key-value cache**, or **KV cache**.

### Simplified intuition

The model computes attention-related intermediate values for earlier tokens.

Instead of throwing them away:

```text
previous attention state
        ↓
store in GPU memory
        ↓
reuse next generation step
```

This saves computation.

### The cost

The cache consumes GPU memory.

Longer sequences:

```text
more tokens
→ larger KV cache
```

More concurrent users:

```text
more sequences
→ more KV caches
```

This creates tension between:

- long context windows,
- large batch sizes,
- model size,
- concurrent-user capacity.

That is why memory optimization becomes central to LLM serving.

---

## 21. Static versus continuous batching

GPUs are very good at parallel matrix computation.

Instead of processing one request at a time, an inference server can group work.

### Static batching

Wait until a fixed-size batch is formed.

```text
request A ┐
request B ├→ batch of 4 → model
request C ┤
request D ┘
```

Problem:

Requests generate different output lengths.

Suppose:

```text
A finishes after 20 tokens
B after 100
C after 35
D after 200
```

If the batch is handled rigidly, completed slots may sit idle while the longest sequence continues.

### Continuous batching

The batch changes dynamically.

When one request finishes:

```text
A finishes
   ↓
new request E fills available slot
```

So the inference server keeps the GPU busier.

{{image:continuous-batching}}

### Why this improves serving

Continuous batching aims to achieve:

- higher GPU utilization,
- higher throughput,
- lower waiting time,
- more efficient resource use.

The source notes that specialized servers such as vLLM can provide this mechanism automatically.

---

## 22. Paged attention: manage KV-cache memory more efficiently

The KV cache grows as sequences grow.

Traditional contiguous allocation can waste GPU memory through fragmentation.

The chapter introduces **paged attention** as a memory-management strategy.

### Operating-system analogy

Think of virtual memory pages.

Instead of requiring one large continuous physical block:

```text
logical sequence
→ block table
→ several physical pages
```

The mapping separates logical order from physical storage location.

### Paged-attention steps

The source describes a flow like:

1. Split KV cache into fixed-size pages.
2. Maintain a mapping/lookup structure.
3. Allocate/load only the pages needed.
4. Use those key/value blocks during attention computation.

### Why this helps

It can reduce wasted GPU memory and improve the ability to serve many variable-length sequences.

A useful mental model is:

```text
without paging:
reserve large contiguous KV regions
→ fragmentation/waste

with paging:
allocate smaller blocks dynamically
→ more flexible memory use
```

[[IMAGE_NEEDED: Paged attention memory mapping | Diagram showing a logical KV-cache sequence divided into blocks, a block table mapping those logical blocks to noncontiguous physical GPU-memory pages, and only required pages being accessed during attention | Learner should notice the analogy to virtual memory and the reduction of contiguous-memory waste]]

### Continuous batching + paged attention

These optimizations complement each other:

```text
continuous batching
→ better compute utilization

paged attention
→ better KV-cache memory utilization
```

Together, they help a serving engine handle more concurrent generation efficiently.

---

## 23. Long-running inference jobs

Some generation tasks take much longer than ordinary request/response interactions.

Examples include:

- batch image generation,
- expensive image models,
- other long-running media generation.

If the user must keep one HTTP request open for minutes:

- the experience is poor,
- requests may time out,
- queues can grow,
- resources remain tied to long-lived interactions.

A better pattern is:

```text
user submits job
       ↓
server accepts job
       ↓
immediate acknowledgement
       ↓
work continues
       ↓
result stored
       ↓
client checks status / receives update
```

### FastAPI BackgroundTasks

For simple tasks, FastAPI provides a convenient mechanism.

Conceptually:

```python
@app.get("/generate/image/background")
def generate_in_background(
    background_tasks: BackgroundTasks,
    prompt: str,
    count: int,
):
    background_tasks.add_task(
        batch_generate_image,
        prompt,
        count,
    )

    return {
        "message": "Task is being processed"
    }
```

The client receives a response before all work is complete.

### Possible result-delivery patterns

The chapter suggests ideas such as:

- store results for later retrieval,
- expose polling endpoint,
- update the client through a live connection,
- notify the user when complete.

### Important limitation

Background tasks do **not** create true parallelism.

If a background task runs heavy compute directly on the event loop, it can still block the server.

Likewise, an async background function that internally uses blocking operations can block.

### Synchronous background tasks

FastAPI can place normal sync background functions in its thread pool.

That helps for suitable blocking operations, but it does not turn CPU-intensive inference into efficient parallel model serving.

---

## 24. When BackgroundTasks are not enough

FastAPI background tasks are convenient for simple jobs.

But production workloads may need:

- retries,
- durable queues,
- failure handling,
- task status,
- multiple workers,
- distributed processing,
- scheduling,
- backpressure.

The source mentions more specialized infrastructure such as:

- Celery,
- Redis,
- RabbitMQ,
- Ray Serve,
- BentoML,
- vLLM.

The categories matter more than memorizing product names.

### Model-serving framework

Best for:

```text
efficient inference
batching
GPU management
model workers
```

### Task queue + broker

Best for:

```text
durable asynchronous jobs
retries
worker distribution
job orchestration
```

### Application server

Best for:

```text
HTTP API
authentication
validation
business logic
user-facing orchestration
```

### Scalable architecture

```text
                 ┌─────────────────┐
Users ──────────→│ FastAPI API     │
                 └────────┬────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
   async database    task queue      model server
   / web I/O         / workers       / GPU inference
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                     persistent data
```

The final principle is:

> **Concurrency is an architecture decision, not an `async` keyword.**

{{exercise:M01.L05.EX08}}

---

## Important misconceptions

### Misconception 1

> Concurrency and parallelism mean the same thing.

### Why this is wrong

Concurrency means overlapping progress on multiple tasks. Parallelism means tasks actually execute simultaneously on separate compute resources.

### Misconception 2

> Threads give Python unlimited CPU parallelism.

### Why this is wrong

In the execution model described by the source, the GIL prevents multiple threads in one Python process from simultaneously executing Python bytecode.

### Misconception 3

> `async def` makes any slow function nonblocking.

### Why this is wrong

A synchronous blocking operation inside an async route still blocks the event loop.

### Misconception 4

> Every slow task should be solved with async I/O.

### Why this is wrong

Async is mainly valuable when work is waiting for I/O. CPU/GPU-heavy compute needs different strategies.

### Misconception 5

> A hosted LLM API is compute-bound inside my FastAPI process.

### Why this is wrong

From your service's perspective, the heavy inference happens remotely. Your process is mostly waiting on network I/O.

### Misconception 6

> RAG eliminates hallucinations.

### Why this is wrong

RAG can add relevant evidence, but retrieval can fail and the language model can still produce unsupported output.

### Misconception 7

> A vector database only needs embeddings.

### Why this is wrong

The RAG pipeline also needs readable metadata/original text so retrieved vectors can provide actual context to the model and sources to users.

### Misconception 8

> Adding more FastAPI worker processes is always the best way to scale a large model.

### Why this is wrong

Each process may require its own model copy, quickly exhausting memory.

### Misconception 9

> A large GPU means inference is never memory-bound.

### Why this is wrong

Large models and KV caches move huge amounts of data through GPU memory; memory bandwidth and capacity can become major bottlenecks.

### Misconception 10

> Batching always increases latency.

### Why this is wrong

Naive static batching can add waiting and idle capacity, while continuous batching is designed to dynamically refill work and improve overall utilization.

### Misconception 11

> KV caching is free.

### Why this is wrong

It avoids recomputation but consumes substantial GPU memory, especially for long sequences and many concurrent users.

### Misconception 12

> FastAPI BackgroundTasks run heavy inference in parallel automatically.

### Why this is wrong

They provide a convenient post-response execution mechanism, but heavy compute can still block unless moved to appropriate external workers/model servers.

---

## Key terminology

| Term | Meaning |
|---|---|
| Blocking operation | Work that prevents an execution flow from progressing until it finishes |
| I/O-bound | Work dominated by waiting for files, networks, databases, users, or other I/O |
| Compute-bound | Work dominated by CPU/GPU computation |
| Memory-bound | Work limited significantly by memory movement/access rather than arithmetic alone |
| Concurrency | Managing multiple tasks during overlapping periods |
| Parallelism | Executing tasks simultaneously on separate compute resources |
| Thread | Execution flow within a process that shares that process's memory |
| Process | Isolated executing program with its own memory space |
| GIL | Global Interpreter Lock described in the source as limiting simultaneous Python-bytecode execution across threads in one process |
| Time slicing | Switching CPU time among tasks to make overlapping progress |
| Async I/O | Cooperative concurrency that lets tasks yield while waiting for I/O |
| Coroutine | Async function execution object that can pause and later resume |
| Event loop | Scheduler that runs/resumes asynchronous tasks |
| `await` | Yields control while waiting for an awaitable operation |
| Thread pool | Pre-created worker threads used for synchronous/blocking operations |
| Multiprocessing | Running work in multiple independent processes, often across CPU cores |
| Exponential backoff | Retry strategy that increases waiting time after repeated failures |
| RAG | Retrieval-augmented generation: retrieve external context before generation |
| Embedding | Vector representation used to compare semantic content |
| Semantic search | Retrieval based on vector meaning/similarity rather than exact keywords |
| Cosine similarity | Vector similarity measure used in the chapter's semantic-search examples |
| Vector database | Database optimized for storing/searching vector representations |
| Repository | Data-access abstraction between services and a database client |
| Async generator | Generator whose iterations can await asynchronous operations |
| Latency | Delay experienced by one request before receiving output |
| Throughput | Amount of model-serving work completed per unit time |
| KV cache | Stored transformer key/value attention state reused during autoregressive generation |
| Static batching | Fixed-size request batching |
| Continuous batching | Dynamically filling/replacing request slots as generations start and finish |
| Paged attention | KV-cache memory-management strategy using page/block mappings |
| Model server | Separate service specialized in running model inference |
| Background task | Work triggered after the main HTTP response can be returned |
| Task queue | Infrastructure for durable asynchronous jobs, retries, and worker distribution |

---

## Self-check

Before continuing, make sure you can answer:

1. What makes an operation I/O-bound?
2. What makes an operation compute-bound?
3. Why can large-model inference be memory-bound?
4. What is the difference between concurrency and parallelism?
5. Why can async concurrency work on a single CPU core?
6. What role does the GIL play in the chapter's threading model?
7. Why are processes better suited than threads for some CPU-heavy work?
8. Why is multiprocessing awkward for a huge in-memory model?
9. When should you prefer async I/O?
10. When might a thread pool still be useful?
11. What does `await` communicate to the event loop?
12. What is a coroutine?
13. Why does calling a coroutine not behave like calling a normal synchronous function?
14. What does `asyncio.gather` help you do?
15. Why does a provider LLM call become I/O-bound from your server's perspective?
16. Why do concurrent provider requests need rate-limit control?
17. What is exponential backoff?
18. What happens when you put a synchronous blocking client inside an `async def` route?
19. How does FastAPI treat synchronous route handlers?
20. How does it treat asynchronous handlers?
21. Why should an async handler use async-compatible dependencies?
22. How does the web-scraper example benefit from `aiohttp` and `asyncio.gather`?
23. What legal/operational concerns accompany scraping external sites?
24. What are the seven conceptual stages of the RAG pipeline?
25. Why upload large files in chunks?
26. Why is a synchronous PDF extractor dangerous if run directly on the event loop?
27. What is an asynchronous generator useful for in document processing?
28. Why should original text be stored alongside embeddings?
29. How does semantic search retrieve relevant chunks?
30. What do retrieval limit and similarity threshold control?
31. Why can RAG still produce poor answers?
32. Why might context ranking matter?
33. Why can async I/O not solve self-hosted heavy inference by itself?
34. What is gained by externalizing LLM serving?
35. What is latency?
36. What is throughput?
37. Why does the KV cache improve generation speed?
38. What resource does the KV cache consume?
39. Why does static batching waste capacity with variable-length generations?
40. How does continuous batching improve GPU utilization?
41. What problem does paged attention target?
42. How is paged attention conceptually similar to virtual memory?
43. What is an appropriate use for FastAPI BackgroundTasks?
44. Why are BackgroundTasks not a substitute for parallel inference infrastructure?
45. When would you introduce a durable task queue?
46. What responsibilities should remain in FastAPI when model inference is externalized?

---

## Retain this idea

**Scalable AI services come from matching the execution strategy to the bottleneck: use async I/O for waiting on networks, files, and databases; isolate CPU/GPU-heavy inference from the application server; optimize LLM serving with batching and cache-aware memory management; and use background or queued jobs when the user's request should not remain open for long-running work.**
""",

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "blocking-workloads",
                "title": "Why AI services become blocked",
                "order": 1,
            },
            {
                "id": "concurrency-vs-parallelism",
                "title": "Concurrency versus parallelism",
                "order": 2,
            },
            {
                "id": "gil-threads-processes",
                "title": "The GIL, threads, and processes",
                "order": 3,
            },
            {
                "id": "strategy-selection",
                "title": "Choose the concurrency strategy from the workload",
                "order": 4,
            },
            {
                "id": "async-basics",
                "title": "Synchronous versus asynchronous execution",
                "order": 5,
            },
            {
                "id": "event-loop-coroutines",
                "title": "Event loop and coroutines",
                "order": 6,
            },
            {
                "id": "async-provider-apis",
                "title": "Async model-provider APIs",
                "order": 7,
            },
            {
                "id": "fastapi-event-loop-thread-pool",
                "title": "FastAPI's event loop and thread pool",
                "order": 8,
            },
            {
                "id": "blocking-main-server",
                "title": "How an async route accidentally blocks the entire server",
                "order": 9,
            },
            {
                "id": "web-scraper",
                "title": "Project: asynchronously talk to the web",
                "order": 10,
            },
            {
                "id": "rag-overview",
                "title": "Project: talk to documents with RAG",
                "order": 11,
            },
            {
                "id": "async-file-upload",
                "title": "Asynchronous file uploads and document extraction",
                "order": 12,
            },
            {
                "id": "rag-transform",
                "title": "Chunk, clean, and embed document content",
                "order": 13,
            },
            {
                "id": "semantic-search-qdrant",
                "title": "Semantic search and asynchronous vector storage",
                "order": 14,
            },
            {
                "id": "rag-background-ingestion",
                "title": "Background document ingestion",
                "order": 15,
            },
            {
                "id": "rag-retrieval",
                "title": "Query-time retrieval and prompt augmentation",
                "order": 16,
            },
            {
                "id": "compute-memory-bound",
                "title": "Why async does not solve heavy self-hosted inference",
                "order": 17,
            },
            {
                "id": "external-vllm",
                "title": "Externalize LLM serving with vLLM",
                "order": 18,
            },
            {
                "id": "latency-throughput",
                "title": "Latency versus throughput",
                "order": 19,
            },
            {
                "id": "kv-cache",
                "title": "KV caching: avoid recomputing attention state",
                "order": 20,
            },
            {
                "id": "batching",
                "title": "Static versus continuous batching",
                "order": 21,
            },
            {
                "id": "paged-attention",
                "title": "Paged attention: manage KV-cache memory more efficiently",
                "order": 22,
            },
            {
                "id": "long-running-inference",
                "title": "Long-running inference jobs",
                "order": 23,
            },
            {
                "id": "queues-and-scale",
                "title": "When BackgroundTasks are not enough",
                "order": 24,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L05.EX01",

            "title": "Classify the Workload and Execution Strategy",

            "lesson_code": "M01.L05",

            "section_id": "concurrency-vs-parallelism",

            "placement": "after_section",

            "description": (
                "Practice distinguishing I/O, compute, and memory bottlenecks before "
                "selecting a concurrency strategy."
            ),

            "instructions": (
                "For each task, classify it primarily as `I/O-bound`, `compute-bound`, "
                "or `memory/model-serving-bound`, then choose the most appropriate "
                "strategy from this lesson.\n\n"
                "1. Fetching 20 web pages.\n"
                "2. Waiting for an external LLM provider API.\n"
                "3. Running a CPU-heavy simulation.\n"
                "4. Serving a very large local LLM to many users.\n"
                "5. Writing a large uploaded file to disk.\n"
                "6. Generating hundreds of embeddings locally.\n\n"
                "Explain each choice in one or two sentences."
            ),

            "expected_output": (
                "A six-row classification table containing workload type, strategy, and reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "workload-classification",
                "concurrency-strategy",
                "systems-reasoning",
            ],
        },

        {
            "id": "M01.L05.EX02",

            "title": "Measure Sync versus Async Waiting",

            "lesson_code": "M01.L05",

            "section_id": "async-basics",

            "placement": "after_section",

            "description": (
                "Observe why overlapping I/O waits can dramatically reduce elapsed time."
            ),

            "instructions": (
                "1. Write a synchronous function that waits using `time.sleep(2)`.\n"
                "2. Run it three times sequentially and record the elapsed time.\n"
                "3. Write an async version using `await asyncio.sleep(2)`.\n"
                "4. Run three copies concurrently with `asyncio.gather`.\n"
                "5. Record the elapsed time.\n"
                "6. Explain why the async example is faster even though it does not "
                "perform three CPU computations simultaneously."
            ),

            "expected_output": (
                "Two runnable examples, two elapsed-time observations, and an explanation "
                "of overlapping I/O waits."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "asyncio",
                "async-await",
                "concurrency-intuition",
            ],
        },

        {
            "id": "M01.L05.EX03",

            "title": "Design an Async Provider Endpoint",

            "lesson_code": "M01.L05",

            "section_id": "async-provider-apis",

            "placement": "after_section",

            "description": (
                "Build the request flow for a FastAPI route calling a hosted model provider."
            ),

            "instructions": (
                "Design a POST endpoint that calls an asynchronous model-provider client.\n\n"
                "Include:\n"
                "1. `async def` route handler.\n"
                "2. An awaited provider API call.\n"
                "3. Basic exception handling.\n"
                "4. A simple rate-limit/backoff strategy description.\n"
                "5. A sentence explaining why this call is I/O-bound from your server's perspective.\n\n"
                "Then explain what would go wrong if you replaced the async client "
                "with a synchronous client inside the same async handler."
            ),

            "expected_output": (
                "A short endpoint implementation/pseudocode plus rate-limit and blocking explanations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "async-provider-api",
                "rate-limits",
                "fastapi-async",
            ],
        },

        {
            "id": "M01.L05.EX04",

            "title": "Find the Event-Loop Blocking Bug",

            "lesson_code": "M01.L05",

            "section_id": "blocking-main-server",

            "placement": "after_section",

            "description": (
                "Recognize the dangerous combination of an async route and synchronous blocking dependency."
            ),

            "instructions": (
                "Inspect this pattern:\n\n"
                "```python\n"
                "@app.get('/chat')\n"
                "async def chat():\n"
                "    result = sync_client.generate('hello')\n"
                "    return result\n"
                "```\n\n"
                "1. Explain why the route can block the event loop.\n"
                "2. Rewrite it using an async client.\n"
                "3. Give a second valid alternative using a normal synchronous handler.\n"
                "4. Explain which option you would prefer if an async SDK is available."
            ),

            "expected_output": (
                "A bug explanation and two corrected route implementations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "event-loop",
                "blocking-detection",
                "fastapi-routing",
            ],
        },

        {
            "id": "M01.L05.EX05",

            "title": "Draw the RAG Ingestion and Query Paths",

            "lesson_code": "M01.L05",

            "section_id": "rag-overview",

            "placement": "after_section",

            "description": (
                "Separate offline/background document processing from query-time retrieval."
            ),

            "instructions": (
                "Draw two flows.\n\n"
                "**Ingestion path:**\n"
                "PDF upload → extraction → chunking/cleaning → embeddings → vector store.\n\n"
                "**Query path:**\n"
                "question → query embedding → semantic search → top chunks → augmented "
                "prompt → LLM → answer.\n\n"
                "For each step, label it as mainly I/O-bound or compute/model work.\n"
                "Finally, explain why the original text must be stored as metadata "
                "alongside the embedding vector."
            ),

            "expected_output": (
                "Two labeled RAG pipeline diagrams plus a metadata explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "rag-pipeline",
                "embeddings",
                "workload-analysis",
            ],
        },

        {
            "id": "M01.L05.EX06",

            "title": "Design a Vector Retrieval Contract",

            "lesson_code": "M01.L05",

            "section_id": "semantic-search-qdrant",

            "placement": "after_section",

            "description": (
                "Practice the inputs and outputs of semantic retrieval in a RAG service."
            ),

            "instructions": (
                "Design a `search` method for a vector repository.\n\n"
                "It should accept:\n"
                "- collection name,\n"
                "- query vector,\n"
                "- retrieval limit,\n"
                "- similarity threshold.\n\n"
                "The returned results should include:\n"
                "- similarity score,\n"
                "- original text,\n"
                "- source metadata.\n\n"
                "Then explain what happens when the retrieval limit is too high, the "
                "threshold is too low, or the threshold is too high."
            ),

            "expected_output": (
                "A typed/pseudocode repository method and three retrieval trade-off explanations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "vector-database",
                "semantic-retrieval",
                "rag-tuning",
            ],
        },

        {
            "id": "M01.L05.EX07",

            "title": "Separate Application and Inference Servers",

            "lesson_code": "M01.L05",

            "section_id": "compute-memory-bound",

            "placement": "after_section",

            "description": (
                "Apply external model serving to prevent heavy inference from dominating the main API."
            ),

            "instructions": (
                "Design a two-service architecture for a self-hosted LLM.\n\n"
                "The FastAPI application server must handle:\n"
                "- authentication,\n"
                "- Pydantic validation,\n"
                "- RAG retrieval,\n"
                "- business logic.\n\n"
                "The model server must handle:\n"
                "- model loading,\n"
                "- GPU inference,\n"
                "- batching,\n"
                "- KV-cache management.\n\n"
                "1. Draw the request path.\n"
                "2. Explain why the FastAPI → model-server call can be asynchronous.\n"
                "3. Explain why simply adding more FastAPI workers may duplicate model memory."
            ),

            "expected_output": (
                "A two-service architecture diagram and explanations of async networking and memory duplication."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "external-model-serving",
                "vllm-architecture",
                "scalability",
            ],
        },

        {
            "id": "M01.L05.EX08",

            "title": "Choose BackgroundTasks or a Durable Queue",

            "lesson_code": "M01.L05",

            "section_id": "queues-and-scale",

            "placement": "after_section",

            "description": (
                "Decide when FastAPI's built-in background mechanism is sufficient "
                "and when a dedicated job system is justified."
            ),

            "instructions": (
                "For each scenario, choose `FastAPI BackgroundTasks` or a `durable "
                "task queue / worker system` and explain why:\n\n"
                "1. Send one confirmation email after an API response.\n"
                "2. Process a short uploaded document in a small internal tool.\n"
                "3. Run thousands of multi-minute image-generation jobs with retries.\n"
                "4. Execute jobs that must survive API-server restarts.\n"
                "5. Perform a simple noncritical post-response log operation.\n\n"
                "For the durable-queue cases, list at least three capabilities the "
                "queue system should provide."
            ),

            "expected_output": (
                "Five architecture choices plus required capabilities for durable job processing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "background-tasks",
                "task-queues",
                "production-architecture",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L05.QZ01",

        "title": "Achieving Concurrency in AI Workloads — Knowledge Check",

        "lesson_code": "M01.L05",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",

                "section_id": "blocking-workloads",

                "question": "Which task is primarily I/O-bound?",

                "options": [
                    "Waiting for a database query over the network",
                    "Running a large matrix multiplication on a GPU",
                    "Training a neural network",
                    "Rendering a complex 3D simulation",
                ],

                "correct": 0,

                "explanation": (
                    "Database communication spends significant time waiting for I/O, "
                    "whereas the other examples are dominated by computation."
                ),
            },

            {
                "id": "M01.L05.Q02",

                "section_id": "concurrency-vs-parallelism",

                "question": "What best distinguishes parallelism from concurrency?",

                "options": [
                    "Parallelism requires every task to use async syntax",
                    "Parallelism executes tasks simultaneously on separate compute resources",
                    "Concurrency can only be implemented with several machines",
                    "Concurrency always executes tasks at exactly the same instant",
                ],

                "correct": 1,

                "explanation": (
                    "Concurrency allows overlapping progress; parallelism means actual "
                    "simultaneous execution on distinct resources."
                ),
            },

            {
                "id": "M01.L05.Q03",

                "section_id": "gil-threads-processes",

                "question": (
                    "Why can multiprocessing help CPU-bound Python workloads?"
                ),

                "options": [
                    "Each process can execute independently on separate CPU cores",
                    "All processes automatically share one model in memory",
                    "It converts compute into network I/O",
                    "It removes the need for scheduling",
                ],

                "correct": 0,

                "explanation": (
                    "Separate processes can use multiple cores and have independent "
                    "execution resources, though sharing data becomes more complex."
                ),
            },

            {
                "id": "M01.L05.Q04",

                "section_id": "async-basics",

                "question": "What does `await` do in an async function?",

                "options": [
                    "It indicates a point where the coroutine can yield while awaiting compatible asynchronous work",
                    "It creates a new CPU core",
                    "It forces a synchronous function into parallel execution",
                    "It disables the event loop",
                ],

                "correct": 0,

                "explanation": (
                    "`await` allows the coroutine to pause cooperatively while the "
                    "event loop schedules other ready work."
                ),
            },

            {
                "id": "M01.L05.Q05",

                "section_id": "async-provider-apis",

                "question": (
                    "Why is a hosted LLM-provider call primarily I/O-bound from your "
                    "FastAPI service's perspective?"
                ),

                "options": [
                    "The heavy model inference runs on the provider's infrastructure while your service waits on the network",
                    "Hosted providers do not perform model inference",
                    "FastAPI converts every provider request into a local GPU task",
                    "Network calls use no external resources",
                ],

                "correct": 0,

                "explanation": (
                    "Your service sends a network request and waits; the provider owns "
                    "the compute-heavy inference."
                ),
            },

            {
                "id": "M01.L05.Q06",

                "section_id": "blocking-main-server",

                "question": (
                    "What is dangerous about calling a synchronous blocking SDK inside "
                    "an `async def` FastAPI handler?"
                ),

                "options": [
                    "It may block the main event loop and delay other requests",
                    "It automatically creates too many processes",
                    "It disables Pydantic validation",
                    "It forces every response to use WebSockets",
                ],

                "correct": 0,

                "explanation": (
                    "FastAPI expects async handlers to cooperate with the event loop. "
                    "A blocking synchronous call prevents that scheduling."
                ),
            },

            {
                "id": "M01.L05.Q07",

                "section_id": "rag-overview",

                "question": "What is the main role of retrieval in RAG?",

                "options": [
                    "Find relevant external context to add before language-model generation",
                    "Train the LLM from scratch on every request",
                    "Replace all embeddings with keyword counts",
                    "Eliminate the model context window",
                ],

                "correct": 0,

                "explanation": (
                    "RAG retrieves relevant source material and uses it to augment the "
                    "model's prompt/context."
                ),
            },

            {
                "id": "M01.L05.Q08",

                "section_id": "semantic-search-qdrant",

                "question": (
                    "Why should original text be stored as metadata with its embedding?"
                ),

                "options": [
                    "The retrieved embedding helps locate relevant content, while the original text provides readable context for the model/user",
                    "Embeddings are always directly readable English",
                    "Qdrant cannot store vectors without PDFs",
                    "Original text is required to create HTTP status codes",
                ],

                "correct": 0,

                "explanation": (
                    "The vector supports similarity search, while the original source "
                    "text is what the application can place into the model context."
                ),
            },

            {
                "id": "M01.L05.Q09",

                "section_id": "compute-memory-bound",

                "question": (
                    "Why can adding async code fail to solve slow local LLM inference?"
                ),

                "options": [
                    "The inference itself is heavy compute/memory work rather than merely waiting for I/O",
                    "Async functions cannot call neural networks",
                    "FastAPI disables GPUs in async applications",
                    "LLMs can only run synchronously over HTTP",
                ],

                "correct": 0,

                "explanation": (
                    "Async excels at overlapping waits. It does not make expensive "
                    "model computation or memory movement disappear."
                ),
            },

            {
                "id": "M01.L05.Q10",

                "section_id": "latency-throughput",

                "question": "What is throughput in an LLM-serving system?",

                "options": [
                    "The amount of serving work the system completes over a period of time",
                    "Only the first-token delay for one user",
                    "The number of model parameters",
                    "The size of one request body",
                ],

                "correct": 0,

                "explanation": (
                    "Throughput measures total processing capacity over time, while "
                    "latency measures delay for an individual request."
                ),
            },

            {
                "id": "M01.L05.Q11",

                "section_id": "kv-cache",

                "question": "What is the main trade-off of KV caching?",

                "options": [
                    "It reduces repeated attention computation but consumes GPU memory",
                    "It lowers memory use to zero but doubles computation",
                    "It replaces tokenization",
                    "It guarantees factual model output",
                ],

                "correct": 0,

                "explanation": (
                    "Caching previous key/value attention state speeds autoregressive "
                    "generation but increases memory usage."
                ),
            },

            {
                "id": "M01.L05.Q12",

                "section_id": "batching",

                "question": (
                    "What advantage does continuous batching have over rigid static batching?"
                ),

                "options": [
                    "Finished request slots can be refilled with new work, improving GPU utilization",
                    "It forces every output to have the same length",
                    "It removes all model memory use",
                    "It requires only one request at a time",
                ],

                "correct": 0,

                "explanation": (
                    "Continuous batching dynamically changes the active batch as "
                    "requests complete and arrive."
                ),
            },

            {
                "id": "M01.L05.Q13",

                "section_id": "paged-attention",

                "question": "What problem does paged attention primarily target?",

                "options": [
                    "Inefficient and fragmented KV-cache memory allocation",
                    "Invalid JSON request bodies",
                    "Slow PDF uploads",
                    "Missing database authentication",
                ],

                "correct": 0,

                "explanation": (
                    "Paged attention organizes KV cache into manageable blocks/pages "
                    "and maps logical sequence blocks to physical memory."
                ),
            },

            {
                "id": "M01.L05.Q14",

                "section_id": "long-running-inference",

                "question": (
                    "What is the main user-experience benefit of accepting a long-running "
                    "job and processing it after the HTTP response?"
                ),

                "options": [
                    "The user does not need to hold one request open for the entire generation time",
                    "The model becomes deterministic",
                    "The job automatically runs on another machine",
                    "The GPU no longer needs memory",
                ],

                "correct": 0,

                "explanation": (
                    "The request can be acknowledged quickly while work continues and "
                    "the result is delivered or retrieved later."
                ),
            },

            {
                "id": "M01.L05.Q15",

                "section_id": "queues-and-scale",

                "type": "open",

                "question": (
                    "Design the execution strategy for a production GenAI service that "
                    "must fetch web pages, query a vector database, call a self-hosted "
                    "large LLM, and run multi-minute image-generation jobs. State which "
                    "parts should use async I/O, which should be external model services, "
                    "and which should use a durable job queue. Explain why."
                ),
            },
        ],

        "passing_score": 70,
    },
}
