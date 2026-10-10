"""M08.L08 — Advanced GCP Deployment: Autoscaling and Global Load Balancing.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 8, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L08"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Transform the single-VM GCP deployment into a replicated multi-region architecture using "
    "custom images, instance templates, managed instance groups, autoscaling, health checks, "
    "firewall tags, and a global HTTPS load balancer."
)
SOURCE_CHAPTER = 8
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Advanced Deployment in GCP: Autoscaling and Load Balancing Across Global Regions",
    "slug": "gcp-autoscaling-global-load-balancing-m08-l08",
    "description": (
        "Create reusable machine images and templates, deploy managed instance groups in Europe and the US, "
        "autoscale them from load-balancer utilization, autoheal through health checks, and front them with "
        "a global external HTTPS application load balancer using the existing SSL certificate and subdomains."
    ),
    "order": 8,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 4.0,
    "skill_tags": [
        "gcp", "custom-image", "instance-template", "managed-instance-groups", "autoscaling",
        "health-checks", "firewall", "global-load-balancer", "https", "dns", "multi-region"
    ],
    "prerequisite_ids": ["M08.L07"],

    "lesson": {
        "title": "Advanced Deployment in GCP: Autoscaling and Load Balancing Across Global Regions",
        "content": r"""
# Advanced Deployment in GCP: Autoscaling and Load Balancing Across Global Regions

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L08  
> **Source alignment:** BOOK-XXX, Chapter 8. This lesson follows the supplied chapter's custom-image, template, managed-instance-group, autoscaling, health-check, firewall, SSL, global load-balancer, and DNS configuration.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why the source converts the configured VM disk into a reusable image.
- Explain why the source changes the VM disk deletion rule to `Keep disk`.
- Create the conceptual relationship between image, instance template, and managed instance group.
- Explain the role of network tags in reusable instance templates.
- Describe the Europe and US managed instance groups from the source.
- Explain min/max instance counts and load-balancer-utilization autoscaling.
- Explain the source's global TCP health check on port 443.
- Distinguish autoscaling from autohealing.
- Explain the source firewall rule targeting HTTPS and a network tag.
- Understand the source's CIDR `/32`, `/24`, and broader range examples.
- Upload the existing TLS certificate/private key into a global GCP SSL certificate resource.
- Explain the frontend and backend sides of a global external Application Load Balancer.
- Explain how both regional managed instance groups become load-balancer backends.
- Explain the source's backend rate configuration and health-check attachment.
- Update DNS A records to point all application names to the load balancer's global IP.

---

## 1. Move from one configured VM to a reusable machine image

Chapter 7 produced one working VM.

Chapter 8 asks:

> How do we create many identical copies without manually configuring each VM?

The source's answer is a **custom machine image** derived from the existing VM disk.

### Preserve the disk first

Before deleting the old VM, the source changes:

```text
Deletion rule
Delete disk
→
Keep disk
```

Then it:

1. stops the VM,
2. deletes the VM instance,
3. keeps the disk,
4. creates an image from that disk.

### Why image the disk?

The original disk already contains:

```text
installed software
repository files
Docker setup
application configuration
subdomain deployment state
```

A reusable image captures that prepared machine state.

Conceptually:

```text
Configured VM disk
      ↓
Custom image
      ↓
many future VM instances
```

### Source image settings

The example uses:

```text
Name: webserver-image-with-subdomains
Source: Disk
Location: Multi-regional
Selected location: eu
```

[[IMAGE_NEEDED: VM-to-image-to-replicas | A diagram showing a configured GCP VM disk being preserved, converted into a custom image, then reused to create multiple identical VM instances | Learner should notice that the image becomes the reusable machine blueprint]]

---

## 2. Wrap the image in an instance template

A custom image describes disk content.

An **instance template** describes how new VM instances should be created.

The source creates:

```text
webserver-template-with-subdomains
```

with:

```text
Location: Global
Machine type: e2-standard-4
Custom boot image: webserver-image-with-subdomains
Network tag: vm-network-tag
```

The source describes `e2-standard-4` as:

