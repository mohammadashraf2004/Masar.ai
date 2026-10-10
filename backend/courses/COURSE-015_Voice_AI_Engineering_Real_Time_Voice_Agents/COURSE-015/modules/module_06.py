"""M01.L06 — Multi-Agent Systems, A2A Interoperability, and Implementation.

Three source chapters -> one complete learner-facing lesson.

Source alignment:
- Chapter 7: Multi-Agent Systems: Collaboration and Orchestration (Illustrated with ADK)
- Chapter 8: The Agent2Agent (A2A) Protocol: Enabling Agent-to-Agent Communication
- Chapter 9: Implementing A2A-Compliant Agents

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L06"
MODULE_ORDER = 1
MODULE_TITLE = "Multi-Agent Systems, Interoperability & A2A Implementation"
MODULE_DESCRIPTION = (
    "Design and orchestrate teams of specialized agents, exchange context through "
    "shared state, add guardrails with callbacks, expose a single live interface, "
    "extend collaboration across framework boundaries with the A2A protocol, "
    "and implement real A2A servers, clients, adapters, rich-data exchanges, and "
    "cross-framework research workflows using the source-described Python SDK patterns."
)
SOURCE_CHAPTER = "7-9"
SOURCE_PAGES = "Early Release drafts for Chapters 7-9; page numbers not provided"

TOPIC = {
    "title": "Multi-Agent Systems, A2A Interoperability, and Implementation",
    "slug": "agent-foundations-m01-l06",
    "description": (
        "Learn how to decompose a monolithic agent into specialists, coordinate them "
        "with workflow patterns and shared state, connect independent remote agents "
        "through A2A discovery/task/transport/security contracts, and implement those "
        "contracts with practical server, client, adapter, and multi-framework patterns."
    ),
    "order": 6,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 7.0,
    "skill_tags": [
        "multi-agent-systems",
        "agent-orchestration",
        "sequential-agents",
        "parallel-agents",
        "shared-state",
        "callbacks",
        "guardrails",
        "live-agents",
        "agent-as-tool",
        "a2a",
        "agent-card",
        "tasks",
        "artifacts",
        "sse",
        "webhooks",
        "agent-security",
        "interoperability",
        "a2a-python-sdk",
        "agent-executor",
        "a2a-client",
        "adapter-pattern",
        "cross-framework-agents",
        "filepart",
        "datapart",
        "distributed-debugging",
    ],
    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03", "M01.L04", "M01.L05"],

    "lesson": {
        "title": "Multi-Agent Systems, A2A Interoperability, and Implementation",
        "estimated_minutes": 420,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Multi-Agent Systems and Agent-to-Agent Interoperability

> **Lesson:** M01.L06  
> **Source alignment:** Chapters 7 and 8 of the supplied Early Release material.  
> This lesson combines the two chapters into one learning path.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a single do-everything agent becomes difficult to scale and maintain.
- Apply the "agents as microservices" mental model.
- Split a complex problem into specialist agents.
- Compare Router, Parallel, Sequential, Circular, and Dynamic collaboration patterns.
- Choose a collaboration pattern based on dependencies between subtasks.
- Explain shared Session State as a team's working memory.
- Explain how specialist outputs are written into and read from shared state.
- Explain why deterministic workflow agents can be safer than prompt-only orchestration.
- Use callbacks conceptually for context loading, guardrails, validation, logging, caching, and conditional skipping.
- Trace the Grammar -> Math -> Summary Teaching Assistant workflow.
- Explain why a multi-agent live system usually exposes one front-facing Live Agent.
- Explain the agent-as-a-tool pattern and its scalability limits.
- Explain why live-agent transfer is different from background collaboration.
- Describe the framework interoperability problem that A2A is intended to solve.
- Explain A2A's core principles as presented in the source.
- Distinguish End-User, Client, and Server roles.
- Explain how Agent Cards enable discovery and capability negotiation.
- Distinguish direct Messages from stateful Tasks.
- Explain the Task lifecycle and the purpose of task status.
- Distinguish Messages, Artifacts, and Parts.
- Compare polling, SSE streaming, and webhook-based asynchronous communication.
- Explain the major security layers described in the source.
- Design an architecture that combines internal orchestration with external agent interoperability.
- Explain the roles of the source-described A2A Python SDK components: `AgentExecutor`, `A2AStarletteApplication`/`A2AFastAPIApplication`, and `A2AClient`.
- Explain how an `AgentExecutor` acts as an adapter between A2A protocol events and a framework-specific agent runtime.
- Trace a cross-framework ADK-to-LangGraph handshake using discover, connect, and communicate steps.
- Explain how an existing agent can be exposed as an A2A service without rewriting its core logic.
- Translate an internal framework event stream into A2A task updates and artifacts.
- Design a cross-framework Research Assistant with strategist, worker, and orchestrator roles.
- Reuse a generic remote-agent helper that discovers an Agent Card, creates a client, sends a message, and extracts an artifact.
- Handle file artifacts with `FilePart` and structured form-like exchanges with `DataPart`.
- Debug distributed A2A workflows using the Task object, task history, artifacts, server logs, and isolated client tests.

---

## 1. Why move beyond a single agent?

A single agent is easy to understand when the problem is small.

You might begin with:

```text
One agent
+ one prompt
+ several tools
```

As the application grows, developers often continue adding:

```text
more tools
more responsibilities
more rules
more exceptions
more examples
```

Eventually the agent becomes a monolith.

Imagine one Teaching Agent that handles:

- grammar,
- mathematics,
- summarization,
- research,
- writing,
- scheduling,
- recommendations.

Its prompt and tool list become increasingly crowded.

This can make the agent:

- harder to test,
- harder to debug,
- harder to maintain,
- more likely to confuse responsibilities,
- more difficult to evolve independently.

The source uses a software-engineering analogy:

```text
monolithic software
      ↓
microservices

monolithic agent
      ↓
specialized agents
```

The key idea is not "use many agents everywhere."

It is:

> When responsibilities are clearly different, splitting them into focused specialists can improve modularity.

[[IMAGE_NEEDED: Monolithic agent vs specialist team | Left: one huge agent connected to many unrelated tools; right: an orchestrator connected to Grammar, Math, and Summary specialists | Learner should see why specialization can reduce complexity]]

---

## 2. Split agents like microservices

A good specialist has a narrow job.

The source uses the Teaching Assistant example.

### Grammar Agent

Responsibility:

```text
Check the user's input for grammatical errors.
```

Tool:

```text
check_grammar
```

### Math Agent

Responsibility:

```text
Perform mathematical operations.
```

Tools:

```text
add
subtract
multiply
divide
```

### Summary Agent

Responsibility:

```text
Combine the team's findings into one friendly response.
```

Tools:

```text
none required
```

This decomposition is useful because each agent can have:

- its own prompt,
- its own tools,
- its own tests,
- its own output contract.

A useful design question is:

> Can I describe this agent's responsibility in one clear sentence?

If not, its responsibility may still be too broad.

---

## 3. Five collaboration patterns

A team of agents still needs an orchestration pattern.

### Router pattern

```text
             ┌-> Billing Agent
User -> Router
             ├-> Support Agent
             └-> Weather Agent
```

One central router selects the most relevant specialist.

Use it when one request usually belongs to one domain.

---

### Parallel pattern

```text
                 ┌-> Flight Agent --┐
Travel Planner --|                  |-> combine
                 └-> Hotel Agent ---┘
```

Independent tasks run concurrently.

Use it when subtasks do not depend on one another.

---

### Sequential pattern

```text
Agent A
   ↓
Agent B
   ↓
Agent C
```

Each stage runs in a fixed order.

Use it when later stages depend on earlier outputs.

---

### Circular pattern

```text
Writer
  ↓
Editor
  ↓
Writer
  ↓
...
```

Agents repeatedly refine work.

Use it for critique and revision loops.

---

### Dynamic pattern

```text
Agent A <-> Agent B
  ↕          ↕
Agent C <-> Agent D
```

Agents communicate flexibly.

This is powerful but harder to reason about.

[[IMAGE_NEEDED: Five multi-agent orchestration patterns | Router, Parallel, Sequential, Circular, and Dynamic shown side by side | Learner should visually compare the control flow of each pattern]]

---

## 4. Choose the pattern from the dependency structure

The source's Teaching Assistant has a clear dependency order:

```text
1. Correct the grammar
2. Use the corrected query for math
3. Summarize the results
```

Therefore:

```text
Grammar
   ↓
Math
   ↓
Summary
```

is a natural Sequential workflow.

A simple selection guide:

| Question | Likely pattern |
|---|---|
| Does one request map to one specialist? | Router |
| Can several specialists work independently? | Parallel |
| Does each stage depend on the previous one? | Sequential |
| Does the work need repeated refinement? | Circular |
| Is communication highly flexible and adaptive? | Dynamic |

{{exercise:M01.L06.EX01}}

---

## 5. Shared Session State: the team workbench

A multi-agent workflow needs a way to exchange information.

The source describes Session State as a shared:

```text
workbench
```

or:

```text
whiteboard
```

Every specialist can read relevant values and write new values.

Example:

```python
state = {
    "student_profile": {...}
}
```

After Grammar Agent:

```python
state = {
    "student_profile": {...},
    "grammar_response": "..."
}
```

After Math Agent:

```python
state = {
    "student_profile": {...},
    "grammar_response": "...",
    "math_response": "..."
}
```

After Summary Agent:

```python
state = {
    "student_profile": {...},
    "grammar_response": "...",
    "math_response": "...",
    "summary_response": "..."
}
```

The state becomes the team's shared short-term memory.

---

## 6. Writing specialist outputs into state

The source uses an ADK concept called `output_key`.

Conceptually:

```python
grammar_agent:
    output_key = "grammar_response"

math_agent:
    output_key = "math_response"

summary_agent:
    output_key = "summary_response"
```

The exact ADK syntax is framework-specific.

The durable idea is:

> Every specialist should have a clear output contract.

That contract answers:

```text
What does this agent produce?
Where is that result stored?
Who consumes it next?
```

This is similar to defining interfaces between microservices.

---

## 7. Deterministic workflow agents

The source uses ADK's SequentialAgent for the Teaching Assistant.

Conceptually:

```python
root_agent = SequentialAgent(
    sub_agents=[
        grammar_agent,
        math_agent,
        summary_agent,
    ]
)
```

The workflow order is encoded directly.

That is preferable to relying only on instructions such as:

```text
"First call grammar.
Then call math.
Then call summary."
```

when the business rule is fixed.

### General principle

> Fixed workflow logic belongs in orchestration, not only in natural-language prompts.

This makes the process easier to:

- test,
- audit,
- debug,
- change deliberately.

[[IMAGE_NEEDED: Teaching Assistant pipeline with shared state | Grammar Agent -> Math Agent -> Summary Agent, with each agent connected to one Shared Session State box | Learner should see deterministic order and context exchange together]]

---

## 8. Callbacks: lifecycle hooks around execution

The source introduces callbacks as control points around the agent lifecycle.

Think of callbacks as:

```text
middleware
interceptors
hooks
```

They allow custom Python code to run at specific execution boundaries.

The source describes six key callback positions:

```text
before_agent
after_agent

before_model
after_model

before_tool
after_tool
```

---

## 9. Before-agent and after-agent callbacks

### Before-agent callback

Runs before an agent begins its main work.

Useful for:

- loading initial context,
- validating prerequisites,
- enforcing entry rules.

### After-agent callback

Runs after the agent finishes.

Useful for:

- logging,
- auditing,
- output checks,
- state cleanup.

Example:

```text
Before Math Agent:
Does grammar_response exist?
```

If not, stop rather than continue with invalid state.

---

## 10. Before-model and after-model callbacks

### Before-model

Runs before context is sent to the model.

Useful for:

- injecting dynamic context,
- checking sensitive content,
- applying caching,
- modifying the final request.

### After-model

Runs after raw model output returns.

Useful for:

- filtering,
- reformatting,
- validation,
- adding standard behavior.

This creates an application-controlled boundary around the model.

---

## 11. Before-tool and after-tool callbacks

### Before-tool

Runs after a tool has been selected but before it executes.

Ideal for:

- permission checks,
- input validation,
- safety checks,
- cache lookups.

### After-tool

Runs after tool execution.

Useful for:

- logging,
- normalizing tool results,
- writing new state,
- caching.

This is especially important for tools with side effects.

---

## 12. What callbacks can implement

The source gives several patterns.

### Guardrails

Block operations that violate policy.

### Dynamic state management

Read and write state depending on current context.

### Logging and monitoring

Build detailed execution traces.

### Caching

Return a cached result instead of repeating an expensive call.

### Request/response modification

Inject context or normalize results.

### Conditional skipping

Skip a model/tool call when a callback already has the needed result.

Callbacks therefore move important control out of prompt text and into deterministic application code.

---

## 13. Seed the shared state before the pipeline begins

The Teaching Assistant needs a student profile before any specialist runs.

The orchestrator callback checks whether it exists.

Conceptually:

```python
if not state.get("student_profile"):
    state["student_profile"] = load_profile()
```

Now every later specialist can access it.

This is a clean way to initialize the pipeline.

---

## 14. Guard dependencies between stages

The Math Agent depends on Grammar Agent output.

Its callback can validate:

```text
student_profile exists?
grammar_response exists?
```

If a required value is missing, the system should fail clearly rather than produce a misleading answer.

A robust specialist should know:

```text
required input keys
produced output keys
```

{{exercise:M01.L06.EX02}}

---

## 15. Reading shared state through prompt templates

The source uses placeholders like:

```text
{student_profile}
{grammar_response}
{math_response}
```

The runtime resolves these using current state values.

For the Summary Agent:

```text
Student:
{student_profile}

Grammar result:
{grammar_response}

Math result:
{math_response}

Task:
Combine the information into one helpful response.
```

The Summary Agent can focus on synthesis instead of redoing previous work.

---

## 16. Trace the complete Teaching Assistant flow

Suppose the user asks a math question with a grammar mistake.

### Grammar Agent

Receives:

```text
original user input
student profile
```

Calls:

```text
check_grammar
```

Writes:

```text
grammar_response
```

### Math Agent

Checks that `grammar_response` exists.

Uses the corrected question.

May call:

```text
multiply([1,2,3,4,5,6,7,8,9,10])
```

Writes:

```text
math_response
```

### Summary Agent

Reads:

```text
student_profile
grammar_response
math_response
```

Produces:

```text
summary_response
```

The user receives one cohesive answer, even though several agents contributed.

---

## 17. Debug shared state step by step

If the final output is wrong, the problem may not be the final agent.

Possible causes:

- Grammar Agent produced a bad correction.
- Math Agent received the wrong state.
- A state key was missing.
- Prompt templating referenced the wrong key.
- Summary Agent misunderstood upstream results.

A good multi-agent debugger should expose:

```text
state before agent
state after agent
tool calls
tool results
agent outputs
```

The source uses ADK Web to inspect the workbench visually.

### Rule

> Debug the pipeline at every stage, not only at the final answer.

---

## 18. One Live Agent should usually face the user

Now imagine turning the Teaching Assistant into a real-time voice application.

A naive design might let:

```text
Grammar Agent speak
Math Agent speak
Summary Agent speak
```

This would create a confusing experience.

Instead, the source recommends:

```text
User
  ↓
one Live Agent
  ↓
background multi-agent team
```

The specialists collaborate silently.

Only the final synthesized result is spoken to the user.

[[IMAGE_NEEDED: Single Live Agent with background team | User speaks with one Live Agent; behind it, a Sequential Orchestrator runs Grammar, Math, and Summary agents using Shared State | Learner should understand the separation between user-facing conversation and internal collaboration]]

---

## 19. Agent-as-a-tool

The source presents a practical integration:

```text
Live Agent
   ↓
calls Teaching Assistant as one tool
   ↓
multi-agent pipeline executes
   ↓
final result returns
   ↓
Live Agent speaks
```

### Why it is useful

- straightforward,
- easy to integrate,
- hides internal complexity.

### Why it can become limiting

The whole team becomes one black box.

The front agent may have little visibility into internal specialists.

The source therefore presents this as practical for a contained pipeline, not as the final answer for all large systems.

---

## 20. Collaboration is different from Live Agent handoff

Multiple Live Agents make more sense when the user is being transferred to a different conversational experience.

Examples from the source include:

- changing language,
- changing voice/persona,
- secure data entry,
- accessibility configuration,
- escalation to a human.

This is:

```text
handoff
```

not:

```text
parallel collaboration
```

---

## 21. Why live handoff is difficult

A live conversation contains more than transcript text.

It may include:

- tone,
- emotion,
- timing,
- interruptions,
- hesitation.

If a new agent receives only:

```text
text summary
```

some context is lost.

The developer may need to transfer:

- conversation summary,
- current task state,
- preferences,
- tool results,
- possibly interaction/emotional state.

This motivates a broader question:

> How do independent agents communicate using a standard interface?

That is where Chapter 8 begins.

---

## 22. The "walled garden" problem

Imagine:

```text
Teaching Assistant -> ADK
Research Agent -> LangGraph
Onboarding Agent -> CrewAI
Payroll Agent -> LangChain
```

Each framework has its own:

- runtime,
- state,
- tool format,
- agent object,
- message model.

Without a standard, every pair may need custom integration.

The source calls this a Tower-of-Babel problem.

The goal is to let agents collaborate even when their internal frameworks are different.

---

## 23. A2A: a common external language for agents

The source introduces the Agent2Agent (A2A) Protocol.

Conceptually:

```text
Internal implementation:
ADK / LangGraph / CrewAI / other

External contract:
A2A
```

The remote caller does not need to know how the other agent is built.

It needs to know:

- how to discover it,
- what it can do,
- how to authenticate,
- how to submit work,
- how to receive status/results.

This enables an "Agents as a Service" model.

---

## 24. Five A2A principles described by the source

### Opaque execution

The remote agent may hide its internal implementation.

### Async first

The protocol assumes some tasks may take a long time.

### Modality agnostic

The protocol can represent more than plain text.

### Enterprise ready

Security, privacy, tracing, and monitoring matter.

### Simple and consistent

A2A builds on familiar web concepts rather than requiring an entirely unusual stack.

[[IMAGE_NEEDED: Five A2A principles | Opaque Execution, Async First, Modality Agnostic, Enterprise Ready, and Simple & Consistent around an A2A hub | Learner should remember the protocol design goals]]

---

## 25. Opaque execution

A Research Agent might internally:

- run many searches,
- inspect documents,
- call sub-agents,
- revise its answer.

The Client does not need all of that internal detail.

It may only need:

```text
working
```

and later:

```text
completed + result
```

This preserves encapsulation.

Opaque execution does not mean "no observability."

A developer may still expose useful status updates without revealing private prompts or implementation logic.

---

## 26. Why A2A is async-first

Agent tasks can be very different in duration.

Example:

```text
2 + 2
```

may complete immediately.

But:

```text
review a contract and wait for human approval
```

may take hours.

A protocol that assumes every operation finishes in one short connection would not handle agentic workloads well.

So the source emphasizes asynchronous task management.

---

## 27. The three A2A actors

### End-User

Originates the high-level goal.

This may be:

- a human,
- an application,
- a scheduled job.

### Client

Acts as initiator/orchestrator.

The Client may:

- understand the request,
- find a specialist,
- delegate work.

### Server

The remote agent that executes the delegated task.

It exposes a standardized external contract while keeping its internal implementation private.

[[IMAGE_NEEDED: End-User Client Server chain | End-User -> Client/Concierge -> Remote Server/Specialist, with status/results returning in the opposite direction | Learner should distinguish who asks, who delegates, and who performs the work]]

---

## 28. Client and Server are roles

An agent can be a Server in one relationship and a Client in another.

Example:

```text
Concierge -> Research Agent
```

Here Research Agent is the Server.

But Research Agent may call:

```text
PDF Analysis Agent
```

Now Research Agent acts as a Client.

This allows deep agent networks.

---

## 29. Agent Card: the digital business card

How does a Client know:

```text
which remote agent exists?
what skills it offers?
how to reach it?
how to authenticate?
```

The source answers with the **Agent Card**.

It is a standardized description of an agent's public contract.

Think of it as:

```text
identity
+
capabilities
+
connection information
+
security requirements
```

---

## 30. Three discovery approaches

The source describes:

### Direct configuration

The Client already knows the remote agent.

Useful for small static systems.

### Well-known location

The Client knows the domain and retrieves the Agent Card from a standard location.

The exact URI pattern is protocol-version-specific and should be verified against the current specification.

### Registry/catalog

A central directory lets Clients search by skill.

Example:

```text
Find an agent that can perform academic research.
```

This becomes important in large organizations.

---

## 31. Important Agent Card fields

The source describes several categories.

### Name and description

What the agent is.

### Supported interfaces

How it can be contacted.

### Version

Helps compatibility management.

### Capabilities

May describe features such as streaming or push notifications.

### Security schemes

What authentication mechanisms are supported.

### Security requirements

Which authentication combination is required.

### Skills

What jobs the agent can perform.

The Client should select a remote Server based on its published skill contract.

[[IMAGE_NEEDED: Agent Card anatomy | Structured card showing identity, interfaces, version, capabilities, security, and skills | Learner should understand the Agent Card as a discovery and compatibility contract]]

---

## 32. Direct Message vs stateful Task

Not every request requires a long-running Task.

### Direct Message

Appropriate for:

- simple interaction,
- clarification,
- stateless request.

### Task

Appropriate for:

- multi-step work,
- long-running activity,
- trackable progress,
- authorization or input pauses.

The Server can determine the appropriate interaction style.

---

## 33. Task: the stateful unit of work

A Task gives long-running work a persistent identity.

Conceptually:

```text
submit request
   ↓
create Task
   ↓
track Task state
   ↓
receive final result
```

The source describes IDs such as task ID and context ID.

Exact field names are protocol-specific and should be checked against the current A2A specification.

---

## 34. Task lifecycle

The source describes states including:

```text
submitted
working
input-required
auth-required
completed
failed
canceled
rejected
```

### submitted

The server accepted the request.

### working

The agent is processing it.

### input-required

The remote agent needs clarification.

### auth-required

Additional authorization is required.

### completed

The work finished successfully.

### failed / canceled / rejected

The task stopped without successful completion.

Explicit status lets the Client decide what to do next.

[[IMAGE_NEEDED: A2A Task state machine | submitted -> working -> completed, with side branches to input-required, auth-required, failed, canceled, and rejected | Learner should see how status coordinates long-running work]]

{{exercise:M01.L06.EX03}}

---

## 35. Messages and Artifacts serve different purposes

The source separates process context from deliverables.

### Message

Explains what is happening.

Examples:

```text
"Checking available sources."
"Which date range do you mean?"
"Please authorize calendar access."
```

### Artifact

Contains the result of the work.

Examples:

- report,
- image,
- text answer,
- structured dataset.

A useful mental model:

```text
Message = process/context
Artifact = result/deliverable
```

---

## 36. Parts: the content atoms

Messages and Artifacts are built from Parts.

### TextPart

Text content.

### FilePart

Binary/file content or a file reference.

Examples:

- image,
- audio,
- PDF.

### DataPart

Structured data.

Example:

```json
{
  "temperature": 22,
  "unit": "C"
}
```

DataPart is valuable when one agent needs machine-readable output from another.

[[IMAGE_NEEDED: A2A content hierarchy | Task contains status Messages and result Artifacts; both can contain TextPart, FilePart, and DataPart | Learner should remember the distinction between container and content type]]

---

## 37. Three communication patterns

Different tasks require different communication mechanisms.

The source presents:

```text
Polling
SSE streaming
Webhook push
```

---

## 38. Request/response and polling

For very short work:

```text
Client -> request
Server -> result
```

For slightly longer work:

```text
Client -> request
Server -> working + task id

Client -> status check
Server -> working

Client -> status check
Server -> completed
```

This is easy to implement.

It is best when the task is relatively short.

---

## 39. Streaming with Server-Sent Events

For generative work, the server can stream partial output.

Conceptually:

```text
Client opens stream
Server sends chunk
Server sends chunk
Server sends chunk
Server marks final chunk
```

This improves perceived responsiveness.

### Important distinction

SSE is primarily server-to-client streaming.

It is not the same as the full-duplex WebSocket architecture used earlier for live audio.

---

## 40. Asynchronous push with webhooks

For a task that may take a long time:

```text
generate report
render video
perform deep research
```

keeping a connection open may be undesirable.

Webhook flow:

```text
Client submits task + callback URL
Server responds: submitted
connection closes

... later ...

Server calls webhook
Client verifies notification
Client retrieves result
```

This is a "notify me when ready" architecture.

[[IMAGE_NEEDED: Polling vs SSE vs Webhook | Three timelines showing repeated polls, one streaming connection, and submit-then-later-callback | Learner should compare how connection lifetime changes with task duration]]

---

## 41. Choose transport based on workload

| Workload | Good fit |
|---|---|
| Quick calculation | Direct response / polling |
| Incremental generation | SSE streaming |
| Long background job | Webhook push |

The best mechanism depends on:

- expected duration,
- need for partial output,
- tolerance for open connections,
- whether the Client can expose a callback endpoint.

{{exercise:M01.L06.EX04}}

---

## 42. Security becomes a first-class concern

Inside one local application, agents may already trust one another.

Across the internet, the assumptions change.

You need to ask:

```text
Who is calling?
Is the connection encrypted?
What is the caller allowed to do?
Should internal implementation stay private?
Can I trust the callback?
```

The source describes five security layers.

---

## 43. Authentication

Authentication answers:

```text
Who are you?
```

The source discusses standard web mechanisms such as:

- OAuth 2.0,
- OpenID Connect,
- API keys.

The Agent Card can advertise supported and required methods.

The point is to reuse mature identity standards rather than invent a custom agent login system.

---

## 44. Transport security

Sensitive agent data should travel over encrypted channels.

Conceptually:

```text
HTTPS + TLS
```

This protects:

- credentials,
- user data,
- task content,
- artifacts.

Exact protocol-version requirements should be checked against current A2A and organizational security guidance.

---

## 45. Authorization and least privilege

Authentication says who the caller is.

Authorization decides what the caller may do.

Example:

```text
Manager Agent:
read + delete

Intern Agent:
read only
```

The Principle of Least Privilege means:

> Give each caller only the permissions it actually needs.

---

## 46. Opaque execution also protects internals

Remote clients do not need access to:

- system prompts,
- private memory,
- proprietary algorithms,
- internal model configuration.

They need:

```text
skills
status
results
```

Opaque execution therefore acts as both an architectural boundary and a security boundary.

---

## 47. Verify webhook callbacks

An internet-facing webhook can receive forged requests.

So a notification such as:

```text
"Task completed"
```

should not be trusted automatically.

The source discusses verification mechanisms such as:

- signatures,
- shared secrets.

Conceptually:

```text
Server signs notification
Client verifies
accept or reject
```

[[IMAGE_NEEDED: Five A2A security layers | Authentication, Transport Security, Authorization/RBAC, Opaque Execution, and Webhook Verification shown as stacked protection layers | Learner should see security as defense in depth]]

---

## 48. Internal orchestration and external interoperability are different layers

Inside one application:

```text
SequentialAgent
ParallelAgent
Shared State
Callbacks
Prompt templates
```

Across independent applications:

```text
Agent Card
Task
Message
Artifact
Transport
Security
```

The first layer answers:

> How do my agents work together internally?

The second answers:

> How does my system collaborate with agents I do not control?

Both are important.

---

## 49. Combine the two chapters into one architecture

Imagine a university assistant.

### User-facing layer

```text
Student
   ↓
Live Teaching Assistant
```

### Internal team

```text
Grammar
   ↓
Math
   ↓
Summary
```

with:

```text
Shared Session State
Callbacks
Guardrails
```

### External need

The student asks:

```text
"What are the latest breakthroughs in quantum computing?"
```

The local team does not have research capability.

The Client searches for a remote:

```text
Academic Research Agent
```

### Discovery

It reads the remote agent's Agent Card.

### Delegation

It submits a research request.

### Task lifecycle

The remote agent may report:

```text
submitted
working
completed
```

### Result

The Research Agent returns an Artifact.

### Final presentation

The local system combines the research with:

- student profile,
- current conversation,
- teaching style.

The Live Agent speaks the final answer.

[[IMAGE_NEEDED: Internal multi-agent plus external A2A architecture | Student -> Live Agent -> internal Grammar/Math/Summary team; a branch from the orchestrator discovers a remote Research Agent through Agent Card and receives an Artifact through A2A | Learner should understand how internal orchestration and external interoperability combine]]

---

## 50. Practical design guidelines

### 1. Split by responsibility

Create specialists with clear purpose and independently testable behavior.

### 2. Encode fixed order in workflow logic

Do not rely on the LLM to remember deterministic business sequencing.

### 3. Define state contracts

For every agent:

```text
required keys
written keys
```

### 4. Validate dependencies

Use callbacks/guardrails before a stage executes.

### 5. Keep one conversational face

For live systems, let specialists collaborate behind one user-facing agent.

### 6. Treat remote agents as services

Depend on their public contract, not their internal implementation.

### 7. Match transport to task

Short:

```text
direct/poll
```

Incremental:

```text
stream
```

Long-running:

```text
webhook
```

### 8. Use layered security

Combine identity, encrypted transport, authorization, bounded interfaces, and callback verification.

{{exercise:M01.L06.EX05}}

---

## 51. A2A is a living standard

The source explicitly frames the protocol as evolving.

Therefore, verify current official documentation before implementing details such as:

- exact Agent Card schema,
- discovery paths,
- Task fields,
- Task state names,
- RPC methods,
- transport options,
- webhook conventions,
- SDK APIs,
- security requirements.

The durable concepts are:

```text
discovery
capability advertisement
opaque execution
long-running Tasks
status communication
result Artifacts
asynchronous transport
enterprise security
```

The exact wire format can evolve.

---

## 52. End-to-end mental model

You should now be able to trace three levels of agent architecture.

### Level 1 — specialist teamwork

```text
Orchestrator
   ↓
Agent A
   ↓
Agent B
   ↓
Agent C
```

with shared state.

### Level 2 — live user interaction

```text
User
  ↓
one Live Agent
  ↓
background specialist team
  ↓
one final response
```

### Level 3 — internet-scale collaboration

```text
Local Client Agent
  ↓ discover
Agent Card
  ↓ delegate
Remote Server Agent
  ↓ Task
Status / Messages
  ↓
Artifact
  ↓
Local system continues
```

This progression takes us from:

```text
one agent
```

to:

```text
agent team
```

to:

```text
agent ecosystem
```

---


## 53. From A2A theory to implementation

Chapters 7 and 8 gave us two architectural layers:

```text
Chapter 7:
internal multi-agent orchestration

Chapter 8:
standardized communication between independent agents
```

Chapter 9 turns the A2A layer into code.

The source uses the official A2A Python SDK to demonstrate three recurring roles.

### Server-side bridge: `AgentExecutor`

This is the adapter between:

```text
A2A request
```

and:

```text
your agent's internal runtime
```

Its job is conceptually:

```text
receive request
    ↓
extract user input
    ↓
run framework-specific agent
    ↓
convert results/status into A2A events
```

### Server application wrapper

The source describes application wrappers such as:

```text
A2AStarletteApplication
A2AFastAPIApplication
```

Their role is to handle protocol plumbing such as:

- HTTP,
- JSON-RPC,
- server routing,
- SSE behavior.

This allows the agent developer to focus on execution logic.

### Client-side connector: `A2AClient`

A Client needs to:

```text
discover
connect
send work
receive Task/events/results
```

The source uses `A2AClient` for this responsibility.

> The exact SDK names and signatures are source/version-specific. Treat the architecture as durable and re-check the current SDK before implementation.

[[IMAGE_NEEDED: A2A Python toolkit roles | Remote Client on the left using Agent Card Resolver + A2AClient; A2A web application in the middle; AgentExecutor on the server side bridging into LangGraph/ADK/internal agent logic | Learner should see protocol plumbing separated from framework-specific logic]]

---

## 54. First implementation: a cross-framework handshake

The source begins with the smallest useful interoperability proof.

Two agents use different frameworks:

```text
ADK Initiator
      ↓ A2A
LangGraph Greeter
```

The Greeter does not need to understand ADK.

The Initiator does not need to understand LangGraph internals.

They only need to agree on:

```text
A2A
```

This is an important systems principle:

> Interoperability comes from agreeing on the boundary, not from agreeing on the internal implementation.

### Project separation

The source separates the agents into independent directories.

Conceptually:

```text
a2a_handshake/
├── langgraph_greeter/
│   ├── greeter_agent_logic.py
│   └── server.py
│
└── adk_initiator/
    ├── initiator_agent.py
    └── main.py
```

This reinforces that the agents are separate deployable concerns rather than two modules tightly coupled inside one application.

---

## 55. Build the framework-specific agent first

The source's Greeter uses a minimal LangGraph workflow.

The internal logic is intentionally simple.

Conceptually:

```python
class GreeterState(TypedDict):
    message: str

def greet(state):
    return {
        "message": "Hello from the LangGraph agent!"
    }
```

Then a graph is assembled:

```text
START
  ↓
greet
  ↓
END
```

Why keep the internal graph simple?

Because the purpose of this example is not to teach complex LangGraph routing.

It is to isolate the interoperability boundary.

### General engineering technique

When testing a new integration:

```text
minimize unrelated complexity
```

First prove:

```text
Framework A
    ↔ protocol
Framework B
```

Then add richer agent behavior later.

---

## 56. Expose the Greeter with an Agent Card

Before another agent can call the Greeter, the Greeter needs a public contract.

The source defines an Agent Card containing information such as:

```text
name
description
endpoint/interface
version
capabilities
input/output modes
skills
```

Its advertised skill is conceptually:

```text
Skill:
greet

Description:
Return a friendly greeting.
```

This creates a useful separation:

```text
internal LangGraph implementation
        !=
external A2A capability contract
```

A future Greeter could be rewritten in another framework while preserving the same public skill contract.

---

## 57. `AgentExecutor` is the protocol-to-agent adapter

The most important server-side implementation pattern is the adapter.

The source creates a custom executor that:

1. receives a `RequestContext`,
2. creates or uses an event/task updater,
3. invokes the internal LangGraph application,
4. extracts the result,
5. publishes an A2A Artifact,
6. marks the Task complete.

Conceptually:

```python
async def execute(context, event_queue):
    user_input = context.get_user_input()

    internal_result = await run_internal_agent(user_input)

    await publish_artifact(internal_result)
    await complete_task()
```

The exact SDK objects are version-specific.

The architecture is not.

### The adapter boundary

```text
A2A world
    ↓ RequestContext
AgentExecutor
    ↓ framework-specific invocation
LangGraph / ADK / CrewAI / custom code
    ↓ internal result
AgentExecutor
    ↓ TaskStatus + Artifact
A2A world
```

This is a powerful pattern because the remote protocol does not leak into all internal business logic.

[[IMAGE_NEEDED: AgentExecutor adapter pattern | A2A RequestContext enters AgentExecutor; executor invokes a framework-specific agent; result is translated into TaskUpdater status and Artifact events | Learner should see the executor as translation glue rather than the agent's intelligence]]

---

## 58. Wrap the executor in an A2A web application

The executor implements behavior.

Something still needs to expose that behavior over the network.

The source combines:

```text
Agent Card
AgentExecutor
Task Store
Request Handler
A2A web application
```

Conceptually:

```text
HTTP / JSON-RPC / SSE
        ↓
A2A application
        ↓
request handler
        ↓
AgentExecutor
        ↓
internal agent
```

The source uses an in-memory task store for the tutorial.

That is appropriate for learning.

A production service would need to consider:

- persistence,
- multiple server instances,
- restart recovery,
- task retention,
- scaling.

### Important distinction

```text
AgentExecutor:
what happens when work arrives

A2A web application:
how protocol requests reach the executor
```

---

## 59. Client flow: Discover → Connect → Communicate

The source's ADK Initiator wraps A2A communication in a tool.

The recurring client pattern is:

```text
1. Discover
2. Connect
3. Communicate
4. Extract result
```

### Step 1 — Discover

Fetch the remote Agent Card.

Conceptually:

```python
resolver = A2ACardResolver(...)
card = await resolver.get_agent_card()
```

The Client can inspect:

- identity,
- skills,
- capabilities,
- security requirements.

### Step 2 — Connect

Create a client using the discovered card.

Conceptually:

```python
client = A2AClient(..., agent_card=card)
```

### Step 3 — Communicate

Create a protocol Message and send it.

Conceptually:

```text
role = user
content = TextPart(...)
```

The remote Server may return a Task.

### Step 4 — Extract the deliverable

The source looks for an Artifact and extracts its text part.

The durable mental model is:

```text
Agent Card
   ↓
A2A Client
   ↓
Message
   ↓
Task
   ↓
Artifact
```

[[IMAGE_NEEDED: Discover-connect-communicate client flow | Client fetches Agent Card -> creates A2AClient -> sends Message -> receives Task -> extracts Artifact | Learner should remember this reusable four-step client pattern]]

---

## 60. Why the handshake proves interoperability

When the example succeeds:

```text
ADK Initiator
   ↓
A2A request
   ↓
LangGraph Greeter
   ↓
A2A Artifact
   ↓
ADK Initiator
```

neither framework needed a custom integration with the other framework.

Only the A2A boundary mattered.

This is the protocol's central value:

```text
N frameworks
do not require
N × N custom framework integrations
```

Instead, each system implements one standard external boundary.

{{exercise:M01.L06.EX06}}

---

## 61. Wrap an existing agent instead of rewriting it

Real organizations already have working agents.

The source next takes the Math Agent from Chapter 6 and exposes it through A2A.

The internal Math Agent stays intact.

A new server adapter is added around it.

Conceptually:

```text
Existing Math Agent
├── prompts
├── tools
├── ADK Runner logic
└── tested behavior

New:
A2A server.py
```

This is the **adapter pattern**.

### Why this matters

Interoperability adoption becomes much easier if:

```text
legacy agent
    +
thin protocol adapter
```

is enough.

You do not want:

```text
rewrite every working agent
```

merely to participate in a new protocol ecosystem.

---

## 62. Translate internal events into A2A events

The Math Agent already emits ADK events.

The A2A adapter must translate them.

Conceptually:

```text
ADK intermediate event
    ↓
A2A status: working

ADK final response
    ↓
A2A Artifact: math_result
    ↓
Task: completed
```

The executor contains no arithmetic logic.

It only knows:

```text
how to run the Math Agent
how to interpret its events
how to publish A2A updates
```

This is a strong separation of concerns.

### Adapter rule

> Translate protocols at the boundary; do not duplicate domain logic in the adapter.

[[IMAGE_NEEDED: Legacy-agent A2A adapter | Existing ADK Math Agent on the right remains unchanged; A2A AgentExecutor wrapper around it translates RequestContext into ADK Runner calls and ADK events into A2A working/completed + Artifact events | Learner should see how interoperability can be added without rewriting core agent logic]]

---

## 63. Capstone: an interoperable Research Assistant

The source moves from one-to-one calls to a realistic multi-agent workflow.

Research naturally breaks into three stages:

```text
Strategize
    ↓
Execute
    ↓
Synthesize
```

### Strategist

Responsibility:

```text
turn a broad research topic
into focused search queries
```

In the source:

```text
LangGraph remote A2A agent
```

### Worker

Responsibility:

```text
execute one search query
and return raw information
```

In the source:

```text
ADK remote A2A agent
```

### Orchestrator & Synthesizer

Responsibility:

```text
receive user topic
call strategist
call worker for each query
collect results
produce final synthesis
```

In the source:

```text
ADK coordinator
```

This proves that a single workflow can combine remote agents implemented with different frameworks.

---

## 64. Trace the Research Assistant workflow

Suppose the user asks:

```text
"What is the impact of quantum computing on cryptography?"
```

### Stage 1 — Strategize

Coordinator calls the remote Query Generator.

It may return focused questions such as:

```text
How does Shor's algorithm affect RSA?
What is post-quantum cryptography?
What is the current state of fault-tolerant quantum computing?
```

### Stage 2 — Execute

For each query, the coordinator calls the remote Researcher.

Conceptually:

```text
query 1 -> Researcher -> result 1
query 2 -> Researcher -> result 2
query 3 -> Researcher -> result 3
```

### Stage 3 — Synthesize

The Coordinator combines:

```text
result 1
result 2
result 3
```

into a coherent answer.

### Why specialist roles help

The Strategist can optimize for:

```text
query quality
coverage
diversity
```

The Worker can optimize for:

```text
retrieval execution
```

The Coordinator can optimize for:

```text
workflow management
final synthesis
```

[[IMAGE_NEEDED: Cross-framework Research Assistant | User -> ADK Coordinator; Coordinator -> A2A -> LangGraph Strategist -> search queries; Coordinator loops over queries -> A2A -> ADK Research Worker -> raw results; results return to Coordinator for final synthesis | Learner should see the strategize-execute-synthesize workflow across framework boundaries]]

---

## 65. Reuse the remote-agent call pattern

The source extracts the repeated A2A client logic into a helper.

Conceptually:

```python
async def call_remote_agent(client, agent_url, prompt):
    card = await discover(agent_url)
    remote = connect(card)
    task = await communicate(remote, prompt)
    return extract_artifact(task)
```

This encapsulates:

```text
discover
connect
communicate
extract
```

### Why a helper matters

Without it, every orchestration step repeats protocol plumbing.

With it, high-level workflow code becomes easier to read:

```python
queries = await call_remote_agent(
    query_generator_url,
    topic
)

for query in queries:
    result = await call_remote_agent(
        researcher_url,
        query
    )
```

This is an example of building a reusable integration primitive.

---

## 66. A2A is not limited to text

Real agents exchange more than strings.

The source demonstrates two important content types:

```text
FilePart
DataPart
```

These build on the Part model introduced in Chapter 8.

---

## 67. Handle file artifacts with `FilePart`

Suppose a remote image-generation agent produces an image.

The Task may contain an Artifact with a FilePart.

Conceptually:

```text
Task
  ↓
Artifact
  ↓
FilePart
  ├── name
  ├── MIME type
  └── bytes or URI
```

The source demonstrates inline file bytes represented through Base64.

A Client must:

1. inspect each Artifact,
2. inspect each Part type,
3. identify FilePart,
4. decode bytes if inline,
5. process or store the file.

### Do not assume every Artifact is text

Bad client logic:

```text
always read artifact.parts[0].text
```

Robust client logic:

```text
inspect part kind
dispatch to correct handler
```

### Practical handler design

```text
TextPart -> display/process text
FilePart -> decode/download/process file
DataPart -> parse structured object
```

[[IMAGE_NEEDED: A2A rich-result dispatcher | Task -> Artifact -> inspect Part type -> Text handler / File handler / Data handler | Learner should understand that A2A clients need typed content handling rather than text-only assumptions]]

---

## 68. Use `DataPart` for structured interactions

Sometimes the remote agent cannot continue without structured information.

Example:

```text
"I need to file an expense."
```

The agent needs:

- date,
- amount,
- purpose.

Instead of asking for each field through free-form conversation, the Server can return:

```text
Task state:
input-required
```

with a DataPart describing a form/schema.

Conceptually:

```json
{
  "type": "form",
  "fields": {
    "date": "...",
    "amount": "...",
    "purpose": "..."
  }
}
```

The Client can:

1. parse the schema,
2. render a form,
3. collect values,
4. send structured data back.

### Why structured data is better here

It reduces ambiguity.

The Client knows:

```text
field names
types
required values
descriptions
```

This is a powerful example of agent-to-application collaboration, not merely agent-to-chat.

{{exercise:M01.L06.EX07}}

---

## 69. Debug distributed agent workflows systematically

Distributed systems fail in more places than local systems.

Potential failure sources include:

```text
discovery
authentication
network
remote server
adapter
internal agent
tool call
artifact parsing
orchestration logic
```

The source provides several debugging techniques.

---

## 70. Inspect the final Task object

The Task is the interaction record.

The source highlights two especially useful fields.

### History

Contains exchanged Messages.

Use it to inspect:

```text
what the Client sent
what the Server asked
what status/context messages occurred
```

### Artifacts

Contains produced deliverables.

Use it to verify:

```text
Did the remote agent actually produce a result?
Was it text, file, or structured data?
Was the expected Artifact missing?
```

This leads to a useful rule:

> When an A2A call behaves unexpectedly, inspect the Task before blaming the model.

---

## 71. Check server logs at the remote boundary

A remote call can fail before internal agent logic even starts.

Server logs help answer:

```text
Did the request arrive?
Did AgentExecutor execute?
Did the internal agent start?
Where did it fail?
```

Good distributed-agent logging should include:

- task/context identifiers,
- request receipt,
- state changes,
- adapter errors,
- internal runtime errors,
- completion/failure.

Avoid logging secrets or unnecessary sensitive content.

---

## 72. Isolate specialists before debugging the whole team

When the Research Assistant fails, do not immediately debug:

```text
Coordinator + Strategist + Researcher + network
```

all at once.

Instead:

```text
test Strategist directly
test Researcher directly
then test Coordinator integration
```

The source uses an A2A CLI client as an isolated test tool.

The durable technique is:

> Replace the orchestrator temporarily with a simple protocol client and test one remote Server at a time.

This separates:

```text
specialist failure
```

from:

```text
orchestration/integration failure
```

[[IMAGE_NEEDED: A2A debugging ladder | Step 1 inspect Task history/artifacts; Step 2 inspect Server logs; Step 3 call specialist directly with isolated CLI/client; Step 4 reconnect full orchestrator | Learner should follow a narrowing debugging strategy rather than debugging the entire distributed system at once]]

---

## 73. Implementation checklist: from local agent to interoperable service

When exposing an existing agent through A2A, ask:

### Public contract

```text
What is the Agent Card?
Which skills are advertised?
Which input/output modes are supported?
What authentication is required?
```

### Adapter

```text
How does AgentExecutor invoke the internal runtime?
How are internal events translated to A2A status?
How is the final result converted to an Artifact?
```

### Task behavior

```text
When is status working?
When can input-required occur?
Can the task be canceled?
How is failure represented?
```

### Rich data

```text
Can the client handle TextPart?
FilePart?
DataPart?
```

### Persistence

```text
Is an in-memory Task store enough?
What happens on restart?
```

### Debugging

```text
Can I inspect Task history?
Can I see Server logs?
Can I test the Server independently?
```

### Security

```text
How are callers authenticated?
What are they authorized to do?
Is transport encrypted?
Are callbacks verified?
```

---

## 74. Source-specific implementation details to re-check

Chapter 9 is a hands-on Early Release chapter.

The following details may change as A2A and its SDK evolve:

- package import paths,
- `AgentExecutor` signatures,
- `RequestContext` APIs,
- `TaskUpdater` methods,
- event queue APIs,
- `A2AStarletteApplication` / `A2AFastAPIApplication`,
- `A2AClient`,
- Agent Card resolver APIs,
- message-send helper methods,
- Task/Artifact/Part object structure,
- CLI commands,
- discovery URI conventions,
- server wrapper configuration.

The durable architecture is:

```text
Server:
Agent Card
+ protocol application
+ executor adapter
+ task/event translation

Client:
discover
+ inspect contract
+ connect
+ send
+ track Task
+ parse Artifact

Orchestrator:
compose remote calls into workflow
```

Do not memorize one SDK version as if it were the protocol itself.

---

## 75. The complete three-layer model

After combining Chapters 7, 8, and 9, the architecture can be understood in three layers.

### Layer 1 — Internal collaboration

```text
Specialist Agents
Shared State
Workflow Agents
Callbacks
Guardrails
```

### Layer 2 — External protocol contract

```text
Agent Card
Client / Server roles
Message / Task
TaskStatus
Artifact / Parts
Polling / SSE / Webhooks
Security
```

### Layer 3 — Implementation adapter

```text
AgentExecutor
A2A server application
A2AClient
framework adapters
remote-call helpers
rich-data handlers
debugging tools
```

This is the bridge from:

```text
architecture
```

to:

```text
running interoperable software
```

---


## Important misconceptions

### Misconception 1
> "More agents always means a better system."

No. Multi-agent design is useful when responsibilities and workflow boundaries justify the added complexity.

### Misconception 2
> "Dynamic orchestration is always better than Sequential."

No. Deterministic workflows are often more reliable when dependencies are known.

### Misconception 3
> "Shared state and direct agent calls are identical."

No. Shared state decouples information exchange from explicit caller-to-callee arguments.

### Misconception 4
> "Sequential orchestration means guardrails are unnecessary."

No. Each stage should still verify that required state exists.

### Misconception 5
> "Callbacks are only for logging."

No. They can enforce policy, validate tools, modify requests, manage context, cache results, and skip steps.

### Misconception 6
> "Every specialist in a live system should speak to the user."

No. The source recommends one front-facing live interface for this architecture.

### Misconception 7
> "Agent-as-a-tool is always the final architecture."

No. It is practical but can hide an entire team behind one black-box interface.

### Misconception 8
> "A2A requires the same framework on both sides."

No. Its purpose is cross-framework interoperability.

### Misconception 9
> "Opaque execution means no status information."

No. Status can be exposed without revealing internal implementation.

### Misconception 10
> "Every request needs a stateful Task."

No. Simple interactions may use direct Messages.

### Misconception 11
> "Artifacts are only files."

No. The source treats Artifacts as the vehicle for deliverables, including text or structured results.

### Misconception 12
> "SSE and WebSockets are the same."

No. SSE is primarily server-to-client streaming; WebSockets support full-duplex messaging.

### Misconception 13
> "If a callback reached my webhook URL, it is trustworthy."

No. Verify its authenticity.

### Misconception 14
> "Authentication means the caller can perform any operation."

No. Authorization determines what the authenticated caller is allowed to do.

### Misconception 15
> "Protocol details are permanent."

No. A2A is evolving, so current specification details should be verified before implementation.

---


### Misconception 16
> "An A2A server requires rewriting the internal agent in A2A-native logic."

No. The source demonstrates an adapter pattern in which an AgentExecutor wraps an existing framework-specific agent.

### Misconception 17
> "AgentExecutor should contain the domain logic of the agent."

No. Its main role is to bridge protocol requests/events to the existing internal runtime and translate results back.

### Misconception 18
> "An A2A client should hard-code assumptions about the remote framework."

No. It should depend on the Agent Card and A2A contract, not whether the Server is implemented with ADK, LangGraph, or another framework.

### Misconception 19
> "Every remote result can be parsed as text."

No. A2A Artifacts can contain FilePart or DataPart content and clients should inspect the Part type.

### Misconception 20
> "If the full Research Assistant fails, debug the full distributed workflow first."

No. Isolate each remote Server and test it independently before debugging orchestration across the entire system.


## Key terminology

| Term | Meaning |
|---|---|
| Multi-agent system | Team of specialized agents collaborating on a larger task |
| Specialist agent | Agent with a narrow responsibility |
| Orchestrator | Component controlling collaboration flow |
| Router | Pattern that selects one specialist |
| Parallel pattern | Multiple independent specialists run concurrently |
| Sequential pattern | Fixed pipeline of dependent stages |
| Circular pattern | Iterative feedback loop |
| Dynamic pattern | Flexible many-to-many communication |
| Shared Session State | Common working memory for collaborating agents |
| `output_key` | Source-specific mechanism for saving an agent result into shared state |
| Callback | Lifecycle hook around agent, model, or tool execution |
| Guardrail | Validation or policy rule that can block unsafe/invalid behavior |
| Prompt templating | Injecting state values into instructions |
| Live Agent | Front-facing real-time conversational interface |
| Agent-as-a-tool | Wrapping another agent/team as a callable capability |
| Handoff | Transfer from one live conversational system to another |
| A2A | Agent2Agent protocol described by the source |
| Opaque execution | Exposing an interface/results without exposing internal implementation |
| End-User | Originator of the high-level request |
| Client | Initiator/orchestrator delegating work |
| Server | Remote agent executing work |
| Agent Card | Discovery/capability contract for a remote agent |
| Skill | Capability advertised by an agent |
| Task | Stateful tracked unit of work |
| TaskStatus | Lifecycle state of a Task |
| Message | Context/status communication |
| Artifact | Deliverable/result |
| Part | Atomic content unit in Messages or Artifacts |
| TextPart | Text content |
| FilePart | File or binary content/reference |
| DataPart | Structured machine-readable content |
| Polling | Repeatedly requesting task status |
| SSE | Server-Sent Events for incremental server-to-client streaming |
| Webhook | Callback endpoint for asynchronous notification |
| Authentication | Verification of identity |
| Authorization | Determination of permitted actions |
| RBAC | Role-Based Access Control |
| TLS | Transport encryption |
| Webhook verification | Verification that a callback is authentic |


| A2A Python SDK | Source-used Python toolkit for implementing A2A clients and servers |
| AgentExecutor | Adapter that connects A2A protocol requests to internal agent logic |
| RequestContext | Source-used SDK object carrying request/task context into the executor |
| EventQueue | Source-used SDK mechanism for emitting server-side A2A events |
| TaskUpdater | Source-used helper for status and Artifact updates |
| A2A web application | Server wrapper handling protocol-level HTTP/JSON-RPC/SSE concerns |
| A2AClient | Client-side SDK abstraction for calling A2A-compliant agents |
| Agent Card Resolver | Client-side discovery helper used to fetch a remote Agent Card |
| Adapter pattern | Wrapping an existing agent behind a new protocol interface without rewriting core logic |
| Event translation | Mapping internal framework events into A2A statuses, Messages, and Artifacts |
| Remote-agent helper | Reusable discover-connect-communicate-extract function |
| Research Strategist | Specialist that decomposes a broad topic into focused search queries |
| Research Worker | Specialist that executes an individual research/search request |
| FilePart handler | Client logic that processes binary/file Artifact content |
| DataPart form | Structured data exchange that can describe fields required from the user |
| Task history | Message sequence associated with a Task and useful for debugging |
| Isolated A2A test | Testing one Server directly outside the full orchestrator |


---

## Self-check

1. Why can a monolithic agent become difficult to maintain?
2. What does the microservices analogy mean for agents?
3. When is Router orchestration appropriate?
4. When is Parallel orchestration appropriate?
5. Why was Sequential chosen for the Teaching Assistant?
6. What is the purpose of shared Session State?
7. What is an output contract for an agent?
8. Why encode fixed workflow logic in orchestration?
9. What are the six callback boundaries described by the source?
10. Why is `before_tool` a useful guardrail point?
11. How can a callback implement caching?
12. Why should Math verify Grammar output exists?
13. How does prompt templating read state?
14. What data does Summary consume?
15. Why should one Live Agent face the user?
16. What is the agent-as-a-tool pattern?
17. Why can agent-as-a-tool become limiting?
18. When is a live handoff appropriate?
19. Why does live handoff lose context?
20. What interoperability problem does A2A solve?
21. What does opaque execution mean?
22. Why is A2A async-first?
23. What are the End-User, Client, and Server roles?
24. Why can an agent be both Client and Server?
25. What is an Agent Card?
26. What are the three discovery approaches described in the source?
27. Why are skills important in an Agent Card?
28. When should an interaction become a Task?
29. What does `input-required` mean?
30. What does `auth-required` mean?
31. What is the difference between Message and Artifact?
32. What is a DataPart useful for?
33. When is polling appropriate?
34. When is SSE appropriate?
35. When is a webhook appropriate?
36. Why is SSE different from a WebSocket?
37. What does authentication prove?
38. What does authorization control?
39. Why should opaque execution be considered a security feature?
40. Why must webhook notifications be verified?
41. Which A2A implementation details should be checked against the current specification?


42. What are the three main source-described A2A Python SDK roles?
43. What does an AgentExecutor translate between?
44. Why is a minimal Greeter useful for the first cross-framework handshake?
45. What are the four reusable client steps: discover, connect, communicate, and what?
46. Why is the handshake independent of whether the remote agent uses LangGraph or ADK?
47. How can an existing Math Agent be made A2A-compliant without rewriting its arithmetic logic?
48. What should happen to internal intermediate events when translating them into A2A?
49. What are the Strategist, Worker, and Coordinator responsibilities in the Research Assistant?
50. Why is a reusable `call_remote_agent` helper valuable?
51. Why should an A2A client inspect Part types instead of assuming text?
52. What information might a FilePart contain?
53. How can DataPart support an input-required form workflow?
54. Which Task fields are especially helpful for debugging according to the source?
55. Why are remote Server logs useful?
56. Why should a problematic specialist be tested independently from the orchestrator?
57. Which Chapter 9 SDK details should be treated as version-specific?

---

## Retain this idea

**Multi-agent architecture has three connected layers. Inside your system, specialists collaborate through orchestration, shared state, callbacks, and guardrails. Across system boundaries, A2A provides discovery, capability contracts, task lifecycle, result formats, transport choices, and security. At implementation time, adapters such as AgentExecutor and clients such as A2AClient translate those contracts into real cross-framework software without forcing every agent to share the same internal framework.**
""".strip(),

        "sections": [
            {"id": "why-multi-agent", "title": "Why Move Beyond a Single Agent?", "order": 1},
            {"id": "microservices", "title": "Split Agents Like Microservices", "order": 2},
            {"id": "patterns", "title": "Five Collaboration Patterns", "order": 3},
            {"id": "pattern-choice", "title": "Choose the Pattern from Dependencies", "order": 4},
            {"id": "shared-state", "title": "Shared Session State", "order": 5},
            {"id": "output-key", "title": "Writing Specialist Outputs into State", "order": 6},
            {"id": "workflow-agent", "title": "Deterministic Workflow Agents", "order": 7},
            {"id": "callbacks", "title": "Callbacks", "order": 8},
            {"id": "agent-callbacks", "title": "Before-Agent and After-Agent Callbacks", "order": 9},
            {"id": "model-callbacks", "title": "Before-Model and After-Model Callbacks", "order": 10},
            {"id": "tool-callbacks", "title": "Before-Tool and After-Tool Callbacks", "order": 11},
            {"id": "callback-patterns", "title": "What Callbacks Can Implement", "order": 12},
            {"id": "seed-context", "title": "Seed the Shared State", "order": 13},
            {"id": "stage-guardrails", "title": "Guard Dependencies Between Stages", "order": 14},
            {"id": "prompt-templating", "title": "Reading Shared State Through Prompt Templates", "order": 15},
            {"id": "teaching-flow", "title": "Trace the Teaching Assistant Flow", "order": 16},
            {"id": "debugging", "title": "Debug Shared State Step by Step", "order": 17},
            {"id": "one-live-agent", "title": "One Live Agent Should Usually Face the User", "order": 18},
            {"id": "agent-as-tool", "title": "Agent-as-a-Tool", "order": 19},
            {"id": "handoffs", "title": "Collaboration vs Live Handoff", "order": 20},
            {"id": "handoff-context", "title": "Why Live Handoff Is Difficult", "order": 21},
            {"id": "walled-gardens", "title": "The Walled Garden Problem", "order": 22},
            {"id": "a2a", "title": "A2A: a Common External Language", "order": 23},
            {"id": "a2a-principles", "title": "Five A2A Principles", "order": 24},
            {"id": "opaque", "title": "Opaque Execution", "order": 25},
            {"id": "async", "title": "Why A2A Is Async-First", "order": 26},
            {"id": "actors", "title": "The Three A2A Actors", "order": 27},
            {"id": "fluid-roles", "title": "Client and Server Are Roles", "order": 28},
            {"id": "agent-card", "title": "Agent Card", "order": 29},
            {"id": "discovery", "title": "Three Discovery Approaches", "order": 30},
            {"id": "card-fields", "title": "Important Agent Card Fields", "order": 31},
            {"id": "message-task", "title": "Direct Message vs Stateful Task", "order": 32},
            {"id": "task", "title": "Task: the Stateful Unit of Work", "order": 33},
            {"id": "task-status", "title": "Task Lifecycle", "order": 34},
            {"id": "artifact-message", "title": "Messages and Artifacts", "order": 35},
            {"id": "parts", "title": "Parts: the Content Atoms", "order": 36},
            {"id": "transport", "title": "Three Communication Patterns", "order": 37},
            {"id": "polling", "title": "Request/Response and Polling", "order": 38},
            {"id": "sse", "title": "Streaming with SSE", "order": 39},
            {"id": "webhook", "title": "Asynchronous Push with Webhooks", "order": 40},
            {"id": "transport-choice", "title": "Choose Transport Based on Workload", "order": 41},
            {"id": "security", "title": "Security Becomes a First-Class Concern", "order": 42},
            {"id": "authentication", "title": "Authentication", "order": 43},
            {"id": "transport-security", "title": "Transport Security", "order": 44},
            {"id": "authorization", "title": "Authorization and Least Privilege", "order": 45},
            {"id": "opaque-security", "title": "Opaque Execution Protects Internals", "order": 46},
            {"id": "webhook-security", "title": "Verify Webhook Callbacks", "order": 47},
            {"id": "internal-external", "title": "Internal Orchestration vs External Interoperability", "order": 48},
            {"id": "combined-architecture", "title": "Combine the Two Chapters into One Architecture", "order": 49},
            {"id": "guidelines", "title": "Practical Design Guidelines", "order": 50},
            {"id": "living-standard", "title": "A2A Is a Living Standard", "order": 51},
            {"id": "end-to-end", "title": "End-to-End Mental Model", "order": 52},
            {"id": "a2a-python-toolkit", "title": "From A2A Theory to Implementation", "order": 53},
            {"id": "a2a-handshake", "title": "First Implementation: a Cross-Framework Handshake", "order": 54},
            {"id": "langgraph-greeter", "title": "Build the Framework-Specific Agent First", "order": 55},
            {"id": "server-agent-card", "title": "Expose the Greeter with an Agent Card", "order": 56},
            {"id": "agent-executor", "title": "AgentExecutor as the Protocol-to-Agent Adapter", "order": 57},
            {"id": "a2a-server-wrapper", "title": "Wrap the Executor in an A2A Web Application", "order": 58},
            {"id": "a2a-client-flow", "title": "Client Flow: Discover, Connect, Communicate", "order": 59},
            {"id": "handshake-proof", "title": "Why the Handshake Proves Interoperability", "order": 60},
            {"id": "legacy-adapter", "title": "Wrap an Existing Agent Instead of Rewriting It", "order": 61},
            {"id": "event-translation", "title": "Translate Internal Events into A2A Events", "order": 62},
            {"id": "research-assistant", "title": "Capstone: an Interoperable Research Assistant", "order": 63},
            {"id": "research-flow", "title": "Trace the Research Assistant Workflow", "order": 64},
            {"id": "remote-helper", "title": "Reuse the Remote-Agent Call Pattern", "order": 65},
            {"id": "rich-data", "title": "A2A Is Not Limited to Text", "order": 66},
            {"id": "filepart", "title": "Handle File Artifacts with FilePart", "order": 67},
            {"id": "datapart", "title": "Use DataPart for Structured Interactions", "order": 68},
            {"id": "a2a-debugging", "title": "Debug Distributed Agent Workflows Systematically", "order": 69},
            {"id": "task-debugging", "title": "Inspect the Final Task Object", "order": 70},
            {"id": "server-logs", "title": "Check Server Logs at the Remote Boundary", "order": 71},
            {"id": "isolated-testing", "title": "Isolate Specialists Before Debugging the Whole Team", "order": 72},
            {"id": "implementation-checklist", "title": "Implementation Checklist", "order": 73},
            {"id": "chapter9-boundaries", "title": "Source-Specific Implementation Details to Re-Check", "order": 74},
            {"id": "three-layer-model", "title": "The Complete Three-Layer Model", "order": 75},
        ],
    },

    "exercises": [
        {
            "id": "M01.L06.EX01",
            "title": "Choose a Collaboration Pattern",
            "lesson_code": "M01.L06",
            "section_id": "pattern-choice",
            "placement": "after_section",
            "description": "Map different workflows to the correct multi-agent pattern.",
            "instructions": (
                "Choose Router, Parallel, Sequential, Circular, or Dynamic for each case:\n"
                "1. Billing vs technical support routing.\n"
                "2. Searching flights and hotels simultaneously.\n"
                "3. Clean -> analyze -> summarize data.\n"
                "4. Writer and editor repeatedly revise a draft.\n"
                "5. A scientific expert team communicates flexibly.\n"
                "Explain the dependency structure behind every choice."
            ),
            "expected_output": "A five-row decision table with pattern and justification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["multi-agent-design", "orchestration"],
        },
        {
            "id": "M01.L06.EX02",
            "title": "Design Shared State and Guardrails",
            "lesson_code": "M01.L06",
            "section_id": "stage-guardrails",
            "placement": "after_section",
            "description": "Design a robust state contract for a three-stage pipeline.",
            "instructions": (
                ('1. Create Intake -> Eligibility -> Recommendation agents.\n'
                 '2. Define required and produced state keys for each.\n'
                 '3. Add one before-agent guardrail to each stage.\n'
                 '4. Add one before-tool permission/validation rule.\n'
                 '5. Show state after each stage.')
            ),
            "expected_output": "State schema, guardrails, and stage-by-stage snapshots.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["shared-state", "callbacks", "guardrails"],
        },
        {
            "id": "M01.L06.EX03",
            "title": "Design an Agent Card and Task",
            "lesson_code": "M01.L06",
            "section_id": "task-status",
            "placement": "after_section",
            "description": "Define the public contract of a remote Academic Research Agent.",
            "instructions": (
                ('1. Define its name, description, two skills, supported capabilities, and security needs.\n'
                 '2. Then define a long-running research Task with possible states.\n'
                 '3. Write example Messages for working, input-required, and auth-required.\n'
                 '4. Define the final Artifact and its Part types.')
            ),
            "expected_output": "An Agent Card sketch plus Task lifecycle and result contract.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agent-card", "tasks", "artifacts"],
        },
        {
            "id": "M01.L06.EX04",
            "title": "Choose an A2A Communication Mechanism",
            "lesson_code": "M01.L06",
            "section_id": "transport-choice",
            "placement": "after_section",
            "description": "Choose between direct/polling, SSE, and webhook push.",
            "instructions": (
                "Choose the best mechanism for:\n"
                "1. 245 * 81.\n"
                "2. Generating a long report while showing text as it appears.\n"
                "3. Rendering a video that may take 40 minutes.\n"
                "4. Research that may pause for human approval.\n"
                "Explain why an open connection is or is not appropriate."
            ),
            "expected_output": "A communication decision table with reasoning.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["polling", "sse", "webhooks", "a2a"],
        },
        {
            "id": "M01.L06.EX05",
            "title": "Architect a Cross-Framework Agent Ecosystem",
            "lesson_code": "M01.L06",
            "section_id": "guidelines",
            "placement": "after_section",
            "description": "Combine internal orchestration with remote A2A collaboration.",
            "instructions": (
                ('1. Design a university assistant with one Live Agent, three internal specialists, and one remote Research Agent built with another framework.\n'
                 '2. Define internal pattern, shared state, callbacks, remote Agent Card skills, Task type, transport choice, returned Artifact, authentication, authorization, TLS, and webhook verification where applicable.')
            ),
            "expected_output": "A complete architecture diagram and design specification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["multi-agent-architecture", "a2a", "security"],
        },
        {
            "id": "M01.L06.EX06",
            "title": "Design a Cross-Framework A2A Handshake",
            "lesson_code": "M01.L06",
            "section_id": "handshake-proof",
            "placement": "after_section",
            "description": (
                "Design a minimal proof that two agents using different internal frameworks "
                "can communicate through the same external protocol."
            ),
            "instructions": (
                "Design a Greeter Server and an Initiator Client using different frameworks.\n"
                "1. Define the Greeter Agent Card and one advertised skill.\n"
                "2. Define what the AgentExecutor must do.\n"
                "3. Draw Discover -> Connect -> Communicate -> Extract Artifact.\n"
                "4. Show which details are framework-specific and which are A2A-specific.\n"
                "5. Explain why the Client should not need to import or understand the Server framework."
            ),
            "expected_output": (
                "A handshake architecture diagram, public Agent Card sketch, and protocol/framework boundary explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["a2a-python-sdk", "agent-executor", "a2a-client", "interoperability"],
        },
        {
            "id": "M01.L06.EX07",
            "title": "Wrap a Legacy Agent with an A2A Adapter",
            "lesson_code": "M01.L06",
            "section_id": "event-translation",
            "placement": "after_section",
            "description": (
                "Practice applying the adapter pattern without duplicating existing domain logic."
            ),
            "instructions": (
                "Assume you already have a tested Weather Agent.\n"
                "1. Define its public Agent Card skills.\n"
                "2. Describe how AgentExecutor passes user input into its existing runtime.\n"
                "3. Define how internal intermediate events map to A2A working status.\n"
                "4. Define how the final response becomes an Artifact.\n"
                "5. Explain what logic must remain inside the original Weather Agent rather than the adapter."
            ),
            "expected_output": (
                "An adapter specification that exposes the existing agent without rewriting its core weather logic."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["adapter-pattern", "event-translation", "agent-card"],
        },
        {
            "id": "M01.L06.EX08",
            "title": "Build and Debug an Interoperable Research Workflow",
            "lesson_code": "M01.L06",
            "section_id": "isolated-testing",
            "placement": "after_section",
            "description": (
                "Combine orchestration, remote calls, rich data handling, and debugging."
            ),
            "instructions": (
                "Design a Coordinator, remote Strategist, and remote Research Worker.\n"
                "1. Define the A2A call sequence.\n"
                "2. Specify what each remote Agent Card advertises.\n"
                "3. Define a reusable call_remote_agent helper contract.\n"
                "4. Add one FilePart result and one DataPart input-required interaction.\n"
                "5. Describe how you would inspect Task history and Artifacts on failure.\n"
                "6. Describe how you would test each Server independently before debugging the full workflow."
            ),
            "expected_output": (
                "A cross-framework research architecture plus a distributed-debugging checklist."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "cross-framework-agents",
                "remote-agent-helper",
                "filepart",
                "datapart",
                "distributed-debugging",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L06.QZ01",
        "title": "Multi-Agent Systems, A2A Interoperability & Implementation — Knowledge Check",
        "lesson_code": "M01.L06",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L06.Q01",
                "section_id": "microservices",
                "question": "Why split a large agent into specialists?",
                "options": [
                    "To make responsibilities easier to build, test, and maintain",
                    "To remove orchestration",
                    "To make every agent use every tool",
                    "To eliminate state",
                ],
                "correct": 0,
                "explanation": "Specialization reduces responsibility overload and improves modularity.",
            },
            {
                "id": "M01.L06.Q02",
                "section_id": "patterns",
                "question": "Which pattern fits independent tasks that can run at the same time?",
                "options": ["Parallel", "Sequential", "Circular", "Single-agent only"],
                "correct": 0,
                "explanation": "Parallel execution is appropriate when tasks have no dependency on one another.",
            },
            {
                "id": "M01.L06.Q03",
                "section_id": "pattern-choice",
                "question": "Why is Sequential appropriate for Grammar -> Math -> Summary?",
                "options": [
                    "Each stage depends on earlier outputs",
                    "The stages must run randomly",
                    "All tasks are independent",
                    "Each agent should answer the user separately",
                ],
                "correct": 0,
                "explanation": "The workflow has a strict dependency order.",
            },
            {
                "id": "M01.L06.Q04",
                "section_id": "shared-state",
                "question": "What is shared Session State used for?",
                "options": [
                    "A common workbench for exchanging intermediate results",
                    "Replacing every model call",
                    "Storing only UI code",
                    "Preventing information exchange",
                ],
                "correct": 0,
                "explanation": "Agents read and write shared working context.",
            },
            {
                "id": "M01.L06.Q05",
                "section_id": "tool-callbacks",
                "question": "Where should permissions be checked immediately before a risky tool executes?",
                "options": ["before_tool", "after_agent", "after_model", "after_tool only"],
                "correct": 0,
                "explanation": "The before-tool boundary can block invalid or unauthorized execution.",
            },
            {
                "id": "M01.L06.Q06",
                "section_id": "one-live-agent",
                "question": "Why use one front-facing Live Agent?",
                "options": [
                    "To give the user one coherent real-time conversation",
                    "Because specialists cannot exist",
                    "Because state works with only one agent",
                    "Because tools cannot run in the background",
                ],
                "correct": 0,
                "explanation": "Background specialists can collaborate while one live interface handles user interaction.",
            },
            {
                "id": "M01.L06.Q07",
                "section_id": "a2a",
                "question": "What problem does A2A address?",
                "options": [
                    "Cross-framework agent isolation and custom integration",
                    "Audio echo",
                    "Python virtual environments",
                    "Image quality",
                ],
                "correct": 0,
                "explanation": "A2A standardizes external communication across heterogeneous agents.",
            },
            {
                "id": "M01.L06.Q08",
                "section_id": "opaque",
                "question": "What does opaque execution mean?",
                "options": [
                    "The remote agent can hide internal implementation while exposing status/results",
                    "The client receives no result",
                    "The agent cannot have logs",
                    "The connection is unencrypted",
                ],
                "correct": 0,
                "explanation": "Clients rely on the service contract rather than internal implementation details.",
            },
            {
                "id": "M01.L06.Q09",
                "section_id": "actors",
                "question": "Which role delegates work to a remote specialist?",
                "options": ["Client", "Artifact", "Part", "TLS"],
                "correct": 0,
                "explanation": "The Client acts as initiator/orchestrator.",
            },
            {
                "id": "M01.L06.Q10",
                "section_id": "agent-card",
                "question": "What is an Agent Card primarily for?",
                "options": [
                    "Discovery and capability/security/interface description",
                    "Storing hidden model reasoning",
                    "Replacing Tasks",
                    "Executing local Python automatically",
                ],
                "correct": 0,
                "explanation": "The Agent Card describes a remote agent's public contract.",
            },
            {
                "id": "M01.L06.Q11",
                "section_id": "task-status",
                "question": "Which state means the remote agent needs more information?",
                "options": ["input-required", "completed", "working", "submitted"],
                "correct": 0,
                "explanation": "input-required signals that progress is blocked pending clarification.",
            },
            {
                "id": "M01.L06.Q12",
                "section_id": "artifact-message",
                "question": "What is the difference between Message and Artifact?",
                "options": [
                    "Message carries context/status; Artifact carries the deliverable",
                    "Artifact is only an image",
                    "Message is always a file",
                    "There is no difference",
                ],
                "correct": 0,
                "explanation": "The source separates task communication from the final work product.",
            },
            {
                "id": "M01.L06.Q13",
                "section_id": "sse",
                "question": "How does SSE differ from WebSocket live interaction?",
                "options": [
                    "SSE is primarily server-to-client streaming",
                    "SSE cannot send text",
                    "WebSockets are only for files",
                    "They are the same protocol",
                ],
                "correct": 0,
                "explanation": "WebSockets are full-duplex; SSE is primarily one-way server streaming.",
            },
            {
                "id": "M01.L06.Q14",
                "section_id": "webhook",
                "question": "Which pattern best fits an hour-long background task?",
                "options": [
                    "Webhook-based asynchronous push",
                    "Keep one synchronous HTTP response open for an hour",
                    "No task tracking",
                    "Poll every millisecond",
                ],
                "correct": 0,
                "explanation": "Webhook notification avoids holding a connection open for long jobs.",
            },
            {
                "id": "M01.L06.Q15",
                "section_id": "authorization",
                "question": "What is the difference between authentication and authorization?",
                "options": [
                    "Authentication verifies identity; authorization determines permitted actions",
                    "Authentication encrypts; authorization compresses",
                    "Authorization verifies identity; authentication selects model",
                    "They are identical",
                ],
                "correct": 0,
                "explanation": "Identity and permission are separate security concerns.",
            },
            {
                "id": "M01.L06.Q16",
                "section_id": "webhook-security",
                "question": "Why verify webhook notifications?",
                "options": [
                    "To confirm the callback came from a trusted sender",
                    "To increase model temperature",
                    "To replace TLS",
                    "To avoid task IDs",
                ],
                "correct": 0,
                "explanation": "Internet-facing callbacks can be forged if authenticity is not checked.",
            },
            {
                "id": "M01.L06.Q17",
                "section_id": "living-standard",
                "question": "Why should exact A2A fields and endpoints be re-verified before implementation?",
                "options": [
                    "Because A2A is described as an evolving standard",
                    "Because protocols never document fields",
                    "Because all agents use different internet protocols",
                    "Because security is optional",
                ],
                "correct": 0,
                "explanation": "The durable concepts remain useful while specification details can evolve.",
            },
            {
                "id": "M01.L06.Q18",
                "section_id": "agent-executor",
                "question": "What is the main architectural role of AgentExecutor in the source?",
                "options": [
                    "Bridge A2A protocol requests to framework-specific agent logic and translate results back",
                    "Replace the agent's domain logic",
                    "Store only frontend assets",
                    "Train the foundation model",
                ],
                "correct": 0,
                "explanation": (
                    "AgentExecutor is the adapter boundary between the A2A server protocol and the internal agent runtime."
                ),
            },
            {
                "id": "M01.L06.Q19",
                "section_id": "a2a-client-flow",
                "question": "What is the reusable A2A client sequence demonstrated by the source?",
                "options": [
                    "Discover -> Connect -> Communicate -> Extract result",
                    "Train -> Fine-tune -> Deploy -> Delete",
                    "Prompt -> Screenshot -> Compile -> Stream",
                    "Authenticate -> Rewrite framework -> Run locally -> Stop",
                ],
                "correct": 0,
                "explanation": (
                    "The Client discovers the Agent Card, builds a client, sends a Message, and extracts the Task Artifact."
                ),
            },
            {
                "id": "M01.L06.Q20",
                "section_id": "legacy-adapter",
                "question": "What is the main benefit of wrapping a legacy agent with an A2A adapter?",
                "options": [
                    "The existing core agent can remain unchanged while gaining a standardized external interface",
                    "Every internal tool must be rewritten",
                    "The agent no longer needs tests",
                    "The framework-specific runtime is removed",
                ],
                "correct": 0,
                "explanation": (
                    "The adapter pattern lets organizations expose existing agents without duplicating or replacing their domain logic."
                ),
            },
            {
                "id": "M01.L06.Q21",
                "section_id": "research-assistant",
                "question": "What are the three major roles in the source's Research Assistant?",
                "options": [
                    "Strategist, Research Worker, and Orchestrator/Synthesizer",
                    "Browser, database, and CSS renderer",
                    "Trainer, evaluator, and tokenizer",
                    "Authentication server, firewall, and load balancer",
                ],
                "correct": 0,
                "explanation": (
                    "The workflow separates query planning, retrieval execution, and final synthesis."
                ),
            },
            {
                "id": "M01.L06.Q22",
                "section_id": "filepart",
                "question": "Why must a robust A2A client inspect each Artifact Part type?",
                "options": [
                    "Because results may contain text, files, structured data, or a mixture",
                    "Because every Part is guaranteed to be text",
                    "Because FilePart cannot appear in Artifacts",
                    "Because DataPart is only used internally by models",
                ],
                "correct": 0,
                "explanation": (
                    "A modality-independent client should dispatch handling based on the actual Part type."
                ),
            },
            {
                "id": "M01.L06.Q23",
                "section_id": "datapart",
                "question": "Which use case best demonstrates DataPart in the source?",
                "options": [
                    "Returning a structured form/schema when the agent needs specific user input",
                    "Streaming microphone PCM over WebSocket",
                    "Storing only a PNG file",
                    "Choosing a foundation model",
                ],
                "correct": 0,
                "explanation": (
                    "DataPart can carry machine-readable structured information such as fields required to continue a Task."
                ),
            },
            {
                "id": "M01.L06.Q24",
                "section_id": "a2a-debugging",
                "question": "What should you inspect first when an A2A interaction returns an unexpected result?",
                "options": [
                    "The Task history and Artifacts, then Server logs and isolated Server behavior",
                    "Only the final UI text",
                    "The user's screen resolution",
                    "Retrain every agent immediately",
                ],
                "correct": 0,
                "explanation": (
                    "The source recommends using the Task as a source of truth, inspecting server logs, and isolating individual agents."
                ),
            },
            {
                "id": "M01.L06.Q25",
                "section_id": "three-layer-model",
                "type": "open",
                "question": (
                    "Design a complete agent ecosystem with one Live Agent, three internal specialists, "
                    "and one remote cross-framework Research Agent. Explain internal orchestration and shared "
                    "state, callbacks, Agent Card discovery, AgentExecutor server adaptation, A2AClient calls, "
                    "Task lifecycle, chosen transport, Text/File/Data Part handling, returned Artifacts, "
                    "security controls, and a distributed-debugging plan."
                ),
            },
        ],
        "passing_score": 70,
    },
}
