"""M05.L01 — Constructing Your First CI/CD Pipeline.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 6, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "CI/CD Automation with GitHub Actions"

MODULE_DESCRIPTION = (
    "Connect Git, Docker, Terraform, GitHub Actions, AWS ECR, and AWS App Runner "
    "into a first automated software delivery pipeline, from commit and testing "
    "through image publishing and staging deployment."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Constructing Your First CI/CD Pipeline",

    "slug": "constructing-first-ci-cd-pipeline-m05-l01",

    "description": (
        "Understand Continuous Integration and Continuous Delivery in depth, learn "
        "the GitHub Actions execution model, build an automated test workflow, "
        "understand a two-job container delivery pipeline to AWS staging, and "
        "explore how generative AI can assist pipeline development and review."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "ci-cd",
        "continuous-integration",
        "continuous-delivery",
        "github-actions",
        "pytest",
        "docker",
        "aws-ecr",
        "aws-app-runner",
        "terraform",
        "github-secrets",
        "devops",
        "module-05",
    ],

    "prerequisite_ids": ["M04.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Constructing Your First CI/CD Pipeline",

        "content": r"""
# Constructing Your First CI/CD Pipeline

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M05.L01  
> **Module:** CI/CD Automation with GitHub Actions  
> **Source alignment:** BOOK-XXX, Chapter 6. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain Continuous Integration as a discipline of frequent integration plus automated feedback.
- Distinguish Continuous Delivery from Continuous Deployment.
- Describe a CI/CD pipeline as an automated path from source change to deployable software.
- Explain GitHub Actions concepts: workflow, event, job, step, action, and runner.
- Read and explain a simple GitHub Actions YAML workflow.
- Add a `pytest` test to the Flask application from the previous Docker lesson.
- Build a CI workflow that installs dependencies and runs tests automatically.
- Explain how branch protection can turn CI into a merge quality gate.
- Diagnose a failed GitHub Actions run by inspecting step logs.
- Explain why a container registry is required in the CD pipeline.
- Explain the role of AWS ECR, GitHub Secrets, Terraform, and AWS App Runner in the staging deployment architecture.
- Describe the dependency between a build-and-push job and a deploy job.
- Explain why the ECR repository name must match workflow configuration.
- Explain the principle of least privilege for pipeline cloud credentials.
- Identify realistic uses of generative AI in CI/CD without treating AI as a replacement for pipeline fundamentals.

---

## 1. CI/CD connects the DevOps tools you already learned

Up to this point, each major DevOps tool solved a different part of the delivery problem.

You learned:

```text
Git
→ manage and collaborate on source code

Docker
→ package the application consistently

Terraform
→ define and manage infrastructure
```

The next step is connecting them.

A **CI/CD pipeline** is the automated path that moves a change through the delivery process.

A simple mental model is:

```text
Developer changes code
        ↓
Git push / Pull Request
        ↓
Automated build and tests
        ↓
Package application
        ↓
Publish artifact or image
        ↓
Deploy to environment
        ↓
Running application
```

This is where separate DevOps tools begin acting as one system.

### Why pipelines matter

Without automation, a release might depend on someone remembering to:

1. pull the latest code,
2. install dependencies,
3. run tests,
4. build a Docker image,
5. log in to a registry,
6. tag the image correctly,
7. push it,
8. update infrastructure,
9. deploy it.

Every manual step creates opportunities for:

- forgotten actions,
- inconsistent execution,
- slow feedback,
- deployment errors.

A pipeline turns those repeated mechanics into a defined process.

---

## 2. Continuous Integration: integrate small changes and get feedback fast

**Continuous Integration (CI)** is more than "a tool runs tests."

It is a development discipline.

The source defines CI around frequent integration of changes into a shared repository, often multiple times per day.

After an integration event, automation validates the change.

### The problem CI solves

Imagine three developers working for two weeks without integrating.

Each branch evolves separately.

At the end:

```text
Branch A ────────────────\
                         \
Branch B ─────────────────> giant merge
                         /
Branch C ────────────────/
```

Now the team must solve many conflicts and interaction bugs at once.

This is often called **merge hell**.

CI reduces the size of the problem.

Instead of:

```text
large + rare integrations
```

CI encourages:

```text
small + frequent integrations
```

Small problems are usually easier to understand and fix.

### The CI feedback loop

The source describes this sequence:

```text
1. Developer commits a change
        ↓
2. Push or pull request
        ↓
3. CI system triggers
        ↓
4. Build + automated tests
        ↓
5. Immediate result
        ↓
Pass → continue
Fail → fix quickly
```

The goal is not simply "green checks."

The goal is:

> **detect integration problems as early as possible.**

### Why CI improves quality

CI provides a baseline quality gate.

