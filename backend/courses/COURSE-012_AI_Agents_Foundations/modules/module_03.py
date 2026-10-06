"""M01.L03 — Actions with Model Context Protocol for AI Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 3, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how the Model Context Protocol (MCP) standardizes agent access to "
    "tools and external services, how MCP clients and servers communicate, "
    "how local and remote transports differ, how to inspect and consume MCP "
    "servers, and how to turn internal tools into reusable agent services."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Actions with Model Context Protocol for AI Agents",

    "slug": "ai-agents-m01-l03",

    "description": (
        "Understand MCP as the standardized integration layer for AI agents, "
        "build and inspect MCP servers, connect them to agents over local and "
        "remote transports, and design reusable, safer agent capabilities."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "mcp",
        "model-context-protocol",
        "agent-tools",
        "json-rpc",
        "fastmcp",
        "stdio",
        "sse",
        "mcp-inspector",
        "openai-agents-sdk",
        "tool-security",
        "agent-integration",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Actions with Model Context Protocol for AI Agents",

        "content": (
            "# Actions with Model Context Protocol for AI Agents\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L03  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 3. "
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
            "- Explain the integration problems MCP is intended to solve.\n"
            "- Describe MCP's client-server-service architecture.\n"
            "- Distinguish MCP tools, resources, and prompts.\n"
            "- Explain how JSON-RPC 2.0 standardizes MCP communication.\n"
            "- Compare local STDIO and remote HTTP/SSE deployment patterns as presented in the chapter.\n"
            "- Explain how MCP can support multiple functional layers of an agent.\n"
            "- Build a simple MCP server with `FastMCP`.\n"
            "- Explain why tool signatures, docstrings, and return types matter.\n"
            "- Use the MCP Inspector to inspect and test a server.\n"
            "- Connect an OpenAI Agents SDK agent to an MCP server.\n"
            "- Explain when MCP is useful and when an in-process function may be simpler.\n"
            "- Describe the major safety risks introduced by autonomous tool access.\n"
            "- Convert internal agent tools into a reusable MCP server.\n"
            "- Explain how shared server state changes when many agents connect to one server.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why MCP exists\n"
            "\n"
            "In Chapter 2, we gave agents tools directly inside their own code. That works well "
            "for small systems, but the approach becomes difficult to maintain when many agents "
            "need access to many external systems.\n"
            "\n"
            "Imagine one research agent that must connect to:\n"
            "\n"
            "- a filesystem,\n"
            "- a database,\n"
            "- a web-search API,\n"
            "- a calendar,\n"
            "- GitHub,\n"
            "- and another agent.\n"
            "\n"
            "Without a shared protocol, each integration may require its own schema, request "
            "format, authentication logic, error handling, and result parser.\n"
            "\n"
            "The Model Context Protocol (MCP) is designed to standardize that integration boundary.\n"
            "\n"
            "The source describes MCP as an open standard created by Anthropic and based on "
            "JSON-RPC 2.0. Its purpose is to let AI systems connect to external capabilities "
            "consistently, securely, and efficiently.\n"
            "\n"
            "A useful analogy from the chapter is **USB-C for AI systems**: instead of building "
            "a unique connector for every service, clients and servers agree on one protocol.\n"
            "\n"
            "[[IMAGE_NEEDED: Before MCP versus with MCP | "
            "Left: one agent connected to filesystem, database, web API, and SaaS service through "
            "four different custom connectors. Right: the agent connects through MCP to reusable "
            "servers that wrap those services | "
            "Learner should notice that MCP standardizes the integration boundary rather than "
            "eliminating the underlying services]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. The standardization problems MCP addresses\n"
            "\n"
            "The chapter identifies several recurring problems that existed before MCP-style "
            "standardization became common.\n"
            "\n"
            "### Fragmented tool integration\n"
            "\n"
            "Different model providers and agent frameworks may represent tools differently. "
            "A developer can end up rewriting schemas, parameters, response envelopes, and parsing "
            "logic for the same underlying capability.\n"
            "\n"
            "### Inconsistent data access\n"
            "\n"
            "Filesystems, databases, web APIs, and cloud applications traditionally require "
            "different custom interfaces. Those integrations are difficult to reuse across agents.\n"
            "\n"
            "### Ad hoc multi-agent communication\n"
            "\n"
            "If one agent needs to expose a capability to another, custom plumbing is often "
            "required unless both sides agree on a protocol.\n"
            "\n"
            "### Uneven security and control\n"
            "\n"
            "When every integration is built differently, it becomes harder to apply consistent "
            "access rules, auditing, and monitoring.\n"
            "\n"
            "MCP does not remove every production concern. The chapter explicitly notes that "
            "authentication, authorization, versioning, server availability, and error handling "
            "still matter. What MCP removes is much of the repeated provider-specific tool wiring.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. MCP architecture: client, server, and service\n"
            "\n"
            "The chapter presents MCP using three practical components:\n"
            "\n"
            "1. **MCP client**\n"
            "2. **MCP server**\n"
            "3. **Underlying service**\n"
            "\n"
            "### MCP client\n"
            "\n"
            "The client is the application that connects to an MCP server. An AI agent is one "
            "kind of MCP client, but desktop assistants, IDEs, and other LLM applications can also "
            "act as clients.\n"
            "\n"
            "The client discovers capabilities and invokes them through the protocol.\n"
            "\n"
            "### MCP server\n"
            "\n"
            "The server exposes capabilities to clients and handles MCP requests and responses.\n"
            "\n"
            "### Service\n"
            "\n"
            "The chapter uses the word **service** as a convenient term for the real system behind "
            "the MCP server, such as:\n"
            "\n"
            "- a database,\n"
            "- a filesystem,\n"
            "- a web API,\n"
            "- a SaaS platform,\n"
            "- or another agent.\n"
            "\n"
            "This gives us a clean abstraction:\n"
            "\n"
            "```text\n"
            "Agent / LLM app\n"
            "      |\n"
            "      v\n"
            "   MCP client\n"
            "      |\n"
            "      v\n"
            "   MCP server\n"
            "      |\n"
            "      v\n"
            "Database / API / Filesystem / Agent\n"
            "```\n"
            "\n"
            "The agent should not need to know how the underlying service is implemented. It only "
            "needs to understand the interface exposed by the server.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. MCP capabilities: tools, resources, and prompts\n"
            "\n"
            "The chapter describes three capability primitives that an MCP server can expose.\n"
            "\n"
            "### Tools\n"
            "\n"
            "**Tools** are actions the model or agent can invoke.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- create an issue,\n"
            "- run a database query,\n"
            "- send a message,\n"
            "- list files,\n"
            "- retrieve a URL.\n"
            "\n"
            "Tools are generally **model-controlled**: the model decides whether and when to use them.\n"
            "\n"
            "### Resources\n"
            "\n"
            "**Resources** represent external data or objects such as files, configuration, or "
            "database-accessible information.\n"
            "\n"
            "### Prompts\n"
            "\n"
            "**Prompts** are reusable templates supplied by a server for common interactions or workflows.\n\n"
            "\n"
            "The chapter makes an important distinction about control:\n"
            "\n"
            "- tools are typically chosen by the model,\n"
            "- resources and prompts are more often surfaced or selected by the user/application.\n"
            "\n"
            "The book focuses mostly on tools because they are the capability most directly used "
            "for agent actions in its examples.\n"
            "\n"
            "| MCP primitive | Main purpose | Typical controller |\n"
            "|---|---|---|\n"
            "| Tool | Perform an action | Model/agent |\n"
            "| Resource | Provide data/object access | User or application |\n"
            "| Prompt | Provide a reusable interaction template | User or application |\n"
            "\n"
            "---\n"
            "\n"

            "## 5. JSON-RPC 2.0 as the communication foundation\n"
            "\n"
            "MCP communication is built on JSON-RPC 2.0 in the chapter's description.\n"
            "\n"
            "The engineering benefit is consistency. Whether the underlying server is written "
            "in Python, TypeScript, Go, or another language, requests and responses follow a "
            "shared message protocol.\n"
            "\n"
            "This is what makes MCP useful as a language-independent integration boundary.\n"
            "\n"
            "A Python agent can consume a server implemented in another language without needing "
            "a language-specific bridge, as long as both sides speak MCP.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. MCP deployment patterns\n"
            "\n"
            "The chapter presents local, remote, and mixed deployment setups.\n"
            "\n"
            "### Local server\n"
            "\n"
            "A server can run on the same machine as the client, often as a subprocess.\n"
            "\n"
            "Advantages described in the chapter include:\n"
            "\n"
            "- low latency,\n"
            "- no network hop,\n"
            "- simple development setup,\n"
            "- useful for local or sensitive operations.\n"
            "\n"
            "### Remote server\n"
            "\n"
            "A server can run as a network service and be shared by multiple clients or agents.\n"
            "\n"
            "This is useful for:\n"
            "\n"
            "- shared services,\n"
            "- distributed architectures,\n"
            "- cloud deployment,\n"
            "- multiclient access,\n"
            "- remote APIs or agent services.\n"
            "\n"
            "### Mixed deployment\n"
            "\n"
            "A real agent may connect to several servers at once. Some may be local and some remote.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Agent\n"
            "  +--> local filesystem MCP server\n"
            "  +--> local Git MCP server\n"
            "  +--> remote GitHub MCP server\n"
            "  +--> remote Slack MCP server\n"
            "```\n"
            "\n"
            "The chapter carefully notes that each individual server is local or remote; the "
            "overall agent setup is what becomes mixed.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. STDIO and SSE transports in the chapter\n"
            "\n"
            "The source focuses on two MCP transport patterns: STDIO and SSE.\n"
            "\n"
            "### STDIO\n"
            "\n"
            "With STDIO, the client launches the server as a subprocess on the same host and "
            "communicates through standard input and output pipes.\n"
            "\n"
            "The chapter positions STDIO as a strong fit for:\n"
            "\n"
            "- local development,\n"
            "- helper processes,\n"
            "- command-line experiments,\n"
            "- simple one-client process-to-process integration.\n"
            "\n"
            "### SSE\n"
            "\n"
            "In the chapter's remote-server examples, SSE is used over HTTP. The server can remain "
            "running independently, and multiple clients can connect through a URL.\n"
            "\n"
            "The chapter positions this pattern for:\n"
            "\n"
            "- remote or cloud deployment,\n"
            "- shared servers,\n"
            "- network-addressable tools,\n"
            "- multiclient access.\n"
            "\n"
            "| Property | STDIO | SSE in the chapter |\n"
            "|---|---|---|\n"
            "| Typical location | Same host | Local or remote HTTP service |\n"
            "| Client connection | Process pipes | URL/network connection |\n"
            "| Server lifecycle | Often launched by client | Often runs independently |\n"
            "| Sharing | Usually one parent client | Can support multiple clients |\n"
            "| Good fit | Local tools and development | Shared or remote services |\n"
            "\n"
            "[[IMAGE_NEEDED: STDIO versus remote SSE connection | "
            "Left: Agent launches MCP server subprocess and communicates through stdin/stdout. "
            "Right: Agent connects over HTTP to a separately running MCP server | "
            "Learner should notice the difference in process ownership, networking, and sharing]]\n"
            "\n"
            "{{exercise:M01.L03.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. MCP can support several agent layers\n"
            "\n"
            "It is easy to think of MCP as only a way to add action tools. The chapter expands "
            "that view by mapping MCP-hosted capabilities to the functional layers introduced earlier.\n"
            "\n"
            "### Tools and actions\n"
            "\n"
            "Examples include GitHub, Slack, and filesystem operations.\n"
            "\n"
            "### Reasoning and planning\n"
            "\n"
            "A server may expose specialized planning or structured-thinking capabilities.\n"
            "\n"
            "### Knowledge and memory\n"
            "\n"
            "A server may expose databases, vector stores, cloud documents, or persistent memory.\n"
            "\n"
            "### Evaluation and feedback\n"
            "\n"
            "A server may expose scoring, judging, benchmarking, or human-approval routing.\n\n"
            "\n"
            "The architectural lesson is that MCP is a **connection pattern**, not merely a category "
            "of action tool.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Building a simple MCP server with FastMCP\n"
            "\n"
            "The chapter begins with a simple research-source tool and wraps it in an MCP server.\n"
            "\n"
            "```python\n"
            "from mcp.server.fastmcp import FastMCP\n"
            "\n"
            "mcp = FastMCP(\"Research Tools\")\n"
            "\n"
            "@mcp.tool()\n"
            "def get_research_sources() -> list[str]:\n"
            "    \"\"\"Provides a list of research sources.\"\"\"\n"
            "    return [\n"
            "        \"Wikipedia\",\n"
            "        \"Google\",\n"
            "        \"YouTube\",\n"
            "    ]\n"
            "```\n"
            "\n"
            "The key architectural change from Chapter 2 is the decorator:\n"
            "\n"
            "```python\n"
            "@mcp.tool()\n"
            "```\n"
            "\n"
            "The function becomes a capability exposed by the MCP server rather than a function "
            "registered directly inside one agent.\n"
            "\n"
            "### Why the function signature matters\n"
            "\n"
            "The tool signature becomes the parameter schema the agent sees.\n"
            "\n"
            "### Why the docstring matters\n"
            "\n"
            "The chapter emphasizes that the docstring becomes part of the description the model "
            "uses when deciding whether to call the tool.\n"
            "\n"
            "That means a poor docstring is not merely poor documentation; it can cause poor tool selection.\n"
            "\n"
            "### Why return types matter\n"
            "\n"
            "Return annotations help describe what kind of result the client should expect.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "Function name     -> tool identity\n"
            "Function signature-> input schema\n"
            "Docstring         -> decision guidance\n"
            "Return type       -> expected result shape\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Testing MCP tools through an LLM client\n"
            "\n"
            "The chapter uses Claude Desktop as a teaching environment for connecting to and "
            "executing MCP tools.\n"
            "\n"
            "The flow is:\n"
            "\n"
            "1. Build an MCP server.\n"
            "2. Install/configure it in the desktop client.\n"
            "3. Restart or reload the client if needed.\n"
            "4. Confirm the server is available.\n"
            "5. Invoke the exposed tool.\n"
            "\n"
            "One important behavior highlighted by the chapter is explicit tool approval in the "
            "desktop environment. This demonstrates a useful security pattern: the user sees and "
            "approves an external action before it executes.\n"
            "\n"
            "The broader lesson is that MCP tools should be tested in isolation before being "
            "trusted inside a more autonomous agent loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Using the MCP Inspector\n"
            "\n"
            "The MCP Inspector is presented as the first debugging tool to use when an MCP server "
            "does not behave as expected.\n"
            "\n"
            "The inspector helps you examine:\n"
            "\n"
            "- the live list of tools,\n"
            "- tool descriptions,\n"
            "- input parameters,\n"
            "- return types,\n"
            "- direct tool execution,\n"
            "- raw protocol traffic,\n"
            "- initialization problems.\n"
            "\n"
            "The chapter shows a command pattern like:\n"
            "\n"
            "```bash\n"
            "mcp dev /absolute/path/to/01_claude_mcp_server.py\n"
            "```\n"
            "\n"
            "The use of an absolute path is emphasized because the inspector must be able to "
            "locate the server file reliably.\n"
            "\n"
            "### Why inspect before integrating?\n"
            "\n"
            "Suppose an agent refuses to call a tool you know exists. The problem might be:\n"
            "\n"
            "- the server did not initialize,\n"
            "- the tool schema is wrong,\n"
            "- the docstring is unclear,\n"
            "- the parameters do not match your expectation,\n"
            "- the function returns an unexpected shape.\n"
            "\n"
            "The inspector lets you separate **server problems** from **agent reasoning problems**.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP Inspector workflow | "
            "A small debugging flow: MCP server -> Inspector -> list tools -> inspect schema -> run "
            "tool manually -> inspect raw response, followed by Agent integration only after success | "
            "Learner should notice that server behavior should be verified independently before blaming the agent]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. MCP with assistants versus agents\n"
            "\n"
            "The chapter makes a useful architectural distinction: permission prompts do not by "
            "themselves define whether something is an assistant or an agent.\n"
            "\n"
            "The stronger distinction is the execution loop.\n"
            "\n"
            "### Assistant-like interaction\n"
            "\n"
            "```text\n"
            "User request -> choose action -> perform action -> return result -> stop\n"
            "```\n"
            "\n"
            "### Agent loop\n"
            "\n"
            "```text\n"
            "Goal -> choose tool -> observe result -> decide next step -> call another tool -> ...\n"
            "```\n"
            "\n"
            "This matters because a tool mistake in a one-step assistant may produce one bad result. "
            "A tool mistake inside an autonomous loop can be amplified through several later steps.\n"
            "\n"
            "That is why MCP tool access becomes a security and reliability concern once agents "
            "operate with meaningful autonomy.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. MCP security: autonomy raises the stakes\n"
            "\n"
            "The chapter strongly warns that an agent may misuse any capability you give it.\n"
            "\n"
            "Several risk categories are highlighted.\n"
            "\n"
            "### Destructive actions\n"
            "\n"
            "Write, delete, version-control, database, and cloud-resource tools can change or "
            "destroy state.\n"
            "\n"
            "### Data exfiltration\n"
            "\n"
            "If an agent can both read sensitive information and send information elsewhere, "
            "an attacker may try to redirect that data.\n"
            "\n"
            "### Privacy violations\n"
            "\n"
            "A tool may run using powerful user credentials and expose more information than the "
            "user realizes is being shared with the wider agent system.\n"
            "\n"
            "### Cost runaways\n"
            "\n"
            "A looping agent can repeatedly call expensive APIs or models unless budgets and rate "
            "limits are enforced.\n"
            "\n"
            "### Prompt injection through tool output\n"
            "\n"
            "External content returned from websites, files, or messages can contain malicious "
            "instructions that enter the model context.\n"
            "\n"
            "The chapter recommends a defense-in-depth posture including:\n"
            "\n"
            "- tool allowlisting,\n"
            "- sandboxing,\n"
            "- output validation,\n"
            "- rate limiting,\n"
            "- budget caps,\n"
            "- human approval for high-stakes actions.\n"
            "\n"
            "A crucial design principle is:\n"
            "\n"
            "> Treat every powerful tool as a capability the agent may eventually use incorrectly.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Connecting an agent to a local MCP server over STDIO\n"
            "\n"
            "The chapter shows how an OpenAI Agents SDK agent can launch and consume a local MCP "
            "server as a subprocess.\n"
            "\n"
            "A simplified version looks like this:\n"
            "\n"
            "```python\n"
            "import asyncio\n"
            "from pathlib import Path\n"
            "\n"
            "from agents import Agent, Runner\n"
            "from agents.mcp import MCPServerStdio, MCPServerStdioParams\n"
            "\n"
            "SCRIPT = Path(__file__).with_name(\n"
            "    \"01_claude_mcp_server.py\"\n"
            ").resolve()\n"
            "\n"
            "async def main():\n"
            "    async with MCPServerStdio(\n"
            "        name=\"Research Tools\",\n"
            "        params=MCPServerStdioParams(\n"
            "            command=\"mcp\",\n"
            "            args=[\"run\", str(SCRIPT)],\n"
            "        ),\n"
            "    ) as research_server:\n"
            "        agent = Agent(\n"
            "            name=\"Assistant\",\n"
            "            instructions=\"Use the research tools to perform research.\",\n"
            "            mcp_servers=[research_server],\n"
            "        )\n"
            "\n"
            "        result = await Runner.run(\n"
            "            agent,\n"
            "            \"Get the available research sources\",\n"
            "        )\n"
            "\n"
            "        print(result.final_output)\n"
            "\n"
            "asyncio.run(main())\n"
            "```\n"
            "\n"
            "### What happens here?\n"
            "\n"
            "1. The path to the server script is resolved.\n"
            "2. The agent application launches the server process.\n"
            "3. The client connection is opened through STDIO.\n"
            "4. The agent receives the server through `mcp_servers=[...]`.\n"
            "5. The agent discovers the server's tools.\n"
            "6. The runner processes the request.\n"
            "7. Exiting the context manager shuts down the subprocess.\n"
            "\n"
            "This gives the application control over the complete server lifecycle.\n"
            "\n"
            "The chapter also emphasizes language independence: the agent and the server do not "
            "need to be implemented in the same programming language.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Connecting an agent to an independently running server\n"
            "\n"
            "The same conceptual server can be run separately and reached over a network transport.\n"
            "\n"
            "The chapter shows an SSE-based example similar to:\n"
            "\n"
            "```python\n"
            "from agents.mcp import MCPServerSse\n"
            "\n"
            "async with MCPServerSse(\n"
            "    name=\"SSE Python Server\",\n"
            "    params={\n"
            "        \"url\": \"http://localhost:8000/sse\",\n"
            "    },\n"
            ") as research_server:\n"
            "    agent = Agent(\n"
            "        name=\"Assistant\",\n"
            "        instructions=\"Use the research tools to perform research.\",\n"
            "        mcp_servers=[research_server],\n"
            "    )\n"
            "```\n"
            "\n"
            "The important architectural difference is not the agent instructions. The difference "
            "is how the client reaches the server:\n"
            "\n"
            "- STDIO: launch a process using a command and arguments.\n"
            "- remote-style connection in the chapter: connect to a URL.\n"
            "\n"
            "This is what allows the same logical capability to move from local development to "
            "a shared service without redesigning the agent's role.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Consuming existing MCP servers\n"
            "\n"
            "A major benefit of MCP is that you do not have to build every server yourself.\n"
            "\n"
            "The chapter lists server examples for capabilities such as:\n"
            "\n"
            "- filesystem access,\n"
            "- sequential thinking,\n"
            "- Google Drive,\n"
            "- Google Calendar,\n"
            "- Todoist,\n"
            "- Notion,\n"
            "- Slack,\n"
            "- Brave Search,\n"
            "- GitHub,\n"
            "- Google Maps,\n"
            "- web fetching.\n"
            "\n"
            "The architectural lesson matters more than any individual server name: if a capability "
            "already exists as a compatible server, the agent can consume it through the shared protocol "
            "instead of rebuilding a custom integration.\n"
            "\n"
            "### Example: filesystem server\n"
            "\n"
            "The chapter shows an agent launching a filesystem MCP server with `npx` and granting "
            "access to a selected directory.\n"
            "\n"
            "```python\n"
            "async with MCPServerStdio(\n"
            "    name=\"Filesystem Server, via npx\",\n"
            "    params={\n"
            "        \"command\": \"npx\",\n"
            "        \"args\": [\n"
            "            \"-y\",\n"
            "            \"@modelcontextprotocol/server-filesystem\",\n"
            "            current_dir,\n"
            "        ],\n"
            "    },\n"
            ") as server:\n"
            "    agent = Agent(\n"
            "        name=\"Filesystem Agent\",\n"
            "        instructions=\"Use the filesystem tools to help the user.\",\n"
            "        mcp_servers=[server],\n"
            "    )\n"
            "```\n"
            "\n"
            "This example demonstrates both the convenience and the risk. The server may allow the "
            "agent to inspect or modify files in the exposed directory. Therefore, the directory "
            "should be isolated carefully.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. When MCP is worth the extra layer\n"
            "\n"
            "The chapter gives an important engineering trade-off: MCP adds abstraction, but it "
            "also adds another process or network connection, another protocol layer, and another "
            "potential failure mode.\n"
            "\n"
            "A useful rule of thumb from the source is:\n"
            "\n"
            "### Prefer MCP when\n"
            "\n"
            "- the capability is genuinely external,\n"
            "- another team owns the implementation,\n"
            "- the tool is a separate deployment unit,\n"
            "- multiple agents need to share it,\n"
            "- language/runtime independence is valuable,\n"
            "- isolation is beneficial.\n"
            "\n"
            "### Prefer an in-process function when\n"
            "\n"
            "- the logic belongs only to this agent,\n"
            "- it already runs inside the same process,\n"
            "- protocol abstraction gives little reuse benefit.\n"
            "\n"
            "This avoids turning every tiny helper function into a distributed service.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Converting internal tools into an MCP server\n"
            "\n"
            "The chapter demonstrates the architectural shift using a small journaling agent.\n"
            "\n"
            "Initially, the agent owns two tools directly:\n"
            "\n"
            "- `record_event(entry)`\n"
            "- `load_journal()`\n"
            "\n"
            "The tools share an in-memory list with the same Python process.\n"
            "\n"
            "The MCP version moves the tools into a separate server:\n"
            "\n"
            "```python\n"
            "from mcp.server.fastmcp import FastMCP\n"
            "\n"
            "mcp = FastMCP(\"Time Travel Tracker\")\n"
            "\n"
            "_journal = []\n"
            "\n"
            "@mcp.tool()\n"
            "def record_event(entry: str) -> dict:\n"
            "    \"\"\"Add a new travel event to the journal.\"\"\"\n"
            "    _journal.append(entry)\n"
            "    return {\n"
            "        \"status\": \"recorded\",\n"
            "        \"entry\": entry,\n"
            "    }\n"
            "\n"
            "@mcp.tool()\n"
            "def load_journal() -> dict:\n"
            "    \"\"\"Load the current travel journal entries.\"\"\"\n"
            "    return {\n"
            "        \"status\": \"loaded\",\n"
            "        \"journal\": \"\\n\".join(_journal),\n"
            "    }\n"
            "\n"
            "if __name__ == \"__main__\":\n"
            "    mcp.run(transport=\"sse\")\n"
            "```\n"
            "\n"
            "### Why this is more than copy-paste\n"
            "\n"
            "Before conversion, the agent and tools share implementation details and process state.\n"
            "\n"
            "After conversion, the agent only sees:\n"
            "\n"
            "- tool name,\n"
            "- description,\n"
            "- parameter schema,\n"
            "- return structure.\n"
            "\n"
            "The server can later change its internal storage from a Python list to Redis, Postgres, "
            "or a remote API without requiring the agent to understand the implementation.\n"
            "\n"
            "[[IMAGE_NEEDED: Internal tools versus MCP-separated tools | "
            "Left: Agent and record_event/load_journal functions inside one process sharing direct "
            "state. Right: Agent connects through MCP to a standalone Time Travel Tracker server "
            "that privately owns the journal implementation | "
            "Learner should notice that the interface remains visible while implementation details become isolated]]\n"
            "\n"
            "{{exercise:M01.L03.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Shared state changes the architecture\n"
            "\n"
            "The chapter uses an in-memory journal for teaching, but it highlights an important "
            "difference between local subprocess execution and a shared remote server.\n"
            "\n"
            "If each local agent launches its own server process, each process can have its own "
            "separate in-memory state.\n"
            "\n"
            "If several agents connect to one long-running server, they may all share the same "
            "module-level list.\n"
            "\n"
            "That can produce surprising behavior such as duplicate or mixed journal entries.\n"
            "\n"
            "This teaches a broader systems lesson:\n"
            "\n"
            "> Moving a capability behind a shared server changes state ownership, isolation, and concurrency assumptions.\n"
            "\n"
            "A production design may therefore need:\n"
            "\n"
            "- user/session identifiers,\n"
            "- tenant isolation,\n"
            "- transactional storage,\n"
            "- locking or concurrency control,\n"
            "- explicit persistence rules.\n"
            "\n"
            "The simple list is intentionally educational, not a production storage design.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Putting MCP into the complete agent architecture\n"
            "\n"
            "You can now read an MCP-enabled agent system like this:\n"
            "\n"
            "```text\n"
            "User goal\n"
            "   |\n"
            "   v\n"
            "Agent instructions + LLM\n"
            "   |\n"
            "   v\n"
            "MCP client connection\n"
            "   |\n"
            "   +--> discover tools\n"
            "   +--> inspect schemas/descriptions\n"
            "   +--> call selected capability\n"
            "   |\n"
            "   v\n"
            "MCP server\n"
            "   |\n"
            "   v\n"
            "External service / data / agent\n"
            "   |\n"
            "   v\n"
            "Structured result\n"
            "   |\n"
            "   v\n"
            "Agent evaluates and continues\n"
            "```\n"
            "\n"
            "The important design questions are now:\n"
            "\n"
            "1. Does this capability belong in-process or behind MCP?\n"
            "2. Should the server be local or remote?\n"
            "3. What capabilities should the server expose?\n"
            "4. Are descriptions and schemas precise enough for safe model selection?\n"
            "5. What permissions does the server have?\n"
            "6. What can happen if the agent misuses the tool?\n"
            "7. What state is shared across clients?\n"
            "8. How will you inspect, trace, validate, and limit execution?\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: MCP removes the need to understand the underlying service\n"
            "\n"
            "> MCP standardizes the interface, but production concerns still exist.\n"
            "\n"
            "Authentication, authorization, failures, server uptime, versioning, and service-specific "
            "behavior still need engineering attention.\n"
            "\n"
            "### Misconception 2: MCP is only for action tools\n"
            "\n"
            "> MCP can expose tools, resources, and prompts, and MCP-hosted capabilities can support "
            "reasoning, memory, knowledge, and evaluation layers as well.\n"
            "\n"
            "### Misconception 3: If a tool works in an assistant, it is automatically safe for an agent\n"
            "\n"
            "> Autonomous loops amplify mistakes.\n"
            "\n"
            "A destructive or misleading tool result can influence many later actions.\n"
            "\n"
            "### Misconception 4: Every internal function should become an MCP server\n"
            "\n"
            "> MCP adds indirection, latency, deployment work, and failure modes.\n"
            "\n"
            "Use it where reuse, isolation, external ownership, or distribution justify the cost.\n"
            "\n"
            "### Misconception 5: Moving state behind a server does not change behavior\n"
            "\n"
            "> Shared servers can turn per-process state into shared multi-client state.\n"
            "\n"
            "State isolation must be designed explicitly.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| MCP | Model Context Protocol, a standard interface for AI systems and external capabilities |\n"
            "| MCP client | Application that connects to an MCP server and consumes its capabilities |\n"
            "| MCP server | Process/service exposing tools, resources, or prompts through MCP |\n"
            "| Service | Chapter term for the underlying API, database, filesystem, SaaS app, or other capability behind a server |\n"
            "| JSON-RPC 2.0 | Structured request-response protocol used as MCP's communication basis in the chapter |\n"
            "| Tool | Model-invokable external action |\n"
            "| Resource | External data or object exposed through MCP |\n"
            "| Prompt | Reusable server-provided interaction template |\n"
            "| FastMCP | Python helper used in the chapter to build MCP servers |\n"
            "| STDIO | Local subprocess transport using standard input/output pipes |\n"
            "| SSE | Server-sent-events HTTP transport used for remote examples in the chapter |\n"
            "| MCP Inspector | Tool for inspecting schemas, capabilities, initialization, and live tool execution |\n"
            "| Tool allowlist | Explicit set of capabilities an agent is permitted to access |\n"
            "| Sandboxing | Isolating risky tool execution from broader system access |\n"
            "| Shared state | Data accessible by multiple clients connected to the same long-running server |\n"
            "| Separation of concerns | Keeping agent logic separate from external tool implementation |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What integration problems does MCP attempt to standardize?\n"
            "2. What are the roles of MCP client, server, and underlying service?\n"
            "3. How do tools, resources, and prompts differ?\n"
            "4. Why is JSON-RPC important to MCP's portability?\n"
            "5. When is STDIO a natural fit?\n"
            "6. When is a remote server connection a better fit?\n"
            "7. How can MCP support knowledge or evaluation, not only actions?\n"
            "8. What information does `@mcp.tool()` expose to the model?\n"
            "9. Why are tool docstrings important?\n"
            "10. What should you inspect before wiring a server into an agent?\n"
            "11. Why can autonomous MCP tool use be riskier than one-shot assistant tool use?\n"
            "12. Name four defense-in-depth controls from this lesson.\n"
            "13. Why might an in-process function be better than MCP for a private helper?\n"
            "14. What architectural benefit appears when tools move into a standalone MCP server?\n"
            "15. Why can module-level in-memory state become dangerous in a shared server?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**MCP is valuable because it separates an agent from the implementation details of "
            "external capabilities. The agent sees a stable interface; the server owns the tool "
            "implementation. That reuse and isolation are powerful, but once autonomous agents "
            "can call those capabilities, security, state isolation, validation, and observability "
            "become part of the architecture—not optional extras.**\n"
        ),

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-mcp", "title": "Why MCP exists", "order": 1},
            {"id": "standardization-problem", "title": "The standardization problems MCP addresses", "order": 2},
            {"id": "architecture", "title": "MCP architecture: client, server, and service", "order": 3},
            {"id": "mcp-primitives", "title": "MCP capabilities: tools, resources, and prompts", "order": 4},
            {"id": "json-rpc", "title": "JSON-RPC 2.0 as the communication foundation", "order": 5},
            {"id": "deployment-patterns", "title": "MCP deployment patterns", "order": 6},
            {"id": "transports", "title": "STDIO and SSE transports in the chapter", "order": 7},
            {"id": "mcp-agent-layers", "title": "MCP can support several agent layers", "order": 8},
            {"id": "first-server", "title": "Building a simple MCP server with FastMCP", "order": 9},
            {"id": "desktop-testing", "title": "Testing MCP tools through an LLM client", "order": 10},
            {"id": "inspector", "title": "Using the MCP Inspector", "order": 11},
            {"id": "assistant-vs-agent", "title": "MCP with assistants versus agents", "order": 12},
            {"id": "mcp-security", "title": "MCP security: autonomy raises the stakes", "order": 13},
            {"id": "agent-stdio", "title": "Connecting an agent to a local MCP server over STDIO", "order": 14},
            {"id": "agent-sse", "title": "Connecting an agent to an independently running server", "order": 15},
            {"id": "standard-servers", "title": "Consuming existing MCP servers", "order": 16},
            {"id": "when-to-use-mcp", "title": "When MCP is worth the extra layer", "order": 17},
            {"id": "convert-tools", "title": "Converting internal tools into an MCP server", "order": 18},
            {"id": "shared-state", "title": "Shared state changes the architecture", "order": 19},
            {"id": "complete-model", "title": "Putting MCP into the complete agent architecture", "order": 20},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Build and Inspect Your First MCP Server",

            "lesson_code": "M01.L03",

            "section_id": "transports",

            "placement": "after_section",

            "description": (
                "Build a single-tool MCP server and inspect its live schema and "
                "behavior before connecting it to an agent."
            ),

            "instructions": (
                "1. Create a FastMCP server named `Research Tools`.\n"
                "2. Add a `get_research_sources()` tool that returns three strings.\n"
                "3. Give the function a clear return type and docstring.\n"
                "4. Run or inspect the server using the MCP tooling described in this lesson.\n"
                "5. Verify the tool name, description, input schema, and return value in the Inspector.\n"
                "6. Execute the tool manually from the Inspector.\n"
                "7. Write one sentence explaining why the docstring matters to an agent.\n"
                "8. State whether you would initially deploy this tiny server over STDIO or as a "
                "separately running network service, and justify the choice using the chapter."
            ),

            "expected_output": (
                "A small FastMCP server, evidence or notes from manual inspection, "
                "and a short explanation of the tool schema and deployment choice."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "fastmcp",
                "mcp-tool-schema",
                "mcp-inspector",
                "stdio",
                "transport-selection",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Convert Internal Agent Tools into a Reusable MCP Service",

            "lesson_code": "M01.L03",

            "section_id": "convert-tools",

            "placement": "after_section",

            "description": (
                "Practice the architectural shift from direct in-process tools "
                "to an isolated, reusable MCP server."
            ),

            "instructions": (
                "Start with two internal functions: `record_event(entry)` and `load_journal()`.\n"
                "1. Implement them first as ordinary agent tools using a shared in-memory list.\n"
                "2. Move both functions into a separate FastMCP server using `@mcp.tool()`.\n"
                "3. Update the agent so it registers the MCP server rather than the individual functions.\n"
                "4. Sketch both deployment options from the chapter: local STDIO and separately running SSE.\n"
                "5. Explain what implementation details the agent no longer needs to know after the conversion.\n"
                "6. Describe one reuse benefit of the MCP version.\n"
                "7. Describe one new failure mode introduced by moving behind a server.\n"
                "8. Explain what happens to the in-memory `_journal` if several agents connect to one long-running server.\n"
                "9. Propose one production-safe storage or isolation improvement.\n"
                "10. Add one security restriction you would apply before exposing the server to an autonomous agent."
            ),

            "expected_output": (
                "A before-and-after architecture, server code or pseudocode, agent-side "
                "connection code, and a short analysis of reuse, failures, shared state, "
                "and security."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tool-to-mcp-conversion",
                "separation-of-concerns",
                "agent-mcp-integration",
                "shared-state",
                "security-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "Actions with Model Context Protocol for AI Agents — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",

                "section_id": "standardization-problem",

                "question": "What is one major problem MCP is designed to reduce?",

                "options": [
                    "The need for any external service",
                    "Repeated custom integration logic across tools and model providers",
                    "The use of structured data",
                    "The need for model instructions",
                ],

                "correct": 1,

                "explanation": (
                    "MCP standardizes the integration boundary so developers do not "
                    "need to rebuild the same tool plumbing for every client or provider."
                ),
            },

            {
                "id": "M01.L03.Q02",

                "section_id": "architecture",

                "question": "Which component exposes capabilities through MCP?",

                "options": [
                    "Only the underlying database",
                    "The MCP server",
                    "The tokenizer",
                    "The model's context window",
                ],

                "correct": 1,

                "explanation": (
                    "The MCP server exposes tools, resources, or prompts to MCP clients."
                ),
            },

            {
                "id": "M01.L03.Q03",

                "section_id": "mcp-primitives",

                "question": "Which MCP primitive is primarily an action the model can invoke?",

                "options": [
                    "Resource",
                    "Prompt",
                    "Tool",
                    "Context window",
                ],

                "correct": 2,

                "explanation": (
                    "Tools are actionable capabilities. Resources provide data, while prompts "
                    "provide reusable interaction templates."
                ),
            },

            {
                "id": "M01.L03.Q04",

                "section_id": "transports",

                "question": "Which pattern best matches STDIO in this chapter?",

                "options": [
                    "A client launches a local server subprocess and communicates through process pipes",
                    "A browser connects to a public website",
                    "A model reads its own weights",
                    "Two servers communicate through a database",
                ],

                "correct": 0,

                "explanation": (
                    "STDIO is presented as a local subprocess transport using standard input/output pipes."
                ),
            },

            {
                "id": "M01.L03.Q05",

                "section_id": "first-server",

                "question": "Why is an MCP tool's docstring important?",

                "options": [
                    "It changes the Python interpreter version",
                    "It helps the model understand what the tool does and when to call it",
                    "It encrypts tool traffic",
                    "It removes the need for a return type",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter explains that the tool description is derived from the function "
                    "documentation and is used by the model when selecting a tool."
                ),
            },

            {
                "id": "M01.L03.Q06",

                "section_id": "inspector",

                "question": "What is a strong reason to use the MCP Inspector before agent integration?",

                "options": [
                    "To train the LLM",
                    "To confirm schemas, descriptions, initialization, and tool results independently",
                    "To increase temperature",
                    "To replace the MCP server",
                ],

                "correct": 1,

                "explanation": (
                    "The Inspector separates server-level problems from agent decision-making problems."
                ),
            },

            {
                "id": "M01.L03.Q07",

                "section_id": "mcp-security",

                "question": "Why is prompt injection through tool output dangerous?",

                "options": [
                    "Tool output never enters model context",
                    "External content can contain malicious instructions that influence later agent decisions",
                    "It only changes token pricing",
                    "It prevents the server from starting",
                ],

                "correct": 1,

                "explanation": (
                    "External pages, files, or messages can carry instructions into the model's "
                    "context and redirect an autonomous workflow."
                ),
            },

            {
                "id": "M01.L03.Q08",

                "section_id": "agent-stdio",

                "question": (
                    "What does the async context manager around a local MCPServerStdio connection "
                    "help manage in the chapter's example?"
                ),

                "options": [
                    "Model training epochs",
                    "The MCP server subprocess lifecycle",
                    "The user's password",
                    "Database indexing",
                ],

                "correct": 1,

                "explanation": (
                    "The server remains available while the context is open and is shut down "
                    "when the block exits."
                ),
            },

            {
                "id": "M01.L03.Q09",

                "section_id": "when-to-use-mcp",

                "question": "When is an in-process function often preferable to MCP?",

                "options": [
                    "When a tool must be shared across several languages",
                    "When a capability is an internal helper used only by one agent process",
                    "When another team owns the tool",
                    "When the tool must be remotely accessible",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter warns that MCP adds a protocol and service layer, so a private "
                    "internal helper may be simpler as a normal function."
                ),
            },

            {
                "id": "M01.L03.Q10",

                "section_id": "convert-tools",

                "question": (
                    "What is the key architectural benefit of moving agent tools behind an MCP server?"
                ),

                "options": [
                    "The agent can directly mutate the server's private variables",
                    "The tool interface is separated from its implementation and can be reused",
                    "The model no longer needs instructions",
                    "All server failures disappear",
                ],

                "correct": 1,

                "explanation": (
                    "The agent interacts through a stable interface while implementation details "
                    "remain private to the server."
                ),
            },

            {
                "id": "M01.L03.Q11",

                "section_id": "shared-state",

                "question": (
                    "Why can a module-level in-memory list behave differently when an MCP server "
                    "is shared by several agents?"
                ),

                "options": [
                    "Python automatically creates a separate list for every client",
                    "All connected agents may interact with the same server process and therefore the same list",
                    "MCP converts the list into a database",
                    "STDIO encrypts the list",
                ],

                "correct": 1,

                "explanation": (
                    "A long-running shared server owns one process-level state unless the developer "
                    "adds explicit client/session isolation."
                ),
            },

            {
                "id": "M01.L03.Q12",

                "section_id": "complete-model",

                "type": "open",

                "question": (
                    "Design an MCP-enabled research agent. Describe one local server, one remote "
                    "server, the capabilities each exposes, how the agent discovers and uses them, "
                    "one shared-state concern, and at least three security controls you would apply."
                ),
            },
        ],

        "passing_score": 70,
    },
}
