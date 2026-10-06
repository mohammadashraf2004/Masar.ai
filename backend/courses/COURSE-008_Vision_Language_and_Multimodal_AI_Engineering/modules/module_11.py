"""M01.L11 — Agentic VLMs and Vision-Language-Action Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 11, "Advanced Topics and Cutting-Edge Research".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L11"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Extend VLMs from passive perception to action. Learn agent loops, tool use, "
    "computer-use agents, GUI localization and control, production agent design, "
    "and vision-language-action models for robotics with imitation learning, "
    "action chunks, asynchronous control, and flow-matching action experts."
)
SOURCE_CHAPTER = 11
SOURCE_PAGES = "Chapter 11 — page numbers not provided"


TOPIC = {
    "title": "Agentic VLMs and Vision-Language-Action Models",
    "slug": "vision-language-m01-l11",
    "description": (
        "Learn how VLMs move from seeing and describing to taking action. Build an "
        "understanding of the agency spectrum, ReAct loops, tool use, computer-use "
        "agents, screenshot feedback, GUI localization, production agent security, "
        "robot imitation learning, VLA action heads, asynchronous action chunks, "
        "robotics data quality, and modern VLA model trade-offs."
    ),
    "order": 11,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "agentic-vlms",
        "agents",
        "tool-calling",
        "react",
        "smolagents",
        "computer-use-agents",
        "gui-localization",
        "screenshot-agents",
        "agent-evaluation",
        "agent-security",
        "vision-language-action",
        "robotics",
        "imitation-learning",
        "teleoperation",
        "proprioception",
        "action-chunks",
        "flow-matching",
        "diffusion-policy",
        "asynchronous-control",
        "vla-data",
        "action-expert",
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
        "M01.L10",
    ],

    "lesson": {
        "title": "Agentic VLMs and Vision-Language-Action Models",
        "content": r"""
# Agentic VLMs and Vision-Language-Action Models

> **Lesson:** M01.L11  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 11, *Advanced Topics and Cutting-Edge Research*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## From seeing to doing

A VLM can answer:

```text
"What is on the screen?"
```

An agentic VLM can go further:

```text
"Click the correct button."
"Fill the form."
"Search the website."
"Use a tool."
```

A vision-language-action model goes further still:

```text
"Pick up the cup."
"Fold the shirt."
"Pour the coffee."
```

These systems look very different on the surface.

One manipulates:

```text
software
```

The other manipulates:

```text
the physical world
```

But the chapter's central idea is that both follow the same loop:

```text
OBSERVE
   ↓
DECIDE
   ↓
ACT
   ↓
OBSERVE AGAIN
```

For a computer-use agent:

```text
observation = screenshot
action      = click / type / scroll / tool call
```

For a robot:

```text
observation = camera + language + proprioception
action      = future joint/gripper set-points
```

That shared loop connects the two halves of the chapter.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Define an agent using the chapter's model-in-a-loop-with-tools framing.
- Explain why agency is a spectrum rather than a binary feature.
- Distinguish tool selection, tool calling, and a multistep ReAct loop.
- Explain the think → act → observe → memory → continue/stop cycle.
- Decide when an agent loop is justified and when deterministic code is better.
- Explain why open-ended reasoning and deterministic operations should be separated.
- Evaluate agents at the step level and task level.
- Describe the core memory objects in a multistep agent lifecycle.
- Distinguish code-generating agents from structured tool-calling agents.
- Explain why tool descriptions matter.
- Explain how external specialist models can become agent tools.
- Compare local and hosted model-connection strategies conceptually.
- Explain why screenshot-based computer-use agents exist despite their brittleness.
- Distinguish GUI localization models from agentic GUI-control models.
- Explain normalized click coordinates.
- Convert normalized GUI coordinates back to image pixels.
- Explain the role of a GUI action-space system prompt.
- Explain how screenshot callbacks close the observation step in browser agents.
- Explain why stale screenshots should be pruned from context.
- Describe a production agent control-plane architecture.
- Explain why permissions, session management, queueing, and dispatch should often remain deterministic.
- Explain security risks created by tool access, third-party extensions, and untrusted web content.
- Define a VLA as a policy mapping observations to actions.
- Distinguish classical explicit robot control from learned implicit policies.
- Compare reinforcement learning with imitation learning for robotics.
- Define policy, proprioception, episode, action chunk, flow matching, diffusion transformer, and teleoperation.
- Explain what a VLA observation contains.
- Explain why VLA outputs are controller set-points rather than raw motor voltages.
- Explain why modern VLAs predict chunks of actions.
- Quantify the compute benefit of action chunking.
- Explain asynchronous robot control with an action queue.
- Explain why robotics datasets require precise multimodal time synchronization.
- Explain why corrupted robot-state measurements are much more dangerous than ordinary noisy web data.
- Describe a VLA dataset validation pipeline.
- Explain how a VLM becomes a VLA by adding state information and an action expert.
- Explain why the VLM context can be cached during iterative action generation.
- Describe a flow-matching/diffusion action head.
- Explain the common VLA processing pipeline.
- Compare the chapter's three VLA examples: π0.6, GR00T N1.5, and SmolVLA.
- Explain advantage conditioning in π0.6.
- Explain the dual-system pattern in GR00T N1.5.
- Explain how SmolVLA reduces compute through a small backbone, truncated features, and token reduction.
- Connect digital agent design and physical-action model design through the observe-decide-act loop.

---

## 1. The shift from perception to action

The previous chapters focused on models that:

```text
understand
retrieve
generate
```

This chapter asks:

> What happens when the model's output changes the world?

Digital action examples:

- clicking buttons;
- typing;
- filling forms;
- searching;
- creating files;
- calling APIs.

Physical action examples:

- moving a robot arm;
- closing a gripper;
- stacking objects;
- pouring liquid.

The stakes also change.

A wrong caption is inconvenient.

A wrong API call can alter data.

A wrong robot action can damage hardware.

So action-capable systems need more than model quality.

They need:

- control structure;
- evaluation;
- validation;
- security;
- fallbacks.

---

## 2. What is an agent?

The source gives a practical working definition:

```text
LLM
running in a loop
with access to tools
```

The **loop** is essential.

A one-shot model can answer:

```text
"Use tool X."
```

An agent can:

```text
reason
→ call tool X
→ inspect result
→ revise plan
→ call tool Y
→ inspect result
→ stop when goal is complete
```

So agency comes from:

```text
decision
+
action
+
feedback
+
repetition
```

---

## 3. Agency is a spectrum

The chapter presents increasing levels of autonomy.

### Level 1 — Tool selection

The model chooses which operation should run.

Example:

```text
"translate this"
→ translation function
```

### Level 2 — Tool calling

The model produces structured arguments.

Example:

```json
{
  "city": "Bern"
}
```

for a weather function.

### Level 3 — Multistep loop

The model repeatedly:

```text
thinks
acts
observes
updates memory
continues
```

until completion.

### Important lesson

More autonomy is not automatically better.

The correct design question is:

> **How much open-ended reasoning does this task actually require?**

[[IMAGE_NEEDED: Agency spectrum |
Show tool routing → structured tool calling → multistep ReAct agent, with
increasing autonomy and increasing complexity/risk |
Learner should understand that agency is a design continuum]]

---

## 4. The ReAct loop

The chapter describes this cycle.

### Step 1 — Receive task

```text
user instruction
```

### Step 2 — Think / plan

The model decides:

- what is known;
- what is missing;
- which tools might help;
- what to do next.

### Step 3 — Act

Execute a tool/action.

### Step 4 — Observe

Read:

- tool output;
- screenshot;
- error;
- external state.

### Step 5 — Decide

If goal is complete:

```text
return final answer
```

Otherwise:

```text
store useful state
→ continue loop
```

Conceptually:

```text
TASK
 ↓
THINK
 ↓
ACT
 ↓
OBSERVE
 ↓
DONE?
 ├─ yes → FINAL
 └─ no  → MEMORY → THINK
```

[[IMAGE_NEEDED: ReAct loop |
Show task → think/plan → action/tool → observation → completion decision →
either final answer or memory and another cycle |
Learner should understand feedback as the defining feature of agent behavior]]

