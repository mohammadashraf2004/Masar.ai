"""M01.L01 — DevOps & Cloud Foundations: From Culture to Your First Workstation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapters 1–2, page numbers not provided in the supplied chapter exports.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "DevOps & Cloud Foundations"

MODULE_DESCRIPTION = (
    "Build the mental model behind DevOps and cloud computing, then turn that "
    "understanding into a usable beginner DevOps workstation with the command "
    "line, Git, VS Code, Docker, and access to a major cloud provider."
)

SOURCE_CHAPTER = "1–2"

SOURCE_PAGES = "Page numbers not provided in supplied chapter exports"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "DevOps & Cloud Foundations: From Culture to Your First Workstation",

    "slug": "devops-cloud-foundations-m01-l01",

    "description": (
        "Understand why DevOps emerged, how its lifecycle and CI/CD practices "
        "work, how cloud service models fit into modern delivery, and how to "
        "prepare a practical workstation for future DevOps labs."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "devops",
        "cloud-computing",
        "devops-lifecycle",
        "ci-cd",
        "bash",
        "git",
        "vs-code",
        "docker",
        "aws",
        "azure",
        "gcp",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "DevOps & Cloud Foundations: From Culture to Your First Workstation",

        "content": r"""
# DevOps & Cloud Foundations: From Culture to Your First Workstation

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M01.L01  
> **Module:** DevOps & Cloud Foundations  
> **Source alignment:** BOOK-XXX, Chapters 1–2. Page numbers were not provided in the supplied chapter exports. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain DevOps as a culture and operating model rather than merely a collection of tools.
- Describe the historical path from Waterfall to Agile and then to DevOps.
- Explain the eight stages of the DevOps lifecycle and the feedback loop that connects them.
- Distinguish automation, Continuous Integration, Continuous Delivery, and Continuous Deployment.
- Explain IaaS, PaaS, and SaaS using the idea of shared responsibility.
- Describe the role of AWS, Microsoft Azure, and Google Cloud in a DevOps environment.
- Explain the difference between a terminal, shell, CLI, and GUI.
- Navigate a filesystem and perform basic file operations from a command line.
- Install and perform first-time configuration of Git.
- Explain why VS Code, Docker Desktop, and cloud access are useful parts of a beginner DevOps workstation.
- Verify a basic Docker installation and recognize important safety precautions for shell commands and cloud billing.
- Connect all of these ideas into one end-to-end mental model of modern software delivery.

---

## 1. DevOps starts with culture, not tools

When beginners first hear **DevOps**, they often imagine a list of technologies: Docker, Kubernetes, Jenkins, Terraform, AWS, GitHub Actions, and so on. Those tools are useful, but they are not the definition of DevOps.

A better starting point is this:

> **DevOps is a way of organizing people, processes, and technology so that software can move from idea to production quickly, safely, and repeatedly.**

The name combines **Development (Dev)** and **Operations (Ops)** because these groups historically had different goals.

Development teams were usually rewarded for **change**:

- ship new features,
- fix product problems,
- respond to business requests,
- release improvements quickly.

Operations teams were usually rewarded for **stability**:

- keep systems available,
- prevent outages,
- control production risk,
- maintain predictable infrastructure.

Neither goal is wrong. The problem appears when each team optimizes only its own objective.

Imagine this workflow:

```text
Developer writes feature
        |
        v
Developer tests locally
        |
        v
"Works on my machine"
        |
        v
Code is handed to Operations
        |
        v
Operations discovers missing configuration,
dependencies, permissions, or performance problems
        |
        v
Production incident
        |
        v
Dev blames Ops / Ops blames Dev
```

This organizational barrier is often described as the **wall of confusion**.

The wall creates slow releases because every deployment becomes risky. It also encourages large handoffs, late discovery of problems, emergency fixes, and poor feedback between the people building the software and the people running it.

DevOps tries to replace this handoff model with a shared system.

### The three cultural pillars

#### 1. Shared ownership and systems thinking

In a DevOps culture, responsibility does not stop at a team boundary.

Developers should think about questions such as:

- How will this service be deployed?
- How will we know whether it is healthy?
- What configuration does it require?
- What happens if one dependency fails?
- Can it scale?
- Can it be rolled back safely?

Operations engineers are not merely gatekeepers who manually deploy everything. They help create platforms, automation, environments, policies, and self-service capabilities that make safe delivery easier.

This is **systems thinking**: optimize the whole value stream rather than optimizing one isolated department.

A local improvement is not useful if it damages the overall system. For example, developers producing ten releases per day is not an improvement if Operations can deploy only one release per month.

#### 2. Fast and amplified feedback

The earlier you learn about a problem, the cheaper it usually is to fix.

DevOps therefore encourages short feedback loops:

- CI reports integration failures quickly.
- Automated tests expose regressions before release.
- Monitoring reveals production problems.
- Observability helps engineers understand why a system behaves a certain way.
- Customer feedback informs the next iteration.

Think of feedback as a sensor in a control system. If the sensor reports a problem immediately, the system can correct course quickly. If feedback arrives weeks later, the team may have built many additional changes on top of the original mistake.

#### 3. Continuous improvement and experimentation

A healthy DevOps environment assumes that processes and systems can always improve.

That requires a culture where incidents are examined for **systemic causes**, not merely used to find a person to blame.

A useful post-incident question is:

> "What conditions allowed this failure to reach users, and what can we change so the same class of failure is less likely?"

That question encourages better tests, safer deployment methods, clearer monitoring, improved documentation, stronger automation, or better design.

DevOps therefore combines delivery speed with learning.

