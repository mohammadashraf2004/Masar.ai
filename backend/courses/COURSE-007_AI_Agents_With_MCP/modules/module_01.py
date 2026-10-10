"""M01.L01 — From LLMs to Agents and the Model Context Protocol.

Two source chapters -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapters 1–2 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Agentic AI & MCP Foundations"

MODULE_DESCRIPTION = (
    "Understand how LLM applications evolved into agents, how agentic loops differ "
    "from deterministic workflows, why MCP was created, and how MCP clients, "
    "servers, transports, tools, resources, and prompts work together."
)

SOURCE_CHAPTER = "1–2"

SOURCE_PAGES = "Not provided in the supplied chapter extracts"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "From LLMs to Agents and the Model Context Protocol",

    "slug": "ai-agents-mcp-m01-l01",

    "description": (
        "A practical foundation for agentic AI and MCP: move from plain LLMs to "
        "augmented LLMs and self-directed agents, distinguish agents from fixed "
        "agentic workflows, then learn why MCP exists and how its architecture "
        "connects models to tools, data, prompts, and external systems."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "agentic-ai",
        "llm-agents",
        "react",
        "tool-use",
        "mcp",
        "context-engineering",
        "mcp-client",
        "mcp-server",
        "mcp-transport",
        "json-rpc",
        "agent-workflows",
    ],

    "prerequisite_ids": [],

    "lesson": {
        "title": "From LLMs to Agents and the Model Context Protocol",

        "content": (
            "# From LLMs to Agents and the Model Context Protocol\n"
            "\n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Agentic AI & MCP Foundations  \n"
            "> **Source alignment:** Chapters 1–2 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain how plain LLM chat evolved through RAG and function calling into augmented LLMs and agents.\n"
            "- Describe the Reason → Act → Observe loop and why feedback is central to agent behavior.\n"
            "- Distinguish an autonomous agent from a code-controlled agentic workflow.\n"
            "- Recognize common workflow patterns such as prompt chaining, routing, parallelization, orchestrator-worker, and evaluator-optimizer.\n"
            "- Explain the M × N integration problem and how MCP changes it into an M + N problem.\n"
            "- Describe the roles of the host application, MCP client, MCP server, and transport.\n"
            "- Distinguish MCP tools, resources, and prompts.\n"
            "- Compare local stdio transport with remote Streamable HTTP transport.\n"
            "- Explain requests, responses, notifications, and the modern stateless MCP connection model described in the source.\n"
            "- Apply practical design guidance when choosing tools, MCP servers, CLIs, or skills.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. From a plain LLM to an agent\n"
            "\n"
            "A useful way to understand agents is to start with what early LLM applications could **not** do.\n"
            "\n"
            "A basic LLM chat application receives text and produces text. Its behavior is limited by the information "
            "available in its training and whatever context is included in the current request. It can explain, summarize, "
            "or generate content, but by itself it cannot reach into your files, query a live database, run a test suite, "
            "or update an external service.\n"
            "\n"
            "The first major step beyond this limitation was **retrieval-augmented generation (RAG)**. In a typical early RAG "
            "flow, middleware intercepts the user's query, searches a vector database for semantically related information, "
            "adds that retrieved information to the prompt, and then sends the enriched prompt to the LLM.\n"
            "\n"
            "RAG changes what the model can **know at request time**, but not necessarily what it can **do**.\n"
            "\n"
            "A second major step was **function calling**. Instead of giving the model only text, the application can expose "
            "structured tool definitions. The model can then return structured instructions identifying a function and the "
            "arguments it wants the application to use. The surrounding compute environment executes that function and sends "
            "the result back to the model.\n"
            "\n"
            "This leads to the idea of an **augmented LLM**: an LLM surrounded by capabilities such as retrieval, tools, and "
            "memory. These capabilities form the foundation on which agents are built.\n"
            "\n"
            "### Mental model\n"
            "\n"
            "Think of the progression this way:\n"
            "\n"
            "```text\n"
            "Plain LLM\n"
            "    ↓\n"
            "LLM + Retrieval (RAG)\n"
            "    ↓\n"
            "LLM + Structured Tool Calling\n"
            "    ↓\n"
            "Augmented LLM = Retrieval + Tools + Memory\n"
            "    ↓\n"
            "Agent = Augmented LLM + Self-directed multi-step action/feedback loops\n"
            "```\n"
            "\n"
            '{{image:chatbot-to-augmented-llm}}'
            '\n'
            "\n"
            "The key transition is not simply 'the model has tools.' The key transition is that the model can use those tools "
            "inside an iterative process where each result changes what it decides to do next.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. What makes a system an agent?\n"
            "\n"
            "In the source chapters, an agent is treated as a system in which the LLM dynamically directs its own process and "
            "tool use. The model is not merely answering a prompt once; it is deciding how to complete a task.\n"
            "\n"
            "A **tool** is code outside the LLM that the LLM can choose to call. Examples could include reading a file, running tests, "
            "querying a service, or performing another deterministic action.\n"
            "\n"
            "### The Reason → Act → Observe loop\n"
            "\n"
            "The source connects the agent's action-feedback loop to the ReAct pattern:\n"
            "\n"
            "1. **Reason** — determine the current goal, inspect the current state, and decide the next action.\n"
            "2. **Act** — use something available in the environment, such as a tool, file, user input, or other capability.\n"
            "3. **Observe** — receive the result of the action, add that feedback to the working context, and decide what happens next.\n"
            "\n"
            "Then the cycle repeats until the model decides the task is complete, needs another action, or needs more information "
            "from the user.\n"
            "\n"
            "[[IMAGE_NEEDED: Agent Reason-Act-Observe loop | "
            "A circular diagram with Reason → Act → Observe → Reason, with environment inputs such as tools, files, prompt, and history "
            "feeding the Act stage and tool results feeding Observe | "
            "Learner should notice that the next action depends on observed feedback, which is what makes the process adaptive]]\n"
            "\n"
            "### Worked example: a coding agent writes tests\n"
            "\n"
            "Suppose the user asks an agent to write unit tests for `feature.py`.\n"
            "\n"
            "**Loop 1 — inspect the target**\n"
            "\n"
            "```text\n"
            "Goal: write tests\n"
            "Reason: I need to understand feature.py first.\n"
            "Act: call a file-reading tool.\n"
            "Observe: receive the source code or a useful representation of it.\n"
            "```\n"
            "\n"
            "**Loop 2 — create the tests**\n"
            "\n"
            "```text\n"
            "Reason: I now know the behavior that needs coverage.\n"
            "Act: write the test file using the available file-writing capability.\n"
            "Observe: receive the written test content or confirmation.\n"
            "```\n"
            "\n"
            "**Loop 3 — validate the result**\n"
            "\n"
            "```text\n"
            "Reason: written tests are not enough; I need evidence that they work.\n"
            "Act: run the test suite.\n"
            "Observe: receive passing/failing tests, coverage, or other diagnostics.\n"
            "```\n"
            "\n"
            "If tests fail, the agent can decide to edit the tests or code and run them again. The important idea is that the "
            "agent's behavior is **feedback-driven**.\n"
            "\n"
            "### A critical boundary\n"
            "\n"
            "An LLM with a single tool is not automatically an agent. The distinguishing behavior is the ability to perform "
            "self-directed loops in which tool results are fed back into the model and influence later decisions.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Agents vs agentic workflows\n"
            "\n"
            "This distinction is one of the most important ideas in the two chapters.\n"
            "\n"
            "An **agent** lets the LLM decide which actions to take and which tools to use across one or more loops.\n"
            "\n"
            "An **agentic workflow** can still use LLMs and tools, but the **code determines the path**. The developer specifies "
            "the sequence, branches, and conditions in advance.\n"
            "\n"
            "### Side-by-side comparison\n"
            "\n"
            "| Question | Agent | Agentic workflow |\n"
            "|---|---|---|\n"
            "| Who decides the next step? | Primarily the LLM | Primarily application code |\n"
            "| Can the path change from feedback? | Yes, dynamically | Only through predefined branches |\n"
            "| Tool selection | Chosen by the model from available tools | Chosen by the programmed flow |\n"
            "| Control | More model autonomy | More developer determinism |\n"
            "| Typical strength | Open-ended tasks requiring adaptive planning | Tasks that benefit from predictable logic |\n"
            "\n"
            "### Workflow pattern 1: prompt chaining\n"
            "\n"
            "A prompt-chaining workflow makes several LLM calls in a predetermined sequence, with later prompts using earlier "
            "outputs. For example, a code-translation workflow could detect a language, choose a translation path, translate, and "
            "then validate the translation. The LLM helps with individual steps, but the application owns the path.\n"
            "\n"
            "### Workflow pattern 2: parallelization\n"
            "\n"
            "Several independent LLM calls are made at once and their outputs are combined. This is useful when subtasks do not "
            "depend on each other.\n"
            "\n"
            "### Workflow pattern 3: routing\n"
            "\n"
            "An LLM classifies an input and the application sends that input to one of several specialized routes. A translation "
            "request might go to one path, while a grammar-check request goes to another.\n"
            "\n"
            "### Workflow pattern 4: orchestrator-worker\n"
            "\n"
            "One LLM breaks a task into smaller pieces, worker LLMs process those pieces, and an aggregator combines their outputs.\n"
            "\n"
            "### Workflow pattern 5: evaluator-optimizer\n"
            "\n"
            "One model produces an answer, another evaluates it, and the result is either accepted or returned for refinement.\n"
            "\n"
            "[[IMAGE_NEEDED: Fixed workflow versus autonomous agent | "
            "Two side-by-side diagrams: left shows a predetermined code-controlled chain of LLM calls; right shows an LLM choosing among tools "
            "inside repeated action-feedback loops | "
            "Learner should notice that both may use LLMs and tools, but control of the path is different]]\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. What agents enable\n"
            "\n"
            "Agents are useful when a task requires more than producing text. By combining an LLM with retrieval, tools, memory, "
            "and iterative decision making, an agent can interact with an environment and adapt its next step to what happens.\n"
            "\n"
            "The chapters highlight several common categories:\n"
            "\n"
            "- **Coding agents** that inspect files, edit code, and run tests.\n"
            "- **Research agents** that use search, memory, scratchpads, and sometimes subagents.\n"
            "- **Customer-service agents** that combine knowledge retrieval with actions and escalation.\n"
            "- **Software-specific copilots** that expose application-specific capabilities through tools.\n"
            "\n"
            "The learner should not confuse the user interface with the architecture. A sophisticated agent may still look like "
            "a normal chat box. The difference is what happens behind that interface: the system can choose actions, call tools, "
            "retrieve new information, remember useful context, and potentially coordinate with other agents.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Why MCP was created\n"
            "\n"
            "As agents gained tools, another problem became obvious: every application and model could end up needing its own "
            "custom connector for every tool or data source.\n"
            "\n"
            "If you have `M` model/application environments and `N` integrations, naive custom integration creates roughly:\n"
            "\n"
            "```text\n"
            "M × N connectors\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "3 model environments × 4 tools = 12 connectors\n"
            "```\n"
            "\n"
            "This duplicates work and increases maintenance and debugging cost.\n"
            "\n"
            "MCP introduces a shared protocol between AI applications and integrations. The model side implements an MCP client, "
            "and the integration side implements an MCP server. The integration problem becomes conceptually:\n"
            "\n"
            "```text\n"
            "M + N connectors\n"
            "```\n"
            "\n"
            "In the same example:\n"
            "\n"
            "```text\n"
            "3 model/application connectors + 4 integration connectors = 7\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: M×N integration problem transformed into M+N with MCP | "
            "First panel shows three model applications each connected separately to four tools, producing twelve links; second panel shows "
            "the applications connecting through MCP clients to MCP servers so each side needs only its protocol connection | "
            "Learner should notice how a shared protocol removes repeated pairwise connectors]]\n"
            "\n"
            "### Why the name 'Model Context Protocol' matters\n"
            "\n"
            "The word **context** is central. Context is the information available to the model while it works on a request. "
            "MCP can provide context in several forms: tool names and definitions, prompts, resource identifiers, data, and more.\n"
            "\n"
            "This connects MCP to **context engineering**: deliberately deciding what information and capabilities should be made "
            "available to the model at the right moment so that it can make better decisions.\n"
            "\n"
            "### Inspiration from LSP\n"
            "\n"
            "MCP was inspired by the Language Server Protocol (LSP). LSP standardized how IDEs communicate with language servers "
            "through a common protocol, avoiding a separate implementation for every editor-language combination. MCP applies a "
            "similar architectural idea to AI applications and integrations.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. The problems MCP addresses\n"
            "\n"
            "MCP is not merely about making tool calls possible. The source emphasizes several broader problems.\n"
            "\n"
            "### 6.1 Integration\n"
            "\n"
            "Historically, tools were often tightly coupled to an application's codebase. MCP provides a common interface for "
            "discovering and using integrations so applications do not need a unique connector for every model-tool combination.\n"
            "\n"
            "### 6.2 Distribution\n"
            "\n"
            "When integrations are decoupled from application code, they become easier to share. Teams can distribute tools, "
            "prompts, and resources through code or as running MCP servers that compatible applications can connect to.\n"
            "\n"
            "### 6.3 Two-way communication\n"
            "\n"
            "MCP is bidirectional. The client can request capabilities or actions from the server, and the server can return data "
            "and participate in supported client-side interactions. Bidirectional communication is essential for workflows in "
            "which the two sides need to exchange state and results.\n"
            "\n"
            "### 6.4 MCP is a protocol, not simply an API wrapper\n"
            "\n"
            "The chapters stress that MCP is closer in spirit to LSP than to simply exposing another REST API. It standardizes "
            "how clients and servers exchange capabilities and messages, and it is not tied to one SDK implementation.\n"
            "\n"
            "### MCP vs CLI vs agent skills\n"
            "\n"
            "The source does not claim MCP is always the best tool. It presents a more practical rule: choose the mechanism that "
            "fits the use case.\n"
            "\n"
            "| Option | Strong fit described in the source |\n"
            "|---|---|\n"
            "| CLI | Local developer workflows where a mature, well-documented command-line tool already exists |\n"
            "| Agent skill | Teaching an agent how to perform a specialized task through targeted instructions and progressive disclosure |\n"
            "| MCP | Reusable tool/data/prompt distribution, remote services, authentication-aware integrations, and production agent access |\n"
            "\n"
            "Agent skills can also complement MCP by helping the model load detailed tool information only when needed, reducing "
            "unnecessary context usage.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. MCP architecture: host, client, server, and transport\n"
            "\n"
            "At a high level, MCP follows a client/server architecture.\n"
            "\n"
            "```text\n"
            "User\n"
            "  ↓\n"
            "Host Application + LLM\n"
            "  ↓\n"
            "MCP Client\n"
            "  ↓\n"
            "Transport / JSON-RPC\n"
            "  ↓\n"
            "MCP Server\n"
            "  ↓\n"
            "Tools / Resources / Prompts / External Systems\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: MCP host-client-server architecture | "
            "A diagram showing a host application containing an LLM and MCP client, the client communicating across a transport with an MCP server, "
            "and the server exposing tools, resources, and prompts | "
            "Learner should notice that the MCP client belongs to the host side, while capabilities are exposed by the server side]]\n"
            "\n"
            "### Host application\n"
            "\n"
            "The **host application** is the user-facing application that contains or works with the LLM and hosts MCP client code. "
            "Examples in the source include IDEs, desktop chat applications, agent frameworks, and AI-powered terminals.\n"
            "\n"
            "The host is necessary for using MCP, even though the source distinguishes it from the core protocol components.\n"
            "\n"
            "### MCP client\n"
            "\n"
            "The **MCP client** is the code inside the host application that connects to an MCP server and relays messages between "
            "the host/LLM and that server. The source describes a client instance as maintaining a one-to-one connection with a "
            "single server.\n"
            "\n"
            "The client can also decide which server capabilities become available to the host. One client might expose only tools; "
            "another might expose tools, prompts, and resources.\n"
            "\n"
            "### MCP server\n"
            "\n"
            "The **MCP server** exposes capabilities through a standard interface. It may run locally or remotely, and it is usually "
            "the place where tools execute and where resources and prompts are provided.\n"
            "\n"
            "### MCP transport\n"
            "\n"
            "The **transport** handles the communication channel between client and server. It is responsible for moving messages "
            "and managing the underlying communication mechanism.\n"
            "\n"
            "---\n"
            "\n"
            "## 8. MCP server building blocks: tools, resources, and prompts\n"
            "\n"
            "The server's main capabilities can be organized into three primitives.\n"
            "\n"
            "| Building block | Think of it as | What it provides |\n"
            "|---|---|---|\n"
            "| **Tools** | Actions / verbs | Executable functions the model can choose to call |\n"
            "| **Resources** | Data / nouns | Files, text, schemas, documentation, blobs, and other data |\n"
            "| **Prompts** | Reusable interaction guidance | Server-provided prompts that the host or user can choose to use |\n"
            "\n"
            "### Tools\n"
            "\n"
            "Tools represent actions. Their names and descriptions are made available to the LLM through the client. If the model "
            "chooses a tool, the tool runs where the MCP server is running, and its result returns through the client to the application.\n"
            "\n"
            "### Resources\n"
            "\n"
            "Resources represent data. The source gives examples such as text files, PDFs, database schemas, and documentation. "
            "A resource can be placed directly into model context, used by a tool, or used as part of a caching strategy.\n"
            "\n"
            "### Prompts\n"
            "\n"
            "Prompts are reusable prompt definitions that the host application or user can choose to apply. The important boundary "
            "is that server-provided prompts are not the same thing as a server directly calling the host LLM.\n"
            "\n"
            "### Client-side features: sampling, roots, and elicitation\n"
            "\n"
            "The chapters also describe capabilities that clients can provide to servers:\n"
            "\n"
            "- **Sampling** lets a server request that the host application's model perform an LLM call.\n"
            "- **Roots** let a client identify filesystem locations that are intended to be available to a server.\n"
            "- **Elicitation** lets a server ask the host application to obtain additional input from the user.\n"
            "\n"
            "A security warning is important here: roots should not be treated as a complete security boundary. The source notes "
            "that servers are expected to respect roots, but roots are not a substitute for proper access control.\n"
            "\n"
            "> **Version note from the supplied chapter:** sampling and roots are described as being in the process of deprecation, "
            "with support stated through at least July 2027. Logging is also described as being deprecated on the same support horizon. "
            "Treat these details as version-specific protocol information when studying or implementing MCP.\n"
            "\n"
            "### Server utilities\n"
            "\n"
            "Beyond the three main primitives, the source discusses utilities such as completions, logging, and pagination. "
            "Pagination is especially useful when a server must return large result sets in manageable pieces.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Transports and JSON-RPC messages\n"
            "\n"
            "MCP's communication layer is implemented by transports. The two built-in transport styles emphasized in the source are:\n"
            "\n"
            "### stdio\n"
            "\n"
            "`stdio` is primarily used for **local MCP servers**. The host launches or communicates with a local process and messages "
            "flow through standard input/output.\n"
            "\n"
            "### Streamable HTTP\n"
            "\n"
            "Streamable HTTP is used for **remote MCP servers**. Remote servers can be hosted by a third party or inside an organization's "
            "network and can support authentication and multiple outside connections.\n"
            "\n"
            "### JSON-RPC message types\n"
            "\n"
            "Regardless of transport, MCP messages are represented as JSON-RPC messages. The chapter describes three main message types:\n"
            "\n"
            "1. **Request** — asks the connected side to perform an operation.\n"
            "2. **Response** — carries the result or error for a request.\n"
            "3. **Notification** — a one-way message that does not require a response.\n"
            "\n"
            "[[IMAGE_NEEDED: Local and remote MCP transports | "
            "A split diagram showing a local host and MCP server connected through stdio on one side, and a host connecting to a remote MCP server "
            "through Streamable HTTP on the other; annotate that JSON-RPC messages travel through either transport | "
            "Learner should notice that the protocol message model stays consistent even though the transport changes]]\n"
            "\n"
            "### Transport as a security boundary\n"
            "\n"
            "The source explicitly encourages thinking of the transport as a security boundary. Custom transports are possible when "
            "an application has unusual performance, security, or existing messaging requirements.\n"
            "\n"
            "---\n"
            "\n"
            "## 10. The MCP connection lifecycle and the stateless model\n"
            "\n"
            "The source distinguishes legacy lifecycle behavior from the model introduced in the **2026-07-28 specification**.\n"
            "\n"
            "### Earlier lifecycle\n"
            "\n"
            "Older MCP connections were described in three phases:\n"
            "\n"
            "1. **Initialization** — client and server negotiate protocol version, capabilities, and implementation details.\n"
            "2. **Operation** — requests and responses perform the actual work.\n"
            "3. **Shutdown** — the client closes the protocol connection.\n"
            "\n"
            "### Stateless model described in the source\n"
            "\n"
            "Under the 2026-07-28 specification described by the chapter, the connection model becomes stateless. The separate "
            "initialization phase disappears. Protocol compatibility and capabilities travel with requests, and the server provides "
            "a `server/discover` endpoint that a client can use to inspect compatibility before relying on a capability.\n"
            "\n"
            "For Streamable HTTP, there is no durable connection that must remain open in the older sense; the client can simply stop "
            "sending requests when it is finished.\n"
            "\n"
            "The built-in transports and SDK session managers handle much of this complexity for developers.\n"
            "\n"
            "### Authorization\n"
            "\n"
            "The chapter also notes that authorization can be implemented at the transport layer and describes OAuth 2.1 as the "
            "required authorization approach for transport implementations that include authorization.\n"
            "\n"
            "### Protocol utilities\n"
            "\n"
            "The source discusses cancellation and progress reporting. It also notes that ping belonged to the earlier stateful model "
            "and is no longer part of the modern stateless behavior, although legacy implementations may still support it.\n"
            "\n"
            "---\n"
            "\n"
            "## 11. Practical MCP design lessons\n"
            "\n"
            "Understanding the architecture is not enough. The source gives several design warnings that are especially important "
            "when you build real agent systems.\n"
            "\n"
            "### Warning 1: more tools can make tool choice worse\n"
            "\n"
            "Adding many servers and tools can introduce overlapping names and descriptions. This can reduce tool-choice accuracy, "
            "cause the model to select the wrong tool, hallucinate arguments, loop repeatedly, or cycle between similar tools.\n"
            "\n"
            "The practical lesson is to evaluate tool selection before and after adding capabilities rather than assuming that more "
            "tools always make the agent better.\n"
            "\n"
            "### Warning 2: do not mechanically wrap every REST endpoint as an MCP tool\n"
            "\n"
            "Traditional REST APIs are usually designed as many small, composable endpoints. That can be excellent for human-written "
            "software, but a poor match for an LLM because tool names and descriptions consume context and too many fine-grained tools "
            "make selection harder.\n"
            "\n"
            "A better MCP design is to expose **fewer, task-oriented tools** that represent meaningful actions the agent should perform.\n"
            "\n"
            "### Example: service provider\n"
            "\n"
            "A SaaS provider can expose an MCP server that gives compatible agents access to selected tools, prompts, and resources "
            "while still enforcing authentication, authorization, throttling, and scaling at the remote service boundary.\n"
            "\n"
            "### Example: engineering team\n"
            "\n"
            "A team could connect coding agents to a ticketing-system MCP server. The agents can update tickets as work happens, "
            "reducing the need for developers to manually repeat the same project-tracking updates.\n"
            "\n"
            "### Example: developer environment\n"
            "\n"
            "A developer can combine an AI-powered IDE with carefully selected MCP servers for documentation, infrastructure tools, "
            "APIs, language intelligence, or other capabilities. The important word is **carefully**: tool quality and selection "
            "accuracy matter more than simply maximizing the number of connected servers.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. MCP and other agent protocols\n"
            "\n"
            "MCP focuses on how models and agentic applications gain access to **tools, prompts, and data resources**.\n"
            "\n"
            "The source contrasts this with protocols such as **A2A** and **ACP**, which focus more on **agent-to-agent communication**. "
            "These ideas are complementary rather than mutually exclusive: one protocol can help an agent use tools while another "
            "helps agents communicate with each other.\n"
            "\n"
            "This gives you a useful architectural separation:\n"
            "\n"
            "```text\n"
            "MCP: agent/application ↔ tools, prompts, resources\n"
            "A2A / ACP: agent ↔ agent communication\n"
            "```\n"
            "\n"
            "The broader lesson is that agentic systems may eventually rely on a stack of specialized protocols rather than one "
            "protocol solving every problem.\n"
            "\n"
            "### Developer tooling\n"
            "\n"
            "The chapter also highlights official SDKs and MCP Inspector. MCP Inspector acts as a testing and debugging client that "
            "lets developers inspect server capabilities and manually exercise MCP behavior. This is valuable because an MCP server "
            "should be tested as an actual protocol participant, not only as a set of ordinary functions.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'If an LLM can call one tool, it is an agent.'\n"
            "\n"
            "**Why this is wrong:** tool access alone does not create agency. The important behavior is a self-directed sequence in "
            "which the model decides what to do, acts, observes feedback, and may repeat the loop.\n"
            "\n"
            "### Misconception 2: 'Agentic workflow and agent mean the same thing.'\n"
            "\n"
            "**Why this is wrong:** an agent dynamically selects actions; an agentic workflow can still be fully controlled by code.\n"
            "\n"
            "### Misconception 3: 'MCP replaces APIs.'\n"
            "\n"
            "**Why this is wrong:** the source presents MCP as a protocol for model-facing integrations. A service may still use ordinary "
            "APIs internally or alongside MCP. The warning is specifically against blindly turning every REST endpoint into a separate tool.\n"
            "\n"
            "### Misconception 4: 'More MCP tools always make an agent more capable.'\n"
            "\n"
            "**Why this is wrong:** too many overlapping tools can reduce tool-choice accuracy and waste context.\n"
            "\n"
            "### Misconception 5: 'Roots are a complete filesystem security sandbox.'\n"
            "\n"
            "**Why this is wrong:** the supplied chapter explicitly warns that roots are not a substitute for access control.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| LLM | A language model that processes context and generates language output |\n"
            "| RAG | Retrieval-augmented generation; retrieve relevant external information and add it to model context |\n"
            "| Augmented LLM | An LLM extended with capabilities such as retrieval, tools, and memory |\n"
            "| Agent | An LLM-centered system that dynamically directs actions and tool use across feedback-driven loops |\n"
            "| Tool | External deterministic code the model can choose to call |\n"
            "| ReAct | A Reason → Act → Observe pattern for iterative problem solving |\n"
            "| Action-feedback loop | Repeated cycle where an action result becomes feedback for the next model decision |\n"
            "| Agentic workflow | LLM-based workflow whose path is primarily controlled by code |\n"
            "| MCP | Model Context Protocol; a common protocol for providing tools, prompts, resources, and related context to model-driven applications |\n"
            "| Context engineering | Designing what information and capabilities enter the model's working context |\n"
            "| Host application | User-facing application that hosts the LLM interaction and MCP client code |\n"
            "| MCP client | Host-side connector that communicates with one MCP server instance |\n"
            "| MCP server | Component that exposes capabilities such as tools, resources, and prompts |\n"
            "| Tool primitive | MCP building block representing an action |\n"
            "| Resource primitive | MCP building block representing data |\n"
            "| Prompt primitive | MCP building block representing reusable model prompts |\n"
            "| Transport | Communication mechanism carrying MCP messages between client and server |\n"
            "| stdio | Local transport based on standard input/output |\n"
            "| Streamable HTTP | Transport used for remote MCP server communication |\n"
            "| JSON-RPC | Message format/protocol used for MCP requests, responses, and notifications |\n"
            "| Request | Message asking the connected side to perform an operation |\n"
            "| Response | Reply containing an operation result or error |\n"
            "| Notification | One-way message that does not require a response |\n"
            "| Sampling | Client feature allowing a server to request use of the host's LLM; described as being deprecated in the supplied chapter |\n"
            "| Roots | Client-provided filesystem scope hints; not a complete security boundary |\n"
            "| Elicitation | Server request for additional user input through the host application |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What capability does RAG add that a plain LLM does not have by itself?\n"
            "2. Why does function calling move an LLM closer to becoming an agent?\n"
            "3. What happens in the Reason, Act, and Observe stages?\n"
            "4. Why is a tool-enabled chatbot not automatically an agent?\n"
            "5. Who controls the path in an agent versus an agentic workflow?\n"
            "6. What is the difference between routing and orchestrator-worker workflows?\n"
            "7. What is the M × N integration problem?\n"
            "8. How does MCP reduce M × N to M + N conceptually?\n"
            "9. What are the responsibilities of the host, client, server, and transport?\n"
            "10. How do tools, resources, and prompts differ?\n"
            "11. When would stdio be a better fit than Streamable HTTP?\n"
            "12. Why can exposing too many small tools hurt an agent?\n"
            "13. What changed in the stateless MCP lifecycle described in the source?\n"
            "14. Why should roots not be treated as a security sandbox?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**An agent is not simply an LLM with tools: it is an augmented LLM that can repeatedly decide, act, observe feedback, "
            "and adapt. MCP does not create that agency by itself; it standardizes how the agentic application discovers and uses "
            "external tools, data, and prompts through a client-server protocol.**\n"
        ),

        "estimated_minutes": 120,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "from-llm-to-agent",
                "title": "From a plain LLM to an agent",
                "order": 1,
            },
            {
                "id": "agent-loop",
                "title": "What makes a system an agent?",
                "order": 2,
            },
            {
                "id": "agents-vs-workflows",
                "title": "Agents vs agentic workflows",
                "order": 3,
            },
            {
                "id": "agent-capabilities",
                "title": "What agents enable",
                "order": 4,
            },
            {
                "id": "why-mcp",
                "title": "Why MCP was created",
                "order": 5,
            },
            {
                "id": "mcp-problems",
                "title": "The problems MCP addresses",
                "order": 6,
            },
            {
                "id": "mcp-architecture",
                "title": "MCP architecture: host, client, server, and transport",
                "order": 7,
            },
            {
                "id": "server-primitives",
                "title": "MCP server building blocks",
                "order": 8,
            },
            {
                "id": "transport-messages",
                "title": "Transports and JSON-RPC messages",
                "order": 9,
            },
            {
                "id": "connection-lifecycle",
                "title": "The MCP connection lifecycle and the stateless model",
                "order": 10,
            },
            {
                "id": "practical-design",
                "title": "Practical MCP design lessons",
                "order": 11,
            },
            {
                "id": "mcp-ecosystem",
                "title": "MCP and other agent protocols",
                "order": 12,
            },
        ],
    },

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Classify Agent vs Workflow Designs",

            "lesson_code": "M01.L01",

            "section_id": "agents-vs-workflows",

            "placement": "after_section",

            "description": (
                "Practice identifying who controls the execution path in different "
                "LLM-powered system designs."
            ),

            "instructions": (
                "For each scenario below, label it as Agent, Agentic Workflow, or Neither, "
                "then justify your answer.\n\n"
                "1. A program always calls an LLM to detect a language, then follows a fixed "
                "if/else branch to choose one translator.\n"
                "2. An LLM is given file-reading, file-writing, and test-running tools and "
                "decides which to call repeatedly until the tests pass.\n"
                "3. A chatbot receives a prompt and produces an answer without retrieval, "
                "tools, or iterative actions.\n"
                "4. A router model classifies a request and application code sends it to one "
                "of three specialist prompts.\n"
                "5. For the two agentic cases, write one possible Reason → Act → Observe cycle."
            ),

            "expected_output": (
                "A five-row classification table with justification, plus at least one "
                "complete Reason → Act → Observe example."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-vs-workflow",
                "react-loop",
                "architecture-reasoning",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Design a Small MCP Architecture",

            "lesson_code": "M01.L01",

            "section_id": "server-primitives",

            "placement": "after_section",

            "description": (
                "Apply the MCP architecture to a realistic agent integration and decide "
                "what belongs in the host, client, server, and primitives."
            ),

            "instructions": (
                "Design an MCP integration for an engineering assistant that can read project "
                "documentation, create a deployment ticket, and offer a reusable deployment-review "
                "prompt.\n\n"
                "1. Identify the host application.\n"
                "2. Identify what the MCP client is responsible for.\n"
                "3. Define one Tool, one Resource, and one Prompt.\n"
                "4. Decide whether the first version should use stdio or Streamable HTTP and explain why.\n"
                "5. Draw the message path from the user's request to the server and back.\n"
                "6. Explain one security concern and one tool-choice concern.\n"
                "7. Explain why exposing every underlying REST endpoint as a separate MCP tool would be a poor design."
            ),

            "expected_output": (
                "A short architecture description or diagram containing Host → Client → Transport → "
                "Server, definitions for one tool/resource/prompt, a transport decision, and design justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "mcp-architecture",
                "mcp-primitives",
                "transport-selection",
                "tool-design",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "From LLMs to Agents and MCP — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "from-llm-to-agent",

                "question": "What is the main role of RAG in the evolution from plain LLMs to augmented LLMs?",

                "options": [
                    "It gives the model a deterministic execution engine.",
                    "It retrieves external information and adds it to the model's context.",
                    "It replaces the language model with a vector database.",
                    "It automatically turns every chatbot into an autonomous agent.",
                ],

                "correct": 1,

                "explanation": (
                    "RAG enriches the model's input with retrieved information. It improves "
                    "the information available to the model but does not by itself create agency."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "agent-loop",

                "question": "Which sequence best describes the ReAct-style loop used to explain agent behavior?",

                "options": [
                    "Retrieve → Train → Deploy",
                    "Prompt → Fine-tune → Cache",
                    "Reason → Act → Observe",
                    "Route → Aggregate → Stop",
                ],

                "correct": 2,

                "explanation": (
                    "The agent reasons about the next step, acts through its environment, and "
                    "observes the feedback before deciding what to do next."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "agents-vs-workflows",

                "question": "What is the clearest difference between an agent and an agentic workflow in this lesson?",

                "options": [
                    "Only agents can use language models.",
                    "Only workflows can call tools.",
                    "Agents primarily choose their own next actions, while workflows primarily follow code-defined paths.",
                    "Workflows always use more models than agents.",
                ],

                "correct": 2,

                "explanation": (
                    "Both can use LLMs and tools. The important distinction is who controls the "
                    "execution path: the model or the programmed workflow."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "why-mcp",

                "question": "What integration problem is MCP designed to reduce?",

                "options": [
                    "The need to train M models on N datasets.",
                    "The M × N growth of custom model-to-integration connectors.",
                    "The number of tokens needed to train a transformer.",
                    "The number of users allowed to connect to one application.",
                ],

                "correct": 1,

                "explanation": (
                    "Without a common interface, each model/application may require a custom "
                    "connector to each integration. MCP replaces this pairwise pattern with a common protocol."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "mcp-architecture",

                "question": "Which component is the host-side connector that communicates with an MCP server?",

                "options": [
                    "MCP client",
                    "MCP resource",
                    "MCP prompt",
                    "Vector database",
                ],

                "correct": 0,

                "explanation": (
                    "The MCP client lives on the host side and manages communication with an MCP server."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "server-primitives",

                "question": "Which mapping of MCP server primitives is correct?",

                "options": [
                    "Tools = data, Resources = actions, Prompts = transports",
                    "Tools = actions, Resources = data, Prompts = reusable model prompts",
                    "Tools = connections, Resources = models, Prompts = authentication",
                    "Tools = memory, Resources = routes, Prompts = servers",
                ],

                "correct": 1,

                "explanation": (
                    "The lesson uses the simple mental model: tools are actions, resources are "
                    "data, and prompts are reusable instructions for interacting with the model."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "transport-messages",

                "question": "Which transport pairing matches the source chapters?",

                "options": [
                    "stdio for local servers; Streamable HTTP for remote servers",
                    "Streamable HTTP for local-only servers; stdio for public cloud servers",
                    "WebSocket is the only supported transport",
                    "Transport choice changes MCP messages away from JSON-RPC",
                ],

                "correct": 0,

                "explanation": (
                    "The chapters describe stdio as the standard local transport and Streamable "
                    "HTTP as the remote transport. MCP messages remain JSON-RPC messages across transports."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "practical-design",

                "question": "Why can directly exposing every REST endpoint as a separate MCP tool be a poor design?",

                "options": [
                    "MCP tools cannot call APIs.",
                    "LLMs are unable to process structured tool definitions.",
                    "Too many fine-grained tools consume context and can reduce tool-choice accuracy.",
                    "REST endpoints can only be used with local servers.",
                ],

                "correct": 2,

                "explanation": (
                    "The source warns that large numbers of small, overlapping tools can confuse "
                    "tool selection and increase context usage. Task-oriented tools are often a better fit."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "connection-lifecycle",

                "type": "open",

                "question": (
                    "Explain how the 2026-07-28 stateless MCP model described in the source differs "
                    "from the older Initialization → Operation → Shutdown lifecycle. Include the role "
                    "of server/discover in your answer."
                ),
            },
        ],

        "passing_score": 70,
    },
}
