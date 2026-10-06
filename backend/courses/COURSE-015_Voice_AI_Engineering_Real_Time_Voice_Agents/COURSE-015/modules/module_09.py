"""M01.L09 — Live Multi-Agent UX and AgentOps Productionization.

Two source chapters -> one complete learner-facing lesson.

Source alignment:
- Chapter 14: Designing User Experience for a Live, Multimodal, Multi-Agent System
- Chapter 15: The Birth of AgentOps: Introduction to an Agent Operationalization Platform

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L09"
MODULE_ORDER = 1
MODULE_TITLE = "Live Agent UX & AgentOps Productionization"
MODULE_DESCRIPTION = (
    "Design a live, multimodal, multi-agent experience that makes system state legible "
    "to users, then extend the same product into a production discipline with AgentOps: "
    "evaluation, governance, tool and agent registries, memory, monitoring, CI/CD, and "
    "enterprise platform architecture."
)
SOURCE_CHAPTER = "14-15"
SOURCE_PAGES = "Early Release drafts; page numbers not provided"

TOPIC = {
    "title": "Live Multi-Agent UX and AgentOps Productionization",
    "slug": "agent-foundations-m01-l09",
    "description": (
        "Learn how to turn a technically correct live agent system into a trustworthy user "
        "experience, then learn how to operationalize that system at scale through the "
        "people, processes, and technologies of MLOps, GenAIOps, and AgentOps."
    ),
    "order": 9,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 7.0,
    "skill_tags": [
        "live-agent-ux",
        "multimodal-ux",
        "task-cards",
        "human-in-the-loop-ux",
        "provenance",
        "personalization",
        "accessibility",
        "agentops",
        "mlops",
        "genaiops",
        "evaluation",
        "tool-registry",
        "agent-registry",
        "memory-governance",
        "agents-as-a-service",
        "monitoring",
        "ci-cd",
        "productionization",
        "governance",
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
    ],

    "lesson": {
        "title": "Live Multi-Agent UX and AgentOps Productionization",
        "estimated_minutes": 420,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Live Multi-Agent UX and AgentOps Productionization

> **Lesson:** M01.L09  
> **Source alignment:** Chapters 14 and 15 of the supplied Early Release material.  
> This lesson combines product experience and operational productionization into one continuous path.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a technically correct live agent can still feel broken to the user.
- Explain why live, multimodal, multi-agent systems need more than a chat transcript.
- Apply the rule: voice carries intent, screen carries durable detail.
- Define user-facing live states such as listening, speaking, tool use, specialist work, approval, reconnecting, completion, and failure.
- Distinguish interrupting speech, revising scope, pausing work, canceling work, and asking a side question.
- Design agent activity labels that explain meaningful work without exposing protocol machinery.
- Explain why long-running backend Tasks should have visible task identity in the UI.
- Design task cards, activity timelines, source panels, approval prompts, recovery banners, and artifact views.
- Explain why fake progress precision reduces trust.
- Explain the host-controlled generative UI principle.
- Design clear human-in-the-loop approval and authentication flows.
- Design error states around recovery actions rather than generic failure messages.
- Explain why provenance, conflicts, recency, and partial-output status should be visible.
- Apply the three personalization rules: visible, scoped, reversible.
- Explain accessibility requirements for voice, visual state, keyboard/touch, and screen-reader paths.
- Trace an end-to-end long-running workflow from the user's perspective.
- Identify recurring UX patterns and anti-patterns.
- Explain the progression from DevOps to MLOps to GenAIOps to AgentOps.
- Distinguish model creators from model consumers.
- Explain PromptOps, RAGOps, and AgentOps as sub-disciplines of GenAIOps in the source's framing.
- Explain why autonomous decision-making makes AgentOps operationally distinct.
- Explain why AgentOps evaluation must cover tool selection and execution path, not only final output.
- Explain the purpose of Tool Registries and Agent Registries.
- Explain why short-term and long-term memory require governance.
- Explain the people/process/technology framing used throughout the source.
- Describe the source's MLOps environment progression from sandbox to production and governance.
- Explain the source's three-step model-selection process.
- Explain how prompt catalogs and prompt-template catalogs support evaluation and reuse.
- Compare labeled-data metrics, human evaluation, and LLM-as-a-judge approaches.
- Explain why production GenAI applications need guardrails, context retrieval, monitoring, and feedback loops.
- Explain the source's AgentOps platform additions: augmented evaluation catalog, Agents as a Service, registries, and dedicated memory.
- Explain how MLOps and GenAI/AgentOps can coexist in a unified enterprise platform.

---

## 1. UX is not visual polish

The source begins with an important point:

A system can be technically non-blocking and still feel unreliable.

The backend may know exactly what it is doing.

But if the user cannot tell whether the assistant is:

```text
listening
thinking
speaking
using a tool
delegating
waiting for approval
recovering
```

then the experience feels broken.

### Core principle

> UX for integrated agents is the work of making system state legible.

This is not an afterthought.

It is part of system design.

[[IMAGE_NEEDED: Technical state vs user-visible state | Left: backend event graph with listening, tool call, agent delegation, approval, reconnect; right: clean user UI with meaningful labels and controls | Learner should see that UX translates system state into understandable action]]

---

## 2. Why live multi-agent UX is different

Traditional chat has a simple rhythm:

```text
user sends
assistant replies
transcript grows
```

Live systems have several channels at once.

For example:

```text
microphone active
assistant speaking
video preview running
specialist working
tool processing
progress updates arriving
user can interrupt
```

These channels are not synchronized perfectly.

The assistant may stop speaking while a background task continues.

A tool may fail while the rest of the workflow succeeds.

The connection may drop while the task remains alive.

A simple transcript cannot represent all of this clearly.

---

## 3. Show meaningful state, not machinery

Users usually do not care whether the implementation used:

```text
A2A
MCP
JSON-RPC
background worker
```

They care about what that means.

Good labels:

```text
Research agent is collecting sources.
Data tool is processing the spreadsheet.
Calendar access needs authentication.
Report generator is assembling the document.
```

Weak labels:

```text
A2A statusUpdate received.
MCP tool pending.
JSON-RPC request in flight.
```

### Product rule

> Translate implementation events into user-meaningful activity.

---

## 4. From live chat to live workspace

The earlier live app had:

- microphone,
- WebSocket,
- video preview,
- audio output,
- tool calls.

Durable task handling turns that into a workspace.

The UI may now need:

```text
task cards
activity timeline
source panels
approval prompts
partial results
final artifacts
reconnect state
recovery actions
```

A task should not disappear into an invisible backend process.

[[IMAGE_NEEDED: Live chat vs live workspace | Left: simple mic + transcript interface; right: live controls plus task cards, source panel, approval card, activity timeline, artifact panel | Learner should see the interface evolve from conversation-only to task-aware workspace]]

---

## 5. Four questions the workspace should answer

At most moments, the interface should help answer:

```text
What is the assistant doing?
Is it waiting for me?
Can I interrupt, cancel, or change direction?
Where will the result appear?
```

These questions provide a practical UX review checklist.

If the user cannot answer them, the interface is likely hiding important state.

---

## 6. Voice-first, visual-augmented design

Voice is strong for:

- intent,
- steering,
- natural language,
- quick corrections.

Voice is weaker for:

- long lists,
- citations,
- tables,
- approvals,
- dense recovery choices.

The source's design rule is:

> Let voice carry intent; let the screen carry durable detail.

Example:

User:

```text
"Compare three suppliers on price,
delivery time, and warranty."
```

Good response:

```text
"I'll compare them.
I'll show the table as it comes together."
```

The spoken response stays concise.

The table lives visually.

---

## 7. Voice alerts; screen supports review

Suppose the system finds a paid dataset.

Voice can say:

```text
"I need your approval before accessing the paid dataset."
```

But the screen should show:

```text
cost
provider
intended use
consequences
approve
skip
details
```

For expensive, destructive, or privacy-sensitive actions, exact review matters more than conversational convenience.

---

## 8. Design an explicit live system state model

Avoid vague labels such as:

```text
Working
Loading
Thinking
```

because "working" may mean:

- model preparing response,
- tool running,
- specialist processing,
- waiting for approval,
- backend reconnecting,
- artifact generation.

A better model distinguishes those states.

Possible states:

```text
idle
connecting
listening
user_speaking
assistant_thinking
assistant_speaking
tool_running
agent_working
input_required
reconnecting
completed
failed
canceled
```

[[IMAGE_NEEDED: Live agent UI state machine | States for idle, connecting, listening, user speaking, thinking, speaking, tool running, specialist working, input required, reconnecting, completed, failed, canceled with user actions | Learner should see why state-specific UI beats one generic spinner]]

---

## 9. Similar controls can mean very different things

These are not equivalent:

```text
Mute
Interrupt
Cancel task
Stop session
```

### Mute

Stops sending audio.

### Interrupt

Stops current assistant speech and listens.

### Cancel task

Requests termination of background work.

### Stop session

Ends the live interaction.

The UI should not collapse all four into one ambiguous Stop button.

---

## 10. Interruption is part of the interface

Example:

Assistant:

```text
"I found twelve suppliers. The first is—"
```

User:

```text
"Actually, only compare European suppliers."
```

A good system should:

1. stop speech quickly,
2. acknowledge the change,
3. update visible task scope,
4. explain whether collection is restarting or being filtered.

The background task must change appropriately.

Stopping audio alone is not enough.

---

## 11. Five different interruption intents

The source separates:

### Interrupt speech

Stop speaking and listen.

### Revise scope

Change active task constraints.

### Pause work

Temporarily stop work without discarding it.

### Cancel work

Move the Task toward terminal cancellation.

### Ask a side question

Answer without modifying the active Task.

This is important because a user saying "wait" may not mean "destroy all work."

{{exercise:M01.L09.EX01}}

---

## 12. Show agent activity under one conversational owner

The source recommends keeping the main assistant as the conversational owner.

Specialists and tools can appear as:

- activity cards,
- timeline entries,
- source annotations.

Avoid turning every agent into a separate personality unless the product intentionally wants that style.

Good:

```text
Research agent collecting sources.
```

Not:

```text
Three agent personalities debating in chat.
```

---

## 13. Activity timeline

A timeline can provide calm visibility:

```text
10:14 Started supplier comparison
10:15 Collecting sources
10:16 Extracted 23 spreadsheet rows
10:17 Waiting for paid-data approval
10:20 Draft comparison ready
```

This gives the user a narrative of work.

Advanced users can expand:

```text
Show tool details
View sources
Inspect activity
```

The default interface stays simple.

---

## 14. Task cards make asynchronous work visible

Chapter 13 gave Tasks identity in the backend.

Chapter 14 gives Tasks identity in the UI.

A task card can show:

```text
title
status
phase
owner/activity label
progress
last updated
partial artifact
sources
available actions
final result
```

Conceptual state:

```python
task = {
    "id": "task_123",
    "title": "Battery storage market report",
    "status": "working",
    "phase": "collecting_sources",
    "progress": {"current": 12, "total": 40},
    "actions": ["view_details", "cancel"],
}
```

---

## 15. Avoid fake precision

Some tasks cannot honestly say:

```text
37% complete
```

A phase label may be better:

```text
Collecting sources
Reviewing documents
Building comparison table
Drafting report
Waiting for approval
```

False precision damages trust.

Use numeric progress only when the denominator has real meaning.

---

## 16. Show partial results when useful

A task may not be finished, but useful artifacts can already exist.

Examples:

- source list,
- draft table,
- outline,
- preliminary chart.

Show them with status labels such as:

```text
Draft
Still updating
Partial result
```

Partial output is useful when its incompleteness is visible.

---

## 17. Generative UI: agent proposes, host controls

A specialist may discover that it needs:

- comparison table,
- approval card,
- chart,
- source panel.

The stable UX principle in the source is:

> Agents may propose surfaces; the Host controls rendering.

The Host decides:

- which approved component is allowed,
- which props are valid,
- what actions exist,
- how accessibility works,
- whether a high-risk approval is acceptable.

The agent should not send arbitrary executable UI code.

[[IMAGE_NEEDED: Host-controlled generative UI | Agent proposes structured component description -> host component catalog validates -> safe Task Card / Approval Card / Chart renders | Learner should understand that agents do not get unrestricted UI execution]]

---

## 18. Human-in-the-loop UX asks four questions

A good approval interface must tell the user:

```text
What does the system need?
Why does it need it?
What happens if I approve?
What happens if I reject or ignore it?
```

Weak:

```text
Approve action?
```

Strong:

```text
Approval needed

Dataset: ExampleData
Cost: £120
Purpose: supplier revenue estimates

[Approve purchase]
[Skip dataset]
[Show details]
```

---

## 19. Authentication prompts need the same clarity

If the system needs:

- calendar,
- repository,
- CRM,
- document store,

the prompt should explain:

```text
which service
why access is needed
what task depends on it
```

The user should not be surprised by permission requests.

---

## 20. Structured input belongs on screen when precision matters

Voice can handle a small choice.

Example:

```text
"PDF or PowerPoint?"
```

But choosing among:

```text
20 database schemas
```

should be visual.

Use a form or selection surface when:

- options are numerous,
- values are precise,
- mistakes are expensive.

---

## 21. Error presentation should map to recovery

"Something went wrong" is rarely enough.

Different failures need different recovery.

Examples:

### Voice input unclear

```text
Repeat
Type instead
Use touch controls
```

### Tool failure

```text
Retry
Continue without it
```

### Authentication expired

```text
Reconnect
Skip step
```

### Remote agent timeout

```text
Wait
Retry
Cancel
```

### Partial completion

```text
Download completed source set
Retry export only
```

### Network disconnect

```text
Reconnect
Continue later
```

[[IMAGE_NEEDED: Error recovery matrix | Failure types mapped to user-facing explanation and specific next actions | Learner should see that good errors explain what remains usable]]

---

## 22. Provenance, sources, and confidence

Integrated systems may synthesize information from:

- model knowledge,
- documents,
- APIs,
- user files,
- specialist agents,
- tool outputs.

The final response may sound like one answer.

The UI should still help users understand where claims came from.

Useful source panel fields:

```text
source
timestamp
artifact
recency warning
confidence warning
unresolved conflict
```

---

## 23. Show disagreement instead of hiding it

Suppose two providers disagree about revenue.

A strong UI may say:

```text
"Revenue estimates vary across sources."
```

Then show:

```text
Source A: value + timestamp
Source B: value + timestamp
```

Do not hide conflict behind a false single number.

---

## 24. Personalization can improve or damage trust

The difference is control.

The source gives three rules:

```text
visible
scoped
reversible
```

---

## 25. Make personalization visible

If project context is being used, say so.

Example:

```text
Using project context:
Battery Storage Research

[Change]
[Ignore for this task]
```

If response style is adapted:

```text
Voice mode: Brief summaries
[Adjust]
```

The system should not appear to use hidden knowledge mysteriously.

---

## 26. Define personalization scope

"Remember this" is ambiguous.

Possible scope:

```text
this response
this task
this project
this device
all future sessions
```

A preference should not silently expand beyond the user's intent.

This matters especially for approval memory.

Approving one purchase does not imply permission for all future purchases.

---

## 27. Make personalization reversible

Users should be able to inspect and change:

```text
report format
preferred sources
voice style
project context
accessibility settings
approval memory
```

Concision should not hide detail permanently.

If voice is brief, detailed content should still remain available visually.

---

## 28. Accessibility is part of the state model

Multimodal does not automatically mean accessible.

Critical interactions need overlapping paths across:

```text
voice
visual
touch
keyboard
screen reader
```

Examples:

- spoken response -> captions/transcript,
- color state -> text label,
- chime -> visible state,
- voice interruption -> explicit button,
- dense report -> semantic visual structure.

---

## 29. High-risk review must remain safe across modalities

Accessibility should never bypass review.

If a user asks by voice to prepare a purchase:

the UI should still show:

```text
item
price
merchant
delivery
payment method
```

and ask for explicit confirmation.

Alternative input/output paths should preserve safeguards.

---

## 30. End-to-end UX walkthrough

The source revisits the long-running battery-storage report.

### Start

User speaks the request.

The assistant acknowledges briefly.

### Task identity

A task card appears.

### Scope change

User interrupts:

```text
"Only include European companies."
```

The task scope visibly updates.

### Progress

The timeline shows:

```text
collecting sources
reviewing sources
building table
```

### Approval

A paid-data request appears as a reviewable card.

### Completion

Final artifact panel includes:

- report,
- comparison table,
- sources.

The user experiences one continuous workflow.

[[IMAGE_NEEDED: End-to-end live workspace screen composition | Live status strip, task card, activity timeline, approval card, source drawer, final artifact panel, recovery banner | Learner should see the complete UX surface for long-running agent work]]

---

## 31. Reusable UX patterns

The source highlights recurring patterns:

```text
Live status strip
Task card
Activity timeline
Source drawer
Approval card
Final artifact panel
Recovery banner
Interruption acknowledgment
Resumable session view
```

These are useful building blocks for many integrated agent products.

---

## 32. Common UX anti-patterns

### Mystery spinner

Shows activity but no meaning.

### Uninterruptible monologue

User cannot redirect the system.

### Agent committee UI

Every specialist becomes a separate personality.

### Raw tool logs

Implementation details become product UI.

### Disappearing tasks

Work starts without visible durable identity.

### Generic error messages

Partial success becomes invisible.

### Voice-only dense output

User must remember complex details.

### Hidden personalization

Adaptation happens without explanation.

### Protocol names as product concepts

Users must learn implementation vocabulary.

### Overbroad cancellation

Interrupting speech cancels background work.

{{exercise:M01.L09.EX02}}

---

## 33. Production UX checklist

Before shipping, check for:

- visible listening/speaking/thinking states,
- agent/tool activity labels,
- task cards,
- meaningful phase progress,
- partial results,
- cancel/pause/retry/resume controls,
- interruption handling,
- approval/authentication flows,
- reconnect/recovery,
- source inspection,
- partial-failure explanation,
- accessible modality alternatives,
- visible/reversible personalization,
- device-appropriate layouts.

UX testing still matters because timing and device context strongly affect live systems.

---

## 34. From product UX to production operations

Once the interface is understandable, another problem remains:

> How do we run this system securely, reliably, and repeatedly at organizational scale?

That is the focus of AgentOps.

The source presents AgentOps as an additive evolution from:

```text
DevOps
   ↓
MLOps
   ↓
GenAIOps
   ↓
AgentOps
```

Earlier disciplines remain relevant.

AgentOps adds operational practices specific to autonomous, tool-using systems.

---

## 35. DevOps and MLOps foundations

DevOps focuses on productionizing deterministic software.

Core ideas include:

- repositories,
- CI/CD,
- testing,
- security,
- repeatability.

MLOps extends this for machine learning.

ML adds problems such as:

```text
data dependence
non-determinism
model monitoring
retraining
data governance
```

The source frames MLOps through:

```text
People
Processes
Technology
```

---

## 36. Why MLOps matters

The source emphasizes outcomes such as:

- faster time to production,
- standardization,
- reusable templates,
- reduced manual work,
- stronger governance,
- scalable infrastructure.

The specific business numbers in the source are illustrative.

The durable lesson is:

> Standardization turns one-off ML projects into repeatable organizational capability.

---

## 37. Model creators vs model consumers

The source separates two roles.

### Model creators

Build/train/fine-tune models.

Operational disciplines:

```text
MLOps
FMOps
LLMOps
```

### Model consumers

Use existing foundation models to build applications.

Operational discipline:

```text
GenAIOps
```

Most companies are primarily model consumers.

That shifts attention from:

```text
training models
```

to:

```text
building and operating applications around models
```

[[IMAGE_NEEDED: Model creators vs consumers | Left: model creation pipeline with MLOps/FMOps; right: application builders consuming FMs through GenAIOps | Learner should see the organizational split between model development and application development]]

---

## 38. GenAIOps

GenAIOps extends DevOps for GenAI applications.

The source treats it as an umbrella around evolving practices.

### PromptOps

Standardize:

- prompt reuse,
- versioning,
- templates,
- evaluation.

### RAGOps

Operationalize:

- data cleaning,
- chunking,
- vectorization,
- indexing,
- retrieval,
- reranking,
- grounded generation.

### AgentOps

Operationalize:

- autonomous decisions,
- tools,
- memory,
- multi-agent systems.

---

## 39. Why agents need a distinct Ops discipline

An agent does more than generate.

It:

```text
perceives
decides
acts
uses tools
pursues goals
```

That autonomy introduces new operational questions.

A system can fail even when the final sentence looks good.

For example:

- wrong tool chosen,
- right tool with wrong args,
- unsafe tool sequence,
- memory contamination,
- agent-loop failure.

AgentOps therefore evaluates and governs the path, not only the output.

---

## 40. Four core AgentOps challenges

The source emphasizes:

### Autonomous decision-making

Agents choose tools and sequences.

### Tool orchestration and governance

Organizations may need hundreds of tools.

### Complex memory management

Short-term and long-term memory affect privacy and behavior.

### Multi-agent systems

Many agents behave like distributed microservices.

[[IMAGE_NEEDED: Four AgentOps challenge pillars | Autonomous Decisions, Tool Governance, Memory Governance, Multi-Agent Operations around a central AgentOps platform | Learner should remember why AgentOps extends GenAIOps]]

---

## 41. People, process, and technology

The source consistently frames operational disciplines through three pillars.

### People

Who owns:

- infrastructure,
- data,
- model/application development,
- governance.

### Process

How work moves from:

```text
idea
experiment
evaluation
approval
deployment
monitoring
```

### Technology

The platforms, registries, pipelines, observability, and memory systems that support the process.

A strong AgentOps program requires all three.

---

## 42. MLOps personas and responsibilities

The source includes roles such as:

### Cloud platform team

Infrastructure and security foundation.

### Data engineering

Data pipelines and quality.

### Data science / ML engineering / MLOps engineering

Experimentation, training, automation, production pipelines.

### ML governance

Central metadata, artifact, performance, lineage, and approval control.

The source notes these are roles, not mandatory headcount.

One person may wear several hats.

---

## 43. MLOps environment progression

The source describes a modular environment structure.

### Shared service and data projects

Networking, IAM, monitoring, data lake/mesh.

### Experimentation

Sandbox for exploration.

### Development

Turn experiments into automated pipelines.

### Staging

Production-like validation.

### Production

Live serving, monitoring, controlled rollout.

### Governance

Model/Artifact Registry and approval control.

This creates an auditable path from experimentation to production.

[[IMAGE_NEEDED: MLOps environment lifecycle | Sandbox -> Development -> Staging -> Production, with Shared Services/Data underneath and Governance/Registry above | Learner should see separation of concerns across environments]]

---

## 44. GenAI adds new application personas

The source introduces roles such as:

### Prompt Engineer

Domain/prompt specialist.

### AI Engineer

Builds model-integrated backend logic and understands model families.

### Application/DevOps developers

Build the user-facing and production application.

The point is not job-title purity.

The point is ensuring these responsibilities exist.

---

## 45. Validate the use case before selecting models

The source recommends beginning with business reality.

Ask:

```text
Does this create real value?
What is the expected ROI?
Is GenAI really needed?
Could a simpler system solve it?
```

Operational excellence begins before infrastructure.

A bad use case does not become good because the platform is sophisticated.

---

## 46. Three-step model selection process

### Step 1 — Build an approved FM reference table

Curate a manageable set of candidate models.

Consider:

- licensing,
- proprietary/open,
- context window,
- multimodality,
- fine-tuning support,
- live capabilities,
- team expertise.

### Step 2 — Evaluate top candidates on your data

Generic leaderboards are not enough.

Use task-specific business data.

### Step 3 — Select based on business priorities

Balance:

```text
precision
cost
speed/latency
```

The highest raw score is not automatically the best business choice.

---

## 47. Prompt catalog as evaluation data

A prompt catalog begins as a collection of:

```text
input prompts
expected/reference outputs
model outputs
```

It can grow from a few examples into hundreds or thousands.

This becomes a custom evaluation dataset.

The source treats it as a cornerstone of production evaluation.

---

## 48. Prompt Template Catalog

Prompt templates let organizations generate consistent variants.

A centralized catalog can improve:

- reuse,
- versioning,
- ownership,
- collaboration,
- model migration.

Different model families may require different prompt variants.

A catalog lets those differences be managed deliberately.

---

## 49. Prompt optimization creates a feedback loop

The source also mentions automated prompt optimization.

Conceptually:

```text
historical evaluation results
    ↓
optimizer/model
    ↓
candidate prompt improvements
    ↓
evaluation
    ↓
better prompt version
```

This is an example of using operational data to improve application behavior.

---

## 50. Choose evaluation metrics based on the task

If labeled data exists, possible approaches include:

- precision/recall/F1 for definitive answers,
- cosine similarity,
- ROUGE,
- BLEU,
- factuality metrics,
- safety/bias metrics.

If labeled data does not exist:

### Human evaluation

High-quality but expensive.

### LLM as a judge

More scalable, potentially less precise.

The source describes enterprise evaluation as often evolving from more human review toward increasing automation.

---

## 51. Rigorous model evaluation

The source's workflow is:

```text
prompt catalog
+
candidate models
+
evaluation metrics
    ↓
record-level scores
    ↓
aggregated model scores
    ↓
stored results + lineage
```

This creates repeatable evidence for model choice.

---

## 52. Production GenAI needs more than model selection

Once a model is chosen, the application still needs:

### Guardrails and security

Input/output filtering and protection.

### Context retrieval

RAG or agent-based access to current/private knowledge.

### Continuous monitoring

Track behavior and operational quality in production.

### Feedback and ratings

Use user feedback to improve future evaluation data.

This creates a loop:

```text
production
  ↓
monitoring + feedback
  ↓
evaluation data
  ↓
improvement
  ↓
production
```

---

## 53. Agent evaluation adds the execution path

Agent evaluation cannot stop at:

```text
user input
→ final answer
```

The source adds tool-oriented dimensions.

### Tool unit testing

Each tool must work independently.

### Augmented evaluation dataset

Evaluation records include:

```text
correct tool
correct parameters
expected response
```

### Tool selection evaluation

Measure:

- correct tool choice,
- parameter accuracy,
- tool-use behavior.

### End-to-end evaluation

Still evaluate final response quality.

### Operational metrics

Measure:

- latency,
- cost,
- efficiency.

[[IMAGE_NEEDED: Agent evaluation stack | Tool unit tests -> augmented prompt catalog -> tool selection/argument evaluation -> end-to-end output evaluation -> latency/cost metrics | Learner should see that agent quality includes execution path plus outcome]]

{{exercise:M01.L09.EX03}}

---

## 54. Tool Registry

At enterprise scale, organizations may have many tools:

- local functions,
- private APIs,
- public APIs,
- MCP Servers,
- database actions.

A Tool Registry becomes a centralized source of truth.

It can support:

```text
discovery
ownership
versioning
security
reuse
lifecycle
```

Without a registry, teams may:

- rebuild existing tools,
- call outdated versions,
- lack clear ownership,
- miss security constraints.

---

## 55. Agent Registry

The same problem appears for agents.

Large organizations may have many specialists.

A central Agent Registry can store information such as:

```text
agent identity
skills
versions
owners
deployment endpoint
Agent Card
access policy
```

This enables:

- discovery,
- reuse,
- routing,
- governance.

It is especially important for multi-agent systems.

---

## 56. Memory and data governance

Agents depend on:

### Short-term memory

Current conversation/task context.

### Long-term memory

Persistent user/project/organizational knowledge.

Memory introduces questions such as:

```text
What may be stored?
For how long?
Who can access it?
How is it evaluated?
How does stale memory get corrected?
```

Memory is therefore an operational and governance concern, not just a prompting feature.

---

## 57. Unified AgentOps platform

The source extends GenAIOps with AgentOps-specific components.

Key additions include:

```text
augmented evaluation prompt catalog
Agents as a Service
Tool Registry
Agent Registry
short-term memory
long-term memory
```

These are integrated with:

- CI/CD,
- development/staging/production environments,
- monitoring,
- governance.

[[IMAGE_NEEDED: Unified AgentOps platform | Development/Staging/Production pipeline connected to Evaluation Catalog, Tool Registry, Agent Registry, Short-Term Memory, Long-Term Memory, CI/CD, Governance | Learner should see AgentOps as an operational platform rather than one library]]

---

## 58. Agents as a Service

The source highlights a design choice:

```text
agent embedded directly in app backend
```

versus:

```text
agent deployed as independent service
```

Agents as a Service can improve:

- reuse,
- independent deployment,
- versioning,
- CI/CD,
- discovery,
- ownership.

This aligns with the multi-agent and A2A architecture studied earlier.

---

## 59. Augmented evaluation catalog for AgentOps

A normal prompt catalog stores:

```text
prompt
expected answer
```

AgentOps needs more.

It may also store:

```text
expected tool
expected parameters
expected tool trajectory
expected final response
latency target
cost target
```

This makes evaluation aware of agent behavior, not only language output.

---

## 60. Short-term vs long-term memory in the platform

The source proposes:

### Short-term memory

Close to the production agent.

Used for:

- current conversation,
- current run state.

### Long-term memory

Persistent data layer.

Used for:

- historical interactions,
- user preferences,
- cross-session memory,
- graph-like relationships.

The exact storage products are implementation choices.

The durable design is separation of ephemeral working context from persistent memory.

---

## 61. Registries are governance infrastructure

A registry is not just a list.

A strong registry can help answer:

```text
Who owns this tool/agent?
Which version is approved?
What security policy applies?
Where is it deployed?
What capabilities does it expose?
Is it deprecated?
```

Registries therefore connect:

```text
discovery
reuse
governance
```

---

## 62. Unifying model and application operations

Many organizations consume models rather than create them.

For them, GenAIOps/AgentOps may be enough.

Some enterprises also:

- fine-tune,
- train,
- manage custom models.

Those organizations may need one broader platform combining:

```text
MLOps/FMOps
+
GenAIOps/AgentOps
```

The two streams remain conceptually different but can share:

- governance,
- security,
- CI/CD,
- observability,
- artifact management.

---

## 63. UX and AgentOps are connected

These two chapters are not unrelated.

The UX layer exposes:

```text
state
progress
approvals
errors
sources
artifacts
```

AgentOps must make those states trustworthy.

For example:

### UX says:

```text
"Research agent is collecting sources."
```

AgentOps must provide reliable observability to support that claim.

### UX shows:

```text
"Tool failed. Retry?"
```

AgentOps must know which tool version failed and how to retry safely.

### UX shows:

```text
"Using project context."
```

Memory governance must know what context exists and whether it is allowed.

### UX asks for approval

Operational state must correlate the approval to the exact action.

The production platform and the user experience reinforce one another.

[[IMAGE_NEEDED: UX surface connected to AgentOps backbone | Top: live workspace with task card, progress, approval, sources; bottom: monitoring, registries, memory, evaluation, CI/CD, governance supporting those visible states | Learner should see that trustworthy UX depends on operational discipline]]

---

## 64. The full AgentOps improvement loop

A production agent platform should support a cycle:

```text
Design
  ↓
Develop
  ↓
Evaluate
  ↓
Deploy
  ↓
Monitor
  ↓
Collect feedback
  ↓
Update evaluation catalog
  ↓
Improve prompts/tools/agents
  ↓
Redeploy
```

AgentOps is therefore not only deployment.

It is lifecycle management.

---

## 65. Practical production principles

### 1. Keep user state understandable

Do not expose protocol jargon.

### 2. Keep system behavior observable

User-facing progress must be supported by real operational state.

### 3. Evaluate tool behavior

Final-answer quality is not enough.

### 4. Centralize discoverability

Use tool/agent registries when scale requires them.

### 5. Govern memory

Persistent personalization creates privacy and correctness obligations.

### 6. Reuse CI/CD and environment discipline

AgentOps builds on software and ML operations rather than replacing them.

### 7. Keep approvals explicit

Operational automation must not silently expand authority.

### 8. Preserve feedback loops

Production data should improve evaluation and future versions.

{{exercise:M01.L09.EX04}}

---

## 66. Source-specific details to treat carefully

These chapters include many technology and platform examples.

Treat exact items as source-specific and potentially time-sensitive:

- named cloud services,
- model families,
- package/platform examples,
- precise FM counts,
- exact business-performance percentages,
- AgentOps platform product choices,
- generative UI terminology,
- implementation names such as A2UI/AG-UI/MCP Apps,
- specific evaluation metric examples.

The durable ideas are:

```text
state legibility
voice + visual complementarity
task identity
approval clarity
provenance
visible personalization
accessibility
evaluation
registries
memory governance
CI/CD
monitoring
operational feedback loops
```

---

## 67. Complete mental model

The lesson has two halves.

### User-facing half

```text
Live state
Voice intent
Visual durable detail
Task card
Activity timeline
Approval
Recovery
Sources
Accessibility
Personalization
```

### Operational half

```text
DevOps foundation
MLOps foundation
GenAIOps
AgentOps
Evaluation
Tool Registry
Agent Registry
Memory
Monitoring
CI/CD
Governance
```

Together they create:

```text
trustworthy product experience
+
repeatable operational system
```

The user should experience one understandable assistant.

The organization needs an operational platform capable of evaluating, governing, deploying, monitoring, and improving the many moving parts beneath that experience.

---

## Important misconceptions

### Misconception 1
> "If the backend is correct, the UX will feel reliable."

No. Hidden state makes technically correct systems feel broken.

### Misconception 2
> "A chat transcript is enough for live multi-agent work."

No. Long-running and multimodal workflows need stateful workspace surfaces.

### Misconception 3
> "Voice should carry all information in a voice-first product."

No. Voice carries intent well; dense durable detail often belongs visually.

### Misconception 4
> "Interrupting speech should automatically cancel the active Task."

No. Speech interruption and task cancellation are different actions.

### Misconception 5
> "More detailed protocol labels make the UI more transparent."

No. Transparency means meaningful state, not raw implementation jargon.

### Misconception 6
> "A task card must always show numeric progress."

No. Honest phase labels are better than fake precision.

### Misconception 7
> "Agents should be free to generate arbitrary UI code."

No. The source's stable principle is host-controlled rendering through approved components.

### Misconception 8
> "An approval prompt only needs an Approve button."

No. The user needs context, consequence, alternatives, and safe expiry.

### Misconception 9
> "Personalization should be invisible when it is helpful."

No. The source emphasizes visible, scoped, reversible adaptation.

### Misconception 10
> "Voice automatically solves accessibility."

No. Critical interactions need alternative modalities.

### Misconception 11
> "AgentOps replaces MLOps and GenAIOps."

No. The source presents the evolution as additive.

### Misconception 12
> "Agent quality can be evaluated only from final answers."

No. Tool choice, parameters, trajectory, latency, and cost matter too.

### Misconception 13
> "Tool Registry and Agent Registry are simple inventories."

No. They support governance, ownership, versioning, discovery, and secure reuse.

### Misconception 14
> "Memory is only a model-context feature."

No. Persistent memory creates governance, privacy, and lifecycle concerns.

### Misconception 15
> "The highest-accuracy model is automatically the correct model."

No. The source balances performance with cost and latency/business priorities.

### Misconception 16
> "Public model leaderboards are sufficient for production selection."

No. Evaluate candidate models on your own use-case data.

### Misconception 17
> "Human evaluation and LLM-as-a-judge are mutually exclusive."

No. The source describes a progression and combination depending on precision and scale.

### Misconception 18
> "AgentOps is only monitoring."

No. It spans evaluation, registries, memory, governance, deployment, observability, and lifecycle improvement.

---

## Key terminology

| Term | Meaning |
|---|---|
| Live workspace | UI combining live conversation with durable task state |
| Live status strip | Surface showing listening/speaking/thinking/reconnecting state |
| Task card | Visible UI identity for long-running work |
| Activity timeline | Human-readable history of meaningful workflow progress |
| Source drawer | UI area for provenance and supporting evidence |
| Approval card | Reviewable HITL decision surface |
| Artifact panel | Stable location for final or partial outputs |
| Recovery banner | UI explaining reconnect/retry/continue-later state |
| Barge-in | User interrupting the assistant while it is speaking |
| Scope revision | Updating active task constraints |
| Generative UI | Agent-proposed structured UI rendered under host control |
| Provenance | Information showing where a claim/result came from |
| Visible personalization | Showing which context/preference is affecting behavior |
| Scoped personalization | Limiting a preference to defined contexts |
| Reversible personalization | Allowing the user to inspect/change/disable adaptation |
| AgentOps | Discipline for operationalizing agent systems |
| DevOps | Operational discipline for deterministic software |
| MLOps | Operational discipline for ML model lifecycle |
| FMOps | Operational discipline for foundation-model development |
| GenAIOps | Operational discipline for applications using foundation models |
| PromptOps | Prompt lifecycle/versioning/evaluation discipline |
| RAGOps | Operationalization of retrieval and grounded generation pipelines |
| Tool Registry | Central governed catalog of organization tools |
| Agent Registry | Central governed catalog of deployed agents |
| Agent evaluation | Evaluation of tool behavior plus final output and operations |
| Prompt catalog | Curated evaluation dataset of prompts and expected/reference behavior |
| Prompt Template Catalog | Central repository of reusable/versioned prompt templates |
| Human evaluation | People scoring model/application behavior |
| LLM as a judge | Model-based automated evaluator |
| Agents as a Service | Deploying agents as independently managed services |
| Short-term memory | Current session/task context |
| Long-term memory | Persistent cross-session/project/user memory |
| Governance | Controls for ownership, approvals, lineage, security, and policy |

---

## Self-check

1. Why can a technically correct agent still feel unreliable?
2. Why is a chat transcript insufficient for live multimodal work?
3. What does "voice carries intent, screen carries durable detail" mean?
4. What are the four questions a live workspace should answer?
5. Why should listening, tool use, specialist work, and approval be separate states?
6. What is the difference between mute, interrupt, cancel task, and stop session?
7. What should happen after a user revises task scope by voice?
8. Why should specialist activity usually remain under one conversational owner?
9. What belongs in an activity timeline?
10. What should a task card contain?
11. Why is fake numeric progress harmful?
12. When are partial artifacts useful?
13. What does host-controlled generative UI mean?
14. What four questions should an approval prompt answer?
15. Why are visual reviews important for high-risk voice actions?
16. How should error UX support recovery?
17. Why should provenance show source disagreement?
18. What are the three rules for trustworthy personalization?
19. Why must personalization scope be explicit?
20. How should accessibility interact with approvals and high-risk actions?
21. What are the main recurring UX patterns?
22. What are the main UX anti-patterns?
23. How do DevOps, MLOps, GenAIOps, and AgentOps relate?
24. What is the difference between a model creator and model consumer?
25. What is PromptOps?
26. What is RAGOps?
27. Why is AgentOps operationally distinct?
28. What are the four AgentOps challenges highlighted by the source?
29. Why does the source use the People/Process/Technology framework?
30. What are the main MLOps environment stages?
31. What roles appear in the MLOps organization?
32. Why should a GenAI use case be validated before model selection?
33. What are the three model-selection steps?
34. Why should candidate models be tested on your own data?
35. What is a prompt catalog?
36. What is a Prompt Template Catalog?
37. When are traditional metrics useful?
38. When might human evaluation be preferred?
39. When might LLM-as-a-judge be useful?
40. What additional production components does a GenAI application need after model selection?
41. Why does AgentOps evaluation need tool-unit tests?
42. What data should be added to an AgentOps evaluation catalog?
43. What is the purpose of a Tool Registry?
44. What is the purpose of an Agent Registry?
45. Why is memory a governance concern?
46. What does Agents as a Service mean?
47. How can UX state and AgentOps observability support one another?
48. What is the complete AgentOps improvement loop?
49. How can MLOps and GenAI/AgentOps coexist in one enterprise platform?
50. Which source details should be treated as time-sensitive implementation examples rather than timeless architecture?

---

## Retain this idea

**A production agent system must be understandable to users and operable by organizations. The UX layer makes live state, progress, approvals, provenance, personalization, recovery, and accessibility legible. The AgentOps layer makes the same system repeatable and governable through evaluation, registries, memory management, CI/CD, monitoring, security, and lifecycle improvement. Trust comes from both layers working together: users need to understand what the system is doing, while engineering and governance teams need evidence that the system is behaving correctly, safely, and consistently at scale.**
""".strip(),

        "sections": [
            {"id": "ux-not-polish", "title": "UX Is Not Visual Polish", "order": 1},
            {"id": "why-live-ux", "title": "Why Live Multi-Agent UX Is Different", "order": 2},
            {"id": "meaningful-state", "title": "Show Meaningful State, Not Machinery", "order": 3},
            {"id": "workspace", "title": "From Live Chat to Live Workspace", "order": 4},
            {"id": "four-questions", "title": "Four Questions the Workspace Should Answer", "order": 5},
            {"id": "voice-screen", "title": "Voice-First, Visual-Augmented Design", "order": 6},
            {"id": "approval-voice", "title": "Voice Alerts; Screen Supports Review", "order": 7},
            {"id": "live-state-model", "title": "Design an Explicit Live System State Model", "order": 8},
            {"id": "control-differences", "title": "Similar Controls Can Mean Different Things", "order": 9},
            {"id": "interruptions", "title": "Interruption Is Part of the Interface", "order": 10},
            {"id": "interruption-types", "title": "Five Different Interruption Intents", "order": 11},
            {"id": "activity", "title": "Show Agent Activity Under One Conversational Owner", "order": 12},
            {"id": "timeline", "title": "Activity Timeline", "order": 13},
            {"id": "task-card", "title": "Task Cards Make Asynchronous Work Visible", "order": 14},
            {"id": "fake-progress", "title": "Avoid Fake Precision", "order": 15},
            {"id": "partial-results", "title": "Show Partial Results When Useful", "order": 16},
            {"id": "generative-ui", "title": "Generative UI: Agent Proposes, Host Controls", "order": 17},
            {"id": "hitl-ux", "title": "Human-in-the-Loop UX", "order": 18},
            {"id": "auth-ux", "title": "Authentication Prompts Need Clarity", "order": 19},
            {"id": "structured-input", "title": "Structured Input Belongs on Screen", "order": 20},
            {"id": "errors", "title": "Error Presentation Should Map to Recovery", "order": 21},
            {"id": "provenance", "title": "Provenance, Sources, and Confidence", "order": 22},
            {"id": "conflicts", "title": "Show Disagreement Instead of Hiding It", "order": 23},
            {"id": "personalization", "title": "Personalization Can Improve or Damage Trust", "order": 24},
            {"id": "visible-personalization", "title": "Make Personalization Visible", "order": 25},
            {"id": "scope-personalization", "title": "Define Personalization Scope", "order": 26},
            {"id": "reversible-personalization", "title": "Make Personalization Reversible", "order": 27},
            {"id": "accessibility", "title": "Accessibility Is Part of the State Model", "order": 28},
            {"id": "accessibility-review", "title": "High-Risk Review Must Remain Safe Across Modalities", "order": 29},
            {"id": "ux-walkthrough", "title": "End-to-End UX Walkthrough", "order": 30},
            {"id": "ux-patterns", "title": "Reusable UX Patterns", "order": 31},
            {"id": "ux-antipatterns", "title": "Common UX Anti-Patterns", "order": 32},
            {"id": "ux-checklist", "title": "Production UX Checklist", "order": 33},
            {"id": "production-shift", "title": "From Product UX to Production Operations", "order": 34},
            {"id": "devops-mlops", "title": "DevOps and MLOps Foundations", "order": 35},
            {"id": "mlops-value", "title": "Why MLOps Matters", "order": 36},
            {"id": "creators-consumers", "title": "Model Creators vs Model Consumers", "order": 37},
            {"id": "genaiops", "title": "GenAIOps", "order": 38},
            {"id": "agentops-need", "title": "Why Agents Need a Distinct Ops Discipline", "order": 39},
            {"id": "agentops-challenges", "title": "Four Core AgentOps Challenges", "order": 40},
            {"id": "people-process-tech", "title": "People, Process, and Technology", "order": 41},
            {"id": "mlops-personas", "title": "MLOps Personas and Responsibilities", "order": 42},
            {"id": "mlops-environments", "title": "MLOps Environment Progression", "order": 43},
            {"id": "genai-personas", "title": "GenAI Adds New Application Personas", "order": 44},
            {"id": "validate-usecase", "title": "Validate the Use Case Before Selecting Models", "order": 45},
            {"id": "model-selection", "title": "Three-Step Model Selection Process", "order": 46},
            {"id": "prompt-catalog", "title": "Prompt Catalog as Evaluation Data", "order": 47},
            {"id": "prompt-template-catalog", "title": "Prompt Template Catalog", "order": 48},
            {"id": "prompt-optimization", "title": "Prompt Optimization Creates a Feedback Loop", "order": 49},
            {"id": "evaluation-metrics", "title": "Choose Evaluation Metrics Based on the Task", "order": 50},
            {"id": "model-eval", "title": "Rigorous Model Evaluation", "order": 51},
            {"id": "genai-production", "title": "Production GenAI Needs More Than Model Selection", "order": 52},
            {"id": "agent-evaluation", "title": "Agent Evaluation Adds the Execution Path", "order": 53},
            {"id": "tool-registry", "title": "Tool Registry", "order": 54},
            {"id": "agent-registry", "title": "Agent Registry", "order": 55},
            {"id": "memory-governance", "title": "Memory and Data Governance", "order": 56},
            {"id": "agentops-platform", "title": "Unified AgentOps Platform", "order": 57},
            {"id": "agents-as-service", "title": "Agents as a Service", "order": 58},
            {"id": "augmented-catalog", "title": "Augmented Evaluation Catalog for AgentOps", "order": 59},
            {"id": "memory-architecture", "title": "Short-Term vs Long-Term Memory in the Platform", "order": 60},
            {"id": "registry-governance", "title": "Registries Are Governance Infrastructure", "order": 61},
            {"id": "unified-platform", "title": "Unifying Model and Application Operations", "order": 62},
            {"id": "ux-agentops-connection", "title": "UX and AgentOps Are Connected", "order": 63},
            {"id": "operational-loop", "title": "The Full AgentOps Improvement Loop", "order": 64},
            {"id": "production-principles", "title": "Practical Production Principles", "order": 65},
            {"id": "source-boundaries", "title": "Source-Specific Details to Treat Carefully", "order": 66},
            {"id": "complete-model", "title": "Complete Mental Model", "order": 67},
        ],
    },

    "exercises": [
        {
            "id": "M01.L09.EX01",
            "title": "Design Live State and Interruption Controls",
            "lesson_code": "M01.L09",
            "section_id": "interruption-types",
            "placement": "after_section",
            "description": "Design a state model that distinguishes speech, task, and session actions.",
            "instructions": (
                "Create a state/control table for a live assistant.\n"
                "Include listening, assistant_speaking, tool_running, agent_working, input_required, reconnecting, completed, and failed.\n"
                "For each state define user-facing label, visual treatment, and allowed actions.\n"
                "Then explain the difference between mute, interrupt speech, revise scope, cancel work, and stop session."
            ),
            "expected_output": "A live-state table plus control semantics.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["live-agent-ux", "state-design", "interruptions"],
        },
        {
            "id": "M01.L09.EX02",
            "title": "Turn a Chat UI into a Live Workspace",
            "lesson_code": "M01.L09",
            "section_id": "ux-antipatterns",
            "placement": "after_section",
            "description": "Replace weak live-agent UX patterns with durable workspace surfaces.",
            "instructions": (
                "Start with a UI containing only transcript + spinner.\n"
                "Add: status strip, task card, activity timeline, source drawer, approval card, artifact panel, recovery banner, and resumable session view.\n"
                "For each component explain what user uncertainty it resolves.\n"
                "Identify and remove three anti-patterns from the original design."
            ),
            "expected_output": "A before/after UX architecture with rationale.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["task-cards", "workspace-design", "recovery"],
        },
        {
            "id": "M01.L09.EX03",
            "title": "Design an Agent Evaluation Dataset",
            "lesson_code": "M01.L09",
            "section_id": "agent-evaluation",
            "placement": "after_section",
            "description": "Extend a normal prompt catalog into an AgentOps evaluation catalog.",
            "instructions": (
                "Create five evaluation records for a support agent.\n"
                "For each include user input, expected tool, expected parameters, expected final answer behavior, latency target, and cost target.\n"
                "Add one tool-unit-test requirement and one human/LLM-as-a-judge criterion."
            ),
            "expected_output": "A five-row augmented evaluation catalog.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agentops", "evaluation", "tool-selection"],
        },
        {
            "id": "M01.L09.EX04",
            "title": "Design an Enterprise AgentOps Platform",
            "lesson_code": "M01.L09",
            "section_id": "production-principles",
            "placement": "after_section",
            "description": "Combine production UX and AgentOps infrastructure into one architecture.",
            "instructions": (
                "Design a platform with development, staging, and production environments.\n"
                "Include Prompt/Evaluation Catalog, Tool Registry, Agent Registry, Agents as a Service, short-term memory, long-term memory, CI/CD, monitoring, governance, and user-facing task UX.\n"
                "Explain how an agent version moves from development to production and how user feedback returns to evaluation."
            ),
            "expected_output": "An end-to-end AgentOps platform diagram and lifecycle explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agentops-platform", "registries", "ci-cd", "governance"],
        },
        {
            "id": "M01.L09.EX05",
            "title": "Audit Personalization and Accessibility",
            "lesson_code": "M01.L09",
            "section_id": "accessibility-review",
            "placement": "after_section",
            "description": "Check that personalization and multimodal interaction preserve user control.",
            "instructions": (
                "Audit a live assistant that remembers project context, prefers short voice answers, and can approve purchases.\n"
                "1. Make each personalization visible.\n"
                "2. Define its scope.\n"
                "3. Add a reversal control.\n"
                "4. Add keyboard/screen-reader/visual alternatives.\n"
                "5. Preserve explicit confirmation for high-risk purchases."
            ),
            "expected_output": "A personalization/accessibility risk-control matrix.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["personalization", "accessibility", "hitl"],
        },
        {
            "id": "M01.L09.EX06",
            "title": "Select a Foundation Model Systematically",
            "lesson_code": "M01.L09",
            "section_id": "model-selection",
            "placement": "after_section",
            "description": "Apply the source's three-step model-selection process.",
            "instructions": (
                "Create an approved reference table with three candidate FMs.\n"
                "Evaluate them on one custom use-case dataset using quality, latency, and cost.\n"
                "Then select one based on stated business priorities rather than highest accuracy alone.\n"
                "Explain why public leaderboard ranking was not sufficient."
            ),
            "expected_output": "A model-selection table plus decision rationale.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["genaiops", "model-evaluation", "business-tradeoffs"],
        },
    ],

    "quiz": {
        "id": "M01.L09.QZ01",
        "title": "Live Agent UX and AgentOps — Knowledge Check",
        "lesson_code": "M01.L09",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L09.Q01",
                "section_id": "ux-not-polish",
                "question": "What is the main UX problem in integrated live-agent systems?",
                "options": [
                    "Making system state understandable to the user",
                    "Showing every protocol packet",
                    "Maximizing the number of visible agents",
                    "Removing all visual controls",
                ],
                "correct": 0,
                "explanation": "The source frames UX as making active/pending/recoverable system state legible.",
            },
            {
                "id": "M01.L09.Q02",
                "section_id": "voice-screen",
                "question": "What is the source's core voice/visual rule?",
                "options": [
                    "Voice carries intent; screen carries durable detail",
                    "Everything should be spoken",
                    "Everything should be visual only",
                    "Voice should display tables",
                ],
                "correct": 0,
                "explanation": "Dense reviewable information is better preserved visually.",
            },
            {
                "id": "M01.L09.Q03",
                "section_id": "control-differences",
                "question": "Which action stops the assistant's current speech without necessarily canceling background work?",
                "options": ["Interrupt", "Cancel task", "Stop session", "Delete task"],
                "correct": 0,
                "explanation": "Speech interruption and task cancellation are separate controls.",
            },
            {
                "id": "M01.L09.Q04",
                "section_id": "activity",
                "question": "Which activity label is most appropriate for a normal user?",
                "options": [
                    "Research agent is collecting sources",
                    "A2A statusUpdate received",
                    "JSON-RPC request pending",
                    "MCP transport frame emitted",
                ],
                "correct": 0,
                "explanation": "The UI should translate protocol activity into user-meaningful work.",
            },
            {
                "id": "M01.L09.Q05",
                "section_id": "fake-progress",
                "question": "Why can a phase label be better than a numeric progress bar?",
                "options": [
                    "Some tasks do not have an honest measurable percentage",
                    "Percentages are never useful",
                    "Task cards cannot show numbers",
                    "Users dislike all progress",
                ],
                "correct": 0,
                "explanation": "Fake precision can reduce trust.",
            },
            {
                "id": "M01.L09.Q06",
                "section_id": "generative-ui",
                "question": "What is the stable generative-UI principle in the source?",
                "options": [
                    "Agents may propose surfaces, but the Host controls rendering",
                    "Agents should execute arbitrary JavaScript",
                    "Users should see raw protocol payloads",
                    "Every agent creates its own frontend",
                ],
                "correct": 0,
                "explanation": "Host-controlled component catalogs preserve safety and consistency.",
            },
            {
                "id": "M01.L09.Q07",
                "section_id": "hitl-ux",
                "question": "What should a strong approval prompt include?",
                "options": [
                    "Need, reason, consequence of approval, and alternatives/rejection path",
                    "Only an Approve button",
                    "Only a voice prompt",
                    "Only the internal tool name",
                ],
                "correct": 0,
                "explanation": "Reviewable decisions require context and consequences.",
            },
            {
                "id": "M01.L09.Q08",
                "section_id": "personalization",
                "question": "What are the three source rules for trustworthy personalization?",
                "options": [
                    "Visible, scoped, reversible",
                    "Hidden, global, permanent",
                    "Automatic, silent, irreversible",
                    "Fast, random, implicit",
                ],
                "correct": 0,
                "explanation": "User control depends on understanding and being able to change adaptation.",
            },
            {
                "id": "M01.L09.Q09",
                "section_id": "accessibility",
                "question": "Which statement best matches the source?",
                "options": [
                    "Critical interactions should have alternative modality paths",
                    "Voice alone solves accessibility",
                    "High-risk review can be skipped for accessibility",
                    "Keyboard support is unnecessary in multimodal apps",
                ],
                "correct": 0,
                "explanation": "Accessibility is integrated into state, approval, recovery, and controls.",
            },
            {
                "id": "M01.L09.Q10",
                "section_id": "production-shift",
                "question": "How does the source present AgentOps relative to MLOps and GenAIOps?",
                "options": [
                    "As an additive evolution that builds on them",
                    "As a total replacement",
                    "As unrelated to software operations",
                    "As only a UX discipline",
                ],
                "correct": 0,
                "explanation": "Earlier operational layers remain necessary.",
            },
            {
                "id": "M01.L09.Q11",
                "section_id": "creators-consumers",
                "question": "Which group primarily uses GenAIOps in the source's framing?",
                "options": [
                    "Model consumers building applications with foundation models",
                    "Only chip manufacturers",
                    "Only model-training researchers",
                    "Only data-center operators",
                ],
                "correct": 0,
                "explanation": "GenAIOps focuses on productionizing applications that consume FMs.",
            },
            {
                "id": "M01.L09.Q12",
                "section_id": "agentops-challenges",
                "question": "Which challenge is unique enough to motivate AgentOps?",
                "options": [
                    "Autonomous tool selection and action sequencing",
                    "Serving static HTML",
                    "Compiling Python",
                    "Image resizing only",
                ],
                "correct": 0,
                "explanation": "Agent autonomy introduces path-level operational complexity.",
            },
            {
                "id": "M01.L09.Q13",
                "section_id": "model-selection",
                "question": "Why should model selection not rely only on highest accuracy?",
                "options": [
                    "Business decisions also consider cost and latency/speed",
                    "Accuracy has no value",
                    "Only licensing matters",
                    "The cheapest model is always best",
                ],
                "correct": 0,
                "explanation": "The source describes a trade-off among performance and business priorities.",
            },
            {
                "id": "M01.L09.Q14",
                "section_id": "prompt-catalog",
                "question": "What is a prompt catalog used for?",
                "options": [
                    "A curated evaluation dataset of prompts and expected/reference behavior",
                    "A tool execution sandbox",
                    "A network load balancer",
                    "An Agent Card registry only",
                ],
                "correct": 0,
                "explanation": "It grows into a repeatable custom evaluation dataset.",
            },
            {
                "id": "M01.L09.Q15",
                "section_id": "evaluation-metrics",
                "question": "What can be used when labeled data is unavailable?",
                "options": [
                    "Human evaluation and LLM-as-a-judge",
                    "Only precision/recall",
                    "No evaluation at all",
                    "Only cost measurement",
                ],
                "correct": 0,
                "explanation": "The source presents human review and LLM judges as alternatives when labels are scarce.",
            },
            {
                "id": "M01.L09.Q16",
                "section_id": "agent-evaluation",
                "question": "What does AgentOps evaluation add beyond normal GenAI output evaluation?",
                "options": [
                    "Tool selection, parameters, trajectory, and operational metrics",
                    "Only UI color testing",
                    "Only model parameter counts",
                    "Only prompt length",
                ],
                "correct": 0,
                "explanation": "Agent quality depends on the execution path as well as the final answer.",
            },
            {
                "id": "M01.L09.Q17",
                "section_id": "tool-registry",
                "question": "What is a Tool Registry primarily for?",
                "options": [
                    "Central discovery, governance, ownership, versioning, and reuse of tools",
                    "Replacing every tool with one model",
                    "Only storing source code comments",
                    "Making tools invisible",
                ],
                "correct": 0,
                "explanation": "The registry is a governed source of truth.",
            },
            {
                "id": "M01.L09.Q18",
                "section_id": "agent-registry",
                "question": "What can an Agent Registry help store?",
                "options": [
                    "Agent identity, skills, versions, endpoints, owners, and Agent Cards",
                    "Only user passwords",
                    "Only model weights",
                    "Only frontend CSS",
                ],
                "correct": 0,
                "explanation": "Registries support discovery and governance across many agents.",
            },
            {
                "id": "M01.L09.Q19",
                "section_id": "memory-governance",
                "question": "Why is long-term memory an AgentOps governance concern?",
                "options": [
                    "It persists user/project information across time and affects privacy and behavior",
                    "It cannot contain data",
                    "It is always temporary",
                    "It eliminates the need for security",
                ],
                "correct": 0,
                "explanation": "Persistent memory requires policy, lifecycle, and privacy controls.",
            },
            {
                "id": "M01.L09.Q20",
                "section_id": "agents-as-service",
                "question": "What does Agents as a Service mean?",
                "options": [
                    "Deploying agents as independently managed reusable services",
                    "Embedding every agent permanently in one frontend component",
                    "Training a new foundation model for every agent",
                    "Removing CI/CD",
                ],
                "correct": 0,
                "explanation": "Independent services improve reuse, deployment, ownership, and discovery.",
            },
            {
                "id": "M01.L09.Q21",
                "section_id": "ux-agentops-connection",
                "question": "Why are UX and AgentOps connected?",
                "options": [
                    "Visible progress, failures, approvals, and provenance depend on reliable operational state underneath",
                    "They are completely unrelated",
                    "UX can invent backend state",
                    "AgentOps only controls visual styling",
                ],
                "correct": 0,
                "explanation": "Trustworthy UI requires trustworthy system state and observability.",
            },
            {
                "id": "M01.L09.Q22",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design a production live multi-agent product and its AgentOps platform. "
                    "Explain live state UX, task cards, activity, approvals, errors, provenance, personalization, "
                    "accessibility, evaluation datasets, model selection, tool and agent registries, memory, Agents "
                    "as a Service, CI/CD, monitoring, governance, and the feedback loop from production back to evaluation."
                ),
            },
        ],
        "passing_score": 70,
    },
}
