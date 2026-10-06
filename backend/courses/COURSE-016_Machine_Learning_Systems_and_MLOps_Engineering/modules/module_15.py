"""M14.L01 — MLOps for Azure.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 8, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M14.L01"

MODULE_ORDER = 14

MODULE_TITLE = "MLOps for Azure"

MODULE_DESCRIPTION = (
    "Learn how Azure Machine Learning supports the ML lifecycle through the CLI "
    "and Python SDK, secure authentication, reproducible compute, model and dataset "
    "versioning, online and batch deployment, local container debugging, observability, "
    "pipelines, Designer, and continuous feedback."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "MLOps for Azure",

    "slug": "practical-mlops-m14-l01-azure",

    "description": (
        "A practical Azure MLOps lesson covering CLI/SDK setup, service principals, "
        "API authentication, compute instances and clusters, model and dataset registration, "
        "ACI/AKS deployment, REST inference, troubleshooting, logs, Application Insights, "
        "local container debugging, Azure ML pipelines, published pipeline endpoints, "
        "Designer, and the iterative ML lifecycle."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.0,

    "skill_tags": [
        "azure",
        "azure-machine-learning",
        "mlops",
        "azure-cli",
        "python-sdk",
        "workspace",
        "authentication",
        "service-principal",
        "least-privilege",
        "compute-instance",
        "compute-cluster",
        "reproducible-environments",
        "model-registry",
        "dataset-versioning",
        "batch-inference",
        "online-inference",
        "aci",
        "aks",
        "rest-api",
        "deployment-debugging",
        "application-insights",
        "local-container-debugging",
        "inference-config",
        "score-script",
        "azure-ml-pipelines",
        "pipeline-publishing",
        "azure-ml-designer",
        "continuous-feedback",
    ],

    "prerequisite_ids": ["M13.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "MLOps for Azure",

        "content": (
            "# MLOps for Azure\n"
            "\n"
            "> **Lesson:** M14.L01  \n"
            "> **Module:** MLOps for Azure  \n"
            "> **Source alignment:** Chapter 8. Page numbers were not included in the supplied source. "
            "The Azure commands, deployment products, SDK classes, and defaults in this lesson follow the supplied chapter's timeframe. "
            "The source itself notes that Azure and its SDK change frequently, so these examples should be read as MLOps patterns rather "
            "than guarantees about the current Azure interface.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the chapter's view of Azure ML as a set of flexible abstractions around difficult production tasks.\n"
            "- Explain how the Azure CLI, Python SDK, and workspace configuration connect local code to Azure ML.\n"
            "- Explain why authentication belongs inside automation rather than being bypassed.\n"
            "- Define a service principal and explain why least privilege matters.\n"
            "- Distinguish authentication for automation from authentication for deployed model APIs.\n"
            "- Explain the key/token authentication differences presented for AKS and ACI in the source.\n"
            "- Explain how Azure compute instances support rapid, reproducible ML development.\n"
            "- Distinguish batch inference from online inference.\n"
            "- Explain why production models should normally be registered and versioned.\n"
            "- Register existing models conceptually using the SDK, CLI, or Studio.\n"
            "- Explain why datasets need versioning and why ordinary source-control tools are not ideal for large data artifacts.\n"
            "- Explain the role of Azure dataset references and versions.\n"
            "- Distinguish training compute from inference/deployment compute.\n"
            "- Explain how compute-cluster size, node count, and scale-to-zero affect cost and workload capacity.\n"
            "- Compare ACI and AKS using the chapter's deployment guidance.\n"
            "- Explain how a deployed model becomes an authenticated HTTP service.\n"
            "- Diagnose common HTTP deployment problems involving payloads, methods, content type, and authentication.\n"
            "- Apply the chapter's debugging rule: question assumptions, inspect details, reproduce the problem.\n"
            "- Retrieve deployment logs conceptually through the Azure SDK.\n"
            "- Explain how Application Insights contributes to observability.\n"
            "- Explain why observability needs system context rather than isolated tracebacks.\n"
            "- Deploy a model locally in a container conceptually using Azure ML's SDK abstractions.\n"
            "- Explain the roles of `score.py`, `init()`, `run()`, environment definitions, and inference configuration.\n"
            "- Explain why reproducing a production container locally is valuable.\n"
            "- Define an Azure ML pipeline as coordinated steps toward an objective.\n"
            "- Explain how datasets, script steps, outputs, compute targets, and runtime configuration fit into a pipeline.\n"
            "- Explain why publishing a pipeline as an HTTP endpoint enables external orchestration.\n"
            "- Explain where Azure ML Designer fits in the platform.\n"
            "- Describe the Azure ML lifecycle as an iterative feedback loop rather than a linear path.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Azure ML hides difficult infrastructure behind multiple interfaces\n"
            "\n"
            "The chapter opens with a practical example: deploying a machine-learning model to Kubernetes is normally a difficult infrastructure problem.\n"
            "\n"
            "Azure ML can reduce that complexity to selecting a configured cluster as the deployment target.\n"
            "\n"
            "The broader platform offers several ways to work:\n"
            "\n"
            "- Azure ML Studio,\n"
            "- Designer,\n"
            "- Jupyter Notebooks,\n"
            "- AutoML,\n"
            "- CLI,\n"
            "- Python SDK.\n"
            "\n"
            "This flexibility is important because MLOps teams do not all work the same way.\n"
            "\n"
            "The chapter does not argue for one mandatory Azure workflow. It argues for using the abstraction that best fits the task while still preserving good operational practices.\n"
            "\n"
            "[[IMAGE_NEEDED: Azure ML interface map | "
            "Azure ML at the center connected to Studio, Designer, notebooks, AutoML, CLI, and Python SDK, all reaching shared models, data, compute, and deployment services | "
            "Learner should notice that different interfaces operate on the same underlying lifecycle]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. CLI and SDK are the programmatic foundation\n"
            "\n"
            "The chapter assumes the Azure CLI and Azure ML Python SDK are installed.\n"
            "\n"
            "The CLI is used for operations such as:\n"
            "\n"
            "- installing the ML extension,\n"
            "- logging in,\n"
            "- creating identities,\n"
            "- registering models.\n"
            "\n"
            "The Python SDK connects code to an Azure ML workspace.\n"
            "\n"
            "A source-aligned example is:\n"
            "\n"
            "```python\n"
            "from azureml.core import Workspace\n"
            "\n"
            "ws = Workspace.from_config()\n"
            "```\n"
            "\n"
            "`Workspace.from_config()` depends on a local `config.json` describing the workspace association.\n"
            "\n"
            "If that configuration file cannot be found, the SDK cannot infer which workspace the code should use.\n"
            "\n"
            "The important concept is not the file name itself. It is that programmatic ML operations need a reproducible way to bind code to the correct cloud environment.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Authentication is a core part of automation, not an obstacle to remove\n"
            "\n"
            "The chapter strongly warns against 'fixing' automation by weakening permissions.\n"
            "\n"
            "Examples of dangerous shortcuts include:\n"
            "\n"
            "- using an all-powerful/root-like account because it is convenient,\n"
            "- making resources world-readable or world-writable,\n"
            "- removing authentication from test systems just to make development easier.\n"
            "\n"
            "These approaches may eliminate an immediate error while creating a much more serious security problem.\n"
            "\n"
            "The operational rule is:\n"
            "\n"
            "> **Automate authentication correctly. Do not automate by removing security constraints.**\n"
            "\n"
            "[[IMAGE_NEEDED: Secure automation versus permission bypass | "
            "Two paths: service identity with scoped permissions versus a shortcut using overly broad permissions, with the second path leading to security exposure | "
            "Learner should notice that convenience and secure automation are not the same thing]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Service principals give automated systems their own identity\n"
            "\n"
            "Azure service principals are used to authenticate automated workflows without requiring repeated interactive login.\n"
            "\n"
            "The source creates one through the CLI and then associates the identity with the Azure ML workspace/resource group.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Create service identity\n"
            "      ↓\n"
            "Identify its client/object ID\n"
            "      ↓\n"
            "Grant workspace/resource access\n"
            "      ↓\n"
            "Use identity in automation\n"
            "```\n"
            "\n"
            "The chapter's example uses a broad role, but it explicitly recommends adapting the role to the **least permissions needed**.\n"
            "\n"
            "That is the important security lesson.\n"
            "\n"
            "{{exercise:M14.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Deployed model APIs need an authentication strategy too\n"
            "\n"
            "Authentication for automation identities is one problem.\n"
            "\n"
            "Authentication for a deployed HTTP prediction API is another.\n"
            "\n"
            "The chapter discusses two broad mechanisms:\n"
            "\n"
            "- key-based authentication,\n"
            "- token-based authentication.\n"
            "\n"
            "It also explains that support/defaults differ between deployment types such as AKS and ACI in the source's timeframe.\n"
            "\n"
            "The lasting lesson is:\n"
            "\n"
            "> **Understand the security behavior of the deployment target before exposing a model.**\n"
            "\n"
            "The chapter recommends enabling authentication even in test environments so testing resembles production rather than creating a dangerous dev/prod mismatch.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Compute instances reduce setup friction for ML development\n"
            "\n"
            "Azure compute instances are described as managed cloud workstations for data scientists.\n"
            "\n"
            "They are useful for:\n"
            "\n"
            "- Jupyter notebooks,\n"
            "- tutorials and experiments,\n"
            "- preinstalled ML dependencies,\n"
            "- repeatable cloud-based environments,\n"
            "- queued jobs,\n"
            "- parallel work,\n"
            "- GPU-backed workloads where configured.\n"
            "\n"
            "The chapter's underlying DevOps point is reproducibility.\n"
            "\n"
            "A managed environment can reduce the classic problem:\n"
            "\n"
            "> 'It works on my machine.'\n"
            "\n"
            "A shared/reproducible environment gives collaborators a more normalized place to develop and debug.\n"
            "\n"
            "[[IMAGE_NEEDED: Reproducible Azure compute environment | "
            "Several engineers connecting to a managed Azure compute instance with the same libraries, notebook environment, workspace, and data access | "
            "Learner should notice how a shared environment reduces machine-specific differences]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Start small when experimenting with compute\n"
            "\n"
            "The source recommends beginning with a relatively low-cost machine for notebooks and experiments rather than immediately choosing an expensive option.\n"
            "\n"
            "This is a practical cost-control habit:\n"
            "\n"
            "```text\n"
            "Start with modest resources\n"
            "      ↓\n"
            "Measure actual need\n"
            "      ↓\n"
            "Scale compute when evidence requires it\n"
            "```\n"
            "\n"
            "The same idea appears later when configuring clusters: trial and measurement should guide resource sizing.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Choose deployment style from inference behavior\n"
            "\n"
            "The chapter distinguishes two deployment needs.\n"
            "\n"
            "### Batch inference\n"
            "\n"
            "A better fit when processing very large quantities of data in bulk rather than responding instantly to individual requests.\n"
            "\n"
            "### Online inference\n"
            "\n"
            "A better fit when clients need predictions quickly through a live HTTP service.\n"
            "\n"
            "Azure can create the serving API around a trained model, reducing the amount of custom HTTP infrastructure a team has to build.\n"
            "\n"
            "That lets the team invest more effort in data quality and deployment robustness.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Register production models even when registration is technically optional\n"
            "\n"
            "The source points out that Azure model registration is optional in the narrow sense that a model can sometimes be deployed without it.\n"
            "\n"
            "But skipping registration trades short-term convenience for long-term operational ambiguity.\n"
            "\n"
            "Versioned model registration helps teams:\n"
            "\n"
            "- identify exactly which model version is in use,\n"
            "- attach descriptions and metadata,\n"
            "- browse versions clearly,\n"
            "- roll back to a previous version.\n"
            "\n"
            "This is similar to source-code version control conceptually, even though models are different artifact types.\n"
            "\n"
            "[[IMAGE_NEEDED: Azure model registry version history | "
            "One model name with versions v1, v2, v3, each with metadata and a production pointer, plus a rollback arrow from v3 to v2 | "
            "Learner should notice why version identity matters during release and rollback]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Model registration is intentionally flexible\n"
            "\n"
            "The chapter demonstrates several ways to register models.\n"
            "\n"
            "### Register from an Azure training run\n"
            "\n"
            "```python\n"
            "model = run.register_model(description=\"AutoML trained model\")\n"
            "```\n"
            "\n"
            "### Register an existing local model with the SDK\n"
            "\n"
            "```python\n"
            "from azureml.core.model import Model\n"
            "\n"
            "model = Model.register(\n"
            "    workspace=ws,\n"
            "    model_path=\"models/world_wines.onnx\",\n"
            "    model_name=\"world_wines\",\n"
            "    tags={\"onnx\": \"world-wines\"},\n"
            "    description=\"Image classification model\",\n"
            ")\n"
            "```\n"
            "\n"
            "### Register with the CLI\n"
            "\n"
            "The source also shows a CLI-based model-registration path.\n"
            "\n"
            "This reinforces the chapter's flexibility theme: use the interface that best fits the automation context.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Dataset versioning is as important as model versioning\n"
            "\n"
            "Large datasets do not fit naturally into Git-style source control.\n"
            "\n"
            "Yet reproducible ML requires knowing which data version produced which model.\n"
            "\n"
            "Azure dataset versioning addresses that problem by allowing a dataset to be registered and assigned versions.\n"
            "\n"
            "The source emphasizes that data often changes through multiple stages:\n"
            "\n"
            "```text\n"
            "Raw data\n"
            "   ↓\n"
            "cleaning\n"
            "   ↓\n"
            "transformation\n"
            "   ↓\n"
            "training-ready data\n"
            "```\n"
            "\n"
            "Versioning makes those transitions traceable.\n"
            "\n"
            "The source also notes that a new Azure dataset version can reference storage rather than copying an entire massive dataset into the workspace.\n"
            "\n"
            "{{exercise:M14.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Training compute should match the workload—not an arbitrary maximum size\n"
            "\n"
            "The chapter creates compute as part of an AutoML run.\n"
            "\n"
            "Important cluster decisions include:\n"
            "\n"
            "- machine type,\n"
            "- RAM/CPU capability,\n"
            "- minimum nodes,\n"
            "- maximum nodes,\n"
            "- degree of parallelism.\n"
            "\n"
            "The maximum number of parallel runs cannot exceed the cluster's available maximum nodes in the source's example.\n"
            "\n"
            "Sizing is presented as an empirical process: start with modest resources and increase them as needed.\n"
            "\n"
            "The example uses a minimum node count of zero to avoid paying for idle nodes when the cluster is unused.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Training compute and inference compute are different concerns\n"
            "\n"
            "The chapter warns that the word **cluster** can create confusion.\n"
            "\n"
            "A cluster used for training is not necessarily the same infrastructure used to serve live or batch predictions.\n"
            "\n"
            "These workloads have different resource patterns:\n"
            "\n"
            "- training may prioritize parallel model fitting and throughput,\n"
            "- online inference may prioritize latency and availability,\n"
            "- batch inference may prioritize large-scale throughput over immediate response.\n"
            "\n"
            "MLOps design should therefore select compute based on the stage of the lifecycle.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. The source positions ACI and AKS for different deployment needs\n"
            "\n"
            "The source gives a practical distinction for its timeframe.\n"
            "\n"
            "### Azure Container Instances (ACI)\n"
            "\n"
            "Presented as a good fit for testing/test environments and relatively small models.\n"
            "\n"
            "### Azure Kubernetes Service (AKS)\n"
            "\n"
            "Presented as a stronger production/scaling target and suitable for larger models.\n"
            "\n"
            "The durable lesson is not the historical size threshold. It is the decision pattern:\n"
            "\n"
            "> **Use a simpler deployment target for experimentation and a more scalable orchestration target when production requirements justify it.**\n"
            "\n"
            "[[IMAGE_NEEDED: Azure deployment target trade-off | "
            "A simple test deployment path toward ACI and a scalable production deployment path toward AKS/Kubernetes | "
            "Learner should notice that target choice should follow workload and environment requirements]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. A deployed model becomes a service contract\n"
            "\n"
            "After deployment, Azure exposes model-serving details through an endpoint dashboard.\n"
            "\n"
            "A client needs to know:\n"
            "\n"
            "- endpoint URL,\n"
            "- HTTP method,\n"
            "- content type,\n"
            "- authentication mechanism,\n"
            "- request schema,\n"
            "- response schema.\n"
            "\n"
            "The source uses Python's `requests` library to call the endpoint, showing that clients do not need the Azure SDK once a normal HTTP interface exists.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "headers = {\"Content-Type\": \"application/json\"}\n"
            "headers[\"Authorization\"] = f\"Bearer {key}\"\n"
            "response = requests.post(scoring_uri, data=input_data, headers=headers)\n"
            "```\n"
            "\n"
            "The exact input schema is model-specific.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. HTTP errors often point directly to contract violations\n"
            "\n"
            "The chapter demonstrates several common failure types.\n"
            "\n"
            "### Invalid model input\n"
            "\n"
            "The runtime may fail because a required model input is missing.\n"
            "\n"
            "### Wrong content type\n"
            "\n"
            "The service may reject a request whose body is JSON but whose headers do not declare JSON correctly.\n"
            "\n"
            "### Wrong HTTP method\n"
            "\n"
            "Calling a scoring route with GET when it expects POST can produce a method error.\n"
            "\n"
            "### Malformed authorization\n"
            "\n"
            "The authentication header must match the required format.\n"
            "\n"
            "A model deployment is therefore not only a model. It is an API contract plus runtime behavior.\n"
            "\n"
            "{{exercise:M14.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Good debugging is a practiced method: question, observe, verify\n"
            "\n"
            "The chapter compares debugging to finding your way through an unfamiliar city.\n"
            "\n"
            "The useful habits are:\n"
            "\n"
            "- pay attention to details,\n"
            "- record what you observed,\n"
            "- retrace the path,\n"
            "- question assumptions,\n"
            "- trust suggestions only after validating them,\n"
            "- backtrack when evidence contradicts the hypothesis.\n"
            "\n"
            "The operational motto is:\n"
            "\n"
            "> **Never assume. Trust, but verify.**\n"
            "\n"
            "This mindset is transferable across clouds and tools.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Deployment logs reveal container startup and runtime behavior\n"
            "\n"
            "Azure deployment logs can be retrieved from Studio, CLI, or the Python SDK.\n"
            "\n"
            "A source-aligned SDK pattern is:\n"
            "\n"
            "```python\n"
            "from azureml.core.webservice import Webservice\n"
            "\n"
            "service = Webservice(ws, \"my-service\")\n"
            "logs = service.get_logs()\n"
            "print(logs)\n"
            "```\n"
            "\n"
            "Successful logs may show:\n"
            "\n"
            "- model path,\n"
            "- runtime/session initialization,\n"
            "- bound addresses/ports.\n"
            "\n"
            "The chapter cautions that logs can be noisy. Debugging requires extracting the meaningful signals rather than treating every line equally.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Application Insights adds observability beyond raw logs\n"
            "\n"
            "The source defines observability as the ability to understand the system's state using evidence such as:\n"
            "\n"
            "- dashboards,\n"
            "- aggregated logs,\n"
            "- graphs,\n"
            "- alerting,\n"
            "- response-time data,\n"
            "- failure rates,\n"
            "- exceptions.\n"
            "\n"
            "Application Insights can be enabled for a deployed Azure ML service.\n"
            "\n"
            "The value is not simply prettier graphs.\n"
            "\n"
            "It provides context for understanding how the service behaves over time.\n"
            "\n"
            "[[IMAGE_NEEDED: From logs to observability | "
            "A deployed model sending requests, failures, latency, exceptions, and logs into an Application Insights-style dashboard | "
            "Learner should notice that observability combines multiple signals into a system-level story]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. A traceback may be the symptom, not the root cause\n"
            "\n"
            "The source gives a distributed-system example.\n"
            "\n"
            "Suppose Python raises an error because it expected a JSON payload.\n"
            "\n"
            "The obvious conclusion might be: fix the Python code.\n"
            "\n"
            "But what if an upstream system sent an empty file instead of JSON?\n"
            "\n"
            "Now the root cause is elsewhere.\n"
            "\n"
            "This is why observability should tell a cross-component story.\n"
            "\n"
            "A real ML pipeline may contain:\n"
            "\n"
            "```text\n"
            "ingest → clean → remove columns → normalize → version dataset → train/serve\n"
            "```\n"
            "\n"
            "When a later stage fails, you need evidence from earlier stages too.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Reproducing production behavior locally is a powerful debugging technique\n"
            "\n"
            "The source strongly discourages making production servers the primary debugging environment.\n"
            "\n"
            "A containerized model can often be run locally using the same image/runtime style used in Azure.\n"
            "\n"
            "Benefits include:\n"
            "\n"
            "- avoid disrupting production,\n"
            "- inspect the running container,\n"
            "- inspect files and dependencies,\n"
            "- retrieve logs freely,\n"
            "- send repeated test requests,\n"
            "- change settings rapidly,\n"
            "- reproduce the problem before guessing at a fix.\n"
            "\n"
            "Reproduction is described as a 'golden ticket' for debugging.\n"
            "\n"
            "[[IMAGE_NEEDED: Production issue reproduced locally | "
            "A production Azure container and an equivalent local Docker container receiving the same failing request, with inspection tools attached locally | "
            "Learner should notice that reproducibility enables safer and deeper debugging]]\n"
            "\n"
            "---\n"
            "\n"

            "## 22. A local Azure ML deployment combines model, environment, score script, and inference config\n"
            "\n"
            "The chapter's local deployment path has several components.\n"
            "\n"
            "### Registered model\n"
            "\n"
            "The model artifact is registered with the workspace.\n"
            "\n"
            "### Environment\n"
            "\n"
            "Dependencies such as the ONNX runtime are declared.\n"
            "\n"
            "### Scoring script\n"
            "\n"
            "The source says `score.py` is model-specific and must implement the expected Azure entry points such as:\n"
            "\n"
            "- `init()` — initialize/load model state,\n"
            "- `run()` — accept request data and produce scores.\n"
            "\n"
            "### Inference configuration\n"
            "\n"
            "The inference configuration binds the scoring script to the environment.\n"
            "\n"
            "### Local web-service configuration\n"
            "\n"
            "The deployment exposes an HTTP endpoint on a local port.\n"
            "\n"
            "```text\n"
            "model + environment + score.py\n"
            "          ↓\n"
            "InferenceConfig\n"
            "          ↓\n"
            "LocalWebservice\n"
            "          ↓\n"
            "local Docker container + HTTP endpoint\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Inspect the actual container when deployment fails\n"
            "\n"
            "The source verifies the local deployment with normal Docker tooling.\n"
            "\n"
            "Inside the container, the engineer can inspect whether files such as:\n"
            "\n"
            "- `score.py`,\n"
            "- the registered model,\n"
            "- generated runtime files\n"
            "\n"
            "are present where expected.\n"
            "\n"
            "The chapter also shows a failure caused by the scoring module not exposing the expected initialization function.\n"
            "\n"
            "The error becomes much easier to diagnose locally because the container can be inspected directly.\n"
            "\n"
            "{{exercise:M14.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Azure ML pipelines coordinate multiple steps toward one objective\n"
            "\n"
            "The chapter defines pipelines in the familiar CI/CD sense: several steps work together to achieve an objective.\n"
            "\n"
            "Azure describes pipeline scenarios such as:\n"
            "\n"
            "- machine-learning workflows,\n"
            "- data preparation,\n"
            "- application orchestration.\n"
            "\n"
            "Pipelines can be created through Studio or the Python SDK.\n"
            "\n"
            "The important abstraction is the **step**.\n"
            "\n"
            "A step has inputs, outputs, code to execute, and compute on which to execute it.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. A PythonScriptStep packages a data-processing command as a pipeline stage\n"
            "\n"
            "The source creates a pipeline step that accepts a registered dataset and produces output in a datastore.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "prep_step = PythonScriptStep(\n"
            "    script_name=\"prep.py\",\n"
            "    source_directory=\"./src\",\n"
            "    arguments=[\"--input\", dataset_input, \"--output\", output],\n"
            "    inputs=[dataset_input],\n"
            "    outputs=[output],\n"
            ")\n"
            "```\n"
            "\n"
            "The source notes that this Python class behaves like a command-line tool abstraction: arguments are explicitly passed to the script.\n"
            "\n"
            "This is useful because a normal script can become a reproducible pipeline component.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Pipeline steps still need a compute target and runtime environment\n"
            "\n"
            "A step definition is incomplete without deciding where and how it runs.\n"
            "\n"
            "The chapter retrieves a previously created compute target from the workspace.\n"
            "\n"
            "A run configuration can then associate:\n"
            "\n"
            "- compute target,\n"
            "- runtime/environment behavior,\n"
            "- dependency-management settings.\n"
            "\n"
            "This separates **what the step does** from **where/how the step executes**.\n"
            "\n"
            "That separation is a recurring MLOps pattern across cloud platforms.\n"
            "\n"
            "[[IMAGE_NEEDED: Azure pipeline step anatomy | "
            "A pipeline step showing inputs, Python script/arguments, outputs, compute target, and runtime configuration | "
            "Learner should notice that execution code and execution environment are separate concerns]]\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Publishing a pipeline turns it into an externally triggerable service\n"
            "\n"
            "One of the chapter's most useful pipeline features is the ability to publish a workflow and trigger it through HTTP.\n"
            "\n"
            "That means the pipeline can be started by systems outside Azure ML, such as:\n"
            "\n"
            "- an on-premises system,\n"
            "- a source-code platform,\n"
            "- another cloud service,\n"
            "- a custom application.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "External system\n"
            "      ↓ authenticated HTTP request\n"
            "Published Azure ML pipeline\n"
            "      ↓\n"
            "Pipeline run ID\n"
            "      ↓\n"
            "coordinated Azure ML steps\n"
            "```\n"
            "\n"
            "This gives Azure ML workflows a clean integration boundary.\n"
            "\n"
            "{{exercise:M14.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Azure ML Designer provides a visual route through the same ecosystem\n"
            "\n"
            "The chapter presents Designer as a graphical way to build and run ML projects.\n"
            "\n"
            "A learner can open a sample project, inspect the pipeline visually, and submit a job.\n"
            "\n"
            "The value is educational as well as operational: exploring Designer exposes users to the surrounding Azure ML concepts such as:\n"
            "\n"
            "- datasets,\n"
            "- compute,\n"
            "- jobs,\n"
            "- AutoML,\n"
            "- reports.\n"
            "\n"
            "This reinforces the chapter's interface-flexibility principle: graphical and code-driven paths can coexist.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Azure ML services exist to support an iterative model lifecycle\n"
            "\n"
            "The chapter concludes by placing all of the individual tools into one ML lifecycle.\n"
            "\n"
            "A simplified flow is:\n"
            "\n"
            "```text\n"
            "Train\n"
            "Notebooks / AutoML / SDK\n"
            "     ↓\n"
            "Validate\n"
            "Studio / Designer / evaluation\n"
            "     ↓\n"
            "Register + version model/data\n"
            "     ↓\n"
            "Deploy\n"
            "ACI / AKS / online or batch targets\n"
            "     ↓\n"
            "Observe\n"
            "logs / Application Insights / failures\n"
            "     ↓\n"
            "Feedback\n"
            "data/model/deployment changes\n"
            "     ↺\n"
            "```\n"
            "\n"
            "The chapter explicitly rejects a purely linear interpretation.\n"
            "\n"
            "Monitoring and scaling checkboxes do not guarantee success. The system must be continuously evaluated, and observations should send the team back to earlier steps when necessary.\n"
            "\n"
            "[[IMAGE_NEEDED: Iterative Azure ML lifecycle | "
            "A circular lifecycle from training to validation, registration/versioning, deployment, observability, and feedback returning to data/training | "
            "Learner should notice that production feedback changes earlier stages rather than ending the process]]\n"
            "\n"
            "---\n"
            "\n"

            "## 30. The final lesson: ship models, do not reimplement solved cloud problems\n"
            "\n"
            "The chapter's conclusion is practical.\n"
            "\n"
            "Azure already provides mechanisms for difficult operational tasks such as:\n"
            "\n"
            "- dataset/model registration and versioning,\n"
            "- compute management,\n"
            "- containerized deployment,\n"
            "- scalable inference,\n"
            "- monitoring,\n"
            "- pipelines.\n"
            "\n"
            "MLOps engineers should leverage suitable technology instead of building incomplete substitutes simply because they can.\n"
            "\n"
            "The objective is not to reinvent the cloud platform.\n"
            "\n"
            "The objective is to build a reliable path that gets models into production and keeps improving them afterward.\n"
            "\n"
            "{{exercise:M14.L01.EX06}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Azure ML requires one opinionated workflow\n"
            "\n"
            "The chapter explicitly presents Studio, Designer, notebooks, AutoML, CLI, and SDK as alternative/complementary interfaces.\n"
            "\n"
            "### Misconception 2: Authentication slows automation, so test environments should disable it\n"
            "\n"
            "The source recommends proper authentication and environment parity rather than insecure shortcuts.\n"
            "\n"
            "### Misconception 3: A service principal should always receive the broadest possible role\n"
            "\n"
            "The chapter explicitly recommends restricting access to the minimum needed permissions.\n"
            "\n"
            "### Misconception 4: Reproducibility only matters in production\n"
            "\n"
            "The source values reproducible compute even for notebooks and experiments because it reduces collaboration surprises.\n"
            "\n"
            "### Misconception 5: Model registration is unnecessary because deployment already knows the model file\n"
            "\n"
            "Registration enables identity, metadata, version history, and easier rollback.\n"
            "\n"
            "### Misconception 6: Git is a good default system for versioning huge datasets\n"
            "\n"
            "The source treats source-code version control and dataset versioning as different problems.\n"
            "\n"
            "### Misconception 7: The cluster used for training should also be assumed to be the production serving cluster\n"
            "\n"
            "Training and inference have different compute patterns and can use different resources.\n"
            "\n"
            "### Misconception 8: A successfully trained model is automatically a valid HTTP service\n"
            "\n"
            "Request method, content type, authentication, input schema, runtime, and deployment all need to work too.\n"
            "\n"
            "### Misconception 9: A Python traceback proves Python is the root cause\n"
            "\n"
            "The chapter's observability discussion shows that an upstream system may have produced invalid input.\n"
            "\n"
            "### Misconception 10: Production debugging should happen directly on the production server whenever possible\n"
            "\n"
            "The source recommends reproducing containerized services in safer local environments when possible.\n"
            "\n"
            "### Misconception 11: A pipeline is just a long Python script\n"
            "\n"
            "Pipeline steps have explicit inputs, outputs, compute, runtime configuration, and orchestration boundaries.\n"
            "\n"
            "### Misconception 12: Monitoring and Kubernetes scaling make an ML system successful automatically\n"
            "\n"
            "The source concludes that continuous evaluation and feedback are still required.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Azure ML workspace | Cloud context that groups ML assets, compute, models, datasets, and related operations. |\n"
            "| Azure CLI | Command-line interface used to authenticate and manage Azure resources/workflows. |\n"
            "| Python SDK | Programmatic interface used by the chapter to work with Azure ML resources. |\n"
            "| Service principal | Non-human Azure identity used for automated access to resources. |\n"
            "| Least privilege | Granting only the permissions required for a task. |\n"
            "| Compute instance | Managed cloud workstation/environment for ML development. |\n"
            "| Compute cluster | Scalable group of machines used for training or other jobs. |\n"
            "| Batch inference | Producing predictions over large datasets/jobs rather than request-by-request interactive serving. |\n"
            "| Online inference | Serving predictions through a live endpoint, typically over HTTP. |\n"
            "| Model registration | Storing a model as a managed/versioned Azure ML asset with metadata. |\n"
            "| Dataset versioning | Managing named/versioned references to data used across ML workflows. |\n"
            "| ACI | Azure Container Instances, presented by the source as a simpler deployment option for testing. |\n"
            "| AKS | Azure Kubernetes Service, presented by the source as the scalable Kubernetes-backed deployment option. |\n"
            "| Scoring script | Model-specific serving script defining initialization and request-scoring behavior. |\n"
            "| InferenceConfig | Azure ML abstraction combining scoring code and serving environment in the source SDK. |\n"
            "| Application Insights | Azure observability tooling for requests, latency, failures, exceptions, dashboards, and related signals. |\n"
            "| LocalWebservice | Source SDK abstraction used to run an Azure ML-style model deployment locally in a container. |\n"
            "| Pipeline step | One explicit unit of work with inputs, outputs, code, and execution resources. |\n"
            "| Published pipeline | Pipeline exposed as an authenticated endpoint so external systems can trigger runs. |\n"
            "| Designer | Visual Azure ML interface for constructing and running ML workflows. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why does the chapter describe Azure ML as flexible rather than opinionated?\n"
            "2. What role does `config.json` play in the source's SDK workflow?\n"
            "3. Why is weakening permissions a bad automation strategy?\n"
            "4. What problem does a service principal solve?\n"
            "5. What does least privilege mean in this context?\n"
            "6. Why should authentication also be tested in nonproduction environments?\n"
            "7. What is the difference between automation identity and deployed API authentication?\n"
            "8. Why are compute instances useful for notebooks and proof-of-concept work?\n"
            "9. How do reproducible environments reduce 'works on my machine' problems?\n"
            "10. Why does the source recommend starting with low-cost compute?\n"
            "11. When is batch inference appropriate?\n"
            "12. When is online inference appropriate?\n"
            "13. Why does the source recommend model registration for production models?\n"
            "14. What operational benefits come from model versions?\n"
            "15. Which interfaces can register models in the source?\n"
            "16. Why is Git not ideal for versioning large datasets?\n"
            "17. What does Azure dataset versioning preserve conceptually?\n"
            "18. Why can a dataset version reference storage instead of copying the whole dataset?\n"
            "19. Which parameters matter when sizing a training cluster?\n"
            "20. Why can minimum nodes = 0 reduce cost?\n"
            "21. Why are training and inference clusters conceptually different?\n"
            "22. How does the chapter distinguish ACI and AKS?\n"
            "23. Which information is part of an HTTP model-serving contract?\n"
            "24. What could cause a 500 error in the model-serving example?\n"
            "25. What does a 'Method Not Allowed' response often indicate?\n"
            "26. Why does malformed authorization fail before useful scoring occurs?\n"
            "27. What debugging habits does the source recommend?\n"
            "28. Why is 'trust but verify' useful in operations?\n"
            "29. How can Azure deployment logs be retrieved conceptually?\n"
            "30. What signals does Application Insights add beyond one log file?\n"
            "31. Why can a Python traceback be only a symptom?\n"
            "32. Why is reproducing a production problem locally valuable?\n"
            "33. Which components are needed for the source's local model deployment?\n"
            "34. What are the roles of `init()` and `run()` in a scoring script?\n"
            "35. What does InferenceConfig combine?\n"
            "36. What can Docker inspection reveal after local deployment?\n"
            "37. What is an Azure ML pipeline?\n"
            "38. What information does a PythonScriptStep contain?\n"
            "39. Why does a pipeline step need a compute target?\n"
            "40. Why separate the script logic from compute/runtime configuration?\n"
            "41. What new integration capability appears when a pipeline is published?\n"
            "42. Why can an external Git/source platform benefit from a published Azure pipeline?\n"
            "43. What learning value does Designer provide?\n"
            "44. Why is the ML lifecycle not linear?\n"
            "45. What does the chapter mean by leveraging existing cloud capabilities rather than reinventing them?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Azure MLOps is most useful when its abstractions remove repeated infrastructure work without removing engineering discipline. "
            "Secure authentication, reproducible compute, versioned models and data, testable containerized deployments, observable services, "
            "and externally triggerable pipelines all support one goal: ship models reliably and use production feedback to improve them.**\n"
        ),

        "estimated_minutes": 360,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "azure-framing", "title": "Azure ML hides difficult infrastructure behind multiple interfaces", "order": 1},
            {"id": "cli-sdk-workspace", "title": "CLI and SDK are the programmatic foundation", "order": 2},
            {"id": "auth-core", "title": "Authentication is a core part of automation, not an obstacle to remove", "order": 3},
            {"id": "service-principal", "title": "Service principals give automated systems their own identity", "order": 4},
            {"id": "api-auth", "title": "Deployed model APIs need an authentication strategy too", "order": 5},
            {"id": "compute-instance", "title": "Compute instances reduce setup friction for ML development", "order": 6},
            {"id": "start-small-compute", "title": "Start small when experimenting with compute", "order": 7},
            {"id": "batch-online", "title": "Choose deployment style from inference behavior", "order": 8},
            {"id": "register-models", "title": "Register production models even when registration is technically optional", "order": 9},
            {"id": "model-registration-paths", "title": "Model registration is intentionally flexible", "order": 10},
            {"id": "dataset-versioning", "title": "Dataset versioning is as important as model versioning", "order": 11},
            {"id": "training-cluster", "title": "Training compute should match the workload—not an arbitrary maximum size", "order": 12},
            {"id": "training-vs-serving-cluster", "title": "Training compute and inference compute are different concerns", "order": 13},
            {"id": "aci-aks", "title": "The source positions ACI and AKS for different deployment needs", "order": 14},
            {"id": "rest-endpoint", "title": "A deployed model becomes a service contract", "order": 15},
            {"id": "http-errors", "title": "HTTP errors often point directly to contract violations", "order": 16},
            {"id": "debugging-mindset", "title": "Good debugging is a practiced method: question, observe, verify", "order": 17},
            {"id": "deployment-logs", "title": "Deployment logs reveal container startup and runtime behavior", "order": 18},
            {"id": "app-insights", "title": "Application Insights adds observability beyond raw logs", "order": 19},
            {"id": "observability-story", "title": "A traceback may be the symptom, not the root cause", "order": 20},
            {"id": "local-debug-value", "title": "Reproducing production behavior locally is a powerful debugging technique", "order": 21},
            {"id": "local-deploy-components", "title": "A local Azure ML deployment combines model, environment, score script, and inference config", "order": 22},
            {"id": "local-container-inspection", "title": "Inspect the actual container when deployment fails", "order": 23},
            {"id": "azure-pipelines", "title": "Azure ML pipelines coordinate multiple steps toward one objective", "order": 24},
            {"id": "python-script-step", "title": "A PythonScriptStep packages a data-processing command as a pipeline stage", "order": 25},
            {"id": "pipeline-compute", "title": "Pipeline steps still need a compute target and runtime environment", "order": 26},
            {"id": "publish-pipeline", "title": "Publishing a pipeline turns it into an externally triggerable service", "order": 27},
            {"id": "designer", "title": "Azure ML Designer provides a visual route through the same ecosystem", "order": 28},
            {"id": "lifecycle", "title": "Azure ML services exist to support an iterative model lifecycle", "order": 29},
            {"id": "reuse-not-reinvent", "title": "The final lesson: ship models, do not reimplement solved cloud problems", "order": 30},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M14.L01.EX01",
            "title": "Design secure automation identity",
            "lesson_code": "M14.L01",
            "section_id": "service-principal",
            "placement": "after_section",
            "description": (
                "Practice designing automation without removing authentication safeguards."
            ),
            "instructions": (
                "A CI system needs to register a model and deploy it into an Azure ML workspace.\n\n"
                "Design the authentication approach:\n"
                "1. explain why an interactive personal login is a poor long-term automation dependency,\n"
                "2. identify the role of a service principal,\n"
                "3. list the resources/actions the identity actually needs,\n"
                "4. explain how least privilege should affect the assigned role,\n"
                "5. explain why giving the identity broad owner-level access merely for convenience creates risk."
            ),
            "expected_output": (
                "A secure automation plan based on non-human identity and minimum required permissions."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "service-principal",
                "authentication",
                "least-privilege",
                "automation",
            ],
        },

        {
            "id": "M14.L01.EX02",
            "title": "Design model and dataset lineage",
            "lesson_code": "M14.L01",
            "section_id": "dataset-versioning",
            "placement": "after_section",
            "description": (
                "Connect model versions to the dataset versions that produced them."
            ),
            "instructions": (
                "A team has three dataset states: raw-v1, cleaned-v1, and cleaned-v2. "
                "Model version 4 was trained on cleaned-v1, while model version 5 was trained on cleaned-v2.\n\n"
                "Design a minimal lineage record containing:\n"
                "1. model name/version,\n"
                "2. dataset name/version,\n"
                "3. description/tags,\n"
                "4. training run reference,\n"
                "5. deployment environment,\n"
                "6. rollback target.\n\n"
                "Explain why keeping only `model.pkl` and `latest.csv` is insufficient."
            ),
            "expected_output": (
                "A traceable model-data versioning design suitable for production rollback and reproduction."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "model-versioning",
                "dataset-versioning",
                "lineage",
                "rollback",
            ],
        },

        {
            "id": "M14.L01.EX03",
            "title": "Debug an Azure prediction request",
            "lesson_code": "M14.L01",
            "section_id": "http-errors",
            "placement": "after_section",
            "description": (
                "Diagnose API-contract errors separately from model errors."
            ),
            "instructions": (
                "A deployed scoring endpoint returns errors for several clients.\n\n"
                "Diagnose these cases:\n"
                "1. client sends GET to `/score` instead of POST,\n"
                "2. JSON body is sent without the expected content-type header,\n"
                "3. authorization header is malformed,\n"
                "4. required model field is missing,\n"
                "5. correct request returns a valid JSON prediction.\n\n"
                "For each case, identify whether the failure is primarily authentication, HTTP contract, input schema, or normal scoring."
            ),
            "expected_output": (
                "A diagnostic table mapping request symptoms to likely contract layers."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "rest-api",
                "authentication",
                "http-debugging",
                "model-serving",
            ],
        },

        {
            "id": "M14.L01.EX04",
            "title": "Reproduce a failed deployment locally",
            "lesson_code": "M14.L01",
            "section_id": "local-container-inspection",
            "placement": "after_section",
            "description": (
                "Apply the chapter's reproduce-first debugging method."
            ),
            "instructions": (
                "A production-style Azure model deployment fails during container startup.\n\n"
                "Design a local debugging plan that checks:\n"
                "1. model registration/path,\n"
                "2. dependency environment,\n"
                "3. `score.py`,\n"
                "4. presence/signature of `init()` and `run()`,\n"
                "5. inference configuration,\n"
                "6. exposed local port,\n"
                "7. container logs,\n"
                "8. filesystem contents inside the container,\n"
                "9. a repeated failing HTTP request.\n\n"
                "Explain why this is safer than experimenting directly on production."
            ),
            "expected_output": (
                "A reproducible local-container debugging checklist."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "local-debugging",
                "containers",
                "score-script",
                "observability",
            ],
        },

        {
            "id": "M14.L01.EX05",
            "title": "Design and publish an Azure ML pipeline",
            "lesson_code": "M14.L01",
            "section_id": "publish-pipeline",
            "placement": "after_section",
            "description": (
                "Build a pipeline that can be triggered from outside Azure ML."
            ),
            "instructions": (
                "Design a three-step pipeline:\n"
                "1. data preparation,\n"
                "2. model training,\n"
                "3. model evaluation.\n\n"
                "For each step define:\n"
                "- inputs,\n"
                "- outputs,\n"
                "- script responsibility,\n"
                "- compute target.\n\n"
                "Then explain how publishing the pipeline allows an external source-control CI system to trigger it and obtain a run ID."
            ),
            "expected_output": (
                "A step-oriented Azure ML pipeline design plus an external-trigger integration."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "azure-ml-pipelines",
                "pipeline-steps",
                "compute-targets",
                "external-orchestration",
            ],
        },

        {
            "id": "M14.L01.EX06",
            "title": "Build an Azure MLOps lifecycle",
            "lesson_code": "M14.L01",
            "section_id": "reuse-not-reinvent",
            "placement": "after_section",
            "description": (
                "Combine the chapter into one iterative production workflow."
            ),
            "instructions": (
                "Design an Azure ML lifecycle for a classification service.\n\n"
                "Include:\n"
                "1. development environment,\n"
                "2. dataset versioning,\n"
                "3. training compute,\n"
                "4. model registration,\n"
                "5. authenticated deployment,\n"
                "6. local pre-production reproduction/debugging,\n"
                "7. Application Insights/logs,\n"
                "8. a pipeline that can be triggered externally,\n"
                "9. a feedback rule that sends the workflow back to data/training when production evidence reveals a problem.\n\n"
                "Explain which Azure features you reuse instead of rebuilding yourself."
            ),
            "expected_output": (
                "An end-to-end iterative Azure MLOps architecture grounded in the chapter."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "azure-ml",
                "ml-lifecycle",
                "deployment",
                "monitoring",
                "pipelines",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M14.L01.QZ01",

        "title": "MLOps for Azure — Knowledge Check",

        "lesson_code": "M14.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M14.L01.Q01",
                "section_id": "azure-framing",
                "question": "What flexibility does the chapter emphasize in Azure ML?",
                "options": [
                    "Users can work through Studio, Designer, notebooks, AutoML, CLI, and SDK.",
                    "Only Designer is supported.",
                    "Only Python SDK workflows are valid.",
                    "All deployments require handwritten Kubernetes configuration.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter presents several interfaces so teams can choose the workflow that fits them."
                ),
            },

            {
                "id": "M14.L01.Q02",
                "section_id": "cli-sdk-workspace",
                "question": "What does `Workspace.from_config()` accomplish conceptually?",
                "options": [
                    "Associates local SDK code with the intended Azure ML workspace configuration.",
                    "Trains a model automatically.",
                    "Creates a Kubernetes cluster.",
                    "Registers every local dataset.",
                ],
                "correct": 0,
                "explanation": (
                    "The configuration gives the SDK the information needed to connect to the workspace."
                ),
            },

            {
                "id": "M14.L01.Q03",
                "section_id": "auth-core",
                "question": "What security behavior does the chapter strongly discourage?",
                "options": [
                    "Weakening permissions or bypassing authentication simply to make automation easier.",
                    "Using explicit authentication.",
                    "Restricting access.",
                    "Testing authenticated endpoints.",
                ],
                "correct": 0,
                "explanation": (
                    "The source gives a real example showing how permissive shortcuts can expose systems."
                ),
            },

            {
                "id": "M14.L01.Q04",
                "section_id": "service-principal",
                "question": "What is the main purpose of a service principal in this chapter?",
                "options": [
                    "Provide an identity for automated Azure resource access.",
                    "Store model weights.",
                    "Replace dataset versioning.",
                    "Create HTTP payloads.",
                ],
                "correct": 0,
                "explanation": (
                    "A service principal supports noninteractive automation with controlled permissions."
                ),
            },

            {
                "id": "M14.L01.Q05",
                "section_id": "service-principal",
                "question": "What access principle does the source recommend after creating a service principal?",
                "options": [
                    "Least privilege",
                    "Always use owner",
                    "Anonymous access",
                    "Disable authentication",
                ],
                "correct": 0,
                "explanation": (
                    "The example may use a broad role, but the source explicitly says to restrict permissions for real use."
                ),
            },

            {
                "id": "M14.L01.Q06",
                "section_id": "compute-instance",
                "question": "Why are Azure compute instances useful for MLOps development?",
                "options": [
                    "They provide ready-to-use, reproducible ML development environments.",
                    "They eliminate the need for data.",
                    "They can only host production APIs.",
                    "They prevent notebooks.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter emphasizes reduced setup friction and reproducibility."
                ),
            },

            {
                "id": "M14.L01.Q07",
                "section_id": "start-small-compute",
                "question": "What compute-sizing habit does the chapter recommend for experimentation?",
                "options": [
                    "Start with low-cost/modest resources and increase them when needed.",
                    "Always choose the largest machine.",
                    "Never measure resource use.",
                    "Use production-scale clusters for every notebook.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly warns against unnecessary cost during exploratory work."
                ),
            },

            {
                "id": "M14.L01.Q08",
                "section_id": "batch-online",
                "question": "Which statement best distinguishes batch and online inference?",
                "options": [
                    "Batch processes large groups of data/jobs; online inference serves request-time predictions through a live endpoint.",
                    "They are identical.",
                    "Online inference is only for terabytes of offline data.",
                    "Batch inference always requires Kubernetes.",
                ],
                "correct": 0,
                "explanation": (
                    "The source discusses these as different serving patterns."
                ),
            },

            {
                "id": "M14.L01.Q09",
                "section_id": "register-models",
                "question": "Why does the source recommend registering production models?",
                "options": [
                    "To track versions, descriptions, identity, and rollback options.",
                    "Because unregistered models cannot exist.",
                    "To remove authentication.",
                    "To store logs only.",
                ],
                "correct": 0,
                "explanation": (
                    "Registration provides lifecycle management even when deployment without it may be technically possible."
                ),
            },

            {
                "id": "M14.L01.Q10",
                "section_id": "dataset-versioning",
                "question": "Why is ordinary Git-style version control a poor fit for very large datasets?",
                "options": [
                    "It is designed primarily for source-code changes rather than massive evolving binary/data artifacts.",
                    "Git cannot store text.",
                    "Datasets never change.",
                    "Model training does not need reproducible data.",
                ],
                "correct": 0,
                "explanation": (
                    "The source motivates cloud dataset versioning with this mismatch."
                ),
            },

            {
                "id": "M14.L01.Q11",
                "section_id": "training-cluster",
                "question": "Why might a compute cluster use a minimum of zero nodes?",
                "options": [
                    "To scale down while idle and reduce unnecessary cost.",
                    "To prevent training forever.",
                    "To disable Azure ML.",
                    "Because clusters cannot have running nodes.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly uses scale-to-zero as a cost-control technique."
                ),
            },

            {
                "id": "M14.L01.Q12",
                "section_id": "training-vs-serving-cluster",
                "question": "Why shouldn't training and inference compute be treated as the same workload?",
                "options": [
                    "Training and serving can have different throughput, latency, scaling, and resource needs.",
                    "Only training uses machines.",
                    "Inference cannot use clusters.",
                    "Training never needs parallelism.",
                ],
                "correct": 0,
                "explanation": (
                    "The source warns that the shared word 'cluster' can hide different lifecycle purposes."
                ),
            },

            {
                "id": "M14.L01.Q13",
                "section_id": "aci-aks",
                "question": "How does the source position ACI relative to AKS?",
                "options": [
                    "ACI as a simpler testing-oriented target; AKS as a more scalable Kubernetes-backed target.",
                    "ACI as the only possible production target.",
                    "AKS as a notebook environment.",
                    "They are described as identical.",
                ],
                "correct": 0,
                "explanation": (
                    "This is the practical distinction made in the supplied chapter."
                ),
            },

            {
                "id": "M14.L01.Q14",
                "section_id": "rest-endpoint",
                "question": "Which information must a client respect when calling a deployed model endpoint?",
                "options": [
                    "URL, HTTP method, content type, authentication, and request schema",
                    "Only the model filename",
                    "Only the Azure region",
                    "Only the HTTP method",
                ],
                "correct": 0,
                "explanation": (
                    "The endpoint behaves as a software contract, not merely a model file."
                ),
            },

            {
                "id": "M14.L01.Q15",
                "section_id": "http-errors",
                "question": "What does 'Method Not Allowed' commonly indicate in the source's scoring example?",
                "options": [
                    "The client used the wrong HTTP method, such as GET instead of POST.",
                    "The model is perfectly healthy.",
                    "The dataset version is missing.",
                    "A service principal expired.",
                ],
                "correct": 0,
                "explanation": (
                    "The source lists incorrect HTTP method as one of the common endpoint failures."
                ),
            },

            {
                "id": "M14.L01.Q16",
                "section_id": "debugging-mindset",
                "question": "Which debugging mindset does the chapter recommend?",
                "options": [
                    "Question assumptions, observe details, reproduce, and verify.",
                    "Trust the first guess.",
                    "Change production until the problem disappears.",
                    "Ignore logs.",
                ],
                "correct": 0,
                "explanation": (
                    "The source repeatedly emphasizes 'never assume' and 'trust but verify.'"
                ),
            },

            {
                "id": "M14.L01.Q17",
                "section_id": "deployment-logs",
                "question": "What can deployment logs reveal?",
                "options": [
                    "Model paths, runtime initialization, listening ports, startup failures, and other service behavior.",
                    "Only model accuracy.",
                    "Only billing information.",
                    "Nothing useful after deployment.",
                ],
                "correct": 0,
                "explanation": (
                    "The source shows startup and runtime details in deployment logs."
                ),
            },

            {
                "id": "M14.L01.Q18",
                "section_id": "app-insights",
                "question": "What does Application Insights add beyond reading one raw log file?",
                "options": [
                    "Aggregated observability such as response times, failure rates, exceptions, dashboards, and trends.",
                    "A replacement model.",
                    "Dataset registration only.",
                    "A Python compiler.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents Application Insights as a system-level observability tool."
                ),
            },

            {
                "id": "M14.L01.Q19",
                "section_id": "observability-story",
                "question": "Why might a Python traceback not identify the true root cause?",
                "options": [
                    "An upstream component may have sent invalid or empty input that caused the downstream error.",
                    "Tracebacks never contain useful information.",
                    "Python cannot fail.",
                    "Azure hides every upstream event.",
                ],
                "correct": 0,
                "explanation": (
                    "Observability requires understanding interactions between components."
                ),
            },

            {
                "id": "M14.L01.Q20",
                "section_id": "local-debug-value",
                "question": "Why reproduce a deployed model locally in a container?",
                "options": [
                    "To inspect and experiment safely without disrupting production.",
                    "To avoid all testing.",
                    "Because cloud containers cannot be debugged.",
                    "To remove the model.",
                ],
                "correct": 0,
                "explanation": (
                    "The source treats local reproduction as a powerful troubleshooting technique."
                ),
            },

            {
                "id": "M14.L01.Q21",
                "section_id": "local-deploy-components",
                "question": "What does an inference configuration combine in the source's local-deployment pattern?",
                "options": [
                    "The scoring entry script and the execution environment.",
                    "Only the model name and region.",
                    "Only the dataset and notebook.",
                    "Only the endpoint key.",
                ],
                "correct": 0,
                "explanation": (
                    "InferenceConfig binds model-serving code to its declared environment."
                ),
            },

            {
                "id": "M14.L01.Q22",
                "section_id": "local-container-inspection",
                "question": "What kind of scoring-script failure does the source demonstrate?",
                "options": [
                    "The expected initialization entry point is missing or incorrect.",
                    "The HTTP client used HTTPS.",
                    "The dataset was too small.",
                    "The model had too much accuracy.",
                ],
                "correct": 0,
                "explanation": (
                    "The example surfaces a container startup failure around the expected `init()` behavior."
                ),
            },

            {
                "id": "M14.L01.Q23",
                "section_id": "azure-pipelines",
                "question": "What is an Azure ML pipeline in the chapter's framing?",
                "options": [
                    "A coordinated sequence/graph of steps working toward an objective.",
                    "A single model file.",
                    "Only a monitoring dashboard.",
                    "Only a Kubernetes cluster.",
                ],
                "correct": 0,
                "explanation": (
                    "The source compares pipelines to familiar CI/CD step workflows."
                ),
            },

            {
                "id": "M14.L01.Q24",
                "section_id": "python-script-step",
                "question": "What does the PythonScriptStep example demonstrate?",
                "options": [
                    "A normal Python data-processing script can become an explicit pipeline step with inputs and outputs.",
                    "Python scripts cannot use datasets.",
                    "Pipeline steps cannot accept arguments.",
                    "Azure pipelines require only GUI tools.",
                ],
                "correct": 0,
                "explanation": (
                    "The source wraps a command-like Python script as a pipeline component."
                ),
            },

            {
                "id": "M14.L01.Q25",
                "section_id": "pipeline-compute",
                "question": "Why does a pipeline step need a compute target?",
                "options": [
                    "The workflow must specify where the step executes, not only what code it runs.",
                    "Compute targets are only labels.",
                    "Pipelines never execute code.",
                    "The dataset itself executes the script.",
                ],
                "correct": 0,
                "explanation": (
                    "Execution code and execution environment are separate concerns."
                ),
            },

            {
                "id": "M14.L01.Q26",
                "section_id": "publish-pipeline",
                "question": "What becomes possible after publishing an Azure ML pipeline?",
                "options": [
                    "External systems can trigger it through an authenticated HTTP endpoint.",
                    "The pipeline cannot run anymore.",
                    "Only Designer can access it.",
                    "Authentication is removed.",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes external triggering as a major integration benefit."
                ),
            },

            {
                "id": "M14.L01.Q27",
                "section_id": "designer",
                "question": "What is one value of Azure ML Designer?",
                "options": [
                    "It provides a visual way to explore/build workflows and exposes users to datasets, compute, jobs, and reports.",
                    "It is the only valid Azure ML interface.",
                    "It replaces model deployment completely.",
                    "It disables AutoML.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter presents Designer as a useful graphical abstraction, not the sole interface."
                ),
            },

            {
                "id": "M14.L01.Q28",
                "section_id": "lifecycle",
                "question": "Why is the Azure ML lifecycle not linear?",
                "options": [
                    "Production feedback can require returning to data, training, validation, or deployment decisions.",
                    "Models cannot be deployed.",
                    "Pipelines cannot be repeated.",
                    "Monitoring ends the lifecycle.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly emphasizes continuous adjustment and feedback."
                ),
            },

            {
                "id": "M14.L01.Q29",
                "section_id": "reuse-not-reinvent",
                "question": "What is the chapter's final MLOps principle?",
                "options": [
                    "Leverage useful cloud capabilities so effort goes toward reliably shipping models rather than rebuilding half-finished infrastructure.",
                    "Build every platform feature yourself.",
                    "Avoid model versioning.",
                    "Never use managed services.",
                ],
                "correct": 0,
                "explanation": (
                    "The conclusion argues for technology reuse and production delivery."
                ),
            },

            {
                "id": "M14.L01.Q30",
                "section_id": "lifecycle",
                "type": "open",
                "question": (
                    "Design an Azure MLOps workflow for a production prediction service. Include secure automation identity, "
                    "reproducible development compute, dataset and model versioning, training compute, authenticated serving, "
                    "local container reproduction, logs/Application Insights, an Azure ML pipeline that can be externally triggered, "
                    "and a feedback rule that sends the workflow back to earlier stages when production problems are found."
                ),
            },
        ],

        "passing_score": 70,
    },
}