If a test that used to pass now fails, the team learns immediately.

That is much better than discovering the same regression after several more changes have been layered on top.

### CI is only as strong as its checks

A pipeline can be technically successful while still providing weak quality assurance if the tests are weak.

The source explicitly states:

> A CI pipeline is only as good as its tests.

So CI requires both:

```text
automation
+
meaningful tests
```

[[IMAGE_NEEDED: Continuous Integration feedback loop | A loop showing developer commit → push/pull request → CI runner → build → automated tests → pass/fail feedback returning immediately to the developer | Learner should notice that CI's main value is fast feedback after small integrations]]

---

## 3. Continuous Delivery versus Continuous Deployment

The abbreviation **CD** can refer to two related practices.

They are not the same.

### Continuous Delivery

In the source's framing, Continuous Delivery automates the software release process so that a tested change can automatically reach a testing or staging environment and remain ready for production.

The final production release is still a human decision.

Conceptually:

```text
Code
 ↓
Build
 ↓
Test
 ↓
Package
 ↓
Staging deployment
 ↓
Production-ready
 ↓
Manual release decision
 ↓
Production
```

The technical pipeline prepares a releasable version.

The business or team decides when to expose it to customers.

{{image:production-approval}}

### Continuous Deployment

Continuous Deployment removes the final manual production gate.

```text
Code
 ↓
Build
 ↓
Test
 ↓
All checks pass
 ↓
Automatic production deployment
```

This requires very strong confidence in:

- automated testing,
- deployment safety,
- monitoring,
- rollback or recovery capability.

### The key distinction

| Practice | Automatic testing/build | Automatic staging/release preparation | Final production decision |
|---|---:|---:|---|
| Continuous Integration | Yes | Not necessarily | Not the focus |
| Continuous Delivery | Yes | Yes | Human-controlled |
| Continuous Deployment | Yes | Yes | Automated |

The source focuses the rest of the chapter on **Continuous Delivery** because it combines high automation with a final layer of control.

{{image:ci-cd-pipeline}}

{{exercise:M05.L01.EX01}}

---

## 4. GitHub Actions: the automation model

A CI/CD pipeline needs something to execute automation.

The source mentions alternatives such as:

- Jenkins,
- CircleCI,
- GitLab CI.

For this chapter, the automation platform is **GitHub Actions**.

Its main advantage in this learning path is that it is integrated directly into the GitHub repository already holding the application code.

### Workflows live with the code

GitHub Actions workflows are YAML files stored under:

```text
.github/workflows/
```

This is important conceptually.

Your automation definition becomes part of the repository.

That means the pipeline itself can be:

- versioned,
- reviewed,
- changed through pull requests.

### Core concepts

The source defines six concepts.

### 4.1 Workflow

A **workflow** is the full automated process.

Example:

```text
Continuous Integration
```

or:

```text
Continuous Delivery
```

One workflow can contain one or more jobs.

### 4.2 Event

An **event** triggers a workflow.

Examples from the source include:

```text
push
pull_request
manual triggers
scheduled triggers
```

A workflow answers:

> "When should this automation run?"

### 4.3 Job

A **job** groups steps that execute on the same runner.

By default, separate jobs can run in parallel.

You can also define dependencies so one job waits for another.

This becomes important in the CD pipeline.

For example:

```text
build-and-push
      ↓
   deploy
```

Deployment should not start until the image exists.

### 4.4 Step

A **step** is one task inside a job.

Examples:

```text
check out code
set up Python
install dependencies
run tests
```

Steps inside a job execute in order.

### 4.5 Action

An **action** is a reusable component that can perform a common task.

The source examples include:

```yaml
actions/checkout
actions/setup-python
```

Instead of rewriting common automation logic, workflows can reuse existing actions.

### 4.6 Runner

A **runner** is the machine that executes the job.

The source describes GitHub-hosted runners for:

- Ubuntu,
- Windows,
- macOS.

You can also host your own runner if the environment needs special configuration.

### Put the hierarchy together

```text
Workflow
│
├── Event triggers it
│
├── Job A
│   ├── Runner
│   ├── Step 1
│   ├── Step 2
│   └── Step 3
│
└── Job B
    ├── Runner
    ├── Step 1
    └── Step 2
```

[[IMAGE_NEEDED: GitHub Actions hierarchy | A hierarchy diagram showing Event → Workflow → Jobs → Runner per job → ordered Steps, with some steps using reusable Actions and others executing shell commands | Learner should notice the difference between a workflow, job, step, action, and runner]]

---

## 5. Build the first CI workflow

The source uses the containerized Flask application from the previous Docker lesson.

The CI goal is:

> Run automated tests whenever relevant repository changes occur.

### 5.1 Add pytest

Update `requirements.txt`:

```text
Flask==2.2.2
gunicorn==20.1.0
pytest==7.2.0
```

Now the CI runner can install the test framework together with the application dependencies.

### 5.2 Add a test

Create:

```text
tests/test_app.py
```

with:

```python
from app import app

def test_hello():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello from inside a Docker Container!" in response.data
```

Let's understand what this verifies.

```python
client = app.test_client()
```

creates a Flask test client.

```python
response = client.get("/")
```

sends a request to the root endpoint.

Then:

```python
assert response.status_code == 200
```

checks that the request succeeds.

And:

```python
assert b"Hello from inside a Docker Container!" in response.data
```

checks that the response contains the expected content.

This is a small test, but it demonstrates the CI principle:

```text
known expected behavior
        ↓
automated check
        ↓
pass or fail
```

### 5.3 Create `.github/workflows/ci.yml`

The source provides:

```yaml
name: Continuous Integration

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests with pytest
        run: |
          pytest
```

### Read this workflow top to bottom

#### Workflow name

```yaml
name: Continuous Integration
```

This is the human-readable name shown in GitHub.

#### Triggers

```yaml
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
```

The workflow runs:

- on pushes to `main`,
- on pull requests targeting `main`.

That gives feedback both before and after integration events in the workflow described by the source.

#### One job

```yaml
jobs:
  build-and-test:
```

The workflow has one job.

#### Runner

```yaml
runs-on: ubuntu-latest
```

The job executes on a GitHub-hosted Ubuntu runner.

#### Checkout step

```yaml
uses: actions/checkout@v3
```

This makes repository code available on the runner.

Without the source files, later test commands would have nothing to execute against.

#### Python setup

```yaml
uses: actions/setup-python@v4
```

with:

```yaml
python-version: "3.9"
```

prepares the required Python runtime.

#### Dependency installation

```yaml
run: |
  python -m pip install --upgrade pip
  pip install -r requirements.txt
```

installs the application and test dependencies.

#### Test execution

```yaml
run: |
  pytest
```

runs the automated test suite.

### The resulting execution path

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Ubuntu runner
        ↓
Checkout repository
        ↓
Set up Python 3.9
        ↓
Install requirements
        ↓
pytest
        ↓
Pass or Fail
```

{{exercise:M05.L01.EX02}}

---

## 6. Turn CI into a real quality gate

A CI workflow is helpful.

But it becomes more powerful when the repository's merge rules depend on it.

### Branch protection

The source recommends branch protection on `main`.

Conceptually:

```text
Pull Request
     ↓
CI tests
     ↓
Pass?
 ┌───┴───┐
No      Yes
↓         ↓
Block    Review/merge can continue
```

This changes CI from:

> "a useful notification"

into:

> "a required condition for merging."

### Why this matters

Without enforcement, someone can ignore a red pipeline and merge anyway.

A required status check turns the automated test result into a governance rule.

### Observe the workflow

After committing:

```bash
git add .
git commit -m "ci: Add pytest and initial CI workflow"
```

and pushing:

```bash
git push origin main
```

the source directs the learner to the GitHub **Actions** tab.

There, you can inspect:

- workflow run,
- job,
- individual steps,
- logs.

### Debugging failures

A failed pipeline is useful feedback.

The source recommends:

1. open the failed workflow run,
2. expand the failed step,
3. read the full log,
4. identify the exact error,
5. fix the issue,
6. push a new commit.

For transient failures, the source also notes the **Re-run jobs** option.

### A disciplined debugging model

```text
Red workflow
    ↓
Which job failed?
    ↓
Which step failed?
    ↓
What does the log say?
    ↓
Is it code, configuration, dependency, or transient?
    ↓
Fix or rerun appropriately
```

Do not treat a red pipeline as "GitHub Actions is broken."

Treat the logs as evidence.

---

## 7. Design the Continuous Delivery pipeline

The source then extends CI into deployment.

The target flow is:

```text
Change merged to main
        ↓
Build Docker image
        ↓
Push image to AWS ECR
        ↓
Pass image URI forward
        ↓
Terraform deploys/updates App Runner staging service
        ↓
Application runs in AWS staging
```

This combines the earlier lessons:

```text
GitHub
+ GitHub Actions
+ Docker
+ AWS ECR
+ Terraform
+ AWS App Runner
```

### Important source boundary

The supplied chapter shows only the beginning of `cd.yml` and replaces the rest with:

```text
....
```

So this lesson teaches the architecture and the explicitly described job relationship without inventing the omitted workflow code.

### 7.1 AWS ECR: the image registry

The source chooses **Amazon Elastic Container Registry (ECR)** as the registry for the CD workflow.

The Docker image needs a location that the AWS staging environment can access.

Conceptually:

```text
CI runner
   |
   | docker image push
   v
AWS ECR
   |
   | image URI
   v
AWS App Runner
```

The source's technical requirements also mention a Docker Hub account, but the shown CD deployment path specifically uses ECR.

### Repository-name consistency

The source warns that the ECR repository name must match the workflow's:

```yaml
ECR_REPOSITORY
```

value.

If the actual repository is:

```text
simple-flask-app
```

but the workflow uses a different name, the push stage can fail.

This is a good example of why configuration consistency matters in pipelines.

### 7.2 AWS credentials via GitHub Secrets

The source stores:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

as GitHub repository secrets.

The main idea is:

> Sensitive credentials should not be written directly into workflow files.

The workflow references secrets securely at execution time.

### Least privilege

The source additionally recommends the **principle of least privilege**.

Instead of giving the pipeline broad permissions "just in case," give it only what the pipeline actually needs.

The chapter gives examples such as ECR actions and the minimum App Runner permissions required.

Why?

Because leaked or misused pipeline credentials should have the smallest possible blast radius.

### 7.3 Terraform manages the staging service

The chapter creates:

```text
terraform/main.tf
```

for AWS App Runner.

Its core resource is:

```hcl
resource "aws_apprunner_service" "staging"
```

The service uses:

```hcl
var.ecr_image_identifier
```

as the image URI.

This is a key integration point.

The build job produces an image.

Terraform receives that image's URI.

Then Terraform updates the staging infrastructure to use it.

### Data flow

```text
Docker build
    ↓
ECR image URI
    ↓
Terraform input variable
    ↓
App Runner source_configuration
    ↓
Staging service
```

### App Runner output

The Terraform code also defines:

```hcl
output "service_url" {
  value = aws_apprunner_service.staging.service_url
}
```

So Terraform can expose the staging service URL after deployment.

[[IMAGE_NEEDED: CD staging architecture | A system diagram showing GitHub push → GitHub Actions build-and-push job → Docker build → AWS ECR → image URI output → deploy job → Terraform → AWS App Runner staging service → service URL | Learner should notice how the Docker image URI becomes the bridge between the build job and Terraform deployment]]

---

## 8. Understand the two-job CD workflow

The source shows the beginning of:

```yaml
name: Continuous Delivery

on:
  push:
    branches: [ "main" ]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: simple-flask-app

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.build-image.outputs.image }}

  ....
