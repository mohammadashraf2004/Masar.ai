"""M04.L01 — Introduction to Infrastructure as Code with Terraform.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 5, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Infrastructure as Code with Terraform"

MODULE_DESCRIPTION = (
    "Learn how Infrastructure as Code replaces manual infrastructure management "
    "with version-controlled configuration, then use Terraform providers, resources, "
    "state, plans, applies, variables, and outputs to manage cloud resources."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introduction to Infrastructure as Code with Terraform",

    "slug": "terraform-infrastructure-as-code-m04-l01",

    "description": (
        "Understand why Infrastructure as Code matters, how Terraform models cloud "
        "infrastructure, and how to safely define, preview, create, modify, destroy, "
        "and parameterize cloud resources."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "terraform",
        "infrastructure-as-code",
        "iac",
        "hcl",
        "terraform-state",
        "terraform-plan",
        "terraform-apply",
        "aws",
        "variables",
        "outputs",
    ],

    "prerequisite_ids": ["M03.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to Infrastructure as Code with Terraform",

        "content": r"""
# Introduction to Infrastructure as Code with Terraform

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M04.L01  
> **Module:** Infrastructure as Code with Terraform  
> **Source alignment:** BOOK-XXX, Chapter 5. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why manual infrastructure management creates speed, consistency, and collaboration problems.
- Define Infrastructure as Code (IaC).
- Distinguish declarative and imperative infrastructure approaches.
- Explain Terraform's role as a declarative IaC tool.
- Describe the purpose of Terraform providers, resources, and state.
- Explain why the Terraform state file is important and why it should not be committed to Git.
- Explain the purpose of a remote backend in the workflow described by the source.
- Install and verify Terraform.
- Write a basic Terraform configuration for AWS.
- Explain the `terraform init → terraform plan → terraform apply` workflow.
- Interpret create, destroy, and modify indicators in a Terraform plan.
- Explain configuration drift and how Terraform detects it.
- Destroy managed infrastructure with `terraform destroy`.
- Replace hardcoded values with Terraform input variables.
- Explain how `.tfvars` files provide variable values.
- Create Terraform outputs and reference resource attributes.
- Connect Terraform planning to pull-request review in a professional workflow.

---

## 1. Infrastructure as Code: managing infrastructure like software

In the previous lesson, Docker gave us a repeatable application artifact.

That solved one major question:

> "How do we package the application so it runs consistently?"

But an application still needs somewhere to run.

It may require:

- servers,
- networks,
- storage,
- databases,
- firewalls,
- load balancers.

The next DevOps question is:

> **How do we create and manage infrastructure with the same discipline we use for application code?**

That is the role of **Infrastructure as Code (IaC)**.

### The old model: click-ops

The source describes the traditional infrastructure workflow as a manual process.

A developer might request a server.

An operations engineer might then:

1. open a cloud console,
2. click through several configuration screens,
3. choose sizes and regions,
4. configure networking,
5. set permissions,
6. repeat the same steps for another environment.

This manual style is often called **click-ops**.

The problem is not that clicking is inherently bad.

The problem is that repeated manual configuration is difficult to make:

- fast,
- consistent,
- repeatable,
- reviewable,
- versioned.

### What IaC changes

With IaC, infrastructure is described in machine-readable files.

Instead of saying:

```text
"Log into AWS and create this resource manually."
```

you write configuration that describes the infrastructure.

Conceptually:

```text
Manual model

Human
  ↓
Cloud console
  ↓
Click settings
  ↓
Resource created


IaC model

Configuration file
  ↓
IaC tool
  ↓
Cloud API
  ↓
Resource created
```

IaC shifts infrastructure from an undocumented manual process into something that can be stored, reviewed, repeated, and automated.

### Four major benefits from the source

#### 1. Automation and speed

A reusable infrastructure definition can create many resources without repeating every manual step.

This makes it possible to create environments much faster.

#### 2. Consistency and reliability

Manual configuration tends to drift.

One environment may have:

```text
Server A
- setting X enabled
- port Y open
- package Z version 1
```

while another manually created server may differ slightly.

IaC reduces this variation by using the same source configuration.

#### 3. Version control and collaboration

Infrastructure definitions can be stored in Git.

That gives you:

- history,
- change tracking,
- pull requests,
- code review,
- team visibility.

Infrastructure changes become reviewable work.

#### 4. Cost control through easy teardown

If environments can be created from code, they can also be destroyed from code.