```text
4 vCPUs
16 GB memory
```

### Why templates matter

A template standardizes instance configuration.

Instead of creating VMs one at a time, higher-level systems can say:

> Create instances from this template.

### Network-tag inheritance

The template carries:

```text
vm-network-tag
```

so VMs created from it can match the existing firewall rule.

This is an important infrastructure-as-code-like concept:

```text
define once in template
→ replicate consistently
```

{{exercise:M08.L08.EX01}}

---

## 3. Create managed instance groups in two regions

The source creates two managed instance groups.

### Europe group

Example:

```text
webserver-instance-group-europe
```

using:

```text
webserver-template-with-subdomains
```

in a European multi-zone region.

### US group

Example:

```text
webserver-instance-group-us
```

using the same template in:

```text
us-east4
```

### Why the same template?

Both regions should run equivalent application servers.

The template ensures consistent VM shape and disk image.

Conceptually:

```text
                 Global template
                    /      \
                   /        \
          Europe MIG       US MIG
          VM VM ...        VM VM ...
```

This is the beginning of geographic distribution.

---

## 4. Autoscale from HTTP load-balancing utilization

For each managed instance group, the source enables:

```text
add and remove instances automatically
```

with:

```text
minimum instances: 1
maximum instances: 2
```

The source then chooses:

```text
Signal type:
HTTP load balancing utilization
```

and sets target utilization to:

```text
80%
```

### Desired behavior

Conceptually:

```text
traffic/load increases
      ↓
load-balancer utilization approaches target
      ↓
managed group adds instance
```

When demand falls, the group can reduce instances within configured limits.

### Autoscaling is bounded

It does not mean:

```text
create unlimited VMs
```

The source constrains the group:

```text
1 ≤ instances ≤ 2
```

for the exercise.

### Autoscaling versus manual scaling

Manual:

```text
operator observes load
operator creates VM
operator joins backend
```

Autoscaling:

```text
platform observes signal
managed group adjusts automatically
```

{{image:gcp-instance-group-autoscaling}}

---

## 5. Autohealing with a global health check

Autoscaling answers:

> How many instances should exist?

Health checks answer:

> Which instances are healthy enough to serve?

The source creates:

```text
https-health-check
```

with:

```text
Scope: Global
Protocol: TCP
Port: 443
```

### Health criteria

The source sets:

```text
Check interval: 10 seconds
Timeout: 5 seconds
Healthy threshold: 2 successes
Unhealthy threshold: 3 failures
Initial delay: 60 seconds
```

{{image:gcp-instance-group-health-check}}

### Why initial delay?

A new VM may need time to initialize its services.

Checking too early may incorrectly classify it as failed.

### Autohealing

The managed instance group uses the health check to replace unhealthy members.

### Distinguish autoscaling and autohealing

```text
Autoscaling
→ adjust quantity for load

Autohealing
→ replace unhealthy instances
```

They solve different problems.

{{exercise:M08.L08.EX02}}

---

## 6. Permit HTTPS traffic to the replicated instances

The source updates the GCP firewall rule so the new instances can accept HTTPS traffic.

It targets:

```text
vm-network-tag
```

and permits:

```text
TCP 443
```

from the selected source range.

It also mentions optionally handling SSH on 22.

### Source CIDR explanation

The source explains:

```text
/32 → one IPv4 address
/31 → two addresses
/30 → four addresses
/24 → 256 addresses
/16 → 65,536 addresses
```

The core idea is:

> Smaller prefix number means a larger address range.

The source recommends restricting access rather than opening globally unless necessary for the scenario.

---

## 7. Upload the existing TLS material to Google Cloud

Before creating the global HTTPS load balancer, the source uploads:

```text
combined certificate
private key
```

into Cloud Shell.

Its folder structure is:

```text
~/config/lb-webserver_pro_combined.crt
~/config/private/private.key
```

Then it creates a global SSL certificate resource:

```bash
gcloud compute ssl-certificates create lb-webserver-cert \
  --certificate=config/lb-webserver_pro_combined.crt \
  --private-key=config/private/private.key \
  --global
```

