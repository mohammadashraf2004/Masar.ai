"""M01.L09 — Securing AI Services Against Misuse and Abuse.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 9, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L09"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Protect production GenAI services against misuse, adversarial inputs, unsafe outputs, "
    "resource exhaustion, and traffic spikes by combining guardrails, evaluation, moderation, "
    "rate limiting, WebSocket controls, stream throttling, and traffic-shaping concepts."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Securing AI Services Against Misuse and Abuse",

    "slug": "generative-ai-services-m01-l09",

    "description": (
        "Learn how GenAI systems can be misused, how input and output guardrails work, "
        "how to design evaluator-based moderation with explicit thresholds, and how to "
        "protect FastAPI services with request quotas, user-based limits, Redis-backed "
        "distributed counters, WebSocket limits, stream throttling, and traffic shaping."
    ),

    "order": 9,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "genai-security",
        "guardrails",
        "prompt-injection",
        "content-moderation",
        "llm-evaluation",
        "rate-limiting",
        "throttling",
        "fastapi",
        "websocket-security",
        "redis",
        "traffic-shaping",
        "abuse-prevention",
    ],

    "prerequisite_ids": [
        "M01.L08",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Securing AI Services Against Misuse and Abuse",

        "content": """
# Securing AI Services Against Misuse and Abuse

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L09  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 9 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why authenticated users can still misuse or abuse a GenAI service.
- Identify major misuse categories affecting text, image, audio, and video generators.
- Recognize the LLM vulnerability categories introduced in the source.
- Explain what guardrails are and where they sit in an AI request/response pipeline.
- Distinguish input guardrails from output guardrails.
- Design topical, prompt-injection, moderation, and attribute checks conceptually.
- Explain why secrets should not be placed inside model-visible prompts.
- Build a simple LLM-based topical classifier with a validated output contract.
- Run a guardrail and model call concurrently while preserving a fail-fast path.
- Explain the false-positive and false-negative trade-off in guardrail thresholds.
- Describe evaluator-based output moderation using explicit criteria, steps, and scores.
- Explain why guardrails remain probabilistic and imperfect.
- Distinguish rate limiting from throttling.
- Compare token-bucket, leaky-bucket, fixed-window, and sliding-window rate-limiting strategies.
- Apply global, endpoint, IP-based, and user-based rate limits conceptually.
- Explain why distributed FastAPI instances need centralized usage counters.
- Explain how WebSocket traffic can be rate-limited separately.
- Throttle real-time model streams without blocking the event loop.
- Explain how infrastructure-level traffic shaping differs from application-level throttling.
- Combine security controls into a layered defense rather than relying on one mechanism.

---

## 1. Authentication does not prevent misuse

Previous lessons added:

- authentication,
- authorization,
- databases,
- concurrency,
- streaming.

Those controls answer questions such as:

```text
Who is the user?
What resources may they access?
```

But a valid authenticated user can still misuse a GenAI system.

For example, a user may attempt to:

- generate deceptive content,
- abuse expensive generation endpoints,
- scrape large volumes of output,
- overload the service,
- manipulate model behavior,
- submit malicious external content.

So production security needs another layer:

> **Usage moderation and abuse protection.**

The source groups malicious use into broad categories such as:

- misinformation/disinformation,
- bias amplification/discrimination,
- malicious or toxic content generation,
- privacy attacks,
- automated cyberattacks,
- identity theft/social engineering,
- deepfakes/multimedia manipulation,
- scams and fraud.

The exact risk depends on the modality.

### Modality changes the risk profile

The source notes patterns such as:

```text
audio/video
→ strong impersonation risk

image/text
→ sockpuppeting, content farming, falsification

image/video
→ multimedia manipulation and hidden/encoded content
```

The engineering implication is:

> **Guardrails should be selected according to the capabilities and likely abuse modes of the system you are building.**

A text-only coding assistant and a public deepfake-generation service do not have the same abuse surface.

{{exercise:M01.L09.EX01}}

---

## 2. Security risks specific to GenAI systems

The chapter introduces a set of LLM security-risk categories based on the source's OWASP framing.

These include:

- prompt injection,
- insecure output handling,
- training-data poisoning,
- model denial of service,
- supply-chain vulnerabilities,
- sensitive-information leakage,
- insecure plug-in/integration design,
- excessive agency,
- overreliance on LLM output,
- model theft.

### Prompt injection

A malicious input attempts to manipulate model behavior.

The danger is larger when the model can access:

- secrets,
- tools,
- databases,
- external systems,
- privileged actions.

### Insecure output handling

Model output should not automatically be trusted.

For example:

```text
LLM output
→ downstream parser/tool
```

If the downstream system assumes the output is safe and valid, malformed output can create failures or security problems.

### Model denial of service

Attackers may try to consume excessive resources through:

- large inputs,
- repeated requests,
- expensive generations,
- many concurrent calls.

This connects directly to rate limiting later in the lesson.

### Sensitive-information leakage

The model or the surrounding application may accidentally expose:

- private data,
- proprietary information,
- internal configuration,
- confidential context.

### Excessive agency

A model connected to powerful tools may be allowed to do too much.

A secure architecture should keep privileged actions behind deterministic application controls.

### Overreliance

Even a well-protected model can generate incorrect output.

Applications should not treat probabilistic model output as guaranteed truth.

[[IMAGE_NEEDED: GenAI attack surface | A defensive architecture diagram showing user inputs, external documents, model, tools/plugins, downstream systems, and stored sensitive data, with risk markers at prompt injection, malicious external content, unsafe output handling, excessive tool permissions, and resource exhaustion | Learner should notice that GenAI security spans inputs, model behavior, outputs, integrations, and infrastructure]]

---

## 3. What guardrails are

The source describes guardrails as controls intended to guide the application toward acceptable behavior.

A useful simplified architecture is:

```text
User input
    ↓
Input guardrails
    ↓
Model
    ↓
Output guardrails
    ↓
User / downstream system
```

### Input guardrails

Check data **before** the model sees it.

Goals can include:

- block inappropriate requests,
- detect unsupported topics,
- reject malformed payloads,
- detect prompt-injection patterns,
- sanitize uploaded content.

