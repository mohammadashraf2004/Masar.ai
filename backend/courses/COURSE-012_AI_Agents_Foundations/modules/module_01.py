"""M01.L01 — The Rise of AI Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 1, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Build a clear mental model of AI agents: what makes them different from "
    "ordinary LLM applications, how the sense-plan-act-learn loop works, how "
    "tools and MCP extend agent capabilities, how the five functional layers "
    "fit together, and when multi-agent patterns become useful."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "The Rise of AI Agents",

    "slug": "ai-agents-m01-l01",

    "description": (
        "Learn how LLM applications evolve from text generators into goal-directed "
        "agents that can reason, plan, use tools, learn from results, connect through "
        "MCP, and coordinate with other agents."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.25,

    "skill_tags": [
        "ai-agents",
        "agentic-systems",
        "tool-use",
        "mcp",
        "reasoning-and-planning",
        "memory",
        "multi-agent-systems",
        "foundations",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "The Rise of AI Agents",

        "content": (
            "# The Rise of AI Agents\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 1. "
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
            "- Explain what makes an AI system an **agent** rather than only an LLM application.\n"
            "- Distinguish direct LLM chat, tool-augmented LLMs, assistants, and agents.\n"
            "- Explain why **autonomy** and **persistence across multiple steps** matter.\n"
            "- Apply the **sense → plan → act → learn** cycle to a practical goal.\n"
            "- Explain how tools allow agents to interact with systems outside the model.\n"
            "- Describe why the **Model Context Protocol (MCP)** reduces repeated integration work.\n"
            "- Identify the five functional layers of an agent and the role of each layer.\n"
            "- Distinguish knowledge from memory and explain why context-window management matters.\n"
            "- Explain the roles of evaluation, feedback, guardrails, and human approval.\n"
            "- Compare agent flow, orchestration, and collaboration as multi-agent patterns.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. From answering questions to taking action\n"
            "\n"
            "A basic LLM application is very good at producing language. You give it a "
            "prompt, it generates a response, and the interaction may end there. That is "
            "useful for tasks such as explaining a topic, drafting text, or answering a question.\n"
            "\n"
            "But many real goals are not solved by a single response. Consider the difference "
            "between these two requests:\n"
            "\n"
            "```text\n"
            "Request A: List flights from Cairo to Calgary.\n"
            "Request B: Arrange my trip to Calgary.\n"
            "```\n"
            "\n"
            "The first request mainly needs information. The second may require several "
            "connected actions: search for flights, compare options, book a flight, book a "
            "hotel, and arrange transportation. A system that can pursue that higher-level "
            "goal needs more than text generation. It needs a way to decide what to do next, "
            "select actions, observe results, and continue until the goal is complete.\n"
            "\n"
            "That is the central motivation for AI agents.\n"
            "\n"
            "### A practical definition\n"
            "\n"
            "For this course, think of an **AI agent** as software that:\n"
            "\n"
            "1. **Perceives** information about its environment or task.\n"
            "2. **Decides** what should happen next.\n"
            "3. **Acts** using the resources available to it.\n"
            "4. Keeps working toward a **goal** rather than only producing one response.\n"
            "\n"
            "The LLM gives the system a flexible ability to interpret language, reason about "
            "goals, and choose among possible actions. Tools, memory, planning, and feedback "
            "mechanisms expand what the agent can actually accomplish.\n"
            "\n"
            "[[IMAGE_NEEDED: Reactive LLM versus goal-directed agent | "
            "A side-by-side diagram. Left: User -> LLM -> Text response -> Stop. "
            "Right: User goal -> Agent -> Plan -> Tool actions -> Observe results -> Continue/finish | "
            "Learner should notice that the agent has a continuing control loop instead of a "
            "single prompt-response interaction]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Agents, agency, and agentic thinking\n"
            "\n"
            "The idea of an agent is older than modern LLMs. In different areas of AI, agents "
            "have been described as entities that observe an environment, make decisions, and "
            "act toward objectives. LLM-powered agents are a newer implementation of that "
            "broader idea.\n"
            "\n"
            "The related word **agentic** describes a system or behavior that shows agency: "
            "it can perceive, decide, and act with some degree of autonomy while pursuing a goal.\n"
            "\n"
            "### Why autonomy matters\n"
            "\n"
            "A traditional generative assistant reacts to a request. An agent can continue "
            "working after the initial request by deciding which intermediate tasks are needed.\n"
            "\n"
            "Suppose the goal is:\n"
            "\n"
            "```text\n"
            "Find the five most important emails and notify me about them.\n"
            "```\n"
            "\n"
            "A useful agent may need to:\n"
            "\n"
            "- inspect available email data,\n"
            "- decide how to judge importance,\n"
            "- rank messages,\n"
            "- prepare a concise result,\n"
            "- use a notification tool.\n"
            "\n"
            "The user specifies the goal, but the agent decides many of the steps.\n"
            "\n"
            "### Autonomy is a spectrum, not an excuse for removing oversight\n"
            "\n"
            "Agents are often called autonomous, but that does **not** mean every action should "
            "run without human control. A production design can use graduated approval:\n"
            "\n"
            "- low-risk, reversible steps may run automatically,\n"
            "- medium-risk actions may require confirmation,\n"
            "- high-stakes actions may be explicitly gated before execution.\n"
            "\n"
            "So the useful question is not simply, \"Is this autonomous?\" The better question "
            "is, \"Which decisions can the agent make safely, and where should a human remain "
            "in the loop?\"\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Four common LLM interaction patterns\n"
            "\n"
            "The chapter describes a progression from simple language-model interaction toward "
            "goal-level autonomy. The terminology is not perfectly standardized across the "
            "industry, so focus on the **behavioral differences**.\n"
            "\n"
            "| Pattern | Tool use | Human approval | Autonomy | Typical behavior |\n"
            "|---|---|---|---|---|\n"
            "| Direct LLM chat | None | Not applicable | None | Generates text from a prompt |\n"
            "| Tool-augmented LLM | Usually one tool call | Triggered by the user request | Low | Uses a tool for a specific task such as search or image generation |\n"
            "| Assistant | Uses tools | Approval is commonly tied to each task/action | Medium | Helps complete user-directed tasks but does not freely pursue a long goal |\n"
            "| Agent | Uses multiple tools as needed | Goal-level approval with gates for sensitive actions | High | Plans and executes multiple steps toward an objective |\n"
            "\n"
            "### Assistant versus agent\n"
            "\n"
            "The chapter draws the line mainly along **autonomy**.\n"
            "\n"
            "An assistant can use tools, but the human remains closely involved in deciding or "
            "approving each action. An agent receives a higher-level objective and can determine "
            "the sequence of tasks required to reach it.\n"
            "\n"
            "This difference is easiest to remember like this:\n"
            "\n"
            "```text\n"
            "Assistant: \"Tell me the next task, and I will help execute it.\"\n"
            "Agent:     \"Tell me the goal, and I will work out the tasks needed.\"\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Assistant versus agent control boundary | "
            "Two flows. Assistant: user approval before each tool action. Agent: user gives a "
            "goal, agent plans and uses several tools, with explicit gates only around selected "
            "high-stakes actions | "
            "Learner should notice that the main difference is where human approval enters the "
            "workflow, not whether tools exist]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. The sense-plan-act-learn cycle\n"
            "\n"
            "A useful mental model for agent behavior is the **sense → plan → act → learn "
            "(SPAL)** cycle.\n"
            "\n"
            "### Step 1 — Sense\n"
            "\n"
            "The agent receives information: the user goal, tool results, feedback, or other "
            "context. It must understand the current situation before choosing an action.\n"
            "\n"
            "### Step 2 — Plan\n"
            "\n"
            "The agent decides which tasks are required and in what order. A plan can be simple "
            "or can involve several subgoals.\n"
            "\n"
            "### Step 3 — Act\n"
            "\n"
            "The agent executes a tool or other action needed for the current task.\n"
            "\n"
            "### Step 4 — Learn\n"
            "\n"
            "The agent observes the result and evaluates what it means. It then decides whether:\n"
            "\n"
            "- the goal is complete,\n"
            "- another step is needed,\n"
            "- the plan should change,\n"
            "- a retry or fallback is required,\n"
            "- human input is necessary.\n"
            "\n"
            "Then the cycle can repeat.\n"
            "\n"
            "### Worked example: planning a trip\n"
            "\n"
            "Goal:\n"
            "\n"
            "```text\n"
            "Travel to Calgary (YYC).\n"
            "```\n"
            "\n"
            "A possible decomposition is:\n"
            "\n"
            "```text\n"
            "Sense: Understand destination and travel requirements.\n"
            "Plan:  Search flight -> book flight -> book hotel -> arrange transport.\n"
            "Act:   Call search_flights.\n"
            "Learn: Inspect options and decide whether the result is usable.\n"
            "Act:   Call book_flights with the selected option.\n"
            "Learn: Confirm booking result, then continue to hotel and transport.\n"
            "```\n"
            "\n"
            "The important idea is that **tool output can become input to the next action**. "
            "That connection is called **tool chaining**.\n"
            "\n"
            '{{image:spal-cycle}}'
            '\n'
            "\n"
            "### Native reasoning versus structured reasoning\n"
            "\n"
            "Modern reasoning-capable models can often handle short, low-risk tasks using their "
            "built-in reasoning. More structure becomes useful when tasks are long, branch into "
            "subgoals, involve many tools, or make costly/irreversible changes.\n"
            "\n"
            "The chapter also distinguishes:\n"
            "\n"
            "- **Single-path reasoning:** commit to one plan and execute it in sequence. It is "
            "faster and cheaper, but more fragile when the task is uncertain.\n"
            "- **Multipath reasoning:** explore multiple candidate strategies and select a more "
            "promising branch. This can improve difficult plans but increases token use and latency.\n"
            "- **External planning:** move sequencing into orchestration code, a workflow engine, "
            "or a dedicated planning agent.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Tools turn language into action\n"
            "\n"
            "Without tools, an LLM can generate information but cannot directly manipulate an "
            "external system. Tools bridge that gap.\n"
            "\n"
            "A tool often wraps something the agent needs to access, such as:\n"
            "\n"
            "- an API,\n"
            "- a database,\n"
            "- a search service,\n"
            "- an external application,\n"
            "- a knowledge store,\n"
            "- another callable capability.\n"
            "\n"
            "To use a tool, the agent needs a machine-readable description of what the tool does, "
            "what inputs it expects, and what output it returns. The model can then choose an "
            "appropriate tool and supply arguments, in a way conceptually similar to calling a "
            "function in ordinary programming.\n"
            "\n"
            "### Tool categories\n"
            "\n"
            "The chapter groups tool roles into several useful categories:\n"
            "\n"
            "| Tool role | Purpose | Example idea |\n"
            "|---|---|---|\n"
            "| Task completion | Changes or acts on the outside world | Create, send, update, book |\n"
            "| Context retrieval | Fetches information needed for the next decision | Search, read file, query vector store |\n"
            "| Reasoning and planning | Supports decision or sequencing work | Planner or reasoning helper |\n"
            "| Knowledge and memory | Reads/writes persistent information | Memory store, knowledge retrieval |\n"
            "| Evaluation and feedback | Checks quality or correctness | Critic, scorer, validation tool |\n"
            "\n"
            "### Tool failures are normal control flow\n"
            "\n"
            "Real tools fail. An API can time out. A database may return an unexpected schema. "
            "Arguments can be malformed. Rate limits can be reached.\n"
            "\n"
            "A robust agent should not treat every tool error as a fatal crash. Instead, the "
            "failure should become new information for the control loop. Depending on the "
            "situation, the agent may retry, use a fallback, ask the user, or stop safely. Retry "
            "limits are important because unlimited retries can create runaway loops.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Model Context Protocol (MCP)\n"
            "\n"
            "As agents gained more tools, developers faced an integration problem: every agent "
            "could require its own wrappers for calendars, messaging systems, databases, project "
            "trackers, and many other services. Repeating that work across many agents creates a "
            "large amount of tool plumbing.\n"
            "\n"
            "The **Model Context Protocol (MCP)** addresses this by providing a standardized way "
            "for AI systems to connect to external tool servers.\n"
            "\n"
            "According to the chapter, MCP was developed by Anthropic and released in November "
            "2024. It is an open standard based on JSON-RPC 2.0.\n"
            "\n"
            "### The core idea\n"
            "\n"
            "Instead of embedding every integration directly inside every agent:\n"
            "\n"
            "```text\n"
            "Before MCP\n"
            "Agent A -> custom calendar wrapper\n"
            "Agent A -> custom Slack wrapper\n"
            "Agent B -> another calendar wrapper\n"
            "Agent B -> another Slack wrapper\n"
            "\n"
            "With MCP\n"
            "Agent A --\\\n"
            "          -> MCP server -> reusable tools\n"
            "Agent B --/\n"
            "```\n"
            "\n"
            "A server exposes tools through a consistent protocol. An agent can connect to the "
            "server, discover what tools are available, understand their descriptions, and then "
            "call the relevant tool.\n"
            "\n"
            "A typical interaction looks like this:\n"
            "\n"
            "1. Set up and run an MCP server.\n"
            "2. Register that server with the agent.\n"
            "3. Ask the server for its available tools, commonly through `list_tools`.\n"
            "4. Read the tool names/descriptions.\n"
            "5. Choose a suitable tool for the task.\n"
            "6. Execute it and observe the result.\n"
            "7. Continue the agent loop as needed.\n"
            "\n"
            '{{image:mcp-tool-discovery}}'
            '\n'
            "\n"
            "### Problems MCP is designed to reduce\n"
            "\n"
            "- **Inconsistent tool access:** one consistent protocol reduces provider-specific adaptation.\n"
            "- **Unreliable response handling:** standardized request/response structures reduce integration mistakes.\n"
            "- **Fragmented integrations:** tool code moves into reusable servers rather than being scattered across agents.\n"
            "- **Language/codebase constraints:** a protocol boundary allows the server and agent to be implemented in different languages.\n"
            "- **Implementation burden:** existing servers can be reused instead of rebuilding every connector.\n"
            "\n"
            "### Security still matters\n"
            "\n"
            "Standardization does not make tools automatically safe. An MCP server exposes "
            "capabilities an agent may invoke, so it becomes a trusted dependency. The chapter "
            "emphasizes authentication, authorization, sandboxing, scoped credentials, human "
            "approval for high-stakes actions, source vetting, version pinning, and least-privilege "
            "execution as important parts of responsible use.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. The five functional layers of an agent\n"
            "\n"
            "The chapter organizes agent capabilities into five functional layers:\n"
            "\n"
            "1. **Persona**\n"
            "2. **Tools and actions**\n"
            "3. **Reasoning and planning**\n"
            "4. **Knowledge and memory**\n"
            "5. **Evaluation and feedback**\n"
            "\n"
            "These are best understood as capabilities, not as five steps that always execute "
            "from top to bottom. During an agent run, they interact continuously. Reasoning may "
            "consult the persona, planning may invoke tools, tool results may update memory, and "
            "evaluation may send the system back to revise a plan.\n"
            "\n"
            '{{image:agent-layers}}'
            '\n'
            "\n"
            "### A compact mental model\n"
            "\n"
            "```text\n"
            "Persona              -> Who am I and how should I behave?\n"
            "Tools & actions      -> What can I do?\n"
            "Reasoning & planning -> How do I decide what to do next?\n"
            "Knowledge & memory   -> What information and experience can I use?\n"
            "Evaluation & feedback-> How do I judge and improve the result?\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Persona, reasoning, and planning\n"
            "\n"
            "### Persona\n"
            "\n"
            "The persona is the base description of the agent's role and operating behavior. "
            "It is often expressed through system instructions.\n"
            "\n"
            "A persona may specify:\n"
            "\n"
            "- role, such as coder or writer,\n"
            "- domain focus,\n"
            "- expertise level,\n"
            "- communication style,\n"
            "- operating constraints,\n"
            "- instructions about reasoning, planning, knowledge, or memory access.\n"
            "\n"
            "A good mental model is that the persona does not give the agent new external powers. "
            "Instead, it shapes how the agent uses the powers it already has.\n"
            "\n"
            "### Reasoning and planning\n"
            "\n"
            "Once tools are available, the agent needs to decide which tools to use, in what "
            "order, and under what conditions. Built-in model reasoning may be enough for short, "
            "simple, low-cost tasks. Structured reasoning becomes more valuable when the work is "
            "long, branching, safety-sensitive, or difficult to audit.\n"
            "\n"
            "The chapter's important engineering lesson is that **planning is a control problem**, "
            "not merely a prompt-writing trick. You must decide how much freedom the executing "
            "agent gets and when planning should be constrained or moved into external orchestration.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Knowledge, memory, evaluation, and feedback\n"
            "\n"
            "### Knowledge and memory are related, but different\n"
            "\n"
            "**Knowledge** is external information the agent uses to do its job. Examples include "
            "documents, manuals, schemas, code repositories, and knowledge-base articles.\n"
            "\n"
            "**Memory** is experiential information that develops through interaction. It can "
            "include recent conversation turns, preferences, past decisions, and observations "
            "recorded during earlier sessions.\n"
            "\n"
            "| Aspect | Knowledge | Memory |\n"
            "|---|---|---|\n"
            "| Nature | External reference information | Interaction-derived experience |\n"
            "| Update pattern | Changes when the underlying source changes | Changes during use |\n"
            "| Typical scope | Often shared across many users | Often session-, user-, or tenant-specific |\n"
            "| Example | Product manual | User prefers concise reports |\n"
            "\n"
            "### Short-term and long-term memory\n"
            "\n"
            "- **Short-term memory** usually refers to recent conversation turns and tool activity "
            "inside the current context window.\n"
            "- **Long-term memory** persists beyond the current session and is selectively retrieved "
            "when relevant.\n"
            "\n"
            "### Context-window management\n"
            "\n"
            "The model can only attend to a limited amount of information at once. Therefore, "
            "agent design includes decisions about what to keep, summarize, retrieve, filter, or "
            "discard. Larger context windows reduce some pressure but do not remove the trade-off: "
            "longer context can increase cost and latency, and unnecessary context can make the "
            "agent's job harder.\n"
            "\n"
            "### Retrieval-augmented generation (RAG)\n"
            "\n"
            "The chapter uses RAG as a general retrieve-then-generate pattern for bringing relevant "
            "knowledge or memory into the agent's context at decision time. The principle is simple:\n"
            "\n"
            "```text\n"
            "Current task\n"
            "    -> retrieve relevant information\n"
            "    -> add it to the context\n"
            "    -> reason/generate using that grounded information\n"
            "```\n"
            "\n"
            "### Evaluation and feedback\n"
            "\n"
            "An agent also needs ways to judge whether its work is good enough. Evaluation may be "
            "performed through:\n"
            "\n"
            "- a separate model acting as a judge,\n"
            "- a critic agent,\n"
            "- validation tools,\n"
            "- guardrails on inputs or outputs,\n"
            "- feedback generated during the learn phase of the agent loop.\n"
            "\n"
            "In an **actor-critic** arrangement, one component produces a candidate response or "
            "plan and another evaluates or revises it before the system commits to the result.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Why use more than one agent?\n"
            "\n"
            "A single agent can accomplish a lot, but some problems become easier to manage when "
            "responsibility is divided among several agents.\n"
            "\n"
            "The chapter gives four major reasons:\n"
            "\n"
            "### 1. Specialization\n"
            "\n"
            "A single agent with every tool, instruction, and domain may become overloaded. "
            "Focused agents can each handle a narrower responsibility, such as triage, billing, "
            "or technical support.\n"
            "\n"
            "### 2. Parallelism\n"
            "\n"
            "Independent tasks can be processed concurrently. For example, several agents can "
            "research different companies at the same time instead of one agent doing them sequentially.\n"
            "\n"
            "### 3. Context management\n"
            "\n"
            "Each agent can keep only the slice of information it needs. This can help when the "
            "full problem would be too large or noisy for one context window.\n"
            "\n"
            "### 4. Problems that are inherently multi-agent\n"
            "\n"
            "Some tasks naturally involve multiple actors with distinct goals or roles, such as "
            "negotiations, social simulations, or red-team/blue-team setups.\n"
            "\n"
            "The important lesson is not that more agents are always better. Multi-agent designs "
            "introduce extra coordination, cost, and latency. The chapter recommends using the "
            "cheapest pattern that still satisfies the requirement.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Three core multi-agent patterns\n"
            "\n"
            "### Pattern A — Agent flow (assembly line)\n"
            "\n"
            "Agents are arranged in a sequence. Each specialized agent performs its part and then "
            "passes work forward.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Planning Agent -> Research Agent -> Content Agent\n"
            "```\n"
            "\n"
            "This is straightforward to implement and control, which makes it useful for "
            "well-defined multistep processes with clear roles.\n"
            "\n"
            "Agents in a flow may share context in three main ways:\n"
            "\n"
            "- **Threaded:** everyone reads/writes the same conversation thread. Rich context, but "
            "the thread can become large and noisy.\n"
            "- **Blackboard:** agents write structured intermediate results under agreed keys. "
            "Organized and selective, but requires a shared schema.\n"
            "- **Chained:** each agent passes only the output required by the next agent. Simple "
            "and efficient, but information not passed forward is lost.\n"
            "\n"
            "### Pattern B — Orchestration (hub-and-spoke)\n"
            "\n"
            "A central orchestrator receives the goal, plans the work, delegates subgoals to "
            "specialized worker agents, collects results, and decides when the overall goal is complete.\n"
            "\n"
            "```text\n"
            "                  -> Worker A\n"
            "User -> Orchestrator -> Worker B\n"
            "                  -> Worker C\n"
            "```\n"
            "\n"
            "This pattern is useful when you want one main control point for inputs and outputs "
            "while still benefiting from specialized agents.\n"
            "\n"
            "A limitation is that workers may be tightly restricted to delegated tasks and may "
            "have fewer opportunities for peer-to-peer feedback.\n"
            "\n"
            "### Pattern C — Collaboration (team of agents)\n"
            "\n"
            "Agents operate more like peers. They can communicate, critique, validate, and improve "
            "one another's work.\n"
            "\n"
            "For example, a coding team might contain:\n"
            "\n"
            "- a product agent that interprets requirements,\n"
            "- a coding agent that implements them,\n"
            "- a QA agent that validates behavior and critiques quality.\n"
            "\n"
            "This can solve complex problems that benefit from interaction and criticism, but it "
            "is also more chatty, repetitive, expensive, and slow.\n"
            "\n"
            '{{image:agent-flow}}\n{{image:agent-orchestration}}\n{{image:agent-collaboration}}'
            '\n'
            "\n"
            "### Comparison\n"
            "\n"
            "| Pattern | Control shape | Best fit from this chapter | Main trade-off |\n"
            "|---|---|---|---|\n"
            "| Agent flow | Sequential pipeline | Well-defined multistep work | Less flexible when downstream agents need missing upstream context |\n"
            "| Orchestration | Central hub with workers | Multiple subgoals under one controlling agent | Workers may have limited collaboration |\n"
            "| Collaboration | Peer/team interaction | Complex work needing critique or joint problem solving | Higher cost, repetition, and latency |\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Putting the whole architecture together\n"
            "\n"
            "You can now read an agent system as a combination of a few recurring ideas.\n"
            "\n"
            "Imagine a goal-directed research agent:\n"
            "\n"
            "```text\n"
            "Goal from user\n"
            "   |\n"
            "   v\n"
            "Persona/instructions\n"
            "   |\n"
            "   v\n"
            "Reason + plan\n"
            "   |\n"
            "   +--> retrieve knowledge/memory\n"
            "   +--> call tools or MCP servers\n"
            "   |\n"
            "   v\n"
            "Observe tool results\n"
            "   |\n"
            "   v\n"
            "Evaluate + learn\n"
            "   |\n"
            "   +--> continue/revise if needed\n"
            "   |\n"
            "   v\n"
            "Final result\n"
            "```\n"
            "\n"
            "If the work becomes too broad for one agent, you can split responsibilities using "
            "a flow, an orchestrator, or a collaborating team.\n"
            "\n"
            "This gives you a reusable architectural lens:\n"
            "\n"
            "1. What is the goal?\n"
            "2. What role and constraints should the agent have?\n"
            "3. What tools can it use?\n"
            "4. How should it reason and plan?\n"
            "5. What knowledge and memory does it need?\n"
            "6. How will results be evaluated?\n"
            "7. Where should humans approve actions?\n"
            "8. Is one agent enough, or is a multi-agent pattern justified?\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: If an LLM can call a tool, it is automatically an agent\n"
            "\n"
            "> Tool use alone does not define an agent.\n"
            "\n"
            "A tool-augmented LLM may perform only one user-triggered action. The chapter's "
            "agent distinction depends more strongly on goal-level autonomy, multistep planning, "
            "decision-making, and continued execution.\n"
            "\n"
            "### Misconception 2: Autonomous means unsupervised\n"
            "\n"
            "> An agent can be autonomous in planning while still using human approval gates.\n"
            "\n"
            "High-stakes actions may require explicit confirmation even when the rest of the "
            "workflow runs automatically.\n"
            "\n"
            "### Misconception 3: More agents always produce a better system\n"
            "\n"
            "> Multi-agent systems add coordination cost, token usage, and latency.\n"
            "\n"
            "Use them when specialization, parallelism, context separation, or the nature of the "
            "problem justifies the added complexity.\n"
            "\n"
            "### Misconception 4: The five layers are a fixed execution pipeline\n"
            "\n"
            "> They are capability categories, not a mandatory runtime order.\n"
            "\n"
            "The layers interact repeatedly throughout the agent loop.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Agent | Software that perceives, decides, and acts toward a goal with some autonomy |\n"
            "| Agency | The ability to make decisions and take actions toward a goal |\n"
            "| Agentic | Describes behavior or systems that exhibit agency |\n"
            "| Assistant | Tool-using LLM system that remains more tightly controlled by user approvals |\n"
            "| Tool | Callable capability that lets an agent retrieve information or act outside the model |\n"
            "| Tool chaining | Using the output of one tool/action as input to a later step |\n"
            "| SPAL | Sense, Plan, Act, Learn — a recurring agent control loop |\n"
            "| MCP | Model Context Protocol, a standardized protocol for connecting AI systems to external tool servers |\n"
            "| Persona | Instructions defining an agent's role, behavior, style, and constraints |\n"
            "| Knowledge | External reference information available to the agent |\n"
            "| Memory | Interaction-derived information retained for later use |\n"
            "| RAG | Retrieve relevant information and add it to context before generation/reasoning |\n"
            "| Evaluation | Mechanisms used to judge the quality or correctness of agent results |\n"
            "| Agent flow | Sequential multi-agent assembly-line pattern |\n"
            "| Orchestration | Hub-and-spoke pattern with a central coordinating agent |\n"
            "| Collaboration | Multi-agent pattern where agents communicate and work as peers |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What does an agent do that a one-shot LLM application does not?\n"
            "2. Why is autonomy better understood as a spectrum?\n"
            "3. What separates an assistant from an agent in this chapter's terminology?\n"
            "4. What happens in each stage of the SPAL cycle?\n"
            "5. What is tool chaining?\n"
            "6. Why does MCP reduce repeated integration work?\n"
            "7. What are the five functional layers of an agent?\n"
            "8. How are knowledge and memory different?\n"
            "9. Why does context-window management matter?\n"
            "10. When might a multi-agent system be justified?\n"
            "11. How does agent flow differ from orchestration?\n"
            "12. Why can collaboration be more expensive than the other multi-agent patterns?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**An AI agent is not just an LLM with extra features. It is a goal-directed system "
            "that repeatedly senses context, plans, acts through tools, evaluates what happened, "
            "and continues until the goal is complete—while using the right amount of memory, "
            "oversight, and coordination for the task.**\n"
        ),

        "estimated_minutes": 135,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-agents",
                "title": "From answering questions to taking action",
                "order": 1,
            },
            {
                "id": "agentic-thinking",
                "title": "Agents, agency, and agentic thinking",
                "order": 2,
            },
            {
                "id": "interaction-patterns",
                "title": "Four common LLM interaction patterns",
                "order": 3,
            },
            {
                "id": "spal-cycle",
                "title": "The sense-plan-act-learn cycle",
                "order": 4,
            },
            {
                "id": "tools-and-actions",
                "title": "Tools turn language into action",
                "order": 5,
            },
            {
                "id": "mcp",
                "title": "Model Context Protocol (MCP)",
                "order": 6,
            },
            {
                "id": "five-layers",
                "title": "The five functional layers of an agent",
                "order": 7,
            },
            {
                "id": "persona-reasoning",
                "title": "Persona, reasoning, and planning",
                "order": 8,
            },
            {
                "id": "knowledge-memory-evaluation",
                "title": "Knowledge, memory, evaluation, and feedback",
                "order": 9,
            },
            {
                "id": "why-multi-agent",
                "title": "Why use more than one agent?",
                "order": 10,
            },
            {
                "id": "multi-agent-patterns",
                "title": "Three core multi-agent patterns",
                "order": 11,
            },
            {
                "id": "putting-it-together",
                "title": "Putting the whole architecture together",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Design a Sense-Plan-Act-Learn Loop",

            "lesson_code": "M01.L01",

            "section_id": "spal-cycle",

            "placement": "after_section",

            "description": (
                "Practice decomposing a higher-level goal into an agent loop with "
                "clear decisions, actions, and observations."
            ),

            "instructions": (
                "Use this goal: `Buy a suitable computer for a machine-learning student.`\n"
                "1. Write what the agent must sense or learn before acting.\n"
                "2. Break the goal into at least three tasks.\n"
                "3. Name a possible tool for each task.\n"
                "4. Show one example of tool chaining.\n"
                "5. For each action, write what the agent should inspect during the learn step.\n"
                "6. Identify one action that might deserve human approval and explain why."
            ),

            "expected_output": (
                "A compact SPAL workflow containing the goal, sensed context, ordered "
                "tasks, tools, one chained result, learn/evaluation steps, and one "
                "human-approval checkpoint."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "goal-decomposition",
                "spal-cycle",
                "tool-selection",
                "tool-chaining",
                "human-in-the-loop",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Choose a Multi-Agent Architecture",

            "lesson_code": "M01.L01",

            "section_id": "multi-agent-patterns",

            "placement": "after_section",

            "description": (
                "Practice selecting among agent flow, orchestration, and collaboration "
                "using the behavioral trade-offs introduced in the chapter."
            ),

            "instructions": (
                "Scenario: Build a system that creates a technical report from a research question.\n"
                "The work includes planning, collecting evidence, drafting, and quality review.\n"
                "1. Sketch an agent-flow solution.\n"
                "2. Sketch an orchestration solution.\n"
                "3. Sketch a collaboration solution.\n"
                "4. For each design, state how information moves between agents.\n"
                "5. Identify the likely cost/latency trade-off of each design.\n"
                "6. Choose the design you would start with and justify your choice using only "
                "the criteria taught in this lesson."
            ),

            "expected_output": (
                "Three small architecture diagrams or text flows plus a short comparison "
                "covering control structure, context sharing, and cost/latency trade-offs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "multi-agent-patterns",
                "architecture-selection",
                "context-sharing",
                "trade-off-analysis",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "The Rise of AI Agents — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "why-agents",

                "question": (
                    "Which capability most clearly moves a system from a one-shot LLM "
                    "response toward agent behavior?"
                ),

                "options": [
                    "Generating longer text",
                    "Using a larger vocabulary",
                    "Continuing to decide and act across multiple steps toward a goal",
                    "Always using more than one model",
                ],

                "correct": 2,

                "explanation": (
                    "The key shift is goal-directed multistep behavior: the system can "
                    "decide what to do next, act, observe results, and continue."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "interaction-patterns",

                "question": (
                    "In this chapter's terminology, what most strongly separates an "
                    "assistant from an agent?"
                ),

                "options": [
                    "Whether the system can generate natural language",
                    "Whether the system is connected to the internet",
                    "Where human approval sits and how much goal-level autonomy the system has",
                    "Whether the system uses Python",
                ],

                "correct": 2,

                "explanation": (
                    "Both assistants and agents may use tools. The chapter mainly separates "
                    "them by autonomy and the placement of human approval."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "spal-cycle",

                "question": (
                    "An agent calls a flight-search tool, inspects the returned options, "
                    "and decides the search needs to be changed. Which SPAL stage is the "
                    "inspection and decision mainly part of?"
                ),

                "options": [
                    "Sense",
                    "Plan",
                    "Act",
                    "Learn",
                ],

                "correct": 3,

                "explanation": (
                    "During Learn, the agent evaluates the result of an action and decides "
                    "whether to finish, continue, retry, or revise the plan."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "tools-and-actions",

                "question": "What is tool chaining?",

                "options": [
                    "Registering several tools with identical names",
                    "Using the output of one tool as input to a later action",
                    "Running every tool at the same time",
                    "Preventing the agent from changing its plan",
                ],

                "correct": 1,

                "explanation": (
                    "Tool chaining connects actions: information produced by one tool becomes "
                    "useful input for the next task or tool call."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "mcp",

                "question": (
                    "What is the main integration advantage of MCP described in the chapter?"
                ),

                "options": [
                    "It eliminates the need for tools",
                    "It guarantees every tool call will succeed",
                    "It provides a standardized, reusable way for agents to discover and call external tools",
                    "It forces all agent systems to use one programming language",
                ],

                "correct": 2,

                "explanation": (
                    "MCP standardizes the connection boundary so tool servers can be reused "
                    "rather than rebuilding provider-specific wrappers for every agent."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "five-layers",

                "question": "Which statement about the five functional layers is correct?",

                "options": [
                    "They must execute in a fixed top-to-bottom order",
                    "They are capability categories that can interact throughout the agent loop",
                    "Only multi-agent systems use them",
                    "Knowledge and memory replace reasoning and planning",
                ],

                "correct": 1,

                "explanation": (
                    "The layers organize capabilities. They interact dynamically rather than "
                    "forming a rigid runtime pipeline."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "knowledge-memory-evaluation",

                "question": "Which example is best classified as agent memory rather than knowledge?",

                "options": [
                    "A product manual",
                    "A code repository",
                    "A database schema",
                    "A user's preference recorded from an earlier session",
                ],

                "correct": 3,

                "explanation": (
                    "Memory is dynamic, interaction-derived information. Manuals, repositories, "
                    "and schemas are examples of external knowledge sources."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "multi-agent-patterns",

                "question": (
                    "Which multi-agent pattern places one central agent in charge of "
                    "delegating work to specialized workers?"
                ),

                "options": [
                    "Agent flow",
                    "Orchestration",
                    "Collaboration",
                    "Direct LLM chat",
                ],

                "correct": 1,

                "explanation": (
                    "Orchestration uses a hub-and-spoke structure: the orchestrator plans "
                    "and coordinates while worker agents handle specialized subgoals."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "multi-agent-patterns",

                "question": (
                    "Why might a collaborative team of agents be less efficient than an "
                    "agent-flow pipeline?"
                ),

                "options": [
                    "Collaborating agents cannot use tools",
                    "Collaboration often produces more back-and-forth communication, token use, and latency",
                    "Agent flow always uses a larger model",
                    "Collaboration does not allow specialized roles",
                ],

                "correct": 1,

                "explanation": (
                    "Peer communication and critique can improve difficult work, but they also "
                    "make the system more chatty, repetitive, costly, and slower."
                ),
            },

            {
                "id": "M01.L01.Q10",

                "section_id": "putting-it-together",

                "type": "open",

                "question": (
                    "You are designing an agent that can read project documents, create a plan, "
                    "update a project tracker, and ask for approval before deleting any record. "
                    "Map this system to the five functional layers and explain where the SPAL "
                    "cycle and human approval fit."
                ),
            },
        ],

        "passing_score": 70,
    },
}
