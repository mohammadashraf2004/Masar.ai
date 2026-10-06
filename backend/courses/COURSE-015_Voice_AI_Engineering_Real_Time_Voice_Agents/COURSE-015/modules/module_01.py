"""M01.L01 — Intelligent Agents and Multimodal AI.

Two source chapters -> one complete learner-facing lesson + inline Images
+ inline Exercises + lesson Quiz.

Source alignment:
- Chapter 1: Intelligent Agents and Collaborative AI
- Chapter 2: Understanding Multimodality: Beyond Text
- Early Release draft; page numbers were not provided in the supplied source.

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Agent Foundations & Multimodal Intelligence"

MODULE_DESCRIPTION = (
    "Build a complete mental model of modern AI agents: how they evolved, "
    "how tools and execution loops turn models into actors, how memory and "
    "multi-agent systems extend them, and how multimodal perception lets "
    "agents reason over text, audio, images, and video."
)

SOURCE_CHAPTER = "1-2"

SOURCE_PAGES = "Early Release draft; page numbers not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Intelligent Agents and Multimodal AI",

    "slug": "agent-foundations-m01-l01",

    "description": (
        "Learn how a foundation model becomes an AI agent through perception, "
        "reasoning, tools, execution loops, memory, and collaboration, then "
        "extend that architecture beyond text to audio, vision, video, and "
        "multimodal fusion."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "ai-agents",
        "foundation-models",
        "rag",
        "tool-calling",
        "function-calling",
        "agent-loop",
        "memory",
        "multi-agent-systems",
        "multimodality",
        "audio-ai",
        "computer-vision",
        "multimodal-fusion",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Intelligent Agents and Multimodal AI",

        "content": r"""
# Intelligent Agents and Multimodal AI

> **Lesson:** M01.L01  
> **Module:** Agent Foundations & Multimodal Intelligence  
> **Source alignment:** Chapters 1–2 of the supplied Early Release material.  
> This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how AI agents evolved from classical autonomous systems to foundation-model-powered agents.
- Distinguish a foundation model, a RAG system, an agent, and a multi-agent system.
- Explain the four defining properties of a modern agent: perception, reasoning, action, and goal-directed autonomy.
- Describe a tool using a clear function declaration and connect that declaration to executable code.
- Trace the complete agent execution loop from user request to tool execution to final response.
- Explain why conversation history acts as short-term memory and how long-term memory differs from it.
- Compare router, parallel, sequential, circular, and dynamic multi-agent architectures.
- Explain why text can become a bottleneck for perception.
- Compare a cascaded voice pipeline with a live multimodal interface.
- Describe tokens, embeddings, visual representations, audio representations, and multimodal fusion at a useful conceptual level.
- Explain what audio, images, and sampled video contribute to an agent.
- Distinguish human-facing outputs from machine-facing structured outputs.
- Identify practical limits involving latency, privacy, media quality, tool safety, and infinite agent loops.

---

## 1. From AI models to AI agents

The easiest way to understand an AI agent is to first understand what came before it.

A normal model can **produce an answer**. An agent is designed to **work toward an objective**.

That difference sounds small, but it changes the architecture of the whole system.

A useful progression is:

```text
Classical autonomous agent
        ↓
Foundation model
        ↓
Foundation model + retrieval
        ↓
Foundation model + retrieval + actions
        ↓
Collaborating agents
```

Each stage adds a capability that the previous stage did not fully provide.

### Stage 0 — Classical or legacy agents

Agent research existed long before modern generative AI.

The central question was already familiar:

> Can a computational system perceive its environment and act autonomously to achieve a goal?

Three important architectural ideas emerged.

| Architecture | Main idea | Strength | Weakness |
|---|---|---|---|
| Deliberative | Build an internal representation, reason, then plan | Can think ahead | Can be slow and rigid |
| Reactive | Respond directly to the environment with simple behaviors | Fast response | Weak long-horizon planning |
| Hybrid | Combine planning with fast reactive behavior | Balances foresight and responsiveness | More complex architecture |

A famous deliberative idea is the **Belief-Desire-Intention (BDI)** model:

- **Beliefs** represent what the agent thinks is true about the world.
- **Desires** represent outcomes it would like to achieve.
- **Intentions** represent the plans or commitments it chooses to pursue.

The important lesson is not that modern agents literally implement BDI. The lesson is that the core problems—perception, planning, autonomy, and coordination—are not new.

Multi-agent systems also existed before generative AI. Researchers studied how many autonomous systems could cooperate, compete, negotiate, or divide work.

Modern foundation models did not erase those ideas. They supplied a new reasoning engine for them.

### Stage 1 — Foundation models and prompts

A large language model can receive a prompt and generate a response using patterns learned during training.

Foundation models broaden that idea. They are general-purpose models that can support many tasks and, depending on the model, more than one modality.

At this stage, the model is powerful but mostly **generic**.

Imagine an AI teaching assistant.

You ask:

> What is machine learning?

A foundation model can probably explain it well.

But then you ask:

> What did my professor say about the exam in yesterday's lecture?

The model cannot answer reliably unless that private course information has been provided to it.

So the limitation is not necessarily intelligence. It is **missing context**.

### Stage 2 — Foundation models plus retrieval

Retrieval-Augmented Generation (RAG) addresses that problem by retrieving relevant information and supplying it to the model when needed.

The simplified flow is:

```text
User question
    ↓
Search private or domain data
    ↓
Retrieve the most relevant pieces
    ↓
Provide them as model context
    ↓
Generate an answer grounded in that context
```

RAG is useful for two reasons.

**Contextual relevance:** the model receives information related to the current question instead of relying only on generic knowledge.

**Context-window management:** the application can retrieve a focused subset instead of placing an entire knowledge base into every prompt.

Our teaching assistant can now answer questions grounded in lecture notes, syllabi, or required readings.

But it is still mainly **answering**.

### Stage 3 — Agents that can act

The next jump occurs when the system receives tools.

A tool can let the application:

- run a calculation,
- call an API,
- retrieve live information,
- write or modify data,
- schedule an event,
- execute code,
- call another service,
- or trigger some other external operation.

Now the system can move from:

```text
"I can tell you how to do it."
```

to:

```text
"I can select the right capability and ask the application to do it."
```

That transition—from knowing to doing—is central to modern agentic systems.

### Stage 4 — Multi-agent systems

A single agent can become overloaded if it must understand every domain and choose among hundreds of tools.

A multi-agent system instead decomposes the work into specialists.

