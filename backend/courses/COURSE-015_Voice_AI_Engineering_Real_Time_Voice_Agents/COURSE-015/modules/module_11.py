"""M01.L11 — Sharing and Governing Agents as Reusable Services.

One source chapter -> one complete learner-facing lesson.

Source alignment:
- Chapter 18: Sharing and Governing Agents as Services and Reusable Components

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L11"
MODULE_ORDER = 1
MODULE_TITLE = "Agent Templates, Registries & Access Governance"
MODULE_DESCRIPTION = (
    "Standardize how agents are created, deployed, discovered, reused, and governed by "
    "combining an Agent Template Catalog, Agent-as-a-Service deployment, a centralized "
    "Agent Registry, Registry Record wrappers, Public Facades, lifecycle hygiene, an "
    "Agent Gateway, federated access governance, and secure frontend/backend discovery."
)
SOURCE_CHAPTER = 18
SOURCE_PAGES = "Early Release draft; page numbers not provided"

TOPIC = {
    "title": "Sharing and Governing Agents as Services and Reusable Components",
    "slug": "agent-foundations-m01-l11",
    "description": (
        "Learn how to prevent agent sprawl by standardizing source code, turning agents into "
        "reusable services, making deployed agents discoverable through a governed registry, "
        "and controlling access through a centralized Agent Gateway and secure backend."
    ),
    "order": 11,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 6.0,
    "skill_tags": [
        "agent-template-catalog",
        "agent-standardization",
        "agent-registry",
        "agent-as-a-service",
        "a2a",
        "agent-card",
        "registry-record",
        "public-facade",
        "agent-identity",
        "registry-hygiene",
        "agent-gateway",
        "access-control",
        "federated-governance",
        "frontend-backend-security",
        "agent-portal",
        "identity-propagation",
        "ci-cd",
        "agentops",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
        "M01.L08",
        "M01.L09",
        "M01.L10",
    ],

    "lesson": {
        "title": "Sharing and Governing Agents as Services and Reusable Components",
        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "content": r"""
# Sharing and Governing Agents as Services and Reusable Components

> **Lesson:** M01.L11  
> **Source alignment:** Chapter 18 of the supplied Early Release material.  
> This lesson focuses on the **social layer of AgentOps**: standardizing agents, discovering them, and governing who can use them.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why agent success creates new operational problems at enterprise scale.
- Define the Snowflake Problem, Discovery Gap, and Access Control Sprawl.
- Explain why governance must begin at source-code creation rather than deployment time.
- Explain the purpose of an Agent Template Catalog.
- Compare Simple Chat, RAG Agent, and Action Agent templates.
- Explain why standard repository structure improves maintainability, security, testing, and collaboration.
- Explain the role of `agent.py`, `context.py`, `prompts.py`, `examples.py`, `tools.py`, evaluation, monitoring, tests, and deployment directories.
- Explain the role of `.well-known/agent.json` and the Agent Card.
- Explain recursive sub-agent structure inside one externally discoverable service.
- Explain why one externally visible Agent Card can represent an internal multi-agent system.
- Design metadata for an Agent Template Catalog.
- Trace the four-step template instantiation workflow: discovery, selection/input, hydration, pipeline initialization.
- Distinguish the generic template from the instantiated project.
- Explain the Center of Excellence vs business-unit ownership model.
- Explain how a deployed agent becomes an Agent-as-a-Service.
- Distinguish the Agent Template Catalog from the Agent Registry.
- Explain why the Registry is a live service directory rather than a source-code library.
- Explain why the standard A2A Agent Card is insufficient for enterprise governance.
- Explain the Registry Record wrapper pattern.
- Define Agent Identity, Internal Code Name, Governance Metadata, and Public Facade Definition.
- Explain why end users should not receive internal service URLs or authentication details.
- Explain registry hygiene: automated birth, pruning/zombie detection, and owner-maintained metadata.
- Trace secure frontend → backend → registry → agent interaction.
- Explain the Agent Gateway as a policy engine answering "Can Subject A access Agent B?"
- Distinguish user-to-agent, group-to-agent, and agent-to-agent policies.
- Explain the performance and security value of agent-to-agent allow-lists.
- Compare central-admin, agent-owner, group-automation, and federated-hybrid governance.
- Explain birthright access vs subscription-marketplace access.
- Compare configuration-as-code, database/policy-store, and cloud-IAM gateway implementations.
- Explain the role of the Agent Registry Portal for consumers, owners, and the platform.
- Explain infrastructure maintenance vs policy maintenance.
- Explain policy drift and periodic access review.
- Trace the Marketing Router → Sales Analytics example using explicit agent identities.
- Explain the identity gap between service identity and human user identity.
- Explain why user identity propagation and delegated authorization are still required after gateway authorization.
- Trace the complete creation, governance, and usage lifecycles.
- Explain how the Template Catalog, Registry, Gateway, Portal, and backend fit together into one AgentOps system.

---

## 1. Success creates a new scaling problem

A platform may begin with one tutor.

Then it grows into a digital workforce:

```text
Math Agent
Grammar Agent
Data Science Agent
HR Agent
Legal Agent
Curriculum Agent
```

At that point, the challenge is no longer:

```text
"Can we build an agent?"
```

It becomes:

```text
"Can we manage hundreds of agents safely and consistently?"
```

The source identifies three major problems that emerge as the fleet grows.

[[IMAGE_NEEDED: Agent sprawl before governance | Many teams creating separate Math, Grammar, SQL, HR, and Legal agents with inconsistent code structures and direct links | Learner should see why successful adoption creates governance pressure]]

---

## 2. The Snowflake Problem

A Snowflake Agent is unique in all the wrong ways.

Two agents may solve the same problem but differ in:

- logging,
- secret handling,
- configuration,
- deployment,
- testing,
- monitoring,
- directory layout.

Example:

```text
Math Agent A -> secure config + cloud logging
Math Agent B -> hard-coded API key + local text logs
```

Both "work."

Only one is safe and maintainable.

### Why this is expensive

Snowflakes increase:

```text
debugging cost
security risk
review effort
deployment complexity
onboarding time
```

### Core principle

> Standardization should begin before the first line of custom business logic is written.

---

## 3. The Discovery Gap

A team may spend weeks rebuilding an agent that already exists elsewhere.

Example:

```text
Student Success team:
builds Natural Language -> SQL Agent

Data Engineering team:
already has production-grade NL -> SQL Agent
```

The problem is not technical capability.

It is discoverability.

This creates:

```text
duplicate cost
duplicate security review
lower quality
fragmented ownership
```

A registry solves this at runtime.

A template catalog solves a related problem at creation time.

---

## 4. Access Control Sprawl

As the number of users and agents grows, access relationships explode.

Questions appear:

```text
Which students may use which tutors?
Which faculty may use which grading agents?
Which agents may call which other agents?
Which internal services should never be user-visible?
```

Hard-coding permissions inside each agent does not scale.

Access policy must become a separate governed system.

---

## 5. The social layer of AgentOps

The source introduces three major components:

```text
Agent Template Catalog
Agent Registry
Agent Gateway
```

### Agent Template Catalog

Standardizes creation.

### Agent Registry

Enables discovery of deployed agents.

### Agent Gateway

Controls access to those agents.

Together they form the social layer:

```text
how agents are born
how agents are found
who is allowed to interact with them
```

