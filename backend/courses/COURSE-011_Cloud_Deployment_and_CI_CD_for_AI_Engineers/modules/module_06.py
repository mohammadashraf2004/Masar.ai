"""M06.L01 — Container Orchestration with Kubernetes.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 8, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "Container Orchestration with Kubernetes"

MODULE_DESCRIPTION = (
    "Move from running individual Docker containers to orchestrating resilient, "
    "scalable applications with Kubernetes. Learn clusters, Nodes, Pods, Deployments, "
    "Services, minikube, kubectl, declarative manifests, scaling, rollouts, and Helm."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Container Orchestration with Kubernetes",

    "slug": "container-orchestration-kubernetes-m06-l01",

    "description": (
        "Understand why container orchestration is required beyond single-container "
        "Docker workflows, then deploy and manage a containerized application using "
        "Kubernetes primitives, declarative YAML, local minikube, kubectl, and Helm."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "kubernetes",
        "k8s",
        "container-orchestration",
        "pods",
        "deployments",
        "services",
        "nodes",
        "kubectl",
        "minikube",
        "helm",
    ],

    "prerequisite_ids": ["M05.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Container Orchestration with Kubernetes",

        "content": r"""
# Container Orchestration with Kubernetes

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M06.L01  
> **Module:** Container Orchestration with Kubernetes  
> **Source alignment:** BOOK-XXX, Chapter 8. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why Docker alone is not enough for operating many containers at scale.
- Define container orchestration and describe the "Day 2" problems Kubernetes solves.
- Explain Kubernetes as a cluster-level management platform.
- Distinguish the roles of the control plane and Nodes.
- Explain why Pods are Kubernetes' smallest deployable unit.
- Describe how Deployments maintain desired state through reconciliation.
- Explain why Services are required when Pods are ephemeral.
- Install and use `kubectl` and minikube for a local cluster workflow.
- Read and explain a Deployment manifest.
- Read and explain a Service manifest.
- Use labels and selectors to connect Services to Pods.
- Explain `port`, `targetPort`, and `NodePort`.
- Apply manifests declaratively with `kubectl apply`.
- Inspect Deployments, Pods, and Services.
- Scale a Deployment live.
- Explain Kubernetes rolling updates and rollback.
- Describe the traffic path from NodePort to Service to Pod.
- Explain the purpose of ConfigMaps, Secrets, probes, and resource requests/limits as production-oriented extensions introduced by the source.
- Explain why Helm becomes useful as Kubernetes application configuration grows.
- Distinguish Helm Charts, repositories, releases, templates, and `values.yaml`.

---

## 1. Why orchestration becomes necessary

Docker solves a major problem:

> Package an application and its dependencies into a portable container.

That is powerful when you have one container.

But production systems usually grow beyond that.

Imagine an e-commerce platform with:

```text
frontend
user API
product API
payment service
database
cache
background workers
monitoring agents
```

Now imagine several replicas of each.

The problem is no longer:

> "Can I start a container?"

The problem becomes:

> **"How do I keep many containers healthy, connected, scaled, and updated over time?"**

The source describes this as the **Day 2 problem**.

Day 1:

```text
Run the application.
```

Day 2:

```text
Keep it running reliably.
Scale it.
Update it.
Recover from failures.
Connect services.
```

### Four major operational problems

The chapter frames orchestration through four practical questions.

### Resilience

What happens if:

- a container crashes,
- a server fails,
- a process becomes unhealthy?

Without orchestration, someone may need to notice and restart workloads manually.

At production scale, that is not acceptable.

### Scalability

Suppose traffic suddenly increases.

You may need:

```text
2 containers
→ 10 containers
→ 30 containers
```

Then, when demand falls:

```text
30
→ 5
```

Doing that manually is slow and expensive.

### Networking

Containers are dynamic.

Addresses can change when instances restart.

Hardcoding:

```text
10.0.0.23
```

into another service is fragile.

Applications need stable service discovery.

### Updates

Production software changes constantly.

You need to answer:

- How do I deploy a new image without downtime?
- How do I replace containers gradually?
- How do I roll back if the new version is bad?

### Container orchestration

A **container orchestrator** automates these operational concerns.

The source defines Kubernetes as the dominant orchestration platform for this job.

A useful mental model is:

```text
Docker
= package and run a container

Kubernetes
= coordinate many containers across a cluster
```

[[IMAGE_NEEDED: From Docker container to Kubernetes orchestration | A progression diagram showing one Docker container on a laptop, then many containers across multiple servers, followed by Kubernetes managing placement, health, networking, scaling, and updates | Learner should notice that orchestration solves lifecycle and scale problems that appear after containerization]]

---

## 2. Kubernetes as a cluster operating platform