The source highlights this as useful for temporary development or test environments.

Create what you need, use it, then remove it when it is no longer required.

[[IMAGE_NEEDED: Click-ops versus Infrastructure as Code | A side-by-side diagram. Left side shows a human manually clicking through cloud-console screens to create resources. Right side shows version-controlled Terraform files flowing through Terraform into cloud APIs to create the same resources | Learner should notice that IaC turns manual infrastructure steps into repeatable, reviewable configuration]]

### The central idea

Remember:

```text
Application code defines software behavior.
Infrastructure code defines the environment the software runs on.
```

Both can be:

- version controlled,
- reviewed,
- automated,
- reproduced.

---

## 2. Declarative versus imperative infrastructure

The source introduces two broad IaC styles.

### Imperative approach

An imperative approach describes **the steps**.

Think:

```text
1. Create a virtual machine.
2. Attach a 10 GB disk.
3. Install Apache.
4. Configure the service.
```

The logic is procedural.

You specify how to reach the final state.

The source uses tools such as Ansible and Chef as examples that can use an imperative style.

### Declarative approach

A declarative approach describes **the desired final state**.

Think:

```text
"I want one virtual machine
with these specifications
and this storage configuration."
```

Then the tool decides what actions are needed.

Terraform is presented in the source as a declarative tool.

### The blueprint analogy

The source uses an intuitive comparison:

```text
Imperative = recipe
Declarative = blueprint
```

A recipe says:

```text
Do step A
then step B
then step C
```

A blueprint says:

```text
This is what the finished thing should look like.
```

### Why declarative thinking matters in Terraform

Suppose your code says:

```text
Desired state:
1 S3 bucket
```

If zero buckets exist, Terraform may plan to create one.

If the managed bucket already exists as expected, Terraform may plan no change.

If the real infrastructure no longer matches the configuration, Terraform can detect the difference and plan a correction.

This desired-state comparison is one of the most important mental models in the entire chapter.

```text
Desired state in code
        ↓
compare
        ↓
Known/current infrastructure state
        ↓
difference
        ↓
execution plan
```

{{exercise:M04.L01.EX01}}

---

## 3. Terraform fundamentals: providers, resources, and state

Terraform is an open-source Infrastructure as Code tool created by HashiCorp.

The source presents Terraform as cloud-agnostic because it can work with many external platforms through **providers**.

Terraform configuration is written in **HashiCorp Configuration Language (HCL)**.

Three concepts form the foundation of this lesson:

1. Providers
2. Resources
3. State

### 3.1 Providers: plugins for external APIs

A Terraform **provider** understands how to communicate with a particular service or platform.

Examples named in the source include:

- AWS,
- Azure,
- GCP,
- GitHub,
- Docker.

Conceptually:

```text
Terraform configuration
       ↓
Provider
       ↓
Platform API
       ↓
Real resource
```

The AWS provider understands AWS APIs.

The Azure provider understands Azure APIs.

Terraform itself provides the workflow and language; providers connect that workflow to external systems.

### Provider installation

When you declare a provider and run:

```bash
terraform init
```

Terraform downloads the provider plugin required by the configuration.

### 3.2 Resources: the building blocks

A Terraform **resource** represents an infrastructure object.

Examples include:

- storage bucket,
- virtual network,
- compute instance,
- DNS record.

The source gives this form:

```hcl
resource "aws_s3_bucket" "app_bucket" {
  bucket = "my-unique-devops-book-bucket-12345"

  tags = {
    Name        = "My DevOps Bucket"
    Environment = "Dev"
  }
}
```

A resource block has two important labels.

```hcl
resource "aws_s3_bucket" "app_bucket"
```

Here:

```text
aws_s3_bucket
```

is the **resource type** defined by the AWS provider.

```text
app_bucket
```

is the **local name** used to reference that resource within Terraform configuration.

Think:

```text
resource type = what kind of thing?
local name    = what do I call this instance in my code?
```

### 3.3 State: Terraform's map to the real world

Terraform needs to remember which real cloud object corresponds to which resource in the configuration.

The source introduces:

```text
terraform.tfstate
```

as the state file.

Conceptually:

```text
Terraform code

aws_s3_bucket.my_bucket
          |
          | mapped through state
          v
Real AWS S3 bucket
my-unique-devops-book-bucket-98765
```

This mapping allows Terraform to reason about existing managed infrastructure.

### Why state matters

The source highlights three purposes.

#### Mapping

