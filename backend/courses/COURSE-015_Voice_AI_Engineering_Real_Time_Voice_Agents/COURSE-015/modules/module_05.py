"""M01.L05 — Designing and Building Agents with ADK.

One source chapter -> one complete learner-facing Lesson + inline Images
+ inline Exercises + lesson Quiz.

Source alignment:
- Chapter 6: Designing and Building Agents
- Early Release draft; page numbers were not provided in the supplied source.

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"

MODULE_ORDER = 1

MODULE_TITLE = "Agent Foundations & Practical Agent Development"

MODULE_DESCRIPTION = (
    "Move from agent-framework theory into practical implementation by designing "
    "an agent blueprint, building a basic agent with Google ADK, adding Python "
    "tools and multi-step execution, refactoring the agent into modular components, "
    "transforming it into a real-time Live Agent, and evaluating behavior through "
    "interactive traces and formal test cases."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Early Release draft; page numbers not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Designing and Building Agents with ADK",

    "slug": "agent-foundations-m01-l05",

    "description": (
        "Learn a complete practical workflow for agent development: design the agent "
        "before coding, configure ADK, create and run an Agent with sessions and a "
        "Runner, add custom tools, inspect the event stream, structure complex agents "
        "into reusable modules, create a Live Agent, and evaluate quality systematically."
    ),

    "order": 5,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "agent-design",
        "google-adk",
        "agent-development",
        "tools",
        "function-calling",
        "sessions",
        "runner",
        "event-streaming",
        "modular-agent-design",
        "live-agents",
        "real-time-ai",
        "adk-web",
        "agent-evaluation",
    ],

    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03", "M01.L04"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Designing and Building Agents with ADK",

        "content": r"""
# Designing and Building Agents with ADK

> **Lesson:** M01.L05  
> **Module:** Agent Foundations & Practical Agent Development  
> **Source alignment:** Chapter 6 of the supplied Early Release material.  
> This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Design an agent before implementation by defining purpose, tools, context, instructions, and example behavior.
- Explain why agent design should begin with a blueprint rather than code.
- Describe the role of Google ADK in the source chapter and distinguish framework concepts from ADK-specific APIs.
- Set up an isolated Python development environment and identify the configuration needed to connect an agent to a model provider.
- Explain the responsibilities of the ADK `Agent`, `Runner`, session service, and artifact service.
- Explain why the `Runner` returns an event stream rather than only one final string.
- Build the mental model of an ADK session and explain how reusing a session creates conversational continuity.
- Define Python functions as tools and explain why their docstrings matter.
- Trace function-call events, function-response events, and final-response events.
- Explain how an agent can chain multiple tools in one request.
- Refactor a growing agent into separate files for tools, context, examples, prompts, and assembly.
- Explain how dynamic context and examples are injected into the agent's instruction.
- Compare the manual live-streaming backend from an earlier lesson with the simplified ADK Live Agent architecture.
- Explain the roles of a live request queue, live event stream, and session state.
- Trace browser audio into a Live Agent and streamed audio/events back to the frontend.
- Explain how ADK Web helps with interactive debugging and trace inspection.
- Explain how "golden" conversations can become formal evaluation cases.
- Distinguish informal testing from repeatable evaluation.
- Identify source-specific items such as ADK versions, model names, voice names, SDK methods, and CLI commands that should be re-verified before production use.

---

## 1. From framework theory to real agent development

The previous lesson explained the anatomy of an agent framework:

```text
Runtime
Memory
Tools
Multi-agent communication
Instructions/prompting
```

Now the focus shifts from architecture to implementation.

The source chooses **Google's Agent Development Kit (ADK)** as the practical framework for this chapter.

The goal is not merely to learn one library.

The deeper learning path is:

```text
Design
   ↓
Build a minimal agent
   ↓
Add tools
   ↓
Observe the execution lifecycle
   ↓
Improve project structure
   ↓
Turn the agent into a live agent
   ↓
Debug and evaluate
```

That workflow is useful even if you later use another framework.

### Why a framework helps

Building an agent manually teaches the fundamentals.

But real projects benefit from framework support for:

- tool registration,
- session management,
- event handling,
- live streaming,
- memory integration,
- orchestration.

This lets the developer focus more on:

```text
agent purpose
behavior
capabilities
context
quality
```

rather than repeatedly rebuilding infrastructure.

---

## 2. Design the agent before writing code

The chapter makes an important software-engineering point:

> Start with a blueprint.

Before implementation, answer:

```text
What problem does the agent solve?
What can it do?
What does it need to know?
How should it behave?
What should good execution look like?
```

The source uses a Math Agent to demonstrate the process.

### The four-part blueprint

The source organizes design around four major steps:

```text
1. Define purpose and tools
2. Determine required context
3. Design core instructions
4. Provide examples of execution
```

These pieces work together.

[[IMAGE_NEEDED: Agent design blueprint | A central Math Agent connected to Purpose, Tools, Context, Core Instructions, and Execution Examples | Learner should see that agent design combines capability, knowledge, behavior, and demonstrations before coding begins]]

---

## 3. Step 1 — Define the purpose and tools

Start with the purpose.

For the Math Agent:

```text
Purpose:
Solve basic arithmetic problems for the user.
```

A narrow purpose helps decide what capabilities belong in the agent.

### From purpose to tools

Ask:

> What actions must the agent perform to achieve its goal?

For the source's Math Agent:

```text
add
subtract
multiply
divide
```

That gives us a simple design rule:

```text
goal
 ↓
required actions
 ↓
tools
```

### Why this matters

Without a clear purpose, developers often add tools because they seem interesting.

That can create:

- larger tool lists,
- harder tool selection,
- wider security surface,
- less predictable behavior.

A well-designed agent should have the capabilities it needs, not every capability available.

---

## 4. Step 2 — Determine required context

Foundation models provide broad knowledge.

An application may need specialized information that the model does not inherently know.

The source's Math Agent uses a **student profile** as context.

Possible fields include:

```text
grade level
current class
recent performance
learning goals
preferred explanation style
```

### Why context changes behavior

Imagine two students ask the same question.

Student A:

