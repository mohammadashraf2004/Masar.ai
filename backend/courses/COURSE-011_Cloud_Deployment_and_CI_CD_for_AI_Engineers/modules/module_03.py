"""M03.L01 — Introduction to Containerization with Docker.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 4, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Containerization with Docker"

MODULE_DESCRIPTION = (
    "Understand why containers solve environment-consistency problems, then build, "
    "run, inspect, compose, and publish Docker-based applications using a practical "
    "Flask example."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introduction to Containerization with Docker",

    "slug": "introduction-containerization-docker-m03-l01",

    "description": (
        "Learn the core container mental model, compare containers with virtual "
        "machines, build a Docker image from a Dockerfile, manage containers and "
        "images, define local multi-container workflows with Docker Compose, and "
        "publish versioned images to Docker Hub."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "docker",
        "containers",
        "containerization",
        "dockerfile",
        "docker-images",
        "docker-compose",
        "docker-hub",
        "image-registry",
        "ports",
        "volumes",
    ],

    "prerequisite_ids": ["M02.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to Containerization with Docker",

        "content": r"""
# Introduction to Containerization with Docker

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M03.L01  
> **Module:** Containerization with Docker  
> **Source alignment:** BOOK-XXX, Chapter 4. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the "it works on my machine" problem using the idea of environmental drift.
- Compare the architecture and trade-offs of containers and virtual machines.
- Distinguish a Docker image, a Dockerfile, and a running container.
- Write and explain a beginner Dockerfile using `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, and `CMD`.
- Explain why `.dockerignore` matters for build size, speed, and avoiding accidental file inclusion.
- Build a Docker image with `docker build`.
- Run a container with port mapping, detached mode, and a custom name.
- Inspect logs and manage container lifecycle with common Docker commands.
- Manage local Docker images.
- Explain why Docker Compose helps manage multi-service applications.
- Read a simple Compose YAML file and explain `services`, `build`, `ports`, and `volumes`.
- Use the modern `docker compose` command family and recognize legacy `docker-compose`.
- Explain what an image registry is.
- Tag and push a versioned Docker image to Docker Hub.
- Connect the local build-run-push workflow to the CI/CD process introduced earlier.

---

## 1. Why containers exist: the environmental drift problem

Before learning Docker commands, you need to understand the problem Docker is solving.

A very common software-development failure sounds like this:

> "It works on my machine."

The developer may be telling the truth.

The application really may work on their laptop.

But the testing server or production server may be different.

For example:

```text
Developer laptop
Python 3.9
Library A installed
Environment variable configured
OS patch level X

Production server
Python 3.8
Library A missing
Environment variable missing
OS patch level Y
```

The application code might be identical, yet the runtime environment is not.

The source calls this **environmental drift**.

### What causes environmental drift?

Differences may appear in:

- language/runtime versions,
- installed libraries,
- system packages,
- environment variables,
- operating-system configuration,
- patch levels,
- local tools and utilities.

The more manually configured an environment becomes, the easier it is for two systems to drift apart.

That creates several problems:

- development and production behave differently,
- bugs are difficult to reproduce,
- setup instructions grow longer,
- deployment becomes fragile,
- engineers spend time debugging the environment instead of the application.

### The container idea

Containers address this by packaging the application with the user-space dependencies it needs.

Instead of saying:

```text
"Install these packages,
use this runtime version,
configure these files,
and hopefully it works."
```

you build a standardized application package.

A useful mental model is:

```text
Application
+
required libraries
+
runtime expectations
+
startup command
=
container image
```

Then any machine capable of running the container platform can run that packaged environment much more consistently.

The key DevOps benefit is **reproducibility**.

You want the same application artifact to move through:

```text
developer machine
        ↓
CI pipeline
        ↓
testing environment
        ↓
production
```

with fewer environment-specific surprises.

---

## 2. Containers versus virtual machines

Before containers became common, virtual machines were a major way to isolate workloads.

Both technologies provide isolation, but they do it differently.

### 2.1 Virtual machines

A **Virtual Machine (VM)** emulates a complete computer system.

A host machine runs a **hypervisor**, and each VM contains its own guest operating system.

Conceptually:

```text
Physical Host
│
├── Host OS / Hypervisor
│
├── VM 1
│   ├── Guest OS
│   ├── Libraries
│   └── Application
│
├── VM 2
│   ├── Guest OS
│   ├── Libraries
│   └── Application
│
└── VM 3
    ├── Guest OS
    ├── Libraries
    └── Application
