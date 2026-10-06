"""M02.L01 — Building Agentic Applications with MCP Clients.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 3 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Building MCP Clients"

MODULE_DESCRIPTION = (
    "Build the client side of an MCP-powered agentic application: understand host "
    "applications, manage stdio and Streamable HTTP connections, discover and use "
    "server capabilities, create tool-use loops, load resources into context, "
    "consume dynamic prompts, and design for reliability and security."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building Agentic Applications with MCP Clients",

    "slug": "ai-agents-mcp-m02-l01",

    "description": (
        "A hands-on lesson on turning an ordinary LLM application into an MCP host. "
        "You will design an MCP client wrapper, connect over stdio and Streamable "
        "HTTP, discover tools/resources/prompts, build a multi-tool agent loop, "
        "load contextual resources, use dynamic prompts, and handle failures safely."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "mcp-client",
        "host-application",
        "agentic-ai",
        "stdio",
        "streamable-http",
        "async-python",
        "tool-calling",
        "mcp-tools",
        "mcp-resources",
        "mcp-prompts",
        "error-handling",
        "context-engineering",
        "module-02",
    ],

    "prerequisite_ids": ["M01.L01"],

    "lesson": {
        "title": "Building Agentic Applications with MCP Clients",

        "content": (
            "# Building Agentic Applications with MCP Clients\n"
            "\n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Building MCP Clients  \n"
            "> **Source alignment:** Chapter 3 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the difference between an LLM provider client and an MCP client.\n"
            "- Describe what makes an application an MCP host application.\n"
            "- Explain the one-client-instance-to-one-server relationship used in the source chapter.\n"
            "- Design a reusable MCP client wrapper with connect, disconnect, discovery, and use methods.\n"
            "- Choose between stdio and Streamable HTTP for a given deployment scenario.\n"
            "- Explain why `AsyncExitStack` is useful for MCP connection lifecycle management.\n"
            "- Discover and call MCP tools while handling multiple content types.\n"
            "- Build a repeated tool-use loop that returns tool results to an LLM until a final answer is produced.\n"
            "- List, select, and load MCP resources into model context.\n"
            "- Use resource templates and understand why resource selection is a context-engineering decision.\n"
            "- Discover, parameterize, and load MCP prompts.\n"
            "- Handle MCP errors, timeouts, unexpected disconnects, and cleanup safely.\n"
            "- Apply client-side design principles such as capability filtering, model agnosticism, logging, retries, and secret handling.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. From an ordinary LLM app to an MCP host\n"
            "\n"
            "Before adding MCP, start with the simplest possible application: a program that accepts user input, sends it to an "
            "LLM API, receives a response, and prints that response.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "User → Host program → LLM API → Host program → User\n"
            "```\n"
            "\n"
            "That application is useful, but it is not yet using MCP. To become an **MCP host application**, it must also host one "
            "or more MCP clients that communicate with MCP servers.\n"
            "\n"
            "A host can be extremely small or very complex. The chapter gives examples ranging from a simple chatbot script to "
            "an IDE, coding-agent harness, chatbot platform, or agent framework. The host's key responsibilities are to interact "
            "with an LLM and to contain the client code that provides access to MCP servers.\n"
            "\n"
            "If the host wants the model to choose tools, the model must also support tool calling.\n"
            "\n"
            "### Two different clients you must not confuse\n"
            "\n"
            "A beginner can easily confuse the **LLM provider client** with the **MCP client**.\n"
            "\n"
            "| Client | Talks to | Purpose |\n"
            "|---|---|---|\n"
            "| LLM provider client | Model provider API | Sends messages to the language model and receives model responses |\n"
            "| MCP client | MCP server | Discovers and uses MCP capabilities such as tools, resources, and prompts |\n"
            "\n"
            "The host application coordinates both sides.\n"
            "\n"
            "```text\n"
            "                    ┌───────────────┐\n"
            "User ─────────────→ │ Host App      │\n"
            "                    │               │\n"
            "                    │ LLM Client ───────→ LLM API\n"
            "                    │ MCP Client ───────→ MCP Server\n"
            "                    └───────────────┘\n"
            "```\n"
            "\n"
            '{{image:host-app-llm-and-mcp-clients}}'
            '\n'
            "\n"
            "### Keep secrets out of source code\n"
            "\n"
            "The chapter's starter host loads an API key from environment variables, optionally through a `.env` file. "
            "The important engineering rule is not the specific library—it is that secrets should not be hard-coded or committed "
            "to version control.\n"
            "\n"
            "> If an API key is accidentally exposed publicly, revoke or de-authorize it and replace it rather than assuming deletion "
            "from the repository history is enough.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. What an MCP client is responsible for\n"
            "\n"
            "The MCP client is the bridge between the host application and an MCP server. In the design used by the source chapter, "
            "one client instance communicates with one server. If a host needs several servers, it creates several client instances.\n"
            "\n"
            "At minimum, a useful client should be able to:\n"
            "\n"
            "1. **Connect** to a server.\n"
            "2. **Discover** what the server provides.\n"
            "3. **Expose or translate** those capabilities into a form the host and LLM can use.\n"
            "4. **Invoke** the selected capability.\n"
            "5. **Disconnect and clean up** resources safely.\n"
            "\n"
            "The chapter also identifies useful cross-cutting client features:\n"
            "\n"
            "- Authentication\n"
            "- Capability filtering\n"
            "- Model agnosticism\n"
            "- Logging\n"
            "- Retry behavior\n"
            "- Response transformation\n"
            "\n"
            "### Why wrap the SDK client?\n"
            "\n"
            "The Python SDK client can be used directly. The chapter nevertheless wraps it in an application-specific `MCPClient` "
            "class. This wrapper gives the application a clean boundary where it can:\n"
            "\n"
            "- verify connection state before calls,\n"
            "- add logs,\n"
            "- add retry policies,\n"
            "- convert MCP-native objects into a format expected by a model API,\n"
            "- filter capabilities,\n"
            "- process results before they reach the rest of the application,\n"
            "- manually control long-lived connections.\n"
            "\n"
            "A minimal interface might look like this:\n"
            "\n"
            "```python\n"
            "class MCPClient:\n"
            "    async def connect(self) -> None:\n"
            "        ...\n"
            "\n"
            "    async def get_available_tools(self):\n"
            "        ...\n"
            "\n"
            "    async def use_tool(self, tool_name, arguments=None):\n"
            "        ...\n"
            "\n"
            "    async def disconnect(self) -> None:\n"
            "        ...\n"
            "```\n"
            "\n"
            "The point of this skeleton is architectural. `connect()` and `disconnect()` manage lifecycle, while discovery and use "
            "methods hide protocol details from the host application.\n"
            "\n"
            "[[IMAGE_NEEDED: Wrapped MCP client layer hierarchy | "
            "A layered diagram showing Host Application → application MCPClient wrapper → SDK Client → Transport → MCP Server | "
            "Learner should notice that the wrapper is an application design choice that adds control without replacing the SDK client]]\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Choosing the transport: stdio or Streamable HTTP\n"
            "\n"
            "Before implementing `connect()`, the client must know how it will communicate with the server.\n"
            "\n"
            "The chapter focuses on two built-in transports:\n"
            "\n"
            "| Transport | Typical location | Main idea |\n"
            "|---|---|---|\n"
            "| `stdio` | Local server | The host launches a subprocess and communicates through standard input/output |\n"
            "| Streamable HTTP | Remote server | The client sends MCP requests to a remote HTTP endpoint |\n"
            "\n"
            "### When stdio fits\n"
            "\n"
            "Use stdio when the server is expected to run alongside the host application. This is common in local developer tools "
            "and IDE scenarios where users install the server on their own machine.\n"
            "\n"
            "The host normally knows:\n"
            "\n"
            "- the executable command,\n"
            "- command-line arguments,\n"
            "- optional environment variables.\n"
            "\n"
            "### When Streamable HTTP fits\n"
            "\n"
            "Use Streamable HTTP when users should not need to install and run the server locally. This is a natural choice for "
            "hosted platforms, SaaS integrations, centrally managed tools, and enterprise services.\n"
            "\n"
            "The host normally needs a server URL and, depending on the service, HTTP headers or authentication configuration.\n"
            "\n"
            "### Important difference\n"
            "\n"
            "With stdio, a real local subprocess is started and managed. With the stateless Streamable HTTP design described in the "
            "chapter, 'connect' does not mean opening one persistent bidirectional socket that stays alive forever. Instead, the client "
            "prepares the HTTP communication path and performs protocol discovery so later requests can be sent correctly.\n"
            "\n"
            "[[IMAGE_NEEDED: stdio versus Streamable HTTP client connection | "
            "A side-by-side architecture: left shows Host + MCP Client launching a local MCP Server subprocess via stdio; right shows "
            "Host + MCP Client sending requests to a remote MCP Server URL over Streamable HTTP | "
            "Learner should notice that stdio manages a local process while Streamable HTTP targets a remote service]]\n"
            "\n"
            "### Security still matters at the transport layer\n"
            "\n"
            "The source explicitly warns that remote transport must be secured. It mentions authenticating the connection and "
            "validating origin headers to defend against DNS-rebinding-style attacks. The larger lesson is that MCP connectivity does "
            "not remove normal network security requirements.\n"
            "\n"
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Managing asynchronous client lifecycle\n"
            "\n"
            "MCP client code is asynchronous because the application is coordinating I/O: subprocess communication, HTTP requests, "
            "tool calls, resource reads, and notifications.\n"
            "\n"
            "The source chapter uses `AsyncExitStack` to manage asynchronous resources. This is useful because the application can "
            "enter several async contexts dynamically and later close them in a controlled order with one cleanup call.\n"
            "\n"
            "A client wrapper can maintain state such as:\n"
            "\n"
            "```python\n"
            "self._client = None\n"
            "self._exit_stack = AsyncExitStack()\n"
            "self._connected = False\n"
            "```\n"
            "\n"
            "The `_connected` flag is a simple guardrail. It prevents accidentally opening a second session through the same wrapper.\n"
            "\n"
            "### stdio connection flow\n"
            "\n"
            "The source's stdio flow can be understood as four steps:\n"
            "\n"
            "```text\n"
            "1. Build StdioServerParameters\n"
            "2. Create stdio transport\n"
            "3. Build SDK Client around the transport\n"
            "4. Enter the async client context and mark the wrapper connected\n"
            "```\n"
            "\n"
            "The configuration includes the executable command, arguments, and optional environment variables. The connection startup "
            "launches the local server process and performs protocol compatibility/capability discovery.\n"
            "\n"
            "### Streamable HTTP connection flow\n"
            "\n"
            "For remote servers, the wrapper stores a URL instead of a local executable. If the application needs custom headers, "
            "it can build an asynchronous HTTP client and pass that into the Streamable HTTP transport. If it does not need custom "
            "configuration, the SDK can create the default transport from the server URL.\n"
            "\n"
            "### Cleanup is part of correctness\n"
            "\n"
            "A robust `disconnect()` should close the exit stack and reset connection state. Cleanup should also happen if connection "
            "setup itself fails; otherwise, partially initialized resources can remain alive.\n"
            "\n"
            "A safe structure is conceptually:\n"
            "\n"
            "```python\n"
            "try:\n"
            "    # build transport and enter client context\n"
            "    ...\n"
            "except Exception:\n"
            "    await self._exit_stack.aclose()\n"
            "    raise\n"
            "```\n"
            "\n"
            "The wrapper can also implement `__aenter__()` and `__aexit__()` so it can be used as an async context manager while "
            "sharing the same `connect()` and `disconnect()` logic.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. The reusable MCP pattern: discover, then use\n"
            "\n"
            "A major simplifying idea in this chapter is that tools, resources, and prompts all follow a similar pattern:\n"
            "\n"
            "```text\n"
            "Connect\n"
            "   ↓\n"
            "Discover available capability\n"
            "   ↓\n"
            "Select capability\n"
            "   ↓\n"
            "Use capability\n"
            "   ↓\n"
            "Process result\n"
            "```\n"
            "\n"
            "Discovery typically uses a `*/list` protocol operation wrapped by an SDK `list_*()` method. Use then calls the operation "
            "appropriate to the primitive, such as `call_tool()`, `read_resource()`, or `get_prompt()`.\n"
            "\n"
            "Wrapping SDK methods inside your application client lets you apply consistent behavior across all primitives: connection "
            "checks, logging, retries, pagination support, filtering, and output transformation.\n"
            "\n"
            "### Notifications\n"
            "\n"
            "Servers can also send notifications. The Python client can listen for them, allowing the application to react when "
            "capabilities or resources change rather than assuming the initial discovery result remains valid forever.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Discovering and calling tools\n"
            "\n"
            "Tools are executable capabilities that the model may choose to invoke. A client can discover them with the SDK's "
            "`list_tools()` call.\n"
            "\n"
            "A tool definition commonly gives the client information such as:\n"
            "\n"
            "- name,\n"
            "- description,\n"
            "- input schema,\n"
            "- annotations.\n"
            "\n"
            "For a model API that accepts structured tools, the client wrapper may translate each MCP tool into a plain structure "
            "containing only what that model API expects.\n"
            "\n"
            "```python\n"
            "async def get_available_tools(self):\n"
            "    if not self._connected:\n"
            "        raise RuntimeError('Client not connected to a server')\n"
            "\n"
            "    result = await self._client.list_tools()\n"
            "    return [\n"
            "        {\n"
            "            'name': tool.name,\n"
            "            'description': tool.description,\n"
            "            'input_schema': tool.input_schema,\n"
            "        }\n"
            "        for tool in result.tools\n"
            "    ]\n"
            "```\n"
            "\n"
            "The exact model-specific format is less important than the design lesson: **the wrapper is an adaptation boundary**. "
            "It can translate MCP-native data into whatever representation the chosen LLM needs.\n"
            "\n"
            "### Tool list caching and change notifications\n"
            "\n"
            "The chapter notes that the SDK may cache discovered tools for a server-controlled TTL. A tool-list-changed notification "
            "can invalidate that cached view. This is another reason not to assume discovery is a one-time event for the entire life "
            "of an application.\n"
            "\n"
            "### Calling a tool\n"
            "\n"
            "The wrapper can call the SDK's `call_tool()` with a tool name and arguments. Importantly, tool results can contain more "
            "than plain text.\n"
            "\n"
            "The source describes these possible content types:\n"
            "\n"
            "- `TextContent`\n"
            "- `ImageContent`\n"
            "- `AudioContent`\n"
            "- `EmbeddedResource`\n"
            "\n"
            "A single call can return a **list** of content blocks. Your client or host must decide whether to normalize these blocks "
            "into a simpler representation or preserve native content types for the caller.\n"
            "\n"
            "That decision depends on your user. A generic SDK-like client should usually preserve flexibility; an application-specific "
            "client may prefer to normalize data for a fixed downstream model.\n"
            "\n"
            "### Progress and timeouts\n"
            "\n"
            "Long-running tools need good UX and failure boundaries. The chapter shows a progress callback that can receive progress, "
            "an optional total, and a message, allowing the host to display a progress indicator. It also notes a read timeout option "
            "for terminating calls that hang too long.\n"
            "\n"
            "[[IMAGE_NEEDED: Tool discovery and invocation sequence | "
            "A sequence diagram with Host → MCP Client → MCP Server for list_tools, then Host/LLM selecting one tool, MCP Client calling it, "
            "and the server returning one or more content blocks | "
            "Learner should notice that discovery happens before execution and that tool results may be multimodal or multi-part]]\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Turning tool access into an agentic tool-use loop\n"
            "\n"
            "Discovering and calling a tool is not yet the whole agent. The host must connect tool use back into the LLM conversation.\n"
            "\n"
            "A common tool loop looks like this:\n"
            "\n"
            "```text\n"
            "1. Send user request + available tool definitions to the LLM.\n"
            "2. Inspect the model response.\n"
            "3. If the model asks for one or more tools:\n"
            "      a. execute each requested tool through the MCP client,\n"
            "      b. package each result with the matching tool-use ID,\n"
            "      c. append tool results to conversation history,\n"
            "      d. call the LLM again.\n"
            "4. Repeat until the model returns a final response instead of another tool request.\n"
            "```\n"
            "\n"
            "This nested loop matters because one user task can require several dependent tool calls. A model may first calculate "
            "one value, inspect the result, and then call another tool before it can answer.\n"
            "\n"
            "### Simplified structure\n"
            "\n"
            "```python\n"
            "while True:\n"
            "    response = call_llm(messages=conversation_messages, tools=available_tools)\n"
            "\n"
            "    if response_requests_tools(response):\n"
            "        results = []\n"
            "        for request in extract_tool_requests(response):\n"
            "            result = await mcp_client.use_tool(\n"
            "                tool_name=request.name,\n"
            "                arguments=request.input,\n"
            "            )\n"
            "            results.append(build_tool_result(request.id, result))\n"
            "\n"
            "        conversation_messages.append(tool_results_message(results))\n"
            "        continue\n"
            "\n"
            "    print(extract_final_text(response))\n"
            "    break\n"
            "```\n"
            "\n"
            "The exact message format depends on the LLM API. What stays constant is the control flow: model chooses → host executes "
            "through MCP → result returns to model → model decides again.\n"
            "\n"
            "[[IMAGE_NEEDED: End-to-end MCP tool-use loop | "
            "A sequence diagram showing User → Host → LLM; LLM returns tool request; Host → MCP Client → MCP Server; tool result returns "
            "to Host; Host sends tool result back to LLM; LLM either asks for another tool or returns final text to User | "
            "Learner should notice that the model never executes the server function directly—the host and MCP client perform the call]]\n"
            "\n"
            "{{exercise:M02.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Error handling, retries, and disconnects\n"
            "\n"
            "Networked and subprocess-based systems fail. A production-quality MCP client should treat that as normal engineering, "
            "not an exceptional afterthought.\n"
            "\n"
            "The chapter says failed MCP calls raise `MCPError`, which carries an error code and message. Some errors can be transient, "
            "including connection-closed and request-timeout cases. That means the wrapper is a natural place to implement a retry policy.\n"
            "\n"
            "### Local stdio failure\n"
            "\n"
            "If a local stdio connection disappears unexpectedly, the subprocess may have crashed. Recovery can require starting a "
            "new session and possibly retrying the operation.\n"
            "\n"
            "### Remote Streamable HTTP failure\n"
            "\n"
            "Because Streamable HTTP is stateless in the chapter's model, a client could theoretically continue by issuing another "
            "request. The source nevertheless points out that using the same reconnect path for both transports has a benefit: it can "
            "refresh negotiated protocol-version information and reduce mismatch risk after a server upgrade.\n"
            "\n"
            "### `try/finally` for cleanup\n"
            "\n"
            "When an agent's run loop owns a client connection, wrapping the loop in `try/finally` ensures the client disconnects even "
            "when the user exits or an exception escapes.\n"
            "\n"
            "```python\n"
            "try:\n"
            "    await client.connect()\n"
            "    await run_agent_loop()\n"
            "finally:\n"
            "    await client.disconnect()\n"
            "```\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Using MCP resources as model context\n"
            "\n"
            "Tools let an agent **do** things. Resources give the host and model **data to reason over**.\n"
            "\n"
            "Resources can represent database records, text files, images, configuration files, documentation, and other server-provided "
            "data. The chapter introduces several resource operations:\n"
            "\n"
            "| Operation | Purpose |\n"
            "|---|---|\n"
            "| `resources/list` / `list_resources()` | Discover fixed resources |\n"
            "| `resources/templates/list` / `list_resource_templates()` | Discover URI templates for dynamically addressed resources |\n"
            "| `resources/read` / `read_resource()` | Read data from a specific resource URI |\n"
            "| listen/subscription behavior | React to resource-list or resource-content changes |\n"
            "\n"
            "### Resources vs resource templates\n"
            "\n"
            "A fixed resource has a concrete URI. A resource template has a URI pattern that is filled with values. The source notes "
            "that the two share similar descriptive metadata, but one carries `uri` while the other carries `uri_template`.\n"
            "\n"
            "### Resource wrapper methods\n"
            "\n"
            "The same discovery/use pattern applies again:\n"
            "\n"
            "```python\n"
            "async def get_available_resources(self):\n"
            "    ...\n"
            "    return (await self._client.list_resources()).resources\n"
            "\n"
            "async def get_resource(self, uri: str):\n"
            "    ...\n"
            "    return (await self._client.read_resource(uri=uri)).contents\n"
            "```\n"
            "\n"
            "The chapter intentionally returns resource content objects with minimal transformation so the consuming application can "
            "decide how to handle text, blobs, images, and other MIME types.\n"
            "\n"
            "### Resource selection is context engineering\n"
            "\n"
            "A host usually should not dump every available resource into every prompt. The source demonstrates one strategy: use an "
            "LLM to inspect the user query and a dictionary of resource names/descriptions, then return only the resources that appear "
            "relevant.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Available resource metadata\n"
            "        +\n"
            "User request\n"
            "        ↓\n"
            "Resource selector\n"
            "        ↓\n"
            "Selected resource names\n"
            "        ↓\n"
            "Read selected URIs\n"
            "        ↓\n"
            "Inject contents into model context\n"
            "```\n"
            "\n"
            "The chapter validates selected names against the known resource dictionary. This simple guard helps avoid accepting an "
            "LLM-hallucinated resource name.\n"
            "\n"
            "### Other valid selection strategies\n"
            "\n"
            "The source explicitly notes that an LLM selector is only one possible UX. Alternatives include:\n"
            "\n"
            "- user file/resource pickers,\n"
            "- a specialized system prompt containing resource metadata,\n"
            "- resource-template driven retrieval,\n"
            "- loading a small stable set of resources up front,\n"
            "- prompt caching for static context.\n"
            "\n"
            "The key tradeoff is between relevance, latency, extra model calls, token cost, and user control.\n"
            "\n"
            "### Injecting selected resources\n"
            "\n"
            "Text resources can be inserted as additional content blocks alongside the user's message. Image blobs can be converted "
            "into the representation required by a multimodal model if the MIME type is supported.\n"
            "\n"
            "The chapter makes an important message-structure point: additional context should be bundled into the same logical user "
            "message content structure rather than pretending each piece of context is a new user turn.\n"
            "\n"
            "[[IMAGE_NEEDED: Intelligent MCP resource loading | "
            "A flow diagram showing user query plus available resource descriptions feeding a selector, selected names mapped to URIs, "
            "resources loaded through MCP, then relevant text/image context attached to the user's message | "
            "Learner should notice that resource discovery, selection, reading, and prompt injection are separate steps]]\n"
            "\n"
            "{{exercise:M02.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Discovering and using MCP prompts\n"
            "\n"
            "Prompts are the third major MCP primitive. In the source chapter, prompts are deliberately **user-controlled**: the "
            "application can show the user available prompts and let the user choose one.\n"
            "\n"
            "A prompt definition can include:\n"
            "\n"
            "- a unique name,\n"
            "- an optional description,\n"
            "- zero or more arguments,\n"
            "- whether each argument is required.\n"
            "\n"
            "### Dynamic prompts\n"
            "\n"
            "A hard-coded prompt such as:\n"
            "\n"
            "```text\n"
            "Review this Python code for bugs: ...\n"
            "```\n"
            "\n"
            "is less reusable than a parameterized prompt such as:\n"
            "\n"
            "```text\n"
            "Review the following {language} code for bugs and style issues:\n"
            "{code}\n"
            "```\n"
            "\n"
            "The host gathers values for `language` and `code`, then calls `get_prompt()` with those arguments. The server returns "
            "filled prompt messages that are ready to place into the LLM conversation after any required conversion.\n"
            "\n"
            "### Discovery and load wrappers\n"
            "\n"
            "The same pattern appears again:\n"
            "\n"
            "```python\n"
            "async def get_available_prompts(self):\n"
            "    ...\n"
            "    return (await self._client.list_prompts()).prompts\n"
            "\n"
            "async def load_prompt(self, name, arguments):\n"
            "    ...\n"
            "    result = await self._client.get_prompt(name=name, arguments=arguments)\n"
            "    return result.messages\n"
            "```\n"
            "\n"
            "### Host-side prompt UX\n"
            "\n"
            "The source builds a small flow where the host:\n"
            "\n"
            "1. displays prompt names and descriptions,\n"
            "2. shows arguments and whether they are required,\n"
            "3. collects values from the user,\n"
            "4. loads the filled prompt from the MCP server,\n"
            "5. converts supported prompt content into LLM conversation messages.\n"
            "\n"
            "This is a good example of the boundary between MCP and application UX. MCP exposes the prompt definition; the host decides "
            "how the user discovers, selects, and fills it.\n"
            "\n"
            "### Prompt content types and roles\n"
            "\n"
            "Prompt messages can contain more than text. The source notes text, image, audio, and embedded-resource content types. "
            "An application may choose to support only a subset, but it should do so deliberately and log or reject unsupported types.\n"
            "\n"
            "The prompt message also carries a role. A subtle warning from the chapter is that some model APIs cannot begin a "
            "conversation with an assistant-role message. A host must therefore validate or adapt prompt roles to the model API it uses.\n"
            "\n"
            "[[IMAGE_NEEDED: Dynamic MCP prompt lifecycle | "
            "A diagram showing list_prompts → user selects prompt → host collects required arguments → get_prompt(name, arguments) → "
            "server returns PromptMessage objects → host converts them into model conversation messages | "
            "Learner should notice that MCP supplies the prompt definition while the host owns argument collection and presentation]]\n"
            "\n"
            "---\n"
            "\n"
            "## 11. Design principles for a strong MCP client\n"
            "\n"
            "The chapter's code examples are intentionally small, but several broader engineering principles emerge.\n"
            "\n"
            "### 11.1 Keep the client model-agnostic when possible\n"
            "\n"
            "MCP is not limited to one model provider. If the wrapper translates MCP tools/resources/prompts into provider-neutral "
            "internal objects first, the host can later add adapters for different LLM APIs.\n"
            "\n"
            "### 11.2 Filter capabilities deliberately\n"
            "\n"
            "A client does not have to expose every server capability to the model. Capability filtering can improve safety, UX, "
            "and tool-choice quality.\n"
            "\n"
            "### 11.3 Separate protocol concerns from application concerns\n"
            "\n"
            "The MCP client should manage protocol communication. The host or agent layer should own user interaction, model-specific "
            "conversation logic, and business rules unless you have a clear reason to place those in the wrapper.\n"
            "\n"
            "### 11.4 Preserve useful type information\n"
            "\n"
            "Over-normalizing content too early can remove information the application needs. A generic client may return MCP-native "
            "resource or content objects; a specialized client may safely simplify them when all consumers have the same expectations.\n"
            "\n"
            "### 11.5 Build for failure\n"
            "\n"
            "Connection checks, timeouts, retries, logging, and guaranteed cleanup are normal software engineering requirements. "
            "Agentic software does not remove them.\n"
            "\n"
            "### 11.6 Refresh mutable server capabilities\n"
            "\n"
            "Tools, resources, and prompts can change. TTLs, list-change notifications, refresh commands, and explicit rediscovery "
            "all help prevent the host from operating on stale capability metadata.\n"
            "\n"
            "### 11.7 Watch the cost of context-selection strategies\n"
            "\n"
            "Using an extra LLM call to select resources can improve relevance, but it adds cost and latency. Context engineering "
            "should consider both model quality and system efficiency.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'The LLM provider SDK client is the MCP client.'\n"
            "\n"
            "**Why this is wrong:** the provider client communicates with the language model API. The MCP client communicates with an "
            "MCP server. The host application coordinates both.\n"
            "\n"
            "### Misconception 2: 'One MCP client instance can talk to every server.'\n"
            "\n"
            "**Why this is wrong:** in the source chapter's design, one client instance is associated with one server connection. Multiple "
            "servers therefore require multiple client instances.\n"
            "\n"
            "### Misconception 3: 'Calling `list_tools()` once is enough forever.'\n"
            "\n"
            "**Why this is wrong:** server capabilities can change, caches can expire, and change notifications can invalidate previous lists.\n"
            "\n"
            "### Misconception 4: 'Tool results are always strings.'\n"
            "\n"
            "**Why this is wrong:** tool calls may return text, images, audio, embedded resources, or several content blocks.\n"
            "\n"
            "### Misconception 5: 'A tool call should immediately be shown to the user.'\n"
            "\n"
            "**Why this is wrong:** in an agentic loop, tool results normally return to the LLM first so it can decide whether more "
            "actions are needed and produce the final user-facing response.\n"
            "\n"
            "### Misconception 6: 'More context should always be loaded.'\n"
            "\n"
            "**Why this is wrong:** irrelevant resources consume tokens and can make reasoning worse. Resource loading is a relevance, "
            "latency, and cost tradeoff.\n"
            "\n"
            "### Misconception 7: 'MCP removes the need for ordinary software security.'\n"
            "\n"
            "**Why this is wrong:** API keys, authentication, transport security, origin validation, timeouts, and safe cleanup still matter.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Host application | LLM-powered application that contains one or more MCP clients |\n"
            "| LLM provider client | SDK/client used to communicate with a model provider's API |\n"
            "| MCP client | Component that communicates with an MCP server and exposes its capabilities to the host |\n"
            "| Client wrapper | Application-specific class placed around the SDK client for guardrails, translation, logging, and lifecycle control |\n"
            "| stdio | Local transport using a server subprocess's standard input/output |\n"
            "| Streamable HTTP | Stateless remote transport for communicating with hosted MCP servers |\n"
            "| `AsyncExitStack` | Python utility for dynamically managing multiple asynchronous context managers and cleanup |\n"
            "| Capability discovery | Listing the tools, resources, prompts, or other features a server provides |\n"
            "| Tool | Executable server capability that the model can choose to call |\n"
            "| `input_schema` | Structured definition of arguments a tool accepts |\n"
            "| Tool-use loop | Repeated LLM → tool call → result → LLM cycle until the model produces a final answer |\n"
            "| Progress callback | Async function invoked when a long-running tool reports progress |\n"
            "| MCPError | Error type described by the source for failed MCP calls, including code and message information |\n"
            "| Resource | Server-provided data addressable by a URI |\n"
            "| Resource template | URI pattern that can be filled dynamically to identify resources |\n"
            "| Resource selection | Process of choosing which resources are relevant enough to load into context |\n"
            "| Prompt | Server-provided reusable model message definition |\n"
            "| Dynamic prompt | Prompt whose placeholders are filled from arguments supplied by the user or application |\n"
            "| Capability filtering | Choosing which server-provided features the host will actually expose |\n"
            "| Model agnosticism | Designing the client so it can support more than one LLM provider |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What makes a normal LLM application an MCP host application?\n"
            "2. What is the difference between an LLM API client and an MCP client?\n"
            "3. Why might you wrap the SDK Client class in your own `MCPClient` class?\n"
            "4. Why does the source use one MCP client instance per server?\n"
            "5. When would you choose stdio over Streamable HTTP?\n"
            "6. Why is `AsyncExitStack` useful for MCP client lifecycle management?\n"
            "7. What are the discovery and use steps for tools?\n"
            "8. Why must `call_tool()` results be treated as a list of content blocks?\n"
            "9. How does the nested tool-use loop make the application agentic?\n"
            "10. What kinds of failures should trigger retry or reconnect logic?\n"
            "11. What is the difference between a resource and a resource template?\n"
            "12. Why might an LLM-based resource selector be useful, and what does it cost?\n"
            "13. What information can an MCP prompt definition contain?\n"
            "14. Why should the host inspect prompt roles and content types before sending them to a model API?\n"
            "15. Why are capability filtering and model agnosticism useful client features?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**An MCP client is not just a network connector. It is the host application's control boundary for discovering server "
            "capabilities, translating them for the model, managing connection lifecycle, executing actions, loading context, handling "
            "failures, and deciding which capabilities the agent is actually allowed to use.**\n"
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "host-app",
                "title": "From an ordinary LLM app to an MCP host",
                "order": 1,
            },
            {
                "id": "client-responsibilities",
                "title": "What an MCP client is responsible for",
                "order": 2,
            },
            {
                "id": "transport-choice",
                "title": "Choosing the transport",
                "order": 3,
            },
            {
                "id": "async-lifecycle",
                "title": "Managing asynchronous client lifecycle",
                "order": 4,
            },
            {
                "id": "discovery-use",
                "title": "The discover-then-use pattern",
                "order": 5,
            },
            {
                "id": "tools",
                "title": "Discovering and calling tools",
                "order": 6,
            },
            {
                "id": "tool-loop",
                "title": "Turning tool access into an agentic tool-use loop",
                "order": 7,
            },
            {
                "id": "errors",
                "title": "Error handling, retries, and disconnects",
                "order": 8,
            },
            {
                "id": "resources",
                "title": "Using MCP resources as model context",
                "order": 9,
            },
            {
                "id": "prompts",
                "title": "Discovering and using MCP prompts",
                "order": 10,
            },
            {
                "id": "client-design",
                "title": "Design principles for a strong MCP client",
                "order": 11,
            },
        ],
    },

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Choose the Right MCP Transport",

            "lesson_code": "M02.L01",

            "section_id": "transport-choice",

            "placement": "after_section",

            "description": (
                "Practice selecting stdio or Streamable HTTP based on how an MCP "
                "server is deployed and operated."
            ),

            "instructions": (
                "For each scenario, choose stdio or Streamable HTTP and justify your answer.\n\n"
                "1. A developer installs a local filesystem MCP server that should run only while their IDE is open.\n"
                "2. A SaaS company operates one centrally managed MCP endpoint for thousands of customers.\n"
                "3. A local coding assistant launches a Python calculator server from the same project folder.\n"
                "4. An enterprise hosts an authenticated internal ticketing MCP service in its private network.\n"
                "5. For one remote case, identify two security concerns the client/server design must address."
            ),

            "expected_output": (
                "A table with scenario, selected transport, justification, and security notes "
                "for at least one Streamable HTTP scenario."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "transport-selection",
                "mcp-architecture",
                "security-reasoning",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Trace a Multi-Tool Agent Loop",

            "lesson_code": "M02.L01",

            "section_id": "tool-loop",

            "placement": "after_section",

            "description": (
                "Trace the complete message flow when an LLM needs more than one MCP "
                "tool call before it can answer the user."
            ),

            "instructions": (
                "A calculator MCP server exposes multiply_two_numbers and add_two_numbers. "
                "The user asks: 'What is 5 × 3 + 7?'\n\n"
                "1. Write the initial message sent to the LLM conceptually.\n"
                "2. Show the first tool request the LLM might produce.\n"
                "3. Show how the host sends that request through the MCP client.\n"
                "4. Show the tool result returning to the conversation history.\n"
                "5. Repeat for the second tool call.\n"
                "6. Show the final stage where the LLM returns the answer rather than another tool request.\n"
                "7. Explain why the nested loop is necessary."
            ),

            "expected_output": (
                "A numbered trace or sequence diagram containing User, Host, LLM, MCP Client, "
                "MCP Server, two tool requests/results, and the final response."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tool-calling",
                "agent-loop",
                "conversation-state",
                "mcp-client",
            ],
        },

        {
            "id": "M02.L01.EX03",

            "title": "Design Resource Selection for an Agent",

            "lesson_code": "M02.L01",

            "section_id": "resources",

            "placement": "after_section",

            "description": (
                "Design a context-loading strategy that gives the model relevant MCP resources "
                "without loading everything into every prompt."
            ),

            "instructions": (
                "Imagine an engineering assistant has these resources: architecture.md, "
                "deployment-guide.md, incident-log.txt, and a build-artifact image.\n\n"
                "1. For the question 'How should I deploy this service?', select the likely relevant resource(s).\n"
                "2. For the question 'What failed in yesterday's deployment?', select the likely relevant resource(s).\n"
                "3. Propose one selection strategy: user picker, LLM selector, deterministic routing, or another strategy.\n"
                "4. Explain the latency/token-cost tradeoff of your strategy.\n"
                "5. Describe how text and image resources should be represented when added to the user's message.\n"
                "6. Explain how you would reject a hallucinated resource name."
            ),

            "expected_output": (
                "A short resource-selection design with per-query choices, the selection mechanism, "
                "context-injection format, and one hallucination guardrail."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "mcp-resources",
                "context-engineering",
                "resource-selection",
                "guardrails",
            ],
        },
    ],

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Building MCP Clients — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",

                "section_id": "host-app",

                "question": "What turns an ordinary LLM-powered application into an MCP host application?",

                "options": [
                    "It fine-tunes its own language model.",
                    "It hosts one or more MCP clients that communicate with MCP servers.",
                    "It stores every prompt in a vector database.",
                    "It must run an MCP server inside the same Python process.",
                ],

                "correct": 1,

                "explanation": (
                    "The host remains the user-facing LLM application, but it becomes an MCP host "
                    "by containing MCP client code that connects to servers."
                ),
            },

            {
                "id": "M02.L01.Q02",

                "section_id": "client-responsibilities",

                "question": "Why does the chapter wrap the SDK Client in an application-specific MCPClient class?",

                "options": [
                    "Because the SDK Client cannot connect to servers.",
                    "To add lifecycle control, guardrails, logging, translation, retries, and custom processing.",
                    "Because MCP requires every client to use the same class name.",
                    "To replace asynchronous code with synchronous networking.",
                ],

                "correct": 1,

                "explanation": (
                    "The wrapper is an application design layer. It lets the host add behavior around "
                    "the SDK without changing the protocol itself."
                ),
            },

            {
                "id": "M02.L01.Q03",

                "section_id": "transport-choice",

                "question": "Which transport is the better default match for a locally launched MCP server subprocess?",

                "options": [
                    "stdio",
                    "Streamable HTTP",
                    "FTP",
                    "SMTP",
                ],

                "correct": 0,

                "explanation": (
                    "stdio is designed for local server processes and communicates through their "
                    "standard input/output streams."
                ),
            },

            {
                "id": "M02.L01.Q04",

                "section_id": "async-lifecycle",

                "question": "What is the main benefit of AsyncExitStack in the client design?",

                "options": [
                    "It converts tools into prompts.",
                    "It dynamically manages asynchronous contexts and lets the application clean them up together.",
                    "It automatically selects the best MCP resource.",
                    "It removes the need for disconnect logic.",
                ],

                "correct": 1,

                "explanation": (
                    "AsyncExitStack helps the application enter and later unwind async context managers "
                    "in a controlled way, which is useful for connection/resource lifecycle management."
                ),
            },

            {
                "id": "M02.L01.Q05",

                "section_id": "tools",

                "question": "Why should a tool call result be treated as a collection of content blocks?",

                "options": [
                    "Because every tool must return exactly four strings.",
                    "Because a tool result can contain text, images, audio, embedded resources, or multiple pieces of content.",
                    "Because MCP does not allow plain text results.",
                    "Because tool outputs are always resource templates.",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes several supported content types and notes that a single call "
                    "can return multiple content objects."
                ),
            },

            {
                "id": "M02.L01.Q06",

                "section_id": "tool-loop",

                "question": "What should happen after the model requests an MCP tool and the tool returns a result?",

                "options": [
                    "The host should always print the raw tool result immediately and stop.",
                    "The result should normally be added to conversation history and sent back to the model for the next decision.",
                    "The MCP server should directly answer the user without involving the host.",
                    "The model should forget the original user request.",
                ],

                "correct": 1,

                "explanation": (
                    "Returning the tool result to the model closes the action-feedback loop and lets "
                    "the model decide whether it needs another tool or can produce the final answer."
                ),
            },

            {
                "id": "M02.L01.Q07",

                "section_id": "errors",

                "question": "Why might a client intentionally reconnect after a transient Streamable HTTP failure?",

                "options": [
                    "Because Streamable HTTP permanently stores no URL.",
                    "To use the same recovery path as stdio and refresh negotiated protocol information.",
                    "Because HTTP requests cannot be retried.",
                    "Because reconnecting converts the server into a local process.",
                ],

                "correct": 1,

                "explanation": (
                    "The source notes that a stateless HTTP request could simply be retried, but a reconnect "
                    "path can refresh protocol-version information and simplify recovery logic across transports."
                ),
            },

            {
                "id": "M02.L01.Q08",

                "section_id": "resources",

                "question": "What is the main purpose of selecting only relevant MCP resources for a user request?",

                "options": [
                    "To force every resource to become a tool.",
                    "To control context relevance, token usage, latency, and cost.",
                    "To eliminate resource URIs.",
                    "To prevent the model from ever seeing external data.",
                ],

                "correct": 1,

                "explanation": (
                    "Selective loading is a context-engineering decision. Loading everything can waste "
                    "tokens and introduce irrelevant information, while selection itself may add latency or cost."
                ),
            },

            {
                "id": "M02.L01.Q09",

                "section_id": "prompts",

                "question": "What makes an MCP prompt dynamic?",

                "options": [
                    "It is automatically converted into a tool.",
                    "It contains arguments/placeholders that the host fills with values when loading it.",
                    "It can only contain assistant-role messages.",
                    "It is stored as an HTTP header.",
                ],

                "correct": 1,

                "explanation": (
                    "Dynamic prompts define arguments such as language or code and are filled when the "
                    "application calls get_prompt() with argument values."
                ),
            },

            {
                "id": "M02.L01.Q10",

                "section_id": "client-design",

                "type": "open",

                "question": (
                    "Design a robust MCP client for an application that must support both a local stdio "
                    "server and a remote Streamable HTTP server. Explain your lifecycle strategy, discovery "
                    "strategy, error handling, capability filtering, and how you would keep the client model-agnostic."
                ),
            },
        ],

        "passing_score": 70,
    },
}