[[IMAGE_NEEDED: Breaking the wall of confusion | A before-and-after diagram. On the left, Development and Operations are separated by a wall and exchange a large risky release. On the right, Dev, Ops, QA, Security, and Product collaborate around one continuous delivery flow with shared feedback arrows | Learner should notice that DevOps changes the organizational flow and ownership model, not merely the toolset]]

### A practical mental model

Do not memorize "DevOps = Dev + Ops."

Remember instead:

```text
Shared ownership
      +
Automation
      +
Fast feedback
      +
Continuous improvement
      =
Reliable flow of value to users
```

---

## 2. From Waterfall to Agile to DevOps

Understanding the history helps explain why DevOps exists.

### Waterfall: optimize for prediction

The traditional **Waterfall** model treats software development as a sequence of major phases:

```text
Requirements
    ↓
Design
    ↓
Implementation
    ↓
Testing
    ↓
Deployment
    ↓
Maintenance
```

Each phase is largely completed before the next begins.

This can appear logical because it creates a clear plan. The difficulty is that software requirements are often uncertain and can change while the project is being built.

Three major problems appear repeatedly:

1. **Late feedback**  
   Users may not see working software until near the end.

2. **Risk accumulates**  
   A mistaken requirement or architectural assumption may remain hidden for months.

3. **Change becomes expensive**  
   The process is optimized around the assumption that the original plan is correct.

### Agile: shorten the development feedback loop

Agile methods emerged to make development more iterative and adaptive.

The Agile Manifesto emphasizes:

- people and interaction,
- working software,
- customer collaboration,
- responding to change.

Instead of building one huge release before showing it to users, teams work in smaller increments.

Two familiar Agile approaches are **Scrum** and **Kanban**.

### Scrum in one mental model

Scrum organizes work into short iterations called **Sprints**.

A simplified flow is:

```text
Product Backlog
      ↓
Sprint Planning
      ↓
Sprint Backlog
      ↓
Build during Sprint
      ↓
Sprint Review
      ↓
Retrospective
      ↺
```

Important roles include:

- **Product Owner** — prioritizes product value and desired work.
- **Development Team** — builds the increment.
- **Scrum Master** — helps the team use Scrum effectively and remove impediments.

Important events include Sprint Planning, Daily Scrum, Sprint Review, and Sprint Retrospective.

### Kanban in one mental model

Kanban focuses on **flow** rather than fixed-length Sprints.

A simple board might be:

```text
To Do | In Progress | In Test | Done
```

The important idea is not the board itself. The important idea is to **limit Work in Progress (WIP)**.

Why?

Suppose a team starts 20 tasks but finishes only two. Starting more work does not increase delivery. It creates queues, context switching, and hidden bottlenecks.

WIP limits encourage teams to finish existing work before starting more.

### The Agile "last mile" problem

Agile improved how software was **developed**, but many organizations still had slow and manual deployment processes.

This created a mismatch:

```text
Fast, iterative development
          |
          v
    ready-to-release code
          |
          X  bottleneck
          |
          v
Slow, manual operations process
```

The source chapter describes this as the **last mile problem**.

DevOps extends Agile thinking beyond coding and testing into:

- release,
- deployment,
- infrastructure,
- production operation,
- monitoring,
- feedback.

So a useful relationship is:

> **Agile improves the development loop; DevOps extends the loop through delivery and operation.**

DevOps is therefore not simply a replacement for Agile. It builds on many of the same ideas: small batches, collaboration, feedback, and continuous improvement.

---

## 3. The DevOps lifecycle: from idea to feedback

The DevOps lifecycle is often drawn as an **infinity loop** because there is no permanent "finished" state.

Software is planned, built, delivered, observed, and improved continuously.

The source organizes the lifecycle into eight stages:

1. Plan
2. Code
3. Build
4. Test
5. Release
6. Deploy
7. Operate
8. Monitor

[[IMAGE_NEEDED: DevOps infinity loop | An infinity-loop diagram containing the eight stages Plan, Code, Build, Test, Release, Deploy, Operate, and Monitor, with arrows showing continuous movement and monitoring feedback returning toward planning | Learner should notice that the lifecycle is cyclic and overlapping rather than a one-way project sequence]]

Let's understand what each stage contributes.

### 3.1 Plan — decide what value to build

Planning answers:

- What problem are we solving?
- Why is it valuable?
- How will success be measured?
- What work should happen next?

Work is often represented as user stories, issues, or features in a backlog.

Typical tools include Jira, Azure Boards, Trello, and similar work-management systems.

The DevOps difference is that planning is not a giant one-time requirements phase. Plans are updated as feedback arrives.

### 3.2 Code — implement the change

Developers translate planned work into software.

Good DevOps-oriented coding includes:

- maintainable code,
- unit tests,
- peer review,
- configuration stored as code where appropriate,
- version control.

**Git** is central because the delivery process needs a trustworthy history of changes.

### 3.3 Build — convert source into a deployable artifact

A build process may:

- compile code,
- resolve dependencies,
- run fast tests,
- package the application,
- produce a versioned artifact.

Examples of artifacts include:

- a `.jar`,
- a ZIP package,
- a binary,
- a Docker image.

A CI system can trigger this process automatically after a commit.

### 3.4 Test — gain confidence

Testing goes beyond checking whether code compiles.

A delivery pipeline may include:

- unit tests,
- integration tests,
- end-to-end tests,
- performance tests,
- security tests,
- selected manual exploratory tests.

The goal is not "prove the software has zero bugs." The goal is to reduce uncertainty before the change reaches users.

### 3.5 Release — prepare a production-ready version

A successful build that passes required checks can become a **release candidate**.

Release work may include:

- assigning a version,
- generating release notes,
- collecting approvals,
- promoting the artifact,
- confirming readiness.

### 3.6 Deploy — move the version into production