This makes the certificate available to the load-balancer frontend.

### Certificate role moves outward

In Chapter 7, Nginx on each VM handled TLS.

Chapter 8 introduces a global load-balancer frontend that can itself use the uploaded certificate resource.

The source's backend is also configured using HTTPS.

---

## 8. Create the global external HTTPS Application Load Balancer

The source chooses:

```text
Application Load Balancer (HTTP/HTTPS)
Public facing
Best for global workloads
Global external Application Load Balancer
```

This becomes the global entry point for the multi-region application.

### Frontend configuration

The source configures:

```text
Protocol: HTTPS
IP version: IPv4
Reserved frontend IP
Port: 443
Certificate: lb-webserver-cert
```

The frontend answers:

> How do clients connect?

### Backend service

The source creates:

```text
https-lb-backend-webserver
```

with:

```text
Backend type: Instance group
Protocol: HTTPS
Named port: https-port
Timeout: 30 seconds
```

Then it adds:

```text
Europe managed instance group
US managed instance group
```

as backends.

### Backend load settings

For each backend, the source uses a **Rate** balancing mode with:

```text
Maximum RPS: 50
Scope: per instance
Capacity: 100
```

and notes that utilization is an alternative.

### Health check

The backend service attaches:

```text
https-health-check
```

so unhealthy instances can be excluded/repaired.

### Global request model

```text
Client
  ↓
Global HTTPS LB :443
  ↓
frontend certificate
  ↓
backend service
  ├── Europe MIG
  └── US MIG
       ↓
healthy instance
       ↓
application stack
```

{{image:gcp-global-load-balancer}}

{{exercise:M08.L08.EX03}}

---

## 9. Move DNS from the VM static IP to the load balancer IP

After creating the global load balancer, the source obtains its external IP.

Then it updates Namecheap A records:

```text
@         → load balancer IP
flask     → load balancer IP
jenkins   → load balancer IP
streamlit → load balancer IP
```

### Important architectural shift

Before:

```text
DNS
 ↓
one VM static IP
```

After:

```text
DNS
 ↓
global load balancer IP
 ↓
multi-region backend groups
```

The public identity stays the same.

The infrastructure behind it becomes scalable and geographically distributed.

### Verify

The source checks:

```text
streamlit.domain
flask.domain
jenkins.domain
```

after DNS propagation.

[[IMAGE_NEEDED: DNS shift from VM to global load balancer | A before/after diagram. Before: four A records point to one VM static IP. After: the same A records point to one global load-balancer IP, which distributes to Europe and US instance groups | Learner should notice that DNS names remain stable while backend architecture becomes multi-region]]

---

## 10. Put the complete Chapter 8 architecture together

The final source design can be read in layers.

### Layer 1 — reusable machine

```text
configured disk
→ custom image
→ global instance template
```

### Layer 2 — regional capacity

```text
instance template
→ Europe managed instance group
→ US managed instance group
```

### Layer 3 — elasticity

```text
HTTP LB utilization
→ autoscaling 1..2
```

### Layer 4 — health

```text
TCP 443 health check
→ autohealing / backend health
```

### Layer 5 — security

```text
firewall
→ target tag vm-network-tag
→ HTTPS 443
```

### Layer 6 — global entry

```text
global HTTPS frontend
→ certificate
→ backend service
→ Europe + US groups
```

### Layer 7 — stable naming

```text
DNS A records
→ global load-balancer IP
```

This is a substantial evolution from the original single EC2/VM deployment.

---

## Important misconceptions

### Misconception 1
> "The custom image and instance template are the same thing."

The image captures machine disk content; the template describes how new VMs should be created.

### Misconception 2
> "Autoscaling and autohealing are identical."

Autoscaling changes capacity. Autohealing replaces unhealthy instances.

### Misconception 3
> "The global load balancer points directly to one VM."

The source uses managed instance groups as backends.

### Misconception 4
> "DNS must know which region should serve the user."