[[IMAGE_NEEDED: AgentOps social layer | Template Catalog -> deployed Agent-as-a-Service -> Agent Registry -> Agent Gateway -> authorized consumers | Learner should see creation, discovery, and governance as separate but connected responsibilities]]

{{exercise:M01.L11.EX01}}

---

## 6. Agent Template Catalog

Governance should begin at source code.

Instead of telling every developer:

```text
"Please remember all security, monitoring, and deployment standards."
```

the platform gives them a pre-approved blueprint.

The Agent Template Catalog is:

```text
a library of production-ready scaffolding
```

The source uses the "Cookie Cutter" analogy.

Every new agent begins with the same basic DNA.

---

## 7. Simple Chat template

A Simple Chat template is suitable for:

```text
Math Tutor
Grammar Tutor
basic conversational assistant
```

It may already include:

- conversation memory,
- basic guardrails,
- standard prompts,
- tests,
- deployment skeleton.

The developer then focuses on domain behavior.

---

## 8. RAG Agent template

A RAG template is appropriate when the agent must answer from a knowledge base.

It may include:

```text
vector database integration
embeddings
document pipeline
retrieval
grounded-answer pattern
```

Example:

```text
Curriculum Agent
```

The template removes repetitive setup.

The developer adds the actual syllabus/data.

---

## 9. Action Agent template

An Action Agent calls tools or external services.

It may include:

```text
A2A implementation
error handling
authentication flow
tool structure
```

Examples:

```text
Calendar Agent
Drive Agent
Workflow Agent
```

This template gives action-oriented agents a secure starting point.

---

## 10. A standardized agent repository

The source proposes a "Gold Standard" structure.

Conceptually:

```text
<agent_name>/
├── .well-known/
│   └── agent.json
├── deploy/
├── evaluation/
├── monitoring/
├── sub_agents/
├── tests/
├── utils/
├── agent.py
├── context.py
├── examples.py
├── prompts.py
├── tools.py
└── requirements.txt
```

The exact names are source-specific.

The architectural principle is:

> Separate concerns so every agent project looks familiar.

[[IMAGE_NEEDED: Standardized agent repository tree | Display the root folders/files with short annotations: Agent Card, deploy, evaluation, monitoring, sub-agents, tests, core logic | Learner should be able to mentally map where each responsibility lives]]

---

## 11. Core agent files

The source separates several concerns.

### `agent.py`

Main orchestration and agent logic.

### `context.py`

Session state and context-window management.

### `prompts.py`

System instructions and persona definitions.

### `examples.py`

Few-shot behavior examples.

This is useful because prompt engineers can modify examples/prompts without touching core orchestration code.

---

## 12. Tool and utility layer

### `tools.py`

Defines tools for simpler agents.

More complex projects may replace it with a full `tools/` hierarchy.

### `utils/helper.py`

Contains generic helpers.

Examples:

```text
date formatting
string utilities
common transformations
```

This keeps domain agent logic clean.

---

## 13. Protocol layer: `.well-known/agent.json`

The source calls this one of the most important interoperability files.

The Agent Card describes the deployed service.

It may include:

```text
name
description
version
capabilities
endpoint
authentication
skills
```

Placing it under:

```text
.well-known/
```

supports standard discovery.

The Agent Registry can read these capabilities without manual re-entry.

---

## 14. Sub-agents can follow the same structure recursively

A complex agent may contain:

```text
Supervisor
Geometry Agent
Algebra Agent
Calendar Agent
```

The source's template allows `sub_agents/` to repeat a smaller version of the same structure.

This gives a "fractal" design:

```text
parent agent
  contains
child agents
  using
similar conventions
```

Each child can be tested in isolation.

---

## 15. One discoverable service can contain many internal agents

The entire repository may run as one runtime/container.

Externally:

```text
one Agent Card
one service identity
one endpoint
```

Internally:

```text
Supervisor
+ several sub-agents
```

This is powerful because enterprise consumers do not need to understand internal orchestration.

### Encapsulation principle

> Expose a stable service boundary; hide internal multi-agent complexity.

---

## 16. Standardization creates predictability

If every agent follows the same structure, a developer knows where to find:

```text
prompts
context logic
tools
tests
evaluation
deployment config
```

That improves:

- code review,
- onboarding,
- debugging,
- security review,
- shared ownership.

Predictability is a major operational advantage.

---

## 17. What belongs in the Template Catalog?

A catalog entry should contain enough information to help a developer choose the correct blueprint.

The source includes metadata such as:

```text
template name
description
repository location
owner/maintainer
version
performance/evaluation information
```

Example:

```text
template-rag-agent-python
```

with a description explaining the intended use.

---

## 18. Where can the catalog live?

For a small organization:

```text
templates.json
in a central repository
```

For a larger organization:

```text
database
internal developer portal
platform catalog
```

The implementation can vary.

The conceptual contract stays the same:

```text
discover standardized blueprints
```

---

## 19. From catalog to codebase

The source describes a four-step workflow.

```text
1. Discovery
2. Selection & Input
3. Hydration
4. Pipeline Initialization
```

This should feel like using an internal product catalog.

---

## 20. Step 1 — Discovery

The developer searches for a capability.

Example:

```text
"SQL"
```

and finds:

```text
Natural Language to SQL Template
```

The template is chosen based on the business need.

---

## 21. Step 2 — Selection and input

The developer supplies project-specific metadata.

Examples:

```text
new agent name
target project/environment
owning team
```

This metadata feeds automation.

---

## 22. Step 3 — Hydration

Automation clones/copies the blueprint into a new dedicated repository.

At this moment:

```text
generic template
```

becomes:

```text
specific project instance
```

The source mentions Infrastructure-as-Code-style automation as one possible mechanism.

The exact technology is not the durable idea.

---

## 23. Step 4 — Pipeline initialization

The new repository should not merely contain code.

Its CI/CD pipeline should also be initialized.

That pipeline can later handle:

```text
testing
evaluation
container build
deployment
registration
```

This links standard code structure to standard operations.

[[IMAGE_NEEDED: Agent template instantiation workflow | Developer searches catalog -> selects template and metadata -> platform hydrates new repo -> CI/CD pipeline initialized -> custom development begins | Learner should remember the four-step flow]]

{{exercise:M01.L11.EX02}}

---

## 24. Customize the instance, not the template

After hydration, the developer works on the new project.

They may add:

### Logic

Example:

```text
student grades database schema
```

### Tools

Example:

```text
export results to CSV
```

### Tests

Example:

```text
department-specific privacy edge cases
```

The template provides the skeleton.

The team provides the domain knowledge.

---

## 25. CoE standards, business-unit implementation

The source creates an important ownership balance.

### Center of Excellence / Platform Team

Owns:

```text
templates
platform automation
shared standards
```

### Business Unit

Owns:

```text
domain implementation
custom behavior
department-specific tests
```

This supports both consistency and local expertise.

---

## 26. From repository to Agent-as-a-Service

A repository is not yet reusable at runtime.

After deployment, the agent becomes:

```text
an independent service
```

with:

```text
endpoint
identity
version
lifecycle
```

The source calls this transformation Agent-as-a-Service.

This is the runtime foundation for reuse.

---

## 27. Agents as microservices

Whether simple or internally multi-agent, each deployed agent can appear as one service.

Examples:

```text
Grammar Checker
Math Tutor
Curriculum Planner
```

Each has:

- its own endpoint,
- its own lifecycle,
- its own identity.

