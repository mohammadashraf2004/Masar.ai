"""M01.L09 — Understanding the Agentic Loop.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 9, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L09"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Understand the three layers of agentic looping: the internal SPAL loop, "
    "external task loops for long-horizon work, and meta loops for orchestrated "
    "or collaborative multi-agent systems. Learn how state, plans, typed outputs, "
    "termination conditions, synthesis, retries, and consensus keep loops useful "
    "instead of allowing them to run indefinitely."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Understanding the Agentic Loop",

    "slug": "ai-agents-m01-l09",

    "description": (
        "Learn how agentic systems iterate toward goals across three layers: "
        "internal SPAL execution, external task loops for long-horizon work, "
        "and multi-agent meta loops controlled by orchestrators or collaborating peers."
    ),

    "order": 9,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.25,

    "skill_tags": [
        "agentic-loop",
        "spal",
        "long-horizon-agents",
        "deep-research",
        "state-management",
        "planning",
        "termination-conditions",
        "stagnation-detection",
        "typed-output",
        "task-loops",
        "orchestration",
        "collaboration",
        "consensus",
        "mcp",
        "module-01",
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


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Understanding the Agentic Loop",

        "content": (
            "# Understanding the Agentic Loop\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L09  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 9. "
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
            "- Explain the three layers of agentic looping.\n"
            "- Describe the internal SPAL loop and why it is agentic rather than merely repetitive code.\n"
            "- Identify the four core loop elements: goal, plan, state, and decision.\n"
            "- Explain why long-horizon work requires plan and state outside the agent.\n"
            "- Build the conceptual structure of a deep-research task loop.\n"
            "- Define typed state, plan, and iteration-output models.\n"
            "- Explain why structured iteration output is critical for loop control.\n"
            "- Apply layered termination conditions.\n"
            "- Explain hard limits, budget limits, goal satisfaction, quality thresholds, and stagnation detection.\n"
            "- Describe breadth-first versus depth-first exploration in research loops.\n"
            "- Explain why final synthesis should be separated from iterative exploration.\n"
            "- Identify when an agentic loop is useful and when it only adds cost.\n"
            "- Explain repetitive task loops, retries, and parallel processing.\n"
            "- Distinguish layer-2 deterministic task control from layer-3 agent-controlled meta loops.\n"
            "- Explain orchestrator-controlled meta loops.\n"
            "- Explain collaboration loops with shared state and consensus.\n"
            "- Choose between orchestration and collaboration based on task structure.\n"
            "- Design loop boundaries that prevent runaway cost and infinite execution.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why agentic loops matter\n"
            "\n"
            "Many useful agent tasks cannot be completed in one model call.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- researching an unfamiliar topic,\n"
            "- debugging a system through several observations,\n"
            "- processing a queue of documents,\n"
            "- refining an answer after critique,\n"
            "- coordinating several specialist agents.\n"
            "\n"
            "These tasks require the system to **repeat purposeful work while carrying forward what it has learned**.\n"
            "\n"
            "That repeated structure is the agentic loop.\n"
            "\n"
            "The chapter extends the SPAL loop from Chapter 1 into three layers:\n"
            "\n"
            "```text\n"
            "Layer 1 -> Internal SPAL loop\n"
            "Layer 2 -> External task loop\n"
            "Layer 3 -> Meta loop controlling agents/loops\n"
            "```\n"
            "\n"
            "Each layer adds a wider control horizon.\n"
            "\n"
            '{{image:task-loop-layers}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. Layer 1: the internal SPAL loop\n"
            "\n"
            "The first layer is the core sense-plan-act-learn cycle.\n"
            "\n"
            "```text\n"
            "Sense -> Plan -> Act -> Learn/Evaluate -> Decide whether to continue\n"
            "```\n"
            "\n"
            "The agent begins with a goal and current internal state.\n"
            "\n"
            "It then:\n"
            "\n"
            "1. **Senses** the current state and context.\n"
            "2. **Plans** the next step.\n"
            "3. **Acts** using a tool or generated action.\n"
            "4. **Learns/evaluates** the result.\n"
            "5. **Decides** whether the goal is complete or another iteration is required.\n"
            "\n"
            "Internal state grows as the loop proceeds, so later cycles can use information accumulated earlier.\n"
            "\n"
            "The defining property is not that code contains a `while` loop. The defining property is that the **agent chooses what to do inside the iteration**.\n"
            "\n"
            "The developer supplies goals, tools, and boundaries; the agent drives the local decisions.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Every loop needs goal, plan, state, and decision\n"
            "\n"
            "The chapter reduces agentic looping to four essential elements.\n"
            "\n"
            "### Goal\n"
            "\n"
            "What must be achieved?\n"
            "\n"
            "### Plan\n"
            "\n"
            "How should progress be made across iterations?\n"
            "\n"
            "### State\n"
            "\n"
            "What has already happened, and what context must survive into the next iteration?\n"
            "\n"
            "### Decision / termination condition\n"
            "\n"
            "Should the loop continue or stop?\n"
            "\n"
            "A loop that lacks one of these elements usually behaves poorly.\n"
            "\n"
            "For example:\n"
            "\n"
            "- no clear goal -> agent drifts,\n"
            "- no plan -> agent repeats random actions,\n"
            "- no state -> every iteration starts almost from scratch,\n"
            "- no termination condition -> runaway loop.\n"
            "\n"
            "[[IMAGE_NEEDED: Four core loop elements | "
            "A loop diagram around four labeled concepts: Goal, Plan, State, Decision. Show arrows indicating that state and plan "
            "are updated each iteration while the decision controls whether another cycle begins | "
            "Learner should notice that iteration alone is not enough; the loop needs explicit memory and stopping logic]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Layer 2: externalizing the task loop\n"
            "\n"
            "Layer 1 works well for short-horizon goals. Long-horizon work creates a new problem: one internal agent loop should not be expected to hold the entire evolving task forever.\n"
            "\n"
            "Layer 2 moves the major control objects outside the agent.\n"
            "\n"
            "```text\n"
            "External Goal\n"
            "External Plan\n"
            "External State\n"
            "External Decision Logic\n"
            "        |\n"
            "        v\n"
            "      Agent\n"
            "```\n"
            "\n"
            "The agent still performs its own internal reasoning, but a deterministic controller manages the larger task.\n"
            "\n"
            "This makes longer work possible because:\n"
            "\n"
            "- plan state can persist across calls,\n"
            "- accumulated findings can be stored outside the context window,\n"
            "- code can enforce hard limits,\n"
            "- the controller can decide what context the agent sees next.\n"
            "\n"
            "A deep-research system is the chapter's main example of this pattern.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Deep research as a layer-2 loop\n"
            "\n"
            "A deep-research agent works through many small searches to answer one larger question.\n"
            "\n"
            "A high-level architecture is:\n"
            "\n"
            "```text\n"
            "Long-horizon research goal\n"
            "        |\n"
            "        v\n"
            "Initialize state + plan\n"
            "        |\n"
            "        v\n"
            "Choose current question\n"
            "        |\n"
            "        v\n"
            "Run research agent\n"
            "        |\n"
            "        v\n"
            "Update findings / plan / follow-up questions\n"
            "        |\n"
            "        v\n"
            "Termination gate\n"
            "   |           |\n"
            " stop      continue\n"
            "   |           |\n"
            '   v           +-----> next iteration\nSynthesis\n```\n\n{{image:deep-research-loop}}'
            '\n'
            "\n"
            "The quality of the loop depends heavily on three areas emphasized by the chapter:\n"
            "\n"
            "1. **State management** between iterations.\n"
            "2. **Termination conditions**.\n"
            "3. **External tools** used by the agent.\n"
            "\n"
            "If these are weak, the loop may waste tokens repeating itself.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. External state and plan objects\n"
            "\n"
            "The chapter uses Pydantic objects to keep the research plan and execution state explicit.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "from pydantic import BaseModel, Field\n"
            "\n"
            "class SubTopic(BaseModel):\n"
            "    name: str\n"
            "    status: str = \"pending\"\n"
            "    notes: str = \"\"\n"
            "\n"
            "class ResearchPlan(BaseModel):\n"
            "    sub_topics: list[SubTopic] = Field(default_factory=list)\n"
            "    strategy_notes: str = \"\"\n"
            "\n"
            "class ResearchState(BaseModel):\n"
            "    goal: str = \"\"\n"
            "    findings: list[str] = Field(default_factory=list)\n"
            "    sources_consulted: list[str] = Field(default_factory=list)\n"
            "    follow_up_questions: list[str] = Field(default_factory=list)\n"
            "    plan: ResearchPlan = Field(default_factory=ResearchPlan)\n"
            "    iteration_count: int = 0\n"
            "    max_iterations: int = 10\n"
            "    status: str = \"in_progress\"\n"
            "```\n"
            "\n"
            "The state becomes the durable memory of the loop.\n"
            "\n"
            "The plan becomes the durable strategy.\n"
            "\n"
            "The agent may be called many times, but these objects survive across calls.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Control what state enters the context window\n"
            "\n"
            "External state can grow much larger than what should be sent to the model on every iteration.\n"
            "\n"
            "The chapter uses helper methods such as `to_context()` to serialize only useful information.\n"
            "\n"
            "This gives the controller an important responsibility:\n"
            "\n"
            "> Store more than the model sees.\n"
            "\n"
            "Possible strategies include:\n"
            "\n"
            "- send only recent findings,\n"
            "- summarize older findings,\n"
            "- include only unfinished plan items,\n"
            "- omit redundant sources,\n"
            "- pass a compact progress summary.\n"
            "\n"
            "This protects the context window and keeps the agent focused.\n"
            "\n"
            "The full state remains available to the system even if only a compact subset is passed into the next call.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Tools give the loop new information\n"
            "\n"
            "The research agent needs tools that can change what it knows between iterations.\n"
            "\n"
            "The chapter uses an MCP web-search server as an example:\n"
            "\n"
            "```python\n"
            "async def create_search_server() -> MCPServerStdio:\n"
            "    server = MCPServerStdio(\n"
            "        name=\"Brave Search\",\n"
            "        params={\n"
            "            \"command\": \"npx\",\n"
            "            \"args\": [\"-y\", \"@anthropic/brave-search-mcp\"],\n"
            "            \"env\": {\n"
            "                \"BRAVE_API_KEY\": os.environ[\"BRAVE_API_KEY\"]\n"
            "            },\n"
            "        },\n"
            "    )\n"
            "    await server.connect()\n"
            "    return server\n"
            "```\n"
            "\n"
            "A loop may use one or many tool families:\n"
            "\n"
            "- web search,\n"
            "- files,\n"
            "- databases,\n"
            "- retrieval systems,\n"
            "- classifiers,\n"
            "- analysis tools.\n"
            "\n"
            "The important point is that each iteration should be able to gain new evidence rather than merely rephrase what the agent already knew.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Typed iteration output is the control contract\n"
            "\n"
            "The external loop controller needs specific signals from the agent.\n"
            "\n"
            "Free-form prose is not reliable enough for this job.\n"
            "\n"
            "The chapter uses a structured iteration output similar to:\n"
            "\n"
            "```python\n"
            "class SubTopicUpdate(BaseModel):\n"
            "    name: str\n"
            "    status: str\n"
            "    notes: str = \"\"\n"
            "\n"
            "class ResearchIteration(BaseModel):\n"
            "    summary_of_findings: str\n"
            "    sources_used: list[str]\n"
            "    follow_up_questions: list[str]\n"
            "    goal_satisfied: bool\n"
            "    confidence: float\n"
            "    reasoning: str\n"
            "    plan_updates: list[SubTopicUpdate] = []\n"
            "    new_sub_topics: list[SubTopicUpdate] = []\n"
            "    strategy_notes: str = \"\"\n"
            "```\n"
            "\n"
            "The most important control fields are:\n"
            "\n"
            "- `follow_up_questions`: what should be investigated next,\n"
            "- `goal_satisfied`: whether the agent believes the goal is complete,\n"
            "- `confidence`: self-assessed confidence,\n"
            "- plan updates: how strategy changes.\n"
            "\n"
            "Typed output lets ordinary code update state and make decisions without parsing arbitrary prose.\n"
            "\n"
            "The chapter treats this as essential for robust loop control.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. The termination gate\n"
            "\n"
            "Every iteration must end with a decision: stop or continue.\n"
            "\n"
            "The chapter recommends **layered termination conditions** instead of relying on one signal.\n"
            "\n"
            "### Hard iteration limit\n"
            "\n"
            "Maximum number of cycles.\n"
            "\n"
            "This is the non-negotiable safety net.\n"
            "\n"
            "### Budget limit\n"
            "\n"
            "Maximum token or monetary spend.\n"
            "\n"
            "### Goal satisfaction\n"
            "\n"
            "The agent declares that enough information has been collected.\n"
            "\n"
            "### Quality threshold\n"
            "\n"
            "A confidence or evaluator score reaches the required level.\n"
            "\n"
            "### Stagnation detection\n"
            "\n"
            "The latest iterations are no longer producing meaningfully new information.\n"
            "\n"
            "A production loop should usually have more than one of these conditions active.\n"
            "\n"
            "[[IMAGE_NEEDED: Layered termination gate | "
            "Show an iteration result entering a decision gate with checks for hard limit, cost budget, goal satisfied, quality threshold, "
            "and stagnation. Any stop condition leads to exit; otherwise flow returns to the next iteration | "
            "Learner should notice that stopping is layered rather than delegated entirely to agent self-assessment]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Stagnation is different from failure\n"
            "\n"
            "A failing loop may return an exception or empty result.\n"
            "\n"
            "A stagnating loop is more subtle: it produces plausible output that adds little new information.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Iteration 4: Battery costs are falling.\n"
            "Iteration 5: Battery prices are decreasing.\n"
            "Iteration 6: Battery costs continue to decline.\n"
            "```\n"
            "\n"
            "The text looks productive, but the loop is not progressing.\n"
            "\n"
            "The chapter suggests comparing consecutive findings using semantic similarity.\n"
            "\n"
            "If similarity remains very high across repeated iterations, the loop can terminate because the marginal value has become too small.\n"
            "\n"
            "This creates an important production rule:\n"
            "\n"
            "> Detect lack of progress, not only explicit errors.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Unconstrained loops are production incidents\n"
            "\n"
            "Every cycle consumes resources:\n"
            "\n"
            "- input tokens,\n"
            "- output tokens,\n"
            "- tool/API calls,\n"
            "- elapsed time,\n"
            "- external service quotas.\n"
            "\n"
            "A loop that runs until the agent simply 'feels done' is not a safe production design.\n"
            "\n"
            "The chapter's strongest rule is:\n"
            "\n"
            "> Always enforce a hard iteration limit and a cost ceiling.\n"
            "\n"
            "Even if goal satisfaction and quality checks usually work, defensive ceilings protect against edge cases where the model keeps searching or reasoning in circles.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Coding the deep-research loop\n"
            "\n"
            "A simplified controller looks like this:\n"
            "\n"
            "```python\n"
            "async def run_research_loop(goal: str, max_iterations: int = 10):\n"
            "    state = ResearchState(\n"
            "        goal=goal,\n"
            "        max_iterations=max_iterations,\n"
            "        follow_up_questions=[goal],\n"
            "    )\n"
            "\n"
            "    while state.should_continue:\n"
            "        state.iteration_count += 1\n"
            "\n"
            "        question = state.follow_up_questions.pop(0)\n"
            "\n"
            "        result = await Runner.run(\n"
            "            agent,\n"
            "            input=str({\n"
            "                \"current_question\": question,\n"
            "                \"state\": state.to_context(),\n"
            "                \"plan\": state.plan.to_context(),\n"
            "            }),\n"
            "        )\n"
            "\n"
            "        iteration = result.final_output\n"
            "\n"
            "        state.findings.append(iteration.summary_of_findings)\n"
            "        state.sources_consulted.extend(iteration.sources_used)\n"
            "        state.follow_up_questions.extend(iteration.follow_up_questions)\n"
            "\n"
            "        apply_plan_updates(state.plan, iteration)\n"
            "\n"
            "        if iteration.goal_satisfied:\n"
            "            state.status = \"complete\"\n"
            "\n"
            "    return state\n"
            "```\n"
            "\n"
            "This code demonstrates the layer-2 pattern clearly:\n"
            "\n"
            "- code owns the outer loop,\n"
            "- the agent performs one meaningful iteration,\n"
            "- typed output updates state,\n"
            "- termination is checked outside the agent.\n"
            "\n"
            "{{exercise:M01.L09.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Breadth-first versus depth-first exploration\n"
            "\n"
            "The chapter uses a queue of follow-up questions.\n"
            "\n"
            "If the controller removes questions from the **front** and appends new ones to the **end**, it behaves like breadth-first exploration.\n"
            "\n"
            "```text\n"
            "Q1 -> Q2 -> Q3 -> child(Q1) -> child(Q2) -> ...\n"
            "```\n"
            "\n"
            "This spreads attention across several branches.\n"
            "\n"
            "If the controller removes the newest question from the **end**, the agent tends toward depth-first exploration.\n"
            "\n"
            "```text\n"
            "Q1 -> child(Q1) -> child(child(Q1)) -> ...\n"
            "```\n"
            "\n"
            "The right choice depends on the research goal.\n"
            "\n"
            "This resembles a Tree-of-Thought search structure: the controller determines which branch to explore next.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Separate exploration from synthesis\n"
            "\n"
            "After the research loop ends, the collected findings are not automatically a polished report.\n"
            "\n"
            "They may contain:\n"
            "\n"
            "- overlap,\n"
            "- contradictions,\n"
            "- incomplete sections,\n"
            "- differently formatted observations.\n"
            "\n"
            "The chapter uses a separate synthesis agent.\n"
            "\n"
            "```python\n"
            "class ResearchReport(BaseModel):\n"
            "    title: str\n"
            "    executive_summary: str\n"
            "    key_findings: list[str]\n"
            "    sources: list[str]\n"
            "    confidence_assessment: str\n"
            "    gaps_and_limitations: str\n"
            "```\n"
            "\n"
            "The synthesis agent receives the final state and plan and turns them into one structured report.\n"
            "\n"
            "Why separate the roles?\n"
            "\n"
            "```text\n"
            "Research Agent  -> optimize for discovery\n"
            "Synthesis Agent -> optimize for structure and communication\n"
            "```\n"
            "\n"
            "Combining both jobs can cause the research agent to optimize too early for report formatting rather than information discovery.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. When an agentic loop is useful\n"
            "\n"
            "Use a loop when the work benefits from repeated interaction with new state.\n"
            "\n"
            "The chapter identifies several strong cases.\n"
            "\n"
            "### Iterative discovery\n"
            "\n"
            "The agent cannot know all required information in advance.\n"
            "\n"
            "### Progressive refinement\n"
            "\n"
            "Output improves over repeated drafts or evaluations.\n"
            "\n"
            "### Batch processing\n"
            "\n"
            "A queue of items must be processed repeatedly.\n"
            "\n"
            "### Conditional branching\n"
            "\n"
            "The next action depends on the previous result.\n"
            "\n"
            "### Multisource aggregation\n"
            "\n"
            "The agent discovers relevant sources dynamically while working.\n"
            "\n"
            "Avoid loops for simple single-pass tasks such as straightforward classification, simple question answering, or pure format conversion.\n"
            "\n"
            "Loops add latency and cost. They need to earn their complexity.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Repetitive task loops\n"
            "\n"
            "Research loops discover what to do next. Task loops already know the work queue.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- process invoices,\n"
            "- transform documents,\n"
            "- test several endpoints,\n"
            "- migrate records,\n"
            "- inspect files one by one.\n"
            "\n"
            "The architecture is:\n"
            "\n"
            "```text\n"
            "Task queue\n"
            "   |\n"
            "   v\n"
            "Select item\n"
            "   |\n"
            "   v\n"
            "Agent processes item\n"
            "   |\n"
            "   v\n"
            "Record success/failure\n"
            "   |\n"
            "   +--> retry if transient\n"
            "   |\n"
            "   v\n"
            "Next item\n"
            "```\n"
            "\n"
            "Because the queue itself defines the work, this variation may not require a separate strategic plan object.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Retries belong in task state\n"
            "\n"
            "Task loops frequently encounter transient errors.\n"
            "\n"
            "A robust design should track:\n"
            "\n"
            "- pending items,\n"
            "- completed items,\n"
            "- failed items,\n"
            "- retry count,\n"
            "- previous error information.\n"
            "\n"
            "The previous error should be available to the next attempt so the agent can adjust if needed.\n"
            "\n"
            "A hard retry ceiling is essential.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Task failed\n"
            "  -> retry 1\n"
            "  -> retry 2\n"
            "  -> retry 3\n"
            "  -> mark permanently failed\n"
            "```\n"
            "\n"
            "Retries are part of the loop design, not an afterthought.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Parallel iteration for independent tasks\n"
            "\n"
            "If several queue items are independent, they do not need to be processed one at a time.\n"
            "\n"
            "The chapter recommends parallel iteration patterns such as `asyncio.gather` for independent batches.\n"
            "\n"
            "```python\n"
            "results = await asyncio.gather(\n"
            "    process(item_1),\n"
            "    process(item_2),\n"
            "    process(item_3),\n"
            ")\n"
            "```\n"
            "\n"
            "Benefits:\n"
            "\n"
            "- lower total elapsed time,\n"
            "- better resource utilization.\n"
            "\n"
            "Constraints:\n"
            "\n"
            "- items must truly be independent,\n"
            "- API rate limits still apply,\n"
            "- concurrency can amplify failures,\n"
            "- shared state must be handled safely.\n"
            "\n"
            "Parallelism is a throughput optimization, not a default for every loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Adaptive iteration budgets still need hard ceilings\n"
            "\n"
            "Some goals naturally require more iterations than others.\n"
            "\n"
            "The chapter notes that systems can allow an agent to estimate or request an iteration budget based on task complexity.\n"
            "\n"
            "However, this adaptive budget should remain inside developer-defined boundaries.\n"
            "\n"
            "```text\n"
            "Agent requests: 12 iterations\n"
            "Developer ceiling: 8\n"
            "Effective maximum: 8\n"
            "```\n"
            "\n"
            "This preserves flexibility without surrendering cost control.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Layer 3: the meta-agentic loop\n"
            "\n"
            "Layer 2 is generally controlled by deterministic code.\n"
            "\n"
            "Layer 3 moves the control decision to an agent or group of agents.\n"
            "\n"
            "That is the defining difference.\n"
            "\n"
            "Two major forms are presented:\n"
            "\n"
            "1. **Orchestration meta loop** — one central agent controls delegation and replanning.\n"
            "2. **Collaboration meta loop** — several peer agents jointly contribute and decide when the goal is complete.\n"
            "\n"
            "[[IMAGE_NEEDED: Layer 2 versus Layer 3 control | "
            "Left: deterministic code loop controls one agent. Right: an orchestrator agent or peer-agent team controls the outer loop and delegates work | "
            "Learner should notice that Layer 3 promotes decision/control from ordinary code to agent reasoning]]\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Orchestrator-controlled meta loops\n"
            "\n"
            "An orchestrator holds the global view of the goal.\n"
            "\n"
            "It can:\n"
            "\n"
            "- decompose the goal,\n"
            "- choose a worker,\n"
            "- delegate a subtask,\n"
            "- evaluate worker output,\n"
            "- revise the plan,\n"
            "- decide when to finalize.\n"
            "\n"
            "A structured decision might look like:\n"
            "\n"
            "```python\n"
            "class OrchestratorDecision(BaseModel):\n"
            "    next_action: str       # delegate | re_plan | finalize\n"
            "    target_worker: str = \"\"\n"
            "    task_description: str = \"\"\n"
            "    reasoning: str = \"\"\n"
            "    plan_updates: list[SubTopicUpdate] = []\n"
            "    is_complete: bool = False\n"
            "```\n"
            "\n"
            "The key difference from layer 2 is that the outer decision is now made by an LLM-driven orchestrator rather than hardcoded routing logic.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Separate strategic reasoning from worker execution\n"
            "\n"
            "The chapter's orchestrator uses specialized workers.\n"
            "\n"
            "Example roles:\n"
            "\n"
            "- **Research Worker** — gathers information.\n"
            "- **Analysis Worker** — identifies patterns, contradictions, and gaps.\n"
            "- **Research Orchestrator** — chooses the next subtask and worker.\n"
            "\n"
            "This produces a clean split:\n"
            "\n"
            "```text\n"
            "Orchestrator -> strategy / delegation / evaluation\n"
            "Workers      -> tactical execution\n"
            "```\n"
            "\n"
            "The orchestrator can also re-plan when new findings reveal that the original decomposition was incomplete.\n"
            "\n"
            "That adaptability is the main advantage over a static layer-2 dispatcher.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Orchestrators add real overhead\n"
            "\n"
            "Every orchestration decision is another model call.\n"
            "\n"
            "If a 15-iteration loop uses one orchestrator call and one worker call per cycle, the system may require roughly twice as many model interactions as a simpler deterministic controller.\n"
            "\n"
            "Use an orchestrator when:\n"
            "\n"
            "- decomposition is uncertain,\n"
            "- worker choice changes dynamically,\n"
            "- new findings may require re-planning,\n"
            "- strategy itself needs reasoning.\n"
            "\n"
            "Prefer a layer-2 deterministic controller when:\n"
            "\n"
            "- task decomposition is known,\n"
            "- routing rules are simple,\n"
            "- cost and latency matter more than flexibility.\n"
            "\n"
            "Do not pay LLM cost for decisions ordinary code can already make reliably.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Collaborative meta loops\n"
            "\n"
            "Collaboration removes the single central orchestrator.\n"
            "\n"
            "Instead, peer agents share state and take turns improving the collective result.\n"
            "\n"
            "The chapter uses a common trio:\n"
            "\n"
            "- researcher,\n"
            "- critic,\n"
            "- synthesizer.\n"
            "\n"
            "```text\n"
            "Researcher -> contributes findings\n"
            "Critic     -> challenges gaps/claims\n"
            "Synthesizer-> integrates and resolves contradictions\n"
            "                 |\n"
            "                 v\n"
            "              next round\n"
            "```\n"
            "\n"
            "This pattern is useful when multiple perspectives and adversarial review improve quality.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Shared state and consensus\n"
            "\n"
            "The collaboration loop uses a shared state object.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "class Contribution(BaseModel):\n"
            "    agent_name: str\n"
            "    content: str\n"
            "    critique: str = \"\"\n"
            "    suggestions: list[str] = []\n"
            "    agrees_goal_met: bool = False\n"
            "    confidence: float = 0.0\n"
            "\n"
            "class CollaborationState(BaseModel):\n"
            "    goal: str\n"
            "    contributions: list[Contribution] = []\n"
            "    round_number: int = 0\n"
            "    max_rounds: int = 5\n"
            "    consensus_threshold: float = 0.8\n"
            "```\n"
            "\n"
            "The loop continues until:\n"
            "\n"
            "- enough recent agents agree the goal is satisfied, or\n"
            "- the hard round limit is reached.\n"
            "\n"
            "The consensus threshold is another termination condition.\n"
            "\n"
            "It should not replace the maximum-round safety ceiling.\n"
            "\n"
            '{{image:collaboration-loop}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 27. Turn-based collaboration execution\n"
            "\n"
            "The chapter uses round-robin execution.\n"
            "\n"
            "```python\n"
            "agents = [researcher_agent, critic_agent, synthesizer_agent]\n"
            "\n"
            "agent_index = 0\n"
            "\n"
            "while state.round_number < state.max_rounds and not state.has_consensus:\n"
            "    current_agent = agents[agent_index % len(agents)]\n"
            "\n"
            "    result = await Runner.run(\n"
            "        current_agent,\n"
            "        input=str({\n"
            "            \"goal\": state.goal,\n"
            "            \"recent_contributions\": state.recent_context(),\n"
            "        }),\n"
            "    )\n"
            "\n"
            "    state.contributions.append(result.final_output)\n"
            "\n"
            "    agent_index += 1\n"
            "```\n"
            "\n"
            "Only agents that need particular tools should receive them. In the chapter's example, the researcher gets the search capability while critic and synthesizer operate on collected findings.\n"
            "\n"
            "This keeps tool access aligned with role responsibility.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Orchestration versus collaboration\n"
            "\n"
            "Use **orchestration** when the goal decomposes into specialist subtasks that can be assigned clearly.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- batch pipelines,\n"
            "- parallel search,\n"
            "- document transformations,\n"
            "- specialist tool routing.\n"
            "\n"
            "Use **collaboration** when interdependent perspectives improve the output.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- research synthesis,\n"
            "- strategic analysis,\n"
            "- document review,\n"
            "- adversarial critique.\n"
            "\n"
            "If uncertain, the chapter recommends beginning with orchestration because it is simpler to debug, then moving to collaboration only when the quality benefit justifies the extra coordination.\n"
            "\n"
            "{{exercise:M01.L09.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Practical agentic-loop design playbook\n"
            "\n"
            "Use this checklist whenever you design a loop.\n"
            "\n"
            "### Step 1 — Decide the loop layer\n"
            "\n"
            "Is the goal short enough for one agent, long enough for an external task loop, or adaptive enough for a meta loop?\n"
            "\n"
            "### Step 2 — Define the goal precisely\n"
            "\n"
            "The loop needs a clear objective.\n"
            "\n"
            "### Step 3 — Define state explicitly\n"
            "\n"
            "What must survive between iterations?\n"
            "\n"
            "### Step 4 — Define the iteration strategy\n"
            "\n"
            "What should one cycle accomplish?\n"
            "\n"
            "### Step 5 — Use typed iteration outputs\n"
            "\n"
            "Loop controllers need machine-readable signals.\n"
            "\n"
            "### Step 6 — Limit what enters each model context\n"
            "\n"
            "Store full history externally; send only what the current step needs.\n"
            "\n"
            "### Step 7 — Layer termination conditions\n"
            "\n"
            "Always include hard iteration and cost limits.\n"
            "\n"
            "### Step 8 — Detect stagnation\n"
            "\n"
            "Repeated plausible output is still a failure mode.\n"
            "\n"
            "### Step 9 — Separate exploration from final synthesis\n"
            "\n"
            "Use different roles when the objectives differ.\n"
            "\n"
            "### Step 10 — Parallelize only independent work\n"
            "\n"
            "Concurrency is useful only when dependencies allow it.\n"
            "\n"
            "### Step 11 — Use orchestration only when strategy needs reasoning\n"
            "\n"
            "Do not replace cheap deterministic code with expensive model decisions unnecessarily.\n"
            "\n"
            "### Step 12 — Use collaboration for genuine multi-perspective value\n"
            "\n"
            "More agents are not automatically better.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Any `while` loop around an LLM is an agentic loop\n"
            "\n"
            "> Agentic behavior requires the agent to make meaningful decisions inside the cycle.\n"
            "\n"
            "### Misconception 2: Long-horizon goals can live entirely inside one context window\n"
            "\n"
            "> Long-running work needs external state and often an external plan.\n"
            "\n"
            "### Misconception 3: The agent should decide all termination conditions\n"
            "\n"
            "> Agent self-assessment is useful, but hard limits and cost ceilings should be enforced by the system.\n"
            "\n"
            "### Misconception 4: A loop is healthy as long as it keeps producing text\n"
            "\n"
            "> Stagnation can produce plausible but non-improving output.\n"
            "\n"
            "### Misconception 5: Free-form output is fine because an LLM can parse it later\n"
            "\n"
            "> Loop control should rely on strongly typed output rather than another probabilistic parsing step.\n"
            "\n"
            "### Misconception 6: The research agent should also write the final report\n"
            "\n"
            "> Exploration and synthesis optimize for different goals and are better separated.\n"
            "\n"
            "### Misconception 7: Layer 3 is always better than layer 2\n"
            "\n"
            "> Meta loops add model calls, latency, and cost. Use them only when adaptive strategy adds value.\n"
            "\n"
            "### Misconception 8: Collaboration should replace orchestration whenever more than one agent is involved\n"
            "\n"
            "> Collaboration is most valuable when interdependent perspectives and critique improve the result.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Agentic loop | Repeated goal-directed agent execution that carries state forward |\n"
            "| SPAL | Sense-plan-act-learn internal agent loop |\n"
            "| Layer 1 | Internal loop inside one agent |\n"
            "| Layer 2 | External task loop controlled mainly by program logic |\n"
            "| Layer 3 | Meta loop controlled by an orchestrator or collaborating agents |\n"
            "| Long-horizon goal | Goal requiring many iterations or subtasks over extended state |\n"
            "| State | Persisted information carried between iterations |\n"
            "| Plan | Strategy describing how work should progress |\n"
            "| Iteration | One execution cycle of the loop |\n"
            "| Termination gate | Decision point determining whether the loop stops or continues |\n"
            "| Hard limit | Maximum iteration count enforced by the system |\n"
            "| Budget limit | Maximum cost/token spend allowed for the loop |\n"
            "| Stagnation | Continued execution without meaningful progress |\n"
            "| Breadth-first exploration | Explore several branches at similar depth before going deeper |\n"
            "| Depth-first exploration | Follow one branch deeply before returning to alternatives |\n"
            "| Synthesis agent | Separate agent that compiles accumulated findings into final output |\n"
            "| Task loop | Loop processing a known queue of work items |\n"
            "| Meta loop | Higher-level agent-controlled loop over workers or other loops |\n"
            "| Orchestrator | Central agent that plans, delegates, evaluates, and replans |\n"
            "| Collaboration loop | Peer-agent loop using shared state and collective refinement |\n"
            "| Consensus threshold | Required level of agent agreement before collaborative termination |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are the three layers of the agentic loop?\n"
            "2. What makes the SPAL cycle agentic rather than merely repetitive code?\n"
            "3. What four elements must every loop design include?\n"
            "4. Why does layer 2 externalize state and planning?\n"
            "5. What is the role of ResearchState?\n"
            "6. What is the role of ResearchPlan?\n"
            "7. Why should the model see only selected state each iteration?\n"
            "8. Why are typed iteration outputs critical?\n"
            "9. What signals can drive loop termination?\n"
            "10. Why are hard limits and budget ceilings mandatory?\n"
            "11. What is stagnation, and why is it difficult to detect?\n"
            "12. How do breadth-first and depth-first research differ?\n"
            "13. Why should exploration and synthesis use separate agents?\n"
            "14. When is an agentic loop unnecessary?\n"
            "15. How does a repetitive task loop differ from a research loop?\n"
            "16. Why must retries be bounded?\n"
            "17. When can task-loop iterations run in parallel?\n"
            "18. What is the defining difference between layer 2 and layer 3?\n"
            "19. What decisions does an orchestrator make?\n"
            "20. Why does orchestration cost more than deterministic dispatch?\n"
            "21. How does collaboration use shared state?\n"
            "22. What does a consensus threshold control?\n"
            "23. When should you prefer orchestration over collaboration?\n"
            "24. Why should every production loop have both iteration and cost ceilings?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Agentic loops are useful because they let systems pursue goals that require repeated action, new evidence, "
            "and evolving state. The safe architecture is always the same at its core: define the goal, persist the state, "
            "control the plan, require structured iteration output, and enforce explicit stopping conditions. Move from "
            "internal loops to task loops or meta loops only when the wider control horizon truly improves the task.**\n"
        ),

        "estimated_minutes": 255,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-loops", "title": "Why agentic loops matter", "order": 1},
            {"id": "layer-one-spal", "title": "Layer 1: the internal SPAL loop", "order": 2},
            {"id": "core-loop-elements", "title": "Every loop needs goal, plan, state, and decision", "order": 3},
            {"id": "layer-two", "title": "Layer 2: externalizing the task loop", "order": 4},
            {"id": "deep-research-architecture", "title": "Deep research as a layer-2 loop", "order": 5},
            {"id": "research-state-plan", "title": "External state and plan objects", "order": 6},
            {"id": "context-control", "title": "Control what state enters the context window", "order": 7},
            {"id": "tools", "title": "Tools give the loop new information", "order": 8},
            {"id": "typed-iteration", "title": "Typed iteration output is the control contract", "order": 9},
            {"id": "termination", "title": "The termination gate", "order": 10},
            {"id": "stagnation", "title": "Stagnation is different from failure", "order": 11},
            {"id": "unconstrained-loops", "title": "Unconstrained loops are production incidents", "order": 12},
            {"id": "deep-research-loop", "title": "Coding the deep-research loop", "order": 13},
            {"id": "breadth-depth", "title": "Breadth-first versus depth-first exploration", "order": 14},
            {"id": "synthesis", "title": "Separate exploration from synthesis", "order": 15},
            {"id": "when-to-loop", "title": "When an agentic loop is useful", "order": 16},
            {"id": "task-loop", "title": "Repetitive task loops", "order": 17},
            {"id": "retry-task-loop", "title": "Retries belong in task state", "order": 18},
            {"id": "parallel-task-loop", "title": "Parallel iteration for independent tasks", "order": 19},
            {"id": "adaptive-budget", "title": "Adaptive iteration budgets still need hard ceilings", "order": 20},
            {"id": "layer-three", "title": "Layer 3: the meta-agentic loop", "order": 21},
            {"id": "orchestrator-loop", "title": "Orchestrator-controlled meta loops", "order": 22},
            {"id": "orchestrator-workers", "title": "Separate strategic reasoning from worker execution", "order": 23},
            {"id": "orchestrator-cost", "title": "Orchestrators add real overhead", "order": 24},
            {"id": "collaboration-loop", "title": "Collaborative meta loops", "order": 25},
            {"id": "shared-collaboration-state", "title": "Shared state and consensus", "order": 26},
            {"id": "collaboration-execution", "title": "Turn-based collaboration execution", "order": 27},
            {"id": "orchestration-vs-collaboration", "title": "Orchestration versus collaboration", "order": 28},
            {"id": "loop-playbook", "title": "Practical agentic-loop design playbook", "order": 29},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L09.EX01",

            "title": "Build a Safe Deep-Research Task Loop",

            "lesson_code": "M01.L09",

            "section_id": "deep-research-loop",

            "placement": "after_section",

            "description": (
                "Build a layer-2 loop with explicit state, typed iteration output, "
                "multiple termination conditions, and context control."
            ),

            "instructions": (
                "Build a small research loop around a local list of facts or a search tool.\n"
                "1. Create `SubTopic`, `ResearchPlan`, `ResearchState`, `SubTopicUpdate`, and `ResearchIteration` models.\n"
                "2. Seed the state with one long-horizon research goal.\n"
                "3. Give the research agent a search tool and typed `ResearchIteration` output.\n"
                "4. Let the first iteration create subtopics.\n"
                "5. Carry findings, sources, follow-up questions, and plan updates into later iterations.\n"
                "6. Limit the model context to the most recent findings or a compact summary.\n"
                "7. Add a hard maximum of five iterations.\n"
                "8. Add a confidence or goal-satisfaction stop condition.\n"
                "9. Add stagnation detection by comparing consecutive findings.\n"
                "10. Print the iteration count, findings count, plan progress, and final status.\n"
                "11. After the loop, call a separate synthesis step to produce a final report.\n"
                "12. Explain why the synthesis agent should not perform new research."
            ),

            "expected_output": (
                "A working or carefully written layer-2 research loop with state, plan, "
                "typed output, context management, layered termination, stagnation handling, "
                "and separate synthesis."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "layer-2-loop",
                "deep-research",
                "state-management",
                "typed-output",
                "termination",
                "stagnation-detection",
                "synthesis",
            ],
        },

        {
            "id": "M01.L09.EX02",

            "title": "Compare Orchestration and Collaboration Meta Loops",

            "lesson_code": "M01.L09",

            "section_id": "orchestration-vs-collaboration",

            "placement": "after_section",

            "description": (
                "Practice both layer-3 subtypes and compare their control style, "
                "cost, state, and output quality."
            ),

            "instructions": (
                "Use the same complex research goal for two implementations.\n"
                "Part A — Orchestration:\n"
                "1. Create a Research Worker and Analysis Worker.\n"
                "2. Create an OrchestratorDecision model with delegate, re_plan, and finalize actions.\n"
                "3. Give the orchestrator the global state/plan and let it choose workers.\n"
                "4. Add a hard maximum of six orchestrator iterations.\n"
                "5. Print the orchestrator decision on every iteration.\n"
                "\n"
                "Part B — Collaboration:\n"
                "6. Create Researcher, Critic, and Synthesizer agents.\n"
                "7. Store their outputs in a shared `CollaborationState`.\n"
                "8. Use round-robin execution for at most three rounds.\n"
                "9. Add a consensus threshold for goal completion.\n"
                "10. Give search access only to the Researcher.\n"
                "\n"
                "Comparison:\n"
                "11. Compare number of model calls, ease of debugging, output quality, and coordination overhead.\n"
                "12. Decide which architecture better fits the goal and justify the choice."
            ),

            "expected_output": (
                "Two layer-3 architecture implementations or detailed pseudocode plus a comparison "
                "of strategic control, shared state, model-call overhead, debugging difficulty, "
                "consensus behavior, and final quality."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "layer-3-loop",
                "orchestration",
                "collaboration",
                "worker-agents",
                "shared-state",
                "consensus",
                "architecture-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L09.QZ01",

        "title": "Understanding the Agentic Loop — Knowledge Check",

        "lesson_code": "M01.L09",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L09.Q01",
                "section_id": "why-loops",
                "question": "What changes as you move from agentic loop layer 1 to layer 3?",
                "options": [
                    "The model stops using tools",
                    "The control horizon expands from one agent's internal loop to external task and multi-agent control",
                    "All state disappears",
                    "Every loop becomes deterministic",
                ],
                "correct": 1,
                "explanation": (
                    "Higher layers move control beyond one internal SPAL cycle toward external task management and meta-agent coordination."
                ),
            },

            {
                "id": "M01.L09.Q02",
                "section_id": "layer-one-spal",
                "question": "What makes an internal SPAL loop agentic?",
                "options": [
                    "It contains Python repetition syntax",
                    "The agent makes decisions about actions and stopping inside the cycle",
                    "It always uses more than one model",
                    "It must be deployed in a container",
                ],
                "correct": 1,
                "explanation": (
                    "Agentic behavior comes from model-driven decisions within the iteration, not merely from repeated code."
                ),
            },

            {
                "id": "M01.L09.Q03",
                "section_id": "core-loop-elements",
                "question": "Which set contains the four core loop elements emphasized in the lesson?",
                "options": [
                    "Goal, plan, state, decision",
                    "Prompt, GPU, browser, Docker",
                    "Agent, CSS, queue, API key",
                    "Tool, image, file, database",
                ],
                "correct": 0,
                "explanation": (
                    "Every loop needs an objective, iteration strategy, carried state, and a stop/continue decision."
                ),
            },

            {
                "id": "M01.L09.Q04",
                "section_id": "layer-two",
                "question": "Why does layer 2 externalize plan and state?",
                "options": [
                    "To prevent the agent from receiving any context",
                    "To support long-horizon work across many calls without relying on one transient context window",
                    "To eliminate structured data",
                    "To prevent tools from being used",
                ],
                "correct": 1,
                "explanation": (
                    "External state lets the system persist information and strategy across multiple short-horizon agent calls."
                ),
            },

            {
                "id": "M01.L09.Q05",
                "section_id": "typed-iteration",
                "question": "Why is strongly typed iteration output important?",
                "options": [
                    "It makes LLMs deterministic",
                    "It gives the loop controller reliable machine-readable fields for state updates and control flow",
                    "It removes the need for state",
                    "It guarantees the research is factually correct",
                ],
                "correct": 1,
                "explanation": (
                    "The controller needs fields such as follow-up questions and goal-satisfaction flags without parsing free-form prose."
                ),
            },

            {
                "id": "M01.L09.Q06",
                "section_id": "termination",
                "question": "Which termination condition should always exist even if the agent can self-assess goal completion?",
                "options": [
                    "Only a confidence score",
                    "A hard iteration limit",
                    "Only a critic agent",
                    "Only a user message",
                ],
                "correct": 1,
                "explanation": (
                    "A hard maximum is the defensive safety net against loops that fail to converge."
                ),
            },

            {
                "id": "M01.L09.Q07",
                "section_id": "stagnation",
                "question": "What best describes loop stagnation?",
                "options": [
                    "The process crashes immediately",
                    "The loop keeps producing plausible output without meaningful new progress",
                    "The loop reaches the goal quickly",
                    "The tool server shuts down normally",
                ],
                "correct": 1,
                "explanation": (
                    "Stagnation is deceptive because the system appears active while adding little value."
                ),
            },

            {
                "id": "M01.L09.Q08",
                "section_id": "breadth-depth",
                "question": "What does popping follow-up questions from the front of a queue encourage?",
                "options": [
                    "Breadth-first exploration",
                    "Only final synthesis",
                    "No exploration",
                    "Infinite recursion",
                ],
                "correct": 0,
                "explanation": (
                    "Front-of-queue processing spreads effort across branches before going deeply into one."
                ),
            },

            {
                "id": "M01.L09.Q09",
                "section_id": "synthesis",
                "question": "Why use a separate synthesis agent after a research loop?",
                "options": [
                    "Because the research agent cannot produce text",
                    "To separate discovery from final organization and contradiction resolution",
                    "To reset all research state",
                    "To avoid using structured output",
                ],
                "correct": 1,
                "explanation": (
                    "Exploration and final reporting optimize for different objectives and are cleaner as separate roles."
                ),
            },

            {
                "id": "M01.L09.Q10",
                "section_id": "task-loop",
                "question": "What distinguishes a repetitive task loop from a deep-research loop?",
                "options": [
                    "The task loop usually has a known work queue rather than discovering follow-up work dynamically",
                    "The task loop cannot use tools",
                    "The research loop cannot store state",
                    "The task loop must use collaboration",
                ],
                "correct": 0,
                "explanation": (
                    "Task loops process predefined items; research loops discover what should be investigated next."
                ),
            },

            {
                "id": "M01.L09.Q11",
                "section_id": "layer-three",
                "question": "What is the defining change at layer 3?",
                "options": [
                    "The outer control is performed by an agent or agents rather than only deterministic code",
                    "The agent no longer has a goal",
                    "State becomes unnecessary",
                    "Every task runs in parallel",
                ],
                "correct": 0,
                "explanation": (
                    "Layer 3 promotes planning/decision control into an agent-controlled meta loop."
                ),
            },

            {
                "id": "M01.L09.Q12",
                "section_id": "orchestrator-cost",
                "question": "When is an orchestrator most justified?",
                "options": [
                    "When task decomposition is fixed and trivial",
                    "When decomposition, routing, or replanning must adapt to intermediate results",
                    "Whenever one tool exists",
                    "For simple format conversion",
                ],
                "correct": 1,
                "explanation": (
                    "The orchestrator earns its additional model-call cost when strategic decisions cannot be hardcoded reliably."
                ),
            },

            {
                "id": "M01.L09.Q13",
                "section_id": "shared-collaboration-state",
                "question": "What controls normal termination in the collaboration example?",
                "options": [
                    "Only the Researcher's opinion",
                    "A consensus threshold plus a hard maximum number of rounds",
                    "A random timer",
                    "The number of available tools",
                ],
                "correct": 1,
                "explanation": (
                    "Consensus is the quality-style stop condition, while max rounds remains the safety ceiling."
                ),
            },

            {
                "id": "M01.L09.Q14",
                "section_id": "orchestration-vs-collaboration",
                "question": "Which task is a stronger fit for collaboration than simple orchestration?",
                "options": [
                    "Independent batch file conversions",
                    "Strategic analysis that benefits from researcher, critic, and synthesizer perspectives",
                    "A fixed queue of API requests",
                    "One exact database lookup",
                ],
                "correct": 1,
                "explanation": (
                    "Collaboration is most valuable when interdependent perspectives and adversarial review improve the final output."
                ),
            },

            {
                "id": "M01.L09.Q15",
                "section_id": "loop-playbook",
                "type": "open",
                "question": (
                    "Design an agentic system for a long-horizon research task. Explain which loop layer you choose, "
                    "what state and plan are persisted, what one iteration produces, how context is compressed, what tools "
                    "are available, which termination conditions are enforced, whether synthesis is separate, and whether "
                    "orchestration or collaboration would improve the design."
                ),
            },
        ],

        "passing_score": 70,
    },
}
