"""M08.L07 — Rebuild the Infrastructure on Google Cloud Platform.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 7, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L07"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Replicate the AWS-hosted application environment on Google Cloud by creating a project and VM, "
    "automating setup with a startup script, reserving a static IP, configuring firewall rules, "
    "and progressively deploying Streamlit, the full SSL stack, and HTTPS subdomains."
)
SOURCE_CHAPTER = 7
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "How to Set Up This Infrastructure on Google Cloud Platform",
    "slug": "gcp-infrastructure-migration-m08-l07",
    "description": (
        "Migrate the existing Streamlit, Flask, Jenkins, Nginx, and TLS deployment from AWS concepts "
        "to Google Cloud Platform through a three-level progression from a simple Streamlit VM to full HTTPS subdomains."
    ),
    "order": 7,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 4.0,
    "skill_tags": [
        "gcp", "compute-engine", "iam", "startup-script", "static-ip", "ssh",
        "firewall", "docker-compose", "nginx", "ssl", "subdomains", "module-08"
    ],
    "prerequisite_ids": ["M08.L06"],

    "lesson": {
        "title": "How to Set Up This Infrastructure on Google Cloud Platform",
        "content": r"""
# How to Set Up This Infrastructure on Google Cloud Platform

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L07  
> **Source alignment:** BOOK-XXX, Chapter 7. This lesson preserves the source's GCP project, Compute Admin role, VM size, startup script, static IP, firewall, Docker/Nginx, SSL, and subdomain progression.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how the source maps its AWS architecture into Google Cloud.
- Create a GCP project and grant the source's Compute Admin role.
- Explain the source VM configuration: region, machine type, disk size, and network tag.
- Explain why the startup script improves repeatability.
- Identify what the startup script installs and enables.
- Configure an RSA SSH key and static external IP.
- Explain GCP firewall rules using network tags and source CIDRs.
- Deploy a direct Streamlit application on port 8501.
- Reuse the GitHub/Docker/Nginx/SSL stack on GCP.
- Extend the firewall from one application port to three service ports.
- Move the GCP deployment to subdomains on standard ports 80 and 443.
- Explain how the source reuses the same Docker Compose and Nginx design across cloud providers.

---

## 1. Recreate the deployment on another cloud

Chapters 1–6 built the architecture on AWS.

Chapter 7 begins a migration to:

```text
Google Cloud Platform
```

The application architecture itself remains familiar:

```text
Streamlit
Flask
Jenkins
Nginx
TLS certificates
Docker Compose
```

What changes is the infrastructure provider.

This is useful because it separates:

```text
application architecture
```

from:

```text
cloud-specific infrastructure implementation
```

### GCP project

The source creates a new GCP project and makes sure it is selected before provisioning resources.

### IAM role

The source grants:

```text
Compute Engine → Compute Admin
```

to the intended principal.

This is the source's exercise permission model.

[[IMAGE_NEEDED: AWS-to-GCP conceptual migration | A side-by-side diagram showing the same Streamlit/Flask/Jenkins/Nginx application stack, with AWS EC2/networking on the left and GCP Compute Engine/firewall/static IP on the right | Learner should notice that the application architecture is preserved while cloud-specific infrastructure changes]]

---

## 2. Create the Compute Engine VM with a startup script

The source creates a Compute Engine VM using:

```text
Name: webserver
Region: europe-west10 or nearest region
Machine type: e2-standard-8
Disk: 100 GB
Network tag: vm-network-tag
```

It describes `e2-standard-8` as:

```text
8 vCPUs
32 GB RAM
```

### Why the network tag matters

Later GCP firewall rules target:

```text
vm-network-tag
```

So the tag becomes a connection between:

```text
VM/template
and
firewall policy
```

### Startup script

The source automates VM preparation through a boot/startup script.

It performs:

```text
system update/upgrade
Python installation
Docker installation
Docker service start
Docker service enable
current user added to Docker group
Docker Compose installation
Git installation
version verification
```

### Why automate bootstrap work?

Earlier AWS setup required many manual commands.

The GCP chapter makes the setup reproducible:

```text
create VM
      ↓
startup script executes
      ↓
required tools installed consistently
```

The source explicitly frames this as reducing manual errors and dependency inconsistencies.

