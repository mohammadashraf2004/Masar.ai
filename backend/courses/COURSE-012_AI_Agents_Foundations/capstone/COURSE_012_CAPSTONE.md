# COURSE-012 Capstone — Production Agentic AI System

Build a production-oriented agentic system that integrates the architecture developed throughout COURSE-012.

## Required phases

1. **Architecture review** — identify agent vs deterministic-code boundaries.
2. **Typed contracts** — define inputs, outputs, tools, memory access, permissions, timeouts, budgets, and handoffs.
3. **MCP integration** — include at least one custom MCP capability and one additional tool/service.
4. **Multi-agent coordination** — use a justified flow, orchestrator, or collaboration pattern.
5. **Persistent memory** — include session state, long-term memory, capture/retrieval policy, scope isolation, and compression/forgetting.
6. **Long-horizon execution** — external plan/state, structured iterations, hard limits, cost budget, quality threshold, stagnation detection, terminal fallback.
7. **Adaptive behavior** — demonstrate contradiction, stagnation, or low-confidence handling that causes a pivot/replan/escalation.
8. **Evaluation** — at least 25 benchmark cases, repeated runs, deterministic checks, semantic evaluation, and a human-review sample.
9. **Security** — least privilege, user-scoped authorization, schema validation, prompt-injection defenses, untrusted tool-result handling, sandbox/egress restrictions, HITL for high-risk actions, audit trail.
10. **Reliability drill** — simulate tool timeout/failure, duplicate request, bad retrieval, malicious retrieved content, memory conflict, budget exhaustion, worker failure, and low confidence.
11. **Release** — version code/agents/prompts/models/tools/memory schema/policies/eval suite and define canary/rollback gates.

## Acceptance questions

The architecture must clearly answer:

- Why is each component an agent rather than deterministic code?
- Why are multiple agents required?
- Where does state live, and what survives a crash?
- What stops loops and duplicate side effects?
- What happens when evidence is weak or the system does not know?
- Which actions require human approval?
- How is improvement measured?
- How is a bad release rolled back?