For example:

```text
Teaching Assistant Router
├── Math Agent
├── History Agent
└── Grammar Agent
```

The router decides which specialist should handle a request. Each specialist sees only the tools and knowledge that matter for its domain.

This returns us to an old agent idea with a new reasoning engine: **many autonomous components coordinating toward a larger goal**.

[[IMAGE_NEEDED: Five-stage evolution of AI agents | A left-to-right diagram showing Stage 0 classical agents, Stage 1 foundation models, Stage 2 foundation models plus RAG, Stage 3 tool-using agents, and Stage 4 multi-agent systems | Learner should notice that retrieval adds knowledge, tools add action, and multi-agent systems add specialization and collaboration]]

### Classical agents vs foundation-model-powered agents

The shift is deeper than simply replacing rules with an LLM.

| Dimension | Classical agents | FM-powered agents |
|---|---|---|
| Reasoning | Explicit rules, search, symbolic or formal logic | Learned model behavior guided by prompts/context |
| Knowledge | Curated databases and hand-built rules | Broad learned knowledge plus optional retrieved context |
| Planning | Often fixed or formally defined | Can generate flexible plans at runtime |
| Tool selection | Usually hard-coded | Can select tools from natural-language descriptions |
| Transparency | Logic can often be inspected directly | Internal model reasoning is less transparent |
| Flexibility | Strong inside a narrow designed environment | Can adapt to a wider range of natural-language tasks |

The trade-off matters: modern systems gain flexibility, but developers need stronger evaluation, observability, validation, and guardrails.

---

## 2. What actually makes a system an agent?

Calling every chatbot an "agent" makes the word nearly useless.

A better mental model contains four parts.

### 2.1 Perception

The system receives information from its environment.

That could be:

- a user message,
- a document,
- an API result,
- a database record,
- an audio stream,
- a camera frame,
- or another agent's output.

Perception answers:

> What is happening right now?

### 2.2 Reasoning and decision-making

The system interprets what it perceived and chooses what to do next.

It might decide to:

- answer directly,
- retrieve more information,
- call a tool,
- ask the user a clarifying question,
- delegate to another agent,
- or stop because the goal is complete.

Reasoning answers:

> Given the goal and current state, what should happen next?

### 2.3 Action

An agent needs some way to affect its environment.

Tools provide that bridge.

Examples:

```text
calculator()
search_course_notes()
create_calendar_event()
run_python()
send_request_to_crm()
```

The model itself may decide **which action is appropriate**, but the surrounding application remains responsible for actually executing controlled external actions.

### 2.4 Goal-directed autonomy

An agent is not supposed to require the user to manually specify every intermediate operation.

Instead of:

```text
1. Search this database.
2. Read result 4.
3. Call this API.
4. Format the response.
```

the user can provide a higher-level goal:

```text
Find the most relevant course material and explain the concept to me.
```

The system decides the intermediate steps.

A useful definition for this lesson is:

> **An AI agent is a foundation-model-powered system that perceives its environment, makes decisions, and uses available tools to work toward a specific goal with some degree of autonomy.**

[[IMAGE_NEEDED: Sense-think-act agent loop | A circular diagram with Environment -> Perception -> Foundation Model / Reasoning -> Tool or Action -> Environment, with Goal and Instructions influencing the reasoning step | Learner should notice that an agent is a loop interacting with an environment, not merely a single model response]]

### Model vs RAG vs agent

These concepts are related but not interchangeable.

| System | Can generate? | Can retrieve private context? | Can perform external actions? |
|---|---:|---:|---:|
| Foundation model | Yes | Not by itself | Not by itself |
| RAG application | Yes | Yes | Usually not required |
| Tool-using agent | Yes | Possibly | Yes |
| Multi-agent system | Yes | Possibly | Yes, through multiple collaborating agents |

This distinction prevents a common mistake:

> **RAG is not automatically an agent. Tool calling is not automatically a complete agent either.**

Agentic behavior emerges from the full loop: perception, decision-making, action, state, and goal pursuit.

---

## 3. Tools and function declarations: giving the agent hands

Suppose we want a Math Agent to add a list of integers.

We need two different things:

1. A **description** the model can understand.
2. A **real implementation** the application can execute.

These are not the same thing.

### 3.1 The function declaration

The declaration acts like a small user manual.

A good declaration tells the model:

- the function name,
- what the function does,
- which inputs it expects,
- the input types,
- what it returns,
- and useful examples.

For example:

```text
Function: add

Purpose:
    Add a list of integers.

Input:
    numbers: list[int]

Output:
    The sum of the integers.

Examples:
    add([1, 2, 3]) -> 6
    add([-1, 0, 1]) -> 0
    add([]) -> 0
```

Why include examples?

Because examples demonstrate the pattern of correct use. A small set of demonstrations can help the model infer how the function should be called.

### Tool vs function

A useful formal distinction is:

```text
Tool
└── one or more function declarations
```

A tool can therefore be a container for related functions.

For example:

```text
Math Tool
├── add
├── subtract
├── multiply
└── divide
```

In everyday discussion, developers often use *tool* and *function* interchangeably. The distinction becomes useful when one tool groups several related actions.

### 3.2 Human-readable vs machine-readable declarations

A docstring-like declaration is easy for people to read.

Production systems often need a structured schema as well.

Conceptually:

```json
{
  "name": "add",
  "description": "Calculates the sum of a list of integers.",
  "parameters": {
    "type": "object",
    "properties": {
      "numbers": {
        "type": "array",
        "items": {"type": "integer"}
      }
    },
    "required": ["numbers"]
  }
}
```

Structured formats reduce ambiguity and are easier for software to validate and parse.

The supplied source uses an OpenAPI/JSON-style representation and then shows how an SDK can package a function declaration into a tool object.

The format may differ across SDKs, but the engineering principle is stable:

> The model needs a structured description of the action before it can intelligently request that action.

### 3.3 The real implementation

A declaration does not execute anything.

We still need real code:

```python
def add(numbers: list[int]) -> int:
    return sum(numbers)
```

Then we can create a registry:

```python
function_handler = {
    "add": add,
}
```

This registry connects:

```text
model-generated function name
            ↓
real executable application function
```

That separation is important for both architecture and safety.

The model proposes an action. Your application decides whether and how to execute it.

{{exercise:M01.L01.EX01}}

---

## 4. The agent execution loop

This is one of the most important parts of the lesson.

Consider the user request:

> Add all the numbers from 1 through 5.

