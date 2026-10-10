"""M04.L01 — Connecting Clients and Servers: MCP Transports.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 8 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "MCP Transport Layer"

MODULE_DESCRIPTION = (
    "Understand MCP below the client/server API surface: JSON-RPC message shapes, "
    "session dispatch and concurrency, stdio and Streamable HTTP transports, legacy "
    "SSE, custom transport contracts, transport security, and transport selection."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Connecting Clients and Servers: MCP Transports",

    "slug": "ai-agents-mcp-m04-l01",

    "description": (
        "A deep technical lesson on MCP's data, session, and transport layers. "
        "Learn how JSON-RPC requests, responses, errors, and notifications flow through "
        "ClientSession/ServerSession, how stdio and Streamable HTTP frame and move messages, "
        "how cancellation and progress work, how custom transports satisfy the SDK contract, "
        "and how transport choice changes the security model."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.5,

    "skill_tags": [
        "mcp",
        "json-rpc",
        "transport-layer",
        "session-layer",
        "dispatcher",
        "stdio",
        "streamable-http",
        "sse",
        "custom-transports",
        "concurrency",
        "message-framing",
        "cancellation",
        "progress",
        "transport-security",
    ],

    "prerequisite_ids": ["M03.L03"],

    "lesson": {
        "title": "Connecting Clients and Servers: MCP Transports",

        "content": (
            "# Connecting Clients and Servers: MCP Transports\n"
            "\n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** MCP Transport Layer  \n"
            "> **Source alignment:** Chapter 8 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the relationship among the application, protocol/session, transport, and network layers.\n"
            "- Describe MCP's JSON-RPC request, result-response, error-response, and notification messages.\n"
            "- Distinguish transport-layer, protocol-layer, and application-layer failures.\n"
            "- Explain how progress and cancellation notifications correlate with existing requests.\n"
            "- Explain the cost of Base64 binary transport and when resource links are preferable.\n"
            "- Describe what `ClientSession`, `ServerSession`, and the JSON-RPC dispatcher do.\n"
            "- Explain request IDs, pending-response tables, in-flight requests, task groups, and cancel scopes.\n"
            "- Distinguish connection establishment from legacy protocol initialization.\n"
            "- Explain how stdio starts, frames, sends, receives, and closes a local MCP connection.\n"
            "- Explain why stdout discipline matters for stdio servers.\n"
            "- Explain the modern Streamable HTTP lifecycle and why it is stateless.\n"
            "- Compare JSON and per-request SSE responses in Streamable HTTP.\n"
            "- Explain modern `input_required` follow-up behavior and `subscriptions/listen`.\n"
            "- Explain why the original HTTP SSE transport was deprecated.\n"
            "- Describe the implicit Python SDK contract a custom transport must fulfill.\n"
            "- Threat-model stdio and Streamable HTTP separately.\n"
            "- Choose an appropriate transport for local, development, remote, and horizontally scalable deployments.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Where the transport layer fits in MCP\n"
            "\n"
            "Most MCP application code works at a high level: `call_tool()`, `list_resources()`, `get_prompt()`, and similar SDK methods. "
            "Those methods hide several layers underneath.\n"
            "\n"
            "A useful stack is:\n"
            "\n"
            "```text\n"
            "Host application / MCP server code\n"
            "              ↓\n"
            "MCP protocol objects and handlers\n"
            "              ↓\n"
            "ClientSession / ServerSession + dispatcher\n"
            "              ↓\n"
            "Transport\n"
            "              ↓\n"
            "Process pipes / HTTP / custom wire\n"
            "```\n"
            "\n"
            "The protocol defines **what messages mean and how they are shaped**. The transport defines **how those messages travel**.\n"
            "\n"
            "This separation is why the same client/server logic can work over local stdio, remote Streamable HTTP, or a custom transport without rewriting the application itself.\n"
            "\n"
            '{{image:mcp-abstraction-stack}}'
            '\n'
            "\n"
            "### The transport's responsibilities\n"
            "\n"
            "Regardless of implementation, a transport must handle concerns such as:\n"
            "\n"
            "- establishing communication,\n"
            "- serializing/deserializing messages,\n"
            "- framing/deframing messages,\n"
            "- moving bytes over the underlying medium,\n"
            "- surfacing connection errors/timeouts,\n"
            "- closing and cleaning up.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. JSON-RPC: the MCP data layer\n"
            "\n"
            "MCP uses JSON-RPC 2.0 as the message-exchange foundation. JSON-RPC is intentionally small: messages are JSON objects that represent remote procedure calls, their results, failures, and one-way notifications.\n"
            "\n"
            "The chapter treats these messages as MCP's **data layer**.\n"
            "\n"
            "### Important MCP-specific notes\n"
            "\n"
            "The supplied source highlights two protocol-version details:\n"
            "\n"
            "- MCP requires non-null request IDs so responses can be correlated with requests.\n"
            "- JSON-RPC batching existed in the base JSON-RPC specification, but MCP removed batch support in the 2025-06-18 protocol revision described by the source.\n"
            "\n"
            "### Four message families to understand\n"
            "\n"
            "```text\n"
            "Request      → asks the peer to do something and expects a response\n"
            "Result       → successful response to a request\n"
            "Error        → protocol-level failure response to a request\n"
            "Notification → one-way message; no response expected\n"
            "```\n"
            "\n"
            "These few shapes are enough to express all the higher-level MCP methods you have already used.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Request messages\n"
            "\n"
            "A request initiates an operation that expects a response.\n"
            "\n"
            "Its core shape is:\n"
            "\n"
            "```json\n"
            "{\n"
            '  "jsonrpc": "2.0",\n'
            '  "id": 3,\n'
            '  "method": "tools/call",\n'
            '  "params": {\n'
            '    "name": "calculate_gpa",\n'
            '    "arguments": {\n'
            '      "grades": [98, 94, 100, 34],\n'
            '      "weighted": false\n'
            "    }\n"
            "  }\n"
            "}\n"
            "```\n"
            "\n"
            "### Required ideas\n"
            "\n"
            "- `jsonrpc` identifies JSON-RPC version 2.0.\n"
            "- `id` correlates this request with its eventual response.\n"
            "- `method` selects the MCP operation, such as `tools/list` or `tools/call`.\n"
            "- `params` contains parameters for the **MCP operation**.\n"
            "\n"
            "### Do not confuse operation parameters with tool arguments\n"
            "\n"
            "In `tools/call`, the top-level `params` object contains the tool name and an `arguments` object. "
            "The function arguments live inside that nested `arguments` object.\n"
            "\n"
            "```text\n"
            "params                 ← parameters for tools/call\n"
            "├── name               ← which tool\n"
            "└── arguments          ← arguments for the Python/tool function\n"
            "```\n"
            "\n"
            "This distinction matters when debugging malformed requests.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Result responses, protocol errors, and application errors\n"
            "\n"
            "A successful request receives a result response whose `id` matches the initiating request.\n"
            "\n"
            "```json\n"
            "{\n"
            '  "jsonrpc": "2.0",\n'
            '  "id": 3,\n'
            '  "result": {\n'
            '    "content": [{"type": "text", "text": "Your GPA is 3.25"}],\n'
            '    "isError": false\n'
            "  }\n"
            "}\n"
            "```\n"
            "\n"
            "### Structured tool output\n"
            "\n"
            "A tool result may also contain `structuredContent`: a JSON object that gives clients a predictable machine-readable representation alongside the required content blocks.\n"
            "\n"
            "### Result type and multi-round-trip behavior\n"
            "\n"
            "The source notes that modern result objects can identify whether they are complete or whether more input is required. "
            "An `input_required` result lets the server communicate that the client must supply additional information before the larger operation can finish.\n"
            "\n"
            "### Protocol-level error response\n"
            "\n"
            "Malformed protocol usage returns an error object:\n"
            "\n"
            "```json\n"
            "{\n"
            '  "jsonrpc": "2.0",\n'
            '  "id": 3,\n'
            '  "error": {\n'
            '    "code": -32602,\n'
            '    "message": "Invalid parameters"\n'
            "  }\n"
            "}\n"
            "```\n"
            "\n"
            "The source distinguishes three failure layers:\n"
            "\n"
            "| Layer | Example | How it surfaces |\n"
            "|---|---|---|\n"
            "| Transport | Network/process connection fails | Connection failure/exception |\n"
            "| Protocol | Invalid MCP method parameters | JSON-RPC error response |\n"
            "| Application | Tool function raises a recoverable/business error | Result response with `isError=true` and useful content |\n"
            "\n"
            "This separation is critical for debugging. A network timeout is not the same thing as a valid MCP request whose tool returns an application error.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP error layers | "
            "A three-layer diagram for transport, protocol, and application errors, with each layer mapped to connection exception, JSON-RPC error response, or isError tool result | "
            "Learner should notice that not every failure is encoded in the same message type]]\n"
            "\n"
            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Notifications: one-way messages\n"
            "\n"
            "A notification communicates information without asking the receiver to send a response.\n"
            "\n"
            "Because no response will ever need to correlate back to it, a notification has **no request ID**.\n"
            "\n"
            "Example shape:\n"
            "\n"
            "```json\n"
            "{\n"
            '  "jsonrpc": "2.0",\n'
            '  "method": "notifications/prompts/list_changed"\n'
            "}\n"
            "```\n"
            "\n"
            "Notifications are useful for events such as:\n"
            "\n"
            "- primitive-list changes,\n"
            "- resource changes,\n"
            "- progress updates,\n"
            "- legacy cancellation messages.\n"
            "\n"
            "The receiver must not reply to a notification.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Progress and cancellation at the message level\n"
            "\n"
            "### Progress\n"
            "\n"
            "A requester can include a `progressToken` in request metadata. Progress notifications sent during that operation copy the same token, giving the receiver a way to route each progress event to the correct in-flight request/UI callback.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Request id=4, progressToken=P123\n"
            "      ↓\n"
            "progress(P123, 20/100)\n"
            "progress(P123, 50/100)\n"
            "progress(P123, 90/100)\n"
            "      ↓\n"
            "Result id=4\n"
            "```\n"
            "\n"
            "Progress is optional. The source recommends both peers rate-limit progress traffic to avoid overwhelming one another.\n"
            "\n"
            "### Cancellation\n"
            "\n"
            "Older/stdio-style cancellation can use a one-way notification carrying the request ID and optional reason.\n"
            "\n"
            "A receiver should stop the matching operation if it is still running and release resources.\n"
            "\n"
            "### Race conditions\n"
            "\n"
            "Cancellation can race with completion. A result may be sent just before the cancellation reaches the receiver. "
            "The requester should be able to ignore a late result, and the receiver should not treat a cancellation of an already-finished request as a fatal error.\n"
            "\n"
            "### Modern Streamable HTTP difference\n"
            "\n"
            "The source states that for modern Streamable HTTP, client cancellation is achieved by aborting the in-flight POST request rather than sending a client-originated cancellation notification.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Text, binary data, and resource links\n"
            "\n"
            "MCP content blocks can carry text and binary-oriented types such as image or audio content.\n"
            "\n"
            "### Base64 overhead\n"
            "\n"
            "Binary data encoded directly into JSON is transmitted as Base64. The chapter points out the familiar cost: every 3 bytes become roughly 4 ASCII bytes—about **33% size overhead**.\n"
            "\n"
            "That makes direct message embedding increasingly unattractive for large payloads.\n"
            "\n"
            "### Resource links as an alternative\n"
            "\n"
            "A `ResourceLink` describes data without embedding the data blob itself.\n"
            "\n"
            "Benefits include:\n"
            "\n"
            "- **lazy loading** — fetch only when needed,\n"
            "- **out-of-band retrieval** — the application may follow the URI outside the primary MCP payload,\n"
            "- **context savings** — metadata can inform the model without injecting the entire file into the context window.\n"
            "\n"
            "For large data, the source notes that HTTP URLs are becoming a common URI pattern.\n"
            "\n"
            "### Practical message-size discipline\n"
            "\n"
            "The protocol does not define one universal message-size limit, while platforms may impose their own. "
            "The source therefore recommends keeping messages relatively small and using patterns such as pagination or resource links when data grows large.\n"
            "\n"
            "[[IMAGE_NEEDED: Embedded binary versus ResourceLink | "
            "A comparison showing image bytes Base64-encoded inside a JSON-RPC payload versus a lightweight resource link containing URI/metadata and deferred retrieval | "
            "Learner should notice the payload and context savings of lazy/out-of-band loading]]\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Session objects: the boundary above the transport\n"
            "\n"
            "The Python SDK uses session objects as the stable interface between MCP application code and the underlying transport.\n"
            "\n"
            "- `ClientSession` is used on the client side.\n"
            "- `ServerSession` is used on the server side/request path.\n"
            "\n"
            "A high-level call such as `call_tool()` eventually becomes a JSON-RPC request that is sent through a session-managed write stream.\n"
            "\n"
            "### Sending path\n"
            "\n"
            "```text\n"
            "Application calls call_tool()\n"
            "        ↓\n"
            "Session constructs JSON-RPC request\n"
            "        ↓\n"
            "Dispatcher assigns/registers request ID\n"
            "        ↓\n"
            "SessionMessage written to in-memory write stream\n"
            "        ↓\n"
            "Transport serializes/frames/sends it\n"
            "```\n"
            "\n"
            "### Receiving path\n"
            "\n"
            "```text\n"
            "Transport receives bytes\n"
            "        ↓\n"
            "Deframe + validate JSON-RPC\n"
            "        ↓\n"
            "SessionMessage placed on read stream\n"
            "        ↓\n"
            "Dispatcher routes by message type\n"
            "```\n"
            "\n"
            "This is the key abstraction: sessions care about MCP message semantics; transports care about moving those messages over the wire.\n"
            "\n"
            "[[IMAGE_NEEDED: Session and transport message flow | "
            "A sequence diagram showing Host → ClientSession → dispatcher → in-memory write stream → transport → wire → server transport → read stream → dispatcher → handler | "
            "Learner should notice where transport responsibility starts and ends]]\n"
            "\n"
            "---\n"
            "\n"
            "## 9. The dispatcher: correlation, concurrency, and cancellation\n"
            "\n"
            "The JSON-RPC dispatcher is the workhorse that routes received messages and manages in-flight request state.\n"
            "\n"
            "### Routing\n"
            "\n"
            "The dispatcher distinguishes:\n"
            "\n"
            "- request,\n"
            "- notification,\n"
            "- successful response,\n"
            "- error response,\n"
            "- transport exception.\n"
            "\n"
            "Responses and errors use their ID to resolve an entry in the pending-request table.\n"
            "\n"
            "If a response arrives for an unknown/non-pending ID, the source describes it being logged/dropped rather than crashing the entire loop.\n"
            "\n"
            "### Why every request gets independent execution state\n"
            "\n"
            "For an incoming request, the dispatcher can:\n"
            "\n"
            "1. read metadata such as the progress token,\n"
            "2. build a dispatch context,\n"
            "3. create an `anyio.CancelScope`,\n"
            "4. register the request in an in-flight dictionary,\n"
            "5. spawn the handler into a task group,\n"
            "6. send the handler's result/error using the same request ID.\n"
            "\n"
            "This allows many requests to be processed concurrently without one slow tool blocking the wire.\n"
            "\n"
            "### Cancellation reaches the correct task\n"
            "\n"
            "A cancellation event uses the request ID to find the matching in-flight entry and cancels that request's scope.\n"
            "\n"
            "### Closing the connection\n"
            "\n"
            "If the underlying connection closes while requests are waiting, the session must not leave callers waiting forever. "
            "The source describes fanning out a local connection-closed error to all pending requests and clearing the pending table.\n"
            "\n"
            "{{exercise:M04.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 10. What every transport must do\n"
            "\n"
            "Before comparing stdio and HTTP, separate **connection establishment** from protocol initialization.\n"
            "\n"
            "### Connection establishment\n"
            "\n"
            "The transport establishes the communication channel—launching a process, opening HTTP communication, creating a socket, or doing whatever its medium requires.\n"
            "\n"
            "### Initialization is version-dependent\n"
            "\n"
            "The source describes modern 2026-07-28-style operation as having no separate capability/version handshake. "
            "Client identity, protocol version, and capabilities ride with each request's metadata.\n"
            "\n"
            "Older versions used an initialize request/response followed by an initialized notification.\n"
            "\n"
            "For stdio, starting the subprocess and creating the read/write channels is still an initialization-like setup step at the transport/process level even though the old protocol handshake is gone.\n"
            "\n"
            "### Minimum transport responsibilities\n"
            "\n"
            "Any transport must be able to:\n"
            "\n"
            "- establish communication,\n"
            "- send JSON-RPC messages,\n"
            "- receive JSON-RPC messages,\n"
            "- handle errors and timeouts,\n"
            "- close cleanly.\n"
            "\n"
            "---\n"
            "\n"
            "## 11. stdio: the local-process transport\n"
            "\n"
            "stdio is MCP's local-process transport. The client launches the MCP server as a subprocess and communicates through the subprocess's standard input and output.\n"
            "\n"
            "```text\n"
            "Host / MCP Client\n"
            "      │\n"
            "      ├── writes JSON-RPC lines → server stdin\n"
            "      └── reads JSON-RPC lines ← server stdout\n"
            "```\n"
            "\n"
            "### Message framing\n"
            "\n"
            "stdio uses newline-delimited JSON-RPC messages. Each complete JSON message ends with a newline.\n"
            "\n"
            "Request IDs provide correlation even when multiple messages are processed concurrently.\n"
            "\n"
            "### Opening a stdio connection\n"
            "\n"
            "The client-side transport roughly performs:\n"
            "\n"
            "```text\n"
            "1. Resolve command + arguments.\n"
            "2. Launch server subprocess.\n"
            "3. Create zero-capacity in-memory read/write stream pairs.\n"
            "4. Start stdout-reader task.\n"
            "5. Start stdin-writer task.\n"
            "6. Yield read_stream + write_stream to ClientSession.\n"
            "```\n"
            "\n"
            "The zero-capacity memory streams create backpressure: a send waits until the receiving side is ready.\n"
            "\n"
            "[[IMAGE_NEEDED: stdio transport internals | "
            "A diagram showing ClientSession connected via two anyio memory stream pairs to stdin_writer/stdout_reader tasks, which in turn connect to the server subprocess's stdin/stdout | "
            "Learner should notice the separation between in-memory session streams and OS process pipes]]\n"
            "\n"
            "### Server-side file descriptors\n"
            "\n"
            "The server side is already the subprocess, so it does not launch another process. It wraps/claims its own stdin/stdout descriptors for transport use.\n"
            "\n"
            "This is why **server logs should not be casually printed to stdout**: stdout is carrying the JSON-RPC wire protocol. "
            "Diagnostics belong on stderr or another logging channel.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. How stdio sends and receives messages\n"
            "\n"
            "### Client → server send path\n"
            "\n"
            "The session writes a `SessionMessage` to its write stream. The transport's writer task:\n"
            "\n"
            "1. receives the message,\n"
            "2. serializes it to JSON,\n"
            "3. appends a newline frame delimiter,\n"
            "4. encodes the text,\n"
            "5. writes bytes to the server subprocess's stdin.\n"
            "\n"
            "### Server → client send path\n"
            "\n"
            "The server serializes and newline-frames the message, writes it to stdout, and explicitly flushes stdout so buffering does not delay delivery.\n"
            "\n"
            "### Server → client receive path\n"
            "\n"
            "The client reads chunks from server stdout. A chunk may contain:\n"
            "\n"
            "- part of one message,\n"
            "- one complete message,\n"
            "- several messages.\n"
            "\n"
            "Therefore the reader maintains a buffer, splits on newline delimiters, validates complete JSON-RPC messages, wraps them in `SessionMessage`, and pushes them into the session read stream.\n"
            "\n"
            "### Client → server receive path\n"
            "\n"
            "On the server side, stdin is already line-oriented, so each line can be validated and handed upward to the dispatcher with less manual buffering.\n"
            "\n"
            "### stdio disconnect sequence\n"
            "\n"
            "The chapter describes a graceful shutdown sequence:\n"
            "\n"
            "```text\n"
            "Close server stdin\n"
            "     ↓\n"
            "Wait briefly for clean process exit\n"
            "     ↓\n"
            "Terminate process tree if necessary\n"
            "     ↓\n"
            "Close memory streams/tasks\n"
            "```\n"
            "\n"
            "Cleanup runs in a `finally` path so caller cancellation does not leak the subprocess.\n"
            "\n"
            "---\n"
            "\n"
            "## 13. Streamable HTTP: the modern remote transport\n"
            "\n"
            "Streamable HTTP is the remote transport emphasized by the source. In the modern model it is:\n"
            "\n"
            "- **single endpoint**,\n"
            "- **POST-oriented**,\n"
            "- **stateless between requests**,\n"
            "- able to return either ordinary JSON or an SSE stream scoped to one request.\n"
            "\n"
            "### HTTP request itself is the frame\n"
            "\n"
            "Unlike stdio, the transport does not need a newline delimiter. One outbound MCP message lives inside one HTTP POST request.\n"
            "\n"
            "A response may be:\n"
            "\n"
            "- one JSON body, or\n"
            "- a per-request SSE stream containing one or more MCP events.\n"
            "\n"
            "### Why statelessness matters\n"
            "\n"
            "Modern requests do not depend on a durable server-side MCP session. This makes horizontal scaling behind load balancers much more natural.\n"
            "\n"
            "[[IMAGE_NEEDED: Modern Streamable HTTP lifecycle | "
            "A diagram showing ClientSession write stream → post_writer → multiple independent POST request tasks → /mcp endpoint → JSON or per-request SSE responses → read stream | "
            "Learner should notice that each request owns its own HTTP exchange rather than sharing one permanent connection]]\n"
            "\n"
            "---\n"
            "\n"
            "## 14. Opening and sending over Streamable HTTP\n"
            "\n"
            "The client context manager takes a server URL and optionally a preconfigured async HTTP client.\n"
            "\n"
            "A custom HTTP client allows the application to control concerns such as:\n"
            "\n"
            "- authentication,\n"
            "- headers,\n"
            "- timeouts,\n"
            "- TLS/proxy settings.\n"
            "\n"
            "### Opening flow\n"
            "\n"
            "The modern lifecycle can be summarized as:\n"
            "\n"
            "```text\n"
            "1. Create/accept Async HTTP client.\n"
            "2. Create MCP read/write memory streams.\n"
            "3. Create StreamableHTTPTransport for the URL.\n"
            "4. Start long-lived post_writer task.\n"
            "5. Yield read/write streams to ClientSession.\n"
            "6. Each outbound SessionMessage spawns an ephemeral POST task.\n"
            "```\n"
            "\n"
            "The source notes that legacy connection code may still contain session-ID and GET-stream compatibility behavior, but modern operation does not require those mechanisms.\n"
            "\n"
            "### Metadata on modern requests\n"
            "\n"
            "Modern requests carry version/client/capability information with the request so the server can process each stateless request independently.\n"
            "\n"
            "### Notification responses\n"
            "\n"
            "A client notification sent over HTTP does not expect an MCP response body in the same sense as a request. "
            "The source discusses HTTP 202 handling for accepted notifications and treating an unexpected 202 to a request as an error rather than waiting forever.\n"
            "\n"
            "---\n"
            "\n"
            "## 15. How the server responds over Streamable HTTP\n"
            "\n"
            "For an incoming request, the server chooses a response form appropriate to the operation.\n"
            "\n"
            "### JSON response mode\n"
            "\n"
            "For a short operation, the server can return one JSON-RPC result/error in an ordinary HTTP response.\n"
            "\n"
            "### Per-request SSE response mode\n"
            "\n"
            "For long-running work, an SSE response can carry multiple events—such as progress—before the final JSON-RPC response/error event ends the stream.\n"
            "\n"
            "The SSE stream exists only for that specific POST/request. It is not the same thing as the old global long-lived HTTP SSE connection.\n"
            "\n"
            "### Client receive logic\n"
            "\n"
            "The client examines the HTTP content type:\n"
            "\n"
            "```text\n"
            "application/json   → parse one JSON-RPC response\n"
            "text/event-stream  → iterate SSE events, parse each message\n"
            "unexpected type    → transport error path\n"
            "```\n"
            "\n"
            "Parsed responses are wrapped as session messages and sent into the same read stream used by every transport.\n"
            "\n"
            "This is transport abstraction in practice: the session does not need to know whether the response came from process stdout or HTTP SSE.\n"
            "\n"
            "---\n"
            "\n"
            "## 16. Modern server-to-client needs: input_required and subscriptions\n"
            "\n"
            "Modern MCP changes how the server obtains additional information during an operation.\n"
            "\n"
            "### Server needs more input\n"
            "\n"
            "Instead of starting a brand-new unsolicited request over a permanent reverse channel, the server can return a result indicating `input_required`. "
            "The client gathers/provides the requested input and sends a new request.\n"
            "\n"
            "```text\n"
            "Client POST request\n"
            "      ↓\n"
            "Server result: input_required\n"
            "      ↓\n"
            "Client obtains required information\n"
            "      ↓\n"
            "Client sends follow-up POST\n"
            "      ↓\n"
            "Server completes operation\n"
            "```\n"
            "\n"
            "### Long-lived notifications remain opt-in\n"
            "\n"
            "The source identifies one intentional long-lived modern stream: a client can call `subscriptions/listen`, and the server can keep that request's SSE response open to deliver subscribed change notifications.\n"
            "\n"
            "This is very different from the old design where every initialized client opened a broad GET stream for unsolicited server messages.\n"
            "\n"
            "[[IMAGE_NEEDED: Modern input_required versus subscriptions/listen | "
            "Two side-by-side sequences: one showing input_required then a client follow-up POST, and one showing an explicitly requested subscriptions/listen POST whose SSE response stays open for change events | "
            "Learner should notice that both preserve client initiation]]\n"
            "\n"
            "---\n"
            "\n"
            "## 17. Legacy HTTP SSE and why it was replaced\n"
            "\n"
            "Before Streamable HTTP, MCP used a remote HTTP/SSE transport with a long-lived event stream.\n"
            "\n"
            "The source identifies several problems.\n"
            "\n"
            "### Two endpoints\n"
            "\n"
            "Requests and server responses used different endpoints/paths, increasing implementation and correlation complexity.\n"
            "\n"
            "### Long-lived connections\n"
            "\n"
            "Permanent SSE connections are awkward and expensive for serverless infrastructure and scaling-to-zero environments.\n"
            "\n"
            "### Authentication lifetime\n"
            "\n"
            "Long-lived sessions can make it harder to revalidate credentials on every operation.\n"
            "\n"
            "### Poor resumability\n"
            "\n"
            "Dropped SSE connections could lose in-flight responses.\n"
            "\n"
            "The source states that HTTP SSE was deprecated in favor of Streamable HTTP beginning with the 2025-03-26 protocol revision, while SDKs may retain compatibility paths for older systems.\n"
            "\n"
            "---\n"
            "\n"
            "## 18. Building a custom transport\n"
            "\n"
            "MCP does not require you to use only the standard transports. A specialized environment might justify gRPC, WebSocket, a compliance-specific channel, or another communication mechanism.\n"
            "\n"
            "In the Python SDK, the custom transport contract is largely implicit: the session expects a pair of memory-stream endpoints with specific behavior.\n"
            "\n"
            "### Generic custom-transport pattern\n"
            "\n"
            "```text\n"
            "1. Create read stream pair:\n"
            "      transport owns read_stream_writer\n"
            "      session receives read_stream\n"
            "\n"
            "2. Create write stream pair:\n"
            "      session receives write_stream\n"
            "      transport owns write_stream_reader\n"
            "\n"
            "3. Establish underlying connection.\n"
            "\n"
            "4. Start read task:\n"
            "      wire → deframe → deserialize → SessionMessage → read_stream_writer\n"
            "\n"
            "5. Start write task:\n"
            "      write_stream_reader → serialize → frame → wire\n"
            "\n"
            "6. Yield read_stream + write_stream to session.\n"
            "\n"
            "7. In finally:\n"
            "      close wire connection\n"
            "      cancel task group\n"
            "      close memory streams\n"
            "```\n"
            "\n"
            "This design preserves the most valuable architectural property in the chapter: **sessions remain transport-agnostic**.\n"
            "\n"
            "[[IMAGE_NEEDED: Custom MCP transport contract | "
            "A diagram with Session on the left, two anyio memory stream pairs in the middle, custom read/write tasks, framing/serialization, and an arbitrary wire protocol on the right | "
            "Learner should notice which stream endpoints belong to the session versus the transport]]\n"
            "\n"
            "{{exercise:M04.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 19. Transport-level security depends on the transport\n"
            "\n"
            "There is no single MCP transport threat model. stdio and Streamable HTTP live in different environments.\n"
            "\n"
            "### stdio threat model\n"
            "\n"
            "The client executes a server binary/process locally. If that process is malicious or compromised, it executes with whatever privileges/environment the host gives it.\n"
            "\n"
            "The source's mitigation themes are:\n"
            "\n"
            "- install only trusted servers,\n"
            "- pin versions,\n"
            "- run with least privilege,\n"
            "- sandbox/containerize when appropriate,\n"
            "- avoid handing the server the host's entire secret-rich environment,\n"
            "- pass only the secrets/variables the server actually needs.\n"
            "\n"
            "### Streamable HTTP threat model\n"
            "\n"
            "The connection crosses a network boundary.\n"
            "\n"
            "The source emphasizes:\n"
            "\n"
            "- TLS for production,\n"
            "- authentication on every stateless request,\n"
            "- careful compatibility behavior if legacy session IDs are still accepted,\n"
            "- localhost binding for local HTTP deployments,\n"
            "- Origin validation to reduce DNS-rebinding-style attacks.\n"
            "\n"
            "### Statelessness changes some risks\n"
            "\n"
            "Modern stateless Streamable HTTP has no durable MCP session ID to hijack/fixate. "
            "Legacy-compatible stateful behavior retains additional session-management risk.\n"
            "\n"
            "[[IMAGE_NEEDED: stdio versus HTTP transport threat models | "
            "Two panels: stdio risks centered on local process privileges/environment/secrets, Streamable HTTP risks centered on network interception/authentication/origin exposure | "
            "Learner should notice that transport choice changes which security controls matter most]]\n"
            "\n"
            "---\n"
            "\n"
            "## 20. Choosing the right transport\n"
            "\n"
            "The source compares the two standard transports across deployment, authentication, latency, and scalability.\n"
            "\n"
            "| Consideration | stdio | Streamable HTTP |\n"
            "|---|---|---|\n"
            "| Local server | Excellent fit | Also possible |\n"
            "| Remote/network server | Not appropriate | Designed for this |\n"
            "| Trust/authentication | Local process boundary | Network authentication such as OAuth/API keys |\n"
            "| Latency | Very low local pipe latency | Network dependent |\n"
            "| Horizontal scale | One server process per client | Natural fit for stateless load-balanced deployments |\n"
            "| Typical use | Local tools/development/personal projects | Production/enterprise remote services |\n"
            "\n"
            "### A practical decision tree\n"
            "\n"
            "```text\n"
            "Does the server need to run remotely?\n"
            "    ├── Yes → Streamable HTTP (or justified custom transport)\n"
            "    └── No\n"
            "         ↓\n"
            "Is it a local user-installed/developer tool?\n"
            "    ├── Yes → stdio is usually simplest\n"
            "    └── Maybe → HTTP can still be useful for local network/container workflows\n"
            "```\n"
            "\n"
            "For production remote deployment, the source strongly favors Streamable HTTP over legacy SSE or stdio.\n"
            "\n"
            "{{exercise:M04.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'The transport decides what a tools/call request means.'\n"
            "\n"
            "**Why this is wrong:** the protocol/session layer understands MCP semantics; the transport moves framed/serialized messages.\n"
            "\n"
            "### Misconception 2: 'Request IDs are just logging metadata.'\n"
            "\n"
            "**Why this is wrong:** IDs are fundamental to correlating concurrent responses with the requests that created them.\n"
            "\n"
            "### Misconception 3: 'A tool exception is always a JSON-RPC error response.'\n"
            "\n"
            "**Why this is wrong:** the source distinguishes application errors that can be returned as normal result messages with `isError=true` from protocol-level JSON-RPC errors.\n"
            "\n"
            "### Misconception 4: 'Notifications need acknowledgment responses.'\n"
            "\n"
            "**Why this is wrong:** notifications are intentionally one-way and therefore carry no request ID.\n"
            "\n"
            "### Misconception 5: 'Base64 is free.'\n"
            "\n"
            "**Why this is wrong:** Base64 increases payload size by roughly one third and is poorly suited to large blobs.\n"
            "\n"
            "### Misconception 6: 'ClientSession must know whether a message uses stdio or HTTP.'\n"
            "\n"
            "**Why this is wrong:** the session interacts through abstract read/write streams so transport details remain hidden.\n"
            "\n"
            "### Misconception 7: 'stdio can safely use stdout for debug prints.'\n"
            "\n"
            "**Why this is wrong:** stdout carries framed JSON-RPC protocol messages; unrelated output can corrupt the wire stream.\n"
            "\n"
            "### Misconception 8: 'Modern Streamable HTTP is one permanent SSE connection.'\n"
            "\n"
            "**Why this is wrong:** each client message is its own POST exchange; a request may receive JSON or an ephemeral SSE response stream.\n"
            "\n"
            "### Misconception 9: 'The old HTTP SSE transport and SSE responses in Streamable HTTP are the same architecture.'\n"
            "\n"
            "**Why this is wrong:** old SSE relied on a long-lived transport connection; modern Streamable HTTP may use SSE only as a response body for a specific request or explicit subscription.\n"
            "\n"
            "### Misconception 10: 'A custom transport requires rewriting ClientSession.'\n"
            "\n"
            "**Why this is wrong:** if the transport fulfills the SDK's stream contract, the existing session layer can remain unchanged.\n"
            "\n"
            "### Misconception 11: 'A local HTTP server bound to all interfaces is equivalent to stdio security.'\n"
            "\n"
            "**Why this is wrong:** once HTTP is exposed, network-origin and DNS-rebinding risks apply even if the service is intended for local use.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Transport | Layer that moves serialized/framed JSON-RPC messages between MCP peers |\n"
            "| JSON-RPC | Lightweight RPC message format used as MCP's message/data foundation |\n"
            "| Request | Message with an ID that invokes a method and expects a response |\n"
            "| Result response | Successful JSON-RPC response correlated by request ID |\n"
            "| Error response | JSON-RPC response describing a protocol-level failure |\n"
            "| Notification | One-way JSON-RPC message with no request ID |\n"
            "| `isError` result | Application-level failure encoded inside a normal result message |\n"
            "| `structuredContent` | Machine-readable JSON object returned alongside tool content |\n"
            "| `input_required` | Result state indicating additional client input is required before completion |\n"
            "| Progress token | Correlation token used to route progress notifications for one operation |\n"
            "| ResourceLink | Metadata/URI reference to data that can be loaded later rather than embedded directly |\n"
            "| Base64 | Text encoding used to transmit binary content inside JSON, with approximately 33% size overhead |\n"
            "| `ClientSession` | Client-side SDK abstraction above the transport |\n"
            "| `ServerSession` | Server-side/request communication abstraction above the transport |\n"
            "| Dispatcher | Component that routes messages and manages pending/in-flight request state |\n"
            "| Pending request | Outbound request waiting for a response/error with a matching ID |\n"
            "| In-flight request | Request currently being handled and potentially cancellable |\n"
            "| Cancel scope | AnyIO construct used to cancel one running request task |\n"
            "| Framing | Defining where one message ends and another begins on a byte/message stream |\n"
            "| stdio | Local transport using subprocess stdin/stdout and newline-delimited JSON-RPC |\n"
            "| Streamable HTTP | Modern remote transport using independent POST requests with JSON or per-request SSE responses |\n"
            "| SSE | Server-Sent Events; streaming HTTP event format used in legacy transport and per-request streaming responses |\n"
            "| `subscriptions/listen` | Explicit modern operation that can keep a response stream open for subscribed change events |\n"
            "| Custom transport | Nonstandard transport implementing the SDK's session-facing contract |\n"
            "| TLS | Transport Layer Security used to protect network HTTP communication |\n"
            "| DNS rebinding | Browser/network attack relevant to improperly exposed local HTTP services |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is the difference between the MCP protocol layer and transport layer?\n"
            "2. Why does a request need an ID?\n"
            "3. What does the `method` field identify?\n"
            "4. How do tools/call operation parameters differ from tool arguments?\n"
            "5. How does a protocol error differ from an application tool error?\n"
            "6. Why does a notification have no ID?\n"
            "7. How does a progress token relate a progress notification to an operation?\n"
            "8. Why can cancellation race with a completed result?\n"
            "9. What does Base64 cost when transmitting binary data?\n"
            "10. Why can ResourceLink be better than embedding large binary content?\n"
            "11. What do ClientSession and ServerSession abstract away?\n"
            "12. What is stored in a pending-request table?\n"
            "13. Why does each incoming request get its own cancel scope/task?\n"
            "14. What happens to pending requests when the connection closes?\n"
            "15. How does connection establishment differ from legacy MCP initialization?\n"
            "16. How does stdio frame messages?\n"
            "17. Why must an stdio server avoid normal debug output on stdout?\n"
            "18. Why does the stdio client need a buffer when reading stdout chunks?\n"
            "19. What makes Streamable HTTP stateless?\n"
            "20. Why does Streamable HTTP not require newline framing for each outbound message?\n"
            "21. When would an HTTP response use JSON versus SSE?\n"
            "22. How does `input_required` preserve client-initiated interaction?\n"
            "23. What is special about `subscriptions/listen`?\n"
            "24. Why was the old HTTP SSE transport deprecated?\n"
            "25. What read/write endpoints does a custom Python transport own versus yield to the session?\n"
            "26. What security risks dominate stdio?\n"
            "27. What security risks dominate Streamable HTTP?\n"
            "28. Why should a local HTTP server prefer 127.0.0.1 over 0.0.0.0?\n"
            "29. Why is Streamable HTTP a better fit for horizontal scaling?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**MCP transports are intentionally boring plumbing: the protocol defines the messages, sessions correlate and dispatch them, "
            "and transports only establish communication, frame/serialize messages, move them over the wire, surface failures, and clean up. "
            "Understanding that separation makes MCP easier to debug, secure, scale, and extend.**\n"
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "transport-stack", "title": "Where the transport layer fits", "order": 1},
            {"id": "jsonrpc-foundation", "title": "JSON-RPC foundation", "order": 2},
            {"id": "requests", "title": "Request messages", "order": 3},
            {"id": "responses-errors", "title": "Responses and errors", "order": 4},
            {"id": "notifications", "title": "Notifications", "order": 5},
            {"id": "progress-cancellation", "title": "Progress and cancellation", "order": 6},
            {"id": "data-types", "title": "Data types and resource links", "order": 7},
            {"id": "session-objects", "title": "Session objects", "order": 8},
            {"id": "dispatcher", "title": "Dispatcher internals", "order": 9},
            {"id": "transport-contract-basics", "title": "Transport responsibilities and connection lifecycle", "order": 10},
            {"id": "stdio", "title": "stdio transport", "order": 11},
            {"id": "stdio-send-receive", "title": "stdio send, receive, and disconnect", "order": 12},
            {"id": "streamable-http", "title": "Streamable HTTP", "order": 13},
            {"id": "http-open-send", "title": "Opening and sending over Streamable HTTP", "order": 14},
            {"id": "http-server-responses", "title": "Server responses over Streamable HTTP", "order": 15},
            {"id": "modern-server-client-flow", "title": "Modern input and subscription flows", "order": 16},
            {"id": "legacy-sse", "title": "Legacy HTTP SSE", "order": 17},
            {"id": "custom-transport", "title": "Building a custom transport", "order": 18},
            {"id": "transport-security", "title": "Transport-level security", "order": 19},
            {"id": "choosing-transport", "title": "Choosing the right transport", "order": 20},
        ],
    },

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Classify MCP Message and Error Types",

            "lesson_code": "M04.L01",

            "section_id": "responses-errors",

            "placement": "after_section",

            "description": (
                "Practice identifying request, result, protocol error, application error, "
                "notification, and transport-failure cases."
            ),

            "instructions": (
                "For each scenario, identify the correct layer/message behavior and explain why:\n\n"
                "1. A client sends tools/call with an unknown required MCP parameter.\n"
                "2. The server tool runs but reports that the requested project does not exist.\n"
                "3. The TCP/HTTP connection times out before any response arrives.\n"
                "4. The server tells the client that its tool list changed.\n"
                "5. A request asks for progress and receives a 60/100 progress update.\n"
                "6. A successful tools/call returns both content and structuredContent.\n"
                "7. For one request, sketch how its ID is reused in the response."
            ),

            "expected_output": (
                "A table with scenario, layer, message type, expected ID behavior, and reasoning."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "json-rpc",
                "error-classification",
                "message-types",
                "request-correlation",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Trace Concurrent Requests Through the Dispatcher",

            "lesson_code": "M04.L01",

            "section_id": "dispatcher",

            "placement": "after_section",

            "description": (
                "Trace how session/dispatcher state keeps concurrent requests independent "
                "and how one of them can be cancelled."
            ),

            "instructions": (
                "A client sends three requests with IDs 10, 11, and 12. Request 11 is slow and is later cancelled.\n\n"
                "1. Show when each request enters the pending/in-flight structures.\n"
                "2. Show how separate tasks/cancel scopes let requests 10 and 12 complete while 11 is still running.\n"
                "3. Show how responses 12 and 10 can arrive out of order but still resolve correctly.\n"
                "4. Show what happens when cancellation targets request 11.\n"
                "5. Explain what should happen if a late result for 11 arrives after the requester already cancelled it.\n"
                "6. Explain what happens if the connection closes while one pending request has no response."
            ),

            "expected_output": (
                "A sequence diagram or state table covering pending entries, request IDs, "
                "concurrent tasks, cancellation, late results, and connection-close cleanup."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "dispatcher",
                "concurrency",
                "request-correlation",
                "cancellation",
            ],
        },

        {
            "id": "M04.L01.EX03",

            "title": "Design a Custom MCP Transport",

            "lesson_code": "M04.L01",

            "section_id": "custom-transport",

            "placement": "after_section",

            "description": (
                "Apply the transport contract to a hypothetical WebSocket-based MCP transport."
            ),

            "instructions": (
                "Design the architecture of a WebSocket MCP transport for the Python SDK.\n\n"
                "1. Define the two anyio memory stream pairs.\n"
                "2. Identify which endpoints belong to the session and which belong to the transport.\n"
                "3. Describe connection establishment.\n"
                "4. Define message framing for your WebSocket messages.\n"
                "5. Describe the read task from wire to SessionMessage.\n"
                "6. Describe the write task from SessionMessage to wire.\n"
                "7. Explain how errors/timeouts surface to the session.\n"
                "8. Define cleanup in the context manager's finally block.\n"
                "9. Identify two security risks unique or important to your chosen transport."
            ),

            "expected_output": (
                "A transport architecture diagram plus pseudocode-level lifecycle for setup, "
                "read/write loops, error propagation, and cleanup."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "custom-transports",
                "anyio-streams",
                "framing",
                "transport-architecture",
            ],
        },

        {
            "id": "M04.L01.EX04",

            "title": "Choose and Threat-Model a Transport",

            "lesson_code": "M04.L01",

            "section_id": "choosing-transport",

            "placement": "after_section",

            "description": (
                "Choose between stdio and Streamable HTTP for realistic deployments and "
                "apply the correct security posture."
            ),

            "instructions": (
                "For each scenario, choose stdio or Streamable HTTP and justify the decision:\n\n"
                "1. A personal local code-indexing server launched by an IDE.\n"
                "2. A hosted CRM integration used by thousands of customers.\n"
                "3. A locally running Docker container exposed on localhost.\n"
                "4. A production internal service behind a load balancer.\n\n"
                "For every choice, discuss:\n"
                "- process/network boundary,\n"
                "- authentication needs,\n"
                "- TLS needs,\n"
                "- secret handling,\n"
                "- sandboxing/least privilege,\n"
                "- horizontal scaling,\n"
                "- one likely failure mode."
            ),

            "expected_output": (
                "A four-row transport decision and threat-model table."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "transport-selection",
                "security",
                "deployment-architecture",
                "tradeoff-analysis",
            ],
        },
    ],

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "MCP Transports — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",

                "section_id": "jsonrpc-foundation",

                "question": "What is the primary role of JSON-RPC in MCP?",

                "options": [
                    "It chooses which LLM provider the host uses.",
                    "It defines the message structure used for MCP method calls, results, errors, and notifications.",
                    "It encrypts all MCP network traffic.",
                    "It launches local MCP server processes.",
                ],

                "correct": 1,

                "explanation": (
                    "JSON-RPC is MCP's message/data foundation. Transports decide how those "
                    "messages move; JSON-RPC defines their general structure."
                ),
            },

            {
                "id": "M04.L01.Q02",

                "section_id": "requests",

                "question": "Why is the request ID important?",

                "options": [
                    "It identifies the tool's Python module.",
                    "It correlates the response with the request, including during concurrent operations.",
                    "It indicates the protocol version.",
                    "It stores tool arguments.",
                ],

                "correct": 1,

                "explanation": (
                    "The ID lets the dispatcher match an incoming result/error with the "
                    "pending request that created it."
                ),
            },

            {
                "id": "M04.L01.Q03",

                "section_id": "responses-errors",

                "question": "How does the source distinguish an application-level tool failure from a protocol-level failure?",

                "options": [
                    "Both always become connection failures.",
                    "A tool failure can be returned in a normal result with isError=true, while a protocol failure uses a JSON-RPC error response.",
                    "A tool failure has no message at all.",
                    "Protocol failures are always progress notifications.",
                ],

                "correct": 1,

                "explanation": (
                    "This distinction lets application errors carry useful model-readable information "
                    "without confusing them with malformed protocol operations."
                ),
            },

            {
                "id": "M04.L01.Q04",

                "section_id": "notifications",

                "question": "Why does a JSON-RPC notification have no request ID?",

                "options": [
                    "Because notifications are encrypted.",
                    "Because notifications are one-way and do not expect a correlated response.",
                    "Because only servers can send notifications.",
                    "Because notifications contain no method.",
                ],

                "correct": 1,

                "explanation": (
                    "No response is expected, so there is nothing to correlate."
                ),
            },

            {
                "id": "M04.L01.Q05",

                "section_id": "data-types",

                "question": "Why are ResourceLink-style references useful for large binary data?",

                "options": [
                    "They force every file into the LLM context immediately.",
                    "They support deferred/out-of-band loading and avoid Base64/context overhead.",
                    "They eliminate resource URIs.",
                    "They turn all binary data into tool schemas.",
                ],

                "correct": 1,

                "explanation": (
                    "Resource links can carry metadata and a URI without embedding the entire blob, "
                    "which reduces payload and context cost."
                ),
            },

            {
                "id": "M04.L01.Q06",

                "section_id": "dispatcher",

                "question": "Why does the dispatcher register requests in pending/in-flight state?",

                "options": [
                    "To prevent all concurrent requests",
                    "To correlate responses and make individual requests cancellable while they run",
                    "To choose the HTTP hostname",
                    "To translate JSON into Base64",
                ],

                "correct": 1,

                "explanation": (
                    "Request IDs and per-request execution state allow concurrency, correlation, "
                    "progress handling, and targeted cancellation."
                ),
            },

            {
                "id": "M04.L01.Q07",

                "section_id": "stdio",

                "question": "How does stdio frame MCP messages?",

                "options": [
                    "Each message is separated by a newline.",
                    "Each message requires an HTTP Content-Length header.",
                    "Every message opens a new TCP socket.",
                    "Messages are always delivered as SSE events.",
                ],

                "correct": 0,

                "explanation": (
                    "The stdio transport uses newline-delimited JSON-RPC messages over process pipes."
                ),
            },

            {
                "id": "M04.L01.Q08",

                "section_id": "stdio-send-receive",

                "question": "Why should an stdio MCP server avoid writing normal debug output to stdout?",

                "options": [
                    "stdout is reserved for JSON-RPC transport messages and unrelated text can corrupt framing.",
                    "stdout is never available to subprocesses.",
                    "The client can only read stderr.",
                    "JSON-RPC requires binary stdout.",
                ],

                "correct": 0,

                "explanation": (
                    "stdio uses stdout as the protocol wire from server to client, so ordinary logs "
                    "should use stderr or another logging destination."
                ),
            },

            {
                "id": "M04.L01.Q09",

                "section_id": "streamable-http",

                "question": "Which statement best describes modern Streamable HTTP in the supplied chapter?",

                "options": [
                    "One permanent bidirectional WebSocket per client",
                    "Independent client POST requests whose responses are JSON or request-scoped SSE streams",
                    "Two permanent HTTP endpoints connected by a session ID",
                    "A local-only process transport",
                ],

                "correct": 1,

                "explanation": (
                    "Modern Streamable HTTP is stateless and POST-based; each operation is its own "
                    "HTTP exchange."
                ),
            },

            {
                "id": "M04.L01.Q10",

                "section_id": "legacy-sse",

                "question": "Why was the older HTTP SSE transport deprecated?",

                "options": [
                    "It could not transmit text.",
                    "Its two-endpoint, long-lived, nonresumable design complicated deployment and scaling.",
                    "It worked only on Windows.",
                    "It had no JSON-RPC support.",
                ],

                "correct": 1,

                "explanation": (
                    "The source highlights complexity, long-lived connection costs, and lack of "
                    "resumability as major shortcomings."
                ),
            },

            {
                "id": "M04.L01.Q11",

                "section_id": "custom-transport",

                "question": "What lets a custom Python transport work with the existing session objects?",

                "options": [
                    "It must inherit from the stdio subprocess class.",
                    "It fulfills the expected read/write memory-stream contract and handles wire framing/serialization itself.",
                    "It must expose only tools/list.",
                    "It must use HTTP SSE internally.",
                ],

                "correct": 1,

                "explanation": (
                    "The session layer interacts through yielded read/write streams, allowing any "
                    "transport that implements that contract to plug in."
                ),
            },

            {
                "id": "M04.L01.Q12",

                "section_id": "transport-security",

                "type": "open",

                "question": (
                    "Compare the architecture and security posture of an stdio MCP server and a modern "
                    "Streamable HTTP MCP server. Cover connection establishment, framing, session abstraction, "
                    "authentication, TLS, secret handling, cancellation, scaling, and cleanup."
                ),
            },
        ],

        "passing_score": 70,
    },
}
