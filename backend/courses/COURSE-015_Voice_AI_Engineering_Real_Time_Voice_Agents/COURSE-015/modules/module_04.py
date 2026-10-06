"""M01.L04 — Core Components of an Agent Framework.

One source chapter -> one complete learner-facing Lesson + inline Images
+ inline Exercises + lesson Quiz.

Source alignment:
- Chapter 5: Core Components of an Agent Framework
- Early Release draft; page numbers were not provided in the supplied source.

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Agent Foundations & Framework Architecture"

MODULE_DESCRIPTION = (
    "Understand the five core components that turn an LLM application into a "
    "reliable agent system: runtime/orchestration, memory, tooling, multi-agent "
    "communication, and structured instructions/prompting, with practical examples "
    "from Google ADK, LangGraph, and CrewAI."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Early Release draft; page numbers not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Core Components of an Agent Framework",

    "slug": "agent-foundations-m01-l04",

    "description": (
        "Learn what an agent framework actually provides beyond an LLM loop: "
        "execution control, state, checkpointing, asynchronous operations, memory, "
        "secure tools, collaboration, prompt construction, and framework-level "
        "orchestration choices."
    ),

    "order": 4,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "agent-frameworks",
        "orchestration",
        "runtime",
        "state-management",
        "checkpointing",
        "async-agents",
        "memory",
        "rag-memory",
        "tooling",
        "function-calling",
        "multi-agent-systems",
        "prompting",
        "langgraph",
        "google-adk",
        "crewai",
    ],

    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Core Components of an Agent Framework",

        "content": r"""
# Core Components of an Agent Framework

> **Lesson:** M01.L04  
> **Module:** Agent Foundations & Framework Architecture  
> **Source alignment:** Chapter 5 of the supplied Early Release material.  
> This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why production-grade agents need more than an LLM inside a loop.
- Identify the major capabilities expected from an agent framework.
- Explain the responsibilities of a runtime/orchestration engine.
- Describe the perceive–reason–act execution cycle.
- Explain structured state, reducers, checkpointing, pause/resume behavior, and lifecycle management.
- Explain why agent runtimes are often asynchronous.
- Distinguish deterministic routing from LLM-driven routing.
- Explain when concurrency and parallelism are useful.
- Distinguish short-term memory from long-term memory.
- Explain how long-term memory can use a RAG-style ingest/embed/store/search pipeline.
- Explain why memory retrieval is often more difficult than memory storage.
- Describe the three core responsibilities of a tooling interface: definition, selection, and secure execution.
- Explain why schema-based function calling is more reliable than parsing ad-hoc model text.
- Explain how frameworks support delegation and information sharing between agents.
- Distinguish deterministic multi-agent workflows from dynamic supervisor-based delegation.
- Explain how a prompting system separates identity, task context, state, and tool schemas.
- Compare the architectural philosophies of CrewAI, Google ADK, and LangGraph as described in the source.
- Select a framework style based on desired abstraction and control.

---

## 1. Why agent frameworks exist

A simple agent prototype can be surprisingly short.

At first, the flow might look like this:

```text
1. Receive user input
2. Call the LLM
3. If it requests a tool, run the tool
4. Send the result back
5. Return the final answer
```

For one simple interaction, that may be enough.

But production systems introduce much harder questions:

```text
What if the agent needs several tools?
What if one tool depends on another?
What if a tool fails?
What if the agent must pause for a person?
What if it needs state across many steps?
What if several agents collaborate?
What if two tasks can run in parallel?
What if the process must resume tomorrow?
```

At this point, the problem is no longer just:

> "How do I call an LLM?"

It becomes:

> "How do I reliably manage a stateful, multi-step reasoning system?"

That is the problem an agent framework tries to solve.

### A framework is more than an LLM loop

The source identifies several framework-level capabilities:

| Capability | What it handles | Why it matters |
|---|---|---|
| Orchestration | Control flow, state, execution | Prevents tangled manual loops |
| Memory | Short- and long-term context | Enables coherence and recall |
| Tool Use | External capabilities | Lets the agent act beyond the model |
| Multi-Agent Systems | Coordination among specialists | Supports modular decomposition |
| Human-in-the-Loop | Pause for human input/approval | Improves safety and reliability |
| Streaming & Observability | Live feedback, tracing, monitoring | Helps users and developers understand execution |

A framework therefore provides operational infrastructure around the model.

[[IMAGE_NEEDED: Agent framework capability map | A central Agent Framework box connected to Orchestration, Memory, Tools, Multi-Agent Communication, Human-in-the-Loop, and Streaming/Observability | Learner should notice that the framework surrounds the model with operational capabilities rather than replacing the model]]

---

## 2. The runtime: the agent's conductor

The source describes the runtime as the agent's **central nervous system**.

If the LLM is the reasoning engine, the runtime manages:

- lifecycle,
- state,
- control flow,
- repeated execution,
- tool calls,
- routing,
- concurrency,
- pausing,
- resuming,
- and termination.

Without a runtime, the developer has to manually recreate these behaviors.

### The developer's dilemma

Imagine writing everything yourself.

You may quickly accumulate code like:

```python
while True:
    response = call_llm(...)

    if wants_tool_a(response):
        ...
    elif wants_tool_b(response):
        ...
    elif needs_human(response):
        ...
    elif should_retry(response):
        ...
    elif finished(response):
        break
```

Then add state:

```python
history = [...]
tool_results = [...]
current_step = ...
pending_approval = ...
retry_count = ...
```

Then add persistence, errors, asynchronous calls, and multiple agents.

The code becomes difficult to reason about.

A runtime exists to provide formal abstractions for these concerns.

---

## 3. The perceive–reason–act execution loop

The defining behavior of an agent is cyclical.

A useful abstraction is:

```text
Perceive
   ↓
Reason
   ↓
Act
   ↓
Observe result
   ↓
Reason again
```

The runtime keeps this cycle moving until the task reaches a stopping condition.