```

This provides strong separation, but each VM includes a full guest operating system.

That makes VMs comparatively heavy in:

- disk usage,
- RAM,
- CPU overhead,
- startup time.

### 2.2 Containers

Containers share the host operating-system kernel.

Each container packages the application's own user-space dependencies rather than a complete guest OS.

Conceptually:

```text
Host Machine
│
├── Host OS
│
├── Container Engine
│
├── Container 1
│   ├── App
│   └── Libraries
│
├── Container 2
│   ├── App
│   └── Libraries
│
└── Container 3
    ├── App
    └── Libraries
```

[[IMAGE_NEEDED: Containers versus virtual machines | A side-by-side architecture diagram. VM side: hardware/host, hypervisor, multiple guest OS layers, each with libraries and app. Container side: hardware/host OS, container engine, multiple containers sharing the host kernel, each with libraries and app | Learner should notice that VMs repeat the guest operating system while containers share the host kernel]]

### Why this matters

The source highlights three major advantages.

#### Speed

Containers do not need to boot a full guest OS.

They can start and stop quickly.

#### Efficiency

Because they share the host kernel, many containers can often run on a host that would support fewer full VMs.

#### Portability

The application environment can be packaged into a reusable image.

That reduces the chance that the application behaves differently because of missing local dependencies.

### A useful analogy

The source compares:

```text
VM        → single-family house
Container → apartment in a shared building
```

A house is self-contained.

An apartment has a private living space but shares core building infrastructure.

The analogy is not technically perfect, but it captures the resource-efficiency idea.

### Important boundary

Containers and VMs are not simply "old versus new."

The chapter's learning goal is narrower:

> Containers are lighter because they share the host OS kernel instead of packaging a full guest OS for each workload.

{{exercise:M03.L01.EX01}}

---

## 3. Image, container, and Dockerfile: three ideas you must separate

Beginners often mix up these three terms.

### Docker image

A **Docker image** is a read-only template containing what is needed to run an application.

In the source example, that includes:

- Python runtime,
- application dependencies,
- application code,
- startup command.

Think:

> **Image = packaged blueprint.**

### Container

A **container** is a running instance of an image.

Think:

> **Container = running instance created from the blueprint.**

You can create many containers from the same image.

```text
Image: simple-flask-app
        |
        +--> Container A
        |
        +--> Container B
        |
        +--> Container C
```

### Dockerfile

A **Dockerfile** is a text file containing the build instructions Docker uses to create an image.

Think:

> **Dockerfile = recipe used to create the image.**

The relationship is:

```text
Dockerfile
    |
    | docker build
    v
Docker Image
    |
    | docker run
    v
Running Container
```

[[IMAGE_NEEDED: Dockerfile to image to container | A three-stage flow: Dockerfile instructions → `docker build` → Docker image → `docker run` → running container, with one image branching to multiple containers | Learner should notice that a Dockerfile builds an image and an image can create multiple containers]]

---

## 4. Build your first Docker image

The source uses a small Flask application because the goal is Docker, not Python complexity.

### 4.1 Create the project

```bash
cd ~/devops-book-projects
mkdir simple-flask-app && cd simple-flask-app
```

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello from inside a Docker Container!\n"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
```

Create `requirements.txt`:

```text
Flask==2.2.2
gunicorn==20.1.0
```

The source includes:

- Flask as the application framework,
- Gunicorn as the application server used inside the container.

### 4.2 Write the Dockerfile

Create a file named exactly:

```text
Dockerfile
```

with no extension.

Use:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

Now let's understand every instruction.

### `FROM`

```dockerfile
FROM python:3.9-slim
```

A Dockerfile starts from a **base image**.

Here the source uses an official Python 3.9 slim image.

The `slim` variant reduces unnecessary image size compared with a larger base.

### `WORKDIR`

```dockerfile
WORKDIR /app
```

This defines the working directory used by later instructions.

If it does not already exist, Docker creates it.

### `COPY requirements.txt .`

```dockerfile
COPY requirements.txt .
```

This copies only the dependency declaration first.

That order is deliberate.

### `RUN`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

`RUN` executes during the **image build**.

Here it installs the Python dependencies into the image.

### Why dependencies are copied before the rest of the code

The source explains this as a caching optimization.

Imagine:

```text
requirements.txt unchanged
app.py changed
```

