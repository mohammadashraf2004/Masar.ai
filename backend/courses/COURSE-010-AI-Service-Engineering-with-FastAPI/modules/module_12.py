"""M01.L12 — Deployment of AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 12, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L12"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Deploy GenAI services using virtual machines, serverless functions, managed "
    "platforms, and containers; package FastAPI services with Docker; manage image "
    "layers, registries, storage, permissions, networking, GPUs, and Compose; and "
    "optimize container build time and final image size."
)

SOURCE_CHAPTER = 12

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Deployment of AI Services",

    "slug": "generative-ai-services-m01-l12",

    "description": (
        "Learn how to choose a deployment strategy for a GenAI service, understand "
        "virtualization versus containerization, build and distribute Docker images, "
        "persist and share container data safely, configure container networking and "
        "GPU access, orchestrate multicontainer environments with Docker Compose, and "
        "optimize images using minimal bases, build caching, small build contexts, "
        "externalized artifacts, and multi-stage builds."
    ),

    "order": 12,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.0,

    "skill_tags": [
        "deployment",
        "virtual-machines",
        "serverless",
        "paas",
        "containers",
        "docker",
        "dockerfile",
        "container-registry",
        "docker-storage",
        "docker-volumes",
        "docker-networking",
        "linux-permissions",
        "docker-compose",
        "gpu-containers",
        "image-optimization",
        "multi-stage-builds",
    ],

    "prerequisite_ids": [
        "M01.L11",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Deployment of AI Services",

        "content": """
# Deployment of AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L12  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 12 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Compare virtual machines, serverless functions, managed application platforms, and containers as deployment options.
- Explain what a virtual machine is and how a hypervisor allocates virtual hardware.
- Identify when direct VM deployment can be useful and what operational responsibilities it introduces.
- Explain serverless/event-driven execution and recognize workloads that do or do not fit short-lived cloud functions.
- Describe the convenience/cost trade-off of managed application platforms.
- Explain why containerization improves portability and repeatability.
- Distinguish virtualization from containerization.
- Explain the roles of the Docker client, Docker daemon/server, image, container, and registry.
- Read and reason about a basic Dockerfile for a FastAPI service.
- Explain Docker image layers and build-cache behavior.
- Build, tag, push, and pull images conceptually.
- Explain why data written only to a container's writable layer is ephemeral.
- Choose among Docker volumes, bind mounts, and tmpfs mounts.
- Recognize the security and ownership problems caused by running containers as root.
- Interpret basic Linux file permissions and explain the roles of `chown` and `chmod`.
- Compare bridge, host, none, overlay, Macvlan, and IPvlan networking at a high level.
- Build an isolated user-defined bridge network and use container-name DNS.
- Explain the difference between container-internal ports and published host ports.
- Explain how GPU access is exposed to containers.
- Use Docker Compose conceptually to coordinate an application, database, network, volumes, environment variables, and secrets.
- Explain Compose watch and environment-specific Compose overrides.
- Configure GPU reservations conceptually in Compose.
- Reduce container image size/build time using minimal base images, externalized data, correct layer ordering, `.dockerignore`, cache/bind mounts, external caches, and multi-stage builds.
- Explain when avoiding GPU runtimes can significantly reduce container size.
- Design a practical deployment path for a GenAI service from development to a production host.

---

## 1. Deployment starts with choosing the right hosting model

Once a GenAI service works locally, users still cannot access it until it is hosted somewhere reachable.

The chapter introduces four common deployment strategies:

1. virtual machines,
2. serverless functions,
3. managed application platforms,
4. containers.

These are not mutually exclusive.

A realistic system may use:

```text
VM
  ↓
Docker runtime
  ↓
containerized FastAPI service
```

or:

```text
managed platform
  ↓
deploy container image
```

or:

```text
serverless functions
  ↓
small event-driven API workloads
```

The important question is not:

> Which deployment technology is the most advanced?

It is:

> Which deployment model matches this service's resource needs, scale, operational budget, isolation requirements, and model-hosting strategy?

### Quick comparison

| Option | Main strength | Main trade-off |
|---|---|---|
| VM | Control over OS/hardware/GPU | More maintenance |
| Serverless | Event-driven scaling and pay-for-use | Resource/time constraints |
| Managed app platform | Easy deployment and operations | Higher abstraction/cost |
| Containers | Portability and repeatable environments | Requires container knowledge |

[[IMAGE_NEEDED: Deployment options for a GenAI service | Four branches from one FastAPI/GenAI application to VM, serverless function, managed application platform, and container deployment | Learner should notice that deployment choice depends on workload and operational requirements rather than one universal method]]

{{exercise:M01.L12.EX01}}

---

## 2. Deploying to virtual machines

A virtual machine is a software-emulated computer.

It has:

- a guest operating system,
- virtual CPU,
- virtual memory,
- virtual storage,
- applications running inside it.

The physical machine underneath is the **host**.

A **hypervisor** allocates host resources to VMs.

Conceptually:

```text
Physical server
    ↓
Hypervisor
    ├── VM A → guest OS → application
    ├── VM B → guest OS → application
    └── VM C → guest OS → application
```

### Why VMs can be useful for GenAI

The chapter highlights direct control over:

- OS configuration,
- CPU/memory/disk,
- GPU drivers,
- networking,
- security environment.

This can be valuable when self-hosting models or when strong environment isolation is required.

### Operational cost

With control comes responsibility.

You may need to manage:

- security patches,
- OS upgrades,
- packages,
- GPU drivers,
- network configuration,
- disk capacity,
- monitoring,
- uptime.

VMs also commonly remain running continuously unless startup/shutdown is automated.

### A practical VM deployment

A simple approach is:

```text
provision VM
→ clone repository
→ install dependencies
→ configure environment
→ run application
```

The chapter recommends using containers on top of the VM for a more repeatable deployment process.

[[IMAGE_NEEDED: VM architecture | Physical host hardware → hypervisor → multiple VMs, each with its own guest OS and application | Learner should notice that each VM carries a full guest operating system and receives virtualized hardware resources]]

---

## 3. Deploying to serverless functions

Serverless computing runs code in response to events.

Examples include:

- HTTP request,
- queue message,
- storage/blob event,
- database event.

The developer supplies code while the cloud provider manages the compute infrastructure.

### "Serverless" still uses servers

The term means:

```text
you do not manage the server directly
```

not:

```text
no server exists
```

### Good fits from the chapter

Serverless functions are useful when:

- workloads are event-driven,
- functions are short-lived,
- you want pay-for-use behavior,
- you need batch/event automation,
- traffic can scale dynamically.

### Constraints

The source warns that functions generally have:

- limited resources,
- execution-time limits,
- allocation/startup latency,
- provider-specific runtime constraints.

For a resource-heavy or long-running self-hosted model, the chapter recommends considering another deployment approach.

### API-backed model pattern

A lightweight FastAPI service can still call an external model provider:

```text
HTTP request
    ↓
serverless FastAPI/function
    ↓
external model API
    ↓
response
```

This keeps heavy inference outside the function runtime.

### Split by endpoint when appropriate

The source notes that separate endpoints can sometimes be deployed as separate functions.

That can reduce how much of the application must run in a continuously provisioned environment.

---

## 4. Wrap a FastAPI app for a serverless runtime

The chapter demonstrates the idea with an Azure-style function runtime.

The important architecture is:

```text
cloud function runtime
        ↓
ASGI adapter/wrapper
        ↓
FastAPI application
```

A project may contain:

```text
project/
├── host.json
├── main.py
├── app.py
└── requirements.txt
```

A minimal FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/generate/text")
async def generate_text(prompt: str):
    ...