**Kubernetes**, commonly abbreviated **K8s**, is an open-source orchestration platform originally designed by Google and maintained within the Cloud Native Computing Foundation ecosystem.

The source uses a powerful analogy:

> Kubernetes is like an operating system for a data center or cluster.

A normal operating system manages resources on one machine:

```text
CPU
memory
storage
processes
```

Kubernetes manages resources across many machines.

Instead of thinking:

```text
"Run this on server-2."
```

you describe:

```text
"I need five copies of this application."
```

Kubernetes then decides where to place them.

### Declarative control

You tell Kubernetes what you want.

Example:

```text
Desired state:
5 web application replicas
```

Kubernetes continuously works toward that state.

This is similar to the declarative Terraform mental model from the previous lesson.

You declare:

```text
what should exist
```

and the control system handles:

```text
how to reconcile reality with that declaration
```

### Capabilities emphasized in the source

#### Self-healing

If a workload fails, Kubernetes can replace it.

If a Node becomes unavailable, workloads can be rescheduled.

#### Horizontal scaling

You can increase or decrease replicas.

The source also mentions autoscaling based on metrics such as CPU usage.

#### Service discovery and load balancing

Kubernetes gives applications stable names and can distribute traffic across replicas.

#### Automated rollouts and rollbacks

New versions can be introduced gradually.

If something goes wrong, a previous version can be restored.

#### Secret and configuration management

The source introduces Kubernetes mechanisms for keeping configuration and sensitive values separate from the application image.

### The core Kubernetes idea

```text
You declare desired application state.
Kubernetes continually tries to make actual state match it.
```

That sentence will explain many Kubernetes behaviors later in the lesson.

---

## 3. Cluster architecture: control plane and Nodes

A running Kubernetes environment is called a **cluster**.

The source describes the cluster as a group of networked computers called **Nodes**.

### Nodes

A **Node** is a worker machine.

It can be:

- a cloud virtual machine,
- a physical server,
- a local machine abstraction in a development cluster.

Nodes are where application workloads run.

Think:

```text
Node = worker
```

### Control plane

The **control plane** is the management brain.

It is responsible for the cluster's desired state and global decisions.

The source emphasizes responsibilities such as:

- scheduling workloads,
- observing cluster state,
- responding to events.

Think:

```text
Control plane = manager
Nodes         = workers
```

### Simplified architecture

```text
                Kubernetes API
                     |
                     v
               Control Plane
                     |
        -----------------------------
        |             |             |
        v             v             v
      Node 1        Node 2        Node 3
        |             |             |
   application    application    application
    workloads      workloads      workloads
```

You usually interact through the Kubernetes API using:

```bash
kubectl
```

rather than manually assigning work to individual Nodes.

[[IMAGE_NEEDED: Kubernetes cluster architecture | A diagram with the control plane at the top connected through the Kubernetes API to three worker Nodes below, each running Pods | Learner should notice that the control plane manages desired state while Nodes run workloads]]

---

## 4. Pods: Kubernetes' smallest deployable unit

Docker teaches you to think in containers.

Kubernetes adds one more abstraction:

> **Pod**

A **Pod** is Kubernetes' smallest deployable object.

Kubernetes normally manages Pods rather than individual containers directly.

### What is inside a Pod?

A Pod can contain:

```text
one container
```

or:

```text
multiple tightly coupled containers
```

Most beginner application Pods contain one main application container.

### Why have a Pod wrapper?

The source explains that containers inside one Pod:

- run on the same Node,
- share a network namespace,
- can communicate over `localhost`,
- can share storage volumes.

This is useful for tightly coupled containers.

For example:

```text
Pod
├── main application container
└── sidecar logging container
```

### Pod lifetime

A critical concept:

> Pods are ephemeral.

They can be:

- created,
- destroyed,
- replaced.

Their IP addresses are therefore not stable enough to be used as long-term application endpoints.

### Do not manage application Pods directly

The source emphasizes:

> You almost never create Pods directly for normal application management.

Instead, use a higher-level controller such as a **Deployment**.

That controller creates and replaces Pods for you.

---

## 5. Deployments and the reconciliation loop

A **Deployment** manages a desired set of application Pods.

Suppose you declare:

```text
replicas = 3
```

The desired state is:

```text
3 Pods
```

But the cluster currently has:

```text
0 Pods
```

Kubernetes notices:

```text
desired = 3
actual  = 0
```

and creates three Pods.

Now suppose one Pod crashes.

Actual state becomes:

```text
2
```

Desired state remains:

```text
3
```

The Deployment controller creates another Pod.

This continuous comparison is the **reconciliation loop**.

### Reconciliation mental model

```text
Desired state
    3 Pods
      |
      v
Compare
      |
      v
Actual state
    2 Pods
      |
      v
Difference
   missing 1
      |
      v
Create replacement
```