```

The remainder is omitted in the supplied source.

But the source explains the structure.

### Job 1 — build and push

The `build-and-push` job:

1. builds the Docker image,
2. pushes it to ECR,
3. produces the full image URI as an output.

Think:

```text
Source
 ↓
Docker build
 ↓
Image
 ↓
ECR push
 ↓
Image URI output
```

### Job 2 — deploy

The deploy job:

1. waits for the first job to succeed,
2. receives the image URI,
3. runs Terraform,
4. passes that URI as the `ecr_image_identifier` variable,
5. creates or updates the App Runner service.

Think:

```text
Image URI
   ↓
Terraform apply
   ↓
App Runner staging
```

### Why job dependency matters

If deployment started before the image had been published, Terraform could point App Runner to an image that does not exist yet.

So the pipeline must express:

```text
build-and-push succeeds
        ↓
deploy may begin
```

This is a general pipeline principle:

> Downstream work should depend on the successful completion of the upstream artifact it needs.

### Pipeline artifacts and values

The Docker image is the deployable artifact.

The image URI is the value passed between pipeline stages.

That distinction is useful:

```text
Artifact:
container image

Reference:
ECR image URI
```

{{exercise:M05.L01.EX03}}

---

## 9. Generative AI as an assistant for CI/CD work

The final section of the source explores generative AI.

The chapter is careful about the role of AI:

> AI can accelerate DevOps work, but it does not remove the need to understand the fundamentals.

That is the right mental model.

### 9.1 Generate or assist with configuration

The source gives GitHub Copilot as an example.

AI can help suggest:

- YAML steps,
- jobs,
- action names,
- environment variables,
- Dockerfile content,
- Terraform snippets.

This can reduce syntax mistakes and lookup time.

But you still need to understand:

```text
What triggers this workflow?
What permissions does it have?
What is being deployed?
What happens if it fails?
```

### 9.2 Generate tests

AI can help draft unit tests.

That may improve test coverage and strengthen the CI quality gate.

But generated tests still need review.

A generated test that asserts the wrong behavior can give false confidence.

### 9.3 AI-assisted review and DevSecOps

The source describes AI-assisted review that may identify:

- common bugs,
- security issues,
- style inconsistencies.

This can act as an early automated quality gate.

Human reviewers can then focus on:

- architecture,
- business logic,
- system trade-offs,
- intent.

### 9.4 Failure analysis

If a pipeline test fails, AI may help analyze:

- logs,
- code changes,
- likely root cause.

The value is not replacing the evidence.

The value is making the evidence easier to interpret.

### 9.5 Communication automation

The source also lists:

- commit message generation,
- pull request description drafting,
- release note generation.

These are useful because CI/CD creates a large amount of technical metadata that teams must communicate clearly.

### Safe mental model

```text
AI should assist:
- drafting
- summarizing
- suggesting
- reviewing
- diagnosing

