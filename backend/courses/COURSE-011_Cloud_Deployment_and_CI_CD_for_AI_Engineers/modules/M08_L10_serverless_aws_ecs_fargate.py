"""M08.L10 — Serverless Deployment with AWS ECS Fargate.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 10, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L10"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Deploy Flask and Streamlit without managing EC2 servers by publishing container images to ECR, "
    "running them as ECS Fargate services, routing subdomains through an Application Load Balancer, "
    "terminating TLS with ACM, monitoring with CloudWatch, and scaling task counts."
)
SOURCE_CHAPTER = 10
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Serverless Deployment with AWS ECS Fargate",
    "slug": "serverless-aws-ecs-fargate-m08-l10",
    "description": (
        "Build the source's AWS serverless architecture from IAM and AWS CLI through ECR image publishing, "
        "ALB security groups and host routing, ECS task definitions and Fargate services, CloudWatch logs, "
        "custom DNS, ACM-based HTTPS, and manual or automatic service scaling."
    ),
    "order": 10,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 4.5,
    "skill_tags": [
        "aws", "ecs", "fargate", "ecr", "application-load-balancer",
        "target-groups", "iam", "aws-cli", "acm", "cloudwatch",
        "autoscaling", "dns",
    ],
    "prerequisite_ids": ["M08.L09"],

    "lesson": {
        "title": "Serverless Deployment with AWS ECS Fargate",
        "content": r"""
# Serverless Deployment with AWS ECS Fargate

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L10  
> **Source alignment:** BOOK-XXX, Chapter 10. The lesson preserves the supplied ECS/Fargate architecture and source-specific settings. Literal credentials shown in the source are intentionally **not reproduced**. Pasted command-format errors and profile-name inconsistencies are explicitly flagged.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what changes when moving the earlier AWS VM stack to ECS Fargate.
- Explain why Jenkins, Docker Compose, and Nginx disappear from the source's serverless repository layout.
- Create a dedicated source-style IAM user/group for CLI deployment.
- Explain AWS CLI profiles and why access keys must never be committed.
- Explain the ECR image lifecycle: build, tag, authenticate, and push.
- Explain why Fargate target groups use IP targets without manually registered IPs.
- Design separate ALB and ECS-task security groups.
- Explain host-based ALB routing for Flask and Streamlit subdomains.
- Explain why the source returns a default 403 for unmatched/default-DNS requests.
- Define ECS cluster, task definition, task, and service.
- Explain the source's different CPU/memory allocations for Flask and Streamlit.
- Attach ECS services to existing ALB target groups.
- Read container logs through CloudWatch or the ECS console.
- Update DNS to point custom hostnames at the ALB.
- Import the existing certificate into ACM and add an HTTPS listener.
- Explain why the source recreates ECS services when switching listener configuration.
- Manually scale desired tasks and configure target-tracking autoscaling.

---

## 1. Replace server management with ECS Fargate

Earlier AWS chapters used:

```text
EC2
Docker Compose
Nginx
Jenkins
Flask
Streamlit
```

Chapter 10 removes several components.

### Repository changes

The source says:

```text
jenkins/
→ absent

docker-compose.yml
→ absent

nginx reverse proxy
→ absent
```

Why?

### Jenkins

The source keeps Jenkins out because it is stateful and depends on persistent storage.

### Docker Compose

ECS task/service configuration now handles container execution and networking.

### Nginx

The AWS Application Load Balancer handles:

```text
TLS termination
host routing
public entry
```

### Remaining applications

The source deploys:

```text
flask-app
streamlit-app
```

Flask keeps:

```text
port 5000
```

Streamlit keeps:

```text
port 8501
```

Unlike the Cloud Run chapter, the source does not remap both apps to 8080.