Deployment is the technical act of putting the new version into a target environment.

A strong deployment process should be:

- repeatable,
- automated,
- observable,
- reversible where possible.

Useful techniques include automated health checks, rollbacks, canary releases, and blue-green deployments.

Infrastructure can also be managed with **Infrastructure as Code (IaC)** using tools such as Terraform, OpenTofu, or Pulumi.

### 3.7 Operate — keep the system healthy

Production software needs ongoing care.

Operations includes:

- availability,
- infrastructure management,
- access control,
- scaling,
- resilience,
- disaster recovery,
- cost management,
- performance optimization.

In DevOps, this responsibility is shared rather than thrown to a separate team after deployment.

### 3.8 Monitor — learn from reality

Production generates information that cannot be fully predicted in development.

Three important observability signals are:

| Signal | What it tells you | Example |
|---|---|---|
| Logs | Discrete events and messages | "Payment request failed" |
| Metrics | Numerical measurements over time | CPU 85%, error rate 3%, p95 latency 420 ms |
| Traces | The path of one request across components | API → auth service → payment service → database |

Monitoring tools turn these signals into dashboards and alerts.

Representative tools include Prometheus, Grafana, the ELK stack, Datadog, New Relic, and Splunk.

The crucial point is that monitoring is not the end:

```text
Monitor
   ↓
Learn what happened
   ↓
Create new work
   ↓
Plan
   ↓
Next improvement
```

### Lifecycle summary

| Stage | Main question |
|---|---|
| Plan | What should we build and why? |
| Code | How do we implement the change safely? |
| Build | Can we package a consistent deployable artifact? |
| Test | What evidence do we have that the change works? |
| Release | Is this version ready for production? |
| Deploy | How do we move it into production safely? |
| Operate | How do we keep it reliable, secure, and efficient? |
| Monitor | What is production telling us? |

{{exercise:M01.L01.EX01}}

---

## 4. Automation, CI, Continuous Delivery, and Continuous Deployment

The lifecycle describes **what happens**.

Automation and CI/CD describe **how teams make that flow fast and reliable**.

### 4.1 Automation: remove repeatable manual toil

Manual repetitive work causes three problems:

- it is slow,
- it varies from person to person,
- it is easy to perform incorrectly.

Automation means turning repeatable steps into scripts, pipelines, or managed processes.

Examples:

```text
Manual                           Automated
------                           ---------
Developer runs tests manually   CI runs tests on every push
Engineer copies files by hand   Deployment pipeline publishes artifact
Admin configures server GUI     IaC declares desired infrastructure
Person checks logs occasionally Alert triggers on defined condition
```

Automation does not mean "remove humans from every decision."

A better rule is:

> **Automate repeatable mechanics; keep human judgment where judgment is valuable.**

Infrastructure as Code is a strong example. Instead of manually creating servers and networks differently every time, the desired infrastructure is represented as code that can be reviewed, versioned, and reproduced.

### 4.2 Continuous Integration (CI)

CI solves a collaboration problem.

Without frequent integration, developers may work on separate branches for long periods. When the branches finally merge, many conflicts and hidden incompatibilities appear together.

CI encourages small, frequent integrations.

A simplified CI flow:

```text
Developer changes code
        ↓
Commit and push
        ↓
CI server detects change
        ↓
Checkout latest code
        ↓
Build
        ↓
Automated tests
        ↓
Pass? ── yes ──> produce artifact
  |
  no
  ↓
Fast feedback to team
```

The key benefit is **early detection**.

A small integration problem discovered five minutes after a commit is usually easier to fix than the same problem discovered three weeks later.

Representative CI/CD tools mentioned in the source include Jenkins, GitLab CI, GitHub Actions, Azure Pipelines, CircleCI, and AWS CodePipeline.

### 4.3 Continuous Delivery

**Continuous Delivery** means that changes which pass the required automated checks are automatically advanced to a **production-ready state**.

The final production deployment can still require a human decision.

```text
Commit
  ↓
Build
  ↓
Automated tests
  ↓
Security/performance checks
  ↓
Staging
  ↓
Production-ready
  ↓
Manual business approval
  ↓
Production
```

The benefit is that releasing becomes a decision, not a large engineering project.

### 4.4 Continuous Deployment

**Continuous Deployment** goes one step further.

Every change that successfully passes the complete pipeline can be deployed automatically to production.

```text
Commit
  ↓
Pipeline passes
  ↓
Automatic production deployment
```

This requires strong confidence in:

- automated testing,
- production monitoring,
- rollback mechanisms,
- deployment safety,
- change size.

### The distinction you must remember

| Practice | What is automated? | Human production approval? |
|---|---|---|
| CI | Integration, build, early tests | Not the focus |
| Continuous Delivery | Pipeline up to production-ready state | Usually yes |
| Continuous Deployment | Entire path through production | No final manual approval |

[[IMAGE_NEEDED: CI versus Continuous Delivery versus Continuous Deployment | Three horizontal pipelines. CI stops after a tested build artifact; Continuous Delivery continues through staging but shows a manual approval gate before production; Continuous Deployment continues automatically into production | Learner should notice that the main distinction between Delivery and Deployment is the final production approval gate]]

### A subtle but important idea: deployment is not always release

A team can technically deploy code without exposing it to every user immediately.

Feature flags, canary releases, or staged rollouts can separate:

- **deployment** — software is present in production,
- **release** — users can actually access the behavior.

This separation reduces risk and increases control.

---

## 5. Cloud computing and the shared-responsibility ladder

DevOps and cloud computing reinforce each other.

DevOps benefits from infrastructure that can be created quickly and programmatically. Cloud platforms provide on-demand compute, storage, networks, databases, and managed services.

A practical definition is:

> **Cloud computing is on-demand access to IT resources over a network, usually with usage-based pricing and provider-managed infrastructure.**

Key benefits described in the source include:

- **Agility** — provision resources in minutes instead of waiting for physical hardware.
- **Elasticity** — scale resources up or down as demand changes.
- **Cost model** — replace some large up-front hardware purchases with variable usage costs.
- **Global reach** — deploy into multiple geographic regions.

### 5.1 IaaS — Infrastructure as a Service

With **IaaS**, the provider manages the physical data center and virtualization layer, while you manage more of the software stack.

You typically control:

- virtual machines,
- operating system configuration,
- application runtime,
- application,
- much of the network/security configuration.

IaaS gives flexibility but also more responsibility.

Examples from the source include cloud virtual-machine and infrastructure services such as AWS EC2, Azure Virtual Machines, and Google Compute Engine.

### 5.2 PaaS — Platform as a Service

With **PaaS**, the provider manages more of the platform.

You focus primarily on:

- application code,
- application configuration,
- data,
- deployment behavior.

The platform handles more of the underlying operating system, runtime, patching, or scaling mechanics.

Examples include AWS Elastic Beanstalk, Azure App Service, Google App Engine, and Heroku.

PaaS is useful when you want developers to spend more time on application behavior and less time operating servers.

### 5.3 SaaS — Software as a Service

With **SaaS**, the provider delivers a complete application.

You consume the application rather than build the platform beneath it.

Examples include Microsoft 365, Google Workspace, Salesforce, Dropbox, and Slack.

### The management trade-off

A useful way to remember the three models:

```text
More control / more responsibility
           ↑
          IaaS
           |
          PaaS
           |
          SaaS
           ↓
Less infrastructure management
```

[[IMAGE_NEEDED: Cloud service model responsibility stack | A layered stack comparing on-premises, IaaS, PaaS, and SaaS across networking, storage, servers, virtualization, operating system, runtime, application, and data, clearly showing which layers are managed by the customer versus the provider | Learner should notice that moving from IaaS to PaaS to SaaS trades direct control for less operational responsibility]]

### 5.4 The major cloud providers

The source introduces three major providers:

#### Amazon Web Services (AWS)

AWS provides a broad range of infrastructure and managed services.

Relevant DevOps examples include:

- compute and storage services,
- CodePipeline,
- CodeBuild,
- CodeDeploy.

#### Microsoft Azure

Azure is deeply integrated with the Microsoft ecosystem and provides both infrastructure and platform services.

Relevant DevOps capabilities include Azure DevOps and Azure Pipelines, along with application-hosting and infrastructure services.

#### Google Cloud

Google Cloud is strongly associated with data, AI, networking, and container technologies.

Google originally created Kubernetes, and Google Kubernetes Engine (GKE) is its managed Kubernetes service.

### Do not learn cloud by memorizing hundreds of service names

Instead, learn categories:

```text
Need compute?      → virtual machines / containers / serverless
Need storage?      → object / block / file storage
Need a database?   → relational / NoSQL / managed database
Need networking?   → VPC / load balancing / DNS
Need delivery?     → build / artifact / deployment services
Need monitoring?   → logs / metrics / alerts / tracing
```

Provider names differ. Architectural needs are more stable.

{{exercise:M01.L01.EX02}}

---

## 6. Your first DevOps tool: the command line

Now we move from concepts to practice.

A DevOps engineer spends a large amount of time working through command-line interfaces because command-line tools are:

- scriptable,
- composable,
- efficient over remote connections,
- easy to automate,
- commonly available on servers.

### Terminal, shell, and CLI are not the same thing

These terms are related but distinct.

**Terminal**  
The application window that lets you type commands and see output.

**Shell**  
The program that interprets the command text.

Examples:

- Bash
- Zsh
- PowerShell

**CLI**  
A command-line interface exposed by a tool.

Examples:

```text
git status
docker ps
terraform plan
aws s3 ls
```

Here, Git, Docker, Terraform, and the AWS CLI are tools with command-line interfaces.

### Windows, macOS, and Linux

The source recommends:

- macOS: use the Terminal application.
- Linux: use the distribution's terminal.
- Windows: Windows Terminal with PowerShell is a strong native option; Git for Windows also provides Git Bash.

Later tools may run through WSL 2 on Windows, but you do not need to confuse "the backend technology" with "the shell you must type into."

### 6.1 Navigation commands

Three essential commands are:

```bash
pwd
ls
cd
```

`pwd` prints your current directory.

```bash
pwd
```

Think: **Where am I?**

`ls` lists directory contents.

```bash
ls
ls -l
ls -a
```

Think: **What is here?**

`cd` changes directory.

```bash
cd /path/to/directory
cd ..
cd ~
```

Think: **Where do I want to go?**

### 6.2 Create files and directories

```bash
mkdir my-project
touch new-file.txt
```

`mkdir` creates a directory.

`touch` creates an empty file if it does not already exist.

### 6.3 Copy, move, and rename

Copy a file:

```bash
cp source.txt destination.txt
```

Copy a directory recursively:

```bash
cp -r my-project my-project-backup
```

Move a file:

```bash
mv my-file.txt /path/to/other/dir/
```

Rename a file:

```bash
mv old-name.txt new-name.txt
```

### 6.4 Read simple text

```bash
cat README.md
```

`cat` prints file content.

### 6.5 Redirection

The source uses `echo` and `>`:

```bash
echo "# My First Website Project" > README.md
```

The command on the left produces output. The `>` operator redirects that output into the file.

Important:

> `>` normally overwrites the target file.

Later you will also meet `>>`, which appends instead of replacing.

### 6.6 Deletion: understand before you type

Basic examples:

```bash
rm file.txt
rmdir empty-directory
rm -r directory-with-files
```

The dangerous form is:

```bash
rm -rf some-directory
```

`-r` means recursive.  
`-f` means force.

This combination can remove a directory tree without interactive confirmation.

**Safe beginner habit:**

Before a destructive command:

```bash
pwd
ls
```

Then re-read the target path.

Do not copy destructive shell commands from the internet and run them without understanding the path and flags.

### Follow-along lab: create a project structure

Run:

```bash
cd ~
mkdir devops-book-projects
cd devops-book-projects
mkdir my-first-website
cd my-first-website
mkdir src docs
touch src/index.html
touch src/app.js
touch README.md
echo "# My First Website Project" > README.md
cat README.md
ls -lR
```

Expected structure conceptually:

```text
my-first-website/
├── README.md
├── docs/
└── src/
    ├── app.js
    └── index.html
```

What matters is not memorizing every flag immediately. What matters is learning the loop:

```text
inspect location → perform action → inspect result
```

That habit will protect you when commands become more powerful.

{{exercise:M01.L01.EX03}}

---

## 7. Git and VS Code: make your workstation reproducible and usable

### 7.1 Why Git belongs in DevOps

Git is a **distributed Version Control System (VCS)**.

It lets you:

- track changes,
- review history,
- collaborate,
- create branches,
- recover earlier versions,
- connect source changes to automated pipelines.

DevOps depends on repeatability, and repeatability depends on knowing **which version** of code or configuration produced a result.

That is why source code, scripts, and many configuration files belong in version control.

### Install Git

The source describes common installation routes:

- Windows: Git for Windows, which also includes Git Bash.
- macOS: Homebrew or Apple's command-line tools.
- Ubuntu/Debian: the `apt` package manager.

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install git
```

On macOS with Homebrew:

```bash
brew install git
```

### First-time Git identity

Git records an author identity with commits.

Configure it once:

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

Verify:

```bash
git config --list
```

The important concept is that your commits become attributable to an identity.

This lesson does not yet require the full Git workflow; later you can learn `git init`, `git add`, `git commit`, `git push`, branching, merging, and pull requests in depth.

### 7.2 VS Code as the workstation hub

A code editor is more than a place to type text.

VS Code provides:

- file exploration,
- syntax highlighting,
- search,
- source-control integration,
- extensions,
- debugging,
- an integrated terminal.

This makes it useful in DevOps because you frequently move between:

```text
code
configuration
terminal commands
Git
Docker
YAML
Terraform
logs
```

without leaving the same working environment.

[[IMAGE_NEEDED: VS Code DevOps workspace anatomy | A screenshot-style diagram of VS Code with the Explorer, Search, Source Control, Run/Debug, Extensions icons, editor pane, and integrated terminal labeled | Learner should notice that source files, Git workflow, extensions, and terminal commands can be managed from one workspace]]

### Useful extension categories

The source recommends extensions for:

- Docker,
- remote development,
- Terraform,
- Git history,
- YAML.

Treat extensions as productivity tools, not as required theory.

The principle is more important:

> Configure your editor to understand the file formats and remote environments you actually work with.

---

## 8. Docker Desktop and cloud access

### 8.1 Why containers matter

Docker is a platform for working with **containers**.

A container packages an application together with the dependencies and configuration it needs to run in a consistent environment.

This addresses a classic problem:

> "It works on my machine."

If the development machine and production machine differ in installed libraries, versions, or configuration, software can behave differently.

Containers reduce this environment drift by packaging a controlled runtime unit.

A simplified comparison:

```text
Without container:
Application + "please install these 14 things correctly"

With container:
Application + defined runtime/dependencies packaged as an image
```

You will learn container creation in depth later. For now, the goal is to install and verify the tooling.

### 8.2 What Docker Desktop gives you

The source describes Docker Desktop as providing:

- Docker Engine,
- Docker CLI,
- Docker Compose,
- a GUI for managing containers, images, and volumes.

On Windows, Docker Desktop commonly uses **WSL 2** as its backend.

That does not mean you must perform every Docker command inside a separate Linux terminal. The Docker CLI can still be used from your normal supported terminal.

### Verify Docker

After installation and while Docker Desktop is running:

```bash
docker --version
```

Then:

```bash
docker run hello-world
```

Conceptually, the second command tests a chain:

```text
Docker CLI
   ↓
Docker daemon
   ↓
Image available locally?
   ↓ no
Pull image from registry
   ↓
Create container
   ↓
Run container
   ↓
Print confirmation
```

So `hello-world` is more than a decorative message. It confirms several parts of the local container toolchain can communicate.

### 8.3 Prepare access to a cloud provider

The source walks through creating free-tier or trial access for:

- AWS,
- Microsoft Azure,
- Google Cloud.

You do not need to become expert in all three at once.

For learning, one provider is enough to begin. The important idea is to gain access to a real cloud console where later labs can create compute, storage, networking, or managed services.

Typical signup requirements may include:

- email/account identity,
- contact information,
- phone verification,
- a payment method,
- agreement to provider terms.

### Critical cloud-cost rule

A free tier does **not** mean "everything is free."

Free offers have limits.

Resources outside those limits can create charges.

Build these habits from the beginning:

1. Understand whether the resource is covered before creating it.
2. Use provider billing dashboards.
3. Configure budget or billing alerts when available.
4. Stop or delete resources you no longer need.
5. Do not leave experimental infrastructure running simply because a lab is finished.
6. Protect root/admin accounts and enable strong authentication.

The source specifically warns that providers may require a payment card and that usage beyond the free allowance can be billed.

### Cloud accounts are environments, not trophies

The purpose of creating an account is not to collect AWS, Azure, and GCP logos.

The purpose is to be able to practice:

```text
code
  ↓