[[IMAGE_NEEDED: Kubernetes reconciliation loop | A circular diagram showing desired state = 3 Pods, actual state = 2 Pods, controller detects difference, creates replacement Pod, actual state returns to 3 | Learner should notice that self-healing comes from continuous desired-vs-actual reconciliation]]

### Deployments provide more than replication

The source also introduces Deployments as the object used for:

- rolling updates,
- maintaining availability,
- replacing failed Pods.

So a Deployment is not merely:

> "create three Pods"

It is:

> **continuously manage the application's declared Pod state.**

---

## 6. Services: stable networking for unstable Pods

Pods are replaceable.

Their addresses are not stable.

So another application should not depend directly on one Pod's IP.

That is what a **Service** solves.

### Stable endpoint

A Service provides a stable networking abstraction over a logical group of Pods.

Think:

```text
Client
  |
  v
Service
  |
  +--> Pod A
  +--> Pod B
  +--> Pod C
```

The client communicates with the Service.

The Service routes traffic to healthy matching Pods.

### Labels and selectors

How does the Service know which Pods belong to it?

Using **labels**.

Example Pod label:

```yaml
app: flask-app
```

Example Service selector:

```yaml
selector:
  app: flask-app
```

That creates the connection.

### Front-desk analogy

The source compares a Service to a company's front desk.

You do not need to know every employee's changing extension.

You call one stable number.

The front desk routes you to an available person.

In Kubernetes:

```text
Service = stable front desk
Pods    = replaceable workers
```

### Why this decoupling matters

Pods can:

- restart,
- be replaced,
- scale up,
- scale down.

The Service remains the stable network layer.

{{exercise:M06.L01.EX01}}

---

## 7. Set up a local Kubernetes cluster with minikube

You do not need a cloud cluster to learn Kubernetes.

The source uses:

- Docker Desktop,
- `kubectl`,
- minikube.

### 7.1 `kubectl`

`kubectl` is the command-line client for the Kubernetes API.

It is how you ask the cluster to:

- create resources,
- inspect resources,
- scale workloads,
- update workloads.

Think:

```text
kubectl
   ↓
Kubernetes API
   ↓
Cluster
```

### 7.2 minikube

minikube runs a local Kubernetes cluster.

The source uses the Docker driver:

```bash
minikube start --driver=docker
```

This creates a single-node Kubernetes cluster inside Docker.

### Why local clusters are useful

They give you a safe place to practice:

- YAML manifests,
- Deployments,
- Services,
- scaling,
- rollout operations.

without requiring a full cloud Kubernetes setup.

### Verify the cluster

Check cluster information:

```bash
kubectl cluster-info
```

Check Nodes:

```bash
kubectl get nodes
```

The source expects one Node named:

```text
minikube
```

with status:

```text
Ready
```

### If minikube becomes unhealthy

The source gives a reset command:

```bash
minikube delete
```

then start again.

The source also discusses virtualization settings, but notes that the Docker driver can avoid some hypervisor-specific setup issues.

### Verification mindset

Do not just start the cluster and assume success.

Check:

```text
Is the API reachable?
Are Nodes registered?
Is the Node Ready?
```

That habit carries into real Kubernetes operations.

---

## 8. Deploy the Flask application with declarative YAML

Kubernetes is commonly managed declaratively through **manifest files**.

You describe the desired resources in YAML.

The source deploys the Flask application using:

1. a Deployment manifest,
2. a Service manifest.

### 8.1 Deployment manifest

The source provides:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: flask-app-deployment
  labels:
    app: flask-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: flask-app

  template:
    metadata:
      labels:
        app: flask-app

    spec:
      containers:
        - name: web-server
          image: yourdockerhubusername/simple-flask-app:1.0.0
          ports:
            - containerPort: 8080
```

Replace:

```text
yourdockerhubusername
```

with the actual Docker Hub namespace containing the image.

### Read it top to bottom

#### `apiVersion`

```yaml
apiVersion: apps/v1
```

selects the API version used for this resource kind.

#### `kind`

```yaml
kind: Deployment
```

declares the resource type.

#### `metadata`

```yaml
metadata:
  name: flask-app-deployment
```

gives the object a cluster-visible name.

### Desired replica count

```yaml
replicas: 2
```

means:

> Keep two Pod replicas running.

### Deployment selector

```yaml
selector:
  matchLabels:
    app: flask-app
```

tells the Deployment which Pods it manages.

### Pod template

```yaml
template:
```

defines the Pods the Deployment creates.

Its labels must match the selector:

```yaml
app: flask-app
```

### Container specification

```yaml
containers:
  - name: web-server
    image: yourdockerhubusername/simple-flask-app:1.0.0