```text
Year 5
needs confidence
likes real-world examples
```

Student B:

```text
advanced high-school student
preparing for competition math
```

The mathematical result may be the same.

The explanation should not be.

### Context is not the same as instructions

Useful distinction:

```text
Context:
facts about the situation or user

Instructions:
rules for how the agent should behave
```

Example:

```text
Context:
grade_level = Year 5

Instruction:
Explain using age-appropriate language.
```

This separation becomes important later when the agent is refactored into modules.

---

## 5. Step 3 — Design the core instructions

The source calls the instructions the agent's **constitution**.

They define several things.

### Persona

For example:

```text
You are a specialized math assistant.
Be helpful and direct.
```

### Boundaries

Example:

```text
Decline non-mathematical requests.
```

Boundaries help prevent the agent from drifting beyond its intended role.

### Tool-use guidance

The source gives examples such as:

```text
"add 3 5"
"Subtract 10 from 20"
"Multiply the numbers between 1 and 10"
```

This helps communicate expected behavior.

### Response format

The Math Agent returns natural language rather than structured JSON.

For example:

```text
"The answer is 10."
```

### A useful instruction checklist

Ask:

```text
Who is the agent?
What is its goal?
What should it refuse?
When should it use tools?
How should it respond?
```

---

## 6. Step 4 — Provide examples of execution

Instructions tell the agent what you want.

Examples show it what success looks like.

The source provides an end-to-end scenario.

### Example structure

```text
Context:
Student is Year 5

User:
"multiply all the numbers between 1 and 10"

Expected behavior:
1. Recognize math task
2. Choose multiply tool
3. Construct correct argument list
4. Use tool result
5. Produce child-friendly response
```

This is much richer than an example of function syntax alone.

It demonstrates:

- task interpretation,
- tool selection,
- context use,
- tone,
- final answer style.

### "Golden path" thinking

An execution example can become a target behavior.

Later, the same idea appears in formal evaluation:

```text
ideal interaction
    ↓
saved test case
    ↓
regression evaluation
```

This is why examples are useful both for prompting and for testing.

{{exercise:M01.L05.EX01}}

---

## 7. Organizing design assets

The source suggests that larger agents may separate concerns into files such as:

```text
tools.py
context.py
prompt.py
examples.py
agent.py
```

This is a strong architectural habit.

### Why separate these components?

Because each changes for different reasons.

```text
tools.py
    changes when capabilities change

context.py
    changes when data/context strategy changes

prompt.py
    changes when instructions change

examples.py
    changes when desired behavior examples change

agent.py
    changes when assembly/configuration changes
```

This avoids one giant agent file containing everything.

---

## 8. Setting up a clean development environment

The source walks through a typical Python project setup.

### Clone the project

The source points to a companion repository.

The exact repository URL is source-specific.

### Create a virtual environment

Conceptually:

```bash
python -m venv .adk_venv
```

Then activate it.

Why use a virtual environment?

Because it isolates project dependencies from:

- system Python,
- other projects,
- incompatible package versions.

### Install the framework

The source pins a specific ADK version.

That exact version is time-sensitive.

The durable lesson is:

> Pin dependencies when reproducing a tutorial, and verify supported versions for new projects.

### Configure credentials

The source supports two model-access paths:

```text
direct API key
or
Vertex AI / Google Cloud project
```

Configuration is stored in `.env`.

This keeps runtime configuration separate from code.

### Source-specific warning

The chapter includes values such as:

- a particular ADK version,
- specific model examples,
- environment variable names.

These should be re-verified against current ADK/provider documentation before reuse.

---

## 9. Build the simplest possible agent first

The source deliberately begins with an agent that has **no custom tools**.

This is good engineering practice.

Why?

Because it lets you verify:

```text
framework installation
model connection
agent definition
session creation
runner execution
event processing
```

before adding tool complexity.

### Minimal agent configuration

Conceptually:

```python
basic_agent = Agent(
    model=MODEL,
    name="agent_basic",
    description="...",
    instruction="...",
    generate_content_config=...
)
```

The important properties are:

### `model`

The reasoning model used by the agent.

### `name`

The agent's identifier.

Useful for:

- logs,
- debugging,
- multi-agent systems.

### `description`

A concise explanation of what the agent does.

Descriptions become especially important when other agents may need to choose among specialists.

### `instruction`

The agent's core behavior rules.

### generation configuration

Controls model-generation behavior such as randomness.

The exact configuration object is framework/provider-specific.

---

## 10. Session and artifact services

Defining an `Agent` creates a blueprint.

It does not by itself manage execution state.

The source introduces two services.

### In-memory session service

Purpose:

```text
short-term/session memory
```

It can store:

- messages,
- state,
- conversation continuity.

Because it is in memory, it is suitable for learning and local development.

It is not durable across process restarts.

### In-memory artifact service

Purpose:

```text
store artifacts/files associated with the agent
```

Examples might include:

- generated files,
- images,
- text artifacts.

The source's basic example does not use artifacts heavily, but the Runner expects an artifact service to be configured.

### Why these are separate

Conversation state and file/artifact storage solve different problems.

A mature framework keeps them as distinct abstractions.

---

## 11. The Runner: bringing the agent to life

If the `Agent` is the blueprint, the `Runner` is the execution engine.

The source describes the Runner as responsible for the complete interaction lifecycle.

Conceptually:

```text
user message
    ↓
Runner
    ↓
load session state
    ↓
assemble agent context
    ↓
call model
    ↓
execute tools if needed
    ↓
update session
    ↓
emit events
```

The Runner connects the theoretical runtime from the previous chapter to actual code.

### Why this abstraction matters

Without a Runner-like component, you would manually implement:

- prompt assembly,
- state loading,
- tool dispatch,
- state updates,
- model calls,
- event streaming.

The framework centralizes these responsibilities.

[[IMAGE_NEEDED: ADK basic execution architecture | User Query -> Session Service + Agent Blueprint -> Runner -> Foundation Model -> Event Stream -> Final Response, with Artifact Service alongside Runner | Learner should understand that Agent defines behavior while Runner executes it using services]]

---

## 12. Creating and reusing sessions

The source creates a session before running the agent.

