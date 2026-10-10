"""M08.L09 — Serverless Deployment with Google Cloud Run.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 9, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L09"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Move the Flask and Streamlit applications from persistent virtual machines to a serverless "
    "Google Cloud Run architecture, then connect them to a global HTTPS load balancer, custom "
    "subdomains, Identity-Aware Proxy, and Cloud Armor."
)
SOURCE_CHAPTER = 9
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Serverless Deployment with Google Cloud Run",
    "slug": "serverless-google-cloud-run-m08-l09",
    "description": (
        "Understand serverless computing, deploy stateless Flask and Streamlit containers to Cloud Run, "
        "connect them through serverless NEGs and a global HTTPS load balancer, restrict direct service URLs, "
        "and secure browser or machine access with IAP and Cloud Armor."
    ),
    "order": 9,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 4.0,
    "skill_tags": [
        "serverless", "cloud-run", "gcp", "cloud-build", "artifact-registry",
        "serverless-neg", "global-load-balancer", "iap", "cloud-armor",
        "dns", "autoscaling",
    ],
    "prerequisite_ids": ["M08.L08"],

    "lesson": {
        "title": "Serverless Deployment with Google Cloud Run",
        "content": r"""
# Serverless Deployment with Google Cloud Run

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L09  
> **Source alignment:** BOOK-XXX, Chapter 9. The lesson follows the supplied Cloud Run, load-balancing, IAP, and Cloud Armor workflow. Provider UI details, quotas, and examples are treated as source-specific.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain serverless computing in the source's terms.
- Distinguish stateful, stateless, and ephemeral application behavior.
- Explain why the source keeps Jenkins on VMs instead of Cloud Run.
- Explain the source's requirement that the Cloud Run application containers bind to port 8080.
- Build and deploy Flask and Streamlit independently with `gcloud`.
- Explain the difference between building an image and deploying a Cloud Run service.
- Explain Cloud Run minimum instances and the latency trade-off.
- Define a serverless Network Endpoint Group (NEG).
- Explain how serverless NEGs connect Cloud Run services to a global load balancer.
- Build separate backend services for Flask and Streamlit.
- Route traffic by hostname to the correct backend.
- Update DNS to point the Flask and Streamlit subdomains to the load balancer.
- Restrict direct Cloud Run URL access.
- Explain Identity-Aware Proxy for browser-based authenticated access.
- Explain Cloud Armor as the source's IP allow-list option for machine-to-machine access.
- Understand the source's Cloud Armor quota troubleshooting path.

---

## 1. Serverless means you manage the application, not the servers

The previous GCP architecture used:

```text
virtual machines
+
managed instance groups
+
health checks
+
global load balancer
```

Chapter 9 moves Flask and Streamlit into a **serverless** model.

The source describes serverless computing as infrastructure where the cloud provider manages:

```text
server provisioning
operating-system management
scaling
container lifecycle
```

while the developer focuses mainly on:

```text
application code
container image
service configuration
```

### VM mental model

With a VM:

```text
you manage:
OS
packages
Docker
service startup
machine sizing
patching
```

### Serverless mental model

With Cloud Run:

```text
you provide:
container image

Google manages:
underlying servers
instance lifecycle
scaling infrastructure
```

That does **not** mean there are literally no servers.

It means the servers are abstracted away from you.

[[IMAGE_NEEDED: VM deployment versus serverless deployment | A side-by-side diagram showing VM deployment where the engineer manages OS, Docker, services, scaling, and application versus Cloud Run where the engineer provides a container and Google manages infrastructure and scaling | Learner should notice that serverless removes infrastructure-management responsibility rather than eliminating physical servers]]

---

## 2. Stateful, stateless, and ephemeral applications

The source introduces three terms before deployment.

### Stateful

A **stateful** application depends on data or session state that survives beyond one request.

Examples conceptually include:

```text
persistent local files
configuration state
user session state
application history
```

### Stateless

A **stateless** application treats each request independently.

It can usually be replicated more easily because any compatible instance can handle the next request.

### Ephemeral

An **ephemeral** environment is temporary.

A container instance may:

