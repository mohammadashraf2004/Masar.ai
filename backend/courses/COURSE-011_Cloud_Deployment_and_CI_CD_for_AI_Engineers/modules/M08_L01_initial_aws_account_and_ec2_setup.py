"""M08.L01 — Initial AWS Account and EC2 Setup.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 1, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L01"
MODULE_ORDER = 8
MODULE_TITLE = "Secure AWS Deployment Foundations"
MODULE_DESCRIPTION = (
    "Build the base AWS environment for later application deployment: secure account access, "
    "IAM, EC2, security groups, key pairs, storage, and a stable Elastic IP."
)
SOURCE_CHAPTER = 1
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Initial AWS Account and EC2 Setup",
    "slug": "initial-aws-account-ec2-setup-m08-l01",
    "description": (
        "Prepare an AWS account for application deployment by separating root and developer access, "
        "launching an EC2 server, restricting inbound traffic with security groups, and assigning "
        "a stable Elastic IP."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 2.5,
    "skill_tags": [
        "aws", "iam", "ec2", "security-groups", "elastic-ip",
        "cloud-security", "networking", "module-08",
    ],
    "prerequisite_ids": ["M07.L01"],

    "lesson": {
        "title": "Initial AWS Account and EC2 Setup",
        "content": r"""
# Initial AWS Account and EC2 Setup

> **Course:** Secure AWS Deployment Foundations  
> **Lesson:** M08.L01  
> **Module:** Secure AWS Deployment Foundations  
> **Source alignment:** BOOK-XXX, Chapter 1. This lesson follows the supplied chapter closely and treats its instance sizes, policies, ports, and console choices as source-specific exercise settings rather than universal defaults.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why routine development should not be performed with the AWS root user.
- Explain the source's use of 2FA and a separate IAM user.
- Distinguish an IAM user, group, and attached policy.
- Explain the source's EC2 configuration choices: AMI, instance type, key pair, and storage.
- Explain why a `.pem` private key must be protected.
- Define a security group as a virtual firewall.
- Explain CIDR `/32` as a single IPv4 address in the source's access-control example.
- Map the source's application ports to SSH, Streamlit, Flask, and Jenkins.
- Explain why trusted-IP or VPN restrictions reduce exposure.
- Explain why an Elastic IP provides stable public addressing for an EC2 instance.
- Describe the final Chapter 1 infrastructure from user identity to network access.

---

## 1. Start with account security, not application deployment

The source begins with an important cloud principle:

> Before deploying an application, secure the account that controls the infrastructure.

A new AWS account initially gives you the **root user**.

The root user has unrestricted account-level power.

That makes it inappropriate for routine development work.

The source's workflow is:

```text
AWS root account
      ↓
enable 2FA
      ↓
create IAM user
      ↓
work as IAM user instead of root
```

### Why separate root from daily work?

If everyday work uses the root identity, a mistake or credential compromise has the widest possible impact.

A separate IAM identity creates a boundary between:

```text
account ownership
```

and:

```text
day-to-day technical work
```

### Root 2FA

The chapter explicitly tells the learner to enable **Two-Factor Authentication (2FA)** for the root account.

The idea is straightforward:

```text
password only
    <
password + second factor
```

The second factor makes account takeover harder when a password is exposed.

---

## 2. IAM users, groups, and permissions

**IAM** is AWS Identity and Access Management.

The chapter creates a developer-oriented user and adds it to a group.

Conceptually:

```text
IAM User
   ↓ member of
IAM Group
   ↓ has
Policies
   ↓ allow
AWS actions/resources
```

### IAM user

The source uses a descriptive example such as:

```text
developer-user
```

This identity is intended for the hands-on deployment work.

### IAM group

The source creates a group such as:

```text
developer-group
```

Instead of managing permissions separately for each person, permissions can be attached to the group.

### Policies used by the source

The supplied chapter lists:

```text
AmazonEC2FullAccess
AmazonS3FullAccess
ElasticLoadBalancingFullAccess
```

These are the permissions the source uses for its exercise path.

They should be understood as **source-specific training permissions**.

The chapter itself motivates this setup through the principle of least privilege, even though these named managed policies are broad within their respective services.

### Practical lesson

The security principle is not:

> "Every developer should always receive these exact three policies."

The source-supported lesson is:

> Use a separate IAM identity and intentionally assign the permissions needed for the deployment work instead of using the unrestricted root user.

[[IMAGE_NEEDED: AWS root versus IAM daily-access model | A diagram showing Root User protected with 2FA and used for account-level control, while an IAM developer user belongs to a developer group with scoped service policies | Learner should notice the separation between account ownership and routine development access]]

{{exercise:M08.L01.EX01}}

---

## 3. EC2: create the server that will host the applications

An **EC2 instance** is a virtual server running in AWS.

The source creates one machine that will later host several services.

Its example configuration is:

```text
Name: my-web-server
AMI: Amazon Linux 2
Instance type: t2.xlarge
```

The source describes `t2.xlarge` as:

```text
4 vCPUs
16 GiB memory
```

and chooses it so the machine can host several tools and applications during the book exercises.

### AMI

An **Amazon Machine Image (AMI)** defines the starting operating-system image.

The source chooses Amazon Linux 2.

That choice affects later commands, which is why the next chapter uses tools such as:

```bash
yum
```

### Instance type

The instance type controls compute capacity such as:

- CPU,
- memory.

In the source, the machine is intentionally large enough for several later services.

### Key pair

The chapter creates an EC2 key pair and downloads a file such as:

```text
my-web-server-key-pair.pem
```

{{image:ec2-key-pair}}

This private key will later be used for SSH.

Treat it as sensitive.

Conceptually:

```text
public-key side
   → associated with EC2 access

private .pem key
   → stays with you
```

Do not casually share the private key.

### Storage

The source recommends increasing the root volume to at least:

```text
50 GiB
```

and suggests:

```text
100 GiB
```

as a practical starting point for its Docker-heavy exercises.

Its reasoning is that repeated Docker builds and cached images consume disk space.

This is a valuable operational lesson:

> Storage planning matters even when CPU and memory look sufficient.

---

## 4. Security groups: control who can reach the server

A **security group** acts as a virtual firewall around AWS resources such as EC2 instances.

It controls:

- inbound traffic,
- outbound traffic.

The source's security group is designed for four services.

### Inbound ports in the source

| Purpose | Protocol | Port |
|---|---|---:|
| SSH | TCP | 22 |
| Streamlit | TCP | 8501 |
| Flask | TCP | 8502 |
| Jenkins | TCP | 8504 |

The source does **not** open these ports to everyone.

Instead, it restricts them to a trusted address such as:

```text
35.123.123.58/32
```

### What does `/32` mean?

For IPv4, `/32` represents one exact address.

So:

```text
35.123.123.58/32
```

means:

> only this single IPv4 address is allowed by that rule.

### VPN access

The source also discusses corporate VPN access.

If employees emerge onto the internet from a known VPN egress address, the security group can allow that trusted source.

This creates a practical access path:

```text
developer
   ↓
corporate VPN
   ↓
known public IP
   ↓
security group allows request
   ↓
EC2 service
```

### Default outbound behavior

The source leaves outbound rules at their default:

```text
allow all outbound traffic
```

That is part of the source's exercise configuration.

### Why this matters

Compare:

```text
0.0.0.0/0
```

for a sensitive administrative port with:

```text
trusted-ip/32
```

The second has a far smaller exposed surface.

[[IMAGE_NEEDED: EC2 security-group access model | A diagram showing a trusted developer IP or corporate VPN on the internet sending TCP traffic to EC2 only on ports 22, 8501, 8502, and 8504, while other sources are blocked | Learner should notice that a security group filters traffic before it reaches the instance]]

{{exercise:M08.L01.EX02}}

---

## 5. Elastic IP: keep a stable public address

A normal public EC2 address can change when an instance is stopped and started.

That creates a practical problem.

Suppose your SSH command is:

```bash
ssh -i my-key.pem ec2-user@PUBLIC_IP
```

If `PUBLIC_IP` changes after a restart, your connection configuration is stale.

The source solves this with an **Elastic IP**.

### Elastic IP concept

An Elastic IP is a public IPv4 address that you allocate and associate with an AWS resource such as an EC2 instance.

The source's process is:

```text
allocate Elastic IP
      ↓
select EC2 instance
      ↓
select instance private IP
      ↓
associate
```

Now the instance has a stable public address for later steps.

### Public versus private IP

The source also makes you identify the instance's private IP.

These addresses serve different roles.