```

Then the provider-specific runtime wraps the ASGI application.

### Deployment lesson

The exact wrapper/configuration depends on the provider.

The reusable principle is:

> **A serverless provider must support or adapt to the framework/runtime that your FastAPI application requires.**

If it cannot, either:

- migrate the endpoint logic into the provider's supported function model, or
- choose another hosting option.

---

## 5. Managed application platforms

Managed application platforms remove many infrastructure decisions.

They can provide tools for:

- deployment,
- networking,
- scaling,
- SSL certificates,
- custom domains,
- monitoring,
- staging environments.

The chapter gives examples across major cloud providers and third-party application platforms.

### Why use one?

For a prototype or CPU-based backend, the experience can be:

```text
connect repository
→ configure runtime
→ deploy
```

This can be much faster than managing a VM manually.

### Trade-off

The platform manages more for you.

You typically pay for that convenience.

### GPU consideration

The source warns that general managed application platforms may not provide the GPU resources needed to self-host large AI models.

That can push model inference toward:

- dedicated VMs,
- on-premises GPU servers,
- specialized AI hosting platforms,
- external model APIs.

### Runtime compatibility

Managed platforms support specific runtimes/framework versions.

A deployment can fail if your application depends on unsupported versions or system libraries.

This is one reason containers are attractive: they package the runtime and dependencies with the application.

---

## 6. Why containers are useful for deployment

A container packages:

```text
application code
+
runtime
+
dependencies
+
required filesystem content
```

into an isolated unit.

This helps the same application behave consistently across:

- developer machines,
- VMs,
- cloud hosts,
- container platforms.

### Containerization versus virtualization

Virtualization:

```text
physical hardware
→ hypervisor
→ VM
→ guest OS
→ app
```

Containerization:

```text
host OS kernel
→ container runtime
→ isolated containers
→ apps + dependencies
```

Containers share the host kernel rather than carrying a complete guest OS per application.

### Benefits emphasized in the chapter

- portability,
- smaller footprint,
- fast startup,
- repeatable runtime environment,
- easier horizontal scaling.

{{image:containers-vs-vms}}

---

## 7. Docker architecture

Docker is a platform for building, distributing, and running containerized applications.

The chapter introduces several core pieces.

### Docker client

You interact with Docker through tools such as:

```text
docker CLI
Docker Desktop
```

The client sends commands to the Docker server/daemon.

### Docker daemon

The daemon manages:

- images,
- containers,
- container lifecycle,
- networks,
- volumes,
- registry interactions.

### Docker image

An immutable package/recipe used to create containers.

### Container

A running instance of an image.

Mental model:

```text
Dockerfile
   ↓ build
Docker image
   ↓ run