```text
start
handle work
stop
be replaced
```

without you controlling its long-term local filesystem lifecycle.

### Why Jenkins is excluded

The source specifically explains that Jenkins is not a good fit for the chapter's serverless deployment because it relies heavily on:

- persistent storage,
- file permissions,
- stateful configuration,
- long-lived filesystem state.

Earlier chapters deliberately persisted:

```text
/var/jenkins_home
```

Cloud Run's ephemeral container model conflicts with that architecture in the source.

So Chapter 9 deploys only:

```text
Flask
Streamlit
```

### Source alternatives for Jenkins-like scheduled work

The source mentions serverless functions plus a scheduler for certain scheduled ETL-style jobs.

The larger lesson is:

> Choose deployment architecture based on application state requirements.

{{exercise:M08.L09.EX01}}

---

## 3. Prepare the applications for Cloud Run

The source uploads two folders separately:

```text
flask-app-gcp/
streamlit-app-gcp/
```

### Port change

Earlier chapters used:

```text
Streamlit → 8501
Flask     → 8502
```

For the source's Cloud Run setup, both containerized applications are updated to listen on:

```text
8080
```

The repository already contains Cloud-Run-specific versions of:

```text
flask-app-gcp/app.py
flask-app-gcp/Dockerfile
streamlit-app-gcp/Dockerfile
```

### Why this matters

The application's internal interface must match the runtime contract expected by the platform.

Conceptually:

```text
Cloud Run request
      ↓
platform forwards request
      ↓
container :8080
```

### Cloud Shell environment

The source defines:

```bash
export GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT>
export LOCATION=<YOUR_REGION>
```

and authenticates with:

```bash
gcloud auth login
```

These variables make later commands reusable.

---

## 4. Build and deploy Flask and Streamlit independently

For Flask, the source uses:

```bash
gcloud builds submit flask-app-gcp/ \
  --tag gcr.io/$GOOGLE_CLOUD_PROJECT/flask_app \
  --region=$LOCATION
```

followed by:

```bash
gcloud run deploy flask-app \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/flask_app \
  --region=$LOCATION \
  --allow-unauthenticated
```

Streamlit follows the same pattern.

### Two distinct stages

Do not mentally merge these commands.

#### Build stage

```text
source folder
   ↓
Cloud Build
   ↓
container image
   ↓
registry
```

#### Deploy stage

```text
container image
   ↓
Cloud Run service
   ↓
managed serverless instances
   ↓
service URL
```

### Build history

The source emphasizes that submitted builds are recorded, making previous builds visible for:

- troubleshooting,
- reuse,
- rollback/version history.

### Service metrics

Cloud Run exposes source-described metrics such as:

- request count,
- request latency,
- container instance count,
- billable instance time,
- logs.

[[IMAGE_NEEDED: Cloud Run build-and-deploy flow | A diagram showing local/uploaded source → Cloud Build → container registry → Cloud Run service → managed instances → service URL and metrics | Learner should notice that image creation and service deployment are separate stages]]

---

## 5. Understand Cloud Run minimum instances

The source says Cloud Run's minimum instance count defaults to:

```text
0
```

in its example.

That means the platform can have no active application instance while idle.

When a request arrives, an instance may need to start.

### Cold-start trade-off

Conceptually:

```text
minimum = 0
→ potentially lower idle cost
→ first request may wait for startup
```

versus:

```text
minimum >= 1
→ instance kept warm
→ faster initial response
→ additional idle cost
```

The source specifically recommends considering:

```text
minimum instances = 1
```

for latency-sensitive applications.

This is a serverless design trade-off rather than a universally correct value.

---

## 6. Connect Cloud Run to load balancing with serverless NEGs

In Chapter 8, the global load balancer used:

```text
managed instance groups
```

as backends.

Cloud Run is different.

The source creates:

```text
flask-neg
streamlit-neg
```

using:

```text
network endpoint type = serverless
```

Each NEG points to one Cloud Run service.

### Mental model

```text
Cloud Run flask-app
      ↑
   flask-neg

Cloud Run streamlit-app
      ↑
 streamlit-neg
```