The model has been told that an `add` function exists.

### Step 1 — The user asks

The application sends the request to the model together with:

- system instructions,
- relevant conversation content,
- and the available tool declarations.

### Step 2 — The model reasons about the request

The model determines that the request is arithmetic and that the `add` function is appropriate.

### Step 3 — The model returns a function-call request

A crucial point:

> **The model has not executed your Python function.**

Instead, it may return a structured request equivalent to:

```json
{
  "name": "add",
  "arguments": {
    "numbers": [1, 2, 3, 4, 5]
  }
}
```

The model is effectively saying:

```text
I recommend executing add(numbers=[1,2,3,4,5]).
```

### Step 4 — The host application executes the function

Your code receives the request, validates it, looks up the implementation, and executes it:

```python
function_name = "add"
function_args = {"numbers": [1, 2, 3, 4, 5]}

function_to_call = function_handler[function_name]
result = function_to_call(**function_args)

print(result)
# 15
```

### Step 5 — The tool result goes back to the model

The application sends the tool result back into the conversation context.

Conceptually:

```text
User:
    Add 1 through 5.

Assistant tool request:
    add(numbers=[1,2,3,4,5])

Tool result:
    15
```

The model can now generate a natural response:

```text
The sum is 15.
```

### Why send the result back?

Because the model needs to know what actually happened.

It requested an action, but the application performed the action.

Without the tool-result message, the model would not reliably know whether:

- the function succeeded,
- it failed,
- it returned a value,
- or the application rejected the request.

### The core loop

```text
1. User asks
2. Model decides
3. Model requests a tool
4. Application executes
5. Tool result returns to model
6. Model decides again
```

Step 6 is important because real agents may need **another** action.

So a more general loop is:

```python
while not finished:
    response = call_model(history, tools)

    if response.requests_tool:
        result = execute_validated_tool(response.tool_call)
        history.append(result)
    else:
        return response.final_answer
```

This is why frameworks can feel magical: they automate a loop that you can build manually.

[[IMAGE_NEEDED: Complete single-turn agent execution loop | A six-stage flow showing User -> Model with instructions/tools -> Function-call request -> Host application execution -> Tool result -> Model final response | Learner should notice the execution boundary: the model requests an action, while application code performs it]]

### Automatic function calling

Some SDKs can automate parts of this cycle.

That can greatly reduce code, but you should still understand the manual version because it reveals:

- where validation belongs,
- where authorization belongs,
- where failures can occur,
- and which component actually executes side effects.

### Agent deployment is separate from agent logic

The execution loop is application logic.

It can be hosted in many ways:

- locally during development,
- on a virtual machine,
- in a container,
- on Kubernetes,
- or through serverless infrastructure.

Changing deployment does not change the fundamental sense-decide-act loop.

---

## 5. Multi-turn agents and memory

A single-turn agent is useful, but real conversation depends on state.

Consider:

```text
User: What is 100 + 50?
Agent: 150.
User: Now multiply that by 2.
```

What does **that** refer to?

It refers to the previous result: 150.

Without the previous interaction, the second request is incomplete.

### 5.1 Short-term memory

Short-term memory is the current conversation/session context.

It can include:

- user messages,
- model replies,
- tool requests,
- tool results,
- relevant media references,
- and state produced during the session.

A simplified history might look like:

```python
history = [
    {"role": "user", "content": "What is 100 + 50?"},
    {"role": "assistant", "tool_call": "add(100, 50)"},
    {"role": "tool", "content": "150"},
    {"role": "assistant", "content": "150"},
    {"role": "user", "content": "Now multiply that by 2."},
]
```

At each step, the model examines the available history and decides whether to:

1. call another tool,
2. ask the user for missing information,
3. or produce the final answer.

### Multi-step requests

A multi-turn loop is also useful when one user request contains several operations:

```text
Subtract 10 from 50, then divide the result by 4.
```

Possible execution:

```text
subtract(50, 10) -> 40
divide(40, 4) -> 10
final answer -> 10
```

The intermediate result becomes part of the working state.

### 5.2 Where short-term memory can live

Common approaches include:

| Storage | Good for | Main limitation |
|---|---|---|
| In-memory variable | Local scripts and prototypes | Lost when process ends |
| Database | Durable production sessions | More operational overhead |
| Cache such as Redis | Fast session state | Requires retention strategy |
| Client-side storage | Reducing server-side session state | Less server control and limited capacity |
| Cloud logs/storage | Operational history and larger artifacts | Must handle privacy and retrieval carefully |

For multimodal applications, large media such as audio or video is often stored separately, while conversation state stores references and metadata.

### 5.3 Long-term memory

Short-term memory answers:

> What happened in this conversation?

Long-term memory answers:

> What useful information should persist across conversations?

Examples:

- a user preference,
- a stable project fact,
- an important summary,
- a recurring constraint,
- or a previous interaction that is relevant again.

Possible storage strategies include:

**Vector databases**  
Store embeddings and retrieve semantically related memories.

**Graph databases**  
Represent relationships such as users, projects, topics, purchases, or entities.

**Traditional databases/object storage**  
Preserve structured data or complete historical records.

Long-term memory should not mean "store everything forever."

A production system needs decisions about:

- what is worth remembering,
- consent,
- retention,
- deletion,
- access control,
- and when a memory is safe to reuse.

### 5.4 Preventing infinite loops

A multi-turn execution loop can get stuck.

For example:

```text
tool A -> result
model -> tool A again
tool A -> similar result
model -> tool A again
...
```

A practical guardrail is a maximum iteration count.

```python
MAX_STEPS = 8

for step in range(MAX_STEPS):
    ...
```

The exact number depends on the application.

The principle is universal:

> An autonomous loop needs a stopping policy.

You should also record operational metrics such as:

- tool-call count,
- latency,
- token usage,
- failures,
- retries,
- and total execution time.

Those measurements help with debugging, cost control, and optimization.

[[IMAGE_NEEDED: Short-term and long-term memory architecture | A diagram showing one active conversation feeding short-term/session memory, with selected durable facts or summaries written to long-term storage and later retrieved into a future session | Learner should notice that session history and cross-session memory serve different purposes]]

---

## 6. Agents calling agents

Why not build one giant agent with every possible capability?

Because a monolithic agent may need to:

- reason over too many tools,
- process irrelevant instructions,
- maintain too much context,
- handle unrelated domains,
- and debug many possible interaction paths.

Specialization provides another option.

### The specialist model

Imagine an educational system:

```text
Student
   ↓
Teaching Router
   ├── Math Agent
   ├── History Agent
   └── Grammar Agent
```

The router mainly decides where work should go.

Each specialist has:

- narrow instructions,
- limited tools,
- relevant knowledge,
- and a clearly defined responsibility.

This resembles microservice architecture: split a large problem into smaller components with explicit responsibilities.

### Five common collaboration patterns

#### 6.1 Router pattern

```text
User
 ↓
Router
 ├─> Specialist A
 ├─> Specialist B
 └─> Specialist C
```

The router chooses the appropriate specialist and may combine the result.

Use it when requests belong to distinct domains.

#### 6.2 Parallel pattern

```text
          ┌─> Flight Agent ─┐
User ────>├─> Hotel Agent  ─┼─> Aggregator
          └─> Events Agent ─┘
```

Independent tasks run concurrently.

Use it when subtasks do not depend on one another.

The benefit is reduced total latency.

#### 6.3 Sequential pattern

```text
Ingestion Agent
      ↓
Cleaning Agent
      ↓
Analysis Agent
      ↓
Report Agent
```

Each step depends on the previous output.

Use it for predictable pipelines.

#### 6.4 Circular pattern

```text
Writer -> Editor
  ↑        ↓
  └────────┘
```

Agents repeatedly refine an artifact.

Use it for iterative improvement.

You still need a stopping condition, otherwise the collaboration can loop forever.

#### 6.5 Dynamic pattern

```text
Agent A <--> Agent B
   ^  \       /  ^
   |   \     /   |
   v    v   v    v
Agent C <--> Agent D
```

There is no single fixed route. Agents communicate according to the state of the task.

This is flexible but much harder to reason about and debug.

[[IMAGE_NEEDED: Five multi-agent orchestration patterns | One figure containing Router, Parallel, Sequential, Circular, and Dynamic patterns with small labeled node-and-arrow diagrams | Learner should compare how control flow differs across the five designs]]

### The key unifying idea

An agent can treat another agent as a specialized capability.

From the perspective of the caller, this can resemble a tool call:

```text
"I need math expertise"
        ↓
call Math Agent
        ↓
receive result
        ↓
continue reasoning
```

This makes complex systems modular.

{{exercise:M01.L01.EX02}}

---

## 7. Extending perception beyond text

So far, our agent can perceive text and structured information.

But the real world contains much more than text.

A **modality** is a type of signal or communication channel.

Examples include:

- text,
- audio,
- images,
- and video.

A multimodal agent can use more than one modality in the same task.

### The text bottleneck

Text is efficient, but converting everything into text can lose information.

Suppose a person says:

```text
"Oh, fantastic. It's raining again."
```

A transcript captures the words.

But it may fail to preserve:

- a sigh,
- sarcasm,
- unusual stress,
- speaking speed,
- background rain,
- or another sound occurring at the same time.

Now imagine a UI-debugging agent.

A user may have to explain:

```text
The third button from the top is a few pixels lower than the one beside it.
```

A visual model could instead inspect the interface directly.

The problem is the same:

> When people must translate sensory information into text, part of the original signal can disappear.

### Multimodal perception changes the agent loop

A text agent might perceive:

```text
user prompt + retrieved documents + API results
```

A multimodal agent may perceive:

```text
speech + image/frame + text + tool result + conversation state
```

This makes the perception stage richer, but it also introduces new engineering concerns:

- bandwidth,
- synchronization,
- media quality,
- latency,
- privacy,
- and context management.

---

## 8. Cascaded voice systems vs live multimodal interfaces

Before live multimodal systems, voice applications commonly used a cascade.

### Cascaded pipeline

A simplified modern LLM voice pipeline is:

```text
Microphone
   ↓
ASR / Speech-to-Text
   ↓
Text model
   ↓
Text response
   ↓
TTS / Text-to-Speech
   ↓
Speaker
```

This architecture is valid and can work very well.

The important issue is that each boundary has a cost.

### Cost 1 — Latency

The system may need to:

1. collect enough audio,
2. recognize speech,
3. send text to the model,
4. wait for model output,
5. synthesize speech,
6. start playback.

Streaming can reduce the delay, but multiple coordinated components remain.

### Cost 2 — Information loss

When audio is reduced to text, the downstream reasoning system may not receive every useful acoustic cue.

A transcript focuses on linguistic content.

The original signal may also contain:

- timing,
- pitch,
- stress,
- emotion-related cues,
- environmental sound,
- overlap,
- and silence.

### Live multimodal interface

The supplied source describes a developer-facing model where a live session can accept combinations of:

- continuous audio,
- text,
- and sampled visual frames,

while returning streamed responses and structured events.

Conceptually:

```text
Audio ───────────┐
Images/frames ───┼──> Live multimodal session ──> Audio/Text/Tool events
Text ────────────┘
```

The important point is not to invent hidden internal architecture.

The useful engineering claim is about the interface:

> The application does not always have to flatten every input into one text transcript before the model can use it.

This changes the design question.

Instead of asking:

> How do I convert every signal to text?

you can ask:

> Which signals are useful, when should I send them, and how should I preserve the context connecting them?

[[IMAGE_NEEDED: Cascaded pipeline versus live multimodal session | Side-by-side diagram: left shows Microphone -> ASR -> Text Model -> TTS -> Speaker; right shows Audio + Visual Frames + Text entering one stateful multimodal session that streams audio/text/tool events | Learner should notice fewer developer-visible processing boundaries and that text transcription is no longer the mandatory bridge for every modality]]

{{exercise:M01.L01.EX03}}

---

## 9. Tokens, embeddings, and shared representations

How can one model work with such different inputs?

We need a conceptual model.

### 9.1 Text

Models do not simply read text as whole human words.

A tokenizer converts text into units called **tokens**.

A token may represent:

- a word,
- part of a word,
- punctuation,
- whitespace,
- or another learned unit.

Token IDs are mapped to vectors.

These vectors are called **embeddings**.

An embedding is a learned numerical representation that a model can use in computation.

### 9.2 Images

Raw pixel grids also need to become model-readable representations.

A useful model from Vision Transformers is:

```text
Image
 ↓
Split into patches
 ↓
Project patches into vectors
 ↓
Process the sequence
```

A common teaching example uses 16×16 patches, although real systems may use different strategies.

These vectors are sometimes described as **visual tokens**.

Do not take that phrase too literally.

The useful idea is:

> The image becomes a sequence of learned representations the model can reason over.

### 9.3 Audio