[[IMAGE_NEEDED: GCP VM bootstrap | A diagram showing Compute Engine VM creation → startup script → Python + Docker + Docker Compose + Git installation → Docker service enabled → version checks | Learner should notice that the machine configuration is automated rather than repeated manually]]

{{exercise:M08.L07.EX01}}

---

## 3. Configure SSH and reserve a static external IP

The source generates a local SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

producing:

```text
~/.ssh/id_rsa
~/.ssh/id_rsa.pub
```

### Add public key to GCP

The public key is added to the VM's SSH key configuration.

The private key stays on the local machine.

### Reserve static external IP

The source reserves a regional external IP and attaches it to the VM.

This gives the deployment a stable address for:

- SSH config,
- direct Streamlit access,
- DNS later.

### VS Code SSH alias

The source adds:

```text
Host vm-book-project
HostName <STATIC_IP>
IdentityFile ~/.ssh/id_rsa
User <gcp-username>
```

to local SSH config.

### GCP console SSH

The chapter also presents browser-based SSH through the GCP console as an alternative.

### Default SSH firewall note

The source notes that GCP often includes a default SSH rule, but custom firewall priority can still override or conflict with it.

---

## 4. Level 1 — deploy a simple Streamlit app directly

The source deliberately progresses in levels.

Level 1 is a simple direct deployment.

### Create virtual environment

On the VM:

```text
create project folder
create Python virtual environment
install Streamlit
```

### Run Streamlit

The source runs the app on:

```text
8501
```

### GCP firewall rule

It creates:

```text
Name: allow-rule-webserver
Direction: Ingress
Action: Allow
Target tag: vm-network-tag
Source: trusted IP/32
TCP port: 8501
```

This is the GCP equivalent of the earlier security-group thinking.

### Network tag connection

The firewall applies because:

```text
VM has tag vm-network-tag
```

and:

```text
firewall targets vm-network-tag
```

### Direct URL

The application becomes reachable at:

```text
http://STATIC_IP:8501
```

This is intentionally not the final secure design.

It is a validation level.

[[IMAGE_NEEDED: GCP Level 1 direct Streamlit access | A flow showing browser → GCP static IP:8501 → firewall rule targeting vm-network-tag → Compute Engine VM → Streamlit process | Learner should notice the similarity to the earlier direct EC2 deployment]]

{{exercise:M08.L07.EX02}}

---

## 5. Level 2 — deploy the full SSL application stack

The next level reuses the GitHub code and architecture from the AWS chapters.

### GitHub access

The source generates/configures an ED25519 GitHub key and clones:

```text
deploy-secure-ds-apps-book
```

It also configures Git user name/email.

### Shared permissions

The source repeats the `jenkins_shared` approach:

```text
GCP user
docker
jenkins
nginx
```

plus UID/GID values written to `.env`.

### Docker Compose

The source deploys:

```text
streamlit_calc
flask
jenkins
nginx
```

### TLS material

It copies the previously prepared:

```text
combined certificate
private key
```

into the expected project directories.

### Flask credentials

The source also places:

```text
flask/config/auth_flask.json
```

into the expected location.

### DNS apex A record

The source changes:

```text
@
```

to point to the GCP static external IP.

### Expand firewall

The earlier rule allowed only:

```text
8501
```

Now the source allows:

```text
8501
8502
8504
```

for Streamlit, Flask, and Jenkins.

### Deploy

```bash
docker-compose up -d --build
```

The source notes that Jenkins permissions may need to be reapplied after files are created during runtime.

---

## 6. Level 3 — move the GCP deployment to HTTPS subdomains

The final level in Chapter 7 mirrors Chapter 6's AWS subdomain design.

### DNS records

The source creates A records:

```text
@         → GCP static IP
streamlit → GCP static IP
flask     → GCP static IP
jenkins   → GCP static IP
```

### Firewall update

It removes:

```text
8501
8502
8504
```

from public access and permits:

```text
80
443
```

### Docker Compose

Nginx now publishes:

```yaml
- "80:80"
- "443:443"
```

rather than one external port per app.

### Nginx

Host-based routes use:

```text
streamlit.domain → streamlit_calc:8501
flask.domain     → flask:8502
jenkins.domain   → jenkins:8080
```

### Redeploy

The source performs:

```bash
sudo docker-compose down
sudo docker-compose up -d --build
```

and expects:

