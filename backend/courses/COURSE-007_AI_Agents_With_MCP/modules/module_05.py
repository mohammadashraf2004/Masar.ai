"""M03.L02 — Advanced MCP Servers: Utilities and Client Capabilities.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 6 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L02"

MODULE_ORDER = 3

MODULE_TITLE = "Building MCP Servers"

MODULE_DESCRIPTION = (
    "Extend MCP servers with protocol utilities and client-provided capabilities: "
    "completions, context, progress, notifications, pagination, capability detection, "
    "resolvers, elicitations, sampling, roots, and request cancellation."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Advanced MCP Servers: Utilities and Client Capabilities",

    "slug": "ai-agents-mcp-m03-l02",

    "description": (
        "Build more capable and production-aware MCP servers by using server utilities "
        "such as completions, context, progress reporting, notifications, and pagination, "
        "then integrate client-provided capabilities through resolvers while respecting "
        "consent, compatibility, deprecation, filesystem boundaries, and cancellation."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.0,

    "skill_tags": [
        "mcp-server",
        "server-utilities",
        "completions",
        "context-object",
        "progress",
        "notifications",
        "pagination",
        "client-capabilities",
        "resolvers",
        "elicitation",
        "sampling",
        "roots",
        "cancellation",
        "mcpserver",
        "module-03",
    ],

    "prerequisite_ids": ["M03.L01"],

    "lesson": {
        "title": "Advanced MCP Servers: Utilities and Client Capabilities",

        "content": (
            "# Advanced MCP Servers: Utilities and Client Capabilities\n"
            "\n"
            "> **Lesson:** M03.L02  \n"
            "> **Module:** Building MCP Servers  \n"
            "> **Source alignment:** Chapter 6 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what MCP server utilities add beyond tools, prompts, and resources.\n"
            "- Implement completion handlers for prompt and resource-template arguments.\n"
            "- Use the Python SDK `Context` object to inspect server, client, request, session, and lifespan information.\n"
            "- Distinguish protocol-level logging from ordinary Python logging and explain its deprecation status in the source.\n"
            "- Report progress for long-running server operations.\n"
            "- Send primitive-list and resource-update notifications correctly.\n"
            "- Explain cursor-based pagination and which MCP operations support it.\n"
            "- Detect client capabilities and decide when manual checks are useful.\n"
            "- Explain how the resolver mechanism injects externally resolved values before a tool body runs.\n"
            "- Build safe form and URL elicitations.\n"
            "- Explain legacy sampling, model preferences, and HITL concerns.\n"
            "- Explain roots as filesystem coordination rather than security enforcement.\n"
            "- Handle request cancellation and cleanup safely across transports.\n"
            "- Recognize which capabilities are deprecated in the 2026-07-28 specification described by the source.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. From serving primitives to building a complete server\n"
            "\n"
            "The previous lesson focused on the three core server primitives:\n"
            "\n"
            "```text\n"
            "Tools     → actions\n"
            "Prompts   → reusable interaction instructions\n"
            "Resources → contextual data\n"
            "```\n"
            "\n"
            "Those primitives are the foundation, but a serious server also needs support for usability, observability, "
            "large result sets, long-running work, client compatibility, and richer interaction flows.\n"
            "\n"
            "The chapter groups those additions into two broad categories.\n"
            "\n"
            "### Server utilities\n"
            "\n"
            "Utilities improve how a server communicates and operates. The source covers:\n"
            "\n"
            "- completions,\n"
            "- server/primitive icons,\n"
            "- the Python SDK `Context` object,\n"
            "- logging,\n"
            "- progress reporting,\n"
            "- manual change notifications,\n"
            "- pagination.\n"
            "\n"
            "### Client-provided capabilities\n"
            "\n"
            "The second half reverses the usual direction: instead of only giving capabilities to clients, the server may need something "
            "from the client application.\n"
            "\n"
            "The source covers:\n"
            "\n"
            "- **elicitation** → ask the user for input,\n"
            "- **sampling** → request use of the client's LLM,\n"
            "- **roots** → request filesystem scope information,\n"
            "- **cancellation** → allow a client/user to stop long-running work.\n"
            "\n"
            '{{image:mcp-server-capability-map}}'
            '\n'
            "\n"
            "> **Version note from the source:** the chapter states that protocol-level logging, sampling, and roots are deprecated in the "
            "2026-07-28 MCP specification direction. They are still taught for compatibility and architectural understanding.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Completions: autocomplete for prompts and resource templates\n"
            "\n"
            "Completions are inspired by IDE code completion. They let the server return suggestions while a user is filling in arguments "
            "for a prompt or resource template.\n"
            "\n"
            "A completion handler receives three important inputs:\n"
            "\n"
            "| Input | Meaning |\n"
            "|---|---|\n"
            "| `ref` | Which prompt or resource template is being completed |\n"
            "| `argument` | The argument name and current partial value |\n"
            "| `context` | Optional information about values already supplied for other arguments |\n"
            "\n"
            "The handler returns a completion result containing:\n"
            "\n"
            "- `values` — suggested strings, capped at 100 values,\n"
            "- `total` — optional number of available suggestions,\n"
            "- `has_more` — whether more suggestions exist than were returned.\n"
            "\n"
            "### Simple mental model\n"
            "\n"
            "```text\n"
            "User types partial argument\n"
            "        ↓\n"
            "Client sends completion request\n"
            "        ↓\n"
            "Server checks prompt/template + partial value + previous args\n"
            "        ↓\n"
            "Server returns suggestions\n"
            "        ↓\n"
            "Client renders them to user\n"
            "```\n"
            "\n"
            "### Why previous arguments matter\n"
            "\n"
            "Suppose a prompt asks for both `country` and `city`. Once the user has chosen a country, the server can use that earlier value "
            "to narrow the city suggestions. This makes completion context-sensitive instead of simply matching a static list.\n"
            "\n"
            "### Defensive completion design\n"
            "\n"
            "The source recommends thinking about:\n"
            "\n"
            "- rate limiting, because a client may send completion requests very frequently,\n"
            "- relevance ranking,\n"
            "- input validation,\n"
            "- avoiding sensitive suggestions such as credentials or API keys,\n"
            "- respecting the 100-value limit.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP completion lifecycle | "
            "A sequence diagram where the user types progressively more text, the client sends repeated completion requests, and the server returns a narrowing list of suggestions | "
            "Learner should notice that completion frequency is client-controlled, so server-side rate limiting may be necessary]]\n"
            "\n"
            "{{exercise:M03.L02.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Icons and the Context object\n"
            "\n"
            "The chapter briefly introduces icons as metadata that a client application can choose to display. A server may provide icons "
            "for itself and attach icons to tools, prompts, and resources.\n"
            "\n"
            "The more important concept is the Python SDK's **Context object**.\n"
            "\n"
            "A handler can receive it simply by adding a typed parameter:\n"
            "\n"
            "```python\n"
            "@mcp.tool()\n"
            "async def inspect_server(ctx: Context) -> dict:\n"
            "    ...\n"
            "```\n"
            "\n"
            "The SDK recognizes the type and injects the current request context automatically.\n"
            "\n"
            "### What Context gives you\n"
            "\n"
            "At a high level, `Context` gives access to:\n"
            "\n"
            "- server identity/configuration,\n"
            "- current client/session information,\n"
            "- request metadata,\n"
            "- request ID,\n"
            "- request method and parameters,\n"
            "- lifespan context,\n"
            "- client capabilities,\n"
            "- logging helpers,\n"
            "- progress reporting,\n"
            "- primitive/resource notifications.\n"
            "\n"
            "A useful hierarchy is:\n"
            "\n"
            "```text\n"
            "Context\n"
            "├── server information (`mcp_server`)\n"
            "├── session (`session`)\n"
            "├── client capabilities\n"
            "└── request context (`request_context`)\n"
            "    ├── request ID\n"
            "    ├── request metadata\n"
            "    ├── raw method/params\n"
            "    ├── lifespan context\n"
            "    └── transport-level request when available\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: MCP Python Context hierarchy | "
            "A tree diagram showing Context at the top and its mcp_server, session, client_capabilities, and request_context branches with their major properties | "
            "Learner should notice that one injected object exposes both static server state and per-request state]]\n"
            "\n"
            "### Server information\n"
            "\n"
            "`ctx.mcp_server` can expose information such as the server's name, instructions, website URL, icons, debug mode, and configured log level.\n"
            "\n"
            "### Session and client information\n"
            "\n"
            "`ctx.session` provides a lower-level view of communication with the connected client. The source notes that client identity metadata may be optional, "
            "so code should not assume it is always present.\n"
            "\n"
            "If you only need to know which capabilities the client supports, `ctx.client_capabilities` is the more direct source.\n"
            "\n"
            "### Request context and lifespan state\n"
            "\n"
            "The request context lets a handler access data specific to one operation. It can also expose state yielded by a lifespan function—for example, database handles, "
            "shared caches, or other server-lifetime resources created at startup and cleaned up at shutdown.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Logging: protocol logging vs ordinary application logging\n"
            "\n"
            "The chapter shows protocol-level logging through `Context` methods such as:\n"
            "\n"
            "```text\n"
            "ctx.debug(...)\n"
            "ctx.info(...)\n"
            "ctx.warning(...)\n"
            "ctx.error(...)\n"
            "```\n"
            "\n"
            "Historically, these messages were sent to the **client** as MCP logging notifications.\n"
            "\n"
            "### Important deprecation note\n"
            "\n"
            "The source states that protocol-level logging was deprecated in the 2026-07-28 specification direction. "
            "For new servers, it recommends ordinary Python logging instead of sending logs through MCP.\n"
            "\n"
            "That distinction matters:\n"
            "\n"
            "| Logging style | Destination | Modern recommendation in source |\n"
            "|---|---|---|\n"
            "| MCP protocol logging | Client application | Legacy compatibility only |\n"
            "| Python logging | Server's normal logging destination such as stderr/file/collector | Preferred for new servers |\n"
            "\n"
            "### Why logs still matter\n"
            "\n"
            "Whether you use legacy MCP logging or ordinary server logging, useful logs help diagnose:\n"
            "\n"
            "- which operation ran,\n"
            "- what request failed,\n"
            "- timing and latency,\n"
            "- capability changes,\n"
            "- cancellations,\n"
            "- unexpected server state.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Progress reporting for long-running work\n"
            "\n"
            "A long-running tool that appears frozen creates poor UX. Progress notifications let the server communicate ongoing work so the client can show progress to the user.\n"
            "\n"
            "The high-level API exposes a helper such as:\n"
            "\n"
            "```python\n"
            "await ctx.report_progress(\n"
            "    progress=current_step,\n"
            "    total=total_steps,\n"
            "    message='Processing records',\n"
            ")\n"
            "```\n"
            "\n"
            "### Known vs unknown total\n"
            "\n"
            "If the total amount of work is known, provide it. Then the client can render a meaningful fraction such as `40 / 100`.\n"
            "\n"
            "If the total is genuinely unknown, omit it instead of pretending a percentage is exact.\n"
            "\n"
            "### Report useful progress, not noise\n"
            "\n"
            "Sending an update every micro-step can create overhead and noisy UI. The source's example reports progress periodically rather than after every tiny action.\n"
            "\n"
            "[[IMAGE_NEEDED: Long-running tool with progress updates | "
            "A sequence diagram showing Client calling a tool, Server executing in stages, Server sending periodic progress notifications, and finally returning the tool result | "
            "Learner should notice that progress messages improve UX without changing the final result contract]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Manual notifications when server capabilities change\n"
            "\n"
            "A server's tools, prompts, or resources may change at runtime. If clients cache those lists, they need a signal telling them to refresh.\n"
            "\n"
            "The modern helper methods described in the source are:\n"
            "\n"
            "```text\n"
            "notify_tools_changed()\n"
            "notify_prompts_changed()\n"
            "notify_resources_changed()\n"
            "notify_resource_updated(uri)\n"
            "```\n"
            "\n"
            "The first three mean **the list itself changed**. The last one means **one known resource changed**.\n"
            "\n"
            "### Subscriptions/listen model\n"
            "\n"
            "In the modern protocol model described by the chapter, clients opt into change notifications through a `subscriptions/listen` request. "
            "The server publishes change events, and the SDK delivers them to matching listening streams.\n"
            "\n"
            "If no client is listening, publishing a notification does not cause an error—it simply has no recipient.\n"
            "\n"
            "### Server code must announce the change\n"
            "\n"
            "The SDK manages delivery mechanics, but it does not magically know when your business logic changed a tool list or resource. "
            "Your server code is responsible for calling the appropriate notification helper after the mutation.\n"
            "\n"
            "### Legacy compatibility\n"
            "\n"
            "The source also describes older session-level `send_*` notification methods for previous protocol versions. "
            "A server trying to support both old and new clients may need both paths.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Pagination for large discovery lists\n"
            "\n"
            "Pagination lets a server return a large list in manageable pages rather than one enormous response.\n"
            "\n"
            "The source says pagination applies to list operations:\n"
            "\n"
            "- `resources/list`,\n"
            "- `resources/templates/list`,\n"
            "- `prompts/list`,\n"
            "- `tools/list`.\n"
            "\n"
            "It does **not** describe pagination for normal tool calls or resource reads.\n"
            "\n"
            "### Cursor model\n"
            "\n"
            "```text\n"
            "Client requests first page\n"
            "        ↓\n"
            "Server returns items + next_cursor\n"
            "        ↓\n"
            "Client repeats request with cursor\n"
            "        ↓\n"
            "Server returns next page + maybe another cursor\n"
            "        ↓\n"
            "No next_cursor = finished\n"
            "```\n"
            "\n"
            "The cursor should be opaque to the client. Internally, the server may use something as simple as a list index, but the client should only store and return the token.\n"
            "\n"
            "### When pagination is appropriate\n"
            "\n"
            "The source emphasizes that most servers do not need it. If your server exposes hundreds or thousands of tools, for example, pagination may treat a symptom of a deeper interface-design problem.\n"
            "\n"
            "### Why low-level API appears here\n"
            "\n"
            "The high-level API automatically generates primitive-list handlers. To demonstrate custom pagination logic, the source switches to the low-level server API so it can control the list response directly.\n"
            "\n"
            "{{exercise:M03.L02.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Detecting client capabilities\n"
            "\n"
            "A server cannot assume every client supports every optional capability.\n"
            "\n"
            "The chapter explains that client capabilities are available through `ctx.client_capabilities` regardless of whether they came from a legacy initialization handshake or modern per-request metadata.\n"
            "\n"
            "A manual check might conceptually look like:\n"
            "\n"
            "```python\n"
            "if ctx.client_capabilities and ctx.client_capabilities.elicitation:\n"
            "    ...\n"
            "```\n"
            "\n"
            "The context object also provides a capability-check helper.\n"
            "\n"
            "### Why manual checks are not always needed\n"
            "\n"
            "The chapter introduces **resolvers**, which can declare that a tool parameter depends on a capability. If the client does not support the required capability, the SDK can fail the call with a protocol error before the tool body runs.\n"
            "\n"
            "Manual checks remain useful when the capability is optional and you can provide a fallback path.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "If elicitation supported:\n"
            "    ask user which deployment environment to target\n"
            "Else:\n"
            "    use the environment explicitly supplied in the original tool arguments\n"
            "```\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Resolvers: dependency injection before a tool runs\n"
            "\n"
            "Resolvers are one of the most important implementation ideas in this chapter.\n"
            "\n"
            "A resolver computes or obtains a value **before the tool body executes**, and the SDK injects that value into a parameter.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Tool call arrives\n"
            "      ↓\n"
            "SDK examines resolved parameters\n"
            "      ↓\n"
            "Resolver requests external value\n"
            "      ↓\n"
            "SDK validates response\n"
            "      ↓\n"
            "Resolved value injected\n"
            "      ↓\n"
            "Tool body executes\n"
            "```\n"
            "\n"
            "A resolved parameter does not need to appear in the model-visible tool input schema, which is useful when the model should not invent the value itself.\n"
            "\n"
            "### Resolver dependencies\n"
            "\n"
            "The source explains that resolvers can depend on:\n"
            "\n"
            "- ordinary tool arguments by name,\n"
            "- the Context object,\n"
            "- values from other resolvers.\n"
            "\n"
            "The SDK analyzes this dependency graph at registration time, rejects cycles, and ensures a resolver is not redundantly executed multiple times within one tool call.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP resolver dependency flow | "
            "A flow diagram showing model-provided arguments and Context feeding resolvers, resolvers obtaining elicitation/sampling/roots values, and the SDK injecting those results before the tool body runs | "
            "Learner should notice that resolved parameters are not chosen by the model]]\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Elicitations: requesting structured user input\n"
            "\n"
            "Elicitation lets a server workflow request information directly from the user through the client application.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- asking for clarification,\n"
            "- collecting a shipping address,\n"
            "- selecting an option,\n"
            "- confirming a decision,\n"
            "- filling a small form.\n"
            "\n"
            "The server supplies a schema and a message explaining what it needs. The client renders an appropriate UI and obtains consent.\n"
            "\n"
            "### Three outcomes\n"
            "\n"
            "The user can:\n"
            "\n"
            "- **accept** — provide the requested information,\n"
            "- **decline** — explicitly reject the request,\n"
            "- **cancel** — abandon the interaction without an explicit rejection.\n"
            "\n"
            "Your tool should handle all three deliberately.\n"
            "\n"
            "### Form schemas are intentionally limited\n"
            "\n"
            "The source states that elicitation form schemas use a restricted subset of primitive JSON types such as strings, numbers, booleans, and enums. "
            "The SDK converts supported Pydantic fields into the client-facing schema and validates the response structure.\n"
            "\n"
            "That structural validation is not enough by itself. The tool may still need semantic validation:\n"
            "\n"
            "- Is the email actually plausible?\n"
            "- Is the address in a supported delivery region?\n"
            "- Is a numeric value reasonable for the business domain?\n"
            "\n"
            "### Consent-sensitive design\n"
            "\n"
            "The chapter specifically warns against requesting sensitive information casually through form elicitations.\n"
            "\n"
            "### URL mode\n"
            "\n"
            "Some interactions should happen **outside the model/client data path**, such as:\n"
            "\n"
            "- OAuth consent,\n"
            "- payment pages,\n"
            "- password entry.\n"
            "\n"
            "URL elicitation lets the server ask the user to continue in the browser without sending those secrets through the model context.\n"
            "\n"
            "[[IMAGE_NEEDED: Elicitation resolver flow | "
            "A sequence diagram showing tool call → resolver → client UI → user accept/decline/cancel → validated result → tool body | "
            "Learner should notice that user input is injected by the SDK rather than filled by the model]]\n"
            "\n"
            "{{exercise:M03.L02.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 11. Sampling: legacy access to the client's LLM\n"
            "\n"
            "Sampling allows a server to request a model completion from the client application's LLM.\n"
            "\n"
            "This can support workflows such as:\n"
            "\n"
            "- asking the model to explain a computed result,\n"
            "- using the model for classification inside a tool workflow,\n"
            "- planning a set of server-side steps,\n"
            "- transforming intermediate data.\n"
            "\n"
            "### Deprecation warning\n"
            "\n"
            "The source explicitly states that sampling was deprecated in the 2026-07-28 specification revision and recommends that new servers integrate directly with an LLM provider instead of borrowing the client's model.\n"
            "\n"
            "You should therefore study sampling mainly to understand existing/legacy systems and resolver patterns.\n"
            "\n"
            "### Human-in-the-loop expectation\n"
            "\n"
            "A client is expected to ask the user for approval before allowing an external server to spend model resources or inject a server-generated prompt into the user's model session.\n"
            "\n"
            "The server must therefore be prepared for rejection.\n"
            "\n"
            "### Sampling result\n"
            "\n"
            "The returned result may contain text, image, or audio content and identifies which model was used and why generation stopped.\n"
            "\n"
            "Your server should validate the returned content type rather than assuming text.\n"
            "\n"
            "### Model preferences are hints, not commands\n"
            "\n"
            "The source describes model preferences such as:\n"
            "\n"
            "- cost priority,\n"
            "- speed priority,\n"
            "- intelligence priority,\n"
            "- model-family hints.\n"
            "\n"
            "The client is not required to follow them exactly. The server should not make correctness depend on receiving one particular model.\n"
            "\n"
            "### Prompt injection still matters\n"
            "\n"
            "If tool arguments are inserted into the sampling prompt, validate them just as you would validate dynamic SQL parameters or other untrusted input. "
            "Overly strict validation can reduce usefulness, so the goal is a sensible balance between security and flexibility.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. Roots: filesystem coordination, not filesystem security\n"
            "\n"
            "Roots let a client communicate filesystem locations that a server is intended to work within.\n"
            "\n"
            "A client might expose a project directory through a directory picker, allowing a local server to know which workspace the user intends it to use.\n"
            "\n"
            "### Deprecation warning\n"
            "\n"
            "The source states that roots were deprecated in the 2026-07-28 revision. New servers should instead consider paths in tool arguments, resource URIs, or server configuration.\n"
            "\n"
            "### The most important roots rule\n"
            "\n"
            "**Roots are not a security boundary.**\n"
            "\n"
            "A local server process still runs with the operating-system permissions available to that process. A malicious or buggy server can ignore a declared root unless another enforcement mechanism prevents access.\n"
            "\n"
            "Actual boundaries come from things such as:\n"
            "\n"
            "- whether the user installs/runs the server at all,\n"
            "- process sandboxing,\n"
            "- OS permissions,\n"
            "- container/VM isolation,\n"
            "- application-level access controls.\n"
            "\n"
            "### Correct path validation\n"
            "\n"
            "For compatibility with legacy roots, the source demonstrates a safer path check:\n"
            "\n"
            "1. Resolve the requested path to normalize `..` segments and symlinks.\n"
            "2. Decode the file URI into an operating-system path.\n"
            "3. Resolve the root path too.\n"
            "4. Use a path-aware containment check such as `is_relative_to()`.\n"
            "\n"
            "Do **not** rely on naive string-prefix checks, because paths with similar prefixes can bypass them.\n"
            "\n"
            "### Locality limitation\n"
            "\n"
            "The source notes that a server generally manipulates files on the machine where the server itself runs; the SDK does not magically provide remote access to a client's filesystem.\n"
            "\n"
            "[[IMAGE_NEEDED: Roots coordination versus real sandboxing | "
            "A diagram showing a client-declared root passed to a local server, plus a separate true sandbox/OS-permission boundary around the server process | "
            "Learner should notice that roots describe intended scope but the sandbox enforces actual scope]]\n"
            "\n"
            "---\n"
            "\n"
            "## 13. Request cancellation and graceful cleanup\n"
            "\n"
            "Long-running operations need a way for the user to stop them.\n"
            "\n"
            "The chapter explains that cancellation behavior differs by transport and protocol version, but the Python SDK normalizes most of the handling.\n"
            "\n"
            "### stdio\n"
            "\n"
            "The client sends a cancellation notification identifying the request to stop.\n"
            "\n"
            "### Modern Streamable HTTP\n"
            "\n"
            "A per-request stream can be closed, and the SDK interprets that disconnection as cancellation of the associated running handler.\n"
            "\n"
            "### The universal server-side lesson\n"
            "\n"
            "Regardless of transport, cancellation ultimately appears to the running handler as cancellation of its task. Therefore, cleanup belongs inside the operation itself.\n"
            "\n"
            "A robust pattern is:\n"
            "\n"
            "```python\n"
            "try:\n"
            "    await do_long_running_work()\n"
            "finally:\n"
            "    await release_resources()\n"
            "```\n"
            "\n"
            "or, when you need specific cancellation logging:\n"
            "\n"
            "```python\n"
            "try:\n"
            "    await do_long_running_work()\n"
            "except anyio.get_cancelled_exc_class():\n"
            "    logger.info('Operation cancelled; cleaning up')\n"
            "    raise\n"
            "```\n"
            "\n"
            "### Why re-raise?\n"
            "\n"
            "Cancellation is control flow, not an ordinary recoverable business error. After cleanup, re-raising preserves the cancellation signal so the framework can finish terminating the request correctly.\n"
            "\n"
            "### Optional notification handler\n"
            "\n"
            "A separate cancellation-notification handler can provide metadata such as the request ID and client-supplied reason when that notification is available. "
            "It is useful for observability, but the source emphasizes that the SDK already performs the actual cancellation.\n"
            "\n"
            "### What graceful cancellation should do\n"
            "\n"
            "- stop work quickly,\n"
            "- release locks/files/network resources,\n"
            "- roll back partial state if appropriate,\n"
            "- avoid committing an incomplete action,\n"
            "- log useful context,\n"
            "- never swallow the cancellation unintentionally.\n"
            "\n"
            "{{exercise:M03.L02.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## 14. Putting the chapter together: designing a mature MCP server\n"
            "\n"
            "The real value of these features appears when they work together.\n"
            "\n"
            "Consider a long-running deployment-analysis tool:\n"
            "\n"
            "```text\n"
            "1. Client calls deployment_analysis(...)\n"
            "2. Resolver may elicit environment selection from user\n"
            "3. Tool starts work\n"
            "4. Context reports progress periodically\n"
            "5. Tool reads lifespan-managed database/cache state\n"
            "6. Resource data may change\n"
            "7. Server emits resource update notification\n"
            "8. Client may cancel the operation\n"
            "9. Tool cleanup runs\n"
            "10. Final result returns if not cancelled\n"
            "```\n"
            "\n"
            "This illustrates an important shift: advanced MCP server development is not about adding isolated protocol tricks. "
            "It is about creating an interaction that remains understandable, safe, responsive, and recoverable across the full request lifecycle.\n"
            "\n"
            "### Practical design rules from the chapter\n"
            "\n"
            "- Use completions only when they genuinely improve input UX.\n"
            "- Treat `Context` as the main bridge to request/session/server state.\n"
            "- Prefer normal server logging for new systems rather than deprecated protocol logging.\n"
            "- Report progress for genuinely long operations.\n"
            "- Notify clients when your dynamic primitive/resource state changes.\n"
            "- Paginate only when the list is truly large.\n"
            "- Never assume optional client capabilities are present.\n"
            "- Use resolvers to keep user/client-derived values out of the model-controlled schema.\n"
            "- Handle decline/cancel paths as first-class outcomes.\n"
            "- Treat deprecated sampling/roots as compatibility concepts, not default new-server architecture.\n"
            "- Always make long-running work cancellation-safe.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'Completions are model completions.'\n"
            "\n"
            "**Why this is wrong:** in this chapter, completions mean autocomplete suggestions for prompt/resource-template arguments.\n"
            "\n"
            "### Misconception 2: 'The Context object is part of the MCP specification.'\n"
            "\n"
            "**Why this is wrong:** the source presents it as a convenience abstraction from the Python SDK.\n"
            "\n"
            "### Misconception 3: 'Protocol-level logging is the preferred modern logging approach.'\n"
            "\n"
            "**Why this is wrong:** the source states that in-protocol logging is deprecated and recommends ordinary Python logging for new servers.\n"
            "\n"
            "### Misconception 4: 'The SDK automatically announces every runtime change to clients.'\n"
            "\n"
            "**Why this is wrong:** your server code must explicitly call the appropriate change-notification helper.\n"
            "\n"
            "### Misconception 5: 'Everything can be paginated.'\n"
            "\n"
            "**Why this is wrong:** the chapter limits pagination to list operations such as tools/list and resources/list.\n"
            "\n"
            "### Misconception 6: 'If the client lacks a resolver capability, the tool can always run normally.'\n"
            "\n"
            "**Why this is wrong:** a required resolver capability can cause the SDK to reject the operation before the tool body executes.\n"
            "\n"
            "### Misconception 7: 'Elicitation values should be filled by the model.'\n"
            "\n"
            "**Why this is wrong:** a resolver obtains the value from the user/client and injects it outside the model-visible tool argument schema.\n"
            "\n"
            "### Misconception 8: 'Roots secure the host filesystem.'\n"
            "\n"
            "**Why this is wrong:** roots express intended scope but do not enforce OS-level access.\n"
            "\n"
            "### Misconception 9: 'A server can require the client's exact preferred model for sampling.'\n"
            "\n"
            "**Why this is wrong:** model preferences are hints, and the client may choose differently.\n"
            "\n"
            "### Misconception 10: 'Cancellation is just another error to catch and ignore.'\n"
            "\n"
            "**Why this is wrong:** cancellation is control flow. The handler should clean up and normally re-raise the cancellation signal.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Completion | Server-provided autocomplete suggestion for a prompt or resource-template argument |\n"
            "| `CompletionContext` | Optional prior-argument information available to a completion handler |\n"
            "| Icon | Server or primitive metadata that a client may display in its UI |\n"
            "| `Context` | Python SDK object giving handlers access to server, session, request, capability, logging, progress, and notification information |\n"
            "| `ServerSession` | Lower-level session interface used by the server to communicate with the connected client |\n"
            "| Request context | Per-request state including request ID, metadata, method/params, lifespan state, and session |\n"
            "| Protocol logging | Legacy MCP logging notifications sent from server to client |\n"
            "| Progress notification | Server update communicating how far a long-running operation has progressed |\n"
            "| Primitive list notification | Signal that tools, prompts, or resources available from the server have changed |\n"
            "| Resource update notification | Signal that the content behind one resource URI has changed |\n"
            "| Pagination | Splitting a large list operation into multiple cursor-based pages |\n"
            "| Cursor | Opaque token identifying where the next page should continue |\n"
            "| Client capability | Optional feature that a connected client declares it can provide |\n"
            "| Resolver | SDK mechanism that obtains/injects a value before a tool body executes |\n"
            "| Elicitation | Request for structured user input or browser-based continuation through the client |\n"
            "| Accepted elicitation | User approved and supplied the requested information |\n"
            "| Declined elicitation | User explicitly rejected the request |\n"
            "| Cancelled elicitation | User abandoned the interaction without explicit approval/decline |\n"
            "| Sampling | Deprecated capability allowing a server to request use of the client's LLM |\n"
            "| Model preferences | Sampling hints about model family and tradeoffs such as cost/speed/intelligence |\n"
            "| Roots | Deprecated capability describing filesystem locations the client intends a server to use |\n"
            "| Cancellation | Mechanism for stopping an in-flight request and triggering server cleanup |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are server utilities, and how do they differ from MCP primitives?\n"
            "2. What can a completion handler autocomplete?\n"
            "3. What information can `CompletionContext` provide?\n"
            "4. What major categories of information are accessible through `Context`?\n"
            "5. Why is ordinary Python logging preferred for new servers in the source?\n"
            "6. When should a server send progress updates?\n"
            "7. What is the difference between `notify_resources_changed()` and `notify_resource_updated(uri)`?\n"
            "8. Which operations support pagination according to the chapter?\n"
            "9. Why should cursors be opaque to clients?\n"
            "10. How does a server determine whether a client supports elicitation or sampling?\n"
            "11. What does a resolver do before the tool body executes?\n"
            "12. Why can a resolved parameter be omitted from the model-facing tool schema?\n"
            "13. What are the three possible elicitation outcomes?\n"
            "14. Why should OAuth/password/payment flows use URL mode rather than form elicitation?\n"
            "15. What does HITL mean in a sampling flow?\n"
            "16. Why should a new server avoid depending on sampling?\n"
            "17. Why are model preferences only hints?\n"
            "18. Why are roots not a real security boundary?\n"
            "19. Why should paths be resolved before checking whether they are inside a root?\n"
            "20. How does cancellation differ between stdio and modern Streamable HTTP?\n"
            "21. Why should cancellation cleanup live inside the running tool/handler?\n"
            "22. Why should a cancellation exception normally be re-raised after cleanup?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Advanced MCP server engineering is lifecycle engineering: help users enter good inputs, understand request context, communicate progress and change, "
            "scale large lists, safely obtain external input when required, and ensure every long-running operation can be stopped and cleaned up correctly.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "advanced-server-overview", "title": "From primitives to complete servers", "order": 1},
            {"id": "completions", "title": "Completions", "order": 2},
            {"id": "icons-context", "title": "Icons and the Context object", "order": 3},
            {"id": "logging", "title": "Logging", "order": 4},
            {"id": "progress-notifications", "title": "Progress reporting", "order": 5},
            {"id": "primitive-notifications", "title": "Primitive and resource notifications", "order": 6},
            {"id": "pagination", "title": "Pagination", "order": 7},
            {"id": "client-capability-detection", "title": "Detecting client capabilities", "order": 8},
            {"id": "resolvers", "title": "Resolvers", "order": 9},
            {"id": "elicitation", "title": "Elicitations", "order": 10},
            {"id": "sampling", "title": "Sampling", "order": 11},
            {"id": "roots", "title": "Roots", "order": 12},
            {"id": "cancellation", "title": "Request cancellation", "order": 13},
            {"id": "integration-patterns", "title": "Putting the chapter together", "order": 14},
        ],
    },

    "exercises": [
        {
            "id": "M03.L02.EX01",

            "title": "Design a Completion Handler",

            "lesson_code": "M03.L02",

            "section_id": "completions",

            "placement": "after_section",

            "description": (
                "Design context-aware autocompletion for a prompt or resource template "
                "without leaking sensitive information or flooding the client."
            ),

            "instructions": (
                "Your server exposes a deployment prompt with arguments environment and service.\n\n"
                "1. Define at least four valid environment suggestions.\n"
                "2. Explain how the current partial argument should filter suggestions.\n"
                "3. Explain how the already-selected service could affect environment suggestions.\n"
                "4. Decide how to enforce the 100-value limit.\n"
                "5. Add one rate-limiting rule.\n"
                "6. List two values that should never be exposed as autocomplete suggestions.\n"
                "7. Explain how total and has_more should behave if more suggestions exist than can be returned."
            ),

            "expected_output": (
                "A completion-handler design with filtering logic, context use, limit handling, "
                "rate limiting, and sensitive-data safeguards."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "completions",
                "input-validation",
                "server-ux",
                "rate-limiting",
            ],
        },

        {
            "id": "M03.L02.EX02",

            "title": "Paginate a Large Resource Catalog",

            "lesson_code": "M03.L02",

            "section_id": "pagination",

            "placement": "after_section",

            "description": (
                "Practice designing an opaque cursor and page flow for a server with "
                "a genuinely large resource list."
            ),

            "instructions": (
                "Your server exposes 2,400 resource metadata entries through resources/list and returns 120 per page.\n\n"
                "1. Describe the first response, including next_cursor.\n"
                "2. Explain what the client sends for the second page.\n"
                "3. Calculate how many pages exist.\n"
                "4. State what the server returns on the final page to indicate completion.\n"
                "5. Explain why the cursor should be treated as opaque by the client.\n"
                "6. Explain why this same pagination design should not be copied blindly into a tools/call result."
            ),

            "expected_output": (
                "A page-flow description including cursor lifecycle, page count, termination behavior, "
                "and explanation of why pagination is limited to discovery/list operations."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "pagination",
                "cursor-design",
                "large-result-handling",
            ],
        },

        {
            "id": "M03.L02.EX03",

            "title": "Design a Safe Elicitation Resolver",

            "lesson_code": "M03.L02",

            "section_id": "elicitation",

            "placement": "after_section",

            "description": (
                "Design a resolver that gathers user input safely and handles consent outcomes explicitly."
            ),

            "instructions": (
                "Build the design for a tool that books a support call and needs the user's name, preferred time, "
                "and contact email.\n\n"
                "1. Define the elicitation schema using only appropriate primitive field types.\n"
                "2. Identify which fields are required and which are optional.\n"
                "3. Define semantic validation beyond structural schema validation.\n"
                "4. Explain what the tool should do on accept, decline, and cancel.\n"
                "5. Explain why the resolved values should not appear in the model-controlled tool schema.\n"
                "6. Identify one piece of information that should instead use a URL flow or another secure channel.\n"
                "7. Explain what happens if the connected client does not support elicitation."
            ),

            "expected_output": (
                "An elicitation schema and resolver flow including validation, consent branches, "
                "capability failure behavior, and data-sensitivity reasoning."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "elicitation",
                "resolvers",
                "hitl",
                "schema-validation",
                "privacy",
            ],
        },

        {
            "id": "M03.L02.EX04",

            "title": "Make a Long-Running Tool Cancellation-Safe",

            "lesson_code": "M03.L02",

            "section_id": "cancellation",

            "placement": "after_section",

            "description": (
                "Design a long-running operation that reports progress but remains safe if the user cancels midway."
            ),

            "instructions": (
                "A tool processes 10,000 files and writes results to a temporary workspace before publishing a final report.\n\n"
                "1. Decide how often progress should be reported.\n"
                "2. Identify resources that need cleanup if cancellation occurs.\n"
                "3. Show a try/finally or cancellation-exception pseudocode structure.\n"
                "4. Explain why the cancellation exception should be re-raised.\n"
                "5. Explain how stdio and modern Streamable HTTP may signal cancellation differently.\n"
                "6. Decide what information should be logged when cancellation occurs.\n"
                "7. Explain how to avoid publishing a partially completed report."
            ),

            "expected_output": (
                "A cancellation-safe tool design with progress cadence, cleanup plan, exception flow, "
                "transport notes, and partial-state protection."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "cancellation",
                "progress-reporting",
                "cleanup",
                "reliability",
            ],
        },
    ],

    "quiz": {
        "id": "M03.L02.QZ01",

        "title": "Advanced MCP Servers — Knowledge Check",

        "lesson_code": "M03.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L02.Q01",

                "section_id": "completions",

                "question": "What does an MCP completion handler provide in this chapter?",

                "options": [
                    "A full LLM answer to the user",
                    "Autocomplete suggestions for prompt or resource-template arguments",
                    "A list of server OAuth tokens",
                    "Automatic tool execution",
                ],

                "correct": 1,

                "explanation": (
                    "Completions in this chapter are autocomplete suggestions used while filling "
                    "prompt or resource-template arguments."
                ),
            },

            {
                "id": "M03.L02.Q02",

                "section_id": "icons-context",

                "question": "What is the Python SDK Context object mainly used for?",

                "options": [
                    "Training the connected LLM",
                    "Accessing server/session/request information and helpers inside handlers",
                    "Replacing all tool parameters",
                    "Storing client passwords",
                ],

                "correct": 1,

                "explanation": (
                    "Context gives handlers access to server configuration, client/session information, "
                    "request state, lifespan data, progress helpers, and notifications."
                ),
            },

            {
                "id": "M03.L02.Q03",

                "section_id": "logging",

                "question": "What does the supplied chapter recommend for new server logging after the 2026-07-28 deprecation?",

                "options": [
                    "Only protocol-level client logging",
                    "Ordinary Python/server logging rather than deprecated MCP logging notifications",
                    "No logging at all",
                    "Embedding logs into tool descriptions",
                ],

                "correct": 1,

                "explanation": (
                    "The source states that protocol-level logging is deprecated and recommends "
                    "normal Python logging for new servers."
                ),
            },

            {
                "id": "M03.L02.Q04",

                "section_id": "primitive-notifications",

                "question": "Which helper indicates that the content of one known resource has changed?",

                "options": [
                    "notify_resources_changed()",
                    "notify_resource_updated(uri)",
                    "notify_tools_changed()",
                    "notify_prompts_changed()",
                ],

                "correct": 1,

                "explanation": (
                    "notify_resource_updated(uri) targets one resource. notify_resources_changed() "
                    "means the available resource list itself changed."
                ),
            },

            {
                "id": "M03.L02.Q05",

                "section_id": "pagination",

                "question": "Which operation is described as supporting MCP pagination?",

                "options": [
                    "tools/call",
                    "resources/read",
                    "tools/list",
                    "sampling/createMessage",
                ],

                "correct": 2,

                "explanation": (
                    "The source limits pagination to primitive/resource list operations such as tools/list."
                ),
            },

            {
                "id": "M03.L02.Q06",

                "section_id": "resolvers",

                "question": "What is the key purpose of a resolver in the chapter's Python SDK pattern?",

                "options": [
                    "To let the model invent hidden tool parameters",
                    "To obtain and inject a value before the tool body executes",
                    "To paginate tool results",
                    "To replace the MCP server transport",
                ],

                "correct": 1,

                "explanation": (
                    "Resolvers compute or request values before execution and the SDK injects them "
                    "into parameters outside the normal model-controlled input path."
                ),
            },

            {
                "id": "M03.L02.Q07",

                "section_id": "elicitation",

                "question": "Which set contains the three elicitation outcomes described by the source?",

                "options": [
                    "approve, retry, timeout",
                    "accept, decline, cancel",
                    "read, write, delete",
                    "allow, deny, refresh",
                ],

                "correct": 1,

                "explanation": (
                    "An elicitation may be accepted with data, explicitly declined, or cancelled."
                ),
            },

            {
                "id": "M03.L02.Q08",

                "section_id": "sampling",

                "question": "What is the chapter's modern recommendation regarding sampling for new servers?",

                "options": [
                    "Every new server should require sampling.",
                    "Sampling should replace all prompts.",
                    "New servers should prefer direct LLM-provider integration because sampling is deprecated.",
                    "Sampling is the only way to use an LLM in a server.",
                ],

                "correct": 2,

                "explanation": (
                    "The source marks sampling as deprecated and recommends direct provider integration "
                    "for new server designs."
                ),
            },

            {
                "id": "M03.L02.Q09",

                "section_id": "roots",

                "question": "Why must roots not be treated as a filesystem security boundary?",

                "options": [
                    "Roots contain only HTTP URLs.",
                    "Servers are not technically forced to respect them; real enforcement comes from sandboxing/permissions.",
                    "Roots cannot identify directories.",
                    "Roots work only with remote files.",
                ],

                "correct": 1,

                "explanation": (
                    "Roots describe intended scope, but a local process still has whatever OS-level "
                    "permissions it was launched with."
                ),
            },

            {
                "id": "M03.L02.Q10",

                "section_id": "cancellation",

                "question": "What should a handler usually do after performing cleanup for a cancellation exception?",

                "options": [
                    "Silently continue the operation",
                    "Convert cancellation into a successful result",
                    "Re-raise the cancellation signal",
                    "Restart the server",
                ],

                "correct": 2,

                "explanation": (
                    "Re-raising preserves cancellation control flow so the SDK/framework can terminate "
                    "the request correctly after cleanup."
                ),
            },

            {
                "id": "M03.L02.Q11",

                "section_id": "integration-patterns",

                "question": "Which design best reflects the chapter's overall guidance?",

                "options": [
                    "Use every available utility and client capability in every server.",
                    "Use utilities selectively to improve UX/reliability and treat deprecated capabilities mainly as compatibility features.",
                    "Avoid progress and cancellation because they complicate tools.",
                    "Require every client to support sampling, roots, and elicitation.",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter presents these features as tools to use deliberately, with special "
                    "care around deprecated and optional capabilities."
                ),
            },

            {
                "id": "M03.L02.Q12",

                "section_id": "integration-patterns",

                "type": "open",

                "question": (
                    "Design an advanced MCP server tool that performs a long-running deployment review. "
                    "Explain how you would use Context, progress reporting, capability detection, an optional "
                    "elicitation resolver, notifications, logging, and cancellation cleanup. Also explain which "
                    "deprecated capabilities you would avoid in a new implementation and why."
                ),
            },
        ],

        "passing_score": 70,
    },
}