DNS points to the load balancer's global IP; the load-balancer/backend system handles traffic distribution.

### Misconception 5
> "The old VM static IP remains the application's public destination."

Chapter 8 changes DNS to the load balancer IP.

---

## Key terminology

| Term | Meaning |
|---|---|
| Custom image | Reusable machine image created from a configured disk |
| Instance template | Reusable specification for creating VMs |
| Managed instance group (MIG) | Group of VM instances managed as a unit |
| Autoscaling | Automatic adjustment of instance count |
| Autohealing | Replacement/recovery of unhealthy instances |
| Health check | Probe used to determine backend health |
| Load-balancer utilization | Scaling signal used by the source |
| Global external Application Load Balancer | Public global HTTP/HTTPS load-balancing service used in the source |
| Frontend | Client-facing protocol/IP/port/certificate configuration |
| Backend service | Configuration connecting the load balancer to instance groups |
| RPS | Requests per second |

---

## Self-check

1. Why does the source set the original disk to Keep disk?
2. What is captured in the custom image?
3. What does the instance template add beyond the image?
4. Why include `vm-network-tag` in the template?
5. Which two geographic instance groups are created?
6. What are the min/max source replica counts?
7. What scaling signal and target does the source use?
8. What are the health-check interval, timeout, and thresholds?
9. What is the difference between autoscaling and autohealing?
10. Which port does the health check use?
11. How is the TLS certificate uploaded into GCP?
12. What does the load-balancer frontend configure?
13. What does the backend service configure?
14. Which managed groups become backends?
15. Why are DNS A records changed from VM IP to load-balancer IP?
16. Trace one browser request through the final global architecture.

---

## Retain this idea

