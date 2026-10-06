"""M01.L08 — Integrated Live Agent Systems and Long-Running Workflows.

Two source chapters -> one complete learner-facing lesson.

Source alignment:
- Chapter 12: Reference Architecture: An Integrated Live Agent System
- Chapter 13: Asynchronous Operations and Long-Running Tasks in an Integrated Agent System

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L08"
MODULE_ORDER = 1
MODULE_TITLE = "Integrated Live Agents & Durable Workflows"
MODULE_DESCRIPTION = (
    "Combine live browser interaction, ADK Live orchestration, A2A specialist delegation, "
    "and MCP tool services into one bounded reference architecture, then extend that design "
    "for long-running production workflows with durable task identity, persistent state, "
    "progress, recovery, approvals, cancellation, idempotency, observability, and security."
)
SOURCE_CHAPTER = "12-13"
SOURCE_PAGES = "Early Release drafts; page numbers not provided"

TOPIC = {
    "title": "Integrated Live Agent Systems and Long-Running Workflows",
    "slug": "agent-foundations-m01-l08",
    "description": (
        "Learn how a live user-facing agent should delegate domain work through A2A and MCP "
        "without becoming a tool monolith, then evolve the same service boundaries into a "
        "durable asynchronous architecture where long-running work can survive disconnects, "
        "human pauses, retries, cancellations, and process restarts."
    ),
    "order": 8,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 7.0,
    "skill_tags": [
        "reference-architecture",
        "live-agents",
        "adk-live",
        "a2a",
        "mcp",
        "service-boundaries",
        "browser-websocket",
        "provenance",
        "fallback-handling",
        "task-lifecycle",
        "long-running-tasks",
        "durable-state",
        "polling",
        "streaming",
        "push-notifications",
        "human-in-the-loop",
        "cancellation",
        "idempotency",
        "observability",
        "security",
        "frontend-state",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
    ],

    "lesson": {
        "title": "Integrated Live Agent Systems and Long-Running Workflows",
        "estimated_minutes": 420,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Integrated Live Agent Systems and Long-Running Workflows

> **Lesson:** M01.L08  
> **Source alignment:** Chapters 12 and 13 of the supplied Early Release material.  
> This lesson merges the reference architecture and its long-running production extension into one continuous design story.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why attaching every domain tool directly to a live user-facing agent creates architectural collapse.
- Describe the responsibilities of the Browser UI, frontend service, FastAPI/ADK Live backend, host agent, A2A specialists, and MCP tool server.
- Explain why domain parsing and fallback logic should stay downstream of the live host.
- Trace one stock request across browser, backend, ADK Live, host agent, A2A specialist, MCP tool server, and back.
- Explain why the host should delegate natural-language domain requests rather than prematurely narrowing them into tool arguments.
- Explain how provenance, fallback, warning, and unavailable states should travel upstream as structured data.
- Use service boundaries as a debugging map.
- Explain why browser activity is not equivalent to full distributed tracing.
- Describe the bounded local reference app and identify its intentional simplifications.
- Explain why long-running work must be modeled as a task rather than a slow function call.
- Define task identity, state, progress, ownership, persistence, cancellation, retention, and recovery.
- Explain why the task—not the original HTTP request—becomes the unit of reliability.
- Distinguish the responsibilities of ADK, A2A, MCP, and application-owned durable state.
- Explain why blocking work must not run on an async event loop.
- Distinguish short blocking work that can use executors from truly long-running work that needs a durable task model.
- Explain the difference between task initiation and task completion.
- Explain how remote A2A task IDs should be persisted before later updates arrive.
- Compare polling, streaming/subscription, and push notifications for long-running remote work.
- Explain why streaming improves visibility but does not replace durable state.
- Explain how long-running MCP operations should be treated as capability-dependent task-style work.
- Explain human-in-the-loop approval as asynchronous suspension.
- Explain why authentication can also become a suspension point.
- Explain how distributed input-required states should pause and resume workflows safely.
- Design structured progress updates for both user experience and operations.
- Explain cancellation propagation across frontend, backend, A2A, and MCP boundaries.
- Distinguish browser disconnect from explicit cancellation.
- Explain timeout, expiration, retention, and stale-task sweeping.
- Explain why idempotency is essential in asynchronous distributed systems.
- Define correlation metadata for observability across frontend, ADK, A2A, MCP, workers, and callbacks.
- Explain security risks that arise when tasks outlive user sessions and tokens.
- Design frontend state that can recover after refresh, disconnect, or return-later behavior.
- Trace a complete long-running market-report workflow from live submission through delegation, approval, artifact delivery, and cleanup.
- Identify the major anti-patterns and production checklist items from the source.

---

## 1. Why the live agent must not own everything

The source begins with a realistic failure mode.

A live stock assistant starts simply:

```text
Live Agent
   ↓
get_stock_price("NVDA")
```

The first demo works.

Then requirements accumulate:

```text
company-name lookup
market context
quote provenance
weather lookup
customer lookup
document search
compliance checks
fallback rules
provider errors
tool schemas
domain policy
```

The live agent slowly becomes responsible for:

- microphone behavior,
- turn-taking,
- spoken response style,
- domain parsing,
- provider quirks,
- routing,
- fallbacks,
- business rules.

That is dangerous because the live agent already owns the most latency-sensitive part of the system.

### Architectural smell

If the same component owns:

```text
live interaction
+
domain interpretation
+
provider logic
+
fallback rules
+
tool execution
```

then every new domain change risks destabilizing the live experience.

### Core principle

> Keep the user-facing live agent narrow. Let specialists and tool services own domain complexity.

[[IMAGE_NEEDED: Overloaded live agent vs layered system | Left: one live agent connected directly to stock, weather, documents, customer lookup, compliance, and many rules; right: live host delegates to A2A specialists which use MCP tools | Learner should see why the live layer should not become a domain monolith]]

---

## 2. The integrated reference system

Chapter 12 assembles earlier course concepts into one bounded app.

The request path is:

```text
Browser UI
   ↓
Frontend Service
   ↓
FastAPI Backend / ADK Live
   ↓
ADK Host Agent
   ↓
A2A Specialist
   ↓
MCP Tool Server
   ↓
External provider / deterministic fallback
```

Then the result returns through the same path.

The source uses this stock request:

```text
"What is the latest price for NVDA,
and give me a one-sentence market context?"
```

The goal is not to build every production feature.

It is to create one clean request path where each component owns a bounded responsibility.

---

## 3. Browser UI responsibilities

The Browser UI owns user interaction.

The source assigns it things like:

- text fallback,
- microphone input,
- optional sampled frames,
- audio playback,
- captions,
- controls,
- provenance display,
- local activity,
- diagnostics.

What should it not own?

```text
ticker parsing
finance provider calls
specialist routing
```

The browser should render what the system tells it.

It should not reverse-engineer domain meaning from final sentences.

### Example

Bad UI architecture:

```text
final sentence contains "sample"
    ↓
browser guesses data is fallback
```

Better:

```text
backend sends structured provenance/fallback metadata
    ↓
browser renders it directly
```

---

## 4. Frontend service responsibilities

The frontend service is intentionally simple.

It serves:

- static assets,
- `/config.json`,
- frontend health.

The browser uses `/config.json` to learn the live WebSocket URL.

The frontend service should not own:

```text
ADK Live runtime
model credentials
A2A routing
MCP tools
domain logic
```

This keeps static delivery separate from agent execution.

---

## 5. FastAPI backend and ADK Live host process

The backend owns the browser-to-runtime edge.

The source assigns it:

- `/health`,
- `/live`,
- WebSocket origin validation,
- ADK Live input queue,
- ADK Runner,
- event shaping.

It should not own:

- static asset serving,
- quote-provider policy,
- A2A specialist internals,
- MCP tool implementation.

### Important distinction

The backend knows:

```text
how to move live input and output
```

It does not need to know:

```text
how finance works
```

---

## 6. The ADK host agent owns user-facing intent

The host agent is the conversational face of the system.

It owns:

- user-facing conversation,
- concise spoken relay,
- choosing which discovered specialist should handle a domain request.

It should not own:

```text
quote lookup
weather lookup
ticker alias tables
provider fallback policy
general service-registry policy
```

The host should know:

```text
"This is a stock-domain question."
```

It should not know:

```text
"Nvidia -> NVDA"
"Google -> GOOGL"
"this provider needs this fallback"
```

Those are domain details.

---

## 7. A2A specialists own domain interpretation

The source uses separate stock and weather specialists.

A specialist owns:

- domain-specific language,
- interpreting the user request,
- invoking the correct MCP tool,
- shaping structured domain results.

For stocks, the specialist can understand:

```text
"Nvidia"
"NVDA"
"Google's stock"
```

The live host should not need those mappings.

### Why this matters

If mappings leak upward into the host, the host soon accumulates:

- ticker aliases,
- weather location rules,
- document permissions,
- compliance special cases.

That is exactly the monolith Chapter 12 is trying to prevent.

---

## 8. The MCP tool server owns provider access

The MCP tool server owns the lowest-level capability.

For the stock path, it owns:

```text
symbol normalization
provider request
provider failure handling
provenance
fallback labeling
unavailable state
short market context
```

The tool should return data, not the final conversation.

Conceptual result:

```json
{
  "symbol": "NVDA",
  "price": 123.45,
  "currency": "USD",
  "as_of": "...",
  "source": "provider-name",
  "fallback": false,
  "warning": null,
  "market_context": "..."
}
```

### Rule

> The component that first knows data quality should attach data-quality metadata.

Upstream layers should preserve it.

---

## 9. Responsibility boundaries as an architectural contract

A useful way to remember the system is:

| Layer | Owns | Should not own |
|---|---|---|
| Browser | capture, playback, UI, provenance display | domain rules |
| Frontend service | static assets, config | runtime logic |
| Backend | live transport, event shaping | finance/weather behavior |
| Host Agent | conversation, routing | provider/fallback rules |
| A2A Specialist | domain interpretation | browser/live-session ownership |
| MCP Server | tool/provider behavior | conversation/routing |

This is more than documentation.

It is a drift detector.

Ask:

> Is this component starting to own something from another row?

If yes, the architecture may be collapsing.

[[IMAGE_NEEDED: Six-layer responsibility map | Browser, Frontend Service, Backend/ADK Live, Host Agent, A2A Specialist, MCP Server stacked vertically with owned responsibilities and prohibited responsibilities beside each | Learner should use this as a boundary checklist]]

{{exercise:M01.L08.EX01}}

---

## 10. Walk the NVDA request end to end

Now follow the request:

```text
"What is the latest price for NVDA,
and give me a one-sentence market context?"
```

The source describes eight useful stages.

---

## 11. Step 1 — Browser loads config

The browser:

1. loads static assets,
2. reads `/config.json`,
3. learns the backend live WebSocket URL.

This is an important operational detail.

The frontend does not hard-code runtime configuration into the bundle.

---

## 12. Step 2 — Browser sends live input

The browser can send:

- text,
- audio,
- sampled images,
- control/activity events.

For the NVDA walkthrough, text is sufficient.

The backend converts browser payloads into runtime input.

Its concern is:

```text
transport mechanics
```

not:

```text
finance meaning
```

---

## 13. Step 3 — Host recognizes the domain

Inside the live session, the Host Agent sees that the request belongs to the stock domain.

It decides:

```text
delegate to Stock Specialist
```

The host uses discovered specialist information to make this routing decision.

It should not parse or normalize the ticker itself.

---

## 14. Step 4 — Delegate the natural-language request

The source deliberately keeps delegation broad.

The host passes:

```text
specialist name
+
original natural-language request
```

It does not prematurely convert the request into:

```json
{"symbol": "NVDA"}
```

Why?

Because ticker interpretation is domain reasoning.

It belongs to the Stock Specialist.

### Principle

> Route broadly at the host; interpret narrowly at the specialist.

This preserves useful responsibility boundaries.

---

## 15. Step 5 — Host crosses the A2A boundary

The delegation helper sends an A2A message to the Stock Specialist.

At this point:

```text
local host orchestration
```

becomes:

```text
remote/inter-service agent work
```

The specialist is now responsible for the stock request.

---

## 16. Step 6 — Specialist narrows the request and calls MCP

The Stock Specialist interprets:

```text
"Nvidia"
or
"NVDA"
```

and decides on the symbol.

Only now does the workflow narrow to:

```text
get_stock_price(symbol="NVDA")
```

The MCP Server:

- validates/normalizes symbol,
- tries provider path,
- returns structured data,
- labels fallback/unavailable cases.

This is the correct layer for provider behavior.

---

## 17. Step 7 — Preserve structured domain results

The Specialist should not throw away useful metadata.

The source emphasizes preserving fields such as:

```text
source
as_of
warning
fallback
unavailable
```

These fields matter because a user may otherwise hear fallback data as if it were live provider data.

### Bad architecture

```text
tool returns fallback
specialist converts to clean prose
host loses warning
user hears false certainty
```

### Better

```text
structured result
    ↓
metadata preserved
    ↓
host/model can speak honestly
    ↓
browser can display provenance
```

---

## 18. Step 8 — ADK Live returns text, audio, and events

The Host passes the structured result back into the live runtime.

The backend then shapes runtime output into browser-facing events.

Possible event types include:

- text,
- audio,
- transcripts,
- completion,
- interruption,
- errors,
- provenance,
- host-side function events when available.

The browser displays those events.

It does not reconstruct the distributed execution itself.

[[IMAGE_NEEDED: Full NVDA round trip | Browser -> Backend -> ADK Live Host -> A2A Stock Specialist -> MCP Stock Tool -> provider/fallback, then structured result returns back through Specialist -> Host -> Backend -> Browser as text/audio/provenance | Learner should trace the whole system without confusing responsibility boundaries]]

---

## 19. Boundaries are also your debugging map

Each boundary answers a different question.

### Page does not load

Check:

```text
frontend service
static assets
config endpoint
```

### WebSocket fails

Check:

```text
/config.json
backend
allowed origins
/live route
```

### Host does not delegate

Check:

```text
specialist discovery
host routing instructions
```

### A2A response malformed

Check:

```text
specialist
A2A collector
structured part handling
```

### Quote unavailable

Check:

```text
MCP Server
provider path
fallback path
```

A distributed system becomes easier to debug when ownership is explicit.

---

## 20. Browser activity is not distributed tracing

The browser can display useful activity:

```text
listening
thinking
delegating
answering
```

But that does not automatically prove:

```text
A2A Task internals
MCP tool internals
provider events
```

Those occur in separate services.

If you need full proof, add:

- correlated logs,
- trace IDs,
- explicit instrumentation.

### UI principle

> Show users meaningful progress, not raw protocol machinery.

---

## 21. The Chapter 12 app is intentionally bounded

The reference app is not presented as production-complete.

It uses simplifications such as:

- local processes,
- in-memory session state,
- configured specialist URLs,
- static stock/weather routing,
- fast A2A response path,
- deterministic fallback stock data,
- deterministic mock weather,
- no production authorization,
- no durable Task workspace.

These limits are intentional.

They keep the architectural handoffs visible.

---

## 22. Anti-patterns in the bounded reference architecture

The source highlights several.

### Do not attach every tool directly to the host

That recreates a monolith.

### Do not parse domain entities in the host

That weakens specialist boundaries.

### Do not hide fallback/mock data

Users need honest data-quality labels.

### Do not treat browser diagnostics as distributed tracing

Deeper boundaries require explicit instrumentation.

### Do not treat A2A like a local function call

Network calls need:

- timeouts,
- failure handling,
- later durable lifecycle for long work.

### Do not expose raw protocol vocabulary in the UI

Users need understandable state, not implementation jargon.

---

## 23. The next problem is time

The Chapter 12 request is bounded.

A stock quote can fit inside one live turn.

But what about:

```text
50-page research report
large file processing
website crawling
paid dataset approval
compliance review
multi-source analysis
```

These can take:

```text
seconds
minutes
hours
days
weeks
```

Now the architecture must survive time.

That is the focus of Chapter 13.

---

## 24. Long-running work is not a slow function call

A common beginner mental model is:

```python
result = await agent.run(user_request)
```

For small tasks, fine.

For long work, dangerous.

If one request stays open for 20 minutes:

- infrastructure may time out,
- browser may disconnect,
- worker stays occupied,
- UI looks frozen,
- retries may duplicate work,
- process restart may lose state.

The source's key shift is:

> Long-running work is a task with identity and lifecycle.

[[IMAGE_NEEDED: Blocking request vs durable task | Left: browser holds one request open while remote work runs; right: browser submits work, receives task ID, connection closes, task continues in durable store, UI reconnects for updates | Learner should see why task identity replaces request lifetime]]

---

## 25. The task becomes the unit of reliability

A durable task needs more than an ID.

It needs:

```text
identity
state
progress
ownership
persistence
cancellation
retention
recovery
```

A typical task record may connect:

```text
user
session
workflow
remote agent
remote A2A task
MCP operation/task
result artifact
```

The source states the core idea:

```text
request starts the work
task owns the work
```

This changes the architecture fundamentally.

---

## 26. Explicit task states

The source includes states such as:

```text
submitted
working
input_required
auth_required
completed
failed
canceled
expired
```

These states help the application decide:

```text
wait
resume
ask user
request auth
show result
show error
stop
```

A state machine is not decorative.

It is how different services agree on workflow meaning.

---

## 27. ADK, A2A, MCP: separate responsibilities

The source explicitly separates three layers.

### ADK

Manages:

- local agent session,
- tool invocation,
- event flow,
- working context,
- local confirmation/long-running tool features where supported.

### A2A

Manages:

- remote agent delegation,
- remote Task identity,
- Messages,
- status updates,
- polling,
- streaming,
- push notification patterns.

### MCP

Manages:

- Host-to-tool-server capabilities,
- tool/resource/prompt interactions,
- progress/cancellation utilities,
- task-style features where supported.

### Application durable state

Connects all of them.

It stores:

```text
local workflow ID
session ID
remote A2A task IDs
MCP operation IDs
correlation metadata
```

### Principle

> Protocols expose lifecycle signals; the application still owns the durable cross-boundary workflow.

[[IMAGE_NEEDED: ADK A2A MCP responsibility layers | Local ADK session on left, remote A2A agent task in middle, MCP tool operation on right, with one Durable Application State layer underneath mapping all IDs | Learner should see that no single protocol owns the whole workflow]]

{{exercise:M01.L08.EX02}}

---

## 28. Protect the async event loop

Many agent servers use asynchronous runtimes.

Async works because operations yield control while waiting.

Good:

```python
await async_http_call()
```

Bad:

```python
time.sleep(30)
```

inside the event loop.

Blocking operations can freeze the entire process.

### Rule

> Do not run blocking work directly on the event loop.

For short unavoidable blocking operations:

- thread pool for blocking I/O,
- process pool for CPU-heavy work.

For truly long work:

```text
durable task / worker system
```

not merely a thread.

---

## 29. Separate task initiation from task completion

For a 20-minute report:

### Initiation phase

```text
validate request
create task/workflow ID
persist mapping to user/session
start external/background work
return immediately
```

### Completion phase

Later:

```text
receive/retrieve task update
validate ownership
persist new state
attach result
resume local agent if needed
notify UI
```

The original network request does not need to remain alive.

---

## 30. In-memory state is not enough for production

In-memory stores are useful for learning.

They fail when:

```text
process restarts
container moves
server crashes
user returns later
```

Production long-running work needs durable storage.

Examples:

- relational database,
- durable workflow store,
- appropriately configured Redis.

The same principle applies to:

- tasks,
- agent sessions,
- approval state,
- artifact references.

A paused workflow must not depend on a live Python object.

---

## 31. ADK long-running tools should return a receipt

The source discusses ADK long-running tool support.

The architectural rule is more important than the specific API.

A long-running tool should:

```text
start or reference external work
return a job/task receipt
```

It should not:

```text
perform 30 minutes of work inline
```

Examples:

```text
start report job -> job_id
create approval ticket -> pending
start cloud export -> operation_id
```

The actual work belongs in:

- worker queue,
- remote agent,
- workflow engine,
- cloud job,
- MCP task-capable service.

---

## 32. Preserve original function-call identity

When a long-running result returns later, the system needs to correlate it with the original function call.

Useful identifiers include:

```text
function_call_id
session_id
invocation_id
workflow_id
remote A2A task ID
MCP operation/task ID
```

But the source emphasizes:

> Workflow/task IDs do not replace the original function-call identity when the framework expects that identity for resumption.

This prevents the model/runtime from reconstructing a past operation incorrectly.

---

## 33. A2A delegation should return quickly for long work

When a remote A2A agent receives long work, the caller should not necessarily wait for completion.

Conceptually:

```text
Orchestrator
   ↓ submit
Remote Agent
   ↓
Task created
   ↓ immediate receipt
Orchestrator persists remote Task ID
```

Then updates arrive later.

### Critical durability rule

> Persist the remote Task mapping before depending on future updates.

Otherwise a crash between:

```text
remote task created
```

and:

```text
local mapping saved
```

can orphan the work.

---

## 34. Polling for remote progress

Polling is the simplest update strategy.

```text
Client
  ↓ status?
Server
  ↓ working

wait

Client
  ↓ status?
Server
  ↓ completed
```

Good when:

- task is not ultra-time-sensitive,
- inbound webhooks are difficult,
- simplicity matters.

Use:

- backoff,
- adaptive intervals.

Do not hammer the remote agent every second for a multi-hour task.

---

## 35. Streaming and subscription

Streaming is useful when the caller wants immediate visibility.

Possible updates:

- Task status,
- partial Message,
- Artifact update,
- progress.

But the source makes an important distinction:

> A stream is visibility, not durable state.

If the stream disconnects, the application must still recover from persisted Task state.

---

## 36. Push notifications and webhooks

With push:

```text
Orchestrator provides callback
Remote Agent works
Remote Agent sends update later
```

A production callback receiver should:

1. authenticate sender,
2. validate task/context IDs,
3. validate expected remote agent,
4. check duplicate/out-of-order updates,
5. persist update,
6. resume/update workflow if needed,
7. return fast acknowledgment.

Avoid expensive work inside the webhook handler.

Enqueue follow-up processing instead.

[[IMAGE_NEEDED: Polling vs streaming vs push for A2A tasks | Polling timeline, persistent streaming updates, and webhook callback pattern, all pointing into one durable task store | Learner should understand delivery mechanism is separate from state ownership]]

---

## 37. MCP long-running work

Some MCP tool operations can also be long-running.

Examples:

- large exports,
- file transformations,
- indexing,
- expensive computation.

The durable pattern remains:

```text
start work
persist task identity
return receipt
fetch/update later
```

The source warns that MCP task-style capabilities are version/capability-dependent.

Do not assume every MCP Server supports them.

---

## 38. Human-in-the-loop is asynchronous suspension

Some workflows wait because of people, not computation.

Examples:

- approve payment,
- choose target environment,
- authorize paid dataset,
- answer compliance question.

The correct pattern:

```text
reach decision point
persist workflow
store pending prompt
release resources
wait
receive correlated response
resume
```

Do not leave the original request blocked for hours.

---

## 39. Tool confirmation still needs durable correlation

Framework confirmation features can simplify approval prompts.

But production design still needs:

- persistent state,
- correlation ID,
- idempotency,
- expiration,
- ownership checks.

If the user clicks "approve" twice, the system must not execute the sensitive action twice.

The approval must map to the exact original operation.

---

## 40. Authentication can also pause a workflow

Long-running work may reach a protected service after the user's token expires.

The workflow should:

1. detect missing/expired credentials,
2. transition to `auth_required`,
3. store pending operation,
4. present an authorization flow,
5. resume after valid credentials return,
6. re-check authorization before the sensitive action.

Do not assume credentials remain valid simply because the task started while the user was authenticated.

---

## 41. Distributed input-required requests

A remote A2A agent or MCP service may need user input after the original connection is gone.

Example:

```text
Migration tool needs target environment.
```

The task should become:

```text
input_required
```

and persist:

- prompt,
- schema,
- correlation ID.

The frontend renders the request.

The user responds.

The correlated response resumes the workflow.

[[IMAGE_NEEDED: Human-input suspension sequence | Background task -> input_required -> durable store + prompt -> frontend form -> user response with correlation ID -> task resumes | Learner should see that human interaction is modeled as task state, not a held-open request]]

---

## 42. Streams are not state

This is one of the most important production rules in Chapter 13.

A stream can disappear because:

- browser refresh,
- mobile network loss,
- server restart,
- proxy interruption.

Therefore:

```text
stream = real-time visibility
durable store = source of truth
```

A resilient frontend can reconnect and rebuild from persisted state.

---

## 43. Structured progress reporting

Bad progress:

```text
"Still working..."
```

Better:

```json
{
  "phase": "processing_documents",
  "current": 37,
  "total": 120,
  "message": "Processing annual_report_2024.pdf"
}
```

Structured progress lets the UI render:

- progress bar,
- phase,
- current item,
- activity log.

It also helps operations teams measure where workflows spend time.

### Avoid event floods

Do not emit progress for every tiny internal step.

Prefer meaningful milestones.

{{exercise:M01.L08.EX03}}

---

## 44. Cancellation must propagate

If the user presses Cancel, hiding progress is not enough.

The cancellation path may be:

```text
Frontend
  ↓
Application backend
  ↓
local workflow -> canceling
  ↓
A2A remote task cancellation
  ↓
MCP operation cancellation where supported
  ↓
worker cleanup
  ↓
final state: canceled
```

Remote workers should clean up:

- files,
- sockets,
- cursors,
- partial artifacts.

---

## 45. Disconnect is not cancellation

Closing a browser tab may mean:

```text
"I'll come back later."
```

It does not necessarily mean:

```text
"Stop the work."
```

Only explicit cancel intent should terminate underlying work.

This is another reason task state must outlive browser connections.

---

## 46. Timeouts, expiration, and retention are different

Production workflows need several different time controls.

### Request timeout

How long one network request may remain open.

### Task timeout

How long the work itself may run.

### Result retention

How long completed artifacts are kept.

### Approval expiration

How long a pending human decision remains valid.

### Polling interval

How often callers check status.

### Retry policy

Which failures can be retried and how often.

These solve different problems and should not be collapsed into one number.

---

## 47. Ghost tasks need a stale-task sweeper

A ghost task occurs when:

```text
local workflow thinks work is pending
```

but:

```text
remote worker disappeared
```

A sweeper should periodically:

1. find non-terminal tasks,
2. compare last update to task TTL,
3. check whether remote state can still be retrieved,
4. mark unrecoverable tasks failed/timed out,
5. notify/resume local workflow,
6. emit logs/metrics.

No user should wait forever because a worker silently died.

---

## 48. Idempotency is the hidden requirement

Asynchronous systems retry.

Duplicates happen because:

- networks retry,
- webhooks deliver twice,
- user double-clicks,
- streams reconnect,
- polling overlaps with push,
- workers repeat messages.

Without idempotency, the system may:

- create duplicate reports,
- charge twice,
- send duplicate emails,
- repeat destructive actions.

### Idempotency key

The key should represent user intent.

Example:

```text
generate report
for session X
request Y
```

Repeated transport requests should map to the same durable task.

---

## 49. Validate every incoming task update

Before applying an update, ask:

```text
Have I seen this event before?
Is it newer than current state?
Is this state transition valid?
Does this Task belong to expected user/session?
Is the Task already terminal?
```

Duplicate delivery should be normal.

Correct behavior:

```text
acknowledge
ignore duplicate effect
```

not:

```text
repeat side effect
```

[[IMAGE_NEEDED: Idempotent update handler | Incoming event -> verify sender -> check event ID -> load workflow -> validate ownership/state transition -> apply once -> resume if terminal/suspended | Learner should see duplicate delivery as expected rather than exceptional]]

{{exercise:M01.L08.EX04}}

---

## 50. Distributed workflows require correlation

A single request may touch:

```text
frontend
backend
ADK
A2A agent
MCP client
MCP server
worker
external API
webhook
session resume
frontend stream
```

Without correlation, logs are isolated islands.

Useful metadata includes:

```text
user / tenant ID
session ID
invocation ID
workflow ID
remote A2A task ID
MCP operation/task ID
trace ID
idempotency key
parent task ID
```

A state transition log should include:

```text
old state
new state
task ID
session
remote agent
trace ID
timestamp
```

This makes post-incident analysis possible.

---

## 51. Trace context should cross protocol boundaries

The source mentions distributed tracing systems such as OpenTelemetry.

Where possible:

```text
propagate trace context
```

Across boundaries where that is not possible:

```text
include correlation IDs in structured logs
```

### Important distinction

The user UI should not expose all of this machinery.

Observability is for engineers.

User-facing progress should stay understandable.

---

## 52. Long-running workflows expand the security surface

A long task may continue after:

- user disconnects,
- token expires,
- work moves to another worker.

Therefore authorization cannot depend only on the original live session.

The system should store:

```text
authorization context
```

not merely a long-lived raw token.

Before sensitive actions:

```text
re-check permission
```

For machine-to-machine callbacks:

- service identities,
- signed payloads,
- private networking,
- mTLS where appropriate.

Secrets should not appear in:

- task IDs,
- URLs,
- logs,
- progress text.

---

## 53. Frontend responsiveness needs recoverable state

A long-running UI should immediately acknowledge work.

Example:

```text
"I've started generating the report."
```

Then show meaningful states:

```text
Collecting sources...
Reading documents...
Drafting summary...
Preparing final report...
```

If the page refreshes, the UI should fetch current task state and rebuild.

### Event-reducer model

Frontend events can reduce into local state:

```text
task_created
progress_update
artifact_update
input_required
completed
failed
canceled
```

Polling, streaming, and push can all produce the same internal update events.

This decouples UI rendering from transport choice.

---

## 54. Prevent duplicate submissions

Once a task starts:

- disable or distinguish the submit button,
- show existing task state.

If the same intent arrives again:

```text
idempotency key
    ↓
return existing task
```

rather than:

```text
create another expensive task
```

The frontend helps.

The backend must enforce it.

---

## 55. End-to-end long-running market report

The source uses a larger example:

```text
Create a 50-page market research report
on battery storage companies,
including a competitive landscape table.
```

This is a good example because it requires:

- delegation,
- tool work,
- progress,
- possible paid-data approval,
- durable artifacts.

---

## 56. Step 1 — Start or retrieve the local session

The frontend submits the request.

The backend:

- creates/retrieves the ADK session,
- appends user request,
- lets the agent determine that the work is too large for one immediate response.

The system transitions from:

```text
live turn
```

to:

```text
durable workflow
```

---

## 57. Step 2 — Create the durable workflow record

The backend creates something conceptually like:

```text
workflow_id = wf_123
session_id = session_456
user_id = user_789
state = starting
```

This becomes the user-facing durable handle.

It exists independently from:

- browser tab,
- network connection,
- one process.

---

## 58. Step 3 — Delegate to remote research agent

The orchestrator submits the research request through A2A.

The remote agent creates:

```text
research_task_abc
```

The local workflow must store that mapping immediately:

```text
wf_123
   ↔
research_task_abc
```

before waiting for future updates.

This is essential for recovery.

---

## 59. Step 4 — Remote agent uses MCP tools

The research agent may use MCP Servers for:

- document search,
- file processing,
- data retrieval.

Some MCP calls finish quickly.

Others may start longer operations where supported.

The remote agent manages those tool-level details and reports useful progress upward through A2A.

---

## 60. Step 5 — Progress reaches the user

The frontend might show:

```text
Research started
Sources identified
Sources reviewed
Landscape drafted
Outline completed
```

If the user disconnects:

```text
workflow continues
```

When they return:

```text
frontend fetches workflow state
rebuilds progress
```

This is the practical benefit of durable task identity.

---

## 61. Step 6 — Human approval pauses the workflow

Suppose a paid dataset is available.

The workflow becomes:

```text
input_required
```

The backend stores:

- approval prompt,
- correlation ID,
- expiration.

The user chooses:

```text
skip paid source
```

The response is correlated with the pending operation.

The workflow resumes safely.

---

## 62. Step 7 — Final Artifact arrives

The remote research agent completes the report.

The orchestrator:

1. validates update,
2. checks ownership/correlation,
3. stores Artifact,
4. updates workflow state,
5. appends result to ADK session,
6. resumes local agent,
7. notifies user.

The final user experience may be:

```text
summary + report link
```

---

## 63. Step 8 — Cleanup and retention

After completion:

- mark workflow completed,
- retain Artifact according to policy,
- retain task metadata as required,
- delete temporary files,
- keep metrics/traces,
- release resources.

A task is not truly complete until cleanup rules have been applied.

[[IMAGE_NEEDED: Long-running market report lifecycle | Live request -> workflow record -> A2A research task -> MCP tools -> progress -> input_required approval -> resume -> final Artifact -> cleanup/retention | Learner should see the full durable lifecycle across all protocol boundaries]]

{{exercise:M01.L08.EX05}}

---

## 64. Long-running workflow anti-patterns

The source highlights several common mistakes.

### Holding the original request open

Long work should outlive the initiating request.

### Treating stream as storage

A disconnected stream must not erase workflow state.

### Keeping task state only in memory

Process restart must not destroy active work.

### Assuming webhook exactly-once delivery

Duplicates and reordering must be tolerated.

### Assuming cancellation always succeeds

Some operations cross an irreversible point.

### Reconstructing approved operations from scratch

Resume with original correlation/function identity.

### Depending on private SDK internals

Architecture should survive SDK changes.

### Assuming MCP Tasks exist everywhere

Treat task-style support as negotiated/capability-dependent.

---

## 65. Production checklist

### State

- persistent ADK sessions,
- durable workflow records,
- durable task store,
- local ↔ remote task mappings.

### Delivery

- structured progress,
- polling/streaming/push strategy,
- retry policy,
- fast webhook acknowledgment.

### Safety

- idempotency keys,
- cancellation path,
- timeout/expiration,
- stale-task sweeper.

### Observability

- correlation IDs,
- trace propagation,
- structured task-state logs,
- metrics.

### UX

- immediate acknowledgment,
- visible progress,
- approval/input-required state,
- refresh/reconnect recovery.

### Security

- authenticated callbacks,
- authorization re-check,
- careful task ID exposure,
- approval expiry,
- credential handling.

{{exercise:M01.L08.EX06}}

---

## 66. Source-specific implementation details to re-check

Both chapters explicitly warn that these ecosystems evolve quickly.

Verify current documentation for:

- ADK Live APIs,
- Gemini Live event shapes,
- A2A SDK helpers,
- Agent Card routes,
- MCP Streamable HTTP support,
- long-running ADK tool APIs,
- confirmation APIs,
- non-blocking A2A send configuration,
- MCP task-style capabilities,
- push notification schemas,
- cancellation APIs,
- model names,
- package pins.

The durable architecture is more important than exact helper names.

---

## 67. Complete mental model

The two chapters fit together naturally.

### Bounded live turn

```text
Browser
  ↓
Backend / ADK Live
  ↓
Host Agent
  ↓
A2A Specialist
  ↓
MCP Tool
  ↓
structured result
  ↓
Host
  ↓
spoken/text answer
```

### Long-running extension

```text
Live request
  ↓
durable workflow ID
  ↓
remote A2A Task ID
  ↓
MCP operations
  ↓
progress events
  ↓
optional human/auth suspension
  ↓
resume
  ↓
final Artifact
  ↓
cleanup + retention
```

The user still experiences:

```text
one assistant
```

But the system is reliable because each boundary has:

```text
clear ownership
durable identity
recoverable state
honest progress
correlation
security
```

This is what allows an intelligent system to remain dependable when the work becomes slow, distributed, interruptible, or human-dependent.

---

## Important misconceptions

### Misconception 1
> "The live host should normalize every domain entity before delegation."

No. Domain interpretation belongs to the specialist whenever possible.

### Misconception 2
> "The browser should infer provenance from final answer text."

No. Provenance and fallback status should travel as structured metadata.

### Misconception 3
> "Browser activity events prove the full A2A/MCP execution trace."

No. Deeper service activity requires explicit instrumentation and correlation.

### Misconception 4
> "A long-running task is just a normal function call with a larger timeout."

No. It needs durable identity, state, progress, cancellation, and recovery.

### Misconception 5
> "Keeping the stream open makes task state durable."

No. Streams are transport/visibility, not the source of truth.

### Misconception 6
> "In-memory task state is acceptable for production long-running work."

No. Process restart would lose active task identity and recovery state.

### Misconception 7
> "An ADK long-running tool should perform the whole hour-long operation inside the agent process."

No. It should initiate or reference durable external work and return a receipt.

### Misconception 8
> "A remote A2A task ID can be stored later."

No. Persist the mapping immediately before depending on future updates.

### Misconception 9
> "Streaming replaces polling or state retrieval."

No. Streaming improves responsiveness; durable state supports recovery.

### Misconception 10
> "Human approval is a special UI feature, not part of workflow state."

No. It is an asynchronous suspension point that needs persistence and correlation.

### Misconception 11
> "Closing a browser should cancel the underlying task."

No. Disconnect and cancellation are different intents.

### Misconception 12
> "Webhook delivery happens exactly once."

No. Duplicate and out-of-order delivery must be expected.

### Misconception 13
> "Cancellation means every remote side effect can always be undone."

No. Some operations may pass an irreversible point.

### Misconception 14
> "One timeout value can control every aspect of a long-running workflow."

No. Request timeout, task timeout, approval expiry, retention, retries, and polling intervals solve different problems.

### Misconception 15
> "Task IDs alone make a workflow observable."

No. You need correlation across session, workflow, remote task, operation, trace, and idempotency identifiers.

### Misconception 16
> "Authorization checked at task creation is enough for a multi-hour workflow."

No. Sensitive actions may need authorization re-checks later.

### Misconception 17
> "If a progress stream reconnects, every missed update is guaranteed to replay."

No. Recovery should rely on durable state, with replay only where supported.

### Misconception 18
> "MCP long-running task features should be assumed available everywhere."

No. Treat them as capability- and version-dependent.

---

## Key terminology

| Term | Meaning |
|---|---|
| Live Host | User-facing agent handling conversation and routing |
| A2A Specialist | Domain-focused remote agent service |
| MCP Tool Server | External capability service exposing tools |
| Provenance | Metadata describing data source and freshness/quality |
| Fallback | Explicit alternate result used when primary provider path fails |
| Bounded live turn | Request that reasonably completes within one conversational exchange |
| Durable workflow | Persisted orchestration state that survives disconnects/restarts |
| Task ID | Stable handle identifying long-running work |
| Workflow ID | Application-owned identifier connecting task state to user/session |
| Task state machine | Explicit states such as working, input_required, completed, failed |
| Persistent task store | Durable storage for task metadata and status |
| Non-blocking delegation | Submit remote work and return before completion |
| Polling | Periodic task-state retrieval |
| Streaming | Real-time update delivery over a live connection |
| Push notification | Server-initiated callback update |
| Suspension | Persisted pause awaiting human input or authentication |
| Correlation ID | Identifier linking a later response/update to the original operation |
| Function call ID | Runtime identity of the original tool invocation |
| Progress event | Structured update describing task phase/completion |
| Cancellation propagation | Sending cancel intent through all owning layers |
| Ghost task | Task believed pending after its worker disappeared |
| Sweeper | Background process that identifies stale/expired work |
| Idempotency | Ability to safely process retries/duplicates without repeating effects |
| Idempotency key | Stable key representing one user intent |
| Terminal state | Completed, failed, canceled, or another state where work is finished |
| Artifact | Durable work result such as report/file |
| Distributed tracing | Correlated observability across services |
| Trace ID | Identifier linking events across boundaries |
| Authorization context | Persisted permission context used for later re-checks |
| Recoverable frontend state | UI state rebuildable from backend task source of truth |

---

## Self-check

1. Why should the live host remain narrow?
2. Which layer should understand ticker aliases?
3. Which layer should own provider fallback logic?
4. Why should provenance be structured?
5. What are the responsibilities of the Browser UI?
6. What are the responsibilities of the backend?
7. Why does the host delegate natural language rather than a pre-parsed ticker?
8. What does the A2A specialist do before calling MCP?
9. How can service boundaries help debugging?
10. Why is browser activity not distributed tracing?
11. Which Chapter 12 simplifications make it intentionally non-production?
12. Why is a long-running task not just a slow function call?
13. What information should a durable task record contain?
14. Why does the task become the unit of reliability?
15. What belongs to ADK?
16. What belongs to A2A?
17. What belongs to MCP?
18. What still belongs to application durable state?
19. Why must blocking work stay off the async event loop?
20. When is a thread pool appropriate?
21. Why are threads not a durable solution for an hour-long task?
22. What happens during task initiation?
23. What happens during task completion?
24. Why are in-memory stores inadequate for production long work?
25. What should a long-running ADK tool return?
26. Why preserve the original function-call identity?
27. When should a remote A2A Task ID be persisted?
28. When is polling a good update strategy?
29. What is streaming good for?
30. Why is streaming not the source of truth?
31. What does a push receiver need to validate?
32. Why should webhook handlers acknowledge quickly?
33. How should MCP long-running work be modeled?
34. Why is human approval an asynchronous suspension?
35. How is authentication also a suspension state?
36. How should distributed input_required behavior work?
37. What makes a good structured progress event?
38. How should cancellation propagate?
39. Why is browser disconnect different from cancellation?
40. What is the difference between request timeout and task timeout?
41. What is a ghost task?
42. What does a sweeper do?
43. Why does asynchronous work require idempotency?
44. What should an update handler check before changing state?
45. Which correlation identifiers are useful across the stack?
46. Why may authorization need to be re-checked later?
47. How should frontend state recover after refresh?
48. Trace the market-report workflow from submission through final Artifact.
49. What cleanup should happen after completion?
50. Which SDK/protocol details from these chapters are version-sensitive?

---

## Retain this idea

**A robust integrated agent system separates live conversation, domain reasoning, and tool execution into bounded services, then adds durable workflow state when work can outlive a single turn. The browser should remain a presentation layer, the live host should route rather than absorb domain rules, specialists should interpret domain requests, and MCP servers should own provider/tool behavior. When work becomes long-running, the request stops being the unit of reliability: the durable task becomes the unit of reliability, with explicit identity, progress, persistence, suspension, cancellation, idempotency, observability, security, and recovery across every boundary.**
""".strip(),

        "sections": [
            {"id": "architecture-collapse", "title": "Why the Live Agent Must Not Own Everything", "order": 1},
            {"id": "integrated-system", "title": "The Integrated Reference System", "order": 2},
            {"id": "browser-ui", "title": "Browser UI Responsibilities", "order": 3},
            {"id": "frontend-service", "title": "Frontend Service Responsibilities", "order": 4},
            {"id": "live-backend", "title": "FastAPI Backend and ADK Live Host Process", "order": 5},
            {"id": "host-agent", "title": "The ADK Host Agent Owns User-Facing Intent", "order": 6},
            {"id": "specialists", "title": "A2A Specialists Own Domain Interpretation", "order": 7},
            {"id": "mcp-server", "title": "The MCP Tool Server Owns Provider Access", "order": 8},
            {"id": "ownership-map", "title": "Responsibility Boundaries as an Architectural Contract", "order": 9},
            {"id": "stock-request", "title": "Walk the NVDA Request End to End", "order": 10},
            {"id": "browser-config", "title": "Browser Loads Config", "order": 11},
            {"id": "browser-backend", "title": "Browser Sends Live Input", "order": 12},
            {"id": "host-routing", "title": "Host Recognizes the Domain", "order": 13},
            {"id": "natural-language-delegation", "title": "Delegate the Natural-Language Request", "order": 14},
            {"id": "a2a-hop", "title": "Host Crosses the A2A Boundary", "order": 15},
            {"id": "mcp-hop", "title": "Specialist Calls MCP", "order": 16},
            {"id": "structured-result", "title": "Preserve Structured Domain Results", "order": 17},
            {"id": "live-return", "title": "ADK Live Returns Text, Audio, and Events", "order": 18},
            {"id": "boundary-debugging", "title": "Boundaries Are Also Your Debugging Map", "order": 19},
            {"id": "browser-not-tracing", "title": "Browser Activity Is Not Distributed Tracing", "order": 20},
            {"id": "bounded-app", "title": "The Chapter 12 App Is Intentionally Bounded", "order": 21},
            {"id": "chapter12-antipatterns", "title": "Anti-Patterns in the Bounded Reference Architecture", "order": 22},
            {"id": "time-problem", "title": "The Next Problem Is Time", "order": 23},
            {"id": "slow-function-fails", "title": "Long-Running Work Is Not a Slow Function Call", "order": 24},
            {"id": "task-unit", "title": "The Task Becomes the Unit of Reliability", "order": 25},
            {"id": "task-state-machine", "title": "Explicit Task States", "order": 26},
            {"id": "three-boundaries", "title": "ADK, A2A, MCP: Separate Responsibilities", "order": 27},
            {"id": "event-loop", "title": "Protect the Async Event Loop", "order": 28},
            {"id": "persistent-task", "title": "Separate Task Initiation from Task Completion", "order": 29},
            {"id": "persistent-storage", "title": "In-Memory State Is Not Enough for Production", "order": 30},
            {"id": "adk-long-running", "title": "ADK Long-Running Tools Should Return a Receipt", "order": 31},
            {"id": "function-call-identity", "title": "Preserve Original Function-Call Identity", "order": 32},
            {"id": "a2a-long-work", "title": "A2A Delegation Should Return Quickly for Long Work", "order": 33},
            {"id": "polling", "title": "Polling for Remote Progress", "order": 34},
            {"id": "streaming", "title": "Streaming and Subscription", "order": 35},
            {"id": "push", "title": "Push Notifications and Webhooks", "order": 36},
            {"id": "mcp-long-work", "title": "MCP Long-Running Work", "order": 37},
            {"id": "human-suspension", "title": "Human-in-the-Loop Is Asynchronous Suspension", "order": 38},
            {"id": "tool-confirmation", "title": "Tool Confirmation Still Needs Durable Correlation", "order": 39},
            {"id": "auth-suspension", "title": "Authentication Can Also Pause a Workflow", "order": 40},
            {"id": "distributed-input", "title": "Distributed Input-Required Requests", "order": 41},
            {"id": "streams-not-state", "title": "Streams Are Not State", "order": 42},
            {"id": "progress", "title": "Structured Progress Reporting", "order": 43},
            {"id": "cancellation", "title": "Cancellation Must Propagate", "order": 44},
            {"id": "disconnect-vs-cancel", "title": "Disconnect Is Not Cancellation", "order": 45},
            {"id": "timeouts", "title": "Timeouts, Expiration, and Retention Are Different", "order": 46},
            {"id": "ghost-tasks", "title": "Ghost Tasks Need a Stale-Task Sweeper", "order": 47},
            {"id": "idempotency", "title": "Idempotency Is the Hidden Requirement", "order": 48},
            {"id": "update-validation", "title": "Validate Every Incoming Task Update", "order": 49},
            {"id": "observability", "title": "Distributed Workflows Require Correlation", "order": 50},
            {"id": "otel", "title": "Trace Context Should Cross Protocol Boundaries", "order": 51},
            {"id": "security-long-work", "title": "Long-Running Workflows Expand the Security Surface", "order": 52},
            {"id": "frontend-state", "title": "Frontend Responsiveness Needs Recoverable State", "order": 53},
            {"id": "duplicate-submission", "title": "Prevent Duplicate Submissions", "order": 54},
            {"id": "market-report", "title": "End-to-End Long-Running Market Report", "order": 55},
            {"id": "market-step1", "title": "Start or Retrieve the Local Session", "order": 56},
            {"id": "market-step2", "title": "Create the Durable Workflow Record", "order": 57},
            {"id": "market-step3", "title": "Delegate to Remote Research Agent", "order": 58},
            {"id": "market-step4", "title": "Remote Agent Uses MCP Tools", "order": 59},
            {"id": "market-step5", "title": "Progress Reaches the User", "order": 60},
            {"id": "market-step6", "title": "Human Approval Pauses the Workflow", "order": 61},
            {"id": "market-step7", "title": "Final Artifact Arrives", "order": 62},
            {"id": "market-step8", "title": "Cleanup and Retention", "order": 63},
            {"id": "long-work-antipatterns", "title": "Long-Running Workflow Anti-Patterns", "order": 64},
            {"id": "production-checklist", "title": "Production Checklist", "order": 65},
            {"id": "source-boundaries", "title": "Source-Specific Details to Re-Check", "order": 66},
            {"id": "complete-mental-model", "title": "Complete Mental Model", "order": 67},
        ],
    },

    "exercises": [
        {
            "id": "M01.L08.EX01",
            "title": "Assign Responsibilities to the Correct Layer",
            "lesson_code": "M01.L08",
            "section_id": "ownership-map",
            "placement": "after_section",
            "description": "Practice preserving service boundaries in the Chapter 12 reference architecture.",
            "instructions": (
                "For each responsibility, assign it to Browser UI, Frontend Service, Backend/ADK Live, "
                "Host Agent, A2A Specialist, or MCP Tool Server:\n"
                "1. Normalize NVDA ticker input.\n"
                "2. Play generated audio.\n"
                "3. Validate WebSocket origins.\n"
                "4. Choose Stock vs Weather specialist.\n"
                "5. Fetch provider quote and attach fallback metadata.\n"
                "6. Serve /config.json.\n"
                "7. Explain why moving each responsibility one layer upward or downward could create coupling."
            ),
            "expected_output": "A seven-row ownership table with justification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["service-boundaries", "architecture"],
        },
        {
            "id": "M01.L08.EX02",
            "title": "Design a Durable Task Record",
            "lesson_code": "M01.L08",
            "section_id": "three-boundaries",
            "placement": "after_section",
            "description": "Design application-owned state that connects ADK, A2A, and MCP.",
            "instructions": (
                "Design a task record for a long-running research workflow.\n"
                "Include user_id, session_id, workflow_id, status, remote A2A task ID, "
                "MCP operation/task ID where available, progress, artifact references, "
                "correlation IDs, idempotency key, timestamps, cancellation state, and retention metadata.\n"
                "Explain which protocol/runtime owns each external ID and why the application must persist the mapping."
            ),
            "expected_output": "A durable task schema plus an ownership explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["task-lifecycle", "durable-state", "correlation"],
        },
        {
            "id": "M01.L08.EX03",
            "title": "Design Structured Progress",
            "lesson_code": "M01.L08",
            "section_id": "progress",
            "placement": "after_section",
            "description": "Create useful progress events for both users and operators.",
            "instructions": (
                "Design progress updates for a 50-document analysis task.\n"
                "1. Define phases.\n"
                "2. Define current/total counters.\n"
                "3. Include one user-friendly message.\n"
                "4. Include one operator-oriented field.\n"
                "5. Define a policy that prevents excessive event frequency.\n"
                "6. Show how the frontend could reduce progress events into a progress bar and activity log."
            ),
            "expected_output": "A progress-event schema and frontend reduction example.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["progress-reporting", "frontend-state"],
        },
        {
            "id": "M01.L08.EX04",
            "title": "Make a Task Update Handler Idempotent",
            "lesson_code": "M01.L08",
            "section_id": "update-validation",
            "placement": "after_section",
            "description": "Practice safe handling of duplicate and out-of-order asynchronous events.",
            "instructions": (
                "Design a webhook/task-update handler.\n"
                "It must verify sender identity, check event_id duplication, load the expected workflow, "
                "validate ownership, reject invalid state transitions, ignore stale/out-of-order updates, "
                "persist valid changes, and resume the workflow only for valid terminal/suspended states.\n"
                "Explain how the handler responds to the same event arriving twice."
            ),
            "expected_output": "A numbered idempotent update algorithm.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["idempotency", "webhooks", "state-machines"],
        },
        {
            "id": "M01.L08.EX05",
            "title": "Architect the Long-Running Market Report",
            "lesson_code": "M01.L08",
            "section_id": "market-step8",
            "placement": "after_section",
            "description": "Combine durable tasks, A2A, MCP, approval, progress, and artifacts.",
            "instructions": (
                "Design the full market-report workflow from user request to cleanup.\n"
                "1. Define the local workflow record.\n"
                "2. Define the remote A2A task mapping.\n"
                "3. Show MCP tool work inside the remote agent.\n"
                "4. Define three progress events.\n"
                "5. Add one paid-data approval suspension.\n"
                "6. Define cancellation behavior.\n"
                "7. Define final Artifact storage and retention.\n"
                "8. Show how the UI recovers after a browser refresh."
            ),
            "expected_output": "An end-to-end architecture diagram and lifecycle specification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["long-running-tasks", "a2a", "mcp", "human-in-the-loop"],
        },
        {
            "id": "M01.L08.EX06",
            "title": "Production Readiness Review",
            "lesson_code": "M01.L08",
            "section_id": "production-checklist",
            "placement": "after_section",
            "description": "Audit a durable agent workflow before production deployment.",
            "instructions": (
                "Create a readiness table with sections State, Delivery, Safety, Observability, UX, and Security.\n"
                "Add at least four checks to each section.\n"
                "For every failed check, state the failure mode it could cause, such as lost state, duplicate work, "
                "invisible failure, unauthorized callback, or unrecoverable browser refresh."
            ),
            "expected_output": "A production-readiness checklist linked to concrete failure modes.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["production-architecture", "reliability", "security"],
        },
        {
            "id": "M01.L08.EX07",
            "title": "Debug the Integrated Stack",
            "lesson_code": "M01.L08",
            "section_id": "observability",
            "placement": "after_section",
            "description": "Use ownership and correlation IDs to locate failures across the complete architecture.",
            "instructions": (
                "For a user report that never completes, define a debugging sequence across:\n"
                "Browser -> Backend -> ADK Session -> A2A Task -> MCP Operation -> Worker -> Callback.\n"
                "List the identifiers and logs you would inspect at each boundary.\n"
                "Explain how you would distinguish a UI-only problem from a remote task failure."
            ),
            "expected_output": "A distributed debugging runbook with correlation fields.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["observability", "distributed-tracing", "debugging"],
        },
    ],

    "quiz": {
        "id": "M01.L08.QZ01",
        "title": "Integrated Live Agents and Durable Workflows — Knowledge Check",
        "lesson_code": "M01.L08",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L08.Q01",
                "section_id": "architecture-collapse",
                "question": "Why is attaching every domain tool directly to the live host risky?",
                "options": [
                    "It makes the latency-sensitive conversational layer own unrelated domain rules and provider behavior",
                    "It prevents the browser from playing audio",
                    "It makes A2A impossible by definition",
                    "It removes the need for MCP",
                ],
                "correct": 0,
                "explanation": "The source's architecture keeps live interaction separate from domain and provider complexity.",
            },
            {
                "id": "M01.L08.Q02",
                "section_id": "specialists",
                "question": "Which layer should interpret 'Nvidia' as NVDA?",
                "options": ["Stock Specialist", "Browser", "Frontend service", "Generic live backend"],
                "correct": 0,
                "explanation": "Ticker interpretation is stock-domain logic.",
            },
            {
                "id": "M01.L08.Q03",
                "section_id": "mcp-server",
                "question": "Which layer should know whether a quote came from the provider or a deterministic fallback?",
                "options": ["MCP Tool Server", "Browser only", "Frontend static service", "Generic host router"],
                "correct": 0,
                "explanation": "The tool server is the first layer that knows provider success/failure and should attach provenance.",
            },
            {
                "id": "M01.L08.Q04",
                "section_id": "natural-language-delegation",
                "question": "Why does the host pass the original stock request to the specialist instead of only {'symbol':'NVDA'}?",
                "options": [
                    "Domain interpretation belongs to the specialist",
                    "A2A cannot send structured arguments",
                    "The host cannot read text",
                    "MCP requires full sentences",
                ],
                "correct": 0,
                "explanation": "The host routes by domain; the specialist performs domain-specific narrowing.",
            },
            {
                "id": "M01.L08.Q05",
                "section_id": "browser-not-tracing",
                "question": "Why should browser activity not be treated as full distributed tracing?",
                "options": [
                    "A2A and MCP work may happen in separate services that require explicit correlation/instrumentation",
                    "Browsers cannot show any events",
                    "Tracing only applies to databases",
                    "ADK Live automatically hides every event",
                ],
                "correct": 0,
                "explanation": "User-facing activity is not proof of every downstream protocol event.",
            },
            {
                "id": "M01.L08.Q06",
                "section_id": "task-unit",
                "question": "What becomes the unit of reliability for long-running work?",
                "options": ["The durable Task/workflow", "The original HTTP request", "The browser tab", "The LLM prompt"],
                "correct": 0,
                "explanation": "The request may end while work continues; the task owns identity and state.",
            },
            {
                "id": "M01.L08.Q07",
                "section_id": "three-boundaries",
                "question": "What connects ADK, A2A, and MCP lifecycle information into one durable workflow?",
                "options": ["Application-owned persistent state", "The browser DOM", "One long WebSocket", "The model context window"],
                "correct": 0,
                "explanation": "The application must persist mappings and lifecycle state across protocol boundaries.",
            },
            {
                "id": "M01.L08.Q08",
                "section_id": "event-loop",
                "question": "Why should blocking work not run directly on an async event loop?",
                "options": [
                    "It can stall the entire process and prevent other work from progressing",
                    "It always corrupts JSON",
                    "It permanently deletes task state",
                    "It disables A2A discovery",
                ],
                "correct": 0,
                "explanation": "Async runtimes depend on cooperative yielding.",
            },
            {
                "id": "M01.L08.Q09",
                "section_id": "persistent-task",
                "question": "What should happen immediately after starting long-running remote work?",
                "options": [
                    "Persist task/workflow identity and release the initiating request",
                    "Keep the browser request open indefinitely",
                    "Delete the session",
                    "Wait without storing any identifiers",
                ],
                "correct": 0,
                "explanation": "Durable task initiation separates work lifetime from request lifetime.",
            },
            {
                "id": "M01.L08.Q10",
                "section_id": "adk-long-running",
                "question": "What should a long-running ADK tool usually do?",
                "options": [
                    "Start/reference durable external work and return a receipt",
                    "Perform hours of work inline in the agent process",
                    "Keep the WebSocket open until the worker finishes",
                    "Store state only in Python globals",
                ],
                "correct": 0,
                "explanation": "The agent should orchestrate durable work rather than perform it inline.",
            },
            {
                "id": "M01.L08.Q11",
                "section_id": "a2a-long-work",
                "question": "Why persist the remote A2A Task ID immediately?",
                "options": [
                    "So later updates can be correlated even if the local process fails or restarts",
                    "Because Task IDs are required for audio playback",
                    "To avoid using a session ID",
                    "Because MCP needs it as a ticker",
                ],
                "correct": 0,
                "explanation": "The mapping must survive before later asynchronous updates arrive.",
            },
            {
                "id": "M01.L08.Q12",
                "section_id": "streaming",
                "question": "What is streaming primarily used for in long-running workflows?",
                "options": ["Real-time visibility", "Durable storage", "Authorization storage", "Permanent task identity"],
                "correct": 0,
                "explanation": "The source explicitly separates streaming visibility from persistent task state.",
            },
            {
                "id": "M01.L08.Q13",
                "section_id": "human-suspension",
                "question": "How should a workflow wait for human approval?",
                "options": [
                    "Persist the pending state and resume after a correlated response",
                    "Hold the original HTTP request open for days",
                    "Ask the LLM to remember everything without storage",
                    "Cancel the workflow immediately",
                ],
                "correct": 0,
                "explanation": "Human input is modeled as asynchronous suspension.",
            },
            {
                "id": "M01.L08.Q14",
                "section_id": "streams-not-state",
                "question": "What should be the recovery source of truth after a stream disconnects?",
                "options": ["Persisted task state", "The lost stream buffer only", "Browser console", "The model's hidden state"],
                "correct": 0,
                "explanation": "Streams can disappear; durable state supports recovery.",
            },
            {
                "id": "M01.L08.Q15",
                "section_id": "disconnect-vs-cancel",
                "question": "What should happen when a user merely closes the browser tab?",
                "options": [
                    "The underlying task may continue unless explicit cancellation was requested",
                    "Always cancel the remote task",
                    "Delete the workflow record",
                    "Mark the task completed",
                ],
                "correct": 0,
                "explanation": "Disconnect and cancellation express different user intent.",
            },
            {
                "id": "M01.L08.Q16",
                "section_id": "ghost-tasks",
                "question": "What is the role of a stale-task sweeper?",
                "options": [
                    "Detect non-terminal work that stopped updating and move it toward explicit recovery/failure",
                    "Generate final reports",
                    "Replace the frontend progress bar",
                    "Perform all model calls",
                ],
                "correct": 0,
                "explanation": "Sweepers prevent tasks from remaining pending forever after worker failure.",
            },
            {
                "id": "M01.L08.Q17",
                "section_id": "idempotency",
                "question": "Why are idempotency keys necessary?",
                "options": [
                    "Retries and duplicate delivery should not repeat expensive or sensitive effects",
                    "They make streams durable automatically",
                    "They replace authentication",
                    "They eliminate all network failures",
                ],
                "correct": 0,
                "explanation": "Asynchronous systems must tolerate duplicate requests and events.",
            },
            {
                "id": "M01.L08.Q18",
                "section_id": "observability",
                "question": "Which item is useful correlation metadata for a distributed workflow?",
                "options": ["Remote A2A task ID", "CSS font size", "Browser theme", "Audio volume only"],
                "correct": 0,
                "explanation": "Task, workflow, session, operation, and trace identifiers help reconstruct distributed execution.",
            },
            {
                "id": "M01.L08.Q19",
                "section_id": "security-long-work",
                "question": "Why may authorization need to be checked again later in a long workflow?",
                "options": [
                    "The task can outlive the original session or token validity",
                    "Authorization never changes",
                    "A2A disables permissions",
                    "MCP tools always run anonymously",
                ],
                "correct": 0,
                "explanation": "Sensitive work may execute long after the original user session began.",
            },
            {
                "id": "M01.L08.Q20",
                "section_id": "frontend-state",
                "question": "What should a frontend do after refresh during an active task?",
                "options": [
                    "Fetch durable task state and rebuild the UI",
                    "Assume the task disappeared",
                    "Always create a duplicate task",
                    "Wait for the old stream to magically return",
                ],
                "correct": 0,
                "explanation": "Recoverable state lets the user disconnect and return later.",
            },
            {
                "id": "M01.L08.Q21",
                "section_id": "market-step6",
                "question": "What state best represents a report paused for paid-data approval?",
                "options": ["input_required", "completed", "failed", "expired immediately"],
                "correct": 0,
                "explanation": "The workflow is suspended pending correlated human input.",
            },
            {
                "id": "M01.L08.Q22",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design an integrated live agent system that can handle both a fast stock quote and "
                    "a multi-hour research report. Explain Browser, Frontend Service, Backend/ADK Live, "
                    "Host Agent, A2A Specialist, MCP Server, durable workflow storage, task state machine, "
                    "progress transport, human approval, cancellation, idempotency, observability, security, "
                    "frontend recovery, and final Artifact retention."
                ),
            },
        ],
        "passing_score": 70,
    },
}