```text
https://streamlit.domain
https://flask.domain
https://jenkins.domain
```

[[IMAGE_NEEDED: Three-level GCP deployment progression | A three-stage diagram: Level 1 static-IP Streamlit on 8501 → Level 2 full multi-service SSL stack on 8501/8502/8504 → Level 3 subdomains over 80/443 | Learner should notice how the chapter grows complexity incrementally]]

{{exercise:M08.L07.EX03}}

---

## 7. What changed from AWS, and what stayed the same?

### Changed cloud primitives

AWS source concepts:

```text
EC2
Security Groups
Elastic IP
Network Load Balancer
```

GCP source concepts:

```text
Compute Engine VM
VPC Firewall Rules
Static External IP
later: global load balancer
```

### Reused application design

Across both providers, the source keeps:

```text
Docker
Docker Compose
Nginx
Streamlit
Flask
Jenkins
TLS certificate files
DNS provider
```

This demonstrates cloud portability at the application layer.

The VM/network provisioning changes.

The containers and reverse-proxy design largely remain the same.

---

## Important misconceptions

### Misconception 1
> "Migrating to GCP requires rewriting the application stack."

The source largely reuses the same repository, Docker Compose files, Nginx configuration, and application services.

### Misconception 2
> "The startup script is application code."

It is VM bootstrap automation.

### Misconception 3
> "The GCP firewall automatically applies to every VM."

The source explicitly targets a network tag.

### Misconception 4
> "The static IP and VM internal identity are the same concept."

The static external IP is the stable client-facing address used in this chapter.

### Misconception 5
> "Level 1 is the final secure architecture."

It is an incremental validation step before TLS and subdomains.

---

## Key terminology

| Term | Meaning |
|---|---|
| GCP Project | Resource/administrative boundary in Google Cloud |
| Compute Engine | GCP virtual-machine service |
| Compute Admin | IAM role used by the source |
| Startup script | Script executed to bootstrap the VM |
| Network tag | Label targeted by GCP firewall rules |
| Static external IP | Reserved stable public IP |
| VPC firewall rule | Network traffic rule in GCP |
| Target tag | Network tag identifying VMs affected by a firewall rule |
| Level 1/2/3 | Source's progressive deployment stages |

---

## Self-check

1. Which GCP IAM role does the source grant?
2. What VM size does the source initially choose?
3. What does the startup script install?
4. Why enable Docker inside the startup script?
5. What is `vm-network-tag` used for?
6. Why reserve a static external IP?
7. What does Level 1 deploy?
8. Which firewall port does Level 1 allow?
9. What additional services appear in Level 2?
10. Which three application ports does Level 2 allow?
11. What changes in Level 3?
12. Which DNS A records are created?
13. Which parts of the AWS application stack are reused on GCP?

---

## Retain this idea