### Explicit graph example

The source uses LangGraph to demonstrate the loop.

Conceptually:

```python
def should_continue(state):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END
```

Then:

```text
chatbot
   ↓
conditional decision
   ├──> tools
   │      ↓
   └──── chatbot
```

This is useful because the loop is no longer hidden inside an improvised `while`.

It becomes part of the workflow definition.

### Why explicit control flow matters

A runtime can make these transitions:

- visible,
- testable,
- resumable,
- traceable,
- and easier to change.

This is especially valuable when workflows contain:

- cycles,
- branches,
- retries,
- approvals,
- or multiple agents.

[[IMAGE_NEEDED: Perceive-reason-act runtime loop | A graph showing Reasoning node -> conditional edge -> Tool node -> back to Reasoning, with an END path when no more actions are required | Learner should notice how a framework turns a manual while-loop into explicit orchestration]]

---

## 4. State management: the agent's working data

An agent without state is little more than a function:

```text
input -> output
```

A real agent may need to remember information produced during execution.

Examples:

```text
messages
tool results
user name
selected plan
current workflow step
research findings
approval status
```

A framework therefore needs a structured state model.

### State is more than a dictionary

A framework can define rules for how updates should be merged.

The source uses a LangGraph example with a reducer:

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str
```

The important part is not the syntax.

The important concept is:

> An update to `messages` should be merged according to a known rule rather than blindly replacing the old value.

This reduces accidental state corruption.

### Reducer mental model

Without a reducer:

```text
old messages
    ↓
new messages replace everything
```

With a reducer:

```text
old messages
    +
new messages
    ↓
merged history
```

Structured update rules become increasingly important as workflows grow.

{{exercise:M01.L04.EX01}}

---

## 5. Lifecycle management: pause, resume, and stop

Some tasks do not finish in one uninterrupted run.

Examples:

```text
waiting for human approval
waiting for an external system
long-running research
multi-stage business process
workflow paused overnight
```

To support this, a runtime needs **checkpointing**.

### What is a checkpoint?

A checkpoint is a saved snapshot of execution state.

It may include:

- data,
- messages,
- tool results,
- workflow position,
- pending actions,
- session identifiers.

The key idea is:

```text
save state
   ↓
stop execution
   ↓
reload later
   ↓
continue from the same workflow point
```

### Human-in-the-loop depends on this

Suppose an agent reaches:

```text
"Send contract to customer?"
```

The system may need to:

1. save the workflow,
2. ask a human,
3. wait,
4. receive approval,
5. resume exactly where it stopped.

That is difficult without a persistent runtime.

The source illustrates this with ADK's session services, where a session identifier maps to persistent runtime state.

The exact class names are framework-specific.

The durable concept is checkpointed lifecycle management.

---

## 6. Why agent runtimes are asynchronous

Agents spend a large amount of time waiting.

They may wait for:

- an LLM response,
- an HTTP API,
- a database,
- a vector search,
- another agent,
- human approval.

These are mostly I/O-bound operations.

If the whole application blocks during each wait, resources are wasted and the experience becomes sluggish.

### Async mental model

Synchronous:

```text
Task A waits
everything waits
```

Asynchronous:

```text
Task A waits for API
        meanwhile
Task B can progress
```

The source connects async execution to several capabilities.

### Streaming

The system can emit events or partial output while other work continues.

### Concurrency

Independent tools or agents can run at the same time.

### Responsiveness

One waiting agent should not freeze the entire server process.

This is why many agent runtimes expose `async` execution methods.

---

## 7. Control flow and routing

After one step finishes, where should execution go next?

There are two broad strategies.

### 7.1 Deterministic routing

The developer defines the path.

Example:

```text
Manager
   ↓
Researcher
   ↓
Writer
```

Advantages:

- predictable,
- testable,
- easier to audit.

The source uses hierarchical and sequential framework processes as examples of deterministic control.

### 7.2 Dynamic routing

The model helps decide the next destination.

Example:

```text
User request
     ↓
Coordinator
     ├── Billing Agent
     └── Support Agent
```

The coordinator interprets the request and chooses the specialist.

This is more flexible, but introduces uncertainty.

### A useful rule

Use deterministic routing when:

```text
the workflow is known in advance
```

Use dynamic routing when:

```text
the correct next step depends on semantic interpretation
```

Many systems combine both.

---

## 8. Concurrency and parallelism

Some subtasks do not depend on one another.

For example:

```text
Fetch weather
Fetch news
```

These can run at the same time.

Sequential execution:

```text
weather -> wait -> news -> wait
```

Parallel execution:

```text
        ┌-> weather ->┐
start --|             |-> combine
        └-> news ---->┘
```

A framework can abstract the complexity of:

- scheduling,
- async calls,
- waiting for all results,
- merging outputs.

The source illustrates this with ADK's `ParallelAgent`.

The exact class is framework-specific.

The durable concept is:

> Independent work should not be serialized unnecessarily.

[[IMAGE_NEEDED: Sequential versus parallel agent execution | Left side shows Weather then News sequentially; right side shows Weather and News running simultaneously before a Gather step | Learner should notice the latency advantage when tasks are independent]]

---

## 9. Memory is a structured system, not one feature

The source divides memory into two categories:

```text
Short-term memory
Long-term memory
```

They solve different problems.

### Short-term memory

Scope:

```text
current session or task
```

Examples:

- chat history,
- recent tool results,
- intermediate calculations,
- current workflow state.

### Long-term memory

Scope:

```text
across sessions and over time
```

Examples:

- user preferences,
- persistent facts,
- previous interactions,
- durable knowledge.

The important lesson is:

> "Memory" is not simply saving everything.

A robust framework must decide:

- what is stored,
- where,
- for how long,
- and how relevant information is retrieved.

---

## 10. Short-term memory: the conversational workspace

Short-term memory is the agent's working context.

Suppose a user says:

```text
User: My preferred temperature unit is Celsius.
User: What's the weather in Tokyo?
```

Within the same session, the agent should be able to use that preference.

Short-term state may contain:

```python
{
    "messages": [...],
    "preferred_unit": "Celsius",
    "latest_tool_result": {...}
}
```

The runtime manages updates so the next reasoning step receives the information it needs.

### Context-window challenge

A naive implementation might keep appending everything forever.

Eventually:

- context grows,
- cost grows,
- irrelevant history accumulates,
- model limits may be reached.

So production memory systems often need policies for:

- summarization,
- trimming,
- selective retention,
- retrieval.

The source emphasizes framework-managed structured session state rather than manual list handling.

---

## 11. Long-term memory: persistent knowledge

Long-term memory solves a different problem.

Example:

```text
Week 1:
"My shipping address is ..."