```

tells Kubernetes which container image to run.

### Container port

```yaml
containerPort: 8080
```

describes the application port inside the container.

### Production-oriented additions mentioned by the source

The chapter notes that real production manifests often add:

#### Resource requests and limits

To define expected and maximum CPU/memory behavior.

#### Liveness probes

To help Kubernetes determine whether a container should be restarted.

#### Readiness probes

To determine whether a Pod should receive traffic.

#### ConfigMap-based environment configuration

To avoid hardcoding runtime configuration into the image.

These concepts are introduced as production enhancements, not fully implemented in the supplied example.

---

## 9. Create a Service and route traffic to Pods

The source Service manifest is:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: flask-app-service

spec:
  selector:
    app: flask-app

  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

  type: NodePort
```

### `kind: Service`

This creates a Service resource.

### Selector

```yaml
selector:
  app: flask-app
```

finds Pods carrying:

```yaml
app: flask-app
```

This is why label consistency is critical.

### `port`

```yaml
port: 80
```

is the Service's port inside the cluster.

### `targetPort`

```yaml
targetPort: 8080
```

is the application port on the selected Pods.

So:

```text
Service port 80
      ↓
Pod port 8080
```

### `NodePort`

```yaml
type: NodePort
```

makes the Service reachable through a port exposed on the Node.

The source notes that in cloud environments a common alternative is:

```yaml
type: LoadBalancer
```

which can ask the cloud provider to provision an external load balancer.

### Traffic path

The source explicitly describes:

```text
Browser
   ↓
NodePort on minikube Node
   ↓
flask-app-service
   ↓
healthy Pod matching app: flask-app
```

[[IMAGE_NEEDED: Kubernetes Service traffic routing | A diagram showing Browser → NodePort → Service with stable DNS/IP → two Flask Pods labeled app=flask-app, with arrows from the Service load-balancing across both Pods | Learner should notice that the Service is stable while Pods can be replaced]]

### Apply the manifests

The source intends two commands:

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

This tells Kubernetes:

> Make the cluster state match these manifests.

### Inspect resources

Deployment:

```bash
kubectl get deployments
```

Pods:

```bash
kubectl get pods
```

Services:

```bash
kubectl get services
```

### Access through minikube

```bash
minikube service flask-app-service
```

minikube finds the correct exposed URL and opens it.

{{exercise:M06.L01.EX02}}

---

## 10. Scale, update, and roll back the application

One of the most important Kubernetes benefits is that day-to-day operations can target higher-level desired state.

### Scale live

The source uses:

```bash
kubectl scale deployment flask-app-deployment --replicas=5
```

Now the desired state becomes:

```text
5 Pods
```

The Deployment controller creates additional Pods.

Then:

```bash
kubectl get pods
```

shows the new replicas.

The Service automatically includes matching healthy Pods.

### Rolling update

To move to a new image:

```bash
kubectl set image deployment/flask-app-deployment \
web-server=yourusername/simple-flask-app:2.0.0
```

Kubernetes gradually replaces old Pods with new Pods.

The source describes this as preserving availability during the update.

### Watch rollout progress

```bash
kubectl rollout status deployment/flask-app-deployment
```

This reports the progress of the rollout.

### Roll back

If the new version is unhealthy:

```bash
kubectl rollout undo deployment/flask-app-deployment
```

This restores the previous Deployment revision.

### Operational mental model

```text
Change desired image version
        ↓
Deployment begins rollout
        ↓
Old Pods gradually replaced
        ↓
Service continues routing
        ↓
Observe rollout
        ↓
Healthy?
 ┌──────┴──────┐
Yes           No
↓              ↓
Keep          Rollback
```

### This is orchestration in practice

Compare this with manually:

- starting five containers,
- assigning network ports,
- removing old containers,
- starting replacements,
- updating traffic routing,
- restoring the old version if something fails.

Kubernetes centralizes these behaviors around declarative objects and controllers.

{{exercise:M06.L01.EX03}}

---

## 11. Helm: packaging Kubernetes applications

Two YAML files are manageable.

But a real application may need:

```text
Deployment
Service
ConfigMap
Secret
Ingress
PersistentVolume
resource policies
environment-specific settings
```

Now imagine:

```text
dev
staging
production
```

Managing many separate YAML files can become repetitive and error-prone.

This is the problem the source introduces **Helm** to solve.

### Helm as a package manager

The source calls Helm:

> "the package manager for Kubernetes."

The analogy is:

```text
apt / brew
→ operating-system packages

Helm
→ Kubernetes application packages
```

### Core Helm concepts

### Chart

A **Chart** is a packaged collection of Kubernetes resource templates and supporting files.

Instead of loose YAML files:

```text
deployment.yml
service.yml
configmap.yml
secret.yml
```

you can manage them as one chart.

### Repository

A Helm **repository** stores and distributes Charts.

It is similar in purpose to software package repositories.

### Release