---

## 5. When do you actually need an agent?

The source explicitly warns that not every application requires an agent.

If one tool call solves the problem:

```text
use one tool call
```

Example:

```text
choose one image-processing command
→ execute it
```

No complex loop is necessary.

An agent becomes useful when the workflow requires:

- multiple dependent steps;
- external state;
- failures/retries;
- dynamic planning;
- changing information.

---

## 6. Separate open-ended reasoning from deterministic operations

The source's GPU-provider example includes tasks such as:

```text
research providers
navigate sites
check internal spend
compare results
draft email
create reminder
```

Some steps need reasoning.

Others are deterministic.

Example:

```text
internal billing value
```

If an API exists, call it directly.

Do not force a visual agent to fight through:

- login pages;
- popups;
- two-factor prompts;

when a reliable API exists.

The chapter's rule is:

> **At scale, implement deterministic parts deterministically and give the
> agent the open-ended parts.**

{{exercise:M01.L11.EX01}}

---

## 7. Why feedback loops matter

Open-ended workflows fail in unpredictable ways.

The source gives examples:

### Dynamic site flow

A price may require using a calculator.

The agent must adapt.

### CAPTCHA or anti-automation barrier

The visual path may fail.

### Login / two-factor prompt

Use a deterministic alternative if available.

### Hallucinated fact in a draft

Add a verification step.

This is why robust agents need:

```text
reasoning
+
observation
+
verification
+
fallbacks
```

not only tool access.

---

## 8. Evaluating agents

The chapter separates two evaluation levels.

### Step-level grounding

Question:

```text
Did the agent take the correct action now?
```

For GUI agents:

- correct button?
- correct coordinates?
- correct text field?
- correct action type?

Localization can be measured geometrically.

Agentic action correctness may require semantic comparison.

### Task-level success

Question:

```text
Did the whole job finish correctly?
```

Examples:

- form was submitted;
- file exists;
- booking completed;
- database value changed;
- email contains correct content.

Task-level evaluation can require:

- verifiable final state;
- human judgment.

---

## 9. Why traces matter

To debug an agent, log each action.

A useful trace contains:

```text
observation
reasoning/plan
selected action
action arguments
tool result
new observation
completion state
```

This lets you distinguish:

```text
bad perception
from
bad decision
from
bad tool execution
```

A final success/failure number alone cannot explain why the run failed.

---

## 10. Agent frameworks are abstraction choices

The source provides a framework comparison labeled as an **early-2026 snapshot**.

It covers examples such as:

- smolagents;
- LangChain;
- LangGraph;
- LlamaIndex;
- Haystack;
- CrewAI;
- Semantic Kernel.

Treat that table as the book's time-specific ecosystem snapshot, not as a
permanent ranking.

The durable question is:

> What abstraction does your workload need?

Examples from the source:

```text
graph persistence/orchestration
→ graph-oriented framework

RAG-heavy application
→ framework strong in retrieval/evaluation

multiagent role coordination
→ multiagent-oriented framework

vision-agent learning/prototyping
→ lightweight multimodal agent framework
```

---

## 11. Why the chapter uses smolagents

The source gives three main reasons.

### Small and readable

Agent loops are easier to learn if the framework is not hidden beneath many
layers.

### Multimodal observations

Images can flow through agent memory.

This is important for computer-use agents.

### CodeAgent

Instead of only outputting JSON tool calls, the agent can write/execute Python
to compose tools and manipulate data.

The source still recommends other frameworks when production requirements call
for:

- complex branching;
- approval gates;
- heavy retrieval;
- richer persistence.

---

## 12. CodeAgent versus ToolCallingAgent

The source describes two action styles.

### CodeAgent

Model writes executable Python.

Strength:

```text
composition and flexibility
```

It can:

- call multiple tools;
- calculate;
- parse;
- transform outputs.

### ToolCallingAgent

Model produces structured tool calls.

Strength:

```text
clear schema and controlled interface
```

This is closer to standard function calling.

Trade-off:

```text
code execution
→ powerful but larger execution/security surface

structured tools
→ more constrained but easier to validate
```

---

## 13. A toy tool-using agent

The source defines a small addition tool.

A source-aligned educational version:

```python
from smolagents import (
    Tool,
    CodeAgent,
    InferenceClientModel,
)


class AdditionTool(Tool):
    name = "addition_tool"

    description = (
        "Adds two numbers together"
    )

    inputs = {
        "first_number": {
            "type": "integer",
            "description": (
                "first number to add"
            ),
        },
        "second_number": {
            "type": "integer",
            "description": (
                "second number to add"
            ),
        },
    }

    output_type = "integer"

    def forward(
        self,
        first_number,
        second_number,
    ):
        return (
            first_number
            + second_number
        )


model = InferenceClientModel()

agent = CodeAgent(
    tools=[AdditionTool()],
    model=model,
)

result = agent.run(
    "What is 41 plus 1?"
)
```

The important part is not the arithmetic.

It is the lifecycle.

---

## 14. The agent lifecycle in memory

The source describes four memory step classes.

### TaskStep

Stores the original user instruction.

Can include images.

### PlanningStep

Stores a high-level plan when planning is enabled.

### ActionStep

Stores one think-act-observe cycle.

May contain:

- model output;
- tool calls;
- text observations;
- image observations.

### FinalAnswerStep

Stores the final result.

Conceptually:

```text
TaskStep
  ↓
PlanningStep (optional)
  ↓
ActionStep
  ↓
ActionStep
  ↓
...
  ↓
FinalAnswerStep
```

---

## 15. Images can be observations

For a vision agent, observation is not limited to text.

A screenshot can enter the next cycle as:

```text
observations_images
```

This turns a normal tool agent into a visual feedback agent.

Example:

```text
click
→ screenshot changes
→ image added to memory
→ VLM inspects new screen
→ next action
```

That is the basis of screenshot-driven computer use.

---

## 16. Models can become tools

The chapter demonstrates wrapping a hosted image-generation model as an agent
tool.

The deeper idea is:

> The agent does not need to contain every capability internally.

Instead:

```text
agent
→ chooses specialist
→ specialist returns result
→ agent reasons over result
```

The same pattern can support:

- image generation;
- OCR;
- speech recognition;
- document parsing;
- retrieval.

This creates a compositional system of expert models.

---

## 17. The agent framework can be model-agnostic

The source lists ways to connect:

### Local models

- Transformers runtime;
- Apple-Silicon-oriented runtime;
- vLLM server.

### Hosted models

- inference provider/client;
- OpenAI-compatible server;
- API abstraction layer.

The durable architecture lesson:

```text
agent loop
≠
specific model provider
```

Separate:

```text
reasoning interface
from
model-serving backend
```

This makes infrastructure replaceable.

---

## 18. Why computer-use agents exist

Traditional UI automation often uses:

- selectors;
- HTML structure;
- scripted browser automation.

These approaches can be brittle when:

- layouts change;
- critical information is visual;
- the app is not web/DOM based;
- selectors are unavailable.

A VLM can instead operate from:

```text
screenshots
```

This imitates how a human uses a GUI.

But the source emphasizes that screenshot-based approaches are generally more
brittle than structured API/tool interaction.

---

## 19. Structured APIs versus screenshot-based computer use

The source describes multiple approaches in an early-2026 snapshot.

### API/tool agents

```text
structured request
→ structured software action
```

Most reliable when APIs exist.

### Screenshot-based commercial systems

```text
screenshot
→ model action
```

Useful when APIs do not exist.

### Open research models

Open-weight systems can be fine-tuned/deployed by developers.

The source's broader lesson:

> Prefer deterministic structured interfaces where available; use GUI vision
> when the environment forces you to act visually.

---

## 20. Localization model versus agentic GUI model

The chapter separates two capabilities.

### Localization model

Question:

```text
"Where should I click?"
```

Output:

```text
x, y
```

It solves perception/localization.

### Agentic control model

Question:

```text
"What should I do next?"
```

Output can include:

- click;
- scroll;
- drag;
- type;
- multiple actions.