If dependencies were already built in a reusable layer, Docker can reuse that layer instead of reinstalling the same dependencies every time.

A simplified mental model:

```text
Layer 1: Python base
Layer 2: requirements.txt
Layer 3: install dependencies
Layer 4: application source
```

If only application code changes, earlier layers may be reused.

### `COPY . .`

```dockerfile
COPY . .
```

This copies the remaining project files into the image.

But this creates a new question:

> Do we really want every local file inside the build context?

Usually, no.

### Always use `.dockerignore`

The source strongly recommends a `.dockerignore`.

Create:

```text
.dockerignore
```

Example:

```text
.git
__pycache__
*.pyc
venv/
.env
```

This prevents excluded files from being sent into the build context.

Why this matters:

- smaller build context,
- faster builds,
- less unnecessary content,
- reduced chance of including local secrets such as `.env`.

This is especially important when using:

```dockerfile
COPY . .
```

### `EXPOSE`

```dockerfile
EXPOSE 8080
```

The source makes an important distinction:

> `EXPOSE` documents the port used by the container, but it does **not** publish that port to the host by itself.

You will publish it later with `docker run -p`.

### `CMD`

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

`CMD` defines the default process that starts when a container is created from the image.

Here the container launches Gunicorn and serves the Flask app on port 8080.

### 4.3 Build the image

Run:

```bash
docker build -t simple-flask-app .
```

Break it down:

```text
docker build
    = build an image

-t simple-flask-app
    = tag/name the image

.
    = use the current directory as the build context
```

Docker then processes the Dockerfile instructions in order.

### Connection to CI

The source explicitly connects this local workflow to CI.

Today you run:

```bash
docker build ...
```

manually.

Later a CI system can:

```text
pull source
   ↓
docker build
   ↓
run tests
   ↓
push successful image
```

The Dockerfile becomes a reusable build definition across environments.

{{exercise:M03.L01.EX02}}

---

## 5. Run and manage containers

After building the image, you can create a running container.

The source command is:

```bash
docker run -p 4000:8080 -d --name my-web-server simple-flask-app
```

Let's decode it carefully.

### `-p 4000:8080`

This is a port mapping:

```text
host port 4000
       ↓
container port 8080
```

So a browser connects to the host at port 4000, while the application itself listens inside the container on port 8080.

This distinction is crucial:

```text
Browser
  |
  | localhost:4000
  v
Host port 4000
  |
  | Docker port mapping
  v
Container port 8080
  |
  v
Gunicorn / Flask app
```

[[IMAGE_NEEDED: Docker host-to-container port mapping | A network flow diagram showing Browser → localhost:4000 on host → Docker mapping → port 8080 inside container → Gunicorn/Flask | Learner should notice that host port 4000 and container port 8080 are different endpoints connected by `-p 4000:8080`]]

### `-d`

```text
-d = detached mode
```

The container runs in the background.

Without detached mode, its foreground process and logs remain attached to your terminal.

### `--name`

```bash
--name my-web-server
```

This gives the container a human-readable name.

Otherwise Docker can assign an automatically generated name.

### Image name

```text
simple-flask-app
```

is the image used to create the container.

### Inspect running containers

```bash
docker ps
```

shows running containers.

To include stopped containers:

```bash
docker ps -a
```

### Read logs

```bash
docker logs my-web-server
```

Logs are one of the first places to look when the application fails.

### Stop a container

```bash
docker stop my-web-server
```

After stopping:

```bash
docker ps
```

will no longer show it as running.

But:

```bash
docker ps -a
```

will still show the stopped container.

### Restart a stopped container

```bash
docker start my-web-server
```

### Remove a stopped container

```bash
docker rm my-web-server
```

The source notes that a running container must be stopped before normal removal.

### Container lifecycle mental model

```text
docker run
    ↓
running
    |
    | docker stop
    v
stopped
    |
    | docker start
    └──────────→ running

stopped
    |
    | docker rm
    v
removed
```

---

## 6. Manage Docker images

Containers are instances.

Images are the reusable templates those instances come from.

### List local images

```bash
docker images
```

You may see:

- your `simple-flask-app` image,
- the `python:3.9-slim` base image.

### Remove an image

```bash
docker rmi <image_name_or_id>
```

The source notes an important dependency:

If a container still references the image, even if that container is stopped, Docker may prevent normal removal of the image.

So cleanup often happens in this order:

```text
stop container
    ↓
remove container
    ↓
remove image
```

### Day-to-day command set