Audio begins as a waveform.

Digital audio samples that waveform over time.

Systems can derive features related to:

- frequency,
- timing,
- energy,
- pitch,
- and other acoustic patterns.

Modern models can transform the signal into learned audio representations that are useful for downstream reasoning.

### 9.4 Shared or compatible representation spaces

Once different modalities become learned representations, the model can learn relationships between them.

A useful historical example is CLIP.

Its image and text encoders were trained so that matching image-text pairs became closer in representation space while mismatched pairs became farther apart.

Conceptually:

```text
photo of a bicycle  ──close──  "a bicycle"
photo of a bicycle  ──far────  "a bowl of soup"
```

CLIP demonstrates cross-modal alignment.

A live multimodal agent needs an even broader capability because it may need to combine:

- speech,
- visual context,
- conversation state,
- text,
- and tool results.

[[IMAGE_NEEDED: From raw modalities to learned representations | A diagram with Text -> Tokens/Embeddings, Image -> Patches/Visual Representations, and Audio -> Acoustic Features/Audio Representations, all feeding a shared reasoning context | Learner should notice that raw media is transformed before cross-modal reasoning occurs]]

### A careful boundary

Tokens, embeddings, and attention are useful teaching concepts.

They should not be treated as a complete map of a proprietary model's hidden internals.

A good engineering explanation distinguishes:

```text
What the public interface guarantees
        from
What we use as a conceptual model
        from
What the proprietary implementation actually does internally
```

---

## 10. Giving the agent ears

Audio contributes more than a transcript.

### 10.1 Digitizing sound

Sound is a pressure wave.

A digital system samples that wave many times per second and represents those measurements numerically.

The supplied material notes a later implementation path that sends raw PCM microphone audio with a declared 16 kHz sample rate.

The important concept in this lesson is broader:

```text
physical sound
    ↓
digital samples
    ↓
acoustic representation
    ↓
model reasoning
```

### 10.2 What ASR gives you

Automatic Speech Recognition focuses on turning speech into text.

That transcript is extremely useful for:

- captions,
- logs,
- indexing,
- search,
- auditing,
- and text-based downstream systems.

But transcription may not preserve all non-verbal information.

### 10.3 What direct audio context can add

Depending on the selected model and configuration, audio can preserve cues related to:

**Prosody**  
Rhythm, stress, intonation, and pacing.

**Environmental context**  
Non-speech events such as music, alarms, background conversation, or machinery.

**Multilingual conversation**  
Live audio interfaces may support switching languages without forcing one fixed transcription language, although performance depends on the actual model, language, accent, audio quality, and deployment settings.

### 10.4 Native audio output

A traditional system often does:

```text
model text -> TTS -> speech
```

A live audio model can expose streamed speech output through the model interface.

From an application perspective, this can create a tighter conversational loop.

However, do not assume every advertised advanced audio behavior is available on every model.

Model-specific capabilities must be verified for the exact API and model used in production.

---

## 11. Giving the agent eyes

Images add spatial information that text often describes poorly.

### 11.1 From CNNs to multimodal visual reasoning

Convolutional Neural Networks remain important in computer vision.

They detect local visual patterns through learned filters.

But a multimodal agent often needs more than classification.

It may need to:

- read visible text,
- identify an object,
- answer a question about a region,
- understand layout,
- connect a spoken instruction to a visible item,
- or decide that visual evidence requires a tool call.

### 11.2 Visual reasoning capabilities

A multimodal system may support tasks such as:

**Visible text understanding**  
Reading text present in an image.

**Spatial reasoning**  
Understanding relationships such as left/right, alignment, connection, or position.

**Scene understanding**  
Combining objects, layout, labels, and user intent.

A dedicated OCR or computer-vision system can still be valuable in production.

Multimodal models do not eliminate specialized tools.

### 11.3 Visual limitations

Vision performance can degrade because of:

- small text,
- poor lighting,
- motion blur,
- low resolution,
- compression,
- occlusion,
- or missing visual detail.

More visual detail can also increase:

- token usage,
- bandwidth,
- latency,
- and cost.

So visual quality is an engineering trade-off, not simply "more is better."

### 11.4 Video is images plus time

A video may contain many frames every second.

Sending every frame to a model is often unnecessary.

A practical live-agent approach is **frame sampling**.

Instead of:

```text
30 or 60 frames every second
```

the application may periodically select frames.

The supplied source states that its current Live API path uses JPEG/PNG frames at a maximum of one frame per second.

Treat that as an implementation-specific constraint from the supplied material, not as a timeless rule for all multimodal APIs.

Frame sampling is useful for tasks like:

- "What am I looking at?"
- "Which button should I press?"
- "Does this chart match the report?"

It is a poor fit for tasks requiring:

- precise high-speed motion analysis,
- frame-by-frame sports analysis,
- exact gesture timing,
- or other rapidly changing visual signals.

---

## 12. Multimodal fusion: connecting what the user means

Having multiple inputs is not enough.

The system must connect them.

Imagine:

1. A user points a camera at a circuit board.
2. The user points toward a damaged component.
3. The user asks, "What is this part?"

The speech alone is incomplete.

```text
"What is this part?"
```

What does **this** mean?

The image alone is also incomplete.

The model can see many components, but it does not automatically know which one the user means.

The value comes from combining the signals.

```text
spoken reference + visual scene + interaction context
                       ↓
                intended referent
```

That is **multimodal fusion**.

### Attention as a conceptual explanation

In a Transformer, attention helps relate pieces of information.

For teaching purposes, we can extend that intuition:

- a spoken phrase,
- a visible region,
- a gesture,
- and previous conversation context

can influence one another during reasoning.

Do not confuse this with having access to the exact internal attention maps of a proprietary model.

The architectural lesson is simpler:

> Cross-modal context can preserve relationships that disappear when each modality is handled independently.

[[IMAGE_NEEDED: Point-and-ask multimodal fusion | A user points at one component on a circuit board while asking "What is this part?", with arrows from the spoken phrase and indicated image region into one shared context | Learner should notice that neither speech nor image alone fully resolves the word "this"]]

---

## 13. Multimodal output and tool use

Multimodality is not only about input.

An agent may produce outputs for two very different audiences.

### 13.1 Human-facing outputs

These are meant for a person.

Examples:

- spoken response,
- text,
- image,
- visual highlight,
- chart,
- UI overlay.

Imagine a dashboard assistant.

The user asks:

> Which metric changed the most since yesterday?

A useful interface might:

1. answer aloud,
2. highlight the relevant chart,
3. and leave a short text summary.

Using more modalities is not automatically better.

The best output is the one that reduces ambiguity and matches the task.

### 13.2 Machine-facing structured outputs

These are meant for software.

For example, an agent inspecting an analog gauge might produce:

```json
{
  "reading": 74,
  "unit": "psi",
  "confidence_note": "Need a clearer frame to confirm the final digit."
}
```

Or a scheduling agent may convert speech plus visible calendar context into tool arguments.

This reconnects multimodal perception with the execution loop:

```text
Audio/Image/Text
      ↓
Multimodal reasoning
      ↓
Structured tool request
      ↓
Host application validates
      ↓
Tool executes
      ↓
Result returns to model
      ↓
Human-facing answer
```

The execution boundary has not changed.

Even in a multimodal agent:

> **The model can request an action; the host application remains responsible for safe execution.**

---

## 14. Designing a reliable multimodal agent

Combining agents and multimodality creates a powerful system, but also a larger failure surface.

### 14.1 Tool validation

Never treat model-generated arguments as automatically trustworthy.

Validate:

- function name,
- schema,
- data type,
- range,
- authorization,
- and side effects.

For sensitive operations, add explicit confirmation or policy checks.

### 14.2 Loop limits

Every autonomous loop should have a stopping rule.

Possible controls include:

```text
maximum steps
maximum retries
maximum execution time
maximum tool calls
budget/token limit
```

### 14.3 Privacy and consent

Microphones and cameras capture sensitive environmental information.

A production application should make recording state obvious and define:

- when capture starts,
- what is transmitted,
- what is stored,
- how long it is retained,
- who can access it,
- and how users can stop or delete it.

### 14.4 Media quality

Multimodal reasoning depends on the quality of the signal.

Watch for:

- noisy microphones,
- poor lighting,
- tiny text,
- weak network connections,
- compression artifacts,
- and badly sampled video.

### 14.5 Latency

A real-time experience has a latency budget.

Latency may come from:

```text
capture
+ network transfer
+ model processing
+ tool execution
+ additional model turns
+ media playback
```

Agent design therefore requires architectural choices, not just a good prompt.

### 14.6 Observability

Log enough to understand the system without violating privacy.

Useful operational information includes:

- session duration,
- model latency,
- tool latency,
- number of tool calls,
- error type,
- token usage,
- retries,
- user interruptions,
- and agent step count.

### 14.7 Human judgment still matters

Multimodal perception can make an agent feel more capable because it can see and hear.

That does not make its conclusions infallible.

High-risk domains still require:

- validation,
- appropriate safety policies,
- constrained tools,
- and human oversight where needed.

{{exercise:M01.L01.EX04}}

---

## Important misconceptions

### Misconception 1

> "If an LLM can call a function, it directly executes my Python code."

### Why this is wrong

In the manual function-calling model taught here, the foundation model produces a structured request. The host application maps that request to real executable code and decides whether to run it.

---

### Misconception 2

> "RAG and agents are the same thing."

### Why this is wrong

RAG supplies relevant context. An agent additionally makes decisions and can take actions through tools while pursuing a goal.

RAG can be one component inside an agent.

---

### Misconception 3

> "Memory means sending every past conversation to the model forever."

### Why this is wrong

Short-term session history and durable long-term memory solve different problems. Production systems need retrieval, summarization, retention rules, and privacy controls.

---

### Misconception 4

> "A multi-agent system is always better than one agent."

### Why this is wrong

Multi-agent systems add communication, coordination, state, and debugging complexity. Use specialization when the problem benefits from decomposition.

---

### Misconception 5

> "Multimodal means converting audio and images into text first."

### Why this is wrong

That is one possible architecture, but modern live multimodal interfaces can expose audio, images/frames, and text inside the same interaction loop.

---

### Misconception 6

> "If a model can see an image, it sees perfectly."

### Why this is wrong

Resolution, compression, lighting, motion, occlusion, and tiny text can all reduce visual accuracy.

---

### Misconception 7

> "More modalities always produce a better product."

### Why this is wrong

Every modality adds cost, bandwidth, latency, privacy concerns, and interface complexity. Use the modalities that materially improve the task.

---

## Key terminology

| Term | Meaning |
|---|---|
| Agent | A goal-directed system that perceives, decides, and uses available actions/tools |
| Foundation Model (FM) | A general-purpose model that can support many downstream tasks |
| LLM | A foundation model focused strongly on language processing/generation |
| RAG | Retrieval-Augmented Generation; retrieval supplies relevant external context to generation |
| Perception | Information the agent receives from its environment |
| Tool | A packaged capability available to an agent |
| Function declaration | Structured description of an executable function available to the model |
| Function call | A structured model request asking the application to invoke a function |
| Execution boundary | The separation between model-requested action and host-application execution |
| Agent loop | Repeated perceive/decide/act/update cycle |
| Short-term memory | State/history used within an active conversation or session |
| Long-term memory | Information persisted and retrieved across sessions |
| Multi-agent system | Multiple specialized agents collaborating on a larger task |
| Router pattern | A coordinator delegates tasks to appropriate specialists |
| Parallel pattern | Independent agent tasks run concurrently |
| Sequential pattern | One agent's output feeds the next agent |
| Circular pattern | Agents iteratively pass results around a feedback loop |
| Dynamic pattern | Agents communicate flexibly without one fixed control path |
| Modality | A data or communication channel such as text, audio, image, or video |
| ASR | Automatic Speech Recognition; converts speech into text |
| TTS | Text-to-Speech; synthesizes speech from text |
| Token | A model-processing unit derived from input data such as text |
| Embedding | A learned vector representation |
| Visual token/representation | Vectorized representation derived from image content |
| Prosody | Rhythm, stress, pitch, timing, and intonation in speech |
| Frame sampling | Selecting periodic frames from video instead of processing every frame |
| Multimodal fusion | Combining information from multiple modalities into one reasoning context |
| Human-facing output | Output intended for a user to read, hear, or see |
| Machine-facing output | Structured output intended for software or tool execution |

---

## Self-check

Before continuing, make sure you can answer:

1. What capability separates a tool-using agent from a plain foundation-model chatbot?
2. What does RAG add, and what does it not automatically add?
3. Why is a function declaration different from the real function implementation?
4. Who actually executes a tool call?
5. Why must a tool result be returned to the model?
6. What are the three choices a multi-turn agent often makes after reviewing its state?
7. How do short-term and long-term memory differ?
8. Why can a monolithic agent become difficult to maintain?
9. When would you choose parallel orchestration instead of sequential orchestration?
10. Why can text become a bottleneck for audio and visual information?
11. What are the main disadvantages of a cascaded voice pipeline?
12. What is an embedding?
13. Why is a patch-based explanation useful for image representations?
14. Why does a live video agent usually not need every camera frame?
15. What does multimodal fusion solve?
16. Why should capability claims about a proprietary multimodal model remain tied to the tested API/model?
17. Why do microphones and cameras increase the privacy burden of an AI application?
18. Which safeguards would you add before allowing an agent to execute a destructive tool?

---

## Retain this idea

**A modern AI agent is not just a language model with a clever prompt. It is a controlled loop in which a foundation model perceives context, decides what should happen next, requests tools when action is required, receives results, and continues toward a goal. Memory extends that loop across turns, multi-agent systems divide it among specialists, and multimodality expands perception beyond text into signals such as audio and vision.**
""".strip(),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "agent-evolution",
                "title": "From AI Models to AI Agents",
                "order": 1,
            },
            {
                "id": "agent-definition",
                "title": "What Actually Makes a System an Agent?",
                "order": 2,
            },
            {
                "id": "tools",
                "title": "Tools and Function Declarations",
                "order": 3,
            },
            {
                "id": "execution-loop",
                "title": "The Agent Execution Loop",
                "order": 4,
            },
            {
                "id": "memory",
                "title": "Multi-Turn Agents and Memory",
                "order": 5,
            },
            {
                "id": "multi-agent",
                "title": "Agents Calling Agents",
                "order": 6,
            },
            {
                "id": "multimodality",
                "title": "Extending Perception Beyond Text",
                "order": 7,
            },
            {
                "id": "cascaded-vs-native",
                "title": "Cascaded Voice Systems vs Live Multimodal Interfaces",
                "order": 8,
            },
            {
                "id": "representations",
                "title": "Tokens, Embeddings, and Shared Representations",
                "order": 9,
            },
            {
                "id": "audio",
                "title": "Giving the Agent Ears",
                "order": 10,
            },
            {
                "id": "vision-video",
                "title": "Giving the Agent Eyes",
                "order": 11,
            },
            {
                "id": "fusion",
                "title": "Multimodal Fusion",
                "order": 12,
            },
            {
                "id": "multimodal-output",
                "title": "Multimodal Output and Tool Use",
                "order": 13,
            },
            {
                "id": "production-design",
                "title": "Designing a Reliable Multimodal Agent",
                "order": 14,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Design a Safe Calculator Tool",

            "lesson_code": "M01.L01",

            "section_id": "tools",

            "placement": "after_section",

            "description": (
                "Practice separating a model-readable function declaration "
                "from the real executable implementation."
            ),

            "instructions": (
                "1. Design a function declaration for divide(a, b).\n"
                "2. Include a clear function name, description, argument types, "
                "return value, and two examples.\n"
                "3. Write the corresponding Python implementation.\n"
                "4. Add a validation rule for division by zero.\n"
                "5. Explain which part is visible to the model and which part "
                "is executed by the host application."
            ),

            "expected_output": (
                "A short function declaration, a Python divide implementation, "
                "a validation rule, and a paragraph explaining the execution boundary."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "function-declarations",
                "tool-design",
                "execution-boundary",
                "input-validation",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Choose a Multi-Agent Architecture",

            "lesson_code": "M01.L01",

            "section_id": "multi-agent",

            "placement": "after_section",

            "description": (
                "Choose an orchestration pattern based on dependencies between subtasks."
            ),

            "instructions": (
                "You are building an AI research assistant that must search three "
                "independent sources, compare their findings, then write one report.\n"
                "1. Decide which work should run in parallel.\n"
                "2. Decide which work must wait for previous results.\n"
                "3. Draw the agent flow using text arrows.\n"
                "4. Explain why a pure sequential or pure parallel design would be "
                "less appropriate than your chosen hybrid design.\n"
                "5. Add one stopping or failure-handling rule."
            ),

            "expected_output": (
                "A small architecture diagram plus a concise design explanation "
                "covering concurrency, dependencies, aggregation, and failure handling."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "multi-agent-design",
                "parallelism",
                "sequential-workflows",
                "orchestration",
            ],
        },

        {
            "id": "M01.L01.EX03",

            "title": "Compare Voice-Agent Architectures",

            "lesson_code": "M01.L01",

            "section_id": "cascaded-vs-native",

            "placement": "after_section",

            "description": (
                "Compare the information flow and engineering trade-offs of "
                "cascaded and live multimodal voice architectures."
            ),

            "instructions": (
                "1. Draw the cascaded path Microphone -> ASR -> Text Model -> TTS -> Speaker.\n"
                "2. Draw a live multimodal session receiving audio and text directly.\n"
                "3. Identify at least two places where the cascaded design can add latency.\n"
                "4. Give one example of information that transcription may fail to preserve.\n"
                "5. Name one reason you might still intentionally choose a cascaded design."
            ),

            "expected_output": (
                "Two text diagrams and a short comparison discussing latency, "
                "information preservation, modularity, and design trade-offs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "voice-architecture",
                "latency-reasoning",
                "multimodal-design",
            ],
        },

        {
            "id": "M01.L01.EX04",

            "title": "Design a Multimodal Support Agent",

            "lesson_code": "M01.L01",

            "section_id": "production-design",

            "placement": "after_section",

            "description": (
                "Apply the complete lesson by designing an agent that can hear, "
                "see, use tools, remember session context, and operate safely."
            ),

            "instructions": (
                "Design an agent that helps a user troubleshoot a software interface "
                "through voice and screen/camera input.\n"
                "1. Define the agent's goal.\n"
                "2. List the modalities it accepts.\n"
                "3. List three tools it may request.\n"
                "4. Describe its short-term memory.\n"
                "5. Explain one multimodal fusion case where text alone is insufficient.\n"
                "6. Add validation for at least one tool.\n"
                "7. Add a maximum-step rule.\n"
                "8. Add consent/retention rules for microphone or camera data.\n"
                "9. State which outputs should be human-facing and which should be structured."
            ),

            "expected_output": (
                "A one-page architecture specification covering perception, reasoning, "
                "tools, memory, fusion, output, validation, privacy, and stopping conditions."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-architecture",
                "multimodal-perception",
                "tool-safety",
                "memory",
                "privacy",
                "system-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Intelligent Agents and Multimodal AI — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "agent-evolution",
                "question": (
                    "Which change most directly turns a retrieval-based assistant "
                    "into an agent that can affect external systems?"
                ),
                "options": [
                    "Increasing the model context window",
                    "Giving it controlled tools/actions it can request",
                    "Storing more embeddings",
                    "Using a larger prompt",
                ],
                "correct": 1,
                "explanation": (
                    "Retrieval gives the model additional context. Tools create a path "
                    "from reasoning to controlled external action."
                ),
            },

            {
                "id": "M01.L01.Q02",
                "section_id": "agent-definition",
                "question": (
                    "Which set best captures the agent model used in this lesson?"
                ),
                "options": [
                    "Training, compression, deployment, monitoring",
                    "Perception, reasoning, action, goal-directed autonomy",
                    "Tokenization, batching, caching, quantization",
                    "Search, ranking, indexing, storage",
                ],
                "correct": 1,
                "explanation": (
                    "The lesson defines an agent around perception, decision-making, "
                    "action through tools, and autonomous pursuit of a goal."
                ),
            },

            {
                "id": "M01.L01.Q03",
                "section_id": "tools",
                "question": (
                    "What is the purpose of a function declaration?"
                ),
                "options": [
                    "To physically execute Python inside the model",
                    "To describe an available function, its inputs, and its purpose to the model",
                    "To replace all application validation",
                    "To permanently store conversation history",
                ],
                "correct": 1,
                "explanation": (
                    "A declaration is a model-readable description. The real implementation "
                    "still exists in application code or another executable service."
                ),
            },

            {
                "id": "M01.L01.Q04",
                "section_id": "execution-loop",
                "question": (
                    "After the model returns add(numbers=[1,2,3,4,5]), what should "
                    "happen next in manual function calling?"
                ),
                "options": [
                    "Assume the answer is 15 without executing anything",
                    "The model directly runs the local Python interpreter",
                    "The host validates and executes the mapped function",
                    "Delete the conversation history",
                ],
                "correct": 2,
                "explanation": (
                    "The model returns a structured request. Host application logic "
                    "maps it to executable code, validates it, and performs the action."
                ),
            },

            {
                "id": "M01.L01.Q05",
                "section_id": "memory",
                "question": (
                    "Why is conversation history necessary for a request such as "
                    "'Now multiply that result by 2'?"
                ),
                "options": [
                    "It supplies the referent for 'that result'",
                    "It increases camera resolution",
                    "It converts the system into RAG",
                    "It guarantees the tool cannot fail",
                ],
                "correct": 0,
                "explanation": (
                    "The phrase depends on a previous result. Session history provides "
                    "the short-term context needed to resolve that reference."
                ),
            },

            {
                "id": "M01.L01.Q06",
                "section_id": "multi-agent",
                "question": (
                    "Which pattern is most natural when several independent specialists "
                    "can work at the same time before their results are aggregated?"
                ),
                "options": [
                    "Parallel",
                    "Sequential",
                    "Circular",
                    "Single fixed function",
                ],
                "correct": 0,
                "explanation": (
                    "Parallel orchestration is designed for independent subtasks that "
                    "can execute concurrently."
                ),
            },

            {
                "id": "M01.L01.Q07",
                "section_id": "cascaded-vs-native",
                "question": (
                    "What is one limitation of converting speech to text before all reasoning?"
                ),
                "options": [
                    "Text cannot contain words",
                    "The conversion may lose timing, prosody, or environmental cues",
                    "ASR always makes the application faster",
                    "It prevents the use of databases",
                ],
                "correct": 1,
                "explanation": (
                    "A transcript preserves linguistic content but may omit acoustic "
                    "information such as stress, pace, non-speech sounds, or tone."
                ),
            },

            {
                "id": "M01.L01.Q08",
                "section_id": "representations",
                "question": (
                    "What is the safest conceptual statement about multimodal representations?"
                ),
                "options": [
                    "Every proprietary model uses exactly the same tokenizer for text, image, and audio",
                    "Raw modalities are transformed into learned representations that can participate in model computation",
                    "Images are always converted into English captions before reasoning",
                    "Audio must always be transcribed before a model can use it",
                ],
                "correct": 1,
                "explanation": (
                    "Representation details vary by architecture, but the stable teaching "
                    "idea is that raw media becomes model-readable learned representations."
                ),
            },

            {
                "id": "M01.L01.Q09",
                "section_id": "vision-video",
                "question": (
                    "Why might a live visual agent sample frames instead of sending every frame?"
                ),
                "options": [
                    "Because video contains no useful temporal information",
                    "To reduce bandwidth, token use, latency, and unnecessary processing",
                    "Because models can process only text",
                    "To guarantee perfect motion analysis",
                ],
                "correct": 1,
                "explanation": (
                    "Sampling can be efficient for slowly changing interaction contexts, "
                    "although it is unsuitable when fine-grained motion timing is required."
                ),
            },

            {
                "id": "M01.L01.Q10",
                "section_id": "fusion",
                "question": (
                    "Why does the question 'What is this part?' become a multimodal "
                    "fusion problem when a user points at a circuit board?"
                ),
                "options": [
                    "The audio is too loud",
                    "The word 'this' requires visual context to identify its referent",
                    "The image must first be converted to SQL",
                    "Tool calling cannot work with images",
                ],
                "correct": 1,
                "explanation": (
                    "The speech provides intent but an ambiguous reference. The visual "
                    "scene supplies the referent, so the two signals must be connected."
                ),
            },

            {
                "id": "M01.L01.Q11",
                "section_id": "production-design",
                "question": (
                    "Which safeguard directly addresses an agent repeatedly calling tools forever?"
                ),
                "options": [
                    "Increase image resolution",
                    "Add a maximum iteration/tool-call limit",
                    "Store every session permanently",
                    "Remove all structured outputs",
                ],
                "correct": 1,
                "explanation": (
                    "Agent loops need explicit stopping rules such as maximum steps, "
                    "timeouts, budgets, or retry limits."
                ),
            },

            {
                "id": "M01.L01.Q12",
                "section_id": "production-design",
                "type": "open",
                "question": (
                    "Design a small multimodal agent for a real task. Explain its goal, "
                    "inputs/modalities, tools, execution loop, short-term memory, one "
                    "fusion requirement, one privacy safeguard, one tool-validation rule, "
                    "and one stopping condition."
                ),
            },
        ],

        "passing_score": 70,
    },
}