Human/engineering process still owns:
- correctness
- credentials
- permissions
- release decisions
- architecture
- production safety
```

{{exercise:M05.L01.EX04}}

---

## 10. Put the entire pipeline together

Now combine the whole chapter.

A developer changes the Flask application.

### Stage 1 — source control

```text
Developer
   ↓
Git commit
   ↓
GitHub push / PR
```

### Stage 2 — CI

GitHub Actions:

```text
checks out code
    ↓
sets up Python
    ↓
installs dependencies
    ↓
runs pytest
```

If tests fail:

```text
pipeline stops
↓
developer investigates
```

If tests pass, the change can continue through the repository's review and merge rules.

### Stage 3 — CD trigger

After the relevant change reaches `main`, the CD workflow runs.

### Stage 4 — container build

```text
application source
+
Dockerfile
        ↓
Docker image
```

### Stage 5 — registry

```text
Docker image
     ↓
AWS ECR
```

### Stage 6 — handoff between jobs

The first job exposes:

```text
full ECR image URI
```

### Stage 7 — Terraform deploy

The deploy job passes that URI into Terraform:

```text
var.ecr_image_identifier
```

### Stage 8 — staging environment

Terraform creates or updates:

```text
AWS App Runner staging service
```

### Stage 9 — output

Terraform exposes:

```text
service_url
```

The result is a running application in staging.

### End-to-end picture

```text
Developer
   ↓
