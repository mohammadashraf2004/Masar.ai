"""M01.L11 — Tips for Building Agentic Systems.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 11, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L11"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Turn the major concepts from the course into field-tested engineering "
    "patterns. Learn how to design production agents layer by layer across "
    "persona, tools/actions, reasoning/planning, knowledge/memory, and "
    "evaluation/feedback, then apply those principles to customer support, "
    "RAG, and deep research systems."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Tips for Building Agentic Systems",

    "slug": "ai-agents-m01-l11",

    "description": (
        "Apply field-tested patterns across the five agent layers and use them "
        "to design robust customer-support, RAG, and deep-research agent systems "
        "with narrow roles, focused tools, bounded reasoning, grounded retrieval, "
        "evaluation, observability, escalation, and production controls."
    ),

    "order": 11,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "agentic-systems",
        "persona-design",
        "tool-design",
        "reasoning-planning",
        "rag",
        "memory",
        "evaluation",
        "customer-support-agents",
        "deep-research",
        "grounding",
        "hitl",
        "observability",
        "production-patterns",
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
        "M01.L10",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Tips for Building Agentic Systems",

        "content": (
            "# Tips for Building Agentic Systems\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L11  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 11. "
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
            "- Use the five-layer agent model as a production design checklist.\n"
            "- Treat an agent persona as an API contract rather than vague prose.\n"
            "- Define narrow roles, explicit boundaries, and an `I don't know` path.\n"
            "- Prefer typed structured outputs when agents interact with code or other agents.\n"
            "- Use dynamic instructions without creating context bloat.\n"
            "- Design single-responsibility tools with strong names, schemas, and failure behavior.\n"
            "- Control tool invocation and avoid tool bloat.\n"
            "- Apply ReAct, plan-then-execute, self-review, and hard iteration limits appropriately.\n"
            "- Separate short-term sessions from long-term memory.\n"
            "- Treat RAG as a first-class capability and optimize retrieval independently.\n"
            "- Use ANN indexes, metadata filtering, hybrid retrieval, and deliberate embeddings.\n"
            "- Ground answers strictly and preserve the option to say `I don't know`.\n"
            "- Partition knowledge by role, tenant, domain, version, and date.\n"
            "- Build an evaluation and feedback layer with traces, automated evals, HITL, and guardrails.\n"
            "- Design a customer-support agentic system with triage, retrieval, grounding, action, and escalation.\n"
            "- Build a modular RAG agent system and know when not to add orchestration.\n"
            "- Build a two-tier deep-research system with a planner, stateless workers, critic, and writer.\n"
            "- Apply streaming, caching, budgets, and bounded loops to long-running agent systems.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Use the five agent layers as a design checklist\n"
            "\n"
            "The chapter returns to the five functional layers used throughout the book:\n"
            "\n"
            "1. **Persona**\n"
            "2. **Tools and actions**\n"
            "3. **Reasoning and planning**\n"
            "4. **Knowledge and memory**\n"
            "5. **Evaluation and feedback**\n"
            "\n"
            "The practical lesson is to optimize each layer independently before integrating the complete system.\n"
            "\n"
            "A production failure can often be traced to one layer:\n"
            "\n"
            "```text\n"
            "Wrong role / wandering scope      -> Persona\n"
            "Bad API behavior / misuse         -> Tools\n"
            "No decomposition / runaway loops  -> Reasoning\n"
            "Unsupported answers               -> Knowledge\n"
            "Undetected failures               -> Evaluation\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Five-layer production checklist | "
            "Stack five horizontal layers labeled Persona, Tools & Actions, Reasoning & Planning, Knowledge & Memory, Evaluation & Feedback. "
            "Inside each layer show 3-4 best-practice keywords from the lesson | "
            "Learner should notice that production quality depends on all five layers rather than one clever prompt]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Treat persona as an API contract\n"
            "\n"
            "The chapter's first production rule is that persona should not be vague storytelling.\n"
            "\n"
            "A useful persona defines:\n"
            "\n"
            "- role,\n"
            "- responsibility,\n"
            "- boundaries,\n"
            "- output contract,\n"
            "- uncertainty behavior.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "You are SupportMentor.\n"
            "You answer product-support questions using retrieved internal context.\n"
            "You do not make policy exceptions.\n"
            "If required evidence is missing, say you do not know.\n"
            "Return JSON matching the Answer schema.\n"
            "```\n"
            "\n"
            "This is closer to an interface specification than a character description.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Keep the agent's scope narrow\n"
            "\n"
            "Specialized agents are usually easier to:\n"
            "\n"
            "- test,\n"
            "- observe,\n"
            "- secure,\n"
            "- optimize,\n"
            "- reason about.\n"
            "\n"
            "A support agent responsible only for orders, returns, and delivery status is easier to harden than an agent that handles support, sales, billing, HR, and engineering.\n"
            "\n"
            "Narrow scope reduces ambiguity in both prompt instructions and tool selection.\n"
            "\n"
            "This also makes system composition easier because several focused agents can cooperate instead of one giant agent attempting everything.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Prefer typed structured outputs\n"
            "\n"
            "When an agent's result is consumed by code or another agent, free-form prose creates unnecessary parsing risk.\n"
            "\n"
            "The chapter uses Pydantic output such as:\n"
            "\n"
            "```python\n"
            "from pydantic import BaseModel, Field\n"
            "\n"
            "class Answer(BaseModel):\n"
            "    answer: str = Field(..., description=\"Concise user-facing answer\")\n"
            "    citations: list[str] = Field(default_factory=list)\n"
            "    confidence: float = Field(..., ge=0, le=1)\n"
            "```\n"
            "\n"
            "Typed output provides:\n"
            "\n"
            "- predictable fields,\n"
            "- easier validation,\n"
            "- less brittle parsing,\n"
            "- cleaner agent-to-agent integration,\n"
            "- lower ambiguity.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Use dynamic instructions carefully\n"
            "\n"
            "Some prompt information changes at runtime.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- current date,\n"
            "- organization name,\n"
            "- user role,\n"
            "- tenant,\n"
            "- environment.\n"
            "\n"
            "Instead of hardcoding such facts, inject them dynamically.\n"
            "\n"
            "```python\n"
            "from datetime import date\n"
            "\n"
            "def core_instructions(ctx, agent) -> str:\n"
            "    today = date.today().isoformat()\n"
            "    return (\n"
            "        f\"You are SupportMentor. Today is {today}.\\n\"\n"
            "        \"Answer concisely. Prefer retrieved context. \"\n"
            "        \"If context is missing, say you don't know.\"\n"
            "    )\n"
            "```\n"
            "\n"
            "But dynamic injection should remain relevant.\n"
            "\n"
            "Overinjection increases token usage and may distract the model with facts unrelated to the current goal.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Persona pattern in one view\n"
            "\n"
            "A strong persona should answer five questions:\n"
            "\n"
            "```text\n"
            "Who are you?\n"
            "What do you do?\n"
            "What must you not do?\n"
            "What do you return?\n"
            "What happens when you don't know?\n"
            "```\n"
            "\n"
            "This simple checklist prevents a surprising number of production failures.\n"
            "\n"
            "[[IMAGE_NEEDED: Persona as API contract | "
            "A contract card with five fields: Role, Responsibilities, Boundaries, Output Schema, Uncertainty/Fallback. "
            "Beside it show an example SupportMentor persona | "
            "Learner should notice that persona design defines operational behavior, not just tone]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Tools are the agent's hands and senses\n"
            "\n"
            "A strong model with poorly designed tools is still a weak system.\n"
            "\n"
            "The chapter gives five tool-design guidelines.\n"
            "\n"
            "### 1. Single responsibility\n"
            "\n"
            "Each tool should perform one clear job.\n"
            "\n"
            "### 2. Crisp descriptions and typed parameters\n"
            "\n"
            "The model learns how to use the tool from the tool's name, docstring, and schema.\n"
            "\n"
            "### 3. Prefer function tools for your own APIs/code\n"
            "\n"
            "Typed function definitions make schemas easy to generate and test.\n"
            "\n"
            "### 4. Control when tools run\n"
            "\n"
            "Use tool-choice settings, parallel-call settings, and prompt policy where appropriate.\n"
            "\n"
            "### 5. Plan for failure\n"
            "\n"
            "Timeouts, retries, structured error payloads, and fallbacks should be designed before failures occur.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. A well-scoped tool example\n"
            "\n"
            "The chapter demonstrates a focused order-status tool.\n"
            "\n"
            "```python\n"
            "import json\n"
            "from agents import function_tool\n"
            "\n"
            "def failure_error_function(context, error) -> str:\n"
            "    return json.dumps({\n"
            "        \"status\": \"error\",\n"
            "        \"message\": str(error),\n"
            "    })\n"
            "\n"
            "@function_tool(failure_error_function=failure_error_function)\n"
            "def lookup_order(order_id: str) -> dict:\n"
            "    \"\"\"Check order status by ID. Use when the user asks about their order.\"\"\"\n"
            "\n"
            "    if not order_id.startswith(\"ORD-\"):\n"
            "        raise ValueError(\"Invalid order id format\")\n"
            "\n"
            "    return {\n"
            "        \"status\": \"shipped\",\n"
            "        \"eta_days\": 3,\n"
            "    }\n"
            "```\n"
            "\n"
            "Why is this tool strong?\n"
            "\n"
            "- clear name,\n"
            "- one responsibility,\n"
            "- typed input,\n"
            "- validation,\n"
            "- helpful docstring,\n"
            "- structured failure behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Avoid tool bloat\n"
            "\n"
            "Every tool increases context overhead because the model must receive its description and schema.\n"
            "\n"
            "A giant tool catalog creates two costs:\n"
            "\n"
            "### Token cost\n"
            "\n"
            "Tool descriptions consume context on each relevant model call.\n"
            "\n"
            "### Decision cost\n"
            "\n"
            "The model must choose among more similar options, increasing the chance of the wrong selection.\n"
            "\n"
            "The chapter therefore recommends small role-specific tool sets.\n"
            "\n"
            "For MCP servers, inspect how many capabilities the server exposes rather than connecting a large server blindly.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Control tool invocation\n"
            "\n"
            "The agent should not always decide tool usage without constraints.\n"
            "\n"
            "Useful controls include:\n"
            "\n"
            "- `tool_choice=\"auto\"`,\n"
            "- force a required tool,\n"
            "- forbid tools on a turn,\n"
            "- allow parallel tool calls,\n"
            "- stop after the first sufficient tool result.\n"
            "\n"
            "This is especially useful when one API response fully answers the request and further calls only add latency and cost.\n"
            "\n"
            "Tool control is part of planning, not only SDK configuration.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Reasoning and planning need boundaries\n"
            "\n"
            "The chapter gives five practical reasoning rules.\n"
            "\n"
            "### Use ReAct for nontrivial tasks\n"
            "\n"
            "Alternate reasoning, action, and observation where external evidence matters.\n"
            "\n"
            "### Plan before executing large goals\n"
            "\n"
            "Create a short checklist or plan before taking many actions.\n"
            "\n"
            "### Limit iterations\n"
            "\n"
            "Always cap tool calls or turns.\n"
            "\n"
            "### Self-review before final\n"
            "\n"
            "Use a quick check for obvious mistakes and whether the question was actually answered.\n"
            "\n"
            "### Avoid unnecessary reasoning on simple tasks\n"
            "\n"
            "Simple one-shot work does not need a long deliberation loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Plan-then-execute with hard limits\n"
            "\n"
            "The source combines planning, ReAct-style observation, sequential thinking, and a maximum-turn budget.\n"
            "\n"
            "```python\n"
            "MAX_TURNS = 3\n"
            "\n"
            "instructions = f\"\"\"\n"
            "You are a planner-executor.\n"
            "\n"
            "1. Draft a concise 3-5 item checklist.\n"
            "2. Execute using tools.\n"
            "3. Inspect observations before continuing.\n"
            "4. Stop after at most {MAX_TURNS} tool calls.\n"
            "5. If budget is exhausted, return best effort with needs_followup.\n"
            "6. Self-review before finalizing.\n"
            "\"\"\"\n"
            "```\n"
            "\n"
            "The key idea is not the exact number `3`.\n"
            "\n"
            "The key idea is that reasoning must have an explicit budget and safe failure mode.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Reasoning capability is not reasoning reliability\n"
            "\n"
            "Modern models may already include built-in reasoning behavior.\n"
            "\n"
            "That does not mean they should be left unconstrained.\n"
            "\n"
            "Reasoning systems can still:\n"
            "\n"
            "- overthink simple tasks,\n"
            "- call unnecessary tools,\n"
            "- run too many steps,\n"
            "- follow a poor plan,\n"
            "- become expensive.\n"
            "\n"
            "The production goal is **guided reasoning**, not maximum reasoning.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Treat RAG as a first-class capability\n"
            "\n"
            "The chapter argues against stuffing large document sets directly into prompts.\n"
            "\n"
            "Instead:\n"
            "\n"
            "```text\n"
            "Knowledge base\n"
            "   |\n"
            "   v\n"
            "Retrieval tool\n"
            "   |\n"
            "   v\n"
            "Relevant context only\n"
            "   |\n"
            "   v\n"
            "Agent answer\n"
            "```\n"
            "\n"
            "This allows retrieval to be optimized independently from generation.\n"
            "\n"
            "It also allows the agent to search multiple corpora without carrying all documents into every call.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Separate session context from long-term memory\n"
            "\n"
            "The chapter draws a practical distinction:\n"
            "\n"
            "### Session memory\n"
            "\n"
            "Short-term thread state for the current conversation.\n"
            "\n"
            "### Long-term memory\n"
            "\n"
            "Persisted facts and preferences retrieved selectively later.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "Session: user asked about refund policy five minutes ago.\n"
            "Long-term: user prefers email notifications.\n"
            "```\n"
            "\n"
            "Long-term stores should be pruned rather than accumulating every conversation detail forever.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Optimize retrieval at scale\n"
            "\n"
            "The chapter recommends thinking beyond a basic flat vector index.\n"
            "\n"
            "Production retrieval may need:\n"
            "\n"
            "- approximate nearest-neighbor indexes such as HNSW or IVF,\n"
            "- domain sharding,\n"
            "- metadata filtering,\n"
            "- reranking,\n"
            "- multilingual or domain-specific embeddings,\n"
            "- date/version filters.\n"
            "\n"
            "A support query may need to retrieve only:\n"
            "\n"
            "```text\n"
            "tenant = acme\n"
            "role = customer\n"
            "product = API\n"
            "version = 3.2\n"
            "date <= current date\n"
            "```\n"
            "\n"
            "Filtering is both a relevance feature and an access-control feature.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Use hybrid retrieval instead of one retrieval signal\n"
            "\n"
            "The chapter explicitly warns against relying only on vector search.\n"
            "\n"
            "Combine retrieval families when the domain needs them:\n"
            "\n"
            "- semantic/vector,\n"
            "- keyword/lexical,\n"
            "- graph/hierarchical,\n"
            "- metadata filters,\n"
            "- reranking.\n"
            "\n"
            "Why?\n"
            "\n"
            "Because one query may need semantic similarity while another depends on an exact version number, code, name, or explicit relationship.\n"
            "\n"
            "Hybrid search gives the system both recall and precision.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Chunk coherently and ground strictly\n"
            "\n"
            "Poor chunking damages retrieval before the agent even begins reasoning.\n"
            "\n"
            "The chapter recommends semantically coherent chunks and strict grounding instructions.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Use only retrieved context.\n"
            "Cite supporting chunk IDs.\n"
            "If the answer is absent, say you do not know.\n"
            "```\n"
            "\n"
            "Grounding should be treated as a correctness requirement, not only a style preference.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Keep knowledge fresh and partitioned\n"
            "\n"
            "A single undifferentiated index may work during a demo and become unsafe later.\n"
            "\n"
            "Useful partitions include:\n"
            "\n"
            "- tenant,\n"
            "- department,\n"
            "- user role,\n"
            "- product,\n"
            "- version,\n"
            "- date,\n"
            "- content sensitivity.\n"
            "\n"
            "The retrieval layer should prevent the user from receiving content they are not authorized to see.\n"
            "\n"
            "Do not rely on the final LLM prompt to undo an access-control mistake after restricted context has already been retrieved.\n"
            "\n"
            "[[IMAGE_NEEDED: Partitioned RAG architecture | "
            "Show one logical knowledge system divided into tenant, role, product, version, and date partitions. A query passes through metadata/ACL filters "
            "before semantic or lexical search | "
            "Learner should notice that retrieval boundaries are enforced before content reaches the LLM]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Evaluation and feedback wrap the whole system\n"
            "\n"
            "The chapter's principle is simple:\n"
            "\n"
            "> You cannot improve what you do not measure.\n"
            "\n"
            "At minimum, record:\n"
            "\n"
            "- prompts,\n"
            "- tool calls,\n"
            "- token counts,\n"
            "- latency,\n"
            "- outcomes,\n"
            "- user feedback.\n"
            "\n"
            "Then add increasingly mature controls:\n"
            "\n"
            "- automated evaluations,\n"
            "- human review,\n"
            "- guardrails,\n"
            "- moderation,\n"
            "- schema checks,\n"
            "- regression tests.\n"
            "\n"
            "The chapter recommends an AIOps mindset:\n"
            "\n"
            "```text\n"
            "Measure -> Observe -> Improve -> Measure again\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Automate evaluations on every meaningful change\n"
            "\n"
            "Prompt changes, model changes, retrieval changes, and tool changes can all create regressions.\n"
            "\n"
            "A practical evaluation pipeline should maintain:\n"
            "\n"
            "- curated test cases,\n"
            "- known failure cases,\n"
            "- LLM-as-judge checks where semantic evaluation is needed,\n"
            "- accuracy and safety metrics,\n"
            "- resolution-rate metrics.\n"
            "\n"
            "Run these whenever behavior-changing components are updated.\n"
            "\n"
            "Observability systems such as Phoenix can help connect traces, datasets, experiments, and evaluations.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. HITL and guardrails are features, not afterthoughts\n"
            "\n"
            "Human feedback helps with cases that automated checks cannot resolve confidently.\n"
            "\n"
            "Guardrails enforce boundaries at:\n"
            "\n"
            "- input,\n"
            "- tool invocation,\n"
            "- output.\n"
            "\n"
            "A mature architecture may use a secondary critic or guardrail agent to inspect output before it reaches the user.\n"
            "\n"
            "HITL is especially useful for:\n"
            "\n"
            "- high-value refunds,\n"
            "- angry or vulnerable customers,\n"
            "- unclear policy,\n"
            "- irreversible actions,\n"
            "- low-confidence cases.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Customer support: map the five layers to the use case\n"
            "\n"
            "For customer support, the chapter maps the five layers like this:\n"
            "\n"
            "| Agent layer | Support implementation |\n"
            "|---|---|\n"
            "| Persona | Bounded support role |\n"
            "| Tools/actions | Lookup APIs, business APIs, human escalation |\n"
            "| Reasoning/planning | Triage and escalation decisions |\n"
            "| Knowledge/memory | RAG over manuals, policies, releases |\n"
            "| Evaluation/feedback | Logs, grounding checks, HITL feedback |\n"
            "\n"
            "The result is not one magical support bot. It is a small system of focused roles and controls.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Customer-support production guidelines\n"
            "\n"
            "The chapter recommends seven practical controls.\n"
            "\n"
            "### Narrow the charter\n"
            "\n"
            "Begin with a bounded set of intents such as orders, returns, and status.\n"
            "\n"
            "### Ground every answer\n"
            "\n"
            "Retrieve from manuals/policies and verify grounding where appropriate.\n"
            "\n"
            "### Make HITL easy\n"
            "\n"
            "Expose an explicit escalation tool.\n"
            "\n"
            "### Verify identity\n"
            "\n"
            "Authenticate before showing account-specific data.\n"
            "\n"
            "### Apply least privilege\n"
            "\n"
            "Tools should operate with the user's allowed scope.\n"
            "\n"
            "### Engineer resilience\n"
            "\n"
            "Retries, fallbacks, timeouts, and friendly error behavior matter.\n"
            "\n"
            "### Cache and rate-limit selectively\n"
            "\n"
            "Cache stable popular answers; throttle external APIs.\n"
            "\n"
            "### Preserve transparent traces\n"
            "\n"
            "Support teams need to audit searches, sources, tool calls, and escalation decisions.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Triage before action\n"
            "\n"
            "A support agent should first decide **which path** the request belongs to.\n"
            "\n"
            "A simplified escalation tool is:\n"
            "\n"
            "```python\n"
            "@function_tool\n"
            "def escalate_to_human(ticket_id: str, reason: str) -> str:\n"
            "    \"\"\"Escalate angry, high-value, or unclear-policy conversations.\"\"\"\n"
            "    return f\"Escalated ticket {ticket_id}: {reason}\"\n"
            "```\n"
            "\n"
            "The triage agent can choose among:\n"
            "\n"
            "- answer directly from known scope,\n"
            "- delegate to retrieval,\n"
            "- call an approved business API,\n"
            "- escalate to a human.\n"
            "\n"
            "Instructions should be written around these choices.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. A complete support agentic workflow\n"
            "\n"
            "The chapter's complete support workflow is effectively multi-agent:\n"
            "\n"
            "```text\n"
            "User\n"
            " |\n"
            " v\n"
            "Triage Agent\n"
            " |------------------------> Human\n"
            " v\n"
            "Retrieval Agent\n"
            " |\n"
            " v\n"
            "Grounding Agent\n"
            " |\n"
            " +--> if action needed -> Scoped Business API\n"
            " |                          |\n"
            " |                          v\n"
            " |                     Guardrail Agent\n"
            " v\n"
            "Answer Agent\n"
            " |\n"
            " v\n"
            "User + feedback\n"
            "```\n"
            "\n"
            "This architecture separates retrieval, validation, action, and presentation rather than making one agent responsible for every concern.\n"
            "\n"
            "{{exercise:M01.L11.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 27. RAG agent systems: retrieval is the engine\n"
            "\n"
            "The chapter makes an important architectural distinction:\n"
            "\n"
            "> Retrieval is the core capability; agentic control adds routing, critique, refinement, and action around it.\n"
            "\n"
            "Do not add an orchestrator simply because you are building RAG.\n"
            "\n"
            "If this works:\n"
            "\n"
            "```text\n"
            "Query -> retrieve -> answer\n"
            "```\n"
            "\n"
            "then keep it simple.\n"
            "\n"
            "Add agentic components only when you need:\n"
            "\n"
            "- routing across corpora,\n"
            "- corrective retrieval,\n"
            "- diagnostics,\n"
            "- actions,\n"
            "- multistep refinement.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Modular RAG roles\n"
            "\n"
            "A useful progression is:\n"
            "\n"
            "```text\n"
            "Router/Triage\n"
            "    |\n"
            "    v\n"
            "Retriever\n"
            "    |\n"
            "    v\n"
            "Answerer\n"
            "```\n"
            "\n"
            "Optional additions include:\n"
            "\n"
            "- context-ranking agent,\n"
            "- grounding agent,\n"
            "- corrective-retrieval critic,\n"
            "- query-refinement agent.\n"
            "\n"
            "Each role should exist because it solves a specific observed problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. A grounded RAG answerer\n"
            "\n"
            "The chapter provides a simple reminder pattern:\n"
            "\n"
            "```python\n"
            "@function_tool\n"
            "def retrieve(\n"
            "    query: str,\n"
            "    corpus: str = \"product_docs\",\n"
            "    top_k: int = 5,\n"
            ") -> list[dict]:\n"
            "    \"\"\"Return top-k passages with metadata.\"\"\"\n"
            "    return [\n"
            "        {\n"
            "            \"text\": \"...\",\n"
            "            \"source\": \"KB-123\",\n"
            "            \"section\": \"Refunds\",\n"
            "        }\n"
            "    ]\n"
            "\n"
            "answerer = Agent(\n"
            "    name=\"RAG-Answerer\",\n"
            "    instructions=(\n"
            "        \"Use ONLY passages from retrieve. \"\n"
            "        \"If they do not answer the question, say you do not know. \"\n"
            "        \"Cite sources.\"\n"
            "    ),\n"
            "    tools=[retrieve],\n"
            ")\n"
            "```\n"
            "\n"
            "The simplicity is deliberate: begin with the minimum architecture that meets the goal.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Corrective retrieval needs a bounded loop\n"
            "\n"
            "Advanced RAG systems may evaluate retrieved context before answering.\n"
            "\n"
            "```text\n"
            "Query\n"
            " |\n"
            " v\n"
            "Retrieve\n"
            " |\n"
            " v\n"
            "Rank / Grounding check\n"
            " |             |\n"
            " good          weak\n"
            " |             |\n"
            " v             v\n"
            "Answer     Refine query\n"
            "               |\n"
            "               +----> Retrieve again\n"
            "```\n"
            "\n"
            "The chapter explicitly notes that this refinement loop must have a counter or other stop condition.\n"
            "\n"
            "Corrective retrieval without bounded retries can become another runaway agent loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Measure RAG at retrieval and answer layers\n"
            "\n"
            "Do not evaluate only the final generated text.\n"
            "\n"
            "Track:\n"
            "\n"
            "- retrieval recall,\n"
            "- retrieval relevance,\n"
            "- answer accuracy,\n"
            "- grounding/citation quality,\n"
            "- cases where the agent should have said `I don't know`,\n"
            "- failed/refined search queries.\n"
            "\n"
            "This distinction matters because a bad answer may come from bad retrieval rather than bad generation.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Deep research requires a team, not a single giant prompt\n"
            "\n"
            "Deep research combines:\n"
            "\n"
            "- open-ended search,\n"
            "- iterative planning,\n"
            "- source collection,\n"
            "- analysis,\n"
            "- contradiction handling,\n"
            "- final synthesis.\n"
            "\n"
            "The chapter recommends this architecture only when simpler systems are insufficient because the coordination cost is significant.\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Two-tier orchestration: brain and hands\n"
            "\n"
            "The chapter's deep-research blueprint uses a planner as the brain and stateless workers as hands.\n"
            "\n"
            "### Brain\n"
            "\n"
            "Research planner:\n"
            "\n"
            "- decomposes the goal,\n"
            "- decides what to search next,\n"
            "- tracks coverage,\n"
            "- routes work.\n"
            "\n"
            "### Hands\n"
            "\n"
            "Workers:\n"
            "\n"
            "- web searcher,\n"
            "- extractor,\n"
            "- analyst,\n"
            "- summarizer/writer.\n"
            "\n"
            "Workers should remain as stateless and tool-like as possible unless they need their own decision-making loops.\n"
            "\n"
            "This keeps strategic state centralized while specialized workers stay simple.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Force evidence-backed research behavior\n"
            "\n"
            "For factual claims, the deep-research planner should be required to use retrieval or web/document tools.\n"
            "\n"
            "A useful policy is:\n"
            "\n"
            "```text\n"
            "No factual claim without an identified source.\n"
            "Use search/document tools for facts.\n"
            "Track sources throughout the run.\n"
            "Do not finalize unsupported claims.\n"
            "```\n"
            "\n"
            "This prevents the planner from bypassing the research process and answering from model memory alone.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Critic before writer\n"
            "\n"
            "After research workers gather enough evidence, the chapter inserts a critic before final synthesis.\n"
            "\n"
            "The critic checks:\n"
            "\n"
            "- completeness,\n"
            "- missing perspectives,\n"
            "- bias,\n"
            "- contradictions,\n"
            "- whether enough evidence exists to answer.\n"
            "\n"
            "If evidence is insufficient:\n"
            "\n"
            "```text\n"
            "Critic -> Planner -> more research\n"
            "```\n"
            "\n"
            "If evidence is sufficient:\n"
            "\n"
            "```text\n"
            "Critic -> Writer -> final cited report\n"
            "```\n"
            "\n"
            "This cleanly separates discovery, quality control, and communication.\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Stream progress during long-running research\n"
            "\n"
            "Deep research may take long enough that a silent interface feels broken.\n"
            "\n"
            "The chapter recommends streaming partial progress such as:\n"
            "\n"
            "- current search stage,\n"
            "- evolving outline,\n"
            "- source collection progress,\n"
            "- high-level status updates.\n"
            "\n"
            "This improves perceived latency and creates opportunities for checkpoint approvals.\n"
            "\n"
            "The important UX idea is to make progress visible without requiring the system to expose private internal model reasoning.\n"
            "\n"
            "---\n"
            "\n"

            "## 37. Deep research needs cache, call, and token budgets\n"
            "\n"
            "Long-running systems can become expensive quickly.\n"
            "\n"
            "Use:\n"
            "\n"
            "- repeated-query caching,\n"
            "- per-run token budgets,\n"
            "- API-call budgets,\n"
            "- throttling,\n"
            "- alerting.\n"
            "\n"
            "But cache freshness matters.\n"
            "\n"
            "A repeated search result may be useful today and stale later.\n"
            "\n"
            "Therefore caching needs expiration and invalidation rather than a permanent `store everything` policy.\n"
            "\n"
            "---\n"
            "\n"

            "## 38. Integrated production checklist\n"
            "\n"
            "When reviewing an agentic system, ask the following.\n"
            "\n"
            "### Persona\n"
            "\n"
            "- Is the role narrow?\n"
            "- Are boundaries explicit?\n"
            "- Is there an `I don't know` path?\n"
            "- Is the output typed when code consumes it?\n"
            "\n"
            "### Tools\n"
            "\n"
            "- Does every tool have one responsibility?\n"
            "- Are names/docstrings/parameters clear?\n"
            "- Are failure modes structured?\n"
            "- Is the tool set small enough?\n"
            "\n"
            "### Reasoning\n"
            "\n"
            "- Is reasoning used only where it helps?\n"
            "- Is there a plan for large goals?\n"
            "- Are turns/iterations bounded?\n"
            "- Is there a self-review or critic path?\n"
            "\n"
            "### Knowledge and memory\n"
            "\n"
            "- Is retrieval first-class?\n"
            "- Are session and long-term memory separated?\n"
            "- Is retrieval hybrid when needed?\n"
            "- Is access partitioned correctly?\n"
            "- Can the agent safely say `I don't know`?\n"
            "\n"
            "### Evaluation and feedback\n"
            "\n"
            "- Are traces complete?\n"
            "- Are prompt/model changes evaluated automatically?\n"
            "- Is user feedback captured?\n"
            "- Are guardrails present around risky actions?\n"
            "\n"
            "{{exercise:M01.L11.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: A strong persona is mainly about tone\n"
            "\n"
            "> Production persona design defines role, boundaries, uncertainty, and output contract.\n"
            "\n"
            "### Misconception 2: More tools always make an agent more capable\n"
            "\n"
            "> Excess tools increase context cost and selection ambiguity.\n"
            "\n"
            "### Misconception 3: Reasoning models do not need explicit limits\n"
            "\n"
            "> Reasoning still needs turn budgets, stop conditions, and safe fallback behavior.\n"
            "\n"
            "### Misconception 4: RAG means putting all documents into the prompt\n"
            "\n"
            "> Production RAG uses retrieval to select only relevant context.\n"
            "\n"
            "### Misconception 5: One vector index is enough for every future RAG use case\n"
            "\n"
            "> Production systems often require partitions, hybrid search, filtering, reranking, and freshness controls.\n"
            "\n"
            "### Misconception 6: A support agent is one agent\n"
            "\n"
            "> Mature support workflows often contain triage, retrieval, grounding, business-action, guardrail, answer, and HITL roles.\n"
            "\n"
            "### Misconception 7: Every RAG application needs an agentic orchestrator\n"
            "\n"
            "> If one retrieval call plus one answer step solves the task, keep it simple.\n"
            "\n"
            "### Misconception 8: Deep research should keep every worker stateful\n"
            "\n"
            "> The chapter recommends centralized planning with workers kept as stateless/tool-like as practical.\n"
            "\n"
            "### Misconception 9: Caching is always good\n"
            "\n"
            "> Stale cache entries can damage search quality and factual freshness.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Persona contract | Operational definition of agent role, boundaries, outputs, and uncertainty behavior |\n"
            "| Dynamic instructions | Runtime prompt facts injected programmatically |\n"
            "| Single-responsibility tool | Tool designed to perform one clear operation |\n"
            "| Tool bloat | Excessive tool catalog causing token and selection overhead |\n"
            "| Plan-then-execute | Build a short plan before performing a larger multi-step task |\n"
            "| Self-review | Quick final pass used to catch obvious mistakes |\n"
            "| Session memory | Short-term conversational state |\n"
            "| Long-term memory | Persisted facts or preferences retrieved selectively later |\n"
            "| ANN | Approximate nearest-neighbor indexing for scalable vector search |\n"
            "| Hybrid retrieval | Combining semantic, lexical, graph, metadata, and/or reranking signals |\n"
            "| Grounding | Restricting claims to retrieved authoritative context |\n"
            "| HITL | Human-in-the-loop feedback, review, or escalation |\n"
            "| Triage agent | Agent that selects the appropriate support/workflow path |\n"
            "| Corrective RAG | RAG pattern that evaluates and refines retrieval when context is weak |\n"
            "| Two-tier orchestration | Planner/brain delegating to focused workers/hands |\n"
            "| Stateless worker | Worker that performs a task without owning long-lived global planning state |\n"
            "| Critic agent | Evaluator that checks completeness, contradictions, bias, or quality |\n"
            "| Streaming UX | User experience that surfaces partial progress during long-running work |\n"
            "| AIOps | Measure-observe-improve operating cycle applied to AI systems |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are the five functional agent layers?\n"
            "2. Why should persona be treated as an API contract?\n"
            "3. Why does narrow scope improve production quality?\n"
            "4. When should you use typed output?\n"
            "5. What is the risk of overusing dynamic instructions?\n"
            "6. What makes a tool well designed?\n"
            "7. Why does tool bloat hurt both cost and quality?\n"
            "8. What controls can govern tool invocation?\n"
            "9. When is ReAct appropriate?\n"
            "10. Why should large goals use a plan before execution?\n"
            "11. Why should iterations be bounded?\n"
            "12. Why treat RAG as a first-class tool instead of stuffing documents into prompts?\n"
            "13. How is session context different from long-term memory?\n"
            "14. What do ANN indexes and metadata filters contribute?\n"
            "15. Why use hybrid retrieval?\n"
            "16. Why does partitioning matter for both quality and security?\n"
            "17. What should a minimal evaluation stack capture?\n"
            "18. Why automate evals after prompt/model/tool changes?\n"
            "19. What paths should a support triage agent be able to choose?\n"
            "20. Why should account actions enforce identity and least privilege?\n"
            "21. What roles appear in the complete support workflow?\n"
            "22. When should a RAG system remain one-shot rather than agentic?\n"
            "23. What does a corrective RAG loop do?\n"
            "24. Why must corrective retrieval be bounded?\n"
            "25. What is the brain-and-hands deep-research pattern?\n"
            "26. Why should factual deep-research claims be tool-backed?\n"
            "27. What does the critic do before final writing?\n"
            "28. Why is streaming useful in deep research?\n"
            "29. Why do research caches require freshness policies?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Production-ready agentic systems are built by getting the fundamentals right at every layer: a narrow "
            "persona, focused tools, bounded reasoning, disciplined retrieval and memory, and relentless evaluation. "
            "Then compose those pieces only when the use case needs them. The strongest system is rarely the one with "
            "the most agents—it is the one whose roles, tools, evidence, escalation paths, and feedback loops are clearest.**\n"
        ),

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "five-layer-review", "title": "Use the five agent layers as a design checklist", "order": 1},
            {"id": "persona-contract", "title": "Treat persona as an API contract", "order": 2},
            {"id": "persona-scope", "title": "Keep the agent's scope narrow", "order": 3},
            {"id": "structured-output", "title": "Prefer typed structured outputs", "order": 4},
            {"id": "dynamic-instructions", "title": "Use dynamic instructions carefully", "order": 5},
            {"id": "persona-pattern", "title": "Persona pattern in one view", "order": 6},
            {"id": "tool-design", "title": "Tools are the agent's hands and senses", "order": 7},
            {"id": "tool-example", "title": "A well-scoped tool example", "order": 8},
            {"id": "tool-bloat", "title": "Avoid tool bloat", "order": 9},
            {"id": "tool-policy", "title": "Control tool invocation", "order": 10},
            {"id": "reasoning-guidelines", "title": "Reasoning and planning need boundaries", "order": 11},
            {"id": "planning-code", "title": "Plan-then-execute with hard limits", "order": 12},
            {"id": "reasoning-control", "title": "Reasoning capability is not reasoning reliability", "order": 13},
            {"id": "rag-first-class", "title": "Treat RAG as a first-class capability", "order": 14},
            {"id": "session-vs-memory", "title": "Separate session context from long-term memory", "order": 15},
            {"id": "retrieval-scale", "title": "Optimize retrieval at scale", "order": 16},
            {"id": "hybrid-retrieval", "title": "Use hybrid retrieval instead of one retrieval signal", "order": 17},
            {"id": "chunk-ground", "title": "Chunk coherently and ground strictly", "order": 18},
            {"id": "partition-data", "title": "Keep knowledge fresh and partitioned", "order": 19},
            {"id": "evaluation-layer", "title": "Evaluation and feedback wrap the whole system", "order": 20},
            {"id": "automated-evals", "title": "Automate evaluations on every meaningful change", "order": 21},
            {"id": "hitl-guardrails", "title": "HITL and guardrails are features, not afterthoughts", "order": 22},
            {"id": "support-overview", "title": "Customer support: map the five layers to the use case", "order": 23},
            {"id": "support-guidelines", "title": "Customer-support production guidelines", "order": 24},
            {"id": "support-triage", "title": "Triage before action", "order": 25},
            {"id": "support-workflow", "title": "A complete support agentic workflow", "order": 26},
            {"id": "rag-agent-system", "title": "RAG agent systems: retrieval is the engine", "order": 27},
            {"id": "rag-roles", "title": "Modular RAG roles", "order": 28},
            {"id": "rag-answerer", "title": "A grounded RAG answerer", "order": 29},
            {"id": "corrective-rag", "title": "Corrective retrieval needs a bounded loop", "order": 30},
            {"id": "rag-observability", "title": "Measure RAG at retrieval and answer layers", "order": 31},
            {"id": "deep-research-overview", "title": "Deep research requires a team, not a single giant prompt", "order": 32},
            {"id": "two-tier-orchestration", "title": "Two-tier orchestration: brain and hands", "order": 33},
            {"id": "deep-research-tool-policy", "title": "Force evidence-backed research behavior", "order": 34},
            {"id": "critic-writer", "title": "Critic before writer", "order": 35},
            {"id": "streaming-ux", "title": "Stream progress during long-running research", "order": 36},
            {"id": "research-budgets", "title": "Deep research needs cache, call, and token budgets", "order": 37},
            {"id": "integrated-checklist", "title": "Integrated production checklist", "order": 38},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L11.EX01",

            "title": "Design a Production Customer-Support Agentic System",

            "lesson_code": "M01.L11",

            "section_id": "support-workflow",

            "placement": "after_section",

            "description": (
                "Apply all five agent layers to a customer-support workflow with "
                "triage, retrieval, grounding, scoped actions, escalation, and feedback."
            ),

            "instructions": (
                "Scenario: Build a customer-support system for orders, delivery status, returns, and refunds.\n"
                "1. Write a narrow persona contract for the triage agent.\n"
                "2. Define a typed output schema containing route, answer, confidence, and citations.\n"
                "3. Create focused tools for order lookup and human escalation.\n"
                "4. Add a retrieval agent over policies and release notes.\n"
                "5. Add identity verification before account-specific tool calls.\n"
                "6. Apply least-privilege access to business APIs.\n"
                "7. Add a grounding agent before any policy answer reaches the user.\n"
                "8. Add a guardrail around high-value refunds or account-changing actions.\n"
                "9. Define retries, timeout, fallback, and friendly failure behavior.\n"
                "10. Add caching for stable policy answers and rate limiting around external APIs.\n"
                "11. Record per-conversation traces including searches and cited sources.\n"
                "12. Capture thumbs-up/down feedback and define how failed interactions enter an evaluation dataset.\n"
                "13. Draw the full User -> Triage -> Retrieval -> Grounding -> Action/Guardrail -> Answer/Human flow."
            ),

            "expected_output": (
                "A complete support-agent architecture showing narrow roles, typed contracts, "
                "tools, RAG, identity, least privilege, grounding, guardrails, HITL, resilience, "
                "caching, rate limits, tracing, and user feedback."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "persona-design",
                "tool-design",
                "customer-support",
                "rag",
                "grounding",
                "hitl",
                "least-privilege",
                "guardrails",
                "observability",
            ],
        },

        {
            "id": "M01.L11.EX02",

            "title": "Design an Evidence-Driven Deep Research System",

            "lesson_code": "M01.L11",

            "section_id": "integrated-checklist",

            "placement": "after_section",

            "description": (
                "Combine the chapter's field-tested guidance into a bounded, "
                "observable, grounded deep-research architecture."
            ),

            "instructions": (
                "Scenario: Build an internal research system that compares several technical solutions using web and internal-document evidence.\n"
                "1. Create a planner/brain agent responsible for decomposition and routing.\n"
                "2. Create focused workers for search, extraction, and analysis.\n"
                "3. Keep worker state minimal; centralize global research progress in the planner/controller.\n"
                "4. Require all factual claims to come from search or document tools.\n"
                "5. Add source tracking to every retrieved finding.\n"
                "6. Add a critic that checks completeness, contradictions, bias, and missing perspectives.\n"
                "7. Route back to research when the critic says evidence is insufficient.\n"
                "8. Bound the refinement loop with iteration, token, and external-call budgets.\n"
                "9. Add a writer that produces the final cited report only after the critic passes the evidence.\n"
                "10. Stream high-level progress and the evolving outline to the UI.\n"
                "11. Cache repeated searches with a freshness/TTL policy.\n"
                "12. Record traces, tool calls, latency, cost, and source coverage.\n"
                "13. Define the tests that decide whether this architecture actually performs better than a simpler one-shot RAG system."
            ),

            "expected_output": (
                "A two-tier deep-research architecture with planner, focused workers, "
                "tool-use policy, critic loop, bounded retries, cited writer, streaming UX, "
                "caching/freshness policy, observability, and a comparison plan against one-shot RAG."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "deep-research",
                "orchestration",
                "worker-agents",
                "tool-policy",
                "critic-agent",
                "grounding",
                "bounded-loops",
                "streaming",
                "caching",
                "evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L11.QZ01",

        "title": "Tips for Building Agentic Systems — Knowledge Check",

        "lesson_code": "M01.L11",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L11.Q01",
                "section_id": "five-layer-review",
                "question": "Which is one of the five functional agent layers used in the chapter?",
                "options": [
                    "Persona",
                    "CSS rendering",
                    "GPU scheduling",
                    "DNS management",
                ],
                "correct": 0,
                "explanation": (
                    "The five layers are persona, tools/actions, reasoning/planning, knowledge/memory, and evaluation/feedback."
                ),
            },

            {
                "id": "M01.L11.Q02",
                "section_id": "persona-contract",
                "question": "Why should persona be treated like an API contract?",
                "options": [
                    "Because persona should only describe tone",
                    "Because it should clearly define role, boundaries, output behavior, and uncertainty handling",
                    "Because APIs always use natural language",
                    "Because it removes the need for tools",
                ],
                "correct": 1,
                "explanation": (
                    "Production persona design specifies operational behavior, not merely style."
                ),
            },

            {
                "id": "M01.L11.Q03",
                "section_id": "tool-bloat",
                "question": "What is one problem caused by tool bloat?",
                "options": [
                    "Fewer context tokens are used",
                    "The model faces more schema/context overhead and more difficult tool selection",
                    "The agent becomes deterministic",
                    "Tools stop requiring descriptions",
                ],
                "correct": 1,
                "explanation": (
                    "Large tool sets cost tokens and increase decision ambiguity."
                ),
            },

            {
                "id": "M01.L11.Q04",
                "section_id": "reasoning-guidelines",
                "question": "Which task least needs explicit multistep reasoning?",
                "options": [
                    "A one-shot format conversion",
                    "A multistep troubleshooting problem",
                    "A deep research task",
                    "A tool-heavy investigation",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter recommends avoiding unnecessary reasoning on simple one-shot work."
                ),
            },

            {
                "id": "M01.L11.Q05",
                "section_id": "planning-code",
                "question": "Why should a reasoning agent have a maximum-turn limit?",
                "options": [
                    "To prevent runaway loops and define safe fallback behavior",
                    "To eliminate all tool calls",
                    "To make every task fail after one step",
                    "To disable self-review",
                ],
                "correct": 0,
                "explanation": (
                    "Hard limits control latency and cost and create a predictable failure path."
                ),
            },

            {
                "id": "M01.L11.Q06",
                "section_id": "rag-first-class",
                "question": "Why should RAG be treated as a first-class capability?",
                "options": [
                    "So the entire knowledge base can be pasted into every prompt",
                    "So retrieval can select relevant evidence independently from generation",
                    "So memory is never required",
                    "So citations are unnecessary",
                ],
                "correct": 1,
                "explanation": (
                    "Retrieval should be a dedicated capability rather than uncontrolled prompt stuffing."
                ),
            },

            {
                "id": "M01.L11.Q07",
                "section_id": "hybrid-retrieval",
                "question": "Why combine semantic and keyword retrieval?",
                "options": [
                    "Because one retrieval signal cannot serve both fuzzy semantic matches and exact identifiers equally well",
                    "Because vector search cannot use text",
                    "Because keyword search always understands paraphrases",
                    "Because hybrid search removes the need for filters",
                ],
                "correct": 0,
                "explanation": (
                    "Hybrid retrieval combines complementary strengths for recall and precision."
                ),
            },

            {
                "id": "M01.L11.Q08",
                "section_id": "partition-data",
                "question": "Why should RAG data be partitioned by role or tenant?",
                "options": [
                    "Only to make indexes larger",
                    "To improve relevance and prevent unauthorized context from reaching the agent",
                    "To remove the need for metadata",
                    "To guarantee no duplicates",
                ],
                "correct": 1,
                "explanation": (
                    "Partitioning helps both retrieval quality and access control."
                ),
            },

            {
                "id": "M01.L11.Q09",
                "section_id": "evaluation-layer",
                "question": "Which statement best reflects the chapter's evaluation philosophy?",
                "options": [
                    "If the agent works once, tracing is unnecessary",
                    "Measure internal and external behavior so the system can be debugged and improved",
                    "Only final answers matter",
                    "Human feedback should be ignored",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes logging, tracing, evaluation, feedback, and iterative improvement."
                ),
            },

            {
                "id": "M01.L11.Q10",
                "section_id": "support-workflow",
                "question": "What should happen before an account-specific support action?",
                "options": [
                    "Verify identity and apply least-privilege access",
                    "Give the agent administrator credentials",
                    "Skip retrieval",
                    "Disable traces",
                ],
                "correct": 0,
                "explanation": (
                    "Support systems should authenticate users and scope tools to permitted actions."
                ),
            },

            {
                "id": "M01.L11.Q11",
                "section_id": "rag-agent-system",
                "question": "When should a RAG system avoid adding an orchestrator?",
                "options": [
                    "When one retrieval step and one answer step already solve the task well",
                    "Whenever citations are needed",
                    "Whenever a vector database is used",
                    "Whenever the answer is short",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly recommends keeping one-shot RAG simple when it already works."
                ),
            },

            {
                "id": "M01.L11.Q12",
                "section_id": "corrective-rag",
                "question": "Why must a corrective-RAG refinement loop be bounded?",
                "options": [
                    "Because query refinement is illegal",
                    "Because repeated retrieval can otherwise become an endless cost/latency loop",
                    "Because grounding cannot be evaluated twice",
                    "Because RAG cannot use loops",
                ],
                "correct": 1,
                "explanation": (
                    "Corrective retrieval needs explicit retry or iteration limits."
                ),
            },

            {
                "id": "M01.L11.Q13",
                "section_id": "two-tier-orchestration",
                "question": "What is the main idea of two-tier orchestration in deep research?",
                "options": [
                    "Every worker owns the full global research plan",
                    "A planner/brain owns strategy while focused workers/hands perform specialized tasks",
                    "Only one tool is allowed",
                    "The writer controls all retrieval",
                ],
                "correct": 1,
                "explanation": (
                    "The architecture centralizes strategic control while keeping workers focused and tool-like."
                ),
            },

            {
                "id": "M01.L11.Q14",
                "section_id": "critic-writer",
                "question": "What should happen if the deep-research critic finds that evidence is incomplete?",
                "options": [
                    "The writer should invent the missing details",
                    "Control should return to the planner for additional research",
                    "The system should delete all sources",
                    "The report should be finalized immediately",
                ],
                "correct": 1,
                "explanation": (
                    "The critic is a quality gate that can trigger another bounded research pass."
                ),
            },

            {
                "id": "M01.L11.Q15",
                "section_id": "integrated-checklist",
                "type": "open",
                "question": (
                    "Design a production agentic system for either customer support, internal RAG, or deep research. "
                    "Explain the persona contract, tool boundaries, reasoning limits, retrieval/memory design, grounding "
                    "rules, evaluation/observability, HITL/escalation path, caching/budget controls, and why each agent "
                    "or component is necessary."
                ),
            },
        ],

        "passing_score": 70,
    },
}
