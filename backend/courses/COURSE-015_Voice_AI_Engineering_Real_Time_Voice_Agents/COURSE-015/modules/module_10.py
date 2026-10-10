"""M01.L10 — Evaluating Live Agents and Managing Tools at Scale.

Two source chapters -> one complete learner-facing lesson.

Source alignment:
- Chapter 16: Evaluation and Testing of Live Agent Systems
- Chapter 17: Managing Tools at Scale

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L10"
MODULE_ORDER = 1
MODULE_TITLE = "Live Agent Evaluation & Enterprise Tool Governance"
MODULE_DESCRIPTION = (
    "Build a rigorous evaluation factory for autonomous, multimodal, live agents—covering "
    "tool trajectories, multi-turn memory, simulators, raw-audio quality, interruptions, "
    "operational metrics, and production feedback—then organize the tools those agents use "
    "through enterprise Tool Registries, curated toolsets, dynamic search, API-first/MCP "
    "standardization, automated registration, and scalable governance."
)
SOURCE_CHAPTER = "16-17"
SOURCE_PAGES = "Early Release drafts; page numbers not provided"

TOPIC = {
    "title": "Evaluating Live Agents and Managing Tools at Scale",
    "slug": "agent-foundations-m01-l10",
    "description": (
        "Learn how to prove that an autonomous live agent works before and after deployment, "
        "then learn how to manage the growing enterprise tool ecosystem that determines what "
        "those agents can safely and reliably do."
    ),
    "order": 10,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 7.0,
    "skill_tags": [
        "agent-evaluation",
        "golden-dataset",
        "trajectory-evaluation",
        "multi-turn-evaluation",
        "memory-evaluation",
        "simulators",
        "autoraters",
        "adaptive-rubrics",
        "live-voice-evaluation",
        "multimodal-evaluation",
        "barge-in",
        "operational-metrics",
        "continuous-evaluation",
        "tool-registry",
        "tool-governance",
        "specialist-agents",
        "dynamic-tool-search",
        "api-first",
        "mcp",
        "tool-ci-cd",
        "enterprise-governance",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
        "M01.L08",
        "M01.L09",
    ],

    "lesson": {
        "title": "Evaluating Live Agents and Managing Tools at Scale",
        "estimated_minutes": 420,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Evaluating Live Agents and Managing Tools at Scale

> **Lesson:** M01.L10  
> **Source alignment:** Chapters 16 and 17 of the supplied Early Release material.  
> This lesson connects the quality side of AgentOps with the tool-governance side.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why evaluating an autonomous live agent is more complex than testing deterministic software or a static LLM.
- Explain why live-agent evaluation should begin with core reasoning and tool behavior before voice quality.
- Build a single-turn golden record containing expected tool, parameters, tool result, and final response.
- Evaluate correct tool selection, correct parameters, correct no-tool behavior, clarification behavior, and consistency.
- Explain trajectory evaluation and why final-response quality alone is insufficient.
- Explain the role of Autoraters and Adaptive Rubrics.
- Evaluate grounding between tool results and final responses.
- Track operational metrics such as token cost, latency, and oversized runtime/tool payloads.
- Extend a golden dataset from one tool call into a multi-step expected trajectory.
- Evaluate tool-chain efficiency and circuit-breaker/step-limit behavior.
- Evaluate short-term memory for topic relevance and adherence.
- Evaluate long-term memory summarization and retrieval.
- Explain why long-term-memory retrieval is also a RAG evaluation problem.
- Use Simulator agents to generate diverse evaluation interactions at scale.
- Explain why a Simulator is an actor rather than a judge.
- Organize evaluation metrics into generation/grounding, trajectory/execution, memory/context, and operational health.
- Map metric failures to optimization levers such as prompt optimization, context engineering, tool-schema improvement, and model selection.
- Integrate evaluation into staging and CI/CD as a deployment gate.
- Explain transcript-based voice evaluation and its limitations.
- Explain why raw-audio evaluation is needed for emotion, prosody, hesitation, and conversational dynamics.
- Explain how TTS-enabled Simulators can generate test audio with emotion and background noise.
- Evaluate interruption/barge-in behavior using latency, context switching, and context retention.
- Explain the source's view that monitoring is real-time evaluation.
- Identify when a full evaluation suite should be triggered.
- Explain how user feedback becomes richer golden evaluation data when joined with logs, memory, and tool trajectories.
- Categorize enterprise tools as code functions, local VPC REST APIs, or public REST APIs.
- Compare the latency, ownership, shareability, monitoring, security, and versioning trade-offs across tool categories.
- Explain why a Tool Registry becomes a single source of truth.
- Define the core registry functions: metadata, versioning, search/discovery, access control, robustness, lineage, and auditability.
- Compare generalist agents with full registry access against specialist agents with curated Tool Lists.
- Explain why reducing the tool search space can improve performance, predictability, testing, and security.
- Explain dynamic Tool Search as a middle ground between fully generalist and statically specialist designs.
- Explain how tools can remain distributed while registry/governance stays centralized.
- Design a standardized tool repository with tests and automated registration.
- Explain the source's API-first strategy for turning code/data tools into governed services.
- Explain how MCP can standardize discovery and invocation on top of service-based tool deployment.
- Compare decentralized, centralized, and federated organizational models for tool governance.
- Explain why evaluation results should feed Tool Registry governance and why registry constraints should improve evaluation outcomes.

---

## 1. Why live-agent evaluation is different

Traditional software testing often asks:

```text
Did this deterministic function return the expected result?
```

Static LLM evaluation asks something more flexible:

```text
Did the generated output match the intended meaning?
```

A live autonomous agent adds much more:

```text
reasoning
tool selection
tool parameters
multi-step execution
memory
latency
voice
emotion
interruptions
real-time behavior
```

The source describes this shift as moving from grading a static answer to grading a live performance.

### Key principle

> Evaluate the agent as a system, not only as a text generator.

[[IMAGE_NEEDED: Evaluation complexity ladder | Deterministic software -> static LLM -> autonomous tool-using agent -> live multimodal agent, with increasing dimensions of evaluation | Learner should see why each layer adds new failure modes]]

---

## 2. Voice quality cannot rescue bad reasoning

Imagine a Math Tutor that:

- sounds warm,
- detects frustration,
- responds instantly,

but gives the wrong geometry formula.

The system still fails.

Therefore, evaluation should start with:

```text
core intelligence
tool correctness
trajectory
final-answer grounding
```

before moving to:

```text
prosody
emotion
noise
barge-in
```

### Rule

> Establish cognitive correctness before polishing conversational realism.

---

## 3. Single-turn evaluation as the foundation

A simple single turn is:

```text
User asks
   ↓
Agent chooses tool
   ↓
Tool executes
   ↓
Agent answers
```

The source breaks rigorous evaluation into a sequence beginning with ordinary software tests and ending with operational measurements.

The exact step labels matter less than the layered idea:

```text
tool correctness
→ golden expectation
→ trajectory
→ final answer
→ operational quality
```

---

## 4. Start with ordinary tool unit tests

Evaluation does not begin with the LLM.

If a tool is broken, the agent cannot compensate reliably.

Example:

```python
calculate_area(radius=5)
```

should return the expected deterministic result before the tool is ever given to an agent.

Unit tests should verify:

- function logic,
- parameters,
- output format,
- edge cases,
- error behavior.

This gives you confidence that failures later are actually agent failures rather than basic software bugs.

---

## 5. The golden dataset

A normal chatbot evaluation record might contain:

```text
input
expected output
```

An agent's golden record should capture more.

Example structure:

```json
{
  "user_input": "What is the area of a circle with radius 5?",
  "expected_tool": "calculate_area",
  "expected_parameters": {"radius": 5},
  "expected_tool_response": 78.54,
  "expected_final_response": "..."
}
```

This becomes the ground truth for the entire execution path.

### Why this matters

You can now distinguish:

```text
tool-selection error
parameter error
tool failure
grounding error
generation error
```

instead of treating every failure as "the model gave a bad answer."

[[IMAGE_NEEDED: Anatomy of an agent golden record | User input -> expected tool -> expected parameters -> simulated/raw tool result -> expected final response | Learner should see that agent evaluation includes the execution path]]

---

## 6. Trajectory evaluation

Trajectory evaluation asks:

> Did the agent take the right actions on the way to the answer?

The source emphasizes several metrics.

### Successful tool selection

Did it choose the correct tool?

### Successful parameters

Did it extract and format parameters correctly?

### Successful no-tool selection

Did it avoid unnecessary tools when a normal response was enough?

### Successful clarification

Did it ask for missing information instead of hallucinating it?

### Consistency

Does the same input lead to stable behavior across repeated runs?

These metrics tell you *where* autonomy is failing.

---

## 7. "No tool" is also a correct decision

Suppose the user says:

```text
"Hello."
```

A tool call would be unnecessary.

Therefore, evaluation must include negative expectations:

```text
expected_tool = none
```

This prevents an agent from developing a habit of using tools merely because they exist.

The same principle applies when the user has not supplied enough information.

Sometimes the correct next action is:

```text
ask a question
```

not:

```text
guess an argument
```

---

## 8. Evaluate clarification behavior

User:

```text
"What is the area?"
```

Required parameter:

```text
radius
```

A strong agent should recognize the missing value and request clarification.

A weak one may:

- invent a radius,
- call the tool with invalid arguments,
- produce a confident fabricated answer.

### Evaluation target

Your dataset should explicitly represent cases where the expected behavior is:

```text
do not call tool yet
ask for missing information
```

---

## 9. Evaluate the final answer after the trajectory

After the tool path is graded, evaluate the final response.

Useful approaches in the source include:

- semantic similarity,
- task-specific metrics,
- LLM-as-a-judge/Autorater.

The point is to check whether the final answer:

```text
matches intended meaning
uses the tool result
stays grounded
meets quality expectations
```

---

## 10. Autoraters

An Autorater is another model/agent used as an evaluator.

Instead of exact string matching, it can judge dimensions such as:

```text
helpfulness
tone
pedagogical value
grounding
factuality
```

Autoraters are useful when multiple valid outputs exist.

They should be given:

- explicit criteria,
- clear scoring instructions,
- evaluation examples where appropriate.

---

## 11. Adaptive Rubrics

A fixed rubric applies the same criteria everywhere.

An Adaptive Rubric changes emphasis based on the task.

Example:

### Code-generation request

Weight:

```text
correctness
efficiency
executability
```

### Creative explanation request

Weight:

```text
engagement
clarity
tone
```

The source presents adaptive criteria as a way to keep evaluation meaningful across very different agent intents.

---

## 12. Evaluate grounding against tool results

Suppose the calculator returned:

```text
78.54
```

The final answer should use that value.

An agent that ignores the tool and guesses has failed, even if the guessed answer sounds plausible.

A grounding metric therefore asks:

```text
How much of the final response is supported by the tool/context actually retrieved?
```

This is essential for agents whose value comes from external capabilities.

---

## 13. Operational metrics are part of quality

A correct agent can still be unusable.

Track:

### Cost

Input/output tokens and total interaction cost.

### Latency

How long the user waits.

### Runtime/context payload

How much data tools return into the agent runtime.

Example failure:

```text
database tool returns one billion rows
```

just to calculate a simple average.

That can overwhelm:

- context window,
- container memory,
- network,
- latency budget.

### Rule

> Tool output size is also an operational metric.

{{exercise:M01.L10.EX01}}

---

## 14. Multi-turn evaluation adds state and tool chains

Real users do not stop after one turn.

A multi-turn session may involve:

```text
question
tool
follow-up
memory update
second tool
clarification
third tool
final answer
```

The evaluation dataset must evolve accordingly.

---

## 15. Represent an expected tool chain

Example user goal:

```text
"I want to improve my geometry grade.
What should I focus on?"
```

Expected chain:

```text
get_student_grades
      ↓
search_curriculum
      ↓
generate_study_plan
```

The golden record now needs:

```text
expected_trajectory = [
  step 1,
  step 2,
  step 3
]
```

Each step should include:

- tool name,
- expected parameters,
- simulated/expected response.

[[IMAGE_NEEDED: Multi-turn expected trajectory | User goal -> Tool 1 grades -> Tool 2 curriculum -> Tool 3 study plan -> final response, with golden expected trajectory below | Learner should see the difference between a single expected tool and a chain]]

---

## 16. Evaluate trajectory efficiency

Suppose the golden path needs:

```text
3 tool calls
```

but the agent routinely uses:

```text
7 tool calls
```

before succeeding.

It may be functionally correct but operationally inefficient.

Useful metrics:

```text
average steps
unnecessary tool calls
failure before max-step limit
loop/circuit-breaker rate
```

A maximum-step guard prevents agents from looping forever.

---

## 17. Evaluate short-term memory

Multi-turn agents depend on current-session memory.

Evaluate:

### Topic relevance

Is stored state related to the actual conversation?

### Topic adherence

Does the agent stay on the user's ongoing subject?

Example:

If the student spends the session on algebra, memory should not become dominated by unrelated historical facts.

The source suggests using evaluators to inspect short-term memory at the end of a session.

---

## 18. Evaluate long-term memory summarization

Persistent agents do not save every raw transcript blindly.

They may summarize a session into useful memory.

Example profile update:

```text
mastered: right triangles
weakness: area formulas
preference: visual real-world examples
```

Evaluation question:

> Did the memory summary accurately capture the important information?

Compare generated memory against a golden profile.

A poor summary can make future personalization worse than no memory at all.

---

## 19. Evaluate long-term memory retrieval

When the user returns later, the system must retrieve the right history.

This is a retrieval problem.

Therefore, long-term memory evaluation includes RAG-style questions:

```text
Was the right memory retrieved?
Was relevant history ranked well?
Was irrelevant history excluded?
```

The source mentions specialized retrieval evaluation tools as examples.

Treat exact tool names and scores as source-specific and time-sensitive.

---

## 20. Memory quality includes latency

The correct memory is not enough if retrieving it takes too long.

A user returning to a live tutor expects context quickly.

So evaluate:

```text
retrieval accuracy
retrieval latency
payload size
```

Memory should improve responsiveness, not freeze the conversation.

---

## 21. Simulators solve the evaluation-data bottleneck

Large evaluation programs need many scenarios.

Humans cannot manually write every:

- single-turn case,
- edge case,
- multi-turn session,
- long-term return scenario.

The source introduces a Simulator Agent.

A Simulator impersonates a user.

It interacts with the target agent and records the entire interaction.

[[IMAGE_NEEDED: Simulator architecture | Scenario/persona/turn limit/history pointer -> Simulator Agent -> Target Agent -> recorded messages + tool calls + parameters -> evaluation dataset | Learner should see how synthetic interaction data is generated]]

---

## 22. Configure Simulator behavior

The source describes inputs such as:

### Target Agent

Which agent is being tested.

### Scenario

What goal/problem to enact.

### Context/persona

Example:

```text
10th-grade student
low geometry grade
prefers visual learning
```

### Turn limit

Single-turn or bounded multi-turn.

### Optional historical pointer

Used to test continuity across previous sessions.

These inputs let teams produce systematic variants rather than random chats.

---

## 23. The Simulator is an actor, not the judge

This distinction is critical.

The Simulator:

```text
acts out the scenario
records the interaction
```

It does not decide whether the target agent passed.

Evaluation is performed later by:

- metrics,
- Autoraters,
- human reviewers,
- other evaluation systems.

Separating actor and judge reduces conceptual confusion.

---

## 24. Four evaluation categories

The source consolidates many metrics into four groups.

### 1. Generation quality and grounding

Examples:

- semantic similarity,
- factuality,
- safety,
- grounded information.

### 2. Trajectory and execution

Examples:

- tool accuracy,
- parameter accuracy,
- no-tool behavior,
- clarification behavior,
- step efficiency.

### 3. Memory and context

Examples:

- topic relevance,
- topic adherence,
- summarization accuracy,
- retrieval performance.

### 4. Operational health

Examples:

- token cost,
- time to first token,
- total latency,
- CPU/memory,
- runtime payload size.

[[IMAGE_NEEDED: Four-quadrant agent evaluation scorecard | Generation & Grounding, Trajectory & Execution, Memory & Context, Operational Health | Learner should use this as a complete AgentOps evaluation map]]

---

## 25. Match failures to the correct optimization lever

Metrics are valuable only if they guide action.

### Generation/grounding failure

Improve:

```text
system instructions
few-shot examples
prompt design
```

### Memory/context failure

Improve:

```text
context engineering
retrieval
memory summarization
```

### Trajectory failure

Improve:

```text
tool definitions
tool descriptions
parameter schemas
routing rules
```

### Cost/latency failure

Revisit:

```text
model choice
tool payload size
runtime architecture
```

The source emphasizes continuous optimization rather than one-time tuning.

---

## 26. Integrate evaluation into the development lifecycle

Evaluation should not remain on a developer's laptop.

A mature flow is:

```text
code/prompt/tool change
   ↓
commit
   ↓
deploy candidate to staging
   ↓
run Simulators
   ↓
run Autoraters/metrics
   ↓
scorecard
   ↓
pass -> promote
fail -> block
```

This turns evaluation into a deployment gate.

---

## 27. Live voice changes the evaluation problem

A text agent may tolerate several seconds of delay.

A live voice agent cannot.

Users also:

- pause,
- stutter,
- use filler words,
- change direction,
- talk over the assistant,
- express emotion acoustically.

Therefore, voice evaluation must test:

```text
what is said
+
how it is said
+
when it is said
+
how interruption is handled
```

---

## 28. Transcript-based voice evaluation

The simplest approach converts voice interactions into text.

Then reuse the classic evaluation stack.

You can still evaluate:

- tool trajectory,
- factuality,
- semantic quality,
- safety,
- grounding.

### Strength

It lets teams reuse existing text evaluation infrastructure.

### Limitation

It evaluates the "brain" of the voice agent, not the complete human experience.

---

## 29. What transcripts lose

The source emphasizes three dimensions.

### Emotion and sentiment

Sarcasm, frustration, confidence, tension.

### Pacing and hesitation

Pauses and uncertainty.

### Conversational dynamics

Overlap, filler sounds, timing, backchanneling.

A transcript can preserve words while destroying the signal carried by the voice.

---

## 30. Multimodal-native evaluation

To evaluate voice as voice, evaluate the raw audio.

A multimodal Autorater can receive the actual recording.

Rubrics can ask:

```text
Did the student sound confused?
Did the tutor sound encouraging?
Did the response match the user's pace?
Was the turn timing natural?
```

This moves evaluation from text-only meaning into acoustic interaction quality.

---

## 31. Give the Simulator a voice

Text Simulators can be extended with TTS.

The Simulator decides what to say.

The TTS system generates audio.

The source describes varying:

- speaker characteristics,
- emotion,
- pitch,
- sighs/hesitation.

This makes automated live-audio scenarios possible without hiring thousands of human voice actors.

---

## 32. Test background noise

Real users speak from:

- cafés,
- buses,
- offices,
- noisy homes.

The Simulator can inject controlled noise.

Then evaluate:

```text
wake/listen reliability
false activation
speech understanding
quality degradation
```

The goal is to discover the system's breaking point before real users do.

Exact acceptable-noise percentages in the source are illustrative, not universal targets.

---

## 33. Evaluate interruption and barge-in

Real conversation includes interruption.

The source suggests deliberately programming the Simulator to interrupt some interactions.

A good live agent should not collapse when the user says:

```text
"Wait—what is a hypotenuse?"
```

mid-explanation.

---

## 34. Three interruption metrics

### Barge-in latency

How quickly does the agent stop speaking?

### Context switching

Does it answer the new interruption correctly?

### Context retention

After answering the interruption, does it remember the original goal?

These three metrics measure whether interruption is graceful rather than destructive.

[[IMAGE_NEEDED: Interruption evaluation timeline | Agent speaking -> Simulator barges in -> measure stop latency -> agent answers new question -> agent returns to original topic | Learner should understand latency, switching, and retention as separate scores]]

{{exercise:M01.L10.EX02}}

---

## 35. Monitoring as real-time evaluation

The source frames production monitoring as:

```text
evaluation applied to live traffic
```

Metrics and rubrics developed in staging can become:

- alerts,
- dashboards,
- guardrails,
- operational thresholds.

This creates a continuous connection between:

```text
what was tested
```

and:

```text
what is enforced/observed in production
```

---

## 36. Production failures should improve the golden dataset

A user's negative rating alone is weak data.

It becomes useful when joined with:

```text
interaction logs
short-term memory
tool trajectory
runtime metadata
```

Then the system can create a new actionable evaluation record.

That new example can drive:

- Simulator scenarios,
- regression tests,
- new rubric cases.

This creates an operational flywheel:

```text
production issue
→ structured eval case
→ improved testing
→ fix
→ redeploy
```

---

## 37. When should the full evaluation suite run?

The source highlights triggers such as:

```text
monitoring alert
new evaluation data
new agent behavior
new tool
foundation-model upgrade
latency/cost optimization sprint
```

Evaluation is not only a pre-deployment event.

It should respond to system change.

---

## 38. Distribute evaluation across environments

### Development

Humans iterate quickly:

- prompts,
- schemas,
- logic,
- local tests.

### Staging

Run evaluation at scale:

- Simulators,
- Autoraters,
- large scenario sets,
- live-audio testing.

### Human validation

The source recommends retaining a small human-reviewed subset to verify automated judges.

Treat any exact percentage in the source as illustrative rather than universal.

### Production

Capture real interactions and feedback to improve future evaluation.

---

## 39. From evaluating the brain to governing the hands

Chapter 16 tests whether the agent reasons and acts correctly.

Chapter 17 asks:

> What happens when the enterprise has hundreds or thousands of possible tools?

If the model is the brain, tools are the hands.

Good reasoning is not enough if:

- tools are duplicated,
- tools cannot be discovered,
- wrong versions are used,
- insecure tools are exposed,
- too many tools confuse the agent.

Tool governance becomes the next AgentOps problem.

---

## 40. Three broad enterprise tool categories

The source groups tools into:

```text
Code Functions
Local VPC REST APIs
Public REST APIs
```

This is a practical categorization based on implementation and access.

---

## 41. Code Functions

Code functions run close to the agent.

Advantages:

```text
very low latency
easy implementation
full ownership
```

Weakness:

```text
poor shareability
```

If teams copy the same utility into many repositories, versioning becomes difficult.

Ways to improve reuse include:

- shared libraries,
- containerized service deployment.

---

## 42. Local VPC REST APIs

Internal APIs expose organization-owned services over a network boundary.

Advantages:

- better shareability,
- centralized authentication,
- standard monitoring,
- clear service ownership.

Trade-off:

```text
more infrastructure
network latency
```

They are often a good enterprise interface for internal capabilities.

---

## 43. Public REST APIs

External providers supply capabilities such as:

- weather,
- stock data,
- SaaS actions.

The organization does not control them.

Important concerns:

```text
authentication
network access
provider reliability
provider versioning
security
```

They should be treated as external black boxes with explicit operational controls.

---

## 44. Compare tool categories

| Dimension | Code Function | Internal API | Public API |
|---|---|---|---|
| Latency | very low | medium | variable/high |
| Ownership | full | full organization control | external |
| Shareability | weaker | strong internally | broad with access |
| Monitoring | custom | easier with API tooling | provider-limited |
| Versioning | repository | repository/service | provider-dependent |
| Security | agent environment | VPC/API policy | external credentials/network |

No category is universally best.

The architecture should match the tool's operational context.

[[IMAGE_NEEDED: Three enterprise tool categories | Code Functions, Internal VPC APIs, Public APIs with trade-offs for latency, shareability, ownership, security, and monitoring | Learner should understand why registries must manage heterogeneous tools]]

---

## 45. Tool Registry as the single source of truth

Without a registry, teams may repeatedly build:

```text
get_customer_profile
```

without knowing another version already exists.

A Tool Registry is a centralized catalog describing available capabilities.

It supports:

```text
discover
reuse
govern
version
secure
audit
evaluate
```

The source compares it to a restaurant menu:

the agent/developer sees what exists without entering every "kitchen."

---

## 46. Core Tool Registry benefits

### Reusability

Find and reuse existing capabilities.

### Visibility/shareability

Authorized teams can discover what exists.

### Security/accessibility

Control which agents/users can call a tool.

### Standardization

Require consistent metadata and contracts.

### Robustness

Store evaluation/testing/version lineage.

### Auditability

Track usage, access, dependencies, and lifecycle.

This turns a collection of tools into a governed ecosystem.

---

## 47. What should a registry know?

At minimum, registry metadata may include:

```text
name
description
inputs
outputs
location
invocation method
owner
version
evaluation results
access rules
documentation
lineage
```

Search/discovery lets developers find tools by:

- keyword,
- category,
- capability.

Access control limits which agents can use them.

---

## 48. A registry is more than documentation

A strong registry can answer:

```text
Who owns this tool?
Which version is approved?
Which agents use it?
What data can it access?
How well did it test?
Can it be deprecated?
```

This supports:

- compliance,
- debugging,
- dependency analysis,
- cleanup.

A registry should help identify both:

```text
critical heavily used tools
```

and:

```text
unused tools ready for retirement
```

---

## 49. Generalist vs Specialist tool access

Once thousands of tools exist, how many should one agent see?

### Generalist

Give the agent the full registry.

Pros:

```text
flexibility
broad capability
```

Risks:

```text
larger search space
confusing similar tools
less predictable selection
harder testing
larger attack surface
```

### Specialist

Give the agent a curated Tool List.

Benefits:

```text
faster selection
better predictability
simpler testing
reduced security exposure
```

Cost:

```text
more design/coordination
```

[[IMAGE_NEEDED: Generalist vs Specialist agent toolbox | Generalist faces a huge toolbox with many similar tools; Specialist receives a small curated set matching its job | Learner should associate narrower search space with predictability and security]]

---

## 50. Dynamic Tool Search as the middle ground

The source points to an emerging pattern:

```text
large registry
   ↓
search for relevant tools
   ↓
temporary small candidate set
   ↓
agent chooses
```

This preserves broad potential capability without showing every tool to the model at once.

Conceptually, it creates a temporary specialist at runtime.

### Core principle

> Reliable reasoning eventually requires limiting the tool search space—statically or dynamically.

---

## 51. Tools can be distributed while governance is centralized

Enterprise tools may live in different places.

### Data tools

Near data lakes/meshes/databases.

### APIs and agents as tools

In application/service environments.

### Code artifacts

In central repositories/artifact systems.

Physical deployment does not need to be centralized.

The *registry view* should be.

---

## 52. Centralized Tool Registry in the governance layer

The source places the registry in a central governance/"AI Control Tower" environment.

Why?

### Unified discovery

One catalog across deployment environments.

### Consistent metadata

One description standard.

### Centralized governance

Registration/access/audit policies.

### Auditability and observability

Usage, versions, access history.

This separation allows teams to deploy tools near their data while still governing them centrally.

---

## 53. Standardize tool repositories

The source proposes a consistent repository layout.

Conceptually:

```text
tools/
├── shared_libraries/
├── api_tools/
│   └── tool_a/
│       ├── test/
│       ├── implementation
│       └── deployment config
├── code_tools/
│   └── tool_b/
│       └── test/
└── data_tools/
    └── tool_c/
        └── test/
```

Exact directory names are only one example.

The durable principle is:

> Standard structure enables automation.

---

## 54. Each tool should bring its own tests

The tool creator understands its domain logic best.

Therefore each tool should include unit tests before registration.

Possible test assets:

```text
input fixtures
expected outputs
error cases
security checks
```

This connects Chapter 17 directly back to Chapter 16.

A Tool Registry should not contain only descriptions.

It should contain quality evidence.

---

## 55. Automate registration after tests pass

A standardized repository enables a CI/CD pipeline to:

```text
scan tool folders
   ↓
run tests
   ↓
validate metadata
   ↓
build/deploy if required
   ↓
register approved tool
```

This reduces manual errors.

It also makes registration part of governance rather than an informal developer action.

{{exercise:M01.L10.EX03}}

---

## 56. API-first standardization

The source proposes converting heterogeneous tools into service interfaces.

Why?

An API gives:

```text
standard access
shareability
auth
monitoring
rate limiting
central governance
```

The registry can then focus on a consistent service contract.

---

## 57. Code tools to APIs

A local function can be packaged into a container/service.

Conceptually:

```text
Python function
   ↓
container/service
   ↓
API endpoint
```

Benefits:

- reuse across agents,
- independent versioning,
- standardized monitoring,
- deployment rollback.

This trades local simplicity for enterprise shareability.

---

## 58. Data tools to APIs

Direct database tools often need an API layer.

That layer can enforce:

```text
authentication
authorization
data access policy
auditing
```

This is especially important when different agents have different permissions.

The API boundary can unify data governance with tool governance.

---

## 59. Standardize further with MCP

API-first reduces heterogeneity.

MCP can standardize the agent-facing capability protocol further.

Instead of every agent needing custom endpoint schemas and discovery logic, an MCP Server can expose standardized:

```text
Tools
Resources/context
Prompts
```

and support standardized discovery/calling.

The source recommends thinking of:

```text
service deployment
+
MCP communication
```

as complementary enterprise patterns.

---

## 60. Managed registry examples are provider-specific

The source gives cloud-provider managed registry examples.

Those examples may change over time.

The durable ideas are:

```text
import standardized API definitions
centralize authentication
manage execution metadata
expose tools safely
reduce glue code
```

When implementing, verify current platform capabilities rather than memorizing one product name or exact feature.

---

## 61. Tool governance follows organizational structure

The source describes three organizational models.

```text
Functional / Decentralized
Centralized
Federated / Hybrid
```

Each balances:

```text
team autonomy
standardization
governance
speed
reuse
```

---

## 62. Functional / decentralized tool management

Each team:

- creates tools,
- maintains tools,
- may maintain its own local registry.

Advantages:

```text
speed
flexibility
local ownership
```

Risks:

```text
duplication
silos
inconsistent standards
weak enterprise visibility
```

This can work at small scale but becomes challenging as reuse needs grow.

---

## 63. Centralized tool management

A central platform/CoE team manages:

- standards,
- development,
- registration,
- global registry.

Advantages:

```text
strong consistency
easy governance
high reuse
```

Risks:

```text
central bottleneck
slower team velocity
platform-team overload
```

---

## 64. Federated tool management

Teams can build locally.

A central governance group defines common standards and promotes strong reusable tools into the shared registry.

This balances:

```text
local innovation
+
central quality/governance
```

The source presents this as particularly relevant for large enterprises with distributed teams.

[[IMAGE_NEEDED: Three tool-governance organization models | Decentralized team-local registries, Centralized global team/registry, Federated local registries with promoted tools into global catalog | Learner should compare autonomy, speed, and governance]]

---

## 65. Choose the governance model deliberately

Consider:

```text
organization size
number of teams
number of tools
required standardization
development velocity
team autonomy
```

There is no universal structure.

The governance design should match the organization.

---

## 66. Evaluation and Tool Registry form a feedback loop

This is why Chapters 16 and 17 belong together.

### Evaluation discovers:

```text
tool selection mistakes
parameter mistakes
tool latency
oversized outputs
tool failures
weak descriptions
poor consistency
```

### Registry governance can respond:

```text
improve descriptions
deprecate bad versions
publish evaluation scores
restrict access
curate specialist tool lists
promote safer versions
```

### Registry changes trigger evaluation

A new tool or new version should cause:

```text
regression tests
trajectory evaluation
latency/cost checks
```

The two systems reinforce each other.

[[IMAGE_NEEDED: Evaluation–Registry feedback loop | Agent evaluation finds tool problems -> Tool Registry metadata/version/access changes -> agent receives improved curated tools -> re-evaluation -> production monitoring -> new evidence | Learner should see quality and governance as one continuous AgentOps cycle]]

---

## 67. Production checklist

### Evaluation foundation

- tool unit tests,
- golden records,
- correct tool/no-tool behavior,
- parameter validation,
- clarification cases.

### Multi-turn

- expected trajectories,
- step efficiency,
- circuit breakers,
- short-term memory,
- long-term summary/retrieval.

### Live voice

- transcript checks,
- native audio checks,
- emotion/tone,
- noise,
- barge-in latency,
- context switching,
- context retention.

### Operational

- token cost,
- TTFT,
- total latency,
- payload size,
- CPU/memory.

### Continuous improvement

- staging evaluation,
- production monitoring,
- human validation,
- user-feedback conversion to new golden cases.

### Tool governance

- registry metadata,
- owner/version,
- evaluation evidence,
- access control,
- lineage,
- discovery.

### Tool assignment

- curated Tool Lists,
- dynamic Tool Search where useful,
- least privilege.

### Registration lifecycle

- standardized repo,
- unit tests,
- CI/CD,
- automated registration/deprecation.

### Organization

- explicit decentralized/centralized/federated model.

{{exercise:M01.L10.EX04}}

---

## 68. Source-specific details to re-check

These are Early Release chapters.

Treat the following as source examples rather than timeless constants:

- exact simulator interruption percentages,
- exact human-review percentages,
- exact noise thresholds,
- named evaluation frameworks,
- specific cloud-provider registry products,
- specific API gateway/product names,
- exact repository layout,
- current Tool Search implementations,
- current managed MCP tooling.

The durable principles are:

```text
evaluate tools before agents
grade trajectories
evaluate memory
simulate realistic interactions
test raw audio
measure interruption behavior
turn production failures into regression data
centralize tool discovery/governance
curate the agent's tool search space
automate registration
standardize service interfaces
align governance with organization structure
```

---

## 69. Complete mental model

Start with one agent.

Evaluation asks:

```text
Did the tool work?
Did the agent choose it?
Were arguments correct?
Was the final answer grounded?
```

Multi-turn evaluation adds:

```text
tool chains
step efficiency
short-term memory
long-term memory
retrieval
```

Live evaluation adds:

```text
audio
emotion
pacing
noise
barge-in
```

Production adds:

```text
monitoring
feedback
continuous regression testing
```

Then tool scale adds a second problem:

```text
Which tools exist?
Which version is safe?
Who owns it?
Who may use it?
Which small subset should this agent see?
```

The Tool Registry solves the governance/discovery problem.

Together:

```text
Evaluation Factory
        ↕
Tool Registry
        ↕
Curated Agent Toolsets
        ↕
Production Monitoring
```

form a continuous AgentOps quality system.

---

## Important misconceptions

### Misconception 1
> "If the final answer is correct, the agent passed."

No. The trajectory may still be wasteful, unsafe, or accidentally correct.

### Misconception 2
> "Tool unit tests are unnecessary because the LLM will handle errors."

No. Broken deterministic tools must be fixed before agent evaluation.

### Misconception 3
> "The correct behavior always includes a tool call."

No. No-tool and clarification behavior must also be evaluated.

### Misconception 4
> "Autoraters eliminate the need for explicit rubrics."

No. They need clear criteria, and adaptive rubrics can make those criteria task-specific.

### Misconception 5
> "A multi-turn golden dataset is just several independent single-turn examples."

No. It must represent expected chains and state dependencies.

### Misconception 6
> "If an agent reaches the right answer in seven calls instead of three, performance is equivalent."

No. Step efficiency is part of trajectory quality.

### Misconception 7
> "Long-term memory evaluation only checks whether something was stored."

No. Evaluate both summarization and later retrieval.

### Misconception 8
> "The Simulator is the evaluator."

No. The Simulator acts; metrics/Autoraters/humans judge.

### Misconception 9
> "A transcript fully represents voice quality."

No. It loses prosody, emotion, hesitation, and conversational dynamics.

### Misconception 10
> "Barge-in testing only measures how fast audio stops."

No. Also test context switching and retention.

### Misconception 11
> "Evaluation ends when the agent is deployed."

No. The source frames monitoring as real-time evaluation and production feedback as future test data.

### Misconception 12
> "All enterprise tools are basically the same."

No. Local code, internal APIs, and public APIs have different operational properties.

### Misconception 13
> "A Tool Registry is just documentation."

No. It supports access, evaluation, versions, lineage, discovery, auditability, and governance.

### Misconception 14
> "A generalist agent should always see every available tool."

No. Large search spaces can reduce predictability, accuracy, and security.

### Misconception 15
> "Specialist agents are the only way to limit tool search space."

No. Dynamic Tool Search can narrow candidates at runtime.

### Misconception 16
> "Centralized governance means every tool must run in one central environment."

No. Tools can be distributed while their registry/governance view is centralized.

### Misconception 17
> "API-first and MCP are mutually exclusive."

No. The source presents service deployment and MCP standardization as complementary.

### Misconception 18
> "Federated governance means no central standards."

No. Local autonomy is combined with common standards and central curation.

---

## Key terminology

| Term | Meaning |
|---|---|
| Golden dataset | Curated expected agent behavior used as evaluation ground truth |
| Golden record | One evaluation case containing input, trajectory, and expected outcome |
| Trajectory evaluation | Grading the agent's action/tool path |
| Tool selection accuracy | Whether the correct tool was chosen |
| Parameter accuracy | Whether tool arguments were extracted/formatted correctly |
| No-tool success | Correctly choosing not to invoke a tool |
| Clarification success | Asking for missing information rather than guessing |
| Autorater | Model/agent used as an evaluator |
| Adaptive Rubric | Evaluation criteria that adapt to the task |
| Grounding | Degree to which output is supported by actual tool/context data |
| Circuit breaker | Maximum-step/control rule preventing endless agent loops |
| Short-term memory evaluation | Testing session topic/context retention |
| Long-term memory evaluation | Testing persistent summarization and retrieval |
| Simulator Agent | Agent that impersonates users to generate evaluation interactions |
| Operational health | Cost, latency, compute/memory, payload-size metrics |
| Transcript-based evaluation | Voice evaluation reduced to textual transcripts |
| Multimodal-native evaluation | Direct evaluation of raw audio/media |
| Barge-in | User interrupting the speaking agent |
| Barge-in latency | Delay before agent stops speaking after interruption |
| Tool Registry | Central governed catalog of available tools |
| Tool List | Curated subset of registry tools assigned to an agent |
| Code Function | Local in-process tool |
| VPC REST API | Organization-controlled network service |
| Public REST API | External third-party capability |
| Tool Search | Runtime search that selects relevant tools from a larger catalog |
| Tool metadata | Name, description, inputs, outputs, owner, version, quality, location |
| Tool lineage | History of versions and changes |
| API-first | Standardizing tool access through service APIs |
| Federated governance | Local tool development under shared enterprise standards and global curation |

---

## Self-check

1. Why is evaluating a live agent more complex than testing deterministic software?
2. Why should evaluation begin with tool unit tests?
3. What fields belong in a single-turn golden record?
4. What is trajectory evaluation?
5. Why must no-tool behavior be tested?
6. What should the agent do when required arguments are missing?
7. What is an Autorater?
8. What is an Adaptive Rubric?
9. What does grounding evaluation check?
10. Which operational metrics belong in agent evaluation?
11. Why can oversized tool responses be an evaluation failure?
12. How does a multi-turn golden trajectory differ from a single-turn record?
13. Why measure average number of steps?
14. What does a circuit breaker protect against?
15. How do you evaluate short-term memory?
16. What are the two major parts of long-term-memory evaluation?
17. Why is memory retrieval a RAG problem?
18. What is a Simulator Agent?
19. Why is the Simulator an actor rather than a judge?
20. What are the four main evaluation categories?
21. Which optimization lever should you use for trajectory failure?
22. How does evaluation fit into CI/CD?
23. What can transcript-based voice evaluation reuse?
24. What important information does a transcript remove?
25. How can TTS-enabled Simulators improve live testing?
26. Why inject background noise?
27. What are the three interruption metrics?
28. What does "monitoring is real-time evaluation" mean?
29. When should the full evaluation suite be triggered?
30. How can negative user feedback become a useful golden case?
31. What are the three tool categories in the source?
32. What is the main advantage and weakness of code functions?
33. Why are internal APIs easier to share and monitor?
34. What extra risks come with public APIs?
35. What problem does the Tool Registry solve?
36. What metadata should a registry store?
37. Why does registry lineage matter?
38. What are the trade-offs of a Generalist agent?
39. What are the benefits of a curated Specialist Tool List?
40. What is dynamic Tool Search?
41. Why can tools be distributed while governance is centralized?
42. What does the central governance/Control Tower registry provide?
43. Why standardize repository structure?
44. Why should tools include their own tests?
45. How can CI/CD automate tool registration?
46. What is the API-first strategy?
47. Why might code tools be converted into APIs?
48. Why might data tools need an API layer?
49. How does MCP complement API-first deployment?
50. What are the decentralized, centralized, and federated governance models?
51. What factors determine which organizational model fits?
52. How should Chapter 16 evaluation results influence Chapter 17 registry metadata and policies?
53. Why should a new tool or tool version trigger agent reevaluation?
54. Which source-specific examples should be re-verified before implementation?

---

## Retain this idea

**AgentOps needs both a quality factory and a governed toolbox. The evaluation factory proves that an agent chooses the right tools, uses them correctly, remembers the right context, responds efficiently, and behaves naturally under real-time voice conditions. The Tool Registry ensures that those tools are discoverable, tested, versioned, governed, secure, and assigned to agents in a manageable search space. The two systems form one loop: evaluation improves tools and registry policy; registry changes trigger new evaluation; production monitoring supplies the next generation of golden cases.**
""".strip(),

        "sections": [
            {"id": "why-evaluation", "title": "Why Live-Agent Evaluation Is Different", "order": 1},
            {"id": "baseline-first", "title": "Voice Quality Cannot Rescue Bad Reasoning", "order": 2},
            {"id": "single-turn", "title": "Single-Turn Evaluation as the Foundation", "order": 3},
            {"id": "unit-tests", "title": "Start with Ordinary Tool Unit Tests", "order": 4},
            {"id": "golden-dataset", "title": "The Golden Dataset", "order": 5},
            {"id": "trajectory", "title": "Trajectory Evaluation", "order": 6},
            {"id": "no-tool", "title": "No Tool Is Also a Correct Decision", "order": 7},
            {"id": "clarification", "title": "Evaluate Clarification Behavior", "order": 8},
            {"id": "final-response", "title": "Evaluate the Final Answer After the Trajectory", "order": 9},
            {"id": "autorater", "title": "Autoraters", "order": 10},
            {"id": "adaptive-rubric", "title": "Adaptive Rubrics", "order": 11},
            {"id": "grounding", "title": "Evaluate Grounding Against Tool Results", "order": 12},
            {"id": "operational-metrics", "title": "Operational Metrics Are Part of Quality", "order": 13},
            {"id": "multi-turn", "title": "Multi-Turn Evaluation Adds State and Tool Chains", "order": 14},
            {"id": "tool-chain", "title": "Represent an Expected Tool Chain", "order": 15},
            {"id": "trajectory-efficiency", "title": "Evaluate Trajectory Efficiency", "order": 16},
            {"id": "short-term-memory", "title": "Evaluate Short-Term Memory", "order": 17},
            {"id": "long-term-memory", "title": "Evaluate Long-Term Memory Summarization", "order": 18},
            {"id": "memory-retrieval", "title": "Evaluate Long-Term Memory Retrieval", "order": 19},
            {"id": "memory-latency", "title": "Memory Quality Includes Latency", "order": 20},
            {"id": "simulator", "title": "Simulators Solve the Evaluation-Data Bottleneck", "order": 21},
            {"id": "simulator-config", "title": "Configure Simulator Behavior", "order": 22},
            {"id": "actor-not-judge", "title": "The Simulator Is an Actor, Not the Judge", "order": 23},
            {"id": "taxonomy", "title": "Four Evaluation Categories", "order": 24},
            {"id": "optimization-levers", "title": "Match Failures to the Correct Optimization Lever", "order": 25},
            {"id": "ci-cd", "title": "Integrate Evaluation into the Development Lifecycle", "order": 26},
            {"id": "live-voice", "title": "Live Voice Changes the Evaluation Problem", "order": 27},
            {"id": "transcript-eval", "title": "Transcript-Based Voice Evaluation", "order": 28},
            {"id": "transcript-limits", "title": "What Transcripts Lose", "order": 29},
            {"id": "native-audio", "title": "Multimodal-Native Evaluation", "order": 30},
            {"id": "tts-simulator", "title": "Give the Simulator a Voice", "order": 31},
            {"id": "noise-testing", "title": "Test Background Noise", "order": 32},
            {"id": "barge-in", "title": "Evaluate Interruption and Barge-In", "order": 33},
            {"id": "barge-metrics", "title": "Three Interruption Metrics", "order": 34},
            {"id": "monitoring", "title": "Monitoring as Real-Time Evaluation", "order": 35},
            {"id": "feedback-loop", "title": "Production Failures Should Improve the Golden Dataset", "order": 36},
            {"id": "eval-triggers", "title": "When Should the Full Evaluation Suite Run?", "order": 37},
            {"id": "eval-environments", "title": "Distribute Evaluation Across Environments", "order": 38},
            {"id": "brain-to-hands", "title": "From Evaluating the Brain to Governing the Hands", "order": 39},
            {"id": "tool-landscape", "title": "Three Broad Enterprise Tool Categories", "order": 40},
            {"id": "code-tools", "title": "Code Functions", "order": 41},
            {"id": "vpc-api", "title": "Local VPC REST APIs", "order": 42},
            {"id": "public-api", "title": "Public REST APIs", "order": 43},
            {"id": "tool-comparison", "title": "Compare Tool Categories", "order": 44},
            {"id": "registry", "title": "Tool Registry as the Single Source of Truth", "order": 45},
            {"id": "registry-benefits", "title": "Core Tool Registry Benefits", "order": 46},
            {"id": "registry-fields", "title": "What Should a Registry Know?", "order": 47},
            {"id": "registry-as-governance", "title": "A Registry Is More Than Documentation", "order": 48},
            {"id": "generalist-specialist", "title": "Generalist vs Specialist Tool Access", "order": 49},
            {"id": "tool-search", "title": "Dynamic Tool Search as the Middle Ground", "order": 50},
            {"id": "distributed-tools", "title": "Tools Can Be Distributed While Governance Is Centralized", "order": 51},
            {"id": "control-tower", "title": "Centralized Tool Registry in the Governance Layer", "order": 52},
            {"id": "repo-standard", "title": "Standardize Tool Repositories", "order": 53},
            {"id": "tool-tests", "title": "Each Tool Should Bring Its Own Tests", "order": 54},
            {"id": "auto-registration", "title": "Automate Registration After Tests Pass", "order": 55},
            {"id": "api-first", "title": "API-First Standardization", "order": 56},
            {"id": "code-to-api", "title": "Code Tools to APIs", "order": 57},
            {"id": "data-to-api", "title": "Data Tools to APIs", "order": 58},
            {"id": "mcp-standardization", "title": "Standardize Further with MCP", "order": 59},
            {"id": "managed-registry", "title": "Managed Registry Examples Are Provider-Specific", "order": 60},
            {"id": "org-models", "title": "Tool Governance Follows Organizational Structure", "order": 61},
            {"id": "decentralized", "title": "Functional / Decentralized Tool Management", "order": 62},
            {"id": "centralized", "title": "Centralized Tool Management", "order": 63},
            {"id": "federated", "title": "Federated Tool Management", "order": 64},
            {"id": "choose-org", "title": "Choose the Governance Model Deliberately", "order": 65},
            {"id": "eval-registry-loop", "title": "Evaluation and Tool Registry Form a Feedback Loop", "order": 66},
            {"id": "production-checklist", "title": "Production Checklist", "order": 67},
            {"id": "source-boundaries", "title": "Source-Specific Details to Re-Check", "order": 68},
            {"id": "complete-model", "title": "Complete Mental Model", "order": 69},
        ],
    },

    "exercises": [
        {
            "id": "M01.L10.EX01",
            "title": "Build a Single-Turn Golden Evaluation Record",
            "lesson_code": "M01.L10",
            "section_id": "operational-metrics",
            "placement": "after_section",
            "description": "Create a complete evaluation case for a tool-using agent.",
            "instructions": (
                ('1. Design one golden case for a Weather Assistant.\n'
                 '2. Include user input, expected tool/no-tool choice, expected parameters, simulated tool result, expected final response behavior, grounding check, token/cost target, latency target, and maximum allowed tool-response payload size.\n'
                 '3. Add one missing-information variant where clarification is required.')
            ),
            "expected_output": "Two golden records: normal execution and clarification-required.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["golden-dataset", "trajectory-evaluation", "operational-metrics"],
        },
        {
            "id": "M01.L10.EX02",
            "title": "Design a Live Voice Evaluation Scenario",
            "lesson_code": "M01.L10",
            "section_id": "barge-metrics",
            "placement": "after_section",
            "description": "Create a simulator-driven raw-audio test for a live tutor.",
            "instructions": (
                ('1. Define a Simulator persona and scenario.\n'
                 '2. Add emotional TTS behavior, one noisy environment, and one deliberate barge-in.\n'
                 '3. Define an Adaptive Rubric covering response correctness, tone, pacing, barge-in latency, context switching, and context retention.\n'
                 '4. Explain which criteria require raw audio rather than transcripts.')
            ),
            "expected_output": "A complete multimodal evaluation scenario and rubric.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["simulators", "multimodal-evaluation", "barge-in"],
        },
        {
            "id": "M01.L10.EX03",
            "title": "Design a Tool Registration Pipeline",
            "lesson_code": "M01.L10",
            "section_id": "auto-registration",
            "placement": "after_section",
            "description": "Connect standardized repositories, tests, CI/CD, and the Tool Registry.",
            "instructions": (
                ('1. Design a registration pipeline for a new customer-profile tool.\n'
                 '2. Include repository structure, unit tests, metadata validation, security checks, version assignment, deployment/build step if needed, registry registration, owner/access fields, and rollback/deprecation rules.')
            ),
            "expected_output": "A CI/CD flow from tool source code to governed registry entry.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["tool-registry", "tool-ci-cd", "governance"],
        },
        {
            "id": "M01.L10.EX04",
            "title": "Build an Evaluation–Registry Feedback Loop",
            "lesson_code": "M01.L10",
            "section_id": "production-checklist",
            "placement": "after_section",
            "description": "Use evaluation evidence to improve tool governance and agent tool assignment.",
            "instructions": (
                "Assume an agent repeatedly selects the wrong of two similar CRM tools.\n"
                "1. Define the evaluation evidence you would collect.\n"
                "2. Identify possible registry causes.\n"
                "3. Improve metadata/descriptions/versioning/access as needed.\n"
                "4. Decide whether to create a curated Tool List or dynamic search rule.\n"
                "5. Define regression cases that must pass before redeployment."
            ),
            "expected_output": "A quality-governance remediation plan.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["trajectory-evaluation", "registry-governance", "tool-selection"],
        },
        {
            "id": "M01.L10.EX05",
            "title": "Choose Generalist, Specialist, or Dynamic Tool Search",
            "lesson_code": "M01.L10",
            "section_id": "tool-search",
            "placement": "after_section",
            "description": "Choose a tool assignment strategy for different agents.",
            "instructions": (
                "Choose Generalist, Specialist, or Dynamic Tool Search for:\n"
                "1. Payroll Agent with six sensitive payroll tools.\n"
                "2. Enterprise Concierge that may route across hundreds of capabilities.\n"
                "3. Narrow Tax Calculator.\n"
                "4. Research Agent whose relevant tools depend heavily on domain.\n"
                "For each, discuss performance, predictability, testing, and security."
            ),
            "expected_output": "A four-row tool-access strategy table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["specialist-agents", "dynamic-tool-search", "least-privilege"],
        },
        {
            "id": "M01.L10.EX06",
            "title": "Design a Federated Enterprise Tool Registry",
            "lesson_code": "M01.L10",
            "section_id": "federated",
            "placement": "after_section",
            "description": "Balance team autonomy with enterprise governance.",
            "instructions": (
                ('1. Design a company with three business-unit teams and one central AI Governance team.\n'
                 '2. Define local tool-development responsibilities, common metadata/testing/security standards, the promotion process into the global registry, ownership/version rules, access policy, and the criteria used to reject or deprecate a tool.')
            ),
            "expected_output": "A federated governance operating model.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["federated-governance", "tool-registry", "organizational-design"],
        },
        {
            "id": "M01.L10.EX07",
            "title": "Create a Multi-Turn Evaluation Trajectory",
            "lesson_code": "M01.L10",
            "section_id": "short-term-memory",
            "placement": "after_section",
            "description": "Evaluate tool chains, efficiency, and memory together.",
            "instructions": (
                ('1. Design a three-step Academic Advisor workflow using three tools.\n'
                 '2. Define expected tool order, parameters, simulated responses, max step count, final response, short-term memory topics, and one deliberately irrelevant memory item that the evaluator should reject.')
            ),
            "expected_output": "A multi-turn golden trajectory plus memory-evaluation criteria.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["multi-turn-evaluation", "memory-evaluation", "trajectory-efficiency"],
        },
    ],

    "quiz": {
        "id": "M01.L10.QZ01",
        "title": "Live Agent Evaluation and Tool Governance — Knowledge Check",
        "lesson_code": "M01.L10",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L10.Q01",
                "section_id": "why-evaluation",
                "question": "Why is evaluating a live agent more complex than evaluating a static LLM?",
                "options": [
                    "The live agent has tools, memory, timing, audio, and autonomous execution behavior",
                    "Static LLMs cannot generate text",
                    "Live agents never use models",
                    "Only voice quality matters",
                ],
                "correct": 0,
                "explanation": "Agent evaluation covers a whole execution system rather than only one output.",
            },
            {
                "id": "M01.L10.Q02",
                "section_id": "unit-tests",
                "question": "What should happen before evaluating whether the model selects a tool correctly?",
                "options": [
                    "Unit test the tool itself",
                    "Deploy to production",
                    "Ignore deterministic behavior",
                    "Train a new model",
                ],
                "correct": 0,
                "explanation": "A broken tool invalidates higher-level agent evaluation.",
            },
            {
                "id": "M01.L10.Q03",
                "section_id": "golden-dataset",
                "question": "What should an agent golden record contain beyond input and output?",
                "options": [
                    "Expected tool, parameters, and expected tool result/trajectory",
                    "Only model temperature",
                    "Only UI theme",
                    "Only token count",
                ],
                "correct": 0,
                "explanation": "The path is part of the expected behavior.",
            },
            {
                "id": "M01.L10.Q04",
                "section_id": "trajectory",
                "question": "Which metric checks whether the agent correctly avoided unnecessary tools?",
                "options": [
                    "Successful no-tool selection",
                    "Barge-in latency",
                    "Artifact retention",
                    "Registry lineage",
                ],
                "correct": 0,
                "explanation": "Sometimes the correct action is simply to respond without a tool.",
            },
            {
                "id": "M01.L10.Q05",
                "section_id": "adaptive-rubric",
                "question": "What distinguishes an Adaptive Rubric?",
                "options": [
                    "Its criteria change based on the evaluated task or intent",
                    "It never uses criteria",
                    "It is only for audio",
                    "It always uses exact string matching",
                ],
                "correct": 0,
                "explanation": "The rubric can emphasize different qualities for different tasks.",
            },
            {
                "id": "M01.L10.Q06",
                "section_id": "trajectory-efficiency",
                "question": "Why measure the number of tool steps?",
                "options": [
                    "An agent can reach the right answer inefficiently through unnecessary calls",
                    "More tool calls are always better",
                    "Step count replaces correctness",
                    "It only measures audio latency",
                ],
                "correct": 0,
                "explanation": "Trajectory efficiency is part of agent quality.",
            },
            {
                "id": "M01.L10.Q07",
                "section_id": "long-term-memory",
                "question": "What is one major long-term-memory evaluation target?",
                "options": [
                    "Accuracy of the summarized persistent profile/context",
                    "Only current audio volume",
                    "Only tool version",
                    "Browser rendering speed",
                ],
                "correct": 0,
                "explanation": "Poor persistent summaries can corrupt future personalization.",
            },
            {
                "id": "M01.L10.Q08",
                "section_id": "actor-not-judge",
                "question": "What is the Simulator's role?",
                "options": [
                    "Act out scenarios and record interactions",
                    "Be the final evaluator",
                    "Own the Tool Registry",
                    "Replace all unit tests",
                ],
                "correct": 0,
                "explanation": "Evaluation is performed by metrics, judges, or humans after simulation.",
            },
            {
                "id": "M01.L10.Q09",
                "section_id": "taxonomy",
                "question": "Which category includes tool-selection accuracy and parameter formatting?",
                "options": [
                    "Trajectory and execution",
                    "Memory and context",
                    "Generation only",
                    "UI design",
                ],
                "correct": 0,
                "explanation": "Those metrics evaluate the action path.",
            },
            {
                "id": "M01.L10.Q10",
                "section_id": "transcript-limits",
                "question": "What important information can transcript-only evaluation lose?",
                "options": [
                    "Prosody, emotion, hesitation, and conversational timing",
                    "Tool names",
                    "All text meaning",
                    "JSON schemas only",
                ],
                "correct": 0,
                "explanation": "The acoustic human element is flattened away.",
            },
            {
                "id": "M01.L10.Q11",
                "section_id": "barge-metrics",
                "question": "Which is NOT one of the source's three interruption metrics?",
                "options": [
                    "Tool Registry size",
                    "Barge-in latency",
                    "Context switching",
                    "Context retention",
                ],
                "correct": 0,
                "explanation": "Registry size is unrelated to interruption quality.",
            },
            {
                "id": "M01.L10.Q12",
                "section_id": "monitoring",
                "question": "How does the source relate production monitoring to evaluation?",
                "options": [
                    "Monitoring is real-time evaluation applied to live traffic",
                    "Monitoring replaces evaluation entirely",
                    "They are unrelated",
                    "Evaluation only happens after production incidents",
                ],
                "correct": 0,
                "explanation": "The same quality concepts can be applied before and after deployment.",
            },
            {
                "id": "M01.L10.Q13",
                "section_id": "tool-landscape",
                "question": "Which three broad tool categories does the source use?",
                "options": [
                    "Code functions, local VPC REST APIs, public REST APIs",
                    "Prompts, models, embeddings",
                    "HTML, CSS, JavaScript",
                    "CPU, GPU, TPU",
                ],
                "correct": 0,
                "explanation": "The categories reflect implementation/access style.",
            },
            {
                "id": "M01.L10.Q14",
                "section_id": "registry",
                "question": "What is the Tool Registry's central role?",
                "options": [
                    "Provide a governed source of truth for available tools",
                    "Execute every tool locally",
                    "Train the foundation model",
                    "Replace all APIs",
                ],
                "correct": 0,
                "explanation": "The registry supports discovery, governance, reuse, and lifecycle metadata.",
            },
            {
                "id": "M01.L10.Q15",
                "section_id": "generalist-specialist",
                "question": "What is a major benefit of giving a Specialist a curated Tool List?",
                "options": [
                    "Smaller search space and more predictable tool selection",
                    "More unrelated tools",
                    "No need for testing",
                    "Unlimited privileges",
                ],
                "correct": 0,
                "explanation": "A smaller toolset can improve performance, predictability, testing, and security.",
            },
            {
                "id": "M01.L10.Q16",
                "section_id": "tool-search",
                "question": "What is dynamic Tool Search trying to achieve?",
                "options": [
                    "Find a small relevant subset from a much larger registry at runtime",
                    "Delete the registry",
                    "Give every tool to every prompt",
                    "Prevent specialist agents",
                ],
                "correct": 0,
                "explanation": "It narrows the search space dynamically.",
            },
            {
                "id": "M01.L10.Q17",
                "section_id": "control-tower",
                "question": "Why centralize registry governance if tools are deployed in many environments?",
                "options": [
                    "To provide unified discovery, metadata, policy, and auditability",
                    "To force every tool onto one server",
                    "To eliminate local ownership",
                    "To prevent version control",
                ],
                "correct": 0,
                "explanation": "Registry centralization does not require deployment centralization.",
            },
            {
                "id": "M01.L10.Q18",
                "section_id": "tool-tests",
                "question": "Why should each tool include its own tests?",
                "options": [
                    "The tool should prove deterministic behavior before agents depend on it",
                    "Tools cannot be evaluated after registration",
                    "Tests replace registry metadata",
                    "Tests make authentication unnecessary",
                ],
                "correct": 0,
                "explanation": "This connects software-quality evidence to tool governance.",
            },
            {
                "id": "M01.L10.Q19",
                "section_id": "api-first",
                "question": "What is a main benefit of API-first tool standardization?",
                "options": [
                    "Consistent access, governance, monitoring, and reuse across implementations",
                    "Every tool becomes local",
                    "No authentication is required",
                    "Agents must understand internal implementation",
                ],
                "correct": 0,
                "explanation": "Service boundaries normalize heterogeneous tool implementations.",
            },
            {
                "id": "M01.L10.Q20",
                "section_id": "mcp-standardization",
                "question": "How does MCP complement API-first design in the source?",
                "options": [
                    "It standardizes agent-facing discovery and invocation of capabilities",
                    "It prevents service deployment",
                    "It requires every tool to be a Python function",
                    "It eliminates governance",
                ],
                "correct": 0,
                "explanation": "MCP provides a standard protocol over capability services.",
            },
            {
                "id": "M01.L10.Q21",
                "section_id": "federated",
                "question": "What defines federated tool governance?",
                "options": [
                    "Teams develop locally under shared standards while central governance curates reusable tools",
                    "No standards exist",
                    "One central team writes every tool",
                    "Every team is isolated forever",
                ],
                "correct": 0,
                "explanation": "Federation balances autonomy and enterprise reuse/governance.",
            },
            {
                "id": "M01.L10.Q22",
                "section_id": "eval-registry-loop",
                "question": "Why should Tool Registry changes trigger reevaluation?",
                "options": [
                    "New descriptions, versions, or toolsets can change agent selection and execution behavior",
                    "Registry changes never affect agents",
                    "Only audio can affect evaluation",
                    "Evaluation is unrelated to tools",
                ],
                "correct": 0,
                "explanation": "Tool availability and metadata directly influence trajectories.",
            },
            {
                "id": "M01.L10.Q23",
                "section_id": "source-boundaries",
                "question": "How should exact noise percentages, product names, and tool-search implementations in the source be treated?",
                "options": [
                    "As source-specific examples to re-verify before implementation",
                    "As universal permanent standards",
                    "As irrelevant and removable",
                    "As legal requirements",
                ],
                "correct": 0,
                "explanation": "The chapters are Early Release and fast-moving implementation details can change.",
            },
            {
                "id": "M01.L10.Q24",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design an AgentOps quality-and-tool-governance system for a live enterprise assistant. "
                    "Include tool unit tests, single-turn and multi-turn golden datasets, memory evaluation, Simulators, "
                    "raw-audio evaluation, interruption metrics, operational metrics, CI/CD evaluation gates, production "
                    "monitoring, Tool Registry metadata and lineage, curated/dynamic tool assignment, API-first/MCP "
                    "standardization, and a federated governance model."
                ),
            },
        ],
        "passing_score": 70,
    },
}