The NEG becomes the connection object that the load balancer can use.

### Source commands

Conceptually:

```bash
gcloud compute network-endpoint-groups create flask-neg \
  --network-endpoint-type=serverless \
  --cloud-run-service=flask-app
```

and similarly for Streamlit.

[[IMAGE_NEEDED: VM backend versus serverless NEG backend | A comparison showing Chapter 8 global load balancer → managed instance group → VMs, versus Chapter 9 load balancer → serverless NEG → Cloud Run service | Learner should notice that the backend attachment object changes when moving from VMs to serverless]]

{{exercise:M08.L09.EX02}}

---

## 7. Build the global HTTPS load balancer

The source creates a:

```text
Global external Application Load Balancer
```

with an HTTPS frontend.

### Frontend

Source settings include:

```text
Protocol: HTTPS
IPv4
Reserved frontend IP
Port: 443
Existing SSL certificate
```

### Separate backend services

The source creates:

```text
lb-https-backend-flask
lb-https-backend-streamlit
```

Each backend uses:

```text
Backend type:
Serverless network endpoint group
```

and points to:

```text
flask-neg
streamlit-neg
```

respectively.

### Why two backends?

Because hostname routing needs to select different application destinations.

### Source Cloud CDN choice

The source disables Cloud CDN because it later wants to use IAP in the described architecture.

### Routing rules

The source defines host rules such as:

```text
streamlit.lb-webserver.pro
  → lb-https-backend-streamlit

flask.lb-webserver.pro
  → lb-https-backend-flask
```

The default rule catches unmatched traffic.

[[IMAGE_NEEDED: Cloud Run global HTTPS routing | A diagram showing HTTPS frontend on port 443 → host rules → Flask backend service → flask-neg → flask-app and Streamlit backend service → streamlit-neg → streamlit-app | Learner should notice that hostname routing selects separate serverless backends]]

---

## 8. Point DNS to the load balancer and disable direct Cloud Run access

After load-balancer creation, the source retrieves the frontend IP.

It updates only the relevant application DNS records:

```text
flask
streamlit
```

to use the new load-balancer IP.

It explicitly says not to change unrelated services such as Jenkins because Jenkins is not running in Cloud Run.

### Why disable the default Cloud Run URLs?

At first, the services were deployed with direct public URLs.

If you want users to enter only through the load balancer, those direct URLs create a bypass path.

The source changes ingress using:

```text
internal-and-cloud-load-balancing
```

for both services.

Conceptually:

```text
Before:
Internet ──────────→ Cloud Run URL
   └──────────────→ Load Balancer → Cloud Run

After:
Internet ─X───────→ direct Cloud Run URL
   └──────────────→ Load Balancer → Cloud Run
```

This centralizes:

- TLS endpoint,
- hostname routing,
- access controls.

{{exercise:M08.L09.EX03}}

---

## 9. Use Identity-Aware Proxy for browser authentication

Restricting direct Cloud Run access does not automatically mean only approved users can use the application.

The source introduces **Identity-Aware Proxy (IAP)**.

### IAP model

```text
Browser
  ↓
Load Balancer
  ↓
IAP sign-in
  ↓
authorized user?
  ├── no → deny
  └── yes → backend service
```

### Granting access

The source adds user principals and grants the role:

```text
IAP-secured Web App User
```

for the relevant backend.

### Best fit in the source

The chapter presents IAP as useful for:

```text
browser-based applications
```

such as Streamlit and a human-facing Flask page.

### Machine-to-machine caveat

For API calls such as:

```text
POST /predict
```

the source says IAP may be cumbersome.

That motivates the next security option.

---

## 10. Use Cloud Armor for source-IP restrictions

The source presents **Cloud Armor** as an alternative when you want:

```text
allow specific IPs
deny everyone else
```

### Policy structure

The source creates:

```text
Backend security policy
Scope: Global
Layer: Application
Default action: Deny 403
```

Then it adds a higher-priority allow rule such as:

```text
source IP /32
→ Allow
```

and attaches the policy to the Flask and Streamlit backend services.