This makes independent deployment and discovery possible.

---

## 28. Deployment creates a discovery problem

Suppose the Math Tutor is running somewhere internally.

How does another service find it?

Hard-coding:

```text
https://math-service-v1.internal
```

everywhere is brittle.

The Agent Registry solves this.

---

## 29. Agent Registry

The source compares the Agent Registry to a university staff directory.

It is:

```text
a centralized live database of deployed agents
```

When an agent comes online, its pipeline registers:

```text
who it is
where it is
what it can do
whether it is active
```

Consumers then query the registry instead of hard-coding service URLs.

---

## 30. Template Catalog vs Agent Registry

This distinction is essential.

### Template Catalog

Think:

```text
Recipe
Blueprint
Source code
```

Primary consumer:

```text
developer building a new agent
```

### Agent Registry

Think:

```text
Meal
Running service
Live endpoint
```

Primary consumer:

```text
application or another agent
```

### Lifecycle

```text
build from Catalog
deploy
operate through Registry
```

[[IMAGE_NEEDED: Template Catalog vs Agent Registry | Left: Recipe/Blueprint with repo URL, owner, version -> used by developers; right: Live Service Directory with endpoint, Agent Card, health/status -> used by apps/agents | Learner should never confuse creation assets with running services]]

---

## 31. Why the Agent Card is not enough for enterprise governance

A standard Agent Card is designed for interoperability.

It is like a business card.

It may contain:

```text
name
description
version
capabilities
URL
authentication methods
```

But enterprise operations need more.

Examples:

```text
immutable internal identity
cost center
compliance level
owner
public/private field policy
internal code name
```

These do not belong in the public protocol contract.

---

## 32. Registry Record wrapper pattern

The source solves this by wrapping the Agent Card.

Conceptually:

```text
Registry Record
├── Agent Card
└── Enterprise Metadata
```

Do not modify the standard protocol object merely to store enterprise-specific fields.

Wrap it.

This preserves interoperability and adds governance.

[[IMAGE_NEEDED: Registry Record wrapper | Inner Agent Card containing standard protocol fields, surrounded by enterprise metadata: identity, code name, owner, compliance, cost center, public facade | Learner should see standard protocol and enterprise governance as separate layers]]

---

## 33. Agent Identity

The source introduces a stable immutable identity.

Example:

```text
identity-math-tutor-001
```

This identity should remain stable even if:

```text
URL changes
version changes
display name changes
```

This is useful for:

```text
access policy
audit
ownership
security
```

### Key principle

> Human-readable names can change; security identities should remain stable.

---

## 34. Internal Code Name

The display name may change for branding.

Example:

```text
Personal Assistant
→ My University Buddy
```

But CI/CD and routing should not break.

An internal code name such as:

```text
personal-assistant-agent
```

stays stable.

This separates:

```text
product naming
```

from:

```text
system identity
```

---

## 35. Governance metadata

Enterprise metadata may include:

```text
owner
cost center
compliance classification
business unit
support contact
lifecycle state
```

These fields matter for operations.

They do not need to be exposed to ordinary end users.

---

## 36. Public Facade Definition

A powerful part of the Registry Record is the Public Facade.

It defines:

```text
which fields are visible
to which audience
```

Example:

### End user

May see:

```text
name
description
icon
```

### Developer

May also see:

```text
skills
input schema
version
```

### Backend/platform

May see:

```text
internal URL
auth metadata
service identity
```

### Principle

> Discovery does not imply disclosure of internal infrastructure.

---

## 37. Registry hygiene

A registry is useful only if it is trusted.

If search returns:

```text
old
dead
duplicate
deprecated
```

agents, users stop relying on it.

The source describes lifecycle hygiene.

---

## 38. Automated registration: birth

When CI/CD deploys an agent:

```text
deployment
   ↓
automatic registry registration
```

This is better than manually updating a spreadsheet.

The registry reflects what actually runs.

---

## 39. Automated pruning: zombie agents

A "Zombie Agent" is a service that was deployed but later abandoned.

The source suggests health/liveness policies.

If an agent:

```text
fails heartbeat/health checks
for too long
```

then the registry may:

```text
mark inactive
or
remove/deprecate it
```

Treat exact time windows from the source as configurable examples.

---

## 40. Human ownership still matters

Automation can validate service health.

It cannot always maintain human meaning.

Agent owners should update:

```text
description
business purpose
public facade
ownership metadata
```

when capabilities change.

Good registry hygiene requires:

```text
automation + accountability
```

---

## 41. The registry must support frontend/backend separation

The source returns to the secure runtime architecture.

### Frontend

Untrusted browser environment.

### Backend

Trusted environment containing:

```text
internal URLs
credentials
routing logic
authorization
```

The frontend should never receive the full Registry Record.

---

## 42. Safe frontend discovery flow

A student loads the portal.

The frontend asks the backend:

```text
Which agents may I see?
```

The backend queries the Registry.

Then it applies:

```text
access policy
+
Public Facade
```

The frontend receives only safe fields.

Example:

```json
{
  "name": "Math Tutor",
  "description": "Helps with Algebra",
  "icon": "..."
}
```

Not:

```text
internal URL
service ID
auth scheme
```

---

## 43. The browser should select by public identifier, not internal URL

The user clicks:

```text
Math Tutor
```

The browser sends:

```text
agent public identifier/name
```

The backend resolves that to the internal Registry Record.

Then the backend:

- authenticates,
- opens the service session,
- proxies messages.

This preserves infrastructure secrecy.

[[IMAGE_NEEDED: Secure Agent Registry runtime flow | Browser requests agents -> Backend queries Registry -> Gateway filters -> Public Facade sanitizes -> Browser sees safe list -> user selects public ID -> Backend resolves internal endpoint and opens agent session | Learner should see why URLs and auth stay server-side]]

---

## 44. Agent Gateway

The Registry answers:

```text
Who exists?
```

The Gateway answers:

```text
Who may access whom?
```

At its core it is a policy engine.

Question:

```text
Can Subject A access Agent B?
```

This decouples access rules from agent source code.

---

## 45. User-to-Agent policies

Example:

```text
Student A
   may use
Math Tutor
```

This is the standard human interaction case.

The policy can be based on:

- individual user,
- role,
- group,
- organization.

---

## 46. Group-to-Agent policies

Example:

```text
Faculty group
   may use
Grading Assistant
```

This is more scalable than listing every user individually.

When a new member joins the group, access can be inherited automatically.

---

## 47. Agent-to-Agent policies

Example:

```text
Concierge Router
   may call
Schedule Manager
```

This is important in large multi-agent systems.

A Router capable of finding 1000 agents should not automatically have permission to invoke all 1000.

Allow-lists create a Circle of Trust.

Benefits:

```text
smaller search space
better performance
least privilege
better predictability
```

---

## 48. Who decides access?

Defining a policy engine is only half the problem.

The organizational question is:

```text
Who is allowed to change the policy?
```

The source presents several governance models.

---

## 49. Central administrator model

One administrator controls all access.

Works for:

```text
small pilots
few agents
```

Fails at enterprise scale because the administrator becomes a bottleneck.

---

## 50. Agent-owner model

The agent owner directly manages allow-lists.

This distributes authority.

But it can turn developers into:

```text
manual access-ticket managers
```

That reduces engineering velocity.

---

## 51. Group automation model

Access follows existing organization groups.

Example:

```text
Class 101
→ Agent 101
```

Advantage:

```text
high automation
```

Limitation:

```text
rigid exceptions
```

Cross-team access becomes difficult.

---

## 52. Federated Hybrid governance

The source presents this as a mature model.

It combines:

```text
baseline automated access
+
request/approval marketplace
+
owner accountability
```

### Birthright access

Low-risk/default agents may automatically be available to groups.

### Subscription marketplace

Sensitive/specialized agents require explicit request.

### Owner accountability

The owner approves/denies non-default access.

This balances:

```text
scale
speed
control
```

[[IMAGE_NEEDED: Federated Agent Gateway governance | Baseline group policies grant common agents automatically; specialized agents appear in marketplace; request routes to Agent Owner; approval updates Gateway policy | Learner should see how automation and owner review coexist]]

{{exercise:M01.L11.EX03}}

---

## 53. Three Agent Gateway implementation strategies

The source describes three broad patterns:

```text
Config as Code
Policy Database / Policy Store
Cloud IAM
```

The architectural function matters more than a specific product.

---

## 54. Startup approach: Configuration as Code

For a pilot:

```yaml
allow:
  - subject: group:students
    resource: agent:math-tutor
```

Advantages:

```text
simple
version-controlled
low infrastructure overhead
```

Limitations:

```text
changes may require commit/redeploy
weak dynamic workflows
limited access history
```

Useful for small systems.

---

## 55. Enterprise database/policy-store approach

At larger scale, policies may live in:

```text
relational database
policy engine
policy store
```

The Gateway becomes a service.

Advantages:

```text
real-time updates
custom policy logic
multi-cloud/on-prem flexibility
```

Costs:

```text
engineering burden
security burden
operations burden
```

---

## 56. Cloud-native IAM approach

Agents can map to cloud identities/service accounts.

Policies can use provider IAM.

Advantages:

```text
strong enforcement
auditing
managed security infrastructure
```

Challenges:

```text
complexity
cloud expertise
provider coupling
central IT dependency
```

The correct choice depends on organizational maturity and platform topology.

---

## 57. Agent Registry Portal

Humans need a usable interface over Registry + Gateway.

The Portal serves several roles.

### Consumer view

Feels like an app store:

```text
search
browse
connect
request access
```

### Owner view

Feels like a management dashboard:

```text
pending requests
approve
deny
usage/access view
```

### System role

Acts as control plane by updating Gateway policy.

---

## 58. Gateway ownership is split

### CoE / Platform Team

Maintains:

```text
gateway availability
policy infrastructure
security
performance
```

### Agent Owner

Maintains:

```text
who should retain access
specialized approval decisions
```

The source uses a helpful analogy:

```text
CoE = locksmith
Owner = keyholder
```

---

## 59. Policy drift

Access can become stale.

Examples:

```text
employee changes team
student changes class
project ends
agent is deprecated
```

If access remains, privilege accumulates.

The source proposes periodic access review.

Owners inspect:

```text
which users
which groups
which agents
```

still have access and revoke what is no longer needed.

---

## 60. Real-world example: Marketing Router requests agent access

Suppose a Marketing Campaign Manager needs:

```text
Sales Analytics Agent
Retention Analytics Agent
```

It should not copy their code.

Instead:

```text
Marketing Router
   requests access
through Portal/Gateway
```

The Sales owner approves.

The Gateway creates an explicit A2A rule:

```text
source:
identity-marketing-router

target:
identity-sales-analytics

action:
allow invoke
```

This composes services safely.

---

## 61. Service identity answers only part of the security question

The Gateway can verify:

```text
Marketing Agent is allowed to call Sales Agent
```

That proves the service relationship.

But it does not answer:

```text
Which human user caused the request?
```

This is the identity gap.

---

## 62. User identity still matters downstream

Suppose:

```text
Alice
→ Marketing Router
→ Sales Agent
→ Revenue Database
```

If Sales Agent always uses its own powerful service account, the database may see only:

```text
Sales Agent
```

and not:

```text
Alice
```

That can bypass row-level or user-specific authorization.

---

## 63. Authentication, authorization, and identity propagation

The source previews three further needs.

### Authentication

Who is the human user?

### Authorization / delegation

Has that user authorized the agent to act on their behalf?

### Identity propagation

Can downstream systems know:

```text
this action was performed
by Agent X
on behalf of User Y
```

This becomes critical for:

- row-level security,
- audit,
- least privilege.

The next chapter deepens this topic.

---

## 64. The complete lifecycle has three streams

The source combines everything into three parallel workflows.

```text
Creation
Governance
Usage
```

Understanding these streams gives a complete mental model of the platform.

[[IMAGE_NEEDED: Three-stream AgentOps lifecycle | Creation stream from Template Catalog to hydrated repo/deployment; Governance stream through Portal and Gateway policy; Usage stream from End User -> Frontend -> Backend -> filtered Registry -> selected Agent | Learner should see all three lifecycles operating together]]

---

## 65. Creation lifecycle

The AI Engineer:

```text
discovers template
selects it
hydrates new repository
initializes pipeline
customizes implementation
deploys service
registers agent
```

The resulting agent is standardized from birth.

---

## 66. Governance lifecycle

Admin/automation defines baseline access.

For specialized access:

```text
consumer requests
owner approves
Gateway updates policy
```

This controls who can reach the agent.

---

## 67. Usage lifecycle

The user:

```text
logs in
frontend connects to backend
backend queries Registry
Gateway filters authorized agents
Public Facade removes sensitive fields
user selects agent
backend resolves service
backend opens session
backend proxies interaction
```

This gives a simple user experience over a governed backend.

---

## 68. Why all three lifecycle streams are necessary

If you have only creation:

```text
agents are standardized
but hard to discover/use
```

If you have only Registry:

```text
agents are discoverable
but not necessarily secure
```

If you have only Gateway:

```text
access is controlled
but service creation may still be chaotic
```

Together:

```text
Template Catalog
+ Registry
+ Gateway
```

create a scalable operating model.

---

## 69. Production checklist

### Standardization

- template catalog exists,
- templates are owned/versioned,
- standard repo structure,
- shared test/evaluation/deployment layout.

### Interoperability

- Agent Card exists,
- service boundary is stable,
- internal sub-agents are encapsulated.

### Registry

- automatic registration,
- immutable identity,
- internal code name,
- governance metadata,
- Public Facade,
- health/liveness state.

### Hygiene

- owner maintained,
- zombie detection,
- deprecation lifecycle,
- periodic metadata review.

### Access

- user/group/agent policy,
- least privilege,
- agent-to-agent allow-list,
- subscription workflow where needed.

### Frontend safety

- backend resolves internal endpoints,
- browser receives sanitized agent metadata only.

### Gateway operations

- explicit governance model,
- policy review,
- audit trail,
- drift detection.

### Identity

- service identity defined,
- human identity/delegation considered for downstream resources.

{{exercise:M01.L11.EX04}}

---

## 70. Source-specific details to re-check

This is Early Release material.

Treat exact implementation examples as source-specific:

- exact folder names,
- cloud-provider products,
- exact IAM syntax,
- exact liveness/heartbeat periods,
- specific internal developer portal examples,
- specific Infrastructure-as-Code tools,
- Agent Card field names,
- exact deployment layout.

The durable principles are:

```text
standardize creation
separate blueprint from running service
wrap standard protocol metadata with enterprise metadata
hide internal plumbing from end users
treat identity as stable
keep registry data fresh
separate discovery from permission
centralize policy
use least privilege
preserve user identity downstream
```

---

## 71. Complete mental model

The full system is:

```text
Agent Template Catalog
        ↓
standardized project
        ↓
CI/CD
        ↓
Agent-as-a-Service
        ↓
Agent Registry
        ↓
Registry Record
   ├── Agent Card
   └── Enterprise Metadata
        ↓
Agent Gateway
        ↓
authorized/sanitized discovery
        ↓
Backend
        ↓
Frontend / other Agents
```

The Template Catalog answers:

```text
How should I build an agent?
```

The Registry answers:

```text
Which agents are currently running?
```

The Gateway answers:

```text
Who is allowed to use which agent?
```

The Backend answers:

```text
How do I connect safely without exposing infrastructure?
```

And identity propagation eventually answers:

```text
On whose behalf is this action being performed?
```

That is the foundation for a reusable, governable digital workforce.

---

## Important misconceptions

### Misconception 1
> "Governance starts after deployment."

No. The source starts governance at source-code creation through standardized templates.

### Misconception 2
> "A Template Catalog and Agent Registry are the same."

No. One stores blueprints/source scaffolding; the other stores live deployed services.

### Misconception 3
> "Every internal sub-agent needs to be exposed as an independent external service."

No. A multi-agent system can be encapsulated behind one Agent Card/service boundary.

### Misconception 4
> "The Agent Card should store all enterprise metadata."

No. Wrap it in a richer Registry Record instead of changing the standard protocol object.

### Misconception 5
> "Display name is a strong security identity."

No. Display names can change. Use a stable immutable Agent Identity.

### Misconception 6
> "The browser should receive the agent's internal service URL."

No. The backend should resolve internal infrastructure and expose only safe Public Facade fields.

### Misconception 7
> "If an agent exists in the Registry, every user can access it."

No. Discovery and permission are separate concerns.

### Misconception 8
> "Agent-to-agent permissions are only about security."

No. Restricting the callable agent set also reduces search space and improves predictability/performance.

### Misconception 9
> "One central admin is the best governance model at every scale."

No. It can become a major enterprise bottleneck.

### Misconception 10
> "Group-based access solves every governance problem."

No. It can be too rigid for cross-team or exception-based access.

### Misconception 11
> "Federated governance means no central standards."

No. It combines automation/common standards with local owner accountability.

### Misconception 12
> "Registry records stay correct automatically forever."

No. Registry hygiene requires health automation and owner-maintained metadata.

### Misconception 13
> "A browser disconnect or rebrand should change the Agent Identity."

No. Operational identity should remain stable across cosmetic or endpoint changes.

### Misconception 14
> "If Agent A is allowed to call Agent B, downstream data authorization is solved."

No. User identity and delegated authorization may still need to propagate to the final data system.

### Misconception 15
> "Agent Registry Portal is just a search page."

No. It also supports access requests, owner approvals, and control-plane policy updates.

---

## Key terminology

| Term | Meaning |
|---|---|
| Snowflake Agent | Non-standard agent implementation that is expensive to maintain |
| Discovery Gap | Failure to find/reuse existing agents |
| Access Control Sprawl | Rapid growth of user/agent permission relationships |
| Agent Template Catalog | Library of approved agent source-code blueprints |
| Cookie Cutter | Source analogy for reusable standardized templates |
| Simple Chat Template | Lightweight conversational-agent blueprint |
| RAG Agent Template | Blueprint for retrieval-grounded agents |
| Action Agent Template | Blueprint for tool-using/action-oriented agents |
| Agent Card | Standard A2A capability/endpoint metadata |
| `.well-known/agent.json` | Source-described conventional location for Agent Card |
| Hydration | Creating a new project repository from a generic template |
| Agent-as-a-Service | Deployed agent exposed as an independent runtime service |
| Agent Registry | Central live directory of deployed agents |
| Registry Record | Enterprise wrapper containing Agent Card plus governance metadata |
| Agent Identity | Stable immutable identity used for policy and audit |
| Internal Code Name | Stable system identifier independent of branding |
| Governance Metadata | Operational fields such as owner, compliance, cost center |
| Public Facade | Policy defining which Registry fields can be exposed to each audience |
| Registry Hygiene | Keeping records current, active, and trustworthy |
| Zombie Agent | Abandoned/dead service still present in Registry |
| Agent Gateway | Policy layer controlling consumer-to-agent access |
| User-to-Agent Policy | Permission from a specific user to an agent |
| Group-to-Agent Policy | Permission from a user group to an agent |
| Agent-to-Agent Policy | Permission from one agent identity to another |
| Circle of Trust | Curated set of agents another agent may invoke |
| Birthright Access | Default group-based access assigned automatically |
| Subscription Marketplace | Request/approval flow for non-default agent access |
| Policy Drift | Access rules becoming stale over time |
| Identity Propagation | Carrying user/service identity through downstream calls |
| Delegation | User authorizes an agent to act on their behalf |

---

## Self-check

1. What are the three scaling problems introduced at the start of the chapter?
2. What is the Snowflake Problem?
3. What is the Discovery Gap?
4. What is Access Control Sprawl?
5. Why should governance begin with source-code creation?
6. What is the purpose of the Agent Template Catalog?
7. What is the difference between Simple Chat, RAG, and Action templates?
8. What are the main sections of the standardized repository?
9. What belongs in `context.py`?
10. Why separate `examples.py` from core agent logic?
11. What is the role of `.well-known/agent.json`?
12. Why can one Agent Card represent multiple internal sub-agents?
13. What metadata belongs in a Template Catalog?
14. What are the four template instantiation steps?
15. What does hydration mean?
16. Why initialize CI/CD during instantiation?
17. What does the CoE own?
18. What does the business unit own?
19. When does an agent become Agent-as-a-Service?
20. What is the difference between the Template Catalog and Agent Registry?
21. Why should service URLs not be hard-coded into consumers?
22. Why is the Agent Card insufficient as the full enterprise Registry record?
23. What is the Registry Record wrapper pattern?
24. What is Agent Identity?
25. Why separate Agent Identity from display name?
26. Why separate Internal Code Name from branding?
27. What does Public Facade control?
28. Why should end users not see internal URLs/auth schemes?
29. What is Registry hygiene?
30. What is a Zombie Agent?
31. Which lifecycle fields should be automated vs owner-maintained?
32. Why is the browser treated as untrusted territory?
33. What should the frontend receive when listing agents?
34. Why should selection happen through public identifiers?
35. What question does the Agent Gateway answer?
36. What are the three access-policy types?
37. Why should router agents have explicit agent-to-agent allow-lists?
38. What is the central-admin governance model's main weakness?
39. What is the agent-owner model's main weakness?
40. What is the group-automation model's main weakness?
41. How does the Federated Hybrid model work?
42. What is Birthright Access?
43. What is a Subscription Marketplace?
44. How does Config-as-Code implement the Gateway?
45. Why use a database/policy store at enterprise scale?
46. What are the benefits and drawbacks of cloud IAM?
47. What does the Registry Portal provide for consumers?
48. What does it provide for owners?
49. Who maintains Gateway infrastructure?
50. Who maintains agent-specific access policy?
51. What is policy drift?
52. Why perform periodic access review?
53. How does the Marketing Router request access to Sales Analytics?
54. What does the resulting A2A policy contain?
55. What is the difference between service identity and user identity?
56. Why can a powerful service account create a governance hole?
57. What is delegated authorization?
58. What is identity propagation?
59. What are the three lifecycle streams?
60. Trace the Creation lifecycle.
61. Trace the Governance lifecycle.
62. Trace the Usage lifecycle.
63. Why are Template Catalog, Registry, and Gateway all necessary?
64. Which implementation details should be re-verified before production use?

