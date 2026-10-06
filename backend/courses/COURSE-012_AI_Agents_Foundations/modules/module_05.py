"""M01.L05 — Agent Reasoning and Planning.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 5, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how AI agents decompose problems, plan over multiple steps, use "
    "reason-act-observe loops, explore alternatives, critique their own work, "
    "and use external scratchpads such as the Sequential Thinking MCP server "
    "to maintain continuity across complex tasks."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Agent Reasoning and Planning",

    "slug": "ai-agents-m01-l05",

    "description": (
        "Understand the reasoning and planning structures behind capable agents, "
        "from decomposition and linear reasoning to ReAct, explicit planning, "
        "Tree-of-Thought, Reflexion, and Sequential Thinking through MCP."
    ),

    "order": 5,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.75,

    "skill_tags": [
        "agent-reasoning",
        "planning",
        "decomposition",
        "chain-of-thought",
        "react",
        "tree-of-thought",
        "reflexion",
        "sequential-thinking",
        "mcp",
        "agent-evaluation",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Agent Reasoning and Planning",

        "content": (
            "# Agent Reasoning and Planning\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L05  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 5. "
            "The supplied chapter did not include a page range. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Distinguish **decomposition** from **planning**.\n"
            "- Explain why both decomposition and planning can fail independently.\n"
            "- Describe the practical difference between ordinary generation and reasoning-oriented execution.\n"
            "- Explain the purpose and trade-offs of Chain-of-Thought-style reasoning prompts.\n"
            "- Explain the ReAct loop: reason, act, observe, repeat.\n"
            "- Distinguish reactive execution from explicit long-horizon planning.\n"
            "- Store and update plans outside the model so agents can use them across steps.\n"
            "- Identify when a simple agent does not need an explicit reasoning pattern.\n"
            "- Explain Tree-of-Thought as search over multiple candidate reasoning paths.\n"
            "- Explain Reflexion as critique-driven iterative improvement.\n"
            "- Select an appropriate reasoning strategy based on the task and cost constraints.\n"
            "- Explain the purpose of the Sequential Thinking MCP server.\n"
            "- Combine planning, tool use, evaluation, and revision without creating unbounded loops.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Decomposition and planning are different skills\n"
            "\n"
            "The chapter begins with a distinction that is easy to miss but extremely important.\n"
            "\n"
            "### Decomposition asks: What are the pieces?\n"
            "\n"
            "Decomposition means breaking a large task into smaller subproblems.\n"
            "\n"
            "Example goal:\n"
            "\n"
            "```text\n"
            "Prepare a market research report.\n"
            "```\n"
            "\n"
            "Possible decomposition:\n"
            "\n"
            "```text\n"
            "1. Define the market.\n"
            "2. Find competitors.\n"
            "3. Gather pricing data.\n"
            "4. Analyze trends.\n"
            "5. Write conclusions.\n"
            "```\n"
            "\n"
            "### Planning asks: In what order, with which dependencies, and using what approach?\n"
            "\n"
            "Planning takes those pieces and decides how they should be executed.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Define market first.\n"
            "Then research competitors and pricing in parallel.\n"
            "Analyze trends only after evidence is collected.\n"
            "Write conclusions after analysis is complete.\n"
            "```\n"
            "\n"
            "The two operations can fail independently.\n"
            "\n"
            "- A good decomposition can still be followed by a bad plan.\n"
            "- A well-ordered plan can still fail if the original decomposition missed a critical subtask.\n"
            "\n"
            "This matters because the fix depends on what failed.\n"
            "\n"
            "[[IMAGE_NEEDED: Decomposition versus planning | "
            "Left: one large goal breaking into several subproblems. Right: the same subproblems "
            "connected by arrows showing order, dependencies, and parallel branches | "
            "Learner should notice that decomposition defines the pieces while planning defines "
            "how the pieces fit together]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Reasoning in language models\n"
            "\n"
            "A language model generates output token by token. For simple tasks, that is often enough.\n"
            "\n"
            "For harder multistep tasks, however, a model may jump too quickly to a plausible answer "
            "without adequately working through dependencies.\n"
            "\n"
            "The chapter distinguishes two broad behaviors:\n"
            "\n"
            "### General-purpose generation\n"
            "\n"
            "A model may answer directly without a dedicated deliberation phase.\n"
            "\n"
            "This is fast and inexpensive, which is ideal for:\n"
            "\n"
            "- simple lookups,\n"
            "- short transformations,\n"
            "- fixed-format responses,\n"
            "- tasks with little ambiguity.\n"
            "\n"
            "### Reasoning-oriented execution\n"
            "\n"
            "Reasoning-capable systems allocate additional compute or structured steps before the "
            "final answer. This can improve performance on hard multistep tasks, but it usually "
            "increases latency and token usage.\n"
            "\n"
            "The practical question is not simply:\n"
            "\n"
            "```text\n"
            "\"Does this model reason?\"\n"
            "```\n"
            "\n"
            "A better engineering question is:\n"
            "\n"
            "```text\n"
            "\"Does the additional reasoning improve the tasks I care about enough to justify its cost?\"\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Chain-of-Thought-style reasoning\n"
            "\n"
            "Chain-of-Thought (CoT) is a linear reasoning strategy. The model is encouraged to "
            "work through a problem in intermediate stages before committing to the final result.\n"
            "\n"
            "In production systems, you usually do **not** need to expose private internal reasoning "
            "to the user. The useful engineering idea is the **structured decomposition**, not the "
            "publication of hidden model thoughts.\n"
            "\n"
            "A safe and practical prompting style is:\n"
            "\n"
            "```text\n"
            "Analyze the problem carefully.\n"
            "Use the following checkpoints:\n"
            "1. Identify the known values.\n"
            "2. Identify the unknown value.\n"
            "3. Apply the relevant transformations in order.\n"
            "4. Verify the final result.\n"
            "Return a concise answer with the important calculation steps.\n"
            "```\n"
            "\n"
            "### Why CoT-style structure helps\n"
            "\n"
            "It reduces the chance that the model skips a necessary intermediate step.\n"
            "\n"
            "### Main trade-offs\n"
            "\n"
            "- more tokens,\n"
            "- more latency,\n"
            "- longer outputs if not constrained,\n"
            "- still probabilistic,\n"
            "- cannot compensate for a fundamentally weak model on every task.\n"
            "\n"
            "The lesson is not \"always ask for more reasoning.\" The lesson is to use structured "
            "reasoning when the task actually contains multiple dependent steps.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. ReAct: reason, act, observe, repeat\n"
            "\n"
            "CoT stays mainly inside one reasoning pass. ReAct adds interaction with the outside world.\n"
            "\n"
            "The pattern is:\n"
            "\n"
            "```text\n"
            "Reason -> Act -> Observe -> Reason -> Act -> Observe -> ...\n"
            "```\n"
            "\n"
            "### Reason\n"
            "\n"
            "The agent decides what information or action is needed next.\n"
            "\n"
            "### Act\n"
            "\n"
            "The agent calls a tool, API, database, MCP server, or another capability.\n"
            "\n"
            "### Observe\n"
            "\n"
            "The agent receives the result and uses it to decide what happens next.\n"
            "\n"
            "The feedback loop is what makes ReAct different from a one-shot response that happens "
            "to contain one tool call.\n"
            "\n"
            "A true ReAct loop lets observations modify later decisions.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. ReAct example with tools\n"
            "\n"
            "The chapter uses simple time-travel arithmetic to demonstrate tool-assisted reasoning.\n"
            "\n"
            "A similar agent can expose deterministic tools:\n"
            "\n"
            "```python\n"
            "from agents import Agent, Runner, function_tool\n"
            "\n"
            "@function_tool\n"
            "def travel_back(year: int, years: int) -> int:\n"
            "    \"\"\"Move backward by a number of years.\"\"\"\n"
            "    return year - years\n"
            "\n"
            "@function_tool\n"
            "def travel_forward(year: int, years: int) -> int:\n"
            "    \"\"\"Move forward by a number of years.\"\"\"\n"
            "    return year + years\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"TimeTravelerReAct\",\n"
            "    instructions=(\n"
            "        \"Solve the time-travel problem carefully. \"\n"
            "        \"Use the available tools for year calculations. \"\n"
            "        \"After each tool result, decide whether another action is needed. \"\n"
            "        \"Return the final year and a concise summary.\"\n"
            "    ),\n"
            "    tools=[travel_back, travel_forward],\n"
            ")\n"
            "```\n"
            "\n"
            "The tools make the arithmetic deterministic while the LLM decides **which tool to call and when**.\n"
            "\n"
            "This split is useful:\n"
            "\n"
            "```text\n"
            "LLM        -> chooses the operation\n"
            "Tool       -> performs the exact calculation\n"
            "Observation-> informs the next decision\n"
            "```\n"
            "\n"
            "{{exercise:M01.L05.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Planning goes beyond one reasoning loop\n"
            "\n"
            "ReAct is reactive: it decides the next action using the latest observation.\n"
            "\n"
            "Long-horizon planning introduces a **global plan** that coordinates several steps or "
            "several ReAct loops toward a larger objective.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Goal: Build a three-day travel itinerary.\n"
            "\n"
            "Plan:\n"
            "Day 1 -> activity A\n"
            "Day 2 -> activity B\n"
            "Day 3 -> activity C\n"
            "```\n"
            "\n"
            "If new information appears, the plan can be revised.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Observation: Activity A is unavailable.\n"
            "Updated plan: Replace Activity A while preserving the other constraints.\n"
            "```\n"
            "\n"
            "This shows an important architectural idea:\n"
            "\n"
            "> A plan should exist somewhere outside a single model call if the agent needs to revisit it later.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Plans need external state\n"
            "\n"
            "An LLM call does not magically preserve a durable internal world model between calls.\n"
            "\n"
            "If an agent needs a global plan over many steps, the architecture must store information such as:\n"
            "\n"
            "- subtasks,\n"
            "- task status,\n"
            "- dependencies,\n"
            "- intermediate results,\n"
            "- revisions,\n"
            "- remaining work.\n"
            "\n"
            "Possible storage locations include:\n"
            "\n"
            "- conversation context,\n"
            "- a scratchpad,\n"
            "- application state,\n"
            "- a database,\n"
            "- memory storage,\n"
            "- a planning MCP server.\n"
            "\n"
            "A simple plan object might look like:\n"
            "\n"
            "```python\n"
            "plan = {\n"
            "    \"goal\": \"research a topic\",\n"
            "    \"steps\": [\n"
            "        {\"id\": 1, \"task\": \"find sources\", \"status\": \"done\"},\n"
            "        {\"id\": 2, \"task\": \"compare evidence\", \"status\": \"in_progress\"},\n"
            "        {\"id\": 3, \"task\": \"write summary\", \"status\": \"pending\"},\n"
            "    ],\n"
            "}\n"
            "```\n"
            "\n"
            "The model can then read the current state on each step rather than trying to reconstruct "
            "the entire strategy from scratch.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Not every agent needs a reasoning framework\n"
            "\n"
            "The chapter explicitly warns against overengineering simple tasks.\n"
            "\n"
            "A straightforward agent that performs one small operation often does **not** benefit "
            "from CoT, ReAct, ToT, or Reflexion.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- look up a value,\n"
            "- call one tool,\n"
            "- reformat a document,\n"
            "- classify a simple input,\n"
            "- produce a fixed schema from obvious data.\n"
            "\n"
            "Reasoning patterns earn their cost when there is:\n"
            "\n"
            "- more than one meaningful decision,\n"
            "- dependence on intermediate results,\n"
            "- uncertainty,\n"
            "- branching,\n"
            "- revision,\n"
            "- enough difficulty that direct generation is unreliable.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Tree-of-Thought: search across alternatives\n"
            "\n"
            "Chain-of-Thought follows one reasoning path. Tree-of-Thought (ToT) explores several.\n"
            "\n"
            "A simplified ToT process is:\n"
            "\n"
            "1. Generate several candidate next steps.\n"
            "2. Expand each candidate.\n"
            "3. Evaluate the resulting branches.\n"
            "4. Prune weak branches.\n"
            "5. Continue expanding promising branches.\n"
            "6. Stop when a satisfactory solution is found or a search limit is reached.\n"
            "\n"
            "```text\n"
            "                  Start\n"
            "               /    |    \\\n"
            "             A      B      C\n"
            "            / \\    / \\    / \\\n"
            "          ... ... ... ... ... ...\n"
            "                ^\n"
            "                |\n"
            "         evaluate + prune\n"
            "```\n"
            "\n"
            "### Best fit\n"
            "\n"
            "ToT is useful when the problem benefits from **lookahead and search**, such as:\n"
            "\n"
            "- planning puzzles,\n"
            "- games,\n"
            "- strategic search,\n"
            "- problems with several plausible paths.\n"
            "\n"
            "### Cost\n"
            "\n"
            "Each branch may require additional model calls, evaluation, and expansion. Token cost "
            "can grow rapidly.\n"
            "\n"
            "### Important implementation detail\n"
            "\n"
            "A complete ToT system generally needs orchestration code. One prompt can ask for several "
            "candidates, but real pruning and backtracking are external control-flow operations.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. A practical ToT architecture\n"
            "\n"
            "The chapter demonstrates ToT using separate generator and evaluator agents.\n"
            "\n"
            "A simplified architecture is:\n"
            "\n"
            "```python\n"
            "generator = Agent(\n"
            "    name=\"ToT-Generator\",\n"
            "    instructions=(\n"
            "        \"Generate one plausible next step toward the goal.\"\n"
            "    ),\n"
            ")\n"
            "\n"
            "evaluator = Agent(\n"
            "    name=\"ToT-Evaluator\",\n"
            "    instructions=(\n"
            "        \"Evaluate the proposed branch from 0 to 10 for likelihood of success.\"\n"
            "    ),\n"
            ")\n"
            "```\n"
            "\n"
            "The external application then:\n"
            "\n"
            "- samples several branches,\n"
            "- asks the evaluator to score them,\n"
            "- keeps only high-scoring paths,\n"
            "- expands those paths again.\n"
            "\n"
            "This is more expensive than a single linear chain but gives the system a way to avoid "
            "committing too early to one bad path.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Reflexion: improve through critique and retry\n"
            "\n"
            "Reflexion uses a different strategy. Instead of exploring many branches, it follows one "
            "path and improves it through repeated feedback.\n"
            "\n"
            "The loop is:\n"
            "\n"
            "```text\n"
            "Attempt -> Evaluate -> Critique -> Retry\n"
            "```\n"
            "\n"
            'A solver creates an answer. A critic identifies a problem and provides feedback. The solver then tries again with that feedback included in its context.\n'
            "\n"
            "### Important clarification\n"
            "\n"
            "The agent is not updating model weights. It is not literally learning in the training sense.\n"
            "\n"
            "The next attempt improves because the input now contains more useful context.\n"
            "\n"
            "### Best fit\n"
            "\n"
            "Reflexion works well when:\n"
            "\n"
            "- the first attempt may be wrong,\n"
            "- the failure is informative,\n"
            "- useful feedback can guide the next attempt,\n"
            "- one path deserves deeper refinement.\n"
            "\n"
            "### ToT versus Reflexion\n"
            "\n"
            "```text\n"
            "ToT       = breadth: explore several paths\n"
            "Reflexion = depth: improve one path over multiple attempts\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Solver-critic architecture\n"
            "\n"
            "A Reflexion-style system can use two agents.\n"
            "\n"
            "```python\n"
            "solver = Agent(\n"
            "    name=\"Solver\",\n"
            "    instructions=\"Solve the problem carefully and return the answer.\",\n"
            ")\n"
            "\n"
            "critic = Agent(\n"
            "    name=\"Critic\",\n"
            "    instructions=(\n"
            "        \"Evaluate the proposed solution. \"\n"
            "        \"If it is wrong, provide one concise actionable hint.\"\n"
            "    ),\n"
            ")\n"
            "```\n"
            "\n"
            "Then the application controls the retry loop:\n"
            "\n"
            "```python\n"
            "feedback = \"\"\n"
            "\n"
            "for attempt in range(MAX_ATTEMPTS):\n"
            "    answer = await run_solver(problem, feedback)\n"
            "\n"
            "    if passes_check(answer):\n"
            "        break\n"
            "\n"
            "    feedback = await run_critic(answer)\n"
            "```\n"
            "\n"
            "The most important production rule is that `MAX_ATTEMPTS` must be bounded.\n"
            "\n"
            "A retry loop without a hard limit can become an expensive failure loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Choosing the right reasoning strategy\n"
            "\n"
            "The chapter summarizes reasoning strategies by use case and cost.\n"
            "\n"
            "| Strategy | Best fit | Relative cost | Avoid when |\n"
            "|---|---|---:|---|\n"
            "| Linear CoT-style reasoning | Logic and multistep inference | Low | Simple factual tasks |\n"
            "| ReAct | Tool-heavy and information-seeking tasks | Medium | No external action or observation is needed |\n"
            "| Tree-of-Thought | Branching search and strategic planning | High | Low-latency or cheap workflows |\n"
            "| Reflexion | Iterative improvement with useful feedback | Medium-high | One-shot trivial tasks |\n"
            "\n"
            "A practical decision process is:\n"
            "\n"
            "```text\n"
            "Is the task simple?\n"
            "  -> Yes: use a direct agent.\n"
            "\n"
            "Does it require multiple internal reasoning steps but no tools?\n"
            "  -> Use linear structured reasoning.\n"
            "\n"
            "Does it need tools and observation-driven adaptation?\n"
            "  -> Use ReAct.\n"
            "\n"
            "Does it require searching several candidate approaches?\n"
            "  -> Consider ToT.\n"
            "\n"
            "Does it benefit from critique and retry?\n"
            "  -> Consider Reflexion.\n"
            "```\n"
            "\n"
            "The more advanced the pattern, the stronger the justification should be.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. The Sequential Thinking MCP server\n"
            "\n"
            "The chapter introduces Anthropic's reference Sequential Thinking MCP server as a "
            "reasoning and planning scratchpad.\n"
            "\n"
            "The key point is easy to misunderstand:\n"
            "\n"
            "> The server itself is not the intelligence doing the reasoning.\n"
            "\n"
            "The agent performs the reasoning. The server provides a structured place to record, "
            "revise, branch, and revisit intermediate reasoning state across steps.\n"
            "\n"
            "That is valuable because a long-horizon agent may need to remember:\n"
            "\n"
            "- what it has already considered,\n"
            "- what assumptions were revised,\n"
            "- which branch it is exploring,\n"
            "- whether more analysis is needed,\n"
            "- how many steps remain.\n"
            "\n"
            "[[IMAGE_NEEDED: Agent with Sequential Thinking scratchpad | "
            "Show Agent/LLM connected to a Sequential Thinking MCP server. The scratchpad contains "
            "Thought 1, Thought 2, revision of Thought 1, branch B, and status metadata. Also show "
            "ordinary action tools beside it | "
            "Learner should notice that the MCP server stores structured reasoning state while the "
            "agent still makes decisions]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Connecting the Sequential Thinking server\n"
            "\n"
            "The source uses a local MCP server launched through `npx`.\n"
            "\n"
            "A simplified setup is:\n"
            "\n"
            "```python\n"
            "from agents import Agent, Runner\n"
            "from agents.mcp import MCPServerStdio\n"
            "\n"
            "thinking_srv = MCPServerStdio(\n"
            "    name=\"sequential-thinking\",\n"
            "    params={\n"
            "        \"command\": \"npx\",\n"
            "        \"args\": [\n"
            "            \"-y\",\n"
            "            \"@modelcontextprotocol/server-sequential-thinking\",\n"
            "        ],\n"
            "    },\n"
            ")\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Planning Assistant\",\n"
            "    instructions=\"Use the thinking server for complex planning tasks.\",\n"
            "    mcp_servers=[thinking_srv],\n"
            ")\n"
            "```\n"
            "\n"
            "You can inspect the server's available tools before using it:\n"
            "\n"
            "```python\n"
            "async with thinking_srv:\n"
            "    tools = await thinking_srv.list_tools()\n"
            "    print(tools)\n"
            "```\n"
            "\n"
            "This is the same MCP principle learned earlier: the agent discovers a structured external "
            "capability rather than depending on its implementation details.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. What the Sequential Thinking scratchpad tracks\n"
            "\n"
            "The chapter describes metadata that lets the scratchpad represent a flexible reasoning process.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- current thought text,\n"
            "- thought number,\n"
            "- estimated total thoughts,\n"
            "- whether another thought is needed,\n"
            "- whether the current thought revises an earlier one,\n"
            "- which earlier thought is being revised,\n"
            "- a branch point,\n"
            "- a branch identifier.\n"
            "\n"
            "Conceptually, this supports operations such as:\n"
            "\n"
            "```text\n"
            "Record thought\n"
            "Revise thought\n"
            "Branch from thought\n"
            "Increase/decrease expected steps\n"
            "Mark analysis complete\n"
            "```\n"
            "\n"
            "The scratchpad therefore supports more than a purely linear chain.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Combining Sequential Thinking with ReAct\n"
            "\n"
            "The chapter combines the scratchpad with action tools.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "1. Agent records a planning step in Sequential Thinking.\n"
            "2. Agent calls travel_back(...).\n"
            "3. Agent observes the result.\n"
            "4. Agent records a new or revised planning step.\n"
            "5. Agent calls travel_forward(...).\n"
            "6. Agent observes again.\n"
            "7. Agent finishes when the goal is satisfied.\n"
            "```\n"
            "\n"
            "This creates a practical combination:\n"
            "\n"
            "```text\n"
            "Sequential Thinking = external scratchpad\n"
            "ReAct              = action/observation control loop\n"
            "Tools              = deterministic or external capabilities\n"
            "```\n"
            "\n"
            "Tracing is especially useful here because the final answer alone may hide how many "
            "reasoning and tool calls occurred.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Combining multiple reasoning patterns\n"
            "\n"
            "For difficult tasks, the chapter demonstrates combining several strategies.\n"
            "\n"
            "A conceptual architecture is:\n"
            "\n"
            "```text\n"
            "Structured reasoning -> create initial plan\n"
            "ReAct               -> execute actions and observe\n"
            "ToT                 -> explore alternative branches when needed\n"
            "Reflexion           -> critique failed attempts and retry\n"
            "```\n"
            "\n"
            "This can improve robustness on difficult problems, but the cost can become very high.\n"
            "\n"
            "Every added strategy may introduce:\n"
            "\n"
            "- more model calls,\n"
            "- more tool calls,\n"
            "- more context,\n"
            "- more evaluation,\n"
            "- more latency,\n"
            "- more failure paths.\n"
            "\n"
            "Therefore, complex reasoning stacks should be reserved for tasks where their extra "
            "reliability is worth the expense.\n"
            "\n"
            "{{exercise:M01.L05.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Reasoning outputs still need validation\n"
            "\n"
            "A long reasoning process does not guarantee a correct answer.\n"
            "\n"
            "The chapter demonstrates this by combining reasoning patterns with explicit checks.\n"
            "\n"
            "A useful production pattern is:\n"
            "\n"
            "```text\n"
            "Reason / Plan\n"
            "    |\n"
            "    v\n"
            "Execute\n"
            "    |\n"
            "    v\n"
            "Validate\n"
            "    |\n"
            "    +--> pass -> finish\n"
            "    |\n"
            "    +--> fail -> revise (bounded)\n"
            "```\n"
            "\n"
            "Validation may come from:\n"
            "\n"
            "- deterministic checks,\n"
            "- typed schemas,\n"
            "- tests,\n"
            "- a judge or critic,\n"
            "- domain-specific constraints,\n"
            "- tool-based verification.\n"
            "\n"
            "This connects Chapter 5 back to Chapter 4: reasoning improves decisions, while guardrails "
            "and validation keep those decisions from cascading into uncontrolled failures.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Practical reasoning and planning playbook\n"
            "\n"
            "Use this sequence when designing a reasoning agent.\n"
            "\n"
            "### Step 1 — Determine whether reasoning is actually needed\n"
            "\n"
            "Do not add a complex pattern to a one-step task.\n"
            "\n"
            "### Step 2 — Separate decomposition from planning\n"
            "\n"
            "Check both independently.\n"
            "\n"
            "### Step 3 — Use tools for deterministic work\n"
            "\n"
            "Let code perform exact calculations or retrieval where possible.\n"
            "\n"
            "### Step 4 — Use ReAct when observations should change the next action\n"
            "\n"
            "This is the default structure for many production agents.\n"
            "\n"
            "### Step 5 — Store global plans outside one model call\n"
            "\n"
            "Use application state, memory, or a scratchpad.\n"
            "\n"
            "### Step 6 — Add search only when one path is not enough\n"
            "\n"
            "Use ToT selectively.\n"
            "\n"
            "### Step 7 — Add critique when feedback can improve the next attempt\n"
            "\n"
            "Use Reflexion-style loops with hard attempt limits.\n"
            "\n"
            "### Step 8 — Trace tool and planning behavior\n"
            "\n"
            "Do not rely only on the final response when debugging.\n"
            "\n"
            "### Step 9 — Validate outputs\n"
            "\n"
            "Reasoning length is not proof of correctness.\n"
            "\n"
            "### Step 10 — Optimize cost after correctness\n"
            "\n"
            "Once the workflow works, reduce unnecessary reasoning, tools, branches, and retries.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Decomposition and planning are the same\n"
            "\n"
            "> Decomposition defines the pieces; planning defines the execution structure.\n"
            "\n"
            "Either can be wrong even when the other is correct.\n"
            "\n"
            "### Misconception 2: More visible reasoning always means more intelligence\n"
            "\n"
            "> Extra steps can help difficult tasks but also add noise, latency, and cost.\n"
            "\n"
            "The relevant measure is whether task performance improves.\n"
            "\n"
            "### Misconception 3: A tool call makes a workflow ReAct\n"
            "\n"
            "> ReAct requires an observation-feedback loop that influences later decisions.\n"
            "\n"
            "One isolated tool call is not enough.\n"
            "\n"
            "### Misconception 4: Tree-of-Thought is just a long prompt\n"
            "\n"
            "> Real ToT requires branch generation, evaluation, pruning, and control flow.\n"
            "\n"
            "External orchestration is normally required.\n"
            "\n"
            "### Misconception 5: Reflexion updates the model\n"
            "\n"
            "> The model weights do not change.\n"
            "\n"
            "Improvement comes from feeding critique back into the next attempt.\n"
            "\n"
            "### Misconception 6: Sequential Thinking performs the reasoning for the agent\n"
            "\n"
            "> It is primarily a structured scratchpad and thought-state tracker.\n"
            "\n"
            "The agent remains the decision-making component.\n"
            "\n"
            "### Misconception 7: More advanced reasoning patterns should be combined by default\n"
            "\n"
            "> Combining CoT, ReAct, ToT, and Reflexion can be extremely expensive.\n"
            "\n"
            "Use only the complexity justified by the task.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Decomposition | Breaking a large goal into smaller subproblems |\n"
            "| Planning | Choosing order, dependencies, resources, and strategy for solving subproblems |\n"
            "| CoT | Linear structured reasoning across intermediate steps |\n"
            "| ReAct | Loop that interleaves reasoning, action, and observation |\n"
            "| Observation | Information returned after an action/tool call |\n"
            "| Long-horizon plan | Global strategy coordinating multiple steps toward a larger goal |\n"
            "| Scratchpad | External place to store intermediate reasoning or planning state |\n"
            "| Tree-of-Thought | Search procedure that explores, evaluates, and prunes multiple reasoning branches |\n"
            "| Reflexion | Iterative solver-critic pattern that retries using critique as new context |\n"
            "| Critic | Component that evaluates a candidate result and returns feedback |\n"
            "| Sequential Thinking | MCP scratchpad/server for structured thought-state tracking |\n"
            "| Branch | Alternative reasoning path explored during search |\n"
            "| Pruning | Removing low-value branches from further exploration |\n"
            "| Bounded retry | Retry loop with a fixed maximum number of attempts |\n"
            "| Validation | Checking whether reasoning output satisfies deterministic or semantic requirements |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. How is decomposition different from planning?\n"
            "2. Why can the two fail independently?\n"
            "3. When is direct generation preferable to an explicit reasoning pattern?\n"
            "4. What problem does linear structured reasoning solve?\n"
            "5. What makes ReAct a loop rather than a one-shot tool call?\n"
            "6. Why should a long-horizon plan be stored outside one model call?\n"
            "7. When is Tree-of-Thought worth its cost?\n"
            "8. What does pruning mean in ToT?\n"
            "9. How is Reflexion different from ToT?\n"
            "10. Why does Reflexion not count as model training?\n"
            "11. What kinds of tasks fit ReAct best?\n"
            "12. What does the Sequential Thinking MCP server actually provide?\n"
            "13. Why is tracing useful when using Sequential Thinking plus tools?\n"
            "14. Why should retries always be bounded?\n"
            "15. Why must reasoning outputs still be validated?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Reasoning agents become reliable when the architecture separates four things: "
            "decompose the goal, plan the work, act through tools, and validate observations. "
            "Use the simplest reasoning pattern that solves the problem, store long-lived plans "
            "outside a single model call, and add branching or critique only when the task earns "
            "the extra cost.**\n"
        ),

        "estimated_minutes": 225,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "decomposition-vs-planning", "title": "Decomposition and planning are different skills", "order": 1},
            {"id": "reasoning-models", "title": "Reasoning in language models", "order": 2},
            {"id": "cot", "title": "Chain-of-Thought-style reasoning", "order": 3},
            {"id": "react", "title": "ReAct: reason, act, observe, repeat", "order": 4},
            {"id": "react-example", "title": "ReAct example with tools", "order": 5},
            {"id": "planning", "title": "Planning goes beyond one reasoning loop", "order": 6},
            {"id": "external-plan-state", "title": "Plans need external state", "order": 7},
            {"id": "simple-vs-advanced", "title": "Not every agent needs a reasoning framework", "order": 8},
            {"id": "tree-of-thought", "title": "Tree-of-Thought: search across alternatives", "order": 9},
            {"id": "tot-example", "title": "A practical ToT architecture", "order": 10},
            {"id": "reflexion", "title": "Reflexion: improve through critique and retry", "order": 11},
            {"id": "reflexion-example", "title": "Solver-critic architecture", "order": 12},
            {"id": "strategy-selection", "title": "Choosing the right reasoning strategy", "order": 13},
            {"id": "sequential-thinking", "title": "The Sequential Thinking MCP server", "order": 14},
            {"id": "st-setup", "title": "Connecting the Sequential Thinking server", "order": 15},
            {"id": "st-capabilities", "title": "What the Sequential Thinking scratchpad tracks", "order": 16},
            {"id": "st-react", "title": "Combining Sequential Thinking with ReAct", "order": 17},
            {"id": "advanced-combination", "title": "Combining multiple reasoning patterns", "order": 18},
            {"id": "reasoning-validation", "title": "Reasoning outputs still need validation", "order": 19},
            {"id": "planning-playbook", "title": "Practical reasoning and planning playbook", "order": 20},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L05.EX01",

            "title": "Turn a Linear Solver into a ReAct Agent",

            "lesson_code": "M01.L05",

            "section_id": "react-example",

            "placement": "after_section",

            "description": (
                "Practice converting a direct reasoning agent into an agent that "
                "uses deterministic tools and observations."
            ),

            "instructions": (
                "Create a small time-travel agent.\n"
                "1. Start with year 2050.\n"
                "2. The goal requires going 25 years backward, 10 years forward, then 5 years backward.\n"
                "3. Implement `travel_back(year, years)` and `travel_forward(year, years)` as tools.\n"
                "4. Instruct the agent to use tools for all year arithmetic.\n"
                "5. After each tool result, require the agent to decide whether another action is needed.\n"
                "6. Trace the execution and record the sequence of tool calls.\n"
                "7. Explain why this is ReAct rather than a single CoT-style pass.\n"
                "8. Identify one calculation that should remain deterministic rather than be delegated to the LLM."
            ),

            "expected_output": (
                "A working or carefully written ReAct agent example, the tool-call "
                "sequence, final year, and a short explanation of how observations "
                "affected later actions."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "react",
                "tool-use",
                "observation-loop",
                "deterministic-tools",
                "tracing",
            ],
        },

        {
            "id": "M01.L05.EX02",

            "title": "Design a Bounded Reasoning System for a Difficult Goal",

            "lesson_code": "M01.L05",

            "section_id": "advanced-combination",

            "placement": "after_section",

            "description": (
                "Choose and combine reasoning strategies only where they add value, "
                "while keeping the workflow bounded and observable."
            ),

            "instructions": (
                "Scenario: An agent must create a robust migration plan for a legacy service.\n"
                "The system has incomplete documentation, several possible migration paths, "
                "and a hard rule that production downtime must stay below a fixed threshold.\n"
                "1. Write the decomposition of the goal into 4-6 subproblems.\n"
                "2. Create a high-level plan and identify which steps depend on earlier steps.\n"
                "3. Mark which steps require ReAct tool calls.\n"
                "4. Identify one point where exploring 2-3 alternative branches with ToT could help.\n"
                "5. Identify one point where a critic/Reflexion loop could improve an output.\n"
                "6. Set a hard maximum for branch count and retry count.\n"
                "7. Put the downtime requirement in deterministic validation code rather than an LLM prompt alone.\n"
                "8. Describe what state should be kept in a scratchpad or plan store.\n"
                "9. Explain which traces you would inspect during debugging.\n"
                "10. Remove one reasoning pattern if you decide its extra cost is not justified, and explain why."
            ),

            "expected_output": (
                "A compact architecture showing decomposition, plan state, ReAct actions, "
                "optional ToT exploration, bounded Reflexion, deterministic validation, "
                "and observability."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "decomposition",
                "planning",
                "react",
                "tree-of-thought",
                "reflexion",
                "bounded-execution",
                "validation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L05.QZ01",

        "title": "Agent Reasoning and Planning — Knowledge Check",

        "lesson_code": "M01.L05",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",

                "section_id": "decomposition-vs-planning",

                "question": "What is the main difference between decomposition and planning?",

                "options": [
                    "Decomposition chooses tools while planning writes prompts",
                    "Decomposition identifies subproblems; planning decides order, dependencies, and approach",
                    "Planning happens before decomposition in every system",
                    "They are two names for the same operation",
                ],

                "correct": 1,

                "explanation": (
                    "Decomposition defines the pieces of the task. Planning decides how "
                    "those pieces should be executed and connected."
                ),
            },

            {
                "id": "M01.L05.Q02",

                "section_id": "reasoning-models",

                "question": "When is additional reasoning compute most justified?",

                "options": [
                    "Every simple lookup",
                    "When a harder multistep task gains enough quality to justify extra latency and cost",
                    "Whenever the answer must be one word",
                    "Only when no tools exist",
                ],

                "correct": 1,

                "explanation": (
                    "Reasoning is an engineering trade-off. The useful question is whether "
                    "the performance gain is worth the extra cost."
                ),
            },

            {
                "id": "M01.L05.Q03",

                "section_id": "cot",

                "question": "What is the main purpose of linear structured reasoning?",

                "options": [
                    "To eliminate probabilistic behavior",
                    "To encourage the model to process dependent intermediate steps before the final answer",
                    "To replace all tools",
                    "To make every task slower",
                ],

                "correct": 1,

                "explanation": (
                    "Structured intermediate checkpoints reduce the chance that the model "
                    "skips important multistep dependencies."
                ),
            },

            {
                "id": "M01.L05.Q04",

                "section_id": "react",

                "question": "What makes ReAct fundamentally different from a one-shot answer with a tool call?",

                "options": [
                    "ReAct always uses exactly two tools",
                    "Tool observations feed back into later reasoning and actions",
                    "ReAct cannot use plans",
                    "ReAct never terminates",
                ],

                "correct": 1,

                "explanation": (
                    "The observation-feedback loop is the defining feature."
                ),
            },

            {
                "id": "M01.L05.Q05",

                "section_id": "external-plan-state",

                "question": "Why should a long-horizon plan usually exist outside a single model call?",

                "options": [
                    "Because models cannot read structured data",
                    "So later steps can reread task status, dependencies, results, and revisions",
                    "Because plans cannot contain text",
                    "So the model never has to use tools",
                ],

                "correct": 1,

                "explanation": (
                    "Long-running agents need explicit state that can be revisited across calls."
                ),
            },

            {
                "id": "M01.L05.Q06",

                "section_id": "simple-vs-advanced",

                "question": "Which task least needs an advanced reasoning pattern?",

                "options": [
                    "Choosing among several uncertain migration strategies",
                    "Running one deterministic lookup and returning its value",
                    "Debugging a difficult program through several attempts",
                    "Researching a topic using several external sources",
                ],

                "correct": 1,

                "explanation": (
                    "A one-step deterministic lookup does not benefit much from complex reasoning scaffolding."
                ),
            },

            {
                "id": "M01.L05.Q07",

                "section_id": "tree-of-thought",

                "question": "What operation is essential to a real Tree-of-Thought system?",

                "options": [
                    "Only generating one very long answer",
                    "Branching into alternatives and evaluating/pruning them",
                    "Disabling tools",
                    "Removing all external orchestration",
                ],

                "correct": 1,

                "explanation": (
                    "ToT is a search procedure across candidate branches, not merely a longer chain."
                ),
            },

            {
                "id": "M01.L05.Q08",

                "section_id": "reflexion",

                "question": "How does Reflexion improve a later attempt?",

                "options": [
                    "By updating the model's weights after every answer",
                    "By adding critique/feedback to the next attempt's context",
                    "By forcing every branch to run in parallel",
                    "By removing evaluation",
                ],

                "correct": 1,

                "explanation": (
                    "Reflexion is context-based iterative improvement, not training."
                ),
            },

            {
                "id": "M01.L05.Q09",

                "section_id": "strategy-selection",

                "question": "Which reasoning pattern is most naturally suited to tool-heavy tasks where new observations change the next action?",

                "options": [
                    "ReAct",
                    "Tree-of-Thought only",
                    "Best-of-N voting",
                    "Direct one-shot generation",
                ],

                "correct": 0,

                "explanation": (
                    "ReAct is built around repeated reasoning, action, and observation."
                ),
            },

            {
                "id": "M01.L05.Q10",

                "section_id": "sequential-thinking",

                "question": "What is the main role of the Sequential Thinking MCP server in this chapter?",

                "options": [
                    "It replaces the LLM with a deterministic planner",
                    "It provides a structured scratchpad for recording and revising reasoning state",
                    "It automatically proves every answer correct",
                    "It trains the model during runtime",
                ],

                "correct": 1,

                "explanation": (
                    "The agent remains responsible for reasoning. The server stores structured thought/planning state."
                ),
            },

            {
                "id": "M01.L05.Q11",

                "section_id": "advanced-combination",

                "question": "Why should CoT, ReAct, ToT, and Reflexion not be combined by default?",

                "options": [
                    "They cannot coexist technically",
                    "Each additional pattern can add model calls, tool calls, latency, and failure paths",
                    "They always produce identical behavior",
                    "They disable validation",
                ],

                "correct": 1,

                "explanation": (
                    "Advanced reasoning stacks are powerful but expensive and complex."
                ),
            },

            {
                "id": "M01.L05.Q12",

                "section_id": "reasoning-validation",

                "question": "What should happen after a complex reasoning process produces a candidate answer?",

                "options": [
                    "Assume it is correct because the reasoning was long",
                    "Validate it with deterministic checks, schemas, tests, tools, or appropriate evaluation",
                    "Immediately add more reasoning steps",
                    "Delete the trace",
                ],

                "correct": 1,

                "explanation": (
                    "Long reasoning is not evidence of correctness. Candidate outputs still need validation."
                ),
            },

            {
                "id": "M01.L05.Q13",

                "section_id": "planning-playbook",

                "type": "open",

                "question": (
                    "Design a reasoning architecture for an agent that must research an unfamiliar "
                    "technical problem, compare two possible solutions, test one solution, and revise "
                    "the plan if the test fails. Explain where decomposition, planning, ReAct, optional "
                    "branching, validation, and bounded retry would appear."
                ),
            },
        ],

        "passing_score": 70,
    },
}