```text
Public / Elastic IP
→ reachable from external networks according to security rules

Private IP
→ address inside the AWS VPC network
```

The private IP becomes important in the later load-balancer lesson.

---

## 6. Put Chapter 1 together

At the end of this lesson, the source has built the following foundation:

```text
Root User
   └── protected with 2FA

IAM Developer User
   └── permissions through IAM group/policies

Trusted IP / VPN
   ↓
Security Group
   ↓
EC2 Instance
   ├── Amazon Linux 2
   ├── key pair
   ├── expanded storage
   └── application ports

Elastic IP
   ↓
stable public address for EC2
```

This infrastructure is not yet the final production architecture.

It is the base that Chapters 2–4 build on.

---

## Important misconceptions

### Misconception 1
> "The AWS root user is the normal developer account."

The source explicitly separates routine work from root-level access.

### Misconception 2
> "An IAM user and an EC2 user are the same thing."

They are different concepts.

IAM controls AWS API/console identity. Later, `ec2-user` is the Linux account used when connecting to the Amazon Linux machine.

### Misconception 3
> "A security group is application code."

A security group is network-access configuration around AWS resources.

### Misconception 4
> "`/32` opens the port to the whole internet."

In the source's IPv4 examples, `/32` identifies one exact address.

### Misconception 5
> "An Elastic IP and a private IP are interchangeable."

They have different network roles.

---

## Key terminology

| Term | Meaning |
|---|---|
| AWS root user | Account-level identity with unrestricted account access |
| 2FA | Second authentication factor in addition to a password |
| IAM | AWS Identity and Access Management |
| IAM user | AWS identity for a person or workload |
| IAM group | Collection of IAM users sharing permissions |
| Policy | Permissions document controlling allowed AWS actions |
| EC2 | AWS virtual compute service |
| AMI | Starting machine image for an EC2 instance |
| Instance type | EC2 compute size/capacity |
| Key pair | Public/private key material used for instance access |
| `.pem` file | Private-key file format used in the source's EC2 SSH setup |
| Security group | AWS virtual firewall |
| CIDR `/32` | Single IPv4-address range |
| Elastic IP | Allocated public IPv4 address that can remain stable across instance lifecycle events |
| Private IP | Address used inside the VPC network |

---

## Self-check

1. Why does the source move daily work away from the root user?
2. Why enable 2FA on root?
3. What is the relationship between IAM users, groups, and policies?
4. Which three AWS managed policies does the source attach for its exercise?
5. Why does the chapter create a key pair?
6. Why does the source allocate 50–100 GiB of storage?
7. What is a security group?
8. Which four inbound ports does the source configure?
9. What does `/32` mean in the chapter's example?
10. Why does a trusted VPN egress address help restrict access?
11. What problem does an Elastic IP solve?
12. What is the difference between public and private IP addresses in this setup?

---

## Retain this idea