The chapter emphasizes these common commands:

```text
docker run
docker ps
docker logs
docker stop
docker start
docker rm
docker images
docker rmi
```

Do not memorize them as random commands.

Group them mentally:

```text
Create/run   → docker run
Inspect      → docker ps / docker logs
Lifecycle    → docker stop / docker start / docker rm
Images       → docker images / docker rmi
```

---

## 7. Docker Compose: define an application, not individual commands

A single container is useful, but real applications often include multiple services.

For example:

```text
Frontend
Backend API
Database
Cache
```

Starting each service with a long individual `docker run` command becomes difficult to manage.

Docker Compose lets you describe the application in YAML.

### Modern versus legacy command

The source highlights this distinction:

```text
docker compose
```

is the current plugin-style command.

```text
docker-compose
```

is the older standalone command.

For new work, use:

```bash
docker compose
```

### A simple Compose file

Create:

```text
docker-compose.yml
```

The source example is:

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "4000:8080"
    volumes:
      - .:/app
```

The source also notes that modern Docker Compose can treat the `version` key as optional.

### Understand the structure

#### `services`

```yaml
services:
```

This is where application services are defined.

A larger application might have:

```yaml
services:
  web:
  api:
  database:
  cache:
```

The chapter's example contains only `web`.

#### `build`

```yaml
build: .
```

Compose should build this service from the Dockerfile in the current directory.

#### `ports`

```yaml
ports:
  - "4000:8080"
```

Equivalent in concept to:

```bash
docker run -p 4000:8080 ...
```

#### `volumes`

```yaml
volumes:
  - .:/app
```

This mounts the current host project directory into `/app` inside the container.

The source describes this as a live link useful for development.

Conceptually:

```text
Host project directory
        ⇅
Container /app
```

So file edits on the host can appear inside the running container.

### Run with Compose

Modern form:

```bash
docker compose up
```

The source's walkthrough uses the older spelling in commands, but also explicitly states that the space-separated form is the current standard.

If you want a rebuild:

```bash
docker compose up --build
```

### Stop and clean up

```bash
docker compose down
```

### What Compose simplifies

Without Compose:

```text
remember multiple docker run commands
remember each port
remember each volume
remember each service name
```

With Compose:

```text
application configuration lives in YAML
        ↓
docker compose up
```

That configuration becomes part of the project and can be reviewed alongside code.

{{exercise:M03.L01.EX03}}

---

## 8. Troubleshoot common Compose failures

The source provides three very practical failure patterns.

### 8.1 Port already in use

Error concept:

```text
port 4000 is already allocated
```

This means another process or container is already using that host port.

Check:

```bash
docker ps
```

Then either:

- stop the conflicting container,
- or change the host-side port mapping.

For example:

```yaml
ports:
  - "5000:8080"
```

Now the host uses port 5000.

### 8.2 Changes not reflected

If you modify the Dockerfile or dependencies, a rebuild may be required.

Use:

```bash
docker compose up --build
```

Why?

A mounted source-code directory can update ordinary files in a running development container, but changes to the image definition or installed dependencies may require rebuilding the image.

### 8.3 Container exits immediately

Inspect service logs:

```bash
docker compose logs web
```

The source suggests that the application output often reveals the cause, such as:

- missing module,
- incorrect port,
- application crash.

### A troubleshooting habit

Do not randomly rerun commands.

Use evidence:

```text
What is running?
    ↓
docker ps

What exited?
    ↓
docker ps -a

What did it say?
    ↓
docker logs ...
or
docker compose logs ...
```

This is a DevOps pattern you will use everywhere:

> **inspect state → inspect logs → identify cause → change one thing → retest**

---

## 9. Share images through Docker Hub

So far your image exists only on your machine.

To share or deploy it elsewhere, you need an **image registry**.

The source introduces Docker Hub as the common public registry.

A useful analogy is:

```text
GitHub
stores and shares Git repositories