A **release** is one installed instance of a Chart in a cluster.

The same Chart can be installed multiple times with different release names or configuration.

### Templates and `values.yaml`

This is where Helm becomes especially useful.

The Kubernetes YAML inside a Chart can contain templates.

Configuration lives in:

```text
values.yaml
```

For example:

```text
replica count
image tag
resource limits
environment settings
```

Helm combines:

```text
templates
+
values
```

to generate final Kubernetes manifests.

[[IMAGE_NEEDED: Helm chart templating model | A diagram showing Helm Chart templates + values.yaml → Helm render/install → generated Deployment, Service, ConfigMap, and other Kubernetes resources → Kubernetes cluster | Learner should notice that the same templates can be reused with different environment-specific values]]

### Environment reuse

The same Chart can conceptually be paired with:

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

This reduces duplication.

### Public chart example

The source demonstrates adding Bitnami:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Then installing nginx:

```bash
helm install my-nginx bitnami/nginx
```

This:

1. downloads the Chart,
2. renders required manifests,
3. applies them to Kubernetes,
4. creates a Helm release named `my-nginx`.

List releases:

```bash
helm list
```

### Source-reported Airbnb case study

The supplied chapter includes an Airbnb case study describing large-scale use of Helm, including reported figures about microservice count, deployment-time reduction, configuration-error reduction, and rollback speed.

These figures are presented here only as **claims made by the supplied source**; this lesson does not independently verify them.

The educational point of the case study is:

> Standardized Helm Charts can reduce duplicated Kubernetes configuration and make repeated application deployment more consistent across environments.

{{exercise:M06.L01.EX04}}

---

## Important misconceptions

### Misconception 1

> "Kubernetes replaces Docker."

### Why this is wrong

Docker/container tooling packages and runs containers.

Kubernetes orchestrates containerized workloads across a cluster.

They solve different layers of the problem.

---

### Misconception 2

> "Kubernetes mainly exists to start containers."

### Why this is incomplete

The source emphasizes Day 2 operations:

- self-healing,
- scaling,
- networking,
- rollouts,
- rollback,
- configuration.

---

### Misconception 3

> "A Pod is exactly the same thing as a container."

### Why this is wrong

A Pod is the Kubernetes deployable wrapper around one or more containers and provides shared networking and storage context.

---

### Misconception 4

> "I should normally create application Pods directly."

### Why this is wrong

The source recommends using higher-level objects such as Deployments to manage Pods.

---

### Misconception 5

> "If a Pod crashes, the Deployment itself has failed."

### Why this is wrong

A Deployment continuously reconciles actual state against desired replica count and can create replacement Pods.

---

### Misconception 6

> "Applications should connect directly to Pod IP addresses."

### Why this is wrong

Pod addresses are ephemeral.

Services provide stable addressing and traffic distribution.

---

### Misconception 7

> "A Service selector and Deployment labels are unrelated."

### Why this is wrong

Selectors and labels create the relationship between Services, Pods, and controllers.

If they do not match, traffic or management can fail.

---

### Misconception 8

> "`port: 80` and `targetPort: 8080` describe the same endpoint."

### Why this is wrong

`port` is the Service-facing port.

`targetPort` is where the application receives traffic inside the selected Pods.

---

### Misconception 9

> "Helm is another container runtime."

### Why this is wrong

Helm packages and templates Kubernetes resource definitions.

It does not replace the runtime.

---

## Key terminology

| Term | Meaning |
|---|---|
| Container orchestration | Automated management of deployment, scaling, networking, and lifecycle of containerized applications |
| Day 2 problem | Operating an application reliably after initial deployment |
| Kubernetes / K8s | Container orchestration platform introduced in the chapter |
| Cluster | Kubernetes environment consisting of control-plane functionality and Nodes |
| Node | Worker machine that runs application workloads |
| Control plane | Management layer that maintains cluster desired state and schedules work |
| Pod | Smallest Kubernetes deployable object; contains one or more containers |
| Deployment | Higher-level object that manages replicated Pods and desired application state |
| Reconciliation loop | Continuous comparison of desired and actual state followed by corrective action |
| Service | Stable networking abstraction over a selected set of Pods |
| Label | Key-value metadata attached to Kubernetes objects |
| Selector | Rule used to identify objects by labels |
| `kubectl` | Kubernetes command-line client |
| minikube | Local Kubernetes cluster tool used in the lesson |
| Manifest | Declarative YAML definition of a Kubernetes resource |
| Replica | One managed copy of a Pod template |
| NodePort | Service type exposing a Service through a port on each Node |
| LoadBalancer | Service type commonly used in cloud environments to provision external load balancing |
| Rolling update | Gradual replacement of old Pods with a new version |
| Rollback | Returning to an earlier Deployment revision |
| ConfigMap | Kubernetes object used for non-secret configuration |
| Secret | Kubernetes object used for sensitive configuration |
| Liveness probe | Health check used to help determine whether a container should be restarted |
| Readiness probe | Check used to determine whether a Pod should receive traffic |
| Helm | Kubernetes package manager introduced in the source |
| Chart | Helm package containing templates and related files |
| Helm repository | Distribution location for Charts |
| Release | Installed instance of a Helm Chart |
| `values.yaml` | Helm configuration values used to render templates |

