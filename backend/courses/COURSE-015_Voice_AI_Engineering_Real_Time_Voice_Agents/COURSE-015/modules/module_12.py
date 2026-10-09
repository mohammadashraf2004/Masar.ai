"""M01.L12 — Security, Privacy, Responsible AI, and Identity for Agent Systems.

One source chapter -> one complete learner-facing lesson.

Source alignment:
- Chapter 19: Security, Privacy, and Responsible AI

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L12"
MODULE_ORDER = 1
MODULE_TITLE = "Security, Privacy, Responsible AI & Agent Identity"
MODULE_DESCRIPTION = (
    "Secure enterprise agent systems through eight layers of defense, Responsible AI "
    "guardrails for text and live multimodal streams, OAuth-based user and agent identity, "
    "observability, governance, user-identity propagation, token exchange, and secretless "
    "agent authentication."
)
SOURCE_CHAPTER = 19
SOURCE_PAGES = "Early Release draft; page numbers not provided"

TOPIC = {
    "title": "Security, Privacy, Responsible AI, and Identity for Agent Systems",
    "slug": "agent-foundations-m01-l12",
    "description": (
        "Learn how to protect an autonomous digital workforce from infrastructure attacks, "
        "network threats, data leaks, prompt attacks, unsafe tools, identity failures, "
        "observability gaps, compliance problems, and live multimodal risks."
    ),
    "order": 12,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 8.0,
    "skill_tags": [
        "agent-security",
        "defense-in-depth",
        "infrastructure-security",
        "network-security",
        "data-security",
        "responsible-ai",
        "guardrails",
        "prompt-injection",
        "tool-security",
        "oauth2",
        "jwt",
        "identity-propagation",
        "token-exchange",
        "mtls",
        "observability",
        "opentelemetry",
        "grc",
        "live-multimodal-security",
        "privacy-buffer",
        "guardrail-agent",
        "secretless-agents",
    ],
    "prerequisite_ids": [
        "M01.L01", "M01.L02", "M01.L03", "M01.L04", "M01.L05", "M01.L06",
        "M01.L07", "M01.L08", "M01.L09", "M01.L10", "M01.L11",
    ],

    "lesson": {
        "title": "Security, Privacy, Responsible AI, and Identity for Agent Systems",
        "estimated_minutes": 480,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Security, Privacy, Responsible AI, and Identity for Agent Systems

> **Lesson:** M01.L12  
> **Source alignment:** Chapter 19 of the supplied Early Release material.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why agentic systems have higher security stakes than passive applications.
- Describe the eight-layer defense-in-depth model used by the source.
- Explain infrastructure hardening through physical security, hardware trust, HSMs, SBOMs, TEEs, and air-gapped deployment.
- Explain network isolation, ingress, egress, NAT, VPCs, private model access, and private interconnects.
- Explain encryption in transit, encryption at rest, CMEK, redaction, vector-store hygiene, lineage, and retention.
- Explain the AI application threat surface: prompt injection, jailbreaking, and sensitive-information disclosure.
- Distinguish input guardrails and output guardrails.
- Explain why model weights and AI supply chains require protection.
- Explain the purpose of real-time interception, circuit breakers, and kill switches.
- Explain session isolation and indirect prompt injection.
- Apply least privilege, HITL, and schema validation to tool security.
- Explain why generated code must run in isolated sandboxes.
- Distinguish Authentication from Authorization.
- Explain why long-lived passwords and API keys are weaker than scoped, short-lived access tokens.
- Explain JWT scope and expiration.
- Explain the source's 3-legged OAuth Authorization Code flow.
- Explain the source's 2-legged OAuth Client Credentials flow.
- Compare user identity and non-human agent identity.
- Explain why OAuth client secrets must remain server-side.
- Explain the role of redirect URIs and scopes.
- Explain OpenTelemetry distributed tracing for multi-agent systems.
- Track AI-specific operational metrics: tokens, cost, TTFT, latency, CPU, and memory.
- Explain safe audit logging and PII redaction.
- Explain warning alerts, circuit breakers, and kill switches.
- Explain the role of GRC, audits, HITL protocols, and Shadow AI management.
- Explain the six callback interception points described for text-based agent guardrails.
- Explain why reusable security plugins reduce duplicated guardrail code.
- Explain the distinction between developer-level agent guardrails and administrator-level model guardrails.
- Explain the Model Gateway pattern for multimodal safety.
- Explain the role of a dedicated Guardrail Agent.
- Explain why text-transcription guardrails can be reactive rather than proactive.
- Explain the Privacy Buffer architecture for proactive audio screening.
- Explain independent parallel multimodal guardrails and dual-gate control.
- Explain why text transcription alone cannot detect all audio/video safety signals.
- Explain the trade-off between managed and self-hosted guardrail models under strict privacy requirements.
- Explain the multi-agent User Identity Propagation problem.
- Explain the standard On-Behalf-Of flow.
- Explain why per-agent OBO logic can create N-squared maintenance complexity.
- Explain the centralized Agent Authorization Authority pattern.
- Explain the security risk of building a custom credential vault.
- Explain the source's RFC 8693 Token Exchange architecture.
- Explain incremental authorization across multiple identity providers.
- Explain managed Agent Identities and the secretless-agent workflow.
- Explain the role of mTLS and an internal Certificate Authority in bootstrap identity.
- Distinguish human OAuth/OIDC from machine mTLS bootstrapping.
- Explain how unified user and agent identity creates auditable, least-privilege agent systems.

---

## 1. Why agent security has higher stakes

A static chatbot may return a wrong answer.

An agent may:

```text
modify a database
send an email
issue a refund
schedule a meeting
trigger a payment
delete data
```

The source uses a useful analogy:

```text
traditional app = library
agentic app = assistant with the keys to the office
```

The cost of failure can therefore be:

```text
wrong action
```

not only:

```text
wrong text
```

### Core principle

> Autonomy converts model mistakes into operational risk.

[[IMAGE_NEEDED: Passive chatbot vs acting agent | Left: chatbot only returns text; right: agent connected to payments, email, database, calendar, files | Learner should see why tool access increases the consequence of failure]]

---

## 2. Security is a stack, not a toggle

The source organizes security into eight layers:

```text
1. Infrastructure Security
2. Network Security
3. Data Security
4. AI Application Security
5. AI Agent Security
6. Identity & Access Management
7. Logging & Monitoring
8. Governance, Risk & Compliance
```

Each layer protects the next.

If one layer fails, another may contain the damage.

This is:

```text
Defense in Depth
```

[[IMAGE_NEEDED: Eight layers of defense | Stack from Infrastructure at bottom through Network, Data, AI Application, AI Agent, IAM, Logging/Monitoring, GRC at top | Learner should memorize the complete stack]]

---

## 3. Layer 1 — Infrastructure Security

Infrastructure security protects the physical and virtual compute where agents run.

The source divides this layer into:

```text
Physical Hardening
Hardware Integrity
Compute Isolation
```

If the host machine is compromised, prompt-level controls cannot save the system.

---

## 4. Physical hardening

Physical security includes controls such as:

- perimeter barriers,
- controlled entry,
- surveillance,
- security personnel,
- mantraps,
- biometric access.

For cloud users, much of this responsibility is inherited from the cloud provider.

The important lesson is:

> Cloud security includes physical trust assumptions, not only software.

---

## 5. Hardware integrity

The source highlights several mechanisms.

### TPM

A Trusted Platform Module provides a hardware root of trust.

It can help verify that the system booted without unauthorized tampering.

### HSM

A Hardware Security Module is designed for high-value cryptographic operations and key storage.

Use cases include protecting keys used for:

```text
agent identity
signing
encryption
```

### SBOM and supply-chain visibility

A Software Bill of Materials tracks software components and dependencies.

This helps detect compromised or vulnerable supply-chain components.

---

## 6. Compute isolation

Encryption at rest and in transit do not protect data while it is actively being processed.

The source discusses:

### Confidential Computing

Trusted Execution Environments protect data in use.

### Air-gapped systems

For highly sensitive environments, systems may run without public-internet connectivity.

This can require:

```text
local models
local tools
local infrastructure
```

### Principle

> Sensitive agent reasoning may need protection even from infrastructure operators.

---

## 7. Layer 2 — Network Security

If infrastructure is the building, network security is the hallway system.

Agent networks transport:

- prompts,
- retrieved data,
- A2A traffic,
- MCP traffic,
- external API calls,
- streaming responses.

The source focuses on:

```text
Isolation
Traffic Control
Private Model Access
Interconnectivity
```

---

## 8. VPC isolation

A Virtual Private Cloud provides a private software-defined network.

Agents can use private IPs and private routing rather than being directly exposed to the public internet.

### Mental model

```text
public cloud account
    !=
public network exposure
```

A properly designed cloud deployment may still be private.

---

## 9. Ingress control

Ingress defines:

```text
who may reach the agent
```

Examples:

- internal dashboard only,
- approved gateway,
- known source ranges,
- authenticated reverse proxy.

Publicly exposing every agent endpoint is usually unnecessary.

---

## 10. Controlled egress

Autonomous agents often need external access.

Examples:

- public APIs,
- package repositories,
- external SaaS.

The source describes NAT as a way to let private agents make outbound requests without directly exposing their private addresses.

But NAT alone is not enough.

---

## 11. Egress filtering

Egress filtering controls:

```text
where the agent is allowed to send data
```

This matters because a compromised agent may otherwise exfiltrate information.

Example:

```text
HR Agent
allowed:
payroll API

not allowed:
random external host
```

### Principle

> Least privilege applies to network destinations too.

---

## 12. Private model access

The source describes two high-level strategies.

### VPC-native/private managed access

Keep model traffic on provider/private networking.

### On-premise/open-weight hosting

For strict sovereignty/privacy requirements, host models locally.

The trade-off is between:

```text
capability
operational complexity
privacy
regulatory requirements
```

---

## 13. Private interconnectivity

Distributed enterprises may span:

```text
multiple VPCs
multiple clouds
on-premise systems
```

The source discusses:

- VPC peering,
- dedicated cross-cloud/on-premise interconnects.

The durable idea is:

> Sensitive east-west traffic should not automatically traverse the public internet.

---

## 14. Layer 3 — Data Security

The source organizes data security around:

```text
Encryption
Sanitization
Governance
```

Agent data includes:

- prompts,
- memories,
- tool results,
- embeddings,
- logs,
- files,
- vector-store content.

---

## 15. Encryption in transit

Traffic should use TLS.

For internal service-to-service communication, the source discusses mTLS.

With mTLS:

```text
server authenticates client
client authenticates server
```

This adds mutual identity to the encrypted channel.

---

## 16. Encryption at rest

Stored data includes:

```text
SQL data
vector databases
logs
long-term memory
artifacts
```

The source discusses Customer-Managed Encryption Keys as an option for organizations needing stronger control over encryption keys.

The key point is not the product name.

It is ownership of key lifecycle and revocation.

---

## 17. Sanitization before model or memory

Once sensitive data enters:

```text
model context
vector store
long-term memory
```

removal becomes difficult.

The source recommends DLP-style pipelines that detect and redact information such as:

- PII,
- PHI,
- payment data.

### Principle

> The cheapest sensitive datum to protect is the one you never ingest.

---

## 18. Vector-store hygiene

Embeddings should not be treated as magically anonymous.

The source warns that embeddings can still present reconstruction/privacy risks.

Therefore:

```text
vector store
```

should be protected similarly to other sensitive data stores.

Apply:

- access control,
- encryption,
- retention,
- lineage,
- deletion policy.

---

## 19. Data lineage

For high-stakes decisions, you need a paper trail.

If an agent makes a decision based on retrieved information, you should be able to answer:

```text
which document?
which database row?
which source?
which version?
```

Lineage supports:

- audits,
- grounding,
- incident review,
- explanation.

---

## 20. Retention and deletion

Do not retain every interaction forever.

Retention policy should define:

```text
what is stored
how long
why
when it is deleted
```

Examples:

```text
temporary session memory
quality-assurance logs
long-term preferences
regulated records
```

Long-term memory can become a liability if stale or sensitive data accumulates indefinitely.

{{exercise:M01.L12.EX01}}

---

## 21. Layer 4 — AI Application Security

This layer protects the application logic around the model.

The attacker may not attack the server syntax.

They may attack the model's interpretation of language.

This creates semantic security threats.

---

## 22. Prompt injection

A malicious user may provide instructions intended to override the system's intended behavior.

Example pattern:

```text
"Ignore previous instructions..."
```

The specific string is not the whole problem.

The deeper issue is:

```text
untrusted content attempting to become control instructions
```

---

## 23. Jailbreaking

Jailbreaking attempts to bypass model safety behavior.

It may use:

- personas,
- reframing,
- roleplay,
- multi-step manipulation.

The source gives persona-based attacks as an example.

The lesson is:

> Do not rely on one system prompt as the entire security perimeter.

---

## 24. Sensitive-information disclosure

A model or application may expose:

- private context,
- secrets,
- previous-session information,
- sensitive retrieved data.

This can happen even without a traditional infrastructure breach.

AI application security must therefore include explicit leakage prevention.

---

## 25. Input guardrails

Input guardrails inspect requests before the model receives them.

Possible functions:

```text
prompt-injection detection
jailbreak detection
topic policy
PII detection
malware/content screening
```

The source presents these as a deterministic enforcement layer around the model.

---

## 26. Output guardrails

Output guardrails inspect generated content before the user receives it.

Possible checks:

```text
toxicity
unsafe instructions
sensitive data
policy violations
hallucinated high-risk actions
```

The model's response is therefore not automatically trusted merely because it came from the approved model.

---

## 27. Model security and supply chain

Self-hosted models introduce additional concerns.

### Model weights

Treat them as valuable IP.

Apply:

- encryption,
- access control,
- controlled distribution.

### Third-party models/artifacts

Verify provenance and avoid untrusted serialized artifacts.

The source emphasizes software/model supply-chain security.

---

## 28. Observability and kill switches

Agent workflows may run for minutes.

The system needs a way to intervene when:

```text
agent loops
cost explodes
unsafe output repeats
tool calls become dangerous
```

Possible controls:

```text
warning
circuit breaker
kill switch
```

The kill switch is a last resort, not the first response.

---

## 29. Layer 5 — AI Agent Security

Agent security focuses on the unique risks created by:

```text
memory
tools
reasoning
planning
autonomy
```

The source divides it into:

```text
Context Security
Tool Security
Framework Hardening
```

---

## 30. Session isolation

User A's short-term state must never bleed into User B's.

Risks include:

- global variables,
- shared cache keys,
- incorrect session IDs,
- improperly partitioned state stores.

### Rule

> Conversation state is tenant/user/session scoped data.

---

## 31. Indirect prompt injection

The attacker may not be the user.

A retrieved webpage or document can contain malicious instructions.

Example concept:

```text
Research Agent reads webpage
webpage contains hidden instruction
agent follows it as if trusted
```

Therefore:

```text
retrieved content = untrusted data
```

not:

```text
retrieved content = trusted system instruction
```

Use separation, scanning, and clear instruction hierarchy.

---

## 32. Tool least privilege

Do not give an agent a master credential.

If the agent only needs:

```text
read balance
```

do not grant:

```text
modify balance
delete account
```

Permissions should be:

- task-specific,
- minimal,
- time-bounded where possible.

---

## 33. Human-in-the-loop for high-risk actions

Examples:

```text
refund student
change grade
send payment
delete production data
```

The agent can propose.

Execution waits for explicit human approval.

This separates:

```text
reasoning authority
```

from:

```text
final execution authority
```

---

## 34. Validate tool schemas before execution

LLMs can hallucinate arguments.

A tool call should pass strict validation before execution.

Examples:

- JSON Schema,
- typed models,
- parameter allow-lists.

MCP can help standardize tool contracts.

### Principle

> Model-generated arguments are untrusted input.

---

## 35. Framework hardening

Agent frameworks are dependencies.

Treat them like any other production software.

Apply:

- vulnerability scanning,
- patching,
- dependency pinning,
- security review.

Do not assume a popular agent framework is automatically safe.

---

## 36. Sandboxed code execution

Generated code should not run directly on the host.

Use:

```text
ephemeral sandbox
resource limits
no/limited network
temporary filesystem
destroy after execution
```

This is especially important for Python/terminal tools.

[[IMAGE_NEEDED: Agent tool security layers | Agent reasoning -> schema validation -> authorization/least privilege -> HITL for high risk -> sandbox/tool execution | Learner should see multiple controls before a real-world action occurs]]

{{exercise:M01.L12.EX02}}

---

## 37. Layer 6 — Identity & Access Management

IAM answers two different questions.

### Authentication

```text
Who are you?
```

### Authorization

```text
What are you allowed to do?
```

Valid identity does not imply unlimited permission.

---

## 38. Credential evolution

The source describes a progression:

```text
username/password
→ API key
→ short-lived access token
```

### Passwords

Poor for autonomous systems and dangerous to hard-code.

### API keys

Better for service access, but often:

- long-lived,
- broadly scoped.

### Access tokens

Can be:

- short-lived,
- signed,
- scoped,
- purpose-limited.

---

## 39. JWT access tokens

The source uses JWTs as the modern agent credential example.

Two important properties:

### Scope

What the holder may do.

Example:

```text
read:grades
```

not:

```text
write:grades
```

### Expiration

How long the token remains valid.

Short-lived credentials limit damage if stolen.

---

## 40. OAuth 2.0

OAuth provides standardized authorization flows for obtaining access tokens.

The exact provider configuration varies.

The source focuses on two broad patterns:

```text
3-legged Authorization Code
2-legged Client Credentials
```

---

## 41. 3-legged OAuth — human delegation

Use this when an agent needs to act on behalf of a human.

Example:

```text
Personal Assistant
needs user's Calendar access
```

Actors:

```text
User
Agent/Application
Authorization Server / Identity Provider
```

The user participates.

---

## 42. 3-legged flow step by step

### Redirect

User is sent to the trusted identity provider.

### Authenticate

The user logs in to the identity provider.

The agent never receives the raw password.

### Consent

The user sees requested scopes.

### Authorization code

The identity provider sends a temporary code back to an approved redirect URI.

### Token exchange

The backend exchanges the code for a user access token.

This token represents:

```text
Agent acting on behalf of User
```

---

## 43. Three important OAuth configuration elements

### Client ID and secret

Identify the application.

Never expose the secret in browser/client code.

### Authorized redirect URI

Defines where the identity provider may return the authorization result.

### Scopes

Define requested permissions.

Scopes implement least privilege.

---

## 44. 2-legged OAuth — machine identity

Use this when:

```text
Agent A
calls
Service/Agent B
```

without a human consent step.

Actors:

```text
Agent / Client
Authorization Server
```

The source frames this as establishing:

```text
Agent Identity
Non-Human Identity
```

---

## 45. Client Credentials flow

Conceptually:

```text
Agent presents client identity
   ↓
Authorization Server validates
   ↓
short-lived access token
   ↓
Agent calls service
```

There is:

- no browser redirect,
- no human popup.

Permissions are typically preconfigured administratively.

---

## 46. 2-legged vs 3-legged

| Dimension | 2-legged | 3-legged |
|---|---|---|
| Main use | machine-to-machine | user delegation |
| Human present | no | yes |
| Identity context | "I am Agent X" | "I am Agent X acting for User Y" |
| Permission | admin/preassigned | user-consented |
| Interaction | background | interactive |

This distinction becomes crucial later when identities need to flow across multi-agent chains.

---

## 47. Advanced identity exists, but master the core first

The source mentions more advanced patterns such as:

- token exchange,
- verifiable credentials,
- agent-payment identity patterns.

But 2-legged and 3-legged OAuth cover the majority of common scenarios in the chapter's framing.

The next challenge is not getting one token.

It is propagating the correct identity through several agents.

---

## 48. Layer 7 — Logging & Monitoring

Agents can fail without throwing an exception.

Examples:

```text
hallucination
wrong tool repeated
expensive loop
latency spike
memory leak
```

Observability must therefore cover behavior as well as infrastructure.

---

## 49. OpenTelemetry and distributed tracing

A request may cross:

```text
Tutor Agent
→ Search Agent
→ Vector DB
→ Tool Server
```

Isolated logs are insufficient.

Distributed tracing assigns a Trace ID and propagates it through services.

This lets engineers reconstruct:

```text
which hop was slow
which hop failed
where cost accumulated
```

[[IMAGE_NEEDED: Distributed trace across agents | User request -> Tutor Agent -> Search Agent -> Vector DB, all sharing one trace ID with waterfall timings | Learner should understand why local logs are insufficient]]

---

## 50. AI-specific and traditional operational metrics

The source includes:

### Token usage

Input/output consumption.

### Cost

Financial burn per task/session.

### TTFT

Time to first token.

### Total latency

Full interaction duration.

### CPU and memory

Traditional service resource usage.

### Tool/runtime payload size

Large tool results can destabilize context and infrastructure.

These metrics should be monitored together.

---

## 51. Safe audit logging

The source discusses logging enough reasoning/decision context to debug agent behavior.

But logs themselves can become a privacy problem.

Apply redaction before persistence.

Do not write:

```text
passwords
tokens
PII
sensitive tool payloads
```

into plain logs.

### Principle

> Observability must not create a second data leak.

---

## 52. From logs to action

Monitoring should drive action.

### Warning alerts

Example:

```text
80% of daily token budget reached
```

Notify owner before service failure.

### Critical mitigation

Examples:

```text
100% CPU
runaway loop
unsafe repeated output
```

Possible response:

```text
circuit breaker
pause
kill switch
```

---

## 53. Layer 8 — Governance, Risk & Compliance

Security is not only code.

Organizations also need:

- policy,
- audit,
- external validation,
- human accountability,
- legal compliance.

A technically secure system may still be non-compliant or unfair.

---

## 54. Third-party audits and certifications

The source gives examples such as:

- SOC 2 Type II,
- HIPAA-related requirements,
- GDPR obligations.

Treat exact legal/compliance requirements as jurisdiction- and context-specific.

The durable principle is:

> High-stakes systems need evidence that controls operate in practice, not only architecture diagrams.

---

## 55. HITL as a formal governance protocol

For critical actions, the source describes a "4-eyes" principle.

Example:

```text
Agent proposes scholarship > threshold
    ↓
human officer reviews
    ↓
explicit approval
    ↓
action executes
```

This makes HITL part of governance, not merely UX.

---

## 56. Human review can improve the system

HITL corrections can feed back into:

- examples,
- evaluation datasets,
- prompts,
- model/training improvements.

This creates:

```text
human correction
→ structured learning signal
→ future improvement
```

---

## 57. Shadow AI

Shadow AI occurs when employees use unapproved external AI tools.

Risks include:

```text
data leakage
lack of logging
unknown retention
weak governance
```

The source's strategic response is not simply:

```text
ban everything
```

but:

```text
provide secure sanctioned alternatives
```

Registry/discovery becomes part of security strategy.

---

## 58. Responsible AI for live multimodal agents

Traditional text guardrails can inspect a complete request before it reaches the model.

Live audio/video is different.

The stream is continuous.

Security decisions may need to happen:

```text
frame by frame
audio packet by audio packet
```

This changes the guardrail architecture.

---

## 59. Text guardrails use a toll-gate pattern

For text:

```text
input arrives
pause
scan
allow/block
continue
```

Because text is relatively lightweight, sequential inspection is practical.

The source splits responsibilities between:

```text
developer-level agent guardrails
platform-level model guardrails
```

---

## 60. Six callback interception points

The source describes six lifecycle hooks.

### Before Agent Call

Check:

- identity/access,
- session initialization,
- context integrity.

### Before Model Call

Check:

- prompt injection,
- jailbreak,
- input safety.

### After Model Call

Check:

- toxic/unsafe output,
- hallucination or policy risk.

### Before Tool Call

Check:

- authorization,
- OAuth scope,
- schema validity.

### After Tool Call

Check:

- tool-data leakage,
- sensitive fields,
- sanitization.

### After Agent Call

Check:

- final logging,
- cost,
- cleanup.

[[IMAGE_NEEDED: Six callback security hooks | User -> before agent -> before model -> after model -> before tool -> after tool -> after agent -> user, with example security checks at each | Learner should understand callbacks as lifecycle interception points]]

---

## 61. Security plugins reduce duplication

Writing six callbacks for every agent is repetitive.

Reusable plugins can package policies such as:

```text
PII scrubber
prompt-injection scanner
tool authorization
audit logger
```

This improves standardization.

However, if attaching the plugin is optional, developer omission remains a risk.

That leads to centralized platform guardrails.

---

## 62. Model Gateway for centralized policy

A Model Gateway sits between applications and foundation models.

Traffic flows through the gateway.

This enables platform administrators to apply organization-wide controls.

The source also gives managed gateway/security product examples.

Treat those names as time-sensitive implementation examples.

The architecture matters more:

```text
application
→ centralized gateway
→ model
```

---

## 63. Multimodal guardrails need more than regex

A 4K image or live video stream cannot always be checked cheaply with simple rules.

The source extends the gateway with:

```text
Guardrail Agent
```

This specialized model focuses on safety rather than task reasoning.

It may detect:

- PII in images,
- nudity,
- violence,
- unsafe visual content,
- sensitive signals.

---

## 64. Guardrail Agent

The main model is optimized to help.

The Guardrail Agent is optimized to scrutinize.

The source suggests using a smaller/faster multimodal model for this role.

Why?

```text
lower cost
lower latency
specialized task
```

Exact model names and latency claims should be reverified.

---

## 65. Live streaming is the hardest safety case

With WebSocket audio/video:

```text
data never waits for a complete file
```

You cannot simply:

```text
upload
scan
approve
process
```

You need streaming enforcement.

---

## 66. Strategy A — transform audio into text

The source first simplifies live audio security by using real-time transcriptions.

The main model returns:

```text
audio response
input transcript
output transcript
```

The Guardrail Agent scans the transcripts.

This turns:

```text
audio safety problem
```

into:

```text
text safety problem
```

for many policy categories.

---

## 67. Output Gate

If the transcript is safe:

```text
audio continues
```

If unsafe:

```text
gate closes
audio stops
safe fallback/error is returned
```

This is effective for stopping harmful output from reaching the user.

But it is still reactive on the input side.

---

## 68. The reactive privacy gap

If the main model must hear the audio before it can produce a transcript, sensitive information has already reached the model.

Example:

```text
user speaks sensitive identifier
main model receives audio
transcript generated
guardrail detects PII
```

Detection occurred too late to prevent exposure to the model.

---

## 69. Strategy B — proactive Privacy Buffer

The source moves transcription into the gateway.

Components:

```text
local/edge STT
Guardrail Agent
Input Gate
short audio buffer
```

The incoming audio waits briefly before being released to the reasoning model.

Exact buffer durations in the source should be treated as implementation-specific examples.

[[IMAGE_NEEDED: Privacy Buffer architecture | User audio -> Gateway buffer; parallel local STT -> Guardrail Agent -> allow signal; safe audio released to reasoning model, unsafe audio dropped | Learner should see how inspection happens before model exposure]]

---

## 70. Privacy Buffer workflow

### 1. Transcribe locally

Audio becomes text before reaching the main model.

### 2. Scan

Guardrail checks for:

- PII,
- prohibited content.

### 3. Decide

If safe:

```text
open Input Gate
release buffered audio
```

If unsafe:

```text
discard audio
keep gate closed
notify user/client
```

### Benefit

The main model never receives the blocked input.

---

## 71. Text safety still has blind spots

Transcription cannot fully capture:

```text
screaming
sarcasm
gunshot sound
visual weapon
inappropriate gesture
distressed tone
```

These are multimodal signals.

Therefore, the source goes one step further.

---

## 72. Independent parallel multimodal guardrails

The gateway splits the live stream.

### Path A — production

Toward the main model, behind a gate.

### Path B — safety

Directly into a multimodal Guardrail Agent.

The safety model analyzes raw:

```text
audio
video
images
```

rather than only text.

---

## 73. Dual-gate control

The Guardrail Agent can control two gates.

### Input Gate

Protects the reasoning model from unsafe incoming content.

### Output Gate

Protects the user from unsafe generated content.

This creates independent safety enforcement on both directions of the live interaction.

[[IMAGE_NEEDED: Parallel multimodal dual-gate architecture | Gateway splits stream: Production path through Input Gate -> reasoning model -> Output Gate -> user; Safety path -> multimodal Guardrail Agent controlling both gates | Learner should understand independent safety monitoring]]

---

## 74. Privacy and guardrail model selection

A natural question:

```text
If the guardrail uses a managed external model,
is sensitive data still leaving my boundary?
```

The source distinguishes stricter environments from ordinary enterprise deployments.

For extreme requirements:

```text
self-hosted/open-weight guardrail model
inside trusted infrastructure
```

may be preferred.

The broader principle is:

> Safety architecture must satisfy the organization's privacy boundary, not only its content policy.

{{exercise:M01.L12.EX03}}

---

## 75. The Identity Gap in multi-agent systems

Suppose:

```text
Alice
→ Tutor Agent
→ Registrar Agent
→ Database Agent
```

Who is the caller at the database?

If downstream services see only:

```text
Tutor Agent
```

then Alice's permissions may be lost.

The Tutor may accidentally behave like a super-user.

The solution is:

```text
User Identity Propagation
```

---

## 76. Approach 1 — On-Behalf-Of flow

The first approach is a chained token exchange.

Conceptually:

```text
Alice gives token to Tutor
Tutor asks IdP:
"Give me a token for Registrar
on behalf of Alice."
```

The Registrar receives a token constrained for its own audience and still tied to Alice.

Benefits:

```text
least privilege
user-specific permissions
zero-trust style boundaries
```

---

## 77. OBO can create distributed auth complexity

If every agent must implement:

```text
token exchange
expiry recovery
retry
consent handling
audience logic
```

then authentication logic spreads across the agent mesh.

With many agents, this becomes difficult to maintain.

The source describes this as an N-squared-style maintenance problem.

---

## 78. Approach 2 — Agent Authorization Authority

The source centralizes identity work inside the Gateway.

Agents ask:

```text
"I need access to Registrar for Alice."
```

The Authority checks its credential/token store.

### Token exists

Return it.

### Token missing

Pause workflow and trigger user authorization.

This makes individual agents simpler.

---

## 79. Benefits of a centralized Authority

The source emphasizes:

### Single pane of glass

Users/administrators can see access centrally.

### Central revocation

Remove access once.

### Simpler agents

Agents do not reimplement complex OAuth flows.

But this architecture introduces a dangerous responsibility.

---

## 80. The custom-vault risk

If the Authority stores many refresh tokens, it becomes extremely sensitive infrastructure.

If compromised:

```text
many identities
many providers
many long-lived permissions
```

may be exposed.

Building your own identity provider/token vault is therefore a high-risk engineering task.

This motivates a standards-based broker.

---

## 81. Approach 3 — RFC 8693 Token Exchange

The source presents a mature broker architecture based on standardized Token Exchange.

The Authority becomes an identity broker rather than a custom password manager.

This is especially useful when one user has identities across:

```text
Google
GitHub
other providers
```

The broker can link these provider identities to one logical user context.

---

## 82. Incremental authorization

Suppose Alice has already connected Google.

Later the agent needs GitHub.

The workflow can:

```text
pause task
show "Connect GitHub"
redirect Alice to GitHub authorization
receive provider token
link it to Alice's session
resume original task
```

The user is not asked to authorize every possible provider upfront.

This is just-in-time permission expansion.

---

## 83. Multi-provider identity as a keyring

A useful mental model is:

```text
Alice's session
├── Google token
├── GitHub token
└── other provider tokens
```

When the agent needs a service:

```text
ask broker for correct token
```

The agent does not implement every provider's identity-linking rules itself.

---

## 84. Managed Agent Identities: toward secretless agents

User identity is only half the problem.

Agents themselves also need credentials.

Traditional 2-legged OAuth often depends on:

```text
client ID
client secret
```

stored in agent configuration.

That creates:

```text
Secret Sprawl
```

The source moves those secrets into the Authority.

---

## 85. Secretless-agent workflow

### Registration

Admin associates sensitive client credentials with an Agent Identity inside the Authority.

### Bootstrap

Running Agent proves its infrastructure identity.

### Request

Agent asks for a token for a target service.

### Authorization

Authority verifies the agent-to-service policy.

### Issuance

Authority performs the OAuth exchange.

### Return

Agent receives only a short-lived access token.

The long-lived client secret never lives inside application source/config.

---

## 86. Benefits of secretless identities

### Zero-touch rotation

Rotate the secret centrally.

No need to redeploy every agent instance.

### Service-map visibility

Every token request shows:

```text
which agent
wants to call
which service
```

The Authority can build a dependency map.

### Reduced credential leakage

Developers do not handle long-lived secrets directly.

---

## 87. How does an agent authenticate to the Authority?

This is the bootstrap problem.

The source proposes infrastructure identity such as:

```text
mTLS certificate
service identity
```

The agent needs a way to prove:

```text
"I am the authorized production workload."
```

before the Authority gives it tokens.

---

## 88. Internal Certificate Authority

An internal CA signs certificates for trusted internal workloads.

A certificate contains information such as:

```text
subject / workload identity
issuer
public key
```

The workload does not need to hard-code this certificate in source.

Infrastructure can inject it.

---

## 89. mTLS bootstrap

In ordinary TLS:

```text
server proves identity
```

In mTLS:

```text
server proves identity
client proves identity
```

When the Agent calls the Authority:

1. both present certificates,
2. the Authority verifies the agent's certificate against the trusted CA,
3. the secure connection is established,
4. token issuance can proceed.

---

## 90. Why humans use OAuth while agents may use mTLS

Humans interact through:

- browsers,
- phones,
- biometric/password login,
- consent screens.

Installing workload certificates on every user's device would create poor usability.

Agents are software workloads and can receive infrastructure-injected certificates safely.

Therefore:

```text
Human identity
→ OAuth/OIDC-style interactive flows

Agent workload identity
→ mTLS/infrastructure identity
```

The two mechanisms solve different identity problems.

---

## 91. Unified user and agent identity

The source's final identity architecture combines:

```text
User Identity Propagation
+
Agent Identity
```

A downstream action can conceptually be understood as:

```text
Agent X
acting on behalf of
User Y
against
Resource Z
```

This gives stronger:

- authorization,
- auditability,
- least privilege,
- traceability.

[[IMAGE_NEEDED: Unified identity chain | Alice -> Tutor Agent Identity -> Registrar Agent Identity -> Database, with user token context propagating through Token Exchange and agent workloads authenticated by mTLS | Learner should see user identity and agent identity traveling together]]

{{exercise:M01.L12.EX04}}

---

## 92. Complete security architecture

The whole chapter can be summarized as:

### Foundation

```text
Infrastructure
Network
Data
```

### AI-specific protection

```text
Application Guardrails
Agent Context
Tool Security
Framework Hardening
```

### Trust

```text
User Identity
Agent Identity
OAuth
Token Exchange
mTLS
```

### Visibility

```text
Tracing
Tokens
Cost
Latency
Resource metrics
Safe audit logs
```

### Governance

```text
Human approval
Audits
Compliance
Shadow AI management
```

### Live safety

```text
Model Gateway
Guardrail Agent
Input Gate
Output Gate
Privacy Buffer
Parallel Multimodal Safety
```

Security is the composition of all of these.

---

## 93. Production checklist

### Infrastructure

- hardened compute,
- trusted supply chain,
- protected cryptographic keys,
- isolation appropriate to sensitivity.

### Network

- private networking,
- ingress restrictions,
- egress filtering,
- private model/service routes.

### Data

- TLS/mTLS,
- encryption at rest,
- sanitization,
- vector-store controls,
- lineage,
- retention.

### AI application

- prompt-injection/jailbreak defenses,
- input/output guardrails,
- model artifact security,
- emergency controls.

### Agent

- session isolation,
- untrusted RAG-content handling,
- least-privilege tools,
- HITL,
- strict schemas,
- sandboxed code execution.

### IAM

- scoped short-lived tokens,
- 2-legged vs 3-legged flow chosen correctly,
- secrets never in frontend/source,
- user identity propagation,
- agent identity.

### Observability

- trace IDs,
- token/cost/latency metrics,
- CPU/memory,
- redacted audit logs,
- tiered alerts.

### Governance

- human oversight,
- access review,
- compliance controls,
- sanctioned AI alternatives.

### Live multimodal

- gateway-level safety,
- input/output gates,
- privacy buffer where required,
- raw multimodal guardrails for non-verbal risk.

### Identity broker

- standards-based token exchange,
- incremental auth,
- secretless workload identity,
- mTLS/bootstrap trust.

{{exercise:M01.L12.EX05}}

---

## 94. Source-specific details to re-check

This chapter is Early Release material.

Re-verify current guidance for:

- exact OWASP LLM Top 10 numbering,
- cloud-provider security products,
- specific OAuth provider behavior,
- specific access-token lifetimes,
- exact JWT recommendations,
- current RFC/token-exchange implementation support,
- managed identity-broker products,
- current mTLS/service-mesh integrations,
- exact OpenTelemetry AI conventions,
- named guardrail models/products,
- source-specific latency claims,
- privacy-buffer timing examples,
- specific compliance requirements,
- callback/plugin APIs.

Treat legal/compliance examples as educational source material, not as jurisdiction-specific legal advice.

The durable principles are:

```text
defense in depth
least privilege
strong identity
short-lived credentials
explicit human approval
strict schemas
safe memory
centralized observability
policy enforcement
user identity propagation
agent identity
multimodal safety
privacy before model exposure
```

---

## 95. Complete mental model

An enterprise agent should never be trusted merely because:

```text
the model is good
```

Trust emerges from the full system.

The secure path is:

```text
secure compute
   ↓
private network
   ↓
protected data
   ↓
input/application guardrails
   ↓
isolated agent context
   ↓
authorized validated tools
   ↓
verified user + agent identity
   ↓
observable execution
   ↓
human/compliance governance
```

For live multimodal interaction:

```text
Frontend
  ↓
Backend
  ↓
Model Gateway
  ├── Privacy / Input Gate
  ├── Guardrail Agent
  └── Output Gate
  ↓
Reasoning Model
```

For multi-agent identity:

```text
User
  ↓ delegated identity
Agent A
  ↓ token exchange
Agent B
  ↓ propagated user context
Resource
```

while agents themselves prove workload identity through trusted infrastructure.

That is the difference between an intelligent agent and a trustworthy enterprise agent.

---

## Important misconceptions

### Misconception 1
> "Security is mostly prompt engineering."

No. The source starts at hardware and networking and ends with governance.

### Misconception 2
> "A VPC automatically prevents data exfiltration."

No. Egress policy still matters.

### Misconception 3
> "Embeddings are safe because they are not readable text."

No. Treat vector stores as sensitive data stores.

### Misconception 4
> "If the model has safety training, external guardrails are unnecessary."

No. The source uses independent enforcement around the model.

### Misconception 5
> "A successful login means the user can do anything."

No. Authentication and authorization are different.

### Misconception 6
> "API keys are ideal long-term agent credentials."

No. They are often long-lived and broadly scoped.

### Misconception 7
> "3-legged OAuth is for agent-to-agent background traffic."

No. It is used when a human delegates access.

### Misconception 8
> "2-legged OAuth carries the human user's identity."

No. It primarily establishes the machine/agent identity.

### Misconception 9
> "Logging more is always safer."

No. Logs can leak PII or credentials.

### Misconception 10
> "A kill switch should be the first response to any anomaly."

No. Tiered warnings and circuit breakers should precede the nuclear option when appropriate.

### Misconception 11
> "Retrieved documents are trusted because they came from RAG."

No. Retrieved content can contain indirect prompt injection.

### Misconception 12
> "A tool call from the model is safe if the JSON parses."

No. Authorization, schema validation, and policy checks are still required.

### Misconception 13
> "Stopping unsafe output is enough for live-audio privacy."

No. The main model may already have received sensitive input.

### Misconception 14
> "Transcription-based guardrails detect every safety signal."

No. They can miss tone, sounds, gestures, and visual threats.

### Misconception 15
> "Agent Identity is the same as User Identity."

No. Both may need to be present simultaneously.

### Misconception 16
> "Passing the same user token through every agent is always the correct propagation model."

No. Audience-constrained exchange may be safer.

### Misconception 17
> "Centralizing refresh tokens in a custom vault automatically improves security."

No. It can create a catastrophic concentration of sensitive credentials.

### Misconception 18
> "Secretless agent identity means there are no credentials anywhere."

No. Long-lived secrets are removed from app code/runtime, while trusted infrastructure/Authority still manages credentials and certificates.

---

## Key terminology

| Term | Meaning |
|---|---|
| Defense in Depth | Multiple overlapping security layers |
| TPM | Hardware root-of-trust component |
| HSM | Dedicated secure cryptographic key hardware |
| SBOM | Software Bill of Materials |
| TEE | Trusted Execution Environment |
| VPC | Virtual Private Cloud |
| Ingress | Incoming network traffic policy |
| Egress | Outgoing network traffic policy |
| NAT | Network Address Translation gateway pattern |
| CMEK | Customer-managed encryption key |
| DLP | Data Loss Prevention |
| Data Lineage | Trace of where data originated and how it was used |
| Prompt Injection | Untrusted instruction attempting to override intended behavior |
| Jailbreak | Attempt to bypass model safety behavior |
| Input Guardrail | Policy check before model processing |
| Output Guardrail | Policy check after generation and before release |
| Session Isolation | Keeping each user's context separate |
| Indirect Prompt Injection | Malicious instruction embedded in retrieved content |
| Least Privilege | Grant only the minimum required permission |
| HITL | Human-in-the-Loop |
| Schema Validation | Strict validation of generated tool arguments |
| Authentication | Verify identity |
| Authorization | Verify permission |
| JWT | JSON Web Token |
| OAuth 2.0 | Authorization framework used for delegated/service access |
| 3-Legged OAuth | Interactive user-delegation flow |
| 2-Legged OAuth | Machine-to-machine client-credentials flow |
| OpenTelemetry | Telemetry standard for traces/metrics/logs |
| TTFT | Time to First Token |
| Circuit Breaker | Automatic mechanism that stops/pauses runaway behavior |
| GRC | Governance, Risk & Compliance |
| Shadow AI | Unsanctioned use of AI systems |
| Callback | Lifecycle interception hook |
| Security Plugin | Reusable bundle of guardrail callbacks |
| Model Gateway | Central control layer in front of models |
| Guardrail Agent | Dedicated model/agent focused on safety checks |
| Input Gate | Control preventing unsafe input from reaching reasoning model |
| Output Gate | Control preventing unsafe generated output from reaching user |
| Privacy Buffer | Short pre-model buffer enabling proactive input screening |
| User Identity Propagation | Carrying the human caller's identity through agent chains |
| OBO | On-Behalf-Of token exchange flow |
| Agent Authorization Authority | Central identity/token broker described by the source |
| RFC 8693 | Token Exchange standard referenced by the source |
| Incremental Authorization | Adding provider permissions only when needed |
| Secretless Agent | Agent that does not hold long-lived client secrets locally |
| Internal CA | Private Certificate Authority for trusted workloads |
| mTLS | Mutual TLS, where both client and server authenticate |

---

## Self-check

1. Why are agentic systems higher risk than passive chatbots?
2. What are the eight defense layers?
3. What does a TPM provide?
4. What is the role of an HSM?
5. Why is an SBOM relevant to agent security?
6. What problem does confidential computing address?
7. When might air-gapped deployment be appropriate?
8. What does a VPC provide?
9. What is ingress control?
10. Why is NAT not enough without egress filtering?
11. Why might model traffic remain on private networking?
12. What are the three pillars of data security in the source?
13. Why use mTLS internally?
14. Why are vector stores sensitive?
15. What is data lineage?
16. Why are retention policies necessary?
17. What is prompt injection?
18. How is jailbreaking different from ordinary infrastructure attack?
19. What is sensitive-information disclosure?
20. What do input guardrails inspect?
21. What do output guardrails inspect?
22. Why protect model weights?
23. When would a circuit breaker or kill switch be needed?
24. What is session bleeding?
25. What is indirect prompt injection?
26. Why must RAG data be treated as untrusted?
27. What does least privilege mean for agent tools?
28. Which actions deserve HITL?
29. Why validate every model-generated tool argument?
30. Why sandbox generated code?
31. What is the difference between AuthN and AuthZ?
32. Why are passwords poor credentials for autonomous agents?
33. What weakness do long-lived API keys have?
34. What do JWT scopes control?
35. Why does token expiration matter?
36. What is the 3-legged OAuth use case?
37. What happens during consent?
38. Why must Client Secrets never appear in client-side code?
39. Why is redirect URI validation important?
40. What is the 2-legged OAuth use case?
41. How does client-credentials identity differ from delegated user identity?
42. What is OpenTelemetry used for?
43. Why does distributed tracing need one Trace ID across services?
44. What is the difference between TTFT and total latency?
45. Why must logs be redacted?
46. What are warning alerts vs critical mitigation?
47. What is GRC?
48. What does the 4-eyes principle mean?
49. What is Shadow AI?
50. What are the six callback interception points?
51. Why package callbacks into plugins?
52. Why is centralized model-level policy needed in addition to developer callbacks?
53. What is a Guardrail Agent?
54. Why can live streaming not use only stop-and-check file scanning?
55. How does transcript-based guardrailing work?
56. What is the reactive privacy gap?
57. How does a Privacy Buffer close that gap?
58. What signals can raw multimodal guardrails detect that transcripts cannot?
59. What is dual-gate control?
60. When might a self-hosted guardrail model be required?
61. What is the Identity Gap?
62. How does OBO propagate user identity?
63. Why can OBO logic create maintenance complexity in large meshes?
64. What is the Agent Authorization Authority?
65. What is dangerous about a custom refresh-token vault?
66. Why use RFC 8693 Token Exchange?
67. What is incremental authorization?
68. How can one session contain identities from multiple providers?
69. What is Secret Sprawl?
70. How does the secretless-agent workflow reduce it?
71. What is the bootstrap identity problem?
72. How does mTLS solve workload authentication?
73. What is an Internal CA?
74. Why use OAuth/OIDC for humans and mTLS for workloads?
75. What does unified user + agent identity allow an enterprise to audit?
76. Which implementation details from this Early Release chapter should be re-verified before production?

---

## Retain this idea

**Trustworthy agents require defense in depth. Infrastructure, networks, and data must be protected before the model is even considered. The application then needs guardrails, the agent needs isolated context and least-privilege tools, identity must distinguish both the human and the software agent, observability must expose cost and behavior without leaking secrets, and governance must provide human accountability. Live audio and video add a new requirement: safety controls must operate on the stream itself, ideally before sensitive data reaches the reasoning model. In multi-agent systems, the final security challenge is identity propagation—ensuring every downstream service knows not only which agent is calling, but on whose behalf that agent is acting.**
""".strip(),

        "sections": [
            {"id": "power-liability", "title": "Why Agent Security Has Higher Stakes", "order": 1},
            {"id": "defense-depth", "title": "Security Is a Stack, Not a Toggle", "order": 2},
            {"id": "infra-security", "title": "Layer 1 — Infrastructure Security", "order": 3},
            {"id": "physical-hardening", "title": "Physical Hardening", "order": 4},
            {"id": "hardware-integrity", "title": "Hardware Integrity", "order": 5},
            {"id": "compute-isolation", "title": "Compute Isolation", "order": 6},
            {"id": "network-security", "title": "Layer 2 — Network Security", "order": 7},
            {"id": "vpc", "title": "VPC Isolation", "order": 8},
            {"id": "ingress", "title": "Ingress Control", "order": 9},
            {"id": "egress", "title": "Controlled Egress", "order": 10},
            {"id": "egress-filtering", "title": "Egress Filtering", "order": 11},
            {"id": "private-model-access", "title": "Private Model Access", "order": 12},
            {"id": "interconnectivity", "title": "Private Interconnectivity", "order": 13},
            {"id": "data-security", "title": "Layer 3 — Data Security", "order": 14},
            {"id": "encryption-transit", "title": "Encryption in Transit", "order": 15},
            {"id": "encryption-rest", "title": "Encryption at Rest", "order": 16},
            {"id": "sanitization", "title": "Sanitization Before Model or Memory", "order": 17},
            {"id": "vector-hygiene", "title": "Vector-Store Hygiene", "order": 18},
            {"id": "lineage", "title": "Data Lineage", "order": 19},
            {"id": "retention", "title": "Retention and Deletion", "order": 20},
            {"id": "app-security", "title": "Layer 4 — AI Application Security", "order": 21},
            {"id": "prompt-injection", "title": "Prompt Injection", "order": 22},
            {"id": "jailbreaking", "title": "Jailbreaking", "order": 23},
            {"id": "sensitive-disclosure", "title": "Sensitive-Information Disclosure", "order": 24},
            {"id": "input-guardrails", "title": "Input Guardrails", "order": 25},
            {"id": "output-guardrails", "title": "Output Guardrails", "order": 26},
            {"id": "model-supply-chain", "title": "Model Security and Supply Chain", "order": 27},
            {"id": "kill-switch", "title": "Observability and Kill Switches", "order": 28},
            {"id": "agent-security", "title": "Layer 5 — AI Agent Security", "order": 29},
            {"id": "session-isolation", "title": "Session Isolation", "order": 30},
            {"id": "indirect-injection", "title": "Indirect Prompt Injection", "order": 31},
            {"id": "least-privilege-tools", "title": "Tool Least Privilege", "order": 32},
            {"id": "hitl-tools", "title": "HITL for High-Risk Actions", "order": 33},
            {"id": "schema-validation", "title": "Validate Tool Schemas Before Execution", "order": 34},
            {"id": "framework-security", "title": "Framework Hardening", "order": 35},
            {"id": "sandbox", "title": "Sandboxed Code Execution", "order": 36},
            {"id": "iam", "title": "Layer 6 — Identity & Access Management", "order": 37},
            {"id": "credential-evolution", "title": "Credential Evolution", "order": 38},
            {"id": "jwt", "title": "JWT Access Tokens", "order": 39},
            {"id": "oauth", "title": "OAuth 2.0", "order": 40},
            {"id": "three-legged", "title": "3-Legged OAuth — Human Delegation", "order": 41},
            {"id": "three-legged-flow", "title": "3-Legged Flow Step by Step", "order": 42},
            {"id": "oauth-config", "title": "Important OAuth Configuration Elements", "order": 43},
            {"id": "two-legged", "title": "2-Legged OAuth — Machine Identity", "order": 44},
            {"id": "client-credentials", "title": "Client Credentials Flow", "order": 45},
            {"id": "two-vs-three", "title": "2-Legged vs 3-Legged", "order": 46},
            {"id": "advanced-identity", "title": "Advanced Identity Exists, but Master the Core First", "order": 47},
            {"id": "logging", "title": "Layer 7 — Logging & Monitoring", "order": 48},
            {"id": "otel", "title": "OpenTelemetry and Distributed Tracing", "order": 49},
            {"id": "ai-metrics", "title": "AI-Specific and Traditional Operational Metrics", "order": 50},
            {"id": "safe-audit", "title": "Safe Audit Logging", "order": 51},
            {"id": "alerts", "title": "From Logs to Action", "order": 52},
            {"id": "grc", "title": "Layer 8 — Governance, Risk & Compliance", "order": 53},
            {"id": "audits", "title": "Third-Party Audits and Certifications", "order": 54},
            {"id": "four-eyes", "title": "HITL as a Formal Governance Protocol", "order": 55},
            {"id": "human-feedback", "title": "Human Review Can Improve the System", "order": 56},
            {"id": "shadow-ai", "title": "Shadow AI", "order": 57},
            {"id": "rai-live", "title": "Responsible AI for Live Multimodal Agents", "order": 58},
            {"id": "text-tollgate", "title": "Text Guardrails Use a Toll-Gate Pattern", "order": 59},
            {"id": "callbacks", "title": "Six Callback Interception Points", "order": 60},
            {"id": "plugins", "title": "Security Plugins Reduce Duplication", "order": 61},
            {"id": "model-gateway", "title": "Model Gateway for Centralized Policy", "order": 62},
            {"id": "multimodal-gateway", "title": "Multimodal Guardrails Need More Than Regex", "order": 63},
            {"id": "guardrail-agent", "title": "Guardrail Agent", "order": 64},
            {"id": "live-streaming", "title": "Live Streaming Is the Hardest Safety Case", "order": 65},
            {"id": "transcription-strategy", "title": "Strategy A — Transform Audio into Text", "order": 66},
            {"id": "output-gate", "title": "Output Gate", "order": 67},
            {"id": "privacy-gap", "title": "The Reactive Privacy Gap", "order": 68},
            {"id": "privacy-buffer", "title": "Strategy B — Proactive Privacy Buffer", "order": 69},
            {"id": "privacy-workflow", "title": "Privacy Buffer Workflow", "order": 70},
            {"id": "transcription-blindspot", "title": "Text Safety Still Has Blind Spots", "order": 71},
            {"id": "parallel-guardrails", "title": "Independent Parallel Multimodal Guardrails", "order": 72},
            {"id": "dual-gate", "title": "Dual-Gate Control", "order": 73},
            {"id": "guardrail-privacy", "title": "Privacy and Guardrail Model Selection", "order": 74},
            {"id": "identity-gap", "title": "The Identity Gap in Multi-Agent Systems", "order": 75},
            {"id": "obo", "title": "Approach 1 — On-Behalf-Of Flow", "order": 76},
            {"id": "obo-cost", "title": "OBO Can Create Distributed Auth Complexity", "order": 77},
            {"id": "authority", "title": "Approach 2 — Agent Authorization Authority", "order": 78},
            {"id": "authority-benefits", "title": "Benefits of a Centralized Authority", "order": 79},
            {"id": "custom-vault-risk", "title": "The Custom-Vault Risk", "order": 80},
            {"id": "rfc8693", "title": "Approach 3 — RFC 8693 Token Exchange", "order": 81},
            {"id": "incremental-auth", "title": "Incremental Authorization", "order": 82},
            {"id": "multi-provider", "title": "Multi-Provider Identity as a Keyring", "order": 83},
            {"id": "secretless", "title": "Managed Agent Identities: Toward Secretless Agents", "order": 84},
            {"id": "secretless-flow", "title": "Secretless-Agent Workflow", "order": 85},
            {"id": "secretless-benefits", "title": "Benefits of Secretless Identities", "order": 86},
            {"id": "mtls-bootstrap", "title": "How Does an Agent Authenticate to the Authority?", "order": 87},
            {"id": "internal-ca", "title": "Internal Certificate Authority", "order": 88},
            {"id": "mtls-process", "title": "mTLS Bootstrap", "order": 89},
            {"id": "human-vs-agent-auth", "title": "Why Humans Use OAuth While Agents May Use mTLS", "order": 90},
            {"id": "unified-identity", "title": "Unified User and Agent Identity", "order": 91},
            {"id": "complete-security", "title": "Complete Security Architecture", "order": 92},
            {"id": "production-checklist", "title": "Production Checklist", "order": 93},
            {"id": "source-boundaries", "title": "Source-Specific Details to Re-Check", "order": 94},
            {"id": "complete-model", "title": "Complete Mental Model", "order": 95},
        ],
    },

    "exercises": [
        {
            "id": "M01.L12.EX01",
            "title": "Build a Defense-in-Depth Map",
            "lesson_code": "M01.L12",
            "section_id": "retention",
            "placement": "after_section",
            "description": "Map concrete threats to Layers 1–3.",
            "instructions": (
                "For an enterprise Registrar Agent, design controls for:\n"
                "1. compromised host,\n2. public network exposure,\n3. data exfiltration,\n"
                "4. PII entering a vector store,\n5. stale chat logs.\n"
                "Assign each control to Infrastructure, Network, or Data Security and explain why."
            ),
            "expected_output": "A threat-to-control table covering Layers 1–3.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["defense-in-depth", "network-security", "data-security"],
        },
        {
            "id": "M01.L12.EX02",
            "title": "Secure a High-Risk Tool Call",
            "lesson_code": "M01.L12",
            "section_id": "sandbox",
            "placement": "after_section",
            "description": "Apply agent-level protections around an action tool.",
            "instructions": (
                ('1. Design the controls for a ChangeGrade tool.\n'
                 '2. Include session isolation, indirect-injection defense, least-privilege scope, strict schema validation, HITL approval, audit logging, and rollback/error behavior.\n'
                 '3. Explain which checks happen before and after the tool call.')
            ),
            "expected_output": "A secure tool-execution sequence.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["tool-security", "hitl", "schema-validation"],
        },
        {
            "id": "M01.L12.EX03",
            "title": "Design Live Multimodal Guardrails",
            "lesson_code": "M01.L12",
            "section_id": "guardrail-privacy",
            "placement": "after_section",
            "description": "Compare reactive transcript scanning with proactive and parallel safety designs.",
            "instructions": (
                "Design security for a live Admissions Agent that accepts microphone and camera streams.\n"
                "1. Show the reactive transcript-based design.\n"
                "2. Identify its privacy gap.\n"
                "3. Add a Privacy Buffer with local STT and Input Gate.\n"
                "4. Add parallel raw audio/video safety analysis.\n"
                "5. Define Input Gate and Output Gate actions."
            ),
            "expected_output": "Three evolving live-safety architectures with trade-offs.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["live-multimodal-security", "privacy-buffer", "guardrail-agent"],
        },
        {
            "id": "M01.L12.EX04",
            "title": "Close the Multi-Agent Identity Gap",
            "lesson_code": "M01.L12",
            "section_id": "unified-identity",
            "placement": "after_section",
            "description": "Design identity propagation through a multi-agent chain.",
            "instructions": (
                "Trace Alice -> Tutor Agent -> Registrar Agent -> Database.\n"
                "Compare three approaches:\n"
                "1. direct OBO in each agent,\n2. centralized custom Authority,\n3. RFC 8693 broker-based Authority.\n"
                "Then add secretless Agent Identity using mTLS bootstrap.\n"
                "Explain how the final database can know both Alice and the calling Agent."
            ),
            "expected_output": "A user-and-agent identity architecture with trade-off analysis.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["identity-propagation", "token-exchange", "mtls"],
        },
        {
            "id": "M01.L12.EX05",
            "title": "Perform a Production Security Review",
            "lesson_code": "M01.L12",
            "section_id": "production-checklist",
            "placement": "after_section",
            "description": "Audit an enterprise agent platform across all eight layers.",
            "instructions": (
                ('1. Create an eight-layer security review for a live Financial Aid Agent.\n'
                 '2. For each layer, list at least three controls, one failure mode, and one monitoring/evidence item.\n'
                 '3. Add a final section for live multimodal safety and identity propagation.')
            ),
            "expected_output": "A complete production security audit checklist.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["security-architecture", "grc", "observability"],
        },
        {
            "id": "M01.L12.EX06",
            "title": "Choose 2-Legged or 3-Legged OAuth",
            "lesson_code": "M01.L12",
            "section_id": "two-vs-three",
            "placement": "after_section",
            "description": "Practice matching identity flows to real agent scenarios.",
            "instructions": (
                "Choose 2-legged or 3-legged OAuth for:\n"
                "1. Router Agent calling Weather Agent,\n"
                "2. Personal Assistant reading a user's Calendar,\n"
                "3. nightly batch agent updating a service,\n"
                "4. Tutor Agent accessing Alice's grades.\n"
                "For each, state whose identity the token represents and which scopes should be minimal."
            ),
            "expected_output": "A four-row OAuth-flow decision table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["oauth2", "authorization", "identity"],
        },
        {
            "id": "M01.L12.EX07",
            "title": "Design Safe Observability",
            "lesson_code": "M01.L12",
            "section_id": "alerts",
            "placement": "after_section",
            "description": "Build observability without turning logs into a privacy vulnerability.",
            "instructions": (
                ('1. Design telemetry for a Research Agent.\n'
                 '2. Include Trace ID propagation, token use, cost, TTFT, total latency, CPU, memory, tool-call metadata, redaction policy, warning thresholds, circuit breaker, and kill switch.\n'
                 '3. State which values must never be written to logs.')
            ),
            "expected_output": "An observability and mitigation specification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["opentelemetry", "monitoring", "safe-logging"],
        },
        {
            "id": "M01.L12.EX08",
            "title": "Design the Six Security Callbacks",
            "lesson_code": "M01.L12",
            "section_id": "callbacks",
            "placement": "after_section",
            "description": "Place controls at the correct agent lifecycle boundary.",
            "instructions": (
                ('1. For each callback—before agent, before model, after model, before tool, after tool, after agent—define at least one security check and one failure response.\n'
                 '2. Then identify which checks should also be enforced centrally at the platform/model gateway.')
            ),
            "expected_output": "A six-row callback security matrix plus centralized-policy layer.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["guardrails", "callbacks", "platform-security"],
        },
    ],

    "quiz": {
        "id": "M01.L12.QZ01",
        "title": "Security, Privacy, Responsible AI & Identity — Knowledge Check",
        "lesson_code": "M01.L12",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L12.Q01",
                "section_id": "power-liability",
                "question": "Why are agentic applications higher risk than passive chatbots?",
                "options": [
                    "They can perform real-world actions, so errors can become operational side effects",
                    "They cannot generate text",
                    "They never use networks",
                    "They are always public",
                ],
                "correct": 0,
                "explanation": "Autonomy increases the consequence of mistakes.",
            },
            {
                "id": "M01.L12.Q02",
                "section_id": "defense-depth",
                "question": "What does Defense in Depth mean?",
                "options": [
                    "Use multiple overlapping security layers so one failure does not expose the whole system",
                    "Use one perfect firewall",
                    "Rely only on model alignment",
                    "Encrypt only the database",
                ],
                "correct": 0,
                "explanation": "The chapter builds eight mutually reinforcing layers.",
            },
            {
                "id": "M01.L12.Q03",
                "section_id": "compute-isolation",
                "question": "What problem does Confidential Computing address?",
                "options": [
                    "Protecting data while it is in use/being processed",
                    "Only data at rest",
                    "Only public DNS",
                    "Only user passwords",
                ],
                "correct": 0,
                "explanation": "TEEs protect data in memory during computation.",
            },
            {
                "id": "M01.L12.Q04",
                "section_id": "egress-filtering",
                "question": "Why is egress filtering important for agents?",
                "options": [
                    "It restricts where a compromised or misbehaving agent can send data",
                    "It makes models smarter",
                    "It replaces authentication",
                    "It allows all outbound traffic",
                ],
                "correct": 0,
                "explanation": "Outbound least privilege reduces exfiltration risk.",
            },
            {
                "id": "M01.L12.Q05",
                "section_id": "vector-hygiene",
                "question": "How should vector stores be treated?",
                "options": [
                    "As sensitive data stores requiring normal security controls",
                    "As inherently anonymous and harmless",
                    "As public caches",
                    "As logs that never need deletion",
                ],
                "correct": 0,
                "explanation": "Embeddings can still carry sensitive information.",
            },
            {
                "id": "M01.L12.Q06",
                "section_id": "prompt-injection",
                "question": "What is prompt injection?",
                "options": [
                    "Untrusted content attempting to override intended model/application instructions",
                    "A network packet attack only",
                    "A hardware failure",
                    "A type of encryption",
                ],
                "correct": 0,
                "explanation": "Prompt injection targets semantic control of the model.",
            },
            {
                "id": "M01.L12.Q07",
                "section_id": "output-guardrails",
                "question": "Why inspect model output after generation?",
                "options": [
                    "The approved model can still produce unsafe, toxic, or sensitive content",
                    "The model output is always safe",
                    "Only tool outputs can fail",
                    "Output checks are only for formatting",
                ],
                "correct": 0,
                "explanation": "External enforcement should not assume perfect model behavior.",
            },
            {
                "id": "M01.L12.Q08",
                "section_id": "indirect-injection",
                "question": "Where can indirect prompt injection come from?",
                "options": [
                    "Retrieved webpages, documents, or tool/context data",
                    "Only the user keyboard",
                    "Only network routers",
                    "Only OAuth servers",
                ],
                "correct": 0,
                "explanation": "RAG/tool data must be treated as untrusted content.",
            },
            {
                "id": "M01.L12.Q09",
                "section_id": "schema-validation",
                "question": "Why validate tool schemas before execution?",
                "options": [
                    "Model-generated arguments may be malformed or hallucinated",
                    "JSON parsing guarantees authorization",
                    "Schemas replace least privilege",
                    "Validation is only for frontend UI",
                ],
                "correct": 0,
                "explanation": "Type/schema validation is one control before a real action.",
            },
            {
                "id": "M01.L12.Q10",
                "section_id": "iam",
                "question": "What is the difference between Authentication and Authorization?",
                "options": [
                    "Authentication verifies identity; Authorization verifies permissions",
                    "They are identical",
                    "Authentication is for tools only",
                    "Authorization proves identity only",
                ],
                "correct": 0,
                "explanation": "Who you are and what you can do are separate questions.",
            },
            {
                "id": "M01.L12.Q11",
                "section_id": "jwt",
                "question": "Why are short-lived scoped tokens preferred over broad long-lived credentials?",
                "options": [
                    "They limit both permissions and exposure time if stolen",
                    "They never expire",
                    "They always have admin rights",
                    "They can safely be published",
                ],
                "correct": 0,
                "explanation": "Scope and expiration are key security properties.",
            },
            {
                "id": "M01.L12.Q12",
                "section_id": "three-legged",
                "question": "When is 3-legged OAuth appropriate?",
                "options": [
                    "When an agent acts on behalf of a human user with explicit consent",
                    "Only for machine-to-machine calls",
                    "Only for network encryption",
                    "Only for anonymous users",
                ],
                "correct": 0,
                "explanation": "The user participates in authentication and consent.",
            },
            {
                "id": "M01.L12.Q13",
                "section_id": "two-legged",
                "question": "What identity does 2-legged OAuth primarily establish?",
                "options": [
                    "The client/agent service identity",
                    "A delegated human identity",
                    "A browser session only",
                    "A database row identity",
                ],
                "correct": 0,
                "explanation": "Client Credentials represents the non-human client.",
            },
            {
                "id": "M01.L12.Q14",
                "section_id": "otel",
                "question": "Why is distributed tracing important in a multi-agent system?",
                "options": [
                    "One request may cross many services, and one trace ID reconstructs the full path",
                    "It replaces authentication",
                    "It only counts tokens",
                    "It prevents all latency",
                ],
                "correct": 0,
                "explanation": "Per-service logs alone cannot show the end-to-end chain.",
            },
            {
                "id": "M01.L12.Q15",
                "section_id": "safe-audit",
                "question": "What is a key risk of detailed agent logging?",
                "options": [
                    "Logs may capture PII, tokens, passwords, or sensitive context",
                    "Logs cannot store text",
                    "Logs make tracing impossible",
                    "Logs always reduce latency",
                ],
                "correct": 0,
                "explanation": "Observability must include redaction.",
            },
            {
                "id": "M01.L12.Q16",
                "section_id": "shadow-ai",
                "question": "What is Shadow AI?",
                "options": [
                    "Unsanctioned use of AI tools outside approved governance",
                    "An agent with dark UI mode",
                    "A hidden sub-agent",
                    "A backup model",
                ],
                "correct": 0,
                "explanation": "Shadow AI creates governance and data-leak risks.",
            },
            {
                "id": "M01.L12.Q17",
                "section_id": "callbacks",
                "question": "Which callback is the best place to validate tool authorization and arguments?",
                "options": [
                    "Before Tool Call",
                    "After Agent Call only",
                    "Before Agent Call only",
                    "After Tool Call only",
                ],
                "correct": 0,
                "explanation": "The source places authorization and schema validation before execution.",
            },
            {
                "id": "M01.L12.Q18",
                "section_id": "privacy-gap",
                "question": "What is the privacy weakness of transcript-based live guardrails when transcription comes from the main model?",
                "options": [
                    "The main model must receive the sensitive audio before the guardrail can inspect its transcript",
                    "Audio cannot be transcribed",
                    "Output cannot be blocked",
                    "The user cannot speak",
                ],
                "correct": 0,
                "explanation": "Detection happens after model exposure.",
            },
            {
                "id": "M01.L12.Q19",
                "section_id": "privacy-buffer",
                "question": "How does the Privacy Buffer improve safety?",
                "options": [
                    "It temporarily holds incoming audio while local transcription and safety checks occur before model release",
                    "It stores all user audio forever",
                    "It disables guardrails",
                    "It only filters output",
                ],
                "correct": 0,
                "explanation": "The model receives only input that passed proactive screening.",
            },
            {
                "id": "M01.L12.Q20",
                "section_id": "parallel-guardrails",
                "question": "Why analyze raw audio/video in parallel?",
                "options": [
                    "To detect non-verbal and visual threats that text transcripts may miss",
                    "To increase prompt length",
                    "To avoid all input checks",
                    "To remove the reasoning model",
                ],
                "correct": 0,
                "explanation": "Tone, sounds, gestures, and visual content can be lost in transcription.",
            },
            {
                "id": "M01.L12.Q21",
                "section_id": "identity-gap",
                "question": "What is the Identity Gap?",
                "options": [
                    "Downstream agents may know which service called but lose the human user's permission context",
                    "The model has no name",
                    "The browser has no IP address",
                    "The user has two passwords",
                ],
                "correct": 0,
                "explanation": "Multi-hop systems need both service and user identity.",
            },
            {
                "id": "M01.L12.Q22",
                "section_id": "obo",
                "question": "What does an On-Behalf-Of flow accomplish?",
                "options": [
                    "Obtains a downstream token constrained for a service while preserving the user's delegated identity",
                    "Creates one global admin token",
                    "Removes the user from authorization",
                    "Stores passwords in every agent",
                ],
                "correct": 0,
                "explanation": "OBO chains user authorization across service boundaries.",
            },
            {
                "id": "M01.L12.Q23",
                "section_id": "custom-vault-risk",
                "question": "What is the main risk of a custom centralized token vault?",
                "options": [
                    "It becomes a high-value concentration point for many refresh tokens and identities",
                    "It cannot store tokens",
                    "It removes governance",
                    "It always reduces security complexity to zero",
                ],
                "correct": 0,
                "explanation": "Credential centralization without mature identity infrastructure can create catastrophic blast radius.",
            },
            {
                "id": "M01.L12.Q24",
                "section_id": "incremental-auth",
                "question": "What is incremental authorization in the source's multi-provider example?",
                "options": [
                    "Ask the user to connect a new provider only when the workflow actually needs it",
                    "Request every permission at signup",
                    "Never request consent",
                    "Use one provider token for all providers",
                ],
                "correct": 0,
                "explanation": "Just-in-time authorization avoids unnecessary up-front permissions.",
            },
            {
                "id": "M01.L12.Q25",
                "section_id": "secretless-flow",
                "question": "What makes the source's agent identity workflow 'secretless'?",
                "options": [
                    "Long-lived client secrets remain in the central authority rather than inside agent source/config",
                    "No credentials exist anywhere",
                    "Tokens never expire",
                    "Agents are anonymous",
                ],
                "correct": 0,
                "explanation": "Agents receive short-lived tokens after proving workload identity.",
            },
            {
                "id": "M01.L12.Q26",
                "section_id": "mtls-process",
                "question": "What does mTLS add beyond ordinary TLS?",
                "options": [
                    "The client/workload also presents and proves its identity",
                    "It disables encryption",
                    "Only the client is authenticated",
                    "It removes certificates",
                ],
                "correct": 0,
                "explanation": "Both sides authenticate during mutual TLS.",
            },
            {
                "id": "M01.L12.Q27",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design a secure live multi-agent university platform. Cover all eight defense layers, "
                    "network and data controls, prompt/tool security, OAuth, user and agent identity, observability, "
                    "GRC, text callbacks, Model Gateway, Privacy Buffer, parallel multimodal Guardrail Agent, "
                    "OBO/Token Exchange, incremental authorization, secretless agents, and mTLS bootstrap."
                ),
            },
        ],
        "passing_score": 70,
    },
}