### Output guardrails

Check model output **before** it reaches:

- the user,
- a tool,
- another system.

Goals can include:

- moderation,
- hallucination/fact checking,
- syntax validation,
- structured-output checks,
- tool-selection checks.

{{image:io-guardrails}}

### Guardrails are not perfect

The source explicitly warns that guardrails remain an active area of research.

A strong attack may bypass them.

A guardrail may also reject valid content.

Therefore guardrails are best understood as:

```text
risk-reduction controls
```

not:

```text
perfect mathematical security boundary
```

---

## 4. Input guardrails

The chapter groups several input-guardrail types.

### Topical guardrails

Restrict the application to intended subjects.

Example:

```text
allowed:
- API development
- FastAPI
- building GenAI systems

other topics:
- reject or redirect
```

This is useful when the system has a narrow domain.

### Direct prompt-injection checks

Try to detect inputs attempting to:

- override system instructions,
- extract hidden prompts,
- expose secrets/configuration,
- change the model's intended role.

### Indirect prompt injection

The hostile content may come from:

- uploaded files,
- remote web pages,
- images,
- transcripts,
- retrieved documents.

This is especially relevant to RAG systems.

A user may not type the malicious instruction directly.

Instead:

```text
uploaded/retrieved content
        ↓
model context
        ↓
malicious instruction influences model
```

### Moderation

Check for content categories that violate:

- policy,
- brand constraints,
- legal requirements,
- application boundaries.

The source gives examples including:

- profanity,
- explicit content,
- PII,
- self-harm,
- competitor-related restrictions.

### Attribute validation

These are deterministic checks such as:

- query length,
- file size,
- allowed choices,
- numeric ranges,
- data format,
- structure.

A useful principle is:

> **Use deterministic validation for deterministic rules. Do not ask an LLM to decide whether an integer is within a fixed range.**

---

## 5. Do not expose secrets to the model

The source makes an important point:

Even if you build prompt-injection guardrails, the safer architecture is to avoid placing secrets inside the model's reachable context.

Bad idea:

```text
system prompt contains:
DATABASE_PASSWORD=...
API_SECRET=...
private internal token=...
```

Then the application relies on:

```text
"Never reveal these secrets."
```

That makes the model part of the secret-protection boundary.

A stronger design is:

```text
application configuration
→ kept outside model context

model receives
→ only the minimum data needed
```

### Least exposure

Treat model context as potentially exposable.

If the model does not need a secret:

```text
do not send it
```

This is stronger than attempting to detect every prompt-injection attack.

---

## 6. Build an LLM-based topical evaluator

The chapter demonstrates a simple LLM auto-evaluator.

The evaluator's task is narrow:

```text
Input:
user query

Output:
allowed
or
disallowed
```

A simplified evaluator prompt can specify:

```text
Allowed topics:
- API development
- FastAPI
- building GenAI systems

Return only:
allowed
or
disallowed
```

### Why constrain the evaluator output?

The evaluator is still an LLM.

It might produce:

```text
"Yes, this looks allowed."
```

even when the application expects:

```text
allowed
```

So the source validates the classifier output.

Conceptually:

```python
def validate_classification(
    value: str | None,
) -> str:
    if value not in {
        "allowed",
        "disallowed",
    }:
        raise ValueError(
            "Invalid guardrail response"
        )

    return value
```

### Guardrail response schema

```python
class TopicalGuardResponse(BaseModel):
    classification: str
```

The pattern is valuable beyond topical checks:

```text
LLM evaluator
    ↓
strict output contract
    ↓
trusted application branch
```

Do not let arbitrary evaluator text directly drive control flow.

{{exercise:M01.L09.EX02}}

---

## 7. Run guardrails and generation concurrently

Calling several evaluator models sequentially can increase latency.

Suppose:

```text
topical check → 1.0 s
model answer  → 3.0 s
```

Sequential:

```text
1.0 + 3.0 = about 4.0 s
```

If the operations can safely begin together, the source demonstrates concurrency.

Conceptually:

```python
guard_task = asyncio.create_task(
    check_topic(user_query)
)

chat_task = asyncio.create_task(
    llm_client.invoke(user_query)
)
```

Then wait for completion events.

### Fail fast

If the guardrail finishes first and rejects the request:

```text
guardrail → disallowed
        ↓
cancel chat task
        ↓
return safe fixed response
```

This avoids continuing expensive work unnecessarily.

### Important caution

Parallel execution may mean the model generation begins before the guardrail decision is final.

Therefore:

- do not release generated content before the input check permits it,
- cancellation should be handled correctly,
- provider API calls still incur capacity/cost,
- additional evaluator calls can hit provider rate limits.

### Async guardrails trade latency for request volume

Running checks concurrently can reduce visible latency.

But it may increase:

- simultaneous provider calls,
- cost,
- rate-limit pressure.

The chapter therefore frames guardrail design as an **accuracy + latency + cost** trade-off.

{{exercise:M01.L09.EX03}}

---

## 8. Guardrails are probabilistic controls

An LLM-based evaluator can be wrong.

### False positive

Guardrail says:

```text
unsafe
```

but the request/output was actually acceptable.

Effect:

- valid users are blocked,
- user experience worsens.

### False negative

Guardrail says:

```text
safe
```

but the content should have been blocked.

Effect:

- harmful/invalid output passes,
- abuse continues,
- reputation or cost risk increases.

### Combine mechanisms

The source recommends considering combinations such as:

```text
LLM evaluator
+
rules-based checks
+
traditional ML detection
```

Different techniques can catch different errors.

### Recent-message scope

The chapter also notes that some guardrails may consider only the latest message to reduce confusion from very long conversation histories.

The correct design depends on the threat model.

---

## 9. Output guardrails

Output guardrails evaluate what the model generated before it is delivered or acted upon.

### Hallucination / factual checks

Possible strategies include evaluating:

- relevancy,
- coherence,
- consistency,
- fluency,
- alignment with known source material.

In a RAG application, the output can be compared with trusted context.

### Moderation

Check generated content against:

- product rules,
- brand requirements,
- toxicity limits,
- sentiment constraints,
- mention policies.