Conceptually:

```python
session = await session_service.create_session(
    app_name=...,
    user_id=...,
    session_id=...
)
```

Then the Runner executes against that session.

### Important memory behavior

The source notes an important implementation detail:

> If a new session is created for every query, the agent will not remember previous turns.

That gives us a simple rule:

```text
new session each query
    -> isolated interactions

reuse same session
    -> conversational continuity
```

### Session identity matters

Common identifiers include:

```text
app_name
user_id
session_id
```

These help the framework know:

- which application,
- which user,
- which conversation

the state belongs to.

---

## 13. Agent execution produces an event stream

A key idea in the source is that the Runner does not necessarily return one final string.

It returns a **stream of events**.

For the basic agent, you may only care about the final-response event.

Conceptually:

```python
events = runner.run_async(...)

async for event in events:
    if event.is_final_response():
        ...
```

### Why events?

Because once tools are added, execution has intermediate steps.

The runtime may emit:

```text
function call
function result
agent message
control event
final response
```

An event stream makes the agent's execution observable.

This is much more useful than a black-box function returning one string.

---

## 14. Add tools only after the basic loop works

Once the minimal agent works, the source adds arithmetic tools.

The tools are ordinary Python functions.

For example:

```python
def add(numbers: list[int]) -> int:
    return sum(numbers)
```

But the source emphasizes something important:

> The docstring is critical.

Why?

Because the framework can inspect the function to understand how it should be presented to the model.

---

## 15. Tool docstrings are part of the tool interface

A useful docstring can include:

```text
what the function does
arguments
return value
examples
```

Example structure:

```python
def add(numbers: list[int]) -> int:
    # Tool documentation / docstring should explain:
    # - what the function does
    # - the `numbers` argument
    # - the returned value
    # - useful examples such as add([1, 2, 3]) -> 6
    return sum(numbers)
```

The framework can use:

- function name,
- type hints,
- docstring

to build a formal function declaration/schema.

### Why tool documentation affects behavior

Poor documentation:

```python
def do_it(x):
    # Poor documentation: "Does thing."
    ...
```

gives the model very little guidance.

Better documentation improves:

- tool selection,
- argument construction,
- predictability.

This reinforces a broader lesson:

> In agent systems, developer-facing documentation can become model-facing interface design.

---

## 16. Registering tools with the agent

The source passes Python function objects directly into the agent.

Conceptually:

```python
agent_math = Agent(
    ...,
    tools=[add, subtract, multiply, divide],
)
```

The framework handles the bridge between:

```text
Python functions
       ↓
function declarations
       ↓
model tool selection
       ↓
runtime execution
```

This is a major simplification compared with manual tool schemas and dispatch code.

---

## 17. Tool-equipped agents produce richer events

Once tools are enabled, the event stream becomes more informative.

The source highlights three event categories:

### Function call

The model requests a tool.

Contains information such as:

```text
function name
arguments
```

### Function response

The tool has executed.

Contains:

```text
function name
result
```

### Final response

The agent has enough information and returns natural language.

### Why inspect all three?

Because debugging an agent requires understanding:

```text
what did the model choose?
with what arguments?
what did the tool return?
how did the final answer use the result?
```

Without this visibility, tool failures can look like model failures.

---

## 18. Chaining multiple tools in one request

The source uses this request:

```text
First multiply numbers 1 to 3 and then add 4.
```

A correct execution is:

```text
multiply([1, 2, 3])
    ↓
6
    ↓
add([6, 4])
    ↓
10
    ↓
final response
```

This is an important milestone.

The agent is not merely selecting one tool.

It is using the output of one tool as input to another.

### Execution trace

```text
User request
    ↓
Function Call: multiply
    ↓
Function Response: 6
    ↓
Function Call: add
    ↓
Function Response: 10
    ↓
Final Response: 10
```

This illustrates why event-based execution is so useful.

[[IMAGE_NEEDED: Chained tool execution | User request -> multiply tool call -> result 6 -> add tool call with [6,4] -> result 10 -> final answer | Learner should notice that the runtime feeds one tool result back into reasoning before the next tool is selected]]

{{exercise:M01.L05.EX02}}

---

## 19. Refactor before the agent becomes difficult to maintain

The source then improves the project structure before building the Live Agent.

This is a valuable engineering habit.

Do not wait until the system becomes unmanageable.

### Source structure

```text
agent_math/
├── tools.py
├── context.py
├── examples.py
├── prompt.py
└── agent.py
```

Each file has one main responsibility.

---

## 20. `tools.py` — the agent's skills

Move executable capabilities into:

```text
tools.py
```

This keeps the tool implementation independent from:

- prompt text,
- user context,
- agent assembly.

The source keeps the tool docstrings intact because they remain part of the model-facing interface.

---

## 21. `context.py` — specialized and dynamic knowledge

The source creates a structured student profile.

It includes fields such as:

```text
name
age
grade level
learning goals
tone preferences
explanation style
```

### Why structured context is powerful

The agent can adapt:

- vocabulary,
- examples,
- difficulty,
- tone,
- encouragement.

### Why Python instead of only static JSON?

The source makes an important architectural observation.

A Python context module can later do something dynamic:

```python
def load_student_profile(user_id):
    return database.get_profile(user_id)
```

So a static example can evolve into runtime retrieval.

This gives a general design principle:

> Use a representation that can grow with the application.

---

## 22. `examples.py` — the golden path

The source separates ideal interaction examples into their own module.

These examples demonstrate:

- tone,
- pacing,
- teaching style,
- context usage,
- interaction flow.

The example is not merely:

```text
input -> answer
```

It demonstrates how the agent should teach.

For a student, that can include:

```text
encouragement
analogy
step-by-step guidance
question back to learner
```

This is a richer form of behavioral specification.

---

## 23. `prompt.py` — the agent's constitution

The instruction template brings other components together.

Conceptually:

```text
You are a specialized math agent.

Critical rule:
Use tools to derive answers.

Target audience:
{student_profile}

Reference examples:
{examples}
```

The placeholders connect prompt design to runtime state/context.

### Dynamic fields

The source highlights:

```text
{student_profile}
{examples}
```

