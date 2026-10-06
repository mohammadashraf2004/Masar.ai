"""M15.L01 — MLOps for GCP.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 9, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M15.L01"

MODULE_ORDER = 15

MODULE_TITLE = "MLOps for GCP"

MODULE_DESCRIPTION = (
    "Learn how Google Cloud supports production machine learning through its "
    "compute, storage, big-data, serverless, container, CI/CD, Kubernetes, "
    "BigQuery, DataOps, and Vertex AI capabilities, while choosing between "
    "lightweight and comprehensive MLOps workflows."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "MLOps for GCP",

    "slug": "practical-mlops-m15-l01-gcp",

    "description": (
        "A practical Google Cloud MLOps lesson covering compute selection, GKE and "
        "Cloud Run, App Engine, Cloud Functions, Cloud Storage, BigQuery, Vertex AI, "
        "Cloud Build, GitHub Actions, Kubernetes deployment and autoscaling, "
        "serverless DataOps, managed AI APIs, light-versus-heavy MLOps workflows, "
        "monitoring, security, and a final cloud-native project blueprint."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.0,

    "skill_tags": [
        "gcp",
        "google-cloud",
        "mlops",
        "compute-engine",
        "gke",
        "kubernetes",
        "cloud-run",
        "app-engine",
        "cloud-functions",
        "cloud-storage",
        "bigquery",
        "dataops",
        "vertex-ai",
        "cloud-build",
        "github-actions",
        "continuous-integration",
        "continuous-delivery",
        "docker",
        "horizontal-pod-autoscaler",
        "serverless",
        "pub-sub",
        "managed-ai-apis",
        "feature-store",
        "explainable-ai",
        "model-quality",
        "light-mlops",
        "heavy-mlops",
        "monitoring",
        "least-privilege",
    ],

    "prerequisite_ids": ["M14.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "MLOps for GCP",

        "content": (
            "# MLOps for GCP\n"
            "\n"
            "> **Lesson:** M15.L01  \n"
            "> **Module:** MLOps for GCP  \n"
            "> **Source alignment:** Chapter 9. Page numbers were not included in "
            "the supplied source. Product names, market-share discussion, command "
            "syntax, and service behavior reflect the source's timeframe. This lesson "
            "preserves the chapter's technical MLOps patterns rather than updating "
            "them with outside material.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the chapter's view of GCP's strengths and limitations as historical context.\n"
            "- Organize core GCP services into compute, storage, big-data, and machine-learning categories.\n"
            "- Select Compute Engine machine types based on workload characteristics and cost.\n"
            "- Explain the value of preemptible compute for appropriate batch workloads in the source's framing.\n"
            "- Compare GKE and Cloud Run as two different container-deployment abstractions.\n"
            "- Explain where App Engine and Cloud Functions fit in an MLOps system.\n"
            "- Explain why Cloud Storage can serve as a data-lake foundation for ML workloads.\n"
            "- Explain why BigQuery is central to the chapter's GCP MLOps story.\n"
            "- Describe the seven high-level Vertex AI lifecycle capabilities listed in the source.\n"
            "- Explain why CI is a nonoptional part of MLOps.\n"
            "- Compare the roles of GitHub Actions and Cloud Build in the source's recommended CI/CD pattern.\n"
            "- Explain Kubernetes as a portable orchestration layer and why it matters for MLOps.\n"
            "- Describe Kubernetes pods, deployments, services, load balancers, and autoscaling conceptually.\n"
            "- Explain why certified/base container images improve reproducible development.\n"
            "- Build the chapter's local Docker → local Kubernetes progression conceptually.\n"
            "- Explain how BigQuery can support analytics and machine-learning workflows in one platform.\n"
            "- Explain how DataOps supports MLOps by automating the flow of data into modeling systems.\n"
            "- Explain why Cloud Functions are useful for quick event-driven data-engineering and ML prototypes.\n"
            "- Describe how a Cloud Function can call a managed AI API.\n"
            "- Explain how Vertex AI combines multiple MLOps capabilities into a broader platform.\n"
            "- Distinguish the chapter's light and heavy MLOps workflows.\n"
            "- Explain the role of Explainable AI, model-quality tracking, and Feature Store in a broader MLOps platform.\n"
            "- Explain why comparative advantage matters when deciding whether to build or use a managed service.\n"
            "- Design a cloud-native GCP portfolio project with CI/CD, data storage, model serving, monitoring, environments, and security.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. GCP combines cloud infrastructure with influential ML and distributed-systems technology\n"
            "\n"
            "The chapter frames Google Cloud as unusual because Google has created or strongly influenced widely adopted technologies such as:\n"
            "\n"
            "- Kubernetes,\n"
            "- TensorFlow,\n"
            "- Go.\n"
            "\n"
            "The source also discusses historical disadvantages such as smaller cloud market share at the time, fewer certified practitioners, "
            "and concerns about Google's product/customer-service history.\n"
            "\n"
            "Those points are part of the chapter's historical framing rather than timeless technical facts.\n"
            "\n"
            "The durable MLOps idea is that technologies such as Kubernetes and TensorFlow can reduce cloud lock-in because they can operate beyond one provider.\n"
            "\n"
            "[[IMAGE_NEEDED: GCP MLOps technology ecosystem | "
            "Google Cloud surrounded by Kubernetes, TensorFlow, Go, BigQuery, and Vertex AI, with arrows showing portability beyond one cloud | "
            "Learner should notice the source's emphasis on widely adopted technologies rather than only proprietary services]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Organize GCP into four broad service categories\n"
            "\n"
            "The chapter groups the platform into four major categories:\n"
            "\n"
            "1. **Compute**\n"
            "2. **Storage**\n"
            "3. **Big Data**\n"
            "4. **Machine Learning**\n"
            "\n"
            "This is a useful mental model for MLOps because an end-to-end system usually needs capabilities from several categories.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Storage → training data\n"
            "Compute → data/model workloads\n"
            "Big Data → large-scale transformations and analytics\n"
            "Machine Learning → training, model management, deployment, prediction\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Match Compute Engine machines to the actual workload\n"
            "\n"
            "Compute Engine provides virtual machines with different resource profiles.\n"
            "\n"
            "The source names categories such as:\n"
            "\n"
            "- compute intensive,\n"
            "- memory intensive,\n"
            "- accelerator optimized,\n"
            "- general purpose.\n"
            "\n"
            "The MLOps lesson is resource matching.\n"
            "\n"
            "A GPU-heavy accelerator instance can be valuable for workloads that exploit massively parallel computation.\n"
            "\n"
            "Using the same expensive instance for a workload that cannot use the GPU efficiently is wasteful.\n"
            "\n"
            "Cost prediction matters in real production systems because infrastructure spend can determine whether an ML product is economically viable.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Interruptible compute can reduce batch cost when the workload tolerates it\n"
            "\n"
            "The source discusses preemptible VMs as short-lived, lower-cost resources that can suit batch jobs.\n"
            "\n"
            "The important systems principle is:\n"
            "\n"
            "> **Cheap interruptible compute is useful only when the workload can survive interruption.**\n"
            "\n"
            "Batch training or data-processing jobs may be redesigned to checkpoint, restart, or repeat work safely.\n"
            "\n"
            "The economic gain comes from matching workload reliability requirements to a cheaper compute class.\n"
            "\n"
            "{{exercise:M15.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. GKE and Cloud Run expose containers at different abstraction levels\n"
            "\n"
            "The source contrasts two important GCP container paths.\n"
            "\n"
            "### Google Kubernetes Engine (GKE)\n"
            "\n"
            "A managed Kubernetes environment suitable when teams need Kubernetes features and control.\n"
            "\n"
            "### Cloud Run\n"
            "\n"
            "A higher-level service that hides more of the complexity of running containers.\n"
            "\n"
            "The chapter recommends Cloud Run as a practical starting point for organizations that want a simple way to deploy a containerized ML application.\n"
            "\n"
            "This is the same abstraction trade-off seen in the AWS and Azure chapters:\n"
            "\n"
            "```text\n"
            "More orchestration control → GKE\n"
            "Less infrastructure work   → Cloud Run\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: GKE versus Cloud Run abstraction | "
            "The same ML container shown on a detailed Kubernetes/GKE stack and on a simplified Cloud Run managed-service stack | "
            "Learner should notice that the application can be similar while operational responsibility changes]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. App Engine and Cloud Functions provide higher-level application patterns\n"
            "\n"
            "### App Engine\n"
            "\n"
            "The chapter presents App Engine as a fully managed platform-as-a-service that can host applications in several languages.\n"
            "\n"
            "An MLOps workflow can use Cloud Build to continuously deploy an API service to App Engine.\n"
            "\n"
            "### Cloud Functions\n"
            "\n"
            "Cloud Functions provide a functions-as-a-service pattern suitable for event-driven systems.\n"
            "\n"
            "A function might:\n"
            "\n"
            "- start a batch training job,\n"
            "- respond to a data event,\n"
            "- call a managed AI API,\n"
            "- return a prediction.\n"
            "\n"
            "These services reduce how much infrastructure must be managed directly.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Cloud Storage can act as the data-lake foundation\n"
            "\n"
            "The chapter positions Cloud Storage as an important MLOps storage layer for structured and unstructured data.\n"
            "\n"
            "For batch-oriented ML systems, a data lake provides a place where raw or transformed data can live before large processing/training jobs consume it.\n"
            "\n"
            "The storage layer therefore supports the rest of the MLOps workflow rather than existing separately from it.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. BigQuery combines analytics, serverless querying, and ML capabilities\n"
            "\n"
            "The chapter treats BigQuery as one of GCP's most important MLOps tools.\n"
            "\n"
            "Reasons emphasized include:\n"
            "\n"
            "- familiar SQL interface,\n"
            "- serverless operating model,\n"
            "- large public datasets,\n"
            "- ML capabilities inside the platform.\n"
            "\n"
            "The source argues that BigQuery can cover a large portion of the analytics-to-ML value chain without moving data through many separate systems.\n"
            "\n"
            "That is especially attractive when the data already lives in a warehouse-style environment.\n"
            "\n"
            "[[IMAGE_NEEDED: BigQuery-centered MLOps flow | "
            "Public/streaming/storage data feeding BigQuery, with outputs branching to analytics/BI and machine-learning/Vertex AI workflows | "
            "Learner should notice why keeping data and some ML operations close together simplifies the pipeline]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Vertex AI organizes the model lifecycle into managed capabilities\n"
            "\n"
            "The source lists seven high-level capabilities around the Vertex AI workflow:\n"
            "\n"
            "1. dataset creation and storage,\n"
            "2. training a model,\n"
            "3. storing the model,\n"
            "4. deploying it to a prediction endpoint,\n"
            "5. testing/creating prediction requests,\n"
            "6. traffic splitting across endpoints or versions,\n"
            "7. lifecycle management of models and endpoints.\n"
            "\n"
            "The chapter places **data and model management** at the center of this end-to-end MLOps idea.\n"
            "\n"
            "The value of a comprehensive platform is coordination: lifecycle stages are connected rather than managed as unrelated scripts.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Continuous integration is foundational, not optional\n"
            "\n"
            "The chapter calls CI one of the most important—and often neglected—parts of a project.\n"
            "\n"
            "Testing, linting, and repeatable builds provide fast feedback before deployment.\n"
            "\n"
            "For GCP, the source considers two main options:\n"
            "\n"
            "- a SaaS CI platform such as GitHub Actions,\n"
            "- GCP's cloud-native Cloud Build.\n"
            "\n"
            "The important principle is not brand choice. It is that ML software should receive continuous automated quality feedback.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Cloud Build expresses install, lint, build, and deploy steps\n"
            "\n"
            "The source's Cloud Build configuration includes explicit steps such as:\n"
            "\n"
            "- install Python dependencies,\n"
            "- run linting,\n"
            "- deploy to App Engine.\n"
            "\n"
            "A simplified pattern is:\n"
            "\n"
            "```yaml\n"
            "steps:\n"
            "  - install dependencies\n"
            "  - run lint checks\n"
            "  - deploy application\n"
            "```\n"
            "\n"
            "This turns the deployment process into a repeatable pipeline rather than a sequence of manual commands.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Use each CI/CD system where its experience is strongest\n"
            "\n"
            "The source contrasts GitHub Actions and Cloud Build.\n"
            "\n"
            "GitHub Actions is presented as especially pleasant for developer feedback such as:\n"
            "\n"
            "- dependency installation,\n"
            "- linting,\n"
            "- tests,\n"
            "- formatting.\n"
            "\n"
            "Cloud Build is presented as strongly integrated with GCP deployment targets such as App Engine.\n"
            "\n"
            "The source proposes a hybrid pattern:\n"
            "\n"
            "```text\n"
            "GitHub Actions → developer feedback / test / lint\n"
            "Cloud Build     → cloud deployment\n"
            "```\n"
            "\n"
            "This is an important systems lesson: tools do not have to be mutually exclusive.\n"
            "\n"
            "[[IMAGE_NEEDED: Split CI/CD responsibilities | "
            "A Git push feeding GitHub Actions for tests/lint, then a deployment path using Cloud Build into GCP | "
            "Learner should notice how two automation systems can serve different strengths in one workflow]]\n"
            "\n"
            "{{exercise:M15.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Kubernetes is a portable orchestration foundation for ML-powered APIs\n"
            "\n"
            "The chapter describes Kubernetes as a 'mini-cloud' or 'cloud-in-a-box.'\n"
            "\n"
            "Capabilities named in the source include:\n"
            "\n"
            "- high availability,\n"
            "- autoscaling,\n"
            "- service discovery,\n"
            "- container health management,\n"
            "- secrets/configuration management,\n"
            "- a rich ecosystem,\n"
            "- Kubeflow as an end-to-end ML platform on Kubernetes.\n"
            "\n"
            "Kubernetes can run locally, in GKE, or through equivalent managed offerings in other clouds.\n"
            "\n"
            "That portability is one reason it is strategically important for multicloud MLOps.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Understand the Kubernetes deployment hierarchy\n"
            "\n"
            "The source describes a control plane managing worker nodes, with containers grouped into pods.\n"
            "\n"
            "The main operational actions are:\n"
            "\n"
            "1. create a cluster,\n"
            "2. deploy an application,\n"
            "3. expose ports/services,\n"
            "4. scale the application,\n"
            "5. update the application.\n"
            "\n"
            "A simplified mental model is:\n"
            "\n"
            "```text\n"
            "Cluster\n"
            "  ├── control plane\n"
            "  └── worker nodes\n"
            "        └── pods\n"
            "              └── containers\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Horizontal Pod Autoscaler closes the loop between metrics and capacity\n"
            "\n"
            "The source highlights Kubernetes Horizontal Pod Autoscaler (HPA) as a major feature.\n"
            "\n"
            "HPA can adjust the number of pods based on signals such as:\n"
            "\n"
            "- CPU utilization,\n"
            "- memory,\n"
            "- custom metrics.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Observe metric\n"
            "      ↓\n"
            "Compare with target\n"
            "      ↓\n"
            "Increase / decrease pods\n"
            "      ↓\n"
            "Observe again\n"
            "```\n"
            "\n"
            "This is another MLOps feedback loop: system measurements drive automated operational action.\n"
            "\n"
            "[[IMAGE_NEEDED: Kubernetes HPA control loop | "
            "Metrics feeding an autoscaler that changes the replica/pod count behind a load-balanced ML service | "
            "Learner should notice the closed loop from observation to scaling action]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Start Kubernetes learning with a small containerized service\n"
            "\n"
            "The chapter's Kubernetes tutorial deliberately uses a simple Flask 'make change' service.\n"
            "\n"
            "The repository contains:\n"
            "\n"
            "- `Makefile`,\n"
            "- `Dockerfile`,\n"
            "- `app.py`,\n"
            "- Kubernetes YAML configuration.\n"
            "\n"
            "Before Kubernetes is introduced, the project is:\n"
            "\n"
            "1. installed,\n"
            "2. linted,\n"
            "3. tested,\n"
            "4. built into a Docker image,\n"
            "5. run locally,\n"
            "6. invoked with `curl`.\n"
            "\n"
            "This progression isolates container/application issues before adding orchestration complexity.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Base your container on trusted existing images when appropriate\n"
            "\n"
            "The source discusses using official/certified base container images, such as the official Python image.\n"
            "\n"
            "A Dockerfile uses `FROM` to inherit a previously built runtime environment.\n"
            "\n"
            "This is a form of engineering reuse:\n"
            "\n"
            "```text\n"
            "trusted base image\n"
            "      ↓\n"
            "your dependencies\n"
            "      ↓\n"
            "your application\n"
            "      ↓\n"
            "versioned image\n"
            "```\n"
            "\n"
            "The developer then tests locally and distributes the resulting image through a registry.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Move from local Docker to local Kubernetes before cloud Kubernetes\n"
            "\n"
            "The chapter's sequence is valuable:\n"
            "\n"
            "```text\n"
            "Python app\n"
            "   ↓\n"
            "local Docker container\n"
            "   ↓\n"
            "local Kubernetes deployment\n"
            "   ↓\n"
            "managed cloud target such as GKE\n"
            "```\n"
            "\n"
            "The YAML defines a load-balanced service and a deployment with multiple replicas.\n"
            "\n"
            "The developer then verifies:\n"
            "\n"
            "- nodes,\n"
            "- pods,\n"
            "- service configuration,\n"
            "- endpoint response.\n"
            "\n"
            "This staged approach makes failures easier to localize.\n"
            "\n"
            "{{exercise:M15.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 19. BigQuery can keep model creation close to large datasets\n"
            "\n"
            "The chapter calls BigQuery one of GCP's 'crown jewels' partly because ML can be performed within the platform.\n"
            "\n"
            "For analytics-heavy applications, this can reduce the need to move large datasets into a separate custom training environment.\n"
            "\n"
            "The source's example connects BigQuery ML results to a shareable visualization/reporting layer.\n"
            "\n"
            "The larger architecture is:\n"
            "\n"
            "```text\n"
            "DataOps inputs\n"
            "public data / streaming / transformations\n"
            "      ↓\n"
            "BigQuery\n"
            "SQL + analytics + ML\n"
            "      ↓\n"
            "BI/reporting and/or ML engineering outputs\n"
            "```\n"
            "\n"
            "This makes BigQuery a strong starting point when data warehousing and analytics are already central to the use case.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. DataOps is the operational foundation feeding ML systems\n"
            "\n"
            "The source treats data as a necessary input for machine learning at scale.\n"
            "\n"
            "GCP offers many ways to automate data movement and processing, from high-level systems such as Dataflow to simpler serverless functions.\n"
            "\n"
            "DataOps in this lesson means operationalizing the movement, transformation, and availability of data so that ML workflows receive reliable inputs.\n"
            "\n"
            "MLOps cannot be healthy if the data pipeline feeding it is unreliable.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Cloud Functions are a fast way to prototype event-driven workflows\n"
            "\n"
            "The chapter builds an intentionally simple function that accepts a JSON payload containing an amount and returns coin change.\n"
            "\n"
            "The function can be invoked through:\n"
            "\n"
            "- `gcloud`,\n"
            "- `curl`,\n"
            "- a custom CLI using HTTP.\n"
            "\n"
            "This matters because a function can become a small reusable building block in a larger MLOps or DataOps pipeline.\n"
            "\n"
            "The source recommends solving an initial data-engineering workflow with a simple serverless approach before moving to more complex tools if necessary.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. A serverless function can compose external data and managed AI services\n"
            "\n"
            "The chapter's second Cloud Functions example combines:\n"
            "\n"
            "- a request payload,\n"
            "- Wikipedia content retrieval,\n"
            "- Google translation services,\n"
            "- a returned translated result.\n"
            "\n"
            "The architecture is more important than the specific example:\n"
            "\n"
            "```text\n"
            "HTTP/event request\n"
            "      ↓\n"
            "Cloud Function\n"
            "      ↓\n"
            "external data / source\n"
            "      ↓\n"
            "managed AI API\n"
            "      ↓\n"
            "response\n"
            "```\n"
            "\n"
            "Serverless technology can therefore serve both as a lightweight ML application and as a coordination step inside a larger pipeline.\n"
            "\n"
            "[[IMAGE_NEEDED: Serverless DataOps and AI composition | "
            "A Cloud Function receiving an event, reading external or cloud data, calling an AI API, and returning/publishing a result | "
            "Learner should notice how serverless functions glue managed services together]]\n"
            "\n"
            "{{exercise:M15.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Vertex AI brings advanced MLOps capabilities into one platform\n"
            "\n"
            "The source describes Vertex AI as GCP's comprehensive MLOps platform.\n"
            "\n"
            "Capabilities highlighted in the chapter include:\n"
            "\n"
            "- AutoML integration,\n"
            "- Feature Store,\n"
            "- Explainable AI,\n"
            "- model-quality tracking,\n"
            "- model/prediction services,\n"
            "- broader lifecycle management.\n"
            "\n"
            "For a larger organization beginning a substantial MLOps program, the source recommends considering Vertex AI early rather than assembling every capability manually.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Operationalizing a model can start with local prediction, then move to an endpoint\n"
            "\n"
            "The chapter shows a conceptual progression where a local model can first be tested with a prediction command.\n"
            "\n"
            "After that, the model can be hosted behind an endpoint and consumed by services such as:\n"
            "\n"
            "- Cloud Functions,\n"
            "- Cloud Run,\n"
            "- App Engine.\n"
            "\n"
            "This separation is useful:\n"
            "\n"
            "1. verify the model and input format,\n"
            "2. host it,\n"
            "3. integrate the endpoint into application infrastructure.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. A light MLOps workflow favors speed and simplicity\n"
            "\n"
            "The chapter builds a lightweight App Engine workflow.\n"
            "\n"
            "Core files include:\n"
            "\n"
            "- `main.py`,\n"
            "- `requirements.txt`,\n"
            "- `app.yaml`,\n"
            "- a small `cloudbuild.yml` that deploys the app.\n"
            "\n"
            "The application can then call an ML/AI API or an existing prediction endpoint.\n"
            "\n"
            "The source emphasizes how quickly this type of MLOps pipeline can be assembled.\n"
            "\n"
            "That makes it attractive for prototypes, early-stage applications, or teams that do not yet need the full Vertex AI feature set.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. A heavy MLOps workflow adds platform capabilities when the problem requires them\n"
            "\n"
            "The source contrasts the simple App Engine-style workflow with a broader Vertex AI approach.\n"
            "\n"
            "A heavier workflow can justify its complexity when the organization needs capabilities such as:\n"
            "\n"
            "- explainability,\n"
            "- feature management,\n"
            "- model-quality tracking,\n"
            "- richer lifecycle management,\n"
            "- more comprehensive enterprise ML operations.\n"
            "\n"
            "The design rule is:\n"
            "\n"
            "> **Do not add platform weight only because it exists; add it when the application's operational needs justify it.**\n"
            "\n"
            "[[IMAGE_NEEDED: Light versus heavy GCP MLOps | "
            "A lightweight path with App Engine/Cloud Build/API call beside a broader Vertex AI path with data/model management, Feature Store, explainability, and quality tracking | "
            "Learner should notice the trade-off between simplicity and platform capability]]\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Managed MLOps platforms offer more than access to GPUs\n"
            "\n"
            "The chapter's conclusion challenges a common misunderstanding: owning powerful hardware is not the same as owning a mature MLOps platform.\n"
            "\n"
            "A platform includes coordinated services for:\n"
            "\n"
            "- data and model management,\n"
            "- training workflows,\n"
            "- deployment,\n"
            "- endpoints,\n"
            "- monitoring,\n"
            "- explainability,\n"
            "- automation.\n"
            "\n"
            "The source uses **comparative advantage** to argue that organizations should avoid rebuilding an inferior version of a capability that a mature managed service can provide at reasonable cost.\n"
            "\n"
            "The decision is still contextual, but the cost comparison must include engineering effort and time, not only hardware ownership.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. A final GCP project should prove that you can operate ML, not just train it\n"
            "\n"
            "The chapter recommends a realistic cloud-native project.\n"
            "\n"
            "Suggested requirements include:\n"
            "\n"
            "- source code stored in GitHub,\n"
            "- continuous deployment,\n"
            "- data stored in GCP,\n"
            "- ML predictions created and served,\n"
            "- cloud-native monitoring,\n"
            "- HTTP REST API with JSON payloads,\n"
            "- deployment through Cloud Build.\n"
            "\n"
            "The important learning goal is end-to-end operation.\n"
            "\n"
            "A notebook with a good model is not the final deliverable.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Evaluate the project like a production system\n"
            "\n"
            "The source proposes checklist questions such as:\n"
            "\n"
            "- Does the application actually perform ML inference?\n"
            "- Are development and production environments separated?\n"
            "- Are monitoring and alerts comprehensive?\n"
            "- Is the right datastore being used?\n"
            "- Is access restricted appropriately?\n"
            "- Is data encrypted in transit?\n"
            "\n"
            "These questions force the project beyond model accuracy into operational readiness.\n"
            "\n"
            "{{exercise:M15.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Put the chapter together as one GCP MLOps system\n"
            "\n"
            "The chapter's parts can be combined into a single mental model:\n"
            "\n"
            "```text\n"
            "Source control\n"
            "   ↓\n"
            "GitHub Actions / Cloud Build\n"
            "   ↓\n"
            "Data layer\n"
            "Cloud Storage / BigQuery / DataOps\n"
            "   ↓\n"
            "Modeling layer\n"
            "BigQuery ML / managed AI / Vertex AI\n"
            "   ↓\n"
            "Packaging / serving\n"
            "Cloud Functions / App Engine / Cloud Run / GKE\n"
            "   ↓\n"
            "Monitoring + quality + explainability\n"
            "   ↓\n"
            "Feedback and iteration\n"
            "```\n"
            "\n"
            "Not every project needs every box.\n"
            "\n"
            "The chapter repeatedly encourages starting with the simplest architecture that creates value and adding complexity only when the operational problem requires it.\n"
            "\n"
            "[[IMAGE_NEEDED: End-to-end GCP MLOps system | "
            "A flow from source and CI/CD through storage/BigQuery, modeling/Vertex AI, deployment targets, monitoring, and feedback | "
            "Learner should notice that individual GCP services fit into a broader lifecycle rather than being isolated tools]]\n"
            "\n"
            "{{exercise:M15.L01.EX06}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: The most powerful VM is always the best ML compute choice\n"
            "\n"
            "Compute should match the workload; expensive accelerators are wasteful when the workload cannot use them effectively.\n"
            "\n"
            "### Misconception 2: Cheap interruptible compute is appropriate for every workload\n"
            "\n"
            "The workload must tolerate interruption and be designed to recover or restart.\n"
            "\n"
            "### Misconception 3: GKE and Cloud Run are interchangeable in operational responsibility\n"
            "\n"
            "Both run containers, but Cloud Run abstracts more of the infrastructure while GKE exposes Kubernetes capabilities.\n"
            "\n"
            "### Misconception 4: CI is separate from MLOps\n"
            "\n"
            "The source treats testing and continuous integration as foundational, nonoptional parts of production ML engineering.\n"
            "\n"
            "### Misconception 5: One CI/CD tool must perform every automation task\n"
            "\n"
            "The source explicitly suggests GitHub Actions for developer feedback and Cloud Build for cloud deployment.\n"
            "\n"
            "### Misconception 6: Kubernetes should be learned by starting immediately with a complex ML model\n"
            "\n"
            "The chapter deliberately begins with a small Flask service so container/orchestration problems can be learned independently.\n"
            "\n"
            "### Misconception 7: BigQuery is only a traditional SQL database\n"
            "\n"
            "The chapter emphasizes serverless analytics, large public datasets, and inline ML capabilities.\n"
            "\n"
            "### Misconception 8: Serverless functions are only for toy applications\n"
            "\n"
            "The source uses them as event-driven DataOps/ML building blocks and recommends them for fast initial workflows.\n"
            "\n"
            "### Misconception 9: Every GCP ML project needs the full Vertex AI platform\n"
            "\n"
            "The chapter explicitly distinguishes light and heavy workflows.\n"
            "\n"
            "### Misconception 10: Owning GPUs means an organization has built an MLOps platform\n"
            "\n"
            "Hardware is only one component; mature platforms coordinate data, models, deployment, monitoring, and lifecycle automation.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Compute Engine | GCP virtual-machine service used to run workloads with different resource profiles. |\n"
            "| Preemptible VM | Lower-cost interruptible VM type discussed by the source for suitable batch workloads. |\n"
            "| GKE | Google Kubernetes Engine, GCP's managed Kubernetes service. |\n"
            "| Cloud Run | High-level managed service for containerized applications. |\n"
            "| App Engine | Fully managed application platform used in the source's deployment examples. |\n"
            "| Cloud Functions | GCP functions-as-a-service offering used for event-driven workflows. |\n"
            "| Cloud Storage | Object-storage service positioned as a data-lake foundation in the source. |\n"
            "| BigQuery | Serverless analytics/warehouse platform with SQL and ML capabilities. |\n"
            "| Vertex AI | Comprehensive GCP platform combining multiple ML lifecycle and MLOps capabilities. |\n"
            "| Cloud Build | GCP-native build/deployment automation service. |\n"
            "| Horizontal Pod Autoscaler | Kubernetes controller that adjusts pod count from CPU, memory, or custom metrics. |\n"
            "| Pod | Kubernetes execution unit that can contain one or more containers. |\n"
            "| Deployment | Kubernetes resource used to manage replicated application pods. |\n"
            "| Service | Kubernetes abstraction used to expose/access an application, including load-balanced access. |\n"
            "| DataOps | Operational discipline for making data movement, transformation, and availability reliable and automated. |\n"
            "| Managed AI API | Cloud API exposing a pretrained AI capability such as translation. |\n"
            "| Feature Store | Managed capability for reusable model features, highlighted as part of broader Vertex AI MLOps. |\n"
            "| Explainable AI | Platform capability for inspecting/explaining model behavior. |\n"
            "| Light MLOps | Source's simpler deployment pattern using a small number of managed services. |\n"
            "| Heavy MLOps | Broader platform pattern using comprehensive lifecycle capabilities where organizational needs justify them. |\n"
            "| Comparative advantage | Reasoning about whether internal engineering time is better spent building a capability or using an existing service. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Which GCP technologies does the chapter identify as influential beyond Google Cloud itself?\n"
            "2. What are the four broad GCP service categories used by the source?\n"
            "3. Why must Compute Engine instance choice match the workload?\n"
            "4. Why can an accelerator-optimized VM be wasteful for some ML tasks?\n"
            "5. When can preemptible compute be useful?\n"
            "6. What workload property makes interruptible compute risky?\n"
            "7. What is the main operational difference between GKE and Cloud Run in the chapter's framing?\n"
            "8. How can App Engine participate in continuous delivery?\n"
            "9. Why are Cloud Functions useful for event-driven architecture?\n"
            "10. How does Cloud Storage support a data-lake-style ML workflow?\n"
            "11. Why does the source consider BigQuery an important starting point for MLOps?\n"
            "12. What seven lifecycle capabilities does the source list for Vertex AI?\n"
            "13. Why is CI described as nonoptional?\n"
            "14. What steps appear in the source's Cloud Build example?\n"
            "15. What developer-feedback tasks does the GitHub Actions example perform?\n"
            "16. Why might one project use both GitHub Actions and Cloud Build?\n"
            "17. Which Kubernetes capabilities make it useful for MLOps?\n"
            "18. What is the relationship between a cluster, node, pod, and container?\n"
            "19. What does the Horizontal Pod Autoscaler do?\n"
            "20. Which metrics can drive HPA in the source?\n"
            "21. Why does the Kubernetes tutorial use a simple Flask application?\n"
            "22. What role does the Dockerfile play before Kubernetes deployment?\n"
            "23. Why can official/certified base images improve engineering reuse?\n"
            "24. What does the local Docker → local Kubernetes progression help isolate?\n"
            "25. How does the Kubernetes YAML expose and replicate the Flask service?\n"
            "26. How can BigQuery reduce data movement in analytics-heavy ML projects?\n"
            "27. What is DataOps in the context of this chapter?\n"
            "28. Why does the source recommend serverless functions for initial data-engineering workflows?\n"
            "29. Which three invocation styles are shown for the simple Cloud Function?\n"
            "30. How can a Cloud Function compose an external data source with an AI API?\n"
            "31. Which advanced MLOps capabilities does the chapter highlight in Vertex AI?\n"
            "32. Why might a larger organization start with Vertex AI rather than assembling everything independently?\n"
            "33. What is the advantage of testing a model locally before hosting it behind an endpoint?\n"
            "34. Which files form the simple App Engine light-MLOps workflow?\n"
            "35. Why is the light workflow attractive?\n"
            "36. When can a heavier Vertex AI workflow be justified?\n"
            "37. Why is owning many GPUs not equivalent to owning an MLOps platform?\n"
            "38. How does comparative advantage affect cloud-platform decisions?\n"
            "39. Which requirements does the source recommend for a final GCP portfolio project?\n"
            "40. Why should development and production environments be separate?\n"
            "41. Why are monitoring and alerts part of the project checklist?\n"
            "42. Why does least privilege matter in the final project?\n"
            "43. Why should data be encrypted in transit?\n"
            "44. What does an end-to-end GCP MLOps loop look like?\n"
            "45. Why should not every project automatically include every GCP service discussed in the chapter?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**GCP MLOps is strongest when you match the tool to the scale of the problem: use simple serverless or managed services for fast value, "
            "containers and Kubernetes when orchestration matters, BigQuery when data and analytics are central, and Vertex AI when the organization needs "
            "a comprehensive lifecycle platform. CI/CD, monitoring, data operations, security, and feedback remain essential whichever path you choose.**\n"
        ),

        "estimated_minutes": 360,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "gcp-framing", "title": "GCP combines cloud infrastructure with influential ML and distributed-systems technology", "order": 1},
            {"id": "gcp-service-categories", "title": "Organize GCP into four broad service categories", "order": 2},
            {"id": "compute-engine", "title": "Match Compute Engine machines to the actual workload", "order": 3},
            {"id": "preemptible", "title": "Interruptible compute can reduce batch cost when the workload tolerates it", "order": 4},
            {"id": "gke-cloud-run", "title": "GKE and Cloud Run expose containers at different abstraction levels", "order": 5},
            {"id": "app-engine-functions", "title": "App Engine and Cloud Functions provide higher-level application patterns", "order": 6},
            {"id": "cloud-storage", "title": "Cloud Storage can act as the data-lake foundation", "order": 7},
            {"id": "bigquery-center", "title": "BigQuery combines analytics, serverless querying, and ML capabilities", "order": 8},
            {"id": "vertex-seven", "title": "Vertex AI organizes the model lifecycle into managed capabilities", "order": 9},
            {"id": "ci-foundation", "title": "Continuous integration is foundational, not optional", "order": 10},
            {"id": "cloud-build", "title": "Cloud Build expresses install, lint, build, and deploy steps", "order": 11},
            {"id": "github-actions-cloud-build", "title": "Use each CI/CD system where its experience is strongest", "order": 12},
            {"id": "kubernetes-why", "title": "Kubernetes is a portable orchestration foundation for ML-powered APIs", "order": 13},
            {"id": "kubernetes-basics", "title": "Understand the Kubernetes deployment hierarchy", "order": 14},
            {"id": "hpa", "title": "Horizontal Pod Autoscaler closes the loop between metrics and capacity", "order": 15},
            {"id": "kube-hello", "title": "Start Kubernetes learning with a small containerized service", "order": 16},
            {"id": "certified-containers", "title": "Base your container on trusted existing images when appropriate", "order": 17},
            {"id": "local-kubernetes", "title": "Move from local Docker to local Kubernetes before cloud Kubernetes", "order": 18},
            {"id": "bigquery-ml", "title": "BigQuery can keep model creation close to large datasets", "order": 19},
            {"id": "dataops", "title": "DataOps is the operational foundation feeding ML systems", "order": 20},
            {"id": "cloud-function-basic", "title": "Cloud Functions are a fast way to prototype event-driven workflows", "order": 21},
            {"id": "function-ai-api", "title": "A serverless function can compose external data and managed AI services", "order": 22},
            {"id": "vertex-components", "title": "Vertex AI brings advanced MLOps capabilities into one platform", "order": 23},
            {"id": "prediction-service", "title": "Operationalizing a model can start with local prediction, then move to an endpoint", "order": 24},
            {"id": "light-mlops", "title": "A light MLOps workflow favors speed and simplicity", "order": 25},
            {"id": "heavy-mlops", "title": "A heavy MLOps workflow adds platform capabilities when the problem requires them", "order": 26},
            {"id": "comparative-advantage", "title": "Managed MLOps platforms offer more than access to GPUs", "order": 27},
            {"id": "portfolio-project", "title": "A final GCP project should prove that you can operate ML, not just train it", "order": 28},
            {"id": "project-checklist", "title": "Evaluate the project like a production system", "order": 29},
            {"id": "chapter-system", "title": "Put the chapter together as one GCP MLOps system", "order": 30},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M15.L01.EX01",
            "title": "Choose compute for three ML workloads",
            "lesson_code": "M15.L01",
            "section_id": "preemptible",
            "placement": "after_section",
            "description": (
                "Practice selecting GCP compute based on workload characteristics and cost."
            ),
            "instructions": (
                "Choose a source-aligned compute strategy for each workload:\n\n"
                "1. GPU-friendly deep-learning training that benefits from massive parallelism.\n"
                "2. A memory-heavy transformation job with little GPU benefit.\n"
                "3. A restartable overnight batch job that can tolerate interruption.\n\n"
                "For each case, explain the machine characteristic that matters and one cost mistake you want to avoid."
            ),
            "expected_output": (
                "Three workload-to-compute mappings with cost and utilization reasoning."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "compute-engine",
                "cost-awareness",
                "preemptible-compute",
                "workload-matching",
            ],
        },

        {
            "id": "M15.L01.EX02",
            "title": "Split CI and deployment responsibilities",
            "lesson_code": "M15.L01",
            "section_id": "github-actions-cloud-build",
            "placement": "after_section",
            "description": (
                "Design a two-system CI/CD workflow using the chapter's suggested strengths."
            ),
            "instructions": (
                "A Python ML API is stored in GitHub and deployed to GCP.\n\n"
                "Assign each task to GitHub Actions, Cloud Build, or both:\n"
                "1. install dependencies,\n"
                "2. lint,\n"
                "3. unit tests,\n"
                "4. formatting check,\n"
                "5. deploy App Engine/another GCP target,\n"
                "6. block deployment when tests fail.\n\n"
                "Then explain why using two automation systems can be better than forcing one tool to do everything."
            ),
            "expected_output": (
                "A CI/CD responsibility map with developer-feedback and cloud-deployment stages."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "continuous-integration",
                "github-actions",
                "cloud-build",
                "continuous-delivery",
            ],
        },

        {
            "id": "M15.L01.EX03",
            "title": "Move a Flask service from Docker to Kubernetes",
            "lesson_code": "M15.L01",
            "section_id": "local-kubernetes",
            "placement": "after_section",
            "description": (
                "Practice the staged deployment path used by the chapter."
            ),
            "instructions": (
                "You have a tested Flask prediction API.\n\n"
                "Describe the steps to:\n"
                "1. create a Dockerfile from a suitable base image,\n"
                "2. build and run the image locally,\n"
                "3. invoke it with curl,\n"
                "4. define a Kubernetes Deployment with three replicas,\n"
                "5. define a load-balanced Service,\n"
                "6. apply the YAML locally,\n"
                "7. inspect pods and service details,\n"
                "8. later move the same container pattern toward GKE.\n\n"
                "Explain what failure each stage helps isolate."
            ),
            "expected_output": (
                "A staged container-to-Kubernetes deployment plan with diagnostic reasoning."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "docker",
                "kubernetes",
                "gke",
                "deployment-debugging",
            ],
        },

        {
            "id": "M15.L01.EX04",
            "title": "Design a serverless DataOps function",
            "lesson_code": "M15.L01",
            "section_id": "function-ai-api",
            "placement": "after_section",
            "description": (
                "Use Cloud Functions as a lightweight composition layer for data and AI services."
            ),
            "instructions": (
                "Design a Cloud Function that receives JSON describing a document, retrieves or reads the relevant text, "
                "calls a managed language API, and returns the result.\n\n"
                "Specify:\n"
                "1. expected JSON fields,\n"
                "2. validation behavior,\n"
                "3. external/cloud data dependency,\n"
                "4. AI API call,\n"
                "5. returned payload,\n"
                "6. how you would invoke it from `gcloud`, curl, or a CLI,\n"
                "7. when you would replace this simple serverless design with a larger pipeline."
            ),
            "expected_output": (
                "A source-aligned event-driven ML/DataOps micro-workflow."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "cloud-functions",
                "dataops",
                "managed-ai-api",
                "serverless",
            ],
        },

        {
            "id": "M15.L01.EX05",
            "title": "Choose light or heavy MLOps",
            "lesson_code": "M15.L01",
            "section_id": "project-checklist",
            "placement": "after_section",
            "description": (
                "Choose platform complexity based on operational requirements."
            ),
            "instructions": (
                "Compare two projects:\n\n"
                "Project A: a three-person team wants to expose one prediction capability quickly with basic monitoring.\n"
                "Project B: a large company needs shared features, model lifecycle management, explainability, quality tracking, and multiple production endpoints.\n\n"
                "For each project:\n"
                "1. choose a light or heavy MLOps approach,\n"
                "2. name source-supported GCP services/patterns,\n"
                "3. explain which complexity is justified,\n"
                "4. identify one reason not to choose the opposite approach."
            ),
            "expected_output": (
                "Two context-sensitive architectures demonstrating the light-versus-heavy decision."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vertex-ai",
                "light-mlops",
                "heavy-mlops",
                "architecture-selection",
            ],
        },

        {
            "id": "M15.L01.EX06",
            "title": "Design the chapter's final cloud-native ML project",
            "lesson_code": "M15.L01",
            "section_id": "chapter-system",
            "placement": "after_section",
            "description": (
                "Integrate the whole chapter into a portfolio-quality MLOps architecture."
            ),
            "instructions": (
                "Design a cloud-native classification application on GCP.\n\n"
                "Your design must include:\n"
                "1. GitHub source control,\n"
                "2. CI checks,\n"
                "3. automated GCP deployment,\n"
                "4. data stored in Cloud Storage or BigQuery,\n"
                "5. an ML training/prediction path,\n"
                "6. a REST/JSON serving layer,\n"
                "7. separate development and production environments,\n"
                "8. monitoring and alerts,\n"
                "9. least-privilege access,\n"
                "10. encryption in transit,\n"
                "11. one argument for choosing either a light workflow or Vertex AI.\n\n"
                "Explain how the architecture would evolve if usage and organizational complexity increased."
            ),
            "expected_output": (
                "An end-to-end GCP MLOps project architecture grounded in the source chapter."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "gcp-architecture",
                "mlops",
                "ci-cd",
                "monitoring",
                "security",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M15.L01.QZ01",

        "title": "MLOps for GCP — Knowledge Check",

        "lesson_code": "M15.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M15.L01.Q01",
                "section_id": "gcp-framing",
                "question": "Which technologies does the source highlight as examples of Google's influential engineering ecosystem?",
                "options": [
                    "Kubernetes, Go, and TensorFlow",
                    "Only Flask and Pandas",
                    "Only Azure ML and SageMaker",
                    "Hadoop, Ruby, and SQLite only",
                ],
                "correct": 0,
                "explanation": (
                    "The source specifically names Kubernetes, Go, and TensorFlow."
                ),
            },

            {
                "id": "M15.L01.Q02",
                "section_id": "gcp-service-categories",
                "question": "Which four categories organize the chapter's core GCP services?",
                "options": [
                    "Compute, Storage, Big Data, and Machine Learning",
                    "Frontend, Backend, Mobile, and Desktop",
                    "Training, Hiring, Marketing, and Sales",
                    "CPU, GPU, TPU, and RAM",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly introduces GCP using these four categories."
                ),
            },

            {
                "id": "M15.L01.Q03",
                "section_id": "compute-engine",
                "question": "Why is choosing the correct Compute Engine machine type important?",
                "options": [
                    "Workloads benefit from different resource profiles, and mismatched expensive hardware can waste money.",
                    "Every workload uses GPUs equally well.",
                    "Machine type has no cost effect.",
                    "General-purpose machines cannot run ML.",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes workload fit and cost forecasting."
                ),
            },

            {
                "id": "M15.L01.Q04",
                "section_id": "preemptible",
                "question": "When is lower-cost interruptible compute most appropriate?",
                "options": [
                    "For workloads such as batch jobs that can tolerate interruption or restart.",
                    "For every latency-critical production request.",
                    "Only for databases that cannot restart.",
                    "Only when no checkpointing is possible.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents preemptible compute as useful for suitable batch workloads."
                ),
            },

            {
                "id": "M15.L01.Q05",
                "section_id": "gke-cloud-run",
                "question": "How does the chapter position Cloud Run relative to GKE?",
                "options": [
                    "Cloud Run is a higher-level container service that abstracts more infrastructure complexity.",
                    "Cloud Run is a Kubernetes control plane only.",
                    "GKE cannot run containers.",
                    "They are described as identical.",
                ],
                "correct": 0,
                "explanation": (
                    "The source calls Cloud Run a good starting point for simpler container deployment."
                ),
            },

            {
                "id": "M15.L01.Q06",
                "section_id": "app-engine-functions",
                "question": "What deployment pattern is associated with Cloud Functions?",
                "options": [
                    "Event-driven functions as a service",
                    "Only long-running virtual machines",
                    "Only SQL queries",
                    "Only Kubernetes pods",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly describes Cloud Functions as a FaaS option for event-driven architecture."
                ),
            },

            {
                "id": "M15.L01.Q07",
                "section_id": "bigquery-center",
                "question": "Why does the source consider BigQuery a strong MLOps starting point?",
                "options": [
                    "It combines serverless SQL analytics, public datasets, and ML capabilities close to the data.",
                    "It is only a static-file host.",
                    "It replaces all container platforms.",
                    "It cannot work with large datasets.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter emphasizes BigQuery's broad analytics-to-ML value chain."
                ),
            },

            {
                "id": "M15.L01.Q08",
                "section_id": "vertex-seven",
                "question": "Which is one capability listed in the source's Vertex AI workflow?",
                "options": [
                    "Traffic splitting for prediction endpoints",
                    "Only DNS registration",
                    "Only notebook rendering",
                    "Replacing source control",
                ],
                "correct": 0,
                "explanation": (
                    "Traffic splitting is one of the seven high-level capabilities listed."
                ),
            },

            {
                "id": "M15.L01.Q09",
                "section_id": "ci-foundation",
                "question": "How does the chapter characterize continuous integration?",
                "options": [
                    "A foundational component of DevOps and MLOps that is often neglected.",
                    "Optional after deployment.",
                    "Only useful for frontend applications.",
                    "Unrelated to testing.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly calls testing and CI fundamental."
                ),
            },

            {
                "id": "M15.L01.Q10",
                "section_id": "cloud-build",
                "question": "What can Cloud Build automate in the source example?",
                "options": [
                    "Dependency installation, linting, and application deployment",
                    "Only model labeling",
                    "Only database backups",
                    "Only browser testing",
                ],
                "correct": 0,
                "explanation": (
                    "The source's configuration includes install, lint, and deploy steps."
                ),
            },

            {
                "id": "M15.L01.Q11",
                "section_id": "github-actions-cloud-build",
                "question": "What hybrid CI/CD strategy does the source suggest?",
                "options": [
                    "GitHub Actions for developer feedback and Cloud Build for GCP deployment.",
                    "Cloud Build for local text editing only.",
                    "GitHub Actions only for production monitoring.",
                    "Use no CI if Cloud Build exists.",
                ],
                "correct": 0,
                "explanation": (
                    "The source separates developer experience from cloud deployment strengths."
                ),
            },

            {
                "id": "M15.L01.Q12",
                "section_id": "kubernetes-why",
                "question": "Which is a Kubernetes capability highlighted by the source?",
                "options": [
                    "Autoscaling",
                    "Service discovery",
                    "Container health management",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "All three appear in the chapter's Kubernetes capability list."
                ),
            },

            {
                "id": "M15.L01.Q13",
                "section_id": "kubernetes-basics",
                "question": "What contains one or more containers in the chapter's Kubernetes hierarchy?",
                "options": [
                    "A pod",
                    "A SQL table",
                    "A Cloud Function",
                    "A model registry only",
                ],
                "correct": 0,
                "explanation": (
                    "The source describes containers running inside pods on worker nodes."
                ),
            },

            {
                "id": "M15.L01.Q14",
                "section_id": "hpa",
                "question": "What does the Horizontal Pod Autoscaler do?",
                "options": [
                    "Adjusts pod replicas using observed resource/custom metrics.",
                    "Stores container images.",
                    "Versions datasets.",
                    "Trains BigQuery models.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents HPA as a metrics-driven scaling control loop."
                ),
            },

            {
                "id": "M15.L01.Q15",
                "section_id": "kube-hello",
                "question": "Why does the chapter test the Flask service in Docker before Kubernetes?",
                "options": [
                    "To isolate application/container problems before adding orchestration complexity.",
                    "Because Kubernetes cannot run Flask.",
                    "Because Docker guarantees autoscaling.",
                    "Because local tests are unrelated to deployment.",
                ],
                "correct": 0,
                "explanation": (
                    "The staged workflow makes debugging easier."
                ),
            },

            {
                "id": "M15.L01.Q16",
                "section_id": "certified-containers",
                "question": "What does the Docker `FROM` pattern illustrate?",
                "options": [
                    "Reusing an existing base image as the foundation for your own container.",
                    "Creating a dataset version.",
                    "Deploying a Cloud Function.",
                    "Training in BigQuery.",
                ],
                "correct": 0,
                "explanation": (
                    "The source discusses official Python base images as reusable foundations."
                ),
            },

            {
                "id": "M15.L01.Q17",
                "section_id": "local-kubernetes",
                "question": "What does the Kubernetes YAML in the source configure?",
                "options": [
                    "A load-balanced service and a replicated deployment.",
                    "Only one local Python function.",
                    "A BigQuery dataset.",
                    "A Vertex AI feature store.",
                ],
                "correct": 0,
                "explanation": (
                    "The example declares a Service and a Deployment with multiple replicas."
                ),
            },

            {
                "id": "M15.L01.Q18",
                "section_id": "bigquery-ml",
                "question": "What is one MLOps benefit of doing ML inside BigQuery?",
                "options": [
                    "It can keep model-related work close to large analytics data and reduce unnecessary movement.",
                    "It removes the need for data.",
                    "It only works for static websites.",
                    "It prevents BI integration.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents BigQuery as the center of an analytics/ML workflow."
                ),
            },

            {
                "id": "M15.L01.Q19",
                "section_id": "dataops",
                "question": "Why is DataOps important to MLOps?",
                "options": [
                    "ML systems depend on reliable, automated data flow and transformation.",
                    "Models never require data pipelines.",
                    "DataOps only concerns frontend design.",
                    "It replaces model evaluation.",
                ],
                "correct": 0,
                "explanation": (
                    "The source describes data as the necessary input for ML at scale."
                ),
            },

            {
                "id": "M15.L01.Q20",
                "section_id": "cloud-function-basic",
                "question": "Why does the source recommend Cloud Functions for an initial data-engineering workflow?",
                "options": [
                    "They provide a quick, serverless way to prototype before adopting more complex tools if needed.",
                    "They are always the only correct production choice.",
                    "They eliminate APIs.",
                    "They cannot process JSON.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly recommends starting simple with serverless technology."
                ),
            },

            {
                "id": "M15.L01.Q21",
                "section_id": "function-ai-api",
                "question": "What does the translation-function example demonstrate?",
                "options": [
                    "A Cloud Function can compose request handling, external content, and a managed AI API.",
                    "Cloud Functions cannot use third-party libraries.",
                    "Managed AI APIs require Kubernetes.",
                    "Functions cannot return text.",
                ],
                "correct": 0,
                "explanation": (
                    "The source's function combines Wikipedia retrieval and translation."
                ),
            },

            {
                "id": "M15.L01.Q22",
                "section_id": "vertex-components",
                "question": "Which advanced capabilities does the source associate with Vertex AI?",
                "options": [
                    "Feature Store, Explainable AI, and model-quality tracking",
                    "Only DNS and static websites",
                    "Only virtual machines",
                    "Only source control",
                ],
                "correct": 0,
                "explanation": (
                    "These are explicitly named as valuable components of a comprehensive MLOps solution."
                ),
            },

            {
                "id": "M15.L01.Q23",
                "section_id": "prediction-service",
                "question": "Why test a model locally before creating a cloud endpoint?",
                "options": [
                    "To verify model/input behavior before adding hosting and network complexity.",
                    "Because cloud endpoints cannot be tested.",
                    "Because local prediction is always production.",
                    "To avoid model validation.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents local prediction as a useful earlier step."
                ),
            },

            {
                "id": "M15.L01.Q24",
                "section_id": "light-mlops",
                "question": "What characterizes the chapter's light MLOps workflow?",
                "options": [
                    "A small managed application/deployment stack that can call an AI or prediction endpoint.",
                    "Every possible Vertex AI feature.",
                    "Custom-built cluster management.",
                    "No automation.",
                ],
                "correct": 0,
                "explanation": (
                    "The App Engine/Cloud Build example is intentionally simple."
                ),
            },

            {
                "id": "M15.L01.Q25",
                "section_id": "heavy-mlops",
                "question": "When is a heavier Vertex AI workflow more justified?",
                "options": [
                    "When the project needs richer capabilities such as explainability, feature management, quality tracking, and lifecycle management.",
                    "For every hello-world project.",
                    "Only when no data exists.",
                    "Only for static sites.",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts platform capability with lightweight simplicity."
                ),
            },

            {
                "id": "M15.L01.Q26",
                "section_id": "comparative-advantage",
                "question": "Why does the source argue that owning GPUs does not equal owning an MLOps platform?",
                "options": [
                    "A platform coordinates many lifecycle services beyond raw compute hardware.",
                    "GPUs cannot train models.",
                    "Cloud platforms contain no hardware.",
                    "MLOps never uses compute.",
                ],
                "correct": 0,
                "explanation": (
                    "The conclusion emphasizes integrated platform capabilities rather than hardware alone."
                ),
            },

            {
                "id": "M15.L01.Q27",
                "section_id": "portfolio-project",
                "question": "Which requirement belongs in the source's suggested final GCP project?",
                "options": [
                    "Cloud-native monitoring",
                    "Source control",
                    "ML inference/serving",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The project is intended to demonstrate end-to-end ML engineering."
                ),
            },

            {
                "id": "M15.L01.Q28",
                "section_id": "project-checklist",
                "question": "Which security concern appears in the final project checklist?",
                "options": [
                    "Use appropriately restricted access and encrypt data in transit.",
                    "Disable authentication everywhere.",
                    "Share one admin account.",
                    "Store secrets in public source files.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly includes least-security/least-privilege style access and encryption in transit."
                ),
            },

            {
                "id": "M15.L01.Q29",
                "section_id": "chapter-system",
                "question": "What is the best summary of the chapter's architecture philosophy?",
                "options": [
                    "Start with the simplest GCP services that solve the problem, then add platform complexity when operational needs justify it.",
                    "Use every GCP product in every project.",
                    "Always start with Kubernetes regardless of need.",
                    "Avoid managed services.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter repeatedly contrasts simple serverless/light workflows with richer platforms such as Vertex AI."
                ),
            },

            {
                "id": "M15.L01.Q30",
                "section_id": "chapter-system",
                "type": "open",
                "question": (
                    "Design a GCP MLOps architecture for a cloud-native prediction product. "
                    "Include source control, CI checks, Cloud Build or another deployment stage, a data layer, "
                    "one model-training/prediction path, a serving target, monitoring, separate development/production environments, "
                    "least-privilege access, and a reasoned choice between a light workflow and Vertex AI. "
                    "Explain how the design could evolve if traffic, team size, and governance needs increase."
                ),
            },
        ],

        "passing_score": 70,
    },
}
