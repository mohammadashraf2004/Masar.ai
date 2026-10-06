"""M01.L04 — Architecting and Building Multi-Agent Systems.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 4, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how to architect reliable multi-agent systems by deliberately "
    "controlling decision-making, execution, communication, coordination, "
    "handoffs, typed data flow, observability, and guardrails."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Architecting and Building Multi-Agent Systems",

    "slug": "ai-agents-m01-l04",

    "description": (
        "Move from a monolithic agent to structured multi-agent systems. "
        "Learn flow, orchestration, collaboration, communication strategies, "
        "handoffs, deterministic decision points, guardrails, retries, and "
        "practical architecture trade-offs."
    ),

    "order": 4,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "multi-agent-systems",
        "agent-flow",
        "orchestration",
        "collaboration",
        "handoffs",
        "guardrails",
        "typed-io",
        "coordination",
        "observability",
        "retries",
        "architecture",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Architecting and Building Multi-Agent Systems",

        "content": (
            "# Architecting and Building Multi-Agent Systems\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L04  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 4. "
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
            "- Explain when a single agent should remain single and when decomposition is useful.\n"
            "- Distinguish decision-making, control, communication, and coordination in agent systems.\n"
            "- Compare flow, orchestration, collaboration, and manager-worker structures.\n"
            "- Choose among message passing, shared context, and tool-mediated communication.\n"
            "- Compare sequential, parallel, hierarchical, iterative, ensemble, routing, and peer patterns.\n"
            "- Explain why agency should be constrained according to risk.\n"
            "- Refactor a monolithic tool-heavy agent into specialized agents.\n"
            "- Insert deterministic decision points outside the LLM when repeatability is required.\n"
            "- Use typed outputs to stabilize agent-to-agent data transfer.\n"
            "- Explain conversational handoffs versus explicit pass-off routing.\n"
            "- Visualize and monitor handoffs with graphs and traces.\n"
            "- Use callbacks for observation and guardrails for enforcement.\n"
            "- Implement input and output guardrails and bounded retry loops.\n"
            "- Explain when LLM-powered guardrails are justified and when deterministic checks are better.\n"
            "- Recognize shape failure, context leakage, and instruction injection at agent boundaries.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why multi-agent systems appeared\n"
            "\n"
            "The first instinct in agent development was often simple: if one agent can solve a "
            "problem, several agents should solve a harder one. Early systems demonstrated that "
            "this is only partly true.\n"
            "\n"
            "More agents can increase capability, but they also introduce new problems:\n"
            "\n"
            "- coordination overhead,\n"
            "- more LLM calls,\n"
            "- higher token cost,\n"
            "- longer latency,\n"
            "- more failure points,\n"
            "- harder debugging,\n"
            "- less predictable behavior.\n"
            "\n"
            "The important shift is from asking:\n"
            "\n"
            "```text\n"
            "\"How many agents should I add?\"\n"
            "```\n"
            "\n"
            "to asking:\n"
            "\n"
            "```text\n"
            "\"What architecture gives each agent the right responsibility, context, and authority?\"\n"
            "```\n"
            "\n"
            "That is the main theme of this chapter.\n"
            "\n"
            "[[IMAGE_NEEDED: Monolithic agent versus structured multi-agent system | "
            "Left: one overloaded agent with many tools and responsibilities. Right: several "
            "specialized agents connected through a clear flow, each with a small tool set | "
            "Learner should notice that decomposition reduces responsibility per agent but adds "
            "coordination boundaries]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. The four architecture questions: decision-making, control, communication, coordination\n"
            "\n"
            "Before choosing a multi-agent pattern, the chapter asks us to reason about four ideas.\n"
            "\n"
            "### Decision-making\n"
            "\n"
            "Decision-making is the authority to choose what happens next.\n"
            "\n"
            "Example: a research system has ten sources and must choose which three to summarize. "
            "The component that makes that choice owns the decision.\n"
            "\n"
            "Two questions matter:\n"
            "\n"
            "1. Which agent has authority to decide?\n"
            "2. What context does it see while deciding?\n"
            "\n"
            "Too little context can produce uninformed choices. Too much context can bury the relevant signal.\n"
            "\n"
            "### Control\n"
            "\n"
            "Control is the authority to execute work.\n"
            "\n"
            "A planner may decide what should happen without directly calling any tool. A worker "
            "may execute a tool without being allowed to choose the next task.\n"
            "\n"
            "Therefore:\n"
            "\n"
            "```text\n"
            "Decision-making = Who chooses?\n"
            "Control         = Who executes?\n"
            "```\n"
            "\n"
            "### Communication\n"
            "\n"
            "Communication determines what information flows between agents.\n"
            "\n"
            "A collaborative system may share a common context, while a hierarchical system may "
            "show each worker only the information selected by an orchestrator.\n"
            "\n"
            "### Coordination\n"
            "\n"
            "Coordination determines how execution is arranged over time:\n"
            "\n"
            "- sequentially,\n"
            "- in parallel,\n"
            "- hierarchically,\n"
            "- through revision loops,\n"
            "- through branching or routing.\n"
            "\n"
            "These four questions are more useful than starting from a framework name.\n"
            "\n"
            "[[IMAGE_NEEDED: Four Cs of multi-agent architecture | "
            "A diagram with four labeled blocks: Decision-making, Control, Communication, "
            "Coordination. Under each, show one guiding question: Who decides? Who acts? What "
            "context moves? How does execution proceed? | "
            "Learner should use these four questions as an architecture checklist]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Three core multi-agent architectures\n"
            "\n"
            "The chapter revisits three main architectures.\n"
            "\n"
            "### Agent flow\n"
            "\n"
            "Agents are arranged in an ordered sequence. Control and information move from one "
            "stage to the next.\n"
            "\n"
            "```text\n"
            "Research -> Plan -> Write\n"
            "```\n"
            "\n"
            "Strengths:\n"
            "\n"
            "- easy to understand,\n"
            "- easy to trace,\n"
            "- good for decomposable goals,\n"
            "- little central decision complexity.\n"
            "\n"
            "Weaknesses:\n"
            "\n"
            "- a failure can break the entire chain,\n"
            "- the whole sequence may run even when some steps are unnecessary,\n"
            "- limited dynamic decision-making.\n"
            "\n"
            "### Orchestrator\n"
            "\n"
            "A central agent decides which workers to call and when.\n"
            "\n"
            "```text\n"
            "               -> Research Agent\n"
            "User -> Orchestrator -> Planning Agent\n"
            "               -> Filesystem Agent\n"
            "```\n"
            "\n"
            "Strengths:\n"
            "\n"
            "- dynamic decision-making,\n"
            "- can execute only required workers,\n"
            "- convenient for user-facing systems,\n"
            "- can recover from some worker failures.\n"
            "\n"
            "Weaknesses:\n"
            "\n"
            "- more difficult to build and evaluate,\n"
            "- central planner errors affect the system,\n"
            "- needs stronger feedback and guardrails.\n"
            "\n"
            "### Collaboration\n"
            "\n"
            "Agents interact more freely and may jointly decide, critique, or negotiate.\n"
            "\n"
            "Strengths:\n"
            "\n"
            "- suitable for ambiguous or exploratory problems,\n"
            "- can combine diverse viewpoints.\n"
            "\n"
            "Weaknesses:\n"
            "\n"
            "- high token usage,\n"
            "- high latency,\n"
            "- harder evaluation,\n"
            "- more communication complexity.\n"
            "\n"
            "The chapter repeatedly recommends starting with simpler flows before introducing "
            "centralized or collaborative complexity.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Manager-worker hierarchy\n"
            "\n"
            "A manager-worker structure extends orchestration into a hierarchy.\n"
            "\n"
            "```text\n"
            "Manager\n"
            "  |\n"
            "  +--> Submanager A -> Workers\n"
            "  +--> Submanager B -> Workers\n"
            "```\n"
            "\n"
            "The manager passes commands downward. Workers retain control over execution inside "
            "their assigned responsibility.\n"
            "\n"
            "This can improve organization in large systems, but every management level adds planning "
            "cost, latency, and another place where information can be distorted.\n"
            "\n"
            "A more complicated hierarchy is useful only when the management work itself is valuable.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Communication patterns: send only what earns its place\n"
            "\n"
            "The chapter emphasizes that communication is not free.\n"
            "\n"
            "Sharing more context increases token cost, and irrelevant context can make it harder "
            "for the model to identify the information that matters.\n"
            "\n"
            "Consider a competitive-analysis system with three research agents and one synthesis agent.\n"
            "\n"
            "Each research worker may only need:\n"
            "\n"
            "- one company name,\n"
            "- the research rubric,\n"
            "- the required output schema.\n"
            "\n"
            "It does **not** necessarily need:\n"
            "\n"
            "- the full orchestrator history,\n"
            "- sibling agents' partial work,\n"
            "- every intermediate planning note.\n"
            "\n"
            "The synthesis agent has different needs: it should receive the completed research outputs.\n"
            "\n"
            "This leads to three communication strategies.\n"
            "\n"
            "### Message passing\n"
            "\n"
            "Pass a concise object or message to the next agent.\n"
            "\n"
            "Pros: focused, cheap, easy to reason about.  \n"
            "Cons: the next agent only knows what the previous one passed.\n"
            "\n"
            "### Shared thread or shared memory\n"
            "\n"
            "Every agent can see a common conversation history.\n"
            "\n"
            "Pros: rich continuity and recoverability.  \n"
            "Cons: growing token usage and context dilution.\n"
            "\n"
            "### Tool-mediated communication\n"
            "\n"
            "An agent may expose another agent or capability through MCP or a function-like interface.\n"
            "\n"
            "Pros: structured, narrow interface.  \n"
            "Cons: each exchange has tool-call overhead.\n\n"
            "\n"
            "| Pattern | Information visibility | Main benefit | Main cost |\n"
            "|---|---|---|---|\n"
            "| Message passing | Explicitly selected data | Focus and low token use | Upstream omission can hurt downstream work |\n"
            "| Shared thread | Broad shared history | Rich context | Cost and context dilution |\n"
            "| Tool exchange | Schema-controlled interface | Clear boundaries | Extra call/protocol overhead |\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Coordination strategies overview\n"
            "\n"
            "Multi-agent systems are not limited to a simple chain. The chapter describes several "
            "ways execution can be coordinated.\n"
            "\n"
            "### Sequential pipeline\n"
            "\n"
            "Agents run one after another. Use this when later stages truly depend on earlier outputs.\n"
            "\n"
            "### Parallel delegation\n"
            "\n"
            "Independent subtasks run at the same time and are merged later.\n"
            "\n"
            "### Hierarchical coordination\n"
            "\n"
            "A manager performs real planning, assigns different roles, monitors work, and reconciles results.\n"
            "\n"
            "### Iterative critique or refinement\n"
            "\n"
            "A worker creates output, a critic evaluates it, and the process repeats until the "
            "quality condition is met or a maximum number of rounds is reached.\n"
            "\n"
            "### Debate\n"
            "\n"
            "Two or more peer agents challenge each other's proposals and attempt to converge.\n"
            "\n"
            "### Voting / best-of-N\n"
            "\n"
            "Several candidate solutions are generated and a vote or judge selects among them.\n"
            "\n"
            "### Role-playing collaboration\n"
            "\n"
            "Agents adopt complementary roles such as client/developer or teacher/student and "
            "improve the task through interaction.\n"
            "\n"
            "### Conditional routing\n"
            "\n"
            "A router classifies the input and sends it to a specialized agent or workflow.\n"
            "\n"
            "### Peer-to-peer network\n"
            "\n"
            "Agents communicate without a central leader and coordinate in a decentralized manner.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Sequential versus parallel execution\n"
            "\n"
            "The easiest coordination decision is whether work is dependent or independent.\n"
            "\n"
            "### Sequential is correct when dependency exists\n"
            "\n"
            "```text\n"
            "Generate data -> Analyze data -> Summarize analysis\n"
            "```\n"
            "\n"
            "You cannot analyze data that does not yet exist.\n"
            "\n"
            "Sequential pipelines are easy to understand, but they have three important costs:\n"
            "\n"
            "1. **Latency:** total time accumulates across stages.\n"
            "2. **Fragility:** one failure can stop the pipeline.\n"
            "3. **Limited revision:** the flow is naturally one-way unless revision logic is added.\n"
            "\n"
            "### Parallel is correct when tasks are independent\n"
            "\n"
            "```text\n"
            "            -> Analyze text ---\\\n"
            "Input -----> Analyze image ----> Merge\n"
            "            -> Analyze audio ---/\n"
            "```\n"
            "\n"
            "Parallel execution can reduce wall-clock time, but it introduces merging and "
            "synchronization work.\n"
            "\n"
            "A useful test is:\n"
            "\n"
            "> Does task B need task A's result to begin?\n"
            "\n"
            "If yes, keep the dependency sequential. If no, parallel execution may be appropriate.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Parallel flow is not the same as hierarchical coordination\n"
            "\n"
            "These two patterns may look similar because both can show one component above several workers.\n"
            "\n"
            "The difference is the amount of intelligence in the manager.\n"
            "\n"
            "### Simple parallel fan-out\n"
            "\n"
            "A component splits a uniform task, runs workers, and merges results.\n"
            "\n"
            "```text\n"
            "Split -> Workers -> Aggregate\n"
            "```\n"
            "\n"
            "The central step could often be replaced with ordinary fan-out/fan-in code.\n"
            "\n"
            "### Hierarchical coordination\n"
            "\n"
            "The orchestrator performs meaningful planning:\n"
            "\n"
            "- chooses different subtasks,\n"
            "- assigns role-specific instructions,\n"
            "- supervises execution,\n"
            "- reconciles conflicting outputs,\n"
            "- adjusts the plan.\n"
            "\n"
            "A useful test from the chapter is:\n"
            "\n"
            "> If the orchestrator could be replaced by a simple split-and-merge primitive, it is probably parallel flow rather than true hierarchical coordination.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Critique, debate, and refinement loops\n"
            "\n"
            "Revision loops are useful when the first plausible answer is not good enough.\n"
            "\n"
            "### Asymmetric worker-critic loop\n"
            "\n"
            "```text\n"
            "Worker -> Candidate -> Critic\n"
            "  ^                    |\n"
            "  |------ feedback ----|\n"
            "```\n"
            "\n"
            "The critic has authority to accept or reject the worker's output.\n"
            "\n"
            "This fits tasks with a measurable quality bar, such as:\n"
            "\n"
            "- code passing tests,\n"
            "- a plan satisfying a rubric,\n"
            "- a response meeting formatting constraints.\n"
            "\n"
            "### Symmetric debate\n"
            "\n"
            "Peer agents propose and challenge ideas without one fixed authority.\n"
            "\n"
            "This can help when the task is exploratory or ambiguous.\n"
            "\n"
            "### Stopping conditions are essential\n"
            "\n"
            "Every revision loop needs an exit condition, such as:\n"
            "\n"
            "- maximum rounds,\n"
            "- critic approval,\n"
            "- convergence,\n"
            "- no meaningful change.\n"
            "\n"
            "Without a hard maximum, an agent loop can consume tokens indefinitely.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Ensembles, routing, role-play, and peer networks\n"
            "\n"
            "### Voting or best-of-N\n"
            "\n"
            "Generate several answers and select one using majority vote, weighted voting, or a judge.\n"
            "\n"
            "This only helps if the candidates provide meaningful diversity. Several identical "
            "agents with identical prompts may reproduce the same mistake.\n"
            "\n"
            "### Role-playing collaboration\n"
            "\n"
            "Complementary roles create useful interaction. A client agent can clarify requirements "
            "while a developer agent implements them.\n"
            "\n"
            "The pattern adds little value if the roles do not contribute distinct information.\n"
            "\n"
            "### Conditional routing\n"
            "\n"
            "A router chooses which expert should handle the input.\n"
            "\n"
            "```text\n"
            "User request -> Router -> Billing Agent\n"
            "                      -> Technical Agent\n"
            "                      -> Legal Agent\n"
            "```\n"
            "\n"
            "Routing is valuable when the task distribution is heterogeneous. It is unnecessary "
            "when one general agent already handles all inputs effectively.\n"
            "\n"
            "### Peer-to-peer networks\n"
            "\n"
            "Peers communicate without a central coordinator. This can improve robustness, but "
            "it makes global control, debugging, and conflict resolution harder.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Agency versus system ownership\n"
            "\n"
            "Agent systems need enough freedom to make useful decisions, but unrestricted autonomy "
            "is rarely appropriate for production systems.\n"
            "\n"
            "The chapter frames agency and constraint as a spectrum.\n"
            "\n"
            "### Lower-stakes work can tolerate more agency\n"
            "\n"
            "Examples include exploratory analysis and draft-quality internal research.\n"
            "\n"
            "### Higher-stakes work needs stronger boundaries\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- irreversible actions,\n"
            "- customer-facing outputs,\n"
            "- regulated workflows,\n"
            "- production changes.\n"
            "\n"
            "Useful constraint points include:\n"
            "\n"
            "- allowed tools,\n"
            "- output schemas,\n"
            "- action budgets,\n"
            "- deterministic business rules,\n"
            "- human approval.\n"
            "\n"
            "A practical strategy is to begin with the least autonomy necessary and loosen the "
            "boundaries only after reliability has been demonstrated.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. When a single agent should become a flow\n"
            "\n"
            "A single agent is often the correct starting point. Decomposition becomes useful when "
            "the agent starts becoming overloaded.\n"
            "\n"
            "The chapter identifies three strong signals.\n"
            "\n"
            "### Overload\n"
            "\n"
            "The agent has too many tools, too much instruction text, or overlapping tool descriptions.\n"
            "\n"
            "### Specialization\n"
            "\n"
            "Different parts of the task benefit from focused roles.\n"
            "\n"
            "### Cost and latency\n"
            "\n"
            "A specialized agent can receive a smaller prompt, smaller tool list, and narrower context.\n"
            "\n"
            "Suppose one research assistant currently owns:\n"
            "\n"
            "- research-source tools,\n"
            "- planning tools,\n"
            "- filesystem tools.\n"
            "\n"
            "A natural decomposition is:\n"
            "\n"
            "```text\n"
            "Research Agent -> Planning Agent -> Filesystem Agent\n"
            "```\n"
            "\n"
            "Each agent now has one primary responsibility.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Building a simple agent-to-agent flow\n"
            "\n"
            "A straightforward flow manually executes each agent and passes the previous output forward.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "research_result = await Runner.run(research_agent, goal)\n"
            "\n"
            "planning_result = await Runner.run(\n"
            "    planning_agent,\n"
            "    research_result.final_output,\n"
            ")\n"
            "\n"
            "filesystem_result = await Runner.run(\n"
            "    filesystem_agent,\n"
            "    planning_result.final_output,\n"
            ")\n"
            "```\n"
            "\n"
            "The important design principle is **role-first decomposition**:\n"
            "\n"
            "1. Identify responsibilities inside the monolithic agent.\n"
            "2. Create one focused role for each responsibility.\n"
            "3. Give each role only the tools it needs.\n"
            "4. Define the data contract between stages.\n"
            "\n"
            "This makes the system more predictable and easier to inspect.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Move hard rules out of the LLM\n"
            "\n"
            "LLMs make probabilistic decisions. Some workflow decisions should not be probabilistic.\n"
            "\n"
            "Suppose the research step returns zero sources. A hard system requirement might be:\n"
            "\n"
            "```text\n"
            "If no sources exist, do not create a research plan.\n"
            "```\n"
            "\n"
            "Instead of asking the model to remember this rule, encode it in deterministic code.\n"
            "\n"
            "```python\n"
            "sources = result.final_output.research_sources\n"
            "\n"
            "if sources:\n"
            "    # run the planning agent\n"
            "    ...\n"
            "else:\n"
            "    research_plan = \"No research sources found.\"\n"
            "```\n"
            "\n"
            "### Why typing matters here\n"
            "\n"
            "A typed result such as:\n"
            "\n"
            "```python\n"
            "class ResearchSourcesModel(BaseModel):\n"
            "    research_sources: list[str]\n"
            "```\n"
            "\n"
            "makes the decision easy and reliable. Without typing, code would need to parse arbitrary prose.\n"
            "\n"
            "This produces a useful rule:\n"
            "\n"
            "> If the decision must be repeatable and expressible as code, prefer deterministic code over LLM judgment.\n"
            "\n"
            "{{exercise:M01.L04.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Three ways to pass work between agents\n"
            "\n"
            "The chapter presents three broad communication styles for agent flows.\n"
            "\n"
            "### Shared conversational flow\n"
            "\n"
            "Agents work on one shared thread.\n"
            "\n"
            "Benefit: continuity is automatic.  \n"
            "Cost: every agent may see noise it does not need.\n"
            "\n"
            "### Explicit pass-off in code\n"
            "\n"
            "Your application controls exactly what is sent into each `Runner.run(...)` call.\n"
            "\n"
            "Benefit: maximum control.  \n"
            "Cost: more orchestration code.\n"
            "\n"
            "### SDK handoffs\n"
            "\n"
            "The framework transfers control between configured agents.\n"
            "\n"
            "Benefit: less manual transition code.  \n"
            "Cost: relationships become more implicit and agents must know their handoff targets.\n\n"
            "\n"
            "The right choice depends on whether you prioritize speed of development or fine-grained control.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Agent handoffs in the SDK\n"
            "\n"
            "A handoff lets one agent transfer control internally to another.\n"
            "\n"
            "A simplified pattern is:\n"
            "\n"
            "```python\n"
            "research_agent.handoffs = [thinking_agent]\n"
            "thinking_agent.handoffs = [filesystem_agent]\n"
            "\n"
            "result = await Runner.run(\n"
            "    research_agent,\n"
            "    goal,\n"
            "    max_turns=25,\n"
            ")\n"
            "```\n"
            "\n"
            "The prompts also need to tell agents when to hand off.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Research Agent:\n"
            "Always hand off to the Thinking Agent after finding sources.\n"
            "\n"
            "Thinking Agent:\n"
            "Always hand off to the Filesystem Agent after creating the plan.\n"
            "```\n"
            "\n"
            "This reduces explicit orchestration code, but creates a new dependency: the agents now "
            "need awareness of their positions in the flow.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Visualizing and tracing agent flows\n"
            "\n"
            "As flows grow, code alone stops being an effective mental model.\n"
            "\n"
            "The chapter demonstrates graph visualization with a pattern like:\n"
            "\n"
            "```python\n"
            "from agents.extensions.visualization import draw_graph\n"
            "\n"
            "draw_graph(research_agent).view()\n"
            "```\n"
            "\n"
            "A graph helps reveal:\n"
            "\n"
            "- which agents can hand off to which,\n"
            "- unexpected connections,\n"
            "- missing paths,\n"
            "- role boundaries.\n"
            "\n"
            "Tracing complements the graph by showing runtime details:\n"
            "\n"
            "- actual transitions,\n"
            "- model calls,\n"
            "- tool calls,\n"
            "- latency,\n"
            "- repeated loops.\n"
            "\n"
            "### Naming matters\n"
            "\n"
            "Agent names become identifiers in traces, visualizations, and routing. Large systems "
            "benefit from stable naming conventions and eventually from an agent registry that "
            "tracks definitions and dependencies.\n"
            "\n"
            "[[IMAGE_NEEDED: Agent flow graph and trace relationship | "
            "Show a static graph Research -> Planning -> Filesystem beside a runtime timeline "
            "showing actual calls, tool use, latency, and a handoff event | "
            "Learner should notice that a graph documents possible structure while a trace shows what actually happened]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Monitor handoffs with callbacks\n"
            "\n"
            "A default handoff may not make the transferred data obvious. The SDK's handoff wrapper "
            "can attach an observation callback.\n"
            "\n"
            "A simplified pattern is:\n"
            "\n"
            "```python\n"
            "async def research_handoff(ctx, sources: ResearchSourcesModel):\n"
            "    print(\"Handoff sources:\", sources.research_sources)\n"
            "\n"
            "agent_handoff = handoff(\n"
            "    agent=thinking_agent,\n"
            "    on_handoff=research_handoff,\n"
            "    input_type=ResearchSourcesModel,\n"
            ")\n"
            "\n"
            "research_agent.handoffs = [agent_handoff]\n"
            "```\n"
            "\n"
            "The callback is useful for:\n"
            "\n"
            "- logging,\n"
            "- debugging,\n"
            "- metrics,\n"
            "- inspecting why a handoff occurred.\n"
            "\n"
            "The chapter gives a useful division of responsibility:\n"
            "\n"
            "> Use callbacks to observe. Use guardrails to block or correct invalid data.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Guardrails are semantic circuit breakers\n"
            "\n"
            "A guardrail is more than a content filter. In the chapter, it is treated as a control "
            "that can stop execution before an invalid or risky result moves further through the system.\n"
            "\n"
            "Guardrails may validate:\n"
            "\n"
            "- user input,\n"
            "- agent output,\n"
            "- an agent-to-agent transfer,\n"
            "- a high-stakes action boundary.\n"
            "\n"
            "### Use the cheapest reliable validation first\n"
            "\n"
            "The chapter distinguishes several validation layers.\n"
            "\n"
            "#### Deterministic checks\n"
            "\n"
            "- schemas,\n"
            "- type checks,\n"
            "- assertions,\n"
            "- business-rule predicates,\n"
            "- pattern matching.\n"
            "\n"
            "Use these when the rule can be expressed precisely.\n"
            "\n"
            "#### Small classifiers\n"
            "\n"
            "Useful for structured risks such as PII, toxicity, or prompt-injection detection.\n"
            "\n"
            "#### LLM guardrails\n"
            "\n"
            "Useful when the rule is semantic or fuzzy, such as \"Is this plan sufficiently detailed?\"\n"
            "\n"
            "LLM-based validation adds model calls, latency, and cost, and the validator can make "
            "mistakes too. Therefore it should not automatically replace cheaper deterministic checks.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Input and output guardrails\n"
            "\n"
            "A guardrail function returns information plus a Boolean tripwire signal.\n"
            "\n"
            "A simplified input example:\n"
            "\n"
            "```python\n"
            "@input_guardrail\n"
            "async def research_guardrail(ctx, agent, input):\n"
            "    forbidden = \"forbidden topic\" in str(input)\n"
            "\n"
            "    return GuardrailFunctionOutput(\n"
            "        output_info=f\"user asked: {input}\",\n"
            "        tripwire_triggered=forbidden,\n"
            "    )\n"
            "```\n"
            "\n"
            "A simplified output example:\n"
            "\n"
            "```python\n"
            "@output_guardrail\n"
            "async def output_guardrail(ctx, agent, output):\n"
            "    too_short = len(output.research_plan) < 100\n"
            "\n"
            "    return GuardrailFunctionOutput(\n"
            "        output_info=\"research plan validation\",\n"
            "        tripwire_triggered=too_short,\n"
            "    )\n"
            "```\n"
            "\n"
            "When the tripwire fires, the runtime raises the corresponding guardrail exception.\n\n"
            "\n"
            "The important pattern is not the example's exact string or length rule. The pattern is:\n"
            "\n"
            "```text\n"
            "Input/output -> validate -> pass OR trip -> recovery path\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Using an agent as a guardrail\n"
            "\n"
            "Some validation rules are hard to express with deterministic code.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "\"Is this research plan sufficiently detailed and useful?\"\n"
            "```\n"
            "\n"
            "An LLM-powered guardrail agent can evaluate a structured input and return a typed result.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Primary agent output\n"
            "      |\n"
            "      v\n"
            "Guardrail agent\n"
            "      |\n"
            "      +--> pass\n"
            "      +--> trip\n"
            "```\n"
            "\n"
            "This is flexible because changing the policy can sometimes be as simple as changing "
            "the validator instructions. But it also adds another probabilistic component.\n"
            "\n"
            "A strong production design layers deterministic validation and semantic validation "
            "instead of expecting one LLM validator to guarantee correctness.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Three important handoff failure modes\n"
            "\n"
            "Agent boundaries are security and reliability boundaries.\n"
            "\n"
            "The chapter highlights three recurring failure modes.\n"
            "\n"
            "### Shape failure\n"
            "\n"
            "The sending agent provides data in a structure the receiving agent does not expect.\n"
            "\n"
            "Mitigation: typed schemas and validation.\n"
            "\n"
            "### Context leakage\n"
            "\n"
            "Too much upstream history, internal planning, or unrelated context is passed to the next agent.\n"
            "\n"
            "Mitigation: explicit pass-off objects and minimal context.\n"
            "\n"
            "### Instruction injection\n"
            "\n"
            "An upstream tool result or agent output contains text that the receiving agent treats "
            "as authoritative instructions.\n"
            "\n"
            "Mitigation: treat transferred content as untrusted data, validate high-risk boundaries, "
            "and separate system instructions from payload data.\n"
            "\n"
            "High-stakes handoffs deserve the strongest validation, especially before writes, sends, "
            "deletes, or other irreversible actions.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Guardrail recovery and bounded retries\n"
            "\n"
            "A tripped guardrail does not always have to terminate the workflow immediately. In some "
            "cases, feedback can be sent back to the responsible agent for another attempt.\n"
            "\n"
            "```python\n"
            "max_retries = 3\n"
            "final_output = first_input\n"
            "\n"
            "for attempt in range(max_retries):\n"
            "    try:\n"
            "        result = await Runner.run(planning_agent, final_output)\n"
            "        final_output = result.final_output.research_plan\n"
            "        break\n"
            "    except OutputGuardrailTripwireTriggered as exc:\n"
            "        final_output = exc.guardrail_result.output.output_info\n"
            "else:\n"
            "    final_output = \"Plan generation failed after retries.\"\n"
            "```\n"
            "\n"
            "### Why the retry count must be bounded\n"
            "\n"
            "Retries increase:\n"
            "\n"
            "- token usage,\n"
            "- latency,\n"
            "- cost,\n"
            "- the chance of loops.\n"
            "\n"
            "For transient infrastructure failures such as rate limits or network errors, the "
            "chapter recommends exponential backoff with jitter rather than immediate synchronized retries.\n"
            "\n"
            "{{exercise:M01.L04.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Evolving a flow into an orchestrator\n"
            "\n"
            "Architectures can evolve. A sequential flow can later replace one node with an orchestrator.\n"
            "\n"
            "One approach is to expose specialized agents as tools:\n"
            "\n"
            "```python\n"
            "@function_tool\n"
            "async def research_worker(instructions: str):\n"
            "    result = await Runner.run(research_agent, instructions)\n"
            "    return result.final_output\n"
            "```\n"
            "\n"
            "Then the orchestrator can decide whether and when to delegate.\n"
            "\n"
            "```text\n"
            "Orchestrator\n"
            "  +--> research worker\n"
            "  +--> filesystem worker\n"
            "  +--> planning capability\n"
            "```\n"
            "\n"
            "This increases flexibility, but it also makes output more dependent on the orchestrator's "
            "planning quality. The chapter therefore recommends gaining experience with successful "
            "flows before adding orchestration complexity.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. A practical architecture playbook\n"
            "\n"
            "When designing a multi-agent system, work through these questions in order.\n"
            "\n"
            "### Step 1 — Start with one agent\n"
            "\n"
            "Do not distribute work unless you have a real reason.\n"
            "\n"
            "### Step 2 — Identify overload or natural roles\n"
            "\n"
            "Split responsibilities where prompts, tools, or objectives are clearly different.\n"
            "\n"
            "### Step 3 — Choose the communication boundary\n"
            "\n"
            "Pass only the information each worker needs.\n"
            "\n"
            "### Step 4 — Decide where authority lives\n"
            "\n"
            "Who chooses the next step? Who is allowed to execute it?\n"
            "\n"
            "### Step 5 — Use deterministic code for hard rules\n"
            "\n"
            "Do not ask an LLM to probabilistically enforce a rule that ordinary code can enforce exactly.\n"
            "\n"
            "### Step 6 — Type your handoffs\n"
            "\n"
            "Make outputs machine-checkable before they become downstream inputs.\n"
            "\n"
            "### Step 7 — Add traces early\n"
            "\n"
            "Observe what actually happens rather than reasoning only from your code.\n"
            "\n"
            "### Step 8 — Guard high-risk boundaries\n"
            "\n"
            "Validate writes, sends, irreversible actions, and data crossing trust boundaries.\n"
            "\n"
            "### Step 9 — Bound retries and budgets\n"
            "\n"
            "Every loop needs a stopping condition.\n"
            "\n"
            "### Step 10 — Add orchestration only if it solves a real limitation\n"
            "\n"
            "Architecture should follow the problem, not the desire to use more agents.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: More agents automatically improve quality\n"
            "\n"
            "> More agents also add communication, cost, latency, and failure modes.\n"
            "\n"
            "Use additional agents only when specialization, parallelism, routing, evaluation, or "
            "coordination provides real value.\n"
            "\n"
            "### Misconception 2: Decision-making and control are the same thing\n"
            "\n"
            "> An agent may decide without executing, or execute without choosing what happens next.\n"
            "\n"
            "Separating these authorities is a powerful architecture tool.\n"
            "\n"
            "### Misconception 3: Sharing all context is safest\n"
            "\n"
            "> Excess context increases cost and can reduce focus.\n"
            "\n"
            "Send each agent the context required for its responsibility.\n"
            "\n"
            "### Misconception 4: A handoff callback is a guardrail\n"
            "\n"
            "> A callback observes; a guardrail enforces.\n"
            "\n"
            "Use the right mechanism for the job.\n"
            "\n"
            "### Misconception 5: LLM guardrails are always better than code checks\n"
            "\n"
            "> Deterministic rules are cheaper and more reliable when the condition is explicit.\n"
            "\n"
            "Use semantic LLM validation only where understanding is actually required.\n"
            "\n"
            "### Misconception 6: Retries should continue until the agent succeeds\n"
            "\n"
            "> Unbounded retries create runaway cost and latency.\n"
            "\n"
            "Every retry loop needs a maximum and a clear failure path.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Decision-making | Authority to choose what happens next |\n"
            "| Control | Authority to execute actions or tools |\n"
            "| Communication | Rules governing what information moves between agents |\n"
            "| Coordination | How agent execution is arranged over time |\n"
            "| Agent flow | Ordered chain of specialized agents |\n"
            "| Orchestrator | Central agent that decides which workers to delegate to |\n"
            "| Collaboration | Pattern where agents interact more freely as peers or teammates |\n"
            "| Manager-worker | Hierarchical delegation structure with managers and specialized workers |\n"
            "| Message passing | Explicit transfer of selected data between agents |\n"
            "| Shared thread | Common conversation/context visible to several agents |\n"
            "| Parallel delegation | Independent subtasks executed concurrently |\n"
            "| Iterative critique | Worker output repeatedly evaluated by a critic |\n"
            "| Debate | Peer agents challenge one another toward a result |\n"
            "| Best-of-N | Generate multiple candidates and select among them |\n"
            "| Conditional routing | Choose an agent/workflow based on input classification |\n"
            "| Handoff | Transfer of execution control from one agent to another |\n"
            "| Pass-off | Explicit application-controlled transfer of selected data |\n"
            "| Guardrail | Validation boundary that can trip and stop or redirect execution |\n"
            "| Tripwire | Boolean guardrail condition that triggers a guardrail failure |\n"
            "| Typed I/O | Structured validated data contract between workflow stages |\n"
            "| Context leakage | Passing unnecessary upstream information into a downstream agent |\n"
            "| Instruction injection | Untrusted content influencing downstream agent instructions |\n"
            "| Backoff with jitter | Retry strategy that increases delay and randomizes timing between attempts |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can a multi-agent system be worse than a single agent?\n"
            "2. What is the difference between decision-making and control?\n"
            "3. Why should communication boundaries be designed deliberately?\n"
            "4. When is a sequential pipeline appropriate?\n"
            "5. When is parallel delegation appropriate?\n"
            "6. How is hierarchical coordination different from simple fan-out/fan-in?\n"
            "7. What separates critique from debate?\n"
            "8. Why does best-of-N require genuine diversity?\n"
            "9. What signals indicate a monolithic agent should be decomposed?\n"
            "10. Why should hard business rules be implemented outside an LLM where possible?\n"
            "11. What is the difference between shared-thread, pass-off, and SDK handoff communication?\n"
            "12. What information can graph visualization reveal?\n"
            "13. What information can runtime traces reveal?\n"
            "14. Why are callbacks not a substitute for guardrails?\n"
            "15. When should you prefer schema validation over an LLM guardrail?\n"
            "16. What are shape failure, context leakage, and instruction injection?\n"
            "17. Why must retries be bounded?\n"
            "18. When does evolving a flow into an orchestrator make sense?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A good multi-agent system is not defined by how many agents it contains. It is "
            "defined by deliberate boundaries: who decides, who executes, what context crosses "
            "between roles, how execution is coordinated, which decisions are deterministic, and "
            "where validation stops bad state before it spreads through the flow.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-multi-agent", "title": "Why multi-agent systems appeared", "order": 1},
            {"id": "four-cs", "title": "The four architecture questions", "order": 2},
            {"id": "core-architectures", "title": "Three core multi-agent architectures", "order": 3},
            {"id": "manager-worker", "title": "Manager-worker hierarchy", "order": 4},
            {"id": "communication-patterns", "title": "Communication patterns", "order": 5},
            {"id": "coordination-strategies", "title": "Coordination strategies overview", "order": 6},
            {"id": "sequential-vs-parallel", "title": "Sequential versus parallel execution", "order": 7},
            {"id": "hierarchy-vs-parallel", "title": "Parallel flow versus hierarchy", "order": 8},
            {"id": "iterative-patterns", "title": "Critique, debate, and refinement loops", "order": 9},
            {"id": "ensembles-routing-peers", "title": "Ensembles, routing, role-play, and peer networks", "order": 10},
            {"id": "agency-spectrum", "title": "Agency versus system ownership", "order": 11},
            {"id": "when-to-decompose", "title": "When a single agent should become a flow", "order": 12},
            {"id": "build-flow", "title": "Building a simple agent-to-agent flow", "order": 13},
            {"id": "deterministic-decisions", "title": "Move hard rules out of the LLM", "order": 14},
            {"id": "handoff-patterns", "title": "Three ways to pass work between agents", "order": 15},
            {"id": "sdk-handoffs", "title": "Agent handoffs in the SDK", "order": 16},
            {"id": "visualization", "title": "Visualizing and tracing agent flows", "order": 17},
            {"id": "monitor-handoffs", "title": "Monitor handoffs with callbacks", "order": 18},
            {"id": "guardrail-concept", "title": "Guardrails are semantic circuit breakers", "order": 19},
            {"id": "input-output-guardrails", "title": "Input and output guardrails", "order": 20},
            {"id": "agent-guardrails", "title": "Using an agent as a guardrail", "order": 21},
            {"id": "handoff-failures", "title": "Three important handoff failure modes", "order": 22},
            {"id": "guardrail-retry", "title": "Guardrail recovery and bounded retries", "order": 23},
            {"id": "flow-to-orchestrator", "title": "Evolving a flow into an orchestrator", "order": 24},
            {"id": "architecture-playbook", "title": "A practical architecture playbook", "order": 25},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",

            "title": "Refactor a Monolithic Agent into a Typed Flow",

            "lesson_code": "M01.L04",

            "section_id": "deterministic-decisions",

            "placement": "after_section",

            "description": (
                "Practice splitting a tool-heavy agent into focused roles and "
                "moving a hard workflow decision into deterministic code."
            ),

            "instructions": (
                "Scenario: one agent currently finds research sources, creates a research plan, "
                "and writes the plan to disk.\n"
                "1. Split it into ResearchAgent, PlanningAgent, and FilesystemAgent.\n"
                "2. Give each agent only the tools required for its role.\n"
                "3. Create a `ResearchSourcesModel` with `research_sources: list[str]`.\n"
                "4. Make ResearchAgent return this typed model.\n"
                "5. After the first run, add deterministic code: if the list is empty, skip PlanningAgent.\n"
                "6. If sources exist, pass only the goal and source list to PlanningAgent.\n"
                "7. Pass only the finished plan and destination requirement to FilesystemAgent.\n"
                "8. Draw the resulting flow as text or a diagram.\n"
                "9. Explain one token-cost benefit and one reliability benefit of the decomposition.\n"
                "10. Identify one failure mode that still remains."
            ),

            "expected_output": (
                "A three-agent flow design or code sample with typed research output, "
                "a deterministic branch, minimal pass-off objects, and a short trade-off analysis."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-decomposition",
                "typed-output",
                "deterministic-control",
                "message-passing",
                "tool-scoping",
            ],
        },

        {
            "id": "M01.L04.EX02",

            "title": "Protect an Agent Handoff with Guardrails and Retry",

            "lesson_code": "M01.L04",

            "section_id": "guardrail-retry",

            "placement": "after_section",

            "description": (
                "Practice validation at an agent boundary and implement a bounded "
                "recovery loop for low-quality output."
            ),

            "instructions": (
                "Use a PlanningAgent that outputs a `ResearchPlanModel` containing "
                "`research_plan: str` and `is_detailed: bool`.\n"
                "1. Add a deterministic schema/type check first.\n"
                "2. Add an output guardrail that rejects plans below a chosen quality threshold.\n"
                "3. Implement a maximum of two retries.\n"
                "4. Feed guardrail feedback into the next attempt.\n"
                "5. After the final failed attempt, return a clear static failure result.\n"
                "6. Add a handoff callback that logs the validated payload before the FilesystemAgent receives it.\n"
                "7. Explain why the callback is observational while the guardrail is enforcing.\n"
                "8. Identify how you would defend against instruction injection inside the plan text.\n"
                "9. State one case where an LLM guardrail is justified and one where ordinary code is better.\n"
                "10. Explain why the retry loop must not be infinite."
            ),

            "expected_output": (
                "Guardrail and retry pseudocode or runnable code plus an explanation "
                "of validation order, recovery behavior, callback monitoring, and security."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "guardrails",
                "retry-control",
                "handoff-monitoring",
                "input-validation",
                "instruction-injection",
                "failure-recovery",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Architecting and Building Multi-Agent Systems — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",
                "section_id": "four-cs",
                "question": "What is the best description of control in a multi-agent system?",
                "options": [
                    "The authority to decide which action should happen next",
                    "The authority to execute work or call tools",
                    "The amount of conversation history available",
                    "The number of agents in the system",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter separates decision-making from control. Decision-making "
                    "chooses; control executes."
                ),
            },

            {
                "id": "M01.L04.Q02",
                "section_id": "core-architectures",
                "question": "Which architecture centralizes decision-making in one coordinating agent?",
                "options": [
                    "Sequential flow",
                    "Orchestrator",
                    "Peer-to-peer collaboration",
                    "Simple message passing",
                ],
                "correct": 1,
                "explanation": (
                    "An orchestrator owns central delegation and decides which workers "
                    "should execute tasks."
                ),
            },

            {
                "id": "M01.L04.Q03",
                "section_id": "communication-patterns",
                "question": "Why might passing the full conversation history to every worker be harmful?",
                "options": [
                    "Workers cannot read text",
                    "It increases token cost and can dilute relevant context",
                    "It prevents typed outputs",
                    "It forces all work to run sequentially",
                ],
                "correct": 1,
                "explanation": (
                    "Shared context can be useful, but irrelevant history increases cost and "
                    "makes relevant information harder to select."
                ),
            },

            {
                "id": "M01.L04.Q04",
                "section_id": "sequential-vs-parallel",
                "question": "When is a sequential pipeline the better coordination choice?",
                "options": [
                    "When all tasks are fully independent",
                    "When each stage depends on the previous stage's output",
                    "Whenever low latency is the only goal",
                    "Whenever agents have different names",
                ],
                "correct": 1,
                "explanation": (
                    "Dependency is the key reason to serialize stages."
                ),
            },

            {
                "id": "M01.L04.Q05",
                "section_id": "hierarchy-vs-parallel",
                "question": "What distinguishes hierarchical coordination from simple parallel fan-out?",
                "options": [
                    "Hierarchy cannot run tasks concurrently",
                    "The manager performs meaningful planning, supervision, and reconciliation",
                    "Parallel fan-out always uses more agents",
                    "Hierarchy does not use specialized workers",
                ],
                "correct": 1,
                "explanation": (
                    "A true orchestrator contributes planning and management beyond simply "
                    "splitting work and merging results."
                ),
            },

            {
                "id": "M01.L04.Q06",
                "section_id": "iterative-patterns",
                "question": "What is the main difference between critique and debate?",
                "options": [
                    "Critique uses no agents",
                    "Critique is typically hierarchical worker-critic evaluation, while debate is peer-to-peer",
                    "Debate cannot use stopping conditions",
                    "Critique always runs in parallel",
                ],
                "correct": 1,
                "explanation": (
                    "A critic gates a worker's output; debate involves peers challenging one another."
                ),
            },

            {
                "id": "M01.L04.Q07",
                "section_id": "deterministic-decisions",
                "question": (
                    "A workflow must never run PlanningAgent when the source list is empty. "
                    "Where should this rule preferably live?"
                ),
                "options": [
                    "Only in the LLM prompt",
                    "In deterministic application code",
                    "Inside the final FilesystemAgent",
                    "In a higher temperature setting",
                ],
                "correct": 1,
                "explanation": (
                    "A hard, precisely expressible requirement should be implemented "
                    "deterministically rather than left to probabilistic judgment."
                ),
            },

            {
                "id": "M01.L04.Q08",
                "section_id": "handoff-patterns",
                "question": "Which communication approach provides the most explicit control over exactly what each agent receives?",
                "options": [
                    "Shared conversation thread",
                    "Explicit pass-off in application code",
                    "Unbounded collaboration",
                    "Voting",
                ],
                "correct": 1,
                "explanation": (
                    "Explicit pass-off lets the application construct the exact input for each stage."
                ),
            },

            {
                "id": "M01.L04.Q09",
                "section_id": "monitor-handoffs",
                "question": "What is the chapter's recommended distinction between callbacks and guardrails?",
                "options": [
                    "Callbacks block bad data; guardrails only log it",
                    "Callbacks observe and log; guardrails enforce and can stop execution",
                    "They are identical mechanisms",
                    "Guardrails only visualize graphs",
                ],
                "correct": 1,
                "explanation": (
                    "Callbacks are useful for observation. Guardrails are the enforcement boundary."
                ),
            },

            {
                "id": "M01.L04.Q10",
                "section_id": "guardrail-concept",
                "question": "When is an LLM-based guardrail most justified?",
                "options": [
                    "When checking whether an integer is greater than zero",
                    "When validation requires semantic judgment that deterministic rules cannot express well",
                    "Whenever a regex could solve the problem",
                    "For every agent call regardless of cost",
                ],
                "correct": 1,
                "explanation": (
                    "Semantic quality judgments are the case where an LLM validator earns its extra cost."
                ),
            },

            {
                "id": "M01.L04.Q11",
                "section_id": "handoff-failures",
                "question": "Which failure mode occurs when too much irrelevant upstream history reaches a downstream agent?",
                "options": [
                    "Shape failure",
                    "Context leakage",
                    "Parallelism",
                    "Voting collapse",
                ],
                "correct": 1,
                "explanation": (
                    "Context leakage passes excessive or inappropriate upstream state across the boundary."
                ),
            },

            {
                "id": "M01.L04.Q12",
                "section_id": "guardrail-retry",
                "question": "Why should a guardrail retry loop have a fixed maximum?",
                "options": [
                    "Because agents cannot run twice",
                    "To prevent runaway cost, latency, and endless loops",
                    "Because typed outputs stop working after two calls",
                    "To force every attempt to succeed",
                ],
                "correct": 1,
                "explanation": (
                    "Retries consume additional calls and may still fail, so the workflow needs "
                    "a bounded failure path."
                ),
            },

            {
                "id": "M01.L04.Q13",
                "section_id": "architecture-playbook",
                "type": "open",
                "question": (
                    "Design a multi-agent research workflow from scratch. Identify who owns "
                    "decision-making and control, what each agent receives, which steps are "
                    "sequential or parallel, one deterministic checkpoint, one high-risk handoff "
                    "that deserves a guardrail, and one bounded recovery strategy."
                ),
            },
        ],

        "passing_score": 70,
    },
}