It combines:

```text
reasoning
+
action selection
+
localization
```

[[IMAGE_NEEDED: GUI localization versus agentic control |
Left: screenshot + target → one predicted click coordinate.
Right: screenshot + goal → reasoning model chooses multiple UI actions over
several steps |
Learner should distinguish perception/localization from full control]]

---

## 21. GUI localization with normalized coordinates

The source uses a model that returns coordinates normalized to:

```text
0 ... 1000
```

Example output:

```text
x = 549
y = 395
```

This is not yet a raw pixel coordinate.

If processed image size is:

```text
W × H
```

convert:

```text
pixel_x = x / 1000 × W
pixel_y = y / 1000 × H
```

Normalization makes the action representation less dependent on screenshot
resolution.

{{exercise:M01.L11.EX02}}

---

## 22. Screenshot preprocessing and coordinate consistency

The source resizes a screenshot before localization.

Why must the click be interpreted against the processed image?

Because the model predicts coordinates in the geometry it saw.

Pipeline:

```text
original screenshot
→ model-specific resize
→ VLM localization
→ normalized coordinate
→ processed-image pixel coordinate
```

If you later need to click in the original environment, convert coordinates
back consistently.

This is the same geometric principle learned earlier for bounding-box scaling.

---

## 23. Structured GUI outputs

The source validates localization output using a schema.

Conceptually:

```python
class ClickCoordinates(BaseModel):
    x: int
    y: int
```

with bounds:

```text
0 ≤ x ≤ 1000
0 ≤ y ≤ 1000
```

Why structured output?

It lets the application reject:

- malformed text;
- missing fields;
- impossible coordinates.

For action systems, schema validation is part of the safety boundary.

---

## 24. Source prompt-formatting note

The supplied Holo2 snippet spreads string concatenation across lines with leading
`+` operators outside a clear parenthesized expression.

The intended prompt is structurally:

```python
prompt = (
    "Localize an element on the GUI image "
    "according to the provided target and "
    "output a click position. "
    "* You must output valid JSON following "
    f"the format: {ClickCoordinates.model_json_schema()} "
    "Your target is:"
)
```

This lesson normalizes only that mechanical Python formatting issue.

The source's intended conditioning remains unchanged.

---

## 25. Agentic computer-use action spaces

A full GUI-control model needs more than coordinates.

The source shows an action space including operations such as:

```text
click
double click
right click
move
drag
swipe
long press
```

These action definitions are placed in the model's system prompt.

That tells the model:

```text
what actions exist
what arguments they accept
how output should be formatted
```

This is effectively a tool schema embedded in natural-language/code form.

---

## 26. Constrain actions to valid primitives

The chapter's GUI system prompt includes rules such as:

```text
only output defined actions
avoid invalid states
wrap actions in expected tags
```

This is important.

Without a constrained action space, the model may produce:

- unsupported commands;
- malformed actions;
- ambiguous text.

The execution layer should parse/validate before acting.

Never assume natural-language output is executable just because it "looks right."

---

## 27. One task may require multiple GUI actions

The source shows a date-range request resulting in two clicks.

Conceptually:

```text
goal:
select July 3 → July 6

output:
click(start_date)
click(end_date)
```

This illustrates a difference from pure localization.

A full agentic GUI model must reason about:

```text
task structure
+
action ordering
```

not just find one element.

---

## 28. Coordinate conventions are model-specific

The Holo localization example explicitly uses:

```text
0–1000 normalized coordinates
```

The separate agentic GUI example emits `click(x=..., y=...)` values in its own
model/action convention.

Do **not** assume all GUI models use the same coordinate system.

Always inspect:

- training convention;
- model card;
- screenshot resizing;
- execution environment.

A correct action in the wrong coordinate frame is still a wrong action.

---

## 29. The visual browser agent

The source connects the ReAct loop to a real browser.

Three pieces matter:

```text
1. screenshot callback
2. action-space/system instructions
3. outer agent loop
```

The specific automation library is less important than this architecture.

---

## 30. Screenshot callback closes the observation step

After an action:

```text
click
```

the page changes.

The agent must see the new state.

The source's callback:

- waits briefly;
- captures screenshot;
- stores screenshot in `observations_images`;
- stores current URL as text observation.

Conceptually:

```text
ACTION
→ ENVIRONMENT CHANGES
→ SCREENSHOT
→ OBSERVATION
→ NEXT REASONING STEP
```

Without this callback, the visual agent would be acting blindly after the first
step.

---

## 31. Prune stale screenshots

A multistep visual agent can accumulate many screenshots.

If every old screenshot remains in context:

```text
context window grows
cost rises
stale states distract model
```

The source describes clearing older screenshots after a small number of cycles.

This is a general multimodal-memory principle:

> Keep enough visual history to understand recent change, but do not blindly
> retain every frame.

---

## 32. System prompts are behavioral guardrails

The source's browser example gives practical instructions such as:

```text
act
→ observe what happened
→ then continue
```

and defines which navigation method to use for certain tasks.

These heuristics reduce common failures such as:

- executing too many blind actions;
- assuming a click succeeded;
- repeatedly fighting an impossible login flow.

Guardrails shape the agent's policy before any model weight changes.

---

## 33. Production agents need a deterministic control plane

The chapter's production case study maps agent concepts into a larger runtime.

A robust system may separate:

### Agent reasoning

```text
what should happen next?
```

### Control plane

```text
session management
permissions
tool dispatch
run queueing
memory persistence
```

{{image:agent-runtime-control-plane}}

The source's core principle is consistent:

> **Do not make the LLM responsible for deterministic infrastructure behavior
> that normal software can handle reliably.**

---

## 34. Tool bundles and skills

The source describes packaged skills as versioned tool bundles.

Conceptually:

```text
skill
=
tools
+
usage instructions
+
metadata
```

Benefits:

- reuse;
- installation;
- discovery;
- versioning.

But reusable third-party capabilities also create a supply-chain/security
boundary.

---

## 35. Long-term and session memory

The production case study describes two memory layers.

### Long-term memory

Editable persistent files.

### Session transcripts

Structured per-run logs.

This distinction is useful:

```text
durable user/project knowledge
vs
temporary execution history
```

Agents need memory policies, not just "more context."

---

## 36. Tool access creates a security boundary

The source uses its production case study as a caution.

When an agent can combine:

```text
web content
+
third-party extensions
+
filesystem/API/tools
```

an attacker may try to influence actions through untrusted content.

Risks mentioned by the source include:

- prompt injection;
- malicious extensions;
- data exfiltration.

The architectural lesson:

```text
permissions
validation
tool isolation
trusted extension policy
```

must be designed before deployment.

[[IMAGE_NEEDED: Agent trust boundary |
Show untrusted web content and third-party tools outside a security boundary,
with a permission/validation layer before sensitive tools, files, or APIs |
Learner should understand why tool-capable agents need explicit trust controls]]

---

## 37. From digital agents to physical action

The second half of the chapter makes a powerful analogy.

Digital agent:

```text
screenshot
+
goal
→
tool action
```

VLA:

```text
camera views
+
instruction
+
robot state
→
physical action
```

In both:

```text
observe
decide
act
observe again
```

The main difference is the action space.

---

## 38. Three broad approaches to robot behavior

The source contrasts a classical explicit approach with learned approaches.

### Classical explicit modeling

Pipeline:

```text
perception
→ planning
→ control
```

Strengths:

- interpretable;
- predictable in controlled environments;
- easy to inspect module by module.

Weakness:

- assumptions can fail in messy real scenes.

### Reinforcement learning

Learns from:

```text
reward
+
interaction
```

Useful when simulation provides many cheap trials.

### Imitation learning

Learns from:

```text
human demonstrations
```

This is the chapter's main VLA training path.

---

## 39. Why classical robotics still matters

The source does not argue that VLA methods replace classical robotics
everywhere.

Classical control is excellent when:

- geometry is known;
- objects are rigid;
- fixtures are stable;
- tolerances are controlled.

Example:

```text
high-volume industrial pick-and-place
```

The weakness appears when real-world assumptions break:

- transparent object;
- deformable object;
- unexpected friction;
- unusual lighting.

So architecture choice depends on environment variability.

---

## 40. Reinforcement learning in robotics

Robotic RL can be powerful where simulation is cheap.

Example:

```text
legged locomotion
```

Millions of simulated interactions can teach non-obvious strategies.

But real-world RL is expensive because:

- hardware can break;
- experiments are slow;
- reward design is difficult.

This makes RL less convenient for some everyday manipulation tasks.

---

## 41. Imitation learning

Imitation learning uses expert demonstrations.

A human teleoperates the robot.

Training data records:

```text
what robot saw
+
robot internal state
+
action human executed
```

Then the policy learns:

```text
observation
→ action
```

A pretrained VLM provides useful prior knowledge about:

- objects;
- language;
- spatial relationships.

So VLA adaptation can start from stronger representations than training a robot
policy from scratch.

---

## 42. Essential robotics vocabulary

### Policy

A function:

```text
observations
→ actions
```

### Proprioception

Robot's internal body state.

Examples:

- joint angle;
- joint velocity;
- gripper state.

### Episode

One complete demonstration from start to finish.

### Action chunk

A predicted sequence of future actions.

### Flow matching

Iterative generation method for continuous action vectors.

### Diffusion transformer

Transformer used as an iterative action generator.

### Teleoperation

Human controls the robot to record expert demonstrations.

---

## 43. What a VLA observes

Typical observation includes:

### Multi-view RGB

Examples:

- base camera;
- left wrist camera;
- right wrist camera.

### Language instruction

Example:

```text
"Stack the red block on the blue block."
```

### Proprioception

Examples:

```text
joint positions
joint velocities
gripper state
```

The VLA combines:

```text
external perception
+
goal
+
internal body state
```

---

## 44. What a VLA outputs

A common misunderstanding is that the model directly controls motor voltage.

The source explains that the VLA usually predicts controller set-points.

Example:

```text
joint 0 target = 1.2 radians
gripper target = closed
```

A lower-level controller handles:

- motor voltage;
- torque;
- fast stabilization.

This abstraction makes the learned policy more manageable.

---

## 45. Why predict action chunks?

Instead of predicting:

```text
one action
```

modern VLAs often predict:

```text
next H actions
```

Example:

```text
[a_t, a_t+1, ..., a_t+9]
```

This reduces how often the expensive VLA must run.

---

## 46. Action chunking can dramatically reduce inference demand

The source gives the intuition:

Suppose:

```text
control frequency = 50 Hz
```

and action generation requires:

```text
5–10 denoising forward passes
```

One-action-at-a-time generation could require:

```text
50 × 5 = 250
to
50 × 10 = 500

model forward passes / second
```

If each model inference predicts:

```text
10 future actions
```

then policy generation only needs roughly:

```text
5 Hz
```

for the same 50 Hz action stream.

That is approximately a:

```text
10× reduction
```

in high-level generation frequency.

{{exercise:M01.L11.EX03}}

---

## 47. Asynchronous robot control

Action chunking enables pipelining.

Conceptually:

```text
GPU generates chunk B
while
robot executes chunk A
```

The robot maintains:

```text
action queue
```

When queue length drops below a threshold:

```text
send new observation
→ request next chunk
```

Goal:

```text
queue never becomes empty
```

so robot motion does not stall waiting for inference.

{{image:vla-asynchronous-control}}

---

## 48. VLA data is a calibrated experiment

Web-scale VLM datasets can tolerate some noise.

Robot datasets cannot tolerate the same kind of misalignment.

A training example may combine:

```text
camera frames
joint angles
joint velocities
gripper state
executed action
```

All must correspond to the same moment.

If timestamps drift:

```text
image at t=1.50 s
paired with
state/action at t=1.58 s
```

the model learns an incorrect observation-action relationship.

---

## 49. Complete episodes and variation

Manipulation skills unfold over time.

For pouring:

```text
reach
grasp
lift
tilt
monitor
stop
```

Training needs complete demonstrations.

It also needs variation.

Example:

- mug moved left/right;
- object orientation changed;
- starting height changed.

Otherwise the policy may memorize one trajectory rather than learn the task.

---

## 50. Validate robotics data aggressively

The source recommends checking that:

- all camera streams recorded;
- expected frame rate was maintained;
- proprioception stayed within physical bounds;
- commanded actions really executed;
- safety stops/limits are recorded;
- streams stayed synchronized;
- clocks did not drift.

A corrupted text sample may lower model quality.

A corrupted action target can teach unsafe motion.

This makes robot data quality a systems/safety problem.

{{exercise:M01.L11.EX04}}

---

## 51. From VLM to VLA

Architecturally, the source says a VLA often begins as a pretrained VLM.

The VLM already processes:

```text
visual tokens
+
language tokens
```

A VLA adds:

```text
robot state tokens
+
action generation
```

So input may contain:

```text
camera 1 tokens
camera 2 tokens
instruction tokens
proprioception tokens
```

The major new component is the:

```text
action expert
```

---

## 52. The action expert

The action expert is usually a separate transformer trained with:

- diffusion;
- flow matching.

Output:

```text
future action chunk
```

Conceptually:

```text
VLM context
→ semantic/visual state
→ action expert
→ [a_t ... a_t+H-1]
```

The source notes that the VLM can run at a slower frequency than the action
system.

---

## 53. Common VLA pipeline

The chapter gives a common recipe.

### Step 1 — Encode observation

```text
images
→ visual tokens

instruction
→ text tokens

robot state
→ proprioception/state tokens
```

### Step 2 — Run VLM

Fuse those tokens into contextual hidden representations.

### Step 3 — Cache VLM context

Treat VLM outputs as fixed conditioning during iterative action generation.

### Step 4 — Refine action chunk

Start from noisy/random action vectors.

Repeat:

```text
action self-attention
+
cross-attention to cached VLM context
+
update toward target action
```

### Step 5 — Execute

Push clean action chunk into robot action queue.

{{image:groot-dual-system-vla}}
{{image:groot-n15-action-expert}}
{{image:pi06-advantage-conditioning}}

---

## 54. Why cache the VLM context?

Diffusion/flow matching requires multiple refinement steps.

If the VLM observation does not change inside those refinement steps, rerunning
the full VLM is wasteful.

Instead:

```text
run VLM once
→ cache context K/V/features

for each action denoising step:
reuse VLM context
```

Only the action-query representation changes.

This makes iterative action generation cheaper.

The idea directly echoes KV-cache reasoning from language-model inference.

---

## 55. Use earlier/middle VLM features when speed matters

The source notes that some VLAs do not always wait for the final VLM layer.

Why?

Later layers cost compute.

Intermediate features may already contain enough:

- visual semantics;
- instruction grounding;
- object relationships;

to condition a controller.

Trade-off:

```text
earlier layer
→ faster
→ potentially less abstract semantic processing

later layer
→ richer representation
→ more cost
```

---

## 56. Three VLA design points

The chapter compares:

```text
π0.6
GR00T N1.5
SmolVLA
```

They share the broad pattern:

```text
pretrained VLM
+
action head
```

but optimize for different goals.

### π0.6

Focus:

```text
learn from experience and outcomes
```

### GR00T N1.5

Focus:

```text
foundation model across robot embodiments
```

### SmolVLA

Focus:

```text
efficiency and accessible hardware
```

---

## 57. π0.6: learning from experience

The source describes two important ideas.

### Broad offline training

Learn from large recorded multirobot datasets.

### Advantage conditioning

A separate value function estimates whether an outcome was:

```text
better than expected
or
worse than expected
```

This is converted into simple conditioning such as:

```text
Advantage: positive
Advantage: negative
```

The policy can then learn to favor behavior associated with successful outcomes.

---

## 58. Improvement through rollout feedback

The chapter's described adaptation loop is roughly:

```text
collect demonstrations
→ run policy on robot
→ record success and failure
→ optionally record human interventions
→ update value function
→ update advantage labels
→ fine-tune policy
```

This turns deployment experience into training signal.

It is a bridge between:

- imitation;
- offline RL-style evaluation;
- continual improvement.

---

## 59. GR00T N1.5: dual-system VLA

The source describes a split-frequency architecture.

### VLM side

Runs relatively slowly.

Processes:

- vision;
- instruction;
- context.

### Action head

Runs at much higher frequency.

Uses a DiT-style flow-matching policy.

Cross-attends to:

```text
frozen VLM tokens
+
embodiment-specific state
```

This separates:

```text
slow semantic understanding
from
fast motor generation
```

---

## 60. Embodiment-aware control

Different robots have different:

- joints;
- kinematics;
- action dimensions.

A foundation VLA needs a way to condition on the specific body.

The source describes embodiment-aware encoders/decoders in the action system.

Conceptually:

```text
shared semantic policy
+
robot-specific state/action interface
```

This supports adaptation across:

- humanoids;
- manipulators;
- other robot bodies.

---

## 61. SmolVLA: efficiency by shrinking every stage

The source presents SmolVLA as an accessibility-oriented system.

Efficiency choices include:

### Small VLM backbone

Use a compact pretrained VLM.

### Truncated VLM

Use earlier layers rather than the whole backbone for action conditioning.

### Aggressive visual token reduction

The source mentions pixel shuffle reducing each frame to roughly:

```text
~64 visual tokens
```

### Small action head

A relatively compact flow-matching transformer.

The broad engineering pattern:

```text
small backbone
+
fewer tokens
+
fewer layers
+
small controller
```

makes consumer hardware more realistic.

---

## 62. The same loop in software and robotics

Digital agent:

```text
screenshot
→ model
→ click/type/tool
→ new screenshot
```

Robot VLA:

```text
camera + state
→ model
→ action chunk
→ new camera + state
```

The shared abstraction is:

```text
stateful closed-loop control
```

The difference is:

- action representation;
- timing requirements;
- safety cost of mistakes.

This is why concepts transfer surprisingly well between the two domains.

---

## 63. Agent/VLA design checklist

When building an acting VLM system, ask:

### Observation

- What can the model see?
- Is the state complete?
- Are observations synchronized?

### Action space

- Which actions are allowed?
- Are arguments validated?
- Are coordinates/units defined?

### Loop

- What triggers another step?
- When should the model stop?
- What state is retained?

### Determinism

- Which parts should be normal software instead?
- Is there an API instead of GUI manipulation?

### Evaluation

- Step-level accuracy?
- Task-level success?
- End-state verification?

### Safety/security

- What can the model modify?
- What requires approval?
- Which inputs are untrusted?

### Performance

For robots:

- control frequency?
- action chunk length?
- queue threshold?
- VLM refresh rate?
- action-head latency?

---

## 64. Source-specific notes and implementation cautions

### Framework table is time-specific

The chapter labels its framework comparison as:

```text
early 2026
```

Treat it as a historical ecosystem snapshot, not a permanent ranking.

### Product/model landscape is fast-moving

The chapter itself closes by noting that model and benchmark names will change.

The durable concepts are:

- feedback loops;
- tool/action interfaces;
- GUI grounding;
- action experts;
- asynchronous control.

### Holo2 prompt formatting

The pasted source splits string concatenation in a way that is not clean,
copy-paste-ready Python.

The lesson normalizes only that mechanical syntax.

### Coordinate conventions differ

The Holo example explicitly uses normalized `0–1000` coordinates.

The separate agentic GUI model example should be interpreted according to its
own documented action convention.

Do not reuse one model's coordinate system blindly for another.

### Screenshot automation is not equivalent to APIs

The source repeatedly favors structured/deterministic interfaces when they are
available.

Use visual interaction where needed, not by default.

### Robot action values are controller targets

The source emphasizes that learned policies generally output set-points, not raw
motor voltages.

That distinction matters for portability and safety.

---

## 65. The complete agentic-VLM/VLA mental model

The chapter can be compressed into one common loop:

```text
OBSERVE
   ↓
BUILD STATE
   ↓
DECIDE / GENERATE ACTION
   ↓
VALIDATE
   ↓
EXECUTE
   ↓
OBSERVE AGAIN
```

### DIGITAL VERSION

```text
screenshot / tool result
→ LLM/VLM
→ tool call / click / type / code
→ software environment
→ new observation
```

### PHYSICAL VERSION

```text
cameras + instruction + proprioception
→ pretrained VLM
→ cached semantic context
→ diffusion/flow action expert
→ action chunk
→ low-level controller
→ new observation
```

And the major engineering rules are:

```text
use deterministic code for deterministic jobs
keep actions structured and validated
evaluate both individual steps and final outcomes
keep multimodal memory bounded
treat tool permissions as a security boundary
synchronize robot observations/actions precisely
predict action chunks to control inference cost
cache slow semantic context when repeated refinement is required
```

The chapter's final principle is simple:

> **Whether the output is a JSON tool call, a mouse click, or a joint angle, an
> action-capable multimodal system succeeds by closing the loop between
> perception and action.**

{{exercise:M01.L11.EX05}}

{{exercise:M01.L11.EX06}}

---

## Important misconceptions

### Misconception 1: "An agent is just an LLM that can call one function."

Tool calling is one level of agency.

The multistep feedback loop is what enables open-ended agent behavior.

### Misconception 2: "More autonomy is always better."

No.

Simple routing or one deterministic call is often the better engineering
solution.

### Misconception 3: "Everything should be delegated to the agent."

No.

Use deterministic software for deterministic steps.

### Misconception 4: "If the final task succeeded once, the agent is reliable."

You also need repeated task evaluation and step-level traces.

### Misconception 5: "Code-generating agents and structured tool-calling agents are identical."

They expose different action surfaces and security/validation trade-offs.

### Misconception 6: "A screenshot-based computer-use agent is more reliable than a direct API."

The source presents structured APIs/tool calls as preferable when available.

### Misconception 7: "GUI localization and GUI reasoning are the same problem."

Localization answers where.

Agentic control also decides what action to take and in what order.

### Misconception 8: "Every GUI model uses normalized 0–1000 coordinates."

No.

Coordinate systems are model-specific.

### Misconception 9: "Keeping every screenshot improves agent memory."

Too many stale screenshots can waste context and distract the model.

### Misconception 10: "Agent security is mainly about harmful text output."

Tool permissions, third-party code, and untrusted web content create real action
and data-access risks.

### Misconception 11: "VLA means sending raw motor voltage from an LLM."

The source describes action set-points consumed by lower-level controllers.

### Misconception 12: "Robotics data can tolerate rough timestamp alignment."

Small timing errors can teach systematically incorrect observation-action
relationships.

### Misconception 13: "One demonstration is enough if the VLM is strong."

Policies need episodes with meaningful variation to avoid memorizing one
trajectory.

### Misconception 14: "A VLA is a completely new architecture unrelated to VLMs."

The chapter presents modern VLAs as pretrained VLMs plus state/action machinery.

### Misconception 15: "The VLM must rerun at every action denoising step."

The source describes caching VLM context while refining action queries.

### Misconception 16: "Predicting one action at a time is always more precise and therefore better."

It can make inference requirements impractical; action chunks trade refresh
frequency for efficient continuous control.

---

## Key terminology