Docker Hub
stores and shares Docker images
```

### 9.1 Tag the image

Before pushing, the image needs a fully qualified name associated with your Docker Hub username.

Example:

```bash
docker tag simple-flask-app yourusername/simple-flask-app:1.0.0
```

Break down the target tag:

```text
yourusername
/
simple-flask-app
:
1.0.0
```

Meaning:

```text
account / repository : version tag
```

The source emphasizes that version tags such as:

```text
1.0.0
```

are important for managing image versions.

### Tagging does not rebuild the image

After:

```bash
docker tag ...
```

`docker images` may show both names.

They refer to the same underlying image content with different tags.

### 9.2 Log in

```bash
docker login
```

The chapter notes that automated CI/CD systems should use a personal access token rather than a normal password.

The learning principle is:

> Human interactive login and automated pipeline credentials should be handled appropriately for their context.

### 9.3 Push

```bash
docker push yourusername/simple-flask-app:1.0.0
```

Docker uploads the image layers to the registry.

### 9.4 Run the published image elsewhere

Once available in the registry, another Docker host can run:

```bash
docker run -p 4000:8080 yourusername/simple-flask-app:1.0.0
```

Docker can retrieve the image and create a container from it.

[[IMAGE_NEEDED: Build-run-push Docker workflow | A left-to-right diagram showing source + Dockerfile → docker build → local image → docker run → local container, with another arrow from local image → docker tag/docker push → Docker Hub registry → docker pull/run on another machine | Learner should notice that the same versioned image artifact can move from local development to a registry and then to another environment]]

### The core Docker delivery pattern

The chapter ends with a fundamental pattern:

```text
Build
  ↓
Run
  ↓
Verify
  ↓
Tag
  ↓
Push
```

And in a future CI/CD pipeline:

```text
Git push
   ↓
CI builds image
   ↓
tests
   ↓
registry push
   ↓
