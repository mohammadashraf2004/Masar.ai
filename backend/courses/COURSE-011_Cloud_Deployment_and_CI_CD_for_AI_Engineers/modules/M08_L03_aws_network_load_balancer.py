"""M08.L03 — AWS Network Load Balancer and Target Groups.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 3, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L03"
MODULE_ORDER = 8
MODULE_TITLE = "Secure AWS Deployment Foundations"
MODULE_DESCRIPTION = "Add a Network Load Balancer and target-group routing in front of the EC2 application server."
SOURCE_CHAPTER = 3
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "AWS Network Load Balancer and Target Groups",
    "slug": "aws-network-load-balancer-target-groups-m08-l03",
    "description": (
        "Place an AWS Network Load Balancer in front of the EC2 server, route multiple TCP services "
        "through target groups, reorganize security groups, and validate Streamlit access through the load-balancer DNS."
    ),
    "order": 3,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 2.75,
    "skill_tags": ["aws", "network-load-balancer", "target-groups", "vpc", "security-groups", "tcp", "streamlit"],
    "prerequisite_ids": ["M08.L02"],

    "lesson": {
        "title": "AWS Network Load Balancer and Target Groups",
        "content": r"""
# AWS Network Load Balancer and Target Groups

> **Course:** Secure AWS Deployment Foundations  
> **Lesson:** M08.L03  
> **Source alignment:** BOOK-XXX, Chapter 3. This lesson follows the source's Network Load Balancer design and ports exactly as a learning architecture.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the load balancer as the public gateway in the source architecture.
- Explain the roles of listeners and target groups.
- Explain why target registration uses the EC2 private IP.
- Configure the source's TCP listener/target-group mapping for ports 8501, 8502, 8504, and 22.
- Explain the importance of using the same VPC and compatible network placement.
- Describe the source's security-group reorganization.
- Explain the traffic path from client to NLB to target group to EC2 application.
- Validate the Streamlit application through the load balancer's DNS endpoint.

---

## 1. Why put a load balancer in front of the instance?

In the previous lesson, the browser reached:

```text
EC2 Elastic IP:8501
```

directly.

Chapter 3 introduces another layer:

```text
Internet
   ↓
Load Balancer
   ↓
Target Group
   ↓
EC2 private IP
   ↓
Application
```

The source describes the load balancer as a gateway that:

- receives public requests,
- forwards them to target groups,
- provides another control layer in front of the server,
- helps distribute incoming requests.

### Architectural change

Before:

```text
client → EC2 public IP
```

After:

```text
client → load balancer → EC2
```

This decouples the client-facing endpoint from the application server itself.