Terraform needs to know which real resource corresponds to which declared resource.

#### Performance

State helps Terraform avoid treating every run as if nothing exists.

#### Planning

Terraform uses state while comparing current and desired infrastructure to determine what should change.

[[IMAGE_NEEDED: Terraform code-state-cloud relationship | A three-part diagram showing HCL configuration on the left, `terraform.tfstate` in the middle as the mapping layer, and real AWS resources on the right | Learner should notice that state connects Terraform resource addresses in code to real infrastructure objects]]

---

## 4. State safety and remote backends

The state file is important, but the source also treats it as sensitive.

It can contain infrastructure details and may contain sensitive values.

Therefore, the source explicitly says:

> Do not commit Terraform state files to Git.

### `.gitignore`

The chapter recommends adding at least:

```text
.terraform/
*.tfstate
*.tfstate.backup
```

to `.gitignore`.

Why?

#### `.terraform/`

This directory contains downloaded provider data.

It can be recreated with:

```bash
terraform init
```

so it does not need to be stored in source control.

#### `*.tfstate`

These files contain Terraform state.

They should not be committed.

### Remote backend

For real team projects, the source recommends storing state remotely rather than only in a local file.

It gives an S3 backend example:

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}
```

The source connects remote state with:

- centralized state storage,
- safer team collaboration,
- state locking to avoid simultaneous conflicting Terraform operations.

The important beginner idea is:

```text
Configuration belongs in Git.
State should be managed separately and securely.
```

Do not confuse these two artifacts.

### Configuration versus state

| Artifact | Purpose |
|---|---|
| `.tf` files | Describe desired infrastructure |
| `terraform.tfstate` | Tracks Terraform's mapping to managed real infrastructure |
| `.terraform/` | Local downloaded provider/project data |

---

## 5. Set up Terraform and your first AWS project

The source now moves from concepts to practice.

### 5.1 Install Terraform

The chapter's installation flow is:

1. Download Terraform for your operating system and architecture.
2. Unzip the archive.
3. Put the executable somewhere in your system `PATH`.
4. Open a new terminal.
5. Verify:

```bash
terraform -version
```

If the command prints a Terraform version, the executable is available.

### 5.2 Create the project directory

The source uses:

```bash
cd ~/devops-book-projects
mkdir terraform-s3-bucket
cd terraform-s3-bucket
```

This directory will contain the Terraform configuration.

### 5.3 Configure AWS credentials

The source uses AWS for the hands-on example.

It presents two local-development approaches:

#### Environment variables

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

#### AWS CLI

```bash
aws configure
```

The source explains that Terraform can read AWS credentials configured by the AWS CLI.

The chapter's AWS exercise uses credentials with access to S3.

### Important credential boundary

The configuration file should describe infrastructure.

Credentials should not be embedded into `main.tf`.

The source keeps credentials separate and also warns against committing sensitive Terraform state.

### 5.4 Create `main.tf`

The source example is:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-devops-book-bucket-98765"

  tags = {
    Name      = "My DevOps Book Bucket"
    ManagedBy = "Terraform"
  }
}
```

Let's read it from top to bottom.

### Required provider

```hcl
required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "~> 4.0"
  }
}
```

This tells Terraform that the project requires the AWS provider.

### Provider configuration

```hcl
provider "aws" {
  region = "us-east-1"
}
```

This configures the AWS provider to work in the specified region.

### Resource declaration

```hcl
resource "aws_s3_bucket" "my_bucket"
```

declares one AWS S3 bucket resource.

### Globally unique bucket name

The source explicitly warns that S3 bucket names must be globally unique.

Therefore, this value:

```hcl
bucket = "my-unique-devops-book-bucket-98765"
```

must be changed if it is already taken.

### Tags

The source example adds:

```hcl
tags = {
  Name      = "My DevOps Book Bucket"
  ManagedBy = "Terraform"
}
```

Tags attach descriptive metadata to the resource.

{{exercise:M04.L01.EX02}}

---

## 6. The core Terraform workflow: init, plan, apply

The most important operational workflow in the chapter is:

```text
terraform init
      ↓
terraform plan
      ↓
terraform apply
```

Each command has a distinct purpose.

### 6.1 `terraform init`

Run:

```bash
terraform init
```

This initializes the project.

The source explains that Terraform:

- reads the configuration,
- identifies required providers,
- downloads the required provider plugins,
- stores provider data in `.terraform/`.

You typically run `init`:

- when starting a new Terraform project,
- when adding or changing providers.

### 6.2 `terraform plan`

Run:

```bash
terraform plan
```

This is the chapter's most important safety step.

The command previews what Terraform **would** do.

It does not make the changes yet.

Terraform compares:

```text
desired configuration
        +
known/current state
        ↓
execution plan
```

### Plan symbols

The source uses:

```text
+  create
-  destroy
~  modify in place
```

Always review the plan before applying.

The plan is your opportunity to ask:

- Is Terraform creating what I expect?
- Is it trying to destroy something unexpectedly?
- Is the replacement or modification intentional?

### 6.3 `terraform apply`

Once the plan is acceptable:

```bash
terraform apply
```

Terraform shows the plan again and asks for confirmation.

The source instructs the learner to type:

```text
yes
```

to continue.

Terraform then makes the provider API calls required to reach the desired state.

For this lesson, that means creating the S3 bucket.

After the apply completes, a local:

```text
terraform.tfstate
```

file exists and maps the Terraform resource to the real S3 bucket.

{{image:terraform-state-flow}}

---

## 7. Drift detection, pull-request plans, and destroy

Terraform is not only for creating resources.

The source also shows how Terraform helps maintain and remove infrastructure.

### 7.1 Configuration drift

Suppose the Terraform code describes one configuration, but someone changes the real infrastructure manually.

Now:

```text
Terraform code
      ≠
real infrastructure
```

That difference is **configuration drift**.

The source explains that:

```bash
terraform plan
```

can detect this mismatch.

Terraform may propose:

```text
~ modify
```

or:

```text
-/+ replace
```

depending on the change.

The declarative idea is:

> The code represents the desired state, and Terraform plans changes that move reality back toward that state.

### 7.2 Terraform plan in pull requests

The source extends the idea into team workflows.

In professional teams, a CI system can run:

```bash
terraform plan
```

when an infrastructure pull request is opened.

Then reviewers can inspect the proposed infrastructure change before it is applied.

Conceptually:

```text
Infrastructure code change
        ↓
Pull Request
        ↓
terraform plan
        ↓
Review proposed resources
        ↓
Approve or revise
```

This connects the Git collaboration model from earlier lessons directly to infrastructure changes.

### 7.3 Destroy managed infrastructure

The source uses:

```bash
terraform destroy
```

to remove resources Terraform manages.

Terraform first shows the destruction plan and requests confirmation.

For a practice environment, this is important because leaving cloud resources running may create unnecessary cost.

The source emphasizes that IaC makes teardown easy.

Conceptually:

```text
terraform apply
    ↓
resources exist

terraform destroy
    ↓
managed resources removed
```

### Why destroy matters conceptually

IaC is not only:

> "Create infrastructure faster."

It is also:

> "Manage the entire infrastructure lifecycle through code."

That includes:

- create,
- modify,
- replace,
- destroy.

{{exercise:M04.L01.EX03}}

---

## 8. Variables: remove hardcoded values

The first configuration hardcodes values such as:

```hcl
region = "us-east-1"
```

and:

```hcl
bucket = "my-unique-devops-book-bucket-98765"
```

That works for one experiment, but it reduces reuse.

Terraform input variables let values come from outside the main resource definition.

### Create `variables.tf`

The source defines:

```hcl
variable "aws_region" {
  description = "The AWS region to create resources in."
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
}
```

Notice the difference.

### Variable with default

```hcl
variable "aws_region"
```

contains:

```hcl
default = "us-east-1"
```

so Terraform already has a value if none is supplied.

### Required variable

```hcl
variable "bucket_name"
```

has no default.

Therefore, Terraform needs a value from another source.

### Reference a variable

Use:

```hcl
var.aws_region
```

or:

```hcl
var.bucket_name
```

For example:

```hcl
provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
}
```

### `terraform.tfvars`

The source uses:

```hcl
bucket_name = "my-super-unique-bucket-from-a-variable"
```

in:

```text
terraform.tfvars
```

Terraform automatically loads this file in the workflow described by the chapter.

### Why variables matter

Instead of rewriting infrastructure logic for each environment, you can separate:

```text
infrastructure structure
```

from:

```text
environment-specific values
```

Conceptually:

```text
main.tf
defines what exists

variables.tf
defines configurable inputs

terraform.tfvars
provides concrete values
```

This makes the configuration more reusable.

---

## 9. Outputs: expose useful information from managed resources

After Terraform creates infrastructure, you often want to display useful values.