Week 2:
"Ship my order to my address."
```

The second conversation needs information from a previous session.

### Storage is not the hard part

Saving data to a database is straightforward.

The difficult question is:

> Which memory is relevant right now?

You usually cannot place a user's entire lifetime history into one prompt.

So long-term memory becomes an information-retrieval problem.

### RAG-style memory pipeline

The source describes a common flow:

```text
1. Ingest
2. Embed
3. Store
4. Search
```

#### Ingest

Identify useful information to retain.

#### Embed

Convert it into a semantic vector representation.

#### Store

Persist the embedding and original content.

#### Search

Embed the new query and retrieve similar memories.

Conceptually:

```text
Past memory:
"User prefers AI ethics articles"
        ↓ embed
     [vector]
        ↓ store

New query:
"Recommend a topic for me"
        ↓ embed
     [vector]
        ↓ similarity search
retrieve relevant preference
```

[[IMAGE_NEEDED: Long-term memory RAG pipeline | Conversation facts -> Ingest -> Embed -> Vector Store; later Query -> Embed -> Similarity Search -> Relevant memories -> Agent context | Learner should notice that retrieval, not just storage, is the core challenge]]

---

## 12. How short-term and long-term memory work together

The most useful agent combines both memory types.

A typical flow:

```text
New user query
      ↓
Short-term session state
      ↓
Agent notices missing information
      ↓
Search long-term memory
      ↓
Retrieve relevant fact
      ↓
Add fact to current working context
      ↓
Generate response
```

Example:

```text
User: Suggest something I'd enjoy reading.
```

Short-term memory may not contain a preference.

The agent searches long-term memory and retrieves:

```text
Favorite topic = AI ethics
```

That fact then becomes part of the current context.

The important principle is:

> Long-term memory is usually useful only after its relevant pieces are brought into short-term working context.

{{exercise:M01.L04.EX02}}

---

## 13. The tooling interface: connecting reasoning to action

An agent that can only generate text is limited.

A tooling interface lets the agent interact with external systems.

Examples:

- web search,
- databases,
- email,
- calendars,
- code execution,
- device control.

The source identifies three core responsibilities:

```text
1. Tool definition
2. Tool selection
3. Secure execution
```

---

## 14. Tool definition and registration

Without framework support, a developer might manually invent a protocol:

```text
_TOOL_CALL_: get_weather(city='Cairo')
```

Then parse it with strings or regular expressions.

This is brittle.

A framework instead lets developers register code as a formal tool.

Conceptually:

```python
@tool
def calculator(expression: str) -> str:
    ...
```

The framework can inspect:

- function name,
- docstring,
- argument names,
- type hints.

Then generate a structured schema.

### Introspection

The process is roughly:

```text
Python function
   ↓ inspect
name + docstring + types
   ↓
tool schema
   ↓
model sees formal interface
```

This reduces custom boilerplate.

---

## 15. Tool selection through structured function calling

Once schemas exist, the model can produce structured tool requests.

Instead of:

```text
"Please run calculator somehow"
```

the system receives something like:

```json
{
  "name": "calculator",
  "arguments": {
    "expression": "2+2"
  }
}
```

This is more reliable because:

- the function name is explicit,
- arguments are structured,
- types can be validated,
- execution can be mapped to registered code.

The source describes this as a major improvement over free-form text parsing.

[[IMAGE_NEEDED: Code introspection to function calling | Python function -> introspection -> JSON schema -> LLM tool selection -> structured function call -> registered function execution | Learner should understand how frameworks convert native code into model-usable tool interfaces]]

---

## 16. Secure tool execution

A tooling interface should not simply execute anything the model invents.

The source highlights several safety responsibilities.

### Registered tools only

If a function is not registered, it should not be callable through the framework.

### Argument validation

If the schema expects:

```text
city: string
```

then an invalid argument should be caught before execution.

### Sandboxing

High-risk tools may require isolation.

For example, code execution should not have unrestricted access to the host system.

The source gives a dangerous conceptual example involving arbitrary `exec()` and system commands to illustrate why secure execution matters.

The lesson is:

> Tool interfaces are security boundaries.

### Important note on examples

The source also shows a simple calculator example using `eval()` to demonstrate framework registration.

That example is useful for understanding tool wrapping, but the same chapter explicitly emphasizes sandboxing and secure execution for risky capabilities.

So the educational takeaway is not "use unrestricted eval."

It is:

> Frameworks should make tool registration convenient while execution remains controlled and validated.

---

## 17. How frameworks represent tools

The source compares two broad patterns.

### Function-as-a-tool

Frameworks such as CrewAI and ADK can expose ordinary Python functions as tools.

Conceptually:

```python
def get_weather(city: str) -> dict:
    ...

agent = Agent(
    tools=[get_weather]
)
```

The framework handles:

- introspection,
- schema generation,
- dispatch.

### Tool node

LangGraph represents tool execution as a graph node.

Conceptually:

```text
Reasoning node
     ↓ tool call?
ToolNode
     ↓