[[IMAGE_NEEDED: VM AWS stack versus Fargate stack | A before/after architecture. Before: EC2 + Docker Compose + Nginx + Flask + Streamlit + Jenkins. After: ALB → ECS Fargate Flask/Streamlit tasks, with ECR and CloudWatch around them | Learner should notice that Fargate replaces server/container-host management while ALB replaces Nginx's public routing role]]

---

## 2. Create a deployment identity and configure the AWS CLI

The source creates a dedicated IAM user such as:

```text
serverless-user
```

inside a group such as:

```text
serverless
```

### Source training policies

The source attaches broad managed policies for its learning lab, including access to:

- S3,
- EC2,
- ECR,
- ECS,
- Certificate Manager,
- CloudWatch.

The source itself warns that production should use tighter least-privilege permissions.

### Programmatic access

The IAM user receives an:

```text
Access Key ID
Secret Access Key
```

for CLI use.

### Security rule

These are credentials.

Do not:

```text
commit them
paste them into lesson code
share them in screenshots
```

The uploaded source contains a literal-looking example key pair in one configuration example. This lesson deliberately replaces it with placeholders.

### `aws configure`

The source configures:

```text
region
output format
credentials/profile
```

under:

```text
~/.aws/
```

### Profiles

The source uses a named profile such as:

```text
serverless-user
```

so commands can select that credential set with:

```text
--profile serverless-user
```

### Source inconsistency

One pasted ECR login command uses a different profile name than the user/profile created earlier.

Treat that as a source inconsistency.

The intended principle is:

> Use the profile that actually contains the deployment user's credentials.

{{exercise:M08.L10.EX01}}

---

## 3. Publish both application images to ECR

The source creates two private ECR repositories:

```text
flask-app
streamlit-app
```

### ECR flow

```text
application source
      ↓
Docker build
      ↓
local image
      ↓
tag with ECR URI
      ↓
Docker authenticated to ECR
      ↓
push
      ↓
ECR image
```

### Environment variables

The source defines placeholders such as:

```bash
export REGION=<AWS_REGION>
export AWS_ACCOUNT_ID=<AWS_ACCOUNT_ID>
```

### Authenticate Docker

The durable pattern is:

```text
AWS CLI obtains temporary ECR login password
        ↓
docker login
        ↓
ECR registry
```

### Build and push

Each app is:

1. built locally,
2. tagged using the ECR repository URI,
3. pushed.

### Source formatting issues

The pasted source contains commands such as:

```text
docker build ... -t flask-app.
docker build -t streamlit-app.
sudo./aws/install
```

which visibly omit spaces.

Do not copy malformed pasted syntax blindly.

Use the source repository or correctly structured shell syntax:

```text
command arguments path
```

### Image architecture

The Flask example explicitly includes:

```text
--platform=linux/amd64
```

in its build command.

That reflects the source's chosen runtime architecture.

[[IMAGE_NEEDED: ECR image publishing workflow | A diagram showing Flask and Streamlit source folders → local Docker builds → ECR authentication → separate ECR repositories → image URIs consumed by ECS task definitions | Learner should notice that ECR is the handoff point between local build and Fargate runtime]]

---

## 4. Separate public ALB traffic from private task traffic

The source creates two security groups.

### ALB security group

Example:

```text
alb-sg
```

Initially allows:

```text
HTTP 80
from trusted workstation IP/32
```

Later it switches to:

```text
HTTPS 443
```

### ECS task security group

Example:

```text
ecs-sg-tasks
```

Allows:

```text
8501 from alb-sg
5000 from alb-sg
```

### Why security-group-to-security-group source?

The task containers should not be directly reachable from arbitrary internet clients.

The intended path is:

```text
trusted client
   ↓
ALB security group
   ↓
ALB
   ↓
ecs-sg-tasks permits ALB
   ↓
Fargate task
```

This is a layered network boundary.

[[IMAGE_NEEDED: ALB and ECS security-group boundary | A diagram showing internet/trusted client → alb-sg → ALB → ecs-sg-tasks → Flask:5000 and Streamlit:8501 Fargate tasks, with direct internet-to-task traffic blocked | Learner should notice that task security rules trust the ALB security group rather than public client IPs]]

---

## 5. Create dynamic IP target groups for Fargate tasks

The source creates:

```text
streamlit-tg
flask-tg
```

with:

```text
Target type: IP addresses
```

### Ports

```text
streamlit-tg → HTTP 8501
flask-tg     → HTTP 5000
```

### Why leave targets empty?

Fargate tasks receive dynamically attached network interfaces and IP addresses.

You should not manually hardcode task IPs in the source's design.

Instead:

```text
ECS service
starts task
   ↓
task gets network interface/IP
   ↓
service registers task IP with target group
```

When a task is replaced:

```text
old IP deregistered
new IP registered
```

This is essential to understanding why serverless/container orchestration cannot depend on manually fixed backend addresses.

{{exercise:M08.L10.EX02}}

---

## 6. Create the Application Load Balancer and host rules

The source creates:

```text
ecs-fargate-alb
```

as:

```text
Internet-facing
IPv4
multiple Availability Zones
```

### Why multiple AZs?

The source wants Fargate tasks scheduled across enabled subnets/AZs to be able to register behind the ALB.

### Initial listener

It begins with:

```text
HTTP :80
```

### Block default ALB DNS use

The source changes the listener's default action to:

```text
Return fixed response
403
```

with a message instructing users to use the official custom domain.

This creates:

```text
unmatched host / direct ALB DNS
→ 403
```

### Host routing

The source adds:

```text
Host = streamlit.<domain>
→ streamlit-tg

Host = flask.<domain>
→ flask-tg
```

### Routing model

```text
ALB :80
  |
  +-- Host flask.domain
  |      → flask-tg
  |
  +-- Host streamlit.domain
  |      → streamlit-tg
  |
  +-- anything else
         → 403
```

[[IMAGE_NEEDED: ALB host-based routing | A diagram showing one ALB listener with three rules: flask hostname → flask-tg, streamlit hostname → streamlit-tg, default/unmatched → fixed 403 | Learner should notice that the ALB replaces the earlier Nginx host-routing layer]]

---

## 7. Understand ECS cluster, task definitions, tasks, and services

The source creates an ECS cluster with:

```text
Fargate
```

selected as the compute model.

### Cluster

A cluster is the logical environment where ECS services/tasks run.

### Task definition

The source compares a task definition to:

```text
docker-compose-style declaration
```

for one workload.

It defines:

- image URI,
- CPU,
- memory,
- container port,
- execution role.

### Streamlit task definition

Source settings:

```text
1 vCPU
3 GB memory
port 8501
```

### Flask task definition

Source settings:

```text
2 vCPU
4 GB memory
port 5000
```

### Task

A **task** is a running instance of a task definition.

### Service

A service keeps a desired number of tasks running and integrates them with networking/load balancing.

Mental model:

```text
Task definition
   ↓ template for runtime
Task
   ↓ one running copy
Service
   ↓ maintains N copies + ALB registration
Cluster
   ↓ logical ECS environment
```

{{exercise:M08.L10.EX03}}

---

## 8. Create Fargate services and attach them to the ALB

The source creates one service per application.

### Flask service

Key source choices:

```text
task definition: flask-app
security group: ecs-sg-tasks
load balancer: ecs-fargate-alb
target group: flask-tg
```

### Streamlit service

Uses:

```text
task definition: streamlit-app
security group: ecs-sg-tasks
load balancer: ecs-fargate-alb
target group: streamlit-tg
```

### Automatic registration

When the service launches tasks:

```text
task starts
→ task obtains IP
→ ECS registers target
→ ALB health checks/routing can use it
```

This is why the target groups were left empty during creation.

---

## 9. Monitor container output with CloudWatch

The source explains that container output is forwarded to:

```text
CloudWatch Logs
```

This includes:

- startup messages,
- warnings,
- request logs,
- errors,
- stdout,
- stderr.

### Why this matters in Fargate

There is no EC2 host you should SSH into for routine application debugging.

Instead:

```text
Fargate task
   ↓ stdout/stderr
CloudWatch Logs
   ↓
engineer investigates
```

The source also notes that the ECS service's **Logs** tab exposes the same log stream for convenience.

[[IMAGE_NEEDED: Fargate logging path | A diagram showing Flask/Streamlit Fargate task stdout/stderr → CloudWatch Logs → either CloudWatch log group UI or ECS service Logs tab | Learner should notice that operational debugging no longer depends on SSH access to a host]]

---

## 10. Point custom hostnames to the ALB and add TLS with ACM

The source updates DNS so:

```text
flask
streamlit
```

resolve to the ALB's generated DNS name through the provider-specific record approach described in the chapter.

### DNS role

DNS only gets the request to the ALB.

ALB host rules decide which application receives it.

### Import certificate into ACM

The source reuses the certificate purchased/prepared earlier.

It imports:

```text
certificate body
private key
certificate chain
```

into AWS Certificate Manager.

### Regional requirement

The source emphasizes:

> The ACM certificate must exist in the same AWS region as the ALB.

Otherwise it will not appear as an available listener certificate.

### Add HTTPS listener

The source adds:

```text
HTTPS :443
```

and attaches the ACM certificate.

It recreates the same host rules:

```text
flask.domain
→ flask-tg

streamlit.domain
→ streamlit-tg
```

and keeps default:

```text
403
```

### ALB security group update

The source changes public entry from:

```text
HTTP 80
```

to:

```text
HTTPS 443
```

while preserving the trusted source CIDR.

[[IMAGE_NEEDED: HTTPS ALB termination | A diagram showing browser HTTPS → ALB port 443 with ACM certificate → host rule → Flask or Streamlit target group → Fargate task over internal application port | Learner should notice that TLS terminates at the ALB rather than inside the application container]]

---

## 11. Recreate services when switching to the HTTPS listener

The source states that, in its console workflow, it cannot simply replace the service's load-balancer listener in place.

So it performs:

```text
desired tasks → 0
wait for 0/0
delete service
recreate service
```

The target groups stay the same.

Only the selected listener changes from:

```text
HTTP :80
```

to:

```text
HTTPS :443
```

### Why scale to zero first?

The source uses this to stop active tasks cleanly before deleting/recreating the service.

### Final test

The expected endpoints become:

```text
https://flask.<domain>
https://streamlit.<domain>
```

---

## 12. Scale Fargate with task size and task count

Fargate capacity has two dimensions in the source.

### Vertical allocation per task

Task definition sets:

```text
vCPU
memory
```

Example:

```text
Flask:
2 vCPU + 4 GB

Streamlit:
1 vCPU + 3 GB
```

### Horizontal task count

Service sets:

```text
desired tasks
```

If Flask has:

```text
1 task
→ 2 vCPU + 4 GB total
```

then:

```text
2 tasks
→ 4 vCPU + 8 GB total
```

conceptually, assuming the same task definition.

### Manual scaling

Change:

```text
Desired tasks
```

directly.

### Service autoscaling

The source enables service autoscaling with:

```text
minimum tasks
maximum tasks
target-tracking policy
```

and uses:

```text
ECSServiceAverageCPUUtilization
```

as the metric.

The source gives an example target around:

```text
50%
```

though one screenshot example may display another value.

The durable concept is:

```text
average CPU rises above target
→ add tasks

average CPU falls sufficiently
→ remove tasks
```

within configured min/max bounds.

### Source introductory inconsistency

The chapter introduction broadly describes serverless elasticity as scaling to zero and back up.

Its actual ECS service autoscaling example later configures a minimum task count of:

```text
1
```

Treat the concrete service configuration as the hands-on example.

[[IMAGE_NEEDED: Fargate task autoscaling | A diagram showing one ECS service with task definition size fixed, task count increasing from 1 to multiple replicas as average CPU crosses a target, then shrinking within min/max bounds | Learner should notice the difference between per-task resources and number of tasks]]

{{exercise:M08.L10.EX04}}

---

## 13. Put the complete AWS serverless architecture together

The complete source architecture is:

```text
Developer workstation
       ↓
Docker build
       ↓
ECR repositories
       ↓
ECS task definitions
       ↓
Fargate services/tasks
       ↓
target groups
       ↓
ALB host routing
       ↓
HTTPS listener + ACM certificate
       ↓
custom subdomains
```

Supporting controls:

```text
IAM profile
→ deployment permissions

alb-sg
→ public HTTPS entry

ecs-sg-tasks
→ only ALB may reach app ports

CloudWatch
→ application logs

ECS autoscaling
→ task count adjusts with load
```

This achieves the source's goal of running Flask and Streamlit without maintaining EC2 application hosts.

---

## Important misconceptions

### Misconception 1
> "Fargate means there are no containers."

Fargate runs containers; it removes the need to manage the container-host servers.

### Misconception 2
> "The task IPs should be manually registered in the target groups."

The source leaves target lists empty because ECS services dynamically register Fargate task IPs.

### Misconception 3
> "The ECS task security group should allow the whole internet."

The source allows application ports from the ALB security group.

### Misconception 4
> "An ECS task definition is the same thing as a running task."

The task definition is the specification; a task is a running copy.

### Misconception 5
> "ALB host routing requires Nginx."

The ALB itself performs the host-based routing in this architecture.

### Misconception 6
> "The source credentials shown in the pasted chapter are safe to reuse."

Never reuse or expose literal credentials from examples. Use your own securely created credentials and placeholders in documentation.

### Misconception 7
> "The ECR login profile name in every source command is consistent."

One pasted command uses a different profile name. Use the profile you actually configured.

---

## Key terminology

| Term | Meaning |
|---|---|
| ECS | Amazon Elastic Container Service |
| Fargate | Serverless compute model for ECS tasks |
| ECR | AWS managed container registry |
| Task definition | Runtime specification for an ECS workload |
| Task | Running instance of a task definition |
| ECS service | Controller maintaining desired tasks and load-balancer integration |
| ALB | Application Load Balancer |
| Target group | Backend set receiving ALB traffic |
| ACM | AWS Certificate Manager |
| CloudWatch Logs | Central logging system used by the source |
| Target tracking | Autoscaling policy that tries to maintain a metric around a target |
| Desired tasks | Number of service task replicas ECS attempts to keep running |

---

## Self-check

1. Why are Jenkins, Docker Compose, and Nginx absent from the Chapter 10 serverless repository?
2. What are the Flask and Streamlit internal ports?
3. Why use a dedicated IAM user/profile?
4. Why must access keys never be committed?
5. What are the stages from local image to ECR?
6. Why do Fargate target groups use IP target type?
7. Why are target groups created without static target IPs?
8. What does `alb-sg` protect?
9. What does `ecs-sg-tasks` protect?
10. How does the ALB distinguish Flask from Streamlit?
11. Why does the default listener rule return 403?
12. What is the difference between an ECS cluster, task definition, task, and service?
13. Which CPU/memory sizes does the source assign to Flask and Streamlit?
14. How does ECS automatically register tasks with target groups?
15. Where do Fargate application logs go?
16. Why must the ACM certificate be in the ALB's region?
17. What changes when the HTTPS listener is added?
18. Why does the source recreate services?
19. What is the difference between task size and task count?
20. How does target-tracking autoscaling work?

---

## Retain this idea

**ECS Fargate keeps the container model but removes server ownership: publish images to ECR, describe workloads with task definitions, let ECS services maintain dynamic tasks, place an ALB and security boundaries in front, and scale by changing task count instead of provisioning EC2 application hosts.**
""",
        "estimated_minutes": 270,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "fargate-shift", "title": "Replace server management with ECS Fargate", "order": 1},
            {"id": "iam-cli", "title": "Create a deployment identity and configure the AWS CLI", "order": 2},
            {"id": "ecr", "title": "Publish both application images to ECR", "order": 3},
            {"id": "network-foundation", "title": "Separate public ALB traffic from private task traffic", "order": 4},
            {"id": "target-groups", "title": "Create dynamic IP target groups for Fargate tasks", "order": 5},
            {"id": "alb-routing", "title": "Create the Application Load Balancer and host rules", "order": 6},
            {"id": "ecs-model", "title": "Understand ECS cluster, task definitions, tasks, and services", "order": 7},
            {"id": "ecs-services", "title": "Create Fargate services and attach them to the ALB", "order": 8},
            {"id": "cloudwatch", "title": "Monitor container output with CloudWatch", "order": 9},
            {"id": "dns-acm", "title": "Point custom hostnames to the ALB and add TLS with ACM", "order": 10},
            {"id": "service-recreation", "title": "Recreate services when switching to the HTTPS listener", "order": 11},
            {"id": "fargate-scaling", "title": "Scale Fargate with task size and task count", "order": 12},
            {"id": "fargate-full", "title": "Put the complete AWS serverless architecture together", "order": 13},
        ],
    },

    "exercises": [
        {
            "id": "M08.L10.EX01",
            "title": "Design a Safe AWS CLI Credential Workflow",
            "lesson_code": "M08.L10",
            "section_id": "iam-cli",
            "placement": "after_section",
            "description": "Separate IAM identity, local profiles, commands, and source control.",
            "instructions": (
                ('1. Draw IAM user → access keys → local AWS profile → `--profile` command usage.\n'
                 '2. Mark which data must never enter Git.\n'
                 '3. Then explain how a profile-name mismatch can cause a deployment command to authenticate as the wrong identity or fail.')
            ),
            "expected_output": "A secure credential-flow diagram and profile troubleshooting explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["iam", "aws-cli", "credentials"],
        },
        {
            "id": "M08.L10.EX02",
            "title": "Trace Dynamic Fargate Registration",
            "lesson_code": "M08.L10",
            "section_id": "target-groups",
            "placement": "after_section",
            "description": "Explain why Fargate backends cannot depend on static task IPs.",
            "instructions": (
                ('1. Trace service launch → task ENI/IP allocation → automatic target-group registration → task replacement → old target deregistration → new target registration.\n'
                 '2. Explain why the target group starts empty.')
            ),
            "expected_output": "A dynamic target-registration lifecycle.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["fargate", "target-groups", "ecs-services"],
        },
        {
            "id": "M08.L10.EX03",
            "title": "Map ECS Runtime Objects",
            "lesson_code": "M08.L10",
            "section_id": "ecs-model",
            "placement": "after_section",
            "description": "Distinguish ECS cluster, task definition, task, and service.",
            "instructions": (
                ('1. Put the cluster at the top of the hierarchy.\n'
                 '2. Place the flask-app task definition with its settings: 2 vCPU / 4 GB and port 5000.\n'
                 '3. Show the one or more running tasks created from it, and the Flask service that keeps them running.\n'
                 '4. Connect the service to the flask-tg target group and the ALB.')
            ),
            "expected_output": "An ECS runtime object hierarchy.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["ecs", "task-definition", "service"],
        },
        {
            "id": "M08.L10.EX04",
            "title": "Compare Vertical and Horizontal Fargate Capacity",
            "lesson_code": "M08.L10",
            "section_id": "fargate-scaling",
            "placement": "after_section",
            "description": "Understand the difference between task size and replica count.",
            "instructions": (
                ("1. Using the source's Flask task size of 2 vCPU/4 GB, calculate conceptual total reserved capacity for 1, 2, and 4 tasks.\n"
                 '2. Then explain how target-tracking CPU autoscaling changes task count without changing the task definition.')
            ),
            "expected_output": "A capacity table plus autoscaling explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["fargate", "autoscaling", "capacity"],
        },
    ],

    "quiz": {
        "id": "M08.L10.QZ01",
        "title": "Serverless Deployment with AWS ECS Fargate — Knowledge Check",
        "lesson_code": "M08.L10",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L10.Q01", "section_id": "fargate-shift", "question": "Which component replaces the source's Nginx public-routing role?", "options": ["ECR", "Application Load Balancer", "CloudWatch", "IAM"], "correct": 1, "explanation": "The ALB terminates/routs public traffic in the Fargate architecture."},
            {"id": "M08.L10.Q02", "section_id": "iam-cli", "question": "Why use a named AWS CLI profile?", "options": ["To store application logs", "To select a credential/config set without hard-coding keys in commands", "To build Docker images", "To create DNS records"], "correct": 1, "explanation": "The profile references credentials stored in the local AWS configuration."},
            {"id": "M08.L10.Q03", "section_id": "ecr", "question": "What is ECR used for?", "options": ["Container image registry", "DNS", "TLS listener", "Jenkins storage"], "correct": 0, "explanation": "Fargate task definitions pull the application images from ECR."},
            {"id": "M08.L10.Q04", "section_id": "network-foundation", "question": "What is the source for the task security-group app-port rules?", "options": ["0.0.0.0/0", "The ALB security group", "GitHub", "The certificate"], "correct": 1, "explanation": "The source allows only the ALB security group to reach task ports."},
            {"id": "M08.L10.Q05", "section_id": "target-groups", "question": "Why are static IP targets not manually registered?", "options": ["Fargate task IPs are dynamic and ECS registers them", "ALB does not support IPs", "Flask has no IP", "ECR handles target registration"], "correct": 0, "explanation": "Fargate ENIs/IPs change as tasks start and stop."},
            {"id": "M08.L10.Q06", "section_id": "alb-routing", "question": "What happens to an unmatched/default ALB request in the source?", "options": ["It always goes to Flask", "It receives a fixed 403 response", "It goes to Jenkins", "It creates a task"], "correct": 1, "explanation": "The source deliberately blocks direct/unmatched access."},
            {"id": "M08.L10.Q07", "section_id": "ecs-model", "question": "What is a task definition?", "options": ["A running container instance", "The runtime specification for an ECS workload", "A DNS record", "A CloudWatch stream"], "correct": 1, "explanation": "It declares image, resources, ports, and related runtime settings."},
            {"id": "M08.L10.Q08", "section_id": "ecs-model", "question": "Which source resources are assigned to Flask?", "options": ["1 vCPU/3 GB", "2 vCPU/4 GB", "4 vCPU/16 GB", "8 vCPU/32 GB"], "correct": 1, "explanation": "The source gives Flask more headroom than Streamlit."},
            {"id": "M08.L10.Q09", "section_id": "cloudwatch", "question": "Where does the source inspect Fargate stdout/stderr?", "options": ["CloudWatch Logs", "Namecheap", "ECR only", "ACM"], "correct": 0, "explanation": "CloudWatch receives task application output."},
            {"id": "M08.L10.Q10", "section_id": "dns-acm", "question": "Why must the imported ACM certificate be in the same region as the ALB?", "options": ["Otherwise it will not be available to that listener in the source workflow", "Because Docker requires it", "Because DNS cannot resolve", "Because ECR requires it"], "correct": 0, "explanation": "The source explicitly gives this regional requirement."},
            {"id": "M08.L10.Q11", "section_id": "service-recreation", "question": "What remains unchanged when the source recreates services for HTTPS?", "options": ["Target groups", "Task ports become 443", "Images move out of ECR", "Security group becomes public"], "correct": 0, "explanation": "The services continue using the same application target groups."},
            {"id": "M08.L10.Q12", "section_id": "fargate-scaling", "question": "What metric does the source use for target-tracking autoscaling?", "options": ["DNS latency", "ECSServiceAverageCPUUtilization", "ECR image size", "Certificate age"], "correct": 1, "explanation": "The example policy uses average ECS service CPU utilization."},
            {"id": "M08.L10.Q13", "section_id": "fargate-full", "type": "open", "question": "Describe the complete Chapter 10 architecture from local Docker build to HTTPS request handling, including ECR, task definitions, Fargate services, security groups, target groups, ALB host routing, ACM, CloudWatch, and autoscaling."},
        ],
        "passing_score": 70,
    },
}