**Scalable cloud infrastructure comes from replacing hand-configured servers with reusable images and templates, grouping identical instances under managed control, using metrics and health checks to adjust capacity and recover failures, and placing one stable global HTTPS endpoint in front of all regional backends.**
""",
        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "why-image", "title": "Move from one configured VM to a reusable machine image", "order": 1},
            {"id": "instance-template", "title": "Wrap the image in an instance template", "order": 2},
            {"id": "managed-groups", "title": "Create managed instance groups in two regions", "order": 3},
            {"id": "autoscaling", "title": "Autoscale from HTTP load-balancing utilization", "order": 4},
            {"id": "health-check", "title": "Autohealing with a global health check", "order": 5},
            {"id": "firewall-https", "title": "Permit HTTPS traffic to the replicated instances", "order": 6},
            {"id": "ssl-resource", "title": "Upload the existing TLS material to Google Cloud", "order": 7},
            {"id": "global-lb", "title": "Create the global external HTTPS Application Load Balancer", "order": 8},
            {"id": "dns-global", "title": "Move DNS from the VM static IP to the load balancer IP", "order": 9},
            {"id": "full-architecture", "title": "Put the complete Chapter 8 architecture together", "order": 10},
        ],
    },

    "exercises": [
        {
            "id": "M08.L08.EX01",
            "title": "Separate Image, Template, and Instance Group",
            "lesson_code": "M08.L08",
            "section_id": "instance-template",
            "placement": "after_section",
            "description": "Clarify the three layers of reusable compute configuration.",
            "instructions": (
                ('1. Create a table for custom image, instance template, and managed instance group.\n'
                 '2. For each, state what it stores, what consumes it, and the source-specific name used in Chapter 8.')
            ),
            "expected_output": "A three-layer reusable-infrastructure table.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["gcp-images", "instance-templates", "managed-instance-groups"],
        },
        {
            "id": "M08.L08.EX02",
            "title": "Reason About Scaling and Health Independently",
            "lesson_code": "M08.L08",
            "section_id": "health-check",
            "placement": "after_section",
            "description": "Distinguish load-driven capacity management from failure recovery.",
            "instructions": (
                ('1. Scenario A: utilization reaches the source target while all instances are healthy.\n'
                 '2. Scenario B: utilization is low but one VM fails three consecutive health checks.\n'
                 '3. Explain what autoscaling versus autohealing should do in each scenario.')
            ),
            "expected_output": "A two-scenario explanation separating scaling from healing.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["autoscaling", "health-checks", "autohealing"],
        },
        {
            "id": "M08.L08.EX03",
            "title": "Trace the Global HTTPS Request",
            "lesson_code": "M08.L08",
            "section_id": "global-lb",
            "placement": "after_section",
            "description": "Trace one request through the final multi-region architecture.",
            "instructions": (
                ('1. Trace `https://flask.example.com` through DNS → global load-balancer IP → HTTPS frontend/certificate → backend service → one healthy Europe or US instance-group member → application stack.\n'
                 '2. Mark where health checks and autoscaling influence the path.')
            ),
            "expected_output": "A full global request-path diagram with control loops.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["global-load-balancing", "dns", "managed-instance-groups", "https"],
        },
    ],

    "quiz": {
        "id": "M08.L08.QZ01",
        "title": "Advanced GCP Autoscaling and Global Load Balancing — Knowledge Check",
        "lesson_code": "M08.L08",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L08.Q01", "section_id": "why-image", "question": "Why does the source set the VM disk to Keep disk before deleting the VM?", "options": ["To preserve it for image creation", "To enable Git", "To create a CNAME", "To run Jenkins"], "correct": 0, "explanation": "The disk becomes the source for the reusable custom image."},
            {"id": "M08.L08.Q02", "section_id": "instance-template", "question": "Which source machine type is used in the instance template?", "options": ["e2-standard-8", "e2-standard-4", "t2.xlarge", "e2-micro"], "correct": 1, "explanation": "The source uses e2-standard-4 in Chapter 8."},
            {"id": "M08.L08.Q03", "section_id": "managed-groups", "question": "Which two broad regions are represented by managed instance groups?", "options": ["Europe and US", "Asia and Africa", "Australia and Canada", "Only Europe"], "correct": 0, "explanation": "The source creates Europe and US groups."},
            {"id": "M08.L08.Q04", "section_id": "autoscaling", "question": "What source utilization target triggers the scaling logic?", "options": ["20%", "50%", "80%", "100%"], "correct": 2, "explanation": "The source configures target HTTP load-balancing utilization at 80%."},
            {"id": "M08.L08.Q05", "section_id": "health-check", "question": "Which port does the health check probe?", "options": ["22", "80", "443", "8501"], "correct": 2, "explanation": "The source uses a TCP health check on 443."},
            {"id": "M08.L08.Q06", "section_id": "health-check", "question": "What is the unhealthy threshold?", "options": ["1", "2", "3", "10"], "correct": 2, "explanation": "Three failed checks mark the instance unhealthy in the source."},
            {"id": "M08.L08.Q07", "section_id": "firewall-https", "question": "What does a /32 source represent?", "options": ["One exact IPv4 address", "256 addresses", "65,536 addresses", "All addresses"], "correct": 0, "explanation": "The source explains /32 as one IP."},
            {"id": "M08.L08.Q08", "section_id": "ssl-resource", "question": "What creates the global SSL certificate resource?", "options": ["docker-compose", "gcloud compute ssl-certificates create", "git clone", "openssl req only"], "correct": 1, "explanation": "The source uses the gcloud command with certificate and private key."},
            {"id": "M08.L08.Q09", "section_id": "global-lb", "question": "What backend type does the source select?", "options": ["Cloud Storage bucket", "Instance group", "Git repository", "DNS zone"], "correct": 1, "explanation": "The global backend service uses managed instance groups."},
            {"id": "M08.L08.Q10", "section_id": "dns-global", "question": "Where do application A records point after Chapter 8?", "options": ["Old VM static IP", "Global load-balancer IP", "GitHub IP", "Jenkins container IP"], "correct": 1, "explanation": "DNS is moved to the global load-balancer IP."},
            {"id": "M08.L08.Q11", "section_id": "full-architecture", "type": "open", "question": "Explain the final Chapter 8 architecture from custom image through global DNS and describe where autoscaling and autohealing act."},
        ],
        "passing_score": 70,
    },
}