---

## Self-check

Before continuing, make sure you can answer:

1. What does the source mean by the "Day 2 problem"?
2. Why is running one Docker container different from operating hundreds of containers?
3. What four major problems does Kubernetes solve in the source?
4. Why does the chapter compare Kubernetes to an operating system for a cluster?
5. What is the difference between the control plane and a Node?
6. What is a Pod?
7. Why can a Pod contain multiple containers?
8. Why are Pods considered ephemeral?
9. Why should a Deployment usually manage application Pods?
10. What is a reconciliation loop?
11. What happens if desired replicas = 3 but actual replicas = 2?
12. Why is a Service needed?
13. How do labels and selectors connect Kubernetes objects?
14. What is the difference between Service `port` and `targetPort`?
15. What does `type: NodePort` do conceptually?
16. What does `kubectl apply` mean in declarative terms?
17. What should `kubectl get nodes` show after a healthy minikube setup?
18. What does `kubectl scale` change?
19. What does `kubectl set image` initiate?
20. How do you observe rollout progress?
21. What does `kubectl rollout undo` do?
22. Trace the request path from a browser through NodePort and Service to a Pod.
23. Why do production manifests commonly add resource limits and health probes?
24. What problem does Helm solve?
25. What is the difference between a Chart and a release?
26. What role does `values.yaml` play?
27. Why should the numerical Airbnb claims in the supplied case study be treated as source-reported rather than independently verified facts?

---

## Retain this idea