Git
   ↓
GitHub
   ↓
GitHub Actions CI
   ├── checkout
   ├── Python setup
   ├── install
   └── pytest
   ↓
Merge to main
   ↓
GitHub Actions CD
   ↓
Docker build
   ↓
AWS ECR
   ↓
Image URI
   ↓
Terraform
   ↓
AWS App Runner
   ↓
Staging URL
```

This is the first point in the course where the major tools from earlier lessons operate as one connected delivery system.

---

## Important misconceptions

### Misconception 1

> "CI means automatically deploying every commit."

### Why this is wrong

CI focuses on frequent integration, automated build/test, and fast feedback.

Deployment belongs to later delivery stages.

---

### Misconception 2

> "Continuous Delivery and Continuous Deployment are identical."

### Why this is wrong

The source distinguishes them by the final production decision.

Continuous Delivery keeps software ready while retaining a manual production gate.

Continuous Deployment removes that final human gate.

---

### Misconception 3

> "A GitHub Actions workflow is the same thing as a job."

### Why this is wrong

A workflow can contain multiple jobs.

Each job contains ordered steps and runs on a runner.

---

### Misconception 4

> "An action and a step are the same thing."

### Why this is incomplete

A step is one task inside a job.

A step can invoke a reusable action or execute shell commands directly.

---

### Misconception 5

> "If CI is green, the application must be perfect."

### Why this is wrong

CI only verifies the checks you actually define.

Weak or incomplete tests create weak evidence.

---

### Misconception 6

> "Pipeline credentials should be written directly in `cd.yml`."

### Why this is wrong

The source uses GitHub Secrets for AWS credentials.

Sensitive values should not be committed in workflow source.

---

### Misconception 7

> "The CD deploy job can run independently of the image build."

### Why this is wrong

The deploy step needs the image URI produced by the successful build-and-push job.

---

### Misconception 8

> "The source provides the full CD YAML."

### Why this is wrong

The supplied chapter explicitly replaces the remainder of the workflow with `....` and says the rest is available in the book's repository.

This lesson therefore explains only the architecture and workflow behavior supported by the supplied text.

---

### Misconception 9

> "Generative AI removes the need to understand CI/CD."

### Why this is wrong

The source explicitly presents AI as an accelerator and assistant, not a replacement for understanding the pipeline.

---

## Key terminology

| Term | Meaning |
|---|---|
| CI | Continuous Integration; frequent integration plus automated build/test feedback |
| CD | Continuous Delivery in this chapter's main workflow; automation that keeps software ready for release |
| Continuous Deployment | Automatic release to production after successful pipeline checks |
| Pipeline | Automated sequence moving a software change through delivery stages |
| GitHub Actions | GitHub's workflow automation platform used in the chapter |
| Workflow | Automated process defined in YAML under `.github/workflows/` |
| Event | Activity that triggers a workflow |
| Job | Group of steps executed on the same runner |
| Step | Individual task inside a job |
| Action | Reusable automation component used by a step |
| Runner | Machine that executes a GitHub Actions job |
| `pytest` | Python testing framework used in the CI example |
| Status check | Automated result that can be required before merge |
| Branch protection | Repository rule that can block merging until required conditions pass |
| ECR | Amazon Elastic Container Registry |
| Registry | Service used to store and distribute container images |
| GitHub Secret | Encrypted repository value available to workflows |
| Least privilege | Granting only the permissions required for a task |
| App Runner | AWS service used by the source for the staging deployment |
| Image URI | Registry reference identifying the Docker image to deploy |
| DevSecOps | Integrating security checks and concerns into software delivery workflows |

---

## Self-check

Before continuing, make sure you can answer:

1. What delivery problem does CI/CD automation solve?
2. Why does CI encourage small and frequent integrations?
3. What happens after a CI trigger in the source's feedback loop?
4. What is the difference between Continuous Delivery and Continuous Deployment?
5. Where must GitHub Actions workflow files be stored?
6. What is the difference between a workflow and a job?
7. What is the difference between a job and a step?
8. What is a runner?
9. What does `actions/checkout` accomplish in the CI workflow?
10. Why does the workflow set up Python before running `pytest`?
11. What behavior does the Flask test verify?
12. Why can branch protection make CI more meaningful?
13. Where should you look first when a workflow fails?
14. Why does the CD pipeline need a container registry?
15. What role does ECR play?
16. Why are AWS credentials stored as GitHub Secrets?
17. What does least privilege mean for the pipeline IAM identity?
18. What Terraform variable receives the container image URI?
19. Why must the deploy job wait for the build-and-push job?
20. What does the Terraform `service_url` output represent?
21. Which parts of the CD workflow code are actually present in the supplied source, and which part is omitted?
22. Name three ways generative AI can assist CI/CD work.
23. Why must AI-generated pipeline configuration still be reviewed?
24. Explain the full path from Git commit to staging App Runner service.

---

## Retain this idea

**CI/CD is the automated connection between the DevOps practices you already learned: Git triggers feedback, tests protect quality, Docker produces the deployable artifact, a registry distributes it, and Terraform delivers it into a managed environment.**
""",

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "ci-cd-foundations",
                "title": "CI/CD connects the DevOps tools you already learned",
                "order": 1,
            },
            {
                "id": "continuous-integration",
                "title": "Continuous Integration: integrate small changes and get feedback fast",
                "order": 2,
            },
            {
                "id": "delivery-deployment",
                "title": "Continuous Delivery versus Continuous Deployment",
                "order": 3,
            },
            {
                "id": "github-actions-model",
                "title": "GitHub Actions: the automation model",
                "order": 4,
            },
            {
                "id": "build-ci",
                "title": "Build the first CI workflow",
                "order": 5,
            },
            {
                "id": "quality-gates",
                "title": "Turn CI into a real quality gate",
                "order": 6,
            },
            {
                "id": "cd-architecture",
                "title": "Design the Continuous Delivery pipeline",
                "order": 7,
            },
            {
                "id": "multi-job-workflow",
                "title": "Understand the two-job CD workflow",
                "order": 8,
            },
            {
                "id": "ai-pipelines",
                "title": "Generative AI as an assistant for CI/CD work",
                "order": 9,
            },
            {
                "id": "end-to-end",
                "title": "Put the entire pipeline together",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",

            "title": "Classify CI, Delivery, and Deployment",

            "lesson_code": "M05.L01",

            "section_id": "delivery-deployment",

            "placement": "after_section",

            "description": (
                "Practice distinguishing the three automation levels from realistic "
                "software delivery scenarios."
            ),

            "instructions": (
                "For each scenario, classify it as Continuous Integration, Continuous Delivery, "
                "or Continuous Deployment, and explain why:\n"
                "1. Every pull request automatically runs unit tests but never deploys anything.\n"
                "2. Every successful merge builds and deploys automatically to staging, while production requires a manual approval.\n"
                "3. Every change that passes the full pipeline goes automatically to production.\n"
                "4. For each scenario, identify the feedback or control benefit provided by that practice."
            ),

            "expected_output": (
                "A three-row classification table with the practice, evidence from the scenario, "
                "and the main automation or control benefit."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "continuous-integration",
                "continuous-delivery",
                "continuous-deployment",
            ],
        },

        {
            "id": "M05.L01.EX02",

            "title": "Build and Explain the CI Workflow",

            "lesson_code": "M05.L01",

            "section_id": "build-ci",

            "placement": "after_section",

            "description": (
                "Implement the source's first GitHub Actions CI workflow and explain "
                "the purpose of every major YAML block."
            ),

            "instructions": (
                "1. Add pytest to requirements.txt using the version shown in the lesson.\n"
                "2. Create tests/test_app.py with the Flask endpoint test from the lesson.\n"
                "3. Create .github/workflows/ci.yml using the supplied workflow.\n"
                "4. For each of these items, explain its purpose: name, on, jobs, runs-on, steps, uses, run.\n"
                "5. Commit the files with a meaningful CI-related commit message.\n"
                "6. Push the change and inspect the workflow in the GitHub Actions UI.\n"
                "7. Record which step runs first, which runs last, and what evidence proves the test passed."
            ),

            "expected_output": (
                "A working CI workflow plus a structured explanation of its trigger, runner, "
                "steps, reusable actions, commands, and final test result."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "github-actions",
                "workflow-yaml",
                "pytest",
                "ci",
            ],
        },

        {
            "id": "M05.L01.EX03",

            "title": "Trace the CD Data Flow",

            "lesson_code": "M05.L01",

            "section_id": "multi-job-workflow",

            "placement": "after_section",

            "description": (
                "Practice reasoning about the CD architecture without inventing the omitted "
                "workflow code from the source."
            ),

            "instructions": (
                "Using only the architecture described in the lesson:\n"
                "1. Draw a flow from a push to main through build-and-push and deploy.\n"
                "2. Mark where the Docker image is created.\n"
                "3. Mark where the image is stored.\n"
                "4. Mark where the image URI is produced and consumed.\n"
                "5. Mark where Terraform runs.\n"
                "6. Mark where the App Runner staging service is created or updated.\n"
                "7. Explain why the deploy job must depend on build-and-push.\n"
                "8. Explain what would happen conceptually if ECR_REPOSITORY did not match the real ECR repository name."
            ),

            "expected_output": (
                "A pipeline diagram plus a short explanation of the artifact, image URI, "
                "job dependency, Terraform input, and configuration consistency requirement."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "continuous-delivery",
                "docker-image",
                "aws-ecr",
                "terraform",
                "aws-app-runner",
                "job-dependencies",
            ],
        },

        {
            "id": "M05.L01.EX04",

            "title": "Evaluate AI Assistance in a Pipeline",

            "lesson_code": "M05.L01",

            "section_id": "ai-pipelines",

            "placement": "after_section",

            "description": (
                "Practice deciding where generative AI can help and where human engineering "
                "review remains necessary."
            ),

            "instructions": (
                "For each task below, state how AI could assist and what a human must still verify:\n"
                "1. Generate a GitHub Actions YAML step.\n"
                "2. Draft unit tests for a Flask endpoint.\n"
                "3. Analyze a failed workflow log.\n"
                "4. Draft a pull request description.\n"
                "5. Suggest an IAM policy for the deployment pipeline.\n"
                "6. Write a short rule explaining why security-sensitive AI suggestions must be reviewed before use."
            ),

            "expected_output": (
                "A six-row table separating AI assistance from human verification responsibility."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "generative-ai",
                "ci-cd",
                "review",
                "security-awareness",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Constructing Your First CI/CD Pipeline — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",

                "section_id": "continuous-integration",

                "question": (
                    "What is the primary goal of Continuous Integration in the source?"
                ),

                "options": [
                    "To deploy every commit directly to production",
                    "To detect integration problems as early as possible",
                    "To replace Git with GitHub Actions",
                    "To remove the need for automated tests",
                ],

                "correct": 1,

                "explanation": (
                    "CI uses frequent integration and automated build/test feedback to expose "
                    "problems while changes are still small."
                ),
            },

            {
                "id": "M05.L01.Q02",

                "section_id": "delivery-deployment",

                "question": (
                    "What distinguishes Continuous Delivery from Continuous Deployment in this chapter?"
                ),

                "options": [
                    "Continuous Delivery has no automated tests",
                    "Continuous Delivery keeps a manual production release decision, while Continuous Deployment does not",
                    "Continuous Deployment cannot use staging",
                    "Continuous Delivery does not build artifacts",
                ],

                "correct": 1,

                "explanation": (
                    "The source identifies the final human production gate as the central distinction."
                ),
            },

            {
                "id": "M05.L01.Q03",

                "section_id": "github-actions-model",

                "question": (
                    "Where must GitHub Actions workflow YAML files be stored?"
                ),

                "options": [
                    ".github/workflows/",
                    ".git/actions/",
                    "terraform/workflows/",
                    "docker/actions/",
                ],

                "correct": 0,

                "explanation": (
                    "The source states that GitHub Actions workflows live under `.github/workflows/`."
                ),
            },

            {
                "id": "M05.L01.Q04",

                "section_id": "github-actions-model",

                "question": (
                    "Which GitHub Actions concept is the machine that actually executes a job?"
                ),

                "options": [
                    "Event",
                    "Action",
                    "Runner",
                    "Workflow name",
                ],

                "correct": 2,

                "explanation": (
                    "A runner is the execution machine for a GitHub Actions job."
                ),
            },

            {
                "id": "M05.L01.Q05",

                "section_id": "build-ci",

                "question": (
                    "What does actions/checkout do in the source CI workflow?"
                ),

                "options": [
                    "Deploys the application to App Runner",
                    "Makes the repository source code available on the runner",
                    "Creates an ECR repository",
                    "Runs pytest automatically without source files",
                ],

                "correct": 1,

                "explanation": (
                    "The checkout action retrieves the repository contents onto the runner so later steps can use them."
                ),
            },

            {
                "id": "M05.L01.Q06",

                "section_id": "build-ci",

                "question": (
                    "What two properties does the supplied Flask test explicitly verify?"
                ),

                "options": [
                    "Docker image size and Terraform state",
                    "HTTP 200 status and expected response text",
                    "ECR repository name and IAM permissions",
                    "Python version and Ubuntu version",
                ],

                "correct": 1,

                "explanation": (
                    "The test asserts a 200 response and checks for the expected Hello message in the response body."
                ),
            },

            {
                "id": "M05.L01.Q07",

                "section_id": "quality-gates",

                "question": (
                    "Why would a team require the CI status check in branch protection?"
                ),

                "options": [
                    "To ensure changes cannot merge to main until the required automated check passes",
                    "To disable pull requests",
                    "To make GitHub Actions run only once",
                    "To store AWS credentials in the branch rule",
                ],

                "correct": 0,

                "explanation": (
                    "Required status checks turn CI into an enforced merge quality gate."
                ),
            },

            {
                "id": "M05.L01.Q08",

                "section_id": "cd-architecture",

                "question": (
                    "What is AWS ECR used for in the chapter's CD pipeline?"
                ),

                "options": [
                    "Running pytest",
                    "Storing the Docker image",
                    "Replacing Terraform state",
                    "Hosting Git branches",
                ],

                "correct": 1,

                "explanation": (
                    "ECR is the container registry used to hold the built Docker image."
                ),
            },

            {
                "id": "M05.L01.Q09",

                "section_id": "cd-architecture",

                "question": (
                    "Why are AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY configured as GitHub Secrets?"
                ),

                "options": [
                    "Because secrets are encrypted workflow inputs for sensitive values",
                    "Because Terraform cannot use environment variables",
                    "Because Docker requires them in the source repository",
                    "Because GitHub Secrets automatically create IAM users",
                ],

                "correct": 0,

                "explanation": (
                    "The source uses GitHub Secrets so sensitive credentials are not written directly into workflow code."
                ),
            },

            {
                "id": "M05.L01.Q10",

                "section_id": "multi-job-workflow",

                "question": (
                    "What important value is passed from the build-and-push job to the deploy job?"
                ),

                "options": [
                    "The Flask test client",
                    "The full ECR image URI",
                    "The Git commit message only",
                    "The runner operating system",
                ],

                "correct": 1,

                "explanation": (
                    "The first job produces the full image URI, which the deployment job passes into Terraform."
                ),
            },

            {
                "id": "M05.L01.Q11",

                "section_id": "multi-job-workflow",

                "question": (
                    "Why must the deploy job wait for build-and-push?"
                ),

                "options": [
                    "Because the staging deployment requires the image that the first job creates and publishes",
                    "Because GitHub Actions never allows parallel jobs",
                    "Because Terraform must run before Docker",
                    "Because App Runner stores Git commits instead of images",
                ],

                "correct": 0,

                "explanation": (
                    "Deployment depends on an image URI that does not exist until the build-and-push work succeeds."
                ),
            },

            {
                "id": "M05.L01.Q12",

                "section_id": "ai-pipelines",

                "question": (
                    "How does the source frame generative AI in CI/CD?"
                ),

                "options": [
                    "As a replacement for understanding DevOps fundamentals",
                    "As an assistant that can accelerate configuration, testing, review, diagnosis, and documentation",
                    "As a requirement for GitHub Actions to function",
                    "As a secure replacement for IAM permissions",
                ],

                "correct": 1,

                "explanation": (
                    "The source presents AI as a productivity and quality accelerator while explicitly preserving the need for fundamental understanding."
                ),
            },

            {
                "id": "M05.L01.Q13",

                "section_id": "end-to-end",

                "type": "open",

                "question": (
                    "Describe the full delivery path taught in this lesson from a developer's Git change "
                    "to a running AWS App Runner staging service. Include CI testing, Docker image creation, "
                    "ECR, the image URI handoff, Terraform, and the role of GitHub Actions."
                ),
            },
        ],

        "passing_score": 70,
    },
}