### Rule evaluation idea

```text
specific allow rule
       ↓
matches?
  yes → allow
  no  → default deny 403
```

### Why this suits machine-to-machine access in the source

A trusted external system with a known IP does not need an interactive Google sign-in page.

Its network identity can be the access condition.

### Cloud Armor quota issue

The source documents a practical failure:

```text
SECURITY_POLICY_RULES quota = 0
```

on some new projects.

Its troubleshooting sequence is:

1. search quotas for `security_policy_rules`,
2. locate the global quota,
3. confirm the value,
4. request an increase through the provider path described by the source,
5. verify that the quota changed.

Treat the exact provider support process as source-specific.

[[IMAGE_NEEDED: IAP versus Cloud Armor access models | A split diagram. Left: human browser → Google sign-in/IAP → backend. Right: trusted machine IP → Cloud Armor allow rule → backend, all other IPs → 403 | Learner should notice that authentication and IP allow-listing solve different access-control problems]]

{{exercise:M08.L09.EX04}}

---

## 11. Put the full Cloud Run architecture together

The final source design is:

```text
Developer
   ↓
Cloud Build
   ↓
container registry
   ↓
Cloud Run services
   ├── flask-app
   └── streamlit-app
        ↓
serverless NEGs
        ↓
separate backend services
        ↓
host-based routing
        ↓
Global HTTPS Load Balancer
        ↓
custom DNS
```

Security is layered on top:

```text
direct Cloud Run URL
→ blocked by ingress policy

browser users
→ optionally authenticated by IAP

trusted machine/API clients
→ optionally filtered by Cloud Armor
```

This is the serverless equivalent of the earlier VM-based deployment, but with far less direct infrastructure management.

---

## Important misconceptions

### Misconception 1
> "Serverless means there are no servers."

The provider manages the servers; you no longer manage them directly.

### Misconception 2
> "Every application is a good serverless candidate."

The source excludes Jenkins because its state and filesystem expectations conflict with the chapter's ephemeral model.

### Misconception 3
> "Cloud Run services automatically become load-balancer backends."

The source creates serverless NEGs and backend services first.

### Misconception 4
> "Changing DNS to the load balancer automatically blocks the direct Cloud Run URL."

The source explicitly changes ingress to prevent bypass.

### Misconception 5
> "IAP and Cloud Armor are the same security control."

IAP authenticates users; the source uses Cloud Armor to allow/deny based on IP conditions.

---

## Key terminology

| Term | Meaning |
|---|---|
| Serverless | Managed runtime model that abstracts infrastructure management |
| Stateless | Request handling without relying on persistent local session state |
| Ephemeral | Temporary runtime instance that may be created and removed |
| Cloud Run | GCP serverless container service used in the source |
| Cloud Build | Build service used to create container images |
| Serverless NEG | Load-balancer attachment object for a serverless service |
| Backend service | Load-balancer backend configuration |
| Ingress | Rules controlling how a service may be reached |
| IAP | Identity-Aware Proxy |
| Cloud Armor | GCP security policy product used for IP restrictions in the source |

---

## Self-check

1. What does serverless abstract away?
2. Why is Jenkins excluded from the Cloud Run deployment?
3. How do stateful and stateless applications differ?
4. What internal port does the source use for Cloud Run containers?
5. What is the difference between `gcloud builds submit` and `gcloud run deploy`?
6. Why might a minimum instance count of 1 reduce latency?
7. What is a serverless NEG?
8. Why does the source create two backend services?
9. How does the load balancer know whether to send a request to Flask or Streamlit?
10. Why does the source block direct Cloud Run URLs?
11. What problem does IAP solve?
12. Why might Cloud Armor be more convenient for a machine client?
13. What does a default-deny Cloud Armor policy do?
14. What quota problem does the source document?
15. Trace one request from `https://flask.<domain>` to the Flask Cloud Run service.

---

## Retain this idea