| Term | Meaning |
|---|---|
| Agent | Model running in a feedback loop with access to tools/actions |
| Agency spectrum | Increasing levels from tool routing to multistep autonomous loops |
| ReAct | Think/act/observe loop with repeated feedback |
| Tool selection | Choosing which external function should handle a task |
| Tool calling | Producing a structured tool invocation |
| TaskStep | Agent memory object containing the initial task |
| PlanningStep | Optional high-level plan |
| ActionStep | One reasoning/action/observation cycle |
| FinalAnswerStep | Final result returned by the agent |
| observations_images | Visual observations such as screenshots stored in an agent step |
| CodeAgent | Agent that writes/executes code as its action mechanism |
| ToolCallingAgent | Agent that emits structured tool calls |
| Computer-use agent | Agent that operates GUI environments |
| GUI localization | Predicting where an interface target is located |
| Normalized coordinate | Position represented relative to a fixed scale rather than pixels |
| Action space | Set of valid operations the agent may execute |
| Step-level grounding | Whether each action was correct for the current state |
| Task-level success | Whether the full workflow completed correctly |
| Control plane | Deterministic runtime handling sessions, permissions, queues, and dispatch |
| VLA | Vision-language-action model mapping observations/instructions to actions |
| Policy | Function mapping observations to actions |
| Proprioception | Robot's internal body state |
| Episode | Complete task demonstration |
| Teleoperation | Human control used to collect robot demonstrations |
| Imitation learning | Learning a policy from expert demonstrations |
| Action chunk | Sequence of future actions predicted at once |
| Flow matching | Iterative continuous-generation method used for action vectors |
| DiT | Diffusion transformer |
| Action expert | Specialized network generating future robot actions |
| Controller set-point | Desired joint/gripper state sent to lower-level control |
| Action queue | Buffer of future robot actions awaiting execution |
| Asynchronous control | Generating future chunks while current actions execute |
| Embodiment | Particular robot body's sensors, joints, and action structure |
| Advantage conditioning | Conditioning policy on whether behavior performed better or worse than expected |

---

## Self-check

Before moving on, make sure you can answer:

1. What makes an agent different from a one-shot language model?
2. Why is the loop central to the chapter's definition of agency?
3. What are the three agency levels described in the source?
4. What happens during the ReAct loop?
5. When is a simple tool call better than an agent?
6. Why should deterministic steps remain deterministic?
7. Why does a CAPTCHA demonstrate the need for fallback reasoning?
8. Why should hallucinated facts be reverified before an action such as sending email?
9. What is step-level grounding?
10. What is task-level success?
11. Why log an action trace?
12. What is the difference between CodeAgent and ToolCallingAgent?
13. Why does a tool description matter?
14. What is a TaskStep?
15. What is a PlanningStep?
16. What is an ActionStep?
17. What is a FinalAnswerStep?
18. How do screenshots enter a visual agent loop?
19. Why can external models be treated as tools?
20. Why should the agent runtime be separated from the model backend?
21. Why do screenshot-based computer-use agents exist?
22. Why are structured APIs usually preferred when available?
23. What is the difference between GUI localization and agentic GUI control?
24. What does a normalized coordinate mean?
25. How do you map 0–1000 coordinates back to pixels?
26. Why does screenshot resizing affect coordinate interpretation?
27. Why validate action output against a schema?
28. What kinds of GUI actions can an agentic model expose?
29. Why constrain the action space?
30. Why can one task require multiple GUI actions?
31. Why should you verify each model's coordinate convention?
32. What closes the observation step in a visual browser agent?
33. Why prune old screenshots?
34. Why are system-prompt heuristics useful in browser agents?
35. Which infrastructure responsibilities should a deterministic control plane handle?
36. What are tool/skill bundles?
37. What is the difference between long-term memory and session transcript memory?
38. Why are third-party tools and untrusted web content a security concern?
39. What is the shared loop between digital agents and VLAs?
40. How does classical robotics decompose perception, planning, and control?
41. Where does classical robotics work particularly well?
42. Why can reinforcement learning be effective in simulation?
43. Why can real-world RL be expensive?
44. What is imitation learning?
45. Why does a pretrained VLM help imitation-learning robotics?
46. What is a policy?
47. What is proprioception?
48. What is an episode?
49. What is an action chunk?
50. What is teleoperation?
51. What are typical VLA inputs?
52. What does a VLA usually output?
53. Why are outputs set-points rather than raw voltages?
54. Why predict action chunks?
55. How does chunking reduce high-level inference frequency?
56. What is asynchronous robot control?
57. What is the purpose of the action queue?
58. Why must camera and robot-state streams be tightly synchronized?
59. Why does starting-condition variation matter?
60. What robotics data checks does the source recommend?
61. How does a VLM become a VLA architecturally?
62. What is the action expert?
63. Why can VLM context be cached during action refinement?
64. Why might a VLA use middle-layer VLM features?
65. What is the central idea of π0.6?
66. What does advantage conditioning communicate?
67. What is the main architectural idea of GR00T N1.5?
68. What does embodiment-aware control solve?
69. How does SmolVLA reduce compute?
70. What principle connects the entire chapter?

---

## Retain this idea

