"""M03.L03 — Testing, Securing, and Sharing Your MCP Server.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 7 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L03"

MODULE_ORDER = 3

MODULE_TITLE = "Building MCP Servers"

MODULE_DESCRIPTION = (
    "Finish the MCP server lifecycle by testing behavior, evaluating model-facing "
    "quality, securing local and remote deployments, applying security frameworks, "
    "and packaging, deploying, and publishing servers for real users."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Testing, Securing, and Sharing Your MCP Server",

    "slug": "ai-agents-mcp-m03-l03",

    "description": (
        "A production-focused lesson covering MCP server testing, MCP Inspector, "
        "automated tests, evaluations, prompt/tool quality measurement, server security, "
        "sandboxing, OAuth, RBAC, gateways, observability, prompt-injection frameworks, "
        "local packaging, remote deployment, containerization, and registry publishing."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.5,

    "skill_tags": [
        "mcp-server",
        "testing",
        "mcp-inspector",
        "pytest",
        "integration-testing",
        "evaluations",
        "tool-choice-evaluation",
        "security",
        "prompt-injection",
        "oauth",
        "rbac",
        "sandboxing",
        "observability",
        "mcp-gateway",
        "deployment",
        "mcp-registry",
    ],

    "prerequisite_ids": ["M03.L02"],

    "lesson": {
        "title": "Testing, Securing, and Sharing Your MCP Server",

        "content": (
            "# Testing, Securing, and Sharing Your MCP Server\n"
            "\n"
            "> **Lesson:** M03.L03  \n"
            "> **Module:** Building MCP Servers  \n"
            "> **Source alignment:** Chapter 7 supplied by the course author. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Choose an appropriate testing depth based on server risk and deployment context.\n"
            "- Use MCP Inspector as a rapid manual development and debugging loop.\n"
            "- Distinguish unit, integration, end-to-end, and evaluation-style testing.\n"
            "- Design automated tests for server functions, client interactions, and external dependencies.\n"
            "- Evaluate prompts and tools across multiple models, cost levels, and task scenarios.\n"
            "- Measure tool-choice accuracy and structured-output adherence.\n"
            "- Explain why evaluations complement but do not replace software tests.\n"
            "- Identify important MCP server vulnerability classes and their mitigations.\n"
            "- Apply sandboxing, least privilege, OAuth, RBAC, gateways, observability, and supply-chain controls.\n"
            "- Explain token pass-through and confused-deputy risks at a conceptual level.\n"
            "- Use the Lethal Trifecta and MCP Colors frameworks to reason about tool combinations.\n"
            "- Package local MCP servers for users.\n"
            "- Prepare remote servers for Streamable HTTP and horizontal scaling.\n"
            "- Mount MCP servers inside ASGI applications.\n"
            "- Containerize and publish an MCP server.\n"
            "- Explain the role of the MCP Registry in discovery and distribution.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Building the server is not the end\n"
            "\n"
            "By this point, an MCP server may already expose tools, prompts, and resources, support useful utilities, and participate in richer client workflows. "
            "That still does not make it production ready.\n"
            "\n"
            "The source organizes the remaining work into four major responsibilities:\n"
            "\n"
            "```text\n"
            "Build server\n"
            "    ↓\n"
            "Test correctness\n"
            "    ↓\n"
            "Evaluate model-facing behavior\n"
            "    ↓\n"
            "Secure the system\n"
            "    ↓\n"
            "Package / deploy / publish\n"
            "```\n"
            "\n"
            "These responsibilities solve different problems:\n"
            "\n"
            "| Discipline | Main question |\n"
            "|---|---|\n"
            "| Software testing | Does the code behave correctly? |\n"
            "| Evaluations | Do models use the server effectively? |\n"
            "| Security | Can malicious or unsafe behavior cause damage or data exposure? |\n"
            "| Distribution | Can real users install, connect to, and operate the server reliably? |\n"
            "\n"
            "A production server needs all four perspectives.\n"
            "\n"
            "[[IMAGE_NEEDED: MCP server production lifecycle | "
            "A pipeline from server implementation through testing, evaluations, security hardening, packaging/deployment, and publication | "
            "Learner should notice that passing unit tests is only one stage of production readiness]]\n"
            "\n"
            "---\n"
            "\n"
            "## 2. How much testing does an MCP server need?\n"
            "\n"
            "The chapter does not recommend one universal test-coverage target. Instead, testing depth depends on **risk**.\n"
            "\n"
            "A private experiment that exposes a calculator tool has a very different failure cost from a remote multitenant server handling confidential data or financial actions.\n"
            "\n"
            "Ask questions such as:\n"
            "\n"
            "- Who will use the server?\n"
            "- Is the server local or remotely exposed?\n"
            "- What data can it access?\n"
            "- Can its tools mutate state?\n"
            "- Can errors create financial, privacy, compliance, or operational damage?\n"
            "- How many external systems does it depend on?\n"
            "\n"
            "### Testing levels\n"
            "\n"
            "| Level | What it verifies |\n"
            "|---|---|\n"
            "| Unit test | Individual functions and business logic |\n"
            "| Integration test | Interactions with clients, databases, files, APIs, authorization, etc. |\n"
            "| End-to-end test | Full request path through the running server and client |\n"
            "| Evaluation | Whether models choose/use server capabilities effectively |\n"
            "\n"
            "Testing should be proportional to the server's risk profile, not driven by a desire to maximize a coverage percentage for its own sake.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. MCP Inspector as a development loop\n"
            "\n"
            "MCP Inspector acts like an interactive MCP client designed for development and debugging. It can connect to your server, discover its capabilities, trigger operations, and show the request/response traffic.\n"
            "\n"
            "The chapter recommends an iterative workflow:\n"
            "\n"
            "```text\n"
            "1. Build a minimal connectable server skeleton.\n"
            "2. Connect MCP Inspector.\n"
            "3. Verify primitive discovery.\n"
            "4. Implement one behavior.\n"
            "5. Refresh Inspector.\n"
            "6. Test the happy path.\n"
            "7. Test edge/failure paths.\n"
            "8. Inspect notifications and message history.\n"
            "9. Repeat for the next behavior.\n"
            "10. Test remote deployment when ready.\n"
            "```\n"
            "\n"
            "### Why Inspector is valuable\n"
            "\n"
            "A Python function can appear correct in isolation yet expose the wrong MCP schema, message, notification, or capability metadata. Inspector tests the interface the client actually sees.\n"
            "\n"
            "### Specialized views\n"
            "\n"
            "The source describes Inspector views for features such as:\n"
            "\n"
            "- tools,\n"
            "- resources,\n"
            "- prompts,\n"
            "- sampling,\n"
            "- elicitations,\n"
            "- roots,\n"
            "- authentication,\n"
            "- message history,\n"
            "- server notifications.\n"
            "\n"
            "For sampling, a developer can inspect the request and simulate approval or rejection without necessarily invoking a real model. "
            "For elicitation, Inspector can render the schema as a form and test accept/decline/cancel paths.\n"
            "\n"
            "[[IMAGE_NEEDED: Inspector-driven MCP development loop | "
            "A circular workflow showing code change → reconnect Inspector → discover capability → execute happy path → inspect messages → test edge cases → code change | "
            "Learner should notice that testing happens continuously during development rather than after the server is finished]]\n"
            "\n"
            "{{exercise:M03.L03.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Automated testing: unit and integration tests\n"
            "\n"
            "Manual Inspector testing is excellent for rapid feedback, but it is not enough for regression protection.\n"
            "\n"
            "### Unit tests\n"
            "\n"
            "Unit-test MCP code using familiar software techniques:\n"
            "\n"
            "- `pytest`,\n"
            "- fixtures,\n"
            "- mocks/fakes,\n"
            "- happy-path assertions,\n"
            "- failure-path assertions,\n"
            "- coverage measurement when useful.\n"
            "\n"
            "If a tool function contains business logic such as input validation or calculations, test that logic directly.\n"
            "\n"
            "### Why mocking matters\n"
            "\n"
            "MCP servers often depend on:\n"
            "\n"
            "- databases,\n"
            "- external APIs,\n"
            "- local files,\n"
            "- identity providers,\n"
            "- client-provided capabilities.\n"
            "\n"
            "Unit tests should isolate your code from unstable or expensive dependencies whenever the dependency itself is not what you are testing.\n"
            "\n"
            "### Integration tests\n"
            "\n"
            "Integration tests validate boundaries:\n"
            "\n"
            "- connect/disconnect behavior,\n"
            "- real or test database access,\n"
            "- API calls,\n"
            "- resource file loading,\n"
            "- authorization flows,\n"
            "- simple MCP-client-to-server interactions.\n"
            "\n"
            "A small test client can make protocol requests to a running test server and verify results, which moves testing closer to the behavior experienced by real applications.\n"
            "\n"
            "### Real-client integration testing\n"
            "\n"
            "The source also uses Claude Desktop as an example of testing with a real-world client. The broader lesson is to test against at least one realistic host environment, not only against your own test harness.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Why MCP servers need evaluations\n"
            "\n"
            "Traditional software tests answer deterministic questions such as:\n"
            "\n"
            "> Given these inputs, did the function return the expected result?\n"
            "\n"
            "But MCP servers expose model-facing interfaces. A tool can be perfectly implemented and still be difficult for an LLM to choose correctly because its name or description is confusing.\n"
            "\n"
            "Evaluations answer questions such as:\n"
            "\n"
            "- Does the model choose the correct tool?\n"
            "- Does the prompt produce the intended behavior?\n"
            "- Does output follow the expected structure?\n"
            "- Does behavior remain acceptable across model families and sizes?\n"
            "- How expensive is the interaction?\n"
            "- Do guardrails hold?\n"
            "\n"
            "### Evaluations improve the interface, not usually the base model\n"
            "\n"
            "As an MCP server developer, you usually cannot retrain the users' models. Instead, evaluation results help you improve:\n"
            "\n"
            "- tool names,\n"
            "- tool descriptions,\n"
            "- argument schemas,\n"
            "- prompt templates,\n"
            "- examples,\n"
            "- output formats,\n"
            "- server interaction design.\n"
            "\n"
            "[[IMAGE_NEEDED: Software tests versus LLM evaluations | "
            "A side-by-side diagram: deterministic software test checks function correctness while evaluation sends natural-language tasks to models and measures tool choice/prompt behavior/cost | "
            "Learner should notice that both are required because they measure different failure modes]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Designing useful MCP evaluations\n"
            "\n"
            "The chapter identifies several useful evaluation dimensions:\n"
            "\n"
            "- tool-choice performance,\n"
            "- tool-use cost,\n"
            "- guardrail adherence,\n"
            "- prompt cost,\n"
            "- prompt correctness,\n"
            "- structured-output adherence,\n"
            "- LLM-as-a-judge scoring for appropriate tasks,\n"
            "- performance across model families and sizes.\n"
            "\n"
            "### Prompt evaluation workflow\n"
            "\n"
            "A practical process is:\n"
            "\n"
            "```text\n"
            "1. Choose representative prompt/tasks.\n"
            "2. Run them a few times on one model.\n"
            "3. Inspect obvious failures and costs.\n"
            "4. Refine the prompt.\n"
            "5. Add automated checks.\n"
            "6. Run across several relevant models.\n"
            "7. Analyze failures.\n"
            "8. Add stronger rubrics/judges if useful.\n"
            "9. Repeat until behavior stabilizes.\n"
            "```\n"
            "\n"
            "This iterative examination of failure patterns is a form of **error analysis**.\n"
            "\n"
            "### Simple assertions vs rubric grading\n"
            "\n"
            "A basic evaluation may check whether the response contains a required phrase or structure. This is cheap and deterministic but may produce false positives/negatives.\n"
            "\n"
            "An LLM-as-a-judge can score against a rubric, capturing more semantic quality, but it is more expensive and itself requires careful evaluation.\n"
            "\n"
            "### Cross-model evaluation matters for MCP\n"
            "\n"
            "An application developer can choose one model and tune specifically for it. A reusable MCP server author often cannot. "
            "Therefore, tool definitions and prompts should be evaluated across models likely to be used by your users.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Evaluating tool-choice behavior\n"
            "\n"
            "A simple tool-choice evaluation dataset can contain pairs:\n"
            "\n"
            "```text\n"
            "(natural-language request, expected tool)\n"
            "```\n"
            "\n"
            "For each task, let a model see the available tool definitions and record which tool it selects.\n"
            "\n"
            "A simple metric is:\n"
            "\n"
            "```text\n"
            "tool-choice accuracy = correct tool selections / total test tasks\n"
            "```\n"
            "\n"
            "### What a tool-choice score can reveal\n"
            "\n"
            "Low performance may indicate:\n"
            "\n"
            "- overlapping tool responsibilities,\n"
            "- vague names,\n"
            "- confusing descriptions,\n"
            "- incomplete parameter documentation,\n"
            "- too many active tools,\n"
            "- task ambiguity.\n"
            "\n"
            "### What it cannot prove\n"
            "\n"
            "A high tool-choice score does not prove the entire system is reliable. It may not capture:\n"
            "\n"
            "- multi-turn context,\n"
            "- user corrections,\n"
            "- real client system prompts,\n"
            "- failures in the tool itself,\n"
            "- external dependency outages,\n"
            "- adversarial prompts.\n"
            "\n"
            "For stronger end-to-end evaluation, the source suggests running tasks through a simple MCP client or using frameworks with MCP integrations.\n"
            "\n"
            "{{exercise:M03.L03.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Security mindset: assume language is an attack surface\n"
            "\n"
            "MCP servers combine two difficult security domains:\n"
            "\n"
            "1. ordinary software/network security,\n"
            "2. LLM systems that consume untrusted natural-language content.\n"
            "\n"
            "The chapter argues that it is unrealistic to detect every possible malicious phrasing. A better goal is to design the system so that dangerous instructions **cannot easily succeed even if the model is influenced**.\n"
            "\n"
            "This leads to a layered strategy:\n"
            "\n"
            "```text\n"
            "Code-level validation\n"
            "      +\n"
            "Least privilege\n"
            "      +\n"
            "Sandboxing/isolation\n"
            "      +\n"
            "Strong authorization\n"
            "      +\n"
            "Observability\n"
            "      +\n"
            "Human approval for sensitive actions\n"
            "```\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Injection and path-related vulnerabilities\n"
            "\n"
            "The source begins with familiar injection classes that remain relevant in MCP systems.\n"
            "\n"
            "### SQL injection\n"
            "\n"
            "If a tool inserts untrusted text into database queries through raw string interpolation, an attacker may be able to alter the query.\n"
            "\n"
            "**Primary defense:** parameterized queries plus restricted database permissions.\n"
            "\n"
            "### Command injection\n"
            "\n"
            "If user/model-controlled strings are passed unsafely to a shell, arbitrary commands may be executed.\n"
            "\n"
            "**Defenses:** avoid shells when possible, use allowlisted commands/arguments, isolate the process, and reduce OS permissions.\n"
            "\n"
            "### Prompt injection\n"
            "\n"
            "Prompt injection is different because malicious instructions can arrive inside content the model is expected to read: websites, emails, files, issue descriptions, documents, and other tool results.\n"
            "\n"
            "The server developer cannot solve prompt injection by simply filtering a list of bad phrases. Instead, ask what damage could occur if the model followed a malicious instruction and remove that capability where possible.\n"
            "\n"
            "For example:\n"
            "\n"
            "- sandbox file access,\n"
            "- reduce network reachability,\n"
            "- restrict tool scopes,\n"
            "- require confirmation for sensitive actions,\n"
            "- sanitize fetched web content and URLs,\n"
            "- separate data-reading and external-communication capabilities.\n"
            "\n"
            "### Path traversal\n"
            "\n"
            "Any tool or resource that accepts a filesystem path should assume the path is untrusted.\n"
            "\n"
            "The robust pattern from the source is:\n"
            "\n"
            "```text\n"
            "requested = Path(user_value).resolve()\n"
            "allowed = Path(base_dir).resolve()\n"
            "verify requested.is_relative_to(allowed)\n"
            "```\n"
            "\n"
            "Resolving first handles relative segments and symlinks much more safely than string-prefix checks.\n"
            "\n"
            "[[IMAGE_NEEDED: Layered defenses against injected input | "
            "A diagram where untrusted model/user/content input passes through validation, least-privilege permissions, sandbox boundaries, and controlled tool execution before reaching database/filesystem/network resources | "
            "Learner should notice that security does not depend on one text filter]]\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Access control, denial of service, and token boundaries\n"
            "\n"
            "### Access-control vulnerabilities\n"
            "\n"
            "A remote MCP server may be multitenant. Authentication alone is not enough; authorization must ensure that one user cannot access another user's objects or privileged actions.\n"
            "\n"
            "This can require:\n"
            "\n"
            "- object-level authorization,\n"
            "- per-tool permissions,\n"
            "- plan/role restrictions,\n"
            "- scoped credentials.\n"
            "\n"
            "### DoS/DDoS\n"
            "\n"
            "Remote servers can be overwhelmed by request volume. Standard defenses remain relevant:\n"
            "\n"
            "- rate limiting,\n"
            "- throttling,\n"
            "- quotas,\n"
            "- bounded request sizes,\n"
            "- infrastructure-level traffic controls.\n"
            "\n"
            "### Token pass-through\n"
            "\n"
            "The source warns against taking an authorization token supplied by a client and blindly forwarding it to an unrelated third-party service.\n"
            "\n"
            "Why this is dangerous:\n"
            "\n"
            "- the token may have been issued for another audience,\n"
            "- responsibility/auditing boundaries become unclear,\n"
            "- stolen or over-scoped tokens can be abused,\n"
            "- the server may unintentionally act with privileges it should not possess.\n"
            "\n"
            "A cleaner architecture uses credentials issued specifically to the server's relationship with the downstream service. "
            "If client-provided credentials truly must be accepted, validate the token and its scope rather than blindly forwarding it.\n"
            "\n"
            "---\n"
            "\n"
            "## 11. The confused-deputy problem\n"
            "\n"
            "A **confused deputy** is a more privileged system that is tricked into exercising its authority on behalf of a less privileged actor.\n"
            "\n"
            "In MCP-related authorization flows, the risk can appear when a server proxies access to another service and fails to preserve the boundaries between different clients/users during OAuth consent and redirects.\n"
            "\n"
            "The source's mitigation themes are standard OAuth security principles:\n"
            "\n"
            "- preserve per-user/per-client consent boundaries,\n"
            "- show clear consent information,\n"
            "- validate redirect URIs against an allowed registry,\n"
            "- use and validate the OAuth `state` parameter,\n"
            "- protect consent pages from CSRF/clickjacking,\n"
            "- avoid designs where a shared static identity collapses distinct users into one trust boundary.\n"
            "\n"
            "The key idea is broader than OAuth: **never let a lower-privilege actor cause a privileged server to reuse authority outside the actor's legitimate scope.**\n"
            "\n"
            "---\n"
            "\n"
            "## 12. A three-layer security architecture\n"
            "\n"
            "The chapter groups practical defenses into three layers.\n"
            "\n"
            "### Layer 1 — Infrastructure foundations\n"
            "\n"
            "The foundational tool is **sandboxing**: isolate the server from resources it does not need.\n"
            "\n"
            "For local servers, this can mean:\n"
            "\n"
            "- Docker containers,\n"
            "- virtual machines,\n"
            "- restricted filesystem mounts,\n"
            "- constrained network access,\n"
            "- non-privileged users.\n"
            "\n"
            "The principle is simple: if a compromised tool cannot reach sensitive data or dangerous system capabilities, the impact of compromise is smaller.\n"
            "\n"
            "### Layer 2 — Access control\n"
            "\n"
            "This layer applies the **principle of least privilege**.\n"
            "\n"
            "Mechanisms include:\n"
            "\n"
            "- OAuth 2.1,\n"
            "- scoped access tokens,\n"
            "- object-level authorization,\n"
            "- role-based access control (RBAC),\n"
            "- MCP gateways that centralize authentication, authorization, routing, and policy.\n"
            "\n"
            "### Layer 3 — Operational controls\n"
            "\n"
            "You also need visibility and response capability:\n"
            "\n"
            "- structured logging,\n"
            "- traces,\n"
            "- metrics,\n"
            "- alerts,\n"
            "- dependency vulnerability scanning,\n"
            "- supply-chain monitoring,\n"
            "- human approval of sensitive actions.\n"
            "\n"
            "[[IMAGE_NEEDED: Three-layer MCP server security architecture | "
            "A stacked diagram with infrastructure isolation at the bottom, access control in the middle, and observability/supply-chain/HITL controls at the top | "
            "Learner should notice that strong security combines prevention, authorization, and detection/response]]\n"
            "\n"
            "{{exercise:M03.L03.EX03}}\n"
            "\n"
            "---\n"
            "\n"
            "## 13. OAuth, RBAC, and gateways for remote servers\n"
            "\n"
            "### MCP server as an OAuth resource server\n"
            "\n"
            "For a protected remote deployment, the MCP server commonly acts as a **resource server**. A separate authorization server authenticates users and issues tokens.\n"
            "\n"
            "The server verifies incoming access tokens before allowing access.\n"
            "\n"
            "The Python SDK pattern described in the source uses:\n"
            "\n"
            "- authorization settings,\n"
            "- a token verifier implementation,\n"
            "- the verified token's scopes/claims.\n"
            "\n"
            "### RBAC\n"
            "\n"
            "RBAC assigns allowed actions based on role rather than individual identity.\n"
            "\n"
            "Example:\n"
            "\n"
            "| Role | Allowed operations |\n"
            "|---|---|\n"
            "| Viewer | Read project data |\n"
            "| Operator | Read + run operational tools |\n"
            "| Admin | Manage configuration and sensitive actions |\n"
            "\n"
            "Always design roles around the least privilege required for legitimate work.\n"
            "\n"
            "### MCP gateways\n"
            "\n"
            "A gateway sits between clients and one or more deployed MCP servers. Depending on the implementation, it can centralize:\n"
            "\n"
            "- authentication,\n"
            "- authorization,\n"
            "- traffic management,\n"
            "- routing,\n"
            "- policy enforcement,\n"
            "- server administration.\n"
            "\n"
            "This is especially useful when operating many servers rather than embedding the same policy logic independently into each deployment.\n"
            "\n"
            "---\n"
            "\n"
            "## 14. Observability and supply-chain security\n"
            "\n"
            "Security requires knowing what your system is doing.\n"
            "\n"
            "### Observability\n"
            "\n"
            "Production systems should consider:\n"
            "\n"
            "- structured logs,\n"
            "- distributed tracing,\n"
            "- metrics,\n"
            "- alerting,\n"
            "- latency/error dashboards,\n"
            "- authorization-event monitoring.\n"
            "\n"
            "The source mentions vendor-neutral observability approaches such as OpenTelemetry and metrics platforms such as Prometheus, as examples of the broader pattern.\n"
            "\n"
            "### Supply-chain management\n"
            "\n"
            "Your server is more than your own source code. Dependencies, base images, database software, and build tooling can introduce vulnerabilities.\n"
            "\n"
            "A healthy process includes:\n"
            "\n"
            "- dependency updates,\n"
            "- reproducible/pinned builds,\n"
            "- vulnerability scans,\n"
            "- static analysis,\n"
            "- CI/CD security checks.\n"
            "\n"
            "### HITL monitoring\n"
            "\n"
            "Sensitive actions should often retain a human approval step. MCP client UX usually owns the approval dialog, but server workflows should be designed to accept rejection/cancellation cleanly.\n"
            "\n"
            "---\n"
            "\n"
            "## 15. Security framework: the Lethal Trifecta\n"
            "\n"
            "The source introduces a useful way to reason about prompt-injection risk. Risk becomes especially serious when one agent/server workflow combines all three of these capabilities:\n"
            "\n"
            "1. **Access to private data**\n"
            "2. **Exposure to untrusted content**\n"
            "3. **Ability to communicate with third parties**\n"
            "\n"
            "Why is this combination dangerous?\n"
            "\n"
            "```text\n"
            "Untrusted content contains malicious instructions\n"
            "          ↓\n"
            "Agent can access confidential data\n"
            "          ↓\n"
            "Agent can send data outside the trust boundary\n"
            "          ↓\n"
            "Possible exfiltration\n"
            "```\n"
            "\n"
            "The framework encourages **removing at least one side of the triangle** for any risky workflow.\n"
            "\n"
            "Examples of structural mitigations:\n"
            "\n"
            "- restrict private-data scope,\n"
            "- isolate untrusted content processing,\n"
            "- disable or narrowly constrain outbound communication,\n"
            "- enforce per-resource OAuth scopes,\n"
            "- use gateway middleware to deny suspicious cross-boundary requests.\n"
            "\n"
            "[[IMAGE_NEEDED: Lethal Trifecta triangle | "
            "A triangle labeled Private Data, Untrusted Content, and Third-Party Communication, with a warning in the center and examples of controls that remove one edge | "
            "Learner should notice that security can improve by structurally breaking the dangerous combination]]\n"
            "\n"
            "---\n"
            "\n"
            "## 16. Security framework: MCP Colors\n"
            "\n"
            "The chapter also presents a tool-classification exercise called **MCP Colors**.\n"
            "\n"
            "The framework uses:\n"
            "\n"
            "- **Red** — tools that handle untrusted content.\n"
            "- **Blue** — tools that perform critical actions.\n"
            "- **Neither** — tools that do not fall into either class.\n"
            "\n"
            "The source explains that data is treated as private by default rather than receiving a third color.\n"
            "\n"
            "### How to use the framework\n"
            "\n"
            "For each individual tool:\n"
            "\n"
            "1. Label it red, blue, or neither.\n"
            "2. Explain why.\n"
            "3. Ask whether you can redesign the tool to remove the risky property.\n"
            "4. Avoid mixing red and blue capabilities in the same server/agent workflow when practical.\n"
            "\n"
            "The value is the analysis process: it forces you to think explicitly about which tools read adversarial data and which tools can take sensitive actions.\n"
            "\n"
            "---\n"
            "\n"
            "## 17. Sharing local MCP servers\n"
            "\n"
            "A local server can often be distributed simply as source/package code plus clear installation instructions for supported clients.\n"
            "\n"
            "Good distribution documentation should explain:\n"
            "\n"
            "- prerequisites,\n"
            "- installation command,\n"
            "- server launch command,\n"
            "- required environment variables,\n"
            "- expected transport,\n"
            "- client configuration,\n"
            "- permissions/security expectations.\n"
            "\n"
            "### MCP Bundles (MCPB)\n"
            "\n"
            "The source describes an MCP Bundle as a ZIP package containing the server and a `manifest.json`. A compatible client can install the bundle as one distributable artifact.\n"
            "\n"
            "A bundle is useful when you want a simpler user-facing installation experience than manually cloning/configuring a repository.\n"
            "\n"
            "---\n"
            "\n"
            "## 18. Preparing a remote MCP deployment\n"
            "\n"
            "Remote servers need Streamable HTTP.\n"
            "\n"
            "The source also discusses options that improve deployability/scaling:\n"
            "\n"
            "```python\n"
            "mcp.run(\n"
            "    transport='streamable-http',\n"
            "    stateless_http=True,\n"
            "    json_response=True,\n"
            ")\n"
            "```\n"
            "\n"
            "### Stateless behavior\n"
            "\n"
            "Forcing stateless behavior for compatible clients makes horizontal scaling easier because requests do not depend on one sticky long-lived server session.\n"
            "\n"
            "### JSON-only responses\n"
            "\n"
            "A JSON-only response mode can fit infrastructure that buffers complete HTTP responses, such as some serverless platforms, API gateways, and CDNs. "
            "The tradeoff is reduced support for streaming behavior.\n"
            "\n"
            "### Request-size limits\n"
            "\n"
            "Bound request bodies. The chapter notes a configurable maximum request body size, which protects server resources and prevents accidental or abusive oversized payloads.\n"
            "\n"
            "---\n"
            "\n"
            "## 19. Mounting MCP inside an ASGI application\n"
            "\n"
            "For more conventional web deployment, the source shows mounting an MCP server into an ASGI framework such as Starlette.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Uvicorn / ASGI server\n"
            "       ↓\n"
            "Starlette/FastAPI application\n"
            "       ↓\n"
            "Mounted MCP Streamable HTTP app\n"
            "       ↓\n"
            "/mcp endpoint\n"
            "```\n"
            "\n"
            "A lifespan context starts/stops the MCP session manager along with the web application.\n"
            "\n"
            "If multiple MCP servers are hosted in one application, mount them under distinct paths.\n"
            "\n"
            "[[IMAGE_NEEDED: Remote MCP deployment stack | "
            "A layered diagram showing cloud/container → Uvicorn → ASGI app → mounted MCP server → /mcp endpoint, with OAuth/gateway in front | "
            "Learner should notice how MCP can fit into a conventional scalable web-service deployment]]\n"
            "\n"
            "---\n"
            "\n"
            "## 20. Containerizing the server\n"
            "\n"
            "Containers serve two different purposes in the chapter:\n"
            "\n"
            "- **Local use:** sandbox the server away from the host machine.\n"
            "- **Remote use:** package the application consistently for deployment.\n"
            "\n"
            "A minimal deployment image typically:\n"
            "\n"
            "1. chooses a Python base image,\n"
            "2. copies the project,\n"
            "3. installs dependencies,\n"
            "4. exposes the web port for remote servers,\n"
            "5. launches the ASGI/MCP process.\n"
            "\n"
            "### Container security still matters\n"
            "\n"
            "A container is not automatically a perfect sandbox. Continue applying least privilege:\n"
            "\n"
            "- avoid unnecessary mounts,\n"
            "- avoid privileged mode,\n"
            "- restrict network access when possible,\n"
            "- run as a non-root user where practical,\n"
            "- pin dependencies/base images,\n"
            "- scan the image.\n"
            "\n"
            "---\n"
            "\n"
            "## 21. Publishing through the MCP Registry\n"
            "\n"
            "The source describes the MCP Registry as a centralized server-discovery system—conceptually similar to a package index for MCP integrations.\n"
            "\n"
            "For a Python server, the chapter's publishing flow is conceptually:\n"
            "\n"
            "```text\n"
            "Package server\n"
            "    ↓\n"
            "Publish Python package to PyPI\n"
            "    ↓\n"
            "Generate server.json with publisher tooling\n"
            "    ↓\n"
            "Update package metadata and environment-variable declarations\n"
            "    ↓\n"
            "Verify package/server ownership\n"
            "    ↓\n"
            "Authenticate publisher\n"
            "    ↓\n"
            "Publish registry entry\n"
            "    ↓\n"
            "Verify discovery/search result\n"
            "```\n"
            "\n"
            "The exact registry tooling may evolve, but the durable lesson is that public discovery requires:\n"
            "\n"
            "- clear identity,\n"
            "- a versioned package,\n"
            "- connection metadata,\n"
            "- ownership verification,\n"
            "- repeatable releases.\n"
            "\n"
            "{{exercise:M03.L03.EX04}}\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: 'If unit tests pass, my MCP server is production ready.'\n"
            "\n"
            "**Why this is wrong:** unit tests do not measure model tool choice, prompt quality, network integration, security posture, or deployment behavior.\n"
            "\n"
            "### Misconception 2: 'Evaluations replace software tests.'\n"
            "\n"
            "**Why this is wrong:** evaluations measure probabilistic model-facing behavior, while tests validate deterministic software correctness.\n"
            "\n"
            "### Misconception 3: 'Prompt injection can be solved by filtering a list of bad phrases.'\n"
            "\n"
            "**Why this is wrong:** untrusted instructions can take countless forms. Structural isolation and least privilege are essential.\n"
            "\n"
            "### Misconception 4: 'Authentication is enough for multitenant security.'\n"
            "\n"
            "**Why this is wrong:** authenticated users still need object-, role-, and action-level authorization boundaries.\n"
            "\n"
            "### Misconception 5: 'A client token can safely be forwarded to any downstream API.'\n"
            "\n"
            "**Why this is wrong:** tokens are issued for specific audiences/scopes and should not be blindly passed through.\n"
            "\n"
            "### Misconception 6: 'A Docker container completely solves MCP security.'\n"
            "\n"
            "**Why this is wrong:** containers reduce blast radius but still need constrained mounts, privileges, networks, credentials, and dependency hygiene.\n"
            "\n"
            "### Misconception 7: 'The Lethal Trifecta says private data itself is unsafe to use.'\n"
            "\n"
            "**Why this is wrong:** the dangerous condition is combining private-data access, untrusted content, and third-party communication without adequate controls.\n"
            "\n"
            "### Misconception 8: 'Remote deployment is just `mcp.run()` on a public IP.'\n"
            "\n"
            "**Why this is wrong:** remote systems need authorization, request limits, observability, scaling, safe infrastructure, and deployment operations.\n"
            "\n"
            "### Misconception 9: 'Registry publication proves the server is secure.'\n"
            "\n"
            "**Why this is wrong:** discoverability and ownership metadata are not substitutes for code review, testing, isolation, and runtime security controls.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Unit test | Test of one function/class/logic unit in isolation |\n"
            "| Integration test | Test of interactions between the server and another component/system |\n"
            "| End-to-end test | Test of a full operational path through real or realistic components |\n"
            "| MCP Inspector | Interactive MCP client used to manually test and inspect server behavior |\n"
            "| Evaluation | Test of probabilistic model-facing behavior such as prompt quality or tool choice |\n"
            "| Tool-choice accuracy | Fraction of evaluation tasks for which the model selects the expected tool |\n"
            "| LLM-as-a-judge | Using a model to score output against a rubric or quality criteria |\n"
            "| Error analysis | Studying failure patterns to improve prompts, tools, or system design |\n"
            "| Prompt injection | Untrusted instructions influencing model behavior through model-visible content |\n"
            "| Path traversal | Attempt to reach files outside an intended directory boundary through crafted paths |\n"
            "| Least privilege | Granting only the minimum access required for legitimate work |\n"
            "| Token pass-through | Forwarding client authorization tokens to downstream services instead of maintaining proper trust boundaries |\n"
            "| Confused deputy | Privileged system tricked into exercising authority for a less privileged actor |\n"
            "| Sandboxing | Isolating the server from host resources and other systems |\n"
            "| OAuth resource server | Protected server that validates access tokens issued by an authorization server |\n"
            "| RBAC | Role-based access control; permissions based on roles |\n"
            "| MCP gateway | Network intermediary that can route, authenticate, authorize, and enforce policies across MCP servers |\n"
            "| Observability | Logs, traces, metrics, and alerts used to understand system behavior |\n"
            "| Supply-chain security | Protecting dependencies, images, build systems, and third-party components |\n"
            "| Lethal Trifecta | Private data + untrusted content + third-party communication risk combination |\n"
            "| MCP Colors | Tool-risk classification framework using red/untrusted-content and blue/critical-action labels |\n"
            "| MCPB | MCP Bundle; packaged server plus manifest for supported installers |\n"
            "| Stateless HTTP | Request handling that does not rely on persistent per-client server session state |\n"
            "| ASGI | Python asynchronous web application interface used by frameworks such as Starlette and FastAPI |\n"
            "| MCP Registry | Discovery/publishing system for MCP servers described in the source |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is testing depth dependent on risk rather than a universal coverage number?\n"
            "2. What does MCP Inspector test that direct Python function calls do not?\n"
            "3. What is the difference between a unit test and an integration test?\n"
            "4. Why should at least one real or realistic client be used during integration testing?\n"
            "5. What is an evaluation measuring that normal unit tests are not?\n"
            "6. Why should reusable MCP prompts be evaluated across multiple models?\n"
            "7. How is tool-choice accuracy calculated?\n"
            "8. What are the limitations of a simple tool-choice benchmark?\n"
            "9. Why is structural security more reliable than relying only on text filters?\n"
            "10. How do parameterized SQL queries reduce injection risk?\n"
            "11. Why is path normalization required before containment checks?\n"
            "12. Why is authentication insufficient without authorization?\n"
            "13. What problem does rate limiting address?\n"
            "14. Why is token pass-through risky?\n"
            "15. What is the confused-deputy problem?\n"
            "16. What are the three layers in the chapter's security architecture?\n"
            "17. How does OAuth help implement least privilege?\n"
            "18. What does an MCP gateway centralize?\n"
            "19. Why are observability and dependency scanning security controls?\n"
            "20. What are the three parts of the Lethal Trifecta?\n"
            "21. What do red and blue mean in MCP Colors?\n"
            "22. How can containers reduce the blast radius of a local MCP server?\n"
            "23. What is the difference between distributing source code and distributing an MCPB?\n"
            "24. Why can stateless remote servers be easier to scale horizontally?\n"
            "25. Why might JSON-only remote responses be useful for some hosting infrastructure?\n"
            "26. What is the role of an ASGI application around an MCP server?\n"
            "27. What does registry publication add beyond simply hosting a server?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**A production-ready MCP server is not defined by how many tools it exposes. It is defined by whether its code is tested, its model-facing interface is evaluated, "
            "its privileges and attack surface are deliberately constrained, its behavior is observable, and users can install or connect to it through a reliable, documented deployment path.**\n"
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "production-lifecycle", "title": "The production server lifecycle", "order": 1},
            {"id": "testing-strategy", "title": "Choosing a testing strategy", "order": 2},
            {"id": "inspector-workflow", "title": "MCP Inspector development workflow", "order": 3},
            {"id": "automated-testing", "title": "Automated unit and integration testing", "order": 4},
            {"id": "evaluations", "title": "Why MCP servers need evaluations", "order": 5},
            {"id": "evaluation-design", "title": "Designing useful evaluations", "order": 6},
            {"id": "tool-evaluation", "title": "Evaluating tool choice", "order": 7},
            {"id": "security-mindset", "title": "Security mindset", "order": 8},
            {"id": "injection-risks", "title": "Injection and path vulnerabilities", "order": 9},
            {"id": "access-dos-token", "title": "Access control, DoS, and token boundaries", "order": 10},
            {"id": "confused-deputy", "title": "Confused-deputy problem", "order": 11},
            {"id": "security-layers", "title": "Three-layer security architecture", "order": 12},
            {"id": "oauth-rbac-gateways", "title": "OAuth, RBAC, and MCP gateways", "order": 13},
            {"id": "operational-controls", "title": "Observability and supply-chain security", "order": 14},
            {"id": "lethal-trifecta", "title": "The Lethal Trifecta", "order": 15},
            {"id": "mcp-colors", "title": "MCP Colors", "order": 16},
            {"id": "sharing-local", "title": "Sharing local MCP servers", "order": 17},
            {"id": "remote-deployment", "title": "Preparing remote deployments", "order": 18},
            {"id": "asgi-deployment", "title": "ASGI deployment", "order": 19},
            {"id": "containerization", "title": "Containerizing the server", "order": 20},
            {"id": "registry", "title": "Publishing through the MCP Registry", "order": 21},
        ],
    },

    "exercises": [
        {
            "id": "M03.L03.EX01",

            "title": "Build an Inspector-Driven Test Plan",

            "lesson_code": "M03.L03",

            "section_id": "inspector-workflow",

            "placement": "after_section",

            "description": (
                "Create a manual testing plan for a server that exposes a tool, resource, "
                "elicitation flow, and authorization requirement."
            ),

            "instructions": (
                "Your server exposes create_ticket(), project://{id}, a user-confirmation elicitation, "
                "and OAuth-protected remote access.\n\n"
                "Design an MCP Inspector workflow that covers:\n"
                "1. Initial connectivity and capability discovery.\n"
                "2. Happy-path create_ticket() execution.\n"
                "3. Invalid tool arguments.\n"
                "4. Resource discovery and read.\n"
                "5. Elicitation accept, decline, and cancel.\n"
                "6. OAuth/authentication flow.\n"
                "7. Notifications/history inspection.\n"
                "8. One realistic failure case after remote deployment."
            ),

            "expected_output": (
                "A step-by-step Inspector test plan with expected observations for each stage."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "mcp-inspector",
                "manual-testing",
                "integration-testing",
                "debugging",
            ],
        },

        {
            "id": "M03.L03.EX02",

            "title": "Design a Tool-Choice Evaluation Suite",

            "lesson_code": "M03.L03",

            "section_id": "tool-evaluation",

            "placement": "after_section",

            "description": (
                "Create an evaluation dataset that tests whether several models can reliably "
                "choose among related MCP tools."
            ),

            "instructions": (
                "Your server exposes:\n"
                "- github_create_issue\n"
                "- github_comment_issue\n"
                "- github_close_issue\n"
                "- github_search_issues\n\n"
                "1. Write at least eight representative user requests and the expected tool for each.\n"
                "2. Include at least two ambiguous or difficult cases.\n"
                "3. Define tool-choice accuracy.\n"
                "4. Add one structured-output assertion.\n"
                "5. Add one cost metric.\n"
                "6. Explain why you would run the same suite across several model families/sizes.\n"
                "7. Describe how you would use failures to improve tool names or descriptions."
            ),

            "expected_output": (
                "An evaluation table with tasks, expected tools, metrics, model matrix, "
                "and an error-analysis improvement plan."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "evaluations",
                "tool-choice",
                "metrics",
                "error-analysis",
            ],
        },

        {
            "id": "M03.L03.EX03",

            "title": "Threat-Model an MCP Server",

            "lesson_code": "M03.L03",

            "section_id": "security-layers",

            "placement": "after_section",

            "description": (
                "Apply the chapter's vulnerability taxonomy and layered defenses to a realistic MCP server."
            ),

            "instructions": (
                "A remote MCP server can read private project documents, fetch public web pages, "
                "and send messages to external users.\n\n"
                "1. Identify the Lethal Trifecta in this design.\n"
                "2. Identify at least four relevant vulnerability classes from the chapter.\n"
                "3. Propose one Layer 1 infrastructure control.\n"
                "4. Propose two Layer 2 access controls.\n"
                "5. Propose two Layer 3 operational controls.\n"
                "6. Label each exposed tool red, blue, or neither using MCP Colors.\n"
                "7. Redesign the architecture to remove at least one leg of the Lethal Trifecta for risky requests.\n"
                "8. Explain where human approval should be required."
            ),

            "expected_output": (
                "A threat-model table plus a redesigned architecture showing layered mitigations "
                "and how at least one dangerous capability combination is broken."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "security",
                "threat-modeling",
                "least-privilege",
                "lethal-trifecta",
                "mcp-colors",
            ],
        },

        {
            "id": "M03.L03.EX04",

            "title": "Create a Server Release Plan",

            "lesson_code": "M03.L03",

            "section_id": "registry",

            "placement": "after_section",

            "description": (
                "Design the release path for both local users and a scalable remote deployment."
            ),

            "instructions": (
                "You have finished a production-quality Python MCP server.\n\n"
                "Create two release paths:\n\n"
                "A. Local distribution\n"
                "1. Repository/package structure.\n"
                "2. Installation instructions.\n"
                "3. Environment variables and permissions documentation.\n"
                "4. Optional MCPB packaging.\n"
                "5. Containerized sandbox option.\n\n"
                "B. Remote distribution\n"
                "1. Streamable HTTP configuration.\n"
                "2. Authentication/authorization placement.\n"
                "3. ASGI application/mount strategy.\n"
                "4. Container image strategy.\n"
                "5. Horizontal-scaling considerations.\n"
                "6. Request-size limits and observability.\n"
                "7. Package/registry publication and ownership verification."
            ),

            "expected_output": (
                "A two-path release checklist covering local installation and remote production deployment."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "deployment",
                "containerization",
                "asgi",
                "distribution",
                "mcp-registry",
            ],
        },
    ],

    "quiz": {
        "id": "M03.L03.QZ01",

        "title": "Testing, Securing, and Sharing MCP Servers — Knowledge Check",

        "lesson_code": "M03.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L03.Q01",

                "section_id": "testing-strategy",

                "question": "What should primarily determine how extensively an MCP server is tested?",

                "options": [
                    "The number of lines of Python code",
                    "The server's risk, users, data, operations, and deployment context",
                    "Whether the developer enjoys writing tests",
                    "Whether MCP Inspector is installed",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter frames testing depth as a risk decision: sensitive, remote, or "
                    "critical systems justify more extensive testing than low-risk prototypes."
                ),
            },

            {
                "id": "M03.L03.Q02",

                "section_id": "inspector-workflow",

                "question": "What is MCP Inspector especially useful for?",

                "options": [
                    "Training a new language model",
                    "Manually exercising MCP server capabilities and inspecting protocol behavior",
                    "Replacing every automated test",
                    "Publishing packages to PyPI",
                ],

                "correct": 1,

                "explanation": (
                    "Inspector acts as a development MCP client that exposes primitives, requests, "
                    "responses, notifications, and specialized interactions."
                ),
            },

            {
                "id": "M03.L03.Q03",

                "section_id": "evaluations",

                "question": "Why are evaluations useful even when tool functions pass unit tests?",

                "options": [
                    "Because unit tests cannot execute Python",
                    "Because models may still select or use perfectly implemented tools incorrectly",
                    "Because evaluations replace authentication",
                    "Because evaluations guarantee security",
                ],

                "correct": 1,

                "explanation": (
                    "Evaluations measure model-facing behavior such as tool choice and prompt quality, "
                    "which deterministic function tests do not measure."
                ),
            },

            {
                "id": "M03.L03.Q04",

                "section_id": "tool-evaluation",

                "question": "What does tool-choice accuracy measure?",

                "options": [
                    "How quickly the MCP server starts",
                    "The proportion of test tasks where the model selects the expected tool",
                    "The percentage of code lines covered",
                    "The percentage of requests authenticated with OAuth",
                ],

                "correct": 1,

                "explanation": (
                    "A simple tool-choice benchmark compares the selected tool with the expected tool "
                    "for each representative task."
                ),
            },

            {
                "id": "M03.L03.Q05",

                "section_id": "injection-risks",

                "question": "Which is the strongest general defense against path traversal in a file tool?",

                "options": [
                    "Reject every filename containing a dot",
                    "Resolve paths and perform a path-aware containment check against an allowed directory",
                    "Compare raw path strings with startswith() only",
                    "Allow the model to decide whether the path looks safe",
                ],

                "correct": 1,

                "explanation": (
                    "Normalization plus path-aware containment handles traversal and symlink cases "
                    "better than naive string checks."
                ),
            },

            {
                "id": "M03.L03.Q06",

                "section_id": "access-dos-token",

                "question": "Why is blindly passing a client's authorization token to a third-party service risky?",

                "options": [
                    "Tokens can never be used over HTTP",
                    "The token may have the wrong audience/scope and breaks clean trust and audit boundaries",
                    "OAuth tokens cannot contain scopes",
                    "It always prevents the third-party API from responding",
                ],

                "correct": 1,

                "explanation": (
                    "Tokens are issued for specific services and permissions. Pass-through can create "
                    "confused authorization boundaries and enable misuse."
                ),
            },

            {
                "id": "M03.L03.Q07",

                "section_id": "security-layers",

                "question": "Which sequence matches the chapter's three-layer security model?",

                "options": [
                    "Prompts → tools → resources",
                    "Infrastructure foundations → access control → operational controls",
                    "OAuth → Docker → MCPB",
                    "Unit tests → evals → publishing",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter groups controls into infrastructure isolation, access control, "
                    "and operational visibility/governance."
                ),
            },

            {
                "id": "M03.L03.Q08",

                "section_id": "lethal-trifecta",

                "question": "Which combination forms the Lethal Trifecta described in the source?",

                "options": [
                    "Private data + untrusted content + third-party communication",
                    "OAuth + RBAC + sandboxing",
                    "Tools + prompts + resources",
                    "Logs + traces + metrics",
                ],

                "correct": 0,

                "explanation": (
                    "The dangerous combination is access to private data, exposure to untrusted content, "
                    "and a channel to communicate with third parties."
                ),
            },

            {
                "id": "M03.L03.Q09",

                "section_id": "mcp-colors",

                "question": "In the MCP Colors framework, what does a red tool represent?",

                "options": [
                    "A tool that handles untrusted content",
                    "A tool that always fails",
                    "A tool that requires OAuth",
                    "A tool that is deprecated",
                ],

                "correct": 0,

                "explanation": (
                    "Red identifies tools that process untrusted content; blue identifies tools that "
                    "perform critical actions."
                ),
            },

            {
                "id": "M03.L03.Q10",

                "section_id": "remote-deployment",

                "question": "Why can stateless HTTP behavior help scale a remote MCP server horizontally?",

                "options": [
                    "Every request must return an SSE stream forever.",
                    "Requests depend less on persistent server-local session state, so different instances can handle them.",
                    "It disables authentication.",
                    "It prevents multiple clients from connecting.",
                ],

                "correct": 1,

                "explanation": (
                    "Reducing persistent per-client state makes it easier for load balancers to distribute "
                    "requests across several server instances."
                ),
            },

            {
                "id": "M03.L03.Q11",

                "section_id": "registry",

                "question": "What does publishing to an MCP Registry primarily add?",

                "options": [
                    "Automatic proof that the server is vulnerability-free",
                    "A standard discovery and metadata path for clients and users",
                    "A replacement for packaging the server",
                    "A replacement for OAuth",
                ],

                "correct": 1,

                "explanation": (
                    "Registry publication improves discovery, identity, connection metadata, and release "
                    "distribution; it does not replace security review."
                ),
            },

            {
                "id": "M03.L03.Q12",

                "section_id": "production-lifecycle",

                "type": "open",

                "question": (
                    "Design a production-readiness plan for a remote MCP server that can read private "
                    "documents and create external support tickets. Cover software tests, model evaluations, "
                    "the Lethal Trifecta, sandboxing, OAuth/RBAC, gateway/observability controls, containerized "
                    "deployment, and publication/discovery."
                ),
            },
        ],

        "passing_score": 70,
    },
}
