"""M10.L01 — AI Engineering Architecture and User Feedback.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 10, "AI Engineering Architecture and User Feedback".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M10.L01"
MODULE_ORDER = 10
MODULE_TITLE = "AI Engineering Architecture and User Feedback"
MODULE_DESCRIPTION = (
    "Learn how production AI applications grow from a simple model call into "
    "systems with context construction, guardrails, routers, gateways, caches, "
    "agents, observability, orchestration, and feedback loops that continuously "
    "improve product and model quality."
)
SOURCE_CHAPTER = 10
SOURCE_PAGES = "Page range not provided in the supplied chapter text"


TOPIC = {
    "title": "AI Engineering Architecture and User Feedback",
    "slug": "ai-engineering-m10-l01-architecture-user-feedback",
    "description": (
        "A complete learner-facing guide to AI application architecture and "
        "feedback-driven improvement, covering context augmentation, guardrails, "
        "routing, model gateways, exact and semantic caches, agent patterns, "
        "observability, logs/traces/drift, orchestration, explicit and implicit "
        "feedback, conversational signals, feedback design, bias, and feedback loops."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 6.0,
    "skill_tags": [
        "ai-architecture",
        "context-construction",
        "guardrails",
        "model-routing",
        "model-gateway",
        "caching",
        "agents",
        "observability",
        "monitoring",
        "tracing",
        "drift-detection",
        "orchestration",
        "user-feedback",
        "data-flywheel",
        "feedback-bias",
    ],
    "prerequisite_ids": [],

    "lesson": {
        "title": "AI Engineering Architecture and User Feedback",
        "content": (
            "# AI Engineering Architecture and User Feedback\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M10.L01  \n"
            "> **Module:** AI Engineering Architecture and User Feedback  \n"
            "> **Source alignment:** Chapter 10, *AI Engineering Architecture and "
            "User Feedback*. This lesson is an instructor-authored curriculum "
            "adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Build an AI application architecture incrementally instead of starting "
            "with unnecessary complexity.\n"
            "- Explain why context construction is often the first major architectural addition.\n"
            "- Design input and output guardrails around concrete failure modes.\n"
            "- Explain masking/unmasking workflows for sensitive information.\n"
            "- Balance guardrail reliability against latency, cost, and user friction.\n"
            "- Explain when retries, parallel candidate generation, or human fallback can help.\n"
            "- Distinguish model routing from model gateways.\n"
            "- Design intent-based routing and next-action routing.\n"
            "- Explain why routers should usually be small, fast, and cheap.\n"
            "- Explain how a model gateway provides unified access, access control, "
            "cost management, fallbacks, logging, and analytics.\n"
            "- Compare exact and semantic caching.\n"
            "- Explain cache-eviction policies and the risks of caching personalized data.\n"
            "- Explain when semantic caching can return incorrect answers.\n"
            "- Add agent loops and write actions while recognizing the new risks they create.\n"
            "- Explain monitoring, observability, MTTD, MTTR, and CFR.\n"
            "- Design metrics around failure modes instead of tracking metrics for their own sake.\n"
            "- Distinguish metrics, logs, and traces.\n"
            "- Identify prompt, user-behavior, and underlying-model drift.\n"
            "- Explain AI-pipeline orchestration and chaining.\n"
            "- Evaluate orchestration tools by integration, extensibility, control flow, "
            "ease of use, latency, and scalability.\n"
            "- Explain why user feedback is a proprietary data asset and part of a data flywheel.\n"
            "- Distinguish explicit and implicit user feedback.\n"
            "- Identify conversational signals such as early termination, correction, "
            "complaints, sentiment, regeneration, editing, and conversation organization.\n"
            "- Design feedback collection that is useful but nonintrusive.\n"
            "- Explain feedback biases including leniency, randomness, position, "
            "preference, and recency bias.\n"
            "- Explain degenerate feedback loops, exposure bias, and sycophancy risks.\n"
            "- Connect production feedback back into evaluation, development, and personalization.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Start simple, then add components because you need them\n"
            "\n"
            "The simplest AI application is:\n"
            "\n"
            "```text\n"
            "user query -> model -> response\n"
            "```\n"
            "\n"
            "No retrieval. No guardrails. No router. No cache. No agent loop.\n"
            "\n"
            "That simplicity is useful because every extra component introduces new failure "
            "modes, latency, operational work, and debugging difficulty.\n"
            "\n"
            "The chapter therefore builds the architecture gradually:\n"
            "\n"
            "1. Enhance context.\n"
            "2. Add guardrails.\n"
            "3. Add routing and a model gateway.\n"
            "4. Add caches.\n"
            "5. Add agent patterns and write actions.\n"
            "6. Instrument the whole system with observability.\n"
            "7. Orchestrate components into a maintainable pipeline.\n"
            "\n"
            "This order is not a universal recipe. The governing principle is:\n"
            "\n"
            "> Add complexity when it solves a real problem in your application.\n"
            "\n"
            "[[IMAGE_NEEDED: Progressive AI architecture | A left-to-right sequence "
            "starting with user->model and progressively adding context, guardrails, "
            "router/gateway, cache, agent loops, observability, and orchestration | "
            "Learner should notice that each component is introduced to address a "
            "specific production need]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Step 1 — Enhance context\n"
            "\n"
            "A foundation model often fails because it lacks the right information at the "
            "right time.\n"
            "\n"
            "Context construction can provide that information through:\n"
            "\n"
            "- Text retrieval.\n"
            "- Image retrieval.\n"
            "- Tabular/database retrieval.\n"
            "- Uploaded files.\n"
            "- Search APIs.\n"
            "- Weather/news/event APIs.\n"
            "- Other tools that gather information.\n"
            "\n"
            "The chapter compares context construction with feature engineering: both try "
            "to present the model with inputs that make the target task easier.\n"
            "\n"
            "Different model providers and frameworks support different context limits, "
            "document types, retrieval algorithms, chunking options, and tool-execution modes.\n"
            "\n"
            "Do not choose a provider only by model name. Evaluate whether its context "
            "construction capabilities match your application.\n"
            "\n"
            "[[IMAGE_NEEDED: Context-enhanced architecture | User query flowing into "
            "retrieval/tools, retrieved context joining the query, then both entering "
            "the model | Learner should notice that external information is constructed "
            "per query rather than memorized inside every prompt]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Step 2 — Put in guardrails where risks exist\n"
            "\n"
            "Guardrails reduce risk around inputs, outputs, and actions.\n"
            "\n"
            "They should be tied to actual exposures. A system that sends sensitive data "
            "to an external API has different guardrail needs from a fully self-hosted system.\n"
            "\n"
            "The chapter separates two broad classes:\n"
            "\n"
            "- **Input guardrails** — protect the system before the main model call.\n"
            "- **Output guardrails** — detect and handle bad model responses.\n"
            "\n"
            "Guardrails cannot eliminate all failures. They reduce probability and impact.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Input guardrails\n"
            "\n"
            "Two important input-side risks are:\n"
            "\n"
            "1. Sensitive information leaving your trust boundary.\n"
            "2. Malicious or unsafe prompts compromising system behavior.\n"
            "\n"
            "Sensitive information can enter a prompt because:\n"
            "\n"
            "- A user pastes private data.\n"
            "- An employee pastes internal secrets.\n"
            "- A system prompt contains confidential information.\n"
            "- A tool retrieves protected data and adds it to context.\n"
            "\n"
            "Common detection targets include:\n"
            "\n"
            "- Identity numbers.\n"
            "- Phone numbers.\n"
            "- Bank-account details.\n"
            "- Human faces.\n"
            "- Internal IP keywords or privileged phrases.\n"
            "\n"
            "Once detected, the application can block the request or redact/mask the sensitive value.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Masking and unmasking private information\n"
            "\n"
            "A useful pattern is to replace private values before sending data to an external model.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Original:\n"
            "Call me at 01012345678.\n"
            "\n"
            "Masked:\n"
            "Call me at [PHONE_NUMBER].\n"
            "```\n"
            "\n"
            "The application stores a private reverse map:\n"
            "\n"
            "```text\n"
            "[PHONE_NUMBER] -> 01012345678\n"
            "```\n"
            "\n"
            "If the model returns the placeholder, the application can restore the original "
            "value after the external model step.\n"
            "\n"
            "The reverse map itself is sensitive and must stay inside the trusted system.\n"
            "\n"
            "[[IMAGE_NEEDED: PII masking workflow | Input containing private data -> "
            "sensitive-data detector -> placeholder substitution -> external model -> "
            "placeholder response -> trusted reverse map -> final restored response | "
            "Learner should notice which parts must remain inside the trust boundary]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Output guardrails\n"
            "\n"
            "Output guardrails have two jobs:\n"
            "\n"
            "1. Detect output failures.\n"
            "2. Define what the application should do when a failure is detected.\n"
            "\n"
            "### Quality failures\n"
            "\n"
            "- Empty response when one is expected.\n"
            "- Invalid JSON or another malformed structure.\n"
            "- Hallucinated or factually inconsistent claims.\n"
            "- Irrelevant or generally poor output.\n"
            "\n"
            "### Security failures\n"
            "\n"
            "- Toxic or unsafe content.\n"
            "- Leakage of sensitive information.\n"
            "- Output that triggers unsafe remote execution.\n"
            "- Brand-risk behavior.\n"
            "\n"
            "Security evaluation should also track **false refusals**. A system that blocks "
            "everything may be 'safe' but unusable.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Retries, parallel candidates, and human fallback\n"
            "\n"
            "Foundation models are probabilistic. A failed response does not always repeat "
            "on the next call.\n"
            "\n"
            "For some failures, simple retry logic is useful:\n"
            "\n"
            "- Empty output -> retry.\n"
            "- Invalid structure -> retry or repair.\n"
            "- Temporary provider failure -> retry/fallback.\n"
            "\n"
            "But retries increase cost and latency.\n"
            "\n"
            "One alternative is to generate multiple candidates in parallel and select a valid "
            "or better response. This controls latency but increases redundant computation.\n"
            "\n"
            "For difficult or risky cases, the strongest fallback may be a human operator.\n"
            "\n"
            "Human escalation triggers can include:\n"
            "\n"
            "- Certain high-risk intents.\n"
            "- User frustration/anger.\n"
            "- Too many unsuccessful conversation turns.\n"
            "- Low confidence.\n"
            "- Repeated guardrail failures.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Guardrails have latency and UX costs\n"
            "\n"
            "Every extra detector or scorer may add another model call, classifier call, "
            "or validation pass.\n"
            "\n"
            "This creates a tradeoff:\n"
            "\n"
            "```text\n"
            "more checking -> potentially higher reliability\n"
            "more checking -> higher latency/cost\n"
            "```\n"
            "\n"
            "Streaming creates another challenge. Once tokens have already been shown to the "
            "user, a later output guardrail cannot prevent those earlier tokens from being seen.\n"
            "\n"
            "The correct guardrail design depends on risk, latency requirements, model provider, "
            "and whether you self-host.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Step 3 — Add a router\n"
            "\n"
            "Using one expensive general model for every query is often unnecessary.\n"
            "\n"
            "A **router** decides which solution should handle a request.\n"
            "\n"
            "A common router is an **intent classifier**.\n"
            "\n"
            "Example support routes:\n"
            "\n"
            "```text\n"
            "password reset -> FAQ / retrieval\n"
            "billing dispute -> human operator\n"
            "technical issue -> technical assistant\n"
            "out-of-scope request -> stock refusal/redirect\n"
            "```\n"
            "\n"
            "Routing can improve:\n"
            "\n"
            "- Quality through specialization.\n"
            "- Cost by using smaller/cheaper models for easy requests.\n"
            "- Safety by intercepting unsupported requests.\n"
            "- UX by asking clarification for ambiguous queries.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Routing is broader than intent classification\n"
            "\n"
            "Routers can decide what happens next inside a complex system.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Search API or code interpreter?\n"
            "- Use short-term memory or long-term memory?\n"
            "- Use retrieval or answer directly?\n"
            "- Stay with the current model or switch to one with a larger context window?\n"
            "\n"
            "Routing can happen before retrieval, after retrieval, or between agent steps.\n"
            "\n"
            "Because routers may be called frequently, they should generally be small, fast, "
            "and cheap relative to the main generation model.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Model gateway: one controlled interface to many models\n"
            "\n"
            "A **model gateway** is an intermediate layer between applications and model providers.\n"
            "\n"
            "Its most basic purpose is abstraction:\n"
            "\n"
            "```text\n"
            "application\n"
            "   -> model gateway\n"
            "        -> provider A\n"
            "        -> provider B\n"
            "        -> self-hosted model\n"
            "```\n"
            "\n"
            "Instead of every application implementing every provider API separately, applications "
            "depend on one internal interface.\n"
            "\n"
            "That makes provider changes easier to absorb and centralizes operational controls.\n"
            "\n"
            "[[IMAGE_NEEDED: Model gateway | Multiple applications connecting to one gateway "
            "which fans out to several commercial and self-hosted model endpoints | Learner "
            "should notice that model access and policies are centralized]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. A minimal gateway mental model\n"
            "\n"
            "A simplified implementation might normalize a request, pick a provider adapter, "
            "call it, and normalize the response.\n"
            "\n"
            "```python\n"
            "def call_model(provider, model, prompt, max_tokens):\n"
            "    if provider == 'provider_a':\n"
            "        raw = provider_a_generate(model, prompt, max_tokens)\n"
            "    elif provider == 'provider_b':\n"
            "        raw = provider_b_generate(model, prompt, max_tokens)\n"
            "    else:\n"
            "        raise ValueError('Unsupported provider')\n"
            "\n"
            "    return normalize_response(raw)\n"
            "```\n"
            "\n"
            "Real gateways need substantially more:\n"
            "\n"
            "- Authentication.\n"
            "- Error handling.\n"
            "- Timeouts.\n"
            "- Retry/fallback policies.\n"
            "- Rate limits.\n"
            "- Logging.\n"
            "- Cost controls.\n"
            "- Model-specific parameter translation.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. What belongs in a model gateway\n"
            "\n"
            "A gateway is a natural centralized point for:\n"
            "\n"
            "- Access control.\n"
            "- API-key protection.\n"
            "- Usage quotas.\n"
            "- Cost monitoring.\n"
            "- Rate-limit handling.\n"
            "- Provider fallback.\n"
            "- Load balancing.\n"
            "- Logging and analytics.\n"
            "- Optional caching.\n"
            "- Optional guardrails.\n"
            "\n"
            "The gateway reduces duplicated logic across applications.\n"
            "\n"
            "But avoid turning it into an unmaintainable 'everything service.' Keep clear boundaries "
            "around what your organization wants centralized.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Step 4 — Exact caching\n"
            "\n"
            "Caching avoids repeating expensive work.\n"
            "\n"
            "**Exact caching** reuses a result only when the cache key matches exactly.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Same product summary request.\n"
            "- Same embedding query.\n"
            "- Same deterministic multi-step computation.\n"
            "\n"
            "Possible storage layers include in-memory caches, Redis-like stores, databases, "
            "or tiered storage.\n"
            "\n"
            "A cache also needs an **eviction policy** such as:\n"
            "\n"
            "- LRU — least recently used.\n"
            "- LFU — least frequently used.\n"
            "- FIFO — first in, first out.\n"
            "\n"
            "Caching makes most sense for requests likely to recur and remain valid.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Cache safety: personalization can leak data\n"
            "\n"
            "A cache entry may look generic while its response actually depends on private user context.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "User A asks: What is the return policy?\n"
            "System retrieves A's membership tier.\n"
            "Response contains A-specific policy.\n"
            "Response is cached as if it were generic.\n"
            "\n"
            "User B asks the same wording.\n"
            "System returns A's cached answer.\n"
            "```\n"
            "\n"
            "This is a data leak.\n"
            "\n"
            "Cache keys must include all information that materially changes the answer, or the response "
            "should not be shared across users.\n"
            "\n"
            "Time-sensitive and highly user-specific queries may be poor caching candidates.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Semantic caching\n"
            "\n"
            "Semantic caching reuses results for **similar**, not identical, requests.\n"
            "\n"
            "Typical flow:\n"
            "\n"
            "```text\n"
            "incoming query\n"
            " -> query embedding\n"
            " -> vector search over cached-query embeddings\n"
            " -> highest similarity score\n"
            " -> if score >= threshold: return cached result\n"
            " -> otherwise: compute result and cache it\n"
            "```\n"
            "\n"
            "This increases possible cache hits, but it also creates a new failure mode: two queries "
            "can be semantically close while requiring different answers.\n"
            "\n"
            "Semantic caching depends on:\n"
            "\n"
            "- Embedding quality.\n"
            "- Vector-search quality.\n"
            "- Similarity metric.\n"
            "- Threshold calibration.\n"
            "- Cache size and query latency.\n"
            "\n"
            "Evaluate whether the savings justify the complexity and correctness risk.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic-cache lookup | Query -> embedding -> vector search over "
            "cached queries -> similarity threshold -> cache hit or normal model pipeline | "
            "Learner should notice that an incorrect similarity decision can return an incorrect answer]]\n"
            "\n"
            "{{exercise:M10.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Step 5 — Add agent patterns when the workflow needs loops or branches\n"
            "\n"
            "The earlier architecture is mostly sequential. Agentic systems can add:\n"
            "\n"
            "- Loops.\n"
            "- Conditional branches.\n"
            "- Parallel actions.\n"
            "- Repeated retrieval.\n"
            "- Tool calls.\n"
            "- Write actions.\n"
            "\n"
            "For example, after generating an answer, the system may decide that evidence is insufficient, "
            "retrieve more context, and generate again.\n"
            "\n"
            "This makes the system more capable but also harder to reason about and debug.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Write actions multiply capability and risk\n"
            "\n"
            "An agent can move beyond reading data and start changing the world:\n"
            "\n"
            "- Send email.\n"
            "- Place an order.\n"
            "- Update a record.\n"
            "- Initialize a transfer.\n"
            "- Modify files.\n"
            "\n"
            "Write tools make the system much more useful, but mistakes are no longer only bad text—they "
            "can become real side effects.\n"
            "\n"
            "High-impact actions therefore need stronger controls such as permissions, validation, confirmation, "
            "logging, and human approval.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Observability should be designed in, not added later\n"
            "\n"
            "As architecture complexity grows, the number of possible failure points grows too.\n"
            "\n"
            "Monitoring helps detect risks and opportunities. Observability goes further: the system should "
            "be instrumented so that when something goes wrong, you can determine **where and why** without "
            "shipping new debugging code first.\n"
            "\n"
            "Three useful operational measures are:\n"
            "\n"
            "- **MTTD** — mean time to detection.\n"
            "- **MTTR** — mean time to response/resolution.\n"
            "- **CFR** — change failure rate.\n"
            "\n"
            "Evaluation and monitoring should reinforce each other. Production failures should become future "
            "evaluation cases; evaluation metrics should predict production behavior as well as possible.\n"
            "\n"
            "[[IMAGE_NEEDED: Evaluation-monitoring feedback loop | Offline evaluation -> deployment -> "
            "monitoring/observability -> production failures -> new evaluation cases -> next release | "
            "Learner should notice that evaluation and production monitoring form one learning loop]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Design metrics around failure modes\n"
            "\n"
            "Metrics are tools, not goals.\n"
            "\n"
            "Start with failures you care about, then choose measurements that reveal those failures.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Hallucination risk -> groundedness/factual-consistency metric.\n"
            "- Invalid JSON -> format-failure rate.\n"
            "- Safety risk -> toxicity, PII leakage, refusal/false-refusal rates.\n"
            "- Cost risk -> tokens/request, queries/user, cache hit rate, provider spend.\n"
            "- Latency risk -> TTFT, TPOT, total latency.\n"
            "- Retrieval risk -> context relevance/precision.\n"
            "\n"
            "Metrics should also be related to business north-star metrics when possible.\n"
            "\n"
            "A metric that improves but has no relation to product success may not deserve heavy optimization effort.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Conversation behavior itself is a production metric\n"
            "\n"
            "User behavior can reveal quality problems even without explicit ratings.\n"
            "\n"
            "Useful signals include:\n"
            "\n"
            "- Users stopping generation early.\n"
            "- Number of turns per conversation.\n"
            "- Input-token length trends.\n"
            "- Output-token length trends.\n"
            "- Output-token distribution changes.\n"
            "- Refusal frequency.\n"
            "- Guardrail-trigger frequency.\n"
            "\n"
            "Length metrics matter for quality, latency, and cost simultaneously.\n"
            "\n"
            "Always break aggregate metrics down by meaningful dimensions such as:\n"
            "\n"
            "- User segment.\n"
            "- Release/version.\n"
            "- Prompt/chain version.\n"
            "- Task type.\n"
            "- Time.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Spot checks versus exhaustive monitoring\n"
            "\n"
            "Some metrics are cheap enough to run on every request. Others are expensive.\n"
            "\n"
            "Use:\n"
            "\n"
            "- **Exhaustive checks** for cheap, important validations.\n"
            "- **Spot checks** for expensive judges or human review.\n"
            "\n"
            "A mixed strategy lets you monitor broadly without spending the full cost of heavyweight evaluation "
            "on every request.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Logs explain individual events\n"
            "\n"
            "Metrics aggregate. Logs preserve event detail.\n"
            "\n"
            "A common debugging pattern is:\n"
            "\n"
            "1. Metric alert says something is wrong.\n"
            "2. Inspect logs around the relevant time/request.\n"
            "3. Find the failing event or configuration.\n"
            "4. Correlate it back to the metric change.\n"
            "\n"
            "Useful AI-application logs include:\n"
            "\n"
            "- Model/provider/version.\n"
            "- Sampling configuration.\n"
            "- Prompt template/version.\n"
            "- User query.\n"
            "- Final model prompt.\n"
            "- Model output.\n"
            "- Intermediate outputs.\n"
            "- Tool calls and tool results.\n"
            "- Component start/end/crash events.\n"
            "- Request IDs and tags linking related events.\n"
            "\n"
            "Logs grow quickly, so automated analysis becomes important.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Traces reconstruct the complete request path\n"
            "\n"
            "A trace connects related logs into a timeline for one request or workflow.\n"
            "\n"
            "A useful AI trace might show:\n"
            "\n"
            "```text\n"
            "raw query\n"
            " -> router decision\n"
            " -> retrieval query\n"
            " -> retrieved documents\n"
            " -> final prompt\n"
            " -> model generation\n"
            " -> tool call\n"
            " -> guardrail score\n"
            " -> final response\n"
            "```\n"
            "\n"
            "Each step should ideally include latency, errors, and cost where measurable.\n"
            "\n"
            "If a request fails, tracing should help pinpoint whether the error came from routing, retrieval, "
            "prompt construction, model generation, tools, or post-processing.\n"
            "\n"
            "[[IMAGE_NEEDED: AI request trace | A horizontal timeline showing router, retrieval, model, "
            "tool, guardrail, and final response spans with latency/cost annotations | Learner should notice "
            "how one trace connects component-level failures to the user-visible result]]\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Drift detection\n"
            "\n"
            "A production AI system can change even if you do not deliberately change the application code.\n"
            "\n"
            "The chapter highlights three forms.\n"
            "\n"
            "### System-prompt drift\n"
            "\n"
            "A template, typo fix, or shared configuration changes the prompt.\n"
            "\n"
            "### User-behavior drift\n"
            "\n"
            "Users learn how to interact with the system and change their prompts, lengths, wording, or workflows.\n"
            "\n"
            "### Underlying-model drift\n"
            "\n"
            "A provider may change the actual model behind a stable API name.\n"
            "\n"
            "Version everything you control and monitor behavior for changes you do not control.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. AI pipeline orchestration\n"
            "\n"
            "An AI application may include models, retrievers, databases, tools, scorers, guardrails, and humans.\n"
            "\n"
            "An **orchestrator** defines how these components work together.\n"
            "\n"
            "At a high level it does two things:\n"
            "\n"
            "### Component definition\n"
            "\n"
            "Tell the system what models, data sources, tools, evaluators, and other components exist.\n"
            "\n"
            "### Chaining\n"
            "\n"
            "Define how output from one component becomes input to the next.\n"
            "\n"
            "A pipeline can include sequential steps, branches, loops, parallel work, retries, and human escalation.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Example orchestrated pipeline\n"
            "\n"
            "A simple RAG support workflow could be:\n"
            "\n"
            "```text\n"
            "raw user query\n"
            " -> preprocess query\n"
            " -> retrieve relevant data\n"
            " -> construct model prompt\n"
            " -> generate response\n"
            " -> evaluate response\n"
            " -> if good: return\n"
            " -> if bad/high-risk: human fallback\n"
            "```\n"
            "\n"
            "The orchestrator should also detect data-contract failures. If one component returns data in a "
            "shape the next component cannot consume, that failure should be visible and actionable.\n"
            "\n"
            "For strict-latency applications, run independent steps in parallel when possible.\n"
            "\n"
            "{{exercise:M10.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 28. When and how to choose an orchestrator\n"
            "\n"
            "An orchestration framework can save engineering work, but it also introduces an abstraction layer.\n"
            "\n"
            "Starting without one can help a team understand the actual system before hiding it behind a framework.\n"
            "\n"
            "When evaluating orchestrators, examine:\n"
            "\n"
            "### Integration and extensibility\n"
            "\n"
            "- Does it support your models, databases, and tools?\n"
            "- How hard is it to add unsupported components?\n"
            "\n"
            "### Complex pipeline support\n"
            "\n"
            "- Branching.\n"
            "- Parallel execution.\n"
            "- Loops.\n"
            "- Error handling.\n"
            "- Human-in-the-loop workflows.\n"
            "\n"
            "### Ease of use, performance, and scalability\n"
            "\n"
            "- Clear APIs/documentation.\n"
            "- No hidden expensive calls.\n"
            "- Minimal unnecessary latency.\n"
            "- Ability to scale with traffic and team size.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. User feedback is product data\n"
            "\n"
            "User feedback helps with three major goals:\n"
            "\n"
            "1. **Evaluation** — understand how the product performs.\n"
            "2. **Development** — improve prompts, systems, datasets, and future models.\n"
            "3. **Personalization** — adapt the application to an individual user.\n"
            "\n"
            "Feedback can become proprietary data and create a data flywheel:\n"
            "\n"
            "```text\n"
            "better product\n"
            " -> more usage\n"
            " -> more feedback/data\n"
            " -> better evaluation/training\n"
            " -> better product\n"
            "```\n"
            "\n"
            "But feedback is still user data. Privacy, consent, and transparency apply.\n"
            "\n"
            "[[IMAGE_NEEDED: AI product data flywheel | Product -> users -> interaction/feedback data -> "
            "evaluation/training/personalization -> improved product | Learner should notice that product "
            "usage can become a model-improvement advantage only when feedback is responsibly captured]]\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Explicit versus implicit feedback\n"
            "\n"
            "### Explicit feedback\n"
            "\n"
            "Users intentionally answer a feedback request:\n"
            "\n"
            "- Thumbs up/down.\n"
            "- Star rating.\n"
            "- Better/worse comparison.\n"
            "- 'Did we solve your problem?'\n"
            "\n"
            "This is easier to interpret but can be sparse and biased toward users motivated enough to respond.\n"
            "\n"
            "### Implicit feedback\n"
            "\n"
            "Infer user satisfaction/preferences from behavior:\n"
            "\n"
            "- Regenerate.\n"
            "- Edit.\n"
            "- Stop generation.\n"
            "- Rephrase.\n"
            "- Share/bookmark/delete.\n"
            "- Accept or ignore a suggestion.\n"
            "\n"
            "Implicit feedback is abundant but much noisier.\n"
            "\n"
            "One action rarely proves one interpretation. Context matters.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Conversational signal: early termination\n"
            "\n"
            "If a user stops a response halfway, exits, tells a voice agent to stop, or abandons an agent before "
            "choosing an option, the interaction may be going poorly.\n"
            "\n"
            "This is not perfect evidence. The user may simply be interrupted. But at scale it can be a useful signal, "
            "especially when combined with other evidence such as rephrasing or negative sentiment.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Conversational signal: correction and rephrasing\n"
            "\n"
            "Follow-ups such as:\n"
            "\n"
            "- 'No, ...'\n"
            "- 'I meant ...'\n"
            "- 'Check again.'\n"
            "- 'Are you sure?'\n"
            "- 'Show me the sources.'\n"
            "\n"
            "can indicate misunderstanding, insufficient detail, distrust, or factual concern.\n"
            "\n"
            "Rephrasing attempts are especially useful because they show how the user's original intent differs "
            "from what the system apparently understood.\n"
            "\n"
            "For agentic systems, users may also correct the action plan: 'Check the company's repository too.'\n"
            "\n"
            "---\n"
            "\n"

            "## 33. User edits can become strong preference data\n"
            "\n"
            "If users directly edit generated code, text, or structured output, the edit provides a strong signal.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "query\n"
            "generated response -> losing response\n"
            "user-edited version -> preferred/winning response\n"
            "```\n"
            "\n"
            "This can create preference data for future model alignment, subject to privacy/consent and quality checks.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Complaints and sentiment\n"
            "\n"
            "Users may explicitly complain that an answer is:\n"
            "\n"
            "- Wrong.\n"
            "- Irrelevant.\n"
            "- Not grounded in evidence.\n"
            "- Incomplete.\n"
            "- Too vague.\n"
            "- Too verbose.\n"
            "- Repetitive.\n"
            "- Rude.\n"
            "\n"
            "Even vague emotional signals—frustration, disappointment, ridicule—can help reveal poor interactions.\n"
            "\n"
            "Sentiment is application-specific and should not be overinterpreted. A user can begin angry and end satisfied, "
            "which may indicate that the system successfully resolved the problem.\n"
            "\n"
            "Model refusal rate can also be useful: frequent 'I can't help' responses may signal over-restriction or "
            "poor task coverage.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Regeneration is useful but ambiguous\n"
            "\n"
            "A user requesting another answer may be dissatisfied—or may simply want options.\n"
            "\n"
            "The signal becomes more meaningful when combined with context:\n"
            "\n"
            "- Did the user regenerate repeatedly?\n"
            "- Did they choose one of the responses afterward?\n"
            "- Did they complain before regenerating?\n"
            "- Does regeneration cost them money/credits?\n"
            "\n"
            "If the product asks which regenerated response is better, the comparison can become preference data.\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Conversation organization and length\n"
            "\n"
            "Actions such as delete, rename, share, and bookmark can also be signals.\n"
            "\n"
            "Interpretation depends on context:\n"
            "\n"
            "- Delete may mean bad conversation—or sensitive/embarrassing content.\n"
            "- Rename may mean the conversation is valuable but the automatic title is poor.\n"
            "- Share may mean extremely useful—or hilariously wrong.\n"
            "\n"
            "Conversation length is similarly ambiguous.\n"
            "\n"
            "- Long companionship chat -> potentially positive engagement.\n"
            "- Long customer-support chat -> potentially inefficient problem solving.\n"
            "\n"
            "Combine length with **dialogue diversity**. A long conversation with repetitive content may indicate a loop.\n"
            "\n"
            "---\n"
            "\n"

            "## 37. Feedback design: collect it without breaking the workflow\n"
            "\n"
            "Good feedback collection should be:\n"
            "\n"
            "- Easy.\n"
            "- Nonintrusive.\n"
            "- Optional when possible.\n"
            "- Closely integrated with the user's task.\n"
            "- Clear about what the signal means.\n"
            "\n"
            "Feedback should be available throughout the journey rather than only in a final survey.\n"
            "\n"
            "---\n"
            "\n"

            "## 38. When to collect feedback\n"
            "\n"
            "### At the beginning\n"
            "\n"
            "Use initial calibration when the application genuinely needs it, such as language level, voice profile, "
            "or personal preferences. Otherwise, optional calibration reduces onboarding friction.\n"
            "\n"
            "### When something goes wrong\n"
            "\n"
            "Let users report hallucinations, bad refusals, slow responses, or incorrect outputs. Better still, let "
            "them correct the result so they can finish their task.\n"
            "\n"
            "### When the model is uncertain\n"
            "\n"
            "Ask a targeted clarification or offer choices when uncertainty matters.\n"
            "\n"
            "### When something is exceptionally good\n"
            "\n"
            "Positive feedback can identify high-value features, but constant prompts for praise can clutter the UX. "
            "Sampling feedback requests can reduce interruption.\n"
            "\n"
            "---\n"
            "\n"

            "## 39. The best feedback often comes from normal product actions\n"
            "\n"
            "Users should not always need to fill out a form.\n"
            "\n"
            "Examples of workflow-integrated signals:\n"
            "\n"
            "- Pick one generated image to upscale.\n"
            "- Ask for variations.\n"
            "- Regenerate everything.\n"
            "- Accept a code suggestion.\n"
            "- Ignore the suggestion and keep typing.\n"
            "- Edit AI-generated text before sending it.\n"
            "\n"
            "Integrated products can observe what happens after generation. A standalone chatbot often cannot tell "
            "whether generated content was actually used.\n"
            "\n"
            "[[IMAGE_NEEDED: Workflow-integrated feedback | A generated suggestion with actions accept, edit, "
            "regenerate, ignore, and share, each producing different feedback strengths | Learner should notice "
            "that useful feedback can be collected as a natural side effect of accomplishing the task]]\n"
            "\n"
            "---\n"
            "\n"

            "## 40. Feedback without context is often insufficient\n"
            "\n"
            "A thumbs-down tells you the user disliked something. It may not tell you why.\n"
            "\n"
            "Useful diagnosis may require surrounding conversation turns, the prompt, retrieved context, model version, "
            "and tool trace.\n"
            "\n"
            "But this context can contain personal data. Collection must follow user consent and privacy requirements.\n"
            "\n"
            "Be transparent about whether feedback is used for:\n"
            "\n"
            "- Personalization.\n"
            "- Analytics.\n"
            "- Product improvement.\n"
            "- Training future models.\n"
            "\n"
            "Never promise that data is not used for training or does not leave the device unless that is actually true.\n"
            "\n"
            "---\n"
            "\n"

            "## 41. Do not ask users for feedback they cannot reliably give\n"
            "\n"
            "A user may not know which of two mathematical answers is correct. Asking them to choose anyway creates noise.\n"
            "\n"
            "Good feedback interfaces:\n"
            "\n"
            "- Let users say 'I don't know' where appropriate.\n"
            "- Explain choices with labels/tooltips.\n"
            "- Avoid confusing icon placement.\n"
            "- Avoid forcing unnecessary extra work after a negative rating.\n"
            "\n"
            "The feedback UI is part of the data pipeline. Poor UI produces poor labels.\n"
            "\n"
            "---\n"
            "\n"

            "## 42. Public versus private feedback changes behavior\n"
            "\n"
            "Users may behave differently when feedback is visible to others.\n"
            "\n"
            "Private feedback can encourage candor because users feel less judged.\n"
            "\n"
            "Public feedback can improve discoverability and social explanation but can also distort behavior.\n"
            "\n"
            "Therefore, signal visibility is not only a UI decision; it can change the distribution and reliability "
            "of the feedback data itself.\n"
            "\n"
            "---\n"
            "\n"

            "## 43. Feedback is biased data\n"
            "\n"
            "Feedback should never be treated as objective truth automatically.\n"
            "\n"
            "The chapter describes several biases.\n"
            "\n"
            "### Leniency bias\n"
            "\n"
            "People may give overly positive ratings because that is socially easier or requires less follow-up effort.\n"
            "\n"
            "### Randomness\n"
            "\n"
            "Users may click a response without carefully reading all choices.\n"
            "\n"
            "### Position bias\n"
            "\n"
            "The first option may get more clicks simply because it appears first.\n"
            "\n"
            "### Preference/length bias\n"
            "\n"
            "Users may prefer a longer response because length is easier to notice than factual quality.\n"
            "\n"
            "### Recency bias\n"
            "\n"
            "Users may favor the most recently seen answer.\n"
            "\n"
            "Measure feedback distributions and run experiments to understand these effects in your own product.\n"
            "\n"
            "[[IMAGE_NEEDED: Feedback bias map | A central 'user feedback' node connected to leniency, "
            "randomness, position, length/preference, and recency bias | Learner should notice that raw feedback "
            "needs interpretation before it becomes training or product truth]]\n"
            "\n"
            "---\n"
            "\n"

            "## 44. Degenerate feedback loops\n"
            "\n"
            "You receive feedback only on what the system chooses to show.\n"
            "\n"
            "That creates a dangerous loop:\n"
            "\n"
            "```text\n"
            "model ranks A slightly above B\n"
            " -> A gets more exposure\n"
            " -> A gets more clicks\n"
            " -> system interprets clicks as proof A is better\n"
            " -> A gets even more exposure\n"
            "```\n"
            "\n"
            "Small initial differences can become amplified. Related effects include exposure bias, popularity bias, "
            "and filter bubbles.\n"
            "\n"
            "The same dynamic can shift an application's entire identity: if a small group rewards one content type, "
            "the system may generate more of it, attracting more users who like it, reinforcing the cycle.\n"
            "\n"
            "[[IMAGE_NEEDED: Degenerate feedback loop | Ranking -> exposure -> user feedback -> model update -> "
            "stronger ranking, shown as an amplifying cycle | Learner should notice that model outputs influence the "
            "data that later trains the model]]\n"
            "\n"
            "---\n"
            "\n"

            "## 45. User preference is not always the same as truth or benefit\n"
            "\n"
            "Training indiscriminately on user approval can teach a model to produce what it believes users want "
            "instead of what is accurate or beneficial.\n"
            "\n"
            "A model may become **sycophantic**—agreeing with a user's view to gain positive feedback.\n"
            "\n"
            "Therefore, user feedback should be combined with other signals:\n"
            "\n"
            "- Factual evaluation.\n"
            "- Safety requirements.\n"
            "- Expert review.\n"
            "- Product goals.\n"
            "- Diverse user sampling.\n"
            "- Counterfactual/exploration data where appropriate.\n"
            "\n"
            "Feedback is valuable input, not an unquestionable objective function.\n"
            "\n"
            "{{exercise:M10.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A production AI application should start with the most complete architecture possible.\n"
            "\n"
            "**Why this is wrong:** unnecessary components add latency, cost, operational complexity, and failure modes.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Guardrails can eliminate AI risk.\n"
            "\n"
            "**Why this is wrong:** they mitigate risk but cannot guarantee perfect behavior.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> More guardrails are always better.\n"
            "\n"
            "**Why this is wrong:** extra checks can increase false refusals, latency, cost, and user frustration.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A router and a gateway are the same thing.\n"
            "\n"
            "**Why this is wrong:** a router decides where a request should go; a gateway provides a unified controlled "
            "interface to model endpoints and policies.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> If two queries are semantically similar, their answers are interchangeable.\n"
            "\n"
            "**Why this is wrong:** small semantic differences, user context, or time can require different answers.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Monitoring means collecting as many metrics as possible.\n"
            "\n"
            "**Why this is wrong:** metrics should be chosen to detect failures and opportunities that matter.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Metrics, logs, and traces are redundant.\n"
            "\n"
            "**Why this is wrong:** metrics aggregate, logs preserve events, and traces reconstruct end-to-end execution paths.\n"
            "\n"
            "### Misconception 8\n"
            "\n"
            "> A thumbs-up is clean ground-truth training data.\n"
            "\n"
            "**Why this is wrong:** feedback can be biased, random, ambiguous, or caused by UI position rather than quality.\n"
            "\n"
            "### Misconception 9\n"
            "\n"
            "> Longer conversations always mean better engagement.\n"
            "\n"
            "**Why this is wrong:** in productivity applications, long conversations may mean the system is failing to resolve the task.\n"
            "\n"
            "### Misconception 10\n"
            "\n"
            "> Optimizing only for what users approve will necessarily improve truthfulness.\n"
            "\n"
            "**Why this is wrong:** approval-driven learning can amplify bias or sycophancy.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Context construction | Supplying query-specific external information/tools to the model. |\n"
            "| Input guardrail | Check or transformation applied before the main model/tool step. |\n"
            "| Output guardrail | Check and response policy applied to generated output. |\n"
            "| False refusal | Legitimate request blocked by an overly restrictive system. |\n"
            "| Router | Component deciding which model/solution/action should handle a request. |\n"
            "| Intent classifier | Model/classifier predicting the user's task or intent for routing. |\n"
            "| Model gateway | Unified controlled interface to multiple model providers/endpoints. |\n"
            "| Exact cache | Cache reused only on exact matching keys. |\n"
            "| Semantic cache | Cache reused for sufficiently similar queries based on embeddings/similarity. |\n"
            "| LRU | Least Recently Used cache-eviction policy. |\n"
            "| LFU | Least Frequently Used cache-eviction policy. |\n"
            "| Observability | Instrumenting a system so failures can be diagnosed from collected runtime information. |\n"
            "| MTTD | Mean time to detection. |\n"
            "| MTTR | Mean time to response/resolution. |\n"
            "| CFR | Change failure rate. |\n"
            "| Log | Append-only record of an event. |\n"
            "| Trace | Linked timeline of related events across one request/workflow. |\n"
            "| Drift | Change in prompts, users, models, data, or system behavior over time. |\n"
            "| Orchestrator | Layer coordinating components and data flow across an AI pipeline. |\n"
            "| Chaining | Composing components so output from one feeds another. |\n"
            "| Explicit feedback | Feedback intentionally provided in response to a request for feedback. |\n"
            "| Implicit feedback | Feedback inferred from normal user behavior/actions. |\n"
            "| Data flywheel | Product usage creates data that helps improve the product, attracting more usage. |\n"
            "| Early termination | User stops or abandons a response/workflow before completion. |\n"
            "| Preference data | Comparative evidence indicating one response/action is preferred over another. |\n"
            "| Dialogue diversity | Variety of tokens/topics/actions across a conversation. |\n"
            "| Leniency bias | Tendency to rate more positively than warranted. |\n"
            "| Position bias | Feedback influenced by where an option is displayed. |\n"
            "| Recency bias | Preference toward an option encountered later/more recently. |\n"
            "| Degenerate feedback loop | Predictions affect exposure/feedback, which then reinforces later predictions. |\n"
            "| Sycophancy | Model behavior that agrees with users to gain approval rather than prioritizing accuracy. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does the chapter recommend evolving the architecture gradually?\n"
            "2. What problem does context construction solve?\n"
            "3. What are two major categories of guardrails?\n"
            "4. What types of sensitive information can input guardrails detect?\n"
            "5. How does placeholder masking protect private data?\n"
            "6. What are common quality failures on the output side?\n"
            "7. Why should false refusals be monitored?\n"
            "8. What latency/cost problem do retries create?\n"
            "9. When is human fallback appropriate?\n"
            "10. Why can output guardrails be difficult with streaming?\n"
            "11. What is the purpose of a router?\n"
            "12. How can routing reduce cost?\n"
            "13. What is next-action routing?\n"
            "14. Why should routers typically be small and fast?\n"
            "15. What is the purpose of a model gateway?\n"
            "16. What gateway functions can be centralized beyond API abstraction?\n"
            "17. What is exact caching?\n"
            "18. Name three cache-eviction policies.\n"
            "19. How can a cache accidentally leak one user's information to another?\n"
            "20. How does semantic caching work?\n"
            "21. What makes semantic caching risky?\n"
            "22. Why do write actions require stronger controls than read-only tools?\n"
            "23. Define MTTD, MTTR, and CFR.\n"
            "24. Why should evaluation failures flow into monitoring and vice versa?\n"
            "25. Why should metrics be designed from failure modes?\n"
            "26. Give three conversational metrics that can be monitored without explicit ratings.\n"
            "27. When should checks be exhaustive versus sampled?\n"
            "28. How do metrics differ from logs?\n"
            "29. What extra information does a trace provide?\n"
            "30. Name the three drift categories highlighted in the lesson.\n"
            "31. What does an AI orchestrator do?\n"
            "32. What is chaining?\n"
            "33. Why can parallel steps reduce latency?\n"
            "34. Why might you delay adopting an orchestration framework?\n"
            "35. What three areas should you evaluate when choosing an orchestrator?\n"
            "36. What are the three major uses of user feedback?\n"
            "37. What is the difference between explicit and implicit feedback?\n"
            "38. Why is early termination only a probabilistic signal of failure?\n"
            "39. What does user rephrasing reveal?\n"
            "40. How can user edits become preference examples?\n"
            "41. Why is sentiment useful but ambiguous?\n"
            "42. Why is regeneration not automatically a negative signal?\n"
            "43. How can delete/share/rename actions be misinterpreted?\n"
            "44. Why does conversation length mean different things for companions and support bots?\n"
            "45. When should feedback be requested during the user journey?\n"
            "46. Why is workflow-integrated feedback often stronger than survey feedback?\n"
            "47. Why is surrounding conversation context useful when analyzing a downvote?\n"
            "48. Why must context collection respect privacy and consent?\n"
            "49. Why should users have an 'I don't know' option in some comparisons?\n"
            "50. How can public versus private feedback visibility change behavior?\n"
            "51. Explain leniency bias.\n"
            "52. Explain position bias.\n"
            "53. Explain recency/length preference bias.\n"
            "54. What is a degenerate feedback loop?\n"
            "55. What is exposure/popularity bias?\n"
            "56. Why can optimizing user approval create sycophancy?\n"
            "57. What signals should be combined with user feedback before model updates?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Successful AI products are systems, not model calls. Add architecture only when it solves a real "
            "problem, instrument every important component, and treat user feedback as noisy but valuable data. "
            "The long-term advantage comes from a loop in which production behavior improves evaluation, data, "
            "models, and product design without allowing complexity, privacy risk, or biased feedback to take "
            "control of the system.**\n"
        ),
        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "architecture-progression", "title": "Progressive architecture", "order": 1},
            {"id": "context-construction", "title": "Enhance context", "order": 2},
            {"id": "guardrails-overview", "title": "Guardrails overview", "order": 3},
            {"id": "input-guardrails", "title": "Input guardrails", "order": 4},
            {"id": "pii-masking", "title": "PII masking", "order": 5},
            {"id": "output-guardrails", "title": "Output guardrails", "order": 6},
            {"id": "retries-fallback", "title": "Retries and fallback", "order": 7},
            {"id": "guardrail-tradeoffs", "title": "Guardrail tradeoffs", "order": 8},
            {"id": "router", "title": "Router", "order": 9},
            {"id": "next-action-routing", "title": "Next-action routing", "order": 10},
            {"id": "gateway", "title": "Model gateway", "order": 11},
            {"id": "gateway-code", "title": "Gateway mental model", "order": 12},
            {"id": "gateway-capabilities", "title": "Gateway capabilities", "order": 13},
            {"id": "exact-cache", "title": "Exact caching", "order": 14},
            {"id": "cache-safety", "title": "Cache safety", "order": 15},
            {"id": "semantic-cache", "title": "Semantic caching", "order": 16},
            {"id": "agent-patterns", "title": "Agent patterns", "order": 17},
            {"id": "write-actions", "title": "Write actions", "order": 18},
            {"id": "observability", "title": "Observability", "order": 19},
            {"id": "metrics-by-failure", "title": "Metrics by failure mode", "order": 20},
            {"id": "conversational-monitoring", "title": "Conversational monitoring", "order": 21},
            {"id": "spot-vs-exhaustive", "title": "Spot versus exhaustive checks", "order": 22},
            {"id": "logs", "title": "Logs", "order": 23},
            {"id": "traces", "title": "Traces", "order": 24},
            {"id": "drift", "title": "Drift detection", "order": 25},
            {"id": "orchestration", "title": "Pipeline orchestration", "order": 26},
            {"id": "orchestration-example", "title": "Orchestrated pipeline example", "order": 27},
            {"id": "choosing-orchestrator", "title": "Choosing an orchestrator", "order": 28},
            {"id": "feedback-value", "title": "Value of user feedback", "order": 29},
            {"id": "explicit-implicit", "title": "Explicit versus implicit feedback", "order": 30},
            {"id": "early-termination", "title": "Early termination", "order": 31},
            {"id": "error-correction", "title": "Error correction", "order": 32},
            {"id": "edits-preferences", "title": "User edits and preferences", "order": 33},
            {"id": "complaints-sentiment", "title": "Complaints and sentiment", "order": 34},
            {"id": "regeneration", "title": "Regeneration", "order": 35},
            {"id": "conversation-actions", "title": "Conversation actions and length", "order": 36},
            {"id": "feedback-design", "title": "Feedback design", "order": 37},
            {"id": "when-feedback", "title": "When to collect feedback", "order": 38},
            {"id": "workflow-feedback", "title": "Workflow-integrated feedback", "order": 39},
            {"id": "feedback-context", "title": "Feedback context and privacy", "order": 40},
            {"id": "feedback-usability", "title": "Feedback usability", "order": 41},
            {"id": "public-private-feedback", "title": "Public versus private feedback", "order": 42},
            {"id": "feedback-biases", "title": "Feedback biases", "order": 43},
            {"id": "degenerate-loop", "title": "Degenerate feedback loops", "order": 44},
            {"id": "sycophancy", "title": "Sycophancy risk", "order": 45},
        ],
    },

    "exercises": [
        {
            "id": "M10.L01.EX01",
            "title": "Evolve a Simple AI App into a Production Architecture",
            "lesson_code": "M10.L01",
            "section_id": "semantic-cache",
            "placement": "after_section",
            "description": (
                "Start with a single model call and add only the architecture needed "
                "for a realistic customer-support assistant."
            ),
            "instructions": (
                "You start with `query -> model -> response`.\n\n"
                "1. Add context construction for company policies and customer records.\n"
                "2. Define two input guardrails and two output guardrails.\n"
                "3. Design a PII masking strategy before external API calls.\n"
                "4. Create at least four router destinations/intent classes.\n"
                "5. Define what belongs in the model gateway.\n"
                "6. Decide which queries are safe for exact caching.\n"
                "7. Decide whether semantic caching is worth using and define a "
                "false-hit evaluation if you use it.\n"
                "8. Give one personalized query that must never use a shared generic cache.\n"
                "9. Add a fallback policy for provider outage and repeated bad responses.\n"
                "10. Draw the final request flow and explain why each added component exists."
            ),
            "expected_output": (
                "A production architecture diagram/description that justifies context, guardrails, "
                "routing, gateway, caching, and fallback choices."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "architecture-design",
                "guardrails",
                "routing",
                "gateway",
                "caching",
            ],
        },

        {
            "id": "M10.L01.EX02",
            "title": "Design Observability for a RAG Agent",
            "lesson_code": "M10.L01",
            "section_id": "orchestration-example",
            "placement": "after_section",
            "description": (
                "Design metrics, logs, traces, and drift checks for a multi-component "
                "AI pipeline rather than monitoring only the final model output."
            ),
            "instructions": (
                "Assume your application is a RAG assistant that can search internal documents "
                "and escalate to a human.\n\n"
                "1. Define five important failure modes.\n"
                "2. Define at least one metric per failure mode.\n"
                "3. Define TTFT/TPOT/cost metrics and how they should be sliced.\n"
                "4. Decide which quality checks run exhaustively and which run on samples.\n"
                "5. List the model/prompt/retrieval/tool configuration that must be logged.\n"
                "6. Design one end-to-end request trace.\n"
                "7. Define alerts that would reduce MTTD.\n"
                "8. Define the debugging information needed to reduce MTTR.\n"
                "9. Define prompt-drift, user-behavior-drift, and provider-model-drift checks.\n"
                "10. Explain how production failures are added back into the evaluation set.\n"
                "11. Identify two pipeline steps that can run in parallel.\n"
                "12. State what an orchestrator must expose so it does not hide debugging details."
            ),
            "expected_output": (
                "An observability and orchestration design covering metrics, logs, traces, "
                "drift, alerts, debugging, evaluation feedback, and latency-aware execution."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "observability",
                "metrics",
                "logging",
                "tracing",
                "drift-detection",
                "orchestration",
            ],
        },

        {
            "id": "M10.L01.EX03",
            "title": "Build a Trustworthy User-Feedback System",
            "lesson_code": "M10.L01",
            "section_id": "sycophancy",
            "placement": "after_section",
            "description": (
                "Design feedback collection that creates useful product/model signals "
                "without treating noisy user behavior as ground truth."
            ),
            "instructions": (
                "Design feedback for an AI writing assistant.\n\n"
                "1. Define three explicit feedback mechanisms.\n"
                "2. Define six implicit conversational/workflow signals.\n"
                "3. For each implicit signal, list at least one alternative interpretation.\n"
                "4. Define when the product should ask for feedback and when it should stay silent.\n"
                "5. Explain how direct user edits can become preference examples.\n"
                "6. Define what conversation context is useful for interpreting a downvote.\n"
                "7. Define the consent/privacy flow for collecting that context.\n"
                "8. Design an experiment to detect position bias in side-by-side comparisons.\n"
                "9. Explain how you would detect leniency and random-click bias.\n"
                "10. Design one safeguard against a degenerate feedback loop.\n"
                "11. Explain how factual evaluation prevents pure approval optimization from "
                "turning into sycophancy.\n"
                "12. Define how feedback feeds evaluation, personalization, and future training differently."
            ),
            "expected_output": (
                "A feedback-system specification covering explicit/implicit signals, ambiguity, "
                "privacy, bias experiments, feedback-loop safeguards, and downstream uses."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "feedback-design",
                "implicit-feedback",
                "preference-data",
                "privacy",
                "feedback-bias",
                "data-flywheel",
            ],
        },
    ],

    "quiz": {
        "id": "M10.L01.QZ01",
        "title": "AI Engineering Architecture and User Feedback — Knowledge Check",
        "lesson_code": "M10.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M10.L01.Q01",
                "section_id": "architecture-progression",
                "question": "Why does the chapter build the architecture gradually?",
                "options": [
                    "Each extra component should solve a real need because complexity adds new failure modes",
                    "Foundation models cannot use multiple components",
                    "Only simple systems can be deployed",
                    "Routers must always be implemented last",
                ],
                "correct": 0,
                "explanation": (
                    "Progressive architecture keeps the system understandable and adds complexity only when justified."
                ),
            },
            {
                "id": "M10.L01.Q02",
                "section_id": "pii-masking",
                "question": "What is the purpose of a reverse PII map?",
                "options": [
                    "Restore masked sensitive values inside the trusted system after external processing",
                    "Train the external model on user data",
                    "Route requests to a cheaper model",
                    "Increase cache hit rate",
                ],
                "correct": 0,
                "explanation": (
                    "The map links placeholders back to original private values without sending those values outside the trust boundary."
                ),
            },
            {
                "id": "M10.L01.Q03",
                "section_id": "output-guardrails",
                "question": "Why should false refusals be monitored?",
                "options": [
                    "Overly restrictive guardrails can block legitimate user tasks",
                    "They always indicate data leakage",
                    "They reduce the number of logs",
                    "They only occur in self-hosted models",
                ],
                "correct": 0,
                "explanation": (
                    "A system can become unusable if safety controls reject too many legitimate requests."
                ),
            },
            {
                "id": "M10.L01.Q04",
                "section_id": "router",
                "question": "What is a router primarily responsible for?",
                "options": [
                    "Selecting the appropriate model, solution, or path for a request",
                    "Storing all model weights",
                    "Replacing observability",
                    "Deduplicating training data",
                ],
                "correct": 0,
                "explanation": (
                    "Routing decides where a request should go based on intent, cost, context, or next action."
                ),
            },
            {
                "id": "M10.L01.Q05",
                "section_id": "gateway-capabilities",
                "question": "Which is a natural responsibility of a model gateway?",
                "options": [
                    "Centralized access control and provider fallback",
                    "Manually labeling all training data",
                    "Computing transformer gradients",
                    "Replacing every tool with one prompt",
                ],
                "correct": 0,
                "explanation": (
                    "A gateway centralizes access to model endpoints and can enforce policies, quotas, logging, and fallbacks."
                ),
            },
            {
                "id": "M10.L01.Q06",
                "section_id": "cache-safety",
                "question": "Why can exact caching still cause a privacy leak?",
                "options": [
                    "The same query text can produce user-specific answers based on hidden context",
                    "Exact caches cannot store strings",
                    "Caches always send data to public APIs",
                    "LRU automatically shares all responses",
                ],
                "correct": 0,
                "explanation": (
                    "A cache key that ignores personalization can reuse one user's sensitive result for another user."
                ),
            },
            {
                "id": "M10.L01.Q07",
                "section_id": "semantic-cache",
                "question": "What is the main correctness risk of semantic caching?",
                "options": [
                    "Two similar queries can still require different answers",
                    "Embeddings always cost more than model calls",
                    "Vector search cannot store metadata",
                    "It only works for exact matches",
                ],
                "correct": 0,
                "explanation": (
                    "A false semantic match can return a cached response that does not answer the actual query."
                ),
            },
            {
                "id": "M10.L01.Q08",
                "section_id": "write-actions",
                "question": "Why are write actions especially risky?",
                "options": [
                    "Errors can create real side effects in the environment",
                    "They cannot be logged",
                    "They always require a large model",
                    "They remove all user control",
                ],
                "correct": 0,
                "explanation": (
                    "A wrong write action can send, purchase, modify, or transfer something rather than merely generate bad text."
                ),
            },
            {
                "id": "M10.L01.Q09",
                "section_id": "observability",
                "question": "What does MTTD measure?",
                "options": [
                    "How long it takes to detect a problem",
                    "How long it takes to train a model",
                    "How many tokens a response contains",
                    "How often users regenerate",
                ],
                "correct": 0,
                "explanation": (
                    "Mean time to detection measures how quickly operational problems become visible."
                ),
            },
            {
                "id": "M10.L01.Q10",
                "section_id": "metrics-by-failure",
                "question": "What is the best starting point for choosing monitoring metrics?",
                "options": [
                    "Identify the failure modes and opportunities you need to detect",
                    "Track every number available",
                    "Use only business metrics",
                    "Copy another company's dashboard",
                ],
                "correct": 0,
                "explanation": (
                    "Metrics are useful when they reveal specific risks, failures, or opportunities relevant to the product."
                ),
            },
            {
                "id": "M10.L01.Q11",
                "section_id": "traces",
                "question": "What distinguishes a trace from a set of logs?",
                "options": [
                    "A trace links related events into the end-to-end path of one request/workflow",
                    "A trace contains only aggregate numbers",
                    "Logs cannot contain timestamps",
                    "Traces never include tool calls",
                ],
                "correct": 0,
                "explanation": (
                    "Tracing reconstructs how one request moved through multiple components."
                ),
            },
            {
                "id": "M10.L01.Q12",
                "section_id": "drift",
                "question": "Which is an example of underlying-model drift?",
                "options": [
                    "A provider changes the model behind an unchanged API endpoint/name",
                    "A user writes a longer prompt",
                    "The application adds a new cache key",
                    "A log file grows",
                ],
                "correct": 0,
                "explanation": (
                    "Provider-side model changes can alter behavior even when the client integration appears unchanged."
                ),
            },
            {
                "id": "M10.L01.Q13",
                "section_id": "orchestration",
                "question": "What is a core job of an AI orchestrator?",
                "options": [
                    "Define components and chain their data flow into an end-to-end pipeline",
                    "Replace all models with one classifier",
                    "Design GPU hardware",
                    "Remove the need for monitoring",
                ],
                "correct": 0,
                "explanation": (
                    "Orchestration coordinates components and passes outputs/inputs across the workflow."
                ),
            },
            {
                "id": "M10.L01.Q14",
                "section_id": "explicit-implicit",
                "question": "Which is an example of implicit feedback?",
                "options": [
                    "User stops generation and rephrases the request",
                    "User clicks a requested thumbs-down button",
                    "User completes a five-star survey",
                    "User explicitly writes 'this was useful' in a feedback form",
                ],
                "correct": 0,
                "explanation": (
                    "Implicit feedback is inferred from normal user behavior rather than a dedicated feedback request."
                ),
            },
            {
                "id": "M10.L01.Q15",
                "section_id": "edits-preferences",
                "question": "How can a user edit become preference data?",
                "options": [
                    "The edited version can be treated as preferred over the original generated version",
                    "The original response is automatically deleted from all logs",
                    "Every edit proves the full answer was wrong",
                    "Edits replace the need for consent",
                ],
                "correct": 0,
                "explanation": (
                    "The original and edited outputs can form a losing/winning pair, subject to privacy and quality checks."
                ),
            },
            {
                "id": "M10.L01.Q16",
                "section_id": "regeneration",
                "question": "Why is regeneration an ambiguous feedback signal?",
                "options": [
                    "Users may be dissatisfied or may simply want additional options",
                    "Regeneration always means the first answer was wrong",
                    "It cannot be measured",
                    "Only developers can trigger it",
                ],
                "correct": 0,
                "explanation": (
                    "The same action can reflect dissatisfaction, uncertainty checking, or curiosity."
                ),
            },
            {
                "id": "M10.L01.Q17",
                "section_id": "feedback-usability",
                "question": "Why should users sometimes be offered an 'I don't know' option?",
                "options": [
                    "Forcing a choice on questions users cannot judge creates noisy labels",
                    "It increases model latency",
                    "It prevents all feedback bias",
                    "It guarantees more positive ratings",
                ],
                "correct": 0,
                "explanation": (
                    "Users should not be forced to fabricate preference or correctness judgments they cannot make."
                ),
            },
            {
                "id": "M10.L01.Q18",
                "section_id": "feedback-biases",
                "question": "What is position bias?",
                "options": [
                    "Users are more likely to select an option because of where it is displayed",
                    "Users always choose the longest answer",
                    "Users dislike recent outputs",
                    "Users prefer private feedback",
                ],
                "correct": 0,
                "explanation": (
                    "Presentation order can influence feedback independently of true quality."
                ),
            },
            {
                "id": "M10.L01.Q19",
                "section_id": "degenerate-loop",
                "question": "What creates a degenerate feedback loop?",
                "options": [
                    "Model outputs influence what users see, user feedback then reinforces those outputs",
                    "Users never provide feedback",
                    "All feedback is hidden from the model",
                    "A system uses exact caching",
                ],
                "correct": 0,
                "explanation": (
                    "Exposure affects feedback, and feedback affects future exposure, which can amplify small initial biases."
                ),
            },
            {
                "id": "M10.L01.Q20",
                "section_id": "sycophancy",
                "type": "open",
                "question": (
                    "Design a production architecture and feedback loop for an AI support assistant. "
                    "Explain where you would place retrieval, guardrails, routing, the model gateway, "
                    "caches, human fallback, logging/tracing, and orchestration. Then define explicit "
                    "and implicit feedback signals, explain their biases, and describe how you would "
                    "use feedback to improve evaluation and future models without creating privacy "
                    "violations, degenerate feedback loops, or sycophancy."
                ),
            },
        ],
        "passing_score": 70,
    },
}
