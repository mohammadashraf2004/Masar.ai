"""M05.L01 — MCP Ecosystem, Extensions, and Contributing to the Protocol.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 9 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "MCP Ecosystem and Extensions"

MODULE_DESCRIPTION = (
    "Move beyond the MCP core protocol into the broader ecosystem: registries, "
    "governance platforms, gateways, context-management techniques, alternative "
    "frameworks, testing tools, official extensions, the SEP contribution process, "
    "and the future direction of MCP."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "MCP Ecosystem, Extensions, and Contributing to the Protocol",

    "slug": "ai-agents-mcp-m05-l01",

    "description": (
        "A final ecosystem lesson covering MCP registries and subregistries, governance "
        "tools, gateways and tunnels, Code Mode, alternative frameworks, MCPJam, official "
        "MCP extensions, durable Tasks, Specification Enhancement Proposals, contribution "
        "tracks, conformance testing, and the MCP roadmap."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.0,

    "skill_tags": [
        "mcp-ecosystem",
        "mcp-registry",
        "governance",
        "mcp-gateway",
        "mcp-tunnels",
        "code-mode",
        "fastmcp",
        "arcade-mcp",
        "mcp-inspector",
        "mcpjam",
        "mcp-extensions",
        "mcp-apps",
        "auth-extensions",
        "mcp-tasks",
        "sep",
        "conformance-testing",
        "mcp-roadmap",
        "module-05",
    ],

    "prerequisite_ids": ["M04.L01"],

    "lesson": {
        "title": "MCP Ecosystem, Extensions, and Contributing to the Protocol",

        "content": (
            "# MCP Ecosystem, Extensions, and Contributing to the Protocol\n"
            "\n"
            "> **Lesson:** M05.L01  \n"
            "> **Module:** MCP Ecosystem and Extensions  \n"
            "> **Source alignment:** Chapter 9 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "> **Version-awareness note:** this chapter describes a fast-moving ecosystem. "
            "Statements about supported clients, extension availability, SDK support, roadmap priorities, "
            "and specific products should be interpreted as source-time facts rather than timeless guarantees.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why the MCP ecosystem needs governance and context-management tooling beyond the core protocol.\n"
            "- Describe the role of the official MCP Registry and curated subregistries.\n"
            "- Explain how governance platforms, MCP gateways, and tunnels change deployment and security architecture.\n"
            "- Explain Code Mode and why it can reduce tool-schema context and model round trips.\n"
            "- Identify when Code Mode is useful and when normal purpose-built tools remain better.\n"
            "- Compare the goals of alternative MCP frameworks such as FastMCP and arcade-mcp.\n"
            "- Distinguish MCP Inspector-style direct protocol testing from model-connected testing tools.\n"
            "- Explain what MCP extensions are and how extension identifiers are structured.\n"
            "- Describe MCP Apps and how UI resources are attached to tools.\n"
            "- Explain OAuth Client Credentials and Enterprise-Managed Authorization at a conceptual level.\n"
            "- Explain the MCP Tasks extension and its durable asynchronous state machine.\n"
            "- Describe the Specification Enhancement Proposal (SEP) process.\n"
            "- Distinguish Standards, Informational, Process, and Extensions SEP tracks.\n"
            "- Explain the role of sponsors, reference implementations, and conformance tests.\n"
            "- Interpret the roadmap areas described by the source without treating them as permanent guarantees.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. What comes after learning the MCP core?\n"
            "\n"
            "The previous chapters covered the protocol itself: clients, servers, primitives, utilities, security, deployment, and transports.\n"
            "\n"
            "The final chapter asks a different question:\n"
            "\n"
            "> **How do we build, operate, discover, govern, extend, and evolve MCP at ecosystem scale?**\n"
            "\n"
            "The source groups the emerging ecosystem around two especially important problems:\n"
            "\n"
            "### Governance\n"
            "\n"
            "Governance tooling helps organizations answer questions such as:\n"
            "\n"
            "- Which servers are approved?\n"
            "- How are they deployed?\n"
            "- Who may access them?\n"
            "- How are authentication and authorization enforced?\n"
            "- How are activity and failures observed?\n"
            "- Can many servers be exposed through one managed endpoint?\n"
            "\n"
            "### Context management\n"
            "\n"
            "Context-management tooling asks:\n"
            "\n"
            "- How do we avoid sending hundreds of tool definitions to the model?\n"
            "- How do we expose a huge API without overwhelming tool selection?\n"
            "- How do we minimize token use while preserving capability?\n"
            "- Which work should be done deterministically in code instead of round-tripping through the model?\n"
            "\n"
            '{{image:mcp-ecosystem-overview}}'
            '\n'
            "\n"
            "---\n"
            "\n"
            "## 2. MCP Registry: discovering servers at ecosystem scale\n"
            "\n"
            "MCP makes capabilities discoverable **inside a connected server**, but early MCP did not solve discovery of servers themselves.\n"
            "\n"
            "The MCP Registry addresses that gap by acting as a centralized, programmable repository of **server metadata**.\n"
            "\n"
            "### The registry is a metaregistry\n"
            "\n"
            "The source describes the official registry as storing metadata that points to code or binaries living elsewhere, such as package registries.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Server developer\n"
            "      ↓\n"
            "Publish package to package registry\n"
            "      ↓\n"
            "Submit metadata to official MCP Registry\n"
            "      ↓\n"
            "Clients / agents / subregistries query standardized registry API\n"
            "```\n"
            "\n"
            "Typical metadata includes:\n"
            "\n"
            "- name,\n"
            "- title,\n"
            "- description,\n"
            "- source-code repository,\n"
            "- package locations,\n"
            "- flexible metadata fields.\n"
            "\n"
            "### Why an API matters\n"
            "\n"
            "The important design idea is not merely having a website. A standardized API means humans, normal software, and autonomous agents can search and consume server metadata programmatically.\n"
            "\n"
            "[[IMAGE_NEEDED: Official MCP Registry discovery flow | "
            "A diagram showing server publisher → package registry + official MCP Registry metadata → clients/agents querying the Registry | "
            "Learner should notice that the official Registry points to distributable artifacts rather than necessarily hosting the server code itself]]\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Subregistries: discovery with curation and policy\n"
            "\n"
            "The source's more interesting registry idea is the **subregistry**.\n"
            "\n"
            "A subregistry can consume entries from:\n"
            "\n"
            "- the official registry,\n"
            "- other subregistries,\n"
            "- its own private/internal entries.\n"
            "\n"
            "Then it can curate, annotate, and republish them using the same general registry API model.\n"
            "\n"
            "### Why subregistries matter\n"
            "\n"
            "A public community may want ratings and comments. An enterprise may want only security-reviewed servers. "
            "A team may want only servers approved for a specific workflow.\n"
            "\n"
            "The flexible `_meta` field described by the source enables registry-specific annotations such as:\n"
            "\n"
            "- ratings,\n"
            "- comments,\n"
            "- trust labels,\n"
            "- approval state,\n"
            "- ownership metadata,\n"
            "- organization-specific policy attributes.\n"
            "\n"
            "This turns registry infrastructure into part of the **governance layer**.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP Registry and subregistry ecosystem | "
            "Official Registry at top, several public/private subregistries beneath it, and multiple clients connected downstream; include an enterprise private subregistry with vetted-only entries | "
            "Learner should notice that subregistries can filter and enrich upstream data rather than simply copy it]]\n"
            "\n"
            "{{exercise:M05.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Governance platforms and MCP gateways\n"
            "\n"
            "Enterprises rarely need only one server with one authentication rule. They often need a managed fleet.\n"
            "\n"
            "The chapter describes an ecosystem of governance tools that may combine:\n"
            "\n"
            "- deployment,\n"
            "- hosting,\n"
            "- authentication,\n"
            "- authorization,\n"
            "- observability,\n"
            "- server registries,\n"
            "- gateway routing,\n"
            "- agent governance.\n"
            "\n"
            "### MCP gateway\n"
            "\n"
            "A gateway provides a controlled entry point in front of several MCP servers.\n"
            "\n"
            "```text\n"
            "Clients\n"
            "  ↓\n"
            "MCP Gateway\n"
            "  ├── auth / policy\n"
            "  ├── routing\n"
            "  ├── observability\n"
            "  ├── tool filtering\n"
            "  └── server discovery\n"
            "        ↓\n"
            "Server A   Server B   Server C\n"
            "```\n"
            "\n"
            "This can centralize controls that would otherwise be duplicated across every server.\n"
            "\n"
            "### Tool minimization at the gateway\n"
            "\n"
            "The source describes gateway/portal patterns where the full set of tools is not exposed up front. "
            "Instead, the connected agent may get only a small search/execute interface or request full definitions on demand.\n"
            "\n"
            "This combines governance and context management: the gateway controls what is visible **and** prevents a giant tool catalog from filling the context window.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. MCP tunnels: reversing the inbound network model\n"
            "\n"
            "Normally, self-hosting a remote MCP server requires a publicly reachable inbound connection.\n"
            "\n"
            "The source describes an alternative tunnel architecture:\n"
            "\n"
            "```text\n"
            "Traditional\n"
            "Internet client → open inbound port → MCP server\n"
            "\n"
            "Tunnel model\n"
            "MCP server → outbound tunnel → edge proxy ← client\n"
            "```\n"
            "\n"
            "The internal server initiates the connection outward, reducing the need to expose a new inbound port directly to the public internet.\n"
            "\n"
            "The source emphasizes security benefits such as:\n"
            "\n"
            "- smaller inbound attack surface,\n"
            "- connection validation,\n"
            "- encrypted traffic between client and server.\n"
            "\n"
            "The broader architecture lesson is important even if a specific tunnel product changes: **outbound-initiated connectivity can be safer and operationally simpler than exposing internal services directly.**\n"
            "\n"
            "[[IMAGE_NEEDED: Direct inbound MCP access versus tunnel architecture | "
            "Two-panel comparison: direct public inbound connection to internal server versus internal server making outbound connection to edge proxy that clients use | "
            "Learner should notice how the tunnel removes the direct public inbound port]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Code Mode: compressing tool orchestration into deterministic code\n"
            "\n"
            "One recurring MCP problem is tool overload. Imagine hundreds or thousands of available operations. Sending every schema to the model is expensive and can hurt tool selection.\n"
            "\n"
            "**Code Mode** attacks this by translating tool capability into a compact programming interface and asking the model to generate code against that interface.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Large tool catalog\n"
            "      ↓\n"
            "Compact typed API / searchable interface\n"
            "      ↓\n"
            "LLM writes code\n"
            "      ↓\n"
            "Code runs in isolated sandbox\n"
            "      ↓\n"
            "Sandbox performs deterministic chained operations\n"
            "```\n"
            "\n"
            "### Why this can save tokens\n"
            "\n"
            "The model does not need every verbose tool schema in its context. It may also avoid a model round trip after every deterministic tool step.\n"
            "\n"
            "### Client-side Code Mode\n"
            "\n"
            "One architecture runs generated code in a sandbox near the client. The sandbox itself can act like another MCP client and emit the required protocol messages.\n"
            "\n"
            "### Server-side Code Mode\n"
            "\n"
            "Another architecture places the sandbox inside the server and exposes a very small tool surface, such as:\n"
            "\n"
            "```text\n"
            "search(...)\n"
            "execute(...)\n"
            "```\n"
            "\n"
            "The model searches for relevant operations and then writes code that chains them within one isolated execution.\n"
            "\n"
            "### Security requirement\n"
            "\n"
            "Code execution is only attractive if the sandbox is genuinely isolated. The source describes a server-side example with no filesystem access, no environment variables, and restricted outbound networking.\n"
            "\n"
            "[[IMAGE_NEEDED: Code Mode architecture | "
            "A diagram showing LLM receiving compact API → generating code → isolated sandbox → multiple MCP/API calls internally → final result returned to model | "
            "Learner should notice that multiple deterministic operations can happen without repeated model round trips]]\n"
            "\n"
            "---\n"
            "\n"
            "## 7. When Code Mode helps—and when it does not\n"
            "\n"
            "Code Mode is not automatically superior to good tool design.\n"
            "\n"
            "It is most useful when:\n"
            "\n"
            "- the API/tool catalog is huge,\n"
            "- several calls can be composed deterministically,\n"
            "- intermediate outputs do not need semantic interpretation by the LLM,\n"
            "- a strong sandbox already exists.\n"
            "\n"
            "It may offer little value when:\n"
            "\n"
            "- only a few purpose-built tools exist,\n"
            "- tools already represent end-to-end behaviors,\n"
            "- the next action depends on understanding the semantic meaning of the previous result,\n"
            "- sandboxing complexity outweighs token savings.\n"
            "\n"
            "This connects directly to the earlier server-design principle:\n"
            "\n"
            "> **Prefer deterministic work inside one coherent operation when the model does not need to reason between each small step.**\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Alternative MCP frameworks\n"
            "\n"
            "Official SDKs expose the protocol directly, but ecosystem frameworks add opinionated developer experience and production features.\n"
            "\n"
            "The source discusses two major examples.\n"
            "\n"
            "### FastMCP\n"
            "\n"
            "The source describes FastMCP as emphasizing developer experience while adding features around clients, proxies, middleware, authentication, and productionization.\n"
            "\n"
            "An important historical detail in the chapter is that ideas from earlier FastMCP versions influenced the high-level Python SDK server-development style.\n"
            "\n"
            "### arcade-mcp\n"
            "\n"
            "The source describes arcade-mcp as focused on server construction, deployment/authorization integration, and lightweight tool-calling evaluation support.\n"
            "\n"
            "### The lesson is not 'use a framework instead of the SDK'\n"
            "\n"
            "A useful progression is:\n"
            "\n"
            "```text\n"
            "Learn canonical SDK / protocol fundamentals\n"
            "          ↓\n"
            "Understand where production complexity appears\n"
            "          ↓\n"
            "Adopt framework/platform features intentionally\n"
            "```\n"
            "\n"
            "Frameworks can reduce operational work, but they do not replace the need to understand MCP semantics, security, and transports.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Testing tools: direct protocol debugging vs model-connected testing\n"
            "\n"
            "The chapter revisits **MCP Inspector** as a visual debugger and protocol client.\n"
            "\n"
            "Inspector is well suited for directly testing:\n"
            "\n"
            "- tools,\n"
            "- resources,\n"
            "- prompts,\n"
            "- auth flows,\n"
            "- notifications,\n"
            "- raw protocol payloads.\n"
            "\n"
            "But direct protocol correctness is only one layer.\n"
            "\n"
            "### Model-connected testing\n"
            "\n"
            "The source describes MCPJam as an example of a broader testing environment that can connect the MCP server to actual models, display chat traces, inspect full JSON payloads, and compare behavior across models.\n"
            "\n"
            "The distinction is useful:\n"
            "\n"
            "| Testing style | Main question |\n"
            "|---|---|\n"
            "| Inspector-style | Does my MCP server behave correctly as a protocol server? |\n"
            "| Model-connected | Do real models use this MCP server effectively? |\n"
            "\n"
            "The source also describes OAuth-debugging support and agent-friendly CLI interaction in the broader testing ecosystem.\n"
            "\n"
            "{{exercise:M05.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 10. MCP extensions: evolving without bloating the core\n"
            "\n"
            "Not every useful feature belongs in the MCP core protocol.\n"
            "\n"
            "**MCP extensions** allow independently developed features to extend MCP while remaining outside the core protocol specification.\n"
            "\n"
            "### Extension identifiers\n"
            "\n"
            "The source describes identifiers of the general form:\n"
            "\n"
            "```text\n"
            "<vendor-id>/<extension-name>\n"
            "```\n"
            "\n"
            "with reverse-domain-style vendor identifiers strongly encouraged.\n"
            "\n"
            "Example from the source:\n"
            "\n"
            "```text\n"
            "io.modelcontextprotocol/ui\n"
            "```\n"
            "\n"
            "### Why an extension framework matters\n"
            "\n"
            "It allows experimentation and adoption of specialized capabilities without forcing every MCP implementation to support them as core protocol features.\n"
            "\n"
            "The source lists four official extensions at the time of writing:\n"
            "\n"
            "- MCP Apps,\n"
            "- OAuth Client Credentials,\n"
            "- Enterprise-Managed Authorization,\n"
            "- MCP Tasks.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP core plus extensions | "
            "Core MCP in the center with separate extension modules for Apps, OAuth Client Credentials, Enterprise-Managed Authorization, and Tasks | "
            "Learner should notice that extensions augment but do not redefine the core protocol]]\n"
            "\n"
            "---\n"
            "\n"
            "## 11. MCP Apps: tools with server-defined user interfaces\n"
            "\n"
            "MCP Apps extends tools/resources so a server can define a UI that a compatible client renders.\n"
            "\n"
            "A tool description can include UI metadata pointing to a resource containing the interface.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Tool definition\n"
            "  └── _meta.ui.resourceUri\n"
            "          ↓\n"
            "Resource containing HTML/CSS/JavaScript UI\n"
            "          ↓\n"
            "Compatible client renders app in sandboxed iframe\n"
            "```\n"
            "\n"
            "### Why combine tools and resources?\n"
            "\n"
            "The tool performs the operation. The resource provides the UI artifact.\n"
            "\n"
            "Use cases described by the source include:\n"
            "\n"
            "- visualizing server data,\n"
            "- displaying media,\n"
            "- building interactive reports,\n"
            "- providing richer local-data experiences.\n"
            "\n"
            "### Sandboxing matters\n"
            "\n"
            "The source notes that apps run in a sandboxed iframe so the delivered UI cannot freely access host application/user data.\n"
            "\n"
            "---\n"
            "\n"
            "## 12. MCP Auth Extensions\n"
            "\n"
            "The chapter distinguishes core interactive OAuth from extension-based authorization use cases.\n"
            "\n"
            "### OAuth Client Credentials\n"
            "\n"
            "This is useful for **machine-to-machine authorization** where no interactive human login/consent flow is appropriate.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Client application credentials\n"
            "        ↓\n"
            "Authorization server\n"
            "        ↓\n"
            "Access token\n"
            "        ↓\n"
            "Authenticated MCP request\n"
            "```\n"
            "\n"
            "The source describes a Python SDK provider that can be attached to an async HTTP client used by the MCP transport.\n"
            "\n"
            "### Enterprise-Managed Authorization\n"
            "\n"
            "This extension is intended for organizations that want centrally managed enterprise identity rather than requiring every employee to independently authorize every server.\n"
            "\n"
            "The source describes requirements such as:\n"
            "\n"
            "- client-declared extension support,\n"
            "- SSO integration,\n"
            "- use of enterprise identity assertions/tokens,\n"
            "- organization-controlled configuration,\n"
            "- scope handling.\n"
            "\n"
            "> **Support warning from the source:** client support for these auth extensions was limited at the time the chapter was written. Treat compatibility as something to verify, not assume.\n"
            "\n"
            "---\n"
            "\n"
            "## 13. MCP Tasks: durable asynchronous execution\n"
            "\n"
            "Some tool operations should not keep one request open until completion.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- CI/CD pipelines,\n"
            "- large downloads,\n"
            "- model training,\n"
            "- batch computations,\n"
            "- other long-running external jobs.\n"
            "\n"
            "The MCP Tasks extension lets a tool return a placeholder result containing a `taskId` rather than blocking until final completion.\n"
            "\n"
            "### Basic lifecycle\n"
            "\n"
            "```text\n"
            "Client → tools/call\n"
            "Server → CreateTaskResult(taskId)\n"
            "Client continues other work\n"
            "      ↓\n"
            "Client → tasks/get(taskId)\n"
            "Server → status\n"
            "      ↓\n"
            "... poll again ...\n"
            "      ↓\n"
            "Server → completed + final result\n"
            "```\n"
            "\n"
            "### Task state machine\n"
            "\n"
            "The source lists five states:\n"
            "\n"
            "| State | Meaning |\n"
            "|---|---|\n"
            "| `working` | Task is still executing |\n"
            "| `input_required` | Task is paused until the client supplies required information |\n"
            "| `completed` | Finished successfully |\n"
            "| `failed` | Finished unsuccessfully |\n"
            "| `cancelled` | Cancelled by the client |\n"
            "\n"
            "A task can move between `working` and `input_required` before eventually reaching a terminal state.\n"
            "\n"
            "### Durability is the key idea\n"
            "\n"
            "Task state is keyed by `taskId` on the server rather than tied to one network connection. "
            "A client can reconnect later and continue polling if it persisted the task ID.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP Tasks durable state machine | "
            "A state diagram with working ↔ input_required and terminal states completed, failed, cancelled; show client polling tasks/get using taskId | "
            "Learner should notice that task durability is independent of one connection staying alive]]\n"
            "\n"
            "> **SDK support note from the source:** at the time of writing, the chapter states that Python SDK support for Tasks was not yet available and remained on the roadmap.\n"
            "\n"
            "{{exercise:M05.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 14. Contributing to MCP: the SEP process\n"
            "\n"
            "MCP evolves through a formal proposal process centered on **Specification Enhancement Proposals (SEPs)**.\n"
            "\n"
            "A SEP is appropriate for changes such as:\n"
            "\n"
            "- adding protocol features,\n"
            "- changing existing protocol behavior,\n"
            "- removing/deprecating protocol features,\n"
            "- changing governance/process,\n"
            "- proposing/changing protocol extensions.\n"
            "\n"
            "Small documentation fixes or implementation bugs do not normally need a SEP.\n"
            "\n"
            "### Before writing\n"
            "\n"
            "A strong proposal should:\n"
            "\n"
            "- solve a problem others actually experience,\n"
            "- be researched,\n"
            "- align with MCP design principles,\n"
            "- ideally be discussed with relevant contributor groups first.\n"
            "\n"
            "The lesson is broader than MCP: protocol changes should begin with validated ecosystem need, not just an interesting personal idea.\n"
            "\n"
            "---\n"
            "\n"
            "## 15. SEP tracks\n"
            "\n"
            "The source lists four proposal tracks.\n"
            "\n"
            "| Track | Intended use |\n"
            "|---|---|\n"
            "| Standards | New protocol features or changes to the feature set |\n"
            "| Informational | Nonbinding guidance for users/maintainers |\n"
            "| Process | Governance and process changes |\n"
            "| Extensions | New extensions or modifications to extension specifications |\n"
            "\n"
            "Choosing a track matters because it changes the review/implementation obligations.\n"
            "\n"
            "The source specifically notes that **Standards and Extensions proposals require prototype implementation and conformance testing before final approval**.\n"
            "\n"
            "---\n"
            "\n"
            "## 16. What goes into a strong SEP?\n"
            "\n"
            "The source describes a standard SEP document structure including:\n"
            "\n"
            "- preamble/metadata,\n"
            "- abstract,\n"
            "- motivation,\n"
            "- detailed specification,\n"
            "- rationale and alternatives considered,\n"
            "- backward compatibility,\n"
            "- reference implementation,\n"
            "- security implications.\n"
            "\n"
            "This structure forces proposal authors to answer critical protocol-design questions:\n"
            "\n"
            "```text\n"
            "What problem exists?\n"
            "Why is the current protocol insufficient?\n"
            "What exactly changes?\n"
            "Why this design instead of alternatives?\n"
            "What breaks?\n"
            "Can it be implemented?\n"
            "Can compatibility be tested?\n"
            "What new security risks appear?\n"
            "```\n"
            "\n"
            "A protocol proposal is therefore much more than an API sketch.\n"
            "\n"
            "---\n"
            "\n"
            "## 17. SEP review, sponsorship, implementation, and finalization\n"
            "\n"
            "The source describes a lifecycle roughly like this:\n"
            "\n"
            "```text\n"
            "Research / discussion\n"
            "      ↓\n"
            "Write SEP + open pull request\n"
            "      ↓\n"
            "Find maintainer sponsor\n"
            "      ↓\n"
            "Draft review\n"
            "      ↓\n"
            "Formal in-review stage\n"
            "      ↓\n"
            "Accepted / rejected / revision requested\n"
            "      ↓\n"
            "Reference implementation\n"
            "      ↓\n"
            "Conformance tests when required\n"
            "      ↓\n"
            "Final status + future protocol release\n"
            "```\n"
            "\n"
            "### Sponsor role\n"
            "\n"
            "A sponsor helps shepherd the proposal through review and maintainership processes.\n"
            "\n"
            "### Why reference implementations matter\n"
            "\n"
            "A design may sound elegant on paper but fail under real SDK/client/server implementation constraints. A reference implementation proves practical feasibility.\n"
            "\n"
            "### Why conformance tests matter\n"
            "\n"
            "A protocol exists to enable interoperability. Conformance tests turn prose requirements into repeatable checks that SDKs, clients, and servers can run.\n"
            "\n"
            "[[IMAGE_NEEDED: SEP lifecycle | "
            "A flowchart from idea → discussion → PR → sponsor → draft → review → accepted → reference implementation → conformance tests → final → future release | "
            "Learner should notice that implementation and interoperability testing are part of specification work, not an afterthought]]\n"
            "\n"
            "{{exercise:M05.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## 18. Contributing beyond the protocol specification\n"
            "\n"
            "Not every contribution changes the protocol.\n"
            "\n"
            "The source also points toward contributions through:\n"
            "\n"
            "- official SDK issues and pull requests,\n"
            "- documentation fixes,\n"
            "- working groups,\n"
            "- interest groups,\n"
            "- community discussions,\n"
            "- extension implementations,\n"
            "- conformance tooling.\n"
            "\n"
            "This matters because protocol ecosystems depend on far more than one specification repository. "
            "Documentation, test suites, SDK quality, security research, and production experience all feed back into protocol maturity.\n"
            "\n"
            "---\n"
            "\n"
            "## 19. The MCP roadmap and the direction of travel\n"
            "\n"
            "The source closes by emphasizing that MCP changes quickly.\n"
            "\n"
            "At the time described by the chapter, roadmap priority areas included:\n"
            "\n"
            "- transport evolution and security,\n"
            "- agent communication,\n"
            "- governance maturation,\n"
            "- enterprise readiness.\n"
            "\n"
            "The source also mentions areas of broader interest such as:\n"
            "\n"
            "- event-driven updates,\n"
            "- more flexible/streamable result handling,\n"
            "- authorization improvements,\n"
            "- ecosystem maturation.\n"
            "\n"
            "### Skills over MCP\n"
            "\n"
            "One experimental direction described by the chapter explores distributing **skills/know-how**, not only raw tools. "
            "The idea is to let servers share instructions for orchestrating capabilities toward a goal, potentially using existing resource primitives for discovery and updates.\n"
            "\n"
            "The broader lesson is that protocol evolution is moving upward from simple capability exposure toward richer coordination and governance.\n"
            "\n"
            "---\n"
            "\n"
            "## 20. Final mental model for the whole book\n"
            "\n"
            "You can now view MCP as a complete stack rather than only a tool-calling feature.\n"
            "\n"
            "```text\n"
            "Agent / host application\n"
            "        ↓\n"
            "MCP client\n"
            "        ↓\n"
            "Transport + sessions + JSON-RPC\n"
            "        ↓\n"
            "MCP server\n"
            "        ↓\n"
            "Tools / resources / prompts / extensions\n"
            "        ↓\n"
            "External systems, data, workflows\n"
            "\n"
            "Around the stack:\n"
            "Registry → discovery\n"
            "Gateway → governance\n"
            "Evals/testing → reliability\n"
            "Sandbox/auth → security\n"
            "Extensions → new capabilities\n"
            "SEPs/conformance → protocol evolution\n"
            "```\n"
            "\n"
            "The most important conceptual shift is this:\n"
            "\n"
            "**MCP is not only a way to call tools. It is an interoperability layer surrounded by an ecosystem of discovery, governance, testing, security, extension, and open protocol evolution.**\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'The official Registry hosts every MCP server.'\n"
            "\n"
            "**Why this is wrong:** the source describes it primarily as a metadata metaregistry that points to code/packages hosted elsewhere.\n"
            "\n"
            "### Misconception 2: 'A subregistry is just a mirror.'\n"
            "\n"
            "**Why this is wrong:** it can curate, filter, enrich, and add private entries and organization-specific metadata.\n"
            "\n"
            "### Misconception 3: 'An MCP gateway is only a reverse proxy.'\n"
            "\n"
            "**Why this is wrong:** gateways may also centralize auth, policy, routing, observability, discovery, and tool filtering.\n"
            "\n"
            "### Misconception 4: 'Code Mode is always more efficient than tools.'\n"
            "\n"
            "**Why this is wrong:** small purpose-built tool sets may gain little, and semantic decision points between calls may still require model round trips.\n"
            "\n"
            "### Misconception 5: 'Alternative frameworks mean I no longer need to understand the MCP SDK.'\n"
            "\n"
            "**Why this is wrong:** frameworks add convenience, but protocol/security/transport knowledge is still required for correct production systems.\n"
            "\n"
            "### Misconception 6: 'MCP Inspector tells me whether every model will choose my tools correctly.'\n"
            "\n"
            "**Why this is wrong:** Inspector validates server/protocol behavior. Model-connected evaluations test how actual models use the server.\n"
            "\n"
            "### Misconception 7: 'Extensions automatically become part of core MCP.'\n"
            "\n"
            "**Why this is wrong:** extensions are explicitly separate capabilities that can evolve independently.\n"
            "\n"
            "### Misconception 8: 'MCP Tasks are just progress notifications.'\n"
            "\n"
            "**Why this is wrong:** Tasks represent durable asynchronous state keyed by taskId and can survive connection loss/restarts.\n"
            "\n"
            "### Misconception 9: 'Every contribution needs a SEP.'\n"
            "\n"
            "**Why this is wrong:** small documentation fixes, SDK bugs, and normal code contributions use ordinary project contribution paths.\n"
            "\n"
            "### Misconception 10: 'An accepted SEP is finished once the prose is approved.'\n"
            "\n"
            "**Why this is wrong:** relevant tracks also require reference implementation and conformance testing before finalization.\n"
            "\n"
            "### Misconception 11: 'The roadmap is a permanent contract.'\n"
            "\n"
            "**Why this is wrong:** the chapter explicitly presents MCP as fast-moving; roadmap priorities and implementation support can change.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| MCP Registry | Central programmable registry of MCP server metadata described by the source |\n"
            "| Metaregistry | Registry that indexes metadata pointing to packages/code hosted in other registries |\n"
            "| Subregistry | Curated registry that consumes upstream registry data and adds/filter entries/metadata |\n"
            "| Governance tool | Platform/tooling for deploying, securing, authorizing, observing, and operating MCP infrastructure |\n"
            "| MCP gateway | Managed entry point that can route and enforce policy across multiple MCP servers |\n"
            "| MCP tunnel | Outbound-initiated connection architecture that avoids directly exposing an inbound server port |\n"
            "| Context management | Techniques for reducing context/token cost while preserving capability |\n"
            "| Code Mode | Pattern where models write code against compact tool/API interfaces and execute it in an isolated sandbox |\n"
            "| FastMCP | Alternative MCP framework discussed by the source with emphasis on developer experience and production features |\n"
            "| arcade-mcp | Server-focused alternative framework discussed by the source |\n"
            "| MCP Inspector | Direct interactive debugger/client for testing an MCP server |\n"
            "| MCPJam | Model-connected MCP testing environment described by the source |\n"
            "| MCP extension | Capability developed outside the core protocol using a namespaced extension identifier |\n"
            "| MCP Apps | Extension allowing server tools to provide UI resources rendered by compatible clients |\n"
            "| OAuth Client Credentials | Machine-to-machine authorization extension |\n"
            "| Enterprise-Managed Authorization | Extension for centrally managed enterprise identity/authorization |\n"
            "| MCP Tasks | Extension for durable asynchronous tool execution using task IDs and polling |\n"
            "| `taskId` | Durable identifier used by a client to query task state/result |\n"
            "| SEP | Specification Enhancement Proposal used to propose protocol/governance/extension changes |\n"
            "| Standards track | SEP track for core MCP feature changes |\n"
            "| Informational track | SEP track for nonbinding guidance |\n"
            "| Process track | SEP track for governance/process changes |\n"
            "| Extensions track | SEP track for extension specifications |\n"
            "| Sponsor | Maintainer who shepherds a SEP through the review process |\n"
            "| Reference implementation | Working implementation used to demonstrate feasibility of a proposed specification change |\n"
            "| Conformance test | Repeatable test verifying an implementation follows the protocol specification |\n"
            "| Roadmap | Published direction/priorities for future MCP work, subject to change |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before finishing the course, make sure you can answer:\n"
            "\n"
            "1. Why does MCP need ecosystem tools beyond the core protocol?\n"
            "2. What problem does the official Registry solve?\n"
            "3. Why is the Registry described as a metaregistry?\n"
            "4. What can a subregistry add beyond copying official registry entries?\n"
            "5. What responsibilities can an MCP gateway centralize?\n"
            "6. Why can tool minimization at the gateway also improve context efficiency?\n"
            "7. How does a tunnel reduce inbound attack surface?\n"
            "8. What is Code Mode trying to optimize?\n"
            "9. What is the difference between client-side and server-side Code Mode?\n"
            "10. When is Code Mode unlikely to provide much value?\n"
            "11. Why should code execution happen in a strongly isolated sandbox?\n"
            "12. Why learn the official SDK before adopting higher-level frameworks?\n"
            "13. What is the testing difference between Inspector-style testing and model-connected testing?\n"
            "14. Why do extensions exist outside core MCP?\n"
            "15. How is an extension identifier structured?\n"
            "16. How do MCP Apps connect a tool to a user interface?\n"
            "17. When is OAuth Client Credentials more appropriate than an interactive OAuth flow?\n"
            "18. What problem does Enterprise-Managed Authorization attempt to solve?\n"
            "19. Why is MCP Tasks suitable for long-running external jobs?\n"
            "20. What are the five task states listed by the source?\n"
            "21. Why can a durable task survive a client network failure?\n"
            "22. What kinds of changes deserve a SEP?\n"
            "23. What kinds of contributions generally do not need a SEP?\n"
            "24. What are the four SEP tracks?\n"
            "25. Why do Standards and Extensions proposals require prototype/conformance work?\n"
            "26. What sections should a strong SEP contain?\n"
            "27. What role does a sponsor play?\n"
            "28. Why are conformance tests important for interoperability?\n"
            "29. How can developers contribute without changing the protocol spec?\n"
            "30. Which roadmap priority areas are listed in the supplied chapter?\n"
            "31. What is the idea behind Skills over MCP?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Learning MCP does not end with tools, clients, or servers. Real-world MCP systems need discovery, governance, context management, testing, security, extensibility, "
            "and an open contribution process. Understanding that ecosystem is what turns protocol knowledge into production capability—and gives you a path to help evolve the protocol itself.**\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "beyond-core", "title": "Beyond the MCP core", "order": 1},
            {"id": "registry", "title": "MCP Registry", "order": 2},
            {"id": "subregistries", "title": "Subregistries", "order": 3},
            {"id": "governance-tools", "title": "Governance platforms and gateways", "order": 4},
            {"id": "tunnels", "title": "MCP tunnels", "order": 5},
            {"id": "code-mode", "title": "Code Mode", "order": 6},
            {"id": "code-mode-tradeoffs", "title": "Code Mode tradeoffs", "order": 7},
            {"id": "alternative-frameworks", "title": "Alternative MCP frameworks", "order": 8},
            {"id": "testing-tools", "title": "Testing tools", "order": 9},
            {"id": "extensions", "title": "MCP extensions", "order": 10},
            {"id": "mcp-apps", "title": "MCP Apps", "order": 11},
            {"id": "auth-extensions", "title": "MCP Auth Extensions", "order": 12},
            {"id": "tasks", "title": "MCP Tasks", "order": 13},
            {"id": "contributing", "title": "Contributing through SEPs", "order": 14},
            {"id": "sep-tracks", "title": "SEP tracks", "order": 15},
            {"id": "sep-structure", "title": "SEP structure", "order": 16},
            {"id": "sep-lifecycle", "title": "SEP lifecycle", "order": 17},
            {"id": "other-contributions", "title": "Other contribution paths", "order": 18},
            {"id": "roadmap", "title": "MCP roadmap", "order": 19},
            {"id": "final-mental-model", "title": "Final MCP mental model", "order": 20},
        ],
    },

    "exercises": [
        {
            "id": "M05.L01.EX01",

            "title": "Design an Enterprise MCP Subregistry",

            "lesson_code": "M05.L01",

            "section_id": "subregistries",

            "placement": "after_section",

            "description": (
                "Design a curated internal registry that consumes public MCP metadata but exposes "
                "only organization-approved servers."
            ),

            "instructions": (
                "Your company wants employees to discover MCP servers safely.\n\n"
                "1. Define what metadata you would import from the official Registry.\n"
                "2. Define at least five organization-specific _meta fields.\n"
                "3. Create an approval workflow from discovered → security-reviewed → approved → blocked.\n"
                "4. Decide whether private/internal servers appear in the same registry.\n"
                "5. Explain how clients/agents should query the subregistry.\n"
                "6. Explain what the subregistry guarantees and what it does NOT guarantee.\n"
                "7. Describe one process for keeping upstream metadata synchronized."
            ),

            "expected_output": (
                "A subregistry architecture, metadata schema, trust workflow, client-discovery flow, "
                "and explanation of its security boundaries."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "mcp-registry",
                "subregistries",
                "governance",
                "security-architecture",
            ],
        },

        {
            "id": "M05.L01.EX02",

            "title": "Choose a Context-Management Strategy",

            "lesson_code": "M05.L01",

            "section_id": "testing-tools",

            "placement": "after_section",

            "description": (
                "Compare purpose-built tools, gateway tool search, and Code Mode for several MCP applications."
            ),

            "instructions": (
                "Choose an approach for each scenario:\n\n"
                "A. An internal assistant with 6 carefully designed tools.\n"
                "B. A cloud platform exposing 2,000+ operations.\n"
                "C. A workflow where each next step depends on interpreting the natural-language meaning of the previous tool result.\n"
                "D. A deterministic batch workflow with 30 API calls and a hardened sandbox already available.\n\n"
                "For each scenario:\n"
                "1. Choose normal tools, search/execute progressive disclosure, or Code Mode.\n"
                "2. Explain token/context implications.\n"
                "3. Explain model round-trip implications.\n"
                "4. Explain security/sandbox implications.\n"
                "5. State how you would test the resulting MCP interface with direct protocol tooling and model-connected evaluation."
            ),

            "expected_output": (
                "A four-row tradeoff table with justified architecture and testing choices."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "code-mode",
                "context-management",
                "tool-design",
                "evaluation",
            ],
        },

        {
            "id": "M05.L01.EX03",

            "title": "Model a Durable MCP Task",

            "lesson_code": "M05.L01",

            "section_id": "tasks",

            "placement": "after_section",

            "description": (
                "Design an asynchronous task lifecycle for a long-running operation that can require "
                "additional user input and survive client disconnection."
            ),

            "instructions": (
                "Your MCP server starts a model-training job that may run for two hours.\n\n"
                "1. Define what the initial tools/call returns.\n"
                "2. Define how the client stores taskId durably.\n"
                "3. Show state transitions from working to input_required and back to working.\n"
                "4. Show one successful terminal path and one failed path.\n"
                "5. Explain how cancellation should be represented.\n"
                "6. Explain how the client resumes after restarting its machine.\n"
                "7. Explain why ordinary progress notifications alone are insufficient for this design."
            ),

            "expected_output": (
                "A task state diagram and polling/recovery workflow using taskId."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "mcp-tasks",
                "asynchronous-workflows",
                "durability",
                "state-machines",
            ],
        },

        {
            "id": "M05.L01.EX04",

            "title": "Draft an SEP Proposal Outline",

            "lesson_code": "M05.L01",

            "section_id": "sep-lifecycle",

            "placement": "after_section",

            "description": (
                "Practice turning a protocol idea into a structured, reviewable specification proposal."
            ),

            "instructions": (
                "Imagine you want to propose a new MCP extension for resumable streamed results.\n\n"
                "1. Choose the correct SEP track and justify it.\n"
                "2. Write a one-paragraph abstract.\n"
                "3. Define the problem/motivation.\n"
                "4. List the major specification changes you would need to describe.\n"
                "5. Identify backward-compatibility risks.\n"
                "6. Identify at least three security implications.\n"
                "7. Describe a prototype/reference implementation.\n"
                "8. Define at least three conformance tests.\n"
                "9. Describe how you would seek discussion and a maintainer sponsor."
            ),

            "expected_output": (
                "A structured SEP outline covering track, abstract, motivation, specification, "
                "compatibility, security, reference implementation, conformance, and review path."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "sep",
                "protocol-design",
                "conformance-testing",
                "security-review",
            ],
        },
    ],

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "MCP Ecosystem and Extensions — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",

                "section_id": "registry",

                "question": "What is the main role of the official MCP Registry in the supplied chapter?",

                "options": [
                    "To execute every MCP server directly",
                    "To provide standardized discoverable metadata that points to MCP server packages/code",
                    "To replace all package registries such as PyPI and npm",
                    "To enforce every organization's internal security policy",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes the Registry as a programmable metaregistry of server "
                    "metadata that references packages/artifacts living elsewhere."
                ),
            },

            {
                "id": "M05.L01.Q02",

                "section_id": "subregistries",

                "question": "What can a subregistry add beyond the official Registry?",

                "options": [
                    "Nothing; it must be an exact mirror",
                    "Curation, private entries, filtering, and registry-specific metadata",
                    "A replacement JSON-RPC protocol",
                    "Direct access to every user's credentials",
                ],

                "correct": 1,

                "explanation": (
                    "Subregistries can curate upstream entries and add organization/community-specific metadata."
                ),
            },

            {
                "id": "M05.L01.Q03",

                "section_id": "code-mode",

                "question": "What problem is Code Mode primarily trying to reduce?",

                "options": [
                    "The need for any MCP server at all",
                    "Large tool-schema context and repeated model round trips for deterministic orchestration",
                    "The use of JSON-RPC request IDs",
                    "The need for sandboxing",
                ],

                "correct": 1,

                "explanation": (
                    "Code Mode compresses the interface and executes deterministic chains inside a sandbox, "
                    "which can reduce tool-schema tokens and round trips."
                ),
            },

            {
                "id": "M05.L01.Q04",

                "section_id": "code-mode-tradeoffs",

                "question": "When is Code Mode least likely to provide a major benefit?",

                "options": [
                    "When thousands of API operations are available",
                    "When only a few well-designed end-to-end tools exist",
                    "When deterministic calls can be chained without semantic interpretation",
                    "When a secure sandbox already exists",
                ],

                "correct": 1,

                "explanation": (
                    "A small, purpose-built tool catalog already avoids much of the context/tool-selection problem."
                ),
            },

            {
                "id": "M05.L01.Q05",

                "section_id": "testing-tools",

                "question": "What is the main distinction between MCP Inspector and model-connected testing tools described by the chapter?",

                "options": [
                    "Inspector cannot connect to MCP servers",
                    "Inspector focuses on direct protocol/server behavior, while model-connected tools also test how real models interact with the server",
                    "Model-connected tools cannot inspect JSON payloads",
                    "Inspector is only for OAuth",
                ],

                "correct": 1,

                "explanation": (
                    "Direct protocol correctness and model behavior are different testing layers."
                ),
            },

            {
                "id": "M05.L01.Q06",

                "section_id": "extensions",

                "question": "Why does MCP have an extension mechanism?",

                "options": [
                    "To require every client to implement every experimental feature",
                    "To allow useful capabilities to evolve outside the core protocol",
                    "To replace SEPs entirely",
                    "To remove namespaces from MCP",
                ],

                "correct": 1,

                "explanation": (
                    "Extensions add independently evolving capabilities without bloating core MCP."
                ),
            },

            {
                "id": "M05.L01.Q07",

                "section_id": "mcp-apps",

                "question": "How does an MCP App connect a tool to its user interface?",

                "options": [
                    "By embedding a desktop executable inside the tool name",
                    "By using tool UI metadata that points to a resource containing the UI",
                    "By replacing tools/call with HTTP GET",
                    "By storing the UI in the OAuth token",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes tool metadata pointing at a UI resource that a compatible client renders."
                ),
            },

            {
                "id": "M05.L01.Q08",

                "section_id": "tasks",

                "question": "What makes MCP Tasks different from keeping one long-running request open?",

                "options": [
                    "A durable taskId identifies server-side state that can be polled across connections",
                    "Tasks cannot fail or be cancelled",
                    "Tasks require stdio only",
                    "Tasks remove the need for a server",
                ],

                "correct": 0,

                "explanation": (
                    "Task state is durable and keyed by taskId, allowing clients to reconnect and continue polling."
                ),
            },

            {
                "id": "M05.L01.Q09",

                "section_id": "sep-tracks",

                "question": "Which SEP track is used for proposing a new MCP extension?",

                "options": [
                    "Informational",
                    "Process",
                    "Extensions",
                    "Documentation",
                ],

                "correct": 2,

                "explanation": (
                    "The Extensions track is intended for new extensions and changes to existing extensions."
                ),
            },

            {
                "id": "M05.L01.Q10",

                "section_id": "sep-lifecycle",

                "question": "Why are reference implementations and conformance tests important in protocol evolution?",

                "options": [
                    "They make documentation unnecessary",
                    "They demonstrate feasibility and verify interoperable implementation of the specification",
                    "They replace maintainers and review",
                    "They ensure every implementation uses the same programming language",
                ],

                "correct": 1,

                "explanation": (
                    "Reference implementations prove practicality, while conformance tests provide repeatable interoperability checks."
                ),
            },

            {
                "id": "M05.L01.Q11",

                "section_id": "roadmap",

                "question": "How should the roadmap priorities in the source be interpreted?",

                "options": [
                    "As permanent guarantees that cannot change",
                    "As source-time priorities in a fast-moving project",
                    "As features already supported by every SDK/client",
                    "As requirements for every MCP server",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter explicitly emphasizes that MCP evolves quickly, so roadmap priorities are time-sensitive."
                ),
            },

            {
                "id": "M05.L01.Q12",

                "section_id": "final-mental-model",

                "type": "open",

                "question": (
                    "Design the ecosystem architecture for an enterprise MCP platform with dozens of internal "
                    "and public servers. Explain how you would use a registry/subregistry, gateway, testing/evaluations, "
                    "context management or Code Mode, authorization, extensions such as Tasks where appropriate, "
                    "and an internal process for proposing/contributing protocol changes through SEPs."
                ),
            },
        ],

        "passing_score": 70,
    },
}