**Docker packages an application; Kubernetes keeps many instances of that application in the desired state by continuously managing placement, health, scale, networking, and updates.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-orchestration",
                "title": "Why orchestration becomes necessary",
                "order": 1,
            },
            {
                "id": "kubernetes-platform",
                "title": "Kubernetes as a cluster operating platform",
                "order": 2,
            },
            {
                "id": "cluster-nodes-control-plane",
                "title": "Cluster architecture: control plane and Nodes",
                "order": 3,
            },
            {
                "id": "pods",
                "title": "Pods: Kubernetes' smallest deployable unit",
                "order": 4,
            },
            {
                "id": "deployments",
                "title": "Deployments and the reconciliation loop",
                "order": 5,
            },
            {
                "id": "services",
                "title": "Services: stable networking for unstable Pods",
                "order": 6,
            },
            {
                "id": "local-cluster",
                "title": "Set up a local Kubernetes cluster with minikube",
                "order": 7,
            },
            {
                "id": "deployment-manifest",
                "title": "Deploy the Flask application with declarative YAML",
                "order": 8,
            },
            {
                "id": "service-manifest",
                "title": "Create a Service and route traffic to Pods",
                "order": 9,
            },
            {
                "id": "scale-rollout",
                "title": "Scale, update, and roll back the application",
                "order": 10,
            },
            {
                "id": "helm",
                "title": "Helm: packaging Kubernetes applications",
                "order": 11,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Map Kubernetes Objects to Responsibilities",

            "lesson_code": "M06.L01",

            "section_id": "services",

            "placement": "after_section",

            "description": (
                "Practice distinguishing the responsibilities of Nodes, Pods, "
                "Deployments, and Services."
            ),

            "instructions": (
                "For each requirement, choose the Kubernetes concept that primarily solves it "
                "and explain why:\n"
                "1. Keep three copies of the web application running.\n"
                "2. Give the frontend one stable endpoint for reaching changing backend Pods.\n"
                "3. Run the actual application container on cluster compute.\n"
                "4. Group one application container and one tightly coupled logging sidecar.\n"
                "5. Replace a failed application instance automatically.\n"
                "6. Draw a small relationship diagram: Cluster → Node → Pod → container, with a Deployment managing Pods and a Service routing traffic to them."
            ),

            "expected_output": (
                "A responsibility table plus a simple Kubernetes object relationship diagram."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "pods",
                "deployments",
                "services",
                "nodes",
                "reconciliation",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Deploy the Flask App Declaratively",

            "lesson_code": "M06.L01",

            "section_id": "service-manifest",

            "placement": "after_section",

            "description": (
                "Create the Deployment and Service manifests from the lesson and verify "
                "that Kubernetes reaches the declared state."
            ),

            "instructions": (
                "1. Start minikube with the Docker driver.\n"
                "2. Verify the cluster with kubectl cluster-info and kubectl get nodes.\n"
                "3. Create deployment.yml using 2 replicas and your Docker Hub image.\n"
                "4. Create service.yml with selector app: flask-app, port 80, targetPort 8080, and NodePort type.\n"
                "5. Before applying, identify every label and selector that must match.\n"
                "6. Apply both manifests.\n"
                "7. Inspect deployments, Pods, and Services.\n"
                "8. Use minikube service flask-app-service to access the application.\n"
                "9. Explain the full traffic route from browser to container."
            ),

            "expected_output": (
                "Two valid manifest files, evidence of 2 running replicas, a reachable Service, "
                "and a written explanation of label selection and traffic flow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "kubectl",
                "minikube",
                "deployment-yaml",
                "service-yaml",
                "labels-selectors",
            ],
        },

        {
            "id": "M06.L01.EX03",

            "title": "Scale and Roll Out a New Version",

            "lesson_code": "M06.L01",

            "section_id": "scale-rollout",

            "placement": "after_section",

            "description": (
                "Practice the Kubernetes operations that demonstrate orchestration: scaling, "
                "rolling updates, observation, and rollback."
            ),

            "instructions": (
                "1. Start from a Deployment with 2 replicas.\n"
                "2. Scale it to 5 replicas using kubectl scale.\n"
                "3. Run kubectl get pods and confirm that three new Pods appear.\n"
                "4. Explain why the Service does not need a new manually configured list of Pod IPs.\n"
                "5. Update the Deployment to a new image tag using kubectl set image.\n"
                "6. Track progress with kubectl rollout status.\n"
                "7. If testing the new image indicates a problem, run kubectl rollout undo.\n"
                "8. Explain how desired state and reconciliation are involved in both scaling and rollout."
            ),

            "expected_output": (
                "A command sequence plus a conceptual explanation linking scaling and rollout "
                "operations back to desired-state reconciliation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "kubernetes-scaling",
                "rolling-update",
                "rollback",
                "reconciliation",
            ],
        },

        {
            "id": "M06.L01.EX04",

            "title": "Design a Helm-Based Multi-Environment Configuration",

            "lesson_code": "M06.L01",

            "section_id": "helm",

            "placement": "after_section",

            "description": (
                "Practice separating reusable Kubernetes templates from environment-specific values."
            ),

            "instructions": (
                "Scenario: the Flask application must run in dev, staging, and production.\n"
                "1. List at least four Kubernetes resources that might belong in one Helm Chart.\n"
                "2. Identify which values should vary by environment, such as replica count, image tag, or resource limits.\n"
                "3. Sketch values-dev.yaml, values-staging.yaml, and values-prod.yaml conceptually.\n"
                "4. Explain why using one Chart with different values is easier to maintain than copying whole manifest folders.\n"
                "5. Distinguish a Chart, Helm repository, and release.\n"
                "6. Explain what happens conceptually when helm install renders templates with values."
            ),

            "expected_output": (
                "A reusable Chart design showing shared templates, environment-specific values, "
                "and a clear explanation of Chart/repository/release terminology."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "helm",
                "helm-charts",
                "values-yaml",
                "kubernetes-templating",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "Container Orchestration with Kubernetes — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",

                "section_id": "why-orchestration",

                "question": (
                    "What does the source mean by the Kubernetes 'Day 2 problem'?"
                ),

                "options": [
                    "Building the first Docker image",
                    "Keeping containerized applications reliable, scalable, connected, and updateable after initial deployment",
                    "Creating a Git repository on the second day of a project",
                    "Installing Docker Desktop after Kubernetes",
                ],

                "correct": 1,

                "explanation": (
                    "The Day 2 problem is operating the application over time rather than merely starting a container once."
                ),
            },

            {
                "id": "M06.L01.Q02",

                "section_id": "kubernetes-platform",

                "question": (
                    "Which Kubernetes capability automatically replaces failed workloads to restore desired state?"
                ),

                "options": [
                    "Self-healing",
                    "Docker tagging",
                    "Git branching",
                    "Helm repositories only",
                ],

                "correct": 0,

                "explanation": (
                    "The chapter identifies self-healing as Kubernetes' ability to detect failures and recreate/reschedule workloads."
                ),
            },

            {
                "id": "M06.L01.Q03",

                "section_id": "cluster-nodes-control-plane",

                "question": (
                    "What is the primary relationship between the control plane and Nodes?"
                ),

                "options": [
                    "Nodes manage the control plane's Git history",
                    "The control plane makes cluster-level decisions while Nodes run workloads",
                    "The control plane is a Docker image stored on every Node",
                    "Nodes are Services and the control plane is a Pod",
                ],

                "correct": 1,

                "explanation": (
                    "The source presents the control plane as the manager/brain and Nodes as workers."
                ),
            },

            {
                "id": "M06.L01.Q04",

                "section_id": "pods",

                "question": (
                    "What is the smallest deployable Kubernetes object introduced in the chapter?"
                ),

                "options": [
                    "Container image",
                    "Pod",
                    "Service",
                    "Helm repository",
                ],

                "correct": 1,

                "explanation": (
                    "Kubernetes manages Pods as its smallest deployable unit."
                ),
            },

            {
                "id": "M06.L01.Q05",

                "section_id": "deployments",

                "question": (
                    "A Deployment wants 3 replicas but only 2 Pods are running. What does reconciliation do?"
                ),

                "options": [
                    "Deletes the Deployment",
                    "Creates a replacement Pod to move actual state back toward 3",
                    "Changes the Service to use only one Pod",
                    "Requires a human to create a Pod manually",
                ],

                "correct": 1,

                "explanation": (
                    "The Deployment controller continuously compares desired and actual state and corrects the difference."
                ),
            },

            {
                "id": "M06.L01.Q06",

                "section_id": "services",

                "question": (
                    "Why should another application normally connect through a Service instead of directly to one Pod IP?"
                ),

                "options": [
                    "Services store Docker images",
                    "Pod IPs are ephemeral while a Service provides a stable endpoint",
                    "Pods cannot receive network traffic",
                    "Services always run on a different cloud provider",
                ],

                "correct": 1,

                "explanation": (
                    "Pods can be replaced and addresses can change, while the Service provides stable discovery and routing."
                ),
            },

            {
                "id": "M06.L01.Q07",

                "section_id": "services",

                "question": (
                    "How does a Service identify which Pods should receive its traffic?"
                ),

                "options": [
                    "Docker Hub usernames",
                    "Labels and selectors",
                    "Terraform state",
                    "Git commit hashes",
                ],

                "correct": 1,

                "explanation": (
                    "The Service selector matches labels attached to Pods."
                ),
            },

            {
                "id": "M06.L01.Q08",

                "section_id": "local-cluster",

                "question": (
                    "What is kubectl used for?"
                ),

                "options": [
                    "Building Docker images",
                    "Interacting with the Kubernetes API",
                    "Storing Helm Charts",
                    "Replacing minikube with Terraform",
                ],

                "correct": 1,

                "explanation": (
                    "`kubectl` is the command-line client used to interact with Kubernetes clusters."
                ),
            },

            {
                "id": "M06.L01.Q09",

                "section_id": "service-manifest",

                "question": (
                    "In the Service manifest, what does targetPort: 8080 refer to?"
                ),

                "options": [
                    "The Service's external Docker Hub port",
                    "The application port on the selected Pods",
                    "The minikube control-plane port",
                    "The Helm repository port",
                ],

                "correct": 1,

                "explanation": (
                    "The Service forwards traffic from its own port to targetPort 8080 on matching Pods."
                ),
            },

            {
                "id": "M06.L01.Q10",

                "section_id": "scale-rollout",

                "question": (
                    "Which command from the lesson changes the desired replica count to five?"
                ),

                "options": [
                    "kubectl scale deployment flask-app-deployment --replicas=5",
                    "kubectl rollout undo flask-app-deployment --replicas=5",
                    "minikube scale 5",
                    "helm repo add replicas=5",
                ],

                "correct": 0,

                "explanation": (
                    "`kubectl scale` updates the Deployment's desired replica count."
                ),
            },

            {
                "id": "M06.L01.Q11",

                "section_id": "scale-rollout",

                "question": (
                    "What is the purpose of kubectl rollout undo in the lesson?"
                ),

                "options": [
                    "Delete the cluster",
                    "Return the Deployment to a previous revision",
                    "Remove the Service",
                    "Stop all Nodes permanently",
                ],

                "correct": 1,

                "explanation": (
                    "The command is used to roll back a Deployment when a new rollout is problematic."
                ),
            },

            {
                "id": "M06.L01.Q12",

                "section_id": "helm",

                "question": (
                    "What does Helm combine with Kubernetes templates to produce final manifests?"
                ),

                "options": [
                    "terraform.tfstate",
                    "values such as those in values.yaml",
                    "Docker layers only",
                    "GitHub Secrets only",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter explains Helm's templating model as templates plus configurable values."
                ),
            },

            {
                "id": "M06.L01.Q13",

                "section_id": "helm",

                "type": "open",

                "question": (
                    "Describe the full Kubernetes path taught in this lesson from a Docker Hub image "
                    "to a running, reachable, scalable application. Include the Deployment, Pod template, "
                    "labels/selectors, Service, NodePort, scaling, rolling updates, rollback, and where Helm "
                    "would help as the application configuration becomes more complex."
                ),
            },
        ],

        "passing_score": 70,
    },
}