The source uses an S3 bucket ARN as the example.

Create:

```text
outputs.tf
```

with:

```hcl
output "s3_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.my_bucket.arn
}
```

### Read the reference

```hcl
aws_s3_bucket.my_bucket.arn
```

can be read as:

```text
resource type
      .
local resource name
      .
attribute
```

So:

```text
aws_s3_bucket
    = resource type

my_bucket
    = local Terraform name

arn
    = attribute returned for that resource
```

### After `terraform apply`

The source explains that Terraform displays an **Outputs** section containing the value.

### Inputs and outputs together

Variables move information **into** the configuration.

Outputs expose selected information **from** the resulting infrastructure.

```text
Input variables
      ↓
Terraform configuration
      ↓
Managed infrastructure
      ↓
Output values
```

[[IMAGE_NEEDED: Terraform variables and outputs | A diagram showing `terraform.tfvars` and input variables feeding into `main.tf`, Terraform creating an S3 bucket, then an output block exposing the bucket ARN | Learner should notice that variables parameterize configuration while outputs expose useful resource attributes]]

{{exercise:M04.L01.EX04}}

---

## Important misconceptions

### Misconception 1

> "Infrastructure as Code just means saving screenshots of cloud settings."

### Why this is wrong

IaC uses machine-readable configuration to define and manage infrastructure.

The value comes from automation, repeatability, version control, and review.

---

### Misconception 2

> "Terraform is imperative because I run commands in order."

### Why this is wrong

The CLI workflow uses commands such as `init`, `plan`, and `apply`, but the infrastructure configuration itself is declarative in the source's framing.

You describe the desired infrastructure state.

---

### Misconception 3

> "`terraform plan` changes my AWS account."

### Why this is wrong

The source presents `plan` as a preview.

`terraform apply` is the command that executes real infrastructure changes.

---

### Misconception 4

> "The Terraform state file is just another source file that belongs in Git."

### Why this is wrong

The source explicitly warns against committing state.

State tracks real infrastructure mappings and can contain sensitive details.

---

### Misconception 5

> "If someone changes the infrastructure manually, Terraform can no longer help."

### Why this is wrong

The source explains that `terraform plan` can detect configuration drift between the declared desired state and real infrastructure.

---

### Misconception 6

> "Variables are only for secret values."

### Why this is wrong

The chapter uses variables for ordinary reusable configuration such as:

- region,
- bucket name.

Variables are primarily about parameterization and reuse.

---

### Misconception 7

> "Outputs create new cloud resources."

### Why this is wrong

Outputs expose values from Terraform-managed resources after apply.

They do not create the resource by themselves.

---

## Key terminology

| Term | Meaning |
|---|---|
| Infrastructure as Code (IaC) | Practice of managing infrastructure through machine-readable configuration files |
| Click-ops | Manual infrastructure management through interactive consoles and configuration screens |
| Configuration drift | Difference between declared or expected infrastructure and its real current configuration |
| Declarative IaC | Describing the desired end state and letting the tool determine required actions |
| Imperative IaC | Describing the explicit steps required to reach a target state |
| Terraform | Declarative Infrastructure as Code tool introduced in the chapter |
| HCL | HashiCorp Configuration Language |
| Provider | Terraform plugin that communicates with an external platform API |
| Resource | Terraform block representing an infrastructure object |
| Resource type | Provider-defined infrastructure type such as `aws_s3_bucket` |
| Local name | Terraform name used to refer to a resource inside configuration |
| State | Terraform's stored mapping between configuration and managed real resources |
| `terraform.tfstate` | Default local Terraform state file |
| Backend | Location/mechanism used to store Terraform state |
| `.terraform/` | Project directory containing downloaded Terraform provider data |
| `terraform init` | Initializes a Terraform project and downloads required providers |
| `terraform plan` | Previews proposed infrastructure changes |
| `terraform apply` | Executes planned changes against the provider |
| `terraform destroy` | Plans and removes Terraform-managed infrastructure |
| Input variable | Parameter supplied to Terraform configuration |
| `terraform.tfvars` | File used in the chapter to provide variable values |
| Output value | Value exposed by Terraform after evaluating managed resources |
| ARN | Amazon Resource Name; used in the chapter as an example output attribute |

---

## Self-check

Before continuing, make sure you can answer:

1. What problem does Infrastructure as Code solve?
2. Why can click-ops create configuration drift?
3. What is the difference between imperative and declarative IaC?
4. Why is Terraform described as declarative?
5. What does a Terraform provider do?
6. What is the difference between a resource type and local resource name?
7. Why does Terraform need state?
8. Why should `terraform.tfstate` not be committed to Git?
9. Why is `.terraform/` excluded from version control in the source workflow?
10. What does a remote backend solve conceptually?
11. What does `terraform init` do?
12. What does `terraform plan` do?
13. What do `+`, `-`, and `~` mean in the plan described by the chapter?
14. What does `terraform apply` do?
15. How can Terraform detect drift?
16. Why might a team run Terraform plan in a pull request?
17. What does `terraform destroy` do?
18. Why are variables better than hardcoding every environment-specific value?
19. What is the difference between a variable with and without a default?
20. What role does `terraform.tfvars` play?
21. What does `aws_s3_bucket.my_bucket.arn` refer to?
22. What is the difference between an input variable and an output value?
23. How does Terraform connect to the previous Git and Docker lessons?

---

## Retain this idea

**Terraform lets you treat infrastructure as a desired, version-controlled state: define it in code, preview the difference, apply the change, track the result in state, and parameterize the configuration for reuse.**
""",

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "what-is-iac",
                "title": "Infrastructure as Code: managing infrastructure like software",
                "order": 1,
            },
            {
                "id": "declarative-imperative",
                "title": "Declarative versus imperative infrastructure",
                "order": 2,
            },
            {
                "id": "terraform-core",
                "title": "Terraform fundamentals: providers, resources, and state",
                "order": 3,
            },
            {
                "id": "state-safety",
                "title": "State safety and remote backends",
                "order": 4,
            },
            {
                "id": "terraform-setup",
                "title": "Set up Terraform and your first AWS project",
                "order": 5,
            },
            {
                "id": "terraform-workflow",
                "title": "The core Terraform workflow: init, plan, apply",
                "order": 6,
            },
            {
                "id": "drift-destroy",
                "title": "Drift detection, pull-request plans, and destroy",
                "order": 7,
            },
            {
                "id": "variables",
                "title": "Variables: remove hardcoded values",
                "order": 8,
            },
            {
                "id": "outputs",
                "title": "Outputs: expose useful information from managed resources",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Convert Click-Ops into Declarative IaC",

            "lesson_code": "M04.L01",

            "section_id": "declarative-imperative",

            "placement": "after_section",

            "description": (
                "Practice translating a manual infrastructure procedure into a "
                "desired-state description."
            ),

            "instructions": (
                "Scenario: an engineer manually creates a storage bucket, chooses a region, "
                "adds two tags, and repeats the same process for three environments.\n"
                "1. Identify at least three weaknesses of the manual workflow using ideas from the lesson.\n"
                "2. Rewrite the process as an imperative description using ordered steps.\n"
                "3. Rewrite the same requirement as a declarative desired-state description.\n"
                "4. Explain why the declarative version is easier to reuse and review in Git."
            ),

            "expected_output": (
                "A short comparison containing the click-ops weaknesses, one imperative "
                "version, one declarative version, and a reuse/review explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "iac",
                "click-ops",
                "declarative",
                "imperative",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Read and Explain Your First Terraform Configuration",

            "lesson_code": "M04.L01",

            "section_id": "terraform-setup",

            "placement": "after_section",

            "description": (
                "Build the chapter's first Terraform project and explain the role "
                "of each provider and resource declaration."
            ),

            "instructions": (
                "1. Create a terraform-s3-bucket project directory.\n"
                "2. Create main.tf using the lesson's AWS provider and S3 resource example.\n"
                "3. Replace the example bucket name with a unique value.\n"
                "4. Create .gitignore containing .terraform/, *.tfstate, and *.tfstate.backup.\n"
                "5. For each major block in main.tf, explain what Terraform learns from it.\n"
                "6. Identify the provider source, provider region, resource type, local resource name, bucket name, and tags.\n"
                "7. Explain why credentials are configured separately from the infrastructure definition."
            ),

            "expected_output": (
                "A valid beginner Terraform project layout plus a structured explanation "
                "of the required provider, provider configuration, and S3 resource."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "hcl",
                "terraform-provider",
                "terraform-resource",
                "gitignore",
            ],
        },

        {
            "id": "M04.L01.EX03",

            "title": "Run the Terraform Lifecycle Safely",

            "lesson_code": "M04.L01",

            "section_id": "drift-destroy",

            "placement": "after_section",

            "description": (
                "Practice the init-plan-apply-destroy workflow and interpret Terraform's "
                "planned actions before they affect real infrastructure."
            ),

            "instructions": (
                "1. Run terraform init and record what it downloads or initializes.\n"
                "2. Run terraform plan before creating the bucket.\n"
                "3. Identify the action Terraform proposes and the symbol used for it.\n"
                "4. Run terraform apply and review the plan again before confirming.\n"
                "5. Verify that terraform.tfstate now exists locally.\n"
                "6. Change one non-sensitive configuration value such as a tag and run terraform plan again.\n"
                "7. Record whether Terraform proposes creation, destruction, or modification.\n"
                "8. Run terraform destroy when the exercise is complete and review its destruction plan before confirming.\n"
                "9. Explain why plan review is important before both apply and destroy."
            ),

            "expected_output": (
                "A short execution log showing init, plan, apply, a follow-up plan, and destroy, "
                "with explanations of the symbols and decisions at each stage."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "terraform-init",
                "terraform-plan",
                "terraform-apply",
                "terraform-destroy",
                "terraform-state",
            ],
        },

        {
            "id": "M04.L01.EX04",

            "title": "Refactor Hardcoded Terraform into Variables and Outputs",

            "lesson_code": "M04.L01",

            "section_id": "outputs",

            "placement": "after_section",

            "description": (
                "Practice making a Terraform configuration reusable by moving values into "
                "input variables and exposing a useful resource attribute as an output."
            ),

            "instructions": (
                "1. Create variables.tf containing aws_region with the chapter's default and bucket_name without a default.\n"
                "2. Update main.tf to use var.aws_region and var.bucket_name.\n"
                "3. Create terraform.tfvars and provide a unique bucket_name value.\n"
                "4. Create outputs.tf with the s3_bucket_arn output from the lesson.\n"
                "5. Run terraform plan and explain where each variable value comes from.\n"
                "6. Run terraform apply and record the output value shown after completion.\n"
                "7. Explain the difference between an input variable and an output value.\n"
                "8. Explain how the same Terraform structure could be reused with different values."
            ),

            "expected_output": (
                "A refactored Terraform project containing main.tf, variables.tf, "
                "terraform.tfvars, and outputs.tf, plus a short explanation of data flow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "terraform-variables",
                "tfvars",
                "terraform-outputs",
                "reusability",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Introduction to Infrastructure as Code with Terraform — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",

                "section_id": "what-is-iac",

                "question": (
                    "Which statement best describes Infrastructure as Code in this lesson?"
                ),

                "options": [
                    "Manually documenting cloud screenshots",
                    "Managing infrastructure through machine-readable configuration instead of repeated manual setup",
                    "Running Docker containers without cloud resources",
                    "Using Git only for application source code",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter defines IaC as managing and provisioning infrastructure through "
                    "machine-readable definitions rather than manual interactive configuration."
                ),
            },

            {
                "id": "M04.L01.Q02",

                "section_id": "declarative-imperative",

                "question": (
                    "What does a declarative Terraform configuration primarily describe?"
                ),

                "options": [
                    "The exact click sequence in the AWS console",
                    "The desired final infrastructure state",
                    "Only the credentials needed to access AWS",
                    "A list of shell commands that must be executed manually",
                ],

                "correct": 1,

                "explanation": (
                    "The source presents Terraform as declarative: you describe what infrastructure "
                    "should exist, and Terraform determines the actions needed."
                ),
            },

            {
                "id": "M04.L01.Q03",

                "section_id": "terraform-core",

                "question": (
                    "What is the primary role of a Terraform provider?"
                ),

                "options": [
                    "Store Git commit history",
                    "Understand and communicate with an external platform API",
                    "Replace the Terraform state file",
                    "Automatically create variables.tf",
                ],

                "correct": 1,

                "explanation": (
                    "Providers are the plugins through which Terraform understands and interacts "
                    "with platforms such as AWS, Azure, GCP, GitHub, or Docker."
                ),
            },

            {
                "id": "M04.L01.Q04",

                "section_id": "terraform-core",

                "question": (
                    "In resource \"aws_s3_bucket\" \"app_bucket\", what is app_bucket?"
                ),

                "options": [
                    "The AWS provider version",
                    "The globally unique S3 bucket name",
                    "The local Terraform name for that resource",
                    "The backend name",
                ],

                "correct": 2,

                "explanation": (
                    "`aws_s3_bucket` is the resource type, while `app_bucket` is the local name "
                    "used inside the Terraform configuration."
                ),
            },

            {
                "id": "M04.L01.Q05",

                "section_id": "state-safety",

                "question": (
                    "Why does the source say terraform.tfstate should not be committed to Git?"
                ),

                "options": [
                    "Because Terraform cannot read state files after a commit",
                    "Because state can contain infrastructure details and sensitive information",
                    "Because state files are only used by Docker",
                    "Because state files contain no useful information",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter explicitly treats the state file as sensitive and recommends "
                    "keeping it out of Git."
                ),
            },

            {
                "id": "M04.L01.Q06",

                "section_id": "terraform-workflow",

                "question": (
                    "What does terraform init primarily do in the workflow taught here?"
                ),

                "options": [
                    "Destroy all managed resources",
                    "Initialize the project and download required provider plugins",
                    "Create variables automatically",
                    "Upload state to GitHub",
                ],

                "correct": 1,

                "explanation": (
                    "`terraform init` prepares the project and installs the providers declared "
                    "in the configuration."
                ),
            },

            {
                "id": "M04.L01.Q07",

                "section_id": "terraform-workflow",

                "question": (
                    "Which command previews infrastructure changes without applying them?"
                ),

                "options": [
                    "terraform init",
                    "terraform plan",
                    "terraform apply",
                    "terraform destroy",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes `terraform plan` as the major safety preview step."
                ),
            },

            {
                "id": "M04.L01.Q08",

                "section_id": "terraform-workflow",

                "question": (
                    "What does the ~ symbol represent in the plan description from the chapter?"
                ),

                "options": [
                    "Create a resource",
                    "Destroy a resource",
                    "Modify a resource in place",
                    "Ignore the resource",
                ],

                "correct": 2,

                "explanation": (
                    "The chapter associates `~` with an in-place modification."
                ),
            },

            {
                "id": "M04.L01.Q09",

                "section_id": "drift-destroy",

                "question": (
                    "What is configuration drift?"
                ),

                "options": [
                    "A difference between the declared desired infrastructure and the real infrastructure state",
                    "A difference between two Git commit messages",
                    "A Docker image changing registries",
                    "A Terraform provider download failing",
                ],

                "correct": 0,

                "explanation": (
                    "Drift occurs when the real infrastructure no longer matches the configuration "
                    "that is supposed to describe it."
                ),
            },

            {
                "id": "M04.L01.Q10",

                "section_id": "drift-destroy",

                "question": (
                    "Why might a team run terraform plan automatically on an infrastructure pull request?"
                ),

                "options": [
                    "To hide infrastructure changes from reviewers",
                    "To show reviewers what resources would be created, modified, or destroyed before applying changes",
                    "To replace Git branching",
                    "To avoid using Terraform state",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes Terraform plan output as a reviewable preview that can be "
                    "attached to pull-request workflows."
                ),
            },

            {
                "id": "M04.L01.Q11",

                "section_id": "variables",

                "question": (
                    "What is the key difference between aws_region and bucket_name in the chapter's variables.tf example?"
                ),

                "options": [
                    "bucket_name is a number while aws_region is a string",
                    "aws_region has a default while bucket_name requires a supplied value",
                    "bucket_name is an output, not a variable",
                    "aws_region can only be used in outputs.tf",
                ],

                "correct": 1,

                "explanation": (
                    "The region variable has a default value, while bucket_name has no default "
                    "and therefore needs a value from elsewhere."
                ),
            },

            {
                "id": "M04.L01.Q12",

                "section_id": "outputs",

                "question": (
                    "What does aws_s3_bucket.my_bucket.arn refer to?"
                ),

                "options": [
                    "The ARN attribute of the Terraform resource named my_bucket",
                    "The AWS provider version",
                    "The Terraform backend key",
                    "The environment variable containing AWS credentials",
                ],

                "correct": 0,

                "explanation": (
                    "The expression selects the `arn` attribute from the managed S3 bucket resource "
                    "whose local Terraform name is `my_bucket`."
                ),
            },

            {
                "id": "M04.L01.Q13",

                "section_id": "outputs",

                "type": "open",

                "question": (
                    "Describe the complete Terraform workflow for the S3 example from project setup "
                    "through init, plan, apply, state creation, variable refactoring, output display, "
                    "and final destroy. Explain the role of each major artifact and command."
                ),
            },
        ],

        "passing_score": 70,
    },
}