### Syntax checks

Structured outputs should be validated.

Examples:

```text
expected JSON
→ validate schema

function call
→ validate function name + arguments

agent tool selection
→ verify tool is permitted
```

This is especially important because downstream systems may treat structured model output as executable instructions.

### Retry or fail safely

If the output is invalid, the application may:

- reject it,
- return a canned response,
- regenerate,
- repair/reformat,
- ask for clarification.

The correct response depends on the risk.

---

## 10. Choose guardrail thresholds deliberately

Many guardrails output a score.

For example:

```text
toxicity score
hallucination score
quality score
moderation severity
```

The application then chooses a threshold.

Suppose:

```text
score >= 3
→ flag output
```

### Lower threshold

More aggressive blocking.

Likely effect:

```text
more true detections
+
more false positives
```

### Higher threshold

More permissive.

Likely effect:

```text
fewer false positives
+
more false negatives
```

[[IMAGE_NEEDED: Guardrail threshold trade-off | A horizontal score scale from low to high with a movable threshold; mark false-positive region on one side and false-negative risk on the other | Learner should notice that threshold selection trades user friction against safety/abuse risk]]

### Threshold selection is application-specific

A low-risk writing assistant can tolerate a different balance than:

- a medical workflow,
- a financial action system,
- a public image-generation service.

The chapter emphasizes assessing:

- worst-case harm,
- user experience,
- reputation,
- cost.

---

## 11. Build an evaluator-based moderation guardrail

The source demonstrates a G-Eval-style evaluation prompt.

The evaluator defines:

1. **Domain**  
   What kind of content is being evaluated?

2. **Criteria**  
   What counts as valid or invalid?

3. **Steps**  
   How should the evaluator reason about the criteria?

4. **Score**  
   Return a discrete value.

Example conceptual scale:

```text
1 → acceptable
2 → mostly acceptable
3 → borderline
4 → problematic
5 → strongly violates criteria
```

### Validate the score

A Pydantic schema can enforce:

```text
1 <= score <= 5
```

Do not trust the evaluator to always return a valid number.

### Apply threshold

```python
flagged = score >= threshold
```

Then:

```text
flagged
→ return safe response

not flagged
→ deliver model output
```

### Other evaluation methods

The source also mentions traditional evaluation approaches such as:

- ROUGE,
- BERTScore,
- SummEval.

The larger lesson is:

> **Guardrail evaluation can be model-based, rule-based, metric-based, or a combination.**

{{exercise:M01.L09.EX04}}

---

## 12. Keep the guardrail stack practical

More guardrails are not automatically better.

Each check can add:

- latency,
- provider cost,
- infrastructure usage,
- implementation complexity.

The source proposes several optimization ideas.

### Fast failure

Exit as soon as a decisive guardrail fails.

```text
input invalid
→ stop
→ do not run expensive later checks
```

### Select only relevant guardrails

Do not run every possible detector on every request.

Choose controls based on the application's risks.

### Run compatible checks concurrently

Independent asynchronous checks can overlap.

### Sampling

Very expensive checks might be run on only a sample of requests when acceptable for the use case.

The key design question is:

```text
Which controls are mandatory on every request?
Which can be sampled?
Which can be run asynchronously?
Which can fail fast?
```

---

## 13. Rate limiting versus throttling

Guardrails mainly moderate **content and behavior**.

Another problem is resource abuse.

The chapter introduces two related controls.

### Rate limiting

Controls how much traffic is accepted over a period.

Example:

```text
5 requests per minute
```

When the quota is exceeded:

```text
reject request
```

Typical HTTP response:

```text
429 Too Many Requests
```

### Throttling

Temporarily slows request or data processing to stabilize the system.

Instead of rejecting immediately:

```text
reduce throughput
```

### Why GenAI needs both

Generation endpoints can be expensive.

Without controls, one client can monopolize:

- provider quota,
- GPU time,
- CPU,
- memory,
- bandwidth.

### Goals

The source highlights:

- abuse prevention,
- fair usage,
- server stability,
- protection against scraping,
- protection against brute-force/high-volume attacks.

[[IMAGE_NEEDED: Rate limiting versus throttling | Side-by-side diagram where rate limiting rejects requests after a quota is reached, while throttling lets traffic continue but slows processing/transmission | Learner should notice that rate limiting controls admission while throttling controls pace]]

{{exercise:M01.L09.EX05}}

---

## 14. Four rate-limiting strategies

The chapter compares four strategies.

### Token bucket

Imagine a bucket filled with tokens at a steady rate.

```text
incoming request
→ consumes token

tokens available
→ accept

no token
→ reject
```

Strength:

- handles bursts better than simple fixed quotas.

Trade-off:

- more implementation complexity.

### Leaky bucket

Incoming requests enter a queue.

The queue drains at a constant rate.

```text
bursty input
      ↓
queue
      ↓
steady output
```

If the queue is full:

```text
reject new request
```

Good when consistent traffic flow matters.

### Fixed window

Example:

```text
100 requests per minute
```

At minute boundaries, the counter resets.

Simple, but bursty traffic around the boundary can be awkward.

### Sliding window

Tracks requests over a rolling interval.

Example:

```text
number of requests in the last 60 seconds
```

This gives smoother enforcement but requires more state.

{{image:rate-limit-strategies}}

### Source-oriented use cases

The chapter frames the choices roughly as:

```text
token bucket
→ irregular interactive traffic

leaky bucket
→ steady inference throughput

fixed window
→ simple strict quotas/free tier

sliding window
→ flexible conversational/premium access
```

{{exercise:M01.L09.EX06}}

---

## 15. Apply rate limits in FastAPI

The source demonstrates a FastAPI rate-limiting library.

The exact library is less important than the architecture.

### Global limits

Example conceptual policy:

```text
200/day
60/hour
2 requests per 5 seconds
```

The limiter tracks usage and rejects excess traffic.

### Custom 429 response

A good rate-limit response can include:

```json
{
  "detail": "Rate limit exceeded.",
  "retry_after_seconds": 30
}
```

and:

```text
Retry-After: 30
```

This tells clients when they can try again.

