"""M10.L01 — Infrastructure and Tooling for MLOps.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 10, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M10.L01"

MODULE_ORDER = 10

MODULE_TITLE = "ML Systems, Operations & Responsible AI"

MODULE_DESCRIPTION = (
    "Learn how ML systems are built and run in production: the infrastructure and "
    "tooling behind them (storage and compute, containers, workflow orchestration, "
    "ML platforms, model and feature stores, build-versus-buy), and the human side "
    "(UX for probabilistic systems, team structures, end-to-end ownership, and "
    "Responsible AI)."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Infrastructure and Tooling for MLOps",

    "slug": "ml-systems-design-m10-l01",

    "description": (
        "A production-focused guide to the infrastructure behind ML systems: "
        "storage and compute, cloud trade-offs, development environments, containers, "
        "schedulers and orchestrators, workflow management, deployment services, "
        "model stores, feature stores, and build-versus-buy decisions."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.5,

    "skill_tags": [
        "mlops",
        "ml-infrastructure",
        "storage",
        "compute",
        "cloud-compute",
        "resource-utilization",
        "multicloud",
        "development-environment",
        "notebooks",
        "environment-standardization",
        "containers",
        "docker",
        "container-registry",
        "container-orchestration",
        "kubernetes",
        "resource-management",
        "cron",
        "schedulers",
        "orchestrators",
        "dag",
        "workflow-management",
        "airflow",
        "argo",
        "prefect",
        "kubeflow",
        "metaflow",
        "ml-platform",
        "model-deployment",
        "model-store",
        "feature-store",
        "feature-consistency",
        "build-vs-buy",
    ],

    "prerequisite_ids": ["M09.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Infrastructure and Tooling for MLOps",

        "content": (
            "# Infrastructure and Tooling for MLOps\n"
            "\n"
            "> **Lesson:** M10.L01  \n"
            "> **Module:** ML Systems, Operations & Responsible AI  \n"
            "> **Source alignment:** Chapter 10. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why many ML problems become infrastructure problems in production.\n"
            "- Match infrastructure investment to application scale and specialization.\n"
            "- Describe the four infrastructure layers presented in the chapter.\n"
            "- Explain storage, compute units, memory, FLOPS, utilization, and I/O bandwidth.\n"
            "- Compare public cloud, private infrastructure, hybrid approaches, and multicloud trade-offs.\n"
            "- Explain why the development environment strongly affects engineering productivity.\n"
            "- Explain the strengths and reproducibility risks of notebooks.\n"
            "- Explain why teams standardize packages, language versions, and sometimes hardware environments.\n"
            "- Explain Dockerfile, image, container, and registry concepts.\n"
            "- Explain why multi-step ML systems often require multiple containers and orchestration.\n"
            "- Distinguish cron, schedulers, orchestrators, and workflow-management systems.\n"
            "- Represent ML workflows as DAGs with dependencies and conditional steps.\n"
            "- Compare the workflow-tool characteristics discussed for Airflow, Prefect, Argo, Kubeflow, and Metaflow.\n"
            "- Explain what an ML platform is and why shared ML tooling emerges as organizations mature.\n"
            "- Evaluate deployment services for online and batch inference needs.\n"
            "- Explain why a model store needs more than a serialized model binary.\n"
            "- List the major artifacts associated with a production model.\n"
            "- Explain feature management, feature computation, and feature consistency.\n"
            "- Explain how feature stores can reduce training-serving skew.\n"
            "- Reason about build-versus-buy decisions using company stage, strategic focus, and tool maturity.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Good ML logic is useless if infrastructure cannot support it\n"
            "\n"
            "Previous chapters described how to collect training data, engineer features, "
            "train models, deploy them, monitor them, and update them continually.\n"
            "\n"
            "Chapter 10 asks a different question:\n"
            "\n"
            "> **What infrastructure makes those practices possible?**\n"
            "\n"
            "A data scientist may understand the correct production workflow but still be "
            "unable to implement it because the organization lacks the right compute, data "
            "access, workflow automation, deployment tooling, or model-management systems.\n"
            "\n"
            "Good infrastructure can:\n"
            "\n"
            "- automate repetitive processes,\n"
            "- reduce specialized manual work,\n"
            "- shorten development and deployment cycles,\n"
            "- reduce opportunities for bugs,\n"
            "- make new ML use cases possible.\n"
            "\n"
            "Poorly chosen infrastructure can have the opposite effect and may be expensive "
            "to replace after many systems depend on it.\n"
            "\n"
            "[[IMAGE_NEEDED: Infrastructure as the foundation of the ML lifecycle | "
            "A stack where model development, deployment, monitoring, and continual learning "
            "sit above shared infrastructure | Learner should notice that earlier ML-system "
            "practices depend on enabling infrastructure beneath them]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Infrastructure needs depend on scale and specialization\n"
            "\n"
            "The chapter warns against copying another company's infrastructure blindly.\n"
            "\n"
            "Different organizations need different levels of investment.\n"
            "\n"
            "### Small or ad hoc use cases\n"
            "\n"
            "A team doing occasional analytics or a single small application may need little "
            "more than Python, notebooks, data-processing libraries, and a framework compatible "
            "with its deployment target.\n"
            "\n"
            "### Highly specialized systems\n"
            "\n"
            "Applications such as autonomous systems or extremely high-scale search have unusual "
            "latency, accuracy, scale, or hardware requirements and may justify custom infrastructure.\n"
            "\n"
            "### The middle of the spectrum\n"
            "\n"
            "Most companies use ML for several common business problems at reasonable scale, such as:\n"
            "\n"
            "- fraud detection,\n"
            "- price optimization,\n"
            "- churn prediction,\n"
            "- recommendation.\n"
            "\n"
            "These organizations can often benefit from increasingly standardized general-purpose "
            "ML infrastructure rather than building everything from scratch.\n"
            "\n"
            "The design principle is:\n"
            "\n"
            "> **Choose infrastructure for your actual workload, organization, and scale—not for prestige.**\n"
            "\n"
            "---\n"
            "\n"

            "## 3. The four infrastructure layers\n"
            "\n"
            "The chapter organizes ML infrastructure into four layers.\n"
            "\n"
            "| Layer | Main responsibility |\n"
            "|---|---|\n"
            "| Storage and compute | Store data and provide resources that execute ML workloads. |\n"
            "| Resource management | Schedule, coordinate, and allocate resources for jobs and services. |\n"
            "| ML platform | Provide shared ML-specific capabilities such as deployment, model stores, and feature stores. |\n"
            "| Development environment | Give practitioners a place to write, test, version, and experiment with code. |\n"
            "\n"
            "Storage and compute form the foundation because every ML workflow ultimately needs "
            "data and computation.\n"
            "\n"
            "The development environment is the layer practitioners interact with most directly.\n"
            "\n"
            "The ML platform is a higher-level shared layer that tends to emerge after an "
            "organization has multiple ML use cases and wants to reuse common capabilities.\n"
            "\n"
            "[[IMAGE_NEEDED: Four layers of ML infrastructure | "
            "A four-level stack showing storage/compute at the foundation, resource management, "
            "ML platform services, and development environment/user workflows | Learner should "
            "notice that the layers solve different but connected infrastructure problems]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Storage and compute are the physical foundation\n"
            "\n"
            "The storage layer is where data is collected and stored.\n"
            "\n"
            "It may be:\n"
            "\n"
            "- a local disk,\n"
            "- object storage,\n"
            "- a data warehouse,\n"
            "- an on-premises data center,\n"
            "- cloud storage,\n"
            "- several systems at once.\n"
            "\n"
            "The chapter focuses more heavily on compute because data-system concepts were "
            "covered earlier.\n"
            "\n"
            "The **compute layer** contains the resources and mechanisms used to execute jobs.\n"
            "\n"
            "A compute unit can be small or large:\n"
            "\n"
            "- a CPU thread,\n"
            "- a CPU or GPU core,\n"
            "- a multi-core machine,\n"
            "- a virtual machine,\n"
            "- a short-lived serverless-style unit,\n"
            "- a Spark or Ray job,\n"
            "- a Kubernetes pod.\n"
            "\n"
            "Different platforms expose different abstractions, but the underlying question "
            "is the same: **what resource executes this workload?**\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Memory, operation speed, utilization, and bandwidth\n"
            "\n"
            "A job must load data into memory before computation can operate on it.\n"
            "\n"
            "This makes two compute characteristics especially important:\n"
            "\n"
            "1. how much data can fit in memory,\n"
            "2. how quickly useful work can be executed.\n"
            "\n"
            "### Memory capacity\n"
            "\n"
            "More memory allows larger datasets, larger tensors, or larger models to remain in memory.\n"
            "\n"
            "### I/O bandwidth\n"
            "\n"
            "Memory size alone is not enough. The system also needs to move data into and out of "
            "memory quickly enough to keep compute units busy.\n"
            "\n"
            "### FLOPS\n"
            "\n"
            "Hardware is often described using floating-point operations per second.\n"
            "\n"
            "But theoretical FLOPS do not tell you how fast your particular workload will run.\n"
            "\n"
            "### Utilization\n"
            "\n"
            "If a machine can theoretically perform one million floating-point operations per "
            "unit time but your job achieves only 300,000, the utilization is approximately:\n"
            "\n"
            "```text\n"
            "utilization = achieved throughput / theoretical throughput\n"
            "            = 0.3\n"
            "            = 30%\n"
            "```\n"
            "\n"
            "Low utilization can come from memory bottlenecks, poor parallelism, unsuitable workloads, "
            "or other hardware/software mismatches.\n"
            "\n"
            "The practical advice in the source is to benchmark hardware using workloads that resemble "
            "the tasks you actually care about rather than relying only on theoretical FLOPS.\n"
            "\n"
            "[[IMAGE_NEEDED: Compute bottleneck mental model | "
            "A pipeline from storage to memory to compute, annotated with memory capacity, "
            "I/O bandwidth, theoretical FLOPS, and achieved utilization | Learner should "
            "notice that raw compute capability is useful only if data can reach it efficiently]]\n"
            "\n"
            "{{exercise:M10.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Public cloud versus private data centers\n"
            "\n"
            "Public cloud services make storage and compute easy to acquire without building "
            "a data center first.\n"
            "\n"
            "This is especially attractive for **bursty ML workloads**.\n"
            "\n"
            "A team may need a large burst of compute during experimentation, then much less "
            "afterward. Cloud elasticity lets the team increase and decrease resources rather "
            "than purchasing peak capacity permanently.\n"
            "\n"
            "### Cloud advantages emphasized in the chapter\n"
            "\n"
            "- quick startup,\n"
            "- elastic capacity,\n"
            "- lower operational burden,\n"
            "- pay for resources when needed rather than owning all peak capacity.\n"
            "\n"
            "### Cloud is elastic, not infinite\n"
            "\n"
            "Providers impose resource quotas, and highly desirable capacity may not always be "
            "available. Discounted or interruptible capacity can also complicate workload design.\n"
            "\n"
            "### Cloud cost can change the decision at scale\n"
            "\n"
            "The source explains that large organizations sometimes move selected workloads back "
            "to their own infrastructure to reduce long-term cost. This is called **cloud repatriation**.\n"
            "\n"
            "Moving away from cloud is difficult because private infrastructure requires up-front "
            "hardware investment and engineering effort.\n"
            "\n"
            "A hybrid approach is therefore common: keep some workloads in cloud while gradually "
            "running selected workloads in private infrastructure.\n"
            "\n"
            "[[IMAGE_NEEDED: Public cloud versus private infrastructure trade-off | "
            "A comparison showing cloud elasticity and low startup burden versus private "
            "infrastructure's higher up-front investment and potential long-term cost control | "
            "Learner should notice that the economically attractive option can change with scale]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Multicloud can reduce lock-in but increases complexity\n"
            "\n"
            "A **multicloud strategy** spreads workloads across multiple cloud providers.\n"
            "\n"
            "Potential motivations include:\n"
            "\n"
            "- access to different provider strengths,\n"
            "- pricing flexibility,\n"
            "- reducing dependence on one vendor,\n"
            "- organizational history or acquisitions.\n"
            "\n"
            "The chapter is clear that multicloud is operationally difficult.\n"
            "\n"
            "Moving data between providers, making systems compatible with multiple environments, "
            "and orchestrating workloads across clouds all increase complexity.\n"
            "\n"
            "Multicloud may also happen accidentally because independent teams choose different "
            "providers or because acquired companies bring their existing infrastructure.\n"
            "\n"
            "The principle is not that multicloud is good or bad. It is that avoiding vendor "
            "lock-in comes with real engineering cost.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. The development environment deserves serious investment\n"
            "\n"
            "The **development environment** is where engineers:\n"
            "\n"
            "- write code,\n"
            "- run experiments,\n"
            "- debug,\n"
            "- version work,\n"
            "- interact with production systems.\n"
            "\n"
            "The chapter argues that this layer is frequently underinvested even when production "
            "infrastructure is sophisticated.\n"
            "\n"
            "That is costly because engineers interact with the development environment every day.\n"
            "\n"
            "Small improvements in setup time, reproducibility, debugging, and access to compute "
            "can compound into large productivity gains.\n"
            "\n"
            "The development environment includes:\n"
            "\n"
            "- IDEs and notebooks,\n"
            "- versioning,\n"
            "- experiment tracking,\n"
            "- testing and CI/CD tooling.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Notebooks are powerful because they are stateful—and risky for the same reason\n"
            "\n"
            "Notebooks are valuable for exploratory ML work because they can contain:\n"
            "\n"
            "- code,\n"
            "- plots,\n"
            "- images,\n"
            "- tables,\n"
            "- narrative analysis.\n"
            "\n"
            "They are also **stateful**.\n"
            "\n"
            "If loading a large dataset takes a long time and cell 4 fails, the previous cells' "
            "state can remain in memory. You may only need to rerun the failed step.\n"
            "\n"
            "However, statefulness allows cells to run out of order.\n"
            "\n"
            "```text\n"
            "Expected execution:\n"
            "1 → 2 → 3 → 4\n"
            "\n"
            "Possible notebook history:\n"
            "1 → 4 → 2 → 3 → 4\n"
            "```\n"
            "\n"
            "This can make a notebook appear to work in the current session while failing from a "
            "clean restart.\n"
            "\n"
            "Therefore notebook productivity should be paired with reproducibility discipline.\n"
            "\n"
            "[[IMAGE_NEEDED: Notebook statefulness double-edged sword | "
            "One side shows quick rerun after a late-cell failure; the other shows cells executed "
            "out of order creating hidden state | Learner should notice that the same statefulness "
            "that accelerates exploration can damage reproducibility]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Standardize the environment before debugging ghosts\n"
            "\n"
            "The chapter uses several examples of bugs caused by environment differences.\n"
            "\n"
            "One engineer may use a different package version. Another may use a different Python "
            "version. A new laptop may use a different processor architecture.\n"
            "\n"
            "The code can therefore behave differently even though everyone believes they are "
            "running 'the same project.'\n"
            "\n"
            "Useful standardization includes:\n"
            "\n"
            "- exact package versions,\n"
            "- language/runtime version,\n"
            "- system dependencies,\n"
            "- environment setup instructions,\n"
            "- where appropriate, the machine environment itself.\n"
            "\n"
            "### Cloud development environments\n"
            "\n"
            "One way to standardize more aggressively is to let engineers connect to the same type "
            "of cloud machine while continuing to use their preferred local IDE through SSH.\n"
            "\n"
            "Benefits discussed in the chapter include:\n"
            "\n"
            "- fewer machine-specific setup problems,\n"
            "- easier IT support,\n"
            "- easier remote work,\n"
            "- centralized access control,\n"
            "- closer similarity between cloud development and cloud production,\n"
            "- access to data that cannot be downloaded locally.\n"
            "\n"
            "Trade-offs include cost, security policy, setup work, and the need for good cloud hygiene.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Containers make environments reproducible across machines\n"
            "\n"
            "Production services can scale across many machines. New machines need exactly the "
            "software environment required by the workload.\n"
            "\n"
            "Container technology addresses this problem.\n"
            "\n"
            "### Dockerfile\n"
            "\n"
            "A sequence of instructions describing how to construct the environment.\n"
            "\n"
            "### Docker image\n"
            "\n"
            "The packaged environment created from the Dockerfile.\n"
            "\n"
            "### Docker container\n"
            "\n"
            "A running instance of that image.\n"
            "\n"
            "Mental model:\n"
            "\n"
            "```text\n"
            "Dockerfile = recipe\n"
            "Docker image = reusable mold/template\n"
            "Container = running instance created from the image\n"
            "```\n"
            "\n"
            "Images can be built on top of existing images—for example, a framework and GPU-aware "
            "base environment plus project-specific dependencies.\n"
            "\n"
            "A **container registry** stores and distributes images for reuse.\n"
            "\n"
            "[[IMAGE_NEEDED: Dockerfile to image to containers | "
            "A Dockerfile producing one immutable image, then multiple running containers from "
            "that image, with a registry between build and deployment | Learner should notice "
            "the difference between build instructions, packaged environment, and running instances]]\n"
            "\n"
            "{{exercise:M10.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Different pipeline steps may need different containers\n"
            "\n"
            "A single ML application can contain steps with very different resource requirements.\n"
            "\n"
            "Example:\n"
            "\n"
            "- featurization: high memory, little need for GPU,\n"
            "- training: GPU-heavy, different memory profile.\n"
            "\n"
            "Running both on the same expensive GPU instance can waste resources.\n"
            "\n"
            "Separate containers allow each step to run in the environment and hardware that fits it.\n"
            "\n"
            "Containers also help when dependencies conflict—for example, two stages require incompatible "
            "versions of the same library.\n"
            "\n"
            "As the number of services grows, manual container management becomes difficult.\n"
            "\n"
            "### Container orchestration\n"
            "\n"
            "Docker Compose can coordinate containers on one host.\n"
            "\n"
            "A distributed environment requires broader orchestration. The chapter presents Kubernetes "
            "as the major example for networking, scaling, resource sharing, and maintaining service availability "
            "across hosts.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Resource management moved from scarcity optimization to cost effectiveness\n"
            "\n"
            "In fixed private data centers, compute is a hard limit. Giving more resources to one job may mean "
            "taking resources from another.\n"
            "\n"
            "Cloud elasticity changes the optimization problem.\n"
            "\n"
            "Instead of asking only:\n"
            "\n"
            "> How do we maximize utilization of fixed hardware?\n"
            "\n"
            "teams increasingly ask:\n"
            "\n"
            "> Is spending more compute justified by saved engineering time or business value?\n"
            "\n"
            "The source emphasizes that human engineering time can be more expensive than compute. "
            "Automating workloads may be economically rational even if the automation uses somewhat more hardware.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Cron, schedulers, and orchestrators solve different problems\n"
            "\n"
            "ML workflows are characterized by two things:\n"
            "\n"
            "1. they repeat,\n"
            "2. their steps depend on one another.\n"
            "\n"
            "### Cron\n"
            "\n"
            "Cron runs a command at a predetermined time.\n"
            "\n"
            "It is good for:\n"
            "\n"
            "```text\n"
            "Run this script every night at 2 a.m.\n"
            "```\n"
            "\n"
            "Cron does not naturally express complex dependencies such as:\n"
            "\n"
            "```text\n"
            "Run B only if A succeeds.\n"
            "Run C if A fails.\n"
            "```\n"
            "\n"
            "### Scheduler\n"
            "\n"
            "A scheduler understands jobs, dependencies, priorities, retries, queues, and resource requirements.\n"
            "\n"
            "It asks:\n"
            "\n"
            "> **When should each job run, and what resources does the job need?**\n"
            "\n"
            "### Orchestrator\n"
            "\n"
            "An orchestrator operates at a lower infrastructure level—machines, clusters, replicas, "
            "services, and resource provisioning.\n"
            "\n"
            "It asks:\n"
            "\n"
            "> **Where do the required resources come from, and how should the infrastructure be maintained?**\n"
            "\n"
            "The boundary is not perfectly clean. Some tools contain both scheduling and orchestration features.\n"
            "\n"
            "[[IMAGE_NEEDED: Cron versus scheduler versus orchestrator | "
            "Three layers showing fixed-time triggering by cron, dependency/resource-aware job scheduling, "
            "and machine/cluster provisioning by an orchestrator | Learner should notice that these tools "
            "operate at different abstraction levels]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. ML workflows are naturally represented as DAGs\n"
            "\n"
            "Consider this workflow:\n"
            "\n"
            "1. pull last week's data,\n"
            "2. extract features,\n"
            "3. train model A,\n"
            "4. train model B,\n"
            "5. compare A and B,\n"
            "6. deploy the winner.\n"
            "\n"
            "There are dependencies:\n"
            "\n"
            "```text\n"
            "Pull data\n"
            "    ↓\n"
            "Extract features\n"
            "   ↙       ↘\n"
            "Train A   Train B\n"
            "   ↘       ↙\n"
            "Compare models\n"
            "      ↓\n"
            "Conditional deployment\n"
            "```\n"
            "\n"
            "A **directed acyclic graph (DAG)** expresses the execution order.\n"
            "\n"
            "- **directed**: edges show which task depends on which,\n"
            "- **acyclic**: the graph cannot contain an endless dependency loop.\n"
            "\n"
            "Schedulers can use the DAG to decide when tasks are ready, how to retry failures, "
            "and what resources to allocate.\n"
            "\n"
            "[[IMAGE_NEEDED: ML workflow DAG | "
            "Data ingestion flowing into feature extraction, branching to two model-training tasks, "
            "joining at comparison, then conditionally deploying the winner | Learner should notice "
            "parallel tasks, dependencies, and conditional execution]]\n"
            "\n"
            "{{exercise:M10.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Data-science workflow-management tools operate above individual jobs\n"
            "\n"
            "Workflow-management tools let teams define multi-step workflows, often as DAGs.\n"
            "\n"
            "Each step is a **task**.\n"
            "\n"
            "A workflow may be defined using:\n"
            "\n"
            "- Python or another programming language,\n"
            "- configuration such as YAML.\n"
            "\n"
            "The workflow system then works with schedulers and orchestrators to execute each task "
            "on suitable resources.\n"
            "\n"
            "The chapter discusses Airflow, Prefect, Argo, Kubeflow, and Metaflow not to declare "
            "one universal winner, but to illustrate important workflow-tool design choices.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Airflow: configuration as code with historical limitations\n"
            "\n"
            "Airflow defines workflows in Python and provides a large ecosystem of operators for "
            "databases, clouds, containers, and other systems.\n"
            "\n"
            "The chapter highlights three limitations of the Airflow generation discussed in the source:\n"
            "\n"
            "### Monolithic workflow packaging\n"
            "\n"
            "Different steps with conflicting dependencies can be awkward to isolate, even though "
            "container operators can help.\n"
            "\n"
            "### Limited workflow parameterization\n"
            "\n"
            "Running the same logical workflow with different experiment parameters is less natural.\n"
            "\n"
            "### Static DAG structure\n"
            "\n"
            "Creating entirely new workflow steps dynamically at runtime is difficult in the model described.\n"
            "\n"
            "These limitations motivated later workflow systems to emphasize dynamic and parameterized behavior.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Prefect and Argo emphasize different improvements\n"
            "\n"
            "### Prefect\n"
            "\n"
            "The chapter presents Prefect as improving parameterized and dynamic workflows while retaining "
            "a Python-oriented 'configuration as code' approach.\n"
            "\n"
            "Containerized isolation is possible, but containers are not the central abstraction in the same "
            "way as in Argo.\n"
            "\n"
            "### Argo\n"
            "\n"
            "Argo makes each workflow step a container.\n"
            "\n"
            "Its workflows are represented declaratively in YAML and are designed around Kubernetes.\n"
            "\n"
            "This solves dependency isolation well, but the source highlights a development inconvenience: "
            "running an Argo workflow locally generally requires a Kubernetes-like environment as well.\n"
            "\n"
            "[[IMAGE_NEEDED: Workflow-tool design dimensions | "
            "A comparison matrix with Python-vs-YAML definition, dynamic workflows, parameterization, "
            "container-per-step design, Kubernetes dependence, and local/cloud execution | Learner should "
            "notice that workflow tools optimize different developer and infrastructure trade-offs]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Kubeflow and Metaflow try to bridge development and production\n"
            "\n"
            "A major ML workflow problem is that development often happens locally while full-scale execution "
            "happens in cloud or production infrastructure.\n"
            "\n"
            "Kubeflow and Metaflow aim to reduce the boilerplate required to move between those environments.\n"
            "\n"
            "### Kubeflow\n"
            "\n"
            "The chapter describes Kubeflow Pipelines as operating on top of Kubernetes/Argo-style infrastructure. "
            "It offers ML-oriented workflow abstractions but can still require substantial Docker/YAML configuration.\n"
            "\n"
            "### Metaflow\n"
            "\n"
            "The source highlights a Python/decorator experience where individual steps can declare library and "
            "resource requirements.\n"
            "\n"
            "A small step can run locally while a GPU-heavy step can be delegated to cloud batch infrastructure.\n"
            "\n"
            "The important idea is not a specific product recommendation. It is the desirable abstraction:\n"
            "\n"
            "> **Use the same logical workflow across local experimentation and production-scale execution, while "
            "letting infrastructure details change beneath each task.**\n"
            "\n"
            "---\n"
            "\n"

            "## 20. The ML platform emerges when many teams need the same capabilities\n"
            "\n"
            "Early ML teams often build tools for one application—for example, a recommender system needs deployment, "
            "features, model management, and monitoring.\n"
            "\n"
            "As more teams build ML applications, the organization discovers that many of those capabilities are shared.\n"
            "\n"
            "A dedicated **ML platform** can then provide reusable infrastructure across teams.\n"
            "\n"
            "The source focuses on three common ML-platform components:\n"
            "\n"
            "1. model deployment,\n"
            "2. model store,\n"
            "3. feature store.\n"
            "\n"
            "Monitoring is also important but was covered separately in the previous chapter.\n"
            "\n"
            "When evaluating platform tools, the chapter suggests considering at least:\n"
            "\n"
            "- compatibility with your cloud or private infrastructure,\n"
            "- open source/self-hosted versus managed service trade-offs.\n"
            "\n"
            "[[IMAGE_NEEDED: Shared ML platform across teams | "
            "Several ML applications such as fraud, churn, ranking, and pricing consuming common "
            "deployment, model-store, feature-store, and monitoring capabilities | Learner should "
            "notice why shared platform investment becomes more valuable as ML adoption grows]]\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Model deployment services should support the serving modes you actually need\n"
            "\n"
            "A deployment service helps move a model and its dependencies into production and make predictions accessible.\n"
            "\n"
            "The earlier serving distinction still matters:\n"
            "\n"
            "- online prediction generates predictions in response to requests,\n"
            "- batch prediction generates/stores predictions as batch jobs.\n"
            "\n"
            "The chapter warns not to confuse **batching online requests** with true **batch prediction**.\n"
            "\n"
            "An organization may even use separate infrastructure for these two serving patterns.\n"
            "\n"
            "A deployment platform should also make desired production tests practical, such as the controlled "
            "deployment techniques discussed in the previous chapter.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. A model store is not just a folder of serialized models\n"
            "\n"
            "Imagine a production model starts failing for a subset of inputs.\n"
            "\n"
            "The debugging team needs more than a `.pkl`, `.pt`, or other model file.\n"
            "\n"
            "They need to answer questions such as:\n"
            "\n"
            "- Who owns this model?\n"
            "- Which exact model version is live?\n"
            "- Which feature definition did it use?\n"
            "- Which featurization code produced the inputs?\n"
            "- Which data trained it?\n"
            "- Which environment/dependencies are required?\n"
            "- Which code and hyperparameters created it?\n"
            "- What evaluation results did it achieve?\n"
            "\n"
            "If these pieces live in disconnected systems with no reliable references, reproducing a production failure "
            "can become extremely difficult.\n"
            "\n"
            "This is the real purpose of a model store: **make a production model discoverable, reproducible, and maintainable.**\n"
            "\n"
            "---\n"
            "\n"

            "## 23. What should be associated with a production model?\n"
            "\n"
            "The chapter lists eight broad categories of artifacts.\n"
            "\n"
            "### 1. Model definition\n"
            "\n"
            "The structure of the model, loss definition, architecture, layer sizes, and related configuration.\n"
            "\n"
            "### 2. Model parameters\n"
            "\n"
            "The learned parameter values required to reconstruct the trained model.\n"
            "\n"
            "### 3. Featurize and predict functions\n"
            "\n"
            "The code that turns a request into model features and turns those features into a prediction.\n"
            "\n"
            "### 4. Dependencies\n"
            "\n"
            "Runtime requirements such as Python and package versions, often captured in a container.\n"
            "\n"
            "### 5. Data\n"
            "\n"
            "Pointers, identifiers, or versions describing which data generated the model.\n"
            "\n"
            "### 6. Model-generation code\n"
            "\n"
            "The training code and details such as:\n"
            "\n"
            "- framework,\n"
            "- split construction,\n"
            "- experiment count,\n"
            "- hyperparameter search space,\n"
            "- final hyperparameters.\n"
            "\n"
            "### 7. Experiment artifacts\n"
            "\n"
            "Loss curves, metrics, reports, and other outputs from model development.\n"
            "\n"
            "### 8. Tags\n"
            "\n"
            "Metadata for discovery and ownership, such as responsible team and business task.\n"
            "\n"
            "[[IMAGE_NEEDED: Model store artifact graph | "
            "A model version at the center connected to model definition, weights, feature/predict code, "
            "dependencies, data version, generation code, experiment artifacts, owner and task tags | "
            "Learner should notice that a deployable model is a bundle of related artifacts and lineage]]\n"
            "\n"
            "{{exercise:M10.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Feature stores address three core problems\n"
            "\n"
            "The term **feature store** is used differently across tools, but the chapter identifies three core problems.\n"
            "\n"
            "### 1. Feature management\n"
            "\n"
            "Different models often reuse the same features.\n"
            "\n"
            "A feature store can act as a catalog where teams:\n"
            "\n"
            "- discover existing features,\n"
            "- reuse them,\n"
            "- document ownership,\n"
            "- control access to sensitive features.\n"
            "\n"
            "### 2. Feature computation\n"
            "\n"
            "A feature definition still needs to be executed.\n"
            "\n"
            "If a feature is expensive to calculate and many models need it, compute it once and reuse/store the result "
            "rather than repeating expensive work independently.\n"
            "\n"
            "In this role, a feature store begins to resemble a specialized data system.\n"
            "\n"
            "### 3. Feature consistency\n"
            "\n"
            "Training and inference often use different execution environments.\n"
            "\n"
            "A feature may be written once in a development language for historical batch data and rewritten in another "
            "language for real-time serving.\n"
            "\n"
            "Duplicated logic increases the chance that the two feature definitions diverge.\n"
            "\n"
            "Modern feature stores aim to unify the feature definition used for batch training and online/streaming inference, "
            "reducing training-serving inconsistency.\n"
            "\n"
            "[[IMAGE_NEEDED: Feature-store three-problem model | "
            "A central feature store with three branches labeled catalog/management, computation/storage, and "
            "training-serving consistency, connected to multiple models | Learner should notice that 'feature store' "
            "can refer to several related but distinct capabilities]]\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Feature-store capabilities vary between tools\n"
            "\n"
            "The chapter emphasizes that feature stores were still an evolving category in the source's timeframe.\n"
            "\n"
            "Different systems may provide different subsets of capabilities:\n"
            "\n"
            "- feature definitions only,\n"
            "- definitions plus computation,\n"
            "- batch features,\n"
            "- online features,\n"
            "- streaming features,\n"
            "- validation against feature schemas,\n"
            "- access management and discovery.\n"
            "\n"
            "Therefore, buying something called a 'feature store' does not guarantee it solves all three problems "
            "described above. Evaluate actual capabilities against the system's needs.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Build versus buy is a strategic infrastructure decision\n"
            "\n"
            "Most companies use a mixture of managed services and in-house infrastructure.\n"
            "\n"
            "At one extreme, a vendor can manage almost the whole ML application.\n"
            "\n"
            "At the other extreme, regulatory or technical requirements may force an organization to run nearly everything itself.\n"
            "\n"
            "The chapter highlights three major decision factors.\n"
            "\n"
            "### Factor 1: company stage\n"
            "\n"
            "Early companies often benefit from vendors because speed matters more than infrastructure customization.\n"
            "\n"
            "As usage grows, vendor cost can become large enough to justify internal investment.\n"
            "\n"
            "### Factor 2: strategic advantage\n"
            "\n"
            "If a capability is central to what the company wants to be exceptionally good at, building or deeply controlling "
            "that layer may be justified.\n"
            "\n"
            "If it is not strategically differentiating, buying can save engineering effort.\n"
            "\n"
            "### Factor 3: maturity of available tools\n"
            "\n"
            "Sometimes a team wants to buy but no external product satisfies its requirements. Early adopters may therefore "
            "build custom infrastructure simply because the market is immature.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Building is not automatically cheaper\n"
            "\n"
            "Custom infrastructure has costs beyond hardware or cloud bills.\n"
            "\n"
            "You also pay for:\n"
            "\n"
            "- engineers to build it,\n"
            "- engineers to maintain it,\n"
            "- operational support,\n"
            "- migrations,\n"
            "- integrations with the rest of the stack,\n"
            "- slower adoption of new technologies when custom interfaces do not fit them.\n"
            "\n"
            "The chapter describes this last problem as a kind of **integration cost**: highly customized infrastructure "
            "can make future tools difficult to adopt.\n"
            "\n"
            "Buying also has costs:\n"
            "\n"
            "- recurring vendor fees,\n"
            "- vendor lock-in,\n"
            "- data/privacy considerations,\n"
            "- integration constraints,\n"
            "- less control over roadmap and behavior.\n"
            "\n"
            "There is no universal correct answer. Build-versus-buy is highly context dependent.\n"
            "\n"
            "{{exercise:M10.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Putting the infrastructure stack together\n"
            "\n"
            "A practical production ML stack can now be understood as connected layers:\n"
            "\n"
            "```text\n"
            "Data scientists / ML engineers\n"
            "            ↓\n"
            "Development environment\n"
            "  IDEs, notebooks, versioning, CI/CD\n"
            "            ↓\n"
            "ML platform\n"
            "  deployment, model store, feature store\n"
            "            ↓\n"
            "Workflow and resource management\n"
            "  DAGs, schedulers, orchestrators, containers\n"
            "            ↓\n"
            "Storage and compute\n"
            "  data systems, CPU/GPU, cloud/private infrastructure\n"
            "```\n"
            "\n"
            "The chapter's broader message is that **bringing ML to production is an infrastructure problem as much as a modeling problem**.\n"
            "\n"
            "The best infrastructure is not the stack with the greatest number of tools. It is the stack that lets practitioners "
            "develop, reproduce, deploy, operate, and update the organization's actual ML applications with acceptable cost and complexity.\n"
            "\n"
            "[[IMAGE_NEEDED: End-to-end MLOps infrastructure stack | "
            "A layered architecture combining development environment, shared ML platform, workflow/resource management, "
            "and storage/compute, with model-development-to-production flow through all layers | Learner should notice how "
            "the chapter's individual infrastructure components fit into one coherent system]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Every ML team needs a full ML platform\n"
            "\n"
            "Infrastructure investment should reflect use-case count, specialization, scale, and organizational needs.\n"
            "\n"
            "### Misconception 2: More theoretical FLOPS guarantees faster ML workloads\n"
            "\n"
            "Actual speed depends on utilization, data movement, memory, and workload characteristics.\n"
            "\n"
            "### Misconception 3: Cloud compute is infinite\n"
            "\n"
            "Clouds are elastic but still have quotas, capacity constraints, and operational trade-offs.\n"
            "\n"
            "### Misconception 4: Multicloud automatically protects you from every vendor problem\n"
            "\n"
            "It reduces some dependency but adds substantial data-movement and orchestration complexity.\n"
            "\n"
            "### Misconception 5: A notebook that runs once is reproducible\n"
            "\n"
            "Hidden state and out-of-order execution can make a notebook difficult to reproduce from a clean environment.\n"
            "\n"
            "### Misconception 6: Containers and virtual environments solve exactly the same problem\n"
            "\n"
            "The chapter uses containers to recreate a broader executable environment across dynamically allocated machines.\n"
            "\n"
            "### Misconception 7: Cron is a workflow orchestrator\n"
            "\n"
            "Cron handles fixed-time execution but not the rich dependencies, retries, conditions, and resource logic of ML workflows.\n"
            "\n"
            "### Misconception 8: Kubernetes and a workflow scheduler are identical\n"
            "\n"
            "Their responsibilities overlap, but the scheduler operates primarily on jobs/workflows while the orchestrator manages lower-level resources and services.\n"
            "\n"
            "### Misconception 9: A model store is simply object storage\n"
            "\n"
            "Object storage can hold a model binary, but reliable model operations require lineage, ownership, code, dependencies, data references, and experiment artifacts.\n"
            "\n"
            "### Misconception 10: Every feature store has the same capabilities\n"
            "\n"
            "The category is broad; tools differ in management, computation, streaming support, validation, and consistency features.\n"
            "\n"
            "### Misconception 11: Building infrastructure is always cheaper than buying it\n"
            "\n"
            "Building also incurs engineering, maintenance, integration, and future innovation costs.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| ML infrastructure | Fundamental facilities and systems supporting ML development and maintenance. |\n"
            "| Compute layer | Resources and mechanisms used to execute ML workloads. |\n"
            "| Compute unit | Resource abstraction that executes work, such as a thread, VM, job, or pod. |\n"
            "| FLOPS | Floating-point operations per second, a theoretical hardware throughput measure. |\n"
            "| Utilization | Fraction of theoretical compute throughput achieved by a workload. |\n"
            "| I/O bandwidth | Rate at which data can move into or out of memory/storage. |\n"
            "| Cloud elasticity | Ability to increase and decrease cloud resources as workload demand changes. |\n"
            "| Cloud repatriation | Moving selected workloads from public cloud back to private infrastructure. |\n"
            "| Multicloud | Operating workloads across more than one public cloud provider. |\n"
            "| Vendor lock-in | Difficulty moving away from a vendor because systems depend heavily on its services. |\n"
            "| Development environment | Environment where practitioners write, test, debug, and run experiments. |\n"
            "| Container | Running isolated environment instantiated from a container image. |\n"
            "| Container image | Packaged environment used to create containers. |\n"
            "| Container registry | Service for storing and distributing container images. |\n"
            "| Container orchestration | Coordinating container placement, scaling, networking, and lifecycle. |\n"
            "| Cron | Fixed-time command scheduling mechanism. |\n"
            "| Scheduler | System that decides when jobs run and allocates suitable resources. |\n"
            "| Orchestrator | System that provisions and manages lower-level compute/service resources. |\n"
            "| DAG | Directed acyclic graph expressing task dependencies. |\n"
            "| Workflow | Ordered/dependent collection of tasks implementing a larger process. |\n"
            "| ML platform | Shared ML-specific infrastructure reused across multiple applications and teams. |\n"
            "| Model store | System for model artifacts, metadata, lineage, ownership, and reproduction information. |\n"
            "| Feature store | System that may manage feature definitions, computation, storage, sharing, and training-serving consistency. |\n"
            "| Feature consistency | Ensuring a feature has the same meaning and computation in training and inference. |\n"
            "| Build versus buy | Decision whether to create/operate infrastructure internally or use external products/services. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why can infrastructure prevent a team from applying otherwise correct ML practices?\n"
            "2. Why should infrastructure investment depend on company scale and application specialization?\n"
            "3. What are the four infrastructure layers in this chapter?\n"
            "4. What does the compute layer provide?\n"
            "5. Why does memory capacity matter for an ML workload?\n"
            "6. Why can theoretical FLOPS differ greatly from realized performance?\n"
            "7. What does utilization measure?\n"
            "8. Why is I/O bandwidth important even on powerful hardware?\n"
            "9. Why is public cloud attractive for bursty ML workloads?\n"
            "10. What is cloud repatriation?\n"
            "11. What benefit and cost come with multicloud?\n"
            "12. Why does investment in the development environment improve productivity directly?\n"
            "13. Why are notebooks useful for experiments?\n"
            "14. How can notebook state hurt reproducibility?\n"
            "15. Which parts of a team development environment should usually be standardized?\n"
            "16. Why might a cloud development environment reduce dev-production differences?\n"
            "17. What is the difference between a Dockerfile, image, and container?\n"
            "18. Why might one ML pipeline use several containers?\n"
            "19. When does container orchestration become necessary?\n"
            "20. How has cloud elasticity changed the resource-management objective?\n"
            "21. What can cron do, and what important workflow capability does it lack?\n"
            "22. What is the difference between a scheduler and an orchestrator?\n"
            "23. Why are DAGs useful for ML workflows?\n"
            "24. What is a conditional dependency?\n"
            "25. What design limitations of Airflow does the source highlight?\n"
            "26. How do Prefect and Argo differ in the chapter's framing?\n"
            "27. What problem do Kubeflow and Metaflow try to solve between dev and prod?\n"
            "28. Why does an ML platform become more useful as ML adoption grows?\n"
            "29. What deployment-service capabilities should be checked for batch and online prediction?\n"
            "30. Why is storing only a model binary insufficient for production maintenance?\n"
            "31. What eight artifact categories does the chapter associate with a model store?\n"
            "32. What are the three core feature-store problems?\n"
            "33. How can a feature store reduce training-serving skew?\n"
            "34. Why should feature-store products be evaluated by capabilities rather than category name?\n"
            "35. What three factors guide build-versus-buy decisions in the chapter?\n"
            "36. Why can custom infrastructure carry a future innovation cost?\n"
            "37. How do all four infrastructure layers combine into an end-to-end MLOps system?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**MLOps infrastructure should remove friction from correct ML engineering. "
            "The goal is not to collect the most tools; it is to give teams reproducible "
            "development environments, appropriate compute, reliable workflow automation, "
            "and shared model/feature capabilities that fit the organization's real scale, "
            "constraints, and strategic priorities.**\n"
        ),

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "infra-enabler", "title": "Good ML logic is useless if infrastructure cannot support it", "order": 1},
            {"id": "infra-scale", "title": "Infrastructure needs depend on scale and specialization", "order": 2},
            {"id": "four-layers", "title": "The four infrastructure layers", "order": 3},
            {"id": "storage-compute", "title": "Storage and compute are the physical foundation", "order": 4},
            {"id": "compute-metrics", "title": "Memory, operation speed, utilization, and bandwidth", "order": 5},
            {"id": "public-private-cloud", "title": "Public cloud versus private data centers", "order": 6},
            {"id": "multicloud", "title": "Multicloud can reduce lock-in but increases complexity", "order": 7},
            {"id": "dev-environment", "title": "The development environment deserves serious investment", "order": 8},
            {"id": "notebooks", "title": "Notebooks are powerful because they are stateful—and risky for the same reason", "order": 9},
            {"id": "standardizing-dev", "title": "Standardize the environment before debugging ghosts", "order": 10},
            {"id": "containers", "title": "Containers make environments reproducible across machines", "order": 11},
            {"id": "multi-container", "title": "Different pipeline steps may need different containers", "order": 12},
            {"id": "resource-management", "title": "Resource management moved from scarcity optimization to cost effectiveness", "order": 13},
            {"id": "cron-scheduler-orchestrator", "title": "Cron, schedulers, and orchestrators solve different problems", "order": 14},
            {"id": "dag-workflow", "title": "ML workflows are naturally represented as DAGs", "order": 15},
            {"id": "workflow-management", "title": "Data-science workflow-management tools operate above individual jobs", "order": 16},
            {"id": "airflow", "title": "Airflow: configuration as code with historical limitations", "order": 17},
            {"id": "prefect-argo", "title": "Prefect and Argo emphasize different improvements", "order": 18},
            {"id": "kubeflow-metaflow", "title": "Kubeflow and Metaflow try to bridge development and production", "order": 19},
            {"id": "ml-platform", "title": "The ML platform emerges when many teams need the same capabilities", "order": 20},
            {"id": "deployment-platform", "title": "Model deployment services should support the serving modes you actually need", "order": 21},
            {"id": "model-store", "title": "A model store is not just a folder of serialized models", "order": 22},
            {"id": "model-artifacts", "title": "What should be associated with a production model?", "order": 23},
            {"id": "feature-store", "title": "Feature stores address three core problems", "order": 24},
            {"id": "feature-store-variation", "title": "Feature-store capabilities vary between tools", "order": 25},
            {"id": "build-buy", "title": "Build versus buy is a strategic infrastructure decision", "order": 26},
            {"id": "hidden-costs-build-buy", "title": "Building is not automatically cheaper", "order": 27},
            {"id": "chapter-model", "title": "Putting the infrastructure stack together", "order": 28},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M10.L01.EX01",
            "title": "Choose compute from workload constraints",
            "lesson_code": "M10.L01",
            "section_id": "compute-metrics",
            "placement": "after_section",
            "description": (
                "Reason about compute capacity using memory, bandwidth, utilization, "
                "and workload behavior rather than theoretical FLOPS alone."
            ),
            "instructions": (
                "You need to choose compute for two workloads:\n\n"
                "A. A feature job that loads very large arrays and performs relatively simple operations.\n"
                "B. A training job that performs heavy tensor computation on data that comfortably fits in memory.\n\n"
                "For each workload:\n"
                "1. identify whether memory capacity, I/O bandwidth, or compute throughput is likely to matter most,\n"
                "2. explain why theoretical FLOPS alone is insufficient,\n"
                "3. state what real benchmark you would run,\n"
                "4. explain how low utilization would change your interpretation of the hardware specification."
            ),
            "expected_output": (
                "A short compute-selection analysis grounded in memory, bandwidth, achieved utilization, "
                "and workload-specific benchmarking."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "compute-selection",
                "utilization",
                "memory-bandwidth",
                "benchmarking",
            ],
        },

        {
            "id": "M10.L01.EX02",
            "title": "Make a development environment reproducible",
            "lesson_code": "M10.L01",
            "section_id": "containers",
            "placement": "after_section",
            "description": (
                "Design an environment strategy that reduces 'works on my machine' failures."
            ),
            "instructions": (
                "A four-person ML team has these problems:\n"
                "- different Python versions,\n"
                "- unpinned package versions,\n"
                "- one ARM laptop and three x86 laptops,\n"
                "- notebooks that work only when cells are executed in a particular hidden order,\n"
                "- production runs in cloud containers.\n\n"
                "Design a reproducibility plan covering:\n"
                "1. package/runtime standardization,\n"
                "2. notebook execution discipline,\n"
                "3. local versus cloud development,\n"
                "4. Dockerfile/image usage,\n"
                "5. how the plan reduces the dev-production gap."
            ),
            "expected_output": (
                "A concrete environment standardization plan using source-supported practices."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "environment-standardization",
                "notebook-reproducibility",
                "containers",
                "dev-prod-consistency",
            ],
        },

        {
            "id": "M10.L01.EX03",
            "title": "Turn an ML pipeline into a DAG",
            "lesson_code": "M10.L01",
            "section_id": "dag-workflow",
            "placement": "after_section",
            "description": (
                "Practice separating time scheduling, task dependencies, and resource provisioning."
            ),
            "instructions": (
                "You need a weekly pipeline that:\n"
                "1. pulls data,\n"
                "2. validates data,\n"
                "3. extracts features,\n"
                "4. trains model A and model B in parallel,\n"
                "5. evaluates both,\n"
                "6. deploys the winner only if it passes a quality threshold,\n"
                "7. retries training once if one training task fails.\n\n"
                "Draw or describe the DAG, then identify:\n"
                "- what cron alone could do,\n"
                "- what requires a scheduler,\n"
                "- what an orchestrator would manage,\n"
                "- which tasks could use different containers/hardware."
            ),
            "expected_output": (
                "A dependency-aware DAG plus a correct mapping from workflow requirements "
                "to cron, scheduler, orchestrator, and container responsibilities."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "dag-design",
                "scheduling",
                "orchestration",
                "resource-management",
            ],
        },

        {
            "id": "M10.L01.EX04",
            "title": "Design model-store and feature-store metadata",
            "lesson_code": "M10.L01",
            "section_id": "model-artifacts",
            "placement": "after_section",
            "description": (
                "Practice designing shared ML-platform capabilities for debugging and reuse."
            ),
            "instructions": (
                "Your company operates fraud, churn, and recommendation models.\n\n"
                "1. List the artifact categories you would attach to each model version in the model store.\n"
                "2. Explain how ownership tags help during incidents.\n"
                "3. Propose three features that two models might share.\n"
                "4. Explain how a feature catalog would help discovery and access control.\n"
                "5. Explain when feature computation should be cached/reused.\n"
                "6. Explain how one shared feature definition can reduce training-serving skew."
            ),
            "expected_output": (
                "A compact ML-platform design connecting model reproducibility, ownership, "
                "feature reuse, feature computation, and feature consistency."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "model-store",
                "model-lineage",
                "feature-store",
                "feature-consistency",
            ],
        },

        {
            "id": "M10.L01.EX05",
            "title": "Make a build-versus-buy decision",
            "lesson_code": "M10.L01",
            "section_id": "hidden-costs-build-buy",
            "placement": "after_section",
            "description": (
                "Apply the chapter's strategic framework rather than assuming build or buy is always better."
            ),
            "instructions": (
                "Compare two organizations:\n\n"
                "Company A is an early-stage retail startup with six engineers and wants to launch a recommendation system quickly.\n"
                "Company B is a mature technology company whose recommendation infrastructure is a major competitive advantage "
                "and whose data has strict internal requirements.\n\n"
                "For each company:\n"
                "1. identify where you would initially lean toward managed services versus internal systems,\n"
                "2. justify the decision using company stage,\n"
                "3. discuss whether the capability is strategically differentiating,\n"
                "4. discuss tool-market maturity,\n"
                "5. identify one hidden cost of building and one hidden cost of buying."
            ),
            "expected_output": (
                "Two context-sensitive infrastructure strategies rather than a universal build-or-buy answer."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "build-vs-buy",
                "infrastructure-strategy",
                "vendor-lock-in",
                "engineering-cost",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M10.L01.QZ01",

        "title": "Infrastructure and Tooling for MLOps — Knowledge Check",

        "lesson_code": "M10.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M10.L01.Q01",
                "section_id": "infra-scale",
                "question": "Which principle best matches the chapter's view of ML infrastructure?",
                "options": [
                    "Every company should copy the infrastructure of the largest technology companies.",
                    "Infrastructure should match the number, scale, and specialization of the organization's ML applications.",
                    "Every ML project requires Kubernetes.",
                    "Infrastructure matters only after a model fails.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes that infrastructure requirements vary dramatically by workload and organization."
                ),
            },

            {
                "id": "M10.L01.Q02",
                "section_id": "four-layers",
                "question": "Which is NOT one of the four infrastructure layers presented in the chapter?",
                "options": [
                    "Storage and compute",
                    "Resource management",
                    "ML platform",
                    "Marketing automation",
                ],
                "correct": 3,
                "explanation": (
                    "The fourth layer is the development environment."
                ),
            },

            {
                "id": "M10.L01.Q03",
                "section_id": "storage-compute",
                "question": "What is the main role of the compute layer?",
                "options": [
                    "Only store model documentation.",
                    "Provide resources and mechanisms for executing ML workloads.",
                    "Replace feature engineering.",
                    "Only schedule meetings.",
                ],
                "correct": 1,
                "explanation": (
                    "The compute layer is the execution engine for training, feature computation, inference, and other jobs."
                ),
            },

            {
                "id": "M10.L01.Q04",
                "section_id": "compute-metrics",
                "question": "Why can a machine's advertised FLOPS overstate your workload's real performance?",
                "options": [
                    "FLOPS measure disk size.",
                    "Actual utilization can be limited by memory, bandwidth, workload structure, and software efficiency.",
                    "FLOPS are only used for text models.",
                    "Every workload always achieves 100% utilization.",
                ],
                "correct": 1,
                "explanation": (
                    "Theoretical throughput is different from achieved workload throughput."
                ),
            },

            {
                "id": "M10.L01.Q05",
                "section_id": "public-private-cloud",
                "question": "Why is cloud compute especially attractive for bursty ML development?",
                "options": [
                    "Teams can temporarily scale resources up and down instead of permanently owning peak capacity.",
                    "Cloud resources are always free.",
                    "Cloud compute has no quotas.",
                    "Cloud eliminates data movement.",
                ],
                "correct": 0,
                "explanation": (
                    "Elastic resource allocation is valuable when experimental compute needs vary strongly over time."
                ),
            },

            {
                "id": "M10.L01.Q06",
                "section_id": "multicloud",
                "question": "What is a major cost of multicloud?",
                "options": [
                    "It removes all vendor choices.",
                    "Moving data and orchestrating compatible workloads across providers is complex.",
                    "It prevents teams from using cloud services.",
                    "It guarantees lower cost.",
                ],
                "correct": 1,
                "explanation": (
                    "Reduced provider dependence comes with integration and orchestration complexity."
                ),
            },

            {
                "id": "M10.L01.Q07",
                "section_id": "notebooks",
                "question": "Why can notebook statefulness harm reproducibility?",
                "options": [
                    "Notebooks cannot display data.",
                    "Cells can be executed out of order, leaving hidden state that a clean run does not reproduce.",
                    "Notebooks cannot run Python.",
                    "Statefulness deletes previous results.",
                ],
                "correct": 1,
                "explanation": (
                    "A notebook can depend on execution history that is not obvious from the visible top-to-bottom cell order."
                ),
            },

            {
                "id": "M10.L01.Q08",
                "section_id": "standardizing-dev",
                "question": "What is a primary reason to standardize package and Python versions?",
                "options": [
                    "To make every engineer use the same IDE theme.",
                    "To reduce environment-specific bugs and inconsistent behavior.",
                    "To prevent version control.",
                    "To eliminate the need for tests.",
                ],
                "correct": 1,
                "explanation": (
                    "Different dependency or runtime versions can cause code to behave differently across machines."
                ),
            },

            {
                "id": "M10.L01.Q09",
                "section_id": "containers",
                "question": "What is a Docker image?",
                "options": [
                    "A running process created from a container.",
                    "The packaged environment built from Dockerfile instructions and used to create containers.",
                    "A data warehouse.",
                    "A workflow DAG.",
                ],
                "correct": 1,
                "explanation": (
                    "A container is the running instance; the image is the reusable packaged environment."
                ),
            },

            {
                "id": "M10.L01.Q10",
                "section_id": "multi-container",
                "question": "Why might featurization and training use separate containers?",
                "options": [
                    "Different steps can require different dependencies and hardware profiles.",
                    "A container can execute only one line of code.",
                    "Training cannot run on GPUs inside containers.",
                    "Feature code cannot access memory.",
                ],
                "correct": 0,
                "explanation": (
                    "Separate containers let each task use appropriate dependencies and compute resources."
                ),
            },

            {
                "id": "M10.L01.Q11",
                "section_id": "resource-management",
                "question": "How does cloud elasticity change resource-management thinking?",
                "options": [
                    "Resources no longer have any cost.",
                    "The focus can shift from only maximizing fixed-resource utilization toward cost-effective automation and productivity.",
                    "Schedulers are no longer useful.",
                    "All jobs should receive maximum compute.",
                ],
                "correct": 1,
                "explanation": (
                    "Elastic resources make engineering time and economic return more central to allocation decisions."
                ),
            },

            {
                "id": "M10.L01.Q12",
                "section_id": "cron-scheduler-orchestrator",
                "question": "What can a scheduler do that cron alone does not naturally express?",
                "options": [
                    "Run a command at a fixed time.",
                    "Manage task dependencies, retries, queues, priorities, and resource requirements.",
                    "Execute shell scripts.",
                    "Read the system clock.",
                ],
                "correct": 1,
                "explanation": (
                    "Cron is mainly fixed-time execution, while schedulers understand richer workflow state."
                ),
            },

            {
                "id": "M10.L01.Q13",
                "section_id": "cron-scheduler-orchestrator",
                "question": "What is the chapter's conceptual distinction between a scheduler and an orchestrator?",
                "options": [
                    "A scheduler reasons mainly about jobs and timing/resources; an orchestrator manages lower-level machines, clusters, and services.",
                    "There is always a perfect and non-overlapping boundary.",
                    "Schedulers only run locally.",
                    "Orchestrators cannot provision resources.",
                ],
                "correct": 0,
                "explanation": (
                    "The tools can overlap, but the chapter distinguishes job/workflow abstractions from lower-level infrastructure management."
                ),
            },

            {
                "id": "M10.L01.Q14",
                "section_id": "dag-workflow",
                "question": "Why must a workflow DAG be acyclic?",
                "options": [
                    "A dependency cycle could cause the workflow to wait or repeat indefinitely.",
                    "A DAG cannot have more than two tasks.",
                    "Only model-training tasks can appear in a DAG.",
                    "Cycles improve reproducibility.",
                ],
                "correct": 0,
                "explanation": (
                    "A dependency graph for a finite workflow needs a valid execution order rather than circular dependencies."
                ),
            },

            {
                "id": "M10.L01.Q15",
                "section_id": "airflow",
                "question": "Which limitation does the chapter associate with the Airflow design it discusses?",
                "options": [
                    "It cannot define workflows in Python.",
                    "DAGs are described as static and not naturally parameterized.",
                    "It requires every task to be written in C.",
                    "It has no concept of task dependencies.",
                ],
                "correct": 1,
                "explanation": (
                    "The source uses static DAGs and limited parameterization as examples of limitations later tools tried to address."
                ),
            },

            {
                "id": "M10.L01.Q16",
                "section_id": "prefect-argo",
                "question": "What is emphasized about Argo in the chapter?",
                "options": [
                    "Every workflow step is container-oriented and the system is built around Kubernetes.",
                    "It cannot use containers.",
                    "It only supports notebooks.",
                    "It requires no configuration.",
                ],
                "correct": 0,
                "explanation": (
                    "Argo strongly embraces container-per-step execution on Kubernetes."
                ),
            },

            {
                "id": "M10.L01.Q17",
                "section_id": "kubeflow-metaflow",
                "question": "What broad problem do Kubeflow and Metaflow try to reduce?",
                "options": [
                    "The gap and boilerplate between local ML development and production-scale execution.",
                    "The number of possible labels.",
                    "Feature normalization.",
                    "Cloud billing itself.",
                ],
                "correct": 0,
                "explanation": (
                    "Both aim to let practitioners express ML workflows while infrastructure details are handled more systematically."
                ),
            },

            {
                "id": "M10.L01.Q18",
                "section_id": "ml-platform",
                "question": "Why does a shared ML platform tend to emerge as organizations mature?",
                "options": [
                    "Many ML applications need the same deployment, model-management, and feature capabilities.",
                    "Each model requires entirely unique infrastructure.",
                    "ML platforms remove the need for compute.",
                    "Only recommendation systems can use shared tools.",
                ],
                "correct": 0,
                "explanation": (
                    "Shared platform investment avoids rebuilding the same operational capabilities for every ML use case."
                ),
            },

            {
                "id": "M10.L01.Q19",
                "section_id": "deployment-platform",
                "question": "Why should a deployment service be evaluated for both online and batch prediction?",
                "options": [
                    "The two modes have different serving requirements, and good support for one does not guarantee good support for the other.",
                    "They are identical.",
                    "Batch prediction means only batching API requests.",
                    "Online prediction requires no deployment tool.",
                ],
                "correct": 0,
                "explanation": (
                    "True batch prediction and request-time inference are distinct workloads."
                ),
            },

            {
                "id": "M10.L01.Q20",
                "section_id": "model-store",
                "question": "Why is storing only the serialized model insufficient?",
                "options": [
                    "Production debugging may require code, feature logic, data/version references, dependencies, ownership, and experiment history.",
                    "Serialized models cannot be loaded.",
                    "A model store should contain only dashboards.",
                    "The model's owner never matters.",
                ],
                "correct": 0,
                "explanation": (
                    "A model artifact must be connected to the context required to reproduce and maintain it."
                ),
            },

            {
                "id": "M10.L01.Q21",
                "section_id": "model-artifacts",
                "question": "Which is one of the artifact categories associated with a model store?",
                "options": [
                    "Model-generation code and hyperparameter details",
                    "Only the company logo",
                    "Only user-interface screenshots",
                    "The engineer's IDE color theme",
                ],
                "correct": 0,
                "explanation": (
                    "Generation code is essential for reproducing how the production model was created."
                ),
            },

            {
                "id": "M10.L01.Q22",
                "section_id": "feature-store",
                "question": "Which three feature-store problems does the chapter emphasize?",
                "options": [
                    "Feature management, feature computation, and feature consistency",
                    "CPU scheduling, GPU drivers, and networking",
                    "Model pruning, quantization, and distillation",
                    "A/B testing, shadowing, and canaries",
                ],
                "correct": 0,
                "explanation": (
                    "Those three capabilities capture the main feature-store roles described in the source."
                ),
            },

            {
                "id": "M10.L01.Q23",
                "section_id": "build-buy",
                "question": "Which is NOT one of the three build-versus-buy factors highlighted by the chapter?",
                "options": [
                    "Company stage",
                    "Strategic competitive advantage",
                    "Maturity of available tools",
                    "The personal favorite cloud of one engineer",
                ],
                "correct": 3,
                "explanation": (
                    "The decision framework is organizational and strategic, not based on one person's preference."
                ),
            },

            {
                "id": "M10.L01.Q24",
                "section_id": "chapter-model",
                "type": "open",
                "question": (
                    "Design a minimal MLOps infrastructure for a company that has three production models "
                    "and a ten-person ML/data team. Cover storage/compute, development environment, containers, "
                    "workflow scheduling/orchestration, deployment, model-store metadata, feature sharing, and "
                    "one build-versus-buy decision. Explain why your design is appropriate for this scale rather "
                    "than copying the infrastructure of a much larger company."
                ),
            },
        ],

        "passing_score": 70,
    },
}