These are injected into the instruction before or during agent execution according to the framework's context mechanism.

This creates:

```text
static behavior rules
+
dynamic user context
+
behavior examples
```

inside one coherent instruction.

---

## 24. `agent.py` — clean assembly point

The assembly file imports:

```text
tools
prompt
context
examples
```

Then constructs the agent.

Conceptually:

```python
def create_math_agent(model):
    context["examples"] = examples

    agent = Agent(
        model=model,
        instruction=instruction_prompt,
        tools=[...]
    )

    return agent, context
```

This creates a clean boundary between:

```text
definition of pieces
```

and:

```text
assembly of system
```

[[IMAGE_NEEDED: Modular agent project structure | Separate boxes for tools.py, context.py, examples.py, and prompt.py all feeding into agent.py, which produces the Agent and session context | Learner should see how modularization improves maintainability and allows each concern to evolve independently]]

{{exercise:M01.L05.EX03}}

---

## 25. From manual live streaming to framework-managed Live Agents

Earlier in the course, the live architecture required the application to manually manage:

```text
Browser
  ⇅ WebSocket
Backend
  ⇅ WebSocket
Live model API
```

The backend was responsible for:

- the second WebSocket,
- media forwarding,
- provider session handling,
- event translation.

That architecture worked.

But integrating:

- tools,
- memory,
- context,
- agent state

required additional custom work.

### ADK Live Agent simplification

The source shows a new architecture where the ADK Runner handles the low-level live-model connection.

Conceptually:

```text
Browser
  ⇅ WebSocket
Backend
  ↓
ADK Live Runner
  ↓
Agent + Tools + Session State
  ↓
Live Model
```

The application still needs a frontend-to-backend connection.

But the framework abstracts much of the provider-side live session.

### Why this matters

The backend can focus more on:

- application protocol,
- agent configuration,
- session state,
- user experience,

instead of low-level provider streaming mechanics.

[[IMAGE_NEEDED: Manual live architecture vs ADK Live Agent | Left: Browser <-> Backend <-> Live API with two manually managed WebSockets; Right: Browser <-> Backend -> ADK Runner -> Agent/Live Model, with Runner abstracting provider streaming | Learner should notice which low-level responsibilities move from application code into the framework]]

---

## 26. New components in the Live Agent architecture

The source introduces two important live components.

### Live Request Queue

Purpose:

```text
buffer incoming live user media/events
```

The browser sends audio.

The backend places audio blobs into this queue.

The ADK live runtime consumes them.

### Live Event Stream

Purpose:

```text
emit agent output and control events
```

Events may contain:

- audio,
- interruption,
- turn complete,
- other agent/runtime signals.

This gives us a clean model:

```text
frontend input
    ↓
Live Request Queue
    ↓
Live Agent Runtime
    ↓
Live Events
    ↓
frontend output
```

---

## 27. Starting a live agent session

The source's live-session setup performs several jobs.

Conceptually:

```text
1. Configure response modality
2. Configure speech/voice
3. Create live-capable Runner
4. Create session with state/context
5. Create Live Request Queue
6. Start live execution
7. Receive live event stream
```

The source uses specific ADK classes, voice names, language codes, and run configuration.

Those exact names are implementation-specific.

### The crucial concept: session state

The source emphasizes:

```python
state=context
```

when the session is created.

This is how the student profile and examples become part of the session's working state.

The state can then support:

- prompt injection,
- tool behavior,
- personalization.

The same runtime-state concepts from Chapter 5 now appear in practical code.

---

## 28. Browser audio to the Live Agent

The frontend still sends audio chunks to the backend.

The backend performs steps similar to the earlier voice application:

```text
receive JSON
    ↓
find audio chunk
    ↓
Base64 decode
    ↓
construct PCM audio blob
    ↓
send to Live Request Queue
```

The difference is what happens next.

Earlier:

```text
backend manually sent audio to provider session
```

Now:

```text
backend gives audio to ADK live runtime
```

That abstraction is the main benefit.

---

## 29. Live Agent events back to the browser

The source's response handler listens to the live event stream.

Important event categories include:

### Interruption

The user begins speaking while the agent is responding.

The backend forwards an interruption signal.

The frontend should stop stale audio playback.

### Turn complete

The agent finishes the current conversational turn.

The frontend may update UI state.

### Audio content

The agent emits PCM audio data.

The backend Base64-encodes it and sends it to the browser.

### Event-driven mental model

```text
live event
   ├── interruption -> stop playback
   ├── turn complete -> update state
   └── audio -> play audio
```

This event protocol keeps UI behavior aligned with agent/runtime state.

---

## 30. Running and testing the Live Agent

The source uses separate backend and frontend servers during local development.

Conceptually:

```text
Backend:
localhost:8081

Frontend:
localhost:8000
```

The browser opens the frontend and starts a session.

The user can then speak with the Math Agent.

### Important source-specific note

The chapter states that live streaming is only available for compatible model versions.

That is exactly the kind of implementation detail that must be checked against current provider/framework documentation.

Do not treat a model example from an Early Release chapter as permanent.

---

## 31. Interactive debugging with ADK Web

As agents become more complex, terminal logs become difficult to inspect.

The source introduces **ADK Web** as a visual development interface.

It can provide:

- agent selection,
- sessions,
- chat,
- event trace,
- state inspection,
- tool-call details.

### Why visual traces matter

Suppose the final answer is wrong.

Possible causes include:

```text
wrong tool chosen
wrong argument
tool returned bad data
state missing
prompt issue
final synthesis issue
```

A trace helps locate the failure.

### Tool-call inspection

The source describes clicking a tool event to inspect:

```text
which function
which arguments
raw event data
```

This is much better than guessing from the final response.

[[IMAGE_NEEDED: Agent debugging cockpit | A conceptual UI with chat on the right and a trace/state/events panel on the left, highlighting a tool-call event with function name and arguments | Learner should see how observability exposes intermediate execution rather than only the final answer]]

---

## 32. Quick live experimentation vs production live architecture

The source notes that ADK Web can quickly turn an agent into a voice-interactive experiment through the UI.

That is useful for:

- development,
- demonstrations,
- rapid testing.

But the source distinguishes this from a production-ready live application.

A real product still needs:

- dedicated frontend,
- backend integration,
- user controls,
- authentication,
- deployment,
- reliability,
- security.

This is an important engineering distinction:

```text
developer tool
≠
production user experience
```

---

## 33. From manual testing to formal evaluation

Talking to an agent manually is useful.

But it does not tell you whether behavior is consistently correct.

Formal evaluation introduces repeatability.

### Evaluation dataset

The source describes test cases containing:

```text
sample user query
expected or "golden" response
```

Potentially also expected tool behavior.

### Golden conversation

A successful interaction can be saved as a test case.

This creates a powerful workflow:

```text
find a good interaction
    ↓
save it
    ↓
rerun it later
    ↓
detect regression
```

### Why this matters

You may change:

- prompts,
- model,
- tools,
- context,
- framework version.

Without tests, you may not notice that an old behavior broke.

Evaluation converts quality from:

```text
"seems okay"
```

into:

```text
repeatable test evidence
```

---

## 34. What should agent evaluation measure?

The source mentions evaluation dimensions such as:

- tool trajectory,
- response matching.

The exact UI/metric names are implementation-specific.

But the broader idea is very important.

### Tool trajectory

Did the agent take the right sequence of actions?

Example expected path:

```text
multiply
then add
```

Wrong trajectory:

```text
add
then multiply
```

Even if a lucky final answer appears correct in one case, the execution logic may be wrong.

### Final response quality

Did the final answer match expected behavior?

This can include:

- correctness,
- style,
- required content,
- format.

### Why both matter

An agent is not only its final sentence.

It is:

```text
decision process
+
tool use
+
state changes
+
final output
```

So agent evaluation should inspect both behavior and outcome.

---

## 35. A practical quality-improvement loop

A useful workflow is:

```text
1. Build
2. Interact manually
3. Inspect traces
4. Find a high-quality interaction
5. Save as golden case
6. Build evaluation dataset
7. Run evaluation after changes
8. Investigate failures
9. Improve agent
10. Repeat
```

This turns debugging into an engineering process.

### Small tests vs production-scale evaluation

The source notes that production systems may eventually require:

```text
hundreds
or
thousands
```

of evaluation records.

The lesson here focuses on the basic workflow, not large-scale evaluation infrastructure.

{{exercise:M01.L05.EX04}}

---

## 36. The complete agent development cycle

We can now connect the entire chapter.

### Design

```text
Purpose
Tools
Context
Instructions
Examples
```

### Implement

```text
Agent
Session Service
Artifact Service
Runner
```

### Add action

```text
Python tools
Docstrings
Tool registration
Function-call events
```

### Handle complexity

```text
Multi-step tool chaining
Structured event stream
Session continuity
```

### Refactor

```text
tools.py
context.py
examples.py
prompt.py
agent.py
```

### Go live

```text
Live Request Queue
Live Runner
Live Events
Audio frontend/backend
```

### Improve quality

```text
ADK Web
Trace inspection
Golden cases
Evaluation dataset
Pass/fail metrics
```

[[IMAGE_NEEDED: End-to-end agent development lifecycle | A circular or staged diagram: Design Blueprint -> Basic Agent -> Tools -> Modular Refactor -> Live Agent -> Debug/Trace -> Formal Evaluation -> Improve -> back to Design | Learner should notice that agent development is iterative, not a one-time coding task]]

---

## 37. Important source-specific and production boundaries

The chapter is an Early Release hands-on tutorial.

Several details should be treated as version-specific.

Verify current documentation for:

- ADK package version,
- supported Python versions,
- `Agent` constructor fields,
- Runner APIs,
- session-service APIs,
- artifact-service APIs,
- Live Agent classes,
- live queue methods,
- event properties,
- supported models,
- supported live-streaming models,
- voice names,
- language codes,
- environment variables,
- ADK Web CLI commands,
- evaluation UI and metric names.

### Do not confuse library syntax with architecture

For example, these concepts are durable:

```text
Agent blueprint
Runner/runtime
Session state
Tool registration
Event stream
Live input queue
Evaluation dataset
```

But these may change:

```text
specific class names
specific method signatures
specific model IDs
specific CLI syntax
```

### Tool safety

The Math Agent uses low-risk arithmetic tools.

Real tools may have side effects.

For production tools, add:

- schema validation,
- authorization,
- timeouts,
- retries,
- logging,
- confirmation where appropriate.

### Session persistence

In-memory sessions are convenient for learning.

Production systems may need durable storage.

Ask:

```text
What happens if the process restarts?
What happens if the user reconnects?
How long should state persist?
```

### Evaluation discipline

Do not wait until production to build tests.

Turn important behaviors into repeatable evaluation cases early.

---

## Important misconceptions

### Misconception 1

> "Agent development should start by writing tool code."

### Why this is wrong

The chapter starts with design: purpose, tools, context, instructions, and examples.

---

### Misconception 2

> "The Agent object is the entire running system."

### Why this is wrong

The Agent defines identity/behavior, while the Runner and services manage execution, sessions, and events.

---

### Misconception 3

> "Creating a new session for every message still preserves conversation memory."

### Why this is wrong

A new session isolates the message from earlier session state. Reuse the same session for continuity.

---

### Misconception 4

> "Tool docstrings are only for human developers."

### Why this is wrong

In the source architecture, the framework can use function metadata and docstrings to build the model-facing function declaration.

---

### Misconception 5

> "A tool-equipped agent returns only one final response."

### Why this is wrong

The Runner can emit intermediate function-call and function-response events before the final answer.

---

### Misconception 6

> "Multi-step tool use means the framework pre-programs the exact sequence."

### Why this is wrong

The agent can use the result of one tool call to decide the next action dynamically.

---

### Misconception 7

> "Putting prompts, tools, examples, and context in one file is always simpler."

### Why this is wrong

As agents grow, separating concerns improves maintainability, testing, and dynamic behavior.

---

### Misconception 8

> "Live Agent support only changes the frontend."

### Why this is wrong

The key architectural change is that the framework/runtime can abstract much of the provider-side live streaming and integrate it with agent state and tools.