**Agentic VLMs and VLAs are two versions of the same core idea: perception becomes
useful when it is connected to a closed action loop. The strongest systems do
not simply maximize autonomy—they carefully define observations, constrain and
validate actions, keep deterministic infrastructure outside the model, measure
success at both step and task level, and repeatedly observe the consequences of
what they do.**
""",

        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "action-shift", "title": "From perception to action", "order": 1},
            {"id": "agent-definition", "title": "What is an agent?", "order": 2},
            {"id": "agency-spectrum", "title": "Agency is a spectrum", "order": 3},
            {"id": "react", "title": "The ReAct loop", "order": 4},
            {"id": "when-agent", "title": "When an agent is needed", "order": 5},
            {"id": "open-vs-deterministic", "title": "Open-ended versus deterministic work", "order": 6},
            {"id": "agent-failures", "title": "Why feedback loops matter", "order": 7},
            {"id": "agent-evaluation", "title": "Evaluating agents", "order": 8},
            {"id": "evaluation-traces", "title": "Agent traces", "order": 9},
            {"id": "frameworks", "title": "Agent framework choices", "order": 10},
            {"id": "smolagents", "title": "Why smolagents", "order": 11},
            {"id": "agent-classes", "title": "CodeAgent versus ToolCallingAgent", "order": 12},
            {"id": "toy-agent", "title": "Toy tool-using agent", "order": 13},
            {"id": "agent-memory", "title": "Agent memory lifecycle", "order": 14},
            {"id": "image-observations", "title": "Visual observations", "order": 15},
            {"id": "models-as-tools", "title": "Models as tools", "order": 16},
            {"id": "model-backends", "title": "Model backends", "order": 17},
            {"id": "computer-use", "title": "Computer-use agents", "order": 18},
            {"id": "computer-use-flavors", "title": "API versus screenshot computer use", "order": 19},
            {"id": "localization-vs-agentic", "title": "Localization versus agentic control", "order": 20},
            {"id": "holo", "title": "Normalized GUI localization", "order": 21},
            {"id": "gui-resize", "title": "Screenshot geometry", "order": 22},
            {"id": "structured-click", "title": "Structured GUI outputs", "order": 23},
            {"id": "holo-code-note", "title": "Holo2 source formatting note", "order": 24},
            {"id": "agentic-gui", "title": "Agentic GUI action spaces", "order": 25},
            {"id": "action-space", "title": "Constrained action primitives", "order": 26},
            {"id": "multi-action", "title": "Multiaction GUI tasks", "order": 27},
            {"id": "coordinate-conventions", "title": "Coordinate conventions", "order": 28},
            {"id": "vision-browser", "title": "Visual browser agent", "order": 29},
            {"id": "screenshot-callback", "title": "Screenshot feedback callback", "order": 30},
            {"id": "stale-images", "title": "Pruning stale screenshots", "order": 31},
            {"id": "browser-guardrails", "title": "Browser agent guardrails", "order": 32},
            {"id": "production-agent", "title": "Production control plane", "order": 33},
            {"id": "agent-skills", "title": "Tool bundles and skills", "order": 34},
            {"id": "agent-memory-layers", "title": "Persistent and session memory", "order": 35},
            {"id": "agent-security", "title": "Agent security", "order": 36},
            {"id": "digital-to-physical", "title": "From digital to physical action", "order": 37},
            {"id": "robot-paradigms", "title": "Robot-learning paradigms", "order": 38},
            {"id": "classical", "title": "Classical robotics", "order": 39},
            {"id": "rl", "title": "Reinforcement learning", "order": 40},
            {"id": "imitation", "title": "Imitation learning", "order": 41},
            {"id": "robot-glossary", "title": "Robotics vocabulary", "order": 42},
            {"id": "vla-observation", "title": "VLA observations", "order": 43},
            {"id": "vla-actions", "title": "VLA outputs", "order": 44},
            {"id": "action-chunks", "title": "Action chunks", "order": 45},
            {"id": "chunk-compute", "title": "Action-chunk compute savings", "order": 46},
            {"id": "async-control", "title": "Asynchronous control", "order": 47},
            {"id": "vla-data", "title": "VLA data synchronization", "order": 48},
            {"id": "episodes", "title": "Episodes and variation", "order": 49},
            {"id": "robot-data-validation", "title": "Robot data validation", "order": 50},
            {"id": "vlm-to-vla", "title": "From VLM to VLA", "order": 51},
            {"id": "action-expert", "title": "The action expert", "order": 52},
            {"id": "vla-pipeline", "title": "Common VLA pipeline", "order": 53},
            {"id": "vla-cache", "title": "Caching VLM context", "order": 54},
            {"id": "middle-features", "title": "Using middle VLM features", "order": 55},
            {"id": "landscape", "title": "VLA model landscape", "order": 56},
            {"id": "pi06", "title": "π0.6", "order": 57},
            {"id": "pi06-loop", "title": "Learning from rollout feedback", "order": 58},
            {"id": "groot", "title": "GR00T N1.5", "order": 59},
            {"id": "embodiment", "title": "Embodiment-aware control", "order": 60},
            {"id": "smolvla", "title": "SmolVLA", "order": 61},
            {"id": "digital-physical-parallel", "title": "Digital and physical action loops", "order": 62},
            {"id": "design-checklist", "title": "Agent/VLA design checklist", "order": 63},
            {"id": "source-notes", "title": "Source-specific notes", "order": 64},
            {"id": "complete-mental-model", "title": "Complete action-system mental model", "order": 65},
        ],
    },

    "exercises": [
        {
            "id": "M01.L11.EX01",
            "title": "Decide what should be agentic",
            "lesson_code": "M01.L11",
            "section_id": "open-vs-deterministic",
            "placement": "after_section",
            "description": (
                "Separate deterministic software steps from open-ended agent reasoning."
            ),
            "instructions": (
                "You are building a procurement assistant that must:\n"
                "1. search three vendor websites,\n"
                "2. get your company's current spend,\n"
                "3. compare plans,\n"
                "4. draft a recommendation,\n"
                "5. create a follow-up task.\n"
                "For each step, choose deterministic API/tool call or agent loop reasoning. "
                "Explain what observation should be verified before continuing."
            ),
            "expected_output": (
                "A five-row table showing execution mode, tool/interface, verification, and fallback."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "agent-design",
                "react",
                "deterministic-systems",
            ],
        },
        {
            "id": "M01.L11.EX02",
            "title": "Convert normalized GUI coordinates",
            "lesson_code": "M01.L11",
            "section_id": "holo",
            "placement": "after_section",
            "description": (
                "Practice translating normalized model output into screenshot pixels."
            ),
            "instructions": (
                "A localization model returns x=625, y=250 on a 0–1000 coordinate scale. "
                "The processed screenshot is 1440×900 pixels.\n"
                "1. Compute pixel_x.\n"
                "2. Compute pixel_y.\n"
                "3. Explain what must change if the execution environment uses the original "
                "1920×1200 screenshot rather than the processed image."
            ),
            "expected_output": (
                "Two numeric pixel coordinates and a coordinate-frame explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "gui-localization",
                "coordinates",
                "computer-use",
            ],
        },
        {
            "id": "M01.L11.EX03",
            "title": "Calculate action-chunk compute savings",
            "lesson_code": "M01.L11",
            "section_id": "chunk-compute",
            "placement": "after_section",
            "description": (
                "Quantify why action chunking is important for expensive iterative policies."
            ),
            "instructions": (
                "A robot executes at 60 Hz. Its action expert needs 8 denoising forward passes "
                "for each policy generation.\n"
                "A. If it predicts one action at a time, how many forward passes/second are needed?\n"
                "B. If it predicts 12 actions per chunk, how many policy generations/second are needed?\n"
                "C. How many action-expert forward passes/second result?\n"
                "D. What approximate reduction factor did chunking provide?"
            ),
            "expected_output": (
                "Step-by-step frequency and forward-pass calculations."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "action-chunks",
                "robot-control",
                "inference-efficiency",
            ],
        },
        {
            "id": "M01.L11.EX04",
            "title": "Audit a VLA demonstration dataset",
            "lesson_code": "M01.L11",
            "section_id": "robot-data-validation",
            "placement": "after_section",
            "description": (
                "Design checks for synchronized multimodal robot demonstrations."
            ),
            "instructions": (
                "A dataset has two cameras at 30 fps, joint states at 100 Hz, and action commands "
                "at 50 Hz.\n"
                "Create a validation checklist that catches:\n"
                "- missing camera frames,\n"
                "- timestamp drift,\n"
                "- impossible joint angles,\n"
                "- actions blocked by safety limits,\n"
                "- episode truncation,\n"
                "- insufficient start-state variation.\n"
                "For each failure, explain what training error it could teach."
            ),
            "expected_output": (
                "A validation table with signal, test, failure symptom, and learned-policy risk."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vla-data",
                "synchronization",
                "imitation-learning",
            ],
        },
        {
            "id": "M01.L11.EX05",
            "title": "Design a screenshot-based browser agent",
            "lesson_code": "M01.L11",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Synthesize perception, action, feedback, validation, and deterministic fallbacks."
            ),
            "instructions": (
                "Design an agent that finds a product on a website, extracts the visible price, "
                "adds it to a comparison table, and stops before purchase.\n"
                "Specify:\n"
                "- observation format,\n"
                "- action space,\n"
                "- screenshot callback,\n"
                "- coordinate convention,\n"
                "- step-level checks,\n"
                "- task completion condition,\n"
                "- API/deterministic fallbacks,\n"
                "- actions requiring explicit prohibition or approval."
            ),
            "expected_output": (
                "An end-to-end browser-agent design and safety boundary."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "computer-use-agent",
                "react",
                "agent-evaluation",
                "agent-security",
            ],
        },
        {
            "id": "M01.L11.EX06",
            "title": "Design a lightweight VLA",
            "lesson_code": "M01.L11",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Apply the chapter's VLA ideas to an accessible robot-manipulation system."
            ),
            "instructions": (
                "Design a VLA for a small robot arm that must sort colored objects.\n"
                "Specify:\n"
                "- cameras,\n"
                "- language instruction format,\n"
                "- proprioception,\n"
                "- compact VLM strategy,\n"
                "- token reduction,\n"
                "- action head,\n"
                "- action chunk length,\n"
                "- asynchronous queue behavior,\n"
                "- demonstration collection,\n"
                "- validation metrics.\n"
                "Use the SmolVLA efficiency principles where appropriate."
            ),
            "expected_output": (
                "A compact VLA architecture plus training/data/control plan."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vla-design",
                "action-expert",
                "asynchronous-control",
                "robotics",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L11.QZ01",
        "title": "Agentic VLMs and Vision-Language-Action Models — Knowledge Check",
        "lesson_code": "M01.L11",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L11.Q01",
                "section_id": "agent-definition",
                "question": "What is the key ingredient in the chapter's working definition of an agent?",
                "options": [
                    "An LLM running in a loop with access to tools",
                    "A model that only produces longer text",
                    "A single classifier call",
                    "A vector database with no model",
                ],
                "correct": 0,
                "explanation": (
                    "The feedback loop lets the model act, observe the result, and decide what to do next."
                ),
            },
            {
                "id": "M01.L11.Q02",
                "section_id": "agency-spectrum",
                "question": "Which is the highest-agency pattern listed in the chapter's spectrum?",
                "options": [
                    "A multistep ReAct-style loop",
                    "Simple tool selection",
                    "A static prompt",
                    "A tokenizer",
                ],
                "correct": 0,
                "explanation": (
                    "The multistep loop repeatedly reasons, acts, and observes until completion."
                ),
            },
            {
                "id": "M01.L11.Q03",
                "section_id": "open-vs-deterministic",
                "question": "What does the source recommend when a reliable API can provide a deterministic result?",
                "options": [
                    "Use the deterministic API rather than forcing the agent through a brittle GUI flow.",
                    "Always use screenshots instead.",
                    "Ask the agent to bypass login security.",
                    "Avoid external tools completely.",
                ],
                "correct": 0,
                "explanation": (
                    "Open-ended reasoning should be reserved for the parts that actually require it."
                ),
            },
            {
                "id": "M01.L11.Q04",
                "section_id": "agent-evaluation",
                "question": "What is step-level grounding?",
                "options": [
                    "Checking whether the agent took the correct action at each step",
                    "Checking only the final answer length",
                    "Measuring model parameter count",
                    "Evaluating robot battery life",
                ],
                "correct": 0,
                "explanation": (
                    "Step-level evaluation identifies local perception/action errors inside the loop."
                ),
            },
            {
                "id": "M01.L11.Q05",
                "section_id": "agent-memory",
                "question": "Which memory object represents one think-act-observe cycle?",
                "options": [
                    "ActionStep",
                    "TaskStep",
                    "FinalAnswerStep",
                    "TokenizerStep",
                ],
                "correct": 0,
                "explanation": (
                    "ActionStep stores the model action and resulting observations."
                ),
            },
            {
                "id": "M01.L11.Q06",
                "section_id": "localization-vs-agentic",
                "question": "What is the main difference between GUI localization and agentic GUI control?",
                "options": [
                    "Localization finds where to act; agentic control also decides what actions to take and in what sequence.",
                    "Localization always uses APIs.",
                    "Agentic control never uses screenshots.",
                    "They are identical tasks.",
                ],
                "correct": 0,
                "explanation": (
                    "Full control requires planning/action selection in addition to visual grounding."
                ),
            },
            {
                "id": "M01.L11.Q07",
                "section_id": "holo",
                "question": "If a localization model returns x=500 on a normalized 0–1000 scale, what horizontal location is that?",
                "options": [
                    "Halfway across the processed image",
                    "Exactly 500 pixels on every image",
                    "The far-right edge",
                    "The top edge",
                ],
                "correct": 0,
                "explanation": (
                    "A normalized value of 500 represents 50% of image width."
                ),
            },
            {
                "id": "M01.L11.Q08",
                "section_id": "screenshot-callback",
                "question": "Why is a screenshot callback needed after browser actions?",
                "options": [
                    "It provides the new environment state for the next observation/reasoning cycle.",
                    "It trains the model from scratch.",
                    "It replaces all tools.",
                    "It increases coordinate normalization.",
                ],
                "correct": 0,
                "explanation": (
                    "Without fresh visual state, the agent would not know what its previous action changed."
                ),
            },
            {
                "id": "M01.L11.Q09",
                "section_id": "agent-security",
                "question": "Why does tool-enabled agent architecture require an explicit security boundary?",
                "options": [
                    "Untrusted content or extensions can influence actions that access real tools and data.",
                    "Agents cannot read text.",
                    "Tools eliminate all risk.",
                    "Only model latency matters.",
                ],
                "correct": 0,
                "explanation": (
                    "Action capability turns prompt/content manipulation into potential real-world side effects."
                ),
            },
            {
                "id": "M01.L11.Q10",
                "section_id": "robot-paradigms",
                "question": "Which robot-learning approach is the chapter's main practical focus for VLAs?",
                "options": [
                    "Imitation learning from demonstrations",
                    "Only classical inverse kinematics",
                    "Only online RL",
                    "Unsupervised clustering",
                ],
                "correct": 0,
                "explanation": (
                    "The source focuses on teleoperation demonstrations and supervised/imitation learning."
                ),
            },
            {
                "id": "M01.L11.Q11",
                "section_id": "robot-glossary",
                "question": "What is proprioception?",
                "options": [
                    "The robot's internal state such as joint positions, velocities, and gripper state",
                    "A screenshot of a website",
                    "A text instruction only",
                    "A cloud API",
                ],
                "correct": 0,
                "explanation": (
                    "Proprioception tells the policy about the robot's own body state."
                ),
            },
            {
                "id": "M01.L11.Q12",
                "section_id": "vla-actions",
                "question": "What does the source say a VLA typically outputs?",
                "options": [
                    "Controller set-points such as target joint positions",
                    "Raw motor voltage directly from the LLM",
                    "Only natural-language descriptions",
                    "Only image embeddings",
                ],
                "correct": 0,
                "explanation": (
                    "Lower-level firmware/controllers translate set-points into motor commands."
                ),
            },
            {
                "id": "M01.L11.Q13",
                "section_id": "action-chunks",
                "question": "Why predict a chunk of future actions instead of one action at a time?",
                "options": [
                    "It reduces how frequently the expensive policy must run.",
                    "It removes the need for observations forever.",
                    "It guarantees perfect control.",
                    "It disables the robot controller.",
                ],
                "correct": 0,
                "explanation": (
                    "One generation can supply several control steps."
                ),
            },
            {
                "id": "M01.L11.Q14",
                "section_id": "async-control",
                "question": "What is the core idea of asynchronous VLA control?",
                "options": [
                    "Generate the next action chunk while the robot is executing the current chunk.",
                    "Stop the robot during every inference call.",
                    "Generate all actions for the entire day at once.",
                    "Remove the action queue.",
                ],
                "correct": 0,
                "explanation": (
                    "Pipelining keeps motion continuous while compute happens in parallel."
                ),
            },
            {
                "id": "M01.L11.Q15",
                "section_id": "vla-data",
                "question": "Why is precise timestamp synchronization critical in VLA datasets?",
                "options": [
                    "The model must learn the correct mapping from a visual/body state to the action executed at that moment.",
                    "It only affects filename sorting.",
                    "Robot actions are independent of observations.",
                    "Timestamp drift improves data augmentation.",
                ],
                "correct": 0,
                "explanation": (
                    "Misalignment teaches systematically incorrect state-action associations."
                ),
            },
            {
                "id": "M01.L11.Q16",
                "section_id": "action-expert",
                "question": "What is the action expert in a modern VLA?",
                "options": [
                    "A specialized network, often using diffusion or flow matching, that generates future action chunks.",
                    "A GUI localization classifier",
                    "A vector database",
                    "A TTS engine",
                ],
                "correct": 0,
                "explanation": (
                    "The VLM supplies context; the action expert generates continuous robot actions."
                ),
            },
            {
                "id": "M01.L11.Q17",
                "section_id": "vla-cache",
                "question": "Why can VLM context be cached while the action expert iteratively refines actions?",
                "options": [
                    "The visual/language observation stays fixed during those refinement steps.",
                    "The robot has no camera.",
                    "Diffusion requires no context.",
                    "The action expert cannot use attention.",
                ],
                "correct": 0,
                "explanation": (
                    "Only action queries need to change during the denoising/refinement loop."
                ),
            },
            {
                "id": "M01.L11.Q18",
                "section_id": "pi06",
                "question": "What is the key idea highlighted for π0.6?",
                "options": [
                    "Advantage conditioning lets the policy learn from which behaviors worked better or worse than expected.",
                    "It is a GUI-only agent.",
                    "It contains no pretrained VLM.",
                    "It uses only hand-coded kinematics.",
                ],
                "correct": 0,
                "explanation": (
                    "A value function helps label successful versus disappointing behavior for further policy learning."
                ),
            },
            {
                "id": "M01.L11.Q19",
                "section_id": "smolvla",
                "question": "Which combination describes SmolVLA's efficiency strategy in the source?",
                "options": [
                    "Small VLM, earlier-layer features, aggressive token reduction, and a small action head",
                    "Largest possible VLM and no token reduction",
                    "Full online RL only",
                    "No visual input",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes reducing compute at every stage."
                ),
            },
            {
                "id": "M01.L11.Q20",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design two closed-loop action systems: (1) a computer-use agent that must "
                    "operate a GUI from screenshots and (2) a VLA that controls a robot arm. "
                    "For each, define observations, actions, feedback, memory/state, validation, "
                    "task completion, safety boundaries, and which parts should remain "
                    "deterministic. Then explain the common observe-decide-act structure."
                ),
            },
        ],
        "passing_score": 70,
    },
}