**Cloud migration can preserve the application architecture while replacing provider-specific infrastructure: automate the new VM, reproduce network controls, then progressively reapply the same container, proxy, TLS, and subdomain design.**
""",
        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "gcp-project", "title": "Recreate the deployment on another cloud", "order": 1},
            {"id": "gcp-vm", "title": "Create the Compute Engine VM with a startup script", "order": 2},
            {"id": "gcp-ssh-static-ip", "title": "Configure SSH and reserve a static external IP", "order": 3},
            {"id": "level1", "title": "Level 1 — deploy a simple Streamlit app directly", "order": 4},
            {"id": "level2", "title": "Level 2 — deploy the full SSL application stack", "order": 5},
            {"id": "level3", "title": "Level 3 — move the GCP deployment to HTTPS subdomains", "order": 6},
            {"id": "cloud-comparison", "title": "What changed from AWS, and what stayed the same?", "order": 7},
        ],
    },

    "exercises": [
        {
            "id": "M08.L07.EX01",
            "title": "Explain the GCP Startup Script",
            "lesson_code": "M08.L07",
            "section_id": "gcp-vm",
            "placement": "after_section",
            "description": "Turn the source bootstrap script into a reproducibility model.",
            "instructions": (
                "List each category automated by the startup script: OS updates, Python, Docker, service enablement, "
                "Docker group, Compose, Git, and version verification. Explain what manual failure each automation avoids."
            ),
            "expected_output": "A bootstrap-task table with purpose and reproducibility benefit.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["gcp", "startup-script", "automation"],
        },
        {
            "id": "M08.L07.EX02",
            "title": "Trace the GCP Firewall Match",
            "lesson_code": "M08.L07",
            "section_id": "level1",
            "placement": "after_section",
            "description": "Understand network-tag-based firewall targeting.",
            "instructions": (
                "Trace a request from your trusted /32 IP to STATIC_IP:8501. Identify source range, firewall target tag, "
                "VM network tag, protocol/port, and Streamlit process. Then explain what would happen if the VM lost the tag."
            ),
            "expected_output": "A tagged-firewall traffic path and failure explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["gcp-firewall", "network-tags", "cidr"],
        },
        {
            "id": "M08.L07.EX03",
            "title": "Compare the Three Deployment Levels",
            "lesson_code": "M08.L07",
            "section_id": "level3",
            "placement": "after_section",
            "description": "Make the chapter's incremental architecture explicit.",
            "instructions": (
                "Create a comparison table for Level 1, Level 2, and Level 3. Include services, public ports, DNS style, "
                "TLS, Docker Compose, Nginx, and firewall configuration."
            ),
            "expected_output": "A three-level architecture comparison table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["gcp", "deployment-architecture", "nginx", "docker-compose"],
        },
    ],

    "quiz": {
        "id": "M08.L07.QZ01",
        "title": "GCP Infrastructure Setup — Knowledge Check",
        "lesson_code": "M08.L07",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L07.Q01", "section_id": "gcp-project", "question": "Which GCP role does the source grant?", "options": ["Viewer", "Compute Admin", "Billing Admin", "Kubernetes Admin"], "correct": 1, "explanation": "The source selects Compute Engine → Compute Admin."},
            {"id": "M08.L07.Q02", "section_id": "gcp-vm", "question": "Which source VM type is used initially?", "options": ["e2-micro", "e2-standard-8", "n2-highmem-2", "t2.xlarge"], "correct": 1, "explanation": "Chapter 7 uses e2-standard-8."},
            {"id": "M08.L07.Q03", "section_id": "gcp-vm", "question": "What is the purpose of `vm-network-tag`?", "options": ["Name Docker images", "Match firewall rules to VM instances", "Create SSL SANs", "Configure Git"], "correct": 1, "explanation": "The source firewall targets this network tag."},
            {"id": "M08.L07.Q04", "section_id": "gcp-ssh-static-ip", "question": "Why reserve a static external IP?", "options": ["Stable VM endpoint", "Train Random Forest", "Store Jenkins state", "Create Git branch"], "correct": 0, "explanation": "The source uses it for stable SSH, DNS, and app access."},
            {"id": "M08.L07.Q05", "section_id": "level1", "question": "Which port does Level 1 expose?", "options": ["22", "443", "8501", "8504"], "correct": 2, "explanation": "The first GCP Streamlit validation uses port 8501."},
            {"id": "M08.L07.Q06", "section_id": "level2", "question": "Which services are deployed together at Level 2?", "options": ["Only Streamlit", "Streamlit, Flask, Jenkins, and Nginx", "Only Jenkins", "Only Flask"], "correct": 1, "explanation": "The source reuses the full multi-service stack."},
            {"id": "M08.L07.Q07", "section_id": "level2", "question": "Which public app ports are allowed in Level 2?", "options": ["80,443", "8501,8502,8504", "8080,9090", "22 only"], "correct": 1, "explanation": "Level 2 still exposes the three application-specific ports."},
            {"id": "M08.L07.Q08", "section_id": "level3", "question": "Which public web ports remain after moving to subdomains?", "options": ["8501/8502/8504", "80/443", "8080 only", "22/8501"], "correct": 1, "explanation": "The source standardizes on HTTP/HTTPS ports."},
            {"id": "M08.L07.Q09", "section_id": "cloud-comparison", "question": "Which layer is mostly reused across AWS and GCP?", "options": ["Cloud VM provisioning", "Docker/Nginx/application stack", "Provider IAM model", "Provider firewall UI"], "correct": 1, "explanation": "The application stack remains largely the same."},
            {"id": "M08.L07.Q10", "section_id": "cloud-comparison", "type": "open", "question": "Explain how Chapter 7 recreates the previous AWS deployment on GCP through Levels 1, 2, and 3."},
        ],
        "passing_score": 70,
    },
}