### Endpoint-specific limits

Different GenAI operations have different costs.

For example:

```text
text generation
→ 5/minute

image generation
→ 1/minute
```

That is better than assuming every request consumes equal resources.

### Health endpoint exemption

The chapter recommends not rate-limiting a health endpoint.

Why?

Infrastructure such as:

- orchestrators,
- load balancers,
- monitoring systems

may check it frequently.

### Load testing

After adding rate limits, test them.

Expected behavior:

```text
200
200
200
429
429
...
```

A policy is only useful if the application actually enforces it.

---

## 16. Prefer user-aware quotas when identity exists

IP-based rate limits are useful but imperfect.

A user may change IP through:

- VPN,
- proxy,
- mobile network,
- rotating addresses.

At the same time, multiple legitimate users may share one IP.

Once authentication exists, usage can also be keyed by user identity.

Example:

```text
user 123
→ 10 requests/minute
```

This supports account-level quotas.

### Combine keys

Production systems may use a combination of:

- user ID,
- IP,
- subscription plan,
- API key,
- endpoint cost.

Example:

```text
FREE
→ 5 text requests/minute

PRO
→ 30 text requests/minute
```

The source focuses on IP and user-based limits, but the deeper idea is:

> **Choose a quota identity that reflects who or what is consuming the scarce resource.**

---

## 17. Rate limiting across several application instances

Suppose production runs:

```text
FastAPI instance A
FastAPI instance B
FastAPI instance C
```

A load balancer distributes requests.

If every instance keeps counters only in local memory:

```text
A thinks user used 3 requests
B thinks user used 4 requests
C thinks user used 2 requests
```

The true usage is:

```text
9 requests
```

but no single instance knows that.

### Centralized counter store

The chapter uses Redis.

Architecture:

```text
                ┌──────────────┐
request ───────→│ FastAPI A    │─┐
                └──────────────┘ │
                                 │
                ┌──────────────┐ │
request ───────→│ FastAPI B    │─┼→ Redis counters
                └──────────────┘ │
                                 │
                ┌──────────────┐ │
request ───────→│ FastAPI C    │─┘
                └──────────────┘
```

Now all instances share one view of quota usage.

[[IMAGE_NEEDED: Distributed rate limiting with Redis | Load balancer distributing requests to three FastAPI instances, all reading/writing the same Redis rate-limit counters | Learner should notice why per-process memory cannot enforce one global quota across replicas]]

### Infrastructure-layer alternative

The source also notes that rate limiting can be placed at:

- load balancer,
- reverse proxy,
- API gateway.

This can be attractive when customized application logic is not required.

---

## 18. Limit WebSocket usage separately

WebSocket connections differ from ordinary HTTP requests.

They may remain open for a long time.

The source therefore introduces WebSocket-specific limiting.

Possible controls include:

- active connection count,
- messages per interval,
- per-user usage,
- streamed data rate.

### User-based WebSocket limiter

Conceptually:

```text
user opens socket
    ↓
authenticate user
    ↓
track user ID
    ↓
each prompt/message
    ↓
rate-limit check
```

If the limit is exceeded:

```text
send "try again later"
```

then enforce the desired connection policy.

### Why this matters

Without limits, one user could keep many connections open or send prompts too quickly.

That consumes:

- server connection state,
- model capacity,
- bandwidth.

---

## 19. Throttle real-time model streams

A model may produce chunks faster than a client or the service can comfortably deliver them.

The source demonstrates adding a nonblocking delay:

```python
async for chunk in stream:
    await asyncio.sleep(throttle_rate)
    yield chunk
```

### Why `await asyncio.sleep(...)`?

It slows the producer without blocking the event loop.

This means other async requests can continue making progress.

### Possible benefits

Throttling can help:

- slow data transmission,
- reduce network pressure,
- stabilize resource use,
- give clients time to consume data,
- spread capacity across several clients.

### Dynamic throttling

A fixed throttle is simple.

A more advanced service might adjust the rate based on:

- server load,
- active streams,
- subscription level,
- network conditions.

The source introduces the concept rather than a full adaptive implementation.

{{exercise:M01.L09.EX07}}

---

## 20. Traffic shaping at the infrastructure layer

Application throttling is not the only way to control flow.

The chapter introduces **traffic shaping**.

Traffic shaping manages network transmission.

Possible controls include:

- bandwidth limits,
- intentional latency,
- packet-loss simulation/control,
- IP-based traffic limits,
- queueing/prioritization.

### Why use it?

Useful for real-time services such as:

- chat streaming,
- video streaming,
- other bandwidth-sensitive AI applications.

### Application throttle versus traffic shaping

```text
Application throttling
→ code intentionally slows model/response production

Traffic shaping
→ infrastructure/network layer controls data transmission
```

### Trade-off

Traffic shaping can improve stability but also introduces:

- configuration complexity,
- monitoring requirements,
- queueing delay.

Use it when network behavior itself needs control.

---

## 21. Build layered abuse protection

The chapter's techniques work best together.

A practical request path can look like:

```text
Request
   ↓
Authentication
   ↓
Authorization
   ↓
Rate limit / quota
   ↓
Attribute validation
   ↓
Input guardrails
   ↓
Model / tool execution
   ↓
Output guardrails
   ↓
Stream throttle
   ↓
User
```

### Each layer solves a different problem

| Control | Main question |
|---|---|
| Authentication | Who are you? |
| Authorization | Are you allowed to do this? |
| Rate limit | How much may you use? |
| Input guardrail | Is this input acceptable/safe for this application? |
| Model/tool policy | What capabilities may execute? |
| Output guardrail | Is generated output acceptable/valid? |
| Throttle | How fast should output flow? |
| Traffic shaping | How should network capacity be allocated? |

### Fail early where possible

Cheap deterministic checks should happen before expensive inference.

Example:

```text
invalid payload
→ reject immediately

quota exceeded
→ reject immediately

clearly disallowed request
→ stop before model generation
```

### Do not rely on one control

A robust system assumes:

```text
individual controls can fail
```

Layering reduces the chance that one missed detection becomes a complete security failure.

{{exercise:M01.L09.EX08}}

