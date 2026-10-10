"""M01.L13 — Deployment, Scaling, and the AgentOps Infinity Loop.

One source chapter -> one complete learner-facing lesson.

Source alignment:
- Chapter 20: Deployment and Scaling the Integrated System

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L13"
MODULE_ORDER = 1
MODULE_TITLE = "Deployment, Scaling & Continuous AgentOps"
MODULE_DESCRIPTION = (
    "Turn an agent from a local prototype into a continuously evaluated, governed, "
    "zero-downtime production service using CI/CD, Development and Staging environments, "
    "Registration as Code, release strategies, observability, parallel team lifecycles, "
    "standardized MCP/A2A contracts, version governance, and continuous feedback."
)
SOURCE_CHAPTER = 20
SOURCE_PAGES = "Early Release draft; page numbers not provided"

TOPIC = {
    "title": "Deployment, Scaling, and the AgentOps Infinity Loop",
    "slug": "agent-foundations-m01-l13",
    "description": (
        "Learn how to operationalize the complete agent platform: validate and package agents, "
        "promote them through Development and Staging, evaluate them automatically, register "
        "them in governance systems, release them safely, monitor production behavior, and "
        "coordinate independent Data, Tool, Frontend, and Agent lifecycles at enterprise scale."
    ),
    "order": 13,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 7.0,
    "skill_tags": [
        "ci-cd",
        "agentops",
        "deployment",
        "docker",
        "dev-staging-prod",
        "quality-gates",
        "simulators",
        "autoraters",
        "trajectory-evaluation",
        "registration-as-code",
        "agent-registry",
        "tool-registry",
        "continuous-monitoring",
        "opentelemetry",
        "blue-green",
        "canary",
        "a-b-testing",
        "rollback",
        "parallel-lifecycles",
        "mcp",
        "a2a",
        "contract-testing",
        "versioning",
        "deprecation",
        "continuous-improvement",
    ],
    "prerequisite_ids": [
        "M01.L01", "M01.L02", "M01.L03", "M01.L04", "M01.L05", "M01.L06",
        "M01.L07", "M01.L08", "M01.L09", "M01.L10", "M01.L11", "M01.L12",
    ],

    "lesson": {
        "title": "Deployment, Scaling, and the AgentOps Infinity Loop",
        "estimated_minutes": 420,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Deployment, Scaling, and the AgentOps Infinity Loop

> **Lesson:** M01.L13  
> **Source alignment:** Chapter 20 of the supplied Early Release material.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a working local agent is not yet a production system.
- Explain the purpose of CI/CD in an AgentOps platform.
- Distinguish feature-branch pipelines from main-branch production pipelines.
- Explain why repository structure becomes a contract between developers and the platform.
- Explain the purpose of repository validation, code-level tests, and containerization.
- Explain why containers reduce environment drift and "works on my machine" failures.
- Describe where CI/CD runners can execute in cloud-native and air-gapped environments.
- Trace the Development environment feedback loop.
- Explain why generative-AI behavior requires manual Development testing even after syntax/unit tests pass.
- Explain how Pull Requests and merges act as promotion triggers.
- Distinguish Development from Staging.
- Explain why Staging should mirror Production security, networking, data shape, and identity restrictions.
- Explain the purpose of the first manual approval gate before expensive evaluation.
- Explain how static golden datasets, Simulators, and Autoraters fit into Staging evaluation.
- Explain trajectory evaluation in a deployment pipeline.
- Explain Registration as Code.
- Explain how Agent and Tool Registries track versions, environments, capabilities, metrics, and approval state.
- Explain why the Registry becomes an operational control plane rather than a simple catalog.
- Explain the final manual approval gate.
- Explain how continuous monitoring extends governance beyond deployment.
- Explain how OpenTelemetry can connect application behavior and pipeline/deployment history.
- Explain how end-user feedback returns to the Agent Registry.
- Compare Blue/Green, Canary, and A/B release strategies.
- Explain when automatic rollback is appropriate.
- Explain why rollback must also update governance/registry state.
- Explain why A/B testing is different from Canary deployment.
- Explain why mature AgentOps separates Data, Tools/APIs, Frontend, and Agent lifecycles.
- Explain why independent repositories and pipelines improve organizational velocity.
- Explain the source's "cross-layer production dependency" rule.
- Explain why standardized contracts are essential in decoupled systems.
- Explain how OpenAPI-like schemas, MCP, and A2A reduce coupling.
- Explain why CI/CD should test backward compatibility.
- Explain why multiple agent versions may need to run simultaneously.
- Explain application-side version pinning.
- Explain why live version retention has real infrastructure cost.
- Explain deprecation policy and archival.
- Explain how production feedback is triaged to the correct team.
- Explain the AgentOps Infinity Loop as continuous independent iteration.
- Design a complete enterprise agent deployment lifecycle from code change to production feedback.

---

## 1. A blueprint is not a building

By this point, an agent may already have:

```text
good prompts
evaluation datasets
governed tools
Agent Card
Agent Registry integration
security controls
identity
monitoring plans
```

Yet it may still exist only:

```text
on a laptop
in one repository
on a manually deployed server
```

That is not enterprise readiness.

The source's final operational question is:

> How do we transform a capable agent into a repeatable, governed production service?

---

## 2. Why manual deployment collapses at scale

Manual deployment works for a pilot.

It fails when:

- models change,
- prompts change,
- tools change,
- many teams contribute,
- hundreds of users depend on the service.

A human-only release process creates:

```text
slow delivery
inconsistent environments
missed tests
configuration drift
deployment errors
fragile rollback
```

### Core principle

> Production reliability comes from repeatable automation, not heroic manual effort.

---

## 3. From boutique workshop to automated factory

The source uses a factory/commercial-kitchen analogy.

Engineers design the recipe.

The CI/CD pipeline repeatedly:

```text
checks
tests
packages
deploys
registers
evaluates
promotes
monitors
```

without relying on people to remember every step.

[[IMAGE_NEEDED: AgentOps automated factory | Developer commit enters CI/CD conveyor belt through validate, test, build, Dev, Staging, evaluate, register, approve, Production | Learner should see deployment as an assembly line rather than one command]]

---

## 4. The environment journey

The high-level path is:

```text
Developer
   ↓
CI/CD
   ↓
Development
   ↓
Staging
   ↓
Production
```

Each environment has a different role.

### Development

Fast iteration and manual validation.

### Staging

Production-like automated quality assurance.

### Production

Real users, strict controls, continuous monitoring.

---

## 5. CI/CD foundation

CI/CD stands for:

```text
Continuous Integration
Continuous Deployment / Delivery
```

It provides the machinery that converts source code into a deployed service.

A pipeline configuration defines the ordered tasks.

Examples of pipeline systems in the source include cloud and self-hosted tools.

Treat exact product names as implementation options rather than architecture requirements.

---

## 6. Pipeline as code

The deployment procedure should live beside the application code.

Conceptual pipeline:

```yaml
steps:
  - validate_repository
  - run_tests
  - build_container
  - deploy_development
  - evaluate
  - register
  - approve
  - deploy_production
```

The exact syntax differs by platform.

The durable idea is:

> The deployment process itself should be version-controlled and reviewable.

---

## 7. Branching controls pipeline behavior

The source distinguishes:

```text
feature branch
main branch
```

They represent different levels of confidence and different pipeline responsibilities.

A branch is not just source-control organization.

It can be an operational trigger.

---

## 8. Feature-branch pipeline

A feature branch supports experimentation.

Example:

```text
improve_geometry_tone
```

A push may trigger:

```text
validate
build
deploy temporary Development version
```

The goal is speed.

The engineer can fail safely.

---

## 9. Main-branch pipeline

Merging into `main` means:

```text
this change is a production candidate
```

The main pipeline should therefore be heavier.

It may include:

```text
full deployment sequence
large-scale evaluation
registry updates
approval gates
production rollout
```

---

## 10. Validate before deploying

A pipeline should not immediately deploy.

First validate the repository.

The source expects the standardized project structure established in the previous chapters.

Examples of required assets:

```text
Agent Card
tests
evaluation assets
core agent files
deployment definitions
```

Missing structural requirements should stop the pipeline early.

---

## 11. Repository structure is a platform contract

Standardization allows one pipeline to understand many agents.

For example, if every project follows:

```text
agent.py
prompts.py
context.py
examples.py
tools.py
tests/
evaluation/
deploy/
.well-known/agent.json
```

the platform can automate without special-case logic.

### Principle

> Predictable structure converts conventions into automation.

---

## 12. Code-level tests come before AI evaluation

The first tests answer ordinary software questions:

```text
Does the code import?
Are dependencies present?
Do unit tests pass?
Does linting pass?
Will the service start?
```

They do not answer:

```text
Is the tutor pedagogically effective?
Is the tone appropriate?
Did the agent choose the right tool?
```

Those require later AI evaluation.

---

## 13. Build a standardized container

After validation, the pipeline packages the application.

A container includes:

```text
agent code
libraries
runtime dependencies
system dependencies
```

The goal is environment consistency.

### Container benefit

```text
same artifact
runs in Dev
runs in Staging
runs in Prod
```

This reduces:

```text
"it works on my machine"
```

problems.

---

## 14. The pipeline itself can be modular

The source points out that pipeline steps may themselves run as short-lived containers.

Conceptually:

```text
validator container
→ test container
→ builder container
→ deployer container
```

Each has one responsibility.

This makes the pipeline:

- modular,
- reproducible,
- scalable.

---

## 15. Where does CI/CD run?

Possible environments include:

### Managed cloud runners

Useful for:

- elasticity,
- low operational burden.

### Self-hosted runners

Useful for:

- private infrastructure,
- air-gapped networks,
- specialized hardware,
- regulatory boundaries.

The core principle stays the same:

> Automation should be standardized regardless of where the runner executes.

{{exercise:M01.L13.EX01}}

---

## 16. Development is the first live destination

After the container is built, deploy it to Development.

Development supports:

```text
rapid feedback
manual interaction
safe experimentation
debugging
```

It is not Production.

It is an engineering sandbox.

---

## 17. The pipeline uses the repository structure as a map

The pipeline knows:

```text
where prompts live
where evaluation data lives
where tools live
where tests live
where the Agent Card lives
```

This makes deployment generic across agents.

A Grammar Agent and a Financial Aid Agent can use the same pipeline machinery.

---

## 18. Mandatory vs optional project components

Some elements may be mandatory.

Examples:

```text
Agent Card
tests
evaluation config
core agent entrypoint
```

Others may be optional.

Example:

```text
sub_agents/
```

This lets the platform enforce governance without forcing every project to be equally complex.

---

## 19. Example: safely changing agent behavior

Suppose students report that the Math Tutor is technically correct but discouraging.

A prompt engineer updates:

```text
prompts.py
```

The change is made in a feature branch.

The feature pipeline then:

```text
validates
builds
deploys private version
```

No live students are affected.

---

## 20. Deploy local tools with the agent when needed

If the agent depends on a local code tool, the Development deployment should include it.

Why?

You need to test:

```text
agent + prompt + tool
```

as one working micro-ecosystem.

Otherwise, the developer may validate the agent against a tool configuration that does not match the real deployment.

---

## 21. Why Development still needs humans

Generative behavior is non-deterministic.

A unit test can prove:

```text
Python executes
```

but not:

```text
explanation is patient
reasoning is pedagogically good
conversation feels natural
```

In Development, AI and prompt engineers manually interact with the candidate.

---

## 22. The Development feedback loop

The loop is:

```text
edit
↓
push feature branch
↓
feature pipeline deploys
↓
manual test
↓
observe behavior
↓
edit again
```

This continues until the engineers are satisfied.

[[IMAGE_NEEDED: Development feedback loop | Feature branch -> lightweight CI/CD -> private Dev agent -> manual engineer testing -> prompt/code changes -> push again | Learner should distinguish fast human iteration from Staging automation]]

---

## 23. Pull Request as an engineering gate

When the feature appears ready:

```text
open Pull Request
peer review
approve
merge to main
```

Peer review adds:

- code review,
- architectural review,
- collaborative accountability.

The feature branch/pipeline can then be destroyed.

---

## 24. Merge to main is a promotion trigger

Merging to `main` acts like a tripwire.

It starts the primary production-bound pipeline.

This pipeline should treat the code as:

```text
candidate for enterprise promotion
```

not simply:

```text
developer experiment
```

---

## 25. Main may deploy to Development again

The source notes that the integrated main-branch version may first return to Development.

Why?

The merged code may interact with other recent changes.

A successful feature branch does not guarantee the combined main branch is healthy.

---

## 26. Why Staging exists

Development is intentionally permissive.

Engineers may have:

- direct access,
- debugging permissions,
- relaxed network rules.

Production should be strict.

Staging exists to reproduce Production constraints before users see the release.

---

## 27. Staging should mirror Production

A strong Staging environment mirrors:

```text
network restrictions
IAM
service topology
data shape
resource constraints
guardrails
monitoring
```

Data should be production-like but appropriately protected/anonymized where needed.

### Principle

> Staging tests the production architecture, not just the application logic.

---

## 28. Why an agent can work in Dev and fail in Prod

Possible causes:

```text
Dev has broad credentials
Prod uses least privilege

Dev can access public internet
Prod egress is filtered

Dev uses local data
Prod uses governed APIs

Dev allows debugging
Prod blocks direct human access
```

Staging reveals these mismatches safely.

---

## 29. First manual approval gate

Before expensive AI evaluation, the pipeline can pause.

A QA lead/Product Owner checks:

```text
basic behavior
obvious regressions
deployment health
```

Why?

Large-scale AI evaluation can consume substantial:

```text
tokens
compute
time
money
```

A quick human sanity check can avoid wasting that budget.

---

## 30. Deploy to Staging

After approval:

```text
candidate image
→ Staging
```

This should be the version that automated evaluation targets.

The evaluation therefore measures the deployed candidate under realistic infrastructure.

---

## 31. Static golden datasets

The pipeline can read:

```text
evaluation/dataset.jsonl
```

and run known cases.

These are useful for:

- regression tests,
- critical expected behaviors,
- known edge cases.

But they are limited.

Static examples cannot represent every dynamic multi-turn interaction.

---

## 32. Simulators generate dynamic interactions

A Simulator acts like a user.

Example persona:

```text
frustrated high-school student
struggling with fractions
```

It interacts dynamically with the candidate agent.

This helps uncover unexpected paths.

The Simulator is the actor.

It is not the judge.

---

## 33. Autoraters evaluate the interaction

After the simulated session, an Autorater grades it.

Possible criteria:

```text
helpfulness
correctness
tone
grounding
tool behavior
safety
```

This enables AI-on-AI evaluation at scale.

Human validation can still be used for calibration.

---

## 34. Evaluate the execution trajectory

The pipeline should not only score the final answer.

It should inspect:

```text
tool selected
arguments
sequence
retries
timeout behavior
clarification behavior
final response
```

Example:

```text
Did the Tutor use calculus_solver?
Did it pass correct JSON?
Did it handle API timeout?
```

This connects deployment directly to the evaluation discipline from Chapter 16.

---

## 35. Promotion thresholds

The Center of Excellence or platform team can define minimum thresholds.

Examples:

```text
tool accuracy >= target
safety >= target
helpfulness >= target
latency <= target
cost <= target
```

If the candidate fails:

```text
pipeline stops
```

It does not proceed because a human "feels" it is probably okay.

---

## 36. Registration as Code

After evaluation, the pipeline updates governance systems automatically.

It may extract:

```text
Agent Card
tool schemas
version
endpoint
evaluation scores
environment
approval state
```

and register them through APIs.

This is:

```text
Registration as Code
```

No manual spreadsheet editing.

[[IMAGE_NEEDED: Registration as Code | CI/CD reads Agent Card + evaluation metrics + tool schemas -> updates Agent Registry and Tool Registry -> portal shows version/environment/verified quality | Learner should see registry state as pipeline-generated operational metadata]]

---

## 37. Register early and update through the lifecycle

The source notes that registration can begin as early as Development.

The Registry record evolves:

```text
Dev
→ Staging
→ Approved
→ Prod
```

It can track:

- current environment,
- version,
- evaluation,
- approval,
- deployment state.

---

## 38. Registry becomes a command center

A registry should not only answer:

```text
What agents exist?
```

It can also answer:

```text
Which version is in Dev?
Which version is in Staging?
Which release awaits approval?
Which release failed?
How is production quality trending?
```

This turns the Registry into an operational control plane.

---

## 39. Approval workflows can be Registry-driven

At a gate:

```text
pipeline pauses
Registry marks pending approval
owner receives notification
owner opens portal
reviews metrics
approve/reject
pipeline resumes/stops
```

This connects human governance to automation cleanly.

---

## 40. Final manual approval gate

Before Production, reviewers may inspect:

```text
evaluation scores
security/guardrail status
Agent Gateway scopes
Staging health
latency
cost
tool contracts
```

Only after this review should the release proceed.

---

## 41. Deployment is the beginning of the feedback loop

Production is not the end.

Real users create:

- new edge cases,
- unexpected language,
- traffic spikes,
- new failure patterns.

The platform must continuously check whether Staging quality remains true in production.

---

## 42. Monitoring definitions should be version-controlled

The source recommends keeping team-specific monitoring logic with the agent project.

Why?

Changes to monitoring become:

```text
reviewable
versioned
deployable
auditable
```

This is the same philosophy as:

```text
Infrastructure as Code
Pipeline as Code
Registration as Code
```

---

## 43. Central and local monitoring both matter

### Central platform

May enforce universal rules:

```text
toxicity checks
hallucination detection
security alerts
cost limits
```

### Agent team

May add domain rules:

```text
Math Tutor daily token budget
student-helpfulness target
tool latency
```

Standardization should not eliminate domain-specific observability.

---

## 44. OpenTelemetry unifies operational history

OpenTelemetry can connect one request across:

```text
frontend
agent
tool
database
```

The source also proposes standardizing pipeline logs.

This allows teams to ask:

```text
Which deployment introduced this latency spike?
```

rather than arguing about which subsystem is responsible.

---

## 45. Production feedback returns to the Registry

Production data can include:

```text
Autorater scores
thumbs up/down
latency
cost
tool errors
resource utilization
```

Feeding this back into the Registry makes it a living command center.

---

## 46. Production quality creates the next feature branch

Example:

```text
helpfulness score drops
↓
Product Owner opens ticket
↓
AI engineer changes prompt
↓
new feature branch
↓
pipeline starts again
```

This is the beginning of the Infinity Loop.

{{exercise:M01.L13.EX02}}

---

## 47. Production release needs a traffic strategy

Simply replacing the running container can:

- drop WebSockets,
- lose sessions,
- interrupt tasks,
- create downtime.

The source presents three release strategies:

```text
Blue/Green
Canary
A/B Testing
```

They solve different problems.

---

## 48. Blue/Green deployment

Maintain two equivalent production environments:

```text
Blue = current live version
Green = new candidate
```

Deploy the new version to Green.

Run health checks.

Then switch traffic.

### Main advantage

Very fast rollback:

```text
Green fails
→ route back to Blue
```

The previous version remains intact.

---

## 49. When Blue/Green is useful

Use when you want:

```text
clean environment switch
simple rollback
full version replacement
```

It is especially useful when infrastructure-level compatibility is the main concern.

Trade-off:

```text
duplicated environment capacity
```

during the transition.

---

## 50. Canary deployment

Canary keeps old and new versions live together.

Only a small subset of traffic goes to the candidate.

Example progression:

```text
small %
→ larger %
→ larger %
→ 100%
```

The exact percentages are policy choices.

The source's numbers are examples.

---

## 51. Canary needs active observation

The candidate cohort should be watched closely.

Possible signals:

```text
crash rate
latency
Autorater score
hallucination rate
tool failures
cost
```

If quality deteriorates:

```text
abort rollout
route traffic back
```

This limits blast radius.

---

## 52. Rollback is also a governance event

A rollback should not only change the load balancer.

The pipeline should also update:

```text
Agent Registry status
Tool Registry state if relevant
approval state
release history
owner notifications
```

This keeps control-plane state aligned with real production state.

---

## 53. Rollback should explain why

A good failure notification includes evidence.

Examples:

```text
Autorater drop
latency spike
error trace
tool failure
resource exhaustion
```

The next engineer should know what to fix.

A rollback without evidence only postpones the diagnosis.

---

## 54. A/B testing

A/B testing is different.

Its primary purpose is not technical safety.

It asks:

```text
Which version creates better outcomes?
```

Example:

```text
Version A = encouraging tutor
Version B = Socratic tutor
```

Users are divided between variants.

Quality/business outcomes are compared.

---

## 55. A/B decisions are often human-driven

Canary may automatically stop a release when technical/safety thresholds fail.

A/B tests often require longer observation.

A Product Owner may review:

```text
learning outcomes
user ratings
Autorater scores
engagement
```

and choose the better variant.

---

## 56. Compare release strategies

| Strategy | Main goal | Traffic | Rollback/decision |
|---|---|---|---|
| Blue/Green | Safe replacement | 0/100 switch | Fast switch back |
| Canary | Limit technical blast radius | Gradual subset | Often automated |
| A/B | Compare product/AI quality | Deliberate cohorts | Usually data-driven human decision |

Do not use these terms interchangeably.

[[IMAGE_NEEDED: Blue/Green vs Canary vs A/B | Three mini diagrams showing full switch, gradual traffic ramp, and fixed experimental cohorts | Learner should visually distinguish technical rollout from product experiment]]

{{exercise:M01.L13.EX03}}

---

## 57. The AgentOps Infinity Loop

Enterprise systems are not one pipeline.

They are many independent systems evolving simultaneously.

The source calls for a shift from:

```text
one linear deployment
```

to:

```text
continuous orchestration of parallel lifecycles
```

---

## 58. A production agent is a distributed ecosystem

The Math Tutor may depend on:

```text
data pipeline
vector/data layer
tools/APIs
frontend
agent runtime
observability
identity
```

Each can be owned by a different team.

Treating all of them as one repository can slow everyone down.

---

## 59. Separate repositories and pipelines

The source describes independent lifecycles for:

```text
Data / ETL
Tools / APIs
Frontend / Application
AI Agent
```

Each team has:

```text
own repository
own Dev
own Staging
own Prod
own CI/CD
```

This supports independent velocity.

---

## 60. Data lifecycle

Data Engineers may update:

```text
PDF extraction
image processing
chunking
ETL
data preparation
```

Their pipeline can deploy data changes independently.

The agent does not need to be redeployed for every ETL improvement if contracts remain stable.

---

## 61. Tool/API lifecycle

API developers may change:

```text
check_grades
calculus_solver
payment API
```

Their pipeline should:

```text
test
build
deploy
update Tool Registry
```

Again, this can happen independently of the agent team.

---

## 62. Frontend lifecycle

App developers may change:

```text
WebSocket handling
graphing UI
live voice UX
task cards
```

The frontend can have its own release cycle.

---

## 63. Agent lifecycle

AI/Prompt Engineers may change:

```text
prompts
examples
routing
model choice
agent logic
```

Their pipeline evaluates agent quality before promotion.

This keeps cognitive behavior changes separate from UI/tool/data changes.

---

## 64. Mature systems may separate environments per layer

Advanced organizations may have:

```text
Data Dev / Staging / Prod
Tool Dev / Staging / Prod
Frontend Dev / Staging / Prod
Agent Dev / Staging / Prod
```

That is more complex.

But it allows independent validation.

---

## 65. Cross-layer production dependency rule

The source suggests a "golden rule":

> When one layer is being tested, connect it to stable Production versions of the other layers.

Example:

```text
Agent Staging
uses
Production Data
Production Tool APIs
```

The intention is to test one moving target at a time.

### Important nuance

In real systems, this policy must be reconciled with privacy, test isolation, and production-safety requirements.

Treat it as the source's architectural principle, not a universal rule.

---

## 66. Independent teams create compatibility risk

Decoupling improves speed.

But it introduces this failure mode:

```text
Tool team changes schema
Agent still sends old arguments
Agent fails
```

Loose organizational coupling requires strong technical contracts.

---

## 67. Standardized contracts are the mounting bolts

The source uses an engineering analogy.

Different teams do not need to work in the same room.

They do need compatible interfaces.

Contracts may include:

```text
OpenAPI-style schemas
MCP
A2A
event schemas
version rules
```

---

## 68. CI/CD should test contract compatibility

When a tool schema changes, the pipeline should ask:

```text
Is this backward compatible?
Will current consumers still work?
Has the Tool Registry schema changed?
Do MCP definitions still match?
```

Contract tests prevent independent pipelines from silently breaking one another.

---

## 69. MCP as a tool contract

MCP can standardize:

```text
tool discovery
tool schemas
tool invocation
```

If Tool Registry metadata and MCP definitions remain consistent, the agent can discover tools without hard-coded integration glue.

---

## 70. A2A as an agent-service contract

A2A provides a standard way for agents to discover and interact with other agent services.

This reduces coupling between:

```text
agent implementation
```

and:

```text
consumer integration
```

Standard protocol boundaries are what allow teams to move independently.

---

## 71. Versioning becomes an operational problem

Suppose:

```text
Math Tutor v1
Math Tutor v2
```

Different applications may migrate at different speeds.

For example:

```text
mobile app wants v2 now
student portal must stay on v1 during finals
```

The platform may need both versions live.

---

## 72. Consumers may pin an agent version

Applications can request:

```text
Math Tutor v1
```

instead of:

```text
latest
```

This is similar to pinning a software dependency.

It improves stability for consumers.

---

## 73. Live version pinning has real cost

A Python package version is static.

A deployed agent version consumes:

```text
compute
memory
monitoring
operational support
possibly GPU
```

Keeping 100 historical versions alive is expensive.

Version pinning must therefore be governed.

---

## 74. Deprecation policy

Governance can define:

```text
support window
deprecation date
migration period
shutdown date
archive policy
```

The source gives an example time window.

Treat exact duration as organization-specific.

The Registry should expose lifecycle state.

---

## 75. Retire execution, preserve history

When an old version is decommissioned, you may still preserve:

```text
metadata
evaluation history
deployment history
audit records
```

The service can stop running while the Registry record remains archived.

This balances cost and traceability.

---

## 76. Route feedback to the correct team

Production feedback should be triaged.

Example:

```text
UI bug
→ Frontend team

hallucination
→ AI Agent team

tool formula bug
→ Tool/API team

bad document extraction
→ Data team
```

The governance/control tower should help route the issue.

---

## 77. Independent iteration creates enterprise agility

Each team:

```text
receives evidence
creates feature branch
tests locally
merges
runs pipeline
deploys independently
```

They do not wait for a giant coordinated release.

Contracts and registries keep the ecosystem coherent.

---

## 78. The complete Infinity Loop

The loop becomes:

```text
Production interaction
   ↓
monitoring + feedback
   ↓
triage
   ↓
correct team
   ↓
feature branch
   ↓
CI/CD
   ↓
Dev
   ↓
Staging
   ↓
evaluation
   ↓
registry/governance
   ↓
safe Production release
   ↓
Production interaction
```

There is no final state.

AgentOps is continuous evolution.

[[IMAGE_NEEDED: AgentOps Infinity Loop | Production feedback -> triage -> Data/Tool/Frontend/Agent team branches -> separate CI/CD pipelines -> Dev/Staging/Prod -> Registries/Governance -> Production -> feedback | Learner should see multiple independent loops connected through contracts and governance]]

---

## 79. Complete main-branch pipeline

A mature pipeline can conceptually perform:

```text
1. Validate repository
2. Run code-level tests
3. Build container
4. Deploy integrated candidate to Dev
5. Manual approval
6. Deploy to Staging
7. Run golden + Simulator + Autorater evaluation
8. Register/update Agent & Tool Registry
9. Final manual approval
10. Deploy to Production
11. Observe release
12. Update Registry status
13. Feed production metrics back
```

The exact step numbering can vary.

The important idea is the gated progression.

---

## 80. Every step needs a failure path

Production pipelines should define:

```text
What happens if validation fails?
What happens if unit tests fail?
What happens if Staging fails?
What happens if evaluation score drops?
What happens if approval is rejected?
What happens if Canary metrics degrade?
```

The safe default is:

```text
stop promotion
preserve evidence
notify owner
keep stable version serving
```

---

## 81. Governance becomes executable

By the end of the chapter, governance is no longer only a policy document.

It is encoded in:

```text
repository structure
pipeline gates
evaluation thresholds
Registry state
Agent Gateway policy
version rules
approval workflow
release strategy
deprecation
```

This is one of the most important AgentOps ideas.

---

## 82. Production principles to retain

### 1. Never deploy directly from a developer laptop

Use a reproducible pipeline.

### 2. Validate ordinary software before expensive AI evaluation

Fail early.

### 3. Separate Development from Staging

They have different goals.

### 4. Treat AI quality as a deployable gate

Do not rely only on syntax/unit tests.

### 5. Automate registration

Registry state should reflect reality.

### 6. Human approval still has a place

Automation does not remove accountability.

### 7. Use safe release strategies

Minimize downtime and blast radius.

### 8. Monitor after deployment

Production is another evaluation environment.

### 9. Decouple teams through stable contracts

Independent delivery requires compatibility.

### 10. Govern versions

Old live services have real cost.

{{exercise:M01.L13.EX04}}

---

## 83. Production deployment checklist

### Source control

- feature branches,
- peer-reviewed Pull Requests,
- protected main branch.

### Repository contract

- Agent Card present,
- tests present,
- evaluation assets present,
- deployment config present,
- standard structure validated.

### CI

- lint/static analysis,
- unit tests,
- dependency checks,
- container build.

### Development

- private deployment,
- local tools where required,
- manual interaction,
- rapid prompt/code iteration.

### Staging

- production-like network/IAM,
- representative protected data,
- golden datasets,
- Simulator runs,
- Autoraters,
- trajectory metrics,
- latency/cost checks.

### Governance

- Registration as Code,
- Agent Registry update,
- Tool Registry update,
- evaluation attached,
- approval status tracked.

### Production

- final approval,
- Blue/Green or Canary rollout,
- A/B when testing product behavior,
- rollback plan,
- registry-state rollback.

### Monitoring

- OpenTelemetry,
- user feedback,
- Autorater monitoring,
- resource/cost monitoring,
- owner alerts.

### Multi-team scale

- separate lifecycles,
- contract tests,
- MCP/A2A compatibility,
- version pinning,
- deprecation policy.

---

## 84. Source-specific details to re-check

This chapter is Early Release material.

Re-verify before implementation:

- exact CI/CD product syntax,
- current cloud build systems,
- exact folder conventions,
- specific Agent Card paths/fields,
- exact Simulator/Autorater tooling,
- exact Registry APIs,
- specific approval-portal implementation,
- Canary traffic percentages,
- deprecation duration,
- OpenTelemetry AI conventions,
- current MCP/A2A schemas,
- cloud runner security models.

Treat the source's concrete percentages and retention windows as illustrative examples unless your organization explicitly adopts them.

The durable ideas are:

```text
automation
gated promotion
production-like staging
AI-specific evaluation
registration as code
safe rollout
continuous monitoring
decoupled lifecycles
standard contracts
version governance
continuous feedback
```

---

## 85. Complete mental model

The final AgentOps platform works like this:

```text
Developer change
   ↓
Feature branch
   ↓
Lightweight Dev pipeline
   ↓
Manual iteration
   ↓
Pull Request
   ↓
Main branch
   ↓
Validated build
   ↓
Development
   ↓
Approval
   ↓
Staging
   ↓
Golden + Simulator + Autorater evaluation
   ↓
Registration as Code
   ↓
Final approval
   ↓
Blue/Green / Canary / A/B
   ↓
Production
   ↓
OpenTelemetry + user feedback + Autoraters
   ↓
Agent Registry
   ↓
Issue triage
   ↓
next feature branch
```

At enterprise scale, this single loop becomes several parallel loops:

```text
Data
Tools/APIs
Frontend
Agent
```

Each team moves independently.

They remain compatible through:

```text
contracts
registries
MCP
A2A
version policy
governance
```

That is the AgentOps Infinity Loop.

---

## Important misconceptions

### Misconception 1
> "A working local agent is production-ready."

No. Production readiness requires repeatable build, test, deployment, governance, monitoring, and rollback.

### Misconception 2
> "Every feature-branch push should go to Production."

No. Feature branches belong in safe Development workflows.

### Misconception 3
> "Syntax and unit tests prove the agent is good."

No. They prove software health, not cognitive/behavioral quality.

### Misconception 4
> "Development and Staging are interchangeable."

No. Staging should reproduce Production constraints and support automated quality gates.

### Misconception 5
> "Human approval makes CI/CD non-automated."

No. Approval is a deliberate gated step inside an otherwise automated system.

### Misconception 6
> "A Simulator is the evaluator."

No. The Simulator generates the interaction; an Autorater or other evaluator judges it.

### Misconception 7
> "Registration belongs at the end as manual paperwork."

No. Registration can be automated and updated throughout the lifecycle.

### Misconception 8
> "The Agent Registry is only a searchable directory."

No. It can become a live command center for versions, environments, metrics, approvals, and deployment state.

### Misconception 9
> "Deployment ends governance."

No. Production monitoring begins the next improvement cycle.

### Misconception 10
> "Blue/Green, Canary, and A/B are equivalent."

No. They optimize different goals.

### Misconception 11
> "A rollback only changes network traffic."

No. Governance and Registry state should also be corrected.

### Misconception 12
> "Canary and A/B both answer which persona users prefer."

No. Canary primarily manages technical release risk; A/B compares product/behavior outcomes.

### Misconception 13
> "One huge repository and pipeline makes enterprise systems easier."

Not necessarily. It can reduce independent team velocity.

### Misconception 14
> "Independent teams can safely change interfaces whenever they want."

No. Decoupling depends on strong contracts and compatibility testing.

### Misconception 15
> "Version pinning has no cost."

Live agent versions consume real infrastructure and operational resources.

### Misconception 16
> "Old agent versions should disappear completely."

Execution may stop, but metadata and audit history can remain archived.

### Misconception 17
> "Production feedback belongs only in dashboards."

No. It should create actionable work and new evaluation cases.

### Misconception 18
> "AgentOps has a final stable endpoint."

No. The source's final model is an Infinity Loop of continuous improvement.

---

## Key terminology

| Term | Meaning |
|---|---|
| CI/CD | Automated integration, test, build, and deployment workflow |
| Feature Branch | Isolated branch used for experimentation |
| Main Branch | Production-candidate integration branch |
| Pipeline as Code | Version-controlled deployment process |
| Repository Contract | Standard project structure expected by automation |
| Container | Portable packaged runtime artifact |
| Development | Fast, permissive environment for manual engineering iteration |
| Staging | Production-like environment for automated verification |
| Production | Live end-user environment |
| Quality Gate | Condition that must pass before promotion |
| Golden Dataset | Curated known evaluation cases |
| Simulator | Agent generating test interactions |
| Autorater | AI evaluator grading an interaction |
| Trajectory Evaluation | Scoring tool/action sequence, not only final output |
| Registration as Code | Programmatic registry updates by CI/CD |
| Agent Registry | Operational record of deployed agents |
| Tool Registry | Operational record of governed tools |
| Manual Approval Gate | Human checkpoint inside automated promotion |
| OpenTelemetry | Standard for distributed telemetry |
| Blue/Green | Two-environment release with all-at-once traffic switch |
| Canary | Gradual live rollout to a small traffic fraction |
| A/B Test | Parallel experiment comparing product/behavior outcomes |
| Rollback | Return traffic/service state to previous stable version |
| Blast Radius | Number/scope of users affected by a failure |
| Contract Testing | Verification that interface/schema changes remain compatible |
| MCP | Standardized tool/context protocol used as an integration contract |
| A2A | Standardized agent-to-agent protocol used as a service contract |
| Version Pinning | Consumer requests a specific agent version |
| Deprecation | Planned retirement of a version |
| Cross-Layer Production Dependency | Source principle of testing one changing layer against stable production-grade dependencies |
| Infinity Loop | Continuous feedback, iteration, evaluation, and deployment cycle |

---

## Self-check

1. Why is a working agent on a laptop not production-ready?
2. What problem does CI/CD solve?
3. Why should pipeline definitions be version-controlled?
4. What is the role of a feature branch?
5. What changes when code is merged into main?
6. Why validate repository structure?
7. Which project files/folders can act as a pipeline contract?
8. Why run ordinary unit tests before AI evaluation?
9. What problem does a container solve?
10. Where can CI/CD runners execute?
11. What is the purpose of the Development environment?
12. Why do generative systems still need manual Dev testing?
13. Why can the integrated main branch be deployed to Dev again?
14. What is Staging for?
15. How should Staging differ from Development?
16. Why have a manual gate before expensive AI evaluation?
17. What is a golden dataset?
18. Why use Simulators?
19. What is the Autorater's job?
20. What does trajectory evaluation inspect?
21. What happens when an evaluation threshold fails?
22. What is Registration as Code?
23. Which metadata should the pipeline register?
24. Why can the Agent Registry be called a command center?
25. What belongs in the final approval review?
26. Why does monitoring continue after Production deployment?
27. Why version-control monitoring definitions?
28. What is the role of OpenTelemetry after deployment?
29. How does user feedback return to the development loop?
30. What is Blue/Green deployment?
31. What is its biggest rollback advantage?
32. What is Canary deployment?
33. Why does Canary reduce blast radius?
34. Why should rollback also update Registry state?
35. How does A/B testing differ from Canary?
36. Why might A/B decisions remain manual?
37. Why split Data, Tool, Frontend, and Agent repositories?
38. What is the advantage of independent pipelines?
39. What is the source's cross-layer production dependency rule?
40. What risk does team decoupling introduce?
41. Why are standardized contracts necessary?
42. What can OpenAPI-like schemas test?
43. What role does MCP play?
44. What role does A2A play?
45. Why can different applications need different live agent versions?
46. What is version pinning?
47. Why does keeping many agent versions alive cost money?
48. What is a deprecation policy?
49. Why archive old Registry records?
50. How should production feedback be triaged?
51. What is the AgentOps Infinity Loop?
52. What are the major main-branch pipeline stages?
53. What should happen when a pipeline gate fails?
54. How does governance become executable?
55. Which source-specific details should be re-verified before implementation?

---

## Retain this idea

**AgentOps productionization is a controlled, repeatable loop—not a one-time deployment. Source code moves through version-controlled pipelines, standardized validation, Development feedback, production-like Staging, AI-specific evaluation, automated registry updates, human governance gates, safe release strategies, and continuous production monitoring. At enterprise scale, Data, Tool, Frontend, and Agent teams evolve independently, so standardized MCP/A2A/API contracts and governed version lifecycles become essential. Production feedback then creates the next feature branch, completing an infinite loop of continuous improvement.**
""".strip(),

        "sections": [
            {"id": "prototype-production", "title": "A Blueprint Is Not a Building", "order": 1},
            {"id": "manual-collapse", "title": "Why Manual Deployment Collapses at Scale", "order": 2},
            {"id": "factory", "title": "From Boutique Workshop to Automated Factory", "order": 3},
            {"id": "environment-journey", "title": "The Environment Journey", "order": 4},
            {"id": "cicd", "title": "CI/CD Foundation", "order": 5},
            {"id": "pipeline-as-code", "title": "Pipeline as Code", "order": 6},
            {"id": "branch-strategy", "title": "Branching Controls Pipeline Behavior", "order": 7},
            {"id": "feature-branch", "title": "Feature-Branch Pipeline", "order": 8},
            {"id": "main-branch", "title": "Main-Branch Pipeline", "order": 9},
            {"id": "validate-first", "title": "Validate Before Deploying", "order": 10},
            {"id": "repo-contract", "title": "Repository Structure Is a Platform Contract", "order": 11},
            {"id": "code-tests", "title": "Code-Level Tests Come Before AI Evaluation", "order": 12},
            {"id": "container", "title": "Build a Standardized Container", "order": 13},
            {"id": "pipeline-containers", "title": "The Pipeline Itself Can Be Modular", "order": 14},
            {"id": "runner-location", "title": "Where Does CI/CD Run?", "order": 15},
            {"id": "development", "title": "Development Is the First Live Destination", "order": 16},
            {"id": "dev-standard-structure", "title": "The Pipeline Uses the Repository Structure as a Map", "order": 17},
            {"id": "mandatory-optional", "title": "Mandatory vs Optional Project Components", "order": 18},
            {"id": "prompt-change-example", "title": "Example: Safely Changing Agent Behavior", "order": 19},
            {"id": "tools-dev", "title": "Deploy Local Tools with the Agent When Needed", "order": 20},
            {"id": "manual-dev", "title": "Why Development Still Needs Humans", "order": 21},
            {"id": "dev-loop", "title": "The Development Feedback Loop", "order": 22},
            {"id": "pull-request", "title": "Pull Request as an Engineering Gate", "order": 23},
            {"id": "merge-tripwire", "title": "Merge to Main Is a Promotion Trigger", "order": 24},
            {"id": "main-dev", "title": "Main May Deploy to Development Again", "order": 25},
            {"id": "staging", "title": "Why Staging Exists", "order": 26},
            {"id": "staging-mirror", "title": "Staging Should Mirror Production", "order": 27},
            {"id": "moving-target", "title": "Why an Agent Can Work in Dev and Fail in Prod", "order": 28},
            {"id": "approval-gate-1", "title": "First Manual Approval Gate", "order": 29},
            {"id": "staging-deploy", "title": "Deploy to Staging", "order": 30},
            {"id": "golden-testing", "title": "Static Golden Datasets", "order": 31},
            {"id": "simulators", "title": "Simulators Generate Dynamic Interactions", "order": 32},
            {"id": "autoraters", "title": "Autoraters Evaluate the Interaction", "order": 33},
            {"id": "trajectory-pipeline", "title": "Evaluate the Execution Trajectory", "order": 34},
            {"id": "thresholds", "title": "Promotion Thresholds", "order": 35},
            {"id": "registration-as-code", "title": "Registration as Code", "order": 36},
            {"id": "registry-lifecycle", "title": "Register Early and Update Through the Lifecycle", "order": 37},
            {"id": "command-center", "title": "Registry Becomes a Command Center", "order": 38},
            {"id": "approval-notifications", "title": "Approval Workflows Can Be Registry-Driven", "order": 39},
            {"id": "final-approval", "title": "Final Manual Approval Gate", "order": 40},
            {"id": "monitoring-begins", "title": "Deployment Is the Beginning of the Feedback Loop", "order": 41},
            {"id": "monitoring-as-code", "title": "Monitoring Definitions Should Be Version-Controlled", "order": 42},
            {"id": "central-team-monitoring", "title": "Central and Local Monitoring Both Matter", "order": 43},
            {"id": "otel-production", "title": "OpenTelemetry Unifies Operational History", "order": 44},
            {"id": "feedback", "title": "Production Feedback Returns to the Registry", "order": 45},
            {"id": "continuous-loop", "title": "Production Quality Creates the Next Feature Branch", "order": 46},
            {"id": "release", "title": "Production Release Needs a Traffic Strategy", "order": 47},
            {"id": "blue-green", "title": "Blue/Green Deployment", "order": 48},
            {"id": "blue-green-strength", "title": "When Blue/Green Is Useful", "order": 49},
            {"id": "canary", "title": "Canary Deployment", "order": 50},
            {"id": "canary-observe", "title": "Canary Needs Active Observation", "order": 51},
            {"id": "rollback-governance", "title": "Rollback Is Also a Governance Event", "order": 52},
            {"id": "failure-evidence", "title": "Rollback Should Explain Why", "order": 53},
            {"id": "ab", "title": "A/B Testing", "order": 54},
            {"id": "ab-human", "title": "A/B Decisions Are Often Human-Driven", "order": 55},
            {"id": "release-comparison", "title": "Compare Release Strategies", "order": 56},
            {"id": "infinity-loop", "title": "The AgentOps Infinity Loop", "order": 57},
            {"id": "distributed-ecosystem", "title": "A Production Agent Is a Distributed Ecosystem", "order": 58},
            {"id": "separate-repos", "title": "Separate Repositories and Pipelines", "order": 59},
            {"id": "data-team", "title": "Data Lifecycle", "order": 60},
            {"id": "tool-team", "title": "Tool/API Lifecycle", "order": 61},
            {"id": "frontend-team", "title": "Frontend Lifecycle", "order": 62},
            {"id": "agent-team", "title": "Agent Lifecycle", "order": 63},
            {"id": "infra-decouple", "title": "Mature Systems May Separate Environments per Layer", "order": 64},
            {"id": "one-moving-target", "title": "Cross-Layer Production Dependency Rule", "order": 65},
            {"id": "parallel-risk", "title": "Independent Teams Create Compatibility Risk", "order": 66},
            {"id": "contracts", "title": "Standardized Contracts Are the Mounting Bolts", "order": 67},
            {"id": "contract-testing", "title": "CI/CD Should Test Contract Compatibility", "order": 68},
            {"id": "mcp-contract", "title": "MCP as a Tool Contract", "order": 69},
            {"id": "a2a-contract", "title": "A2A as an Agent-Service Contract", "order": 70},
            {"id": "versioning", "title": "Versioning Becomes an Operational Problem", "order": 71},
            {"id": "pinning", "title": "Consumers May Pin an Agent Version", "order": 72},
            {"id": "live-cost", "title": "Live Version Pinning Has Real Cost", "order": 73},
            {"id": "deprecation", "title": "Deprecation Policy", "order": 74},
            {"id": "archive", "title": "Retire Execution, Preserve History", "order": 75},
            {"id": "triage", "title": "Route Feedback to the Correct Team", "order": 76},
            {"id": "independent-iteration", "title": "Independent Iteration Creates Enterprise Agility", "order": 77},
            {"id": "infinity", "title": "The Complete Infinity Loop", "order": 78},
            {"id": "full-pipeline", "title": "Complete Main-Branch Pipeline", "order": 79},
            {"id": "failure-paths", "title": "Every Step Needs a Failure Path", "order": 80},
            {"id": "governance-code", "title": "Governance Becomes Executable", "order": 81},
            {"id": "production-principles", "title": "Production Principles to Retain", "order": 82},
            {"id": "production-checklist", "title": "Production Deployment Checklist", "order": 83},
            {"id": "source-boundaries", "title": "Source-Specific Details to Re-Check", "order": 84},
            {"id": "complete-model", "title": "Complete Mental Model", "order": 85},
        ],
    },

    "exercises": [
        {
            "id": "M01.L13.EX01",
            "title": "Design the Feature-to-Development Pipeline",
            "lesson_code": "M01.L13",
            "section_id": "runner-location",
            "placement": "after_section",
            "description": "Build the lightweight pipeline used during active development.",
            "instructions": (
                ('1. Design a feature-branch pipeline for a Tutor Agent.\n'
                 '2. Include repository validation, lint/static checks, unit tests, container build, temporary Development deployment, localized tool deployment, and cleanup when the branch is deleted.\n'
                 '3. Explain what is intentionally NOT included yet and why.')
            ),
            "expected_output": "A lightweight feature CI/CD pipeline with rationale.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["ci-cd", "development", "branch-strategy"],
        },
        {
            "id": "M01.L13.EX02",
            "title": "Build the Staging Quality Gate",
            "lesson_code": "M01.L13",
            "section_id": "continuous-loop",
            "placement": "after_section",
            "description": "Design the automated AI evaluation path between main branch and Production.",
            "instructions": (
                ('1. Design the Staging stage for a Math Tutor.\n'
                 '2. Include production-like IAM/networking, protected representative data, golden tests, Simulator personas, Autorater criteria, trajectory metrics, cost/latency limits, Registration as Code, first/final manual gates, and failure behavior.')
            ),
            "expected_output": "A Staging quality-gate specification.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["staging", "evaluation", "registration-as-code"],
        },
        {
            "id": "M01.L13.EX03",
            "title": "Choose a Production Release Strategy",
            "lesson_code": "M01.L13",
            "section_id": "release-comparison",
            "placement": "after_section",
            "description": "Choose Blue/Green, Canary, or A/B for different release goals.",
            "instructions": (
                "Choose the best strategy for:\n"
                "1. infrastructure/runtime upgrade requiring instant rollback,\n"
                "2. risky new model version needing limited exposure,\n"
                "3. comparison of Socratic vs encouraging tutoring style.\n"
                "For each define traffic behavior, monitoring signals, rollback/decision owner, and Registry updates."
            ),
            "expected_output": "A three-row deployment strategy table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["blue-green", "canary", "a-b-testing"],
        },
        {
            "id": "M01.L13.EX04",
            "title": "Design the AgentOps Infinity Loop",
            "lesson_code": "M01.L13",
            "section_id": "production-principles",
            "placement": "after_section",
            "description": "Connect production feedback to independent team pipelines.",
            "instructions": (
                ('1. Design separate repositories and pipelines for Data/ETL, Tools/APIs, Frontend, and Agent.\n'
                 '2. Add one contract shared by each dependency, define Dev/Staging/Prod for each layer, show how production feedback is triaged, and explain how MCP/A2A/API schemas prevent breaking changes.')
            ),
            "expected_output": "A multi-team Infinity Loop architecture.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["parallel-lifecycles", "contracts", "agentops"],
        },
        {
            "id": "M01.L13.EX05",
            "title": "Create a Registration-as-Code Payload",
            "lesson_code": "M01.L13",
            "section_id": "registration-as-code",
            "placement": "after_section",
            "description": "Define what CI/CD should publish to governance systems.",
            "instructions": (
                ('1. Design the metadata registered for Math Tutor v2.3 after Staging.\n'
                 '2. Include Agent Card reference, version, environment, endpoint, owner, evaluation scores, approval state, tool dependencies, release status, and deprecation field.\n'
                 '3. Explain which fields are updated again after Production deployment.')
            ),
            "expected_output": "A Registry update schema and lifecycle.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agent-registry", "registration-as-code", "governance"],
        },
        {
            "id": "M01.L13.EX06",
            "title": "Design Agent Version Governance",
            "lesson_code": "M01.L13",
            "section_id": "archive",
            "placement": "after_section",
            "description": "Balance compatibility with the cost of running multiple agent versions.",
            "instructions": (
                ('1. Assume Web Portal uses Tutor v1, Mobile uses v2, and a partner API uses v3.\n'
                 '2. Define version pinning, support window, deprecation notice, migration deadline, shutdown behavior, archive metadata, and emergency exceptions.')
            ),
            "expected_output": "A version-retention and migration policy.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["versioning", "deprecation", "registry"],
        },
        {
            "id": "M01.L13.EX07",
            "title": "Design Rollback as a Governance Event",
            "lesson_code": "M01.L13",
            "section_id": "failure-evidence",
            "placement": "after_section",
            "description": "Coordinate traffic rollback, Registry state, evidence, and ownership.",
            "instructions": (
                "A Canary release shows a 40% latency increase and lower helpfulness.\n"
                "Define:\n"
                "1. automatic rollback action,\n"
                "2. Agent Registry state change,\n"
                "3. alerts sent,\n"
                "4. attached evidence,\n"
                "5. the next engineering workflow from failed release to new feature branch."
            ),
            "expected_output": "A complete rollback-and-remediation workflow.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["rollback", "observability", "governance"],
        },
    ],

    "quiz": {
        "id": "M01.L13.QZ01",
        "title": "Deployment, Scaling and the AgentOps Infinity Loop — Knowledge Check",
        "lesson_code": "M01.L13",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L13.Q01",
                "section_id": "manual-collapse",
                "question": "Why does manual deployment fail at enterprise scale?",
                "options": [
                    "It is slow, inconsistent, error-prone, and difficult to govern repeatedly",
                    "It always costs less",
                    "It guarantees perfect testing",
                    "It prevents configuration drift",
                ],
                "correct": 0,
                "explanation": "Repeatability and automation are needed once many changes/users are involved.",
            },
            {
                "id": "M01.L13.Q02",
                "section_id": "pipeline-as-code",
                "question": "What is the main benefit of Pipeline as Code?",
                "options": [
                    "The deployment process becomes version-controlled, reviewable, and repeatable",
                    "It removes the need for source control",
                    "It makes every change production-ready",
                    "It replaces containers",
                ],
                "correct": 0,
                "explanation": "Operational procedure becomes part of the reviewed codebase.",
            },
            {
                "id": "M01.L13.Q03",
                "section_id": "feature-branch",
                "question": "What is the feature-branch pipeline mainly optimized for?",
                "options": [
                    "Fast safe experimentation in Development",
                    "Immediate full production rollout",
                    "Long-term production monitoring only",
                    "Registry archival only",
                ],
                "correct": 0,
                "explanation": "Feature branches support iterative engineering before promotion.",
            },
            {
                "id": "M01.L13.Q04",
                "section_id": "code-tests",
                "question": "What do code-level tests NOT prove?",
                "options": [
                    "That the agent's behavior, pedagogy, or reasoning quality is good",
                    "That imports work",
                    "That unit tests pass",
                    "That syntax is valid",
                ],
                "correct": 0,
                "explanation": "AI-specific quality requires evaluation beyond normal software tests.",
            },
            {
                "id": "M01.L13.Q05",
                "section_id": "container",
                "question": "Why package an agent in a container?",
                "options": [
                    "To run the same runtime artifact consistently across environments",
                    "To eliminate testing",
                    "To make prompts deterministic",
                    "To replace CI/CD",
                ],
                "correct": 0,
                "explanation": "Containers reduce environment drift.",
            },
            {
                "id": "M01.L13.Q06",
                "section_id": "manual-dev",
                "question": "Why is manual Development testing still useful for generative AI?",
                "options": [
                    "Syntax tests cannot judge tone, helpfulness, or conversational behavior",
                    "Manual testing proves formal correctness",
                    "Staging is unnecessary",
                    "Generative systems are deterministic",
                ],
                "correct": 0,
                "explanation": "Behavioral quality requires direct interaction during iteration.",
            },
            {
                "id": "M01.L13.Q07",
                "section_id": "staging-mirror",
                "question": "What is the defining purpose of Staging?",
                "options": [
                    "Validate the release under Production-like infrastructure, IAM, network, and data conditions",
                    "Provide the most permissive developer access",
                    "Host only unit tests",
                    "Replace Production",
                ],
                "correct": 0,
                "explanation": "Staging exists to reveal problems caused by Production constraints.",
            },
            {
                "id": "M01.L13.Q08",
                "section_id": "approval-gate-1",
                "question": "Why use a human gate before expensive AI evaluation?",
                "options": [
                    "To avoid spending evaluation resources on an obviously broken deployment",
                    "To eliminate automation",
                    "To skip Staging",
                    "To make the release manual",
                ],
                "correct": 0,
                "explanation": "A cheap sanity check can protect evaluation budget.",
            },
            {
                "id": "M01.L13.Q09",
                "section_id": "simulators",
                "question": "What is a Simulator?",
                "options": [
                    "An agent that generates realistic test interactions/personas",
                    "The final deployment environment",
                    "A tool registry",
                    "A human approval gate",
                ],
                "correct": 0,
                "explanation": "Simulators generate dynamic evaluation interactions.",
            },
            {
                "id": "M01.L13.Q10",
                "section_id": "trajectory-pipeline",
                "question": "What does trajectory evaluation inspect?",
                "options": [
                    "The agent's sequence of tools/actions, parameters, and handling—not only final text",
                    "Only container size",
                    "Only branch name",
                    "Only user ratings",
                ],
                "correct": 0,
                "explanation": "Agent quality includes execution path.",
            },
            {
                "id": "M01.L13.Q11",
                "section_id": "registration-as-code",
                "question": "What is Registration as Code?",
                "options": [
                    "CI/CD automatically updates Agent/Tool Registry metadata from the deployment",
                    "Developers manually update a spreadsheet",
                    "Users register themselves",
                    "Only tools are containerized",
                ],
                "correct": 0,
                "explanation": "Registry state is generated programmatically from the lifecycle.",
            },
            {
                "id": "M01.L13.Q12",
                "section_id": "command-center",
                "question": "Why can the Agent Registry become a command center?",
                "options": [
                    "It can track versions, environment, evaluation, approvals, release state, and live metrics",
                    "It stores only agent names",
                    "It replaces the frontend",
                    "It only archives old code",
                ],
                "correct": 0,
                "explanation": "Operational metadata turns it into a lifecycle control surface.",
            },
            {
                "id": "M01.L13.Q13",
                "section_id": "monitoring-begins",
                "question": "What happens to governance after Production deployment?",
                "options": [
                    "It continues through monitoring, feedback, alerts, and future evaluation",
                    "It ends immediately",
                    "Only developers remain involved",
                    "Registries are no longer needed",
                ],
                "correct": 0,
                "explanation": "Production starts the next feedback cycle.",
            },
            {
                "id": "M01.L13.Q14",
                "section_id": "blue-green",
                "question": "What is the main Blue/Green rollback advantage?",
                "options": [
                    "Traffic can quickly switch back to the untouched old environment",
                    "No second environment is needed",
                    "It automatically measures business preference",
                    "It never needs health checks",
                ],
                "correct": 0,
                "explanation": "The old environment remains available for fast rollback.",
            },
            {
                "id": "M01.L13.Q15",
                "section_id": "canary",
                "question": "What does a Canary release reduce?",
                "options": [
                    "The blast radius of a bad version by exposing only a small traffic subset first",
                    "The need for monitoring",
                    "The number of versions to one",
                    "The need for rollback",
                ],
                "correct": 0,
                "explanation": "Gradual exposure limits initial impact.",
            },
            {
                "id": "M01.L13.Q16",
                "section_id": "rollback-governance",
                "question": "Why must rollback update Registry state?",
                "options": [
                    "Governance metadata should match what is actually serving users",
                    "The Registry controls DNS only",
                    "Rollback deletes all history",
                    "The Registry is unrelated to deployment",
                ],
                "correct": 0,
                "explanation": "Operational truth and governance truth must remain aligned.",
            },
            {
                "id": "M01.L13.Q17",
                "section_id": "ab",
                "question": "What is A/B testing primarily designed to compare?",
                "options": [
                    "Product/AI behavior and user outcomes between variants",
                    "Only server crash rates",
                    "Only network policies",
                    "Only container startup time",
                ],
                "correct": 0,
                "explanation": "A/B tests are experiments rather than primarily safety rollouts.",
            },
            {
                "id": "M01.L13.Q18",
                "section_id": "separate-repos",
                "question": "Why use separate repositories/pipelines for Data, Tools, Frontend, and Agent layers?",
                "options": [
                    "Different teams can iterate and deploy independently",
                    "To remove all interface contracts",
                    "To force simultaneous releases",
                    "To avoid CI/CD",
                ],
                "correct": 0,
                "explanation": "Independent lifecycles improve velocity.",
            },
            {
                "id": "M01.L13.Q19",
                "section_id": "contracts",
                "question": "What makes independent lifecycles safe?",
                "options": [
                    "Strict standardized contracts and compatibility tests",
                    "No versioning",
                    "Shared global variables",
                    "Manual memory",
                ],
                "correct": 0,
                "explanation": "Loose coupling requires strong interfaces.",
            },
            {
                "id": "M01.L13.Q20",
                "section_id": "mcp-contract",
                "question": "What role does MCP play in the decoupled ecosystem?",
                "options": [
                    "It standardizes tool discovery and invocation contracts",
                    "It replaces deployment environments",
                    "It is only a UI protocol",
                    "It stores user feedback",
                ],
                "correct": 0,
                "explanation": "MCP reduces custom integration between agents and tools.",
            },
            {
                "id": "M01.L13.Q21",
                "section_id": "a2a-contract",
                "question": "What role does A2A play?",
                "options": [
                    "It standardizes agent-to-agent service interaction",
                    "It builds containers",
                    "It replaces IAM",
                    "It is a data warehouse format",
                ],
                "correct": 0,
                "explanation": "A2A defines a stable boundary between agent services.",
            },
            {
                "id": "M01.L13.Q22",
                "section_id": "live-cost",
                "question": "Why does keeping many old agent versions live create cost?",
                "options": [
                    "Each live version consumes runtime infrastructure and operational support",
                    "Version numbers consume GPU by themselves",
                    "Metadata cannot be archived",
                    "Source code storage is extremely expensive",
                ],
                "correct": 0,
                "explanation": "Live services have ongoing compute and support costs.",
            },
            {
                "id": "M01.L13.Q23",
                "section_id": "triage",
                "question": "Where should a broken tool formula generally be routed?",
                "options": [
                    "Tool/API team",
                    "Frontend team",
                    "Prompt engineer only",
                    "End user",
                ],
                "correct": 0,
                "explanation": "Evidence should be routed to the team that owns the failing layer.",
            },
            {
                "id": "M01.L13.Q24",
                "section_id": "infinity",
                "question": "What does the AgentOps Infinity Loop represent?",
                "options": [
                    "Continuous production feedback, team iteration, evaluation, deployment, and monitoring",
                    "One deployment that never changes",
                    "An infinite LLM reasoning loop",
                    "A database replication technique",
                ],
                "correct": 0,
                "explanation": "AgentOps is continuous system evolution.",
            },
            {
                "id": "M01.L13.Q25",
                "section_id": "governance-code",
                "question": "What does it mean for governance to become executable?",
                "options": [
                    "Policies are enforced through pipeline gates, thresholds, registries, approvals, and release rules",
                    "Governance exists only as a PDF",
                    "Developers can bypass all gates",
                    "Only legal teams can deploy",
                ],
                "correct": 0,
                "explanation": "Operational automation turns policy into enforced workflow.",
            },
            {
                "id": "M01.L13.Q26",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design the complete enterprise lifecycle for a live Math Tutor. Include feature branches, "
                    "repository validation, containerization, Development, Pull Requests, main-branch promotion, "
                    "Staging, golden datasets, Simulators, Autoraters, trajectory evaluation, Registration as Code, "
                    "manual approval gates, Blue/Green or Canary release, continuous monitoring, Registry feedback, "
                    "parallel Data/Tool/Frontend/Agent pipelines, MCP/A2A contracts, version pinning, deprecation, "
                    "rollback governance, and the AgentOps Infinity Loop."
                ),
            },
        ],
        "passing_score": 70,
    },
}