[[IMAGE_NEEDED: Network Load Balancer fronting EC2 | A diagram showing a trusted external client reaching an internet-facing AWS Network Load Balancer, which forwards through TCP target groups to the EC2 instance's private IP | Learner should notice that the load balancer becomes the public gateway while EC2 is reached as a backend target]]

---

## 2. Create the Network Load Balancer

The source selects:

```text
Network Load Balancer
```

with:

```text
Scheme: internet-facing
IP address type: IPv4
```

It also emphasizes selecting the same VPC used by the EC2 instance.

### VPC alignment

A target and load balancer need compatible networking.

The source repeatedly tells the learner to verify:

- VPC,
- availability-zone/subnet context,
- EC2 private IPv4 address.

### First listener

The source's first application listener is:

```text
Protocol: TCP
Port: 8501
```

This matches the Streamlit application.

The listener's default action forwards to:

```text
target group tg-8501
```

---

## 3. Target groups connect listeners to backend services

A target group defines where the load balancer should forward traffic.

The source creates:

```text
Target type: IP addresses
Protocol: TCP
Port: 8501
```

and registers:

```text
EC2 private IP
```

### Why private IP?

The request path inside the VPC is:

```text
NLB
 ↓
target group
 ↓
EC2 private IP
```

The source is intentionally moving backend routing away from direct use of the instance's public address.

### Health checks

The first target group uses the default:

```text
TCP health check
```

The load balancer uses health information to determine whether a target should receive traffic.

### Listener versus target group

Think:

```text
Listener
= which front-door port receives traffic?

Target group
= which backend target(s) should receive that traffic?
```

{{exercise:M08.L03.EX01}}

---

## 4. Add target groups for multiple services

The source expands the architecture beyond Streamlit.

Its final port set is:

| Service | TCP port | Example target-group name |
|---|---:|---|
| SSH | 22 | `tg-ssh-22` |
| Streamlit | 8501 | `tg-8501` |
| Flask API | 8502 | `tg-flask-8502` |
| Jenkins | 8504 | `tg-jenkins-8504` |

Each target group registers the EC2 private IP.

Then each load-balancer listener forwards to the corresponding group.

### Mental model

```text
NLB
├── TCP 22   → tg-ssh-22     → EC2 private IP:22
├── TCP 8501 → tg-8501       → EC2 private IP:8501
├── TCP 8502 → tg-flask-8502 → EC2 private IP:8502
└── TCP 8504 → tg-jenkins    → EC2 private IP:8504
```

This is port-based routing at the TCP listener level in the source's architecture.

[[IMAGE_NEEDED: Multi-port NLB target-group map | A central Network Load Balancer with four TCP listeners—22, 8501, 8502, 8504—each pointing to a correspondingly named target group that registers the same EC2 private IP on the matching port | Learner should notice that one EC2 host can expose multiple backend services through separate listener/target-group pairs]]

---

## 5. Reorganize security groups around the load balancer

The source then changes network access rules.

Its desired security model is:

```text
trusted external IP/VPN
        ↓
load balancer security group
        ↓
load balancer
        ↓
EC2 security group permits load-balancer-origin traffic
        ↓
EC2 services
```

### Load-balancer security group

The source shows inbound rules for:

```text
22
8501
8502
8504
```

restricted to a trusted public `/32` address.

### EC2 security group

The source's diagram then shows the EC2 instance allowing application ports from the load balancer side rather than broadly from the public client.

The source specifically illustrates the load balancer private address as the source for EC2 inbound rules.

This is the source architecture being taught.

### Security goal

The design intent is:

> external users interact with the load-balancer layer, while the EC2 instance is no longer the primary public-facing application endpoint.

{{exercise:M08.L03.EX02}}

---

## 6. Validate Streamlit through the load balancer

The Streamlit process still runs on the EC2 instance:

```bash
cd ~/Documents/GitHub/deploy-secure-ds-apps-book
source venv-webs/bin/activate
streamlit run st_example.py
```

But the browser now uses the load-balancer DNS name:

```text
LOAD_BALANCER_DNS:8501
```

instead of:

```text
EC2_ELASTIC_IP:8501
```

### Traffic path

```text
Browser
   ↓
NLB DNS :8501
   ↓
TCP listener 8501
   ↓
tg-8501
   ↓
EC2 private IP :8501
   ↓
Streamlit
```

If the page loads, you have validated:

- NLB creation,
- listener configuration,
- target registration,
- health,
- VPC routing,
- security groups,
- Streamlit process.

[[IMAGE_NEEDED: Streamlit request through NLB | A request-flow diagram from browser → load-balancer DNS:8501 → TCP listener → tg-8501 → EC2 private IP:8501 → Streamlit | Learner should notice that the application process has not changed; the network entry path has]]

{{exercise:M08.L03.EX03}}

---

## Important misconceptions

### Misconception 1
> "The listener and target group are the same object."

The listener receives traffic; the target group defines backend destinations.

### Misconception 2
> "The target group registers the browser's public IP."

The source registers the EC2 instance's private IP.

### Misconception 3
> "Every service needs a separate EC2 instance."

The source routes several ports to one EC2 private IP.

### Misconception 4
> "Adding a load balancer means security groups are no longer needed."

The source uses security groups at both the load-balancer and EC2 layers.

---

## Key terminology

| Term | Meaning |
|---|---|
| Network Load Balancer | AWS load balancer used by the source for TCP traffic |
| Listener | Front-end protocol/port that receives load-balancer traffic |
| Target group | Backend destination group for a listener |
| Target | Registered backend such as an EC2 private IP and port |
| Health check | Test used to determine target availability |
| VPC | Private AWS network containing the resources |
| Internet-facing | Load-balancer scheme reachable from external networks |
| DNS name | Hostname AWS assigns to the load balancer |

---

## Self-check

1. What changes when the NLB is added in front of EC2?
2. What does a listener do?
3. What does a target group do?
4. Why does the source register the EC2 private IP?
5. Which port is used for Streamlit?
6. Which port is used for Flask?
7. Which port is used for Jenkins?
8. Which port is used for SSH?
9. What is the intended security-group relationship between trusted client, NLB, and EC2?
10. Trace a browser request all the way to the Streamlit process.

---

## Retain this idea

**A load balancer separates the client-facing entry point from the application server: listeners receive traffic, target groups define backend destinations, and security groups control which network paths are allowed at each layer.**
""",
        "estimated_minutes": 165,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "why-lb", "title": "Why put a load balancer in front of the instance?", "order": 1},
            {"id": "nlb-create", "title": "Create the Network Load Balancer", "order": 2},
            {"id": "target-group", "title": "Target groups connect listeners to backend services", "order": 3},
            {"id": "multi-target-groups", "title": "Add target groups for multiple services", "order": 4},
            {"id": "sg-reorg", "title": "Reorganize security groups around the load balancer", "order": 5},
            {"id": "validate-lb", "title": "Validate Streamlit through the load balancer", "order": 6},
        ],
    },

    "exercises": [
        {
            "id": "M08.L03.EX01",
            "title": "Map Listener to Target Group",
            "lesson_code": "M08.L03",
            "section_id": "target-group",
            "placement": "after_section",
            "description": "Practice separating front-door listener configuration from backend target registration.",
            "instructions": (
                ('1. For the Streamlit path, write the values for listener protocol/port, target type, target-group protocol/port, registered address, and health-check type.\n'
                 '2. Then explain the role of each field.')
            ),
            "expected_output": "A listener/target-group mapping table for port 8501.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["nlb", "listeners", "target-groups"],
        },
        {
            "id": "M08.L03.EX02",
            "title": "Design the Four-Port Routing Table",
            "lesson_code": "M08.L03",
            "section_id": "sg-reorg",
            "placement": "after_section",
            "description": "Represent the complete source port-routing model.",
            "instructions": (
                ('1. Create one table for TCP ports 22, 8501, 8502, and 8504.\n'
                 '2. Include service, listener, target group, backend EC2 private IP, and trusted external source rule.\n'
                 '3. Then explain which layer is public-facing.')
            ),
            "expected_output": "A four-service NLB routing and security table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["networking", "security-groups", "target-groups"],
        },
        {
            "id": "M08.L03.EX03",
            "title": "Debug a Broken Load-Balancer Path",
            "lesson_code": "M08.L03",
            "section_id": "validate-lb",
            "placement": "after_section",
            "description": "Use the source architecture to reason about a failed request.",
            "instructions": (
                ('1. Suppose LOAD_BALANCER_DNS:8501 does not load.\n'
                 '2. Check the path in order: Streamlit process, EC2 port, target health, target-group registration, listener mapping, security groups, and client source.\n'
                 '3. Explain what evidence you would seek at each step.')
            ),
            "expected_output": "A layered troubleshooting checklist from application to client.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["troubleshooting", "nlb", "streamlit", "security-groups"],
        },
    ],

    "quiz": {
        "id": "M08.L03.QZ01",
        "title": "AWS Network Load Balancer and Target Groups — Knowledge Check",
        "lesson_code": "M08.L03",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L03.Q01", "section_id": "why-lb", "question": "What becomes the public gateway in the source architecture?", "options": ["GitHub", "Network Load Balancer", "Python venv", "IAM group"], "correct": 1, "explanation": "The load balancer sits in front of the EC2 server."},
            {"id": "M08.L03.Q02", "section_id": "nlb-create", "question": "Which scheme does the source choose?", "options": ["internal", "internet-facing", "private-only", "local"], "correct": 1, "explanation": "The source selects an internet-facing NLB."},
            {"id": "M08.L03.Q03", "section_id": "target-group", "question": "Which address is registered as the target?", "options": ["Client public IP", "EC2 private IP", "GitHub IP", "IAM user ID"], "correct": 1, "explanation": "The target group registers the EC2 private IP."},
            {"id": "M08.L03.Q04", "section_id": "target-group", "question": "What does the listener define?", "options": ["Front-end protocol/port", "Python packages", "Git branch", "SSL CSR"], "correct": 0, "explanation": "The listener receives traffic on a protocol/port and forwards to a target group."},
            {"id": "M08.L03.Q05", "section_id": "multi-target-groups", "question": "Which port is mapped to Flask in the source?", "options": ["22", "8501", "8502", "8504"], "correct": 2, "explanation": "The source uses TCP 8502 for Flask."},
            {"id": "M08.L03.Q06", "section_id": "multi-target-groups", "question": "Which port is mapped to Jenkins?", "options": ["22", "8501", "8502", "8504"], "correct": 3, "explanation": "The source uses TCP 8504 for Jenkins."},
            {"id": "M08.L03.Q07", "section_id": "sg-reorg", "question": "What source does the NLB security group allow in the example?", "options": ["Trusted /32 IP", "Every IPv4 address", "Docker Hub only", "No inbound traffic"], "correct": 0, "explanation": "The source restricts public entry to a trusted address."},
            {"id": "M08.L03.Q08", "section_id": "validate-lb", "question": "What hostname does the browser use after adding the NLB?", "options": ["EC2 private hostname only", "Load-balancer DNS name", "GitHub repository name", "IAM username"], "correct": 1, "explanation": "The source validates the app through the NLB DNS name."},
            {"id": "M08.L03.Q09", "section_id": "validate-lb", "question": "Which component actually runs Streamlit?", "options": ["NLB", "EC2 instance", "Target group", "Security group"], "correct": 1, "explanation": "The NLB forwards traffic; Streamlit still runs on EC2."},
            {"id": "M08.L03.Q10", "section_id": "validate-lb", "type": "open", "question": "Trace a Streamlit request from the browser through the NLB to the EC2 process."},
        ],
        "passing_score": 70,
    },
}