---

## Important misconceptions

### Misconception 1

> If users are authenticated, they cannot abuse the AI service.

### Why this is wrong

Authentication identifies users. Authenticated users can still misuse capabilities or consume excessive resources.

### Misconception 2

> Guardrails guarantee that prompt injection cannot succeed.

### Why this is wrong

The source explicitly treats guardrails as imperfect and probabilistic. Sophisticated attacks can bypass them.

### Misconception 3

> A model-based guardrail output can be trusted without validation.

### Why this is wrong

The evaluator is also a probabilistic model and may return an unexpected format or incorrect result.

### Misconception 4

> The safest way to protect secrets is to put them in the system prompt and tell the model never to reveal them.

### Why this is wrong

The stronger architecture is to keep secrets out of model-visible context whenever possible.

### Misconception 5

> More guardrails always make the application safer with no downside.

### Why this is wrong

Guardrails increase latency, provider usage, cost, and the chance of false positives.

### Misconception 6

> A false positive and false negative have the same consequence.

### Why this is wrong

False positives block valid users, while false negatives allow content or behavior the system intended to stop.

### Misconception 7

> Rate limiting and throttling are identical.

### Why this is wrong

Rate limiting controls admission/allowed usage; throttling slows processing or transmission.

### Misconception 8

> One fixed request limit should be used for every AI endpoint.

### Why this is wrong

Different endpoints may have dramatically different resource costs.

### Misconception 9

> Per-IP limiting fully prevents one user from bypassing quotas.

### Why this is wrong

Users can change IP addresses, and multiple users may share an IP. Authenticated user quotas can provide stronger identity-level control.

### Misconception 10

> In-memory rate-limit counters work correctly across multiple FastAPI replicas.

### Why this is wrong

Each process has separate memory. A centralized counter store or infrastructure-layer limit is needed for a shared quota.

### Misconception 11

> HTTP rate limiting automatically protects long-lived WebSocket usage.

### Why this is wrong

WebSocket traffic needs connection/message/data-rate controls appropriate to persistent connections.

### Misconception 12

> Stream throttling blocks the whole FastAPI event loop.

### Why this is wrong

Using nonblocking `await asyncio.sleep(...)` allows the event loop to schedule other work during the delay.

### Misconception 13

> Traffic shaping and model-stream throttling operate at the same layer.

### Why this is wrong

Stream throttling occurs in application logic; traffic shaping operates at the network/infrastructure layer.

---

## Key terminology

| Term | Meaning |
|---|---|
| Misuse | Use of a system in an unintended or harmful way |
| Abuse protection | Controls designed to reduce malicious or excessive use |
| Prompt injection | Input crafted to manipulate model instructions or behavior |
| Indirect prompt injection | Malicious instructions entering through external content such as files or retrieved data |
| Insecure output handling | Trusting model output without validation before downstream use |
| Model denial of service | Resource-exhaustion attack targeting expensive model operations |
| Guardrail | Control that evaluates or constrains model inputs/outputs |
| Input guardrail | Check applied before content reaches the model |
| Output guardrail | Check applied to generated content before delivery/use |
| Topical guardrail | Restricts requests to allowed subject areas |
| Moderation guardrail | Evaluates content against policy/quality criteria |
| Auto-evaluator | Model or automated mechanism that grades another input/output |
| False positive | Valid content incorrectly flagged as invalid |
| False negative | Invalid content incorrectly allowed |
| Threshold | Score boundary used to turn a continuous/discrete metric into a decision |
| Fast failure | Ending processing as soon as a decisive failure is detected |
| Sampling | Running an expensive check on only a subset of requests |
| Rate limiting | Controlling how many requests/operations are accepted over time |
| Throttling | Slowing processing or data transmission |
| Token bucket | Rate limiter using refillable tokens consumed by requests |
| Leaky bucket | Queue-based limiter that emits work at a steady rate |
| Fixed window | Rate limiter counting requests in fixed time intervals |
| Sliding window | Rate limiter counting requests over a moving interval |
| HTTP 429 | Too Many Requests response |
| `Retry-After` | Header indicating when a client may retry |
| User-based quota | Limit keyed to authenticated user identity |
| Redis | Centralized in-memory data store used in the source for shared rate-limit state |
| WebSocket rate limit | Limit applied to persistent connection messages/usage |
| Stream throttle | Intentional delay/rate control applied to generated chunks |
| Traffic shaping | Network-level control over bandwidth, delay, and packet flow |

---

## Self-check

Before continuing, make sure you can answer:

1. Why does authentication not eliminate GenAI misuse?
2. What broad malicious-use categories does the chapter discuss?
3. Why does model modality affect security design?
4. What is prompt injection?
5. What is indirect prompt injection?
6. What is insecure output handling?
7. What is model denial of service?
8. Why is excessive model/tool agency dangerous?
9. What is an input guardrail?
10. What is an output guardrail?
11. Why should secrets stay outside model-visible prompts?
12. What does a topical guardrail do?
13. Why validate the output of an LLM evaluator?
14. What is the benefit of running a guardrail concurrently with model generation?
15. What must happen if the guardrail rejects the request before output is released?
16. Why can concurrent guardrails increase provider rate-limit pressure?
17. What is a false positive?
18. What is a false negative?
19. Why might rules-based checks be combined with model-based guardrails?
20. What can an output guardrail validate?
21. Why validate JSON/function parameters generated by an LLM?
22. What does a guardrail threshold control?
23. How does moving the threshold affect false-positive and false-negative rates?
24. What are the domain, criteria, steps, and score in the source's evaluator pattern?
25. Why constrain evaluator scores with Pydantic?
26. What is fast failure?
27. Why should an application select only relevant guardrails?
28. When might guardrail sampling be useful?
29. What is rate limiting?
30. What is throttling?
31. Why are they valuable for GenAI services?
32. How does a token bucket work?
33. How does a leaky bucket work?
34. What is a fixed-window limit?
35. What is a sliding-window limit?
36. Which strategy handles rolling burst behavior more smoothly?
37. What does HTTP 429 represent?
38. Why return `Retry-After`?
39. Why might image-generation limits be stricter than text-generation limits?
40. Why should health endpoints often be exempt?
41. Why load-test a limiter?
42. Why is per-IP rate limiting incomplete?
43. What advantage does authenticated user-based limiting provide?
44. Why do multiple FastAPI replicas need centralized quota state?
45. What role does Redis play in the source?
46. Where else can rate limiting be applied besides inside FastAPI?
47. Why do WebSocket connections need separate usage controls?
48. What can be rate-limited on a WebSocket?
49. Why use a user ID as a WebSocket rate-limit key?
50. What is stream throttling?
51. Why use `asyncio.sleep` rather than a blocking sleep for throttling?
52. What does traffic shaping control?
53. How is traffic shaping different from application throttling?
54. Why can traffic shaping increase latency?
55. In what order should cheap checks and expensive inference generally occur?
56. Why is layered defense stronger than relying on one guardrail?