Reasoning node
```

This fits LangGraph's control-flow-first philosophy.

Neither representation changes the underlying principle:

```text
model requests action
runtime routes action
registered tool executes
result returns to state
```

---

## 18. Multi-agent communication

A complex problem can be decomposed into specialists.

Example:

```text
Market Report System
├── Research Agent
├── Data Analysis Agent
└── Writing Agent
```

But specialists are useful only if they can:

- delegate work,
- share context,
- return results,
- and coordinate control flow.

That is what the multi-agent communication layer provides.

### The developer's dilemma

Without framework support, you would have to manually build:

- routing,
- state passing,
- cycle handling,
- dependencies,
- specialist invocation.

This becomes another orchestration problem.

---

## 19. Delegation: passing control

The source describes two broad delegation styles.

### Explicit routing

The sequence is predetermined.

Example:

```text
Researcher
   ↓
Writer
```

This is appropriate when the workflow is known.

The source uses CrewAI's sequential process as an example.

### Dynamic supervision

A coordinator decides which specialist to call.

Example:

```text
HelpDeskCoordinator
     ├── Billing
     └── Support
```

The coordinator can treat agents as callable capabilities.

The source illustrates this with ADK's `AgentTool`.

Conceptually:

```text
parent agent
    ↓ calls specialist
specialist agent
    ↓ returns result
parent continues
```

This mirrors ordinary tool use, except the "tool" is another agent.

---

## 20. Information sharing between agents

Delegation is useless if the next agent lacks context.

Frameworks therefore need a way to share outputs.

### Shared state

The source uses a LangGraph example:

```python
class ResearchState(TypedDict):
    topic: str
    research_findings: str | None
    report: str | None
```

Then:

```text
Research Agent
    writes research_findings
          ↓
shared state
          ↓
Writing Agent
    reads research_findings
```

### Task context

The source also describes CrewAI's task `context` mechanism.

Conceptually:

```text
Task B declares:
"I need Task A's output"
```

The runtime then makes that information available.

### The key idea

Communication is not just:

```text
agent A calls agent B
```

It also requires:

```text
what information does B receive?
```

[[IMAGE_NEEDED: Multi-agent delegation and shared context | A Supervisor routes work to Researcher and Writer; Researcher writes findings into Shared State, Writer reads them, and the Supervisor maintains control flow | Learner should notice that delegation and information sharing are separate but complementary responsibilities]]

{{exercise:M01.L04.EX03}}

---

## 21. Instructions and prompting: the agent's charter

A powerful runtime with tools and memory still needs direction.

The prompting system defines:

- identity,
- goal,
- rules,
- boundaries,
- task framing,
- dynamic context,
- available tools.

The source calls this the agent's **charter** or **constitution**.

### The problem with one giant prompt

A monolithic prompt can become:

- brittle,
- hard to update,
- hard to debug,
- inconsistent,
- tightly coupled.

Imagine one huge string containing:

```text
persona
safety rules
user data
tools
conversation history
task
memory
formatting instructions
```

A small change can accidentally affect unrelated behavior.

A framework therefore benefits from modular prompt construction.

---

## 22. Modular and composable instructions

A structured prompting system separates concerns.

For example:

```text
Core instruction:
    "You are a customer support assistant."

Safety rule:
    "Do not give financial advice."

Dynamic state:
    user_name = ...

Current user query:
    ...

Available tools:
    ...
```

The runtime assembles these pieces into the final model context.

### Why this helps

You can change:

- persona,
- tools,
- user state,
- current task

without rewriting one giant prompt.

This improves maintainability.

---

## 23. Dynamic context injection

An agent often needs values from current state.

Example:

```text
topic = "friendship"
```

Instruction template:

```text
Write a short story about a cat, focusing on {topic}.
```

The runtime resolves the placeholder before calling the model.

The source uses ADK's `{key}` style to illustrate this concept.

The exact syntax is framework-specific.

The durable idea is:

> Prompt construction should be able to safely pull current state into the model context.

### Why not just use ad-hoc f-strings everywhere?

For very small programs, simple formatting may be fine.

But large systems benefit from standardized prompt composition because it reduces:

- inconsistent injection,
- duplicated logic,
- accidental omissions.

---

## 24. Identity, persona, and operational boundaries

Prompting is not only about tone.

It can define:

- role,
- goal,
- responsibilities,
- restrictions.

The source uses CrewAI's structured persona fields:

```text
role
goal
backstory
```

This encourages the developer to explicitly define what the agent is supposed to be.

### Example mental model

```text
Role:
    Senior Research Specialist

Goal:
    Find comprehensive information

Backstory:
    Experienced researcher