Container
```

### Registry

A remote system that stores and distributes images.

Examples include:

- public registries,
- private cloud registries,
- self-hosted registries.

{{image:docker-platform}}

---

## 8. Build a FastAPI image with a Dockerfile

A Dockerfile declares how the image should be built.

A teaching example adapted from the chapter:

```dockerfile
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --upgrade \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD [
    "uvicorn",
    "main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

### `FROM`

Chooses the base image.

```dockerfile
FROM python:3.12-slim
```

This provides Python and the underlying environment.

### `WORKDIR`

Sets the working directory inside the image/container.

### `COPY`

Copies files from the build context into the image.

### `RUN`

Executes build-time commands.

Example:

```text
install dependencies
```

### `EXPOSE`

Documents the port the application expects to listen on.

The source explicitly notes:

> `EXPOSE` does not itself publish the port to the host.

### `CMD`

Defines the default command when the container starts.

### Build image

Conceptually:

```bash
docker build -t genai-service .
```

Docker executes Dockerfile instructions and produces an image.

{{exercise:M01.L12.EX02}}

---

## 9. Tag, push, and pull images with registries

A container registry stores images so they can be reused on other machines or deployment platforms.

Typical lifecycle:

```text
build image
    ↓
tag image
    ↓
authenticate to registry
    ↓
push image
    ↓
deployment host pulls image
    ↓
run container
```

### Image tags

Images use a name/tag form:

```text
repository/image:tag
```

Example concept:

```text
genai-service:v1
```

### Avoid careless tag reuse

The source warns that a mutable tag such as:

```text
latest
```

can be overwritten by another build.

For reproducible deployments, track exactly which image/version is being deployed.

### Why registries matter for scaling

Orchestration/deployment systems need a place from which they can fetch the same image repeatedly.

```text
registry
  ↓
instance 1
instance 2
instance 3
```

This supports consistent horizontal scaling.

---

## 10. Docker images are layered

Docker builds images in layers.

A simplified build:

```text
Python base image
    ↓
requirements file
    ↓
installed dependencies
    ↓
application code
```

The final container adds a writable runtime layer on top.

### Why layers help

Shared image layers can be reused instead of copied independently for every container.

That helps:

- disk efficiency,
- faster startup,
- faster rebuilds.

### Build cache

If a layer and its inputs have not changed, Docker can reuse cached build results.

If a layer changes:

```text
that layer
+
later dependent layers
→ rebuild
```

This makes Dockerfile ordering extremely important.

[[IMAGE_NEEDED: Docker layered filesystem | Stack showing base OS/Python layer, dependency layer, application-code layer, and a top writable container layer; several containers share immutable image layers | Learner should notice that image layers are reusable while each running container gets its own ephemeral writable layer]]

---

## 11. A container's writable layer is ephemeral

A container can write files while it runs.

But data written only into its default writable container layer is not a durable persistence strategy.

If the container is destroyed/recreated:

```text
runtime files
→ can disappear
```

Examples of data you should not casually leave only in the writable layer:

- database files,
- uploaded user files,
- important logs,
- generated artifacts that must persist.

### Separate application lifecycle from data lifecycle

Containers should be replaceable.

```text
destroy old container
→ start new container
→ important data still exists elsewhere
```

That requires explicit storage design.

---

## 12. Docker storage options

The chapter introduces three storage/mount approaches:

1. volumes,
2. bind mounts,
3. tmpfs mounts.

### Comparison

| Storage type | Stored where? | Persists? | Strong use case |
|---|---|---:|---|
| Volume | Docker-managed host storage | Yes | Persistent/shared container data |
| Bind mount | Explicit host path | Yes | Local development/source sharing |
| tmpfs | Host RAM | No | Fast temporary/sensitive data |

{{image:storage-mounts}}

---

## 13. Docker volumes

A volume is Docker-managed persistent storage.

The container sees a mounted directory.

Docker owns the host-side storage location.

Use cases include:

- database data,
- state shared across container recreations,
- data shared between containers.

### Persistence model

```text
container A removed
    ↓
volume remains
    ↓
container B mounts same volume
    ↓
data remains available
```

### Lifecycle caution

Volumes persist until explicitly removed.

Recreating a database container does not necessarily reset the underlying database state if it keeps using the same volume.

This is useful in normal operation but can surprise developers when changing database configuration.

---

## 14. Bind mounts

A bind mount maps a real host directory into the container.

Example concept:

```bash
docker run \
  -v ./src:/app \
  genai-service
```

Now:

```text
host ./src
↔
container /app
```

Both sides refer to the same mounted files.

### Useful for local development

You can edit code on the host and let the running container see the updates.

### Important difference from `COPY`

`COPY`:

```text
build time
→ creates a copy inside image
```

Bind mount:

```text
runtime
→ directly maps host directory
```

### Risk

Because the container can modify the mounted host path, accidental deletion or changes inside the container can affect original host files.

Use bind mounts deliberately.

---

## 15. tmpfs mounts

A tmpfs mount stores data in host memory (RAM).

Nothing is written permanently to disk.

When the container stops:

```text
tmpfs data
→ disappears
```

Possible GenAI use cases from the chapter include:

- temporary caches,
- intermediate model computations,
- temporary files,
- session-specific logs,
- test data,
- temporary model artifacts.

### Advantages

- fast I/O,
- no permanent disk write,
- useful for temporary or sensitive state.

### Limitations

The source notes that tmpfs:

- is temporary,
- is Linux-specific,
- is not shared between containers in the same way as normal volumes.

Example:

```bash
docker run \
  --tmpfs /cache \
  genai-service
```

---

## 16. Do not run application containers as root unnecessarily

The source identifies two problems with default root execution.

### Host filesystem ownership

If a root container creates files in a bind-mounted host directory:

```text
container root creates file
        ↓
host file may be owned by root
```

Your normal host user may then struggle to edit or delete it.

### Security risk

If an attacker compromises a root-running container, the consequences can be more serious.

The chapter therefore recommends running as a nonroot user where possible.

### Runtime option

Conceptually:

```bash
docker run --user ... image
```

### Dockerfile option

A Dockerfile can:

1. install/configure required system dependencies as privileged user,
2. create a nonroot user/group,
3. switch to that user near the end.

Conceptually:

```dockerfile
RUN create-nonroot-user
USER appuser

CMD [...]
```

### Principle of least privilege

The process should have only the permissions it needs.

That principle applies equally to:

- filesystem access,
- network access,
- cloud permissions,
- model/tool access.

{{exercise:M01.L12.EX03}}

---

## 17. Understand Linux permissions inside container workflows

A permission listing can look like:

```text
drwxr-xr-x
```

The first character indicates object type.

Then permissions are grouped for:

1. owner,
2. group,
3. others.

Permission symbols:

```text
r → read
w → write
x → execute
```

### Numeric form

The source gives the common mapping:

| Value | Permission |
|---:|---|
| 7 | `rwx` |
| 6 | `rw-` |
| 5 | `r-x` |
| 4 | `r--` |
| 3 | `-wx` |
| 2 | `-w-` |
| 1 | `--x` |
| 0 | `---` |

So:

```text
755
```

means:

```text
owner  = rwx
group  = r-x
others = r-x
```

### `chown`

Changes ownership.

### `chmod`

Changes permissions.

These tools are important when containers create or mount files.

### Mount warning

A bind mount can effectively replace/overlay the permissions visible at the mounted container path with host filesystem permissions.

That means Dockerfile permissions alone may not explain a runtime permission problem.

---

## 18. Docker networking mental model

A GenAI application often needs several services:

```text
FastAPI
PostgreSQL
Redis
Qdrant
model server
```

Docker networking lets containers communicate while controlling isolation.

By default, containers typically get networking through a bridge-style environment.

They can make outgoing connections.

Host access to a container normally requires explicit port publishing.

### Two distinct questions

1. Can containers communicate with one another?
2. Can the host/outside world communicate with the container?

These are not the same thing.

### Security implication

Publishing a port makes a service reachable beyond its internal container network according to the chosen host binding.

Only publish what needs external access.

[[IMAGE_NEEDED: Container networking mental model | Host containing FastAPI, PostgreSQL, Redis, and Qdrant containers connected through an internal Docker network; only FastAPI has a host-published port | Learner should notice that internal service-to-service communication does not require publishing every database port]]

---

## 19. Docker network drivers

The chapter introduces several network drivers.

### Bridge

Connects containers on the same Docker host.

Common local/multicontainer default.

### Host

Container uses the host's network namespace more directly.

Benefits can include reduced networking overhead.

Trade-off:

- less network isolation.

### None

Disables external networking for the container.

Useful when the process should be isolated.

### Overlay

Connects containers across multiple Docker hosts/engines in orchestration scenarios.

### Macvlan

Can make containers appear more like physical devices on the network with their own MAC addresses.

### IPvlan

Provides more direct control over container IP addressing.

### Practical focus

For most local GenAI development, the chapter emphasizes understanding:

```text
bridge
host
none
```

before advanced drivers.

---

## 20. Prefer user-defined bridge networks for related services

A user-defined bridge can isolate one application stack.

Example:

```bash
docker network create genai-net
```

Then:

```text
FastAPI container
→ genai-net

PostgreSQL container
→ genai-net
```

### Why use a custom bridge?

The source highlights:

- better isolation,
- automatic DNS/name resolution,
- clearer service grouping.

### Container-name DNS

Suppose the database container is named:

```text
db
```

Inside the same user-defined network, the application can use:

```text
db
```

as a hostname.

You do not need to hard-code the container's changing internal IP.

{{image:isolated-bridge-networks}}

---

## 21. Publish ports only when external access is required

Containers on the same Docker network can communicate using internal ports.

The host cannot automatically access those services unless the port is published.

Example:

```bash
docker run \
  -p 127.0.0.1:8000:8000 \
  genai-service
```

Mental model:

```text
host 127.0.0.1:8000
        ↓
container :8000
```

### `EXPOSE` versus `-p`

`EXPOSE 8000` in a Dockerfile:

```text
documents intended container port
```

`-p ...` at runtime:

```text
actually publishes/maps host access
```

### Avoid unnecessary database exposure

If FastAPI and PostgreSQL communicate on the same bridge:

```text
FastAPI → db:5432
```

there may be no need to publish PostgreSQL to the entire outside environment.

### Port conflicts

Two host processes cannot casually claim the same host port.

Choose mappings carefully.

{{exercise:M01.L12.EX04}}

---

## 22. Host and none networking

### Host networking

The container shares the host network namespace.

Potential benefit:

- simpler/direct networking,
- reduced NAT/port-forwarding overhead.

Trade-off:

- reduced isolation,
- different platform behavior,
- published-port behavior changes.

### None networking

The container has only its local loopback interface.

This is useful for:

- isolated computation,
- sensitive jobs,
- network-outage testing,
- short-lived processes that do not need external systems.

### Design principle

Choose the narrowest network access required.

If a process does not need the network:

```text
do not give it network access
```

---

## 23. Give containers access to GPUs

A self-hosted GenAI model may require GPU acceleration.

The source explains that Docker can expose NVIDIA GPU devices when the host has the required drivers/toolkit.

Conceptually:

```bash
docker run \
  --gpus=all \
  model-service
```

The containerized application can then use supported deep-learning libraries.

### Application-side device selection

A model library can be configured to place the model on GPU.

Conceptually:

```python
pipeline(
    "text-generation",
    model="...",
    device_map="cuda",
)
```

### Containerization does not create a GPU

The host must already provide:

- compatible GPU hardware,
- drivers/tooling required by the runtime.

Docker exposes those resources to the container.

### Deployment implication

GPU containers are larger and operationally heavier than lightweight API-only containers.

That becomes important during image optimization later.

---

## 24. Docker Compose for multicontainer applications

A real GenAI stack can contain many services.

For example:

```text
server
database
Redis
vector database
monitoring
```

Managing them with separate commands quickly becomes tedious.

Docker Compose describes the stack in YAML.

Example structure adapted from the source:

```yaml
services:
  server:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src/app:/code/app
    networks:
      - genai-net

  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - genai-net

volumes:
  db-data:

networks:
  genai-net:
    driver: bridge
```

### Compose can coordinate

- container images/builds,
- ports,
- environment variables,
- secrets,
- volumes,
- networks,
- service commands.

[[IMAGE_NEEDED: Docker Compose GenAI stack | Compose-defined server and database containers connected to `genai-net`; DB uses a persistent volume, server exposes port 8000, and secrets/environment values enter the server | Learner should notice that Compose describes the whole local stack declaratively]]

### Common lifecycle commands from the chapter

```text
docker compose up
docker compose down
docker compose logs
docker compose ps
```

These allow you to start, stop, inspect, and monitor the defined services as one application environment.

{{exercise:M01.L12.EX05}}

---

## 25. Environment variables and secrets in Compose

The source includes environment variables for runtime configuration.

Examples:

```text
database URL
CORS origins
documentation flags
```

It also demonstrates Docker secrets for sensitive values such as API tokens.

### Configuration versus secret

Configuration:

```text
SHOW_DOCS_IN_PRODUCTION=false
```

Secret:

```text
model API token
database password
private key
```

Secrets deserve stronger handling than ordinary configuration.

### Do not bake secrets into images

A built image may be:

- pushed to a registry,
- copied to other machines,
- inspected later.

Avoid hard-coding secrets in:

- Dockerfile,
- source code,
- committed configuration.

Inject them at deployment/runtime through the appropriate secret/configuration mechanism.

---

## 26. Docker Compose watch

The chapter demonstrates Compose watch for development.

A watch rule can sync changed files into the running container.

Conceptually:

```yaml
develop:
  watch:
    - action: sync
      path: ./src
      target: /code
```

Then:

```text
edit local source
    ↓
Compose detects change
    ↓
sync into container
    ↓
development service updates
```

### Why use watch instead of a broad bind mount?

The source notes that watch can give more granular control.

For example, you may choose to ignore:

- large directories,
- generated files,
- caches.

This can reduce unnecessary I/O.

---

## 27. Use Compose overrides for environment-specific behavior

Development and production often need different settings.

Production:

```text
no hot reload
minimal mounts
production command
```

Development:

```text
local source mount
hot reload
local database
debug configuration
```

The chapter uses:

```text
compose.yml
+
compose.override.yml
```

The override changes only the environment-specific parts.

### Why this helps

You can keep one base application topology while customizing:

- commands,
- environment variables,
- volumes,
- local dependencies.

This reduces duplication across deployment environments.

---

## 28. GPU access through Docker Compose

The source also shows declaring GPU resources in Compose.

Conceptually:

```yaml
services:
  app:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities:
                - gpu
```

The intent is:

```text
service app
→ reserve/access selected GPU resources
```

This gives finer control than casually exposing every GPU to every service.

For multi-model stacks, GPU allocation becomes part of resource planning.

---

## 29. Why Docker image optimization matters

Large images cause several problems.

They take longer to:

- build,
- upload,
- pull,
- start,
- test,
- replicate.

GenAI workloads are especially vulnerable because models and GPU libraries can add gigabytes.

The chapter introduces five major optimization areas:

1. minimal base images,
2. avoiding unnecessary GPU inference runtimes,
3. externalizing application/model data,
4. layer ordering and cache optimization,
5. multi-stage builds.

[[IMAGE_NEEDED: Docker image optimization funnel | Large unoptimized image entering a funnel of minimal base image, externalized artifacts, cache/layer optimization, `.dockerignore`, and multi-stage build, producing a much smaller final production image | Learner should notice that several independent techniques compound to reduce size and build time]]

---

## 30. Choose a minimal base image

The base image becomes the foundation of every later layer.

A full OS image may include many tools the application never uses.

The chapter compares:

- standard/full distributions,
- slim Python images,
- Alpine-based images.

### Slim

A middle ground.

Often easier for Python packages while still smaller than full distributions.

### Alpine

Very small.

But its minimal environment can make some Python/native package installation harder.

### Decision rule from the source

```text
care more about compatibility/build convenience
→ slim may be easier

care aggressively about image size
→ Alpine may be attractive
```

The smallest possible base is not always the most productive choice.

---

## 31. Avoid GPU inference runtimes when you do not need them

GPU-enabled model serving can dramatically enlarge an image because it may require:

- deep-learning frameworks,
- GPU runtime libraries,
- accelerator dependencies.

If the workload can use CPU inference, the source discusses a lighter approach such as:

```text
model export
→ ONNX
→ CPU-oriented runtime
→ optional quantization
```

The chapter connects this to quantization concepts from the previous lesson.

### Important trade-off

Do not remove GPU support if the performance requirement genuinely needs a GPU.

Image-size optimization is not successful if inference becomes unacceptably slow.

The decision still depends on:

- latency,
- throughput,
- cost,
- image size,
- hardware availability.

---

## 32. Externalize models and application data when appropriate

Copying large model artifacts into an image increases:

- build time,
- image size,
- registry transfer time.

An alternative is:

```text
container starts
    ↓
load/download artifact from external storage
```

or mount persistent model storage.

### Local development

Use:

- volumes,
- bind mounts.

### Production

The source suggests:

- external storage,
- persistent storage mechanisms supplied by orchestration environments.

### Startup risk

Downloading a large model at startup may delay readiness.

If the hosting system expects the service to become healthy too quickly:

```text
startup download
→ health check fails
→ platform kills container
```

The chapter therefore warns that health/readiness timing needs to match model initialization behavior.

In some cases, baking the artifact into the image may still be justified.

---

## 33. Order Dockerfile layers from stable to volatile

Docker rebuilds a changed layer and the layers after it.

Bad ordering:

```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

A small source-code edit changes `COPY . .`.

That invalidates the later dependency-install layer.

Dependencies are reinstalled unnecessarily.

Better ordering:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Now:

```text
source code changes
→ application layer rebuilds

requirements unchanged
→ dependency layer stays cached
```

### Rule

Put:

```text
stable + expensive steps earlier
```

and:

```text
frequently changing steps later
```

Examples of stable/expensive work:

- dependency installation,
- large model downloads.

Examples of volatile work:

- application code,
- rapidly changing configuration.

{{exercise:M01.L12.EX06}}

---

## 34. Keep the build context small with `.dockerignore`

The build context is the set of files sent to the Docker builder.

If you run:

```dockerfile
COPY . .
```

you may accidentally include:

- `.git`,
- virtual environments,
- Python caches,
- type-check caches,
- secrets/environment files,
- local artifacts.

Problems:

- larger build context,
- larger image,
- slower builds,
- unnecessary cache invalidation,
- possible secret leakage.

### `.dockerignore`

The source provides examples such as:

```text
**/__pycache__
**/.mypy_cache
**/.venv
**/.env
**/.git
```

This prevents unwanted files from entering the build context/image.

### Security bonus

A smaller build context is not only faster.

It also reduces the chance that local secrets or development files are copied into an image.

---

## 35. Use build cache and bind mounts intentionally

BuildKit-style mounts can make expensive build steps faster without permanently copying every temporary file into the final layer.

### Cache mount

Use a persistent build cache for items such as:

- package downloads,
- model downloads.

Conceptually:

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

Subsequent builds can reuse the cache.

### Build-time bind mount

A file can be made available only during one build step rather than copied permanently.

This can reduce layers/build-context side effects.

### Trade-off with package-manager cache disabling

Using:

```text
--no-cache-dir
```

can reduce final image size.

But it can also force future builds to redownload packages unless other build caching is used.

Optimization must consider both:

```text
final image size
and
developer/CI build speed
```

---

## 36. Use external build cache in CI/CD

Local Docker builds can reuse local cached layers.

CI builders are often temporary.

A fresh CI runner may have no local cache.

The chapter introduces external/registry-backed caches.

Conceptually:

```text
CI build
→ fetch previous cache
→ reuse unchanged expensive layers
→ push updated cache
```

This can reduce:

- build minutes,
- dependency downloads,
- repeated model/artifact fetches.

For large AI images, remote caching can save substantial iteration time.

---

## 37. Multi-stage builds

A multi-stage Dockerfile contains multiple named build stages.

Example mental model:

```text
Stage 1: base/build
→ compilers
→ dependency setup
→ model download
→ build artifacts

Stage 2: production
→ copy only runtime artifacts

Stage 3: development
→ extend production
→ add dev tools
→ hot reload
```

### Why it works

Production does not need every tool required during development/build.

You can leave behind:

- compilers,
- temporary build packages,
- caches,
- debugging tools.

and copy only:

- runtime dependencies,
- model artifacts,
- application files.

[[IMAGE_NEEDED: Multi-stage Docker build | Three stages labeled Base/Builder, Production, and Development; arrows show only selected artifacts copied from earlier stages into a small production image while dev tools remain in the development stage | Learner should notice that build-time tooling does not need to ship in the final production image]]

### Target a stage

One Dockerfile can support several images.

Example concept:

```text
production target
development target
```

This keeps shared setup in one place.

{{exercise:M01.L12.EX07}}

---

## 38. Use `docker init` as a starting point

The chapter closes its Docker workflow with `docker init`.

Conceptually:

```bash
docker init
```

can generate starter files such as:

```text
.dockerignore
compose.yaml
Dockerfile
README.Docker.md
```

The generated setup can then be customized for:

- dependencies,
- additional services,
- volumes,
- secrets,
- networks,
- GPU access,
- production commands.

### Why use a generated starting point?

It can reduce simple configuration mistakes and provide a baseline for applying container best practices.

It is still the developer's responsibility to understand and review the generated configuration.

---

## 39. Put the complete deployment workflow together

A practical deployment path from the chapter can be summarized as:

```text
Develop FastAPI GenAI service
        ↓
choose hosting model
        ↓
containerize service
        ↓
build optimized image
        ↓
test image locally
        ↓
configure networks/storage/secrets
        ↓
push image to registry
        ↓
deployment environment pulls image
        ↓
run container(s)
        ↓
monitor health and logs
        ↓
replace/redeploy new image versions
```

### If the app has several services

```text
FastAPI
PostgreSQL
Redis
vector DB
```

use a multicontainer definition during local development.

In production, equivalent services may be:

- managed databases,
- cloud storage,
- managed Redis,
- container/orchestration services.

### Keep containers replaceable

A strong container design separates:

```text
immutable application image
from
persistent application data
from
runtime secrets/configuration
```

Then deployment becomes:

```text
replace container
without losing data
without rebuilding configuration manually
```

### Deployment decision flow

```text
Need full OS/GPU control?
→ VM / specialized host

Short event-driven workload?
→ serverless may fit

Want fast managed deployment?
→ managed platform

Need portable repeatable packaging?
→ containerize

Need several coordinated containers locally?
→ Compose

Need durable data?
→ external storage / volume

Need GPU?
→ host GPU + container GPU access

Image too large/slow?
→ optimize base, context, layers, cache, stages
```

---

## Important misconceptions

### Misconception 1

> Deployment means simply running `uvicorn` on another computer.

### Why this is incomplete

Production deployment also involves runtime dependencies, networking, persistence, secrets, scaling, monitoring, and repeatability.

### Misconception 2

> Serverless means no servers are involved.

### Why this is wrong

The cloud provider manages the server infrastructure; the hardware still exists.

### Misconception 3

> Serverless functions are ideal for every AI workload.

### Why this is wrong

The source warns about limited resources and execution-time constraints, especially for heavy self-hosted model inference.

### Misconception 4

> Containers and virtual machines are the same technology.

### Why this is wrong

VMs virtualize hardware and include guest operating systems; containers share the host kernel through a container runtime.

### Misconception 5

> A Docker image and a Docker container are the same thing.

### Why this is wrong

An image is the immutable package/template; a container is a running instance.

### Misconception 6

> `EXPOSE 8000` makes port 8000 publicly reachable.

### Why this is wrong

It documents the intended container port; runtime port publishing performs the actual host mapping.

### Misconception 7

> Data written inside a container automatically survives replacement.

### Why this is wrong

The default writable layer is ephemeral from the perspective of durable application state.

### Misconception 8

> Bind mounts and `COPY` do the same thing.

### Why this is wrong

`COPY` stores a separate copy inside the image at build time; a bind mount maps a live host path at runtime.

### Misconception 9

> tmpfs is a good place for durable database files.

### Why this is wrong

tmpfs stores data in memory and is intentionally nonpersistent.

### Misconception 10

> Running containers as root is harmless because containers are isolated.

### Why this is wrong

Root execution increases security risk and can create host filesystem ownership problems with mounts.

### Misconception 11

> Containers on a bridge network require every database port to be publicly published.

### Why this is wrong

Containers on the same internal network can communicate directly using their internal ports.

### Misconception 12

> Container DNS names such as `db` are always resolvable from the host machine.

### Why this is wrong

The source describes Docker's embedded DNS inside user-defined container networks, not as a general host DNS mechanism.

### Misconception 13

> Host networking gives the same isolation as a user-defined bridge.

### Why this is wrong

Host networking removes an important network-isolation boundary.

### Misconception 14

> Docker can provide GPU acceleration even if the host has no compatible GPU environment.

### Why this is wrong

The host must supply compatible hardware and drivers/tooling; Docker exposes those resources to the container.

### Misconception 15

> Compose is only a shorter version of `docker run`.

### Why this is incomplete

Compose declaratively coordinates services, networks, volumes, variables, secrets, commands, and environment-specific configuration.

### Misconception 16

> Putting a secret in a Dockerfile is safe because images are immutable.

### Why this is wrong

Image layers can be distributed and inspected. Secrets should be injected through appropriate runtime secret/configuration mechanisms.

### Misconception 17

> The smallest possible base image is always the best choice.

### Why this is wrong

Minimal distributions can create compatibility and build-complexity trade-offs.

### Misconception 18

> `COPY . .` should always be the first Dockerfile step after `FROM`.

### Why this is wrong

Copying frequently changing source too early can invalidate expensive cached dependency layers.

### Misconception 19

> `.dockerignore` only makes builds slightly cleaner.

### Why this is incomplete

It can reduce build context, image size, cache invalidation, and accidental inclusion of local secrets/artifacts.

### Misconception 20

> Disabling every package cache always makes builds faster.

### Why this is wrong

It may reduce final image size but force repeated downloads. Build-cache strategy and final-image strategy are separate concerns.

### Misconception 21

> Development compilers/debugging tools must ship in the production image.

### Why this is wrong

Multi-stage builds can keep build/development tooling out of the final runtime image.

---

## Key terminology

| Term | Meaning |
|---|---|
| Deployment | Making an application available in a target runtime environment |
| VM | Virtual machine with virtual hardware and a guest OS |
| Hypervisor | Software layer managing virtual machines and host resource allocation |
| Guest OS | Operating system running inside a VM |
| Serverless function | Event-driven cloud execution unit managed by a provider |
| Managed application platform | Platform that manages much of deployment/runtime infrastructure |
| Container | Isolated running application environment sharing the host kernel |
| Containerization | Packaging applications and dependencies into container images/runtimes |
| Docker | Platform for building, distributing, and running containers |
| Docker client | CLI/GUI that sends Docker commands |
| Docker daemon | Background server managing images, containers, networks, and volumes |
| Dockerfile | Build instructions for a Docker image |
| Image | Immutable packaged filesystem/configuration used to create containers |
| Registry | Service storing/distributing container images |
| Tag | Name/version label associated with an image |
| Layer | Cached filesystem change contributing to an image |
| Build cache | Reusable result of unchanged Docker build steps |
| Writable layer | Ephemeral runtime layer added to a container |
| Volume | Docker-managed persistent storage |
| Bind mount | Mapping of a host path into a container |
| tmpfs | In-memory temporary mount |
| Root user | Highly privileged system user |
| `chown` | Command that changes file/directory ownership |
| `chmod` | Command that changes file/directory permissions |
| Bridge network | Docker network connecting containers on one host |
| User-defined bridge | Custom isolated bridge with container-name DNS |
| Host network | Container shares host network namespace |
| None network | Networking disabled except loopback |
| Overlay network | Network connecting containers across multiple Docker hosts |
| Port publishing | Mapping a host port to a container port |
| Embedded DNS | Docker name-resolution service for user-defined networks |
| Docker Compose | Tool for defining/running multicontainer applications from YAML |
| Compose override | Additional Compose configuration overriding a base file |
| Compose watch | Development feature syncing selected source changes into containers |
| GPU reservation | Declared access/allocation of GPU devices to a container/service |
| Build context | Files sent to the Docker builder |
| `.dockerignore` | File excluding paths from the Docker build context |
| Cache mount | Build-time mount persisting reusable cache data |
| Multi-stage build | Dockerfile with several stages that selectively copy runtime artifacts |
| Externalized artifact | Model/data kept outside the application image and loaded/mounted separately |

---

## Self-check

Before continuing, make sure you can answer:

1. What four deployment strategies does the chapter introduce?
2. What is a virtual machine?
3. What does a hypervisor do?
4. What is a guest OS?
5. Why can VMs be useful for GPU-backed AI workloads?
6. What operational responsibilities come with VMs?
7. What does serverless computing mean?
8. Why does serverless not mean there are no servers?
9. What kinds of workloads fit serverless functions well?
10. Why can heavy self-hosted model inference be a poor serverless fit?
11. How can a lightweight serverless API still use a large LLM?
12. What does a managed application platform manage for you?
13. What is the main convenience/cost trade-off of managed platforms?
14. Why can runtime compatibility be a deployment issue?
15. What is a container?
16. How does containerization differ from virtualization?
17. Why are containers generally lighter than VMs?
18. What is the Docker client?
19. What is the Docker daemon?
20. What is a Docker image?
21. What is a container?
22. What is a container registry?
23. What does `FROM` do?
24. What does `WORKDIR` do?
25. What is the difference between `RUN` and `CMD`?
26. What does `COPY` do?
27. What does `EXPOSE` do?
28. Why does `EXPOSE` not make a port reachable from the host?
29. What does `docker build` conceptually produce?
30. Why should image tags be treated carefully?
31. How do registries support repeatable deployments?
32. What is a Docker image layer?
33. Why can multiple containers efficiently share image layers?
34. What happens when an earlier build layer changes?
35. What is the container's writable layer?
36. Why should important data not live only there?
37. What are the three storage types covered in the chapter?
38. When should you use a volume?
39. When is a bind mount useful?
40. What is the key difference between bind mount and `COPY`?
41. What is tmpfs?
42. What kinds of GenAI data can fit a tmpfs mount?
43. Why is tmpfs inappropriate for durable state?
44. Why can root containers cause host file-ownership problems?
45. Why is root execution a security concern?
46. When should you switch to a nonroot user in a Dockerfile?
47. What do `r`, `w`, and `x` mean?
48. What does permission mode 755 represent?
49. What does `chown` change?
50. What does `chmod` change?
51. How can a bind mount affect permissions seen inside a container?
52. What two questions should you separate when thinking about Docker networking?
53. What does the bridge driver do?
54. What does host networking do?
55. What does the none driver do?
56. What does an overlay network address?
57. Why are user-defined bridge networks useful?
58. What does Docker embedded DNS allow?
59. Why can a container use `db` as a hostname inside a user-defined network?
60. Why may the host machine not resolve that same `db` name?
61. What does `-p host:container` do?
62. Why should internal databases not automatically be published externally?
63. What is a host-port conflict?
64. When could `--network none` be useful?
65. What is required on the host before a container can use a GPU?
66. What does `--gpus=all` conceptually do?
67. Why are GPU-serving containers often much larger?
68. What problem does Docker Compose solve?
69. Which resources can Compose define?
70. What does `docker compose up` do conceptually?
71. What is the difference between configuration and secrets?
72. Why should API tokens not be baked into the image?
73. What does Compose watch do?
74. Why can watch be more selective than a broad bind mount?
75. What is a Compose override file used for?
76. Why might development and production use different commands?
77. How can Compose declare GPU resources?
78. Why does image size matter for deployment?
79. What five optimization areas does the chapter introduce?
80. Why use a slim/minimal base image?
81. What is the trade-off between slim and Alpine-style images?
82. Why can GPU runtime dependencies dominate image size?
83. When might an ONNX/CPU runtime be appropriate?
84. Why should model artifacts sometimes be externalized?
85. What startup risk appears when a container downloads a large model?
86. Why should Dockerfile steps be ordered from stable to volatile?
87. Why is copying source before dependency installation often inefficient?
88. What is the build context?
89. Why can a large build context slow builds?
90. What should `.dockerignore` commonly exclude?
91. How can `.dockerignore` reduce secret leakage risk?
92. What does a cache mount do during builds?
93. Why might `pip --no-cache-dir` reduce image size but slow later builds?
94. Why is an external cache useful in CI?
95. What is a multi-stage build?
96. What kinds of tools can be left out of the final production stage?
97. Why can one Dockerfile contain both production and development targets?
98. What files can `docker init` help generate?
99. What three things should be separated in a strong container deployment: application image, persistent data, and what else?
100. How would you choose between VM, serverless, managed platform, and container-based deployment for a new GenAI service?

---

## Retain this idea

**Deploy GenAI services by separating concerns: choose a hosting model that matches the workload, package the application into a reproducible container when portability matters, keep persistent data and secrets outside the disposable container layer, expose only the networks and permissions the service needs, and optimize Docker builds so stable dependencies are cached while development-only tools and large unnecessary artifacts stay out of the production image.**
""",

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "deployment-options", "title": "Deployment starts with choosing the right hosting model", "order": 1},
            {"id": "virtual-machines", "title": "Deploying to virtual machines", "order": 2},
            {"id": "serverless", "title": "Deploying to serverless functions", "order": 3},
            {"id": "serverless-fastapi", "title": "Wrap a FastAPI app for a serverless runtime", "order": 4},
            {"id": "managed-platforms", "title": "Managed application platforms", "order": 5},
            {"id": "containers", "title": "Why containers are useful for deployment", "order": 6},
            {"id": "docker-architecture", "title": "Docker architecture", "order": 7},
            {"id": "dockerfile", "title": "Build a FastAPI image with a Dockerfile", "order": 8},
            {"id": "registries", "title": "Tag, push, and pull images with registries", "order": 9},
            {"id": "layers-unionfs", "title": "Docker images are layered", "order": 10},
            {"id": "ephemeral-storage", "title": "A container's writable layer is ephemeral", "order": 11},
            {"id": "docker-storage", "title": "Docker storage options", "order": 12},
            {"id": "volumes", "title": "Docker volumes", "order": 13},
            {"id": "bind-mounts", "title": "Bind mounts", "order": 14},
            {"id": "tmpfs", "title": "tmpfs mounts", "order": 15},
            {"id": "nonroot", "title": "Do not run application containers as root unnecessarily", "order": 16},
            {"id": "linux-permissions", "title": "Understand Linux permissions inside container workflows", "order": 17},
            {"id": "docker-networking", "title": "Docker networking mental model", "order": 18},
            {"id": "network-drivers", "title": "Docker network drivers", "order": 19},
            {"id": "user-defined-bridge", "title": "Prefer user-defined bridge networks for related services", "order": 20},
            {"id": "published-ports", "title": "Publish ports only when external access is required", "order": 21},
            {"id": "host-none-network", "title": "Host and none networking", "order": 22},
            {"id": "gpu-docker", "title": "Give containers access to GPUs", "order": 23},
            {"id": "compose", "title": "Docker Compose for multicontainer applications", "order": 24},
            {"id": "compose-secrets", "title": "Environment variables and secrets in Compose", "order": 25},
            {"id": "compose-watch", "title": "Docker Compose watch", "order": 26},
            {"id": "compose-overrides", "title": "Use Compose overrides for environment-specific behavior", "order": 27},
            {"id": "compose-gpu", "title": "GPU access through Docker Compose", "order": 28},
            {"id": "optimize-images", "title": "Why Docker image optimization matters", "order": 29},
            {"id": "minimal-base", "title": "Choose a minimal base image", "order": 30},
            {"id": "avoid-gpu-runtime", "title": "Avoid GPU inference runtimes when you do not need them", "order": 31},
            {"id": "externalize-data", "title": "Externalize models and application data when appropriate", "order": 32},
            {"id": "layer-ordering", "title": "Order Dockerfile layers from stable to volatile", "order": 33},
            {"id": "minimize-build-context", "title": "Keep the build context small with .dockerignore", "order": 34},
            {"id": "build-cache-mounts", "title": "Use build cache and bind mounts intentionally", "order": 35},
            {"id": "external-build-cache", "title": "Use external build cache in CI/CD", "order": 36},
            {"id": "multi-stage", "title": "Multi-stage builds", "order": 37},
            {"id": "docker-init", "title": "Use docker init as a starting point", "order": 38},
            {"id": "deployment-workflow", "title": "Put the complete deployment workflow together", "order": 39},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L12.EX01",
            "title": "Choose a Deployment Model",
            "lesson_code": "M01.L12",
            "section_id": "deployment-options",
            "placement": "after_section",
            "description": (
                "Match deployment approaches to realistic GenAI workloads."
            ),
            "instructions": (
                "Choose the strongest primary option from `VM`, `serverless`, "
                "`managed platform`, or `container-based deployment` for each scenario:\n\n"
                "1. A small event-driven API that calls an external LLM provider and receives irregular traffic.\n"
                "2. A self-hosted GPU model requiring direct driver/hardware control.\n"
                "3. A prototype that should be online quickly with minimal operations work.\n"
                "4. A production FastAPI service that must run consistently across local, staging, and cloud environments.\n\n"
                "For each, explain the operational trade-off."
            ),
            "expected_output": (
                "Four deployment decisions with workload and operations reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "deployment-selection",
                "infrastructure-tradeoffs",
                "genai-hosting",
            ],
        },
        {
            "id": "M01.L12.EX02",
            "title": "Read and Improve a FastAPI Dockerfile",
            "lesson_code": "M01.L12",
            "section_id": "dockerfile",
            "placement": "after_section",
            "description": (
                "Practice reasoning about Dockerfile instructions and container startup."
            ),
            "instructions": (
                "Write a minimal Dockerfile for a FastAPI service that:\n"
                "1. starts from a Python slim image,\n"
                "2. sets `/code` as the working directory,\n"
                "3. copies `requirements.txt` before the application source,\n"
                "4. installs dependencies,\n"
                "5. copies source code,\n"
                "6. documents port 8000,\n"
                "7. runs Uvicorn on `0.0.0.0:8000`.\n\n"
                "Then explain why copying requirements before the full source tree becomes useful for build caching."
            ),
            "expected_output": (
                "A Dockerfile plus an explanation of its instruction order."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "dockerfile",
                "fastapi-deployment",
                "docker-build",
            ],
        },
        {
            "id": "M01.L12.EX03",
            "title": "Fix a Root-Owned Bind Mount",
            "lesson_code": "M01.L12",
            "section_id": "nonroot",
            "placement": "after_section",
            "description": (
                "Reason about container users, host ownership, and least privilege."
            ),
            "instructions": (
                "Scenario:\n"
                "- a container runs as root,\n"
                "- `./outputs` is bind-mounted into `/app/outputs`,\n"
                "- the container creates files,\n"
                "- your normal host account can no longer edit them.\n\n"
                "Explain:\n"
                "1. why the files can become root-owned,\n"
                "2. how running the application as a nonroot container user helps,\n"
                "3. when `chown` may be needed,\n"
                "4. when `chmod` may be needed,\n"
                "5. why simply setting permissions very broadly is not a good security strategy."
            ),
            "expected_output": (
                "A permission diagnosis and a safer nonroot ownership/permission plan."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "docker-permissions",
                "linux-permissions",
                "least-privilege",
            ],
        },
        {
            "id": "M01.L12.EX04",
            "title": "Design a Safe Container Network",
            "lesson_code": "M01.L12",
            "section_id": "published-ports",
            "placement": "after_section",
            "description": (
                "Separate internal service networking from host/public port exposure."
            ),
            "instructions": (
                "You have three containers:\n"
                "- `server` on port 8000,\n"
                "- `db` on port 5432,\n"
                "- `redis` on port 6379.\n\n"
                "Design a user-defined bridge network where:\n"
                "1. all three services can communicate internally,\n"
                "2. `server` reaches the database using hostname `db`,\n"
                "3. `server` reaches Redis using hostname `redis`,\n"
                "4. only the FastAPI server is published to the host,\n"
                "5. the database and Redis are not unnecessarily exposed externally.\n\n"
                "Explain the difference between an internal container port and a published host port."
            ),
            "expected_output": (
                "A network diagram/command plan with service names and only required host exposure."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "docker-networking",
                "bridge-network",
                "port-publishing",
            ],
        },
        {
            "id": "M01.L12.EX05",
            "title": "Build a Compose Stack",
            "lesson_code": "M01.L12",
            "section_id": "compose",
            "placement": "after_section",
            "description": (
                "Represent a repeatable FastAPI + PostgreSQL deployment environment in Compose."
            ),
            "instructions": (
                "Create a `compose.yaml` containing:\n"
                "1. a `server` service built from the local Dockerfile,\n"
                "2. host mapping `8000:8000`,\n"
                "3. a PostgreSQL `db` service,\n"
                "4. a named database volume,\n"
                "5. one user-defined bridge network shared by both services,\n"
                "6. an environment variable for the database URL,\n"
                "7. a secret placeholder for an LLM API token.\n\n"
                "Then identify which state should survive `docker compose down` and which parts should be safely recreated."
            ),
            "expected_output": (
                "A Compose file and state-lifecycle explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "docker-compose",
                "volumes",
                "networks",
                "runtime-configuration",
            ],
        },
        {
            "id": "M01.L12.EX06",
            "title": "Repair an Inefficient Docker Build",
            "lesson_code": "M01.L12",
            "section_id": "layer-ordering",
            "placement": "after_section",
            "description": (
                "Apply Docker layer ordering and build-context principles."
            ),
            "instructions": (
                "You find this Dockerfile:\n\n"
                "```dockerfile\n"
                "FROM python:3.12-slim\n"
                "COPY . .\n"
                "RUN pip install -r requirements.txt\n"
                "CMD [\"uvicorn\", \"main:app\"]\n"
                "```\n\n"
                "Every source-code edit causes dependencies to reinstall.\n\n"
                "1. Rewrite the Dockerfile ordering.\n"
                "2. Explain which layer was invalidating the cache.\n"
                "3. List at least five paths that should be considered for `.dockerignore`.\n"
                "4. Explain why `.env` should not enter the build context."
            ),
            "expected_output": (
                "An improved Dockerfile plus cache-invalidation and `.dockerignore` reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "docker-layer-cache",
                "dockerignore",
                "build-optimization",
            ],
        },
        {
            "id": "M01.L12.EX07",
            "title": "Design a Multi-Stage GenAI Image",
            "lesson_code": "M01.L12",
            "section_id": "multi-stage",
            "placement": "after_section",
            "description": (
                "Separate build/development dependencies from the production runtime."
            ),
            "instructions": (
                "Design three stages:\n\n"
                "**Base/build stage**\n"
                "- create virtual environment,\n"
                "- install production dependencies,\n"
                "- obtain required model/runtime artifacts.\n\n"
                "**Production stage**\n"
                "- copy only runtime dependencies/artifacts,\n"
                "- copy application source,\n"
                "- run normal Uvicorn command.\n\n"
                "**Development stage**\n"
                "- extend production,\n"
                "- add testing/debug dependencies,\n"
                "- enable reload.\n\n"
                "Explain why compilers/debuggers should not automatically remain in the production stage."
            ),
            "expected_output": (
                "A three-stage Dockerfile outline plus production-image reasoning."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "multi-stage-builds",
                "image-size",
                "dev-prod-separation",
            ],
        },
        {
            "id": "M01.L12.EX08",
            "title": "Design the Final Deployment Path",
            "lesson_code": "M01.L12",
            "section_id": "deployment-workflow",
            "placement": "after_section",
            "description": (
                "Combine deployment, networking, storage, secrets, images, and registries into one release workflow."
            ),
            "instructions": (
                "Design the deployment workflow for a FastAPI GenAI service with PostgreSQL and an external model provider.\n\n"
                "Include:\n"
                "1. development environment,\n"
                "2. Dockerfile/image build,\n"
                "3. image tag/version,\n"
                "4. local Compose verification,\n"
                "5. persistent database strategy,\n"
                "6. runtime secret injection,\n"
                "7. host/internal network exposure,\n"
                "8. registry push,\n"
                "9. production image pull/run,\n"
                "10. future image replacement without data loss.\n\n"
                "State which artifacts are immutable and which state must persist independently."
            ),
            "expected_output": (
                "A complete containerized release flow with immutable/persistent/runtime-state boundaries."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "deployment-architecture",
                "docker-production",
                "state-management",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L12.QZ01",

        "title": "Deployment of AI Services — Knowledge Check",

        "lesson_code": "M01.L12",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L12.Q01",
                "section_id": "deployment-options",
                "question": "Which deployment option provides the most direct control over the guest OS and GPU drivers?",
                "options": [
                    "Virtual machine",
                    "Static website only",
                    "Browser localStorage",
                    "DNS record",
                ],
                "correct": 0,
                "explanation": (
                    "VM deployment gives direct control over the guest OS, virtual hardware, and driver configuration."
                ),
            },
            {
                "id": "M01.L12.Q02",
                "section_id": "serverless",
                "question": "What does 'serverless' mean in the chapter?",
                "options": [
                    "The cloud provider manages the underlying compute infrastructure for event-driven code",
                    "No physical server hardware exists",
                    "The application cannot receive HTTP requests",
                    "The service must contain its own GPU",
                ],
                "correct": 0,
                "explanation": (
                    "Serverless abstracts server management from the application developer; compute still runs on provider infrastructure."
                ),
            },
            {
                "id": "M01.L12.Q03",
                "section_id": "containers",
                "question": "What is a key difference between containers and VMs?",
                "options": [
                    "Containers share the host kernel instead of requiring a full guest OS per container",
                    "Containers always contain more operating systems than VMs",
                    "VMs cannot run applications",
                    "Containers do not use filesystems",
                ],
                "correct": 0,
                "explanation": (
                    "Containerization isolates applications while sharing the host OS kernel, which is why containers are generally lighter."
                ),
            },
            {
                "id": "M01.L12.Q04",
                "section_id": "docker-architecture",
                "question": "What is the relationship between a Docker image and a container?",
                "options": [
                    "A container is a running instance created from an image",
                    "An image is a running process created from a container",
                    "They are unrelated concepts",
                    "A registry is a running instance of a container",
                ],
                "correct": 0,
                "explanation": (
                    "The image is the immutable package/template; Docker creates running containers from it."
                ),
            },
            {
                "id": "M01.L12.Q05",
                "section_id": "dockerfile",
                "question": "What does the Dockerfile `EXPOSE 8000` instruction do?",
                "options": [
                    "Documents that the containerized application listens on port 8000; runtime publishing is still required for host access",
                    "Guarantees the service is publicly reachable",
                    "Creates a PostgreSQL volume",
                    "Starts Uvicorn automatically",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly distinguishes EXPOSE from actual port publishing with `-p`/`--publish`."
                ),
            },
            {
                "id": "M01.L12.Q06",
                "section_id": "docker-storage",
                "question": "Which Docker storage type is stored in RAM and disappears when the container stops?",
                "options": [
                    "tmpfs",
                    "Named volume",
                    "Bind mount",
                    "Container registry",
                ],
                "correct": 0,
                "explanation": (
                    "tmpfs is temporary memory-backed storage intended for nonpersistent data."
                ),
            },
            {
                "id": "M01.L12.Q07",
                "section_id": "nonroot",
                "question": "Why should application containers avoid running as root when possible?",
                "options": [
                    "It reduces privilege-related security risk and host filesystem ownership problems",
                    "Root users cannot open network sockets",
                    "Docker refuses to run root processes",
                    "Nonroot execution automatically provides GPU acceleration",
                ],
                "correct": 0,
                "explanation": (
                    "Least-privilege execution reduces impact if the container is compromised and avoids common bind-mount ownership issues."
                ),
            },
            {
                "id": "M01.L12.Q08",
                "section_id": "user-defined-bridge",
                "question": "What useful feature do user-defined bridge networks provide between containers?",
                "options": [
                    "Automatic name-based DNS resolution between connected containers",
                    "Automatic public exposure of every port",
                    "A separate guest OS for each container",
                    "Permanent storage of container files",
                ],
                "correct": 0,
                "explanation": (
                    "The source highlights Docker's embedded DNS for containers on user-defined networks."
                ),
            },
            {
                "id": "M01.L12.Q09",
                "section_id": "published-ports",
                "question": "Why does a PostgreSQL container not necessarily need a host-published port?",
                "options": [
                    "The application container can reach it through the shared internal Docker network",
                    "PostgreSQL never uses TCP",
                    "Containers cannot communicate internally",
                    "Publishing a port disables the database",
                ],
                "correct": 0,
                "explanation": (
                    "Internal container networking can carry service-to-service traffic without exposing every dependency to the host."
                ),
            },
            {
                "id": "M01.L12.Q10",
                "section_id": "compose",
                "question": "What is Docker Compose primarily used for?",
                "options": [
                    "Defining and managing a multicontainer application and its networks, volumes, configuration, and services",
                    "Training the LLM inside Python",
                    "Replacing Docker images with virtual machines",
                    "Writing SQL migrations",
                ],
                "correct": 0,
                "explanation": (
                    "Compose provides one declarative configuration for several related Docker resources and services."
                ),
            },
            {
                "id": "M01.L12.Q11",
                "section_id": "compose-secrets",
                "question": "Why should an API token not be hard-coded into a Dockerfile?",
                "options": [
                    "The image can be distributed and inspected, so secrets should be injected through runtime secret/configuration mechanisms",
                    "Dockerfiles cannot contain text",
                    "Secrets work only in PostgreSQL",
                    "Hard-coded tokens improve caching",
                ],
                "correct": 0,
                "explanation": (
                    "Secrets should remain outside distributable image layers."
                ),
            },
            {
                "id": "M01.L12.Q12",
                "section_id": "layer-ordering",
                "question": "Why copy `requirements.txt` and install dependencies before copying frequently changing source code?",
                "options": [
                    "Source edits can then reuse the cached dependency-installation layer",
                    "Docker requires requirements files to be the first file in every image",
                    "It publishes port 8000 automatically",
                    "It converts the image to a VM",
                ],
                "correct": 0,
                "explanation": (
                    "Stable expensive layers should come before volatile source layers to minimize cache invalidation."
                ),
            },
            {
                "id": "M01.L12.Q13",
                "section_id": "minimize-build-context",
                "question": "What is the purpose of `.dockerignore`?",
                "options": [
                    "Exclude unnecessary or sensitive paths from the Docker build context",
                    "Disable Docker networking",
                    "Create a GPU reservation",
                    "Persist PostgreSQL data",
                ],
                "correct": 0,
                "explanation": (
                    "A smaller, cleaner build context improves build performance and reduces accidental inclusion of local artifacts/secrets."
                ),
            },
            {
                "id": "M01.L12.Q14",
                "section_id": "multi-stage",
                "question": "What is the main benefit of a multi-stage Docker build?",
                "options": [
                    "Only selected runtime artifacts need to enter the final production image while build/development tools can stay behind",
                    "Every stage becomes a separate VM",
                    "It permanently disables caching",
                    "It forces all services onto the host network",
                ],
                "correct": 0,
                "explanation": (
                    "Multi-stage builds separate build/development tooling from the minimal production runtime."
                ),
            },
            {
                "id": "M01.L12.Q15",
                "section_id": "deployment-workflow",
                "type": "open",
                "question": (
                    "Design the deployment architecture for a production FastAPI GenAI service "
                    "with PostgreSQL, a model-provider API, and a public HTTPS endpoint. Explain "
                    "which deployment/hosting model you would use, how the application is containerized, "
                    "where persistent data and secrets live, which ports/services are externally exposed, "
                    "how the image is versioned and distributed, and which Docker build optimizations you "
                    "would apply to keep releases fast and reproducible."
                ),
            },
        ],

        "passing_score": 70,
    },
}