---

## Retain this idea

**Securing a GenAI service requires both content-level and resource-level controls: use validated input/output guardrails to reduce unsafe behavior, but treat them as probabilistic defenses rather than perfect security boundaries; enforce deterministic quotas and permissions in trusted code, centralize usage state when scaling, and use throttling or traffic shaping when protecting real-time capacity.**
""",

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "misuse-and-abuse", "title": "Authentication does not prevent misuse", "order": 1},
            {"id": "llm-security-risks", "title": "Security risks specific to GenAI systems", "order": 2},
            {"id": "guardrails", "title": "What guardrails are", "order": 3},
            {"id": "input-guardrails", "title": "Input guardrails", "order": 4},
            {"id": "secrets-boundary", "title": "Do not expose secrets to the model", "order": 5},
            {"id": "topical-guardrail", "title": "Build an LLM-based topical evaluator", "order": 6},
            {"id": "parallel-guardrails", "title": "Run guardrails and generation concurrently", "order": 7},
            {"id": "guardrail-limitations", "title": "Guardrails are probabilistic controls", "order": 8},
            {"id": "output-guardrails", "title": "Output guardrails", "order": 9},
            {"id": "guardrail-thresholds", "title": "Choose guardrail thresholds deliberately", "order": 10},
            {"id": "g-eval-moderation", "title": "Build an evaluator-based moderation guardrail", "order": 11},
            {"id": "guardrail-performance", "title": "Keep the guardrail stack practical", "order": 12},
            {"id": "rate-limiting-vs-throttling", "title": "Rate limiting versus throttling", "order": 13},
            {"id": "rate-limit-algorithms", "title": "Four rate-limiting strategies", "order": 14},
            {"id": "fastapi-rate-limit", "title": "Apply rate limits in FastAPI", "order": 15},
            {"id": "user-rate-limit", "title": "Prefer user-aware quotas when identity exists", "order": 16},
            {"id": "distributed-rate-limit", "title": "Rate limiting across several application instances", "order": 17},
            {"id": "websocket-limits", "title": "Limit WebSocket usage separately", "order": 18},
            {"id": "stream-throttling", "title": "Throttle real-time model streams", "order": 19},
            {"id": "traffic-shaping", "title": "Traffic shaping at the infrastructure layer", "order": 20},
            {"id": "layered-abuse-protection", "title": "Build layered abuse protection", "order": 21},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L09.EX01",
            "title": "Map Abuse Risks to Model Modalities",
            "lesson_code": "M01.L09",
            "section_id": "misuse-and-abuse",
            "placement": "after_section",
            "description": (
                "Identify which misuse categories deserve extra attention for different generative modalities."
            ),
            "instructions": (
                "Create a table for these products:\n"
                "1. text chatbot,\n"
                "2. image generator,\n"
                "3. voice-cloning/audio generator,\n"
                "4. video generator.\n\n"
                "For each, select at least two abuse categories discussed in the lesson "
                "and propose one defensive control category such as moderation, identity checks, "
                "rate limits, content restrictions, or output review.\n\n"
                "Do not design offensive techniques; focus only on risk recognition and defense."
            ),
            "expected_output": (
                "A four-row modality-risk-defense table."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "threat-modeling",
                "abuse-prevention",
                "modality-risk",
            ],
        },
        {
            "id": "M01.L09.EX02",
            "title": "Create a Strict Topical Guardrail Contract",
            "lesson_code": "M01.L09",
            "section_id": "topical-guardrail",
            "placement": "after_section",
            "description": (
                "Design a narrow LLM evaluator whose output is safe for application control flow."
            ),
            "instructions": (
                "Build a topical evaluator for a FastAPI learning assistant.\n\n"
                "Requirements:\n"
                "1. Allowed topics: FastAPI, API design, and GenAI service engineering.\n"
                "2. Evaluator must return exactly `allowed` or `disallowed`.\n"
                "3. Add a Pydantic or validator rule that rejects every other evaluator output.\n"
                "4. Show one allowed user query and one disallowed query.\n"
                "5. Explain why free-form evaluator text should not directly drive application logic."
            ),
            "expected_output": (
                "A topical evaluator prompt, strict response contract, and two test cases."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "input-guardrails",
                "llm-evaluation",
                "output-validation",
            ],
        },
        {
            "id": "M01.L09.EX03",
            "title": "Design a Concurrent Guardrail Flow",
            "lesson_code": "M01.L09",
            "section_id": "parallel-guardrails",
            "placement": "after_section",
            "description": (
                "Reduce guardrail latency while keeping the fail-fast decision explicit."
            ),
            "instructions": (
                "Design async pseudocode that starts:\n"
                "- a topical guardrail task,\n"
                "- a model-generation task.\n\n"
                "Your flow must:\n"
                "1. wait for task completion events,\n"
                "2. cancel generation if the guardrail returns `disallowed`,\n"
                "3. never release model output before the input decision permits it,\n"
                "4. return the model result if the request passes,\n"
                "5. identify one provider-rate-limit downside of this approach."
            ),
            "expected_output": (
                "Concurrent guardrail/generation pseudocode with a short trade-off explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "asyncio",
                "guardrail-orchestration",
                "fail-fast",
            ],
        },
        {
            "id": "M01.L09.EX04",
            "title": "Choose a Moderation Threshold",
            "lesson_code": "M01.L09",
            "section_id": "g-eval-moderation",
            "placement": "after_section",
            "description": (
                "Reason about evaluator scores, thresholds, and false-positive/false-negative costs."
            ),
            "instructions": (
                "Assume an evaluator returns scores from 1 to 5 where higher means more problematic.\n\n"
                "You are comparing thresholds 2, 3, and 4.\n"
                "For each threshold:\n"
                "1. describe whether the policy is more strict or permissive,\n"
                "2. describe the likely change in false positives,\n"
                "3. describe the likely change in false negatives.\n\n"
                "Then choose one threshold for a low-risk internal writing assistant "
                "and one for a high-risk public generation endpoint, explaining the trade-off."
            ),
            "expected_output": (
                "A threshold comparison table and two justified threshold selections."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "guardrail-thresholds",
                "false-positives",
                "false-negatives",
            ],
        },
        {
            "id": "M01.L09.EX05",
            "title": "Rate Limit or Throttle?",
            "lesson_code": "M01.L09",
            "section_id": "rate-limiting-vs-throttling",
            "placement": "after_section",
            "description": (
                "Distinguish admission control from throughput control."
            ),
            "instructions": (
                "For each scenario, choose `rate limiting`, `throttling`, or `both`:\n\n"
                "1. A user sends 500 image requests in one minute.\n"
                "2. The server is healthy but a slow client cannot consume streamed tokens quickly.\n"
                "3. A free account should receive only 10 generations per hour.\n"
                "4. A real-time endpoint must smooth bandwidth across many connected users.\n"
                "5. A bot is scraping the API at high frequency.\n\n"
                "Explain each choice."
            ),
            "expected_output": (
                "Five classifications with concise reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "rate-limiting",
                "throttling",
                "resource-protection",
            ],
        },
        {
            "id": "M01.L09.EX06",
            "title": "Select a Rate-Limiting Algorithm",
            "lesson_code": "M01.L09",
            "section_id": "rate-limit-algorithms",
            "placement": "after_section",
            "description": (
                "Choose a quota algorithm based on traffic behavior."
            ),
            "instructions": (
                "Choose token bucket, leaky bucket, fixed window, or sliding window for:\n\n"
                "1. A conversational AI that should tolerate short bursts.\n"
                "2. A service that must drain inference requests at a steady rate.\n"
                "3. A simple free-tier quota of 100 generations per day.\n"
                "4. A premium chat plan that needs smoother enforcement over a rolling minute.\n\n"
                "For each, state one advantage and one limitation."
            ),
            "expected_output": (
                "Four algorithm selections with benefit/limitation reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "token-bucket",
                "leaky-bucket",
                "sliding-window",
                "fixed-window",
            ],
        },
        {
            "id": "M01.L09.EX07",
            "title": "Protect a Streaming WebSocket Endpoint",
            "lesson_code": "M01.L09",
            "section_id": "stream-throttling",
            "placement": "after_section",
            "description": (
                "Combine authenticated WebSocket rate limits with nonblocking stream throttling."
            ),
            "instructions": (
                "Design a WebSocket message flow where:\n"
                "1. the user is authenticated,\n"
                "2. usage is keyed by user ID,\n"
                "3. each new prompt passes a rate-limit check,\n"
                "4. excessive usage receives a clear rejection message,\n"
                "5. accepted model chunks are throttled with `await asyncio.sleep(...)`,\n"
                "6. disconnect cleanup always runs.\n\n"
                "Explain why the rate limit and stream throttle solve different problems."
            ),
            "expected_output": (
                "A WebSocket protection flow plus a rate-limit-versus-throttle explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "websocket-rate-limiting",
                "stream-throttling",
                "async-security",
            ],
        },
        {
            "id": "M01.L09.EX08",
            "title": "Design a Layered GenAI Abuse-Protection Pipeline",
            "lesson_code": "M01.L09",
            "section_id": "layered-abuse-protection",
            "placement": "after_section",
            "description": (
                "Combine the chapter's defenses in the correct order around an expensive GenAI endpoint."
            ),
            "instructions": (
                "Design the request flow for a paid image-generation API.\n\n"
                "Include:\n"
                "1. authentication,\n"
                "2. authorization/subscription check,\n"
                "3. user quota/rate limit,\n"
                "4. deterministic input constraints,\n"
                "5. input moderation/guardrail,\n"
                "6. model generation,\n"
                "7. output moderation,\n"
                "8. response delivery/throttling where relevant,\n"
                "9. logging/monitoring of blocked requests.\n\n"
                "Explain which checks should happen before expensive generation and why."
            ),
            "expected_output": (
                "A layered defensive pipeline with ordering rationale."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "defense-in-depth",
                "genai-security-architecture",
                "abuse-protection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L09.QZ01",

        "title": "Securing AI Services — Knowledge Check",

        "lesson_code": "M01.L09",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L09.Q01",
                "section_id": "misuse-and-abuse",
                "question": "Why is authentication alone insufficient to protect a GenAI service?",
                "options": [
                    "Authenticated users can still misuse capabilities or consume resources abusively",
                    "Authentication disables all model guardrails",
                    "Authenticated users cannot be rate limited",
                    "Authentication prevents database access",
                ],
                "correct": 0,
                "explanation": (
                    "Identity verification says who the actor is, not whether their usage is safe, appropriate, or within quota."
                ),
            },
            {
                "id": "M01.L09.Q02",
                "section_id": "llm-security-risks",
                "question": "What does insecure output handling mean?",
                "options": [
                    "Trusting model output without adequate validation before downstream use",
                    "Encrypting the output twice",
                    "Using only local models",
                    "Rejecting every model response",
                ],
                "correct": 0,
                "explanation": (
                    "Generated output should be validated before downstream systems treat it as trustworthy structured data or actions."
                ),
            },
            {
                "id": "M01.L09.Q03",
                "section_id": "guardrails",
                "question": "Where does an output guardrail sit?",
                "options": [
                    "After generation and before output reaches users or downstream systems",
                    "Before the request enters the network",
                    "Inside the database only",
                    "Only after the user logs out",
                ],
                "correct": 0,
                "explanation": (
                    "Output guardrails inspect model-generated content before delivery or downstream execution."
                ),
            },
            {
                "id": "M01.L09.Q04",
                "section_id": "secrets-boundary",
                "question": "What is the safer approach to protecting an API secret from prompt injection?",
                "options": [
                    "Keep the secret outside model-visible context whenever the model does not need it",
                    "Put it in the system prompt and ask the model not to reveal it",
                    "Encode it with Base64 inside the prompt",
                    "Repeat it several times so the model remembers it",
                ],
                "correct": 0,
                "explanation": (
                    "Reducing model access to secrets is stronger than depending on prompt instructions to keep them hidden."
                ),
            },
            {
                "id": "M01.L09.Q05",
                "section_id": "topical-guardrail",
                "question": "Why validate the output of an LLM-based classifier?",
                "options": [
                    "The evaluator may return an unexpected format even when instructed otherwise",
                    "Validation makes the model deterministic",
                    "Validation prevents all prompt injection",
                    "Pydantic automatically rate limits the provider",
                ],
                "correct": 0,
                "explanation": (
                    "Model output is probabilistic, so application control flow should depend on a validated contract."
                ),
            },
            {
                "id": "M01.L09.Q06",
                "section_id": "guardrail-thresholds",
                "question": "What usually happens when a moderation threshold becomes more aggressive?",
                "options": [
                    "More content is blocked, which can increase false positives",
                    "No content is ever blocked",
                    "False positives always become zero",
                    "Rate limits are disabled",
                ],
                "correct": 0,
                "explanation": (
                    "Stricter thresholds tend to catch more problematic content but can also reject more acceptable content."
                ),
            },
            {
                "id": "M01.L09.Q07",
                "section_id": "g-eval-moderation",
                "question": "What is the purpose of constraining an evaluator score to a range such as 1–5?",
                "options": [
                    "Ensure the returned evaluator value satisfies the application's scoring contract",
                    "Make the generated answer longer",
                    "Increase the model context window",
                    "Replace authentication",
                ],
                "correct": 0,
                "explanation": (
                    "The guardrail decision logic should operate on validated values rather than arbitrary model text."
                ),
            },
            {
                "id": "M01.L09.Q08",
                "section_id": "rate-limiting-vs-throttling",
                "question": "What is the best distinction between rate limiting and throttling?",
                "options": [
                    "Rate limiting controls allowed traffic volume, while throttling slows processing or transmission",
                    "They are identical terms",
                    "Rate limiting only applies to databases",
                    "Throttling always rejects the request",
                ],
                "correct": 0,
                "explanation": (
                    "Rate limiting is admission/quota control; throttling is pace control."
                ),
            },
            {
                "id": "M01.L09.Q09",
                "section_id": "rate-limit-algorithms",
                "question": "Which rate-limiting algorithm naturally supports temporary bursts using accumulated capacity?",
                "options": [
                    "Token bucket",
                    "Fixed window only",
                    "Leaky bucket only",
                    "No limiter",
                ],
                "correct": 0,
                "explanation": (
                    "A token bucket accumulates tokens over time and can use them during short bursts."
                ),
            },
            {
                "id": "M01.L09.Q10",
                "section_id": "fastapi-rate-limit",
                "question": "Which HTTP status is commonly used when a request exceeds an API quota?",
                "options": [
                    "429 Too Many Requests",
                    "201 Created",
                    "204 No Content",
                    "101 Switching Protocols",
                ],
                "correct": 0,
                "explanation": (
                    "HTTP 429 communicates that the client has exceeded an allowed request rate."
                ),
            },
            {
                "id": "M01.L09.Q11",
                "section_id": "user-rate-limit",
                "question": "Why can user-based limits be stronger than only IP-based limits?",
                "options": [
                    "Authenticated identity remains stable even when a user changes or rotates IP addresses",
                    "User IDs remove all need for authentication",
                    "IP addresses are never available to servers",
                    "User limits automatically share counters across all processes",
                ],
                "correct": 0,
                "explanation": (
                    "A user account can be used as the quota key even when network addresses change."
                ),
            },
            {
                "id": "M01.L09.Q12",
                "section_id": "distributed-rate-limit",
                "question": "Why is Redis useful for rate limiting across several FastAPI instances?",
                "options": [
                    "It provides centralized shared counter state",
                    "It replaces the LLM",
                    "It automatically moderates generated content",
                    "It converts WebSockets into REST requests",
                ],
                "correct": 0,
                "explanation": (
                    "Separate application replicas do not share process memory, so a shared data store keeps one quota view."
                ),
            },
            {
                "id": "M01.L09.Q13",
                "section_id": "stream-throttling",
                "question": "Why use `await asyncio.sleep(...)` when throttling an async model stream?",
                "options": [
                    "It delays the stream without blocking the entire event loop",
                    "It turns the stream into a database transaction",
                    "It bypasses the rate limiter",
                    "It creates a new process for every chunk",
                ],
                "correct": 0,
                "explanation": (
                    "Async sleep yields control so the event loop can serve other ready tasks during the delay."
                ),
            },
            {
                "id": "M01.L09.Q14",
                "section_id": "traffic-shaping",
                "question": "At what layer does traffic shaping primarily operate?",
                "options": [
                    "Network/infrastructure layer",
                    "Only inside Pydantic validation",
                    "Only inside an LLM prompt",
                    "Only in relational database migrations",
                ],
                "correct": 0,
                "explanation": (
                    "Traffic shaping controls bandwidth and packet flow at the network/infrastructure layer."
                ),
            },
            {
                "id": "M01.L09.Q15",
                "section_id": "layered-abuse-protection",
                "type": "open",
                "question": (
                    "Design the protection pipeline for a public multimodal GenAI API. "
                    "Explain where authentication, authorization, deterministic request validation, "
                    "input guardrails, user-level rate limits, model execution, output guardrails, "
                    "WebSocket/stream throttling, and distributed quota storage belong. "
                    "Identify which controls are deterministic and which remain probabilistic."
                ),
            },
        ],

        "passing_score": 70,
    },
}