---

## Retain this idea

**A scalable agent ecosystem needs three different forms of governance: standardization at creation time, discovery at runtime, and permission at interaction time. The Agent Template Catalog standardizes how agents are born. The Agent Registry tracks which agents are alive and how they can be reached. The Agent Gateway decides who may interact with them. A secure backend hides internal infrastructure, Public Facades expose only safe metadata, stable Agent Identities anchor policy, and federated governance balances automation with owner accountability. Together, these pieces turn isolated agent projects into a reusable and governable digital workforce.**
""".strip(),

        "sections": [
            {"id": "success-chaos", "title": "Success Creates a New Scaling Problem", "order": 1},
            {"id": "snowflake", "title": "The Snowflake Problem", "order": 2},
            {"id": "discovery-gap", "title": "The Discovery Gap", "order": 3},
            {"id": "access-sprawl", "title": "Access Control Sprawl", "order": 4},
            {"id": "three-pillars", "title": "The Social Layer of AgentOps", "order": 5},
            {"id": "template-catalog", "title": "Agent Template Catalog", "order": 6},
            {"id": "simple-template", "title": "Simple Chat Template", "order": 7},
            {"id": "rag-template", "title": "RAG Agent Template", "order": 8},
            {"id": "action-template", "title": "Action Agent Template", "order": 9},
            {"id": "gold-standard-structure", "title": "A Standardized Agent Repository", "order": 10},
            {"id": "core-files", "title": "Core Agent Files", "order": 11},
            {"id": "tools-utils", "title": "Tool and Utility Layer", "order": 12},
            {"id": "protocol-layer", "title": "Protocol Layer: Agent Card", "order": 13},
            {"id": "sub-agent-structure", "title": "Sub-Agents Can Follow the Same Structure Recursively", "order": 14},
            {"id": "one-service-many-agents", "title": "One Discoverable Service Can Contain Many Internal Agents", "order": 15},
            {"id": "predictability", "title": "Standardization Creates Predictability", "order": 16},
            {"id": "catalog-metadata", "title": "What Belongs in the Template Catalog?", "order": 17},
            {"id": "catalog-storage", "title": "Where Can the Catalog Live?", "order": 18},
            {"id": "instantiation", "title": "From Catalog to Codebase", "order": 19},
            {"id": "discovery", "title": "Step 1 — Discovery", "order": 20},
            {"id": "selection", "title": "Step 2 — Selection and Input", "order": 21},
            {"id": "hydration", "title": "Step 3 — Hydration", "order": 22},
            {"id": "pipeline-init", "title": "Step 4 — Pipeline Initialization", "order": 23},
            {"id": "customizing", "title": "Customize the Instance, Not the Template", "order": 24},
            {"id": "coe-business-unit", "title": "CoE Standards, Business-Unit Implementation", "order": 25},
            {"id": "agent-service", "title": "From Repository to Agent-as-a-Service", "order": 26},
            {"id": "microservice-agents", "title": "Agents as Microservices", "order": 27},
            {"id": "registry-need", "title": "Deployment Creates a Discovery Problem", "order": 28},
            {"id": "registry", "title": "Agent Registry", "order": 29},
            {"id": "catalog-vs-registry", "title": "Template Catalog vs Agent Registry", "order": 30},
            {"id": "agent-card-limit", "title": "Why the Agent Card Is Not Enough", "order": 31},
            {"id": "registry-record", "title": "Registry Record Wrapper Pattern", "order": 32},
            {"id": "agent-identity", "title": "Agent Identity", "order": 33},
            {"id": "code-name", "title": "Internal Code Name", "order": 34},
            {"id": "governance-metadata", "title": "Governance Metadata", "order": 35},
            {"id": "public-facade", "title": "Public Facade Definition", "order": 36},
            {"id": "registry-hygiene", "title": "Registry Hygiene", "order": 37},
            {"id": "birth", "title": "Automated Registration: Birth", "order": 38},
            {"id": "zombies", "title": "Automated Pruning: Zombie Agents", "order": 39},
            {"id": "owner-metadata", "title": "Human Ownership Still Matters", "order": 40},
            {"id": "secure-runtime", "title": "The Registry Must Support Frontend/Backend Separation", "order": 41},
            {"id": "frontend-discovery", "title": "Safe Frontend Discovery Flow", "order": 42},
            {"id": "selection-backend", "title": "Select by Public Identifier, Not Internal URL", "order": 43},
            {"id": "gateway", "title": "Agent Gateway", "order": 44},
            {"id": "user-agent", "title": "User-to-Agent Policies", "order": 45},
            {"id": "group-agent", "title": "Group-to-Agent Policies", "order": 46},
            {"id": "agent-agent", "title": "Agent-to-Agent Policies", "order": 47},
            {"id": "policy-governance", "title": "Who Decides Access?", "order": 48},
            {"id": "central-admin", "title": "Central Administrator Model", "order": 49},
            {"id": "owner-control", "title": "Agent-Owner Model", "order": 50},
            {"id": "group-automation", "title": "Group Automation Model", "order": 51},
            {"id": "federated-hybrid", "title": "Federated Hybrid Governance", "order": 52},
            {"id": "gateway-implementations", "title": "Three Agent Gateway Implementation Strategies", "order": 53},
            {"id": "config-as-code", "title": "Startup Approach: Configuration as Code", "order": 54},
            {"id": "policy-db", "title": "Enterprise Database / Policy Store", "order": 55},
            {"id": "cloud-iam", "title": "Cloud-Native IAM", "order": 56},
            {"id": "portal", "title": "Agent Registry Portal", "order": 57},
            {"id": "gateway-ownership", "title": "Gateway Ownership Is Split", "order": 58},
            {"id": "policy-drift", "title": "Policy Drift", "order": 59},
            {"id": "developer-journey", "title": "Marketing Router Access Example", "order": 60},
            {"id": "service-identity", "title": "Service Identity Answers Only Part of the Security Question", "order": 61},
            {"id": "user-identity", "title": "User Identity Still Matters Downstream", "order": 62},
            {"id": "delegated-auth", "title": "Authentication, Authorization, and Identity Propagation", "order": 63},
            {"id": "complete-lifecycle", "title": "The Complete Lifecycle Has Three Streams", "order": 64},
            {"id": "creation-lifecycle", "title": "Creation Lifecycle", "order": 65},
            {"id": "governance-lifecycle", "title": "Governance Lifecycle", "order": 66},
            {"id": "usage-lifecycle", "title": "Usage Lifecycle", "order": 67},
            {"id": "why-all-three", "title": "Why All Three Lifecycle Streams Are Necessary", "order": 68},
            {"id": "production-checklist", "title": "Production Checklist", "order": 69},
            {"id": "source-boundaries", "title": "Source-Specific Details to Re-Check", "order": 70},
            {"id": "complete-model", "title": "Complete Mental Model", "order": 71},
        ],
    },

    "exercises": [
        {
            "id": "M01.L11.EX01",
            "title": "Diagnose Agent Sprawl",
            "lesson_code": "M01.L11",
            "section_id": "three-pillars",
            "placement": "after_section",
            "description": "Map enterprise agent problems to the correct governance component.",
            "instructions": (
                "For each problem, classify it as Snowflake Problem, Discovery Gap, or Access Control Sprawl:\n"
                "1. Three teams built separate SQL agents.\n"
                "2. Every agent stores secrets differently.\n"
                "3. A student can see the HR Agent.\n"
                "4. A developer cannot find an existing RAG agent.\n"
                "Then state whether Template Catalog, Registry, or Gateway is the primary fix."
            ),
            "expected_output": "A four-row diagnosis table with governance component.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agentops", "governance", "architecture"],
        },
        {
            "id": "M01.L11.EX02",
            "title": "Design an Agent Template",
            "lesson_code": "M01.L11",
            "section_id": "pipeline-init",
            "placement": "after_section",
            "description": "Create a standardized blueprint for a reusable enterprise agent.",
            "instructions": (
                ("1. Design a 'Customer Support RAG Agent' template.\n"
                 '2. Define repository structure, Agent Card, context, prompts, examples, tools, tests, evaluation dataset, monitoring placeholder, deployment pipeline, owner, version, and template metadata.\n'
                 '3. Then describe Discovery -> Selection -> Hydration -> Pipeline Initialization.')
            ),
            "expected_output": "A template specification plus instantiation workflow.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agent-template-catalog", "standardization", "ci-cd"],
        },
        {
            "id": "M01.L11.EX03",
            "title": "Design a Federated Agent Gateway",
            "lesson_code": "M01.L11",
            "section_id": "federated-hybrid",
            "placement": "after_section",
            "description": "Balance default access, request-based access, and owner accountability.",
            "instructions": (
                "Design access for these agents: Campus Guide, Math Tutor, Payroll Agent, Research Agent.\n"
                "1. Define Birthright Access groups.\n"
                "2. Define which agents require subscription requests.\n"
                "3. Define who approves each request.\n"
                "4. Add one Agent-to-Agent policy.\n"
                "5. Explain how least privilege reduces the search space for Router Agents."
            ),
            "expected_output": "An access-policy matrix and approval flow.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agent-gateway", "federated-governance", "least-privilege"],
        },
        {
            "id": "M01.L11.EX04",
            "title": "Design the Complete Agent Lifecycle",
            "lesson_code": "M01.L11",
            "section_id": "production-checklist",
            "placement": "after_section",
            "description": "Connect creation, governance, and usage into one end-to-end architecture.",
            "instructions": (
                ('1. Design a Physics Tutor lifecycle.\n'
                 '2. Show: template selection, hydrated repository, CI/CD deployment, registry registration, Registry Record, Public Facade, default/group policy, optional access request, frontend discovery, backend resolution, agent session, and one future downstream identity-propagation requirement.')
            ),
            "expected_output": "A three-stream lifecycle diagram and explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["agent-registry", "agent-gateway", "lifecycle"],
        },
        {
            "id": "M01.L11.EX05",
            "title": "Build a Registry Record",
            "lesson_code": "M01.L11",
            "section_id": "public-facade",
            "placement": "after_section",
            "description": "Separate protocol metadata from enterprise metadata and audience-specific exposure.",
            "instructions": (
                ('1. Create a Registry Record for a Data Science Tutor.\n'
                 '2. Include an inner Agent Card and outer fields for immutable identity, internal code name, owner, compliance level, cost center, lifecycle state, and Public Facade.\n'
                 '3. Define separate fields visible to end users, developers, and backend/platform services.')
            ),
            "expected_output": "A three-audience Registry Record schema.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["registry-record", "public-facade", "agent-identity"],
        },
        {
            "id": "M01.L11.EX06",
            "title": "Choose a Gateway Implementation",
            "lesson_code": "M01.L11",
            "section_id": "cloud-iam",
            "placement": "after_section",
            "description": "Select a gateway implementation based on organizational maturity.",
            "instructions": (
                "Choose Config-as-Code, Policy Database/OPA-style service, or Cloud IAM for:\n"
                "1. Five-agent university pilot.\n"
                "2. Hybrid-cloud enterprise with frequent access changes.\n"
                "3. Cloud-native organization with strong central IAM expertise.\n"
                "For each, compare scalability, flexibility, maintenance, and auditability."
            ),
            "expected_output": "A three-row implementation decision table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["access-control", "policy-engine", "architecture-tradeoffs"],
        },
        {
            "id": "M01.L11.EX07",
            "title": "Find the Identity Gap",
            "lesson_code": "M01.L11",
            "section_id": "delegated-auth",
            "placement": "after_section",
            "description": "Distinguish service authorization from end-user authorization.",
            "instructions": (
                ('1. Trace Alice -> Marketing Router -> Sales Analytics Agent -> Revenue Database.\n'
                 '2. Identify where Agent Gateway authorization applies.\n'
                 "3. Then explain why the database still needs Alice's identity, delegated permission, and an audit trail.\n"
                 "4. Describe the risk of using only the Sales Agent's superuser service account.")
            ),
            "expected_output": "An identity/authorization flow and risk explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["identity-propagation", "delegation", "security"],
        },
    ],

    "quiz": {
        "id": "M01.L11.QZ01",
        "title": "Agent Templates, Registries and Access Governance — Knowledge Check",
        "lesson_code": "M01.L11",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L11.Q01",
                "section_id": "snowflake",
                "question": "What is the Snowflake Problem?",
                "options": [
                    "Agents are implemented inconsistently and become difficult to maintain and secure",
                    "Agents cannot call tools",
                    "All agents share one template",
                    "Users cannot log in",
                ],
                "correct": 0,
                "explanation": "Snowflake agents differ unnecessarily in structure, operations, and security.",
            },
            {
                "id": "M01.L11.Q02",
                "section_id": "discovery-gap",
                "question": "What does the Discovery Gap cause?",
                "options": [
                    "Teams rebuild capabilities that already exist",
                    "Agent Cards become encrypted",
                    "Templates cannot contain prompts",
                    "Gateways stop working",
                ],
                "correct": 0,
                "explanation": "Poor discovery leads to duplication and wasted effort.",
            },
            {
                "id": "M01.L11.Q03",
                "section_id": "template-catalog",
                "question": "What is the main purpose of the Agent Template Catalog?",
                "options": [
                    "Standardize how agents are created",
                    "List live deployed endpoints",
                    "Store user passwords",
                    "Replace the Agent Gateway",
                ],
                "correct": 0,
                "explanation": "It provides approved reusable source-code blueprints.",
            },
            {
                "id": "M01.L11.Q04",
                "section_id": "protocol-layer",
                "question": "What is stored in `.well-known/agent.json` in the source?",
                "options": [
                    "The A2A Agent Card",
                    "The user's password",
                    "The entire registry database",
                    "Only application logs",
                ],
                "correct": 0,
                "explanation": "This is the source-described standard Agent Card location.",
            },
            {
                "id": "M01.L11.Q05",
                "section_id": "one-service-many-agents",
                "question": "How can a complex multi-agent system appear externally?",
                "options": [
                    "As one standardized service with one Agent Card",
                    "Only as hundreds of public URLs",
                    "It cannot be encapsulated",
                    "Only through frontend code",
                ],
                "correct": 0,
                "explanation": "Internal sub-agent complexity can stay behind one service boundary.",
            },
            {
                "id": "M01.L11.Q06",
                "section_id": "instantiation",
                "question": "Which sequence matches template instantiation?",
                "options": [
                    "Discovery -> Selection/Input -> Hydration -> Pipeline Initialization",
                    "Deploy -> Delete -> Discover -> Train",
                    "Register -> Hydrate -> Cancel -> Monitor",
                    "Prompt -> Audio -> Vectorize -> Stop",
                ],
                "correct": 0,
                "explanation": "Those are the four source-described steps.",
            },
            {
                "id": "M01.L11.Q07",
                "section_id": "catalog-vs-registry",
                "question": "What is the primary difference between Template Catalog and Agent Registry?",
                "options": [
                    "Catalog stores blueprints; Registry lists live deployed agents",
                    "They are identical",
                    "Catalog is for users; Registry only stores prompts",
                    "Registry contains no runtime data",
                ],
                "correct": 0,
                "explanation": "One supports creation; the other supports runtime discovery.",
            },
            {
                "id": "M01.L11.Q08",
                "section_id": "registry-record",
                "question": "Why use a Registry Record wrapper?",
                "options": [
                    "To keep the standard Agent Card intact while adding enterprise governance metadata",
                    "To remove Agent Cards",
                    "To expose secrets to users",
                    "To avoid stable identities",
                ],
                "correct": 0,
                "explanation": "Protocol and enterprise metadata belong in separate layers.",
            },
            {
                "id": "M01.L11.Q09",
                "section_id": "agent-identity",
                "question": "What should remain stable even if display name or URL changes?",
                "options": [
                    "Agent Identity",
                    "Marketing name",
                    "Browser icon",
                    "Current session ID",
                ],
                "correct": 0,
                "explanation": "Stable identity is needed for policy and audit.",
            },
            {
                "id": "M01.L11.Q10",
                "section_id": "public-facade",
                "question": "What does the Public Facade control?",
                "options": [
                    "Which registry fields are safe to expose to a specific audience",
                    "The LLM temperature",
                    "The database schema only",
                    "The agent's hidden reasoning",
                ],
                "correct": 0,
                "explanation": "Different audiences can receive different sanitized metadata.",
            },
            {
                "id": "M01.L11.Q11",
                "section_id": "zombies",
                "question": "What is a Zombie Agent?",
                "options": [
                    "An abandoned/dead service that remains in the Registry",
                    "An agent with multiple sub-agents",
                    "An agent using OAuth",
                    "A template that was never used",
                ],
                "correct": 0,
                "explanation": "Registry hygiene should detect and deactivate stale services.",
            },
            {
                "id": "M01.L11.Q12",
                "section_id": "frontend-discovery",
                "question": "What should the browser receive from the Registry flow?",
                "options": [
                    "Only sanitized authorized metadata such as name and description",
                    "Internal service URLs and secrets",
                    "Cloud service-account keys",
                    "All enterprise metadata",
                ],
                "correct": 0,
                "explanation": "The backend filters the Registry Record using access rules and Public Facade.",
            },
            {
                "id": "M01.L11.Q13",
                "section_id": "gateway",
                "question": "What core question does the Agent Gateway answer?",
                "options": [
                    "Can Subject A access Agent B?",
                    "Which prompt is most creative?",
                    "How many tokens are in the model?",
                    "Which CSS style should the portal use?",
                ],
                "correct": 0,
                "explanation": "The Gateway is a policy engine for access.",
            },
            {
                "id": "M01.L11.Q14",
                "section_id": "agent-agent",
                "question": "Why restrict a Router Agent to an allow-listed set of other agents?",
                "options": [
                    "To improve both least-privilege security and routing/search efficiency",
                    "To make it more powerful",
                    "To expose more internal URLs",
                    "To remove access governance",
                ],
                "correct": 0,
                "explanation": "A smaller Circle of Trust reduces risk and search space.",
            },
            {
                "id": "M01.L11.Q15",
                "section_id": "federated-hybrid",
                "question": "What does Federated Hybrid governance combine?",
                "options": [
                    "Baseline automated access with request/approval and owner accountability",
                    "Only one central administrator",
                    "No access controls",
                    "Only static user groups",
                ],
                "correct": 0,
                "explanation": "The model balances automation and flexible owner-reviewed access.",
            },
            {
                "id": "M01.L11.Q16",
                "section_id": "config-as-code",
                "question": "Which gateway implementation best fits a small pilot?",
                "options": [
                    "Configuration as Code",
                    "Complex enterprise policy microservice is always required",
                    "No policy system",
                    "Public hard-coded URLs",
                ],
                "correct": 0,
                "explanation": "Config files can be sufficient at small scale.",
            },
            {
                "id": "M01.L11.Q17",
                "section_id": "policy-db",
                "question": "What is a major advantage of a policy database/service?",
                "options": [
                    "Access policies can update dynamically without redeploying agents",
                    "It requires no maintenance",
                    "It removes the need for security",
                    "It exposes all policies publicly",
                ],
                "correct": 0,
                "explanation": "Dynamic policy changes are a key enterprise benefit.",
            },
            {
                "id": "M01.L11.Q18",
                "section_id": "portal",
                "question": "What does the Agent Registry Portal provide to agent owners?",
                "options": [
                    "A dashboard for access requests and policy decisions",
                    "Only a chat transcript",
                    "Only source-code editing",
                    "Model training infrastructure",
                ],
                "correct": 0,
                "explanation": "Owners can review and approve/deny subscriptions.",
            },
            {
                "id": "M01.L11.Q19",
                "section_id": "policy-drift",
                "question": "Why are periodic access reviews needed?",
                "options": [
                    "Users, teams, and projects change while old permissions may remain",
                    "Agent identities change every hour",
                    "The Registry deletes all access automatically",
                    "Public Facades cannot be updated",
                ],
                "correct": 0,
                "explanation": "Review reduces stale privilege and policy drift.",
            },
            {
                "id": "M01.L11.Q20",
                "section_id": "user-identity",
                "question": "Why is service identity alone insufficient for downstream data governance?",
                "options": [
                    "The data system may also need to know which human user caused the action",
                    "Services cannot have identities",
                    "Users never affect authorization",
                    "Agent Cards store database rows",
                ],
                "correct": 0,
                "explanation": "User-specific access rules may require identity propagation and delegation.",
            },
            {
                "id": "M01.L11.Q21",
                "section_id": "complete-lifecycle",
                "question": "What are the three lifecycle streams in the source?",
                "options": [
                    "Creation, Governance, Usage",
                    "Training, Quantization, Inference",
                    "Frontend, CSS, Database",
                    "Audio, Image, Text",
                ],
                "correct": 0,
                "explanation": "These three streams explain how agents are built, permitted, and consumed.",
            },
            {
                "id": "M01.L11.Q22",
                "section_id": "complete-model",
                "type": "open",
                "question": (
                    "Design a governed enterprise agent ecosystem. Include an Agent Template Catalog, standardized repository, "
                    "CI/CD hydration/deployment, Agent-as-a-Service, Agent Registry, Registry Record with immutable identity and "
                    "Public Facade, registry hygiene, Agent Gateway policies for users/groups/agents, federated access governance, "
                    "Registry Portal, secure frontend/backend discovery, and the identity-propagation problem for downstream data."
                ),
            },
        ],
        "passing_score": 70,
    },
}