**Serverless deployment does not remove architecture; it moves infrastructure responsibility to the provider. You still design images, scaling behavior, load-balancer routing, DNS, ingress, and authentication—but you no longer manage the underlying VM fleet yourself.**
""",
        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "serverless-foundations", "title": "Serverless means you manage the application, not the servers", "order": 1},
            {"id": "state-model", "title": "Stateful, stateless, and ephemeral applications", "order": 2},
            {"id": "cloud-run-prep", "title": "Prepare the applications for Cloud Run", "order": 3},
            {"id": "build-deploy", "title": "Build and deploy Flask and Streamlit independently", "order": 4},
            {"id": "cloud-run-scaling", "title": "Understand Cloud Run minimum instances", "order": 5},
            {"id": "serverless-neg", "title": "Connect Cloud Run to load balancing with serverless NEGs", "order": 6},
            {"id": "cloudrun-lb", "title": "Build the global HTTPS load balancer", "order": 7},
            {"id": "dns-ingress", "title": "Point DNS to the load balancer and disable direct Cloud Run access", "order": 8},
            {"id": "iap", "title": "Use Identity-Aware Proxy for browser authentication", "order": 9},
            {"id": "cloud-armor", "title": "Use Cloud Armor for source-IP restrictions", "order": 10},
            {"id": "cloudrun-full", "title": "Put the full Cloud Run architecture together", "order": 11},
        ],
    },

    "exercises": [
        {
            "id": "M08.L09.EX01",
            "title": "Choose Serverless or VM",
            "lesson_code": "M08.L09",
            "section_id": "state-model",
            "placement": "after_section",
            "description": "Decide whether application state fits the source's serverless model.",
            "instructions": (
                ("1. Classify these as better fits for the chapter's Cloud Run model or VM-style deployment: a stateless prediction API, a Streamlit UI, Jenkins with persistent plugin/job state, and a scheduled ETL script.\n"
                 '2. Explain the state/persistence reason for each.')
            ),
            "expected_output": "A four-row deployment-fit table with reasoning.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["serverless", "stateful", "stateless"],
        },
        {
            "id": "M08.L09.EX02",
            "title": "Trace the Serverless Backend Chain",
            "lesson_code": "M08.L09",
            "section_id": "serverless-neg",
            "placement": "after_section",
            "description": "Explain every object between Cloud Run and the load balancer.",
            "instructions": (
                ('1. For Flask and Streamlit separately, draw Cloud Run service → serverless NEG → backend service → host rule → HTTPS frontend.\n'
                 '2. Label the source names for each object.')
            ),
            "expected_output": "Two parallel backend-routing diagrams.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["cloud-run", "serverless-neg", "load-balancing"],
        },
        {
            "id": "M08.L09.EX03",
            "title": "Remove the Direct-URL Bypass",
            "lesson_code": "M08.L09",
            "section_id": "dns-ingress",
            "placement": "after_section",
            "description": "Reason about why DNS alone is not an access-control mechanism.",
            "instructions": (
                ('1. Draw the before and after request paths when direct Cloud Run URLs are public versus when ingress is `internal-and-cloud-load-balancing`.\n'
                 '2. Explain which security controls can now be centralized at the load balancer.')
            ),
            "expected_output": "A before/after ingress diagram plus a short explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["ingress", "cloud-run", "security"],
        },
        {
            "id": "M08.L09.EX04",
            "title": "Choose IAP or Cloud Armor",
            "lesson_code": "M08.L09",
            "section_id": "cloud-armor",
            "placement": "after_section",
            "description": "Select an access-control method for human and machine clients.",
            "instructions": (
                ('1. Scenario A: employees open a Streamlit dashboard in a browser.\n'
                 '2. Scenario B: one trusted external backend calls `/predict` from a fixed IP.\n'
                 "3. Choose IAP or Cloud Armor for each based on the source's recommendations and explain why.")
            ),
            "expected_output": "A two-scenario security design.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["iap", "cloud-armor", "access-control"],
        },
    ],

    "quiz": {
        "id": "M08.L09.QZ01",
        "title": "Serverless Deployment with Google Cloud Run — Knowledge Check",
        "lesson_code": "M08.L09",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L09.Q01", "section_id": "serverless-foundations", "question": "What does serverless primarily abstract in the source?", "options": ["Application code", "Server infrastructure management", "HTTP requests", "Dockerfiles"], "correct": 1, "explanation": "The provider handles infrastructure provisioning, scaling, and server management."},
            {"id": "M08.L09.Q02", "section_id": "state-model", "question": "Why does the source avoid Jenkins on Cloud Run?", "options": ["Jenkins cannot use HTTP", "Jenkins relies on persistent state and filesystem behavior", "Cloud Run supports only Java", "Jenkins has no container image"], "correct": 1, "explanation": "The chapter emphasizes Jenkins' stateful storage and permissions requirements."},
            {"id": "M08.L09.Q03", "section_id": "cloud-run-prep", "question": "Which internal port do the source's Cloud Run containers use?", "options": ["80", "443", "8080", "8501"], "correct": 2, "explanation": "The repository's Cloud Run variants bind to port 8080."},
            {"id": "M08.L09.Q04", "section_id": "build-deploy", "question": "What does `gcloud builds submit` do?", "options": ["Creates an IAP user", "Builds a container image from source", "Updates DNS", "Creates a firewall rule"], "correct": 1, "explanation": "The build command produces the container image used later by Cloud Run."},
            {"id": "M08.L09.Q05", "section_id": "cloud-run-scaling", "question": "What is the source's main reason for setting minimum instances to 1?", "options": ["Increase storage", "Reduce initial response latency", "Enable DNS", "Create a certificate"], "correct": 1, "explanation": "Keeping one instance warm can reduce cold-start delay."},
            {"id": "M08.L09.Q06", "section_id": "serverless-neg", "question": "What does a serverless NEG connect to in the source?", "options": ["A Git repository", "A Cloud Run service", "A VM disk", "An IAM role"], "correct": 1, "explanation": "Each NEG is explicitly associated with one Cloud Run service."},
            {"id": "M08.L09.Q07", "section_id": "cloudrun-lb", "question": "How does the load balancer distinguish Flask and Streamlit?", "options": ["By SSH username", "By host routing rules", "By Docker tag only", "By Cloud Build history"], "correct": 1, "explanation": "Hostname rules direct traffic to separate backend services."},
            {"id": "M08.L09.Q08", "section_id": "dns-ingress", "question": "Why restrict direct Cloud Run URLs?", "options": ["To force traffic through the load balancer and its controls", "To disable autoscaling", "To remove container images", "To stop logging"], "correct": 0, "explanation": "The source centralizes entry through the load balancer."},
            {"id": "M08.L09.Q09", "section_id": "iap", "question": "Which control does the source prefer for browser-based authenticated access?", "options": ["Cloud Armor only", "IAP", "Docker login", "SSH"], "correct": 1, "explanation": "IAP presents a Google sign-in flow and manages user access."},
            {"id": "M08.L09.Q10", "section_id": "cloud-armor", "question": "What is the default action in the source Cloud Armor policy?", "options": ["Allow all", "Deny with 403", "Redirect to Jenkins", "Scale to zero"], "correct": 1, "explanation": "Specific trusted IPs are allowed; the default action denies."},
            {"id": "M08.L09.Q11", "section_id": "cloud-armor", "question": "Which quota issue does the source document?", "options": ["No available VM CPUs", "SECURITY_POLICY_RULES set to zero", "No DNS records", "No Docker storage"], "correct": 1, "explanation": "The chapter shows new projects that may have a zero security-policy-rule quota."},
            {"id": "M08.L09.Q12", "section_id": "cloudrun-full", "question": "What replaces VM instance groups as the serverless load-balancer attachment?", "options": ["Serverless NEGs", "SSH keys", "Persistent disks", "Jenkins volumes"], "correct": 0, "explanation": "The source explicitly compares serverless NEGs with the earlier instance-group backend model."},
            {"id": "M08.L09.Q13", "section_id": "cloudrun-full", "type": "open", "question": "Describe the complete Chapter 9 request path from custom subdomain to Cloud Run service, including NEG, backend service, load balancer, ingress restriction, and either IAP or Cloud Armor."},
        ],
        "passing_score": 70,
    },
}