```

Whether these exact fields are used depends on the framework.

The broader principle is:

> Agent identity should be explicit and structured enough to guide consistent behavior.

---

## 25. Tool schemas are part of prompt construction

When tools are available, their schemas also become part of the model's context.

The prompting/runtime system effectively tells the model:

```text
Here are the capabilities available.
Here is what they do.
Here are their parameters.
Here is how to request them.
```

This connects prompting and tooling.

They are separate architectural components, but they cooperate closely.

The final model input may contain:

```text
core instructions
+
session context
+
retrieved memory
+
tool schemas
+
latest user message
```

That assembly process is one of the framework's most important jobs.

---

## 26. Three framework philosophies in the source

The chapter compares:

- CrewAI,
- Google ADK,
- LangGraph.

The comparison is not simply about features.

It is about **development philosophy**.

### CrewAI — high-level, declarative multi-agent orchestration

The source characterizes CrewAI as:

```text
define WHO
define WHAT
framework handles much of HOW
```

You define:

- agents,
- roles,
- tasks,
- collaboration process.

This favors abstraction and rapid setup.

### Google ADK — component-based agent SDK

The source characterizes ADK as more like traditional software engineering.

You configure:

- agent objects,
- tools,
- services,
- sessions,
- memory,
- runtime components.

The model can direct much of the loop while the SDK provides infrastructure.

### LangGraph — explicit control-flow-first orchestration

LangGraph makes control flow visible as:

- nodes,
- edges,
- state,
- conditions.

This favors fine-grained workflow control.

[[IMAGE_NEEDED: Three framework philosophies | Three side-by-side diagrams: CrewAI as roles/tasks flowing through a managed process, ADK as Agent + Tools + Services + Runner components, LangGraph as explicit nodes and edges over shared state | Learner should compare abstraction level and control style rather than treating frameworks as interchangeable]]

---

## 27. Runtime comparison

### CrewAI

The runtime is highly abstracted.

You define agents/tasks and a process such as:

```text
sequential
hierarchical
```

The framework manages much of the execution.

### Google ADK

The runtime is model-directed and component-oriented.

An agent is configured with:

- instructions,
- tools,
- services.

A Runner manages the execution cycle.

### LangGraph

The developer explicitly defines:

- nodes,
- transitions,
- conditional edges,
- loops.

This exposes control flow directly in code.

### Practical implication

Ask:

> Do I want the framework to hide the workflow, or do I want the workflow visible?

That question strongly affects framework fit.

---

## 28. Memory comparison

### CrewAI

The source describes a high-level memory experience.

Short-term context is integrated into task flow.

Long-term memory can be enabled with framework-managed persistence and retrieval.

### Google ADK

The source describes memory as pluggable infrastructure:

```text
SessionService -> short-term/session
MemoryService -> long-term
```

Long-term memory may be accessed explicitly through a memory tool.

### LangGraph

The source describes memory as part of explicit stateful graph design:

```text
State
Checkpointer
Store
```

This gives the developer direct control over state and persistence.

---

## 29. Tooling comparison

### CrewAI

Tools can be registered declaratively, often through decorators.

### Google ADK

Native Python functions can be attached to the agent's tool list.

### LangGraph

Tools are often executed inside a dedicated `ToolNode`.

The differences reflect the same broader philosophies:

```text
CrewAI -> declarative
ADK -> component-oriented
LangGraph -> explicit workflow
```

---

## 30. Multi-agent communication comparison

### CrewAI

Multi-agent collaboration is a core design focus.

Tasks and process definitions drive communication.

### Google ADK

The source emphasizes hierarchical delegation.

Sub-agents can be represented as callable capabilities.

### LangGraph

Any topology can be constructed with nodes and edges.

Examples:

- supervisor,
- pipeline,
- cycle,
- swarm-like custom graph.

This makes LangGraph flexible for unusual workflows.

---

## 31. Prompting comparison

### CrewAI

Persona is structured through fields such as:

```text
role
goal
backstory
```

### Google ADK

Agent configuration includes an instruction field with support for state injection.

### LangGraph

Prompt creation is programmatic inside graph nodes.

This offers maximum flexibility but also places more responsibility on the developer.

---

## 32. Choosing a framework style

The source recommends choosing based on the project's needs and desired abstraction.

A simple decision model:

### Prefer a high-level declarative style when:

- collaboration structure is known,
- you want fast setup,
- you prefer roles/tasks over explicit state machines.

### Prefer a component-based SDK style when:

- you want reusable services and objects,
- you prefer configuring a pre-built agent loop,
- you want a traditional software-engineering feel.

### Prefer explicit graph orchestration when:

- workflow logic is complex,
- cycles matter,
- human approval points matter,
- custom routing matters,
- you need fine-grained state transitions.

### Do not choose based only on popularity

Ask instead:

```text
How explicit must control flow be?
How much abstraction do I want?
How complex is the state?
Do I need custom loops?
How important is human-in-the-loop?
How many specialized agents are involved?
```

{{exercise:M01.L04.EX04}}

---

## 33. The framework as an assembly line

The chapter's final idea ties everything together.

On each turn, the framework may assemble:

```text
Core instructions
        +
Short-term state
        +
Relevant long-term memory
        +
Available tool schemas
        +
Latest user message
        ↓
Final context for the LLM
```

Then the LLM reasons.

The runtime interprets the result.

It may:

```text
call a tool
route to another agent
retrieve memory
ask a human
continue
stop
```

Then the cycle repeats.

### The complete picture

```text
                    ┌──────────────────┐
                    │   Instructions   │
                    └────────┬─────────┘
                             │
┌──────────────┐     ┌───────▼───────┐      ┌─────────────┐
│ Short-term   │---->│ Runtime /     │<-----│ Long-term   │
│ State        │     │ Orchestration │      │ Memory      │
└──────────────┘     └───────┬───────┘      └─────────────┘
                             │
                     ┌───────▼───────┐
                     │      LLM      │
                     └───────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐    ┌────▼────┐   ┌────▼──────┐
         │  Tools  │    │ Agents  │   │  Human    │
         └─────────┘    └─────────┘   └───────────┘