---

### Misconception 9

> "Interactive chat testing is enough to validate an agent."

### Why this is wrong

Manual testing is valuable, but repeatable evaluation datasets are needed to detect regressions systematically.

---

### Misconception 10

> "If the final answer is correct, the agent's execution path does not matter."

### Why this is wrong

Tool trajectory matters for reliability. A correct result reached through an unsafe or logically incorrect path may fail on future cases.

---

## Key terminology

| Term | Meaning |
|---|---|
| Agent blueprint | Pre-code design describing purpose, tools, context, instructions, and examples |
| Purpose | The problem the agent is intended to solve |
| Context | Specialized information supplied to help the agent adapt to the current user/task |
| Core instruction | Persistent behavioral rules and persona guidance |
| Execution example | End-to-end demonstration of desired agent behavior |
| ADK | Agent Development Kit used as the practical framework in the source chapter |
| Agent | Framework object defining the agent's identity, instructions, model, and tools |
| Session Service | Service managing per-session state and short-term memory |
| Artifact Service | Service for storing files/artifacts associated with execution |
| Runner | Runtime engine that executes the agent and coordinates sessions/tools/events |
| Session | A stateful interaction scope identified by application/user/session identifiers |
| Event Stream | Sequence of runtime events emitted during agent execution |
| Function Call Event | Event indicating that the model requested a tool |
| Function Response Event | Event containing the result of executed tool code |
| Final Response Event | Event containing the completed natural-language answer |
| Tool docstring | Documentation used by the framework as part of the tool's model-facing description |
| Tool chaining | Using multiple tools in sequence where earlier outputs affect later calls |
| Modular agent structure | Separation of tools, context, examples, prompt, and assembly into dedicated modules |
| Golden path | Example interaction demonstrating ideal behavior |
| Live Request Queue | Queue receiving live input for framework-managed real-time execution |
| Live Event Stream | Stream of real-time agent output/control events |
| Interruption event | Signal indicating user input interrupted agent output |
| Turn complete | Signal indicating the current conversational response is complete |
| ADK Web | Visual development/debugging interface described by the source |
| Golden test case | Saved ideal interaction used as an evaluation example |
| Tool trajectory | Sequence of tool actions taken by the agent |
| Regression | Previously correct behavior becoming worse after a change |

---

## Self-check

Before continuing, make sure you can answer:

1. Why should agent design start before coding?
2. What are the four major blueprint steps used in the chapter?
3. How do purpose and tools relate?
4. What is the difference between context and instructions?
5. Why are end-to-end examples more useful than only function syntax examples?
6. Why might a larger agent separate `tools.py`, `context.py`, `prompt.py`, and `examples.py`?
7. What does the ADK `Agent` object define?
8. What does the Runner do?
9. What is the purpose of the session service?
10. What is the purpose of the artifact service?
11. Why does session reuse matter for conversational memory?
12. Why does the Runner return events?
13. What does a function-call event contain?
14. What does a function-response event contain?
15. Why does a tool's docstring matter?
16. How does tool chaining work in the multiply-then-add example?
17. What belongs in `context.py`?
18. What is the "golden path" role of `examples.py`?
19. Why are prompt placeholders useful?
20. What does `agent.py` do in the modular design?
21. How does the ADK Live Agent architecture simplify the earlier two-WebSocket backend?
22. What does the Live Request Queue do?
23. Why is session `state` important in the live agent?
24. What kinds of events flow back from the Live Agent?
25. Why is ADK Web useful for debugging?
26. What is the difference between manual interaction and formal evaluation?
27. What is a golden evaluation case?
28. Why should tool trajectory be evaluated separately from final response quality?
29. Which chapter details are durable architecture and which are version-specific API details?
30. What would you change when moving from an in-memory prototype to a production system?

---

## Retain this idea