version control
  ↓
build/test
  ↓
container/package
  ↓
cloud infrastructure
  ↓
deployment
  ↓
monitoring
```

That is the end-to-end DevOps system you are preparing to learn.

{{exercise:M01.L01.EX04}}

---

## 9. Put everything together: one end-to-end DevOps story

Imagine a team building an API.

### Step 1 — Plan

The product team creates a story:

> "As a customer, I want to view my order status."

The team defines success and adds the work to a backlog.

### Step 2 — Code

A developer edits the API in VS Code.

The repository is tracked with Git.

### Step 3 — Integrate

The developer commits and pushes the change.

A CI pipeline starts.

### Step 4 — Build

The pipeline packages the application and may build a Docker image.

### Step 5 — Test

Automated tests verify behavior and integration.

Security or quality checks may also run.

### Step 6 — Release

A successful artifact becomes a production-ready candidate.

### Step 7 — Deploy

Automation deploys the artifact into cloud infrastructure.

The infrastructure may itself be managed through code.

### Step 8 — Operate

The team keeps the service available, secure, and scalable.

### Step 9 — Monitor

Logs, metrics, and traces reveal what happens under real user traffic.

Suppose the p95 response time rises sharply.

The team now has **feedback**.

### Step 10 — Improve

That observation becomes new planned work.

The loop begins again.

```text
IDE/CLI
   ↓
Git
   ↓
CI
   ↓
Build/Test
   ↓
Artifact or Container
   ↓
Cloud Deployment
   ↓
Operate
   ↓
Logs + Metrics + Traces
   ↓
Feedback
   └──────────────→ Plan
