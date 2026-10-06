"""M01.L07 — Model Context Protocol: Architecture and Implementation.

Two source chapters -> one complete learner-facing lesson.

Source alignment:
- Chapter 10: The Model Context Protocol (MCP): Standardizing Tool Interaction
- Chapter 11: Implementing MCP-Enabled Agents and Tool Servers

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L07"
MODULE_ORDER = 1
MODULE_TITLE = "Model Context Protocol: Architecture & Implementation"
MODULE_DESCRIPTION = (
    "Learn why hard-wired tool integrations fail at scale, how MCP separates Hosts, "
    "Clients, and Servers, how MCP primitives standardize tools/data/prompts and "
    "bidirectional assistance, and how to build a complete MCP-enabled Financial Analyst "
    "using FastMCP, ADK MCPToolset, Stdio, multimodal responses, and MCP Inspector."
)
SOURCE_CHAPTER = "10-11"
SOURCE_PAGES = "Early Release drafts; page numbers not provided"

TOPIC = {
    "title": "Model Context Protocol: Architecture and Implementation",
    "slug": "agent-foundations-m01-l07",
    "description": (
        "Move from brittle, vendor-locked tool wiring to a reusable MCP ecosystem. "
        "Understand the architecture and primitives, then implement a real MCP Server "
        "and Host integration with dynamic tool discovery, multimodal content, debugging, "
        "security boundaries, and transport selection."
    ),
    "order": 7,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 6.0,
    "skill_tags": [
        "mcp",
        "model-context-protocol",
        "tool-integration",
        "host-client-server",
        "mcp-tools",
        "mcp-resources",
        "mcp-prompts",
        "mcp-sampling",
        "mcp-elicitation",
        "stdio",
        "streamable-http",
        "fastmcp",
        "mcp-toolset",
        "dynamic-tool-discovery",
        "json-rpc",
        "multimodal-tools",
        "mcp-inspector",
        "tool-security",
        "agent-architecture",
    ],
    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03", "M01.L04", "M01.L05", "M01.L06"],

    "lesson": {
        "title": "Model Context Protocol: Architecture and Implementation",
        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Model Context Protocol: Architecture and Implementation

> **Lesson:** M01.L07  
> **Source alignment:** Chapters 10 and 11 of the supplied Early Release material.  
> This lesson merges the theory and hands-on implementation into one continuous learning path.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a few hard-coded tools can become unmanageable at production scale.
- Describe the four pre-MCP dilemmas emphasized by the source.
- Explain how vendor-specific function-calling APIs create implementation-level lock-in.
- Explain why structured function calling does not by itself solve sandboxing, orchestration, or dynamic discovery.
- Describe the MCP Host, Client, and Server roles.
- Explain why one Host creates a dedicated Client for each connected Server.
- Trace runtime discovery from configuration through `tools/list` to an aggregated toolset.
- Explain how MCP enables a plug-and-play capability model.
- Distinguish MCP Tools, Resources, and Prompts.
- Explain why Tools are model-controlled, Resources are application-controlled, and Prompts are user-controlled in the source's framing.
- Explain MCP Sampling as a Server asking the Host to borrow central model reasoning.
- Explain Elicitation as a Server pausing to request structured user input.
- Compare Stdio and Streamable HTTP as local and remote MCP transports.
- Explain why Stdio is convenient for local tools and why remote services need stronger network security.
- Build a simple MCP Server conceptually with FastMCP.
- Explain how decorators, type hints, and docstrings become model-facing JSON schemas.
- Explain the role of ADK's source-described `MCPToolset`.
- Trace the MCP handshake: launch, initialize, list tools, adapt.
- Explain how dynamic discovery removes the need to manually duplicate tool schemas in the Host.
- Trace a user request from ADK Runner through MCPToolset to an isolated server process and back.
- Explain how an MCP Server can return image content and how a multimodal Host/agent can consume it.
- Explain why user interfaces may need to intercept tool-result events to render binary/media output directly.
- Use the MCP Inspector conceptually to isolate and debug a Server before integrating it with the Host.
- Explain why arbitrary `print()` output can corrupt a stdio protocol stream.
- Apply source-described security practices for subprocess commands and environment variables.
- Choose between Stdio and remote HTTP-style transports based on deployment topology.
- Explain the "write once, use everywhere" promise of a standardized tool server.

---

## 1. Why MCP exists

Earlier lessons showed how an agent can call a Python function.

For a small prototype, this can be enough:

```text
Agent
  ↓
get_weather()
  ↓
Weather API
```

The problem appears when the system grows.

Imagine an agent with:

```text
10 tools
50 tools
100 tools
```

Each tool may have:

- its own API,
- credentials,
- error handling,
- schema,
- network rules,
- security requirements.

The source frames MCP as the transition from:

```text
isolated custom integrations
```

to:

```text
a standardized capability ecosystem
```

The goal is not merely to make tool calling prettier.

It is to separate:

```text
agent intelligence
```

from:

```text
tool implementation and connectivity
```

[[IMAGE_NEEDED: Hard-wired agent vs MCP ecosystem | Left: one agent directly wired to many APIs/tools with tangled connections; right: Host connected through MCP Clients to independent Git, Filesystem, GitHub, Weather servers | Learner should see how the standardized boundary removes direct coupling]]

---

## 2. Four scaling dilemmas before MCP

The source highlights four major problems.

### 2.1 Glue Code Monolith

Every tool adds routing logic.

Conceptually:

```python
if tool == "weather":
    ...
elif tool == "music":
    ...
elif tool == "lights":
    ...
```

As tools grow, the central application becomes tightly coupled to all of them.

### 2.2 Security Nightmare

Structured tool requests do not make execution safe.

If the model requests:

```text
execute_python(...)
```

the application still needs:

- sandboxing,
- permission checks,
- isolation,
- approval.

### 2.3 Ad-Hoc State Machine

Multi-step tool workflows often become a manual loop:

```text
call model
inspect tool request
execute tool
append result
call model again
repeat
```

This becomes difficult to maintain as complexity grows.

### 2.4 Static Toolset

If tools are compiled directly into agent code:

```python
tools = [GitTool(), GitHubTool()]
```

adding another capability requires:

1. editing agent code,
2. modifying the tool list,
3. redeploying the application.

That is not a true plug-in architecture.

---

## 3. The brittle monolithic tool

The source first examines the tool itself.

A weather function may contain:

```text
API endpoint
API key
provider-specific JSON parsing
provider-specific errors
```

This creates three problems.

### Brittleness

If the provider changes its response schema, the function breaks.

### Lack of scalability

Every new external capability gets another custom implementation.

### Inflexibility

The application becomes implicitly tied to the provider.

A standardized Server boundary improves this.

The agent should only care:

```text
There is a tool called get_weather.
```

The Server can decide internally which provider implements it.

---

## 4. Vendor lock-in around function calling

Native function calling improved agent reliability because the model can emit structured tool requests.

But model providers expose those requests differently.

One provider might expose:

```text
response.choices[...].tool_calls
```

another:

```text
response.content[...] type=tool_use
```

Even when the conceptual tool request is identical, application code may need to change.

This means there are two kinds of coupling:

```text
Agent ↔ Tools
Agent ↔ LLM provider API
```

MCP aims to standardize the Host-to-tool side so the Host can act as a universal adapter.

---

## 5. Why function calling alone is not enough

Function calling solves:

```text
How does the model express a structured request?
```

It does not automatically solve:

```text
How do tools get discovered?
How are they routed?
How are they sandboxed?
How is state managed?
How can new tools be added dynamically?
How can one tool ecosystem work across model vendors?
```

This distinction is important.

> Function calling is one part of the interaction. MCP defines a broader communication architecture around capabilities.

{{exercise:M01.L07.EX01}}

---

## 6. MCP architecture: Host, Client, Server

The source describes three core roles.

### Host

The trusted main application.

Examples in the source's framing include:

- desktop AI app,
- IDE extension,
- custom agent framework.

The Host:

- runs orchestration,
- manages model interaction,
- manages user state,
- decides when tasks are complete,
- enforces security,
- reads Server configuration.

### Server

A specialist capability provider.

Examples:

```text
Git Server
Filesystem Server
GitHub Server
Stock Data Server
```

A Server should focus on one capability domain.

### Client

A protocol component living inside the Host.

The Host creates a dedicated Client for each Server.

Conceptually:

```text
Host
├── Client A -> Git Server
├── Client B -> Filesystem Server
└── Client C -> GitHub Server
```

[[IMAGE_NEEDED: MCP Host-Client-Server architecture | Central Host containing multiple dedicated Client connections, each connected one-to-one to a separate MCP Server | Learner should notice that Clients live inside the Host and isolate Server connections]]

---

## 7. The Host is the trusted orchestrator

The Host absorbs responsibilities that were previously scattered through custom code.

### Runs the orchestration engine

It can manage:

```text
conversation state
model calls
tool loop
termination
```

### Enforces security

A Server can request a sensitive action.

The Host can decide:

```text
allow?
deny?
ask user?
```

This centralizes trust.

### Manages configuration

The Host knows which Servers are connected.

This is what allows capabilities to become configurable rather than compiled into agent source code.

---

## 8. The Server is the tool specialist

A Server should be independent from the agent's model logic.

Example:

```text
Stock Server
```

knows:

```text
stock prices
company metadata
financial API details
```

It should not need to know:

```text
which LLM is being used
what the user's conversation history contains
how the Host orchestrates the task
```

This separation means the same Server can potentially serve many Hosts.

---

## 9. The Client is the secure communication channel

The Client lives inside the Host.

The source emphasizes a one-to-one relationship:

```text
one Client
    ↔
one Server
```

Why is this useful?

Because:

```text
Git Client
```

does not automatically gain access to:

```text
GitHub Server
Filesystem Server
```

This reduces cross-server coupling.

It also gives the Host clearer control over which capabilities are connected.

---

## 10. Plug-and-play capability discovery

The source moves capabilities out of the agent's hard-coded tool list and into configuration.

Conceptually:

```json
{
  "mcpServers": {
    "git": {"command": "python git_server.py"},
    "github": {"command": "python github_server.py"}
  }
}
```

At runtime:

```text
1. Host reads configuration
2. Host launches/connects to Servers
3. Host creates a Client per Server
4. Host asks each Server for available tools
5. Host aggregates all discovered capabilities
6. Host provides them to the model
```

To add a capability:

```text
start/configure another Server
```

rather than:

```text
rewrite core agent code
```

[[IMAGE_NEEDED: MCP dynamic discovery sequence | Config file -> Host launches Servers -> dedicated Clients -> tools/list requests -> discovered tool schemas -> aggregated toolset -> LLM | Learner should see why new tools no longer require editing the agent's core source]]

---

## 11. MCP primitives: the shared language

Architecture tells us who communicates.

Primitives define what they communicate about.

The source divides primitives into two directions.

### Server primitives

What a Server offers to the Host:

```text
Tools
Resources
Prompts
```

### Client-side requests from Server

What a Server can ask the Host for:

```text
Sampling
Elicitation
```

This makes MCP bidirectional.

---

## 12. Tools: the agent's hands

A Tool represents executable behavior.

The Server exposes:

```text
name
description
JSON Schema
```

The model may decide to use it.

The Host receives a provider-specific tool request and translates it into a standardized MCP call.

Conceptually:

```text
LLM-specific request
     ↓
Host adapter
     ↓
tools/call
     ↓
Server
```

This decouples Server implementation from the model vendor.

### Source control model

The source frames Tools as:

```text
model-controlled
```

because the model may choose when to invoke them.

---

## 13. Resources: the agent's library

A Resource is passive data.

Examples:

```text
file://...
git://...
database-like URI
```

Resources are discoverable by the Host.

The Host decides:

```text
which resource to read
when to read it
how much to include
```

The source therefore frames Resources as:

```text
application-controlled
```

### Why this matters for context windows

A Server should not dump huge amounts of data automatically.

The Host can use retrieval strategies such as:

```text
search
RAG
metadata filtering
```

then fetch only relevant content.

This keeps context efficient.

---

## 14. Prompts: the agent's playbook

An MCP Server can expose reusable parameterized prompts.

Examples:

```text
Generate Unit Test
Plan Vacation
Review Pull Request
```

A Host can surface these as:

- buttons,
- slash commands,
- forms.

The user chooses the workflow.

The source therefore frames Prompts as:

```text
user-controlled
```

The Server can return a pre-defined sequence of messages after the user supplies parameters.

---

## 15. Model-controlled, application-controlled, user-controlled

This is a useful way to remember the three main Server offerings.

| Primitive | Primary control in source framing | Purpose |
|---|---|---|
| Tool | Model | Execute an action |
| Resource | Host/application | Read contextual data |
| Prompt | User | Start a reusable workflow |

This separation helps prevent conceptual confusion.

[[IMAGE_NEEDED: MCP primitive control triad | Three columns: Tool -> model-controlled -> action; Resource -> application-controlled -> data; Prompt -> user-controlled -> workflow | Learner should associate each primitive with who initiates its use]]

{{exercise:M01.L07.EX02}}

---

## 16. Sampling: a Server borrows the Host's reasoning

Sampling is one of the most interesting MCP primitives.

A Server may be good at:

```text
fetching data
performing API operations
```

but not contain its own LLM.

Suppose a Flight Server retrieves 50 flights.

It can fetch the data.

But deciding which flight is "best" may require reasoning.

Instead of embedding another model inside the Server, it can ask the Host for help.

### Nested-conversation mental model

Conversation 1:

```text
Host -> Server:
find_best_flight(...)
```

Server fetches 50 options.

Then Conversation 2:

```text
Server -> Host:
Please reason over these 50 options.
```

The Host uses its central LLM.

It returns a recommendation.

The Server resumes Conversation 1 and returns the final tool result.

This keeps:

```text
intelligence
cost control
security control
```

centralized in the Host.

---

## 17. Sampling step by step

### Original tool call

```text
Host
  ↓
tools/call: find_best_flight
  ↓
Flight Server
```

### Server encounters reasoning need

It has:

```text
50 raw flights
```

but needs comparative judgment.

### Server requests sampling

Conceptually:

```text
sampling/createMessage
```

with:

- messages,
- system guidance,
- data to analyze.

### Host decides whether to allow

The Host remains the trust boundary.

It can potentially:

- inspect request,
- ask user,
- enforce policy.

### Host LLM reasons

Returns:

```text
Flight UA245 is the best balance...
```

### Server resumes original tool call

It returns a final structured tool result.

[[IMAGE_NEEDED: Nested MCP Sampling flow | Outer flow Host -> Flight Server tools/call; inside it, Server -> Host sampling/createMessage -> Host LLM -> reasoning result -> Server -> final tools/call response | Learner should see two nested conversations inside one apparent tool call]]

---

## 18. Elicitation: ask the user for missing information

Sometimes a Server cannot proceed because required input is missing.

Example:

```text
Create a GitHub issue
```

but no repository is specified.

Rather than failing, the Server can request structured input.

Conceptually:

```text
elicitation/create
```

with:

- user-facing message,
- requested schema.

The Host renders a UI element.

The user provides data.

The Host validates and returns it.

Then the Server resumes.

This supports:

```text
pause
ask
validate
resume
```

without embedding UI logic inside the Server.

---

## 19. MCP transport layer

Primitives define what is communicated.

Transport defines how bytes/messages move.

The source presents two main transport styles:

```text
Stdio
Streamable HTTP
```

---

## 20. Stdio for local communication

With Stdio:

```text
Host launches Server as child process
```

Then:

```text
Host -> Server stdin
Server -> Host stdout
```

Advantages:

- simple,
- fast,
- no network port,
- useful for local tools.

Good fits:

- desktop agents,
- coding assistants,
- local Git operations,
- filesystem tools,
- local databases.

### Security advantage

Communication stays on the local machine.

There is no exposed TCP port just to connect the Host and Server.

---

## 21. Streamable HTTP for remote capabilities

For remote Servers:

```text
Host
  ↓ HTTPS
Remote MCP Server
```

Good fits:

- SaaS integrations,
- corporate services,
- cloud microservices,
- shared knowledge servers.

The source discusses HTTP POST plus streaming mechanisms for server-originated updates.

Remote transports require stronger attention to:

- authentication,
- authorization,
- TLS,
- multi-client handling,
- network failures.

[[IMAGE_NEEDED: Stdio vs remote MCP transport | Left: Host launches local Server subprocess and exchanges stdin/stdout; right: Host connects over HTTPS to remote shared MCP Server | Learner should understand local-process vs network-service deployment]]

---

## 22. Practical system: the Financial Analyst

Chapter 11 implements the architecture.

The scenario contains two isolated applications.

### Stock Data Server

Responsibilities:

```text
financial data only
```

It knows nothing about:

- agent persona,
- conversation state,
- LLM prompting.

### ADK Host/Agent

Responsibilities:

```text
reasoning
conversation
user interaction
tool orchestration
```

It contains no stock-data implementation.

The bridge is the source-described:

```text
MCPToolset
```

This gives us an important architecture:

```text
Agent intelligence
    separated from
Financial capability implementation
```

---

## 23. Build the Server with FastMCP

The source uses the official Python MCP SDK and its high-level `FastMCP` interface.

Conceptually:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Stock Data Server")
```

Then ordinary Python functions can be exposed as MCP capabilities.

The exact import paths and decorators are version-specific.

The durable idea is:

> Server frameworks can generate MCP schemas from ordinary typed Python functions.

---

## 24. Expose a Python function as an MCP Tool

The source uses a decorator pattern.

Conceptually:

```python
@mcp.tool()
def get_stock_price(ticker: str) -> str:
    ...
```

The SDK can inspect:

```text
function name
type hints
docstring
return type
```

and generate the tool schema.

This is why type hints and docstrings are not cosmetic.

They become part of the machine-readable contract.

### Design rule

A strong tool should have:

- clear name,
- precise description,
- narrow responsibility,
- typed parameters,
- predictable result shape.

---

## 25. Expose passive data as a Resource

The same Server can expose a Resource.

Conceptually:

```python
@mcp.resource("stock://{ticker}/info")
def get_company_info(ticker: str) -> str:
    ...
```

The distinction remains:

```text
Tool:
do something

Resource:
read something
```

A clean MCP Server may expose both.

---

## 26. Run the Server over Stdio

The source's Stock Data Server runs via Stdio.

Conceptually:

```python
if __name__ == "__main__":
    mcp.run()
```

When launched directly, the process may appear to "hang."

That is expected.

It is waiting for JSON-RPC protocol messages on stdin.

### Important debugging implication

Because stdout is part of the protocol channel, arbitrary output can interfere with communication.

This will matter later when we discuss the MCP Inspector.

---

## 27. Turn the ADK agent into an MCP Client

The source uses ADK's `MCPToolset`.

Its purpose is to adapt remote/discovered MCP Tools into ordinary tools usable by the ADK Agent.

Conceptually:

```text
MCP Server tool schema
      ↓
MCPToolset
      ↓
ADK tool representation
      ↓
LLM
```

To the model, the discovered tool can look like any other callable function.

The execution still happens in the external Server.

[[IMAGE_NEEDED: MCPToolset bridge | ADK Agent/LLM on left -> MCPToolset in center -> Stdio connection -> Stock MCP Server on right | Learner should see how the framework dynamically adapts remote Server tools into model-callable capabilities]]

---

## 28. Define how the Host reaches the Server

For Stdio, the Host needs launch parameters.

Conceptually:

```python
StdioServerParameters(
    command="python",
    args=["stock_server.py"]
)
```

This tells the Host:

```text
which executable
which script
which environment
```

to use when creating the Server process.

### Security significance

These command parameters are powerful.

They control process execution on the Host machine.

They must not be constructed directly from untrusted user input.

---

## 29. The MCP handshake and dynamic discovery

The source describes a startup flow roughly like:

```text
1. Launch Server
2. Initialize protocol
3. List available tools
4. Adapt discovered schemas
```

### Launch

Host starts the Server process.

### Initialize

Client and Server establish protocol capabilities.

### List Tools

Host asks:

```text
What tools do you expose?
```

### Adapt

Tool schemas become model-usable function declarations inside the agent framework.

This means adding a new Server tool can become:

```text
change Server
restart/reconnect
discover automatically
```

instead of:

```text
copy schema into Host
edit agent code
redeploy core logic
```

[[IMAGE_NEEDED: MCP startup handshake | Host starts Server -> initialize -> tools/list -> Server returns get_stock_price schema -> MCPToolset adapts it -> LLM sees new tool | Learner should understand dynamic discovery rather than hard-coded registration]]

---

## 30. Define the Financial Analyst Agent

The source then attaches the discovered toolset to an ADK Agent.

Conceptually:

```python
analyst_agent = LlmAgent(
    instruction="Use available tools for stock prices.",
    tools=[stock_toolset]
)
```

Notice what is missing:

```text
no stock API code
no finance library
no hard-coded get_stock_price function
```

The agent only receives capabilities through MCP.

That is the architectural payoff.

---

## 31. Trace the full Financial Analyst request

User asks:

```text
"What is the current price of Apple?"
```

### Step 1 — Initialization

Runner starts.

MCPToolset launches/connects to the Stock Server.

### Step 2 — Discovery

The Host learns that `get_stock_price` exists.

### Step 3 — Reasoning

The model decides:

```text
Call get_stock_price(ticker="AAPL")
```

### Step 4 — Host translates to MCP

The framework converts the model tool call into:

```text
tools/call
```

### Step 5 — Server executes

The Stock Server runs its local Python function.

### Step 6 — Result returns

The Server sends the result over the protocol transport.

### Step 7 — Agent synthesizes final answer

The model receives the tool result and responds to the user.

[[IMAGE_NEEDED: Financial Analyst end-to-end flow | User -> ADK Runner -> LLM decides tool -> MCPToolset -> tools/call over Stdio -> Stock Server -> tool result -> MCPToolset -> LLM -> user response | Learner should trace the request across process boundaries]]

{{exercise:M01.L07.EX03}}

---

## 32. MCP can return more than text

The source upgrades the example with a stock chart.

The Server returns image content.

Conceptually:

```text
Tool result:
type = image
MIME = image/png
data = base64
```

This demonstrates that MCP tool responses can contain richer content.

The exact MCP content classes are version-specific.

The durable concept is:

```text
Tool result
can be typed multimodal content
```

---

## 33. Server-side image result

A chart tool conceptually looks like:

```python
@mcp.tool()
def get_stock_chart(ticker: str):
    return ImageContent(
        data=...,
        mimeType="image/png"
    )
```

In a real application, the Server might:

1. fetch price history,
2. generate a chart,
3. encode the image,
4. return typed image content.

The important boundary remains:

```text
Server generates data
Host/agent consumes it
```

---

## 34. Host-side handling of multimodal tool results

The source describes MCPToolset converting the returned image into the agent framework's multimodal content representation.

A multimodal model may then:

- inspect it,
- describe it,
- reason about it.

But there is another UI concern.

### Model consumption vs user display

These are different.

```text
Model can see image
```

does not automatically mean:

```text
UI displays image
```

A web UI may need to inspect the tool-response event, extract the binary/base64 image, and render it.

This is an important product-design distinction.

---

## 35. Distributed tool systems need isolated debugging

With an MCP architecture, a failure may occur in:

- Host,
- connection configuration,
- Server process,
- tool function,
- JSON-RPC exchange.

The source introduces the MCP Inspector as a dedicated debugging tool.

It acts like an independent Client.

It can help verify the Server before the Host is involved.

---

## 36. Why Stdio debugging is special

With Stdio, stdout is part of the protocol stream.

If the Server randomly prints:

```text
DEBUG: starting...
```

into stdout, that text can interfere with the structured protocol data.

Therefore, debugging must respect the transport.

Use:

- framework logging mechanisms,
- stderr where appropriate,
- dedicated Inspector tooling.

Do not assume ordinary `print()` debugging is harmless inside a protocol channel.

---

## 37. MCP Inspector workflow

The source's recommended debugging sequence is conceptually:

### 1. Launch Inspector against the Server

Run the Inspector as a test client.

### 2. Inspect Tools/Resources

Confirm schemas are discoverable.

### 3. Execute a Tool manually

Example:

```json
{"ticker": "AAPL"}
```

### 4. Inspect raw protocol traffic/logs

Confirm:

- request,
- response,
- error.

### 5. Integrate with Host only after Server passes isolated testing

This creates a useful diagnostic rule:

```text
Fails in Inspector
    -> likely Server bug

Works in Inspector but fails in Host
    -> likely Host/connection/configuration bug
```

[[IMAGE_NEEDED: MCP debugging isolation flow | MCP Server tested first by Inspector; after passing, connected to ADK Host. Branches show Server bug vs Host/configuration bug depending on where failure occurs | Learner should use isolated testing before debugging full integration]]

{{exercise:M01.L07.EX04}}

---

## 38. Security: protect process launch parameters

Stdio lets the Host start processes.

That is powerful.

It also creates risk.

The source warns against building:

```text
command
args
```

directly from untrusted user strings.

Why?

Because process invocation can become command injection.

### Safer design

- hard-code trusted executable,
- hard-code or strictly validate arguments,
- use allow-lists,
- avoid shell interpolation,
- do not pass arbitrary user strings to process launch.

---

## 39. Security: control environment inheritance

Child processes may inherit environment variables from the Host.

That may include secrets such as:

- model API keys,
- database credentials,
- internal service tokens.

An untrusted MCP Server should not receive all Host secrets automatically.

The source recommends being deliberate about the child environment.

General principle:

> Give a Server only the environment variables it actually needs.

This is another application of least privilege.

---

## 40. Choose Stdio or remote HTTP based on topology

### Prefer Stdio when:

- Server is local,
- Host owns the process,
- desktop app,
- local development,
- private repo tool,
- no shared multi-client service is needed.

### Prefer remote HTTP-style transport when:

- Host and Server run on different machines,
- Server is a shared organizational service,
- independent scaling is needed,
- cloud deployment is required.

This is a deployment decision, not just a coding preference.

---

## 41. Why remote transport matters for shared services

Stdio normally means:

```text
one Host launches one Server process
```

For a centralized company knowledge tool, you may instead want:

```text
many Hosts
   ↓
one scalable remote MCP service
```

That enables:

- independent scaling,
- central governance,
- shared maintenance,
- common authentication.

But it also introduces:

- network security,
- concurrency,
- availability,
- observability.

---

## 42. Write once, use everywhere

The source closes with the most important interoperability promise.

A well-built MCP Server should not belong to one agent framework.

If it speaks MCP, then potentially:

```text
ADK Host
IDE Host
Desktop AI Host
Custom Agent Host
```

can all connect to the same Server without rewriting the Server's internal logic.

This is the deeper meaning of the source's "USB-C for AI" analogy.

A standardized boundary lets:

```text
tool implementation
```

outlive:

```text
one agent
one model
one framework
```

---

## 43. MCP and A2A solve different integration problems

The previous lesson focused on A2A.

This lesson focuses on MCP.

It is useful to distinguish them conceptually.

### A2A

Primary problem:

```text
agent ↔ agent collaboration
```

Examples:

- Research Agent delegates to another Agent.
- Remote specialist exposes skills and Tasks.

### MCP

Primary problem:

```text
agent/Host ↔ tools/resources/prompts
```

Examples:

- Agent discovers a Git tool.
- Host reads Filesystem Resources.
- Server provides a reusable Prompt.

They can coexist.

A multi-agent system may use:

```text
A2A between agents
MCP between each Host and its capability Servers
```

[[IMAGE_NEEDED: A2A vs MCP boundary diagram | Left: Agent A <-> Agent B via A2A; beneath each agent, Host connects to Tool/Data Servers via MCP | Learner should see complementary protocol layers rather than competing alternatives]]

---

## 44. Production checklist

Before shipping an MCP-enabled system, ask:

### Server contract

- Are tool names clear?
- Are schemas narrow and typed?
- Are Resources read-only where intended?
- Are Prompts parameterized clearly?

### Security

- Are subprocess commands trusted?
- Are environment variables minimized?
- Are risky actions user-approved?
- Are remote endpoints authenticated?

### Runtime

- Can the Host discover tools reliably?
- What happens if a Server crashes?
- Are timeouts/retries defined?
- Is cleanup handled?

### Transport

- Is Stdio appropriate?
- Does this need a shared remote service?
- Is TLS/authentication configured for remote deployment?

### Multimodal results

- Can the Host/model process image/file content?
- Can the UI render it?

### Debugging

- Does the Server work in isolation?
- Can Inspector/diagnostics show schemas and protocol traffic?
- Are logs separated from the protocol stream?

{{exercise:M01.L07.EX05}}

---

## 45. Source-specific implementation details to re-check

These chapters are Early Release material.

Exact implementation details can change.

Verify current documentation for:

- MCP Python SDK import paths,
- `FastMCP`,
- decorator APIs,
- MCP content classes,
- `MCPToolset`,
- ADK toolset integration,
- Stdio parameter classes,
- remote transport parameter classes,
- handshake timing,
- `tools/list`,
- `tools/call`,
- `resources/read`,
- `prompts/get`,
- Sampling/Elicitation methods,
- MCP Inspector commands,
- transport recommendations.

The durable architecture is more important than memorizing one SDK version.

---

## 46. The complete mental model

Start with the pre-MCP system:

```text
Agent
├── hard-coded tools
├── vendor-specific function parsing
├── manual state loop
└── direct API secrets
```

Move to MCP:

```text
Host
├── orchestration
├── LLM
├── security
├── configuration
│
├── Client -> Git Server
├── Client -> Filesystem Server
└── Client -> Stock Server
```

Servers expose standardized primitives:

```text
Tools
Resources
Prompts
```

Servers may ask the Host for:

```text
Sampling
Elicitation
```

Transports connect them:

```text
Stdio
or
remote HTTP-style transport
```

The implementation path is:

```text
build Server
    ↓
describe capabilities
    ↓
connect Host
    ↓
discover dynamically
    ↓
model chooses tool
    ↓
Host translates request
    ↓
Server executes
    ↓
typed result returns
    ↓
agent continues reasoning
```

This is the difference between a hard-wired demo and a reusable capability ecosystem.

---

## Important misconceptions

### Misconception 1
> "MCP is just another function-calling format."

No. The source presents MCP as a broader Host/Client/Server architecture with discovery, resources, prompts, bidirectional assistance, and transports.

### Misconception 2
> "Structured function calling already solves tool security."

No. Safe execution still requires trusted orchestration, sandboxing, permissions, and approval.

### Misconception 3
> "The Host and Client are the same concept."

No. The Host is the main trusted application; Clients are protocol connections inside it, typically one per Server.

### Misconception 4
> "A Server should know which LLM is using it."

No. MCP aims to decouple capability implementation from the model/provider.

### Misconception 5
> "Resources are just Tools that return text."

No. Resources are passive data, while Tools represent executable actions.

### Misconception 6
> "Prompts are automatically chosen by the model like Tools."

No. In the source's framing, Prompts are user-triggered reusable workflows.

### Misconception 7
> "Sampling means the Server contains its own LLM."

No. Sampling lets the Server request reasoning from the Host's central model.

### Misconception 8
> "Elicitation is a failure."

No. It allows a Server to pause and request missing structured user input.

### Misconception 9
> "Adding a new MCP Tool always requires changing the agent's source code."

No. Dynamic discovery allows the Host to learn new Server capabilities.

### Misconception 10
> "Stdio opens a local network port."

No. It communicates through standard input/output between processes.

### Misconception 11
> "I can freely print debug messages to stdout in a Stdio MCP Server."

No. stdout carries protocol data and can be corrupted by arbitrary output.

### Misconception 12
> "If the model can consume an image tool result, the UI will automatically display it."

No. UI rendering may require intercepting and rendering the media result separately.

### Misconception 13
> "A child MCP Server should inherit every environment variable from the Host."

No. Least privilege means explicitly limiting secrets and environment exposure.

### Misconception 14
> "Stdio is the best transport for a shared cloud service."

No. Remote/shared services generally need a network transport and proper authentication.

### Misconception 15
> "A2A and MCP solve the same exact problem."

No. A2A primarily standardizes agent-to-agent interaction, while MCP standardizes Host-to-capability interaction.

---

## Key terminology

| Term | Meaning |
|---|---|
| MCP | Model Context Protocol |
| Host | Trusted application running the model/orchestration and managing Servers |
| Client | Protocol connection inside the Host for one Server |
| Server | Independent capability provider exposing MCP primitives |
| Glue Code Monolith | Central hard-coded routing logic coupling agent and tools |
| Static Toolset | Tool list compiled directly into agent code |
| Vendor Lock-in | Dependence on provider-specific tool-call formats |
| Tool | Executable MCP capability |
| Resource | Passive/read-only data exposed by a Server |
| Prompt | Reusable parameterized workflow exposed by a Server |
| Sampling | Server request asking the Host to perform model reasoning |
| Elicitation | Server request asking the Host/user for missing structured input |
| JSON-RPC | Structured message format used by MCP in the source |
| Stdio | Local transport over stdin/stdout |
| Streamable HTTP | Remote/web transport style described by the source |
| FastMCP | High-level Python Server interface used in the source |
| MCPToolset | Source-described ADK adapter for MCP Servers |
| Dynamic discovery | Runtime discovery of Server capabilities |
| `tools/list` | Source-described discovery request for Tools |
| `tools/call` | Source-described standardized Tool invocation |
| `resources/read` | Source-described Resource read request |
| `prompts/get` | Source-described Prompt retrieval request |
| ImageContent | Source-used typed image result concept |
| MCP Inspector | Dedicated tool for isolated MCP Server debugging |
| Least privilege | Give Servers/processes only permissions and secrets they need |

---

## Self-check

1. What are the four pre-MCP dilemmas highlighted by the source?
2. Why is native function calling insufficient by itself?
3. How does provider-specific function-call structure create vendor lock-in?
4. What is the role of the Host?
5. What is the role of the Server?
6. What is the role of the Client?
7. Why does the Host create one Client per Server?
8. How does dynamic tool discovery work?
9. What does the Host do with discovered tool schemas?
10. What is the difference between Tool, Resource, and Prompt?
11. Why are Resources useful for context-window management?
12. What does Sampling let a Server do?
13. Why can Sampling centralize model cost and security?
14. What problem does Elicitation solve?
15. When is Stdio appropriate?
16. When is a remote HTTP-style transport appropriate?
17. Why is Stdio attractive for local desktop tools?
18. What does FastMCP provide?
19. Why are Python type hints important in a tool function?
20. What does MCPToolset do?
21. What are the four major handshake/discovery steps in the source?
22. Why does dynamic discovery reduce duplicate schema maintenance?
23. Trace "What is Apple's stock price?" end to end.
24. What happens when the model selects `get_stock_price`?
25. Where does the stock API/data logic live?
26. How can a Server return an image?
27. What is the difference between model consumption of an image and UI display of it?
28. Why can ordinary stdout debugging break Stdio communication?
29. What is the purpose of MCP Inspector?
30. How does isolated Inspector testing help locate bugs?
31. Why should user input never directly construct Stdio process commands?
32. Why should child-process environment variables be restricted?
33. Why might a shared company Server use remote transport instead of Stdio?
34. What does "write once, use everywhere" mean in MCP?
35. How do MCP and A2A differ?
36. How could one system use both MCP and A2A?
37. Which implementation details in these chapters should be re-verified against current documentation?

---

## Retain this idea

**MCP turns tool integration from hard-wired application code into a protocol-based capability ecosystem. The Host remains the trusted orchestrator, each Server specializes in a narrow domain, dedicated Clients isolate connections, and standardized primitives make tools, data, prompts, reasoning requests, and user-input requests discoverable and reusable. The implementation chapter proves the architectural promise: a Host can dynamically acquire capabilities from an isolated Server without embedding that capability's business logic inside the agent itself.**
""".strip(),

        "sections": [
            {"id": "why-mcp", "title": "Why MCP Exists", "order": 1},
            {"id": "four-dilemmas", "title": "Four Scaling Dilemmas Before MCP", "order": 2},
            {"id": "brittle-tool", "title": "The Brittle Monolithic Tool", "order": 3},
            {"id": "vendor-lockin", "title": "Vendor Lock-in Around Function Calling", "order": 4},
            {"id": "function-calling-not-enough", "title": "Why Function Calling Alone Is Not Enough", "order": 5},
            {"id": "architecture", "title": "MCP Architecture: Host, Client, Server", "order": 6},
            {"id": "host", "title": "The Host Is the Trusted Orchestrator", "order": 7},
            {"id": "server", "title": "The Server Is the Tool Specialist", "order": 8},
            {"id": "client", "title": "The Client Is the Secure Communication Channel", "order": 9},
            {"id": "plug-play", "title": "Plug-and-Play Capability Discovery", "order": 10},
            {"id": "primitives", "title": "MCP Primitives", "order": 11},
            {"id": "tools", "title": "Tools: the Agent's Hands", "order": 12},
            {"id": "resources", "title": "Resources: the Agent's Library", "order": 13},
            {"id": "prompts", "title": "Prompts: the Agent's Playbook", "order": 14},
            {"id": "control-triad", "title": "Model-, Application-, and User-Controlled Primitives", "order": 15},
            {"id": "sampling", "title": "Sampling: a Server Borrows the Host's Reasoning", "order": 16},
            {"id": "sampling-flow", "title": "Sampling Step by Step", "order": 17},
            {"id": "elicitation", "title": "Elicitation: Ask the User for Missing Information", "order": 18},
            {"id": "transports", "title": "MCP Transport Layer", "order": 19},
            {"id": "stdio", "title": "Stdio for Local Communication", "order": 20},
            {"id": "streamable-http", "title": "Streamable HTTP for Remote Capabilities", "order": 21},
            {"id": "chapter11-scenario", "title": "Practical System: the Financial Analyst", "order": 22},
            {"id": "fastmcp", "title": "Build the Server with FastMCP", "order": 23},
            {"id": "tool-decorator", "title": "Expose a Python Function as an MCP Tool", "order": 24},
            {"id": "resource-decorator", "title": "Expose Passive Data as a Resource", "order": 25},
            {"id": "stdio-server", "title": "Run the Server over Stdio", "order": 26},
            {"id": "mcp-toolset", "title": "Turn the ADK Agent into an MCP Client", "order": 27},
            {"id": "server-parameters", "title": "Define How the Host Reaches the Server", "order": 28},
            {"id": "handshake", "title": "The MCP Handshake and Dynamic Discovery", "order": 29},
            {"id": "financial-agent", "title": "Define the Financial Analyst Agent", "order": 30},
            {"id": "execution-flow", "title": "Trace the Full Financial Analyst Request", "order": 31},
            {"id": "multimodal", "title": "MCP Can Return More Than Text", "order": 32},
            {"id": "image-content", "title": "Server-Side Image Result", "order": 33},
            {"id": "client-image", "title": "Host-Side Handling of Multimodal Results", "order": 34},
            {"id": "inspector", "title": "Distributed Tool Systems Need Isolated Debugging", "order": 35},
            {"id": "stdio-debugging", "title": "Why Stdio Debugging Is Special", "order": 36},
            {"id": "inspector-workflow", "title": "MCP Inspector Workflow", "order": 37},
            {"id": "security-command", "title": "Security: Protect Process Launch Parameters", "order": 38},
            {"id": "security-env", "title": "Security: Control Environment Inheritance", "order": 39},
            {"id": "transport-choice", "title": "Choose Stdio or Remote HTTP Based on Topology", "order": 40},
            {"id": "shared-service", "title": "Why Remote Transport Matters for Shared Services", "order": 41},
            {"id": "write-once", "title": "Write Once, Use Everywhere", "order": 42},
            {"id": "mcp-vs-a2a", "title": "MCP and A2A Solve Different Problems", "order": 43},
            {"id": "production-checklist", "title": "Production Checklist", "order": 44},
            {"id": "source-boundaries", "title": "Source-Specific Implementation Details to Re-Check", "order": 45},
            {"id": "complete-model", "title": "The Complete Mental Model", "order": 46},
        ],
    },

    "exercises": [
        {
            "id": "M01.L07.EX01",
            "title": "Diagnose a Pre-MCP Agent",
            "lesson_code": "M01.L07",
            "section_id": "function-calling-not-enough",
            "placement": "after_section",
            "description": "Identify the scaling problems in a hard-wired tool architecture.",
            "instructions": (
                "Imagine an agent with Weather, GitHub, Email, Python execution, and Calendar tools.\n"
                "1. Identify where glue code accumulates.\n"
                "2. Identify one vendor-lock-in point.\n"
                "3. Identify one security risk.\n"
                "4. Identify one manual state-machine problem.\n"
                "5. Explain why adding a sixth tool requires code changes in the static design."
            ),
            "expected_output": "A five-part diagnosis mapped to the source's four dilemmas.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["mcp-motivation", "architecture-analysis"],
        },
        {
            "id": "M01.L07.EX02",
            "title": "Classify MCP Primitives",
            "lesson_code": "M01.L07",
            "section_id": "control-triad",
            "placement": "after_section",
            "description": "Practice distinguishing Tools, Resources, Prompts, Sampling, and Elicitation.",
            "instructions": (
                "Classify each scenario:\n"
                "1. Delete a file.\n"
                "2. Read a Git log.\n"
                "3. User selects 'Generate Unit Test'.\n"
                "4. Flight Server asks Host LLM to compare 50 flights.\n"
                "5. GitHub Server asks user which repository to use.\n"
                "For each, identify who initiates/controls the interaction."
            ),
            "expected_output": "A five-row primitive classification table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["mcp-tools", "mcp-resources", "mcp-prompts", "sampling", "elicitation"],
        },
        {
            "id": "M01.L07.EX03",
            "title": "Trace the Financial Analyst Request",
            "lesson_code": "M01.L07",
            "section_id": "execution-flow",
            "placement": "after_section",
            "description": "Trace a complete MCP tool call across process boundaries.",
            "instructions": (
                "For 'What is the current price of Apple?':\n"
                "1. Show initialization/discovery.\n"
                "2. Show the LLM's chosen tool and arguments.\n"
                "3. Show the Host-to-MCP translation.\n"
                "4. Show Server execution.\n"
                "5. Show result return.\n"
                "6. Show final model synthesis.\n"
                "Mark which steps run in the Host process and which run in the Server process."
            ),
            "expected_output": "A numbered end-to-end trace with process boundaries.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["mcp-toolset", "json-rpc", "dynamic-discovery"],
        },
        {
            "id": "M01.L07.EX04",
            "title": "Debug an MCP Server in Isolation",
            "lesson_code": "M01.L07",
            "section_id": "inspector-workflow",
            "placement": "after_section",
            "description": "Use the source's isolation strategy to locate integration failures.",
            "instructions": (
                "Suppose the ADK Agent reports 'Tool execution failed'.\n"
                "1. Define what you would test in MCP Inspector.\n"
                "2. Explain what a failed tool invocation in Inspector suggests.\n"
                "3. Explain what a successful Inspector test but failed ADK integration suggests.\n"
                "4. Explain why raw print() debugging can be dangerous on stdout.\n"
                "5. Define one safe logging approach."
            ),
            "expected_output": "A diagnostic decision tree for Server vs Host/configuration failures.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["mcp-inspector", "stdio-debugging", "distributed-debugging"],
        },
        {
            "id": "M01.L07.EX05",
            "title": "Choose an MCP Deployment Topology",
            "lesson_code": "M01.L07",
            "section_id": "production-checklist",
            "placement": "after_section",
            "description": "Choose Stdio or remote transport for realistic scenarios.",
            "instructions": (
                "Choose a transport and justify it for:\n"
                "1. Local Git tool inside a coding assistant.\n"
                "2. Shared company knowledge service used by many agents.\n"
                "3. Private filesystem tool on a user's laptop.\n"
                "4. Cloud-hosted Jira integration.\n"
                "Then list security controls for each remote/local case."
            ),
            "expected_output": "A four-row topology and security decision table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["stdio", "streamable-http", "security", "deployment"],
        },
        {
            "id": "M01.L07.EX06",
            "title": "Design a Reusable MCP Server",
            "lesson_code": "M01.L07",
            "section_id": "write-once",
            "placement": "after_section",
            "description": "Design a Server intended for use by several different Hosts.",
            "instructions": (
                "Design a Project Management MCP Server.\n"
                "1. Define three Tools.\n"
                "2. Define two Resources.\n"
                "3. Define one Prompt.\n"
                "4. Identify one Sampling use case.\n"
                "5. Identify one Elicitation use case.\n"
                "6. Choose a transport for local development and one for production.\n"
                "7. Explain how ADK, an IDE, and another MCP Host could reuse the same Server."
            ),
            "expected_output": "A complete reusable MCP Server capability contract.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["mcp-design", "primitives", "reusability"],
        },
    ],

    "quiz": {
        "id": "M01.L07.QZ01",
        "title": "Model Context Protocol — Knowledge Check",
        "lesson_code": "M01.L07",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L07.Q01",
                "section_id": "four-dilemmas",
                "question": "Which problem describes a growing central if/elif block that routes every tool?",
                "options": ["Glue Code Monolith", "Sampling", "Resource discovery", "Elicitation"],
                "correct": 0,
                "explanation": "The source uses this term for tightly coupled central tool-routing logic.",
            },
            {
                "id": "M01.L07.Q02",
                "section_id": "vendor-lockin",
                "question": "Why can function calling still create vendor lock-in?",
                "options": [
                    "Providers expose tool calls through different API structures",
                    "Tools cannot accept JSON",
                    "Function calling always uses Stdio",
                    "MCP requires one specific model provider",
                ],
                "correct": 0,
                "explanation": "The conceptual tool request may be the same while provider response structures differ.",
            },
            {
                "id": "M01.L07.Q03",
                "section_id": "architecture",
                "question": "Which MCP component is the trusted main application?",
                "options": ["Host", "Server", "Resource", "Prompt"],
                "correct": 0,
                "explanation": "The Host owns orchestration, configuration, security, and model interaction.",
            },
            {
                "id": "M01.L07.Q04",
                "section_id": "client",
                "question": "What is the Client in the source's MCP architecture?",
                "options": [
                    "A protocol component inside the Host dedicated to one Server",
                    "The end user",
                    "A standalone LLM",
                    "The Server's database",
                ],
                "correct": 0,
                "explanation": "The Host creates dedicated Client connections to Servers.",
            },
            {
                "id": "M01.L07.Q05",
                "section_id": "plug-play",
                "question": "What makes MCP toolsets dynamic rather than static?",
                "options": [
                    "The Host discovers capabilities from connected Servers at runtime",
                    "Every tool is hard-coded in the agent",
                    "The LLM rewrites the Server",
                    "Resources automatically execute themselves",
                ],
                "correct": 0,
                "explanation": "Runtime discovery removes the need to compile every capability into the agent's source.",
            },
            {
                "id": "M01.L07.Q06",
                "section_id": "tools",
                "question": "What does the source frame MCP Tools as?",
                "options": ["Model-controlled actions", "User-controlled workflows", "Read-only context only", "Transport protocols"],
                "correct": 0,
                "explanation": "The model may choose Tools to perform actions.",
            },
            {
                "id": "M01.L07.Q07",
                "section_id": "resources",
                "question": "What is an MCP Resource?",
                "options": [
                    "Passive data that the Host can choose to read",
                    "A process-launch command",
                    "An LLM provider",
                    "A mandatory tool call",
                ],
                "correct": 0,
                "explanation": "Resources expose data while the Host controls retrieval/use.",
            },
            {
                "id": "M01.L07.Q08",
                "section_id": "prompts",
                "question": "How does the source frame MCP Prompts?",
                "options": [
                    "Reusable user-triggered parameterized workflows",
                    "Hidden system prompts only",
                    "Binary file transfers",
                    "Tool sandboxes",
                ],
                "correct": 0,
                "explanation": "Hosts can surface Server-provided Prompts as commands or UI actions.",
            },
            {
                "id": "M01.L07.Q09",
                "section_id": "sampling",
                "question": "What does Sampling allow a Server to do?",
                "options": [
                    "Ask the Host to use its LLM for reasoning",
                    "Directly change the Host's source code",
                    "Open a filesystem Resource automatically",
                    "Bypass Host security",
                ],
                "correct": 0,
                "explanation": "Sampling lets a specialized Server borrow central reasoning while the Host remains in control.",
            },
            {
                "id": "M01.L07.Q10",
                "section_id": "elicitation",
                "question": "What problem does Elicitation solve?",
                "options": [
                    "Missing user information needed to continue execution",
                    "Model vendor switching",
                    "Local process startup",
                    "Tool schema generation",
                ],
                "correct": 0,
                "explanation": "The Server can ask the Host to collect structured user input.",
            },
            {
                "id": "M01.L07.Q11",
                "section_id": "stdio",
                "question": "What is the basic Stdio transport model?",
                "options": [
                    "Host launches a child process and exchanges protocol messages through stdin/stdout",
                    "Server opens a public WebSocket port",
                    "Host sends only email messages",
                    "Model directly imports the Server code",
                ],
                "correct": 0,
                "explanation": "Stdio is a local process-to-process transport.",
            },
            {
                "id": "M01.L07.Q12",
                "section_id": "tool-decorator",
                "question": "Why are type hints and docstrings important for FastMCP tools?",
                "options": [
                    "They help generate the machine-readable tool schema",
                    "They encrypt the tool",
                    "They create a cloud account",
                    "They remove the need for a Host",
                ],
                "correct": 0,
                "explanation": "Function metadata becomes part of the model-facing capability contract.",
            },
            {
                "id": "M01.L07.Q13",
                "section_id": "mcp-toolset",
                "question": "What does MCPToolset do in the source's ADK example?",
                "options": [
                    "Connects to an MCP Server and adapts discovered tools into ADK-usable tools",
                    "Implements all financial business logic",
                    "Replaces the LLM",
                    "Stores every Resource permanently",
                ],
                "correct": 0,
                "explanation": "It acts as the bridge between the framework and the MCP Server.",
            },
            {
                "id": "M01.L07.Q14",
                "section_id": "handshake",
                "question": "Which sequence best matches the source's dynamic discovery flow?",
                "options": [
                    "Launch -> Initialize -> List Tools -> Adapt schemas",
                    "Train -> Fine-tune -> Quantize -> Deploy",
                    "Prompt -> Delete -> Restart -> Ignore",
                    "Authenticate -> Compile Server into LLM -> Finish",
                ],
                "correct": 0,
                "explanation": "The Host connects, initializes the protocol, discovers tools, then adapts them.",
            },
            {
                "id": "M01.L07.Q15",
                "section_id": "execution-flow",
                "question": "Where does get_stock_price actually execute?",
                "options": [
                    "Inside the isolated Stock MCP Server process",
                    "Inside the user's browser",
                    "Inside the LLM weights",
                    "Inside the Prompt primitive",
                ],
                "correct": 0,
                "explanation": "The Host requests the Tool, but execution belongs to the Server.",
            },
            {
                "id": "M01.L07.Q16",
                "section_id": "client-image",
                "question": "Why might a UI need special handling for an image returned by a Tool?",
                "options": [
                    "The model may consume the image while the UI still needs to extract/render the media result",
                    "MCP cannot represent images",
                    "Images can only be Resources",
                    "Stdio deletes image data automatically",
                ],
                "correct": 0,
                "explanation": "Model context handling and user-interface rendering are separate concerns.",
            },
            {
                "id": "M01.L07.Q17",
                "section_id": "stdio-debugging",
                "question": "Why can arbitrary print() calls be dangerous in a Stdio Server?",
                "options": [
                    "stdout carries protocol messages and extra text can corrupt the stream",
                    "Python cannot print from subprocesses",
                    "Printing disables JSON Schema",
                    "It automatically leaks all Resources",
                ],
                "correct": 0,
                "explanation": "Protocol traffic and debugging output must not be mixed carelessly.",
            },
            {
                "id": "M01.L07.Q18",
                "section_id": "security-env",
                "question": "What environment-variable principle does the source recommend?",
                "options": [
                    "Pass only what the child Server actually needs",
                    "Always pass every Host secret",
                    "Never use environment variables at all",
                    "Let the model choose secrets dynamically",
                ],
                "correct": 0,
                "explanation": "Least privilege should apply to child-process environments.",
            },
            {
                "id": "M01.L07.Q19",
                "section_id": "mcp-vs-a2a",
                "question": "Which comparison is most accurate?",
                "options": [
                    "A2A primarily standardizes agent-to-agent communication; MCP standardizes Host-to-capability communication",
                    "A2A and MCP are identical",
                    "MCP only handles agent-to-agent delegation",
                    "A2A only handles local files",
                ],
                "correct": 0,
                "explanation": "The two protocols address complementary integration boundaries.",
            },
            {
                "id": "M01.L07.Q20",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design an MCP-enabled coding assistant with a Host, dedicated Clients, "
                    "a local Git Server, a remote Issue Tracker Server, Tools, Resources, one Prompt, "
                    "one Sampling flow, one Elicitation flow, dynamic discovery, transport choices, "
                    "security controls, multimodal/file handling, and an Inspector-based debugging plan."
                ),
            },
        ],
        "passing_score": 70,
    },
}
