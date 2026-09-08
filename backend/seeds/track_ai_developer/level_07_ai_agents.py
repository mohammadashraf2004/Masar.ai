"""
backend/seeds/levels/level_07_ai_agents.py

AI Developer career track -- Level 7: AI Agents & Orchestration.

Exported as a standalone LEVEL dict (same convention as
level_06_advanced_rag.py) until common.py exists to standardize the
import/export shape across level files.

Shape matches seed_track_ai_developer.py's LEVELS entries:
    LEVEL = {"title", "description", "order", "topics": [ ... ]}
    each topic = {title, slug, description, order, difficulty,
                   estimated_hours, skill_tags, prerequisite_ids,
                   lesson, exercises, quiz, project}
"""
from app.models.learning import DifficultyLevel

LEVEL = {
    "title": "Level 7: AI Agents & Orchestration",
    "description": "Move from static RAG pipelines to systems that can decide their own next action: the agent mental model, tool use, state, and the decide-act-observe loop that underlies every agent framework.",
    "order": 7,
    "topics": [
        # ------------------------------------------------------------
        # Topic 1
        # ------------------------------------------------------------
        {
            "title": "What Is an AI Agent?",
            "slug": "ai-developer-ai-agents-what-is-an-agent",
            "description": "The core mental model for agents: LLM + Tools + State + Decision Loop, and how that differs from a plain LLM call or a fixed RAG pipeline.",
            "order": 1,
            "difficulty": DifficultyLevel.beginner,
            "estimated_hours": 1.0,
            "skill_tags": ["ai-agents", "llm", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "What Is an AI Agent?",
                "content": """# What Is an AI Agent?

You already know how an LLM and a RAG system work. So let's build the mental model of an **agent** from that foundation, one piece at a time.

## The Basic Idea

An **AI Agent** is an AI system that can decide what actions to take in order to achieve a goal.

A normal LLM mostly does this:

```
Input → LLM → Output
```

An agent can do this instead:

```
Goal
 ↓
Think / Decide
 ↓
Choose Action
 ↓
Use Tool
 ↓
Observe Result
 ↓
Decide Again
 ↓
...
 ↓
Final Answer
```

The important difference: an agent is not just generating text. It can **control a process**.

## Why Do We Need Agents?

Imagine a user says:

*"Find me a good apartment in New Cairo under 5 million EGP and compare the investment potential."*

A plain LLM might answer from its existing knowledge. But a real application would need to:

- Search a property database
- Filter apartments under 5M
- Calculate price per square meter
- Compare rental yields
- Search additional market information
- Rank the properties
- Explain the recommendation

The system needs to **perform actions**, not just generate an answer. That's where agents become useful.

## The Agent Mental Model

Think of an agent as:

**LLM + Tools + State + Decision Loop**

Don't worry about implementing all four pieces yet -- we'll learn each one separately across this level. Conceptually:

```
              ┌──────────────┐
              │     Goal     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │     LLM      │
              │   Decision   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │    Tool      │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │    Result    │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │     LLM      │
              │ Decide Again │
              └──────┬───────┘
                     ↓
                  Answer
```

The **decision loop** is one of the most important ideas in agent engineering.

## Agent vs Normal LLM

**Normal LLM** -- user asks *"What is the weather in Cairo?"*:

```
User
 ↓
LLM
 ↓
Answer
```

The LLM generates an answer. It doesn't necessarily perform an external action.

**Agent** -- user asks *"Check the weather in Cairo and tell me whether I should go running."*:

```
User request
     ↓
Understand goal
     ↓
Call weather tool
     ↓
Receive weather
     ↓
Analyze conditions
     ↓
Give recommendation
```

The important part is that the **LLM decides to call the weather tool**.

## Agent vs RAG

You already know RAG. A typical RAG pipeline is roughly:

```
Question
   ↓
Retrieve documents
   ↓
Relevant chunks
   ↓
LLM
   ↓
Answer
```

The retrieval process is generally **predefined** -- the application says "for every question, retrieve relevant documents and give them to the LLM."

An agent can be more dynamic:

```
User Question
      ↓
     LLM
      ↓
Should I search?
   /       \\
 Yes        No
 ↓           ↓
Search      Answer
 ↓
Result
 ↓
LLM
 ↓
Need another action?
 /        \\
Yes        No
 ↓          ↓
Tool       Answer
```

So: **RAG** is a retrieval strategy. **Agent** is a decision-making system capable of choosing actions. And **Agentic RAG** is an agent that can decide *how* and *when* to retrieve information. You already touched Agentic RAG in Level 6 -- now we're going deeper into the underlying agent architecture.

## Agent ≠ "AI That Thinks"

This is an important engineering distinction. People sometimes describe an agent as "an AI that thinks like a human." That's not a useful engineering definition.

Instead: **an agent is a system where an LLM participates in a loop and can choose actions based on the current state and goal.** The exact "thinking" mechanism can vary:

```
Goal
 ↓
LLM chooses search()
 ↓
Search result
 ↓
LLM chooses calculate()
 ↓
Calculation result
 ↓
LLM chooses final_answer()
```

The agent's intelligence comes partly from its ability to **select and sequence actions**.

## A Tiny Agent Example

Imagine we give an LLM two tools:

```
tools = [
    search_products,
    calculate_price
]
```

User: *"Find me a laptop under $1000 and calculate the price after a 10% discount."*

The agent might perform:

```
Goal
 ↓
search_products()
 ↓
Found laptop: $900
 ↓
calculate_price(900, 0.10)
 ↓
$810
 ↓
Final answer
```

Notice: we didn't hard-code the call order of `search_products()` then `calculate_price()`. The agent **decides** which tool to use and when. That's the core idea.

## A Simple Framework-Independent Implementation

We can represent the basic idea with pseudocode:

```
def agent(goal):

    while True:

        decision = llm(goal)

        if decision.type == "tool":
            result = run_tool(
                decision.tool,
                decision.arguments
            )

            goal = update_context(goal, result)

        elif decision.type == "final":
            return decision.answer
```

Don't worry about making this production-ready. The mental model is:

```
LLM → Decision → Action → Observation → LLM → Decision → Action → Observation → ... → Final Answer
```

This is the foundation for almost everything we'll learn in Level 7.

## The Key Components

You will encounter these concepts throughout the level:

- **Goal** -- what are we trying to accomplish? *"Find the best apartment for investment."*
- **LLM** -- the reasoning/decision component. *"What should I do next?"*
- **Tools** -- actions the agent can perform: `search()`, `calculate()`, `database_query()`, `send_email()`
- **State** -- information the agent currently has: goal, previous actions, tool results, conversation, intermediate information
- **Loop** -- the agent repeatedly does *Decide → Act → Observe* until it reaches an appropriate stopping condition

## Agents Are Not Always Better

This is an important AI engineering principle: **you should not use an agent simply because you can.**

Suppose your application always does:

```
Question → Retrieve documents → LLM → Answer
```

If this works reliably, introducing an agent may make the system slower, more expensive, harder to debug, and less predictable. A **deterministic pipeline** can often be better. Use an agent when the problem genuinely requires dynamic decision-making or action selection.

## Three Levels of AI Systems

A useful way to think about AI applications:

**Level 1 -- LLM**
```
Input → LLM → Output
```
Example: *"Explain RAG."*

**Level 2 -- Workflow**
```
Input → Step 1 → Step 2 → Step 3 → Output
```
The developer determines the sequence.

**Level 3 -- Agent**
```
Input → LLM decides → Action → Observation → LLM decides → Action → ...
```
The system can dynamically determine the next action. We'll study Workflow vs Agent in the next lesson.

## Real-World Example

Imagine an AI customer-support agent. User: *"My order hasn't arrived. Can you check it?"*

```
Goal:
Check customer's order
       ↓
Look up customer
       ↓
Get order ID
       ↓
Check shipping status
       ↓
Is it delayed?
   /          \\
 Yes           No
 ↓              ↓
Check reason    Report status
 ↓
Respond
```

The important thing isn't that the LLM writes the final response -- it's that it can **choose and execute actions** to accomplish the goal.

## Connecting to Your Previous RAG Knowledge

```
                 AI Application
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
      RAG                         Agent
        │                           │
 Retrieve information        Choose actions
        │                           │
        ↓                           ↓
 Vector DB / BM25              Tools / APIs
        │                           │
        └─────────────┬─────────────┘
                      ↓
                     LLM
```

A future system could combine them:

```
              Agent
                ↓
       ┌────────┼─────────┐
       ↓        ↓         ↓
     RAG      API      Calculator
       ↓        ↓         ↓
       └────────┼─────────┘
                ↓
               LLM
                ↓
             Answer
```

That's where modern AI applications become much more powerful.

*The single idea to keep: an agent is a system where an LLM decides what action to take next, executes it through a tool, observes the result, and repeats -- a workflow is when the developer decides the steps instead.*
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Flight Search: Agent or Workflow?",
                    "description": (
                        "A user asks: \"Find the cheapest flight from Cairo to Istanbul next Friday.\" "
                        "You have these capabilities: search_flights(), get_flight_details(), calculate_total_price(). "
                        "Answer in your own words: (1) What is the goal of the agent? "
                        "(2) Which tools might it use, and in what order? "
                        "(3) Why could this be built as an agent instead of a fixed workflow? "
                        "There's no single perfect wording -- this checks whether you have the mental model, not exact phrasing."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "systems-thinking"],
                },
                {
                    "title": "Implement the Decision Loop",
                    "description": (
                        "Using the pseudocode from the lesson as a starting point, implement a minimal `agent()` "
                        "function that loops over LLM decisions and tool calls until it receives a 'final' decision. "
                        "You can stub `llm()` and `run_tool()` -- the goal is to get the control flow of the "
                        "decide → act → observe loop correct, including updating state (`goal`/context) after each tool call."
                    ),
                    "starter_code": (
                        "def llm(goal):\n"
                        "    # TODO: stub -- return an object/dict with .type (\"tool\" or \"final\")\n"
                        "    # and either (.tool, .arguments) or (.answer)\n"
                        "    pass\n\n"
                        "def run_tool(tool, arguments):\n"
                        "    # TODO: stub -- pretend to execute a tool and return a result\n"
                        "    pass\n\n"
                        "def update_context(goal, result):\n"
                        "    # TODO: fold the tool result into the goal/state for the next LLM call\n"
                        "    pass\n\n"
                        "def agent(goal):\n"
                        "    # TODO: implement the decide -> act -> observe loop\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def agent(goal):\n"
                        "    while True:\n"
                        "        decision = llm(goal)\n\n"
                        "        if decision.type == \"tool\":\n"
                        "            result = run_tool(decision.tool, decision.arguments)\n"
                        "            goal = update_context(goal, result)\n\n"
                        "        elif decision.type == \"final\":\n"
                        "            return decision.answer\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "control-flow"],
                },
            ],
            "quiz": {
                "title": "What Is an AI Agent? — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the key difference between a plain LLM call and an AI agent?",
                        "options": [
                            "An agent uses a larger or more powerful model",
                            "An agent can decide on and execute actions through a decision loop, not just generate text",
                            "An agent always uses a vector database",
                            "An agent never needs a system prompt",
                        ],
                        "correct": 1,
                        "explanation": "A plain LLM call maps input to output. An agent participates in a decide → act → observe loop and can choose actions via tools to reach a goal.",
                    },
                    {
                        "question": "In the Workflow vs Agent distinction from the lesson, who decides the sequence of steps in a Workflow?",
                        "options": [
                            "The LLM, dynamically, at runtime",
                            "The end user, via natural language",
                            "The developer, in advance",
                            "The vector database's retrieval ranking",
                        ],
                        "correct": 2,
                        "explanation": "In a Workflow (Level 2 of the three-levels model), the developer fixes the sequence of steps ahead of time. In an Agent (Level 3), the LLM decides the next step dynamically.",
                    },
                    {
                        "question": "Which of these is NOT one of the four core components of the 'LLM + Tools + State + Decision Loop' agent mental model?",
                        "options": [
                            "Tools -- actions the agent can perform",
                            "State -- goal, previous actions, and tool results the agent is tracking",
                            "Loop -- the repeated decide/act/observe cycle",
                            "Fine-tuning -- retraining the model's weights on new data",
                        ],
                        "correct": 3,
                        "explanation": "The lesson's mental model is LLM + Tools + State + Decision Loop. Fine-tuning is a separate, unrelated concept -- agents typically use a frozen pretrained model plus tools.",
                    },
                    {
                        "question": "According to the lesson, when should you avoid using an agent even though you technically could?",
                        "options": [
                            "Whenever the task involves more than one tool",
                            "When a deterministic pipeline already works reliably, since an agent can add latency, cost, and unpredictability",
                            "Whenever the user asks a question in natural language",
                            "Only when there is no LLM API available",
                        ],
                        "correct": 1,
                        "explanation": "The lesson stresses that agents aren't always better: if a fixed pipeline reliably solves the problem, an agent can make the system slower, more expensive, and harder to debug.",
                    },
                    {
                        "question": "How does the lesson define 'Agentic RAG'?",
                        "options": [
                            "A RAG pipeline that always retrieves from exactly one document",
                            "An agent that can decide how and when to retrieve information, rather than always retrieving on a fixed schedule",
                            "A RAG system that requires no LLM at all",
                            "A vector database optimized specifically for agents",
                        ],
                        "correct": 1,
                        "explanation": "RAG is a retrieval strategy; an Agent is a decision-making system. Agentic RAG combines them: the agent decides whether and when to invoke retrieval as one of its available actions.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 2
        # ------------------------------------------------------------
        {
            "title": "Workflow vs Agent",
            "slug": "ai-developer-ai-agents-workflow-vs-agent",
            "description": "The core engineering distinction between a workflow (developer controls the steps) and an agent (the LLM controls the next action), where each fits on the autonomy spectrum, and a practical decision rule for choosing between them.",
            "order": 2,
            "difficulty": DifficultyLevel.beginner,
            "estimated_hours": 1.0,
            "skill_tags": ["ai-agents", "system-design", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Workflow vs Agent",
                "content": """# Workflow vs Agent

This is one of the most important distinctions in AI engineering. If you understand it well, you'll know when to build a **workflow** and when to build an **agent**.

## The Core Difference

The simplest way to remember it:

**Workflow** = the developer decides the steps.
**Agent** = the AI decides the steps.

## What Is a Workflow?

A workflow is a **predefined sequence of operations**. For example, imagine a RAG application:

```
User Question
      ↓
Rewrite Query
      ↓
Hybrid Search
      ↓
Rerank
      ↓
Generate Answer
```

The developer designed this pipeline. Every request follows approximately the same process:

```
def rag_workflow(question):
    query = rewrite_query(question)
    documents = hybrid_search(query)
    documents = rerank(documents)
    answer = generate_answer(question, documents)
    return answer
```

The order is determined by the programmer.

## Why Workflows Are Useful

Workflows are excellent when the process is predictable. For example, document processing:

```
PDF
 ↓
Extract text
 ↓
Chunk
 ↓
Embed
 ↓
Store in vector DB
```

There is usually no reason for an LLM to decide *"Hmm... should I embed this PDF today?"* You already know the correct process. A workflow is therefore: **predictable**, easier to test, easier to debug, usually faster, and usually cheaper.

## What Is an Agent?

An agent introduces **dynamic decision-making**. Instead of `Step 1 → Step 2 → Step 3`, you have:

```
Current state
      ↓
     LLM
      ↓
"What should I do next?"
      ↓
Action
      ↓
Result
      ↓
     LLM
      ↓
"What should I do next?"
```

The next step can change depending on the situation.

## A Simple Example

Suppose we build a travel assistant. One user asks *"Find me a cheap hotel in Istanbul and tell me whether it's close to the main attractions."* The agent might decide:

```
User request
     ↓
Search hotels
     ↓
Found candidates
     ↓
Check hotel locations
     ↓
Need attraction information? → Yes
     ↓
Search attractions
     ↓
Calculate distances
     ↓
Compare hotels
     ↓
Answer
```

Another user asks *"What is the best hotel in Istanbul for a business trip?"* The agent might instead do:

```
Search hotels
     ↓
Check business facilities
     ↓
Compare ratings
     ↓
Answer
```

The sequence isn't necessarily identical -- the agent **chooses based on the problem**.

## Workflow vs Agent, Visually

```
WORKFLOW                          AGENT
 Developer                         Goal
    ↓                               ↓
 ┌────────┐                   ┌───────────┐
 │ Step 1 │                   │    LLM    │
 └───┬────┘                   │  Decide   │
     ↓                        └─────┬─────┘
 ┌────────┐                         ↓
 │ Step 2 │                    Action A
 └───┬────┘                         ↓
     ↓                          Result
 ┌────────┐                         ↓
 │ Step 3 │                   ┌───────────┐
 └───┬────┘                   │    LLM    │
     ↓                        │  Decide   │
   Result                     └─────┬─────┘
                                   ↙ ↘
                             Action B  Action C
```

The key difference is **who controls the path**.

## A Very Important Engineering Rule

Don't think *"agents are more advanced, therefore agents are better."* That's wrong. A better rule is:

**Use the simplest architecture that reliably solves the problem.**

If the process is predictable, use a workflow. If the process requires dynamic decisions, consider an agent.

## Example: Customer Support

*"I want to reset my password"* -- a workflow is probably enough:

```
Request → Identify intent → Send reset instructions → Done
```

There is little reason for an autonomous agent here. Now imagine: *"My account is locked, I was charged twice, and I also want to change my shipping address."* The system may need to:

```
Understand multiple problems
       ↓
Check account
       ↓
Check payment
       ↓
Check orders
       ↓
Determine appropriate actions
       ↓
Possibly ask user for confirmation
       ↓
Execute actions
```

Dynamic decision-making becomes more useful here.

## Workflow + LLM Does NOT Automatically Mean Agent

This is a common misconception. Consider:

```
def application(question):
    classification = llm(question)

    if classification == "technical":
        return technical_rag(question)

    if classification == "billing":
        return billing_rag(question)
```

There is an LLM. There is decision-making. But the developer still defined the possible flow: `technical → technical_rag`, `billing → billing_rag`. This is better described as an **LLM-powered workflow/router**, not necessarily a fully autonomous agent. This distinction matters because "agent" is often used too loosely.

## Agent Autonomy Exists on a Spectrum

It's not simply Workflow OR Agent. There is a spectrum:

```
More deterministic                                     More autonomous
Workflow  →  Router  →  Tool-using system  →  Agent
```

Very deterministic:

```
Question → Search → Answer
```

Some dynamic behavior:

```
Question
 ↓
LLM chooses:
 ├── RAG
 ├── Database
 └── API
```

More autonomous:

```
Goal → LLM decides → Tool → Observe → LLM decides again → Tool → Observe → ...
```

The farther right you go, the more important **state, tool control, limits, evaluation, and security** become. We'll learn those later.

## Connecting This to Agentic RAG

Normal RAG:

```
Question → Retriever → Documents → LLM → Answer
```

The retrieval process is predetermined. Agentic RAG:

```
Question
 ↓
Agent
 ↓
Should I retrieve?
 ↓
Which retrieval strategy?
 ↓
Search
 ↓
Are results good enough?
 ↓
No → Search again / rewrite query
 ↓
Yes → Answer
```

The agent **controls the retrieval process**. That's why Agentic RAG is more flexible -- but also more complex.

## When Should You Use a Workflow?

Use a workflow when:

1. **The process is predictable** -- e.g. `Upload PDF → Extract → Chunk → Embed → Store`
2. **You need reliability** -- you want the same steps every time
3. **You care about latency** -- agents may require multiple LLM calls
4. **You want easy debugging** -- you can inspect Step 1, Step 2, Step 3 directly

## When Should You Use an Agent?

Consider an agent when:

1. **The path is unpredictable** -- you don't know exactly which actions will be required
2. **There are many possible tools** -- `search_web()`, `query_database()`, `send_email()`, `calculate()`, `search_documents()`, `create_report()` -- the agent can select among them
3. **The task requires iterative decisions** -- e.g. `Search → Evaluate → Search again → Compare → Calculate → Verify → Answer`
4. **The goal matters more than a fixed sequence** -- instead of *"always perform these 7 steps"*, you say *"achieve this goal using the available tools"*

## The Biggest Trade-Off

Agents give you **flexibility**, but you pay with **complexity**:

```
Workflow                          Agent
  ↓                                 ↓
Predictable                     Dynamic
  ↓                                 ↓
Easy to test                  More LLM calls
  ↓                                 ↓
Easy to debug              More possible failures
                                    ↓
                             Harder to test
```

So in production AI engineering: **more autonomous does not automatically mean more professional**. A well-designed deterministic workflow can be much better than an unnecessary agent.

## A Practical Decision Rule

When designing an AI application, ask:

1. **Do I know the steps beforehand?** If yes → Workflow. If no → keep evaluating.
2. **Does the system need to choose between different actions?** If yes → an agent-like architecture may help.
3. **Can a simpler router or workflow solve it?** If yes → prefer the simpler solution.

That last question is extremely important.

*The single idea to keep: a workflow means "do these steps" and an agent means "achieve this goal, decide what to do" -- use agents only when dynamic decision-making is actually needed, never just because agents are fashionable.*
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Academic Assistant: Workflow, Agent, or Neither?",
                    "description": (
                        "System A always runs: Question → Search university documents → Retrieve top 5 chunks → Generate answer. "
                        "System B can decide to search university documents, query a student database, calculate GPA, ask the user "
                        "for clarification, or search again -- in any order. Answer in your own words: "
                        "(1) Is System A a workflow or an agent? "
                        "(2) Is System B more suitable for an agent? Why? "
                        "(3) Give one reason you might still prefer a workflow over an agent for System B."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "system-design"],
                },
                {
                    "title": "Refactor a Router into an Explicit Workflow",
                    "description": (
                        "The `application()` router below uses an LLM to classify a question, then calls a fixed branch. "
                        "Even though it involves an LLM call, argue in code comments (or a short rewrite) why this is a "
                        "workflow/router rather than an agent, and add a third branch (`\"account\"` → `account_rag`) "
                        "the same way the existing branches are structured -- without introducing a decision loop."
                    ),
                    "starter_code": (
                        "def application(question):\n"
                        "    classification = llm(question)\n\n"
                        "    if classification == \"technical\":\n"
                        "        return technical_rag(question)\n\n"
                        "    if classification == \"billing\":\n"
                        "        return billing_rag(question)\n\n"
                        "    # TODO: add an \"account\" branch calling account_rag(question)\n"
                        "    # TODO: add a short comment explaining why this is still a workflow, not an agent\n"
                    ),
                    "solution_code": (
                        "def application(question):\n"
                        "    classification = llm(question)\n\n"
                        "    if classification == \"technical\":\n"
                        "        return technical_rag(question)\n\n"
                        "    if classification == \"billing\":\n"
                        "        return billing_rag(question)\n\n"
                        "    if classification == \"account\":\n"
                        "        return account_rag(question)\n\n"
                        "    # Still a workflow: the developer enumerated every possible branch\n"
                        "    # (technical / billing / account) in advance. The LLM only picks which\n"
                        "    # pre-defined branch to take -- it cannot invent a new action or loop\n"
                        "    # back to decide again, so there's no decide->act->observe cycle.\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "system-design"],
                },
            ],
            "quiz": {
                "title": "Workflow vs Agent — Knowledge Check",
                "questions": [
                    {
                        "question": "Which statement best captures the core difference between a workflow and an agent?",
                        "options": [
                            "A workflow always uses more tools than an agent",
                            "In a workflow the developer decides the steps in advance; in an agent the LLM decides the next action at runtime",
                            "A workflow never involves an LLM",
                            "An agent is simply a workflow that runs faster",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's core rule: Workflow = developer decides the steps. Agent = the AI decides the steps, dynamically, based on the current state.",
                    },
                    {
                        "question": "A function classifies a question as 'technical' or 'billing' with an LLM call, then always routes to one of two fixed functions accordingly. What is this best described as?",
                        "options": [
                            "A fully autonomous agent",
                            "An LLM-powered workflow/router, since the developer still defined every possible branch",
                            "Agentic RAG",
                            "A decision loop",
                        ],
                        "correct": 1,
                        "explanation": "Using an LLM for classification doesn't make something an agent. The developer enumerated the branches in advance -- that's an LLM-powered router, not an autonomous decision loop.",
                    },
                    {
                        "question": "On the autonomy spectrum described in the lesson (Workflow → Router → Tool-using system → Agent), what generally becomes MORE important as you move toward the 'Agent' end?",
                        "options": [
                            "State, tool control, limits, evaluation, and security",
                            "The need to hard-code every step in advance",
                            "Avoiding the use of any tools",
                            "Reducing the number of LLM calls to zero",
                        ],
                        "correct": 0,
                        "explanation": "As systems become more autonomous, tracking state, controlling which tools can be used, setting limits, evaluating behavior, and securing actions all become more critical concerns.",
                    },
                    {
                        "question": "Per the lesson's practical decision rule, what should you check FIRST when deciding between a workflow and an agent?",
                        "options": [
                            "Whether the marketing team prefers the word 'agent'",
                            "Whether you already know the steps beforehand -- if yes, prefer a workflow",
                            "Whether the model supports function calling",
                            "Whether the task involves any LLM call at all",
                        ],
                        "correct": 1,
                        "explanation": "The first question in the decision rule is: do I know the steps beforehand? If yes, a workflow is the simpler, more reliable choice.",
                    },
                    {
                        "question": "What is the main trade-off the lesson describes when choosing an agent over a workflow?",
                        "options": [
                            "Agents are always cheaper but less accurate",
                            "Agents trade flexibility for complexity: more LLM calls, more possible failures, and harder testing",
                            "Workflows cannot use any tools at all",
                            "There is no trade-off; agents strictly dominate workflows",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: agents give you flexibility but you pay with complexity -- more LLM calls, more possible failure points, and harder testing/debugging compared to a predictable workflow.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 3
        # ------------------------------------------------------------
        {
            "title": "Tools",
            "slug": "ai-developer-ai-agents-tools",
            "description": "What a tool is, how it differs from a plain Python function, the read-only vs action-tool distinction, and the design principles (clear name, description, inputs, limited responsibility) that make tools usable and safe for an agent to call.",
            "order": 3,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "tool-use", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Tools",
                "content": """# Tools

Now we move to one of the most fundamental components of an AI agent: **tools**. If an agent is the "decision maker," tools are the things it can actually *do*.

## The Problem an LLM Has

An LLM by itself is mainly good at processing and generating information. Ask it *"What is 25 × 48?"* and it can answer directly. But ask *"Check my bank balance"* and the LLM cannot magically access your bank account. Ask *"What's the weather in Cairo right now?"* and the model needs access to a weather service. Ask *"Send an email to Ahmed"* and the model needs access to an email system.

So we give the agent **tools**.

## What Is a Tool?

A **tool** is simply a function that an AI system is allowed to call to perform an action or retrieve information. For example:

```
def calculator(a, b):
    return a + b
```

This Python function can become a tool available to an agent:

```
User: "Calculate 25 + 17."
       ↓
      Agent
       ↓
calculator(25, 17)
       ↓
      42
```

The important part: **the LLM decides when the tool is useful, but the actual function executes the operation.**

## Tool Mental Model

Think of an agent like a person. The person has a 🧠 **brain** (the LLM), 🛠️ **tools** (capabilities), 📋 **memory/state** (what they currently know), and a 🎯 **goal** (what they're trying to accomplish):

```
                AGENT
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
       LLM                Tools
    Decision               │
                           ├── Search
                           ├── Calculator
                           ├── Database
                           ├── API
                           └── Email
```

The LLM doesn't physically perform every action -- it **chooses which capability to use**.

## Tools Can Do Many Things

Tools aren't limited to APIs. They can be almost any controlled function: a search tool (`search(query)`), a calculator (`calculate(expression)`), a database lookup (`get_student(student_id)`), a weather lookup (`get_weather(city)`), file operations (`read_file(path)`), RAG retrieval (`search_documents(query)`), an external API (`get_stock_price(symbol)`), or a business action (`create_order(product_id)`).

A tool is essentially an **interface between the AI and the outside world**.

## Tool vs Normal Python Function

Technically, a tool can simply be a function:

```
def calculate_gpa(grades):
    return sum(grades) / len(grades)
```

As a normal Python function, the programmer explicitly calls `calculate_gpa([3.5, 3.8, 4.0])`. But as an **agent tool**:

```
User: "Calculate my GPA."
        ↓
      Agent
        ↓
"calculate_gpa would help."
        ↓
calculate_gpa(...)
```

The **agent decides** whether to call it. That's the important difference.

## Tools Need Descriptions

This is extremely important in real agent systems. Suppose we give an LLM `search()` and `calculator()` -- how does the LLM know what they do? We provide **descriptions**:

```
tools = [
    {"name": "calculator", "description": "Calculate mathematical expressions"},
    {"name": "search", "description": "Search the web for current information"}
]
```

Now the model can reason conceptually: *"User asks 'What is 234 × 17?' Available tools: calculator → mathematical calculations, search → web search. Best tool: calculator."* The tool description is part of the interface the model uses for **tool selection**.

## Tools Have Inputs

A useful tool usually needs parameters:

```
def search_products(query, max_price):
    ...
```

This tool has a **name** (`search_products`), a **description** ("Search products matching a query and maximum price"), and **inputs** (`query`, `max_price`). An agent might determine `search_products(query="laptop", max_price=1000)`. The model doesn't necessarily execute Python itself -- instead, it produces a **structured tool call** that the application executes. We'll study this mechanism deeply in the Function Calling lesson.

## Tools Can Read or Change Things

This distinction is extremely important.

**Read-only tools** retrieve information: `search_web()`, `get_weather()`, `get_student_info()`, `search_documents()`, `get_order_status()`. They don't intentionally change the external world.

**Action tools** perform changes: `send_email()`, `delete_file()`, `create_order()`, `transfer_money()`, `update_address()`, `cancel_subscription()`. These are much more sensitive, because the agent is no longer simply finding information -- it is **causing an external side effect**.

## Why This Matters for AI Engineering

Imagine an agent has `search_web()`, `send_email()`, and `delete_file()`. If the model incorrectly chooses `delete_file()`, you could have a serious problem. So giving an agent a tool is **giving it a capability**, and giving it a capability means you need to think about permissions, validation, authentication, limits, confirmation, logging, and security. We'll study these much more deeply in Agent Security and Human-in-the-Loop.

## Tool Example: Academic Agent

Imagine your university AI assistant has `search_regulations(query)`, `get_course_info(course_code)`, `calculate_gpa(grades)`, and `get_student_schedule(student_id)`.

*"What is my GPA if I get A in ML and B+ in NLP?"*

```
User request → Need GPA calculation → calculate_gpa(...) → Result → Answer
```

*"What are the prerequisites for CSE251?"* -- the agent chooses `get_course_info("CSE251")` instead. The same agent has **multiple capabilities**.

## Tools and RAG

Here's an important connection to your previous knowledge: your RAG retriever can itself become a tool.

```
def search_university_docs(query):
    return vector_database.search(query)
```

An agent can then have:

```
Tools
 ├── search_university_docs()
 ├── calculate_gpa()
 ├── get_course_info()
 └── get_student_schedule()
```

The agent decides: *"What does this question require?" → "Choose capability" → "Call appropriate tool."* So **RAG can be a capability of an agent** rather than the entire architecture -- a very useful mental model.

## A Simple Tool Example

```
def calculator(a: float, b: float, operation: str):
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        return a / b
```

User: *"What is 20 × 5?"* The agent determines `tool = calculator`, `arguments = {a: 20, b: 5, operation: "multiply"}`. The application executes `calculator(a=20, b=5, operation="multiply")` and gets `100`. Then the result goes back to the agent.

## The Complete Interaction

```
User
 │  "What is 20 × 5?"
 ↓
Agent / LLM
 │  decides to use calculator
 ↓
Tool Call
 │  calculator(20, 5, "multiply")
 ↓
Tool Execution
 │  returns 100
 ↓
Agent / LLM
 │  generates final response
 ↓
User
    "The answer is 100."
```

Notice that the **tool execution happens outside the LLM**. That's a critical concept: the LLM *proposes* the action, your *application executes* it.

## Never Blindly Trust Tool Arguments

Suppose we have `transfer_money(amount, recipient)`. You should not simply allow the LLM to execute `transfer_money(amount=10000, recipient="someone")` without validation. A safer architecture is:

```
LLM
 ↓
Tool call
 ↓
Validate arguments
 ↓
Check permissions
 ↓
Maybe ask user confirmation
 ↓
Execute
```

This is how production agent systems should be designed. We'll return to this later.

## A Tool Is an API for the AI

Perhaps the best engineering analogy: **a tool is an API designed for the AI to use.** Humans interact with APIs through code; an agent interacts with tools through structured tool calls. The model doesn't need to know how the weather API works internally -- it only needs to understand `get_weather(city)` and what it returns. This abstraction makes agents much easier to build.

## Good Tool Design

A good agent tool should generally have:

- **A clear name** -- `search_products` is good, `do_thing` is bad
- **A clear description** -- e.g. "Search products by keyword and maximum price"
- **Clear inputs** -- `query: string`, `max_price: number`
- **Predictable output** -- e.g. `{"products": [{"name": "Laptop A", "price": 900}]}`
- **Limited responsibility** -- prefer `search_products()` over a giant `do_everything()`

Small, well-defined tools are generally easier for agents to use correctly.

## Tools Don't Make an Agent Intelligent by Themselves

Suppose you give an agent 50 tools -- that doesn't automatically make it better. In fact, too many tools can make selection harder: the model has more possibilities to consider. So **tool design is an AI engineering problem, not just a programming problem.** You want the *right* tools with clear interfaces and appropriate permissions.

## The Architecture We've Built So Far

- **Lesson 1:** Agent = goal + decision-making + actions + loop
- **Lesson 2:** Workflow → developer controls steps. Agent → LLM can choose next action.
- **Lesson 3 (now):**

```
Agent
  ↓
LLM decides
  ↓
Tool
  ↓
External capability
  ↓
Result
  ↓
Agent
```

The next lesson will explain how the LLM actually *requests* those tools -- a mechanism called **Function Calling**.

*The single idea to keep: a tool is a controlled capability -- not permission for the LLM to do anything it wants -- and the flow is always User → LLM → Tool Call → Application executes tool → Tool Result → LLM → Final Answer.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Real-Estate Investment Assistant: Tool Selection",
                    "description": (
                        "An agent has these capabilities: search_properties(), calculate_roi(), get_property_details(), send_report(). "
                        "A user says: \"Find apartments in New Cairo under 5 million EGP, calculate their expected ROI, and send me a report.\" "
                        "Answer: (1) Which tools would the agent probably use, and in roughly what order? "
                        "(2) Which tool is read-only, and which tool causes an external side effect? "
                        "(3) Why shouldn't send_report() execute blindly just because the LLM requested it? "
                        "(4) What information would the agent need to pass to calculate_roi()?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "tool-use"],
                },
                {
                    "title": "Design and Validate a Tool",
                    "description": (
                        "Write a `get_course_info(course_code)` tool for the academic agent described in the lesson. It should "
                        "return a dict with course name, credits, and prerequisites for a small hard-coded course catalog. Then write "
                        "a `validate_tool_call(tool_name, arguments)` guard function that rejects the call if `course_code` is missing "
                        "or not a string -- following the 'never blindly trust tool arguments' principle from the lesson."
                    ),
                    "starter_code": (
                        "COURSE_CATALOG = {\n"
                        "    \"CSE251\": {\"name\": \"Machine Learning\", \"credits\": 3, \"prerequisites\": [\"CSE201\"]},\n"
                        "}\n\n"
                        "def get_course_info(course_code):\n"
                        "    # TODO: look up course_code in COURSE_CATALOG and return its info,\n"
                        "    # or a clear \"not found\" result if it doesn't exist\n"
                        "    pass\n\n"
                        "def validate_tool_call(tool_name, arguments):\n"
                        "    # TODO: return True/False (or raise) based on whether arguments are valid\n"
                        "    # for the given tool_name -- for get_course_info, course_code must be a\n"
                        "    # non-empty string\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "COURSE_CATALOG = {\n"
                        "    \"CSE251\": {\"name\": \"Machine Learning\", \"credits\": 3, \"prerequisites\": [\"CSE201\"]},\n"
                        "}\n\n"
                        "def get_course_info(course_code):\n"
                        "    course = COURSE_CATALOG.get(course_code)\n"
                        "    if course is None:\n"
                        "        return {\"error\": f\"No course found for '{course_code}'\"}\n"
                        "    return course\n\n"
                        "def validate_tool_call(tool_name, arguments):\n"
                        "    if tool_name == \"get_course_info\":\n"
                        "        code = arguments.get(\"course_code\")\n"
                        "        return isinstance(code, str) and len(code) > 0\n"
                        "    return False\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "tool-use"],
                },
            ],
            "quiz": {
                "title": "Tools — Knowledge Check",
                "questions": [
                    {
                        "question": "What is a tool, in the agent sense described in the lesson?",
                        "options": [
                            "A larger LLM used only for hard problems",
                            "A function that an AI system is allowed to call to perform an action or retrieve information",
                            "A special type of vector database",
                            "A prompt template with no code involved",
                        ],
                        "correct": 1,
                        "explanation": "A tool is a controlled function the agent can call -- it's the interface between the AI and the outside world.",
                    },
                    {
                        "question": "What is the key difference between calling calculate_gpa() as a normal Python function versus exposing it as an agent tool?",
                        "options": [
                            "There is no difference -- tools and functions are identical",
                            "As a tool, the agent (LLM) decides whether and when to call it, rather than the programmer calling it explicitly",
                            "Tools must always be written in a different programming language",
                            "Tools cannot accept any parameters",
                        ],
                        "correct": 1,
                        "explanation": "The function itself can be identical. What changes is who decides to call it: the programmer (normal function) vs. the agent choosing it at runtime (tool).",
                    },
                    {
                        "question": "Why do tools need descriptions when exposed to an LLM?",
                        "options": [
                            "Descriptions are purely cosmetic and don't affect behavior",
                            "The description is part of the interface the model uses to decide which tool fits the user's request",
                            "Descriptions replace the need for input parameters",
                            "Descriptions are only needed for action tools, never for read-only tools",
                        ],
                        "correct": 1,
                        "explanation": "Since the LLM can't read the function's source code at call time, the description (plus name and inputs) is how it reasons about which tool is the best fit.",
                    },
                    {
                        "question": "Which pair correctly matches the read-only vs action tool distinction from the lesson?",
                        "options": [
                            "get_weather() is an action tool; send_email() is read-only",
                            "search_documents() is read-only; transfer_money() is an action tool",
                            "Both get_order_status() and delete_file() are read-only",
                            "There is no meaningful distinction between the two categories",
                        ],
                        "correct": 1,
                        "explanation": "search_documents() only retrieves information (read-only). transfer_money() causes an external side effect (action tool), which is why it needs extra scrutiny like validation and permissions.",
                    },
                    {
                        "question": "Per the lesson's safer architecture for tool calls, what should happen between the LLM proposing a tool call and the application actually executing it?",
                        "options": [
                            "Nothing -- the LLM's tool call should execute immediately and unconditionally",
                            "Validate arguments, check permissions, and possibly ask for user confirmation before executing",
                            "The LLM should execute the tool's code directly inside itself",
                            "The tool call should be discarded and replaced with a hard-coded workflow",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's safer architecture is: LLM → tool call → validate arguments → check permissions → maybe confirm with user → execute. The LLM proposes; the application is responsible for executing safely.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 4
        # ------------------------------------------------------------
        {
            "title": "Function Calling",
            "slug": "ai-developer-ai-agents-function-calling",
            "description": "The mechanism by which an LLM requests a tool be run: structured tool calls instead of natural-language instructions, why schemas and validation matter, and how function calling relates to (but isn't the same as) an agent.",
            "order": 4,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "function-calling", "tool-use"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Function Calling",
                "content": """# Function Calling

Now we answer an important question: **how does an LLM actually tell our application that it wants to use a tool?** The answer is **function calling**.

## The Problem

In the previous lesson, we had:

```
User → LLM → Tool
```

But there's a missing detail. How does the LLM say *"I want you to call calculator with a=20, b=5, and operation=multiply"*? It doesn't directly execute Python. Instead, it produces a **structured tool call**. That's function calling.

## The Mental Model

Think of function calling as a **communication protocol** between the LLM and your application. The LLM says *"I want this function called with these arguments."* Your application says *"Okay, I'll execute it."* Then the result is sent back to the LLM:

```
User
 ↓
LLM
 ↓
Function Call
 ↓
Application
 ↓
Execute Function
 ↓
Function Result
 ↓
LLM
 ↓
Final Answer
```

## Function Calling Is NOT the LLM Executing Python

This distinction is extremely important. Suppose we have:

```
def calculator(a, b):
    return a + b
```

The LLM does **not** magically execute `calculator(10, 20)`. Instead, it generates something conceptually like:

```
{
  "name": "calculator",
  "arguments": {
    "a": 10,
    "b": 20
  }
}
```

Your application receives this. Then your Python code does `result = calculator(10, 20)`. The result (`30`) is then returned to the LLM.

## Why Structured Output Matters

Imagine the LLM simply responds *"Please call calculator with 10 and 20."* Your application would need to parse natural language -- that's unreliable. Instead, we want a structured object like the JSON above, so your application knows exactly which tool and which arguments. This makes tool usage much more reliable.

## A Simple Example

```
def calculator(a: float, b: float, operation: str):
    if operation == "add":
        return a + b
    if operation == "multiply":
        return a * b
```

We tell the LLM this tool exists. Conceptually, its definition might look like:

```
calculator_tool = {
    "name": "calculator",
    "description": "Perform basic mathematical calculations.",
    "parameters": {
        "a": "number",
        "b": "number",
        "operation": "add or multiply"
    }
}
```

User: *"What is 25 × 4?"* The LLM might return:

```
{
  "name": "calculator",
  "arguments": {"a": 25, "b": 4, "operation": "multiply"}
}
```

Your application executes `calculator(25, 4, "multiply")` → `100`. The LLM can then respond: *"25 × 4 = 100."*

## The Complete Flow

```
1. User      → "What is 25 × 4?"
2. LLM       → recognizes this requires a calculation, chooses calculator
3. Function call → {"name": "calculator", "arguments": {"a": 25, "b": 4, "operation": "multiply"}}
4. Application → executes calculator(25, 4, "multiply")
5. Tool result  → 100
6. Send result to LLM → "calculator returned 100"
7. Final response      → "The answer is 100."
```

## Why This Is Powerful

Imagine we provide multiple tools: `search_web()`, `calculator()`, `get_weather()`, `search_documents()`, `get_order()`. Ask *"What's the weather in Cairo?"* → the LLM chooses `get_weather()`. Ask *"What is 456 × 72?"* → it chooses `calculator()`. Ask about a university regulation → it chooses `search_documents()`. Function calling gives the LLM a **structured way to interact with capabilities**.

## Function Calling vs Normal Text Generation

Without function calling, the LLM might just say *"Call calculator with 20 and 5"* in plain text, which your application would have to interpret. With function calling, the LLM produces a **structured tool call** directly. That's why function calling is a fundamental building block of modern agents.

## Multiple Tools

Suppose our agent has `search_products`, `calculate_price`, `get_shipping_cost`. User: *"Find a laptop under $1000 and tell me its final price including shipping."* The agent might chain calls: `search_products()` → laptop = $900 → `calculate_price()` → `get_shipping_cost()` → final answer. Depending on the system, the agent may make **multiple function calls** -- this is where function calling starts connecting directly to agent loops.

## Function Calling Doesn't Automatically Make Something an Agent

Important distinction. You can use function calling in a simple application:

```
Question → LLM → Tool Call → Tool → Answer
```

That's **tool use**. An agent typically goes further, looping:

```
Goal → LLM decides → Tool → Observe result → LLM decides again → Another tool → Observe → ...
```

So: **function calling is a mechanism. An agent is an architecture/system that can use mechanisms like function calling to pursue a goal.**

## Function Calling and APIs

This becomes especially useful when tools wrap APIs:

```
def get_weather(city):
    response = weather_api(city)
    return response
```

The LLM doesn't need to know how the weather API works internally -- it only sees `get_weather(city)`. Then `LLM → get_weather("Cairo") → Python function → Weather API → Result → LLM`. Function calling creates a bridge: **LLM → your Python code → external systems**.

## Function Calling and Your RAG Knowledge

Your RAG retrieval function could be `search_documents(query)`, exposed as a tool. Now the LLM can decide: *"I need information from the knowledge base"* → `search_documents(query)` → retrieved chunks → LLM → answer. This is one way an agent can use your existing RAG system -- your **retriever becomes a tool**.

## Tool Schema

A **tool schema** describes what the tool is, what arguments it accepts, and what types those arguments are:

```
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "parameters": {
    "city": {"type": "string"}
  }
}
```

This tells the LLM: tool = `get_weather`, required input = `city` (string). The model can then produce `{"city": "Cairo"}`. This is why clear schemas and descriptions matter so much.

## What If the Arguments Are Wrong?

This is a real engineering problem. Suppose `get_weather(city)` requires a string, but the model generates `{"city": 12345}`. Your application should **validate the arguments**:

```
LLM
 ↓
Tool Call
 ↓
Validation
 ↓
Valid?
 ├── Yes → Execute
 └── No → Reject / recover
```

Never assume that an LLM-generated tool call is automatically correct.

## Function Calling Is a Contract

A useful mental model: **a tool schema is a contract between the LLM and your application.** The contract says: here is the tool, here is what it does, here are the inputs you can provide, here are the expected types. The LLM tries to satisfy that contract. Your application **enforces** it. This separation is very important in production systems.

## Simple Python Mental Implementation

```
def run_tool(tool_call):
    name = tool_call["name"]
    args = tool_call["arguments"]

    if name == "calculator":
        return calculator(**args)

    if name == "get_weather":
        return get_weather(**args)

    raise ValueError("Unknown tool")
```

Given `tool_call = {"name": "calculator", "arguments": {"a": 10, "b": 5, "operation": "multiply"}}`, `run_tool(tool_call)` returns `50`. This tiny example captures the fundamental mechanism behind much more sophisticated agent frameworks.

## The Architecture So Far

```
                 AGENT
                   │
                   ↓
                  LLM
                   │
             decides action
                   ↓
            Function Call
                   ↓
             Your Application
                   ↓
                Tool
                   ↓
                Result
                   ↓
                  LLM
```

*The single idea to keep: function calling is how an LLM requests a tool -- a structured `{"name": ..., "arguments": {...}}` contract, not code the LLM runs itself -- and the LLM proposes the tool call while your application always validates and executes it.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Real-Estate Agent: Trace the Function Calls",
                    "description": (
                        "An AI real-estate agent has: search_properties(location, max_price), get_property_details(property_id), "
                        "calculate_roi(price, annual_rent). A user says: \"Find apartments in New Cairo below 5 million and calculate "
                        "the ROI of the best one.\" Answer: (1) What tool call might the LLM make first, and with what arguments? "
                        "(2) What information does it need to call calculate_roi()? (3) Why does the application, rather than the LLM "
                        "itself, execute the Python function? (4) If search_properties() returns 10 properties, could the agent make "
                        "another function call afterward? Why?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "function-calling"],
                },
                {
                    "title": "Implement a Tool Dispatcher with Validation",
                    "description": (
                        "Extend the `run_tool()` dispatcher from the lesson to (a) support a `get_shipping_cost(weight_kg, destination)` "
                        "tool in addition to `calculator`, and (b) validate arguments before executing -- raising a clear error instead "
                        "of calling the function if a required argument is missing or the wrong type, following the "
                        "'never assume a tool call is correct' principle from the lesson."
                    ),
                    "starter_code": (
                        "def calculator(a, b, operation):\n"
                        "    if operation == \"add\":\n"
                        "        return a + b\n"
                        "    if operation == \"multiply\":\n"
                        "        return a * b\n"
                        "    raise ValueError(f\"Unknown operation: {operation}\")\n\n"
                        "def get_shipping_cost(weight_kg, destination):\n"
                        "    # TODO: return a simple made-up cost, e.g. weight_kg * 2.5\n"
                        "    pass\n\n"
                        "def run_tool(tool_call):\n"
                        "    name = tool_call[\"name\"]\n"
                        "    args = tool_call[\"arguments\"]\n"
                        "    # TODO: validate args for each tool name before calling it\n"
                        "    # TODO: dispatch to calculator or get_shipping_cost\n"
                        "    # TODO: raise ValueError(\"Unknown tool\") for anything else\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def calculator(a, b, operation):\n"
                        "    if operation == \"add\":\n"
                        "        return a + b\n"
                        "    if operation == \"multiply\":\n"
                        "        return a * b\n"
                        "    raise ValueError(f\"Unknown operation: {operation}\")\n\n"
                        "def get_shipping_cost(weight_kg, destination):\n"
                        "    return weight_kg * 2.5\n\n"
                        "def run_tool(tool_call):\n"
                        "    name = tool_call[\"name\"]\n"
                        "    args = tool_call[\"arguments\"]\n\n"
                        "    if name == \"calculator\":\n"
                        "        if not isinstance(args.get(\"a\"), (int, float)) or not isinstance(args.get(\"b\"), (int, float)):\n"
                        "            raise ValueError(\"calculator requires numeric a and b\")\n"
                        "        return calculator(**args)\n\n"
                        "    if name == \"get_shipping_cost\":\n"
                        "        if not isinstance(args.get(\"weight_kg\"), (int, float)) or not isinstance(args.get(\"destination\"), str):\n"
                        "            raise ValueError(\"get_shipping_cost requires numeric weight_kg and string destination\")\n"
                        "        return get_shipping_cost(**args)\n\n"
                        "    raise ValueError(\"Unknown tool\")\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "function-calling"],
                },
            ],
            "quiz": {
                "title": "Function Calling — Knowledge Check",
                "questions": [
                    {
                        "question": "When an LLM 'calls' a tool like calculator(10, 20), what actually happens?",
                        "options": [
                            "The LLM directly executes the Python function inside itself",
                            "The LLM produces a structured request (e.g. name + arguments) that the application then executes",
                            "The tool call bypasses the application entirely and returns straight to the user",
                            "Function calling requires the LLM to write and run raw Python code",
                        ],
                        "correct": 1,
                        "explanation": "The LLM generates a structured tool call (name + arguments). Your application is responsible for actually executing the underlying function.",
                    },
                    {
                        "question": "Why is structured output (a JSON-like tool call) preferred over the LLM describing the call in natural language?",
                        "options": [
                            "Structured output is shorter, which is the only reason it's used",
                            "Natural language would require unreliable parsing, whereas structured output gives the application an explicit, unambiguous tool name and arguments",
                            "Natural language cannot be generated by LLMs at all",
                            "Structured output removes the need for any validation",
                        ],
                        "correct": 1,
                        "explanation": "Parsing free text like 'please call calculator with 10 and 20' is unreliable. A structured call makes the tool name and arguments explicit and machine-readable.",
                    },
                    {
                        "question": "What is a tool schema, as described in the lesson?",
                        "options": [
                            "A database table that stores tool call logs",
                            "A description of the tool's name, purpose, and expected arguments/types that acts as a contract between the LLM and the application",
                            "A visual diagram used only for documentation, with no effect on the LLM",
                            "A separate model that replaces the main LLM for tool selection",
                        ],
                        "correct": 1,
                        "explanation": "A tool schema (name, description, parameters/types) is the contract the LLM uses to understand and correctly call the tool.",
                    },
                    {
                        "question": "Which statement correctly distinguishes 'function calling' from 'an agent'?",
                        "options": [
                            "They are exactly the same concept with different names",
                            "Function calling is the mechanism an LLM uses to request a tool; an agent is a system that can use that mechanism repeatedly in a decide-act-observe loop toward a goal",
                            "An agent never uses function calling",
                            "Function calling can only be used inside a full agent, never in a simple one-shot application",
                        ],
                        "correct": 1,
                        "explanation": "A single Question → LLM → Tool Call → Tool → Answer flow is just tool use via function calling. An agent goes further, looping through multiple decide/act/observe cycles.",
                    },
                    {
                        "question": "If the LLM generates {\"city\": 12345} for a get_weather(city) tool that expects a string, what should the application do per the lesson?",
                        "options": [
                            "Execute it anyway, since the LLM is usually right",
                            "Validate the arguments first and reject or recover instead of blindly executing",
                            "Silently convert 12345 into a fake city name and proceed",
                            "Shut down the entire agent permanently",
                        ],
                        "correct": 1,
                        "explanation": "The lesson stresses validating tool call arguments before execution -- never assume an LLM-generated tool call is automatically correct.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 5
        # ------------------------------------------------------------
        {
            "title": "Agent State",
            "slug": "ai-developer-ai-agents-agent-state",
            "description": "What agent state is, how it evolves across the decide-act-observe loop, the distinction between state (current task) and memory (persists across tasks), and how state enables multi-step reasoning, error tracking, and loop limits.",
            "order": 5,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "state-management", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Agent State",
                "content": """# Agent State

Now we move to another core concept of agent engineering: **state**. If tools give an agent the ability to *do* things, state gives it the ability to **know what has happened so far**.

## The Problem

Imagine an agent receives *"Find me a laptop under $1,000."* It calls `search_products("laptop", 1000)` and the tool returns three laptops with prices. Then the agent needs to decide: *"Which laptop should I investigate further?"* How does it know the search results? They need to be **stored somewhere**. That's state.

## Simple Mental Model

Think of state as: **everything the agent currently needs to know to continue the task.**

```
State
├── User goal
├── Conversation
├── Previous actions
├── Tool results
├── Current task
└── Intermediate information
```

```
Agent
  ↓
reads state
  ↓
decides next action
  ↓
updates state
  ↓
decides again
```

## Agent Without State

Imagine `User → LLM → Search tool → Result`, then we somehow erase the result. The agent asks itself *"What did the search return?"* -- it doesn't know. Now imagine a multi-step task: `Search → Choose property → Get details → Calculate ROI`. The agent needs to remember which property it chose, its price, its annual rent. **Without state, multi-step agent behavior becomes very difficult.**

## State in a Simple Example

Suppose we're building a real-estate investment agent. Initial state:

```
state = {
    "goal": "Find the best investment apartment under 5M",
    "properties": [],
    "selected_property": None,
    "roi": None
}
```

The agent calls `search_properties()`, gets back a list of properties, and we update `state["properties"] = results`. Now the state contains `goal → properties → selected_property → roi`, and the agent can continue from there.

## State Changes Over Time

Agent state is usually **not static** -- it evolves:

```
Initial:        goal
After search:    goal + search results
After selection: goal + search results + selected property
After calc:      goal + search results + selected property + ROI
```

We can think of an agent as:

```
State₀ → Action → State₁ → Action → State₂ → Action → State₃
```

This concept becomes extremely important when you later work with LangGraph.

## State Is Not the Same as Memory

This distinction is very important. **State** = information needed for the current execution/task. **Memory** = information preserved for future interactions or tasks.

For example, current task state might be `budget = 5M`, `location = New Cairo`, `selected_property = 123`. Memory might contain *"User prefers New Cairo"* or *"User prefers investment properties"* -- information that could remain useful tomorrow. We'll study memory in the next lesson.

## Conversation History Is Part of State

Suppose the conversation goes: *"Find apartments in New Cairo"* → *"I found 20"* → *"Only ones below 5M"* → *"I found 7"* → *"Which has the highest ROI?"* To understand the last request, the system needs context:

```
state = {
    "location": "New Cairo",
    "max_price": 5_000_000,
    "properties": [...],
    "conversation": [...]
}
```

So conversation history can be **one component** of state -- but state can contain much more than conversation.

## State Can Contain Structured Data

Don't think state must be a giant text prompt. It can be structured:

```
state = {
    "user_query": "...",
    "search_query": "...",
    "documents": [...],
    "selected_document": None,
    "tool_results": [],
    "attempts": 0,
    "final_answer": None
}
```

This is much easier to reason about than putting everything into one giant string.

## Example: Agent + RAG

Connecting state to your RAG knowledge. User: *"Can I register this course?"* State begins as `{"question": ..., "documents": [], "answer": None}`. The agent calls `search_documents()`, and state becomes `question + documents`. Maybe the agent decides *"the documents aren't enough, I need course information"* and calls `get_course_info()`. State becomes `question + documents + course_info`. Now it can generate the answer. This is **stateful agentic RAG**.

## State Enables Multi-Step Reasoning

Consider: *"Find the best apartment and calculate whether it has better ROI than the second-best option."* The agent may need candidate properties, property #1 details, property #2 details, ROI #1, ROI #2, and a comparison -- all tracked in state:

```
Search → Update state → Get property details → Update state
       → Calculate ROI → Update state → Compare → Final answer
```

Without state, the agent has no reliable place to maintain intermediate results.

## State and the Agent Loop

Recall our agent loop: `Decide → Act → Observe → Decide again`. We can make it more precise:

```
Read State
    ↓
  Decide
    ↓
   Act
    ↓
Observe Result
    ↓
Update State
    ↓
Read State
    ↓
  Decide again
```

This is a much more useful mental model for real agent systems.

## A Tiny Python Example

```
state = {
    "question": "What is 20 × 5?",
    "tool_result": None
}

tool_call = {
    "name": "calculator",
    "arguments": {"a": 20, "b": 5, "operation": "multiply"}
}

result = calculator(20, 5, "multiply")
state["tool_result"] = result
```

`state` now looks like `{"question": "What is 20 × 5?", "tool_result": 100}`. The LLM can now use the state to generate the final answer.

## State Can Track Errors

State isn't only for successful results. If a search API times out, the agent could update `state = {"attempts": 1, "last_error": "Search timeout"}`. Then the agent might decide to retry, try another tool, or tell the user the search failed. **State can also track execution status and failures.**

## State Can Control Loops

```
state = {"attempts": 0}
```

Every tool call increments `state["attempts"] += 1`, and we can enforce `if state["attempts"] >= 5: stop_agent()`. This is extremely useful -- you don't want an agent to accidentally loop forever. **State helps us implement limits and stopping conditions.**

## State in Production Agents

Real agent state can become more sophisticated, tracking `user_id`, `goal`, `messages`, `current_step`, `tool_calls`, `tool_results`, `documents`, `errors`, `attempt_count`, `requires_approval`, `final_answer`, and more. You don't need to memorize this -- the important idea is: **state is the structured snapshot of where the agent currently is in its task.**

## State in LangGraph

Since you've already worked with LangGraph, this should make the framework much easier to understand. At a high level, LangGraph lets you model:

```
        ┌─────────────┐
        │    State    │
        └──────┬──────┘
               ↓
          Search Node
               ↓
        Updated State
               ↓
          Agent Node
               ↓
        Updated State
               ↓
           Tool Node
               ↓
        Updated State
```

This is one reason state is such a fundamental concept in agent frameworks -- we're learning the architecture first, so that when you see LangGraph code later, you understand *why* it exists rather than just memorizing APIs.

## State Should Be Intentional

A common mistake is putting everything into state (`state = {"everything": ...}`). That's not good design. Ask: *does the agent need this information to continue the task?* If yes, state may make sense. If no, don't necessarily store it. Good state is **relevant, structured, understandable, limited, and easy to update.**

*The single idea to keep: agent state is the information the agent needs to know where it currently is and what it should do next -- the cycle is State → Decide → Action → Result → Update State → Decide again, and state (current task) is not the same as memory (persists across tasks).*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design State for a Multi-Step Comparison Task",
                    "description": (
                        "An agent receives: \"Find the best apartment in New Cairo under 5M, calculate its ROI, and compare it with "
                        "the second-best apartment.\" It has search_properties(), get_property_details(), calculate_roi(). Answer: "
                        "(1) Name at least 4 pieces of information that should be stored in the state. "
                        "(2) After search_properties() returns results, what should happen to the state? "
                        "(3) Why does the agent need state before calling calculate_roi()? "
                        "(4) Give one example of something that would be better considered memory rather than current task state."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "state-management"],
                },
                {
                    "title": "Implement a Bounded Stateful Loop",
                    "description": (
                        "Implement `run_agent(state, decide_fn, execute_tool_fn, max_attempts=5)` that repeatedly calls `decide_fn(state)` "
                        "to get a decision, executes the chosen tool via `execute_tool_fn`, updates `state['tool_results']` and "
                        "`state['attempts']` after each call, and stops -- returning the final answer or raising a clear error -- once "
                        "either a 'final' decision is returned or `max_attempts` is reached. This mirrors the 'state can control loops' "
                        "principle from the lesson."
                    ),
                    "starter_code": (
                        "def run_agent(state, decide_fn, execute_tool_fn, max_attempts=5):\n"
                        "    # state should look like: {\"goal\": ..., \"tool_results\": [], \"attempts\": 0}\n"
                        "    # decide_fn(state) returns either {\"type\": \"tool\", \"tool\": name, \"arguments\": {...}}\n"
                        "    # or {\"type\": \"final\", \"answer\": ...}\n"
                        "    # TODO: implement the read-state -> decide -> act -> update-state loop\n"
                        "    # TODO: stop and raise an error if state['attempts'] reaches max_attempts without a final answer\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def run_agent(state, decide_fn, execute_tool_fn, max_attempts=5):\n"
                        "    while True:\n"
                        "        if state[\"attempts\"] >= max_attempts:\n"
                        "            raise RuntimeError(\"Max attempts reached without a final answer\")\n\n"
                        "        decision = decide_fn(state)\n\n"
                        "        if decision[\"type\"] == \"final\":\n"
                        "            return decision[\"answer\"]\n\n"
                        "        if decision[\"type\"] == \"tool\":\n"
                        "            result = execute_tool_fn(decision[\"tool\"], decision[\"arguments\"])\n"
                        "            state[\"tool_results\"].append(result)\n"
                        "            state[\"attempts\"] += 1\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "state-management"],
                },
            ],
            "quiz": {
                "title": "Agent State — Knowledge Check",
                "questions": [
                    {
                        "question": "What is agent state, per the lesson's definition?",
                        "options": [
                            "The permanent weights of the LLM being used",
                            "Everything the agent currently needs to know to continue the task",
                            "A separate LLM dedicated only to remembering things",
                            "The list of all tools the agent is allowed to ever call",
                        ],
                        "correct": 1,
                        "explanation": "State is the structured snapshot of information the agent needs to continue its current task -- goal, tool results, intermediate data, and so on.",
                    },
                    {
                        "question": "How does the lesson distinguish state from memory?",
                        "options": [
                            "State and memory are exactly the same thing",
                            "State is information needed for the current task/execution; memory is information preserved for future interactions or tasks",
                            "Memory only exists inside vector databases, while state never does",
                            "State is always larger than memory",
                        ],
                        "correct": 1,
                        "explanation": "State = current task info (e.g. selected_property, budget). Memory = information like long-term preferences that could still be useful in a future, separate interaction.",
                    },
                    {
                        "question": "In the more precise agent loop from the lesson, what step comes immediately after 'Observe Result'?",
                        "options": [
                            "Read State",
                            "Update State",
                            "Decide again",
                            "Stop the agent permanently",
                        ],
                        "correct": 1,
                        "explanation": "The refined loop is: Read State → Decide → Act → Observe Result → Update State → Read State → Decide again. The result is folded into state before the next decision.",
                    },
                    {
                        "question": "Why is state described as useful for controlling loops (e.g. tracking 'attempts')?",
                        "options": [
                            "It isn't -- loop control has nothing to do with state",
                            "Because incrementing a counter in state and checking it against a limit lets you stop an agent from looping forever",
                            "Because state automatically limits an agent to exactly one tool call",
                            "Because only memory, not state, can track attempt counts",
                        ],
                        "correct": 1,
                        "explanation": "By storing an attempts counter in state and checking it (e.g. `if state['attempts'] >= 5: stop_agent()`), you can enforce a hard stopping condition on the loop.",
                    },
                    {
                        "question": "According to the lesson, what's the problem with a design like state = {\"everything\": ...}?",
                        "options": [
                            "Nothing -- more state is always strictly better",
                            "It violates the principle that good state should be relevant, structured, understandable, and limited to what the task actually needs",
                            "Python dictionaries cannot hold more than a few keys",
                            "It is required for LangGraph to work at all",
                        ],
                        "correct": 1,
                        "explanation": "The lesson warns against dumping everything into state. Good state should be intentional: only what the agent actually needs to continue the task, kept structured and limited.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 6
        # ------------------------------------------------------------
        {
            "title": "Memory",
            "slug": "ai-developer-ai-agents-memory",
            "description": "The distinction between state (current task) and memory (persistent context), short-term vs long-term memory, how semantic memory relates to your RAG knowledge, and the engineering problems memory introduces: relevance, freshness, conflicts, and privacy.",
            "order": 6,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "memory", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Memory",
                "content": """# Memory

In the previous lesson we learned **state**. Now we need to answer a very important question: **what happens when the agent needs to remember something beyond the current task?** That's where memory comes in.

## State vs Memory

The easiest mental model: **state = what the agent remembers during the current task. Memory = what the system chooses to remember for later.**

Think about a human. If you're solving a math problem, you keep intermediate calculations in your head -- that's like state. If you remember your friend's favorite programming language tomorrow -- that's like memory.

## Simple Example

User: *"Find me an apartment in New Cairo."* During this task, the agent might have:

```
state = {
    "location": "New Cairo",
    "budget": 5_000_000,
    "properties": [...],
    "selected_property": 123
}
```

That's current state. Now the user says *"I prefer apartments with high rental yield."* The system might decide to **remember this preference**. Later, the user asks *"Find me another investment apartment,"* and the system retrieves *"User preference: high rental yield."* That's memory.

## Why Do Agents Need Memory?

Without memory, every conversation starts almost from zero:

```
Monday:  User: "I prefer properties with high rental yield." → Agent: "Got it."
Tuesday: User: "Find me an investment property." → Agent: "What kind do you prefer?"
```

The user has to repeat themselves. With memory:

```
Past interaction → Saved preference → Future interaction → Agent uses preference
```

This makes the system feel much more useful and personalized.

## Memory Is Not Just Conversation History

You might think *"memory = chat history."* Not exactly. Chat history is a raw sequence of turns. **Memory can be derived information from those conversations.** For example, the conversation *"I usually invest for 5+ years"* becomes the memory *"user investment horizon = long-term."* The system doesn't necessarily need to store every word the user ever said -- it can store **useful information**.

## Two Major Types of Memory

**Short-term memory** -- information relevant to the current conversation/task: current conversation, current task, recent tool results, current state.

**Long-term memory** -- information that can persist across conversations: user preferences, past decisions, useful facts, learned preferences.

```
              Agent
                │
        ┌───────┴────────┐
        ↓                ↓
 Short-term          Long-term
   memory              memory
        ↓                ↓
 Current task       Future tasks
```

## Short-Term Memory

Suppose the user says: *"Find apartments in New Cairo."* → *"Under 5 million."* → *"Only 2-bedroom apartments."* → *"Which has the highest ROI?"* The agent needs to remember `location = New Cairo`, `budget = 5M`, `bedrooms = 2` -- information relevant to the **current conversation**. That's short-term memory/context.

## Long-Term Memory

Now suppose the user says *"I generally prefer New Cairo because I already own a property there."* That could be useful in future conversations. The system might store:

```
{"preference": "New Cairo", "reason": "User prefers investing in familiar areas"}
```

Later, when the user asks *"Find me an investment property,"* the system can retrieve the relevant memory.

## Memory Lifecycle

```
Conversation
     ↓
Identify useful information
     ↓
Store memory
     ↓
Future conversation
     ↓
Retrieve relevant memory
     ↓
Agent uses it
```

So memory has two major operations: **WRITE** (store something useful) and **READ** (retrieve something useful) -- very similar to databases.

## Memory Can Be Stored in Many Ways

Memory doesn't require some magical "AI memory system." It can be stored using normal technologies: a **simple database** (PostgreSQL, e.g. `user_id | preference`), a **key-value store** (Redis), or a **vector database** (Qdrant, FAISS, Chroma) for semantic retrieval. For example, stored memory *"I prefer long-term real estate investments"* matched against a new request *"I want something for 7-10 years"* via semantic search. You already understand embeddings and vector search, so this should look familiar.

## Memory + RAG

You already know `Documents → Chunks → Embeddings → Vector DB → Retrieve`. You can build memory using a similar architecture:

```
User interaction → Important memory → Embedding → Vector DB
```

Later: `New user request → Embedding → Memory retrieval → Relevant memories → Agent`. So: **long-term semantic memory can be implemented using techniques very similar to RAG.** The difference is the data being retrieved -- RAG retrieves external knowledge, memory retrieves information about previous interactions or learned user/context information.

## Memory Should Be Selective

This is a very important engineering principle: **you shouldn't save everything.** Imagine storing every sentence a user has ever written -- after months you have 10,000 memories, and retrieval becomes harder. Instead ask: *"is this information likely to be useful later?"* Good memory: *"User prefers Python," "User prefers long-term property investments."* Potentially useless memory: *"User said 'hello' on Tuesday."* Memory should have a **purpose**.

## Memory Can Also Be Wrong

This is one of the biggest challenges. Suppose the user says *"I prefer apartments in New Cairo,"* then six months later *"Actually, I'm no longer interested in New Cairo."* If the old memory remains `prefers New Cairo = true`, the agent might make bad recommendations. Memory needs mechanisms for **updating, correcting, deleting, expiring, and prioritizing**. Memory is data, and data can become stale.

## Memory Should Not Override the User

Suppose memory says *"User prefers New Cairo,"* but the user says *"This time, search in Sheikh Zayed."* The **current request should win**:

```
Current instruction
       ↓
      wins
       ↑
Long-term memory
```

Memory is context. It isn't an absolute command.

## Memory vs State vs Knowledge

- **Knowledge** -- information about the world, e.g. *"Qdrant is a vector database."*
- **State** -- information about the current task, e.g. `current_query = "Find apartments"`
- **Memory** -- information preserved from previous interactions, e.g. `user_prefers = "high rental yield"`

This distinction is extremely useful when designing AI systems.

## Agent With Memory

```
                   User
                     ↓
                  Agent
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
        State                 Memory
          ↓                     ↓
   Current task           Past information
          │                     │
          └──────────┬──────────┘
                     ↓
                    LLM
                     ↓
                   Tools
```

The agent can use both what is happening now and what it learned/remembered before.

## Memory Retrieval

Suppose we have many memories: *"I prefer New Cairo," "I like high rental yield," "I usually invest for 7-10 years."* New query: *"Find me a long-term investment."* A semantic memory retriever might identify *"I usually invest for 7-10 years"* as highly relevant. This is where your knowledge of embeddings + semantic search becomes directly useful.

## Memory Isn't Necessarily Vector Search

Don't assume memory = vector database -- that's only one implementation. You could use SQL, Redis, a document database, a vector database, or a knowledge graph. The correct choice depends on the type of memory: an exact structured preference (`preferred_language = "Python"`) fits SQL/key-value storage; semantic memory (*"I prefer investments that generate steady passive income"*) fits vector retrieval; complex relationships (`User → owns → Property → located_in → New Cairo`) fit a graph structure.

## Memory Introduces New Engineering Problems

Once you add memory, you need to think about **relevance** (should this memory be retrieved?), **freshness** (is it still true?), **conflicts** (what if two memories disagree?), **privacy** (should this be stored at all?), **storage** (where should it live?), **retrieval** (how do we find the right memory?), and **deletion** (can the user remove it?). These become important in real production agents.

*The single idea to keep: state helps the agent continue the current task, while memory helps the agent behave intelligently in future interactions -- and memory should be selective, updatable, and always subordinate to the user's current instruction.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Classify State vs Memory vs Neither",
                    "description": (
                        "Your AI real-estate agent has these pieces of information: (1) The user currently wants an apartment under 5M. "
                        "(2) The user prefers high rental yield. (3) The agent found 10 properties during the current search. "
                        "(4) The user usually prefers New Cairo. (5) Property #7 is currently selected for ROI calculation. "
                        "(6) The user once asked about apartments in 2024. (7) The agent has calculated a 12% ROI for Property #7. "
                        "Classify each as State, Memory, or Probably neither/not useful, and explain briefly. Then answer: if the user "
                        "says 'This time, search in Sheikh Zayed,' should the agent still prioritize its memory that the user usually "
                        "prefers New Cairo? Why or why not?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "memory"],
                },
                {
                    "title": "Implement a Simple Selective Memory Store",
                    "description": (
                        "Implement a tiny in-memory `MemoryStore` class with `save(key, value)`, `get(key)`, and `should_save(text)` "
                        "methods. `should_save` should return False for low-value chatter (e.g. greetings, very short strings) and True "
                        "for statements that look like durable preferences (e.g. containing words like 'prefer', 'usually', 'always'). "
                        "This models the lesson's 'memory should be selective' principle -- don't save everything."
                    ),
                    "starter_code": (
                        "class MemoryStore:\n"
                        "    def __init__(self):\n"
                        "        self._store = {}\n\n"
                        "    def should_save(self, text: str) -> bool:\n"
                        "        # TODO: return False for greetings / very short text,\n"
                        "        # True if it looks like a durable preference statement\n"
                        "        pass\n\n"
                        "    def save(self, key: str, value: str):\n"
                        "        # TODO: only save if should_save(value) is True\n"
                        "        pass\n\n"
                        "    def get(self, key: str):\n"
                        "        # TODO: return the stored value, or None if missing\n"
                        "        pass\n"
                    ),
                    "solution_code": (
                        "class MemoryStore:\n"
                        "    PREFERENCE_MARKERS = (\"prefer\", \"usually\", \"always\", \"never\")\n"
                        "    GREETINGS = (\"hi\", \"hello\", \"hey\", \"thanks\", \"ok\", \"okay\")\n\n"
                        "    def __init__(self):\n"
                        "        self._store = {}\n\n"
                        "    def should_save(self, text: str) -> bool:\n"
                        "        cleaned = text.strip().lower()\n"
                        "        if len(cleaned) < 8 or cleaned in self.GREETINGS:\n"
                        "            return False\n"
                        "        return any(marker in cleaned for marker in self.PREFERENCE_MARKERS)\n\n"
                        "    def save(self, key: str, value: str):\n"
                        "        if self.should_save(value):\n"
                        "            self._store[key] = value\n\n"
                        "    def get(self, key: str):\n"
                        "        return self._store.get(key)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "memory"],
                },
            ],
            "quiz": {
                "title": "Memory — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the core distinction between state and memory in the lesson's mental model?",
                        "options": [
                            "State and memory are interchangeable terms for the same thing",
                            "State is what the agent tracks during the current task; memory is what the system chooses to remember for later",
                            "Memory only exists for read-only tools",
                            "State always persists forever, while memory is deleted after each task",
                        ],
                        "correct": 1,
                        "explanation": "State = current-task tracking. Memory = persistent, selectively stored information that can help in future, separate interactions.",
                    },
                    {
                        "question": "Why does the lesson say memory is 'not just conversation history'?",
                        "options": [
                            "Because memory can store derived, useful information (e.g. 'user investment horizon = long-term') rather than every raw message",
                            "Because conversation history is illegal to store",
                            "Because memory can only be stored in vector databases",
                            "Because conversation history is always more accurate than memory",
                        ],
                        "correct": 0,
                        "explanation": "Memory can be a distilled, useful fact extracted from a conversation, not necessarily the verbatim chat log.",
                    },
                    {
                        "question": "Which of these is an example of long-term memory rather than short-term memory, per the lesson?",
                        "options": [
                            "The budget the user mentioned two messages ago in the current conversation",
                            "A stored user preference like 'generally prefers New Cairo' that could be retrieved in a future, separate conversation",
                            "The list of properties returned by the current search call",
                            "The property currently selected for ROI calculation in this task",
                        ],
                        "correct": 1,
                        "explanation": "Long-term memory persists across conversations/tasks. The other options are all part of the current task's short-term context (state).",
                    },
                    {
                        "question": "If a stored memory says the user prefers New Cairo, but the user's current message says 'search in Sheikh Zayed instead,' what should happen per the lesson?",
                        "options": [
                            "The stored memory should always override the current instruction",
                            "The current instruction should win; memory is context, not an absolute command",
                            "The agent should refuse to search until the conflict is resolved by a human",
                            "The memory should be immediately deleted without checking the request further",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: the current instruction wins over long-term memory. Memory informs behavior but doesn't override what the user is asking for right now.",
                    },
                    {
                        "question": "Why does the lesson caution against saving every sentence a user has ever said as memory?",
                        "options": [
                            "Because storage is always more expensive than compute",
                            "Because memory should be selective -- too many low-value memories make relevant retrieval harder and don't serve a clear purpose",
                            "Because vector databases cannot store more than 100 items",
                            "Because conversation history is not allowed to be persisted under any circumstances",
                        ],
                        "correct": 1,
                        "explanation": "The lesson stresses selectivity: memory should have a purpose. Storing everything ('User said hello on Tuesday') bloats storage and makes finding genuinely useful memories harder.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 7
        # ------------------------------------------------------------
        {
            "title": "Planning",
            "slug": "ai-developer-ai-agents-planning",
            "description": "How an agent decides what actions to take and in what order: task decomposition, plan-then-execute vs replan-as-you-go, how planning connects to state and tools, and why planning shouldn't be added to tasks that don't need it.",
            "order": 7,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "planning", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Planning",
                "content": """# Planning

Now we move from *"what can the agent do?"* to: **how does the agent decide what steps it should take to achieve a goal?** That's planning.

## What Is Planning?

In AI agents, **planning is deciding what actions should be taken, and often in what order, to achieve a goal.** For example, user: *"Find the best apartment for investment under 5M."* The agent may need to plan:

```
Goal
 ↓
Search properties
 ↓
Get details
 ↓
Calculate ROI
 ↓
Compare candidates
 ↓
Recommend best property
```

Planning answers: *"What should I do next?"*

## Why Do Agents Need Planning?

A simple question may need one action: *"What is 20 × 5?"* → `calculator()`. But complex tasks require multiple actions. *"Research Qdrant, compare it with FAISS, and recommend which one I should use."* The agent might need to search Qdrant, search FAISS, collect information, compare, consider requirements, and recommend. The system needs some way to **organize these actions** -- that's planning.

## The Simplest Mental Model

```
Goal
 ↓
Break into smaller tasks
 ↓
Determine order
 ↓
Execute
 ↓
Check result
 ↓
Adjust plan if necessary
```

For example, goal: *"Book a business trip."* Plan: find flights, find hotel, compare options, ask user for confirmation, book.

## Planning vs Workflow

This is subtle because they look similar. A **workflow** says *"these are the steps the developer has defined."* **Planning** says *"given this goal, determine which steps are necessary."*

Workflow (developer-fixed):
```
Search → Rerank → Generate
```

Planning agent (LLM-decided at runtime):
```
Goal → "I need to search first." → Search
     → "I need more information." → Another tool
     → "Now I can answer."
```

So: **workflow = predefined plan. Agent planning = dynamically generated plan.**

## A Real Example

User: *"Find the best laptop for AI development under $1,500."* The agent has `search_products()`, `get_product_details()`, `compare_products()`. A possible plan: search laptops under $1500, get details for promising candidates, compare GPU/RAM/CPU and price, select the best option, explain the recommendation. Notice the agent doesn't necessarily execute every possible action -- it chooses actions **relevant to the goal**.

## Planning Can Happen Before Execution

```
Goal → Create complete plan → Execute plan
```

For example: plan = `[Search, Filter, Compare, Calculate, Answer]`, then execute each step in order. This is called **upfront planning**.

## Planning Can Also Happen Step by Step

```
Goal
 ↓
Decide next action
 ↓
Execute
 ↓
Observe result
 ↓
Decide next action
 ↓
Execute
 ↓
...
```

For example: *"Search properties"* → search → *"found 20 properties"* → *"now I need property details"* → get details → ... This is often called **dynamic planning** or **replanning**. The agent doesn't have to know the entire plan at the beginning.

## Why Dynamic Planning Is Useful

Imagine the search returns 0 properties. The original plan (`Search → Get details → Calculate ROI`) can't continue. The agent may need to adapt:

```
Search → 0 results → Change query → Search again → Results found → Continue
```

This is where agents become powerful -- **the environment can change the plan.**

## Planning Is Not Necessarily "Thinking for a Long Time"

Don't confuse planning with generating a huge reasoning process. A plan can be very simple (`Search → Calculate → Answer`) or more complex (7 steps). The important thing is **action organization**, not how much text the model generates.

## Planning and Decomposition

Complex goals often need to be broken into smaller tasks. *"Build a report about the Egyptian real-estate market"* is too broad as a single action. The agent could decompose it:

```
Goal
 │
 ├── Research market prices
 ├── Research rental yields
 ├── Research demand
 ├── Research major areas
 └── Compare findings
          ↓
       Report
```

This is called **task decomposition**. You already encountered decomposition in prompt engineering -- here we're using it as part of an action-oriented system.

## Planning + Tools

Planning becomes especially useful with multiple tools: `web_search()`, `calculator()`, `database_query()`, `send_email()`. User: *"Analyze our sales data and email me the top three products."* Possible plan: query sales database, identify top products, calculate percentages, generate summary, send email. **Tools provide the capabilities. Planning determines how those capabilities should be combined.**

## Planning + State

Connecting to the previous lesson: `State → Decide → Action → Update State`. Planning **uses** the state. Example: state = *"20 properties found"* → agent decides *"I need details for the top candidates"* → after the tool, state = *"20 properties + details for 5 candidates"* → plan changes: *"I have enough information, calculate ROI."*

```
State → Plan → Action → New State → Updated Plan
```

This is a very important agent architecture.

## Planning Isn't Always Necessary

Just like agents themselves, planning shouldn't be added unnecessarily. For *"What's 25 × 4?"* you don't need a planning engine -- just call `calculator()`. Simple problem → simple action. Complex goal → planning may help.

## Two Important Planning Styles

**A. Plan-then-execute:**
```
Goal → Create plan → Execute plan → Finish
```
Good when the task is relatively predictable.

**B. Replan-as-you-go:**
```
Goal → Choose action → Observe → Update state → Choose next action → Observe → ...
```
Good when the environment is uncertain. For example, `Search → No results → Modify query → Search again`. The agent adapts.

## A Simple Python Mental Model

```
def plan(goal):
    if "find property" in goal:
        return ["search_properties", "get_details", "calculate_roi"]
```

`plan("Find the best property")` might produce `["search_properties", "get_details", "calculate_roi"]`. But real agents can dynamically generate plans based on the current state.

## Dynamic Planning

```
state = {"properties": [], "details": [], "roi": None}
```

The agent sees `properties = []`, decides `search_properties()`. After execution, `properties = [10 properties]`. The agent now sees *"I have candidates, but no details"* → `get_property_details()`. Then `details = [...]` → `calculate_roi()`. The plan **emerges through interaction with the environment**.

## Planning Can Fail

An LLM-generated plan isn't guaranteed to be correct. User: *"Send me a report about my account."* Bad plan: retrieve account → **delete old data** → generate report. The second step is unnecessary and dangerous. So planning needs constraints, validation, tool permissions, maximum steps, error handling, and sometimes human approval. We'll study these later.

## Planning and Autonomy

Planning is one of the things that increases an agent's autonomy. Compare a fixed workflow (`"Always do A → B → C"`) with an agent (`Goal: "Achieve X"` → *"Given the current situation, I'll do A first"* → *"Now B is necessary"* → *"Actually, C is no longer needed"*). The agent is more flexible because the plan isn't completely fixed.

## Connection to Agentic RAG

Question: *"What are the graduation requirements?"* An agent might plan: search regulations, check retrieved results, if incomplete rewrite query and search again, verify relevant sections, generate answer. That's **planning applied to retrieval** -- the agent decides which retrieval actions are necessary based on what it discovers.

## The Deeper Mental Model

```
                   GOAL
                     ↓
                   STATE
                     ↓
                  PLANNER
                     ↓
             Choose next action
                     ↓
                   TOOL
                     ↓
                 RESULT
                     ↓
              Update STATE
                     ↓
                  PLANNER
                     ↓
                 Continue
```

This is the foundation for the next several lessons. Later we'll explore how an agent chooses the best tool -- that's **Tool Selection**.

*The single idea to keep: planning is deciding which actions are needed to achieve a goal, often by breaking it into smaller tasks and determining their order -- a workflow follows a plan the developer designed, while an agent can create or adapt its plan based on the goal and current state.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Plan a Multi-Property Investment Comparison",
                    "description": (
                        "Your AI assistant receives: \"Find the three best investment apartments under 5M, calculate their ROI, and "
                        "tell me which one you recommend.\" Available tools: search_properties(), get_property_details(), calculate_roi(). "
                        "Answer: (1) Break the task into 3-5 planning steps. (2) What information must the agent have before calculating "
                        "ROI? (3) Suppose search_properties() returns no properties -- should the agent blindly continue with the "
                        "original plan? What could it do instead? (4) Is this better suited to a fixed workflow or an agent? Why?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "planning"],
                },
                {
                    "title": "Implement Replan-as-You-Go on Empty Results",
                    "description": (
                        "Implement `find_properties_with_replanning(query, search_fn, widen_query_fn, max_retries=2)` that calls "
                        "search_fn(query); if it returns an empty list, calls widen_query_fn(query) to get a broader query and retries, "
                        "up to max_retries times, before giving up and returning an empty list. This models the lesson's "
                        "'search → no results → modify query → search again' replanning example."
                    ),
                    "starter_code": (
                        "def find_properties_with_replanning(query, search_fn, widen_query_fn, max_retries=2):\n"
                        "    # TODO: call search_fn(query); if empty, widen the query and retry,\n"
                        "    # up to max_retries additional attempts, then return whatever the\n"
                        "    # last search_fn call returned (possibly still empty)\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def find_properties_with_replanning(query, search_fn, widen_query_fn, max_retries=2):\n"
                        "    results = search_fn(query)\n"
                        "    attempts = 0\n\n"
                        "    while not results and attempts < max_retries:\n"
                        "        query = widen_query_fn(query)\n"
                        "        results = search_fn(query)\n"
                        "        attempts += 1\n\n"
                        "    return results\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "planning"],
                },
            ],
            "quiz": {
                "title": "Planning — Knowledge Check",
                "questions": [
                    {
                        "question": "How does the lesson define planning in the context of AI agents?",
                        "options": [
                            "Generating as much reasoning text as possible before answering",
                            "Deciding what actions should be taken, and often in what order, to achieve a goal",
                            "A fixed sequence of steps that never changes once written",
                            "A feature exclusive to vector databases",
                        ],
                        "correct": 1,
                        "explanation": "Planning is about organizing actions toward a goal -- deciding what to do and in what order -- not about the length of any generated text.",
                    },
                    {
                        "question": "What is the key difference between a workflow and agent planning, per the lesson?",
                        "options": [
                            "A workflow follows a plan the developer defined in advance; agent planning is dynamically generated based on the goal and situation",
                            "Workflows always use more tools than planning agents",
                            "Planning can only happen inside a vector database",
                            "There is no meaningful difference between the two",
                        ],
                        "correct": 0,
                        "explanation": "Workflow = predefined plan by the developer. Agent planning = the LLM dynamically determines which steps are necessary given the goal and current state.",
                    },
                    {
                        "question": "What is the difference between plan-then-execute and replan-as-you-go?",
                        "options": [
                            "They are the same strategy with different names",
                            "Plan-then-execute creates the full plan upfront and executes it; replan-as-you-go decides one action at a time and adapts based on what it observes",
                            "Replan-as-you-go can never handle failures or unexpected results",
                            "Plan-then-execute is only used for simple one-step tasks",
                        ],
                        "correct": 1,
                        "explanation": "Plan-then-execute is upfront planning good for predictable tasks. Replan-as-you-go decides step by step, adapting to what actually happens (e.g. empty search results).",
                    },
                    {
                        "question": "Why does the lesson warn that planning can fail or even be dangerous?",
                        "options": [
                            "Because plans always take too long to execute",
                            "Because an LLM-generated plan isn't guaranteed to be correct and could include unnecessary or harmful steps, so it needs constraints and validation",
                            "Because planning requires a vector database that might be unavailable",
                            "Because only workflows can ever go wrong, never agent plans",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's account example shows a bad plan including an unnecessary 'delete old data' step -- illustrating why plans need validation, permissions, and sometimes human approval.",
                    },
                    {
                        "question": "According to the lesson, when should planning NOT be added to a task?",
                        "options": [
                            "Never -- every task benefits from a planning engine",
                            "When the task is simple enough to be solved with a single direct action, like calling calculator() for '25 × 4'",
                            "Only when the agent has more than 10 tools available",
                            "Only when the task involves a vector database",
                        ],
                        "correct": 1,
                        "explanation": "Just like agents in general, planning shouldn't be added unnecessarily -- simple problems deserve simple actions, not a full planning engine.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 8
        # ------------------------------------------------------------
        {
            "title": "Tool Selection",
            "slug": "ai-developer-ai-agents-tool-selection",
            "description": "How an agent chooses the right tool from its toolbox: the role of names and descriptions, how selection depends on current state, tool selection vs planning, and production principles like choosing the least powerful tool and enforcing permissions.",
            "order": 8,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "tool-selection", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Tool Selection",
                "content": """# Tool Selection

We've learned that agents have tools and can plan. Now we need to understand one of the most important questions an agent faces: **"Which tool should I use right now?"** This is tool selection.

## The Problem

Imagine an agent has `search_web()`, `search_documents()`, `query_database()`, `calculator()`, `send_email()`, `get_weather()`. User: *"What is the current temperature in Cairo?"* The agent needs to select `get_weather()` -- not `search_documents()`, `calculator()`, or `send_email()`. So tool selection is: **choosing the most appropriate available tool for the current task.**

## The Mental Model

Think of the agent as having a toolbox:

```
                    Agent
                      │
                      ↓
                  Current goal
                      │
                      ↓
               "What do I need?"
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Search      Database    Calculator
          │
          ↓
       Choose
          │
          ↓
       Execute
```

The LLM acts as the decision-maker, while your application controls which tools are actually available and executes them.

## Tool Descriptions Are Critical

Suppose we give the agent `search_web()` and `search_documents()`. Good descriptions: *"search_web: search the internet for current or external information"* vs *"search_documents: search the company's internal knowledge base."* Now *"What does our company's vacation policy say?"* → internal information → `search_documents()`. But *"What happened in today's AI news?"* → external information → `search_web()`. **Tool descriptions are part of the agent's decision-making interface.**

## Tool Selection Is Not the Same as Tool Execution

**Selection** -- the LLM decides *"I should use search_documents."* **Execution** -- your application executes `search_documents("vacation policy")`.

```
LLM
 ↓
SELECT TOOL
 ↓
Application
 ↓
EXECUTE TOOL
```

The LLM shouldn't be given unrestricted access to your infrastructure.

## Example: University Agent

Academic assistant with `search_regulations()`, `get_course_info()`, `calculate_gpa()`, `get_student_schedule()`. *"What are the prerequisites for CSE251?"* → need course information → `get_course_info("CSE251")`. *"What will my GPA be if I get A in three courses?"* → need calculation → `calculate_gpa(...)`. *"Can I register for this course based on my current courses?"* → may need `get_student_schedule()` **and** `get_course_info()`, then compare prerequisites. This is where tool selection becomes more interesting.

## Sometimes One Tool Isn't Enough

*"Find the cheapest apartment under 5M with the highest expected ROI."* With `search_properties()`, `get_property_details()`, `calculate_roi()`, the agent could chain: search → details → ROI. So tool selection can happen repeatedly:

```
Select → Execute → Observe → Select again → Execute
```

This connects directly to the agent loop we'll study next.

## Tool Selection Depends on the Current State

Suppose `state = {"properties": []}`. The agent sees *"I don't have any properties yet"* → selects `search_properties()`. After execution, `state = {"properties": [property1, property2, property3]}`. The agent sees *"I have candidates but no detailed information"* → selects `get_property_details()`. Then `calculate_roi()`. **Tool selection is contextual -- the best tool depends on what the agent already knows.**

## Tool Selection as Classification

At a simple level: `User request → Determine intent/required capability → Choose tool`. *"What's 20 × 5?"* → mathematical calculation → `calculator()`. *"Find our refund policy"* → internal knowledge retrieval → `search_documents()`. *"Send this report to Ahmed"* → email action → `send_email()`. The LLM is essentially mapping **Goal → Capability**.

## But Tool Selection Can Be Harder Than Simple Classification

*"Compare the current price of NVIDIA with what our database recorded last month."* Now the agent may need `web_search()` + `query_database()` + `calculator()`. The task isn't just Question → One Tool; it's Question → identify required information → choose tool #1 → observe → choose tool #2 → compare → possibly calculate. That's why tool selection becomes closely connected with **planning**.

## Tool Selection vs Planning

**Planning** -- what actions should I take to achieve the goal? (e.g. search → details → ROI → compare). **Tool selection** -- which specific tool should perform the next action? (e.g. need property search → `search_properties()`).

```
Planning → "Search for properties" → Tool Selection → "Use search_properties()"
```

Planning is *what needs to happen*; tool selection is *which capability should do it*.

## What Makes a Good Tool Candidate?

An agent should consider: **capability** (can this tool actually solve the problem?), **inputs** (do we have the required arguments?), **current state** (have we already performed this action?), **reliability** (is the tool appropriate and available?), **cost** (is there a cheaper way?), and **risk** (does this tool cause side effects?). For example, `search_database()` is usually lower risk than `delete_customer()`. Tool selection is not purely "which tool sounds relevant" -- it can involve **safety and constraints**.

## Too Many Tools Can Be a Problem

Imagine an agent has 100 tools with overlapping functionality: `search_web()`, `search_news()`, `search_articles()`, `search_online()`, `search_public_web()`... This makes selection harder. You want a clean toolbox with clear descriptions. A useful principle: **give an agent the smallest useful set of tools.** Don't expose your entire backend to the model.

## Tool Names Matter

Compare `tool_1()`, `tool_2()`, `tool_3()` with `search_products()`, `calculate_roi()`, `get_property_details()`. The second set gives the LLM much more semantic information. Good: `get_order_status()`. Less useful: `process_data()`.

## Tool Descriptions Matter Even More

Compare `calculate()` with *"calculate_roi: calculate estimated annual return on a property using purchase price and annual rental income."* The second description gives the agent what it does, when it's useful, and what information it needs. Better descriptions generally make tool selection easier.

## Tool Arguments Are Part of Selection

Suppose `get_weather(city)`. The agent selects it for *"What's the weather in Cairo?"* and must produce `{"city": "Cairo"}`. If it can't provide the required input, the application may need to ask the user, retrieve the missing information, choose another tool, or stop. For *"What's the weather there?"*, if "there" isn't known from context, the agent may need clarification. So tool selection isn't only *"which tool?"* -- it can also involve **can I provide the correct arguments?**

## Read Tools vs Action Tools

Recall the distinction from the Tools lesson: read tools (`search_properties()`, `get_weather()`, `get_order_status()`) vs action tools (`send_email()`, `create_order()`, `delete_file()`). Tool selection should treat action tools more carefully. *"Draft an email to Ahmed"* → the correct tool might be `create_email_draft()`, **not** `send_email()`, because drafting and sending have very different consequences. A subtle but important production-agent principle: **choose the least powerful tool that can accomplish the task.**

## Example: Real-Estate Agent

Agent has `search_properties()`, `get_property_details()`, `calculate_roi()`, `create_report()`, `send_report()`. User: *"Find the best investment apartment and prepare a report."* Reasonable sequence: search → details → ROI → `create_report()`. Notice `send_report()` isn't needed -- the user asked to *prepare* the report, not send it. Tool selection needs to understand the **actual goal**, not just choose every relevant tool.

## Tool Selection and Permissions

Agent tools: `search_documents()`, `get_user_data()`, `delete_user_data()`. User: *"What information do you have about my account?"* The agent needs `get_user_data()` -- it should **never** decide `delete_user_data()` just because that tool exists. A production architecture enforces permissions separately:

```
LLM chooses
      ↓
Permission check
      ↓
Allowed?
   /       \\
 Yes        No
 ↓          ↓
Execute    Reject
```

**The LLM should not be your security boundary.** We'll return to this in a later Agent Security lesson.

## A Simple Implementation Idea

```
tools = {
    "calculator": calculator,
    "search_properties": search_properties,
    "get_property_details": get_property_details
}

tool_call = {
    "name": "calculate_roi",
    "arguments": {"price": 4_000_000, "annual_rent": 480_000}
}

tool = tools[tool_call["name"]]
result = tool(**tool_call["arguments"])
```

The application controls the mapping: LLM-selected name → known allowed tool → execute. **Not** LLM → arbitrary Python execution.

## The Deeper Architecture

```
                       GOAL
                         ↓
                       STATE
                         ↓
                      PLANNING
                         ↓
                 "What do I need?"
                         ↓
                  TOOL SELECTION
                         ↓
                  "Which tool?"
                         ↓
                  FUNCTION CALL
                         ↓
                      TOOL
                         ↓
                     RESULT
                         ↓
                   UPDATE STATE
                         ↓
                      PLANNING
```

This is becoming the core architecture of an agent.

*The single idea to keep: tool selection is choosing the most appropriate, least powerful, currently-executable tool for what the state says is still needed -- and it should always pass through a permission check the LLM cannot bypass.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Academic Agent: Sequence the Tool Calls",
                    "description": (
                        "Your AI academic agent has: search_regulations(query), get_course_info(course_code), calculate_gpa(grades), "
                        "get_student_schedule(student_id), send_email(to, subject, body). The user says: \"Check whether CSE251 is "
                        "available for me this semester and, if I can register, email me the requirements.\" Answer: "
                        "(1) Which tools should the agent probably use? (2) What should it use first, and why? "
                        "(3) Could it need more than one tool? Explain the sequence. (4) Should it automatically call send_email() as "
                        "soon as it finds the requirements? Why or why not? (5) What information might be missing before calling send_email()?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "tool-selection"],
                },
                {
                    "title": "Implement a Safe Tool Dispatcher with an Allow-List",
                    "description": (
                        "Implement `select_and_execute(tool_call, tools, permissions, user_role)` that: looks up the requested tool "
                        "name in `tools` (a name→function dict), checks `permissions` (a dict mapping tool name to a list of allowed "
                        "roles) before executing, and raises a clear PermissionError if the role isn't allowed or a ValueError if the "
                        "tool name is unknown -- modeling the lesson's 'LLM chooses → permission check → allowed? → execute/reject' flow."
                    ),
                    "starter_code": (
                        "def select_and_execute(tool_call, tools, permissions, user_role):\n"
                        "    name = tool_call[\"name\"]\n"
                        "    arguments = tool_call[\"arguments\"]\n"
                        "    # TODO: raise ValueError(\"Unknown tool\") if name not in tools\n"
                        "    # TODO: raise PermissionError if user_role not in permissions.get(name, [])\n"
                        "    # TODO: otherwise call tools[name](**arguments) and return the result\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def select_and_execute(tool_call, tools, permissions, user_role):\n"
                        "    name = tool_call[\"name\"]\n"
                        "    arguments = tool_call[\"arguments\"]\n\n"
                        "    if name not in tools:\n"
                        "        raise ValueError(\"Unknown tool\")\n\n"
                        "    allowed_roles = permissions.get(name, [])\n"
                        "    if user_role not in allowed_roles:\n"
                        "        raise PermissionError(f\"Role '{user_role}' is not allowed to call '{name}'\")\n\n"
                        "    return tools[name](**arguments)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "tool-selection", "security"],
                },
            ],
            "quiz": {
                "title": "Tool Selection — Knowledge Check",
                "questions": [
                    {
                        "question": "What is tool selection, as defined in the lesson?",
                        "options": [
                            "The process of writing new tools from scratch for every request",
                            "Choosing the most appropriate available tool for the current task",
                            "A synonym for function calling",
                            "The step where the application decides to remove unused tools permanently",
                        ],
                        "correct": 1,
                        "explanation": "Tool selection is the LLM deciding, among the available tools, which one best fits what's currently needed.",
                    },
                    {
                        "question": "How does tool selection differ from tool execution?",
                        "options": [
                            "They are the same step performed by the same component",
                            "The LLM performs selection (deciding which tool); the application performs execution (actually running it)",
                            "Execution always happens before selection",
                            "Only action tools require execution; read tools execute themselves",
                        ],
                        "correct": 1,
                        "explanation": "Selection is a decision made by the LLM. Execution is carried out by your application -- the LLM should not have unrestricted access to run things itself.",
                    },
                    {
                        "question": "According to the lesson, why might an agent choose create_email_draft() instead of send_email() when asked to 'draft an email'?",
                        "options": [
                            "Because send_email() no longer exists once a draft tool is available",
                            "Because the lesson recommends choosing the least powerful tool that can accomplish the task, given the different consequences of drafting vs sending",
                            "Because drafting tools are always faster to execute",
                            "Because action tools can never be selected by an agent",
                        ],
                        "correct": 1,
                        "explanation": "Drafting and sending have very different consequences. The lesson's principle is to choose the least powerful tool sufficient for the actual goal.",
                    },
                    {
                        "question": "Why does the lesson say tool selection is 'contextual' and connects to state?",
                        "options": [
                            "Because the best tool to select next depends on what the agent already knows/has in its current state",
                            "Because tool selection ignores state entirely and only depends on the user's exact wording",
                            "Because state and tool selection are unrelated concepts",
                            "Because tools automatically select themselves once state reaches a certain size",
                        ],
                        "correct": 0,
                        "explanation": "The lesson's property example shows selection changing as state evolves: no properties → search; properties but no details → get details; details known → calculate ROI.",
                    },
                    {
                        "question": "What does the lesson say about the LLM being your 'security boundary'?",
                        "options": [
                            "The LLM should be trusted to decide permissions on its own since it's usually correct",
                            "The LLM should not be the security boundary -- permission checks must be enforced separately by the application before executing a selected tool",
                            "Security checks are unnecessary if tool names are descriptive",
                            "Only action tools ever need permission checks; read tools never do",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: 'The LLM should not be your security boundary.' Permission checks (allowed/rejected) must happen in the application layer regardless of what the LLM selects.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 9
        # ------------------------------------------------------------
        {
            "title": "Agent Loops",
            "slug": "ai-developer-ai-agents-agent-loops",
            "description": "How planning, tool selection, function calling, state, and memory connect into a single decide-act-observe-update cycle; stopping conditions and iteration limits; and why the agent, not the LLM alone, is the whole system around the model.",
            "order": 9,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.5,
            "skill_tags": ["ai-agents", "agent-loops", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Agent Loops",
                "content": """# Agent Loops

We now have the main building blocks: **Tools** (what the agent can do), **Function calling** (how it requests a tool), **State** (what it currently knows), **Memory** (what it remembers), **Planning** (what it wants to accomplish), and **Tool selection** (which capability to use). Now we connect them together.

The **agent loop** is the cycle that allows an agent to repeatedly decide, act, observe, and continue until the task is complete.

## The Simplest Mental Model

```
        ┌──────────────┐
        │    Decide    │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │     Act      │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │   Observe    │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Update State │
        └──────┬───────┘
               ↓
             Decide
               ↑
               └───────────
```

The agent doesn't necessarily perform only one action -- it can repeatedly go through this cycle.

## Why Do We Need a Loop?

*"Find the best investment apartment under 5M and calculate its ROI."* The agent can't necessarily solve this with one LLM call. It might need to search, inspect results, get details, calculate ROI, compare, and answer:

```
LLM → Tool → Result → LLM → Tool → Result → LLM → Final answer
```

The repeated cycle is the **agent loop**.

## Normal LLM Application vs Agent Loop

A traditional application: `User → LLM → Answer`. A RAG application: `User → Retrieve → LLM → Answer`. An agent: `User → LLM → Tool → LLM → Tool → LLM → Tool → LLM → Answer`. The important difference: **the agent can repeatedly interact with its environment before producing the final result.**

## A Concrete Example

User: *"Find the cheapest laptop with at least 32GB RAM and calculate how much it costs over 3 years including electricity."* Tools: `search_products()`, `get_product_details()`, `calculate_cost()`.

**Step 1:** Agent decides *"I need to find candidate laptops"* → `search_products(...)`.
**Step 2:** Tool returns three laptops with prices. Agent decides *"I need detailed specifications"* → `get_product_details(...)`.
**Step 3:** Laptop C has 32GB RAM at $1,100. Agent decides *"I need the 3-year total cost"* → `calculate_cost(...)`.
**Step 4:** Result: $1,450 total. The agent now has enough information -- it exits the loop and responds.

## The Loop Is Driven by State

The state might evolve:

```
State 0: {goal: "...", products: [], selected_product: None, total_cost: None}
State 1: {goal: "...", products: [...], selected_product: None, total_cost: None}
State 2: {goal: "...", products: [...], selected_product: "Laptop C", total_cost: None}
State 3: {goal: "...", products: [...], selected_product: "Laptop C", total_cost: 1450}
```

Now the agent has enough information: `State → Complete → Final answer`.

## The Agent Asks Itself One Question Repeatedly

*"Given everything I currently know, what should I do next?"*

```
What do I know?
       ↓
What is missing?
       ↓
What action can get it?
       ↓
Use tool
       ↓
What did I learn?
       ↓
What should I do next?
```

This is the heart of an agent loop.

## Agent Loop vs Normal Program Loop

A normal loop is explicitly programmed: `for product in products: calculate(product)` -- the developer determines exactly what happens. An agent loop is more dynamic: current state → LLM decides next action → execute → new state → LLM decides again. The developer defines the available tools, state structure, limits, permissions, and stopping rules -- but **the LLM determines the next action.**

## A Simplified Implementation

```
while True:
    decision = agent(state)

    if decision["type"] == "final":
        return decision["answer"]

    if decision["type"] == "tool":
        result = execute_tool(decision["tool"], decision["arguments"])
        state["tool_result"] = result
```

Extremely simplified, but it captures the architecture: `while True` means continue until something tells us to stop. `decision = agent(state)` -- the LLM receives the current state and decides what happens. If it's a tool call, the application executes it and we update state. The loop starts again.

## The Agent Can Decide to Stop

This is crucial -- an agent needs a **termination condition**:

```
if decision["type"] == "final":
    return decision["answer"]
```

The LLM might decide *"I have enough information"* → final answer → **STOP**. Without termination, the agent could continue forever.

## Why Infinite Loops Are Dangerous

`Agent → Search → Agent → Search → Agent → Search → ...` forever. This could happen because the model doesn't realize the task is complete, a tool keeps returning bad results, the agent keeps retrying, the stopping condition is poorly designed, or the plan is impossible to complete. **Production agents need loop limits.**

## Maximum Iterations

```
MAX_STEPS = 10

for step in range(MAX_STEPS):
    decision = agent(state)

    if decision["type"] == "final":
        return decision["answer"]

    result = execute_tool(...)
    state["tool_result"] = result
```

If the agent reaches 10 steps without a final answer: **STOP**. This prevents runaway execution.

## Other Stopping Conditions

You can stop for many reasons: **success** (task completed), **maximum steps** (10 iterations reached), **error** (tool failed repeatedly), **budget** (LLM/tool cost exceeded limit), **time** (execution exceeded 30 seconds), or **human approval** (agent wants to perform a sensitive action). This becomes especially important when agents have real-world capabilities.

## Agent Loop and Planning

Planning tells the agent *"what should I accomplish?"* -- the loop lets it repeatedly execute that plan. Goal: find the best property. Planning: search → details → ROI → compare. Loop: decide search → execute → observe; decide details → execute → observe; decide ROI → execute → observe; decide final → answer. **Planning describes the intended path. The loop is the mechanism that repeatedly moves the agent along that path.**

## Agent Loop and Tool Selection

Inside the loop: agent → *"what do I need?"* → select tool → execute → observe → agent again. State: no properties → select `search_properties()` → results → state: properties available → select `get_property_details()`. **Tool selection happens inside the agent loop.**

## Agent Loop and Memory

Suppose the user says *"Find me an investment apartment."* Before planning, the agent might retrieve memory: *"user prefers New Cairo," "user prefers long-term investments."* Then the loop starts: retrieve memory → create current state → decide → tool → observe → update state → decide → ...

## Agent Loop + RAG

*"Can I register this course?"* Loop: state = question received → agent → search regulations → observe retrieved documents → agent → *"information is incomplete"* → rewrite query → search again → observe → agent → *"enough information"* → answer. This is a practical example of **agentic RAG** -- the key difference is that retrieval can happen multiple times based on what the agent observes.

## The Environment Matters

An agent isn't just LLM ↔ Tools -- there's an **environment** producing feedback:

```
                ┌──────────┐
                │   Agent  │
                └────┬─────┘
                     ↓
                  Action
                     ↓
                ┌──────────┐
                │Environment│
                └────┬─────┘
                     ↓
                  Result
                     ↓
                   Agent
```

The environment could be a database, the web, a filesystem, an API, a RAG system, a CRM, an email system, or another software application. The agent learns what to do next based on the environment's response.

## This Is Why Agents Are Different From Chatbots

A basic chatbot: `User → LLM → Response`. An agent: `User → Goal → LLM → Action → Environment → Observation → LLM → Action → Environment → Observation → ... → Response`. The agent is **interacting with the environment**, not simply generating text.

## A Very Important Engineering Principle

Don't create an agent loop when a deterministic workflow is enough. `PDF → Extract → Chunk → Embed → Store` doesn't need an autonomous agent deciding every step. A normal pipeline is cheaper, easier to test, easier to debug, and more predictable. **Use agent loops when the problem genuinely benefits from dynamic decision-making.**

## A Production-Style Architecture

```
                  User Goal
                      ↓
                  Load Memory
                      ↓
                 Initialize State
                      ↓
               ┌──────────────┐
               │ Agent / LLM  │
               └──────┬───────┘
                      ↓
                 Decide Action
                      ↓
               ┌──────────────┐
               │ Safety Check │
               └──────┬───────┘
                      ↓
                 Execute Tool
                      ↓
                  Tool Result
                      ↓
                 Update State
                      ↓
                Check Limits
                 /          \\
             Continue       Stop
                ↓             ↓
              Agent       Final Answer
```

Notice something important: **the LLM isn't the entire agent. The agent is the whole system around the model.**

## This Will Make LangGraph Easier

Conceptually, LangGraph lets you model: State → Node → State update → Conditional edge → Another node → State update → ... A conditional edge can effectively implement *"should we call a tool? should we continue? should we finish?"* So when you later build agents using LangGraph, don't think *"LangGraph is magic."* Think: *"LangGraph is helping me explicitly represent the agent's state, nodes, transitions, and loops."*

## The Complete Mental Model So Far

```
                         USER GOAL
                             ↓
                          MEMORY
                             ↓
                           STATE
                             ↓
                         PLANNING
                             ↓
                    TOOL SELECTION
                             ↓
                     FUNCTION CALL
                             ↓
                           TOOL
                             ↓
                         RESULT
                             ↓
                       UPDATE STATE
                             ↓
                       AGENT LOOP
                             │
                   ┌─────────┴─────────┐
                   ↓                   ↓
              Continue              Finish
                   ↓                   ↓
                 Agent            Final Answer
                   │
                   └──────→ loop
```

This is the foundation for everything we're going to build next.

*The single idea to keep: an agent loop is the repeated cycle of deciding, acting, observing, and updating state until the goal is completed or a stopping condition is reached -- and in a real system you always control that loop with limits, error handling, permissions, and explicit stopping conditions.*
""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace the Full Agent Loop",
                    "description": (
                        "Your agent receives: \"Find the best investment apartment under 5M and calculate its expected ROI.\" "
                        "Available tools: search_properties(), get_property_details(), calculate_roi(). Describe the agent loop "
                        "step-by-step (e.g. '1. Agent checks state ... 2. ...'). Then answer: "
                        "(1) What should the agent do if search_properties() returns zero results? "
                        "(2) What should happen if calculate_roi() fails twice? "
                        "(3) Why do we need a maximum iteration limit? "
                        "(4) At what point should the agent stop calling tools and produce the final answer?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "agent-loops"],
                },
                {
                    "title": "Implement a Bounded Agent Loop with Stopping Conditions",
                    "description": (
                        "Implement `run_agent_loop(state, decide_fn, execute_tool_fn, max_steps=10, max_tool_failures=2)` that runs the "
                        "decide -> act -> observe -> update cycle, stops and returns the answer on a 'final' decision, stops and raises "
                        "a clear error if max_steps is reached, and also stops and raises a clear error if the same tool fails "
                        "max_tool_failures times in a row -- combining the lesson's 'maximum iterations' and 'error' stopping conditions."
                    ),
                    "starter_code": (
                        "def run_agent_loop(state, decide_fn, execute_tool_fn, max_steps=10, max_tool_failures=2):\n"
                        "    # state should include state['tool_results'] = [] to accumulate results\n"
                        "    # decide_fn(state) -> {\"type\": \"final\", \"answer\": ...} or\n"
                        "    #                     {\"type\": \"tool\", \"tool\": name, \"arguments\": {...}}\n"
                        "    # execute_tool_fn(tool, arguments) -> result, or raises an exception on failure\n"
                        "    # TODO: implement the loop with both stopping conditions\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def run_agent_loop(state, decide_fn, execute_tool_fn, max_steps=10, max_tool_failures=2):\n"
                        "    consecutive_failures = 0\n\n"
                        "    for step in range(max_steps):\n"
                        "        decision = decide_fn(state)\n\n"
                        "        if decision[\"type\"] == \"final\":\n"
                        "            return decision[\"answer\"]\n\n"
                        "        if decision[\"type\"] == \"tool\":\n"
                        "            try:\n"
                        "                result = execute_tool_fn(decision[\"tool\"], decision[\"arguments\"])\n"
                        "                state.setdefault(\"tool_results\", []).append(result)\n"
                        "                consecutive_failures = 0\n"
                        "            except Exception as exc:\n"
                        "                consecutive_failures += 1\n"
                        "                if consecutive_failures >= max_tool_failures:\n"
                        "                    raise RuntimeError(f\"Tool '{decision['tool']}' failed {consecutive_failures} times in a row\") from exc\n\n"
                        "    raise RuntimeError(f\"Agent did not finish within {max_steps} steps\")\n"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["ai-agents", "python", "agent-loops"],
                },
            ],
            "quiz": {
                "title": "Agent Loops — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the agent loop, per the lesson's definition?",
                        "options": [
                            "A single LLM call that produces the final answer immediately",
                            "The repeated cycle of deciding, acting, observing, and updating state until the goal is completed or a stopping condition is reached",
                            "A Python for-loop written entirely by the developer with no LLM involvement",
                            "The step where tools are installed into the agent's toolbox",
                        ],
                        "correct": 1,
                        "explanation": "The agent loop is the decide → act → observe → update-state cycle that repeats until the task is done or a stopping condition triggers.",
                    },
                    {
                        "question": "Why does an agent loop need an explicit termination condition (e.g. a 'final' decision type)?",
                        "options": [
                            "It doesn't -- agents naturally know when to stop without any check",
                            "Without one, the loop could continue indefinitely, especially if the model doesn't realize the task is complete or a tool keeps failing",
                            "Termination conditions are only needed for read-only tools",
                            "Because Python for-loops cannot run more than 10 times",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly warns about infinite loops -- termination conditions and step limits prevent runaway execution.",
                    },
                    {
                        "question": "Which of these is NOT one of the stopping conditions the lesson lists?",
                        "options": [
                            "Maximum steps reached",
                            "Budget exceeded",
                            "Human approval required for a sensitive action",
                            "The tool's function name contains more than 20 characters",
                        ],
                        "correct": 3,
                        "explanation": "The lesson lists success, maximum steps, error, budget, time, and human approval as stopping conditions -- function name length is not one of them.",
                    },
                    {
                        "question": "How does the lesson distinguish an agent loop from a normal programmed loop like 'for product in products: calculate(product)'?",
                        "options": [
                            "They are identical in every way",
                            "In a normal loop the developer determines exactly what happens each iteration; in an agent loop the LLM decides the next action dynamically based on current state",
                            "Agent loops never use Python's while or for constructs",
                            "Normal loops can only run once, while agent loops must run indefinitely",
                        ],
                        "correct": 1,
                        "explanation": "The developer still defines tools, state structure, limits, and permissions -- but the LLM determines the next action inside the loop, unlike a fully deterministic for-loop.",
                    },
                    {
                        "question": "What does the lesson mean by 'the LLM isn't the entire agent -- the agent is the whole system around the model'?",
                        "options": [
                            "The LLM is irrelevant to how agents work",
                            "The agent includes the LLM plus the surrounding system: state management, tool execution, safety checks, limits, and stopping conditions",
                            "Only the prompt matters; everything else is optional",
                            "Agents must always use multiple different LLMs simultaneously",
                        ],
                        "correct": 1,
                        "explanation": "The production-style architecture diagram shows memory, state, safety checks, limits, and stopping conditions surrounding the LLM -- the agent is that whole system, not just the model.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 10
        # ------------------------------------------------------------
        {
            "title": "ReAct",
            "slug": "ai-developer-ai-agents-react",
            "description": "The Reason + Act pattern: how connecting reasoning to real tool actions and observations makes an agent adaptive, how ReAct relates to the agent loop and to Agentic RAG, and the guardrails a production ReAct system needs.",
            "order": 10,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "react", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "ReAct",
                "content": """# ReAct

Now we learn one of the most important patterns in agent systems: **ReAct = Reason + Act**. The key idea is that an agent can decide what to do, take an action, observe the result, and then decide what to do next. This connects directly to the agent loop we just learned.

## The Problem ReAct Solves

User: *"What is the ROI of the cheapest apartment in New Cairo under 5M?"* The agent doesn't know the answer immediately. It needs to find apartments, look at prices, choose the cheapest, get its details, calculate ROI, and answer. The important part: **the agent doesn't know everything before it starts -- it discovers information through actions.** That's exactly what ReAct is designed around.

## The ReAct Mental Model

```
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason
  ↓
Act
  ↓
Observe
  ↓
...
  ↓
Final Answer
```

In simple language: *think about what you need → do something → look at what happened → decide again.* This is very similar to the agent loop -- the important addition is the **explicit relationship between reasoning and actions**.

## Why "Act" Matters

*"What's the current price of Bitcoin?"* A normal LLM could simply generate an answer from learned knowledge, but current information may be unavailable or outdated. A ReAct-style agent instead: needs current information → search web → observe result → use result → answer. The agent uses an **external tool** instead of relying entirely on internal knowledge.

## A Simple Example

User: *"What is 25 × 48?"*

```
Reason: I need an exact calculation.
Act:    calculator(25, 48)
Observe: 1200
Reason: I have the answer.
Final:  1200
```

Pattern: `Reason → Act → Observe → Reason → Answer`.

## A More Interesting Example

User: *"Find the best laptop under $1,500 for AI development."*

```
Reason:  I need current product candidates.
Act:     search_products("AI laptops under $1500")
Observe: Laptop A, Laptop B, Laptop C

Reason:  I need detailed specifications.
Act:     get_product_details(...)
Observe: GPU/RAM/CPU information

Reason:  I need to compare them.
Act:     compare_products(...)
Observe: Laptop B is strongest candidate.

Reason:  I have enough information.
Final:   Recommend Laptop B.
```

This is ReAct behavior.

## ReAct Is Not Just "Thinking"

This distinction is important. ReAct isn't `Think → Think → Think → Think → Answer`. It's `Reason → Act → Observe → Reason → Act → Observe`. The agent's reasoning is connected to **real actions and observations** -- that's what makes it useful for tool-using agents.

## ReAct and the Agent Loop

You've already learned the agent loop: `Decide → Act → Observe → Update State → Decide again`. ReAct is closely related: `Reason → Act → Observe → Reason again`. You can think of ReAct as a **reasoning-and-action pattern for implementing agent behavior**.

## ReAct With State

```
state = {
    "goal": "Find best apartment under 5M",
    "properties": [],
    "selected_property": None,
    "roi": None
}
```

Agent reasons *"I don't have any candidate properties"* → action: `search_properties()` → observation: 10 properties found → `state["properties"] = [...]`. Agent reasons again: *"I have candidates, I need details for the strongest ones"* → action: `get_property_details(...)` → observation → then `calculate_roi()` → observe → reason → final answer.

## ReAct and Planning

Planning might produce a fixed list: search, get details, calculate ROI, compare. **ReAct can work more dynamically**: reason *"I need properties"* → act: search → observe: only 2 found → reason *"I need more candidates"* → act: broaden query → observe: 10 found → reason *"now I can compare."* The agent can **change its next action based on what it observes** -- one of ReAct's strengths.

## ReAct Is Naturally Adaptive

Suppose the plan is `Search → Get details → Calculate ROI`, but search returns no results. A rigid system may fail. A ReAct agent: observe *"no results"* → reason *"the query may be too restrictive"* → act: broaden search → observe: results found → reason: continue. The agent can **react to the environment** -- where the name comes from: Reason + Act.

## ReAct With Multiple Tools

Academic agent with `search_regulations()`, `get_course_info()`, `calculate_gpa()`, `get_student_schedule()`. User: *"Can I register for CSE251?"*

```
Reason: I need the course requirements.
Act:    get_course_info("CSE251")
Observe: Prerequisites returned.

Reason: I need to know the student's current courses.
Act:    get_student_schedule(student_id)
Observe: Student schedule returned.

Reason: Now I can compare prerequisites.
Final:  Registration status...
```

The agent selects different tools **based on the information it obtains**.

## ReAct vs Fixed Workflow

Fixed workflow: `search → retrieve → generate` -- the sequence is predefined. ReAct: `Goal → Reason → Choose action → Observe → Reason → Choose action → Observe → ...` -- the next action can depend on the previous result. **Fixed workflow = predetermined execution path. ReAct = adaptive execution based on observations.**

## A Simplified ReAct Implementation

```
while True:
    decision = agent(state)

    if decision["type"] == "final":
        return decision["answer"]

    if decision["type"] == "tool":
        result = execute_tool(decision["tool"], decision["arguments"])
        state["last_result"] = result
```

Conceptually: `agent(state) → Reason + decide → Tool → Result → state update → agent(state)`. The next call receives the new information.

## What Does the LLM Actually Produce?

Conceptually, `{"type": "tool", "tool": "search_properties", "arguments": {"location": "New Cairo", "max_price": 5000000}}`. The application executes it, then returns *"Tool result: Found 8 properties"* to the LLM. Now the model gets another opportunity to decide. This **repeated interaction** is the important part.

## Don't Confuse ReAct With Chain-of-Thought

ReAct is a **system/agent pattern**, not simply a prompt asking the model to "think step by step." The useful structure is `Reasoning/decision → Action → Observation`. The reasoning leads to an external action, and the observation influences the next decision. The value comes from the **interaction loop**, not merely generating a long hidden reasoning text.

## Modern Implementations May Hide Reasoning

In older descriptions of ReAct, you may see explicit `Thought: ... Action: ... Observation: ...` traces in tutorials. But in modern production systems, you generally don't need to expose or log private chain-of-thought. You can model the system as `Decision → Tool call → Observation → Decision` -- the important engineering behavior remains the same.

## ReAct + RAG

*"According to the university regulations, can I register for CSE251?"* A ReAct-style agent: reason *"need relevant regulation"* → act: `search_regulations()` → observe: retrieved chunks → reason *"prerequisite information is missing"* → act: `search_regulations("CSE251 prerequisites")` → observe: relevant section → reason: enough evidence → final answer. This is essentially an **adaptive retrieval process** -- you've already learned Agentic RAG, so now you can see the underlying mechanism more clearly.

## ReAct Can Reduce Unnecessary Actions

If the first search already gives everything needed, the agent can stop: `Search → Excellent result → Reason: enough information → Answer`. It doesn't need to search again and again. This is another reason **state and stopping conditions matter**.

## But ReAct Can Also Become Inefficient

Every loop may require an LLM inference, tool execution, another LLM inference, another tool execution, and so on -- this can become slower, more expensive, and harder to debug. Use agent loops **when adaptability provides enough value to justify the additional complexity**.

## ReAct and Hallucination

ReAct can reduce some forms of hallucination because the agent can obtain external information -- instead of *"I think the property costs 4.2M,"* it calls `search_properties()` and uses the actual retrieved price. However, ReAct does **not automatically eliminate hallucinations**: the agent can still misunderstand tool output, choose the wrong tool, make incorrect calculations, misinterpret retrieved documents, or fabricate conclusions. Tool use improves grounding, but doesn't guarantee correctness.

## ReAct Needs Guardrails

A production ReAct system should have maximum iterations, tool permissions, timeouts, error handling, input validation, output validation, and cost limits. For example, `MAX_STEPS = 8`; if `step >= MAX_STEPS`, stop. This prevents `Reason → Act → Observe` from looping forever.

## ReAct and LangGraph

A ReAct-style graph can conceptually look like:

```
             ┌─────────────┐
             │  Agent Node │
             └──────┬──────┘
                    ↓
             Should use tool?
                /       \\
              Yes        No
               ↓          ↓
          Tool Node     Answer
               ↓
          Update State
               ↓
          Agent Node
               ↑
               └────────
```

This is essentially `Agent → Tool → Agent → Tool → Agent`. LangGraph can make this loop explicit and controllable.

## The Complete Picture

```
                    USER GOAL
                        ↓
                      STATE
                        ↓
                    PLANNING
                        ↓
                 REACT AGENT
                        ↓
                  REASON / DECIDE
                        ↓
                  SELECT TOOL
                        ↓
                 FUNCTION CALL
                        ↓
                      TOOL
                        ↓
                   OBSERVATION
                        ↓
                  UPDATE STATE
                        ↓
                    REASON AGAIN
                        ↓
                 ┌──────┴──────┐
                 ↓             ↓
              Continue       Finish
                 ↓             ↓
               Tool        Final Answer
                 │
                 └────→ loop
```

*The single idea to keep: ReAct is an agent pattern where the system repeatedly reasons/decides, takes an action, observes the real result, and uses that observation to decide what to do next -- the important thing isn't the word "reason," it's the connection between decision, action, real observation, and new decision that makes the agent adaptive.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace a ReAct Loop for Course Registration",
                    "description": (
                        "Your AI academic agent receives: \"Can I register for CSE251 based on my current courses?\" Available tools: "
                        "get_course_info(), get_student_schedule(), search_regulations(). Describe a ReAct loop for this task. Answer: "
                        "(1) What should the agent do first? (2) What observation might cause it to call another tool? "
                        "(3) Suppose get_course_info() doesn't contain the prerequisite information -- what should the agent do? "
                        "(4) When should the agent stop? (5) Why is this better suited to ReAct than simply asking the LLM to answer immediately?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "react"],
                },
                {
                    "title": "Implement a ReAct Step With Adaptive Query Widening",
                    "description": (
                        "Implement `react_step(state, decide_fn, execute_tool_fn)` that runs exactly one Reason→Act→Observe cycle: "
                        "call decide_fn(state) to get a decision, execute the tool if one was chosen, append the observation to "
                        "state['observations'], and return the updated state. Then write a short driver loop that keeps calling "
                        "react_step until decide_fn returns a 'final' decision or 6 steps have passed -- demonstrating the "
                        "'agent reacts to what it observes' idea from the lesson (e.g. broadening a search after an empty result)."
                    ),
                    "starter_code": (
                        "def react_step(state, decide_fn, execute_tool_fn):\n"
                        "    # TODO: get a decision from decide_fn(state)\n"
                        "    # TODO: if it's a tool call, execute it and append the result to\n"
                        "    # state.setdefault('observations', []); return (state, decision)\n"
                        "    pass\n\n"
                        "def run_react(state, decide_fn, execute_tool_fn, max_steps=6):\n"
                        "    # TODO: call react_step repeatedly until decision type is \"final\"\n"
                        "    # or max_steps is reached; return the final answer or raise an error\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def react_step(state, decide_fn, execute_tool_fn):\n"
                        "    decision = decide_fn(state)\n\n"
                        "    if decision[\"type\"] == \"tool\":\n"
                        "        result = execute_tool_fn(decision[\"tool\"], decision[\"arguments\"])\n"
                        "        state.setdefault(\"observations\", []).append(result)\n\n"
                        "    return state, decision\n\n"
                        "def run_react(state, decide_fn, execute_tool_fn, max_steps=6):\n"
                        "    for _ in range(max_steps):\n"
                        "        state, decision = react_step(state, decide_fn, execute_tool_fn)\n"
                        "        if decision[\"type\"] == \"final\":\n"
                        "            return decision[\"answer\"]\n\n"
                        "    raise RuntimeError(\"ReAct loop did not reach a final answer within max_steps\")\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "react"],
                },
            ],
            "quiz": {
                "title": "ReAct — Knowledge Check",
                "questions": [
                    {
                        "question": "What does ReAct stand for, and what is its core loop?",
                        "options": [
                            "Retrieve + Act; the loop is Retrieve → Generate → Answer",
                            "Reason + Act; the loop is Reason → Act → Observe → Reason again",
                            "Reflect + Activate; the loop is Reflect → Activate → Stop",
                            "React is not an acronym and has no defined loop",
                        ],
                        "correct": 1,
                        "explanation": "ReAct = Reason + Act. The core loop is Reason → Act → Observe → Reason again, repeating until a final answer.",
                    },
                    {
                        "question": "How does the lesson distinguish ReAct from plain chain-of-thought prompting?",
                        "options": [
                            "There is no difference -- they are the same technique",
                            "ReAct is a system/agent pattern connecting reasoning to real external actions and observations, not just generating a long hidden reasoning text",
                            "Chain-of-thought always outperforms ReAct in every case",
                            "ReAct never involves any reasoning at all",
                        ],
                        "correct": 1,
                        "explanation": "The lesson stresses that ReAct's value comes from the interaction loop -- reasoning tied to real tool actions and observations -- not merely 'thinking step by step' in text.",
                    },
                    {
                        "question": "How is ReAct 'naturally adaptive' compared to a fixed plan, per the lesson's search example?",
                        "options": [
                            "It isn't -- ReAct always follows the exact same steps regardless of results",
                            "If a search returns no results, a ReAct agent can observe that, reason that the query was too restrictive, and act by broadening the search -- a fixed plan may just fail",
                            "ReAct eliminates the need for any tools",
                            "ReAct only works when there is exactly one available tool",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's example shows the agent reacting to an empty result by broadening its query -- something a rigid, predetermined plan wouldn't naturally do.",
                    },
                    {
                        "question": "Does ReAct automatically eliminate hallucination, according to the lesson?",
                        "options": [
                            "Yes, using any tool guarantees a fully correct answer",
                            "No -- tool use improves grounding, but the agent can still misinterpret tool output, choose the wrong tool, or make calculation errors",
                            "ReAct has nothing to do with hallucination at all",
                            "Yes, but only if the agent uses exactly one tool per request",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: ReAct reduces some hallucination by grounding answers in real tool results, but doesn't guarantee correctness -- misinterpretation and tool misuse are still possible.",
                    },
                    {
                        "question": "Why does a production ReAct system need guardrails like MAX_STEPS?",
                        "options": [
                            "Guardrails are only cosmetic and don't affect behavior",
                            "Without them, the Reason → Act → Observe cycle could repeat indefinitely, becoming slow, expensive, and hard to debug",
                            "MAX_STEPS is required by the Python language itself",
                            "Guardrails are only needed if the agent uses read-only tools",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly warns that every loop iteration costs LLM inference and tool execution -- without limits like MAX_STEPS, the cycle can run forever or become prohibitively expensive.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 11
        # ------------------------------------------------------------
        {
            "title": "Router Agents",
            "slug": "ai-developer-ai-agents-router-agents",
            "description": "How a router decides which specialist, workflow, or agent should handle a request; rule-based vs LLM-based routing with structured output; router vs tool selection vs supervisor; and why simple requests should route to simple, deterministic systems.",
            "order": 11,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.25,
            "skill_tags": ["ai-agents", "routing", "system-design"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Router Agents",
                "content": """# Router Agents

So far, our agent has learned how to use tools, maintain state, plan, select tools, loop, and use the ReAct pattern. Now we introduce a specialized agent pattern: **a Router Agent decides which path, tool, specialist, or workflow should handle a request.**

## What Problem Does a Router Solve?

Imagine an AI assistant for a university. Users can ask about GPA, course prerequisites, credit-hour costs, or password resets -- completely different systems. Instead of one giant agent handling everything:

```
                    User
                      ↓
                Giant Agent
               /    |     \\
          GPA    Courses   IT
```

we can use a router:

```
                    User
                      ↓
                   Router
                /     |      \\
               ↓      ↓       ↓
             GPA   Academic    IT
            Agent    Agent    Agent
```

The router answers: **"Which specialist should handle this request?"**

## The Mental Model

Think of a router like a **receptionist**. You say *"I need help with my invoice"* -- the receptionist doesn't solve the invoice problem, they say *"Accounting handles that."*

```
User Request
     ↓
  Router
     ↓
Choose destination
     ↓
Specialist
     ↓
Answer
```

The router's main job is **routing, not solving**.

## Why Not Use One Agent?

You could give one agent 50 tools (`calculate_gpa()`, `search_courses()`, `reset_password()`, `create_invoice()`, ...), but this creates too many tools, harder tool selection, larger prompts, more mistakes, harder testing, harder permissions, harder maintenance. Instead:

```
Router
 ├── Academic Agent
 ├── Finance Agent
 ├── IT Agent
 └── Support Agent
```

Each specialist has a **smaller responsibility**.

## Router vs Tool Selection

These are related but not identical. **Tool selection** -- the agent decides *"which tool should I call?"* (e.g. *"What is 25 × 5?"* → `calculator()`). **Routing** -- the router decides *"which system/agent/workflow should handle this?"* (e.g. *"What is my GPA?"* → GPA Agent). So: `Routing → choose specialist`, `Tool Selection → choose capability inside specialist`.

## A Simple Example

Three agents: `academic_agent`, `finance_agent`, `support_agent`. *"What courses can I register for?"* → intent = academic → `academic_agent(...)`. *"How much did I spend this month?"* → intent = finance → `finance_agent(...)`.

## Router as a Classifier

At the simplest level: `User Request → Classification → Route`. *"What is CSE251?"* → academic. *"How much is my tuition?"* → finance. *"My account is locked"* → IT. A router is **a decision layer that maps requests to appropriate destinations.**

## Routing Doesn't Have to Use an LLM

This is an important engineering principle. A router can be **rule-based** (`if "gpa" in query: return "academic"`), **ML-based** (a text classifier), or **LLM-based** (structured route output). You should choose the **simplest method that works**.

## Rule-Based Routing

For predictable requests:

```
def route(query):
    if "gpa" in query.lower():
        return "academic"
    if "invoice" in query.lower():
        return "finance"
    if "password" in query.lower():
        return "support"
```

Extremely simple -- and that's sometimes exactly what you want.

## LLM-Based Routing

For more complex language: *"I've finished my courses and want to know whether I satisfy the graduation requirements."* The router needs to understand the meaning and might produce `{"route": "academic"}`, then `academic_agent` handles the request.

## Structured Routing

You generally don't want the LLM to return free text like *"Hmm, I think this sounds like academic."* Instead, use structured output: `{"route": "academic", "confidence": 0.96}`. Your application can validate `route ∈ {academic, finance, support}` and execute the corresponding path. Much safer than letting the model generate arbitrary routing instructions.

## Router With Workflows

A router doesn't have to route to another agent -- it can route to a **workflow**:

```
                    User
                      ↓
                   Router
                 /        \\
                ↓          ↓
          RAG Workflow   Agent
```

For simple questions: `Router → RAG → Answer`. For complex tasks: `Router → Agent → Tools → Answer`. This is often a very good architecture.

## Example: Customer Support System

```
Router
 ├── FAQ RAG
 ├── Order Agent
 ├── Refund Workflow
 └── Human Support
```

*"Where is my order?"* → order-related → Order Agent. *"What's your return policy?"* → policy question → FAQ RAG. *"I want a refund"* → refund request → Refund Workflow. *"I want to speak to a human"* → human request → Human Support. Much more organized than one giant agent.

## Router + RAG

```
                    User
                      ↓
                   Router
             /        |        \\
            ↓         ↓         ↓
       HR Documents  Legal    Technical
          RAG         RAG        RAG
```

*"What is the vacation policy?"* → HR → HR RAG. *"What does the API documentation say about authentication?"* → Technical → Technical RAG. Now retrieval happens **inside the appropriate domain**.

## Router vs Multi-Agent System

A router is often the **entry point** of a multi-agent architecture:

```
                   User
                     ↓
                  Router
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
  Research Agent  Coding Agent  Finance Agent
```

The router doesn't necessarily perform the task -- it determines **who should perform the task**. We'll go much deeper into multi-agent communication and collaboration in a later lesson.

## Router Can Use Context

Routing shouldn't always depend only on the latest message. *"I need help with CSE251"* → Academic Agent. Then *"And what about the prerequisites?"* -- ambiguous alone, but conversation state says `current_topic = CSE251`, so → Router → Academic Agent. This shows **state matters even at the routing level**.

## Router + Memory

If the user previously said *"I'm working on my graduation requirements,"* and later says *"Can you check this?"*, the router might need conversation context to understand what "this" refers to: `User message → Memory/Context → Router → Destination`. Routing is not necessarily based on one isolated sentence.

## Routing Based on Task Complexity

```
                   User
                     ↓
                  Router
                 /      \\
                ↓        ↓
            Simple       Complex
              ↓            ↓
           RAG/API       Agent
```

*"What is the university's GPA scale?"* → Simple → RAG. *"Analyze my completed courses, calculate my GPA, check graduation requirements, and tell me what I still need"* → Complex → Agent. This architecture can save cost and latency.

## A Very Useful Pattern

```
                         USER
                           ↓
                        ROUTER
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Simple        RAG          Agent
           Request      Request      Request
              ↓            ↓            ↓
             API        Retrieval   Tool Loop
              ↓            ↓            ↓
              └────────────┼────────────┘
                           ↓
                       Final Answer
```

Not every request needs an agent. **Use the least complex architecture that can reliably solve the request.**

## Router Mistakes

*"How much will three credit hours cost?"* -- if the router incorrectly chooses GPA Agent instead of Tuition Agent, the entire downstream system produces the wrong answer. **Routing is a critical decision point.**

## What Can We Do About Routing Errors?

**Clear route definitions** -- instead of just `finance`, `academic`, write full descriptions of what each category covers. **Structured output** -- force `{"route": "academic"}` rather than arbitrary text. **Fallback** -- if uncertain, ask for clarification (e.g. *"Do you mean the course requirements or the tuition cost?"*). **Confidence threshold** -- conceptually `if confidence < 0.7: ask_clarification()`. Don't blindly route uncertain requests.

## Router Can Also Reject

If your system only handles `academic`, `finance`, `support`, and the user asks *"Write me a poem about the ocean,"* the router can return `{"route": "unsupported"}` and the system can respond appropriately. Better than forcing the request into an unrelated agent.

## A Simple Python Router

```
def route(request):
    decision = llm_router(request)

    if decision == "academic":
        return academic_agent(request)
    elif decision == "finance":
        return finance_agent(request)
    elif decision == "support":
        return support_agent(request)
    else:
        return "I can't handle this request."
```

`Request → Router → Destination → Specialized system`.

## Router Inside a Larger Agent

A router can also appear inside an agent. A research agent might have its own internal router deciding between web, RAG, or database sources. Routing doesn't have to happen only at the application's entry point.

## Router vs Supervisor

**Router** -- usually `Input → choose ONE destination → Specialist` (e.g. *"Question"* → Academic Agent). **Supervisor** -- usually `Goal → Supervisor → delegate tasks → Agent A, Agent B, Agent C → combine results`. A supervisor coordinates **multiple** workers. We'll cover Supervisor Agents in a later lesson.

## The Deeper Mental Model

```
                         REQUEST
                            ↓
                         CONTEXT
                            ↓
                          ROUTER
                            ↓
                "Who should handle this?"
                            ↓
        ┌───────────────┬───────────────┐
        ↓               ↓               ↓
     Workflow          RAG            Agent
        ↓               ↓               ↓
     Execute         Retrieve        Agent Loop
        └───────────────┴───────────────┘
                            ↓
                         RESULT
```

*The single idea to keep: a router determines which specialized agent, workflow, tool group, or system should handle a request -- and one of the strongest engineering principles here is: don't send every request through a powerful autonomous agent, route simple tasks to simple, deterministic systems whenever possible.*
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design Routes for a University Assistant",
                    "description": (
                        "You have: Academic RAG, Finance RAG, GPA Calculator, Registration Agent, Human Support. The router receives: "
                        "(A) \"What are the prerequisites for CSE251?\" (B) \"How much do 6 credit hours cost?\" "
                        "(C) \"Calculate my GPA if I get A, B+, and A-.\" (D) \"Check my courses and tell me whether I can register for "
                        "CSE251.\" (E) \"I want to speak to a human.\" For each, decide which destination it should route to. Then answer: "
                        "why shouldn't request D simply go to the Academic RAG? Think carefully about the difference between retrieving "
                        "information and performing a decision/action using multiple pieces of information."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "routing"],
                },
                {
                    "title": "Implement a Router With Fallback and Confidence Threshold",
                    "description": (
                        "Implement `route_request(request, classify_fn, destinations, confidence_threshold=0.7)` where classify_fn(request) "
                        "returns {\"route\": str, \"confidence\": float}. If the route isn't in `destinations` or confidence is below the "
                        "threshold, return {\"route\": \"clarify\", \"message\": \"...\"} instead of calling a destination. Otherwise call "
                        "destinations[route](request) and return its result -- modeling the lesson's fallback and confidence-threshold "
                        "techniques for reducing routing errors."
                    ),
                    "starter_code": (
                        "def route_request(request, classify_fn, destinations, confidence_threshold=0.7):\n"
                        "    # destinations is a dict like {\"academic\": academic_agent, \"finance\": finance_agent}\n"
                        "    # TODO: call classify_fn(request) to get {\"route\": ..., \"confidence\": ...}\n"
                        "    # TODO: if route not in destinations or confidence < confidence_threshold,\n"
                        "    # return {\"route\": \"clarify\", \"message\": \"Could you clarify what you need help with?\"}\n"
                        "    # TODO: otherwise call destinations[route](request) and return its result\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def route_request(request, classify_fn, destinations, confidence_threshold=0.7):\n"
                        "    decision = classify_fn(request)\n"
                        "    route = decision.get(\"route\")\n"
                        "    confidence = decision.get(\"confidence\", 0)\n\n"
                        "    if route not in destinations or confidence < confidence_threshold:\n"
                        "        return {\"route\": \"clarify\", \"message\": \"Could you clarify what you need help with?\"}\n\n"
                        "    return destinations[route](request)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "routing"],
                },
            ],
            "quiz": {
                "title": "Router Agents — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the main job of a Router Agent, per the lesson's receptionist analogy?",
                        "options": [
                            "To solve every request itself using its own tools",
                            "To determine which specialist, workflow, or system should handle a request -- routing, not solving",
                            "To replace all other agents in the system entirely",
                            "To generate the final answer for every user message",
                        ],
                        "correct": 1,
                        "explanation": "Like a receptionist directing a visitor to accounting, a router's job is to route requests to the right destination, not to solve the request itself.",
                    },
                    {
                        "question": "How does routing differ from tool selection?",
                        "options": [
                            "They are exactly the same decision made by the same component",
                            "Routing chooses which specialist/system/workflow should handle a request; tool selection chooses which capability to call inside a given specialist",
                            "Tool selection always happens before any routing occurs",
                            "Routing can only happen using rule-based logic, never an LLM",
                        ],
                        "correct": 1,
                        "explanation": "Routing operates at a higher level (which system handles this?) than tool selection (which specific tool solves this within that system?).",
                    },
                    {
                        "question": "Why does the lesson recommend structured output (e.g. {\"route\": \"academic\"}) over free-text routing decisions?",
                        "options": [
                            "Structured output is only used for aesthetic reasons",
                            "It lets the application validate the route against a known, safe set of destinations rather than parsing arbitrary text",
                            "Free text is always faster to generate than structured output",
                            "Structured output eliminates the need for a router entirely",
                        ],
                        "correct": 1,
                        "explanation": "Structured output like {'route': 'academic'} can be validated against a known set of allowed destinations, which is much safer than interpreting free-form text.",
                    },
                    {
                        "question": "According to the lesson, does routing always require an LLM?",
                        "options": [
                            "Yes, routing is impossible without an LLM",
                            "No -- routing can be rule-based, ML-based, or LLM-based; you should choose the simplest method that works",
                            "Routing requires a dedicated vector database in every case",
                            "Routing can only be done by a human operator",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly lists rule-based (if/else on keywords), ML-based, and LLM-based routing, and recommends choosing the simplest approach that solves the problem.",
                    },
                    {
                        "question": "What is the key difference between a Router and a Supervisor, per the lesson?",
                        "options": [
                            "A router usually chooses one destination for a request; a supervisor delegates tasks across multiple workers and combines their results",
                            "A supervisor can only route to exactly one agent, same as a router",
                            "Routers and supervisors are the same pattern with different names",
                            "A router always coordinates multiple agents simultaneously",
                        ],
                        "correct": 0,
                        "explanation": "Router: Input → choose ONE destination → Specialist. Supervisor: Goal → delegate tasks → multiple agents → combine results. Supervisors coordinate multiple workers; routers pick a single path.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 12
        # ------------------------------------------------------------
        {
            "title": "Supervisor Agents",
            "slug": "ai-developer-ai-agents-supervisor-agents",
            "description": "How a supervisor coordinates multiple specialized worker agents toward a larger goal: supervisor vs router, sequential vs parallel coordination, structured inter-agent communication, hierarchical supervisors, and permission/approval boundaries.",
            "order": 12,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.5,
            "skill_tags": ["ai-agents", "multi-agent-systems", "system-design"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Supervisor Agents",
                "content": """# Supervisor Agents

Now we move from routing to coordination. A **Router** answers *"who should handle this request?"* A **Supervisor** answers *"how should I coordinate multiple agents to complete this task?"* This is the foundation of multi-agent systems.

## The Problem

*"Find good apartments in New Cairo, analyze their ROI, and prepare an investment recommendation."* This may require different specialists: `Property Research Agent → Financial Analysis Agent → Report Agent`. Who coordinates them? That's the **Supervisor Agent**.

## The Mental Model

Think of the supervisor as a **project manager**:

```
                    USER GOAL
                        ↓
                   SUPERVISOR
                  /     |      \\
                 ↓      ↓       ↓
            Research  Finance  Report
              Agent    Agent    Agent
                 \\      |       /
                  ↓     ↓      ↓
                   SUPERVISOR
                        ↓
                  Final Answer
```

The supervisor understands the overall goal, decides which specialist should work, gives them tasks, receives results, decides what to do next, and combines the results.

## Router vs Supervisor

This is one of the most important distinctions in this level. **Router** usually chooses ONE destination: `User → Router → ONE specialist`, and then the router's job is mostly finished. **Supervisor** coordinates an ongoing process: `User → Supervisor → Agent A → Agent B → Agent C → Supervisor → Final answer`. **The supervisor stays involved.**

## A Real Example

*"Analyze whether buying this apartment is a good investment."* Available agents: Research, Financial, Risk, Report. The supervisor might decide: (1) ask Research Agent for property information, (2) ask Financial Agent to calculate ROI, (3) ask Risk Agent to evaluate risks, (4) give all results to Report Agent, (5) return final recommendation. **No single specialist needs to know how to do everything.**

## Why Use Multiple Agents?

A giant agent with web research, financial analysis, risk analysis, report writing, database, email, etc. can become difficult to maintain. Instead, `Supervisor → Research Agent, Finance Agent, Risk Agent, Report Agent` -- each with a focused responsibility. Benefits: smaller prompts, clearer responsibilities, easier testing, easier maintenance, specialized instructions, independent tool access, better separation of permissions.

## A Supervisor Is Itself an Agent

This is important -- the supervisor isn't just a normal router. It can have its own LLM, its own state, planning ability, tool/agent selection, memory, a loop, and stopping conditions:

```
Supervisor
    ↓
Think about task
    ↓
Choose worker
    ↓
Receive result
    ↓
Update state
    ↓
Choose next worker
```

It is essentially an agent whose tools are **other agents**.

## Agents Can Become Tools

From the supervisor's perspective, `research_agent()`, `finance_agent()`, `risk_agent()` can look like tools: `Supervisor → Choose: research_agent() → Research result`. The supervisor receives the result and continues. **A multi-agent system can be viewed as an agent using other agents as specialized capabilities.**

## Example: AI Research System

*"Research whether Qdrant or FAISS is better for my production RAG system."* The supervisor might first ask a Requirements Agent to understand dataset size, deployment environment, filtering needs, distributed requirements. Then dispatch to Qdrant Agent and FAISS Agent in parallel, then combine the findings.

## Sequential Coordination

The simplest supervisor architecture:

```
Supervisor → Agent A → Agent B → Agent C → Supervisor
```

E.g. `Research → Financial analysis → Risk analysis → Report`. Each stage can depend on the previous one.

## Parallel Coordination

Sometimes agents don't depend on each other. `Market analysis`, `Risk analysis`, `Competition analysis` can happen independently:

```
                    Supervisor
                  /      |       \\
                 ↓       ↓        ↓
             Market     Risk   Competition
              Agent     Agent     Agent
```

Conceptually `results = run_parallel([market_agent, risk_agent, competition_agent])` -- this can **reduce latency**.

## Dependency Matters

If the Financial Agent needs the output of the Research Agent, they cannot run independently at the same time: `Research → Property details → Financial analysis`. **The supervisor needs to understand these dependencies.**

## Supervisor State

```
state = {
    "goal": "Analyze property",
    "research": None,
    "financial_analysis": None,
    "risk_analysis": None,
    "report": None
}
```

Supervisor chooses Research Agent; after completion, `state["research"] = research_result`. Now the supervisor knows *"research is complete"* and can decide what happens next.

## Supervisor Loop

```
                  Supervisor
                       ↓
                  Check State
                       ↓
               Choose Worker Agent
                       ↓
                 Worker Executes
                       ↓
                  Worker Result
                       ↓
                 Update State
                       ↓
                  Supervisor
                       ↓
             Task complete?
               /          \\
             No            Yes
             ↓              ↓
       Choose worker     Final answer
```

Notice how similar this is to the normal agent loop -- the difference is **the tools are now specialized agents**.

## Example With a University System

*"Can I register for CSE251, and if I can, how much will the course cost?"* A supervisor might coordinate: Registration Agent first → registration result → Finance Agent → cost → final answer. Why does registration need to happen first? Because if the student cannot register, the cost calculation might not even be relevant.

## Supervisor vs Workflow

A workflow always does `Research → Finance → Risk → Report` in that fixed order. A supervisor can dynamically decide: research → incomplete → research again, OR research → enough information → finance. **Workflow = predefined coordination. Supervisor = dynamic coordination.**

## Supervisor + ReAct

The supervisor can use the same ReAct idea: reason *"I need market data"* → act: `market_agent()` → observe: incomplete → reason: need another source → act: `research_agent()` → observe: more information → reason: now financial analysis is possible → act: `finance_agent()`. That's essentially **ReAct at the multi-agent level**.

## Supervisor Doesn't Necessarily Control Every Detail

A good architecture has layers. The supervisor doesn't need to know exactly how research happens internally (`web_search()`, `database()`, `document_search()`) -- it only needs to know *"Research Agent can perform research."* This gives us **abstraction**.

## Hierarchical Agents

You can have supervisors supervising other agents:

```
                   Main Supervisor
                    /           \\
                   ↓             ↓
          Research Supervisor   Operations
             /       \\
            ↓         ↓
        Web Agent   RAG Agent
```

This is a **hierarchical multi-agent architecture**. But more hierarchy means more complexity, more LLM calls, more latency, more debugging difficulty. **Don't create layers just because you can.**

## Communication Between Agents

Agents need to exchange information reliably:

```
Research Agent → structured result → Supervisor → Finance Agent
```

E.g. `{"property_price": 4200000, "annual_rent": 420000, "location": "New Cairo"}`. The supervisor can then pass the relevant data to the financial agent -- **much safer than passing huge blocks of unstructured text everywhere.**

## Structured Communication Is Important

Bad: *"I searched around and found something interesting... maybe the property costs around 4.2 million..."* Better: `{"price": 4200000, "annual_rent": 420000, "area": 145, "location": "New Cairo"}`. Now another agent can reliably consume it -- **especially important in production systems.**

## Agent Responsibilities Should Be Clear

Good: Research Agent finds and verifies information; Finance Agent calculates financial metrics; Risk Agent analyzes risks; Report Agent transforms verified results into a report. Bad: Agent A, B, and C all *"do everything."* **If responsibilities overlap heavily, you may not actually need multiple agents.**

## A Common Mistake: Too Many Agents

You don't need five agents each doing one tiny operation (search, filter, read, summarize, format) when *one agent with several deterministic tools* would do. **Use multiple agents when there is a meaningful reason for specialization.**

## Supervisor Architecture Example

```
                         USER
                           ↓
                      SUPERVISOR
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
         Research       Finance       Risk
           Agent         Agent        Agent
              ↓            ↓            ↓
              └────────────┼────────────┘
                           ↓
                      SUPERVISOR
                           ↓
                     Report Agent
                           ↓
                      Final Report
```

## How This Relates to Your Agentic RAG Knowledge

`Supervisor → Research Agent → RAG`. The research agent itself might have `search_web()`, `search_documents()`, `rerank()`. So the hierarchy is `Supervisor → Research Agent → RAG system → Hybrid retrieval → Reranker`. **Your previous RAG knowledge becomes one specialized capability inside a larger agent architecture.**

## A Framework-Independent Python Model

```
def supervisor(state):
    if state["research"] is None:
        return "research_agent"
    if state["financial"] is None:
        return "finance_agent"
    if state["risk"] is None:
        return "risk_agent"
    return "finish"

while True:
    next_agent = supervisor(state)
    if next_agent == "finish":
        break
    result = agents[next_agent](state)
    state[next_agent] = result
```

`Supervisor → Choose worker → Worker → Result → State → Supervisor`.

## Supervisor and Human Approval

If the supervisor determines *"the refund should be issued"* but that's a sensitive action:

```
Supervisor → Refund Agent → Approval Required → Human → Approved → Refund
```

This connects directly to a later Human-in-the-Loop lesson.

## Supervisor Security

Imagine the supervisor has access to `database_agent`, `email_agent`, `payment_agent`, `delete_data_agent`. A mistake could have significant consequences:

```
Supervisor → Policy/Permission Layer → Worker → Tool
```

Again: **the LLM should not be the security boundary** -- the application must enforce permissions.

## The Deepest Mental Model

Think of a multi-agent system like an organization:

```
                    CEO / Supervisor
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   Research Team      Finance Team       Operations
        ↓                  ↓                  ↓
      Tools              Tools              Tools
```

The supervisor doesn't perform every task -- it **coordinates specialists**.

*The single idea to keep: a supervisor coordinates multiple specialized agents toward a larger goal, staying involved through the whole process -- while a router picks one destination and steps aside, a supervisor keeps choosing, observing, and deciding until the goal is complete.*
""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design a Supervisor for Investment Analysis",
                    "description": (
                        "Design a supervisor for: \"Analyze whether I should buy this apartment as an investment.\" Available "
                        "specialists: Research Agent, Financial Agent, Risk Agent, Report Agent. Answer: "
                        "(1) What should the supervisor ask each agent to do, and in what order? "
                        "(2) Could any agents work in parallel? Which ones, and why? "
                        "(3) Suppose the Research Agent returns incomplete property information -- what should the supervisor do? "
                        "(4) Why is this a Supervisor problem rather than simply a Router problem?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "multi-agent-systems"],
                },
                {
                    "title": "Implement a State-Driven Supervisor Loop",
                    "description": (
                        "Implement `run_supervisor(state, choose_next_fn, agents, max_steps=10)` where choose_next_fn(state) returns "
                        "either the name of the next worker agent to run or \"finish\". On each step, run the chosen agent (from the "
                        "`agents` name→function dict) with the current state, store its result back into state under that agent's name, "
                        "and stop when choose_next_fn returns \"finish\" or max_steps is reached -- mirroring the lesson's "
                        "check-state -> choose-worker -> execute -> update-state supervisor loop."
                    ),
                    "starter_code": (
                        "def run_supervisor(state, choose_next_fn, agents, max_steps=10):\n"
                        "    # agents: dict like {\"research_agent\": research_agent_fn, \"finance_agent\": finance_agent_fn}\n"
                        "    # choose_next_fn(state) -> agent name (must be a key in agents) or \"finish\"\n"
                        "    # TODO: implement the loop, storing each agent's result as state[name] = result\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def run_supervisor(state, choose_next_fn, agents, max_steps=10):\n"
                        "    for _ in range(max_steps):\n"
                        "        next_agent = choose_next_fn(state)\n\n"
                        "        if next_agent == \"finish\":\n"
                        "            return state\n\n"
                        "        if next_agent not in agents:\n"
                        "            raise ValueError(f\"Unknown agent: {next_agent}\")\n\n"
                        "        result = agents[next_agent](state)\n"
                        "        state[next_agent] = result\n\n"
                        "    raise RuntimeError(f\"Supervisor did not finish within {max_steps} steps\")\n"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["ai-agents", "python", "multi-agent-systems"],
                },
            ],
            "quiz": {
                "title": "Supervisor Agents — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the key difference between a Router and a Supervisor?",
                        "options": [
                            "They are identical patterns with different names",
                            "A router usually chooses one destination and its job is mostly done; a supervisor stays involved, coordinating multiple agents across the task",
                            "A supervisor can only coordinate exactly two agents",
                            "A router coordinates workers while a supervisor picks a single destination",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: a router picks ONE destination and is mostly finished; a supervisor remains engaged, orchestrating multiple agents until the whole task is complete.",
                    },
                    {
                        "question": "In what sense is a supervisor 'itself an agent,' per the lesson?",
                        "options": [
                            "It isn't -- a supervisor is just a simple if/else router",
                            "It can have its own LLM, state, planning ability, and stopping conditions -- its 'tools' are other agents",
                            "A supervisor has no state or decision-making of its own",
                            "Supervisors can never use the ReAct pattern",
                        ],
                        "correct": 1,
                        "explanation": "The lesson describes the supervisor as an agent whose tools happen to be other specialized agents, complete with its own state, planning, and loop.",
                    },
                    {
                        "question": "When can worker agents run in parallel under a supervisor, according to the lesson?",
                        "options": [
                            "Always -- all worker agents should run in parallel by default",
                            "When their tasks don't depend on each other's results (e.g. market analysis, risk analysis, and competition analysis run independently)",
                            "Only when there is exactly one worker agent",
                            "Parallel execution is never possible in multi-agent systems",
                        ],
                        "correct": 1,
                        "explanation": "The lesson distinguishes dependent tasks (must run sequentially, e.g. financial analysis needing research output) from independent tasks that can run in parallel.",
                    },
                    {
                        "question": "Why does the lesson recommend structured messages (e.g. JSON) between agents rather than free-form text?",
                        "options": [
                            "Structured messages are only for visual appeal",
                            "Structured messages act like an API contract, so downstream agents can reliably consume the data instead of parsing ambiguous prose",
                            "Free-form text is not supported by any LLM",
                            "Structured messages remove the need for a supervisor entirely",
                        ],
                        "correct": 1,
                        "explanation": "The lesson compares this to API contracts: structured data like {'price': 4200000, ...} is far more reliable for downstream agents to consume than unstructured prose.",
                    },
                    {
                        "question": "What does the lesson say about enforcing permissions in a supervisor architecture with sensitive tools (e.g. payment_agent, delete_data_agent)?",
                        "options": [
                            "The LLM supervisor can be trusted as the sole security boundary",
                            "A permission/policy layer must sit between the supervisor's choice and the worker's execution -- the LLM should not be the security boundary",
                            "Sensitive tools should never be given to any agent under any circumstances",
                            "Permission checks are unnecessary if the supervisor uses ReAct",
                        ],
                        "correct": 1,
                        "explanation": "The lesson repeats a core principle from earlier lessons: the LLM should not be the security boundary. A policy/permission layer must enforce what's actually allowed.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 13
        # ------------------------------------------------------------
        {
            "title": "Multi-Agent Systems",
            "slug": "ai-developer-ai-agents-multi-agent-systems",
            "description": "When splitting one agent into multiple agents actually makes a system better: specialization, isolation, and permissions; communication patterns (sequential, parallel, hierarchical, peer-to-peer, debate); the costs of multi-agent architectures; and a decision checklist for when to use them.",
            "order": 13,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.5,
            "skill_tags": ["ai-agents", "multi-agent-systems", "system-design"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Multi-Agent Systems",
                "content": """# Multi-Agent Systems

Now we combine what you've learned about routers, supervisors, tools, state, planning, and agent loops. A **Multi-Agent System (MAS)** is a system where multiple specialized AI agents work together to accomplish a task or solve a larger problem. The important question is not *"how do I create many agents?"* It's **"when does splitting one agent into multiple agents actually make the system better?"**

## The Mental Model

Think of a team of engineers -- you don't ask one engineer to simultaneously be backend developer, database engineer, security engineer, UI designer, and DevOps engineer. Instead:

```
                    PROJECT
                       ↓
                 TEAM / MANAGER
              ┌────────┼────────┐
              ↓        ↓        ↓
           Backend   Security   DevOps
           Agent      Agent     Agent
```

Each specialist has a responsibility. That's the basic idea behind multi-agent systems.

## Single Agent vs Multi-Agent

**Single-agent system:**
```
                    User
                      ↓
                    Agent
                /     |      \\
             Tool    Tool    Tool
                \\     |      /
                    Answer
```
One agent controls everything.

**Multi-agent system:**
```
                    User
                      ↓
                 Coordinator
              /       |       \\
             ↓        ↓        ↓
          Agent A   Agent B   Agent C
             ↓        ↓        ↓
           Tools    Tools    Tools
              \\       |       /
               \\      |      /
                Coordinator
                      ↓
                    Answer
```
Now responsibility is distributed.

## Why Multiple Agents?

**Specialization** -- a financial agent can be optimized for ROI, cash flow, cap rate, NPV; a research agent focuses on search, documents, sources, fact verification. **Isolation** -- different agents can have different tools (Research Agent: web_search, document_search; Finance Agent: calculator; Email Agent: send_email). The finance agent doesn't need permission to send emails -- useful for security. **Different instructions** -- each agent can have a focused system prompt tailored to its job.

## Agents Are Not Necessarily Different Models

This is a common misunderstanding. Research Agent, Finance Agent, and Risk Agent could all use the **same** underlying LLM. What makes them different is often instructions, tools, state, responsibilities, permissions, and context. So: **Agent ≠ Model.** An agent is an application-level system built around a model -- you already learned this distinction earlier.

## Example: Real-Estate Investment System

```
                         USER
                           ↓
                      SUPERVISOR
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
      Research          Financial          Risk
       Agent             Agent             Agent
          ↓                ↓                ↓
       Search           Calculator        Analysis
          └────────────────┼────────────────┘
                           ↓
                     Report Agent
                           ↓
                         USER
```

Each agent solves a different part.

## Agent Responsibilities

**Research Agent** -- input: "find suitable properties"; output: `{"properties": [{"name": "Property A", "price": 4200000, "location": "New Cairo"}]}`. **Financial Agent** -- input: Property A, price, rent; output: `{"gross_rental_yield": 0.10}`. **Risk Agent** -- input: Property A; output: `{"risks": ["high service charges", "developer concentration"]}`. **Report Agent** -- input: research + financial + risk; output: investment recommendation.

## Communication Is Critical

A weak design passes huge natural-language conversations between agents (*"Well, I searched around and I think maybe..."*), which becomes difficult to parse. A better design uses **structured messages**: `{"property_id": "P123", "price": 4200000, "annual_rent": 420000}`. Think of it like an API contract.

## Agent Communication Is Similar to APIs

Just like a frontend `POST /users` expects a defined structure from the backend, `Research Agent → Structured Result → Financial Agent` expects a defined schema, e.g. a `PropertyData` class with `property_id`, `price`, `annual_rent`. This makes the multi-agent system much more reliable.

## Communication Patterns

**Sequential:** `A → B → C` (e.g. Research → Finance → Report). **Parallel:** a supervisor dispatches to `A`, `B`, `C` simultaneously (e.g. Market, Risk, Competition), which don't depend on each other's results. **Hierarchical:** a supervisor coordinates another group of agents, which itself may have sub-agents. **Peer-to-peer:** agents communicate directly without a central supervisor, e.g. `Research Agent ↔ Critic Agent`, where the critic reviews research and asks the researcher to improve it -- useful, but more complex.

## Debate-Style Systems

Multiple agents independently solve the same problem, then a **judge** compares outputs:

```
              Problem
                 ↓
        ┌────────┼────────┐
        ↓        ↓        ↓
     Agent A  Agent B  Agent C
        ↓        ↓        ↓
        └────────┼────────┘
                 ↓
              Judge
                 ↓
              Answer
```

*"Evaluate three possible investment strategies"* -- three agents independently analyze, a judge compares. This can provide different perspectives, cross-checking, and error detection. But: **more agents do not automatically mean better results.**

## Multi-Agent Systems Have Costs

If one agent requires 2 LLM calls, five agents + supervisor + communication might end up costing 15-30 LLM calls. The system may become slower, more expensive, harder to debug, harder to evaluate, and harder to reproduce. **Multi-agent architecture should solve a real architectural problem.**

## A Common Mistake

Developers sometimes build six agents because multi-agent systems *look impressive*. But if one agent with three tools works better, **use one agent**. Architecture should follow requirements, not hype.

## Multi-Agent vs Workflow

If you always need `Extract → Validate → Calculate → Generate report` in a fixed sequence, a deterministic **workflow** might be better -- you don't need an autonomous agent deciding every step.

## Multi-Agent vs Supervisor

A supervisor architecture (`Supervisor → Research Agent, Finance Agent, Risk Agent`) is **one type** of multi-agent system. But multi-agent systems can also be peer-to-peer (`Agent A ↔ Agent B`) or debate-style (`Agent A, Agent B, Agent C → Judge`). **Multi-agent system is the broad category. Supervisor is one coordination pattern within it.**

## Multi-Agent + RAG

An enterprise assistant might have `Supervisor → HR Agent, Legal Agent, Technical Agent`, each with its own retrieval system -- e.g. HR Agent → HR Qdrant Collection, Technical Agent → hybrid search + reranker over technical documentation. Your RAG knowledge becomes a component inside specialized agents.

## Multi-Agent + Tools

Each agent can have different tools: Research Agent (`web_search()`, `document_search()`), Financial Agent (`calculator()`, `market_data()`), Operations Agent (`database()`, `email()`). This creates an important **security boundary**: if the research agent doesn't need `send_email()`, don't give it the tool.

## Least Privilege

A principle to remember for production agents: **give each agent only the tools and permissions it actually needs.** Research Agent: search ✓, retrieve ✓, delete_database ✗, issue_refund ✗, send_email ✗. This reduces the **blast radius** of mistakes. We'll go deeper into agent security later.

## Shared State vs Separate State

Agents can share a common state (`state = {"research": ..., "financial": ..., "risk": ...}`), or each can have its own state, coordinated by a supervisor state. Shared state is convenient but excessive sharing can create **coupling**.

## Don't Share Everything

If the research agent produces 100 pages of research, sending everything to every agent is inefficient. Instead, pass only what's relevant -- a **structured summary** -- reducing token usage, latency, confusion, and accidental information leakage.

## Agent Contracts

A strong multi-agent system defines contracts, resembling a microservice architecture: Research Agent input `{"query": "Find investment properties"}` → output `{"properties": [...]}`. Financial Agent input `{"property": {...}}` → output `{"roi": 0.12, "cash_flow": 50000}`. Each component has **Input → Processing → Output**.

## Multi-Agent Systems Resemble Distributed Systems

A multi-agent system has components, communication, state, failures, timeouts, retries, dependencies, permissions, and observability -- very similar to distributed software systems. What if Agent B times out, returns malformed JSON, hallucinates, fails, or produces contradictory information? You need engineering around these failures.

## Failure Handling

If Research fails before Financial Agent needs its output, the supervisor could retry, use a fallback, ask another agent, ask a human, or stop. A production multi-agent system needs **explicit failure strategies**.

## Observability

Debugging one LLM call is straightforward; debugging `Supervisor → Agent A → Tool → Agent B → Tool → Agent C → Agent B` is much harder. You want to record `trace_id`, `agent_name`, `input`, `decision`, `tool_call`, `tool_result`, `latency`, `tokens`, `errors`, `final_output`. Observability becomes increasingly important as agent architecture grows.

## Example Architecture

```
                         USER
                           ↓
                        ROUTER
                           ↓
                     SUPERVISOR
                           ↓
       ┌───────────────────┼───────────────────┐
       ↓                   ↓                   ↓
 Research Agent       Analysis Agent      Verification Agent
       ↓                   ↓                   ↓
   Web + RAG          Python Tools         RAG + Sources
       └───────────────────┼───────────────────┘
                           ↓
                       REPORT AGENT
                           ↓
                         USER
```

Notice how concepts you've already learned fit together: Router, Supervisor, Agents, Tools, RAG, State, ReAct, Structured outputs. You're now building the architecture rather than learning isolated concepts.

## When Should You Use Multi-Agent?

Use it when you have **strong specialization** (genuinely different expertise), **different tools** (significantly different capabilities), **different permissions** (security boundaries matter), **independent work** (tasks can run concurrently), **complex coordination** (naturally decomposes into multiple roles), or **independent verification** (one agent critiques another).

## When Should You NOT Use It?

Avoid multi-agent if one agent + tools can solve the problem reliably, or when the task is simple, agents have overlapping responsibilities, latency is critical, cost is critical, or coordination adds little value.

## The Key Architecture Decision

```
Can a deterministic workflow solve this?
        ↓
      Yes → Use workflow

        No
        ↓
Can one agent + tools solve it?
        ↓
      Yes → Use one agent

        No
        ↓
Do we need specialization?
        ↓
      Yes → Consider multi-agent
```

This is a much better approach than starting with *"I want a multi-agent system."*

## Putting Everything Together

```
                         AI APPLICATION
                              ↓
                         Architecture
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
           Workflow        Agent         Multi-Agent
                              ↓               ↓
                            Tools        Coordination
                              ↓               ↓
                         Agent Loop      Supervisor
                              ↓               ↓
                            ReAct       Specialized Agents
```

And underneath all of them: **LLM + State + Tools + Application Logic**.

*The single idea to keep: a multi-agent system is not "many LLMs talking to each other" -- it's a deliberately designed system where specialized agents collaborate through defined responsibilities, structured communication, state, and coordination, and you should start with the simplest architecture that reliably solves the problem, adding multiple agents only when specialization, isolation, parallelism, or coordination provides a real benefit.*
""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design a Multi-Agent System for Company Analysis",
                    "description": (
                        "Design a multi-agent system for: \"Analyze a company before I invest in it.\" Available capabilities: Web "
                        "Search, Financial Database, News Search, Financial Calculator, Report Generation. Answer: "
                        "(1) Which agents would you create, and what tools would each receive? "
                        "(2) Which agents could run in parallel? "
                        "(3) Who should coordinate them -- Router, Supervisor, or no coordinator? "
                        "(4) Most importantly: would you actually choose a multi-agent architecture for this problem? Explain why or "
                        "why not, rather than creating agents just because the capabilities are available."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "multi-agent-systems", "system-design"],
                },
                {
                    "title": "Enforce Least-Privilege Tool Access Across Agents",
                    "description": (
                        "Implement `build_agent_registry(agent_tool_map, all_tools)` that, given a dict like "
                        "{\"research_agent\": [\"web_search\", \"document_search\"], \"finance_agent\": [\"calculator\"]} and a dict of "
                        "all_tools (name -> function), returns a dict mapping each agent name to a restricted callable dispatcher that "
                        "can ONLY call the tools listed for that agent -- raising PermissionError for anything else. This models the "
                        "lesson's 'least privilege' principle: each agent only gets the tools it actually needs."
                    ),
                    "starter_code": (
                        "def build_agent_registry(agent_tool_map, all_tools):\n"
                        "    # TODO: for each agent_name, allowed_tools in agent_tool_map.items(),\n"
                        "    # build a dispatcher function dispatch(tool_name, arguments) that:\n"
                        "    #   - raises PermissionError if tool_name not in allowed_tools\n"
                        "    #   - otherwise calls all_tools[tool_name](**arguments)\n"
                        "    # return {agent_name: dispatcher, ...}\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def build_agent_registry(agent_tool_map, all_tools):\n"
                        "    registry = {}\n\n"
                        "    for agent_name, allowed_tools in agent_tool_map.items():\n"
                        "        def make_dispatcher(allowed=allowed_tools):\n"
                        "            def dispatch(tool_name, arguments):\n"
                        "                if tool_name not in allowed:\n"
                        "                    raise PermissionError(\n"
                        "                        f\"Tool '{tool_name}' is not allowed for this agent\"\n"
                        "                    )\n"
                        "                return all_tools[tool_name](**arguments)\n"
                        "            return dispatch\n\n"
                        "        registry[agent_name] = make_dispatcher()\n\n"
                        "    return registry\n"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["ai-agents", "python", "multi-agent-systems", "security"],
                },
            ],
            "quiz": {
                "title": "Multi-Agent Systems — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the central question the lesson says you should ask about multi-agent systems?",
                        "options": [
                            "How do I create as many agents as possible?",
                            "When does splitting one agent into multiple agents actually make the system better?",
                            "Which LLM provider supports the most agents?",
                            "How do I avoid using any tools at all?",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly reframes the goal: not 'how many agents can I create' but 'does splitting actually improve this system.'",
                    },
                    {
                        "question": "Why does the lesson say 'Agent ≠ Model'?",
                        "options": [
                            "Because agents cannot use LLMs at all",
                            "Because multiple agents can share the same underlying LLM -- what differs is instructions, tools, state, responsibilities, and permissions",
                            "Because each agent must always use a completely different model",
                            "Because 'model' and 'agent' are simply two names for the exact same thing",
                        ],
                        "correct": 1,
                        "explanation": "The lesson clarifies that Research, Finance, and Risk agents could all run on the same LLM -- what makes them different agents is the application-level configuration around the model.",
                    },
                    {
                        "question": "Which communication pattern does the lesson describe as multiple agents independently solving the same problem, then a judge comparing their outputs?",
                        "options": [
                            "Sequential",
                            "Hierarchical",
                            "Debate-style",
                            "Peer-to-peer only",
                        ],
                        "correct": 2,
                        "explanation": "The debate-style pattern has several agents independently analyze the same problem, followed by a judge that compares and selects/synthesizes an answer.",
                    },
                    {
                        "question": "What does the 'least privilege' principle mean for multi-agent tool access?",
                        "options": [
                            "Every agent should have access to every tool just in case",
                            "Each agent should only receive the tools and permissions it actually needs, reducing the blast radius of mistakes",
                            "Only the supervisor should ever have any tools",
                            "Least privilege only applies to human users, not agents",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's example shows the Research Agent explicitly denied delete_database, issue_refund, and send_email -- giving each agent only what it needs limits potential damage from mistakes.",
                    },
                    {
                        "question": "According to the lesson's decision checklist, what should you check FIRST when deciding on an architecture?",
                        "options": [
                            "Whether a multi-agent system would look impressive to stakeholders",
                            "Whether a deterministic workflow can already solve the problem",
                            "How many different LLM providers are available",
                            "Whether the task can be solved without any AI at all",
                        ],
                        "correct": 1,
                        "explanation": "The decision flow starts with 'Can a deterministic workflow solve this?' before even considering a single agent, let alone a multi-agent system -- always favoring the simplest sufficient architecture.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 14
        # ------------------------------------------------------------
        {
            "title": "Human-in-the-Loop",
            "slug": "ai-developer-ai-agents-human-in-the-loop",
            "description": "Why AI agents shouldn't act autonomously on every action: approval/review/correction/escalation patterns, risk-based approval policies, human-in-the-loop vs human-on-the-loop, and why human approval alone is not a security mechanism.",
            "order": 14,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.5,
            "skill_tags": ["ai-agents", "human-in-the-loop", "agent-security"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Human-in-the-Loop",
                "content": """# Human-in-the-Loop

So far, we've built agents that can choose tools, plan, act, loop, route requests, and coordinate other agents. But there's an important question: **should an AI agent always be allowed to act by itself?** No. For some actions, we want a human to approve, review, or correct the agent before it continues. This is called **Human-in-the-Loop (HITL)**.

## The Mental Model

A normal autonomous agent looks like:

```
User → Agent → Tool → Action → Result
```

With Human-in-the-Loop:

```
User → Agent → Decision → Human Approval → Tool → Action → Result
```

The human becomes **part of the control loop**.

## Why Do We Need Humans?

Because some actions have consequences. An agent that can `send_email()`, `delete_file()`, `issue_refund()`, `transfer_money()`, `publish_post()`, `cancel_order()` -- you probably don't want `LLM → Tool → irreversible action` without any control. Instead: `LLM → "I want to issue a refund" → Human approval → Approved → issue_refund()`.

## The Key Distinction: Information vs Action

Not every agent decision needs human approval. **Low-risk**: *"Search the documentation"* -- Agent → Search, usually fine. **Higher-risk**: *"Delete the customer's account"* -- Agent → Human approval → Delete, much safer. **The more consequential the action, the more important human oversight becomes.**

## Four Common Types of Human-in-the-Loop

**1. Approval** -- the agent asks *"can I do this?"*; human approves or rejects. **2. Review** -- the agent produces something and asks *"does this look correct?"* (e.g. draft email → human reviews → send). **3. Correction** -- the human changes the agent's output (e.g. draft report → human edits → continue). **4. Escalation** -- the agent determines *"I can't confidently solve this"* → hands off to a human specialist. Especially useful when the system encounters an unusual situation.

## Simple Example

Customer-support agent. User: *"I want a refund."* Agent: `check_order() → verify_refund_policy() → calculate_refund()` → refund amount = $850. Because the amount is large: `Agent → Human approval required → Manager → Approve → issue_refund($850)`. **The AI handles the routine work. The human controls the risky action.**

## Human Approval as a Gate

A very useful mental model: **human approval is a gate between decision and execution.**

```
Agent Decision
      ↓
   [ GATE ]
      ↓
   Approved?
   /      \\
 Yes       No
 ↓          ↓
Execute    Stop
```

This pattern is extremely common in production AI systems.

## Important: the Human Should Approve the Actual Action

*"I need to modify the customer's account"* is too vague. Better: `Action: Update customer account. Customer: 12345. Change: Email → new@email.com.` The human should be able to understand **exactly what will happen**. Approval interfaces should expose action, target, parameters, relevant context, and potential consequences.

## Don't Make Humans Approve Everything

Bad architecture: `Search → Human approval → Read document → Human approval → Calculate → Human approval → Format → Human approval` -- the human becomes a bottleneck. Better: `Search → Read → Calculate → Prepare action → Human approval → Execute`. **Only interrupt when human judgment provides meaningful value.**

## Risk-Based Approval

Design approval around risk. Low risk (search web, read document) → autonomous. Medium risk (generate draft, small refund) → optional review. High/critical risk (large refund, delete account, transfer money) → human required. The exact policy depends on the application.

## HITL and Agent State

```
state = {
    "task": "Issue refund",
    "amount": 850,
    "approval": None
}
```

The agent reaches `approval = None` -- the system pauses. Human sets `approval = True`, then the agent continues:

```
State → Pause → Human input → Update state → Resume
```

This is why stateful agent frameworks are useful for HITL.

## HITL and the Agent Loop

Recall the agent loop: `Decide → Act → Observe → Decide again`. With HITL: `Decide → Is approval required? → Yes → Pause → Human → Update state → Resume → Act`. **Human intervention becomes another possible transition in the agent loop.**

## Example: Email Agent

*"Email the client and tell them their contract is terminated."* Instead of automatically calling `send_email()`, we use: `Agent → Generate draft → Human review → Edit if necessary → Approve → send_email()`. This is **review-based HITL**.

## HITL for AI-Generated Code

A coding agent fixes a bug and modifies `auth.py`. Before `git push production`, we require: `Agent → Generate changes → Run tests → Human review → Approve → Deploy`. Extremely useful because deployment is consequential.

## HITL in Your RAG Systems

Normal academic RAG needs no human for routine questions. But *"I want to appeal my academic dismissal"* is sensitive and high-impact: `RAG → Retrieve regulations → Draft guidance → Human academic advisor → Final response`. The AI assists; a human handles the consequential decision.

## HITL in Agentic RAG

Suppose an agent wants to modify a knowledge base: `Agent → Search documents → Detect outdated regulation → Propose update → Human reviewer → Approve → Update knowledge base`. Much safer than letting the agent directly modify authoritative information.

## HITL and Multi-Agent Systems

```
                    Supervisor
                        ↓
              ┌─────────┼─────────┐
              ↓         ↓         ↓
          Research    Finance     Risk
             Agent     Agent      Agent
              \\         |         /
               ↓        ↓        ↓
                  Supervisor
                      ↓
                Human Approval
                      ↓
                  Action Agent
```

The supervisor coordinates the work; the human controls the final consequential action.

## Human as a Specialized Agent

You can think of the human as another participant in the architecture (`Supervisor → Human Reviewer → Decision`), but a human is **not just another LLM worker**. Humans provide judgment, accountability, domain expertise, exception handling, and approval. The architecture should make this explicit.

## Escalation

The agent can detect uncertainty: `confidence = 0.92` → continue automatically; `confidence = 0.41` → escalate to a human. However, **don't rely only on an LLM-generated confidence score as a safety mechanism** -- use application-level rules too, e.g. `if transaction_amount > 1000: require_human()`. That's deterministic and enforceable.

## Human Approval vs Confidence

**Confidence** -- *"how sure does the system appear to be?"* **Approval** -- *"is this action authorized?"* A system might be highly confident (*"I am 99% sure this refund is correct"*) but that doesn't mean the AI is authorized to issue it. **Confidence is not permission** -- a very important production principle.

## Human-in-the-Loop Is Also Useful for Learning

If an agent repeatedly makes a mistake, human reviewers can provide corrections: `Agent output → Human correction → Store feedback → Evaluate → Improve system`. The feedback can improve prompts, routing, tool selection, retrieval, policies, and evaluation datasets. HITL can become part of an AI improvement loop.

## HITL Doesn't Mean Manual AI

The goal isn't *"AI does nothing, human does everything."* It's **AI handles routine work + human handles important decisions**. E.g. AI researches 100 documents, extracts information, calculates metrics, prepares a recommendation; human reviews, approves, and makes the final decision. Often much more efficient than either full automation or full manual work.

## A Production Architecture

```
                       USER
                         ↓
                      ROUTER
                         ↓
                    SUPERVISOR
                         ↓
                ┌────────┼────────┐
                ↓        ↓        ↓
             Research  Analysis  RAG
                Agent    Agent   Agent
                └────────┼────────┘
                         ↓
                    Decision
                         ↓
                Risk / Policy Check
                         ↓
                  Human Required?
                    /          \\
                  No            Yes
                  ↓              ↓
              Execute        Human Review
                                 ↓
                              Approve
                                 ↓
                              Execute
                                 ↓
                               Result
```

## Human-in-the-Loop vs Human-on-the-Loop

**Human-in-the-loop** -- the human directly participates in the decision/action loop: `AI → Human → AI` (e.g. AI proposes refund → human approves → AI executes). **Human-on-the-loop** -- the system operates autonomously while a human supervises and can intervene: `AI → AI → AI → AI` with a human monitoring, e.g. handling normal support tickets automatically while a human watches for serious failures.

## Human-in-the-Loop vs Human-Out-of-the-Loop

`Human-in-the-loop: AI → Human → Action`. `Human-out-of-the-loop: AI → Action` -- no human intervention required. The correct architecture depends on the risk and requirements of the application.

## A Practical Python Mental Model

```
def agent(state):
    action = decide(state)

    if requires_approval(action):
        state["pending_action"] = action
        return "WAIT_FOR_HUMAN"

    return execute(action)
```

Then, if the result is `"WAIT_FOR_HUMAN"`, get human approval; execute the pending action if approved, or cancel it otherwise. The important thing isn't the exact Python -- it's the architecture: `Decide → Check policy → Approval required? → Yes: Pause → Human → Resume | No: Execute`.

## The Security Lesson

One of the most important things to remember: **human approval should not be your only security mechanism.** If the agent says *"I want to transfer $50,000,"* your application should independently enforce: is this user authorized? Is the account valid? Is the amount allowed? Does policy require approval? **The LLM should propose actions. Your software should enforce permissions.**

## The Deeper Architecture

```
Agent → Tools → Agent Loop → ReAct → Router → Supervisor → Multi-Agent → Human-in-the-Loop
```

Each concept adds another layer of control:

```
             LLM
              ↓
         Agent Decision
              ↓
        ┌─────┴─────┐
        ↓           ↓
      Policy      State
        ↓           ↓
        └─────┬─────┘
              ↓
          Human Gate
              ↓
            Tool
              ↓
           Result
```

*The single idea to keep: AI should not perform every action autonomously -- human intervention should be risk-based (approval, review, correction, or escalation, not a gate on every trivial step), and confidence is not permission: the application, not the LLM, always enforces what's actually allowed.*
""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design HITL for a Real-Estate Investment Agent",
                    "description": (
                        "Your agent can search_properties(), calculate_roi(), analyze_risk(), send_email(), submit_purchase_offer(). "
                        "A user says: \"Find me a good investment property and make an offer if you think it's good.\" Design the "
                        "Human-in-the-Loop architecture. Answer: (1) Which actions can happen automatically? "
                        "(2) Which action should require human approval? (3) Where should the approval gate appear in the pipeline? "
                        "(4) What information should the human see before approving? (5) Why shouldn't the agent simply decide the "
                        "investment is good and submit the offer automatically?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "human-in-the-loop"],
                },
                {
                    "title": "Implement a Risk-Based Approval Gate",
                    "description": (
                        "Implement `decide_and_gate(state, decide_fn, risk_fn, threshold=1000)` that calls decide_fn(state) to get an "
                        "action (a dict with at least 'type' and, for money-related actions, 'amount'), uses risk_fn(action) to compute "
                        "a numeric risk score OR simply checks 'amount' > threshold, and returns either {\"status\": \"execute\", "
                        "\"action\": action} directly, or {\"status\": \"pending_approval\", \"action\": action} if human approval is "
                        "required -- modeling the lesson's deterministic 'if transaction_amount > 1000: require_human()' rule rather "
                        "than relying only on an LLM confidence score."
                    ),
                    "starter_code": (
                        "def decide_and_gate(state, decide_fn, risk_fn, threshold=1000):\n"
                        "    # action = decide_fn(state) -> e.g. {\"type\": \"issue_refund\", \"amount\": 850}\n"
                        "    # TODO: determine if approval is required (amount > threshold, or risk_fn(action) says high risk)\n"
                        "    # TODO: return {\"status\": \"execute\", \"action\": action} or\n"
                        "    #              {\"status\": \"pending_approval\", \"action\": action}\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def decide_and_gate(state, decide_fn, risk_fn, threshold=1000):\n"
                        "    action = decide_fn(state)\n\n"
                        "    amount = action.get(\"amount\", 0)\n"
                        "    requires_approval = amount > threshold or risk_fn(action) == \"high\"\n\n"
                        "    if requires_approval:\n"
                        "        return {\"status\": \"pending_approval\", \"action\": action}\n\n"
                        "    return {\"status\": \"execute\", \"action\": action}\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "human-in-the-loop", "security"],
                },
            ],
            "quiz": {
                "title": "Human-in-the-Loop — Knowledge Check",
                "questions": [
                    {
                        "question": "What is Human-in-the-Loop (HITL), per the lesson?",
                        "options": [
                            "A pattern where a human writes every response instead of the AI",
                            "A pattern where a human becomes part of the agent's decision/action control loop for consequential actions",
                            "A synonym for tool selection",
                            "A technique used only for evaluating LLM output quality after deployment",
                        ],
                        "correct": 1,
                        "explanation": "HITL inserts a human into the loop -- typically between decision and execution -- for actions that warrant human judgment or authorization.",
                    },
                    {
                        "question": "Which of these is NOT one of the four HITL patterns described in the lesson?",
                        "options": [
                            "Approval",
                            "Review",
                            "Correction",
                            "Automatic bulk deletion",
                        ],
                        "correct": 3,
                        "explanation": "The lesson lists Approval, Review, Correction, and Escalation as the four common HITL patterns -- automatic bulk deletion is not one of them.",
                    },
                    {
                        "question": "Why does the lesson warn against making humans approve every single agent step (search, read, calculate, format)?",
                        "options": [
                            "Because humans are incapable of approving more than one thing",
                            "Because the human becomes a bottleneck; approval should be reserved for steps where human judgment provides meaningful value",
                            "Because only read-only actions should ever require approval",
                            "Because approval gates are illegal in production systems",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly contrasts a bad architecture (approval after every step) with a better one that only gates the consequential action.",
                    },
                    {
                        "question": "What is the key distinction the lesson draws between 'confidence' and 'approval'?",
                        "options": [
                            "They are the same thing -- high confidence always implies approval",
                            "Confidence is how sure the system appears to be; approval is whether the action is authorized -- confidence is not permission",
                            "Approval only matters for low-confidence actions",
                            "Confidence scores should always be the sole gating mechanism",
                        ],
                        "correct": 1,
                        "explanation": "The lesson stresses that a system can be highly confident yet still not be authorized to act -- confidence and permission are separate concerns.",
                    },
                    {
                        "question": "What does the lesson say about human approval as a security mechanism?",
                        "options": [
                            "Human approval alone is sufficient and no further checks are needed",
                            "Human approval should not be the only security mechanism -- the application must independently enforce authorization, validity, and policy regardless of what a human approves",
                            "Security checks are only relevant when no human is involved",
                            "The LLM should independently verify user authorization without any application-level enforcement",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's security principle: the LLM proposes actions, but the software must independently enforce permissions -- human approval augments but doesn't replace that enforcement.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        # ------------------------------------------------------------
        # Topic 15 (capstone)
        #
        # NOTE: the raw lesson source jumps from Lesson 14 (Human-in-the-
        # Loop) to Lesson 17 (AI Agent Project). Lessons 15-16 -- likely
        # "Agent Security" (explicitly referenced at the end of Lesson 14:
        # "This becomes even more important in the next lessons on agent
        # security") and a second lesson, possibly on evaluation/guardrails
        # -- have not been provided yet. This topic is placed at order=15
        # for now (immediately after Human-in-the-Loop). If lessons 15-16
        # arrive later, they should be inserted here and this capstone
        # topic (plus any topics after it) renumbered accordingly.
        # ------------------------------------------------------------
        {
            "title": "Capstone Project: AI Research & RAG Agent",
            "slug": "ai-developer-ai-agents-capstone-research-rag-agent",
            "description": "The Level 7 capstone: design and (across upcoming project lessons) build a tool-using agent that decides what it needs, retrieves from a knowledge base, searches the web, calculates, and reasons over results to answer complex questions -- applying every concept from this level instead of just discussing it.",
            "order": 15,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 2.0,
            "skill_tags": ["ai-agents", "capstone", "rag", "agentic-systems"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "AI Agent Project 🚀",
                "content": """# AI Agent Project 🚀

Let's treat the project itself as a lesson. This is a practical capstone where we build an AI Agent step by step and apply the concepts you've learned instead of just discussing them.

## 🎯 Project: AI Research & RAG Agent

We will build an agent that can receive a complex question, decide what it needs, use tools, retrieve information from documents, reason over the results, and produce a final answer. For example: *"Analyze Qdrant vs FAISS for a production RAG system and recommend which one I should use."*

```
User Question
      ↓
    Agent
      ↓
What do I need?
      ↓
 ┌────┼──────────────┐
 ↓    ↓              ↓
RAG  Search       Calculator
 ↓    ↓              ↓
 └────┼──────────────┘
      ↓
   Analyze
      ↓
   Answer
```

## 🧠 What Are We Building?

The final system will look approximately like this:

```
                         USER
                           ↓
                    ┌─────────────┐
                    │    AGENT    │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │    STATE    │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │   PLANNER   │
                    └──────┬──────┘
                           ↓
                 ┌─────────┼─────────┐
                 ↓         ↓         ↓
              RAG Tool  Search    Calculator
                 ↓         ↓         ↓
                 └─────────┼─────────┘
                           ↓
                     Agent Loop
                           ↓
                      Evaluation
                           ↓
                     Final Answer
```

We'll add complexity gradually.

## 🏗️ Project Architecture

**1. LLM** -- the brain used by the agent: `LLM → Decision`.

**2. Agent** -- the central controller: decides what to do, chooses tools, observes results, decides what to do next.

**3. Tools** -- useful capabilities, e.g. `search_documents()`, `search_web()`, `calculate()`.

**4. RAG** -- the agent retrieves information from a knowledge base: `Agent → RAG Tool → Retriever → Vector Database → Relevant Documents`. We'll leverage your existing knowledge of embeddings, vector databases, hybrid search, and reranking without re-teaching those topics.

**5. State** -- the agent needs to remember what happened during the current task:

```
state = {
    "question": "...",
    "steps": [],
    "tool_results": [],
    "final_answer": None
}
```

**6. Agent Loop** -- the agent repeatedly thinks, chooses an action, executes a tool, observes the result, thinks again, and so on until a final answer.

## 📚 What You'll Learn Through the Project

Instead of learning these concepts separately, we'll implement them together: LLM, Tools, Function Calling, State, Agent Loop, Planning, RAG, Tool Selection, Memory, Human Approval, Evaluation.

## 🛠️ Technology Stack

We'll keep the architecture framework-independent initially, then implement it using tools you're already familiar with: **Python + LLM API + LangGraph + Qdrant + Sentence Transformers + FastAPI**. An important rule: **we will understand the architecture before using LangGraph abstractions.** You already know LangGraph -- the goal is to understand *why* the graph exists, not just memorize nodes and edges.

## 📁 Project Structure

Eventually we'll aim for something like:

```
ai-research-agent/
│
├── app/
│   ├── agent/
│   │   ├── state.py
│   │   ├── graph.py
│   │   ├── planner.py
│   │   └── prompts.py
│   │
│   ├── tools/
│   │   ├── search.py
│   │   ├── rag.py
│   │   └── calculator.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── reranker.py
│   │
│   └── api/
│       └── main.py
│
├── data/
├── tests/
├── requirements.txt
└── README.md
```

We will not build all of this at once -- we'll build it incrementally.

## 🧩 Project Goal

The user should eventually be able to ask: *"Compare Qdrant and FAISS for a production RAG application. Use my documentation and calculate which option makes more sense for my requirements."* The agent should: understand the request → determine required information → search knowledge base → search external information if necessary → calculate metrics if necessary → compare results → verify important information → generate final answer. The important part is that **the agent decides which capabilities it needs.**

## 🔥 First Project Lesson: Define the Agent

Before writing tools or LangGraph code, we need to answer: **what exactly is our agent responsible for?**

Our agent's job: *research a user's question using available knowledge and tools, determine what information is required, perform the necessary actions, and produce an evidence-based answer.*

```
Agent
│
├── Input
│     └── User question
│
├── Goal
│     └── Produce reliable answer
│
├── Capabilities
│     ├── Document retrieval
│     ├── Web search
│     └── Calculation
│
└── Output
      └── Final answer + evidence
```

## 🤔 Why Not Just Build a Normal RAG Pipeline?

A normal RAG system is roughly `Question → Retrieve → Generate → Answer`, with a mostly predefined retrieval strategy. Our agent can instead decide: *do I need documents? → Yes → RAG. Do I need current information? → Yes → Web Search. Do I need calculations? → Yes → Calculator. Do I need another step? → Yes → Continue.* That's the key difference.

## 🧠 Example

*"What is the tuition cost of 3 courses, and how much would the total be?"* → `RAG → find course prices → Calculator → calculate total → Answer`. *"Explain the university registration policy"* → could simply be `RAG → Answer`. *"What's the current price of NVIDIA stock?"* → could be `Web/Market Tool → Answer`. **The agent doesn't blindly execute the same pipeline every time.**

## ⚙️ Our First Simple Implementation

Before LangGraph, imagine our agent as this:

```
def agent(question):
    decision = llm_decide(question)

    if decision == "rag":
        result = search_documents(question)
    elif decision == "search":
        result = search_web(question)
    elif decision == "calculate":
        result = calculate(question)
    else:
        result = "I don't know how to answer this."

    return generate_answer(question, result)
```

This isn't our final agent -- it's just the simplest mental model: `Question → Decision → Tool → Result → Answer`.

## 🚀 But Our Final Agent Will Be More Powerful

Eventually:

```
while not finished:
    decision = agent(state)

    if decision.requires_tool:
        result = execute_tool(decision.tool)
        state = update_state(state, result)
    else:
        return decision.answer
```

```
              ┌──────────────┐
              │    Agent     │
              └──────┬───────┘
                     ↓
                  Decision
                     ↓
                Tool needed?
                /          \\
              Yes           No
               ↓             ↓
             Tool          Answer
               ↓
            Result
               ↓
             State
               ↓
             Agent
```

That's the core architecture we'll build.

## 🎯 Project Milestones

We'll complete the project through small project lessons:

- **Part 1 -- Agent Foundation**: define state, define agent, connect LLM.
- **Part 2 -- Tools**: create tools, tool schemas, function calling, tool execution.
- **Part 3 -- Agent Loop**: decision, action, observation, loop, stop conditions.
- **Part 4 -- RAG Tool**: connect your existing RAG knowledge, retrieval tool, reranking, context generation.
- **Part 5 -- Planning**: multi-step tasks, task decomposition, planning state.
- **Part 6 -- Memory**: short-term memory, long-term memory, when memory should be used.
- **Part 7 -- Safety**: tool permissions, human approval, risk checks, guardrails.
- **Part 8 -- Production**: FastAPI, logging, error handling, observability, evaluation.
- **Part 9 -- Final Agent**:

```
User → Agent → Plan → Tools → RAG → Memory → Verification → Human approval when needed → Final answer
```

*The single idea to keep: the agent is a decision-making controller that uses tools and state to accomplish a goal -- not simply an LLM that generates text -- and we build it the way an engineer would: define the problem, define the agent's responsibility, define state, define tools, define the loop, implement, test, evaluate.*
""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Project Exercise — Part 1: Design the Agent",
                    "description": (
                        "Imagine the user asks: \"Compare two AI technologies and recommend which one I should use for my project.\" "
                        "Answer these five design questions: (1) What is the agent's main goal? "
                        "(2) What tools should our agent have (name at least 3, with a one-line purpose each)? "
                        "(3) What information should be stored in the agent state (sketch a state dict)? "
                        "(4) Give one example where the agent needs multiple tool calls, showing the sequence. "
                        "(5) What should cause the agent to stop -- when do we know the task is complete?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-agents", "capstone", "system-design"],
                },
                {
                    "title": "Implement the First Simple Agent Dispatcher",
                    "description": (
                        "Implement the simplest mental-model version of the project agent from the lesson: `agent(question, llm_decide, "
                        "search_documents, search_web, calculate, generate_answer)`. It should call llm_decide(question) to get one of "
                        "\"rag\", \"search\", \"calculate\", or anything else; dispatch to the matching function to get a result (or a "
                        "fallback message for an unrecognized decision); and finally call generate_answer(question, result) and return "
                        "its output -- matching the Question → Decision → Tool → Result → Answer flow from the lesson."
                    ),
                    "starter_code": (
                        "def agent(question, llm_decide, search_documents, search_web, calculate, generate_answer):\n"
                        "    # TODO: get decision = llm_decide(question)\n"
                        "    # TODO: dispatch to the right function based on decision (\"rag\" -> search_documents,\n"
                        "    # \"search\" -> search_web, \"calculate\" -> calculate), or a fallback string otherwise\n"
                        "    # TODO: return generate_answer(question, result)\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def agent(question, llm_decide, search_documents, search_web, calculate, generate_answer):\n"
                        "    decision = llm_decide(question)\n\n"
                        "    if decision == \"rag\":\n"
                        "        result = search_documents(question)\n"
                        "    elif decision == \"search\":\n"
                        "        result = search_web(question)\n"
                        "    elif decision == \"calculate\":\n"
                        "        result = calculate(question)\n"
                        "    else:\n"
                        "        result = \"I don't know how to answer this.\"\n\n"
                        "    return generate_answer(question, result)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-agents", "python", "capstone"],
                },
            ],
            "quiz": {
                "title": "AI Agent Project — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the capstone agent's job, as defined in the lesson?",
                        "options": [
                            "Always retrieve documents for every question regardless of what's actually needed",
                            "Research a user's question using available knowledge and tools, determine what information is required, perform the necessary actions, and produce an evidence-based answer",
                            "Only perform mathematical calculations",
                            "Replace the need for any RAG system entirely",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly defines the agent's responsibility this way, emphasizing that it decides what's needed rather than following one fixed pipeline.",
                    },
                    {
                        "question": "How does the project's agent differ from a normal fixed RAG pipeline (Question → Retrieve → Generate → Answer)?",
                        "options": [
                            "It doesn't differ -- they are identical architectures",
                            "The agent dynamically decides whether it needs documents, current web information, or calculations, rather than always retrieving the same way",
                            "The agent never uses retrieval at all",
                            "The agent always skips retrieval in favor of web search",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's key point: the agent decides which capabilities (RAG, web search, calculator) it needs per question, instead of running one predefined retrieval strategy every time.",
                    },
                    {
                        "question": "According to the lesson, why do we understand the architecture before using LangGraph abstractions?",
                        "options": [
                            "Because LangGraph cannot implement agent loops",
                            "Because the goal is to understand why the graph exists (state, nodes, transitions, loops) rather than just memorizing LangGraph APIs",
                            "Because LangGraph will not be used anywhere in the project",
                            "Because understanding architecture is unrelated to using frameworks",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly states the rule: understand the architecture first, then use LangGraph as an implementation tool -- not the other way around.",
                    },
                    {
                        "question": "In the project's simplest mental-model implementation (the agent() function with 'rag'/'search'/'calculate' branches), what determines which branch runs?",
                        "options": [
                            "A random selection each time",
                            "A decision produced by llm_decide(question), which the application then dispatches on",
                            "The order the functions are defined in the file",
                            "The length of the user's question in characters",
                        ],
                        "correct": 1,
                        "explanation": "The simplified agent() function calls llm_decide(question) to get a decision, then dispatches to search_documents, search_web, or calculate accordingly -- mirroring the LLM proposes / application executes principle from earlier lessons.",
                    },
                    {
                        "question": "Per the lesson's key takeaway, what is 'the agent' fundamentally, as opposed to just an LLM?",
                        "options": [
                            "Simply a larger prompt with more context",
                            "A decision-making controller that uses tools and state to accomplish a goal -- not just an LLM that generates text",
                            "A wrapper that exists purely to call a vector database",
                            "An LLM with no additional structure around it",
                        ],
                        "correct": 1,
                        "explanation": "The lesson closes on this framing: the agent is the whole controller system (LLM + tools + state + loop), not simply the language model generating text.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": "AI Research & RAG Agent",
                "description": (
                    "Build a tool-using agent that receives a complex question, dynamically decides what it needs (document "
                    "retrieval, web search, and/or calculation), executes the necessary tools through an agent loop, reasons over "
                    "the observed results, and produces an evidence-based final answer -- e.g. \"Compare Qdrant and FAISS for a "
                    "production RAG application. Use my documentation and calculate which option makes more sense for my "
                    "requirements.\" The project is completed incrementally across the milestones below, applying every concept "
                    "from this level (state, tools, function calling, agent loop, planning, RAG, tool selection, memory, human "
                    "approval) instead of learning them in isolation."
                ),
                "difficulty": DifficultyLevel.advanced,
                "tech_stack": ["Python", "LLM API", "LangGraph", "Qdrant", "Sentence Transformers", "FastAPI"],
                "objectives": [
                    "Part 1 -- Agent Foundation: define state, define the agent's responsibility, connect the LLM",
                    "Part 2 -- Tools: create tools, tool schemas, function calling, tool execution",
                    "Part 3 -- Agent Loop: decision, action, observation, loop, stop conditions",
                    "Part 4 -- RAG Tool: retrieval tool, reranking, context generation using existing RAG knowledge",
                    "Part 5 -- Planning: multi-step tasks, task decomposition, planning state",
                    "Part 6 -- Memory: short-term memory, long-term memory, when memory should be used",
                    "Part 7 -- Safety: tool permissions, human approval, risk checks, guardrails",
                    "Part 8 -- Production: FastAPI, logging, error handling, observability, evaluation",
                    "Part 9 -- Final Agent: integrate plan, tools, RAG, memory, verification, and human approval into one system",
                ],
                "rubric": {
                    "agent_architecture": "Agent correctly separates state, decision-making, tool execution, and stopping conditions",
                    "dynamic_tool_use": "Agent selects RAG, web search, and/or calculation based on the actual question rather than a fixed pipeline",
                    "rag_integration": "Retrieval tool correctly applies embeddings, vector search, and reranking from prior levels",
                    "safety": "Sensitive or irreversible actions are gated behind explicit permission/approval checks, not left to the LLM alone",
                    "production_readiness": "FastAPI service includes logging, error handling, and basic observability",
                },
                "starter_repo_url": None,
                "estimated_hours": 20.0,
            },
        },
    ],
}