**Secure AWS deployment begins before application code: protect the account, separate identities, create only the required server access paths, and give the server stable addressing for the next deployment stages.**
""",
        "estimated_minutes": 150,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "secure-account", "title": "Start with account security, not application deployment", "order": 1},
            {"id": "iam", "title": "IAM users, groups, and permissions", "order": 2},
            {"id": "ec2", "title": "EC2: create the server that will host the applications", "order": 3},
            {"id": "security-groups", "title": "Security groups: control who can reach the server", "order": 4},
            {"id": "elastic-ip", "title": "Elastic IP: keep a stable public address", "order": 5},
            {"id": "chapter-one-model", "title": "Put Chapter 1 together", "order": 6},
        ],
    },

    "exercises": [
        {
            "id": "M08.L01.EX01",
            "title": "Design the Account Access Model",
            "lesson_code": "M08.L01",
            "section_id": "iam",
            "placement": "after_section",
            "description": "Map the source's root, IAM user, group, and policy model.",
            "instructions": (
                ('1. Draw the access chain Root → 2FA → IAM user → IAM group → policies.\n'
                 '2. Then explain why routine deployment work should use the IAM identity rather than root.\n'
                 '3. List the three managed policies used by the source and label them as exercise-specific.')
            ),
            "expected_output": "An identity/permission diagram plus a short security explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["iam", "least-privilege", "aws-account-security"],
        },
        {
            "id": "M08.L01.EX02",
            "title": "Build the Source Security-Group Table",
            "lesson_code": "M08.L01",
            "section_id": "security-groups",
            "placement": "after_section",
            "description": "Translate the source's inbound access design into a clear rule table.",
            "instructions": (
                ('1. Create a table for ports 22, 8501, 8502, and 8504.\n'
                 '2. Include service, protocol, source CIDR, and why each port exists.\n'
                 '3. Then explain the difference between allowing one /32 address and exposing the same port broadly.')
            ),
            "expected_output": "A four-row inbound-rule table plus an exposure comparison.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["security-groups", "cidr", "network-access"],
        },
        {
            "id": "M08.L01.EX03",
            "title": "Trace the Addressing Model",
            "lesson_code": "M08.L01",
            "section_id": "elastic-ip",
            "placement": "after_section",
            "description": "Differentiate the Elastic IP from the instance private IP.",
            "instructions": (
                ("1. Explain what happens to your external SSH configuration when the instance's public address changes.\n"
                 '2. Explain how an Elastic IP solves that problem.\n'
                 "3. Explain why the instance's private IP still matters for later AWS networking.")
            ),
            "expected_output": "A public/private addressing explanation with a small network diagram.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["elastic-ip", "private-ip", "ec2-networking"],
        },
    ],

    "quiz": {
        "id": "M08.L01.QZ01",
        "title": "Initial AWS Account and EC2 Setup — Knowledge Check",
        "lesson_code": "M08.L01",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L01.Q01", "section_id": "secure-account", "question": "Which identity does the source avoid using for routine developer work?", "options": ["IAM user", "AWS root user", "ec2-user", "Docker user"], "correct": 1, "explanation": "The source protects root with 2FA and creates a separate IAM user for daily work."},
            {"id": "M08.L01.Q02", "section_id": "iam", "question": "What is the role of an IAM group in the lesson?", "options": ["Store EC2 disks", "Group users around shared permissions", "Assign Elastic IPs", "Create SSH tunnels"], "correct": 1, "explanation": "The source adds the developer user to a group that carries AWS policies."},
            {"id": "M08.L01.Q03", "section_id": "ec2", "question": "What does the AMI define?", "options": ["Starting machine image", "Security-group CIDR", "Elastic IP", "IAM password"], "correct": 0, "explanation": "The AMI provides the starting operating-system image."},
            {"id": "M08.L01.Q04", "section_id": "ec2", "question": "Why does the source increase EC2 storage?", "options": ["For Route 53", "To accommodate Docker caches and temporary files", "To create an IAM group", "To enable 2FA"], "correct": 1, "explanation": "The source specifically cites Docker image caching and temporary files."},
            {"id": "M08.L01.Q05", "section_id": "security-groups", "question": "What does a security group primarily control?", "options": ["Git history", "Network traffic", "Docker layers", "SSL issuance"], "correct": 1, "explanation": "The source defines it as a virtual firewall controlling inbound and outbound traffic."},
            {"id": "M08.L01.Q06", "section_id": "security-groups", "question": "Which source port is used for SSH?", "options": ["22", "8501", "8502", "8504"], "correct": 0, "explanation": "The chapter uses TCP port 22 for SSH."},
            {"id": "M08.L01.Q07", "section_id": "security-groups", "question": "What does 35.123.123.58/32 represent in the example?", "options": ["All IPv4 addresses", "One IPv4 address", "One VPC", "One port range"], "correct": 1, "explanation": "A /32 IPv4 CIDR represents one exact IP address."},
            {"id": "M08.L01.Q08", "section_id": "elastic-ip", "question": "Why does the source allocate an Elastic IP?", "options": ["To install Python", "To keep a stable public address", "To encrypt SSH", "To create a Docker registry"], "correct": 1, "explanation": "The source wants a public IP that does not change after instance restarts."},
            {"id": "M08.L01.Q09", "section_id": "elastic-ip", "question": "Which address becomes important for later load-balancer target registration?", "options": ["EC2 private IP", "Root password", "IAM username", "Docker bridge only"], "correct": 0, "explanation": "Later source chapters register the EC2 private IP as a load-balancer target."},
            {"id": "M08.L01.Q10", "section_id": "chapter-one-model", "type": "open", "question": "Describe the final Chapter 1 architecture from account identity through network access and EC2 addressing."},
        ],
        "passing_score": 70,
    },
}
