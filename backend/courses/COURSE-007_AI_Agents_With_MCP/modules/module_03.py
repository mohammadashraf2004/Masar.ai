"""M02.L02 — Advanced MCP Clients and Production Best Practices.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 4 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L02"

MODULE_ORDER = 2

MODULE_TITLE = "Building MCP Clients"

MODULE_DESCRIPTION = (
    "Extend a basic MCP client into a production-minded client that supports "
    "advanced capabilities, authorization, multiple models and servers, registry "
    "discovery, context engineering, resilient connections, and safer user flows."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Advanced MCP Clients and Production Best Practices",

    "slug": "ai-agents-mcp-m02-l02",

    "description": (
        "A practical advanced lesson on MCP client engineering: callback-based "
        "client capabilities, MRTR, sampling, roots, elicitations, OAuth 2.1, "
        "multi-model adapters, MCP Registry discovery, multi-server sessions, "
        "tool-context optimization, resilient reconnection, and security/UX best practices."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.0,

    "skill_tags": [
        "mcp-client",
        "advanced-mcp",
        "mrtr",
        "sampling",
        "roots",
        "elicitation",
        "oauth",
        "multi-model",
        "mcp-registry",
        "multi-server",
        "context-engineering",
        "tool-search",
        "code-mode",
        "security",
        "reliability",
        "module-02",
    ],

    "prerequisite_ids": ["M02.L01"],

    "lesson": {
        "title": "Advanced MCP Clients and Production Best Practices",

        "content": (
            "# Advanced MCP Clients and Production Best Practices\n"
            "\n"
            "> **Lesson:** M02.L02  \n"
            "> **Module:** Building MCP Clients  \n"
            "> **Source alignment:** Chapter 4 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain how a client can provide capabilities back to a connected MCP server.\n"
            "- Describe the Multi Round-Trip Requests (MRTR) pattern used by the modern protocol model described in the chapter.\n"
            "- Explain sampling, roots, and elicitations, including their security implications and deprecation status in the source.\n"
            "- Design human-in-the-loop approval flows around server-initiated behavior.\n"
            "- Explain how OAuth 2.1 authorization fits into remote MCP client connections.\n"
            "- Separate MCP-native tool definitions from model-provider-specific formats.\n"
            "- Use an internal representation to support multiple LLM providers.\n"
            "- Explain how the MCP Registry can simplify server discovery and connection configuration.\n"
            "- Manage multiple MCP servers using grouped client sessions.\n"
            "- Identify primitive-name collision risks across multiple servers.\n"
            "- Apply context-engineering patterns to reduce tool-list token cost.\n"
            "- Compare tool assembling, tool search, and code execution approaches.\n"
            "- Design retry, refresh, resubscription, and backoff behavior for failed connections.\n"
            "- Apply security and UX best practices to production MCP clients.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Moving beyond a basic MCP client\n"
            "\n"
            "In the previous lesson, the client mostly consumed capabilities from the server: tools, resources, and prompts. "
            "This chapter adds the reverse direction: **the client can also provide capabilities that a server can make use of**.\n"
            "\n"
            "The source focuses on three client-side capabilities:\n"
            "\n"
            "| Capability | What the server receives from the client |\n"
            "|---|---|\n"
            "| Sampling | Access to the host application's LLM through the client |\n"
            "| Roots | Information about filesystem locations intended to be available |\n"
            "| Elicitation | A way to ask the user for information or consent through the host UI |\n"
            "\n"
            "The general implementation pattern is callback-based:\n"
            "\n"
            "```text\n"
            "1. Implement a callback in the client.\n"
            "2. Match the callback signature expected by the SDK/protocol type.\n"
            "3. Pass the callback into the Client constructor.\n"
            "4. The SDK advertises that capability and invokes the callback when needed.\n"
            "```\n"
            "\n"
            "This is an important architectural shift. Your MCP client is no longer only a tunnel from host to server. It becomes "
            "an active trust and interaction boundary between the server, the user, the LLM, and the host machine.\n"
            "\n"
            "> **Version note from the supplied chapter:** roots, sampling, and logging are described as being deprecated in the "
            "modern specification/SDK direction. They are still taught so that clients can support older servers. Treat these as "
            "version-specific compatibility topics rather than features you should automatically add to every new system.\n"
            "\n"
            "[[IMAGE_NEEDED: Bidirectional MCP client capabilities | "
            "A diagram showing Host + MCP Client in the center, server-provided primitives flowing from MCP Server to Host, and "
            "client-provided capabilities sampling/roots/elicitation flowing back toward the server through callbacks | "
            "Learner should notice that the client becomes an active boundary, not merely a passive connector]]\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Understanding Multi Round-Trip Requests (MRTR)\n"
            "\n"
            "The chapter explains an important change in the modern MCP interaction model. Older protocol behavior could allow a "
            "server to directly initiate requests to a client. In the newer model described by the source, server-to-client needs "
            "are handled as part of a request that **originally came from the client**.\n"
            "\n"
            "This is the **Multi Round-Trip Requests (MRTR)** pattern.\n"
            "\n"
            "### MRTR step by step\n"
            "\n"
            "```text\n"
            "Client → Server: original request\n"
            "Server → Client: InputRequiredResult(inputRequests=...)\n"
            "Client: run callback / gather required input\n"
            "Client → Server: retry original action with a new request ID + inputResponses\n"
            "Server → Client: final result\n"
            "```\n"
            "\n"
            "The key rule is that the server's request for extra input happens **inside the flow of a client-originated action**.\n"
            "\n"
            "For the developer, the good news is that the Python SDK handles most of this round-trip machinery behind the scenes. "
            "Your main responsibility is to implement the callback correctly and safely.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP Multi Round-Trip Request flow | "
            "A sequence diagram with Client sending request, Server returning InputRequiredResult, Client callback collecting information, "
            "Client retrying with inputResponses and a new request ID, then Server returning the final result | "
            "Learner should notice that the server's extra request is part of a client-originated workflow]]\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Sampling: letting a server request use of the host LLM\n"
            "\n"
            "Sampling allows a connected server to ask the client to use the host application's LLM. This can enable sophisticated "
            "nested workflows. For example, a server-side tool could need the model to classify something, generate text, choose among "
            "options, or help complete part of a larger operation.\n"
            "\n"
            "### Why sampling is powerful\n"
            "\n"
            "Without sampling, the server can execute its own deterministic code but does not automatically gain access to the host's "
            "model. Sampling provides a controlled bridge to that model.\n"
            "\n"
            "A sampling request may carry information such as:\n"
            "\n"
            "- messages,\n"
            "- model preferences,\n"
            "- an optional system prompt,\n"
            "- requested context behavior,\n"
            "- temperature,\n"
            "- maximum tokens,\n"
            "- stop sequences.\n"
            "\n"
            "The client callback translates this request into the format expected by the host's LLM provider, calls the model, converts "
            "the result back into MCP content, and returns it to the server.\n"
            "\n"
            "### The most important sampling rule: preserve user control\n"
            "\n"
            "The source strongly emphasizes **human-in-the-loop (HITL)** approval. A server should not silently spend the user's model "
            "budget or inject arbitrary model prompts through the client.\n"
            "\n"
            "A safer flow is:\n"
            "\n"
            "```text\n"
            "Server requests sampling\n"
            "      ↓\n"
            "Client shows server identity + requested prompt/purpose\n"
            "      ↓\n"
            "User approves or rejects\n"
            "      ↓\n"
            "If approved, client calls LLM\n"
            "      ↓\n"
            "Client may show output for approval\n"
            "      ↓\n"
            "Approved result returns to server\n"
            "```\n"
            "\n"
            "The chapter also recommends respecting model preference hints where appropriate and implementing rate limiting.\n"
            "\n"
            "### Simplified callback structure\n"
            "\n"
            "```python\n"
            "async def _handle_sampling(self, context, params):\n"
            "    # 1. Validate / ask for user approval\n"
            "    # 2. Translate MCP messages to provider format\n"
            "    # 3. Call the host LLM\n"
            "    # 4. Convert the result back to MCP content\n"
            "    # 5. Return CreateMessageResult or ErrorData\n"
            "    ...\n"
            "```\n"
            "\n"
            "The source's code intentionally simplifies the HITL layer for teaching, and explicitly warns that such a simplified "
            "implementation is not appropriate for real deployment.\n"
            "\n"
            "{{exercise:M02.L02.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Roots: coordinating filesystem scope\n"
            "\n"
            "Roots communicate which filesystem locations are intended to be available to a server. A coding assistant, for example, "
            "might expose only the user's selected project directory.\n"
            "\n"
            "A root contains at least a file URI and may include a human-readable name and metadata.\n"
            "\n"
            "### Roots are coordination, not enforcement\n"
            "\n"
            "This is one of the most important warnings in the chapter:\n"
            "\n"
            "**Roots are not a security sandbox.**\n"
            "\n"
            "A server can choose not to respect them. Therefore, the host application still needs actual access controls around files "
            "and directories.\n"
            "\n"
            "The source lists several implementation expectations:\n"
            "\n"
            "- expose only locations whose permissions match the intended use,\n"
            "- validate root URIs to prevent path traversal,\n"
            "- implement real access controls,\n"
            "- monitor accessibility,\n"
            "- get user consent before sharing roots,\n"
            "- provide understandable UI for inspecting and changing roots.\n"
            "\n"
            "### Callback pattern\n"
            "\n"
            "The client can keep a list of configured filesystem URIs, validate them, convert them into `Root` objects, and return them "
            "from a roots callback. If no valid roots remain after validation, the callback can return structured error information.\n"
            "\n"
            "The chapter's example also illustrates a broader design principle: **the host owns user configuration; the client exposes "
            "that configuration to MCP in protocol form**.\n"
            "\n"
            "[[IMAGE_NEEDED: Roots as coordination vs real access control | "
            "A diagram showing a user-selected project directory passed as an MCP root to a server, while a separate host-side permission "
            "boundary enforces actual filesystem access | "
            "Learner should notice that the root is a hint/scope declaration, while security enforcement must exist elsewhere]]\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Elicitations: bringing the human into the loop\n"
            "\n"
            "Elicitations allow the server to ask the user for additional information through the client and host application's UI. "
            "This is useful when a workflow needs clarification, approval, structured information, or a decision that should not be "
            "guessed by the model.\n"
            "\n"
            "The chapter describes three user outcomes:\n"
            "\n"
            "| Outcome | Meaning |\n"
            "|---|---|\n"
            "| accept | The user agrees and provides the requested information |\n"
            "| decline | The user explicitly rejects the request |\n"
            "| cancel | The interaction ends without an explicit approval or denial |\n"
            "\n"
            "Servers can provide a structured schema describing the requested fields. The client can render a form, collect input, "
            "validate it, and return the accepted data.\n"
            "\n"
            "### Safe elicitation UX\n"
            "\n"
            "The source recommends that the client:\n"
            "\n"
            "- show which server is asking,\n"
            "- explain what information is requested and why,\n"
            "- allow accept/decline/cancel,\n"
            "- validate returned data against the schema,\n"
            "- rate-limit repeated requests.\n"
            "\n"
            "The chapter also discusses URL-style elicitation. A safe client shows the full destination URL and asks for explicit user "
            "consent before opening it.\n"
            "\n"
            "### Generic callback, specific UI\n"
            "\n"
            "The callback should not need hard-coded knowledge of every server. It receives a request schema and dynamically renders or "
            "collects the required information. This preserves one of MCP's central goals: decoupling host applications from individual "
            "server implementations.\n"
            "\n"
            "[[IMAGE_NEEDED: Elicitation user-consent flow | "
            "A sequence diagram showing Server requesting information, Client displaying server identity and schema, User choosing "
            "accept/decline/cancel, and accepted structured data returning through the client | "
            "Learner should notice that the client protects the user from silent server data collection]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Authorizing remote MCP servers with OAuth 2.1\n"
            "\n"
            "Remote MCP servers often expose protected tools or data. The chapter uses OAuth 2.1 as the authorization model for these "
            "connections.\n"
            "\n"
            "The key OAuth roles map naturally to MCP:\n"
            "\n"
            "| OAuth concept | MCP equivalent |\n"
            "|---|---|\n"
            "| OAuth client | MCP client / host application |\n"
            "| Resource server | Protected MCP server |\n"
            "| Authorization server | Separate identity/authorization system |\n"
            "\n"
            "### Conceptual authorization flow\n"
            "\n"
            "```text\n"
            "User asks host to access protected MCP server\n"
            "        ↓\n"
            "MCP client receives authorization challenge\n"
            "        ↓\n"
            "Authorization server authenticates user\n"
            "        ↓\n"
            "Client receives/stores token\n"
            "        ↓\n"
            "Client uses token when accessing MCP server\n"
            "        ↓\n"
            "MCP server validates token and allows/denies access\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: OAuth flow for a remote MCP server | "
            "A diagram showing User/Host, MCP Client as OAuth client, Authorization Server, and MCP Server as resource server; show token "
            "issuance and authenticated MCP request | "
            "Learner should notice that the authorization server is separate from MCP even though the MCP client uses its token]]\n"
            "\n"
            "### Client registration\n"
            "\n"
            "The chapter introduces two registration ideas:\n"
            "\n"
            "- **Client ID Metadata Document (CIMD)** — the preferred path described in the source for a hosted client identity.\n"
            "- **Dynamic Client Registration (DCR)** — a fallback/alternative supported through client metadata.\n"
            "\n"
            "The application supplies details such as redirect URIs, scopes, token storage, redirect handling, and authorization callbacks. "
            "The SDK then handles much of the detailed registration/authorization flow.\n"
            "\n"
            "### Why OAuth belongs in the HTTP client layer\n"
            "\n"
            "The client wrapper can accept an `auth` object and pass it into the asynchronous HTTP client used by Streamable HTTP. "
            "This keeps authorization integrated with remote transport behavior rather than hard-coding token logic throughout the agent.\n"
            "\n"
            "### Security principle\n"
            "\n"
            "Authorization tokens are credentials. They should be stored and handled using an application-appropriate secure token-storage "
            "mechanism, not printed, embedded into prompts, or committed to source control.\n"
            "\n"
            "{{exercise:M02.L02.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Supporting multiple model providers\n"
            "\n"
            "MCP should not force your host application to use one model provider. However, different model APIs represent tools and "
            "messages differently.\n"
            "\n"
            "A poor design is to make the MCP client return tool objects already formatted for one provider. That couples your client "
            "to that provider.\n"
            "\n"
            "A better design is to create an **internal representation**.\n"
            "\n"
            "```text\n"
            "MCP Tool\n"
            "   ↓\n"
            "InternalTool\n"
            "   ├── translate_to_anthropic()\n"
            "   ├── translate_to_openai()\n"
            "   └── translate_to_other_provider()\n"
            "```\n"
            "\n"
            "An internal tool might store only provider-neutral data:\n"
            "\n"
            "```python\n"
            "class InternalTool:\n"
            "    def __init__(self, name, input_schema, description=None):\n"
            "        self.name = name\n"
            "        self.input_schema = input_schema\n"
            "        self.description = description\n"
            "```\n"
            "\n"
            "The host then decides which translation method to use based on the active model.\n"
            "\n"
            "### Why this architecture is better\n"
            "\n"
            "- MCP protocol handling stays independent of model choice.\n"
            "- The host owns the model-selection decision.\n"
            "- Adding another model provider does not require redesigning server communication.\n"
            "- Testing becomes easier because protocol objects and provider adapters can be tested separately.\n"
            "\n"
            "[[IMAGE_NEEDED: Provider-neutral tool adapter pattern | "
            "A diagram showing MCP Server → MCP Client → InternalTool representation branching into Anthropic adapter, OpenAI adapter, "
            "and another provider adapter → selected LLM | "
            "Learner should notice that model-specific translation happens after MCP-native discovery]]\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Discovering servers with the MCP Registry\n"
            "\n"
            "The chapter describes the MCP Registry as a central discovery mechanism for MCP servers. From a client developer's "
            "perspective, the major benefit is that registry metadata can provide the information required to configure a connection.\n"
            "\n"
            "For a remote server, registry data may provide a Streamable HTTP URL.\n"
            "\n"
            "For a local packaged server, registry metadata may provide information that maps to:\n"
            "\n"
            "- a runtime such as `uvx` or `npx`,\n"
            "- package identifier,\n"
            "- runtime arguments,\n"
            "- transport information.\n"
            "\n"
            "This enables UX such as:\n"
            "\n"
            "```text\n"
            "User selects server by name\n"
            "        ↓\n"
            "Host queries registry\n"
            "        ↓\n"
            "Host resolves supported transport\n"
            "        ↓\n"
            "Host builds MCP client connection settings\n"
            "        ↓\n"
            "Client connects\n"
            "```\n"
            "\n"
            "### Registry trust is not code auditing\n"
            "\n"
            "A registry can improve discoverability and publisher identity, but it does not automatically mean every server's code is "
            "safe. The chapter recommends production practices such as version pinning and secure authorization handling.\n"
            "\n"
            "This is especially important for local packages because installing/running a local MCP server means executing code in the "
            "user's or application's environment.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Connecting to multiple MCP servers\n"
            "\n"
            "A single low-level client session still represents one server relationship. For applications that need many servers, "
            "the source introduces `ClientSessionGroup` as a way to manage several sessions together.\n"
            "\n"
            "A session group can:\n"
            "\n"
            "- connect to multiple servers,\n"
            "- keep a collection of sessions,\n"
            "- aggregate tools, resources, and prompts,\n"
            "- map tools back to the appropriate session,\n"
            "- disconnect individual servers.\n"
            "\n"
            "This changes the client wrapper. Instead of storing one `_client` and one `_connected` flag, it can store a session group "
            "and determine readiness from whether the group currently has sessions.\n"
            "\n"
            "### Name collisions become a real architecture problem\n"
            "\n"
            "The chapter warns that primitive names are aggregated into dictionaries. Two servers exposing the same tool or primitive "
            "name can therefore collide.\n"
            "\n"
            "Solutions include:\n"
            "\n"
            "- rejecting collisions,\n"
            "- namespacing primitives by server,\n"
            "- using a component-name hook to rename them consistently.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "github:create_issue\n"
            "linear:create_issue\n"
            "```\n"
            "\n"
            "is much safer than having two unqualified `create_issue` tools.\n"
            "\n"
            "[[IMAGE_NEEDED: Multi-server session group | "
            "A diagram with one host/client wrapper containing ClientSessionGroup and three separate sessions connected to three MCP servers; "
            "show aggregated tools/resources/prompts and namespaced tool names | "
            "Learner should notice that many sessions are managed together but server identity must still be preserved]]\n"
            "\n"
            "{{exercise:M02.L02.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Context engineering for large tool sets\n"
            "\n"
            "Tool definitions consume model context. If an application connects to many servers, sending every tool schema on every "
            "LLM call can become expensive and can also make tool selection harder.\n"
            "\n"
            "The chapter explores several patterns for reducing this footprint.\n"
            "\n"
            "### Pattern A: tool assembler / refresh every turn\n"
            "\n"
            "The application rebuilds the available tool list on each conversation turn. This does not necessarily reduce tokens, but "
            "it reduces stale definitions.\n"
            "\n"
            "Repeated discovery does not have to hammer the server if the SDK cache is configured. A TTL allows the client to serve "
            "recent tool metadata locally until the cache expires or a list-change event invalidates it.\n"
            "\n"
            "Think of this pattern as prioritizing **freshness**, not token reduction.\n"
            "\n"
            "### Pattern B: tool search\n"
            "\n"
            "Instead of exposing every tool, expose a small `search_tools` capability. The model searches for a relevant tool first, "
            "then only matching tool definitions are added to the active tool list.\n"
            "\n"
            "```text\n"
            "All tools stored outside active context\n"
            "        ↓\n"
            "Model sees search_tools only\n"
            "        ↓\n"
            "Model searches: 'count'\n"
            "        ↓\n"
            "Matching tool definitions added\n"
            "        ↓\n"
            "Model selects actual tool\n"
            "```\n"
            "\n"
            "This can greatly reduce context size when the application has dozens or hundreds of tools.\n"
            "\n"
            "The tradeoff is an extra search step and potentially an extra model/tool round trip.\n"
            "\n"
            "The same concept can be used to search resources before loading them into context.\n"
            "\n"
            "### Pattern C: code execution / code mode\n"
            "\n"
            "The chapter describes a more radical pattern: give the model a small execution interface plus searchable typed tool stubs, "
            "then ask the model to generate code that coordinates several operations inside a sandbox.\n"
            "\n"
            "This can reduce:\n"
            "\n"
            "- the number of tool schemas in model context,\n"
            "- the number of intermediate model round trips,\n"
            "- the amount of intermediate result data copied into the context window.\n"
            "\n"
            "But it introduces a critical requirement: **the execution sandbox must be genuinely isolated**.\n"
            "\n"
            "The source highlights isolation expectations such as:\n"
            "\n"
            "- no outbound network access from the sandbox,\n"
            "- no authorization credentials inside the sandbox,\n"
            "- no access back into the host application's execution environment,\n"
            "- MCP tool execution still routed through the trusted client boundary.\n"
            "\n"
            "[[IMAGE_NEEDED: Tool context optimization patterns | "
            "A three-panel comparison: full refreshed tool list, search_tools progressive disclosure, and code execution with typed stubs inside "
            "an isolated sandbox | "
            "Learner should notice the tradeoff between simplicity, token savings, extra round trips, and security complexity]]\n"
            "\n"
            "{{exercise:M02.L02.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## 11. Security: treat the client as a trust boundary\n"
            "\n"
            "This is one of the chapter's most important production lessons.\n"
            "\n"
            "The MCP client sits between potentially untrusted servers and the host application, model, user data, filesystem, and credentials. "
            "Therefore, **the client is a trust boundary**.\n"
            "\n"
            "### Tool definitions are untrusted input\n"
            "\n"
            "A tool name, description, schema, result, resource, or prompt may contain text that reaches the LLM's context. The source points "
            "out that this is effectively intentional prompt injection: external data is being inserted into the model's prompt by design.\n"
            "\n"
            "The engineering challenge is to allow legitimate context while limiting malicious influence.\n"
            "\n"
            "### Useful client-side defenses from the chapter\n"
            "\n"
            "- require user approval before enabling new tools,\n"
            "- show tool names, descriptions, and schemas,\n"
            "- re-request approval after capability-list changes when appropriate,\n"
            "- namespace tools by server to reduce name-shadowing attacks,\n"
            "- use environment-based credential handling for local servers,\n"
            "- use OAuth for remote protected services,\n"
            "- pin local server/package versions,\n"
            "- prefer trusted registries,\n"
            "- keep sensitive operations behind explicit user consent.\n"
            "\n"
            "### Local server risk\n"
            "\n"
            "Running a local MCP server means executing code in the local environment. That deserves the same caution as installing any "
            "other package or executable.\n"
            "\n"
            "The correct security posture also depends on what the host can reach. A toy local calculator has a very different risk profile "
            "from a banking or enterprise-administration application.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. Resilient connection management\n"
            "\n"
            "The chapter emphasizes retry-and-refresh behavior rather than complicated connection-resume state.\n"
            "\n"
            "### stdio recovery\n"
            "\n"
            "A dropped stdio session often means the subprocess crashed. Recovery generally requires:\n"
            "\n"
            "```text\n"
            "Detect failure → restart subprocess → reconnect → refresh capabilities → retry appropriate action\n"
            "```\n"
            "\n"
            "Anything held only in the old server process's memory is lost, so the client cannot assume server state survived.\n"
            "\n"
            "### Streamable HTTP recovery\n"
            "\n"
            "Remote requests can be retried with backoff. However, the source raises an important issue: retrying an action may duplicate "
            "side effects if the tool is not idempotent.\n"
            "\n"
            "Therefore, the host/client may need deduplication logic for actions such as creating tickets, sending messages, or charging money.\n"
            "\n"
            "### Subscriptions\n"
            "\n"
            "For clients listening to change events, an interrupted subscription should normally trigger:\n"
            "\n"
            "```text\n"
            "Subscription lost\n"
            "      ↓\n"
            "Backoff\n"
            "      ↓\n"
            "Re-listen\n"
            "      ↓\n"
            "Re-fetch state as needed\n"
            "```\n"
            "\n"
            "The source also notes that older servers may not support `listen()`, so clients need a fallback path when listening is unsupported.\n"
            "\n"
            "### Background watcher pattern\n"
            "\n"
            "A change watcher can run beside the main conversation loop as an async task and be cancelled during shutdown. This keeps "
            "capability-change handling independent from the main user interaction loop.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP recovery and resubscription flow | "
            "A diagram showing stdio crash recovery on one side and Streamable HTTP retry/backoff on the other, with a shared branch for "
            "refreshing capabilities and restoring subscriptions | "
            "Learner should notice that recovery strategy differs by transport but both require refresh and careful retry]]\n"
            "\n"
            "---\n"
            "\n"
            "## 13. User experience: pagination, caching, and visibility\n"
            "\n"
            "A technically correct client can still feel slow or confusing. The chapter closes by connecting MCP engineering to user experience.\n"
            "\n"
            "### Pagination\n"
            "\n"
            "Large lists should be fetched in pages. The server can return a `nextCursor`, and the client passes that cursor into the same "
            "list method to request the next page.\n"
            "\n"
            "The source identifies pagination support for list operations such as:\n"
            "\n"
            "- `list_resources()`,\n"
            "- `list_resource_templates()`,\n"
            "- `list_prompts()`,\n"
            "- `list_tools()`.\n"
            "\n"
            "Pagination helps both memory usage and perceived responsiveness.\n"
            "\n"
            "### Caching\n"
            "\n"
            "Caching tool/resource/prompt metadata with sensible TTLs avoids repeated network or process calls for read-heavy workloads. "
            "The challenge is balancing responsiveness against stale data.\n"
            "\n"
            "List-change notifications and explicit refresh paths help solve this.\n"
            "\n"
            "### Make failures visible\n"
            "\n"
            "If a previously available tool disappears, the UI should reflect that quickly. Hiding stale capabilities creates confusing "
            "failures and reduces user trust.\n"
            "\n"
            "### A production client is partly a UX product\n"
            "\n"
            "Approval dialogs, authorization redirects, elicitation forms, progress indicators, error messages, retries, and server pickers "
            "are not merely protocol glue. They determine whether the system feels safe and understandable.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'Client-provided capabilities mean the server can freely control my host.'\n"
            "\n"
            "**Why this is wrong:** the client decides which callbacks to provide and should mediate sensitive interactions through validation, "
            "policy, and user approval.\n"
            "\n"
            "### Misconception 2: 'Roots secure the filesystem.'\n"
            "\n"
            "**Why this is wrong:** roots communicate intended scope but are not an enforcement boundary. Real access control is still required.\n"
            "\n"
            "### Misconception 3: 'Sampling is just another server-side model call.'\n"
            "\n"
            "**Why this is wrong:** sampling uses the host's LLM through the client, which creates cost, trust, privacy, and consent concerns.\n"
            "\n"
            "### Misconception 4: 'OAuth authenticates everything automatically.'\n"
            "\n"
            "**Why this is wrong:** OAuth handles authorization flows, but the application still needs secure token storage, correct redirect/callback "
            "handling, and sensible scopes.\n"
            "\n"
            "### Misconception 5: 'Supporting multiple models means duplicating the whole MCP client.'\n"
            "\n"
            "**Why this is wrong:** a provider-neutral internal representation lets the MCP layer remain stable while adapters translate to each model API.\n"
            "\n"
            "### Misconception 6: 'A registry entry means a server is fully trusted.'\n"
            "\n"
            "**Why this is wrong:** discovery/publisher metadata is not equivalent to code review. Local packages still execute code and should be version-pinned "
            "and evaluated appropriately.\n"
            "\n"
            "### Misconception 7: 'Connecting to more servers only increases capability.'\n"
            "\n"
            "**Why this is wrong:** it also increases tool collisions, context size, security surface, and operational complexity.\n"
            "\n"
            "### Misconception 8: 'Tool search and code mode solve the same problem in the same way.'\n"
            "\n"
            "**Why this is wrong:** tool search narrows what tool definitions enter context; code execution changes how several operations are orchestrated and "
            "can keep intermediate results outside the model context.\n"
            "\n"
            "### Misconception 9: 'Retrying a failed tool call is always safe.'\n"
            "\n"
            "**Why this is wrong:** non-idempotent actions can be duplicated. Retry logic must understand side effects or include deduplication safeguards.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Client capability | Functionality the MCP client exposes for server workflows through callbacks |\n"
            "| MRTR | Multi Round-Trip Requests; a pattern where a server asks for additional input inside a client-originated request flow |\n"
            "| InputRequiredResult | Server response indicating more client/user input is required before the original operation can complete |\n"
            "| Sampling | Client capability that lets a server request use of the host application's LLM |\n"
            "| HITL | Human-in-the-loop approval or input during an automated workflow |\n"
            "| Roots | Filesystem locations the client communicates as intended server scope; not a complete access-control boundary |\n"
            "| Elicitation | Server request for user input, consent, structured form data, or URL continuation through the client |\n"
            "| OAuth 2.1 | Authorization standard used by the source for protected remote MCP server access |\n"
            "| Authorization server | System that authenticates/authorizes the user and issues access tokens |\n"
            "| Resource server | Protected service receiving access tokens; mapped to the MCP server in the chapter's OAuth model |\n"
            "| CIMD | Client ID Metadata Document used to publish client registration metadata |\n"
            "| DCR | Dynamic Client Registration fallback/alternative for registering a client |\n"
            "| InternalTool | Provider-neutral internal representation of an MCP tool |\n"
            "| MCP Registry | Server-discovery metadata source described by the chapter |\n"
            "| ClientSessionGroup | SDK abstraction for managing multiple MCP server sessions together |\n"
            "| Name collision | Conflict where multiple servers expose primitives with the same name |\n"
            "| Tool assembler | Pattern that refreshes/reassembles tools on each turn, often backed by a cache |\n"
            "| Tool search | Progressive-disclosure pattern that loads only tool definitions relevant to the current task |\n"
            "| Code mode | Pattern where model-generated code orchestrates operations inside an isolated sandbox |\n"
            "| TTL | Time to live; duration before cached capability metadata expires |\n"
            "| Idempotent action | Operation that can safely be repeated without unintended duplicate side effects |\n"
            "| Backoff | Waiting between retries, often increasing delay after repeated failures |\n"
            "| `nextCursor` | Pagination pointer used to request the next page of list results |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What changes when an MCP client provides capabilities back to the server?\n"
            "2. What problem does MRTR solve in the modern request model described by the source?\n"
            "3. Why should sampling normally require user approval?\n"
            "4. Why are roots not equivalent to filesystem security?\n"
            "5. What is the difference between elicitation accept, decline, and cancel?\n"
            "6. How do the OAuth client, resource server, and authorization server map onto MCP?\n"
            "7. Why is a provider-neutral `InternalTool` representation useful?\n"
            "8. What can a registry simplify for the host application?\n"
            "9. Why can primitive names collide when multiple servers are aggregated?\n"
            "10. What problem does namespacing solve?\n"
            "11. What is the difference between tool assembler and tool search?\n"
            "12. Why can code execution reduce model context usage?\n"
            "13. What isolation properties should a code-execution sandbox have?\n"
            "14. Why should tool definitions themselves be treated as untrusted input?\n"
            "15. Why can a retry duplicate side effects?\n"
            "16. What should happen after a change subscription is lost?\n"
            "17. How do pagination and caching improve user experience?\n"
            "18. Why should a UI reflect capability changes quickly?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**A production MCP client is a trust boundary and orchestration layer, not just a protocol adapter. It decides what servers may "
            "access, when the user must approve an action, how models and servers are translated and discovered, how much context reaches the LLM, "
            "and how the system recovers when network, process, or capability state changes.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "client-capabilities", "title": "Moving beyond a basic MCP client", "order": 1},
            {"id": "mrtr", "title": "Understanding Multi Round-Trip Requests", "order": 2},
            {"id": "sampling", "title": "Sampling", "order": 3},
            {"id": "roots", "title": "Roots", "order": 4},
            {"id": "elicitations", "title": "Elicitations", "order": 5},
            {"id": "oauth", "title": "OAuth 2.1 authorization", "order": 6},
            {"id": "multi-model", "title": "Supporting multiple model providers", "order": 7},
            {"id": "registry", "title": "Discovering servers with the MCP Registry", "order": 8},
            {"id": "multiple-servers", "title": "Connecting to multiple MCP servers", "order": 9},
            {"id": "context-engineering", "title": "Context engineering for large tool sets", "order": 10},
            {"id": "security", "title": "Security and trust boundaries", "order": 11},
            {"id": "connection-recovery", "title": "Resilient connection management", "order": 12},
            {"id": "ux", "title": "User experience", "order": 13},
        ],
    },

    "exercises": [
        {
            "id": "M02.L02.EX01",
            "title": "Design a Safe Sampling Flow",
            "lesson_code": "M02.L02",
            "section_id": "sampling",
            "placement": "after_section",
            "description": (
                "Design a human-in-the-loop sampling workflow that lets a server request model "
                "assistance without giving it silent access to the user's LLM."
            ),
            "instructions": (
                "A connected MCP server asks your client to use the host LLM to summarize a private "
                "document before the server continues its tool operation.\n\n"
                "1. Identify what information should be displayed to the user before the model call.\n"
                "2. Decide what the user can approve or reject.\n"
                "3. Explain whether the server-provided system prompt should automatically override the host prompt.\n"
                "4. Add one rate-limit rule.\n"
                "5. Decide whether to ask for approval again before returning the model result to the server.\n"
                "6. Draw the MRTR flow from original client request through final server response."
            ),
            "expected_output": (
                "A safe sampling design with approval points, validation/policy decisions, one "
                "rate-limiting rule, and an MRTR sequence."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["sampling", "hitl", "mrtr", "security"],
        },

        {
            "id": "M02.L02.EX02",
            "title": "Map an OAuth-Protected MCP Connection",
            "lesson_code": "M02.L02",
            "section_id": "oauth",
            "placement": "after_section",
            "description": (
                "Practice mapping OAuth roles and client responsibilities to a remote MCP service."
            ),
            "instructions": (
                "Imagine a remote MCP server exposes protected project-management tools.\n\n"
                "1. Identify the OAuth client, resource server, authorization server, and end user.\n"
                "2. Explain what should happen after the MCP server returns an authorization challenge.\n"
                "3. Define example read and write scopes.\n"
                "4. State where tokens should be stored.\n"
                "5. Explain the purpose of a redirect URI.\n"
                "6. Explain why authorization logic belongs in the remote HTTP client layer rather than in every tool wrapper."
            ),
            "expected_output": (
                "An OAuth architecture diagram or table plus a six-step authorization explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["oauth", "remote-mcp", "authorization", "security"],
        },

        {
            "id": "M02.L02.EX03",
            "title": "Design a Multi-Server MCP Client",
            "lesson_code": "M02.L02",
            "section_id": "multiple-servers",
            "placement": "after_section",
            "description": (
                "Design a client that combines several MCP servers without losing server identity "
                "or allowing primitive-name collisions."
            ),
            "instructions": (
                "Your agent connects to three servers: GitHub, Linear, and an internal documentation server.\n\n"
                "1. Describe how ClientSessionGroup can organize the sessions.\n"
                "2. Give an example of a tool-name collision between GitHub and Linear.\n"
                "3. Propose a namespacing convention.\n"
                "4. Explain how you would preserve the mapping from tool to originating server/session.\n"
                "5. Explain how disconnecting one server should affect its primitives.\n"
                "6. List two new security or context-management problems that appear once several servers are connected."
            ),
            "expected_output": (
                "A multi-server design with session management, namespaced tools, origin mapping, "
                "disconnect behavior, and risk analysis."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["multi-server", "namespacing", "session-management", "architecture"],
        },

        {
            "id": "M02.L02.EX04",
            "title": "Choose a Tool Context Strategy",
            "lesson_code": "M02.L02",
            "section_id": "context-engineering",
            "placement": "after_section",
            "description": (
                "Compare context-engineering approaches for an agent with a very large tool catalog."
            ),
            "instructions": (
                "Your host application connects to several servers and has 180 available tools.\n\n"
                "Compare these three strategies:\n"
                "A. Send the full refreshed tool list every turn.\n"
                "B. Expose only a search_tools tool, then progressively add matching tools.\n"
                "C. Use a sandboxed code-execution approach with typed tool stubs.\n\n"
                "For each strategy, discuss token usage, latency/round trips, implementation complexity, "
                "tool freshness, and security. Then select the most appropriate strategy for:\n"
                "1. a small internal prototype,\n"
                "2. a production assistant with 180 tools,\n"
                "3. an automation environment that already has a hardened isolated sandbox."
            ),
            "expected_output": (
                "A comparison table across the five tradeoff dimensions and justified choices for "
                "the three scenarios."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["context-engineering", "tool-search", "code-mode", "tradeoff-analysis"],
        },
    ],

    "quiz": {
        "id": "M02.L02.QZ01",
        "title": "Advanced MCP Clients — Knowledge Check",
        "lesson_code": "M02.L02",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M02.L02.Q01",
                "section_id": "mrtr",
                "question": "What is the purpose of the MRTR pattern described in the chapter?",
                "options": [
                    "To let a server start unlimited unrelated requests to a client.",
                    "To let a server request additional input while completing a client-originated operation.",
                    "To replace OAuth with repeated tool calls.",
                    "To merge several servers into one process.",
                ],
                "correct": 1,
                "explanation": (
                    "MRTR lets the server indicate that it needs more input inside a client-originated "
                    "flow, after which the client gathers that input and retries with inputResponses."
                ),
            },
            {
                "id": "M02.L02.Q02",
                "section_id": "sampling",
                "question": "Why is human approval especially important for sampling?",
                "options": [
                    "Sampling changes the MCP server's filesystem.",
                    "Sampling can cause an external server to use the host application's LLM, budget, and context.",
                    "Sampling disables all tools.",
                    "Sampling can only work with local servers.",
                ],
                "correct": 1,
                "explanation": (
                    "Sampling bridges a connected server to the user's model. That introduces cost, "
                    "privacy, and trust concerns that should be visible to the user."
                ),
            },
            {
                "id": "M02.L02.Q03",
                "section_id": "roots",
                "question": "Which statement about MCP roots is correct according to the supplied chapter?",
                "options": [
                    "Roots are a complete filesystem security sandbox.",
                    "Roots are coordination information and require real access controls for security.",
                    "Roots can only contain HTTP URLs.",
                    "Roots automatically encrypt local files.",
                ],
                "correct": 1,
                "explanation": (
                    "The source explicitly warns that roots are not a security measure. Servers can "
                    "choose not to respect them, so host-side enforcement is still required."
                ),
            },
            {
                "id": "M02.L02.Q04",
                "section_id": "elicitations",
                "question": "Which set contains the three elicitation outcomes described in the chapter?",
                "options": [
                    "allow, block, retry",
                    "accept, decline, cancel",
                    "read, write, execute",
                    "approve, timeout, refresh",
                ],
                "correct": 1,
                "explanation": (
                    "The source describes elicitation responses as accept, decline, or cancel."
                ),
            },
            {
                "id": "M02.L02.Q05",
                "section_id": "oauth",
                "question": "In the chapter's OAuth mapping, what is the MCP server?",
                "options": [
                    "The authorization server only",
                    "The resource server",
                    "The end user's browser",
                    "The OAuth client",
                ],
                "correct": 1,
                "explanation": (
                    "The MCP client is the OAuth client, while the protected MCP server acts as the resource server."
                ),
            },
            {
                "id": "M02.L02.Q06",
                "section_id": "multi-model",
                "question": "What is the main benefit of using an InternalTool representation?",
                "options": [
                    "It makes every tool execute locally.",
                    "It decouples MCP discovery from provider-specific tool formats.",
                    "It removes the need for tool schemas.",
                    "It prevents the host from switching models.",
                ],
                "correct": 1,
                "explanation": (
                    "A provider-neutral internal representation lets the host translate tools into "
                    "the format expected by the currently selected LLM provider."
                ),
            },
            {
                "id": "M02.L02.Q07",
                "section_id": "registry",
                "question": "What can an MCP Registry entry help a client application determine?",
                "options": [
                    "Only the server's natural-language description",
                    "Connection information such as a remote URL or local runtime/package settings",
                    "The user's OAuth password",
                    "The model's hidden reasoning trace",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter shows registry metadata being resolved into Streamable HTTP URLs "
                    "or local stdio runtime/package settings."
                ),
            },
            {
                "id": "M02.L02.Q08",
                "section_id": "multiple-servers",
                "question": "What is a major risk when primitives from several servers are aggregated into one session group?",
                "options": [
                    "Every server is forced to use the same transport.",
                    "Primitive names can collide.",
                    "OAuth can no longer be used.",
                    "Resources can no longer be read.",
                ],
                "correct": 1,
                "explanation": (
                    "The source warns that primitive dictionaries cannot safely contain duplicate names; "
                    "namespacing or renaming is needed."
                ),
            },
            {
                "id": "M02.L02.Q09",
                "section_id": "context-engineering",
                "question": "How does tool search reduce context use?",
                "options": [
                    "It removes the LLM from the system.",
                    "It loads only tool definitions relevant to the current request instead of all tools.",
                    "It permanently deletes unused tools from servers.",
                    "It converts tools into resources.",
                ],
                "correct": 1,
                "explanation": (
                    "Tool search uses progressive disclosure: the model first searches the catalog, then "
                    "only matching tool definitions are made active."
                ),
            },
            {
                "id": "M02.L02.Q10",
                "section_id": "security",
                "question": "Why should tool definitions be treated as untrusted input?",
                "options": [
                    "Because they are always invalid JSON.",
                    "Because server-provided text is injected into model context and could contain malicious instructions.",
                    "Because tools cannot contain descriptions.",
                    "Because they automatically execute during discovery.",
                ],
                "correct": 1,
                "explanation": (
                    "External tool metadata reaches model context by design, so the client must distinguish "
                    "legitimate context from potentially malicious prompt injection."
                ),
            },
            {
                "id": "M02.L02.Q11",
                "section_id": "connection-recovery",
                "question": "Why can blindly retrying a failed non-idempotent tool call be dangerous?",
                "options": [
                    "It can duplicate side effects.",
                    "It changes the transport to stdio.",
                    "It permanently deletes the session cache.",
                    "It prevents pagination.",
                ],
                "correct": 0,
                "explanation": (
                    "If the first action actually completed before the failure was observed, retrying it can "
                    "create a duplicate ticket, message, payment, or other side effect."
                ),
            },
            {
                "id": "M02.L02.Q12",
                "section_id": "ux",
                "type": "open",
                "question": (
                    "Design a production MCP client that connects to multiple remote and local servers. "
                    "Explain your approach to authorization, user approval, primitive namespacing, tool-context "
                    "management, retries, subscriptions, pagination, caching, and visibility of server changes."
                ),
            },
        ],
        "passing_score": 70,
    },
}
