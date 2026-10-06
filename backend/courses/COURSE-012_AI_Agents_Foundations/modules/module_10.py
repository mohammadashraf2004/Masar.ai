"""M01.L10 — Exploring the Cognitive Agent That Thinks, Monitors, and Adapts.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 10, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L10"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how to move beyond isolated reasoning patterns into a modular "
    "cognitive agent architecture that understands tasks, chooses strategies, "
    "monitors its own progress, adapts when evidence changes, remembers past "
    "experience, detects uncertainty, and knows when to stop or escalate."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Exploring the Cognitive Agent That Thinks, Monitors, and Adapts",

    "slug": "ai-agents-m01-l10",

    "description": (
        "Build a cognitive agent architecture from specialized modules connected "
        "through a shared workspace. Learn cognition, metacognition, dynamic "
        "attention routing, memory, confidence gating, stagnation detection, "
        "knowledge-boundary awareness, and practical cognitive evaluation."
    ),

    "order": 10,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.75,

    "skill_tags": [
        "cognitive-agents",
        "metacognition",
        "cognitive-workspace",
        "perception",
        "planning",
        "execution",
        "evaluation",
        "attention-routing",
        "memory",
        "confidence-gating",
        "stagnation-detection",
        "knowledge-boundaries",
        "agentic-loop",
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
        "M01.L09",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Exploring the Cognitive Agent That Thinks, Monitors, and Adapts",

        "content": (
            "# Exploring the Cognitive Agent That Thinks, Monitors, and Adapts\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L10  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 10. "
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
            "- Explain why stacking reasoning patterns does not automatically create a better agent.\n"
            "- Identify five common failure modes of capable-but-non-cognitive agents.\n"
            "- Distinguish cognition from metacognition in practical engineering terms.\n"
            "- Explain task decomposition, dependency reasoning, compositional tool use, and model updating.\n"
            "- Explain confidence calibration, stagnation detection, and knowledge-boundary awareness.\n"
            "- Describe how Minsky, Baars, and Kahneman motivate the architecture in the chapter.\n"
            "- Explain the role of a shared cognitive workspace.\n"
            "- Build the mental model for perception, planning, execution, evaluation, attention, and memory modules.\n"
            "- Explain fast-path versus full-cycle processing.\n"
            "- Explain how memory influences planning without replacing it.\n"
            "- Describe why the evaluation module is metacognitive rather than merely reflective.\n"
            "- Implement deterministic attention routing from workspace signals.\n"
            "- Explain how cognitive architecture layers inside the agentic loop.\n"
            "- Apply confidence gating before presenting an answer.\n"
            "- Detect stagnation and trigger strategy pivoting.\n"
            "- Detect when an agent is operating near or beyond its knowledge boundary.\n"
            "- Explain emergent behaviors such as curiosity, adaptive persistence, selective depth, and graceful degradation.\n"
            "- Measure cognitive efficiency, confidence calibration, adaptation rate, and knowledge-boundary accuracy.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why reasoning patterns alone are not enough\n"
            "\n"
            "By this point, an agent can already use patterns such as:\n"
            "\n"
            "- Chain-of-Thought-style reasoning,\n"
            "- ReAct,\n"
            "- Tree-of-Thought,\n"
            "- Reflexion,\n"
            "- Sequential Thinking,\n"
            "- long-horizon agentic loops.\n"
            "\n"
            "These are valuable **reasoning primitives**. But there is still a missing decision:\n"
            "\n"
            "```text\n"
            "Which reasoning strategy should the agent use for this problem,\n"
            "and how should it know when that strategy is failing?\n"
            "```\n"
            "\n"
            "Simply stacking every reasoning pattern on top of every task creates complexity, cost, and latency.\n"
            "\n"
            "The chapter therefore moves from isolated reasoning skills to a **cognitive architecture** that can:\n"
            "\n"
            "- understand what kind of task it received,\n"
            "- choose an appropriate strategy,\n"
            "- monitor whether that strategy works,\n"
            "- redirect itself when evidence changes,\n"
            "- remember useful experience.\n"
            "\n"
            "[[IMAGE_NEEDED: Reasoning primitives versus cognitive architecture | "
            "Left: separate boxes for CoT, ReAct, ToT, Reflexion used independently. Right: a cognitive architecture that dynamically "
            "selects and monitors these primitives through feedback | "
            "Learner should notice that the new capability is strategy selection and adaptation, not simply more reasoning]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Five failure modes of capable-but-not-cognitive agents\n"
            "\n"
            "The chapter begins with five recurring production failures.\n"
            "\n"
            "### 1. The confident wrong answer\n"
            "\n"
            "The agent retrieves low-quality evidence—such as metadata or a table-of-contents page—and treats it as authoritative content.\n"
            "\n"
            "Missing capability: **evidence evaluation**.  \n"
            "Architectural fix: **evaluation module**.\n"
            "\n"
            "### 2. The broken record\n"
            "\n"
            "The agent retries essentially the same failing search repeatedly.\n"
            "\n"
            "Missing capability: **stagnation awareness**.  \n"
            "Architectural fix: **attention module**.\n"
            "\n"
            "### 3. The rigid plan\n"
            "\n"
            "New evidence contradicts the initial plan, but the agent continues following it.\n"
            "\n"
            "Missing capability: **model updating**.  \n"
            "Architectural fix: **replanning** triggered by evaluation.\n"
            "\n"
            "### 4. The overcommitted guess\n"
            "\n"
            "The agent lacks evidence but presents a confident-sounding answer anyway.\n"
            "\n"
            "Missing capability: **knowledge-boundary awareness**.  \n"
            "Architectural fix: **confidence gate**.\n"
            "\n"
            "### 5. The shallow composition\n"
            "\n"
            "The agent can call tools separately but fails to recognize that a task requires a novel multi-tool composition.\n"
            "\n"
            "Missing capability: **compositional reasoning**.  \n"
            "Architectural fix: **perception + planning modules**.\n"
            "\n"
            '{{image:cognitive-failure-map}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 3. Reasoning versus cognition versus metacognition\n"
            "\n"
            "The chapter separates three ideas.\n"
            "\n"
            "### Reasoning\n"
            "\n"
            "Reasoning patterns help solve a well-defined problem.\n"
            "\n"
            "### Cognition\n"
            "\n"
            "Cognition is about building and updating an internal model of **what the problem actually is**.\n"
            "\n"
            "### Metacognition\n"
            "\n"
            "Metacognition monitors the agent's own problem-solving process:\n"
            "\n"
            "- Is the current approach working?\n"
            "- Is confidence rising or falling?\n"
            "- Is evidence contradictory?\n"
            "- Are we stuck?\n"
            "- Do we actually know enough to answer?\n"
            "\n"
            "The distinction matters most when tasks are ambiguous, contradictory, incomplete, or unfamiliar.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Four capabilities define agent cognition\n"
            "\n"
            "The chapter defines cognition through four observable engineering capabilities.\n"
            "\n"
            "### Task decomposition\n"
            "\n"
            "Can the agent invent a useful set of subtasks for a novel problem?\n"
            "\n"
            "### Dependency reasoning\n"
            "\n"
            "Can it identify that task B depends on task A while task C may run independently?\n"
            "\n"
            "### Compositional tool use\n"
            "\n"
            "Can it combine tools in a configuration it was not explicitly shown?\n"
            "\n"
            "### Model updating\n"
            "\n"
            "Can it revise its working understanding when new evidence contradicts the original assumption?\n"
            "\n"
            "| Capability | Present behavior | Failure when absent | Supporting primitive |\n"
            "|---|---|---|---|\n"
            "| Task decomposition | Invents novel subtask sequence | Treats complex task as flat lookup | CoT/planning |\n"
            "| Dependency reasoning | Orders dependent work correctly | Runs steps arbitrarily | ToT/sequential thinking |\n"
            "| Compositional tool use | Chains tools in novel ways | Maps task to one tool only | ReAct |\n"
            "| Model updating | Revises plan from evidence | Follows stale plan | Reflexion/replanning |\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Three capabilities define metacognition\n"
            "\n"
            "The chapter defines metacognition through three practical abilities.\n"
            "\n"
            "### Confidence calibration\n"
            "\n"
            "Confidence should correlate with actual correctness.\n"
            "\n"
            "The important point is not whether the model writes words such as \"I am confident.\" The chapter distinguishes verbal confidence from internal or architectural signals such as retrieval quality, evidence consistency, and model-level uncertainty signals.\n"
            "\n"
            "### Stagnation detection\n"
            "\n"
            "The system notices when repeated work stops improving the result.\n"
            "\n"
            "### Knowledge-boundary awareness\n"
            "\n"
            "The agent changes behavior when evidence and coverage are insufficient instead of inventing a plausible answer.\n"
            "\n"
            "These three mechanisms are central to trustworthy production behavior because they change what the agent does when certainty is weak.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Three theoretical foundations become engineering patterns\n"
            "\n"
            "The architecture borrows design ideas from three frameworks.\n"
            "\n"
            "### Minsky: society of mind\n"
            "\n"
            "Use multiple specialized modules instead of expecting one monolithic component to perform every cognitive function.\n"
            "\n"
            "### Baars: global workspace\n"
            "\n"
            "Give specialized modules a shared workspace where important state and signals become visible to the rest of the architecture.\n"
            "\n"
            "### Kahneman: system 1 / system 2\n"
            "\n"
            "Route simple, familiar work through a fast path and reserve deeper processing for difficult or ambiguous work.\n"
            "\n"
            "The chapter is not claiming that the agent literally has a human mind. It uses these frameworks as architectural inspiration.\n"
            "\n"
            "[[IMAGE_NEEDED: Three theoretical foundations mapped to architecture | "
            "Three columns: Minsky -> specialized modules; Baars -> shared cognitive workspace; Kahneman -> fast/deep routing through attention | "
            "Learner should notice that each theory contributes one concrete design principle]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Cognitive agent architecture overview\n"
            "\n"
            "The complete architecture contains a shared workspace plus specialized modules.\n"
            "\n"
            "At the center:\n"
            "\n"
            "- **Cognitive workspace** — structured shared state.\n"
            "\n"
            "Around it:\n"
            "\n"
            "- **Perception** — understands the problem.\n"
            "- **Planning** — chooses strategy and subgoals.\n"
            "- **Execution** — acts using tools.\n"
            "- **Evaluation** — monitors progress and evidence quality.\n"
            "- **Attention** — decides which module should run next.\n"
            "- **Memory** — retrieves and records long-term experience.\n"
            "\n"
            "An outer agentic loop drives repeated progress toward convergence.\n"
            "\n"
            "```text\n"
            "                 Memory\n"
            "                   |\n"
            "                   v\n"
            "Perception -> Cognitive Workspace <- Planning\n"
            "                   ^      |\n"
            "                   |      v\n"
            "              Evaluation <- Execution\n"
            "                   |\n"
            "                   v\n"
            "                Attention\n"
            "                   |\n"
            "                   +--> chooses next module\n"
            "```\n"
            "\n"
            "No single module performs the full task. Behavior emerges from their interaction through shared state.\n"
            "\n"
            '{{image:cognitive-architecture}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 8. The cognitive workspace\n"
            "\n"
            "The cognitive workspace is not merely chat history.\n"
            "\n"
            "It is a structured representation of the agent's current cognitive state.\n"
            "\n"
            "The chapter stores six broad categories:\n"
            "\n"
            "1. **Task representation** — what problem the agent thinks it is solving.\n"
            "2. **Active hypotheses/strategy** — how it intends to solve it.\n"
            "3. **Intermediate findings** — what has been learned so far.\n"
            "4. **Confidence state** — how certain the architecture currently is.\n"
            "5. **Execution history** — what has already been tried.\n"
            "6. **Attention signals** — events requiring rerouting.\n"
            "\n"
            "This is richer than the research-state object from the previous chapter because it stores information about the **reasoning process itself**, not only accumulated findings.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Modeling the workspace with typed state\n"
            "\n"
            "The source uses enums and Pydantic models so every module speaks the same language.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "class TaskType(str, Enum):\n"
            "    SIMPLE_LOOKUP = \"simple_lookup\"\n"
            "    MULTI_STEP = \"multi_step\"\n"
            "    CONTRADICTORY = \"contradictory\"\n"
            "    AMBIGUOUS = \"ambiguous\"\n"
            "    COMPOSITIONAL = \"compositional\"\n"
            "    UNKNOWN = \"unknown\"\n"
            "\n"
            "class StrategyType(str, Enum):\n"
            "    DIRECT = \"direct\"\n"
            "    DECOMPOSE = \"decompose\"\n"
            "    EXPLORE = \"explore\"\n"
            "    HYPOTHESIS_TEST = \"hypothesis_test\"\n"
            "\n"
            "class AttentionSignal(str, Enum):\n"
            "    NONE = \"none\"\n"
            "    LOW_CONFIDENCE = \"low_confidence\"\n"
            "    STAGNATION = \"stagnation\"\n"
            "    CONTRADICTION = \"contradiction\"\n"
            "    KNOWLEDGE_GAP = \"knowledge_gap\"\n"
            "    TASK_COMPLETE = \"task_complete\"\n"
            "```\n"
            "\n"
            "Typed state is important because attention routing, evaluation, and confidence logic should operate on predictable fields rather than parsing free-form descriptions.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Attention signals are the workspace's control channel\n"
            "\n"
            "The most important workspace field is the active attention signal.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "CONTRADICTION -> replan using hypothesis testing\n"
            "STAGNATION    -> stop repeating the failed strategy\n"
            "LOW_CONFIDENCE-> gather more or escalate\n"
            "KNOWLEDGE_GAP -> retrieve memory / broaden search\n"
            "TASK_COMPLETE -> prepare response\n"
            "```\n"
            "\n"
            "This is the global-workspace idea in engineering form: one module writes an important signal, and the attention mechanism changes the system's behavior in response.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. The perception module\n"
            "\n"
            "Perception is the agent's first structured interpretation of the request.\n"
            "\n"
            "It should not answer the user's question. It should classify the problem.\n"
            "\n"
            "The chapter's perception module identifies:\n"
            "\n"
            "- task type,\n"
            "- key entities,\n"
            "- complexity estimate,\n"
            "- ambiguities.\n"
            "\n"
            "A simplified instruction set is:\n"
            "\n"
            "```text\n"
            "Classify the task as simple_lookup, multi_step, contradictory,\n"
            "ambiguous, compositional, or unknown.\n"
            "\n"
            "Extract important entities.\n"
            "Estimate complexity from 0.0 to 1.0.\n"
            "List ambiguities.\n"
            "Do not solve the task yet.\n"
            "```\n"
            "\n"
            "Perception therefore acts like triage: it tells the rest of the architecture how much processing the task deserves.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Selective depth: fast path versus full cognitive cycle\n"
            "\n"
            "One of the architecture's main efficiency ideas is that not every query deserves the same amount of thinking.\n"
            "\n"
            "A simple, familiar lookup can take a fast path.\n"
            "\n"
            "```text\n"
            "Simple + familiar\n"
            "   -> retrieve known memory / execute directly\n"
            "   -> respond\n"
            "```\n"
            "\n"
            "A complex, ambiguous, or contradictory task enters the deeper cycle.\n"
            "\n"
            "```text\n"
            "Complex task\n"
            "   -> perceive\n"
            "   -> retrieve memory\n"
            "   -> plan\n"
            "   -> execute\n"
            "   -> evaluate\n"
            "   -> possibly replan\n"
            "```\n"
            "\n"
            "This is the chapter's System 1/System 2 routing idea implemented architecturally.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. The planning module chooses a strategy\n"
            "\n"
            "A standard agent often has one generic behavior: receive a query, call tools, answer.\n"
            "\n"
            "The cognitive planning module selects among strategies.\n"
            "\n"
            "| Task condition | Strategy |\n"
            "|---|---|\n"
            "| Simple, low complexity | DIRECT |\n"
            "| Multi-step | DECOMPOSE |\n"
            "| Ambiguous | EXPLORE |\n"
            "| Contradictory evidence | HYPOTHESIS_TEST |\n"
            "\n"
            "This means the architecture does not apply the same reasoning primitive to every task.\n"
            "\n"
            "The planning module can also use memory hits from earlier tasks.\n"
            "\n"
            "Past experience should **accelerate planning**, not replace current reasoning.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Memory-informed planning\n"
            "\n"
            "Suppose the current task concerns intermittent failures under load.\n"
            "\n"
            "The memory system may retrieve an earlier experience:\n"
            "\n"
            "```text\n"
            "connection_pool_exhaustion\n"
            "Observation: previously caused intermittent failures during high load\n"
            "```\n"
            "\n"
            "The planner can use that experience to generate a stronger hypothesis list.\n"
            "\n"
            "But it should still test the hypothesis against the current problem.\n"
            "\n"
            "This prevents two opposite failures:\n"
            "\n"
            "- ignoring valuable experience,\n"
            "- blindly copying an old solution into a new situation.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. The execution module acts on one plan step\n"
            "\n"
            "Execution is intentionally simpler than perception or planning.\n"
            "\n"
            "It receives a subgoal, calls the required tools, and writes a structured finding back into the workspace.\n"
            "\n"
            "The chapter enriches each finding with metadata:\n"
            "\n"
            "```python\n"
            "class Finding(BaseModel):\n"
            "    content: str\n"
            "    source: str\n"
            "    relevance_score: float = 0.0\n"
            "    quality_note: str = \"\"\n"
            "```\n"
            "\n"
            "The metadata matters because not all retrieval is equally useful.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "content: table of contents page\n"
            "relevance_score: 0.2\n"
            "quality_note: metadata, not substantive evidence\n"
            "```\n"
            "\n"
            "That makes poor evidence visible to downstream evaluation.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. The evaluation module is the metacognitive core\n"
            "\n"
            "The evaluation module asks whether the architecture is actually making progress.\n"
            "\n"
            "It does not search for new facts itself. It monitors the existing trajectory.\n"
            "\n"
            "The chapter's structured result includes:\n"
            "\n"
            "```python\n"
            "class EvaluationResult(BaseModel):\n"
            "    progress_assessment: str\n"
            "    consistency_check: bool\n"
            "    confidence_delta: float\n"
            "    contradictions: list[str] = []\n"
            "    recommendation: str\n"
            "```\n"
            "\n"
            "The recommendation can be:\n"
            "\n"
            "- `CONTINUE`,\n"
            "- `REPLAN`,\n"
            "- `ESCALATE`,\n"
            "- `TERMINATE`.\n"
            "\n"
            "This module directly addresses several production failures:\n"
            "\n"
            "- evidence-quality failure,\n"
            "- contradiction,\n"
            "- stagnation,\n"
            "- declining confidence.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Evaluation is not the same as Reflexion\n"
            "\n"
            "The chapter draws an important distinction.\n"
            "\n"
            "### Reflexion\n"
            "\n"
            "Usually operates after an attempt and feeds critique into another attempt.\n"
            "\n"
            "### Cognitive evaluation\n"
            "\n"
            "Monitors the task **during execution** and can redirect the current trajectory before the full answer is produced.\n"
            "\n"
            "```text\n"
            "Reflexion  -> post-attempt correction\n"
            "Evaluation -> in-process monitoring\n"
            "```\n"
            "\n"
            "Both are useful, but evaluation can stop a bad approach before it compounds into a larger failure.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. The attention module routes control\n"
            "\n"
            "Attention is what turns the modules into a cognitive architecture instead of a fixed pipeline.\n"
            "\n"
            "Rather than always doing:\n"
            "\n"
            "```text\n"
            "Perceive -> Plan -> Execute -> Evaluate -> Repeat\n"
            "```\n"
            "\n"
            "attention can redirect control.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "CONTRADICTION  -> PLAN with HYPOTHESIS_TEST\n"
            "STAGNATION     -> META_PLAN / choose a different strategy\n"
            "LOW_CONFIDENCE -> gather more or ESCALATE\n"
            "KNOWLEDGE_GAP  -> MEMORY\n"
            "TASK_COMPLETE  -> RESPOND\n"
            "```\n"
            "\n"
            "The chapter implements this router in deterministic code rather than another LLM call.\n"
            "\n"
            "That makes routing behavior easier to inspect and tune.\n"
            "\n"
            '{{image:attention-routing}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 19. Deterministic attention routing\n"
            "\n"
            "A simplified version of the chapter's router is:\n"
            "\n"
            "```python\n"
            "def route_attention(workspace: CognitiveWorkspace) -> str:\n"
            "    if (\n"
            "        workspace.complexity_estimate < 0.3\n"
            "        and workspace.memory_hits\n"
            "        and workspace.active_signal == AttentionSignal.NONE\n"
            "    ):\n"
            "        return \"FAST_RESPOND\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.TASK_COMPLETE:\n"
            "        return \"RESPOND\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.STAGNATION:\n"
            "        return \"META_PLAN\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.CONTRADICTION:\n"
            "        workspace.current_strategy = StrategyType.HYPOTHESIS_TEST\n"
            "        return \"PLAN\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.LOW_CONFIDENCE:\n"
            "        return \"ESCALATE\" if workspace.confidence < 0.2 else \"PLAN\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.KNOWLEDGE_GAP:\n"
            "        return \"MEMORY\"\n"
            "```\n"
            "\n"
            "Thresholds such as `0.3` or `0.2` are architecture settings that should be tuned from experience and evaluation data rather than treated as universal truths.\n"
            "\n"
            "{{exercise:M01.L10.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 20. The memory module creates persistent experience\n"
            "\n"
            "The chapter uses the MCP reference memory server, backed by a local knowledge graph.\n"
            "\n"
            "Its basic primitives are:\n"
            "\n"
            "- **entities** — primary nodes,\n"
            "- **relations** — directed links between entities,\n"
            "- **observations** — facts attached to entities.\n"
            "\n"
            "The cognitive memory module adds three behaviors:\n"
            "\n"
            "### Proactive retrieval\n"
            "\n"
            "Before planning, retrieve relevant prior experience.\n"
            "\n"
            "### Experience recording\n"
            "\n"
            "After evaluation, record what strategy was tried and whether it succeeded.\n"
            "\n"
            "### Relation building\n"
            "\n"
            "Connect problem types that share strategies, failure modes, or resolutions.\n"
            "\n"
            "Over time, memory becomes structured institutional experience instead of a flat log.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Why the chapter uses graph memory\n"
            "\n"
            "The source makes a specific trade-off.\n"
            "\n"
            "Vector stores are strong at semantic similarity.\n"
            "\n"
            "Knowledge graphs are strong at explicit structural relationships.\n"
            "\n"
            "For the cognitive architecture, relationships such as:\n"
            "\n"
            "```text\n"
            "timeout_under_load\n"
            "    --often_co_occurs_with-->\n"
            "connection_pool_exhaustion\n"
            "```\n"
            "\n"
            "may be more useful than merely knowing that two texts have similar embeddings.\n"
            "\n"
            "The architecture itself is not tied permanently to one memory backend because MCP provides an interchangeable interface.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Layering the cognitive cycle inside the agentic loop\n"
            "\n"
            "Chapter 9 introduced the outer agentic loop.\n"
            "\n"
            "This chapter enriches what happens **inside each iteration**.\n"
            "\n"
            "```text\n"
            "Outer agentic loop\n"
            "  iteration 1\n"
            "      |\n"
            "      +--> inner cognitive cycle\n"
            "              perceive\n"
            "              memory\n"
            "              plan\n"
            "              execute\n"
            "              evaluate\n"
            "              maybe replan\n"
            "              maybe re-execute\n"
            "      |\n"
            "      v\n"
            "  convergence check\n"
            "```\n"
            "\n"
            "The outer loop controls macro progress and termination.\n"
            "\n"
            "The inner cognitive cycle controls local processing quality.\n"
            "\n"
            "The attention module sits between them and converts evaluation signals into routing decisions.\n"
            "\n"
            '{{image:cognitive-agentic-loop}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 23. A bounded cognitive loop\n"
            "\n"
            "The chapter uses both an outer iteration limit and an inner cognitive-step limit.\n"
            "\n"
            "A simplified structure is:\n"
            "\n"
            "```python\n"
            "async def run_cognitive_loop(\n"
            "    query: str,\n"
            "    max_iterations: int = 10,\n"
            "    confidence_threshold: float = 0.8,\n"
            "    max_cognitive_steps: int = 5,\n"
            "):\n"
            "    workspace = CognitiveWorkspace(raw_query=query)\n"
            "\n"
            "    for i in range(max_iterations):\n"
            "        workspace.iteration_count = i\n"
            "\n"
            "        for step in range(max_cognitive_steps):\n"
            "            next_module = route_attention(workspace)\n"
            "\n"
            "            if next_module == \"FAST_RESPOND\":\n"
            "                return build_response(workspace)\n"
            "\n"
            "            if next_module == \"ESCALATE\":\n"
            "                return build_uncertain_response(workspace)\n"
            "\n"
            "            # run selected module and update workspace\n"
            "\n"
            "        if workspace.confidence >= confidence_threshold:\n"
            "            break\n"
            "\n"
            "    await record_experience(workspace)\n"
            "    return build_response(workspace)\n"
            "```\n"
            "\n"
            "Two limits are important:\n"
            "\n"
            "- outer iterations prevent endless macro looping,\n"
            "- inner cognitive steps prevent endless rerouting inside one iteration.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Walkthrough: contradictory troubleshooting scenario\n"
            "\n"
            "The chapter demonstrates the architecture with a deployment pipeline that fails under high traffic even though the standard timeout fix has already been tried.\n"
            "\n"
            "A flat agent may search for timeout failures and repeat the standard fix.\n"
            "\n"
            "The cognitive architecture behaves differently.\n"
            "\n"
            "### Perception\n"
            "\n"
            "Classifies the task as contradictory and relatively complex.\n"
            "\n"
            "### Memory\n"
            "\n"
            "Retrieves a related past experience such as connection-pool exhaustion under load.\n"
            "\n"
            "### Planning\n"
            "\n"
            "Selects `HYPOTHESIS_TEST` and proposes several candidate explanations.\n"
            "\n"
            "### Execution\n"
            "\n"
            "Tests one hypothesis at a time using relevant tools.\n"
            "\n"
            "### Evaluation\n"
            "\n"
            "Updates confidence according to evidence quality and consistency.\n"
            "\n"
            "### Final response\n"
            "\n"
            "Presents the strongest supported hypothesis and appropriate diagnostics instead of repeating the already-failed standard fix.\n"
            "\n"
            "### Memory recording\n"
            "\n"
            "Stores the new problem pattern and outcome for future tasks.\n"
            "\n"
            "This walkthrough shows how cognition, metacognition, and memory work together rather than as isolated features.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Confidence-gated execution\n"
            "\n"
            "Before presenting an answer, the architecture checks whether confidence is sufficient.\n"
            "\n"
            "The chapter uses three possible decisions:\n"
            "\n"
            "```text\n"
            "PRESENT\n"
            "GATHER_MORE\n"
            "SIGNAL_UNCERTAINTY\n"
            "```\n"
            "\n"
            "A simplified gate is:\n"
            "\n"
            "```python\n"
            "def check_confidence_gate(workspace):\n"
            "    if workspace.confidence < 0.3:\n"
            "        return \"SIGNAL_UNCERTAINTY\"\n"
            "\n"
            "    if workspace.confidence < 0.6:\n"
            "        if workspace.iteration_count < 3:\n"
            "            return \"GATHER_MORE\"\n"
            "        return \"SIGNAL_UNCERTAINTY\"\n"
            "\n"
            "    if workspace.active_signal == AttentionSignal.CONTRADICTION:\n"
            "        return \"GATHER_MORE\"\n"
            "\n"
            "    return \"PRESENT\"\n"
            "```\n"
            "\n"
            "The gate does not ask the model to simply *say* whether it feels confident. It uses architecture-level state built from evidence and evaluation.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Confidence trend can matter more than one score\n"
            "\n"
            "A single confidence value may hide deterioration.\n"
            "\n"
            "Suppose confidence changes like this:\n"
            "\n"
            "```text\n"
            "0.72 -> 0.66 -> 0.58\n"
            "```\n"
            "\n"
            "Even if `0.58` is not catastrophic by itself, the declining trend signals that new evidence is making the current explanation less plausible.\n"
            "\n"
            "The chapter therefore treats several consecutive confidence drops as a reason to gather more evidence rather than present the result immediately.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Stagnation detection and strategy pivoting\n"
            "\n"
            "Stagnation catches the broken-record problem.\n"
            "\n"
            "The chapter demonstrates two simple signals.\n"
            "\n"
            "### Content overlap\n"
            "\n"
            "If the latest two findings share too much vocabulary, the architecture may be repeating itself.\n"
            "\n"
            "### Confidence plateau\n"
            "\n"
            "If confidence barely changes across several steps, the current strategy may not be producing meaningful progress.\n"
            "\n"
            "A simplified detector is:\n"
            "\n"
            "```python\n"
            "def detect_stagnation(workspace):\n"
            "    if len(workspace.findings) < 2:\n"
            "        return False\n"
            "\n"
            "    last = set(workspace.findings[-1].content.lower().split())\n"
            "    prev = set(workspace.findings[-2].content.lower().split())\n"
            "\n"
            "    overlap = len(last & prev) / max(len(last), 1)\n"
            "\n"
            "    if overlap > 0.7:\n"
            "        workspace.active_signal = AttentionSignal.STAGNATION\n"
            "        return True\n"
            "\n"
            "    return False\n"
            "```\n"
            "\n"
            "When stagnation fires, the failed strategy is recorded so replanning can avoid proposing the same approach again.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Knowledge-boundary awareness\n"
            "\n"
            "The safest production agent is not the one that always answers. It is the one that changes behavior when evidence is inadequate.\n"
            "\n"
            "The chapter combines signals such as:\n"
            "\n"
            "- retrieval relevance,\n"
            "- memory coverage,\n"
            "- current confidence.\n"
            "\n"
            "Then it classifies the current task as:\n"
            "\n"
            "```text\n"
            "WITHIN knowledge\n"
            "EDGE of knowledge\n"
            "OUTSIDE knowledge\n"
            "```\n"
            "\n"
            "When the task falls outside supported knowledge, the architecture raises a low-confidence signal and moves toward graceful degradation instead of confident invention.\n"
            "\n"
            "This is the practical meaning of \"knowing what you do not know\" in the chapter.\n"
            "\n"
            "[[IMAGE_NEEDED: Knowledge-boundary awareness | "
            "Show three zones labeled Within Knowledge, Edge of Knowledge, Outside Knowledge, with signals from retrieval quality, memory coverage, "
            "and confidence feeding the classifier. Outside leads to SIGNAL_UNCERTAINTY | "
            "Learner should notice that uncertainty behavior is triggered by multiple architecture signals]]\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Emergent behaviors from simple modules\n"
            "\n"
            "The chapter describes four behaviors that are not coded as one dedicated module.\n"
            "\n"
            "They emerge from interactions among modules.\n"
            "\n"
            "### Curiosity\n"
            "\n"
            "Low confidence plus a knowledge gap causes the architecture to seek additional information beyond the original narrow query.\n"
            "\n"
            "### Adaptive persistence\n"
            "\n"
            "A failed strategy is recorded, attention redirects control, and planning chooses another approach.\n"
            "\n"
            "### Selective depth\n"
            "\n"
            "Simple familiar problems use a fast path; difficult problems use the full architecture.\n"
            "\n"
            "### Graceful degradation\n"
            "\n"
            "When evidence remains weak, the agent presents uncertainty or partial information instead of fabricating certainty.\n"
            "\n"
            "The key idea is architectural composition: several simple mechanisms interact to create richer system behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Diagnose whether your agent needs the full architecture\n"
            "\n"
            "The chapter proposes five practical tests corresponding to the five failure modes.\n"
            "\n"
            "| Test | Passing behavior | Failure behavior |\n"
            "|---|---|---|\n"
            "| Evidence evaluation | Rejects metadata/TOC as substantive evidence | Presents metadata as answer |\n"
            "| Stagnation awareness | Pivots strategy quickly | Repeats same search several times |\n"
            "| Model updating | Revises plan when premise changes | Follows stale plan |\n"
            "| Knowledge boundaries | Signals uncertainty when coverage is absent | Hallucinates plausible answer |\n"
            "| Compositional reasoning | Decomposes multi-tool task correctly | Treats it as one flat lookup |\n"
            "\n"
            "If an existing agent already passes these consistently, the full cognitive architecture may be unnecessary overhead.\n"
            "\n"
            "That is an important engineering principle: complexity should solve observed failures.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Four cognitive-efficiency metrics\n"
            "\n"
            "The chapter recommends measuring the architecture rather than judging it by intuition.\n"
            "\n"
            "### Cognitive efficiency\n"
            "\n"
            "How many cognitive steps are used relative to the number that should be required for that task type?\n"
            "\n"
            "### Metacognitive calibration\n"
            "\n"
            "How well does final confidence correlate with actual correctness?\n"
            "\n"
            "### Adaptation rate\n"
            "\n"
            "How many iterations occur between detecting a bad strategy and successfully pivoting?\n"
            "\n"
            "### Knowledge-boundary accuracy\n"
            "\n"
            "How often does the agent correctly identify insufficient coverage?\n"
            "\n"
            "This metric has two important error types:\n"
            "\n"
            "- **false positive:** signals uncertainty on an easy supported question,\n"
            "- **false negative:** confidently answers when evidence is inadequate.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Measure the architecture against a simpler baseline\n"
            "\n"
            "The chapter recommends comparing:\n"
            "\n"
            "```text\n"
            "Standard ReAct agent\n"
            "        vs.\n"
            "Cognitive agent\n"
            "```\n"
            "\n"
            "on the same queries.\n"
            "\n"
            "Measure:\n"
            "\n"
            "- correctness,\n"
            "- confidence calibration,\n"
            "- graceful-degradation rate,\n"
            "- average token usage.\n"
            "\n"
            "Then compare the cognitive agent at two memory stages:\n"
            "\n"
            "```text\n"
            "Empty knowledge graph\n"
            "        vs.\n"
            "Knowledge graph after many completed tasks\n"
            "```\n"
            "\n"
            "This isolates whether accumulated experience is improving future planning and reducing repeated failures.\n"
            "\n"
            "{{exercise:M01.L10.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Generalization is architectural, not only parametric\n"
            "\n"
            "The source's final argument is that more capable agents do not come only from larger models.\n"
            "\n"
            "A reusable cognitive architecture separates concerns:\n"
            "\n"
            "- reasoning,\n"
            "- monitoring,\n"
            "- memory,\n"
            "- adaptation,\n"
            "- tool use,\n"
            "- confidence control.\n"
            "\n"
            "These components can be improved independently and recombined across domains.\n"
            "\n"
            "For a new domain, you can change:\n"
            "\n"
            "- perception task types,\n"
            "- available execution tools,\n"
            "- planning strategy descriptions,\n"
            "- memory entities and relations,\n"
            "\n"
            "while retaining the same core cognitive infrastructure.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Practical cognitive-agent design playbook\n"
            "\n"
            "Use this process when deciding whether and how to build cognitive architecture.\n"
            "\n"
            "### Step 1 — Observe actual failure modes\n"
            "\n"
            "Do not add modules because the architecture sounds sophisticated.\n"
            "\n"
            "### Step 2 — Build a structured workspace\n"
            "\n"
            "State should represent the task, strategy, findings, confidence, history, and signals.\n"
            "\n"
            "### Step 3 — Separate perception from answering\n"
            "\n"
            "First decide what kind of problem you received.\n"
            "\n"
            "### Step 4 — Select strategy from task type\n"
            "\n"
            "Direct, decompose, explore, or hypothesis-test.\n"
            "\n"
            "### Step 5 — Annotate execution results\n"
            "\n"
            "Attach source, relevance, and quality information.\n"
            "\n"
            "### Step 6 — Evaluate during execution\n"
            "\n"
            "Monitor progress, contradictions, and confidence before the final response.\n"
            "\n"
            "### Step 7 — Route deterministically from signals\n"
            "\n"
            "Make attention behavior inspectable.\n"
            "\n"
            "### Step 8 — Retrieve memory before planning\n"
            "\n"
            "Use experience as evidence, not as unquestioned truth.\n"
            "\n"
            "### Step 9 — Gate final presentation by confidence\n"
            "\n"
            "Gather more or signal uncertainty when necessary.\n"
            "\n"
            "### Step 10 — Detect stagnation explicitly\n"
            "\n"
            "A running agent is not necessarily a progressing agent.\n"
            "\n"
            "### Step 11 — Bound both outer and inner loops\n"
            "\n"
            "Prevent runaway macro iteration and runaway cognitive rerouting.\n"
            "\n"
            "### Step 12 — Measure whether architecture earns its cost\n"
            "\n"
            "Compare it against a simpler baseline on actual tasks.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: More reasoning patterns automatically make an agent smarter\n"
            "\n"
            "> Unselected complexity can make the system slower and harder to control.\n"
            "\n"
            "The new capability is selecting and monitoring the right reasoning strategy.\n"
            "\n"
            "### Misconception 2: Cognition means machine consciousness\n"
            "\n"
            "> In this chapter, cognition is an engineering term for observable problem-modeling capabilities.\n"
            "\n"
            "### Misconception 3: Metacognition is just asking the model how confident it feels\n"
            "\n"
            "> Useful metacognition comes from architecture-level evidence, trends, retrieval quality, consistency, and confidence state.\n"
            "\n"
            "### Misconception 4: A cognitive workspace is just conversation history\n"
            "\n"
            "> It is typed state representing the task model, strategy, findings, confidence, history, and routing signals.\n"
            "\n"
            "### Misconception 5: Every query should run through the full cognitive cycle\n"
            "\n"
            "> Simple familiar tasks should use a fast path when possible.\n"
            "\n"
            "### Misconception 6: Memory should dictate the current answer\n"
            "\n"
            "> Past experience should inform planning but still be checked against current evidence.\n"
            "\n"
            "### Misconception 7: Evaluation and Reflexion are identical\n"
            "\n"
            "> Evaluation monitors during execution; Reflexion typically critiques after an attempt.\n"
            "\n"
            "### Misconception 8: If an agent is still producing output, it is still making progress\n"
            "\n"
            "> Stagnation can look productive while adding little new information.\n"
            "\n"
            "### Misconception 9: The architecture should always answer eventually\n"
            "\n"
            "> Knowledge-boundary awareness and graceful degradation are core production features.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Cognitive primitive | Individual reasoning strategy such as ReAct, ToT, or Reflexion |\n"
            "| Cognitive architecture | System that selects, composes, and monitors cognitive primitives |\n"
            "| Cognition | Quality of the agent's internal representation and handling of the task |\n"
            "| Metacognition | Monitoring and regulating the agent's own problem-solving process |\n"
            "| Task decomposition | Breaking a novel task into useful subtasks |\n"
            "| Dependency reasoning | Understanding ordering and dependency between subtasks |\n"
            "| Compositional tool use | Combining tools in new multi-step configurations |\n"
            "| Model updating | Revising the task model or plan when evidence changes |\n"
            "| Confidence calibration | Alignment between confidence and actual correctness |\n"
            "| Stagnation | Continued activity without meaningful progress |\n"
            "| Knowledge boundary | Boundary between supported and unsupported knowledge/evidence |\n"
            "| Cognitive workspace | Shared structured state used by all modules |\n"
            "| Perception module | Classifies and represents the problem |\n"
            "| Planning module | Selects a strategy and subgoals |\n"
            "| Execution module | Performs plan steps using tools |\n"
            "| Evaluation module | Monitors progress, evidence quality, consistency, and confidence |\n"
            "| Attention module | Routes control according to workspace signals |\n"
            "| Memory module | Retrieves and records persistent experience |\n"
            "| Fast path | Shortcut for simple, familiar tasks |\n"
            "| Hypothesis testing | Strategy for contradictory tasks using competing explanations |\n"
            "| Confidence gate | Structural decision about present, gather more, or signal uncertainty |\n"
            "| Graceful degradation | Safe partial/uncertain response when evidence is insufficient |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does stacking reasoning patterns not automatically improve an agent?\n"
            "2. What are the five failure modes introduced by the chapter?\n"
            "3. How is cognition different from reasoning?\n"
            "4. How is metacognition different from cognition?\n"
            "5. What four capabilities define cognition in this architecture?\n"
            "6. What three capabilities define metacognition?\n"
            "7. What architectural idea comes from Minsky?\n"
            "8. What architectural idea comes from Baars?\n"
            "9. What routing idea comes from Kahneman?\n"
            "10. What information belongs in the cognitive workspace?\n"
            "11. Why is the attention signal important?\n"
            "12. What does the perception module produce?\n"
            "13. How does planning choose among DIRECT, DECOMPOSE, EXPLORE, and HYPOTHESIS_TEST?\n"
            "14. Why should execution findings include quality metadata?\n"
            "15. What does the evaluation module monitor?\n"
            "16. How is evaluation different from Reflexion?\n"
            "17. Why is attention routing implemented deterministically in the chapter?\n"
            "18. What three behaviors does the memory module add on top of the MCP memory server?\n"
            "19. Why does the architecture use graph memory in the chapter example?\n"
            "20. How does the cognitive cycle fit inside the outer agentic loop?\n"
            "21. Why are inner cognitive-step limits useful?\n"
            "22. What does the confidence gate do?\n"
            "23. How does stagnation detection trigger strategy pivoting?\n"
            "24. What signals contribute to knowledge-boundary awareness?\n"
            "25. What are the four emergent behaviors described by the chapter?\n"
            "26. What are the four production metrics for cognitive capability?\n"
            "27. How would you prove the cognitive architecture is better than a simpler ReAct baseline?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A cognitive agent is not simply an agent with more reasoning steps. It is an architecture that builds "
            "a model of the task, chooses an appropriate strategy, monitors evidence and progress, changes course when "
            "necessary, remembers prior experience, and refuses to present weak conclusions as certainty. The important "
            "capability is not endless thinking—it is selective, monitored, adaptive thinking.**\n"
        ),

        "estimated_minutes": 285,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-cognitive-architecture", "title": "Why reasoning patterns alone are not enough", "order": 1},
            {"id": "five-failures", "title": "Five failure modes of capable-but-not-cognitive agents", "order": 2},
            {"id": "reasoning-vs-thinking", "title": "Reasoning versus cognition versus metacognition", "order": 3},
            {"id": "cognitive-capabilities", "title": "Four capabilities define agent cognition", "order": 4},
            {"id": "metacognitive-capabilities", "title": "Three capabilities define metacognition", "order": 5},
            {"id": "theoretical-foundations", "title": "Three theoretical foundations become engineering patterns", "order": 6},
            {"id": "architecture-overview", "title": "Cognitive agent architecture overview", "order": 7},
            {"id": "workspace", "title": "The cognitive workspace", "order": 8},
            {"id": "workspace-model", "title": "Modeling the workspace with typed state", "order": 9},
            {"id": "attention-signal", "title": "Attention signals are the workspace's control channel", "order": 10},
            {"id": "perception", "title": "The perception module", "order": 11},
            {"id": "selective-depth", "title": "Selective depth: fast path versus full cognitive cycle", "order": 12},
            {"id": "planning-module", "title": "The planning module chooses a strategy", "order": 13},
            {"id": "planning-memory", "title": "Memory-informed planning", "order": 14},
            {"id": "execution-module", "title": "The execution module acts on one plan step", "order": 15},
            {"id": "evaluation-module", "title": "The evaluation module is the metacognitive core", "order": 16},
            {"id": "evaluation-vs-reflexion", "title": "Evaluation is not the same as Reflexion", "order": 17},
            {"id": "attention-module", "title": "The attention module routes control", "order": 18},
            {"id": "attention-code", "title": "Deterministic attention routing", "order": 19},
            {"id": "memory-module", "title": "The memory module creates persistent experience", "order": 20},
            {"id": "why-graph-memory", "title": "Why the chapter uses graph memory", "order": 21},
            {"id": "cognitive-loop", "title": "Layering the cognitive cycle inside the agentic loop", "order": 22},
            {"id": "cognitive-loop-code", "title": "A bounded cognitive loop", "order": 23},
            {"id": "walkthrough", "title": "Walkthrough: contradictory troubleshooting scenario", "order": 24},
            {"id": "confidence-gate", "title": "Confidence-gated execution", "order": 25},
            {"id": "confidence-trend", "title": "Confidence trend can matter more than one score", "order": 26},
            {"id": "stagnation-detection", "title": "Stagnation detection and strategy pivoting", "order": 27},
            {"id": "knowledge-boundaries", "title": "Knowledge-boundary awareness", "order": 28},
            {"id": "emergent-behaviors", "title": "Emergent behaviors from simple modules", "order": 29},
            {"id": "diagnostic-tests", "title": "Diagnose whether your agent needs the full architecture", "order": 30},
            {"id": "cognitive-metrics", "title": "Four cognitive-efficiency metrics", "order": 31},
            {"id": "before-after", "title": "Measure the architecture against a simpler baseline", "order": 32},
            {"id": "architectural-generalization", "title": "Generalization is architectural, not only parametric", "order": 33},
            {"id": "cognitive-playbook", "title": "Practical cognitive-agent design playbook", "order": 34},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L10.EX01",

            "title": "Build the Workspace, Evaluator, and Attention Router",

            "lesson_code": "M01.L10",

            "section_id": "attention-code",

            "placement": "after_section",

            "description": (
                "Implement the core shared state and metacognitive routing logic "
                "before assembling the full cognitive agent."
            ),

            "instructions": (
                "1. Implement the `TaskType`, `StrategyType`, and `AttentionSignal` enums.\n"
                "2. Implement `Finding` and `CognitiveWorkspace` with task representation, strategy, findings, memory hits, confidence, history, and active signal.\n"
                "3. Create three sample queries: simple lookup, multistep troubleshooting, and contradictory scenario.\n"
                "4. Populate the workspace for each query as though perception has already run.\n"
                "5. Implement an evaluation function or evaluator agent returning progress, consistency, confidence_delta, contradictions, and recommendation.\n"
                "6. Test the evaluator on one high-quality state, one contradictory state, and one low-confidence state.\n"
                "7. Implement deterministic `route_attention(workspace)` behavior.\n"
                "8. Simulate a cycle where evaluation detects contradiction and verify that routing returns to planning with `HYPOTHESIS_TEST`.\n"
                "9. Simulate stagnation and verify that the failed strategy is recorded before meta-planning.\n"
                "10. Compare the dynamic route to a fixed perceive-plan-execute-evaluate loop and explain the behavioral difference."
            ),

            "expected_output": (
                "A typed CognitiveWorkspace, evaluation output model, deterministic attention router, "
                "three test scenarios, and a short comparison between dynamic and fixed routing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cognitive-workspace",
                "typed-state",
                "evaluation",
                "attention-routing",
                "contradiction-handling",
                "stagnation-handling",
            ],
        },

        {
            "id": "M01.L10.EX02",

            "title": "Build and Measure a Cognitive Agent with Memory",

            "lesson_code": "M01.L10",

            "section_id": "before-after",

            "placement": "after_section",

            "description": (
                "Assemble the complete cognitive architecture, connect memory, and "
                "measure whether the added complexity improves real behavior."
            ),

            "instructions": (
                "1. Assemble perception, planning, execution, evaluation, attention, and memory modules around one `CognitiveWorkspace`.\n"
                "2. Connect a memory service and one domain execution tool or MCP server.\n"
                "3. Add an outer iteration limit and an inner cognitive-step limit.\n"
                "4. Add confidence-gated output: PRESENT, GATHER_MORE, or SIGNAL_UNCERTAINTY.\n"
                "5. Add stagnation detection using overlap or confidence plateau.\n"
                "6. Add knowledge-boundary assessment from retrieval relevance, memory coverage, and confidence.\n"
                "7. Run the agent on a troubleshooting task and record the final experience in memory.\n"
                "8. Run a related second task and show where the retrieved experience changes planning.\n"
                "9. Create a 10-query test set containing easy, multistep, contradictory, compositional, and unsupported questions.\n"
                "10. Run both a standard ReAct baseline and the cognitive agent on the same test set.\n"
                "11. Record correctness, final confidence, uncertainty behavior, number of steps, and approximate token usage.\n"
                "12. Compute or summarize cognitive efficiency, confidence calibration, adaptation rate, and knowledge-boundary accuracy.\n"
                "13. Decide whether the cognitive architecture earns its extra complexity for this workload."
            ),

            "expected_output": (
                "A complete bounded cognitive-agent architecture plus an empirical comparison "
                "against a simpler baseline showing where memory, metacognition, and dynamic "
                "routing improve or fail to improve the system."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cognitive-agent",
                "memory",
                "confidence-gating",
                "stagnation-detection",
                "knowledge-boundaries",
                "agent-evaluation",
                "baseline-comparison",
                "cognitive-metrics",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L10.QZ01",

        "title": "Exploring the Cognitive Agent — Knowledge Check",

        "lesson_code": "M01.L10",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L10.Q01",
                "section_id": "why-cognitive-architecture",
                "question": "What problem does cognitive architecture solve that isolated reasoning primitives do not?",
                "options": [
                    "It guarantees perfect answers",
                    "It chooses, monitors, and adapts reasoning strategies according to the task",
                    "It removes the need for tools",
                    "It eliminates model cost",
                ],
                "correct": 1,
                "explanation": (
                    "The architecture's key contribution is dynamic strategy selection and monitoring."
                ),
            },

            {
                "id": "M01.L10.Q02",
                "section_id": "five-failures",
                "question": "Which failure mode is caused by repeatedly using the same ineffective approach?",
                "options": [
                    "Confident wrong answer",
                    "Broken record",
                    "Shallow composition",
                    "Overcommitted guess",
                ],
                "correct": 1,
                "explanation": (
                    "The broken-record failure is stagnation: the agent is active but not making progress."
                ),
            },

            {
                "id": "M01.L10.Q03",
                "section_id": "cognitive-capabilities",
                "question": "What does model updating mean in this architecture?",
                "options": [
                    "Fine-tuning the base model during every request",
                    "Revising the agent's working understanding or plan when new evidence contradicts it",
                    "Updating Python dependencies",
                    "Increasing context length",
                ],
                "correct": 1,
                "explanation": (
                    "Model updating here refers to updating the internal task model/plan, not model weights."
                ),
            },

            {
                "id": "M01.L10.Q04",
                "section_id": "metacognitive-capabilities",
                "question": "Which is a metacognitive capability?",
                "options": [
                    "Calling a search tool",
                    "Detecting that repeated iterations are not making progress",
                    "Parsing JSON",
                    "Rendering a UI",
                ],
                "correct": 1,
                "explanation": (
                    "Stagnation awareness monitors the system's own problem-solving process."
                ),
            },

            {
                "id": "M01.L10.Q05",
                "section_id": "theoretical-foundations",
                "question": "What architectural idea is drawn from Baars' global workspace theory?",
                "options": [
                    "One monolithic agent performs every function",
                    "Specialized modules share a common workspace",
                    "Every task uses the deepest reasoning path",
                    "Memory should be disabled",
                ],
                "correct": 1,
                "explanation": (
                    "The cognitive workspace is the shared medium through which module state and signals become visible."
                ),
            },

            {
                "id": "M01.L10.Q06",
                "section_id": "selective-depth",
                "question": "When should the fast path be preferred?",
                "options": [
                    "For every contradictory task",
                    "For simple, familiar, low-complexity tasks with adequate known context",
                    "Only when no memory exists",
                    "Only after five failed iterations",
                ],
                "correct": 1,
                "explanation": (
                    "Selective depth saves tokens and latency when full deliberation adds little value."
                ),
            },

            {
                "id": "M01.L10.Q07",
                "section_id": "planning-module",
                "question": "Which planning strategy best fits contradictory evidence?",
                "options": [
                    "DIRECT",
                    "HYPOTHESIS_TEST",
                    "No strategy",
                    "Always EXPLORE",
                ],
                "correct": 1,
                "explanation": (
                    "The source routes contradictory scenarios to competing-hypothesis testing."
                ),
            },

            {
                "id": "M01.L10.Q08",
                "section_id": "execution-module",
                "question": "Why does the execution module annotate findings with relevance and quality notes?",
                "options": [
                    "To make output longer",
                    "So evaluation can distinguish useful evidence from weak or misleading results",
                    "To avoid using tools",
                    "To replace confidence state",
                ],
                "correct": 1,
                "explanation": (
                    "Evidence metadata gives the evaluator a basis for judging whether execution actually improved the task."
                ),
            },

            {
                "id": "M01.L10.Q09",
                "section_id": "evaluation-vs-reflexion",
                "question": "How does cognitive evaluation differ from Reflexion?",
                "options": [
                    "Evaluation monitors during execution, while Reflexion usually critiques after an attempt",
                    "Reflexion cannot produce feedback",
                    "Evaluation cannot detect contradictions",
                    "They are identical",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes evaluation as real-time trajectory monitoring rather than only post-hoc correction."
                ),
            },

            {
                "id": "M01.L10.Q10",
                "section_id": "attention-module",
                "question": "What is the attention module responsible for?",
                "options": [
                    "Writing every final response",
                    "Choosing which module gets control next based on workspace signals",
                    "Storing only user chat history",
                    "Replacing all tools",
                ],
                "correct": 1,
                "explanation": (
                    "Attention turns the system from a fixed pipeline into a dynamically routed architecture."
                ),
            },

            {
                "id": "M01.L10.Q11",
                "section_id": "memory-module",
                "question": "Which is one responsibility of the memory module?",
                "options": [
                    "Proactively retrieve relevant past experience before planning",
                    "Replace all new evidence with old answers",
                    "Prevent any experience from being stored",
                    "Always use semantic vectors only",
                ],
                "correct": 0,
                "explanation": (
                    "The memory module retrieves experience, records outcomes, and builds useful relations."
                ),
            },

            {
                "id": "M01.L10.Q12",
                "section_id": "confidence-gate",
                "question": "What should a confidence gate do when evidence remains weak after the allowed information-gathering budget?",
                "options": [
                    "Invent a plausible final answer",
                    "Signal uncertainty rather than present unsupported confidence",
                    "Increase temperature",
                    "Erase evaluation history",
                ],
                "correct": 1,
                "explanation": (
                    "Graceful degradation is preferable to a confident unsupported answer."
                ),
            },

            {
                "id": "M01.L10.Q13",
                "section_id": "knowledge-boundaries",
                "question": "What does knowledge-boundary awareness attempt to determine?",
                "options": [
                    "Whether the task is inside, near the edge of, or outside supported evidence/coverage",
                    "How much RAM is installed",
                    "Whether the UI is responsive",
                    "Which container image is smallest",
                ],
                "correct": 0,
                "explanation": (
                    "Boundary awareness changes behavior when available evidence and memory are insufficient."
                ),
            },

            {
                "id": "M01.L10.Q14",
                "section_id": "cognitive-metrics",
                "question": "What does metacognitive calibration measure?",
                "options": [
                    "Correlation between confidence and actual correctness",
                    "Number of tools installed",
                    "Average prompt length only",
                    "Container startup time",
                ],
                "correct": 0,
                "explanation": (
                    "A well-calibrated system is confident more often when correct and uncertain more often when wrong."
                ),
            },

            {
                "id": "M01.L10.Q15",
                "section_id": "cognitive-playbook",
                "type": "open",
                "question": (
                    "Design a cognitive agent for a production troubleshooting system. Describe the workspace, "
                    "perception classifications, planning strategies, execution-result metadata, evaluation signals, "
                    "attention routing, memory behavior, confidence gate, stagnation handling, knowledge-boundary "
                    "behavior, loop limits, and the metrics you would use to compare it with a simpler ReAct agent."
                ),
            },
        ],

        "passing_score": 70,
    },
}