deployment
```

This is why Docker fits so naturally into DevOps.

---

## Important misconceptions

### Misconception 1

> "A Docker image is a running application."

### Why this is wrong

The image is the reusable template.

A container is a running instance created from that image.

---

### Misconception 2

> "`EXPOSE 8080` makes the application available on localhost automatically."

### Why this is wrong

The source explicitly distinguishes documenting the container port from publishing it.

A host-to-container mapping is created with something such as:

```bash
-p 4000:8080
```

---

### Misconception 3

> "Containers are just smaller VMs."

### Why this is incomplete

The architectural distinction in the chapter is that VMs include separate guest operating systems, while containers share the host OS kernel and package the application's user-space environment.

---

### Misconception 4

> "`COPY . .` is always harmless."

### Why this is wrong

Without `.dockerignore`, the build context may include unnecessary or sensitive local files such as:

- `.git`,
- virtual environments,
- bytecode,
- `.env`.

---

### Misconception 5

> "Docker Compose is only useful when there are many containers."

### Why this is incomplete

The source demonstrates Compose with even one service because it centralizes configuration such as:

- build instructions,
- port mappings,
- volumes.

Its value grows further as services increase.

---

### Misconception 6

> "`docker-compose` is the preferred modern command."

### Why this is wrong

The chapter explicitly states that modern installations use:

```text
docker compose
```

while the hyphenated standalone command is legacy.

---

### Misconception 7

> "A Docker Hub tag creates a new independent image build."

### Why this is wrong

Tagging creates another name/reference for the same underlying image unless you build new image content.

---

## Key terminology

| Term | Meaning |
|---|---|
| Containerization | Packaging an application and its runtime dependencies into an isolated, portable unit |
| Environmental drift | Differences between environments that cause inconsistent application behavior |
| Virtual Machine (VM) | Virtualized computer containing its own guest operating system |
| Hypervisor | Software layer used to create and run virtual machines |
| Container | Running instance of a container image |
| Docker | Platform and tooling for building, running, and sharing containers |
| Docker image | Read-only application template used to create containers |
| Dockerfile | Text file containing instructions for building a Docker image |
| Base image | Starting image named by `FROM` |
| Build context | Files Docker can access during a build from the specified path |
| `.dockerignore` | File that excludes paths from the build context |
| Layer | Reusable build result associated with Dockerfile steps |
| `EXPOSE` | Dockerfile instruction documenting the container's intended listening port |
| Port mapping | Mapping between a host port and a container port |
| Detached mode | Running a container in the background using `-d` |
| Docker Compose | Tool for defining and running applications using YAML configuration |
| Service | A named application component in a Compose file |
| Volume / bind mount | Mechanism for making host or persistent data accessible inside a container |
| Image registry | Storage/distribution service for container images |
| Docker Hub | Public Docker image registry introduced in the chapter |
| Image tag | Human-readable image name/version reference |
| `origin` | Not a Docker term; from the previous Git lesson, the default remote name after cloning |
| CI | Automated integration workflow that can build, test, and publish images |

---

## Self-check

Before moving on, make sure you can answer:

1. What is environmental drift?
2. Why can an application work locally but fail in production?
3. What is the architectural difference between containers and VMs described in the chapter?
4. What is the difference between a Dockerfile, image, and container?
5. What does `FROM python:3.9-slim` do?
6. Why does the Dockerfile copy `requirements.txt` before copying the full source?
7. Why should a project use `.dockerignore`?
8. What does `EXPOSE 8080` do, and what does it not do?
9. What does the final `.` mean in `docker build -t simple-flask-app .`?
10. Explain `-p 4000:8080`.
11. What is detached mode?
12. How do `docker ps` and `docker ps -a` differ?
13. What would you inspect first if a container exits unexpectedly?
14. Why must containers often be removed before their image can be deleted?
15. Why is Docker Compose useful?
16. What do `build`, `ports`, and `volumes` mean in the provided Compose file?
17. What is the modern Compose command syntax?
18. What should you do if a Compose host port is already in use?
19. Why might `docker compose up --build` be necessary?
20. What is an image registry?
21. What does `yourusername/simple-flask-app:1.0.0` communicate?
22. Why is a version tag useful?
23. How does the Docker workflow connect to CI/CD?

---

## Retain this idea

**Docker turns an application's runtime requirements into a repeatable image: build the image once, run consistent containers from it, and publish the versioned artifact so the same application can move through later DevOps stages.**
""",

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-containers",
                "title": "Why containers exist: the environmental drift problem",
                "order": 1,
            },
            {
                "id": "containers-vs-vms",
                "title": "Containers versus virtual machines",
                "order": 2,
            },
            {
                "id": "image-dockerfile",
                "title": "Image, container, and Dockerfile: three ideas you must separate",
                "order": 3,
            },
            {
                "id": "build-first-image",
                "title": "Build your first Docker image",
                "order": 4,
            },
            {
                "id": "run-manage",
                "title": "Run and manage containers",
                "order": 5,
            },
            {
                "id": "image-management",
                "title": "Manage Docker images",
                "order": 6,
            },
            {
                "id": "docker-compose",
                "title": "Docker Compose: define an application, not individual commands",
                "order": 7,
            },
            {
                "id": "compose-troubleshooting",
                "title": "Troubleshoot common Compose failures",
                "order": 8,
            },
            {
                "id": "docker-hub",
                "title": "Share images through Docker Hub",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Diagnose Environmental Drift",

            "lesson_code": "M03.L01",

            "section_id": "containers-vs-vms",

            "placement": "after_section",

            "description": (
                "Practice recognizing why software can behave differently across "
                "developer, test, and production environments."
            ),

            "instructions": (
                "Scenario: a Python service runs correctly on a developer laptop but fails in testing.\n"
                "Developer environment: Python 3.9, dependency X installed, APP_MODE=dev.\n"
                "Test environment: Python 3.8, dependency X missing, APP_MODE not configured.\n"
                "1. Identify every source of environmental drift in the scenario.\n"
                "2. Explain how each difference could affect the application.\n"
                "3. Explain which parts of this problem a container image can standardize.\n"
                "4. In one paragraph, compare using a container versus a full VM for this application based on the chapter's architectural explanation."
            ),

            "expected_output": (
                "A short drift-analysis table plus a comparison explaining how "
                "container packaging improves runtime consistency."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "environmental-drift",
                "containers",
                "virtual-machines",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Explain and Build the Flask Dockerfile",

            "lesson_code": "M03.L01",

            "section_id": "build-first-image",

            "placement": "after_section",

            "description": (
                "Create the chapter's Dockerfile and explain why every instruction "
                "exists rather than copying it mechanically."
            ),

            "instructions": (
                "1. Create app.py and requirements.txt using the lesson example.\n"
                "2. Create the Dockerfile with FROM, WORKDIR, COPY, RUN, EXPOSE, and CMD.\n"
                "3. Create a .dockerignore excluding .git, __pycache__, *.pyc, venv/, and .env.\n"
                "4. For every Dockerfile instruction, write one sentence explaining its purpose.\n"
                "5. Explain why requirements.txt is copied before the rest of the source.\n"
                "6. Build the image with docker build -t simple-flask-app .\n"
                "7. Record whether Docker reused any build steps on a second build after changing only app.py."
            ),

            "expected_output": (
                "A working Dockerfile and .dockerignore, the image build result, "
                "and a step-by-step explanation of the build design."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "dockerfile",
                "docker-build",
                "dockerignore",
                "build-caching",
            ],
        },

        {
            "id": "M03.L01.EX03",

            "title": "Run the Application with Docker Compose",

            "lesson_code": "M03.L01",

            "section_id": "docker-compose",

            "placement": "after_section",

            "description": (
                "Translate a manual container run configuration into a Compose YAML "
                "definition and practice the local development workflow."
            ),

            "instructions": (
                "1. Create docker-compose.yml with a web service that builds from the current directory.\n"
                "2. Map host port 4000 to container port 8080.\n"
                "3. Mount the current project directory to /app.\n"
                "4. Start the application using the modern docker compose command.\n"
                "5. Verify the application in the browser.\n"
                "6. Change the response text in app.py and determine whether the running container sees the changed file.\n"
                "7. Run docker compose logs web and inspect the output.\n"
                "8. Stop and clean up with docker compose down.\n"
                "9. Explain how this file replaces information you would otherwise need to repeat in docker run commands."
            ),

            "expected_output": (
                "A working Compose file, evidence that the service runs, and a "
                "short explanation of ports, build configuration, volumes, and cleanup."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "docker-compose",
                "yaml",
                "port-mapping",
                "volumes",
                "container-logs",
            ],
        },

        {
            "id": "M03.L01.EX04",

            "title": "Publish a Versioned Image",

            "lesson_code": "M03.L01",

            "section_id": "docker-hub",

            "placement": "after_section",

            "description": (
                "Practice the build-tag-push workflow that later CI/CD pipelines "
                "will automate."
            ),

            "instructions": (
                "1. Confirm that simple-flask-app exists locally with docker images.\n"
                "2. Tag it as your Docker Hub namespace using version 1.0.0.\n"
                "3. Run docker images again and compare the image IDs for the original and new tag.\n"
                "4. Log in to Docker Hub.\n"
                "5. Push the versioned tag.\n"
                "6. Verify that the image repository appears in Docker Hub.\n"
                "7. Write the docker run command another machine could use to run that exact version.\n"
                "8. Explain why a CI system should use a token rather than embedding a normal account password."
            ),

            "expected_output": (
                "A published versioned image plus a short explanation of image "
                "tagging, registry naming, and the build-run-push workflow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "docker-tag",
                "docker-hub",
                "docker-push",
                "image-registry",
                "versioning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Introduction to Containerization with Docker — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",

                "section_id": "why-containers",

                "question": (
                    "What does environmental drift describe?"
                ),

                "options": [
                    "A container moving between cloud regions",
                    "Differences between runtime environments that can change application behavior",
                    "A Docker image changing its tag automatically",
                    "A Git branch becoming outdated",
                ],

                "correct": 1,

                "explanation": (
                    "Environmental drift means machines differ in runtime versions, "
                    "libraries, configuration, or other environment details."
                ),
            },

            {
                "id": "M03.L01.Q02",

                "section_id": "containers-vs-vms",

                "question": (
                    "According to the chapter, what is the key architectural difference between VMs and containers?"
                ),

                "options": [
                    "Containers include a full guest OS while VMs share the host kernel",
                    "VMs require Docker Hub while containers do not",
                    "VMs include separate guest operating systems, while containers share the host OS kernel",
                    "Containers cannot isolate applications",
                ],

                "correct": 2,

                "explanation": (
                    "The chapter contrasts full guest operating systems in VMs with "
                    "containers that share the host kernel and package the application userspace."
                ),
            },

            {
                "id": "M03.L01.Q03",

                "section_id": "image-dockerfile",

                "question": (
                    "Which statement correctly describes an image and a container?"
                ),

                "options": [
                    "An image is a running process and a container is the text build file",
                    "An image is the reusable template and a container is a running instance of it",
                    "A container builds a Dockerfile into an image",
                    "They are two names for the same object",
                ],

                "correct": 1,

                "explanation": (
                    "The image is the packaged template. A container is created and run from that image."
                ),
            },

            {
                "id": "M03.L01.Q04",

                "section_id": "build-first-image",

                "question": (
                    "Why does the example copy requirements.txt and install dependencies before COPY . .?"
                ),

                "options": [
                    "Docker cannot copy Python files until dependencies are installed",
                    "It allows the dependency layer to be reused when application code changes but dependencies do not",
                    "COPY . . cannot copy requirements.txt",
                    "Gunicorn requires requirements.txt to be deleted",
                ],

                "correct": 1,

                "explanation": (
                    "The source presents this ordering as a Docker build-cache optimization."
                ),
            },

            {
                "id": "M03.L01.Q05",

                "section_id": "build-first-image",

                "question": (
                    "What is the purpose of .dockerignore in the lesson?"
                ),

                "options": [
                    "To prevent Docker from reading the Dockerfile",
                    "To exclude unnecessary or sensitive local files from the build context",
                    "To stop all containers when Docker exits",
                    "To define runtime port mappings",
                ],

                "correct": 1,

                "explanation": (
                    "The file excludes paths such as .git, venv, caches, and .env "
                    "from the build context."
                ),
            },

            {
                "id": "M03.L01.Q06",

                "section_id": "build-first-image",

                "question": (
                    "What does EXPOSE 8080 do in the supplied Dockerfile?"
                ),

                "options": [
                    "Publishes host port 8080 automatically",
                    "Documents that the containerized application listens on port 8080",
                    "Creates a cloud load balancer",
                    "Forces Docker Compose to use host port 4000",
                ],

                "correct": 1,

                "explanation": (
                    "The source explicitly says EXPOSE informs Docker about the "
                    "container port but does not publish it to the host."
                ),
            },

            {
                "id": "M03.L01.Q07",

                "section_id": "run-manage",

                "question": (
                    "In -p 4000:8080, what does 4000 represent?"
                ),

                "options": [
                    "The host-machine port",
                    "The internal application file descriptor",
                    "The image version",
                    "The Docker Hub repository ID",
                ],

                "correct": 0,

                "explanation": (
                    "The source maps host port 4000 to port 8080 inside the container."
                ),
            },

            {
                "id": "M03.L01.Q08",

                "section_id": "run-manage",

                "question": (
                    "Which command shows stopped containers as well as running containers?"
                ),

                "options": [
                    "docker ps",
                    "docker ps -a",
                    "docker images",
                    "docker logs -a",
                ],

                "correct": 1,

                "explanation": (
                    "`docker ps` shows running containers; `docker ps -a` includes stopped ones."
                ),
            },

            {
                "id": "M03.L01.Q09",

                "section_id": "docker-compose",

                "question": (
                    "Which Compose command form does the chapter identify as the modern standard?"
                ),

                "options": [
                    "docker-compose",
                    "docker compose",
                    "compose docker",
                    "docker --compose",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter identifies the Docker CLI plugin form `docker compose` "
                    "as the current standard and the hyphenated form as legacy."
                ),
            },

            {
                "id": "M03.L01.Q10",

                "section_id": "docker-compose",

                "question": (
                    "What does the Compose volume mapping .:/app do in the source example?"
                ),

                "options": [
                    "Maps host port . to container port /app",
                    "Mounts the current host project directory into /app inside the container",
                    "Uploads the image to Docker Hub",
                    "Copies /app back into the Dockerfile",
                ],

                "correct": 1,

                "explanation": (
                    "The mapping creates a live host-to-container project directory mount for development."
                ),
            },

            {
                "id": "M03.L01.Q11",

                "section_id": "compose-troubleshooting",

                "question": (
                    "A Compose service exits immediately. Which command from the lesson is most directly useful for inspecting why?"
                ),

                "options": [
                    "docker compose logs web",
                    "docker tag web",
                    "docker rmi web",
                    "docker login",
                ],

                "correct": 0,

                "explanation": (
                    "The chapter recommends inspecting the service logs for errors such as "
                    "missing modules, port problems, or application crashes."
                ),
            },

            {
                "id": "M03.L01.Q12",

                "section_id": "docker-hub",

                "question": (
                    "What is the purpose of an image registry such as Docker Hub?"
                ),

                "options": [
                    "To store and distribute Docker images",
                    "To replace the Dockerfile during local development",
                    "To run Git commits",
                    "To provide host port mappings",
                ],

                "correct": 0,

                "explanation": (
                    "The source introduces the registry as the place where images can "
                    "be stored so other machines or environments can access them."
                ),
            },

            {
                "id": "M03.L01.Q13",

                "section_id": "docker-hub",

                "type": "open",

                "question": (
                    "Describe the complete path from the Flask source code and Dockerfile "
                    "to a versioned image available on Docker Hub. Include build, local run, "
                    "verification, tagging, login, and push, and explain how a later CI "
                    "pipeline could automate the same workflow."
                ),
            },
        ],

        "passing_score": 70,
    },
}
