"""M03.L01 — Building MCP Servers: Tools, Prompts, and Resources.

One supplied source chapter/extract -> one complete learner-facing lesson +
inline Images + inline Exercises + lesson Quiz.

Source alignment: Chapter 5 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Building MCP Servers"

MODULE_DESCRIPTION = (
    "Learn how to design and build MCP servers with Python, choose transports and "
    "server APIs, expose agent-friendly tools, distribute prompts and resources, "
    "handle structured outputs and errors, and test server behavior with MCP Inspector."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building MCP Servers: Tools, Prompts, and Resources",

    "slug": "ai-agents-mcp-m03-l01",

    "description": (
        "Build the server side of MCP. Understand what servers distribute, choose "
        "between MCPServer and the low-level API, design agent-friendly tools, "
        "serve reusable prompts and contextual resources, handle large resources "
        "and errors, and understand the lifecycle of each MCP primitive."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.0,

    "skill_tags": [
        "mcp-server",
        "mcpserver",
        "low-level-mcp",
        "stdio",
        "streamable-http",
        "tool-design",
        "structured-output",
        "prompt-design",
        "mcp-resources",
        "resource-templates",
        "mcp-inspector",
        "agent-stories",
        "error-handling",
        "module-03",
    ],

    "prerequisite_ids": ["M02.L02"],

    "lesson": {
        "title": "Building MCP Servers: Tools, Prompts, and Resources",

        "content": (
            "# Building MCP Servers: Tools, Prompts, and Resources\n"
            "\n"
            "> **Lesson:** M03.L01  \n"
            "> **Module:** Building MCP Servers  \n"
            "> **Source alignment:** Chapter 5 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "> **Scope note:** the supplied source extract ends after the section "
            "on resource lifecycles. The chapter introduction previews additional "
            "server utilities, security, and client-provided capability material, "
            "but those later detailed sections are not present in the supplied file. "
            "This lesson therefore teaches only details actually supported by the "
            "provided source.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the role of an MCP server and why distribution is one of its biggest benefits.\n"
            "- Distinguish tools, resources, and prompts by purpose and intended controller.\n"
            "- Choose between stdio and Streamable HTTP for a server deployment.\n"
            "- Explain why remote MCP servers require serious authorization and transport security.\n"
            "- Compare the high-level `MCPServer` API with the low-level Python server API.\n"
            "- Explain why mechanically converting every REST endpoint into an MCP tool is an antipattern.\n"
            "- Use agent stories to design end-to-end tools around agent intent.\n"
            "- Build tools whose names, descriptions, schemas, namespaces, and outputs are easy for an LLM to use.\n"
            "- Understand structured tool outputs, image/audio outputs, tool annotations, and list-change notifications.\n"
            "- Decide when to raise a normal Python exception versus an `MCPError`.\n"
            "- Design reusable MCP prompts, including parameterized and multiturn prompts.\n"
            "- Explain prefilling and how prompts can refer to tools and resources.\n"
            "- Expose fixed resources and resource templates.\n"
            "- Handle text, binary, and large resources through appropriate patterns.\n"
            "- Explain the discovery/use lifecycle for tools, prompts, and resources.\n"
            "- Use MCP Inspector as an interactive development and testing client.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. What does an MCP server actually provide?\n"
            "\n"
            "On the client side, MCP looked like a way to connect an application to new capabilities. "
            "From the server side, the job is the opposite: **package useful capabilities so that many "
            "different MCP-compatible applications can discover and use them**.\n"
            "\n"
            "The three core primitives remain the same:\n"
            "\n"
            "| Primitive | Intended controller | Main purpose |\n"
            "|---|---|---|\n"
            "| **Tool** | Model | Perform an action |\n"
            "| **Resource** | Application | Provide contextual data |\n"
            "| **Prompt** | Application user | Provide reusable interactive instructions |\n"
            "\n"
            "This controller model is an intended interaction pattern, not an enforcement mechanism. "
            "A client application can choose to expose or use primitives differently. As a server developer, "
            "you therefore design for the normal intended path but cannot completely control the host application's UX.\n"
            "\n"
            "### Distribution is the deeper benefit\n"
            "\n"
            "Before a shared protocol, a tool or data integration was often embedded directly inside one AI application. "
            "If a second application wanted the same integration, its developer would have to repeat the work: study the API, "
            "write authentication logic, create wrappers, define model-facing schemas, and maintain the integration.\n"
            "\n"
            "An MCP server moves that integration into a reusable component:\n"
            "\n"
            "```text\n"
            "Before MCP\n"
            "Application A ── custom integration ── Service\n"
            "Application B ── another integration ── Service\n"
            "Application C ── another integration ── Service\n"
            "\n"
            "With MCP\n"
            "Application A ─┐\n"
            "Application B ─┼── MCP Server ── Service/Data/Logic\n"
            "Application C ─┘\n"
            "```\n"
            "\n"
            "The server author can understand the underlying service deeply and distribute that knowledge once, "
            "while client developers concentrate on their own application behavior.\n"
            "\n"
            '{{image:mcp-server-distribution-layer}}'
            '\n'
            "\n"
            "### Why server design quality matters\n"
            "\n"
            "Easy server development does not automatically produce good servers. The source warns about real failure modes such as:\n"
            "\n"
            "- untrusted servers,\n"
            "- excessive local privileges,\n"
            "- unreliable connections,\n"
            "- huge tool catalogs that consume the context window,\n"
            "- tool-choice confusion.\n"
            "\n"
            "The lesson is that **server quality is partly AI interface design**, not merely ordinary backend API design.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Connecting servers to applications with transports\n"
            "\n"
            "MCP messages use JSON-RPC, but a transport determines how those messages travel between client and server.\n"
            "\n"
            "The supplied chapter focuses on two transports:\n"
            "\n"
            "| Transport | Typical deployment | How it behaves |\n"
            "|---|---|---|\n"
            "| `stdio` | Local server | Client launches server as a long-running subprocess and exchanges messages over stdin/stdout |\n"
            "| Streamable HTTP | Remote server | Client sends one-off HTTP POST requests to an MCP endpoint, with optional SSE streaming for long responses |\n"
            "\n"
            "### stdio\n"
            "\n"
            "stdio is the natural fit for servers distributed as code that users run locally. A README can tell the host application "
            "which command and arguments launch the server. The client starts the process and keeps communicating with it for the "
            "life of that local session.\n"
            "\n"
            "### Streamable HTTP\n"
            "\n"
            "Streamable HTTP is designed for remotely hosted servers. The chapter describes an MCP endpoint such as `/mcp` that handles "
            "POST requests. A short request may return ordinary JSON immediately; a long-running operation may use an ephemeral SSE "
            "response stream to send progress or notifications.\n"
            "\n"
            "A modern remote interaction is therefore better pictured as a sequence of requests than as one permanent socket connection.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP server transport comparison | "
            "Two panels: stdio with a client launching a local server subprocess and reading/writing streams; Streamable HTTP with a client "
            "sending POST requests to a remote /mcp endpoint and optionally receiving an SSE response stream | "
            "Learner should notice the local process lifecycle versus remote request/response lifecycle]]\n"
            "\n"
            "### Remote deployment expands the security surface\n"
            "\n"
            "The source stresses that remotely hosted servers need authorization and security thinking from the beginning. "
            "Threats mentioned include interception, session/token abuse, tool poisoning, and other attacks on data and credentials.\n"
            "\n"
            "The important design mindset is simple: **a remote MCP server is a network service with AI-specific attack paths, "
            "not a trusted helper just because it speaks MCP.**\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Two ways to build Python MCP servers\n"
            "\n"
            "The source presents two server-development levels in the Python SDK.\n"
            "\n"
            "### High-level `MCPServer`\n"
            "\n"
            "`MCPServer` is the preferred approach for most use cases. It provides decorators and type inference so that ordinary "
            "Python functions can become MCP tools, prompts, and resources with little protocol boilerplate.\n"
            "\n"
            "A minimal server can be conceptually this small:\n"
            "\n"
            "```python\n"
            "from mcp.server.mcpserver import MCPServer\n"
            "\n"
            "mcp = MCPServer('example-server')\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    mcp.run()\n"
            "```\n"
            "\n"
            "The high-level API also supports lifecycle management and advanced configuration.\n"
            "\n"
            "### Low-level API\n"
            "\n"
            "The low-level API exposes more of the protocol directly. The developer can implement handlers for operations such as "
            "listing tools and calling tools, construct protocol response objects manually, and control capability behavior more precisely.\n"
            "\n"
            "This flexibility comes with substantial extra code. You may need to define:\n"
            "\n"
            "- initialization metadata,\n"
            "- list handlers,\n"
            "- call handlers,\n"
            "- JSON Schemas,\n"
            "- result objects,\n"
            "- routing among several tools,\n"
            "- lifespan state and cleanup.\n"
            "\n"
            "### Mental model\n"
            "\n"
            "```text\n"
            "MCPServer API\n"
            "Python function + decorator + type hints\n"
            "        ↓\n"
            "SDK infers protocol representation\n"
            "\n"
            "Low-level API\n"
            "Developer writes protocol handlers and result objects directly\n"
            "```\n"
            "\n"
            "The chapter teaches the low-level API to expose the mechanics, but then returns to `MCPServer` because its simplicity is "
            "usually the better tradeoff.\n"
            "\n"
            "### A note on naming\n"
            "\n"
            "The supplied source warns not to confuse the high-level `MCPServer` API with unrelated similarly named frameworks or with FastAPI. "
            "Its historical naming changed over SDK versions, so read code in the context of the SDK version being used.\n"
            "\n"
            "{{exercise:M03.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Why wrapping a REST API endpoint-by-endpoint is often an antipattern\n"
            "\n"
            "Traditional REST APIs and model-facing MCP tools optimize for different consumers.\n"
            "\n"
            "REST APIs often expose small composable endpoints because deterministic application code can reliably chain them. "
            "An LLM, however, has to **choose** each tool based on names, descriptions, schemas, and the current context.\n"
            "\n"
            "Imagine an agent wants to send a direct message to Bob. A granular API wrapper might expose:\n"
            "\n"
            "```text\n"
            "1. find_user_id(name)\n"
            "2. open_direct_message_channel(user_id)\n"
            "3. send_message(channel_id, text)\n"
            "```\n"
            "\n"
            "For an agent, the better tool may be:\n"
            "\n"
            "```text\n"
            "send_direct_message(user_name, text)\n"
            "```\n"
            "\n"
            "The server can still call several private helper functions internally. The key is that the **agent-facing interface reflects "
            "the end-to-end action the agent actually wants to accomplish**.\n"
            "\n"
            "### Why granularity hurts\n"
            "\n"
            "If each tool-selection decision has some probability of error, requiring several selections compounds the chance that the "
            "overall workflow fails. It also creates more model turns, and later turns include earlier input/output tokens, which can "
            "increase cost substantially.\n"
            "\n"
            "The source gives a simple illustration: a 95% tool-choice success rate repeated across five required choices produces an "
            "overall success rate of roughly 77% for the full sequence.\n"
            "\n"
            "### Agent stories\n"
            "\n"
            "The source recommends thinking in **agent stories**, analogous to product user stories.\n"
            "\n"
            "Instead of asking:\n"
            "\n"
            "> What endpoints does the API have?\n"
            "\n"
            "ask:\n"
            "\n"
            "> What meaningful action is the agent trying to complete?\n"
            "\n"
            "This shifts server design from API mirroring to agent usability.\n"
            "\n"
            "[[IMAGE_NEEDED: Granular REST wrapper versus agent-oriented MCP tool | "
            "Left panel shows one user intent requiring three or more small API-shaped MCP tools; right panel shows one end-to-end "
            "agent-oriented tool calling internal helper/API steps behind the server | "
            "Learner should notice that internal composition can remain granular while the model-facing action stays simple]]\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Designing tools that an LLM can use reliably\n"
            "\n"
            "With the high-level API, a Python function becomes a tool when decorated with `@mcp.tool()`.\n"
            "\n"
            "The SDK can infer important protocol metadata from ordinary Python structure:\n"
            "\n"
            "- function name → tool name,\n"
            "- docstring → description,\n"
            "- parameter names/types → input schema,\n"
            "- return annotation → output schema when supported.\n"
            "\n"
            "That convenience makes your Python naming and typing part of the model-facing interface.\n"
            "\n"
            "### Tool design checklist\n"
            "\n"
            "A strong tool should have:\n"
            "\n"
            "- a distinct action-oriented name,\n"
            "- a description clear enough for model selection,\n"
            "- well-defined inputs,\n"
            "- well-defined outputs,\n"
            "- useful type annotations,\n"
            "- an appropriate namespace when several related tools exist,\n"
            "- one coherent end-to-end responsibility.\n"
            "\n"
            "### Namespacing\n"
            "\n"
            "An underscore-separated prefix can provide additional context and reduce ambiguity:\n"
            "\n"
            "```text\n"
            "grader_generate_report_card\n"
            "grader_calculate_gpa\n"
            "```\n"
            "\n"
            "Namespacing becomes especially helpful when client applications combine tools from many servers.\n"
            "\n"
            "### Tool descriptions are part of the model's reasoning surface\n"
            "\n"
            "Descriptions should be detailed enough for the model to understand when the tool applies, but not so verbose that they waste "
            "the context window. The source compares writing a tool description to explaining code to a new engineer: make implicit assumptions "
            "explicit when they affect correct use.\n"
            "\n"
            "### Keep the catalog intentionally small\n"
            "\n"
            "The source warns that tool-choice performance can degrade when many tools are simultaneously active. This means the server "
            "developer should not shift all responsibility to the client. A smaller catalog of well-designed actions is generally easier "
            "for agents and users to work with.\n"
            "\n"
            "### Cache hints and deterministic lists\n"
            "\n"
            "For relatively stable lists, the source describes cache hints such as a TTL. Deterministic ordering also helps downstream "
            "caching because the same logical list is more likely to produce stable prompt content.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Structured, multimodal, and annotated tool outputs\n"
            "\n"
            "A major advantage of the high-level API is that return types can become structured output schemas automatically.\n"
            "\n"
            "The source lists supported structured-return patterns such as:\n"
            "\n"
            "- Pydantic models,\n"
            "- TypedDicts,\n"
            "- dataclasses,\n"
            "- typed classes,\n"
            "- JSON-serializable dictionaries,\n"
            "- primitive/generic types wrapped into a structured result.\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "class ReportCard(BaseModel):\n"
            "    name: str\n"
            "    grades: list[tuple[str, int]]\n"
            "\n"
            "@mcp.tool()\n"
            "async def generate_report_card(name: str, grades: list[tuple[str, int]]) -> ReportCard:\n"
            "    return ReportCard(name=name, grades=grades)\n"
            "```\n"
            "\n"
            "The return annotation gives the SDK enough information to describe and validate the output shape.\n"
            "\n"
            "### Images and audio\n"
            "\n"
            "The high-level server API also provides convenience output types for images and audio. The server can return appropriately "
            "wrapped binary data so the client receives native content blocks without the application developer manually constructing every "
            "wire-level response object.\n"
            "\n"
            "### Tool annotations\n"
            "\n"
            "A tool can include hints about behavior, such as being read-only. These hints give clients more information about the tool, "
            "although they should not be mistaken for security enforcement.\n"
            "\n"
            "### Complete actions can call helper functions internally\n"
            "\n"
            "A tool exposed to the model can call other ordinary Python functions—including functions that are themselves decorated as tools. "
            "The agent does not need to see the internal decomposition. This preserves testability while keeping the model-facing surface simple.\n"
            "\n"
            "[[IMAGE_NEEDED: MCPServer tool inference | "
            "A diagram mapping Python function name, docstring, parameter type hints, and return annotation into MCP tool name, description, "
            "input schema, and output schema | "
            "Learner should notice how normal Python design decisions become part of the protocol-facing tool definition]]\n"
            "\n"
            "{{exercise:M03.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 7. How tools move through the MCP lifecycle\n"
            "\n"
            "Understanding the message flow helps you design better server behavior.\n"
            "\n"
            "A typical tool flow is:\n"
            "\n"
            "```text\n"
            "Client → Server: tools/list\n"
            "Server → Client: tool definitions\n"
            "Client → Model: user request + available tools\n"
            "Model → Client: selected tool + arguments\n"
            "Client → Server: tools/call\n"
            "Server: execute tool + validate output\n"
            "Server → Client: tool result\n"
            "Client → Model: tool result\n"
            "Model: continue reasoning or answer user\n"
            "```\n"
            "\n"
            "The server does not normally decide when the model should call a tool. Its core responsibility is to publish a usable tool "
            "definition and execute the requested operation correctly.\n"
            "\n"
            "### Dynamic tool lists\n"
            "\n"
            "If the available tool catalog changes, the server can announce a list change through the request context. Modern listening "
            "clients can then refresh their view.\n"
            "\n"
            "The source describes context notification helpers for tool, prompt, and resource list changes, as well as updates to specific resources.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP tool lifecycle | "
            "A sequence diagram showing list discovery, model tool selection, tools/call, server execution, tool result returning to the model, "
            "plus an optional list-changed notification path | "
            "Learner should notice that discovery and execution are separate phases]]\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Handling tool errors: can the model recover?\n"
            "\n"
            "The chapter gives a useful decision rule for choosing an error type:\n"
            "\n"
            "> **Could a better-informed model fix the problem?**\n"
            "\n"
            "### Recoverable/model-visible error\n"
            "\n"
            "If the model can correct its request, raise an ordinary Python exception with an informative message.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Requested student: 'Alan Turning'\n"
            "Server knows no such student.\n"
            "```\n"
            "\n"
            "A useful error can tell the model that the name was not found, allowing it to ask the user or retry with a corrected value.\n"
            "\n"
            "### Protocol/unrecoverable error\n"
            "\n"
            "If the request is fundamentally invalid or the model cannot fix the underlying condition with better arguments, the source "
            "recommends a structured MCP protocol error.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Grades have not been published yet.\n"
            "```\n"
            "\n"
            "No spelling correction or alternative argument can make that unavailable state valid.\n"
            "\n"
            "### Error messages have two audiences\n"
            "\n"
            "A good message helps both:\n"
            "\n"
            "- a human developer diagnose the server,\n"
            "- the model decide whether and how to recover.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Serving reusable prompts\n"
            "\n"
            "Prompts let a server distribute reusable interaction instructions to client applications. In the intended MCP interaction model, "
            "prompts are user controlled: the application can show them in a menu, command palette, slash-command interface, or another UI.\n"
            "\n"
            "A prompt function is decorated with `@mcp.prompt()` and can return representations such as text or message objects.\n"
            "\n"
            "### Parameterized prompts\n"
            "\n"
            "Function parameters become values the client can collect and send to the server. The server then injects those values into its template.\n"
            "\n"
            "```python\n"
            "@mcp.prompt()\n"
            "async def greet(username: str) -> str:\n"
            "    return f'Greet the user named {username}.'\n"
            "```\n"
            "\n"
            "MCP does not force a particular templating language. Python f-strings are only one possibility.\n"
            "\n"
            "### Prompt-design principles from the source\n"
            "\n"
            "The chapter summarizes five useful prompting ideas:\n"
            "\n"
            "1. Give direction.\n"
            "2. Specify format when useful.\n"
            "3. Provide examples when they improve behavior.\n"
            "4. Evaluate quality across models and cases.\n"
            "5. Divide labor when one prompt becomes too broad.\n"
            "\n"
            "Examples introduce a tradeoff: they help the model understand the task, but they can also anchor tone, length, and structure more "
            "strongly than intended.\n"
            "\n"
            "### Model-agnostic prompt design\n"
            "\n"
            "Different model families may respond well to different prompt structures. Since MCP servers are intended to work with multiple "
            "models, avoid making your server depend too heavily on one provider-specific trick unless you test it broadly and document the assumption.\n"
            "\n"
            "### System-prompt cost awareness\n"
            "\n"
            "Persistent prompt content is repeatedly sent to a model and therefore has an ongoing token cost. Clear, useful prompts should still be "
            "written with context efficiency in mind.\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Multiturn prompts, prefilling, tools, and resources\n"
            "\n"
            "A prompt does not have to be one text string. It can return a sequence of user and assistant messages, representing the beginning "
            "of a conversation.\n"
            "\n"
            "### Prefilling\n"
            "\n"
            "A server can provide a partial assistant message that establishes a response shape or starting point.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "User message:\n"
            "  Summarize this text into 3 ideas.\n"
            "\n"
            "Assistant prefill:\n"
            "  Here are 3 main ideas:\n"
            "  1.\n"
            "```\n"
            "\n"
            "The model continues from the prefilled assistant content. This can encourage a particular structure more strongly than a plain instruction.\n"
            "\n"
            "### Prompts can guide tool usage\n"
            "\n"
            "A prompt can tell the model to consider a particular tool, or server code can call an ordinary Python function/tool function and use its result "
            "while constructing prompt messages. The server author should understand that the application still ultimately decides how returned prompt messages "
            "are inserted into the model conversation.\n"
            "\n"
            "### Prompts can link resources\n"
            "\n"
            "The source demonstrates including a `ResourceLink` inside prompt content. This allows a reusable prompt to point the client toward contextual "
            "data exposed by the same server.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP prompt lifecycle and composition | "
            "A diagram showing prompts/list discovery, user selecting a prompt, prompts/get with arguments, server returning user/assistant messages, "
            "and optional links to tools/resources | "
            "Learner should notice that prompts are server-distributed but normally user-selected and client-integrated]]\n"
            "\n"
            "### Prompt discovery and use lifecycle\n"
            "\n"
            "```text\n"
            "Client → Server: prompts/list\n"
            "Server → Client: available prompt definitions\n"
            "User selects prompt in application\n"
            "Client → Server: prompts/get(name, arguments)\n"
            "Server → Client: prompt messages\n"
            "Client → Model: integrate prompt according to host UX\n"
            "```\n"
            "\n"
            "If the prompt list changes, the server can notify modern subscribed clients so they refresh it.\n"
            "\n"
            "{{exercise:M03.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 11. Serving resources as read-only context\n"
            "\n"
            "Resources provide data that client applications can use as model context. Examples in the source include:\n"
            "\n"
            "- logs,\n"
            "- database schemas,\n"
            "- images,\n"
            "- PDFs,\n"
            "- JSON/YAML configuration,\n"
            "- documentation and knowledge files.\n"
            "\n"
            "A basic resource is created with `@mcp.resource(uri)`.\n"
            "\n"
            "```python\n"
            "@mcp.resource('file://knowledge.txt')\n"
            "async def knowledge_base() -> str:\n"
            "    ...\n"
            "```\n"
            "\n"
            "The URI is the resource's stable identifier. Descriptions are also valuable because a client can use them when deciding which resource "
            "is relevant to a user's task.\n"
            "\n"
            "### Resources should be lightweight\n"
            "\n"
            "The chapter gives a strong design warning: resource functions should primarily **retrieve data**. They should avoid heavy computation and "
            "side effects. If reading a resource secretly modifies state or launches an action, the server has blurred the boundary between a resource and a tool.\n"
            "\n"
            "A helpful rule is:\n"
            "\n"
            "```text\n"
            "Tool     → action\n"
            "Resource → data\n"
            "```\n"
            "\n"
            "### Content types\n"
            "\n"
            "Text resources can return strings. Binary resources can return bytes. Other serializable structures may be represented as JSON text by the SDK.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. Resource templates and deferred loading\n"
            "\n"
            "A fixed resource has one concrete URI. A **resource template** has variables inside its URI, allowing one server definition to represent many "
            "related resources.\n"
            "\n"
            "Example concept:\n"
            "\n"
            "```python\n"
            "@mcp.resource('file:///{filename}')\n"
            "async def resource_template(filename: str) -> str | bytes:\n"
            "    ...\n"
            "```\n"
            "\n"
            "The URI variable becomes a Python function parameter. The client can select a concrete value when reading the resource.\n"
            "\n"
            "### Deferred loading\n"
            "\n"
            "The server does not need to load every resource's full data just to list resources. The SDK can keep metadata/function representations in a resource "
            "manager and invoke the function only when a client actually reads the resource.\n"
            "\n"
            "This is important for scalability because discovery should be much cheaper than loading every possible resource.\n"
            "\n"
            "### Resource objects\n"
            "\n"
            "The chapter also shows more explicit resource classes such as `FileResource`. These can be returned from decorated functions or directly added to "
            "the server's resource manager when the server needs more control than a simple string/bytes return value provides.\n"
            "\n"
            "### Resource annotations\n"
            "\n"
            "Optional annotations can communicate hints such as audience, priority, and last-modified information. These are metadata for the client, not a replacement "
            "for access control or application policy.\n"
            "\n"
            "[[IMAGE_NEEDED: Fixed resource versus resource template | "
            "A diagram showing one fixed URI mapping to one resource and a templated URI such as file:///{filename} mapping to many concrete resources, "
            "with loading deferred until resources/read | "
            "Learner should notice that templates scale discovery without loading every possible resource upfront]]\n"
            "\n"
            "---\n"
            "\n"
            "## 13. Serving large resources safely and efficiently\n"
            "\n"
            "Large files should not simply be pushed through MCP as one enormous response. The supplied source describes two practical strategies.\n"
            "\n"
            "### Strategy 1: URL indirection\n"
            "\n"
            "The resource can identify or return a URL that the client fetches outside the MCP payload.\n"
            "\n"
            "This is especially useful when the actual object lives in storage designed for large data delivery.\n"
            "\n"
            "For expiring or changing URLs, keep the MCP resource URI stable and return the current fetch URL when the client reads the resource.\n"
            "\n"
            "### Strategy 2: chunking through resource templates\n"
            "\n"
            "A template can expose query-like parameters such as start/count so the client reads only part of the data:\n"
            "\n"
            "```text\n"
            "logs://application.log?start=0&count=100\n"
            "logs://application.log?start=100&count=100\n"
            "```\n"
            "\n"
            "The source uses line-oriented logs as a natural chunking example.\n"
            "\n"
            "### Tell clients about size when possible\n"
            "\n"
            "Providing resource-size metadata allows a client to decide whether loading the full resource is appropriate for its context or UX.\n"
            "\n"
            "### Why this is also context engineering\n"
            "\n"
            "Even if transport limits were not a problem, loading huge resources into a model context can waste tokens and crowd out the information the model actually needs.\n"
            "\n"
            "{{exercise:M03.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## 14. Resource lifecycle and advanced usage patterns\n"
            "\n"
            "The protocol separates resource discovery from resource reading:\n"
            "\n"
            "```text\n"
            "Client → Server: resources/list\n"
            "Server → Client: metadata + URIs\n"
            "\n"
            "Client chooses resource\n"
            "\n"
            "Client → Server: resources/read(uri)\n"
            "Server → Client: content\n"
            "```\n"
            "\n"
            "Resource templates are discovered through their own list operation and instantiated through concrete URI values.\n"
            "\n"
            "### Change notifications and subscriptions\n"
            "\n"
            "The source distinguishes an older resource-specific subscription design from the modern listening model. In the modern flow described, a client can "
            "send one `subscriptions/listen` request describing the kinds of changes it cares about. `MCPServer` handles the subscription mechanics, while server code "
            "announces changes through context notification methods.\n"
            "\n"
            "### Resource use cases beyond 'open this file'\n"
            "\n"
            "The chapter describes richer patterns:\n"
            "\n"
            "- log-analysis context,\n"
            "- up-to-date technical documentation,\n"
            "- entity discovery,\n"
            "- RAG-like retrieval that returns resource URIs,\n"
            "- caching resource references so old context does not have to remain fully expanded.\n"
            "\n"
            "A recurring principle is that **resources are application controlled**. The server makes data discoverable and readable; the client application decides how and when "
            "that data enters the model's context.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP resource discovery-read-subscribe lifecycle | "
            "A sequence diagram showing resources/list, resource selection, resources/read, contextual use by the application, and a modern subscriptions/listen stream receiving "
            "a resource/list or resource update notification | "
            "Learner should notice the separation between metadata discovery, content loading, and later update awareness]]\n"
            "\n"
            "---\n"
            "\n"
            "## 15. Testing during development with MCP Inspector\n"
            "\n"
            "MCP Inspector is presented in the source as an interactive development client for MCP servers. It lets you inspect what the server exposes and manually trigger behavior.\n"
            "\n"
            "This is especially useful because MCP server correctness has several layers:\n"
            "\n"
            "- Does the server start?\n"
            "- Does capability discovery work?\n"
            "- Are tool schemas understandable?\n"
            "- Do tool calls return the expected content and structured output?\n"
            "- Can resources be listed and loaded?\n"
            "- Do prompts appear and render with arguments correctly?\n"
            "- Do notifications appear when expected?\n"
            "\n"
            "The source shows a development command pattern such as:\n"
            "\n"
            "```text\n"
            "uv run mcp dev server.py\n"
            "```\n"
            "\n"
            "and describes options for adding development dependencies or mounting editable local code.\n"
            "\n"
            "### Why interactive protocol testing matters\n"
            "\n"
            "A Python function can work correctly when called directly yet still expose a poor or invalid MCP interface. Testing through an actual MCP client surfaces the protocol-level "
            "representation that real applications will see.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'An MCP server is basically a REST API with renamed endpoints.'\n"
            "\n"
            "**Why this is wrong:** agent-facing tools should often model end-to-end intent instead of mirroring granular API operations.\n"
            "\n"
            "### Misconception 2: 'The more tools my server exposes, the better.'\n"
            "\n"
            "**Why this is wrong:** large tool catalogs consume context and can reduce tool-choice accuracy.\n"
            "\n"
            "### Misconception 3: 'The model executes the Python tool function directly.'\n"
            "\n"
            "**Why this is wrong:** the model selects a tool; the client sends an MCP call to the server; the server executes the function and returns a result.\n"
            "\n"
            "### Misconception 4: 'Structured output is just documentation.'\n"
            "\n"
            "**Why this is wrong:** schemas allow outputs to be validated and consumed predictably by clients.\n"
            "\n"
            "### Misconception 5: 'All tool errors should be MCP protocol errors.'\n"
            "\n"
            "**Why this is wrong:** ordinary model-correctable errors should usually be surfaced in a way the model can learn from and retry.\n"
            "\n"
            "### Misconception 6: 'MCP prompts are automatically system prompts.'\n"
            "\n"
            "**Why this is wrong:** the server distributes prompt content, but the client application decides how to integrate it.\n"
            "\n"
            "### Misconception 7: 'A resource should perform useful actions when it is read.'\n"
            "\n"
            "**Why this is wrong:** resources should remain lightweight, read-oriented data providers; side effects belong in tools.\n"
            "\n"
            "### Misconception 8: 'Listing resources means loading all their content.'\n"
            "\n"
            "**Why this is wrong:** metadata discovery and content reading are separate; resource templates and resource managers can defer loading.\n"
            "\n"
            "### Misconception 9: 'Large files should always be returned directly through MCP.'\n"
            "\n"
            "**Why this is wrong:** URL indirection or chunked resource templates can be much more practical and context-efficient.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| MCP server | Component that distributes tools, resources, prompts, and related capabilities to MCP clients |\n"
            "| Primitive | Core MCP building block: tool, resource, or prompt |\n"
            "| Tool | Model-oriented executable action exposed by the server |\n"
            "| Resource | Application-controlled read-only contextual data identified by a URI |\n"
            "| Prompt | User-oriented reusable prompt template distributed by the server |\n"
            "| stdio | Local transport using a server subprocess's standard input/output |\n"
            "| Streamable HTTP | Remote transport using HTTP POSTs with optional SSE response streaming |\n"
            "| MCPServer | High-level Python server API that infers protocol metadata from decorated functions |\n"
            "| Low-level API | Python API that exposes protocol handlers and response construction more directly |\n"
            "| Agent story | Description of an end-to-end action from the agent's perspective, used to guide tool design |\n"
            "| Namespace | Prefix that groups and differentiates related tools |\n"
            "| Input schema | Structured description of a tool's accepted arguments |\n"
            "| Output schema | Structured description used to validate predictable tool output |\n"
            "| Tool annotation | Hint to clients about tool behavior, such as read-only intent |\n"
            "| Model-visible error | Recoverable tool error described so the model can correct its next action |\n"
            "| MCPError | Protocol-level error used for malformed/unrecoverable MCP conditions in the chapter's examples |\n"
            "| Multiturn prompt | Prompt represented as a sequence of user/assistant messages |\n"
            "| Prefill | Partial assistant message supplied to shape the beginning of model output |\n"
            "| Resource URI | Unique identifier used to address a resource |\n"
            "| Resource template | Parameterized URI pattern that can identify many related resources |\n"
            "| Deferred loading | Keeping resource metadata available while loading actual content only when requested |\n"
            "| URL indirection | Returning or identifying an external URL instead of transporting a large object directly through MCP |\n"
            "| Chunking | Serving manageable slices of large data through template parameters |\n"
            "| MCP Inspector | Interactive MCP client/tool for inspecting and testing server behavior during development |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What problem does an MCP server solve beyond merely exposing functions?\n"
            "2. Who is the intended controller of a tool, resource, and prompt?\n"
            "3. When is stdio a better fit than Streamable HTTP?\n"
            "4. Why is a remote MCP server a security-sensitive network service?\n"
            "5. What does `MCPServer` automate that the low-level API requires you to implement explicitly?\n"
            "6. When might the low-level API still be useful?\n"
            "7. Why is endpoint-by-endpoint REST-to-MCP generation often a poor agent interface?\n"
            "8. What is an agent story?\n"
            "9. What makes a tool easy for an LLM to choose correctly?\n"
            "10. Why can namespacing improve tool choice?\n"
            "11. How can Python return annotations become structured MCP outputs?\n"
            "12. Why might a tool return an image or audio object instead of text?\n"
            "13. What is the difference between a recoverable Python exception and an MCP protocol error in the source's decision rule?\n"
            "14. How are MCP prompt arguments filled?\n"
            "15. What is a multiturn prompt?\n"
            "16. What does prefilling do?\n"
            "17. Why should resource functions avoid side effects?\n"
            "18. What is the difference between a fixed resource and a resource template?\n"
            "19. Why is deferred resource loading useful?\n"
            "20. What two strategies does the source provide for very large resources?\n"
            "21. How do `resources/list` and `resources/read` differ?\n"
            "22. Why should you test the protocol interface with MCP Inspector rather than only unit-test Python functions directly?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**A good MCP server is an agent-oriented product interface. Its job is not to expose everything your backend can do; it is to distribute a small, clear set of actions, "
            "context sources, and reusable instructions that client applications and models can discover, understand, and use reliably.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "server-role", "title": "What an MCP server provides", "order": 1},
            {"id": "transports", "title": "Server transports", "order": 2},
            {"id": "python-apis", "title": "Two Python server APIs", "order": 3},
            {"id": "rest-antipattern", "title": "REST-to-MCP antipattern and agent stories", "order": 4},
            {"id": "tool-design", "title": "Designing tools for LLMs", "order": 5},
            {"id": "tool-outputs", "title": "Structured and multimodal tool outputs", "order": 6},
            {"id": "tool-lifecycle", "title": "Tool lifecycle", "order": 7},
            {"id": "tool-errors", "title": "Handling tool errors", "order": 8},
            {"id": "prompts", "title": "Serving reusable prompts", "order": 9},
            {"id": "multiturn-prompts", "title": "Multiturn prompts and prefilling", "order": 10},
            {"id": "resources", "title": "Serving resources", "order": 11},
            {"id": "resource-templates", "title": "Resource templates and deferred loading", "order": 12},
            {"id": "large-resources", "title": "Serving large resources", "order": 13},
            {"id": "resource-lifecycle", "title": "Resource lifecycle and advanced uses", "order": 14},
            {"id": "testing", "title": "Testing with MCP Inspector", "order": 15},
        ],
    },

    "exercises": [
        {
            "id": "M03.L01.EX01",
            "title": "Choose the Right Server API and Transport",
            "lesson_code": "M03.L01",
            "section_id": "python-apis",
            "placement": "after_section",
            "description": (
                "Practice choosing between MCPServer and the low-level API, and between "
                "stdio and Streamable HTTP."
            ),
            "instructions": (
                "For each scenario, choose both a server API and transport, then justify your choices.\n\n"
                "1. A local calculator server used by one developer in an IDE.\n"
                "2. A hosted company service that exposes authenticated project tools to many users.\n"
                "3. A research prototype that needs custom handling of tools/list responses per client.\n"
                "4. A normal production server exposing a few typed tools, prompts, and resources.\n"
                "5. For the remote scenario, list two security responsibilities the server developer must consider."
            ),
            "expected_output": (
                "A four-row comparison table with API choice, transport choice, justification, "
                "and security notes for the remote case."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["server-architecture", "transport-selection", "mcpserver", "low-level-api"],
        },

        {
            "id": "M03.L01.EX02",
            "title": "Redesign a Granular API as Agent-Friendly MCP Tools",
            "lesson_code": "M03.L01",
            "section_id": "tool-outputs",
            "placement": "after_section",
            "description": (
                "Practice transforming backend operations into a smaller set of end-to-end "
                "agent-facing tools."
            ),
            "instructions": (
                "A ticketing API exposes these endpoints: search_user, create_ticket, add_comment, "
                "assign_ticket, fetch_project, and change_status.\n\n"
                "The agent story is: 'The agent wants to create a bug ticket for Bob, assign it to him, "
                "and mark it ready for triage.'\n\n"
                "1. Design one or two MCP tools that support this intent.\n"
                "2. Give each tool a clear name and namespace.\n"
                "3. Write a concise but useful description.\n"
                "4. Define its inputs and a structured output shape.\n"
                "5. Identify which original API operations should remain private server helpers.\n"
                "6. Explain why your design is easier for a model than exposing all six operations directly."
            ),
            "expected_output": (
                "One or two agent-oriented tool definitions with names, descriptions, input/output "
                "schemas, helper mapping, and design justification."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["tool-design", "agent-stories", "structured-output", "namespacing"],
        },

        {
            "id": "M03.L01.EX03",
            "title": "Build a Reusable MCP Prompt Design",
            "lesson_code": "M03.L01",
            "section_id": "multiturn-prompts",
            "placement": "after_section",
            "description": (
                "Design a parameterized prompt that can be distributed through an MCP server "
                "without assuming one particular model provider."
            ),
            "instructions": (
                "Create a code-review prompt for an MCP server.\n\n"
                "1. Define arguments such as language, code, and review_focus.\n"
                "2. Give clear task direction.\n"
                "3. Specify a useful output structure.\n"
                "4. Decide whether to include an example and explain the anchoring tradeoff.\n"
                "5. Decide whether a multiturn prompt or assistant prefill would improve the UX.\n"
                "6. Explain how a client user would discover and invoke the prompt.\n"
                "7. Identify one model-specific prompting trick you would avoid making mandatory."
            ),
            "expected_output": (
                "A complete prompt design plus a short explanation of arguments, format, "
                "prefilling/example choices, and MCP discovery/use flow."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["mcp-prompts", "prompt-engineering", "multiturn-prompts", "model-agnostic-design"],
        },

        {
            "id": "M03.L01.EX04",
            "title": "Design Resources for a Large Log Archive",
            "lesson_code": "M03.L01",
            "section_id": "large-resources",
            "placement": "after_section",
            "description": (
                "Use resource templates, chunking, and resource metadata to expose large data "
                "without flooding the MCP transport or model context."
            ),
            "instructions": (
                "Your server provides access to 5 GB of application logs split across daily files.\n\n"
                "1. Design a resource URI or resource template for the logs.\n"
                "2. Add parameters that let clients request a manageable slice.\n"
                "3. Explain whether the resource function should perform analysis or only return data.\n"
                "4. Explain when URL indirection would be better than direct resource content.\n"
                "5. State which metadata would help clients decide whether to load the data.\n"
                "6. Describe the resources/list → resources/read flow.\n"
                "7. Explain how the server would announce an updated resource to a modern listening client."
            ),
            "expected_output": (
                "A resource-template design with URI, parameters, loading strategy, metadata, "
                "lifecycle flow, and update strategy."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["mcp-resources", "resource-templates", "chunking", "context-engineering"],
        },
    ],

    "quiz": {
        "id": "M03.L01.QZ01",
        "title": "Building MCP Servers — Knowledge Check",
        "lesson_code": "M03.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M03.L01.Q01",
                "section_id": "server-role",
                "question": "Which mapping of MCP primitives to intended controllers matches the supplied chapter?",
                "options": [
                    "Tool → model, Resource → application, Prompt → application user",
                    "Tool → user, Resource → model, Prompt → server only",
                    "Tool → application, Resource → user, Prompt → model",
                    "All primitives are controlled only by the server",
                ],
                "correct": 0,
                "explanation": (
                    "The source describes tools as model controlled, resources as application "
                    "controlled, and prompts as user controlled in the intended interaction model."
                ),
            },

            {
                "id": "M03.L01.Q02",
                "section_id": "transports",
                "question": "Which transport is primarily designed for a remotely hosted MCP server?",
                "options": [
                    "stdio",
                    "Streamable HTTP",
                    "SMTP",
                    "FTP",
                ],
                "correct": 1,
                "explanation": (
                    "Streamable HTTP is the remote-oriented transport in the supplied chapter; "
                    "stdio is typically used for local subprocess servers."
                ),
            },

            {
                "id": "M03.L01.Q03",
                "section_id": "python-apis",
                "question": "Why does the chapter generally prefer MCPServer over the low-level API?",
                "options": [
                    "The low-level API cannot serve tools.",
                    "MCPServer infers much of the protocol representation and reduces boilerplate for most use cases.",
                    "MCPServer works only with HTTP.",
                    "The low-level API cannot use JSON-RPC.",
                ],
                "correct": 1,
                "explanation": (
                    "The high-level API keeps most of the power while automating listing, schemas, "
                    "decorator registration, and result construction."
                ),
            },

            {
                "id": "M03.L01.Q04",
                "section_id": "rest-antipattern",
                "question": "Why is a one-to-one REST-endpoint-to-MCP-tool mapping often undesirable?",
                "options": [
                    "MCP tools cannot call REST APIs.",
                    "Agents usually benefit from end-to-end actions rather than many granular tool choices.",
                    "REST APIs cannot use authentication.",
                    "MCP requires exactly one tool per server.",
                ],
                "correct": 1,
                "explanation": (
                    "Several small choices can compound selection errors, token usage, and model round trips. "
                    "The server can compose those operations internally behind an end-to-end tool."
                ),
            },

            {
                "id": "M03.L01.Q05",
                "section_id": "tool-design",
                "question": "Which characteristic most improves an LLM's ability to choose an MCP tool?",
                "options": [
                    "A vague name and undocumented inputs",
                    "A distinct action-oriented name, clear description, and well-defined schema",
                    "Returning only raw bytes",
                    "Having as many similar tools as possible",
                ],
                "correct": 1,
                "explanation": (
                    "The model selects tools based on the definitions placed in its context, so names, "
                    "descriptions, and schemas are part of the reasoning interface."
                ),
            },

            {
                "id": "M03.L01.Q06",
                "section_id": "tool-outputs",
                "question": "How can MCPServer infer a structured tool output schema?",
                "options": [
                    "Only from a handwritten XML file",
                    "From supported Python return type annotations such as Pydantic models",
                    "Only from the tool's name",
                    "It cannot infer structured outputs",
                ],
                "correct": 1,
                "explanation": (
                    "The high-level API uses supported return annotations to infer and validate structured outputs."
                ),
            },

            {
                "id": "M03.L01.Q07",
                "section_id": "tool-errors",
                "question": "According to the chapter's decision rule, when is a normal Python exception often appropriate?",
                "options": [
                    "When the model could potentially correct the request using the error information",
                    "Only when the server process must terminate",
                    "Whenever a protocol capability does not exist",
                    "Never; all errors must be MCPError",
                ],
                "correct": 0,
                "explanation": (
                    "Recoverable/model-correctable tool errors should provide useful information that the "
                    "model can use to retry or ask for clarification."
                ),
            },

            {
                "id": "M03.L01.Q08",
                "section_id": "prompts",
                "question": "How are arguments normally inserted into a server-provided MCP prompt?",
                "options": [
                    "The client always performs string interpolation itself.",
                    "The server's prompt function receives arguments and constructs the returned prompt.",
                    "Arguments can only be environment variables.",
                    "MCP prompts cannot accept parameters.",
                ],
                "correct": 1,
                "explanation": (
                    "Clients collect/provide prompt arguments, while the server function decides how to "
                    "inject those values into the prompt representation."
                ),
            },

            {
                "id": "M03.L01.Q09",
                "section_id": "multiturn-prompts",
                "question": "What is prefilling in the context of the chapter's MCP prompt examples?",
                "options": [
                    "Loading every resource before the first user message",
                    "Returning a partial assistant message that the model continues",
                    "Caching tool schemas on the server",
                    "Starting the MCP server before the client",
                ],
                "correct": 1,
                "explanation": (
                    "A partial assistant turn can establish the beginning and format of the response, "
                    "encouraging the model to continue from that structure."
                ),
            },

            {
                "id": "M03.L01.Q10",
                "section_id": "resources",
                "question": "Which behavior best matches the chapter's design guidance for MCP resources?",
                "options": [
                    "Perform side-effecting actions whenever a resource is read",
                    "Keep resource functions lightweight and focused on returning data",
                    "Use resources only for plain text",
                    "Load every resource during resources/list",
                ],
                "correct": 1,
                "explanation": (
                    "Resources are intended as contextual data. The source explicitly warns against "
                    "heavy computation and side effects in resource functions."
                ),
            },

            {
                "id": "M03.L01.Q11",
                "section_id": "large-resources",
                "question": "Which pair of techniques does the source present for serving very large resources?",
                "options": [
                    "Fine-tuning and embeddings",
                    "URL indirection and chunking with resource templates",
                    "Tool annotations and OAuth",
                    "stdio and model sampling",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter recommends external URL indirection or protocol-native chunking through "
                    "resource templates rather than sending an enormous resource in one response."
                ),
            },

            {
                "id": "M03.L01.Q12",
                "section_id": "testing",
                "type": "open",
                "question": (
                    "Design an MCP server for a project-management system. Explain your transport choice, "
                    "high-level versus low-level API choice, two agent-oriented tools, one reusable prompt, "
                    "one resource/resource template, error strategy, and how you would test the server in MCP Inspector."
                ),
            },
        ],

        "passing_score": 70,
    },
}