**Building a strong agent is an iterative engineering process: design the purpose, capabilities, context, and behavior first; implement the smallest working agent; add tools and observe the event stream; refactor the agent into modular components as complexity grows; use the framework's runtime to support live interaction and session state; and turn successful interactions into repeatable evaluations so quality can improve without regressions.**
""".strip(),

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "chapter-goal", "title": "From Framework Theory to Real Agent Development", "order": 1},
            {"id": "design-before-code", "title": "Design the Agent Before Writing Code", "order": 2},
            {"id": "purpose-tools", "title": "Define the Purpose and Tools", "order": 3},
            {"id": "required-context", "title": "Determine Required Context", "order": 4},
            {"id": "core-instructions", "title": "Design the Core Instructions", "order": 5},
            {"id": "execution-examples", "title": "Provide Examples of Execution", "order": 6},
            {"id": "project-structure", "title": "Organizing Design Assets", "order": 7},
            {"id": "environment", "title": "Setting Up a Clean Development Environment", "order": 8},
            {"id": "basic-agent", "title": "Build the Simplest Possible Agent First", "order": 9},
            {"id": "services", "title": "Session and Artifact Services", "order": 10},
            {"id": "runner", "title": "The Runner: Bringing the Agent to Life", "order": 11},
            {"id": "session-lifecycle", "title": "Creating and Reusing Sessions", "order": 12},
            {"id": "events", "title": "Agent Execution Produces an Event Stream", "order": 13},
            {"id": "adding-tools", "title": "Add Tools After the Basic Loop Works", "order": 14},
            {"id": "docstrings", "title": "Tool Docstrings Are Part of the Tool Interface", "order": 15},
            {"id": "register-tools", "title": "Registering Tools with the Agent", "order": 16},
            {"id": "tool-events", "title": "Tool-Equipped Agents Produce Richer Events", "order": 17},
            {"id": "chained-tools", "title": "Chaining Multiple Tools in One Request", "order": 18},
            {"id": "refactor", "title": "Refactor Before the Agent Becomes Difficult to Maintain", "order": 19},
            {"id": "tools-file", "title": "tools.py — the Agent's Skills", "order": 20},
            {"id": "context-file", "title": "context.py — Specialized and Dynamic Knowledge", "order": 21},
            {"id": "examples-file", "title": "examples.py — the Golden Path", "order": 22},
            {"id": "prompt-file", "title": "prompt.py — the Agent's Constitution", "order": 23},
            {"id": "agent-file", "title": "agent.py — Clean Assembly Point", "order": 24},
            {"id": "manual-vs-live", "title": "From Manual Live Streaming to Framework-Managed Live Agents", "order": 25},
            {"id": "live-components", "title": "New Components in the Live Agent Architecture", "order": 26},
            {"id": "start-live-session", "title": "Starting a Live Agent Session", "order": 27},
            {"id": "frontend-to-agent", "title": "Browser Audio to the Live Agent", "order": 28},
            {"id": "agent-to-frontend", "title": "Live Agent Events Back to the Browser", "order": 29},
            {"id": "running-live", "title": "Running and Testing the Live Agent", "order": 30},
            {"id": "debugging", "title": "Interactive Debugging with ADK Web", "order": 31},
            {"id": "quick-live-testing", "title": "Quick Live Experimentation vs Production Live Architecture", "order": 32},
            {"id": "formal-evaluation", "title": "From Manual Testing to Formal Evaluation", "order": 33},
            {"id": "evaluation-metrics", "title": "What Should Agent Evaluation Measure?", "order": 34},
            {"id": "evaluation-workflow", "title": "A Practical Quality-Improvement Loop", "order": 35},
            {"id": "full-development-cycle", "title": "The Complete Agent Development Cycle", "order": 36},
            {"id": "production-boundaries", "title": "Important Source-Specific and Production Boundaries", "order": 37},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L05.EX01",

            "title": "Create an Agent Blueprint",

            "lesson_code": "M01.L05",

            "section_id": "execution-examples",

            "placement": "after_section",

            "description": (
                "Design an agent completely before implementing it."
            ),

            "instructions": (
                "Design a Study Planning Agent.\n"
                "1. Define its single primary purpose.\n"
                "2. List three tools it needs.\n"
                "3. Define five pieces of user/task context it may need.\n"
                "4. Write a concise persona and two boundaries.\n"
                "5. Define its response style.\n"
                "6. Write one end-to-end golden example showing context, user request, tool use, and ideal final response."
            ),

            "expected_output": (
                "A structured agent blueprint containing purpose, tools, context, "
                "instructions, boundaries, response style, and one execution example."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-design",
                "tool-planning",
                "context-design",
                "prompting",
            ],
        },

        {
            "id": "M01.L05.EX02",

            "title": "Trace a Multi-Step Tool Event Stream",

            "lesson_code": "M01.L05",

            "section_id": "chained-tools",

            "placement": "after_section",

            "description": (
                "Practice reasoning about the sequence of function calls, responses, and final output."
            ),

            "instructions": (
                "For the request 'Add 5 and 7, then multiply the result by 3':\n"
                "1. Write the first function call event.\n"
                "2. Write the first function response event.\n"
                "3. Write the second function call event using the previous result.\n"
                "4. Write the second function response event.\n"
                "5. Write the final response event.\n"
                "6. Explain why the Runner needs the intermediate events rather than only the final answer."
            ),

            "expected_output": (
                "A five-step event trace plus a short explanation of event-stream observability."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tool-chaining",
                "event-streams",
                "function-calling",
            ],
        },

        {
            "id": "M01.L05.EX03",

            "title": "Refactor a Monolithic Agent",

            "lesson_code": "M01.L05",

            "section_id": "agent-file",

            "placement": "after_section",

            "description": (
                "Apply the chapter's modular design pattern to a growing agent."
            ),

            "instructions": (
                "You have one 500-line Python file containing tools, prompt text, user profile data, "
                "few-shot examples, and agent creation code.\n"
                "1. Split it into tools.py, context.py, examples.py, prompt.py, and agent.py.\n"
                "2. State exactly what belongs in each file.\n"
                "3. Define two dynamic placeholders the prompt should receive.\n"
                "4. Explain one reason context.py may eventually contain functions rather than only static data.\n"
                "5. Draw the dependency flow into agent.py."
            ),

            "expected_output": (
                "A module plan and dependency diagram showing how the agent is assembled."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "modular-design",
                "separation-of-concerns",
                "agent-architecture",
            ],
        },

        {
            "id": "M01.L05.EX04",

            "title": "Build an Agent Evaluation Plan",

            "lesson_code": "M01.L05",

            "section_id": "evaluation-workflow",

            "placement": "after_section",

            "description": (
                "Turn informal successful interactions into a repeatable quality test suite."
            ),

            "instructions": (
                "Design an evaluation plan for the Math Agent.\n"
                "1. Create five test cases: direct answer, one tool, chained tools, invalid/non-math request, and context-aware explanation.\n"
                "2. For each case, define the expected final behavior.\n"
                "3. For tool cases, define the expected tool trajectory.\n"
                "4. State which failures should be considered regressions.\n"
                "5. Explain how a successful manual session can become a golden evaluation case."
            ),

            "expected_output": (
                "A five-case evaluation table covering inputs, expected behavior, expected tool path, and regression criteria."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-evaluation",
                "golden-tests",
                "tool-trajectory",
                "regression-testing",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L05.QZ01",

        "title": "Designing and Building Agents — Knowledge Check",

        "lesson_code": "M01.L05",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",
                "section_id": "design-before-code",
                "question": (
                    "What should happen before writing the implementation code for an agent?"
                ),
                "options": [
                    "Define purpose, tools, context, instructions, and desired examples",
                    "Add every available tool immediately",
                    "Deploy to production",
                    "Create a new model from scratch",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter begins with a design blueprint so capabilities and behavior are clear before implementation."
                ),
            },

            {
                "id": "M01.L05.Q02",
                "section_id": "required-context",
                "question": (
                    "What is the role of user context such as grade level in the Math Agent?"
                ),
                "options": [
                    "It lets the agent adapt its explanation to the learner",
                    "It replaces arithmetic tools",
                    "It automatically stores files",
                    "It creates the Python environment",
                ],
                "correct": 0,
                "explanation": (
                    "Dynamic context allows the same agent to personalize difficulty, tone, and examples."
                ),
            },

            {
                "id": "M01.L05.Q03",
                "section_id": "runner",
                "question": (
                    "Which component acts as the execution engine around the Agent in the source?"
                ),
                "options": [
                    "Runner",
                    "README",
                    "Canvas",
                    "Dockerfile",
                ],
                "correct": 0,
                "explanation": (
                    "The Runner manages execution, sessions, tool interactions, and event processing."
                ),
            },

            {
                "id": "M01.L05.Q04",
                "section_id": "session-lifecycle",
                "question": (
                    "What is the result of creating a brand-new session for every user query?"
                ),
                "options": [
                    "Previous conversational state is not reused",
                    "The model becomes permanently retrained",
                    "Tool schemas disappear",
                    "The frontend stops working",
                ],
                "correct": 0,
                "explanation": (
                    "Session continuity requires reusing the same session rather than creating an isolated one per turn."
                ),
            },

            {
                "id": "M01.L05.Q05",
                "section_id": "docstrings",
                "question": (
                    "Why are tool docstrings important in the source's ADK example?"
                ),
                "options": [
                    "They help the framework generate a useful model-facing function declaration",
                    "They encrypt the API key",
                    "They replace all runtime code",
                    "They automatically deploy the tool",
                ],
                "correct": 0,
                "explanation": (
                    "The framework can use names, type hints, and docstrings to describe the tool to the model."
                ),
            },

            {
                "id": "M01.L05.Q06",
                "section_id": "tool-events",
                "question": (
                    "Which event occurs after the runtime executes a tool?"
                ),
                "options": [
                    "Function response event",
                    "Repository clone event",
                    "Environment activation event",
                    "Camera permission event",
                ],
                "correct": 0,
                "explanation": (
                    "The function-response event contains the result produced by the executed tool."
                ),
            },

            {
                "id": "M01.L05.Q07",
                "section_id": "chained-tools",
                "question": (
                    "Why is the multiply-then-add example significant?"
                ),
                "options": [
                    "It demonstrates that one tool result can influence the next tool call",
                    "It shows that tools cannot be chained",
                    "It removes the need for a Runner",
                    "It creates long-term memory automatically",
                ],
                "correct": 0,
                "explanation": (
                    "The runtime feeds the first result back into the agent so the next action can use it."
                ),
            },

            {
                "id": "M01.L05.Q08",
                "section_id": "context-file",
                "question": (
                    "Why might context.py eventually contain functions rather than only a static dictionary?"
                ),
                "options": [
                    "To dynamically retrieve current user data from databases or services",
                    "To avoid using any context",
                    "To replace tools.py",
                    "To make Python synchronous",
                ],
                "correct": 0,
                "explanation": (
                    "Programmatic context can fetch live, user-specific information at runtime."
                ),
            },

            {
                "id": "M01.L05.Q09",
                "section_id": "manual-vs-live",
                "question": (
                    "What does the Live Agent framework primarily simplify compared with the earlier manual architecture?"
                ),
                "options": [
                    "It abstracts much of the provider-side live streaming/session plumbing",
                    "It removes the need for a browser entirely",
                    "It eliminates sessions",
                    "It prevents all tool use",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes that the Runner handles the lower-level live-model connection while integrating agent features."
                ),
            },

            {
                "id": "M01.L05.Q10",
                "section_id": "live-components",
                "question": (
                    "What is the role of the Live Request Queue?"
                ),
                "options": [
                    "Buffer incoming live input for the framework's live runtime",
                    "Store long-term vector memories",
                    "Compile CSS",
                    "Create cloud containers",
                ],
                "correct": 0,
                "explanation": (
                    "The backend places incoming live media into the queue for the runtime to consume."
                ),
            },

            {
                "id": "M01.L05.Q11",
                "section_id": "debugging",
                "question": (
                    "Why is a visual event trace useful when debugging an agent?"
                ),
                "options": [
                    "It reveals intermediate decisions such as tool calls and arguments",
                    "It guarantees the model is correct",
                    "It removes the need for tests",
                    "It automatically changes the prompt",
                ],
                "correct": 0,
                "explanation": (
                    "Intermediate traces help identify whether failures came from tool choice, arguments, results, state, or final synthesis."
                ),
            },

            {
                "id": "M01.L05.Q12",
                "section_id": "formal-evaluation",
                "question": (
                    "What is the main advantage of saving successful interactions as golden evaluation cases?"
                ),
                "options": [
                    "They can be rerun later to detect regressions",
                    "They permanently retrain the model",
                    "They remove the need for tool schemas",
                    "They make sessions unnecessary",
                ],
                "correct": 0,
                "explanation": (
                    "Golden cases turn desired behavior into repeatable tests after prompts, models, or tools change."
                ),
            },

            {
                "id": "M01.L05.Q13",
                "section_id": "evaluation-metrics",
                "question": (
                    "Why should tool trajectory be evaluated separately from final response quality?"
                ),
                "options": [
                    "Because an agent can reach a plausible final answer through an incorrect or unsafe action sequence",
                    "Because tool calls are unrelated to agent behavior",
                    "Because only the final sentence matters",
                    "Because tools cannot fail",
                ],
                "correct": 0,
                "explanation": (
                    "Reliable agents need both correct outcomes and correct execution behavior."
                ),
            },

            {
                "id": "M01.L05.Q14",
                "section_id": "production-boundaries",
                "question": (
                    "Which detail should be treated as version-specific rather than timeless architecture?"
                ),
                "options": [
                    "A specific ADK version, model identifier, or SDK method signature",
                    "The need for agent design",
                    "The value of session state",
                    "The idea of tool-event observability",
                ],
                "correct": 0,
                "explanation": (
                    "Framework and provider APIs can change while the underlying architecture remains useful."
                ),
            },

            {
                "id": "M01.L05.Q15",
                "section_id": "full-development-cycle",
                "type": "open",
                "question": (
                    "Design a complete development plan for a new tool-using agent. "
                    "Explain its blueprint, session strategy, Runner/runtime, tool definitions, "
                    "event handling, modular project structure, live interaction path, debugging workflow, "
                    "and formal evaluation plan."
                ),
            },
        ],

        "passing_score": 70,
    },
}