```

This is what separates a robust agent framework from a bare model call.

[[IMAGE_NEEDED: Complete agent framework assembly line | Instructions, short-term memory, long-term memory, and tool schemas feed into Runtime/Orchestration and the LLM; outputs branch to Tools, Other Agents, or Human Approval, then return to state | Learner should see how the five core components cooperate on every execution turn]]

---

## Important misconceptions

### Misconception 1

> "An agent framework is just a convenience wrapper around an LLM call."

### Why this is wrong

The source treats frameworks as infrastructure for state, execution loops, memory, tools, collaboration, lifecycle management, streaming, and observability.

---

### Misconception 2

> "State is just chat history."

### Why this is wrong

State may include messages, tool results, workflow outputs, user data, control flags, and other structured working data.

---

### Misconception 3

> "Checkpointing only means saving messages."

### Why this is wrong

Checkpointing is meant to preserve enough execution state to resume a workflow, including where execution was paused.

---

### Misconception 4

> "Asynchronous execution is only a performance optimization."

### Why this is wrong

In agent systems, async execution supports streaming, concurrency, responsiveness, and non-blocking long-running operations.

---

### Misconception 5

> "Long-term memory means sending all historical conversations to the model."

### Why this is wrong

Long-term memory is primarily a retrieval problem. Relevant memories should be selected and loaded into current context when needed.

---

### Misconception 6

> "If a function exists in Python, the model can automatically call it."

### Why this is wrong

The function must be registered and represented through a schema/tool interface the model can understand.

---

### Misconception 7

> "Structured tool calling removes all security concerns."

### Why this is wrong

Registered tools still need validation, authorization, safe execution, and sandboxing where appropriate.

---

### Misconception 8

> "Multi-agent communication is only about calling another agent."

### Why this is wrong

Useful collaboration also requires passing the right context and sharing outputs through state or task dependencies.

---

### Misconception 9

> "Prompting means writing one large system prompt."

### Why this is wrong

The chapter presents prompting as a structured system that composes identity, dynamic state, tool schemas, current task context, and rules.

---

### Misconception 10

> "One framework is universally best."

### Why this is wrong

The source frames framework selection as a trade-off between abstraction, control, workflow complexity, and developer preference.

---

## Key terminology

| Term | Meaning |
|---|---|
| Agent framework | Infrastructure that standardizes execution, state, memory, tools, collaboration, and prompting |
| Runtime | Engine that manages the agent lifecycle and execution loop |
| Orchestration | Control of workflow order, branching, state, and execution |
| Perceive–Reason–Act | Repeating agent cycle of receiving information, deciding, and acting |
| State | Structured working data available during agent execution |
| Reducer | Rule describing how new state updates merge with existing state |
| Checkpoint | Persisted snapshot used to pause and later resume execution |
| Lifecycle management | Starting, pausing, resuming, stopping, and recovering an agent process |
| Async | Non-blocking execution model useful for I/O-heavy agent operations |
| Deterministic routing | Developer-defined execution path |
| Dynamic routing | Model-influenced choice of the next agent or step |
| Concurrency | Progress on multiple operations during overlapping time |
| Parallelism | Running independent tasks simultaneously |
| Short-term memory | Current-session working context |
| Long-term memory | Persistent knowledge available across sessions |
| RAG memory | Retrieval pipeline used to find relevant stored memories |
| Embedding | Vector representation used for semantic similarity |
| Tool registration | Making a function/capability available to the framework |
| Introspection | Inspecting function metadata to generate a tool schema |
| Function calling | Structured model request to invoke a tool |
| Tool schema | Formal description of tool name, parameters, and purpose |
| Sandboxing | Isolating risky execution from the host system |
| Delegation | Passing responsibility/control from one agent to another |
| Shared state | Common data used to exchange information among workflow steps/agents |
| Prompting system | Structured mechanism for composing model instructions and context |
| Dynamic context injection | Inserting current state values into instructions |
| Persona | Structured role/identity guiding agent behavior |
| CrewAI | Framework described in the source as high-level and declarative |
| Google ADK | Framework described in the source as component-based/batteries-included |
| LangGraph | Framework described in the source as explicit control-flow-first |

---

## Self-check

Before continuing, make sure you can answer:

1. Why does a simple manual agent loop become difficult to maintain?
2. What responsibilities belong to the runtime?
3. What is the perceive–reason–act cycle?
4. Why is explicit workflow control useful for loops and branching?
5. What is the purpose of a reducer in state management?
6. What does checkpointing enable?
7. Why is human-in-the-loop difficult without lifecycle persistence?
8. Why are agent runtimes often async-native?
9. What is the difference between deterministic and dynamic routing?
10. When can parallel execution improve latency?
11. What belongs in short-term memory?
12. What problem does long-term memory solve?
13. Why is retrieval harder than simply storing memories?
14. What are the four stages of the source's long-term-memory RAG flow?
15. How do long-term memories become useful in a current session?
16. What are the three main responsibilities of a tooling interface?
17. Why is structured function calling more reliable than parsing model-generated strings?
18. Why should only registered tools be executable?
19. When is sandboxing important?
20. What is the difference between delegation and information sharing?
21. How can shared state help two agents collaborate?
22. Why is one large monolithic prompt difficult to maintain?
23. What does dynamic context injection do?
24. How are tool schemas related to prompt construction?
25. How does CrewAI's abstraction philosophy differ from LangGraph's?
26. How does ADK's component model differ from explicit graph orchestration?
27. Which framework style would you prefer for a complex approval-heavy workflow, and why?
28. What pieces does the framework assemble before each LLM call?

---

## Retain this idea

**A robust agent framework is the operating system around the model. The runtime controls the loop, state provides working context, memory supplies relevant past knowledge, tools connect reasoning to external actions, multi-agent communication enables specialization, and the prompting system assembles identity, context, and capabilities into the model's working instructions. The framework's value is not merely convenience—it turns a fragile script into a structured, resumable, observable, and extensible agent system.**
""".strip(),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-frameworks", "title": "Why Agent Frameworks Exist", "order": 1},
            {"id": "runtime", "title": "The Runtime: the Agent's Conductor", "order": 2},
            {"id": "execution-loop", "title": "The Perceive–Reason–Act Execution Loop", "order": 3},
            {"id": "state", "title": "State Management", "order": 4},
            {"id": "lifecycle", "title": "Lifecycle Management", "order": 5},
            {"id": "async", "title": "Why Agent Runtimes Are Asynchronous", "order": 6},
            {"id": "routing", "title": "Control Flow and Routing", "order": 7},
            {"id": "parallelism", "title": "Concurrency and Parallelism", "order": 8},
            {"id": "memory-overview", "title": "Memory Is a Structured System", "order": 9},
            {"id": "short-term-memory", "title": "Short-Term Memory", "order": 10},
            {"id": "long-term-memory", "title": "Long-Term Memory", "order": 11},
            {"id": "memory-synergy", "title": "How Short- and Long-Term Memory Work Together", "order": 12},
            {"id": "tooling", "title": "The Tooling Interface", "order": 13},
            {"id": "tool-definition", "title": "Tool Definition and Registration", "order": 14},
            {"id": "tool-selection", "title": "Tool Selection Through Function Calling", "order": 15},
            {"id": "secure-execution", "title": "Secure Tool Execution", "order": 16},
            {"id": "tool-framework-patterns", "title": "How Frameworks Represent Tools", "order": 17},
            {"id": "multi-agent", "title": "Multi-Agent Communication", "order": 18},
            {"id": "delegation", "title": "Delegation: Passing Control", "order": 19},
            {"id": "shared-context", "title": "Information Sharing Between Agents", "order": 20},
            {"id": "prompting", "title": "Instructions and Prompting", "order": 21},
            {"id": "modular-prompts", "title": "Modular and Composable Instructions", "order": 22},
            {"id": "dynamic-context", "title": "Dynamic Context Injection", "order": 23},
            {"id": "persona-identity", "title": "Identity, Persona, and Operational Boundaries", "order": 24},
            {"id": "tool-schema-prompt", "title": "Tool Schemas in Prompt Construction", "order": 25},
            {"id": "framework-comparison", "title": "Three Framework Philosophies", "order": 26},
            {"id": "framework-runtime", "title": "Runtime Comparison", "order": 27},
            {"id": "framework-memory", "title": "Memory Comparison", "order": 28},
            {"id": "framework-tools", "title": "Tooling Comparison", "order": 29},
            {"id": "framework-multiagent", "title": "Multi-Agent Communication Comparison", "order": 30},
            {"id": "framework-prompting", "title": "Prompting Comparison", "order": 31},
            {"id": "choosing-framework", "title": "Choosing a Framework Style", "order": 32},
            {"id": "assembly-line", "title": "The Framework as an Assembly Line", "order": 33},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",

            "title": "Design Structured Agent State",

            "lesson_code": "M01.L04",

            "section_id": "state",

            "placement": "after_section",

            "description": (
                "Practice identifying what should live in state and how updates "
                "should be merged."
            ),

            "instructions": (
                "Design state for a research agent that receives a topic, searches sources, "
                "collects notes, and writes a final report.\n"
                "1. Define at least five state fields.\n"
                "2. Mark which fields should replace old values and which should accumulate.\n"
                "3. Define one reducer-like merge rule for a list field.\n"
                "4. Explain how a bad state update could corrupt the workflow.\n"
                "5. Show one example state before and after a node update."
            ),

            "expected_output": (
                "A state schema, merge rules, and a before/after example."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "state-management",
                "reducers",
                "workflow-design",
            ],
        },

        {
            "id": "M01.L04.EX02",

            "title": "Design a Two-Layer Memory System",

            "lesson_code": "M01.L04",

            "section_id": "memory-synergy",

            "placement": "after_section",

            "description": (
                "Separate session context from persistent memory and design a retrieval flow."
            ),

            "instructions": (
                "Design memory for a learning assistant.\n"
                "1. List four facts that belong in short-term/session memory.\n"
                "2. List four facts that may belong in long-term memory.\n"
                "3. Show an Ingest -> Embed -> Store -> Search flow for one long-term fact.\n"
                "4. Explain how a retrieved memory is inserted into current working context.\n"
                "5. Explain why storing every message forever is not the same as useful memory."
            ),

            "expected_output": (
                "A two-column memory design plus one retrieval example and explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "short-term-memory",
                "long-term-memory",
                "rag",
                "retrieval",
            ],
        },

        {
            "id": "M01.L04.EX03",

            "title": "Build a Multi-Agent Research Workflow",

            "lesson_code": "M01.L04",

            "section_id": "shared-context",

            "placement": "after_section",

            "description": (
                "Practice delegation and context passing among specialist agents."
            ),

            "instructions": (
                "Design a system with Researcher, Analyst, and Writer agents.\n"
                "1. Choose deterministic or dynamic routing and justify it.\n"
                "2. Define the shared state fields.\n"
                "3. Show what the Researcher writes to state.\n"
                "4. Show what the Analyst reads and writes.\n"
                "5. Show what the Writer needs as context.\n"
                "6. Add one case where execution should return to an earlier agent."
            ),

            "expected_output": (
                "A multi-agent flow diagram and shared-state specification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "multi-agent-systems",
                "delegation",
                "shared-state",
                "routing",
            ],
        },

        {
            "id": "M01.L04.EX04",

            "title": "Choose an Agent Framework Style",

            "lesson_code": "M01.L04",

            "section_id": "choosing-framework",

            "placement": "after_section",

            "description": (
                "Use the chapter's framework philosophies to select an orchestration style."
            ),

            "instructions": (
                "For each project below, choose the framework style that best matches the "
                "source's descriptions: CrewAI-like declarative collaboration, ADK-like "
                "component SDK, or LangGraph-like explicit graph control.\n"
                "1. A fixed researcher -> writer content pipeline.\n"
                "2. A support assistant with reusable session/memory/tool services.\n"
                "3. A compliance workflow with approval pauses, retries, and cycles.\n"
                "4. Explain the key trade-off for each choice.\n"
                "5. State one reason a different framework style might still be valid."
            ),

            "expected_output": (
                "A three-row comparison table with justification and trade-offs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "framework-selection",
                "orchestration",
                "abstraction-tradeoffs",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Core Components of an Agent Framework — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",
                "section_id": "why-frameworks",
                "question": (
                    "Why does an agent framework become useful as workflows grow?"
                ),
                "options": [
                    "It replaces every LLM with hard-coded rules",
                    "It standardizes state, execution, memory, tools, and control flow",
                    "It eliminates all errors automatically",
                    "It prevents agents from using external systems",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter presents frameworks as infrastructure for the complex operational "
                    "parts of agent systems rather than as replacements for the model."
                ),
            },

            {
                "id": "M01.L04.Q02",
                "section_id": "execution-loop",
                "question": (
                    "What does the perceive–reason–act cycle represent?"
                ),
                "options": [
                    "A one-time prompt template",
                    "The repeating loop through observation, decision, and action",
                    "A database migration",
                    "A container deployment process",
                ],
                "correct": 1,
                "explanation": (
                    "Agents operate cyclically, with new observations feeding further reasoning and action."
                ),
            },

            {
                "id": "M01.L04.Q03",
                "section_id": "state",
                "question": (
                    "What is the purpose of a reducer-like state rule?"
                ),
                "options": [
                    "To define how new state updates merge with existing values",
                    "To delete all previous state",
                    "To create a new cloud account",
                    "To prevent all tool calls",
                ],
                "correct": 0,
                "explanation": (
                    "Reducers formalize update behavior such as appending messages instead of replacing them."
                ),
            },

            {
                "id": "M01.L04.Q04",
                "section_id": "lifecycle",
                "question": (
                    "Which capability most directly enables an agent to pause for human approval and continue later?"
                ),
                "options": [
                    "Image generation",
                    "Checkpointing and persisted execution state",
                    "A larger font in the UI",
                    "More tool descriptions",
                ],
                "correct": 1,
                "explanation": (
                    "Pause/resume requires saving enough state to restore the workflow at the correct point."
                ),
            },

            {
                "id": "M01.L04.Q05",
                "section_id": "async",
                "question": (
                    "Why are agent runtimes often asynchronous?"
                ),
                "options": [
                    "Because most agent operations are I/O-bound and should not block the whole system",
                    "Because async removes the need for state",
                    "Because synchronous Python cannot call functions",
                    "Because async guarantees correct answers",
                ],
                "correct": 0,
                "explanation": (
                    "Agents spend significant time waiting for models, APIs, databases, and other services."
                ),
            },

            {
                "id": "M01.L04.Q06",
                "section_id": "long-term-memory",
                "question": (
                    "What is the hardest practical problem in long-term memory according to the chapter?"
                ),
                "options": [
                    "Printing the memory",
                    "Retrieving the few relevant memories for the current task",
                    "Creating a Python list",
                    "Naming the database",
                ],
                "correct": 1,
                "explanation": (
                    "The source emphasizes that storage is easier than deciding what information should be retrieved."
                ),
            },

            {
                "id": "M01.L04.Q07",
                "section_id": "memory-synergy",
                "question": (
                    "How does long-term memory become useful during a current conversation?"
                ),
                "options": [
                    "The entire database is copied into every prompt",
                    "Relevant memories are retrieved and loaded into current working context",
                    "The model permanently changes its weights",
                    "The tool registry is deleted",
                ],
                "correct": 1,
                "explanation": (
                    "Retrieved long-term knowledge is brought into short-term context so the model can use it."
                ),
            },

            {
                "id": "M01.L04.Q08",
                "section_id": "tool-selection",
                "question": (
                    "Why is schema-based function calling more reliable than parsing ad-hoc model text?"
                ),
                "options": [
                    "It returns structured names and arguments that can be validated",
                    "It allows any unregistered command to run",
                    "It removes the need for execution code",
                    "It prevents all model mistakes",
                ],
                "correct": 0,
                "explanation": (
                    "Structured tool calls reduce fragile text parsing and support schema validation."
                ),
            },

            {
                "id": "M01.L04.Q09",
                "section_id": "secure-execution",
                "question": (
                    "Which principle is essential for secure tool execution?"
                ),
                "options": [
                    "Allow the model to invent arbitrary system commands",
                    "Only execute registered, validated capabilities",
                    "Put credentials into the prompt",
                    "Disable all schemas",
                ],
                "correct": 1,
                "explanation": (
                    "Registered tools, validation, and sandboxing form part of the framework's security boundary."
                ),
            },

            {
                "id": "M01.L04.Q10",
                "section_id": "shared-context",
                "question": (
                    "What is required in addition to delegation for successful multi-agent collaboration?"
                ),
                "options": [
                    "Information sharing between agents",
                    "A separate operating system for every agent",
                    "Removing state",
                    "Avoiding all tool calls",
                ],
                "correct": 0,
                "explanation": (
                    "Specialists need the relevant outputs/context from previous agents to do useful work."
                ),
            },

            {
                "id": "M01.L04.Q11",
                "section_id": "dynamic-context",
                "question": (
                    "What is dynamic context injection?"
                ),
                "options": [
                    "Inserting current state values into the instructions/context before the model call",
                    "Executing arbitrary operating-system commands",
                    "Deleting long-term memory",
                    "Changing the network transport",
                ],
                "correct": 0,
                "explanation": (
                    "The prompting system can resolve placeholders or state values into the final model context."
                ),
            },

            {
                "id": "M01.L04.Q12",
                "section_id": "framework-comparison",
                "question": (
                    "Which source-described philosophy best matches LangGraph?"
                ),
                "options": [
                    "High-level roles and tasks with most control hidden",
                    "Explicit state-machine-style control with nodes and edges",
                    "No state and no tools",
                    "Only fixed sequential pipelines",
                ],
                "correct": 1,
                "explanation": (
                    "The source describes LangGraph as control-flow-first with explicit nodes, edges, state, branching, and cycles."
                ),
            },

            {
                "id": "M01.L04.Q13",
                "section_id": "framework-comparison",
                "question": (
                    "Which source-described philosophy best matches CrewAI?"
                ),
                "options": [
                    "High-level declarative agents, roles, and tasks",
                    "Only low-level graph nodes",
                    "A database-only framework",
                    "A browser media library",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter presents CrewAI as a high-level declarative framework for multi-agent collaboration."
                ),
            },

            {
                "id": "M01.L04.Q14",
                "section_id": "assembly-line",
                "type": "open",
                "question": (
                    "Design an agent framework architecture for a customer support system. "
                    "Explain its runtime loop, state, checkpointing, short-term memory, long-term "
                    "memory retrieval, tool registration, specialist-agent delegation, shared context, "
                    "and how the final prompt is assembled before each model call."
                ),
            },
        ],

        "passing_score": 70,
    },
}