```

This is why the two source chapters belong together.

The first chapter gives you the **mental model**.

The second chapter gives you the **first tools** that let you participate in that model.

---

## Important misconceptions

### Misconception 1

> "DevOps means hiring a person with the job title DevOps Engineer."

### Why this is incomplete

A DevOps engineer can be useful, but DevOps itself is a broader operating culture. If developers still throw code over a wall to a separate "DevOps team," the organization may have renamed the silo rather than removed it.

---

### Misconception 2

> "CI/CD means every commit must automatically go to production."

### Why this is wrong

CI, Continuous Delivery, and Continuous Deployment are different.

CI focuses on frequent integration and automated verification. Continuous Delivery keeps software production-ready while allowing a manual production decision. Continuous Deployment automatically promotes successful changes into production.

---

### Misconception 3

> "Cloud means the provider manages everything."

### Why this is wrong

Responsibility depends on the service model.

With IaaS, you manage much more of the operating system and application stack. With PaaS, the provider manages more of the platform. With SaaS, you consume a finished application.

---

### Misconception 4

> "A GUI makes command-line skills unnecessary."

### Why this is wrong

GUIs are useful, but automation, remote servers, CI jobs, cloud CLIs, containers, and infrastructure tools depend heavily on command-line interfaces and scripts.

---

### Misconception 5

> "If a cloud account says free tier, I cannot be charged."

### Why this is wrong

Free tiers have conditions and limits. Usage outside those limits may incur charges. Cost awareness is part of responsible cloud engineering.

---

## Key terminology

| Term | Meaning |
|---|---|
| DevOps | A culture and set of practices for improving collaboration, automation, feedback, and software delivery flow |
| Wall of confusion | The organizational barrier created when Development and Operations work as isolated silos |
| Systems thinking | Optimizing the complete delivery system rather than one isolated team |
| Agile | A family of iterative approaches emphasizing working software, collaboration, and adaptation |
| Scrum | An Agile framework using time-boxed Sprints and defined roles/events |
| Kanban | A flow-based method that visualizes work and limits work in progress |
| WIP | Work in Progress; started work that has not yet been completed |
| DevOps lifecycle | Continuous flow across Plan, Code, Build, Test, Release, Deploy, Operate, and Monitor |
| Artifact | A versioned build output that can be stored and deployed |
| Automation | Using software to perform repeatable tasks consistently with minimal manual execution |
| CI | Continuous Integration; frequent integration verified by automated build/test feedback |
| Continuous Delivery | Keeping successful changes automatically prepared and production-ready, usually with a final manual release decision |
| Continuous Deployment | Automatically deploying every qualifying change to production |
| IaC | Infrastructure as Code; defining infrastructure through version-controlled code |
| Observability | Ability to understand system behavior using signals such as logs, metrics, and traces |
| IaaS | Infrastructure as a Service; cloud infrastructure with significant customer management responsibility |
| PaaS | Platform as a Service; managed application platform where the provider operates more of the underlying stack |
| SaaS | Software as a Service; complete provider-managed application consumed by users |
| CLI | Command-Line Interface |
| Terminal | Application that provides a text-based interface to a shell |
| Shell | Program that interprets commands, such as Bash or PowerShell |
| Git | Distributed version-control system |
| Container | Isolated, portable application runtime unit containing application code and its needed environment |
| Docker | Platform and toolset for building and running containers |
| Free tier | Limited cloud usage offered without normal service charges under specific provider conditions |

---

## Self-check

Before continuing, make sure you can answer these without looking back:

1. Why can Development and Operations have conflicting incentives even when both teams are doing their jobs well?
2. What does "shared ownership" change about a developer's responsibility?
3. Why did Agile not fully solve the deployment and operations bottleneck?
4. Name all eight stages of the DevOps lifecycle.
5. What is the difference between an artifact and source code?
6. Why is early CI feedback valuable?
7. What single distinction separates Continuous Delivery from Continuous Deployment?
8. How does IaaS differ from PaaS in management responsibility?
9. What is the difference between a terminal and a shell?
10. Why should you run `pwd` and inspect a target path before destructive shell commands?
11. What does `git config --global user.email ...` configure?
12. What does `docker run hello-world` verify conceptually?
13. Why can a cloud "free tier" still produce charges?
14. How do logs, metrics, and traces feed the next planning cycle?
15. Explain the full path from editing code in VS Code to learning from a production metric.

---

## Retain this idea

**DevOps is the continuous system that connects people, code, automation, infrastructure, production, and feedback. Your workstation is the first practical interface into that system.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "devops-culture",
                "title": "DevOps starts with culture, not tools",
                "order": 1,
            },
            {
                "id": "history",
                "title": "From Waterfall to Agile to DevOps",
                "order": 2,
            },
            {
                "id": "lifecycle",
                "title": "The DevOps lifecycle: from idea to feedback",
                "order": 3,
            },
            {
                "id": "automation-ci-cd",
                "title": "Automation, CI, Continuous Delivery, and Continuous Deployment",
                "order": 4,
            },
            {
                "id": "cloud-foundations",
                "title": "Cloud computing and the shared-responsibility ladder",
                "order": 5,
            },
            {
                "id": "cli",
                "title": "Your first DevOps tool: the command line",
                "order": 6,
            },
            {
                "id": "git-vscode",
                "title": "Git and VS Code: make your workstation reproducible and usable",
                "order": 7,
            },
            {
                "id": "docker-cloud-setup",
                "title": "Docker Desktop and cloud access",
                "order": 8,
            },
            {
                "id": "end-to-end-model",
                "title": "Put everything together: one end-to-end DevOps story",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Map a Feature Through the DevOps Lifecycle",

            "lesson_code": "M01.L01",

            "section_id": "lifecycle",

            "placement": "after_section",

            "description": (
                "Practice identifying what happens at each stage of the DevOps "
                "lifecycle instead of memorizing stage names."
            ),

            "instructions": (
                "Scenario: your team is adding password-reset functionality to a web application.\n"
                "1. Create an eight-row table for Plan, Code, Build, Test, Release, Deploy, Operate, and Monitor.\n"
                "2. Write one realistic activity for the password-reset feature in every stage.\n"
                "3. For Monitor, identify one log, one metric, and one possible alert.\n"
                "4. Explain how information from Monitor could create a new item in Plan."
            ),

            "expected_output": (
                "An eight-row lifecycle table plus a short explanation showing "
                "how production feedback closes the loop."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "devops-lifecycle",
                "feedback-loops",
                "observability",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Choose the Right Cloud Service Model",

            "lesson_code": "M01.L01",

            "section_id": "cloud-foundations",

            "placement": "after_section",

            "description": (
                "Practice reasoning about IaaS, PaaS, and SaaS based on how much "
                "control and operational responsibility a scenario requires."
            ),

            "instructions": (
                "For each scenario, choose IaaS, PaaS, or SaaS and justify the choice:\n"
                "1. A team wants full operating-system control for a custom legacy application.\n"
                "2. A startup wants to deploy web code without managing virtual machines.\n"
                "3. A company needs hosted email and collaboration tools for employees.\n"
                "4. For each answer, state one responsibility the provider handles and one responsibility the customer still has."
            ),

            "expected_output": (
                "A four-row comparison table with a service-model choice, provider "
                "responsibility, customer responsibility, and short justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "iaas",
                "paas",
                "saas",
                "shared-responsibility",
            ],
        },

        {
            "id": "M01.L01.EX03",

            "title": "Build and Inspect Your First DevOps Workspace",

            "lesson_code": "M01.L01",

            "section_id": "cli",

            "placement": "after_section",

            "description": (
                "Use basic command-line operations to create a small project "
                "structure and verify each change."
            ),

            "instructions": (
                "1. Create a directory named devops-practice in your home directory.\n"
                "2. Inside it, create src, docs, and scripts directories.\n"
                "3. Create README.md, src/app.txt, and scripts/deploy.sh.\n"
                "4. Put the text '# DevOps Practice' into README.md.\n"
                "5. Use pwd and a recursive listing to verify your current location and structure.\n"
                "6. Copy README.md to docs/README-copy.md.\n"
                "7. Rename src/app.txt to src/application.txt.\n"
                "8. Write down which commands were safe to repeat and which commands would become destructive if the path were wrong."
            ),

            "expected_output": (
                "The completed directory tree, the exact commands used, and a "
                "short safety reflection about destructive filesystem operations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cli-navigation",
                "file-manipulation",
                "shell-safety",
            ],
        },

        {
            "id": "M01.L01.EX04",

            "title": "Verify Your DevOps Workstation",

            "lesson_code": "M01.L01",

            "section_id": "docker-cloud-setup",

            "placement": "after_section",

            "description": (
                "Confirm that the essential beginner workstation components are "
                "available and explain what each verification proves."
            ),

            "instructions": (
                "1. Verify that Git is installed and inspect your global Git configuration.\n"
                "2. Open VS Code and confirm that you can open an integrated terminal.\n"
                "3. Run docker --version.\n"
                "4. Run docker run hello-world while Docker Desktop is running.\n"
                "5. Choose one cloud provider from AWS, Azure, or Google Cloud for future labs.\n"
                "6. Before creating any cloud resource, write a two-item cost-safety checklist you will follow.\n"
                "7. For each verification step, explain what a successful result proves."
            ),

            "expected_output": (
                "A workstation-readiness checklist showing Git, editor/terminal, "
                "Docker verification, one chosen cloud provider, and two cloud-cost safeguards."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "git-setup",
                "vs-code",
                "docker-verification",
                "cloud-cost-awareness",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "DevOps & Cloud Foundations — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "devops-culture",

                "question": (
                    "Which statement best describes DevOps in the context of this lesson?"
                ),

                "options": [
                    "A job title for the person responsible for all deployments",
                    "A culture and set of practices connecting development, operations, automation, and feedback",
                    "A replacement name for the Operations department",
                    "A cloud platform used to host CI servers",
                ],

                "correct": 1,

                "explanation": (
                    "DevOps is broader than a job title or tool. Its core idea is "
                    "shared ownership, automation, rapid feedback, and continuous improvement."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "history",

                "question": (
                    "What was the 'last mile problem' that helped motivate DevOps?"
                ),

                "options": [
                    "Agile teams could not write unit tests",
                    "Development became faster while deployment and operations often remained slow and manual",
                    "Cloud providers could not run Linux servers",
                    "Waterfall did not contain a maintenance phase",
                ],

                "correct": 1,

                "explanation": (
                    "Agile improved iterative development, but many organizations "
                    "still had slow handoffs into deployment and operations. DevOps "
                    "extended the feedback and collaboration model through production."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "lifecycle",

                "question": (
                    "Which lifecycle stage most directly turns production behavior into feedback using logs, metrics, and traces?"
                ),

                "options": [
                    "Plan",
                    "Build",
                    "Release",
                    "Monitor",
                ],

                "correct": 3,

                "explanation": (
                    "Monitoring and observability collect evidence from production. "
                    "That evidence can then inform planning and future improvements."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "automation-ci-cd",

                "question": (
                    "What is the clearest difference between Continuous Delivery and Continuous Deployment?"
                ),

                "options": [
                    "Continuous Delivery cannot use automated tests",
                    "Continuous Deployment does not use version control",
                    "Continuous Delivery can retain a manual production approval, while Continuous Deployment automatically deploys successful changes",
                    "Continuous Delivery is only for cloud applications",
                ],

                "correct": 2,

                "explanation": (
                    "Both rely on automation. The key distinction is whether the "
                    "final qualifying change is automatically deployed to production "
                    "or waits for a human/business release decision."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "automation-ci-cd",

                "question": (
                    "Why does Continuous Integration encourage small, frequent integrations?"
                ),

                "options": [
                    "To make every commit a production release",
                    "To find integration problems earlier when they are smaller and easier to fix",
                    "To eliminate the need for automated tests",
                    "To avoid using branches or version control",
                ],

                "correct": 1,

                "explanation": (
                    "CI shortens the feedback loop. Frequent integration exposes "
                    "conflicts and regressions before they accumulate into a large merge problem."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "cloud-foundations",

                "question": (
                    "Which cloud service model generally gives the customer the most direct control over the operating-system layer?"
                ),

                "options": [
                    "SaaS",
                    "PaaS",
                    "IaaS",
                    "All three provide the same level of control",
                ],

                "correct": 2,

                "explanation": (
                    "IaaS provides infrastructure while leaving more of the software "
                    "stack, including the operating system and application environment, "
                    "under the customer's management."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "cli",

                "question": (
                    "Why is 'rm -rf' treated as a high-risk beginner command?"
                ),

                "options": [
                    "It only works when connected to the cloud",
                    "It can recursively and forcibly delete a directory tree without confirmation",
                    "It permanently disables the terminal",
                    "It automatically deletes Git history from remote repositories",
                ],

                "correct": 1,

                "explanation": (
                    "The recursive and force flags can remove many files with no "
                    "interactive confirmation. The path must be checked carefully."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "git-vscode",

                "question": (
                    "What does 'git config --global user.email ...' primarily configure?"
                ),

                "options": [
                    "The email used to identify the author of commits",
                    "The password for every Git remote",
                    "The email address Docker uses to pull images",
                    "A cloud billing contact",
                ],

                "correct": 0,

                "explanation": (
                    "Git stores author identity information in commit metadata. "
                    "This setting does not configure remote authentication passwords."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "docker-cloud-setup",

                "question": (
                    "What does a successful 'docker run hello-world' most usefully confirm?"
                ),

                "options": [
                    "Your application is production-ready",
                    "The Docker CLI can communicate with the Docker engine and run a container",
                    "Kubernetes is installed and configured",
                    "Your cloud account has no billing limits",
                ],

                "correct": 1,

                "explanation": (
                    "The hello-world test exercises the local Docker client/engine "
                    "path and runs a small container. It does not validate Kubernetes "
                    "or a production application."
                ),
            },

            {
                "id": "M01.L01.Q10",

                "section_id": "docker-cloud-setup",

                "question": (
                    "Which statement about cloud free tiers is safest?"
                ),

                "options": [
                    "Every resource is free as long as the account is new",
                    "Charges are impossible unless you contact support",
                    "Free usage has limits, so resource usage and billing should still be monitored",
                    "A payment method proves that all services are included",
                ],

                "correct": 2,

                "explanation": (
                    "Free offers are bounded by provider-specific conditions and "
                    "limits. Responsible learners monitor usage and remove resources "
                    "that are no longer needed."
                ),
            },

            {
                "id": "M01.L01.Q11",

                "section_id": "end-to-end-model",

                "type": "open",

                "question": (
                    "A developer changes an API in VS Code, commits it with Git, "
                    "and pushes it. Describe a plausible path from that push to "
                    "production and then explain how production feedback could "
                    "create the next planned improvement."
                ),
            },

            {
                "id": "M01.L01.Q12",

                "section_id": "cloud-foundations",

                "type": "open",

                "question": (
                    "A small team wants to ship a web application quickly and does "
                    "not want to administer operating systems. Which cloud service "
                    "model would you evaluate first, and what control-versus-responsibility "
                    "trade-off are you accepting?"
                ),
            },
        ],

        "passing_score": 70,
    },
}
